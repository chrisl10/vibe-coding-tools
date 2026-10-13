#!/usr/bin/env python3
"""Offline evidence consistency and supplied-input scenario checker; no truth grading."""
import argparse
import datetime as dt
from decimal import Decimal, InvalidOperation, localcontext
import hashlib
import json
from pathlib import Path
import re
import sys

class InputError(ValueError):
    pass

def require(ok, message):
    if not ok:
        raise InputError(message)

def fields(obj, required, optional=()):
    require(isinstance(obj, dict), 'expected object')
    require(set(required) <= set(obj) <= set(required) | set(optional), 'missing or unknown fields')

def text(value, maximum=1000):
    require(isinstance(value, str) and 0 < len(value) <= maximum, 'invalid text')
    return value

def day(value):
    require(isinstance(value, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', value), 'invalid date')
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        raise InputError('invalid calendar date') from None

def sequence(value, maximum):
    require(isinstance(value, list) and len(value) <= maximum, 'invalid or oversized array')
    return value

def refs(value, sources):
    sequence(value, 100)
    require(all(isinstance(x, str) for x in value), 'invalid source reference')
    require(len(set(value)) == len(value) and all(x in sources for x in value), 'unknown or duplicate source reference')

def number(value, fraction=False):
    text(value, 30)
    require(re.fullmatch(r'\d+(?:\.\d+)?(?:[eE][+-]?\d+)?', value), 'invalid decimal string')
    exponent=value.lower().partition('e')[2]
    require(not exponent or abs(int(exponent)) <= 18, 'decimal exponent out of range')
    try:
        n=Decimal(value)
        require(n.is_finite() and n >= 0 and n <= (Decimal(1) if fraction else Decimal('1e12')), 'decimal out of range')
        return n
    except InvalidOperation:
        raise InputError('invalid decimal') from None

def validate(data, root, verify=False):
    fields(data, ['as_of','sources','claims'], ['scenarios'])
    as_of=day(data['as_of']); sources={}; warnings=[]
    for s in sequence(data['sources'],100):
        fields(s,['id','url','retrieved','kind','archive','sha256','freshness_days'])
        sid=text(s['id'],100); require(sid not in sources,'duplicate source id')
        require(isinstance(s['url'],str) and re.fullmatch(r'https?://[^\s/]+(?:/[^\s]*)?',s['url']), 'invalid source URL')
        require(s['kind'] in ['vendor','observation','dataset','other'], 'invalid source kind')
        require(type(s['freshness_days']) is int and 0 <= s['freshness_days'] <= 3660,'invalid expiry policy')
        age=(as_of-day(s['retrieved'])).days; require(age >= 0,'future source date')
        if age>s['freshness_days']: warnings.append({'source_id':sid,'status':'stale','age_days':age})
        require(isinstance(s['sha256'],str) and re.fullmatch('[0-9a-f]{64}',s['sha256']),'invalid archive hash')
        name=text(s['archive'],500); p=Path(name)
        require(not p.is_absolute() and '..' not in p.parts,'archive path escapes input directory')
        if verify:
            resolved=(root/p).resolve(); require(resolved.is_relative_to(root.resolve()),'archive path escapes input directory')
            require(resolved.is_file() and resolved.stat().st_size <= 4*1024*1024,'missing or oversized archive')
            require(hashlib.sha256(resolved.read_bytes()).hexdigest()==s['sha256'],'archive hash mismatch')
        sources[sid]=s
    claims=set()
    for c in sequence(data['claims'],500):
        fields(c,['id','classification','statement','source_ids','scope'])
        cid=text(c['id'],100); require(cid not in claims,'duplicate claim id'); claims.add(cid)
        kind=c['classification']; require(kind in ['vendor_claim','observed','inference','unknown'],'invalid classification')
        text(c['statement']); text(c['scope']); refs(c['source_ids'],sources)
        require(bool(c['source_ids']) == (kind!='unknown'),'claim provenance missing or unknown incorrectly sourced')
        if kind=='observed': require(any(sources[s]['kind']=='observation' for s in c['source_ids']),'observed claim lacks observation source')
    outputs=[]; scenario_ids=set()
    for s in sequence(data.get('scenarios',[]),20):
        fields(s,['id','currency','horizon_months','inputs'])
        sid=text(s['id'],100); require(sid not in scenario_ids,'duplicate scenario id'); scenario_ids.add(sid)
        require(isinstance(s['currency'],str) and re.fullmatch('[A-Z]{3}',s['currency']),'invalid currency')
        require(type(s['horizon_months']) is int and 1 <= s['horizon_months'] <= 120,'invalid horizon')
        keys=['eligible_accounts','reachable_fraction','conversion_fraction','capacity_accounts','annual_price_per_account']; fields(s['inputs'],keys)
        values={}
        for k in keys:
            v=s['inputs'][k]; fields(v,['value','basis','source_ids','rationale']); refs(v['source_ids'],sources)
            require(v['basis'] in ['measured','assumed','unknown'],'invalid input basis')
            require((v['value'] is None)==(v['basis']=='unknown'),'unknown must be null')
            require(isinstance(v['rationale'],str) and len(v['rationale']) <= 1000,'invalid rationale')
            if v['basis']=='measured': require(bool(v['source_ids']),'measured input requires source')
            if v['basis']=='assumed': text(v['rationale'])
            values[k]=None if v['value'] is None else number(v['value'],k.endswith('_fraction'))
        output={'id':sid,'currency':s['currency'],'horizon_months':s['horizon_months'],'interpretation':'supplied-input annualized scenario, not market truth or forecast'}
        if any(v is None for v in values.values()): output.update(status='incomplete',unknown_inputs=[k for k,v in values.items() if v is None])
        else:
            with localcontext() as ctx:
                ctx.prec=80
                reached=values['eligible_accounts']*values['reachable_fraction']; served=min(reached*values['conversion_fraction'],values['capacity_accounts'])
                revenue=served*values['annual_price_per_account']
            output.update(status='computed',reached_accounts=str(reached),served_accounts=str(served),annualized_revenue=str(revenue))
        outputs.append(output)
    return {'status':'consistent','sources':len(sources),'claims':len(claims),'warnings':warnings,'scenarios':outputs,'limits':'Consistency and arithmetic only; human provenance, population fit and proof review required'}

def no_duplicates(pairs):
    result={}
    for k,v in pairs:
        require(k not in result,'duplicate JSON key'); result[k]=v
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('input',type=Path); parser.add_argument('--verify-archives',action='store_true'); args=parser.parse_args()
    try:
        require(args.input.is_file() and args.input.stat().st_size <= 256*1024,'missing or oversized input')
        data=json.loads(args.input.read_text(),object_pairs_hook=no_duplicates,parse_constant=lambda x: (_ for _ in ()).throw(InputError('nonfinite JSON number')))
        result=validate(data,args.input.parent,args.verify_archives)
    except (InputError,ValueError,OSError,RecursionError,TypeError) as e:
        print('Input error: '+(str(e) if isinstance(e,InputError) else 'invalid input or inaccessible local file'),file=sys.stderr); return 2
    print(json.dumps(result,indent=2)); return 0

if __name__=='__main__':
    sys.exit(main())
