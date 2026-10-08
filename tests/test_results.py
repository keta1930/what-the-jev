"""Regression tests for result file validation, tail repair, and strict JSON parsing."""

import io
import json
import tempfile
import unittest
from http.client import HTTPException
from pathlib import Path
from unittest.mock import Mock

from decision_models.results import (
    drop_failed,
    load_recorded_ids,
    locked_output,
    request_sample,
    write_result,
)


class ResultFileTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / 'results.jsonl'
        self.record = {'id': 'T01', 'response': {'text': '中文'}, 'error': None}
        self.line = json.dumps(self.record, ensure_ascii=False).encode('utf-8')

    def scan(self):
        with locked_output(self.path):
            return load_recorded_ids(self.path)

    def test_complete_record_without_newline_is_preserved(self):
        self.path.write_bytes(self.line)
        self.assertEqual(self.scan(), {'T01'})
        self.assertEqual(self.path.read_bytes(), self.line + b'\n')

    def test_truncation_preserves_prefix_bytes(self):
        prefix = self.line + b'\r\n'
        self.path.write_bytes(prefix + b'{"id": "T02", "response":')
        self.assertEqual(self.scan(), {'T01'})
        self.assertEqual(self.path.read_bytes(), prefix)

    def test_incomplete_first_record_can_be_repaired(self):
        tails = [
            b'{"id": "T01", "resp',
            b'{"id": "T01", "response": nul',
            b'{"id": "T01", "response": 1e+',
            b'{"id": "T01", "response": "\\u00',
        ]
        for tail in tails:
            with self.subTest(tail=tail):
                self.path.write_bytes(tail)
                self.assertEqual(self.scan(), set())
                self.assertEqual(self.path.read_bytes(), b'')

    def test_truncated_utf8_tail_can_be_repaired(self):
        prefix = self.line + b'\n'
        tail = b'{"id":"T02","response":"' + '中'.encode('utf-8')[:2]
        self.path.write_bytes(prefix + tail)
        self.assertEqual(self.scan(), {'T01'})
        self.assertEqual(self.path.read_bytes(), prefix)

    def test_invalid_history_is_not_modified_before_tail_repair(self):
        invalid_lines = [
            self.line,
            b'{"id":"T02"}',
            b'{"id":"T02","response":null,"error":"bad"}',
            b'{"id":"T02","id":"T03","response":null,"error":null}',
            b'{"id":"T02","response":NaN,"error":null}',
            b'[]',
            b'',
            b'not json',
            b'\xff',
        ]
        for invalid in invalid_lines:
            with self.subTest(invalid=invalid):
                content = self.line + b'\n' + invalid + b'\n{"id":'
                self.path.write_bytes(content)
                with self.assertRaises(ValueError):
                    self.scan()
                self.assertEqual(self.path.read_bytes(), content)

    def test_invalid_complete_tail_is_not_discarded(self):
        tails = [
            self.line,
            b'{"id":"T02"}',
            b'{"id":"T02","response":NaN,"error":null}',
            b'{"id":"T02","response":1e400,"error":null}',
            b'not json',
            b'{}garbage',
            b'{"id":]}',
            b'{id: "T02"',
        ]
        for tail in tails:
            with self.subTest(tail=tail):
                content = self.line + b'\n' + tail
                self.path.write_bytes(content)
                with self.assertRaises(ValueError):
                    self.scan()
                self.assertEqual(self.path.read_bytes(), content)

    def test_valid_history_is_byte_identical(self):
        content = self.line + b'\r\n'
        self.path.write_bytes(content)
        self.assertEqual(self.scan(), {'T01'})
        self.assertEqual(self.path.read_bytes(), content)

    def test_drop_failed_preserves_success_order_and_response_content(self):
        """Failed records are dropped while successful ones keep their order and full response."""
        failure = {
            'id': 'T02',
            'response': '<html>error</html>',
            'error': {'type': 'http', 'status': 503, 'message': 'HTTP 503'},
        }
        last = {**self.record, 'id': 'T03'}
        lines = [
            json.dumps(row, ensure_ascii=False) + '\n'
            for row in [self.record, failure, last]
        ]
        self.path.write_text(''.join(lines), encoding='utf-8')
        with locked_output(self.path):
            self.assertEqual(drop_failed(self.path), {'T02'})
        self.assertEqual(self.path.read_text(encoding='utf-8'), lines[0] + lines[2])

    def test_drop_failed_leaves_success_only_file_byte_identical(self):
        """A file with no failed records is not rewritten and keeps its line endings."""
        content = self.line + b'\r\n'
        self.path.write_bytes(content)
        with locked_output(self.path):
            self.assertEqual(drop_failed(self.path), set())
        self.assertEqual(self.path.read_bytes(), content)

    def test_lock_is_exclusive_and_released_after_exception(self):
        with self.assertRaisesRegex(RuntimeError, 'stop'):
            with locked_output(self.path):
                with self.assertRaisesRegex(ValueError, 'another run'):
                    with locked_output(self.path):
                        self.fail('the same file was locked exclusively twice')
                raise RuntimeError('stop')
        with locked_output(self.path):
            self.assertEqual(self.path.read_bytes(), b'')


