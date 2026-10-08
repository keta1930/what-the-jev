"""Prepare archived, licensed SocialIQA v1.4 files without network or model calls."""
from pathlib import Path
import json, tarfile

ROOT=Path(__file__).resolve().parents[2]

def write(path,obj):
    """Write JSON to the path, creating parent directories."""
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    """Extract the archived test rows and write the dataset."""
    archive=ROOT/'preparation/raw/socialIQa_v1.4_withDims.tgz'
    with tarfile.open(archive) as tf:
        member=next(m for m in tf.getmembers() if m.name.endswith('socialIWa_v1.4_tst_wDims.jsonl'))
        rows=[json.loads(line) for line in tf.extractfile(member)]
    samples=[]
    for i,row in enumerate(rows,1):
        sid=f'socialiqa-test-{i:05d}'
        question={'type':'choice','instructions':'Select the most plausible answer to the question based on the context and everyday social commonsense. Choose exactly one option.','criteria':{k:row['answer'+k] for k in 'ABC'}}
        samples.append({'id':sid,
            'input':{'state':{'context':row['context'],'question':row['question']},'questions':{'answer':question}},
            'reference':{'answer':{'choice':row['label_letter']}},
            'metadata':{'promptDim':row['promptDim'],'answerSourcesOrigins':row['answerSourcesOrigins'],'row_1based':i}})
    write(ROOT/'data/dataset.json',{'schema_version':1,'samples':samples})
    print(f'Prepared {len(samples)} formal items. No API requests.')

if __name__=='__main__':main()
