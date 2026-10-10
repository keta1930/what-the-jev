import argparse
import json
from .storage import plan_batch, load_batch, GAME

def main():
    p=argparse.ArgumentParser(description='Recorded game interactions; no evaluation scores.')
    p.add_argument('command',choices=('plan','run','resume','build-html','validate'))
    p.add_argument('--batch')
    p.add_argument('--rules-only',action='store_true')
    args=p.parse_args()
    from .config import validate_files
    validate_files(GAME)
    if args.command=='plan':
        m=plan_batch(); print(json.dumps({k:m[k] for k in ('batch_id','totals','max_attempts_per_scan','max_attempts_with_two_recovery_scans','storage_estimate_bytes','disk_free_bytes')},indent=2)); return
    m=load_batch(args.batch)
    if args.command in ('run','resume'):
        from .runner import Runner
        state=Runner(m).run(args.rules_only)
        print(json.dumps({'phase':state['phase'],'counts':state['counts'],'dependency':state['dependency']},ensure_ascii=False,indent=2))
    elif args.command=='validate':
        from .validate import validate_batch
        from game_theory.persistence import locked_output
        with locked_output(GAME/'output'/'records'/m['batch_id']/'batch.lock'):
            print(json.dumps(validate_batch(m),ensure_ascii=False,indent=2))
    else:
        from .html import build
        from game_theory.persistence import locked_output
        with locked_output(GAME/'output'/'records'/m['batch_id']/'batch.lock'):
            print(build(m))
