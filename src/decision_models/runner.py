"""Run orchestration, dynamic concurrency, progress display, and summary logging."""

import logging
import os
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from queue import Empty, Queue
from typing import Any, TextIO

from tqdm import tqdm

from .client import Transport, predict
from .config import DEFAULT_CONCURRENCY as DEFAULT_CONCURRENCY
from .config import MAX_CONCURRENCY as MAX_CONCURRENCY
from .config import REQUIRED_FIELDS as REQUIRED_FIELDS
from .config import RunConfig
from .config import _concurrency as _concurrency
from .config import load_config as load_config
from .data import load_dataset
from .results import (
    drop_failed,
    load_recorded_ids,
    locked_output,
    request_sample,
    write_result,
)

logger = logging.getLogger(__name__)


def run(config_path: str | Path, transport: Transport = predict) -> Path | list[Path]:
    """Validate the input and request the unrecorded samples, per data file and per round."""
    path = Path(config_path).resolve()
    logger.info('loading config: %s', path)
    config = load_config(path)
    api_key = os.environ.get('OPENROUTER_API_KEY', '').strip()
    if not api_key:
        raise ValueError('OPENROUTER_API_KEY must be set.')
    datas = [config['data']] if isinstance(config['data'], str) else config['data']
    configured = config['output']
    outputs = [configured] if isinstance(configured, str) else configured
    repeat = config['repeat']
    results: list[Path] = []
    for data_index, data_name in enumerate(datas):
        samples = load_dataset(path.parent / data_name)
        # output paths are expanded by data order then by round, so each data takes a slice
        if len(datas) == 1:
            names = outputs
        else:
            names = outputs[data_index * repeat : (data_index + 1) * repeat]
        if len(datas) > 1:
            logger.info('data %d/%d: %s', data_index + 1, len(datas), data_name)
        for index, name in enumerate(names, start=1):
            if len(names) > 1:
                logger.info('round %d/%d', index, len(names))
            output = (path.parent / name).resolve()
            results.append(_run_once(samples, config, api_key, transport, output))
    return results[0] if isinstance(configured, str) else results


def _run_once(
    samples: list[dict[str, Any]],
    config: RunConfig,
    api_key: str,
    transport: Transport,
    output: Path,
) -> Path:
    """Run one full round against a single result file and return its path."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with locked_output(output):
        pending = _pending_samples(samples, output)
        skipped = len(samples) - len(pending)
        completed, failed = 0, 0
        if pending:
            completed, failed = _process(pending, config, api_key, transport, output)
    logger.info('results: %s', output)
    logger.info('summary: %d completed, %d failed, %d skipped', completed, failed, skipped)
    return output


def _pending_samples(
    samples: list[dict[str, Any]], output: Path
) -> list[dict[str, Any]]:
    """Validate history, drop failed records, and select the samples to request; the caller holds the lock."""
    recorded = load_recorded_ids(output)
    requeued = drop_failed(output)
    if requeued:
        logger.info('retry: dropped %d failed records and requeued them', len(requeued))
    recorded -= requeued
    pending = [sample for sample in samples if sample['id'] not in recorded]
    if recorded:
        logger.info(
            'resume: %d already recorded, %d skipped, %d to request',
            len(recorded),
            len(samples) - len(pending),
            len(pending),
        )
    return pending


def _process(
    samples: list[dict[str, Any]],
    config: RunConfig,
    api_key: str,
    transport: Transport,
    output: Path,
) -> tuple[int, int]:
    """Write results as they finish, adjusting the limit, and stop submitting cleanly on interruption."""
    completed, failed = 0, 0
    ceiling = min(MAX_CONCURRENCY, len(samples))
    limit = min(config['concurrency'], ceiling)
    if not limit:
        return completed, failed
    remaining = iter(samples)
    finished: Queue[Future[dict[str, Any]]] = Queue()
    pending: set[Future[dict[str, Any]]] = set()
    bar = tqdm(total=len(samples), unit='samples', disable=None)

    with output.open('a', encoding='utf-8') as file:
        pool = ThreadPoolExecutor(max_workers=ceiling)
        writable = True
        current: Future[dict[str, Any]] | None = None

        def submit_next() -> bool:
            """Submit one more sample and register its completion; return False once samples run out."""
            sample = next(remaining, None)
            if sample is None:
                return False
            future = pool.submit(
                _request,
                sample,
                config,
                api_key,
                transport,
            )
            pending.add(future)
            future.add_done_callback(finished.put)
            return True

        def refill() -> None:
            """Top up the in-flight requests to the current concurrency limit."""
            while len(pending) < limit and submit_next():
                pass

        try:
            refill()
            while pending:
                current = finished.get()
                result = current.result()
                writable = False
                success = _save_result(file, result)
                pending.remove(current)
                current = None
                writable = True
                completed += int(success)
                failed += int(not success)
                limit = _adjust_limit(limit, ceiling, success)
                _report_progress(bar, result, failed, limit)
                refill()
        except BaseException:
            logger.warning('run interrupted: stopping submissions and waiting for in-flight requests')
            for future in pending:
                future.cancel()
            pool.shutdown(wait=True, cancel_futures=True)
            if writable:
                _save_finished(file, finished, pending, current)
            else:
                logger.error('result write unfinished: stopping appends to keep the file tail resumable')
            raise
        finally:
            pool.shutdown(wait=True, cancel_futures=True)
            bar.close()
    return completed, failed


def _report_progress(
    bar: tqdm, result: dict[str, Any], failed: int, limit: int
) -> None:
    """Log one sample according to the bar's display mode, then update progress and stats."""
    error = result['error']
    if error is None:
        if bar.disable:
            logger.info('%s: completed', result['id'])
    else:
        logger.warning(
            '%s: failed, type=%s, HTTP status=%s',
            result['id'],
            error['type'],
            error.get('status', '-'),
        )
    bar.update(1)
    bar.set_postfix({'failed': failed, 'concurrency': limit})


def _adjust_limit(limit: int, ceiling: int, success: bool) -> int:
    """Adjust the limit by AIMD: one more on success, halved on failure, kept between 1 and ceiling."""
    if success:
        return min(ceiling, limit + 1)
    return max(1, limit // 2)


def _save_result(file: TextIO, result: dict[str, Any]) -> bool:
    """Persist one result and return whether it succeeded; the caller updates progress and logs."""
    write_result(file, result)
    return result['error'] is None


def _save_finished(
    file: TextIO,
    finished: Queue[Future[dict[str, Any]]],
    pending: set[Future[dict[str, Any]]],
    current: Future[dict[str, Any]] | None = None,
) -> None:
    """Save the remaining results once the pool stops, without masking the original exception."""
    while pending:
        if current is not None:
            future, current = current, None
        else:
            try:
                future = finished.get_nowait()
            except Empty:
                # The interrupt can land between dequeuing a completion and assigning it.
                future = next(iter(pending))
        if future not in pending:
            continue
        pending.remove(future)
        if future.cancelled():
            continue
        if future.exception() is not None:
            logger.error('an in-flight request exited with an exception and produced no recordable result')
            continue
        try:
            _save_result(file, future.result())
        except Exception:
            logger.exception('failed to save the remaining results; stopping appends')
            break


def _request(
    sample: dict[str, Any],
    config: RunConfig,
    api_key: str,
    transport: Transport,
) -> dict[str, Any]:
    """Build one single-turn request; workers only request and never touch the result file."""
    payload = {'model': config['model'], **sample['input']}
    return request_sample(
        sample['id'],
        payload,
        api_key,
        config['endpoint'],
        transport,
    )
