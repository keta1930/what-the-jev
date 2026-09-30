"""Offline integrity/distribution checks for this experiment.

This is a check of recorded evidence and included files, not a legal opinion.
No network/model calls. Default mode rejects locally reconstructed restricted inputs.
"""
from pathlib import Path
from decimal import Decimal
import argparse, hashlib, importlib.util, json, math, re
import jsonschema
import yaml

ROOT=Path(__file__).resolve().parents[2]
NAMES=('socialiqa',)
COUNTS={'socialiqa':2224}
MODEL='typesafe/jev-1.13-20260917'
TRANSIENT={'.pyc','.aux','.log','.out','.toc','.lock','.synctex'}

def require(ok,message):
    if not ok:raise ValueError(message)

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def rows(path):
    with path.open(encoding='utf-8') as stream:
        return [json.loads(line) for line in stream if line.strip()]
def sha(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):digest.update(chunk)
    return digest.hexdigest()
def module(path):
    spec=importlib.util.spec_from_file_location('offline_'+path.parent.parent.name,path)
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value

def files_in(root):
    return sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts
                  and p.suffix not in TRANSIENT and not p.name.endswith('.synctex.gz')
                  and p.name!='distribution_manifest.json')

def restricted_paths(root):
    """Check disk contents as well as Git: ignored inputs also leak in ZIP archives."""
    bad=[]
    for folder in ['data','preparation/raw','result/original']:
        bad.extend(p for p in (root/folder).rglob('*') if p.is_file() and p.name!='README.md')
    bad.extend((root/'report/generated').glob('cases*'))
    return bad

def verify_manifest(root,local_data):
    manifest=read(root/'preparation/distribution_manifest.json')
    expected=manifest['files'];actual={p.relative_to(root).as_posix():p for p in files_in(root)}
    if local_data and root.name in ('moca','oejts'):
        actual={k:v for k,v in actual.items() if k!='data/dataset.json'}
    require(set(expected)==set(actual),f'{root.name}: distribution file inventory changed')
    for rel,path in actual.items():
        require(path.stat().st_size<100*1024*1024,f'{root.name}/{rel}: exceeds 100 MiB')
        require(sha(path)==expected[rel]['sha256'],f'{root.name}/{rel}: hash changed')
        if path.suffix.lower() in {'.json','.jsonl','.yaml','.py','.md','.txt','.csv','.tex'}:
            # Never print potential credentials: only identify the file.
            with path.open(encoding='utf-8-sig') as stream:
                for line in stream:
                    require(not re.search(r'(?:sk-or-v1-|sk-proj-)[A-Za-z0-9_-]{20,}',line),f'{root.name}/{rel}: potential credential')
    return len(actual)

