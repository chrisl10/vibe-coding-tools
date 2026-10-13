#!/usr/bin/env python3
"""Validate discovery record bookkeeping. Never classify demand or select a decision."""
import argparse
from datetime import datetime
import json
import math
from pathlib import Path

MAX_BYTES = 1024 * 1024
TEXT = ['test_id','outcome','assumption','contradicting_observation','population','channel','participant_source','consent_procedure','exposure_definition','stimulus','proxy_limit','owner']
GRADES = {'CONTEXT','REPORTED','OBSERVED','HYPOTHESIS','MISSING'}

def enum(value, choices):
    return isinstance(value, str) and value in choices

def timestamp(value):
    if not isinstance(value, str): return None
    try:
        result = datetime.fromisoformat(value.replace('Z','+00:00'))
        return result if result.tzinfo is not None and result.utcoffset() is not None else None
    except ValueError:
        return None

def number(value):
    if not isinstance(value,(int,float)) or isinstance(value,bool): return False
    try: return math.isfinite(value)
    except OverflowError: return False

def check(record):
    errors=[];warnings=[]
    def need(ok,name):
        if not ok: errors.append(name)
    if not isinstance(record,dict): return {'errors':['record must be an object'],'warnings':[],'scope':'bookkeeping only'}
    need(record.get('schema_version') == 1 and not isinstance(record.get('schema_version'),bool),'schema_version must be 1')
    status=record.get('status');need(enum(status, {'planned','executed','failed','cancelled'}),'status is invalid')
    for key in TEXT: need(isinstance(record.get(key),str) and bool(record[key].strip()),key+' is required')
    start=timestamp(record.get('planned_start'));end=timestamp(record.get('planned_end'))
    need(start is not None,'planned_start requires an offset timestamp');need(end is not None,'planned_end requires an offset timestamp')
    if start and end: need(end >= start,'planned_end precedes planned_start')
    need(number(record.get('budget_limit')) and record['budget_limit'] >= 0,'budget_limit requires a finite nonnegative number')
    metric=record.get('metric')
    if not isinstance(metric,dict): errors.append('metric must be an object');metric={}
    for key in ['name','unit','numerator_definition','denominator_definition','time_window']:
        need(isinstance(metric.get(key),str) and bool(metric[key].strip()),'metric.'+key+' is required')
    criterion=record.get('criterion')
    if not isinstance(criterion,dict): errors.append('criterion must be an object');criterion={}
    need(isinstance(criterion.get('version'),int) and not isinstance(criterion.get('version'),bool) and criterion['version'] >= 1,'criterion.version requires a positive integer')
    declared=timestamp(criterion.get('declared_at'));need(declared is not None,'criterion.declared_at requires an offset timestamp')
    if start and declared: need(declared <= start,'criterion declared after planned exposure')
    need(enum(criterion.get('operator'), {'>=','>','<=','<','=='}),'criterion.operator is invalid')
    need(number(criterion.get('threshold')),'criterion.threshold requires a finite number')
    need(isinstance(criterion.get('minimum_exposures'),int) and not isinstance(criterion.get('minimum_exposures'),bool) and criterion['minimum_exposures'] >= 1,'minimum_exposures requires a positive integer')
    need(isinstance(criterion.get('stop_rule'),str) and bool(criterion['stop_rule'].strip()),'criterion.stop_rule is required')
    for key in ['feasibility_constraints','observations','changes','source_paths']:
        need(isinstance(record.get(key),list),key+' must be an array')
    observations=record.get('observations') if isinstance(record.get('observations'),list) else []
    if status == 'executed':
        need(bool(observations),'executed record needs observations')
        need(bool(record.get('source_paths')),'executed record needs source paths')
    if status == 'planned' and observations: errors.append('planned record cannot contain observed results')
    for item in observations:
        if not isinstance(item,dict): errors.append('observation must be an object');continue
        need(enum(item.get('grade'), GRADES),'observation.grade is invalid')
        for key in ['source','claim','relevance']:
            need(isinstance(item.get(key),str) and bool(item[key].strip()),'observation.'+key+' is required')
        observed=timestamp(item.get('observed_at'));need(observed is not None,'observation.observed_at requires an offset timestamp')
        if observed and declared: need(observed >= declared,'observation precedes declaration')
        if enum(item.get('grade'), {'OBSERVED','REPORTED'}):
            need(isinstance(item.get('participant_code'),str) and bool(item['participant_code'].strip()),'direct observation needs participant_code')
    changes=record.get('changes') if isinstance(record.get('changes'),list) else []
    for change in changes:
        if not isinstance(change,dict): errors.append('change must be an object');continue
        for key in ['field','old','new','reason','approval_source','timing']:
            need(key in change and change[key] is not None,'change.'+key+' is required')
        need(timestamp(change.get('changed_at')) is not None,'change.changed_at requires an offset timestamp')
        need(enum(change.get('timing'), {'before_exposure','after_exposure','after_result_inspection'}),'change.timing is invalid')
        if enum(change.get('timing'), {'after_exposure','after_result_inspection'}):
            warnings.append('post-exposure criterion change: exploratory; human review and a prospective new test required for confirmation')
    decision=record.get('decision')
    if decision is not None:
        if not isinstance(decision,dict): errors.append('decision must be an object')
        else:
            need(enum(decision.get('recommendation'), {'CONTINUE','PIVOT','STOP'}),'decision requires exactly one recommendation')
            for key in ['scope','reason','counterevidence','missing_data','constraints','next_action','owner','reversal_evidence']:
                need(isinstance(decision.get(key),str) and bool(decision[key].strip()),'decision.'+key+' is required')
    warnings.append('Bookkeeping validation does not prove source authenticity, consent, execution, demand, statistical significance, or decision correctness.')
    return {'errors':errors,'warnings':warnings,'scope':'bookkeeping only; no automatic demand classification'}

def reject_constant(_): raise ValueError('non-finite JSON number')
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('record',type=Path);args=parser.parse_args()
    try:
        with args.record.open('rb') as stream: data=stream.read(MAX_BYTES+1)
        if len(data)>MAX_BYTES: raise ValueError('record exceeds 1 MiB limit')
        record=json.loads(data.decode('utf-8'),parse_constant=reject_constant)
        result=check(record)
    except (OSError,UnicodeError,ValueError,OverflowError,RecursionError):
        result={'errors':['Cannot read valid bounded UTF-8 JSON record'],'warnings':[],'scope':'bookkeeping only'}
    print(json.dumps(result,indent=2));return 1 if result['errors'] else 0
if __name__=='__main__': raise SystemExit(main())
