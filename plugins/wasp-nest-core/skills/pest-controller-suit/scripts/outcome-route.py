#!/usr/bin/env python3
"""Read-only lexical discovery over the packaged outcome index.

Candidate ranking is discovery assistance. It neither launches a workflow nor
establishes installed availability. Use Core's selected-owner resolver next.
"""
import argparse
import json
from pathlib import Path
import re
import sys

INDEX = Path(__file__).resolve().parents[1] / 'references' / 'outcome-index.json'
STOP = {'a','an','the','i','my','want','to','with','for','and','of','this','it','how','do','can','me'}
ALIASES = {'explain': 'understand', 'teach': 'learn', 'pricing': 'price',
           'costs': 'cost', 'refactoring': 'refactor', 'repo': 'repository',
           'desktop': 'desktop', 'phone': 'mobile', 'iphone': 'ios',
           'beginner': 'learning', 'bloat': 'simplification', 'saas': 'saas'}

def tokens(value):
    return {ALIASES.get(t,t) for t in re.findall(r'[a-z0-9]+',value.casefold()) if t not in STOP}

def discover(index, query, limit=5, bucket=None):
    if not isinstance(query,str) or not query.strip() or len(query)>2000:
        raise ValueError('query must be a nonempty string of at most 2000 characters')
    if isinstance(limit,bool) or not isinstance(limit,int) or not 1<=limit<=20:
        raise ValueError('limit must be an integer from 1 to 20')
    requested=tokens(query)
    candidates=[]
    for entry in index['outcomes']:
        if bucket and bucket not in (entry['bucket_id'],entry['bucket']):continue
        terms=tokens(entry['outcome']+' '+entry['bucket']+' '+entry['capability_group'])
        overlap=requested & terms
        if not overlap:continue
        score=len(overlap)/len(requested) if requested else 0
        # Exact task terms outrank incidental shared words in a broad bucket.
        direct=len(requested & tokens(entry['outcome']))
        candidates.append((score,direct,entry['id'],entry,sorted(overlap)))
    candidates.sort(key=lambda x:(-x[0],-x[1],x[2]))
    return {'query':query,'method':'lexical shortlist; inspect scope and negative routing before selecting',
        'availability':'unverified; resolve the selected component through Core before dispatch',
        'candidates':[dict(entry,matched_terms=overlap,match_score=round(score,3))
            for score,direct,_,entry,overlap in candidates[:limit]]}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query')
    parser.add_argument('--limit',type=int,default=5)
    parser.add_argument('--bucket')
    args=parser.parse_args()
    try:
        result=discover(json.loads(INDEX.read_text()),args.query,args.limit,args.bucket)
    except (OSError,ValueError,KeyError,TypeError) as exc:
        parser.exit(1,str(exc)+'\n')
    json.dump(result,sys.stdout,indent=2);sys.stdout.write('\n')
    return 0

if __name__=='__main__':raise SystemExit(main())
