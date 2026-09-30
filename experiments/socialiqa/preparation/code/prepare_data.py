"""Prepare archived, licensed SocialIQA v1.4 files without network or model calls."""
from pathlib import Path
import hashlib, json, tarfile

ROOT=Path(__file__).resolve().parents[2]

def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    manifest=json.loads((ROOT/'preparation/original_manifest.json').read_text(encoding='utf-8'))
    archive=ROOT/'preparation/raw/socialIQa_v1.4_withDims.tgz'
    expected=manifest['sha256']['preparation/raw/socialIQa_v1.4_withDims.tgz']
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=expected:raise ValueError('Source archive hash mismatch')
    with tarfile.open(archive) as tf:
        for split,suffix in [('test','tst'),('debug','trn')]:
            member=next(m for m in tf.getmembers() if m.name.endswith(f'socialIWa_v1.4_{suffix}_wDims.jsonl'))
            rows=[json.loads(line) for line in tf.extractfile(member)]
            if split=='debug':rows=rows[:12]
            samples=[];reference={}
            for i,row in enumerate(rows,1):
                sid=f'socialiqa-{split}-{i:05d}'
                samples.append({'id':sid,'input':{'state':{'context':row['context'],'question':row['question']},'questions':{'answer':{'type':'choice','instructions':'Select the most plausible answer to the question based on the context and everyday social commonsense. Choose exactly one option.','criteria':{k:row['answer'+k] for k in 'ABC'}}}}})
                reference[sid]={'answer':row['label_letter'],'promptDim':row['promptDim'],'answerSourcesOrigins':row['answerSourcesOrigins'],'row_1based':i}
            write(ROOT/('data/dataset.json' if split=='test' else 'data/debug.json'),{'schema_version':1,'samples':samples})
            write(ROOT/('data/reference.json' if split=='test' else 'data/debug_reference.json'),reference)
    print('Prepared 2,224 formal and 12 separate debugging items. No API requests.')

if __name__=='__main__':main()
