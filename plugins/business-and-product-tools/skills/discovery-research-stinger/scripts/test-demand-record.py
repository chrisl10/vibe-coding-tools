import copy
import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('checker',Path(__file__).with_name('check-demand-record.py'))
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)

def fixture():
    return {'schema_version':1,'status':'planned',**{key:'recorded '+key for key in checker.TEXT},'planned_start':'2026-10-07T10:00:00-04:00','planned_end':'2026-10-08T10:00:00-04:00','budget_limit':0,'metric':{key:'defined '+key for key in ['name','unit','numerator_definition','denominator_definition','time_window']},'criterion':{'version':1,'declared_at':'2026-10-07T09:00:00-04:00','operator':'>=','threshold':3,'minimum_exposures':6,'stop_rule':'end at declared deadline'},'feasibility_constraints':['owner time'],'observations':[],'changes':[],'source_paths':[],'decision':None}

class Bookkeeping(unittest.TestCase):
    def test_nonstring_enums_are_controlled_errors(self):
        for value in [[],{},True,None,1]:
            for field in ['status','operator','grade','timing','recommendation']:
                with self.subTest(field=field,value=value):
                    f=fixture()
                    if field=='status':f['status']=value
                    elif field=='operator':f['criterion']['operator']=value
                    elif field=='grade':f['observations']=[{'grade':value}]
                    elif field=='timing':f['changes']=[{'timing':value}]
                    else:f['decision']={'recommendation':value}
                    self.assertTrue(checker.check(f)['errors'])
    def test_cli_unhashable_enum_has_no_traceback(self):
        import json,subprocess,sys,tempfile
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'bad.json';f=fixture();f['status']=[];path.write_text(json.dumps(f))
            result=subprocess.run([sys.executable,str(Path(__file__).with_name('check-demand-record.py')),str(path)],capture_output=True,text=True,timeout=5)
            self.assertEqual(result.returncode,1);self.assertEqual(result.stderr,'')
            self.assertTrue(json.loads(result.stdout)['errors'])
    def test_valid_plan_is_not_execution_proof(self):
        r=checker.check(fixture());self.assertFalse(r['errors']);self.assertTrue(any('does not prove' in w for w in r['warnings']))
    def test_required_fields(self):
        for key in checker.TEXT:
            with self.subTest(key=key):
                f=fixture();f[key]='';self.assertTrue(checker.check(f)['errors'])
    def test_invalid_top_level(self):
        for f in [[],None,'text',1]:self.assertTrue(checker.check(f)['errors'])
    def test_non_finite_or_bool(self):
        for value in [True,float('inf'),float('nan'),10**1000]:
            f=fixture();f['criterion']['threshold']=value;self.assertTrue(checker.check(f)['errors'])
    def test_declaration_after_exposure(self):
        f=fixture();f['criterion']['declared_at']='2026-10-07T11:00:00-04:00';self.assertTrue(checker.check(f)['errors'])
    def test_naive_timestamp(self):
        f=fixture();f['criterion']['declared_at']='2026-10-07T09:00:00';self.assertTrue(checker.check(f)['errors'])
    def test_execution_without_sources(self):
        f=fixture();f['status']='executed';self.assertTrue(checker.check(f)['errors'])
    def test_observation_in_planned_record(self):
        f=fixture();f['observations']=[{}];self.assertTrue(checker.check(f)['errors'])
    def test_observed_result_needs_participant(self):
        f=fixture();f['status']='executed';f['source_paths']=['local notes'];f['observations']=[{'grade':'OBSERVED','source':'notes','claim':'task completed','relevance':'declared task','observed_at':'2026-10-07T12:00:00-04:00'}];self.assertTrue(checker.check(f)['errors'])
    def test_post_result_change_is_flagged_not_reclassified(self):
        f=fixture();f['changes']=[{'field':'threshold','old':3,'new':1,'reason':'reconsidered','approval_source':'owner note','timing':'after_result_inspection','changed_at':'2026-10-07T12:00:00-04:00'}];r=checker.check(f);self.assertFalse(r['errors']);self.assertTrue(any('exploratory' in w for w in r['warnings']))
    def test_decision_does_not_choose_itself(self):
        for choice in ['CONTINUE','PIVOT','STOP']:
            f=fixture();f['decision']={key:'human explanation' for key in ['scope','reason','counterevidence','missing_data','constraints','next_action','owner','reversal_evidence']};f['decision']['recommendation']=choice;self.assertFalse(checker.check(f)['errors'])
    def test_multiple_decisions_rejected(self):
        f=fixture();f['decision']={'recommendation':'CONTINUE or PIVOT'};self.assertTrue(checker.check(f)['errors'])
    def test_empty_constraints_field(self):
        f=fixture();f['feasibility_constraints']='none';self.assertTrue(checker.check(f)['errors'])
    def test_invalid_change_shape(self):
        f=fixture();f['changes']=['threshold changed'];self.assertTrue(checker.check(f)['errors'])
    def test_source_status_unknown(self):
        f=fixture();f['status']='validated';self.assertTrue(checker.check(f)['errors'])
    def test_invalid_metric_shape(self):
        f=fixture();f['metric']=None;self.assertTrue(checker.check(f)['errors'])
    def test_bool_minimum(self):
        f=fixture();f['criterion']['minimum_exposures']=True;self.assertTrue(checker.check(f)['errors'])
    def test_reversed_date(self):
        f=fixture();f['planned_end']='2026-10-06T09:00:00Z';self.assertTrue(checker.check(f)['errors'])
if __name__=='__main__':unittest.main()
