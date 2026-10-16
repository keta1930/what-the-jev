"""Test local journal locking across processes."""
import os
import subprocess
import sys
from pathlib import Path

import pytest
from game_theory.persistence import locked_output


def test_lock_release_after_exception(tmp_path):
    path=tmp_path/'journal.jsonl'
    with pytest.raises(RuntimeError):
        with locked_output(path):
            with pytest.raises(ValueError):
                with locked_output(path):
                    pass
            raise RuntimeError('test interruption')
    with locked_output(path):
        assert path.read_bytes()==b''


def test_other_process_excluded_and_result_still_readable(tmp_path):
    path=tmp_path/'journal.jsonl'
    path.write_bytes(b'{}\n')
    script='''
import sys
from pathlib import Path
from game_theory.persistence import locked_output
try:
    with locked_output(Path(sys.argv[1])):
        pass
except ValueError:
    sys.exit(3)
'''
    env=os.environ.copy()
    env['PYTHONPATH']=str(Path(__file__).resolve().parents[1]/'src')
    def attempt():
        return subprocess.run([sys.executable,'-c',script,str(path)],env=env,
                              capture_output=True,text=True,timeout=10)
    with locked_output(path):
        assert path.read_bytes()==b'{}\n'
        assert attempt().returncode==3
    result=attempt()
    assert result.returncode==0,result.stderr
