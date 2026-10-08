"""End-to-end tests of a single-turn run driven by simulated requests."""

import copy
import json
import os
import random
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from queue import Queue
from unittest.mock import Mock, patch

import yaml
from jsonschema import Draft202012Validator

from decision_models.results import locked_output
from decision_models.runner import _adjust_limit, run

ROOT = Path(__file__).resolve().parents[1]


class SingleTurnTests(unittest.TestCase):
    """Verify the final data and the single result file using simulated requests only."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.config = self.root / 'config.yaml'
        self.config.write_text(
            yaml.safe_dump(
                {
                    'model': 'test-model',
                    'endpoint': 'https://example.test/decisions',
                    'data': 'data.json',
                    'output': 'results.jsonl',
                }
            ),
            encoding='utf-8',
        )
        self.sample = {
            'id': 'T01',
            'input': {
                'state': {'task': 'test'},
                'questions': {
                    'action': {
                        'type': 'choice',
                        'instructions': 'choose an action',
                        'criteria': {'a': 'action A', 'b': 'action B'},
                    }
                },
            },
            'reference': {'action': {'choice': 'a'}},
        }
        self.response = {
            'answers': {'action': {'choice': 'a'}},
            'usage': {'cost': 0},
            'extra': ['kept in full'],
        }
        self.transport = Mock(return_value=(200, json.dumps(self.response)))
        self.env = patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-only'})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.save([self.sample])

    def save(self, samples):
        """Write the dataset used by one test."""
        (self.root / 'data.json').write_text(
            json.dumps({'schema_version': 1, 'samples': samples}), encoding='utf-8'
        )

    def records(self):
        return [
            json.loads(line)
            for line in (self.root / 'results.jsonl')
            .read_text(encoding='utf-8')
            .splitlines()
        ]

    def output_bytes(self):
        return (self.root / 'results.jsonl').read_bytes()

    def read_records(self, name):
        """Read every record of the named result file."""
        return [
            json.loads(line)
            for line in (self.root / name).read_text(encoding='utf-8').splitlines()
        ]

    def set_concurrency(self, value):
        """Rewrite the concurrency field in the config."""
        config = yaml.safe_load(self.config.read_text(encoding='utf-8'))
        config['concurrency'] = value
        self.config.write_text(yaml.safe_dump(config), encoding='utf-8')

    def set_repeat(self, value):
        """Rewrite the repeat field in the config."""
        config = yaml.safe_load(self.config.read_text(encoding='utf-8'))
        config['repeat'] = value
        self.config.write_text(yaml.safe_dump(config), encoding='utf-8')

    def tracking_transport(self, delay=0.02):
        """Return a briefly blocking transport to observe the peak in-flight request count."""
        state = {'active': 0, 'peak': 0}
        lock = threading.Lock()

        def transport(*_args):
            with lock:
                state['active'] += 1
                state['peak'] = max(state['peak'], state['active'])
            time.sleep(delay)
            with lock:
                state['active'] -= 1
            return 200, json.dumps(self.response)

        return transport, state

    def test_labeled_and_unlabeled_samples_only_create_one_file(self):
        other = copy.deepcopy(self.sample)
        other['id'] = 'T02'
        del other['reference']
        self.save([self.sample, other])
        self.set_concurrency(1)
        before = set(self.root.rglob('*'))
        output = run(self.config, transport=self.transport)
        self.assertEqual(set(self.root.rglob('*')) - before, {output})
        self.assertEqual(self.transport.call_count, 2)
        self.assertEqual(
            self.records(),
            [
                {'id': name, 'response': self.response, 'error': None}
                for name in ['T01', 'T02']
            ],
        )
        for call in self.transport.call_args_list:
            self.assertEqual(
                call.args[0], {'model': 'test-model', **self.sample['input']}
            )
            self.assertNotIn('reference', call.args[0])

    def test_invalid_data_fails_before_requests_and_output(self):
        cases = [
            [self.sample, self.sample],
            [],
            [{**self.sample, 'id': ''}],
            [{**self.sample, 'input': {'state': {}}}],
            [{**self.sample, 'input': {**self.sample['input'], 'model': 'override'}}],
        ]
        for samples in cases:
            with self.subTest(samples=samples):
                self.save(samples)
                with self.assertRaises(ValueError):
                    run(self.config, transport=self.transport)
                self.assertFalse((self.root / 'results.jsonl').exists())
        self.transport.assert_not_called()

    def test_errors_preserve_response_and_continue(self):
        self.save([{**self.sample, 'id': str(i)} for i in range(4)])
        self.set_concurrency(1)
        self.transport.side_effect = [
            OSError('connection failed'),
            (429, '{"error":"rate limited"}'),
            (200, '<html>not JSON</html>'),
            (200, json.dumps(self.response)),
        ]
        run(self.config, transport=self.transport)
        rows = self.records()
        self.assertEqual([row['id'] for row in rows], ['0', '1', '2', '3'])
        self.assertIsNone(rows[0]['response'])
        self.assertEqual(rows[1]['response'], {'error': 'rate limited'})
        self.assertEqual(rows[2]['response'], '<html>not JSON</html>')
        self.assertTrue(all(row['error'] for row in rows[:3]))
        self.assertIsNone(rows[3]['error'])

    def test_existing_result_is_resumed_not_overwritten(self):
        """Recorded samples are not requested again; only missing ones are appended, keeping existing lines byte-identical."""
        self.save([self.sample, {**self.sample, 'id': 'T02'}])
        self.set_concurrency(1)
        first = {'id': 'T01', 'response': self.response, 'error': None}
        output = self.root / 'results.jsonl'
        output.write_text(
            json.dumps(first, ensure_ascii=False) + '\n', encoding='utf-8'
        )
        head = output.read_bytes()
        run(self.config, transport=self.transport)
        self.transport.assert_called_once()
        self.assertEqual(
            self.transport.call_args.args[0],
            {'model': 'test-model', **self.sample['input']},
        )
        self.assertTrue(self.output_bytes().startswith(head))
        self.assertEqual([row['id'] for row in self.records()], ['T01', 'T02'])

    def test_recorded_failures_are_requeued_on_resume(self):
        """Failures from a previous run are dropped and requested again; on success no failed line remains."""
        self.save([self.sample, {**self.sample, 'id': 'T02'}])
        failure = {
            'id': 'T01',
            'response': None,
            'error': {'type': 'network', 'message': 'connection failed'},
        }
        (self.root / 'results.jsonl').write_text(
            json.dumps(failure, ensure_ascii=False) + '\n', encoding='utf-8'
        )
        run(self.config, transport=self.transport)
        self.assertEqual(self.transport.call_count, 2)
        self.assertEqual([row['id'] for row in self.records()], ['T01', 'T02'])
        self.assertTrue(all(row['error'] is None for row in self.records()))

    def test_resume_discards_trailing_fragment(self):
        """The partial trailing line is dropped, its sample requested again, and the file stays a full record stream."""
        self.save([self.sample, {**self.sample, 'id': 'T02'}])
        self.set_concurrency(1)
        first = {'id': 'T01', 'response': self.response, 'error': None}
        output = self.root / 'results.jsonl'
        complete = json.dumps(first, ensure_ascii=False) + '\n'
        output.write_text(complete + '{"id": "T02", "resp', encoding='utf-8')
        run(self.config, transport=self.transport)
        self.transport.assert_called_once()
        self.assertEqual(output.read_text(encoding='utf-8').startswith(complete), True)
        self.assertEqual([row['id'] for row in self.records()], ['T01', 'T02'])

    def test_resume_mixed_history_retries_failures_once_and_keeps_successes(self):
        """Resume repairs the fragment and requeues failed samples, keeping successes without retrying this run's failures."""
        self.save([{**self.sample, 'id': name} for name in ['T01', 'T02', 'T03']])
        self.set_concurrency(1)
        success = {'id': 'T01', 'response': self.response, 'error': None}
        failure = {
            'id': 'T02',
            'response': None,
            'error': {'type': 'network', 'message': 'timeout'},
        }
        prefix = json.dumps(success, ensure_ascii=False) + '\n'
        output = self.root / 'results.jsonl'
        output.write_text(
            prefix + json.dumps(failure) + '\n{"id":"T03","response":',
            encoding='utf-8',
        )
        self.transport.return_value = (503, '{}')
        with self.assertLogs('decision_models', level='INFO') as logs:
            run(self.config, transport=self.transport)
        self.assertEqual(self.transport.call_count, 2)
        self.assertTrue(output.read_bytes().startswith(prefix.encode('utf-8')))
        self.assertEqual([row['id'] for row in self.records()], ['T01', 'T02', 'T03'])
        self.assertTrue(all(row['error'] for row in self.records()[1:]))
        self.assertIn('retry: dropped 1 failed records and requeued them', '\n'.join(logs.output))
        self.assertIn('summary: 0 completed, 2 failed, 1 skipped', '\n'.join(logs.output))

    def test_progress_and_sample_logs_follow_display_mode(self):
        """A running progress bar omits success logs; failure logs and the summary are always printed."""
        for disabled in [False, True]:
            for status in [200, 503]:
                with self.subTest(disabled=disabled, status=status):
                    (self.root / 'results.jsonl').unlink(missing_ok=True)
                    self.transport.return_value = (status, '{}')
                    bar = Mock(disable=disabled)
                    with (
                        patch('decision_models.runner.tqdm', return_value=bar),
                        self.assertLogs('decision_models.runner', level='INFO') as logs,
                    ):
                        run(self.config, transport=self.transport)
                    messages = '\n'.join(logs.output)
                    self.assertEqual('T01: completed' in messages, disabled and status == 200)
                    self.assertEqual('T01: failed' in messages, status == 503)
                    bar.update.assert_called_once_with(1)
                    bar.set_postfix.assert_called_once_with(
                        {'failed': int(status == 503), 'concurrency': 1}
                    )
                    bar.close.assert_called_once()

    def test_resume_with_every_sample_recorded_sends_nothing(self):
        """With every sample already recorded nothing is requested and the file is untouched."""
        self.set_concurrency(1)
        row = {'id': 'T01', 'response': self.response, 'error': None}
        output = self.root / 'results.jsonl'
        output.write_text(json.dumps(row, ensure_ascii=False) + '\n', encoding='utf-8')
        head = output.read_bytes()
        run(self.config, transport=self.transport)
        self.transport.assert_not_called()
        self.assertEqual(output.read_bytes(), head)

    def test_missing_key_creates_no_result(self):
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': ''}):
            with self.assertRaises(ValueError):
                run(self.config, transport=self.transport)
        self.assertFalse((self.root / 'results.jsonl').exists())

    def test_multiple_questions_still_make_one_request(self):
        self.sample['input']['questions']['another'] = self.sample['input'][
            'questions'
        ]['action']
        self.save([self.sample])
        run(self.config, transport=self.transport)
        self.transport.assert_called_once()

    def test_interruption_keeps_completed_lines(self):
        self.save([self.sample, {**self.sample, 'id': 'T02'}])
        self.set_concurrency(1)
        self.transport.side_effect = [(200, '{}'), KeyboardInterrupt()]
        with self.assertRaises(KeyboardInterrupt):
            run(self.config, transport=self.transport)
        self.assertEqual(self.records(), [{'id': 'T01', 'response': {}, 'error': None}])

    def test_interruption_does_not_request_remaining_samples(self):
        self.save([{**self.sample, 'id': str(i)} for i in range(20)])
        self.set_concurrency(1)
        self.transport.side_effect = [KeyboardInterrupt()] + [(200, '{}')] * 19
        with self.assertRaises(KeyboardInterrupt):
            run(self.config, transport=self.transport)
        self.transport.assert_called_once()
        self.assertEqual(self.records(), [])
        with locked_output(self.root / 'results.jsonl'):
            pass

    def test_main_thread_interruption_preserves_dequeued_response(self):
        self.save([{**self.sample, 'id': str(i)} for i in range(10)])
        self.set_concurrency(1)

        class InterruptedQueue(Queue):
            def get(self, block=True, timeout=None):
                future = super().get(block=block, timeout=timeout)
                if block:
                    raise KeyboardInterrupt()
                return future

        with (
            patch('decision_models.runner.Queue', InterruptedQueue),
            self.assertRaises(KeyboardInterrupt),
        ):
            run(self.config, transport=self.transport)
        self.transport.assert_called_once()
        self.assertEqual(
            self.records(),
            [
                {'id': '0', 'response': self.response, 'error': None},
            ],
        )

    def test_interruption_saves_in_flight_response_without_new_submissions(self):
        samples = []
        for index in range(10):
            sample = copy.deepcopy(self.sample)
            sample['id'] = str(index)
            sample['input']['state'] = str(index)
            samples.append(sample)
        self.save(samples)
        self.set_concurrency(2)
        second_started = threading.Event()
        stopping = threading.Event()
        self.addCleanup(stopping.set)

        def transport(payload, *_args):
            if payload['state'] == '0':
                self.assertTrue(second_started.wait(timeout=5))
                raise KeyboardInterrupt()
            second_started.set()
            self.assertTrue(stopping.wait(timeout=5))
            return 200, '{"complete":true}'

        pool = ThreadPoolExecutor(max_workers=2)
        shutdown = pool.shutdown

        def stop_pool(*args, **kwargs):
            stopping.set()
            return shutdown(*args, **kwargs)

        transport = Mock(side_effect=transport)
        with (
            patch('decision_models.runner.ThreadPoolExecutor', return_value=pool),
            patch.object(pool, 'shutdown', side_effect=stop_pool),
        ):
            with self.assertRaises(KeyboardInterrupt):
                run(self.config, transport=transport)
        self.assertEqual(transport.call_count, 2)
        self.assertEqual(
            self.records(),
            [
                {'id': '1', 'response': {'complete': True}, 'error': None},
            ],
        )

    def test_write_failure_stops_submissions_and_preserves_partial_tail(self):
        self.save([{**self.sample, 'id': str(i)} for i in range(10)])
        self.set_concurrency(1)

        def failing_write(file, _result):
            file.write('{"id":')
            file.flush()
            raise OSError('disk full')

        with patch('decision_models.runner.write_result', failing_write):
            with self.assertRaisesRegex(OSError, 'disk full'):
                run(self.config, transport=self.transport)
        self.transport.assert_called_once()
        self.assertEqual(self.output_bytes(), b'{"id":')

    def test_other_process_cannot_run_against_locked_output(self):
        output = self.root / 'results.jsonl'
        record = {'id': 'T01', 'response': {}, 'error': None}
        output.write_text(json.dumps(record) + '\n', encoding='utf-8')
        before = output.read_bytes()
        code = """
import sys
from unittest.mock import Mock
from decision_models.runner import run

transport = Mock(side_effect=AssertionError('unexpected request'))
try:
    run(sys.argv[1], transport=transport)
except ValueError as exc:
    assert 'another run' in str(exc), str(exc)
else:
    raise AssertionError('output lock was ignored')
transport.assert_not_called()
"""
        env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src')}
        with locked_output(output):
            result = subprocess.run(
                [sys.executable, '-B', '-c', code, str(self.config)],
                env=env,
                capture_output=True,
                text=True,
                timeout=20,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output.read_bytes(), before)

    def test_invalid_history_aborts_before_request_without_mutating_file(self):
        output = self.root / 'results.jsonl'
        line = json.dumps({'id': 'T01', 'response': {}, 'error': None}) + '\n'
        content = (line + line + '{"id":').encode('utf-8')
        output.write_bytes(content)
        with self.assertRaisesRegex(ValueError, 'duplicate sample'):
            run(self.config, transport=self.transport)
        self.transport.assert_not_called()
        self.assertEqual(output.read_bytes(), content)

    def test_missing_newline_does_not_cause_a_duplicate_request(self):
        self.save([self.sample, {**self.sample, 'id': 'T02'}])
        output = self.root / 'results.jsonl'
        first = json.dumps({'id': 'T01', 'response': {}, 'error': None})
        output.write_text(first, encoding='utf-8')
        run(self.config, transport=self.transport)
        self.transport.assert_called_once()
        self.assertEqual([row['id'] for row in self.records()], ['T01', 'T02'])
        self.assertTrue(output.read_bytes().startswith(first.encode('utf-8')))

    def test_metadata_is_not_sent_and_logs_do_not_expose_credentials(self):
        self.sample['metadata'] = {'private': 'test metadata'}
        self.save([self.sample])
        with self.assertLogs('decision_models', level='INFO') as logs:
            run(self.config, transport=self.transport)
        payload = self.transport.call_args.args[0]
        self.assertEqual(payload, {'model': 'test-model', **self.sample['input']})
        self.assertNotIn('test-only', '\n'.join(logs.output))
        self.assertNotIn('test metadata', '\n'.join(logs.output))
        self.assertIn('summary', '\n'.join(logs.output))

    def test_invalid_json_and_duplicate_keys_are_rejected(self):
        for text in [
            '{"schema_version": 1, "samples": NaN}',
            '{"schema_version": 1, "samples": [], "samples": []}',
        ]:
            with self.subTest(text=text):
                (self.root / 'data.json').write_text(text, encoding='utf-8')
                with self.assertRaises(ValueError):
                    run(self.config, transport=self.transport)
        self.transport.assert_not_called()
        self.assertFalse((self.root / 'results.jsonl').exists())

    def test_invalid_choice_fails_before_requests(self):
        del self.sample['input']['questions']['action']['criteria']
        self.save([self.sample])
        with self.assertRaises(ValueError):
            run(self.config, transport=self.transport)
        self.transport.assert_not_called()

    def test_old_entrypoint_config_is_rejected(self):
        config = yaml.safe_load(self.config.read_text())
        config['entrypoint'] = 'code/__init__.py'
        self.config.write_text(yaml.safe_dump(config))
        with self.assertRaises(ValueError):
            run(self.config, transport=self.transport)
        self.transport.assert_not_called()

    def test_result_schema_includes_all_error_variants(self):
        self.save([{**self.sample, 'id': str(i)} for i in range(4)])
        self.transport.side_effect = [
            OSError('timeout'),
            (500, '{}'),
            (200, 'invalid'),
            (200, 'null'),
        ]
        run(self.config, transport=self.transport)
        schema = json.loads((ROOT / 'schema/result.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        for row in self.records():
            Draft202012Validator(schema).validate(row)

    def test_default_concurrency_starts_at_four_and_grows_on_success(self):
        """Without a configured concurrency the initial in-flight count is 4, then AIMD raises it on success."""
        self.save([{**self.sample, 'id': f'S{i:02d}'} for i in range(8)])
        state = {'active': 0, 'peak': 0, 'calls': 0}
        lock = threading.Lock()

        def transport(*_args):
            with lock:
                state['calls'] += 1
                delay = state['calls'] * 0.005
                state['active'] += 1
                state['peak'] = max(state['peak'], state['active'])
            time.sleep(delay)
            with lock:
                state['active'] -= 1
            return 200, json.dumps(self.response)

        run(self.config, transport=transport)
        self.assertGreater(state['peak'], 4)
        self.assertEqual(len(self.records()), 8)

    def test_concurrency_halves_after_failures(self):
        """A failure halves the limit, lowering the in-flight count after the first wave."""
        self.save([{**self.sample, 'id': f'S{i:02d}'} for i in range(8)])
        self.set_concurrency(4)
        lock = threading.Lock()
        gate = threading.Event()
        state = {'active': 0, 'seen': []}

        def transport(*_args):
            with lock:
                state['active'] += 1
                state['seen'].append(state['active'])
                first_wave = len(state['seen']) <= 4
                if len(state['seen']) == 4:
                    gate.set()
            if first_wave:
                gate.wait(5)
            time.sleep(0.001)
            with lock:
                state['active'] -= 1
            return 503, '{}'

        run(self.config, transport=transport)
        self.assertEqual(max(state['seen'][:4]), 4)
        self.assertLessEqual(max(state['seen'][4:]), 2)
        self.assertEqual(len(self.records()), 8)
        self.assertTrue(all(row['error'] for row in self.records()))

    def test_adjust_limit_aimd(self):
        """The limit gains one on success and halves on failure, clamped between 1 and the global ceiling."""
        self.assertEqual(_adjust_limit(4, 16, True), 5)
        self.assertEqual(_adjust_limit(16, 16, True), 16)
        self.assertEqual(_adjust_limit(4, 16, False), 2)
        self.assertEqual(_adjust_limit(1, 16, False), 1)

    def test_concurrency_is_validated(self):
        """Concurrency accepts only integers from 1 to 16; invalid values abort before any request."""
        for value in [0, 17, -1, True, '4', 1.5, [4]]:
            with self.subTest(invalid=value):
                self.set_concurrency(value)
                with self.assertRaises(ValueError):
                    run(self.config, transport=self.transport)
        self.transport.assert_not_called()
        self.assertFalse((self.root / 'results.jsonl').exists())
        for value in [1, 16]:
            with self.subTest(valid=value):
                (self.root / 'results.jsonl').unlink(missing_ok=True)
                self.set_concurrency(value)
                run(self.config, transport=self.transport)
                self.assertEqual(
                    self.records(),
                    [{'id': 'T01', 'response': self.response, 'error': None}],
                )

    def test_repeat_runs_write_separate_files(self):
        """With repeat 2 the run makes two rounds, each written to its own file."""
        self.save([self.sample, {**self.sample, 'id': 'T02'}])
        self.set_concurrency(1)
        self.set_repeat(2)
        outputs = run(self.config, transport=self.transport)
        names = ['results_1.jsonl', 'results_2.jsonl']
        self.assertEqual(outputs, [self.root / name for name in names])
        self.assertEqual(self.transport.call_count, 4)
        expected = [
            {'id': name, 'response': self.response, 'error': None}
            for name in ['T01', 'T02']
        ]
        for name in names:
            self.assertEqual(self.read_records(name), expected)
        self.assertFalse((self.root / 'results.jsonl').exists())

    def test_repeat_resume_is_tracked_per_file(self):
        """Each round resumes on its own: recorded rounds are not requested again, missing ones start fresh."""
        self.set_repeat(2)
        record = {'id': 'T01', 'response': self.response, 'error': None}
        first = self.root / 'results_1.jsonl'
        first.write_text(
            json.dumps(record, ensure_ascii=False) + '\n', encoding='utf-8'
        )
        head = first.read_bytes()
        run(self.config, transport=self.transport)
        self.transport.assert_called_once()
        self.assertEqual(first.read_bytes(), head)
        self.assertEqual(self.read_records('results_2.jsonl'), [record])

    def test_multiple_data_files_map_to_matching_outputs(self):
        """List data pairs one-to-one with list output, each dataset writing its own result file."""
        other = {**self.sample, 'id': 'E01'}
        (self.root / 'data2.json').write_text(
            json.dumps({'schema_version': 1, 'samples': [other]}),
            encoding='utf-8',
        )
        config = yaml.safe_load(self.config.read_text(encoding='utf-8'))
        config['data'] = ['data.json', 'data2.json']
        config['output'] = ['zh.jsonl', 'en.jsonl']
        self.config.write_text(yaml.safe_dump(config), encoding='utf-8')
        self.set_concurrency(1)
        outputs = run(self.config, transport=self.transport)
        self.assertEqual(
            outputs, [self.root / name for name in ['zh.jsonl', 'en.jsonl']]
        )
        self.assertEqual(self.transport.call_count, 2)
        record = {'id': 'T01', 'response': self.response, 'error': None}
        self.assertEqual(self.read_records('zh.jsonl'), [record])
        self.assertEqual(
            self.read_records('en.jsonl'),
            [{'id': 'E01', 'response': self.response, 'error': None}],
        )

    def test_multiple_data_with_repeat_expands_each_output(self):
        """With several data files and repeat together, each output expands per round."""
        other = {**self.sample, 'id': 'E01'}
        (self.root / 'data2.json').write_text(
            json.dumps({'schema_version': 1, 'samples': [other]}),
            encoding='utf-8',
        )
        config = yaml.safe_load(self.config.read_text(encoding='utf-8'))
        config['data'] = ['data.json', 'data2.json']
        config['output'] = ['zh.jsonl', 'en.jsonl']
        config['repeat'] = 2
        self.config.write_text(yaml.safe_dump(config), encoding='utf-8')
        outputs = run(self.config, transport=self.transport)
        self.assertEqual(
            outputs,
            [
                self.root / name
                for name in ['zh_1.jsonl', 'zh_2.jsonl', 'en_1.jsonl', 'en_2.jsonl']
            ],
        )
        self.assertEqual(self.transport.call_count, 4)

    def test_multiple_data_requires_matching_outputs(self):
        """With several data files, output must be a list of the same length without repeats."""
        (self.root / 'data2.json').write_text(
            json.dumps({'schema_version': 1, 'samples': [self.sample]}),
            encoding='utf-8',
        )
        base = yaml.safe_load(self.config.read_text(encoding='utf-8'))
        base['data'] = ['data.json', 'data2.json']
        cases = [
            'results.jsonl',
            ['zh.jsonl'],
            ['zh.jsonl', 'zh.jsonl'],
            ['zh.jsonl', 'en.jsonl', 'fr.jsonl'],
        ]
        for output in cases:
            with self.subTest(invalid=output):
                config = {**base, 'output': output}
                self.config.write_text(yaml.safe_dump(config), encoding='utf-8')
                with self.assertRaises(ValueError):
                    run(self.config, transport=self.transport)
        self.transport.assert_not_called()

    def test_data_field_is_validated(self):
        """data must be one non-empty string or a list of non-empty strings."""
        base = yaml.safe_load(self.config.read_text(encoding='utf-8'))
        for value in [[], ['data.json', ''], [1], {}, None]:
            with self.subTest(invalid=value):
                config = {**base, 'data': value}
                self.config.write_text(yaml.safe_dump(config), encoding='utf-8')
                with self.assertRaises(ValueError):
                    run(self.config, transport=self.transport)
        self.transport.assert_not_called()
        single = {**base, 'data': ['data.json']}
        self.config.write_text(yaml.safe_dump(single), encoding='utf-8')
        output = run(self.config, transport=self.transport)
        self.assertEqual(output, self.root / 'results.jsonl')

    def test_repeat_is_validated(self):
        """repeat accepts only integers of at least 1; a value of 1 matches the default single run."""
        for value in [0, -1, True, '2', 1.5, [2]]:
            with self.subTest(invalid=value):
                self.set_repeat(value)
                with self.assertRaises(ValueError):
                    run(self.config, transport=self.transport)
        self.transport.assert_not_called()
        self.assertEqual(list(self.root.glob('results*.jsonl')), [])
        self.set_repeat(1)
        output = run(self.config, transport=self.transport)
        self.transport.assert_called_once()
        self.assertEqual(output, self.root / 'results.jsonl')
        self.assertEqual(
            self.records(),
            [{'id': 'T01', 'response': self.response, 'error': None}],
        )

    def test_concurrent_writes_stay_complete(self):
        """Under concurrency every line stays complete and ids are neither duplicated nor lost."""
        names = [f'S{i:03d}' for i in range(100)]
        self.save([{**self.sample, 'id': name} for name in names])
        self.set_concurrency(8)

        def transport(*_args):
            time.sleep(random.uniform(0, 0.002))
            return 200, json.dumps(self.response)

        run(self.config, transport=transport)
        text = (self.root / 'results.jsonl').read_text(encoding='utf-8')
        self.assertTrue(text.endswith('\n'))
        rows = [json.loads(line) for line in text.splitlines()]
        self.assertEqual(len(rows), len(names))
        self.assertEqual({row['id'] for row in rows}, set(names))
        self.assertTrue(all(row['error'] is None for row in rows))

    def test_concurrent_failures_do_not_break_other_records(self):
        """Under concurrency a failed sample is still recorded and the other records are unaffected."""
        names = [f'S{i:02d}' for i in range(20)]
        self.save([{**self.sample, 'id': name} for name in names])
        self.set_concurrency(4)
        rng = random.Random(1)

        def transport(*_args):
            if rng.random() < 0.5:
                raise OSError('connection failed')
            return 200, json.dumps(self.response)

        run(self.config, transport=transport)
        rows = self.records()
        self.assertEqual({row['id'] for row in rows}, set(names))
        self.assertTrue(any(row['error'] for row in rows))
        self.assertTrue(any(row['error'] is None for row in rows))

    def test_cli_uses_final_data_without_recipe_code(self):
        received = []

        class Handler(BaseHTTPRequestHandler):
            """A local server exercises a real HTTP request without reaching the internet."""

            def do_POST(self):
                received.append(
                    json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                )
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"answers":{"action":{"choice":"a"}}}')

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            config = yaml.safe_load(self.config.read_text())
            config['endpoint'] = f'http://127.0.0.1:{server.server_port}'
            self.config.write_text(yaml.safe_dump(config))
            process = subprocess.run(
                [sys.executable, '-B', str(ROOT / 'run.py'), str(self.config)],
                cwd=self.root,
                check=True,
                capture_output=True,
                timeout=20,
            )
            self.assertIn('INFO decision_models.runner', process.stdout.decode())
            self.assertEqual(
                received, [{'model': 'test-model', **self.sample['input']}]
            )
            self.assertEqual(len(self.records()), 1)
            self.assertEqual(
                {file.name for file in self.root.iterdir()},
                {'config.yaml', 'data.json', 'results.jsonl'},
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == '__main__':
    unittest.main()
