"""Lock game journals and recognize truncated JSON tails."""
# Persistence helpers derive from decision_models.results under the MIT license.
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from contextlib import contextmanager
from collections.abc import Iterator
if os.name == 'nt':
    import msvcrt
else:
    import fcntl

@contextmanager
def locked_output(path: Path) -> Iterator[None]:
    """Hold the journal lock across scanning, tail repair and appending."""
    # Windows byte locks block other handles reading that byte. Lock a stable
    # sidecar instead, leaving result scanning and append semantics unchanged.
    if os.name == 'nt':
        lock_id = hashlib.sha256(str(path.resolve()).casefold().encode()).hexdigest()
        lock_path = Path(tempfile.gettempdir()) / f'decision-models-{lock_id}.lock'
    else:
        lock_path = path
    path.touch(exist_ok=True)
    with lock_path.open('a+b') as file:
        try:
            if os.name == 'nt':
                file.seek(0)
                msvcrt.locking(file.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                fcntl.flock(file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise ValueError(f'output file is locked by another run: {path}') from exc
        try:
            yield
        finally:
            if os.name == 'nt':
                file.seek(0)
                msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(file.fileno(), fcntl.LOCK_UN)

def _is_truncated_json(error: json.JSONDecodeError) -> bool:
    """Recognize unfinished JSON tokens without accepting malformed complete records."""
    text = error.doc.rstrip()
    if not text.lstrip().startswith('{'):
        return False
    if error.msg.startswith('Unterminated string'):
        return True
    if error.pos >= len(text):
        return True
    tail = text[error.pos :]
    if error.msg == 'Expecting value':
        return tail in {
            'n',
            'nu',
            'nul',
            't',
            'tr',
            'tru',
            'f',
            'fa',
            'fal',
            'fals',
            '-',
        }
    if error.msg == "Expecting ',' delimiter":
        return tail in {'.', 'e', 'E', 'e+', 'e-', 'E+', 'E-'}
    if error.msg == 'Invalid \\uXXXX escape':
        return re.fullmatch(r'u[0-9a-fA-F]{0,3}', tail) is not None
    return False
