"""Durable append-only journals and immutable suite snapshots."""
import json
import os
import shutil
import subprocess
import sys
import importlib.metadata
from datetime import datetime, timezone
from pathlib import Path
from game_theory.json_utils import loads
from game_theory.persistence import _is_truncated_json
from .plan import conditions, totals, MODEL, ENDPOINT, stable

ROOT = Path(__file__).resolve().parents[4]
GAME = ROOT/'games'/'game-theory'

def now(): return datetime.now(timezone.utc).isoformat()

def atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w',encoding='utf-8',newline='\n') as f:
        json.dump(value,f,ensure_ascii=False,allow_nan=False,indent=2)
        f.flush(); os.fsync(f.fileno())
    os.replace(tmp,path)

def append(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps(value,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n')
        f.flush(); os.fsync(f.fileno())

def read(path, repair=False):
    if not path.exists(): return []
    result=[]; offset=0
    with path.open('rb') as f:
        for raw in f:
            try: item=loads(raw.decode('utf-8'))
            except (ValueError,UnicodeDecodeError) as exc:
                partial = isinstance(exc,json.JSONDecodeError) and _is_truncated_json(exc) or isinstance(exc,UnicodeDecodeError) and exc.reason=='unexpected end of data'
                if repair and not raw.endswith(b'\n') and partial:
                    with path.open('r+b') as target: target.truncate(offset)
                    break
                raise ValueError(f'Corrupt journal {path} at byte {offset}') from exc
            result.append(item); offset+=len(raw)
    if repair and result and path.stat().st_size and not path.read_bytes().endswith(b'\n'):
        with path.open('ab') as f: f.write(b'\n'); f.flush(); os.fsync(f.fileno())
    return result

def plan_batch():
    cs=conditions(); count=totals(cs)
    assert count == dict(conditions=5888,matches=14592,rounds=293232,requests=185906)
    batch_id=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+stable(cs)[:8]
    path=GAME/'output'/'records'/batch_id
    if path.exists(): raise ValueError('Batch already exists')
    # Conservative synthetic upper bound: every decision carries 20 six-player
    # rounds and complete raw request/response copies in the offline package.
    synthetic={'round':100,'actions':['contribute']*6,'original':['contribute']*6,'payoffs':[26.6666666667]*6,'cumulative':[2666.66666667]*6}
    observation_bytes=len(json.dumps([synthetic]*20).encode())+4096
    all_decisions=sum(c['matches']*c['rounds']*len(c['players']) for c in cs)
    estimate=all_decisions*(observation_bytes*3+8192)+count['rounds']*4096
    free=shutil.disk_usage(ROOT).free
    if free < estimate*2: raise ValueError(f'Insufficient disk: free={free}, estimate={estimate}, required margin=2x')
    frozen_paths=set(Path(__file__).parent.glob('*.py'))
    frozen_paths.update(Path(__file__).with_name('schema').glob('*.json'))
    frozen_paths.update(ROOT/p for p in ('games/game-theory/run.py','games/game-theory/config/suite.yaml','games/game-theory/requirements.txt'))
    code={str(p.relative_to(ROOT)):stable(p.read_text(encoding='utf-8')) for p in sorted(frozen_paths)}
    packages={}
    for package in ('PyYAML','jsonschema','numpy','pyarrow','tqdm'):
        try:packages[package]=importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:packages[package]=None
    manifest=dict(batch_id=batch_id,created=now(),model=MODEL,endpoint=ENDPOINT,root_seed=1930,conditions=cs,totals=count,
                  max_attempts_per_scan=count['requests']*3,max_attempts_with_two_recovery_scans=count['requests']*9,
                  storage_estimate_bytes=estimate,disk_free_bytes=free,synthetic_estimate_only=True,
                  git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),code_hashes=code,python_executable=sys.executable,python_version=sys.version,package_versions=packages)
    manifest['sha256']=stable(manifest)
    atomic(path/'manifest.json',manifest)
    for relative in code:
        target=path/'code-snapshot'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/relative,target)
    for scenario in {c['scenario'] for c in cs}:
        atomic(GAME/scenario/'result'/batch_id/'manifest.json',dict(batch_id=batch_id,conditions=[c['id'] for c in cs if c['scenario']==scenario]))
    atomic(GAME/'output'/'records'/'latest.json',{'batch_id':batch_id})
    return manifest

def load_batch(batch_id=None):
    if batch_id is None: batch_id=json.loads((GAME/'output'/'records'/'latest.json').read_text(encoding='utf-8'))['batch_id']
    m=json.loads((GAME/'output'/'records'/batch_id/'manifest.json').read_text(encoding='utf-8'))
    if stable({k:v for k,v in m.items() if k!='sha256'})!=m['sha256']: raise ValueError('Manifest checksum mismatch')
    for relative,digest in m['code_hashes'].items():
        if Path(relative).name in ('rules.py','plan.py') and stable((Path(__file__).parent/Path(relative).name).read_text(encoding='utf-8'))!=digest:
            raise ValueError('Rules or enumeration changed after batch freeze; use a new batch')
    return m

def condition_path(m,c): return GAME/'output'/'records'/m['batch_id']/'scenarios'/c['scenario']/c['id']