def verify(local_data=False):
    dataset_validator=jsonschema.Draft202012Validator(read(ROOT/'schema/dataset.schema.json'))
    result_validator=jsonschema.Draft202012Validator(read(ROOT/'schema/result.schema.json'))
    data={};responses={};summary={};report=[]
    for name in NAMES:
        root=ROOT/'experiments'/name
        if name in ('moca','oejts') and not local_data:
            require(not restricted_paths(root),f'{name}: local source-derived files must be removed before distribution')
        file_count=verify_manifest(root,local_data)
        config=yaml.safe_load((root/'config.yaml').read_text(encoding='utf-8'))
        require(set(config)=={'model','endpoint','data','output','concurrency','repeat'},name+': config fields')
        require(config['data']=='data/dataset.json' and config['output']=='result/responses.jsonl',name+': config paths')
        require(config['repeat']==(10 if name=='oejts' else 1),name+': repeat')
        require(config['model']=='typesafe/jev-1.13' and config['endpoint']=='https://openrouter.ai/api/alpha/decisions',name+': model/endpoint')
        require(1<=config['concurrency']<=16,name+': concurrency')
        if (root/'data/dataset.json').exists():
            ds=read(root/'data/dataset.json');dataset_validator.validate(ds)
            samples={s['id']:s for s in ds['samples']}
            require(len(ds['samples'])==len(samples)==COUNTS[name],name+': dataset coverage')
            data[name]=samples
        groups=[]
        for rd in range(1,config['repeat']+1):
            filename=f'responses_{rd}.jsonl' if name=='oejts' else 'responses.jsonl'
            records=rows(root/'result'/filename)
            byid={r['id']:r for r in records}
            require(len(records)==len(byid)==COUNTS[name],name+': response coverage/duplicates')
            if name in data:require(set(byid)==set(data[name]),name+': input/result ID mismatch')
            if name=='moca':require(set(byid)=={f'{k}-{i:03}' for k,n in [('causal',144),('moral',62)] for i in range(n)},'moca: expected ids')
            if name=='oejts':require(set(byid)=={f'oejts-q{i:02}' for i in range(1,33)},'oejts: expected ids')
            for record in records:
                result_validator.validate(record)
                require(record['error'] is None,name+': unexpected final failure')
                response=record['response'];require(response['model']==MODEL,name+': snapshot')
                if name in ('moca','oejts'):
                    require(set(response)<={'model','answers','usage','id','provider'},name+': unexpected response fields')
                    expected={'judgment'} if name=='moca' else {'position'}
                    require(set(response['answers'])==expected,name+': answer fields')
                elif name in data:
                    expected=set(data[name][record['id']]['input']['questions'])
                    require(set(response['answers'])==expected,name+': question coverage')
                for key,answer in response['answers'].items():
                    require(answer['type']=='choice',name+': answer type')
                    if name in ('moca','oejts'):
                        keys={'Yes','No'} if name=='moca' else {'1','2','3','4','5'}
                        require(set(answer)<={'type','choice','probabilities','confidence'},name+': unexpected answer text')
                    else:keys=set(data[name][record['id']]['input']['questions'][key]['criteria'])
                    require(set(answer['probabilities'])==keys and answer['choice'] in keys,name+': option set')
                    require(all(isinstance(v,(int,float)) and math.isfinite(v) and 0<=v<=1 for v in answer['probabilities'].values()),name+': probabilities')
                    require(abs(sum(answer['probabilities'].values())-1)<0.031,name+': probability total')
            groups.append(byid)
        responses[name]=groups;summary[name]=read(root/'report/generated/summary.json')
        if name!='oejts':
            original=read(root/'preparation/import_manifest.json')['historical_files_sha256']
            key='result/test_responses.jsonl' if name=='socialiqa' else 'result/responses.jsonl'
            require(sha(root/'result/responses.jsonl')==original[key],name+': historical response bytes changed')
        else:
            original=read(root/'preparation/import_manifest.json')['converted_response_files_sha256']
            for rel,digest in original.items():
                require(sha(root/rel)==digest,'oejts: converted response bytes changed')
        report.append({'experiment':name,'samples_per_round':COUNTS[name],'rounds':len(groups),'valid_responses':sum(len(g) for g in groups),'distribution_files':file_count})

    # Recompute this experiment's key outcomes from its responses.
    gold=read(ROOT/'experiments/socialiqa/data/reference.json')
    correct=sum(r['response']['answers']['answer']['choice']==gold[sid]['answer'] for sid,r in responses['socialiqa'][0].items())
    require(correct==summary['socialiqa']['correct']==1792,'socialiqa: accuracy')
    # Complete response billing totals, separate from unknown-attempt reservations.
    costs={'socialiqa':('0.035755734',851327,84512),'bbq':('0.921154332',21932246,2456664),'moca':('0.00461748',109940,6798),'moralchoice':('0.046131708',1098374,250161),'oejts':('0.00657426',156530,16640)}
    for name,groups in responses.items():
        usage=[r['response']['usage'] for g in groups for r in g.values()]
        actual=(sum((Decimal(str(u['cost'])) for u in usage),Decimal(0)),sum(u['input_tokens'] for u in usage),sum(u['output_tokens'] for u in usage))
        expected=costs[name];require(actual==(Decimal(expected[0]),expected[1],expected[2]),name+': billing total')
    return {'mode':'local-input audit' if local_data else 'distribution audit','model_calls':0,'experiments':report,'valid_responses':sum(x['valid_responses'] for x in report)}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-data',action='store_true',help='Allow locally reconstructed inputs; this does NOT validate a public distribution')
    args=parser.parse_args()
    print(json.dumps(verify(args.local_data),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