class ResponseTests(unittest.TestCase):
    def test_status_boundaries_preserve_json_values_and_transport_arguments(self):
        """Every JSON value is kept as it is; only 2xx statuses count as success."""
        payload = {'state': 'text'}
        for status in [199, 200, 204, 299, 300, 503]:
            for response in [None, False, 0, 'text', [], {'extra': [1, 2]}]:
                with self.subTest(status=status, response=response):
                    transport = Mock(return_value=(status, json.dumps(response)))
                    result = request_sample('T01', payload, 'key', 'url', transport)
                    transport.assert_called_once_with(payload, 'key', 'url')
                    error = None
                    if not 200 <= status < 300:
                        error = {
                            'type': 'http',
                            'status': status,
                            'message': f'HTTP {status}',
                        }
                    self.assertEqual(
                        result, {'id': 'T01', 'response': response, 'error': error}
                    )

    def test_network_errors_are_recorded_without_retry(self):
        """Connection and HTTP protocol errors are both recorded as network, with no retry."""
        for error in [OSError('timeout'), HTTPException('invalid response')]:
            with self.subTest(error=error):
                transport = Mock(side_effect=error)
                result = request_sample('T01', {}, 'key', 'url', transport)
                transport.assert_called_once()
                self.assertEqual(
                    result,
                    {
                        'id': 'T01',
                        'response': None,
                        'error': {'type': 'network', 'message': str(error)},
                    },
                )

    def test_unexpected_errors_and_interruptions_propagate(self):
        """Programming errors and interruptions reach the caller instead of posing as network failures."""
        for error in [RuntimeError('bug'), KeyboardInterrupt()]:
            with self.subTest(error=error):
                with self.assertRaises(type(error)) as raised:
                    request_sample('T01', {}, 'key', 'url', Mock(side_effect=error))
                self.assertIs(raised.exception, error)

    def test_nonfinite_and_duplicate_fields_preserve_raw_response(self):
        for text in ['{"n":1e400}', '{"n":NaN}', '{"n":1,"n":2}']:
            with self.subTest(text=text):
                result = request_sample(
                    'T01',
                    {},
                    'key',
                    'endpoint',
                    Mock(return_value=(200, text)),
                )
                self.assertEqual(result['error']['type'], 'invalid_json')
                self.assertEqual(result['response'], text)
                output = io.StringIO()
                write_result(output, result)
                self.assertEqual(json.loads(output.getvalue()), result)

    def test_http_status_takes_precedence_over_invalid_json(self):
        result = request_sample(
            'T01',
            {},
            'key',
            'endpoint',
            Mock(return_value=(429, '<html>')),
        )
        self.assertEqual(result['error']['type'], 'http')
        self.assertEqual(result['error']['status'], 429)
        self.assertEqual(result['response'], '<html>')


if __name__ == '__main__':
    unittest.main()
