"""HTTP JSON requests, full response reading, and request result wrapping."""

import json
from collections.abc import Callable
from http.client import HTTPException
from typing import Any, TypeAlias
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from .json_utils import JSONValue as JSONValue
from .json_utils import loads

Transport: TypeAlias = Callable[[dict[str, JSONValue], str, str], tuple[int, str]]


def predict(
    payload: dict[str, JSONValue], api_key: str, endpoint: str
) -> tuple[int, str]:
    """Send a JSON request and return the HTTP status code and the full response text."""
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    request = Request(
        endpoint,
        data=data,
        method='POST',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            text = response.read().decode('utf-8', errors='replace')
            return response.status, text
    except HTTPError as exc:
        with exc:
            return exc.code, exc.read().decode('utf-8', errors='replace')


def request_sample(
    sample_id: str,
    payload: dict[str, JSONValue],
    api_key: str,
    endpoint: str,
    transport: Transport,
) -> dict[str, Any]:
    """Keep the full response without parsing business answers and without retrying."""
    result: dict[str, Any] = {
        'id': sample_id,
        'response': None,
        'error': None,
    }
    try:
        status, text = transport(payload, api_key, endpoint)
    except (OSError, HTTPException) as exc:
        result['error'] = {'type': 'network', 'message': str(exc)}
        return result
    result['response'] = text
    try:
        result['response'] = loads(text)
    except ValueError:
        result['error'] = {'type': 'invalid_json', 'message': 'response is not valid JSON'}
    if not 200 <= status < 300:
        result['error'] = {
            'type': 'http',
            'status': status,
            'message': f'HTTP {status}',
        }
    return result
