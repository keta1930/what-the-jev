# Send prepared OpenRouter requests and save resumable full responses beside the raw prompts.

import argparse
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
import json
import os
from pathlib import Path
import sys

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[4]
RAW = Path(__file__).resolve().parents[1] / 'raw'
sys.path.insert(0, str(ROOT / 'src'))

from decision_models.client import predict, request_sample
from decision_models.json_utils import loads
from decision_models.results import drop_failed, load_recorded_ids, locked_output, write_result


def result_id(request):
    return f'{request["language"]}:{request["id"]}'


def load_requests(path):
    requests = []
    seen = set()
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        request = loads(line)
        label = f'{path}:{number}'
        fields = {'schema_version', 'method', 'endpoint', 'id', 'language', 'body'}
        if not isinstance(request, dict) or set(request) != fields:
            raise ValueError(f'{label}: unexpected request fields')
        if type(request['schema_version']) is not int or request['schema_version'] != 1:
            raise ValueError(f'{label}: schema_version must be 1')
        if request['method'] != 'POST' or request['endpoint'] != 'https://openrouter.ai/api/v1/chat/completions':
            raise ValueError(f'{label}: expected an OpenRouter Chat Completions POST')
        if not isinstance(request['id'], str) or not request['id'].strip() or request['language'] not in ('zh', 'en'):
            raise ValueError(f'{label}: invalid sample ID or language')
        body = request['body']
        if not isinstance(body, dict) or body.get('model') != 'openai/gpt-4.1-mini':
            raise ValueError(f'{label}: expected model openai/gpt-4.1-mini')
        messages = body.get('messages')
        if (not isinstance(messages, list) or len(messages) != 2
                or any(not isinstance(message, dict) or not isinstance(message.get('content'), str)
                       or not message['content'].strip() for message in messages)
                or [message.get('role') for message in messages] != ['system', 'user']):
            raise ValueError(f'{label}: expected complete system and user messages')
        response_format = body.get('response_format')
        if (not isinstance(response_format, dict) or response_format.get('type') != 'json_schema'
                or not isinstance(response_format.get('json_schema'), dict)
                or response_format['json_schema'].get('strict') is not True
                or 'schema' not in response_format['json_schema']):
            raise ValueError(f'{label}: expected a strict response JSON schema')
        Draft202012Validator.check_schema(response_format['json_schema']['schema'])
        key = result_id(request)
        if key in seen:
            raise ValueError(f'{label}: duplicate language/sample ID: {key}')
        seen.add(key)
        requests.append(request)
    if not requests:
        raise ValueError(f'{path}: request file is empty')
    return requests


def call_llm(request, api_key, transport=predict):
    result = request_sample(result_id(request), request['body'], api_key, request['endpoint'], transport)
    if result['error'] is not None:
        return result
    try:
        response = result['response']
        if not isinstance(response, dict) or response.get('error'):
            raise ValueError('response contains an API error or is not an object')
        if response.get('model') != request['body']['model'] or response.get('provider') != 'OpenAI':
            raise ValueError('response model or provider differs from the requested baseline')
        choices = response.get('choices')
        if not isinstance(choices, list) or len(choices) != 1 or choices[0].get('finish_reason') != 'stop':
            raise ValueError('response does not contain one complete answer')
        message = choices[0]['message']
        if message.get('refusal') or message.get('tool_calls'):
            raise ValueError('response contains a refusal or tool call')
        answer = loads(message['content'])
        schema = request['body']['response_format']['json_schema']['schema']
        error = next(Draft202012Validator(schema).iter_errors(answer), None)
        if error is not None:
            raise ValueError(f'answer violates the response schema: {error.message}')
    except (KeyError, IndexError, TypeError, AttributeError, ValueError) as exc:
        result['error'] = {'type': 'invalid_json', 'message': f'invalid completion: {exc}'}
    return result


def run_requests(requests, output, api_key, concurrency, transport=predict):
    output.parent.mkdir(parents=True, exist_ok=True)
    completed = failed = 0
    with locked_output(output):
        recorded = load_recorded_ids(output)
        expected = {result_id(request) for request in requests}
        if recorded - expected:
            raise ValueError(f'{output}: contains IDs absent from the input requests')
        recorded -= drop_failed(output)
        pending = iter(request for request in requests if result_id(request) not in recorded)
        total = len(requests) - len(recorded)
        print(f'{len(requests)} requests; {len(recorded)} already saved; {total} pending', flush=True)
        pool = ThreadPoolExecutor(max_workers=concurrency)
        active = {}
        writable = True

        def submit_next():
            request = next(pending, None)
            if request is not None:
                active[pool.submit(call_llm, request, api_key, transport)] = result_id(request)

        with output.open('a', encoding='utf-8') as file:
            try:
                for _ in range(min(concurrency, total)):
                    submit_next()
                while active:
                    finished, _ = wait(active, return_when=FIRST_COMPLETED)
                    for future in finished:
                        result = future.result()
                        writable = False
                        write_result(file, result)
                        del active[future]
                        writable = True
                        completed += 1
                        failed += result['error'] is not None
                        status = 'OK' if result['error'] is None else f'ERROR {result["error"]["type"]}'
                        print(f'[{completed}/{total}] {result["id"]}: {status}', flush=True)
                        submit_next()
            except KeyboardInterrupt:
                print('Interrupted; waiting for in-flight requests and saving their responses.', flush=True)
                for future in active:
                    future.cancel()
                pool.shutdown(wait=True, cancel_futures=True)
                if writable:
                    for future in active:
                        if not future.cancelled():
                            result = future.result()
                            write_result(file, result)
                            completed += 1
                            failed += result['error'] is not None
                else:
                    print('Result write interrupted; leaving the file tail for repair on rerun.', flush=True)
                raise
            finally:
                pool.shutdown(wait=True, cancel_futures=True)
    print(f'Saved {completed} responses ({failed} failed, {len(recorded)} skipped): {output}', flush=True)
    return failed


def main():
    parser = argparse.ArgumentParser(description='Call GPT-4.1-mini with prepared JSONL requests and save full responses.')
    parser.add_argument('--input', type=Path, default=RAW / 'prompts.gpt-4.1-mini.jsonl')
    parser.add_argument('--output', type=Path, default=RAW / 'responses.gpt-4.1-mini.jsonl',
                        help='Result JSONL; IDs use language:sample_id to distinguish the bilingual requests')
    parser.add_argument('--concurrency', type=int, choices=range(1, 17), default=4, metavar='1..16')
    parser.add_argument('--dry-run', action='store_true', help='Validate requests without calling the API or writing results')
    args = parser.parse_args()
    source, output = args.input.resolve(), args.output.resolve()
    if source == output or (output.exists() and source.samefile(output)):
        parser.error('input and output must be different files')
    requests = load_requests(source)
    if args.dry_run:
        print(f'Validated {len(requests)} requests; model openai/gpt-4.1-mini; output: {output}')
        return
    api_key = os.environ.get('OPENROUTER_API_KEY', '').strip()
    if not api_key:
        parser.error('OPENROUTER_API_KEY must be set')
    try:
        failed = run_requests(requests, output, api_key, args.concurrency)
    except KeyboardInterrupt:
        raise SystemExit(130)
    raise SystemExit(1 if failed else 0)


if __name__ == '__main__':
    main()
