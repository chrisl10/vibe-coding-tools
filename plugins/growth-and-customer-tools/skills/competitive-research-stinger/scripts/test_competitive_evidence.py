import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
spec=importlib.util.spec_from_file_location('competitive_evidence',Path(__file__).with_name('competitive_evidence.py')); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def fixture():
    values={'eligible_accounts':'1000','reachable_fraction':'0.2','conversion_fraction':'0.1','capacity_accounts':'12','annual_price_per_account':'1200'}
    return {'as_of':'2026-10-07','sources':[{'id':'vendor-a','url':'https://vendor.example/product','retrieved':'2026-10-01','kind':'vendor','archive':'vendor.txt','sha256':hashlib.sha256(b'fixture').hexdigest(),'freshness_days':30}], 'claims':[{'id':'feature-a','classification':'vendor_claim','statement':'Hypothetical vendor states feature A','source_ids':['vendor-a'],'scope':'Vendor statement only; no execution proof'}], 'scenarios':[{'id':'hypothetical-a','currency':'USD','horizon_months':12,'inputs':{k:{'value':v,'basis':'assumed','source_ids':[],'rationale':'Hypothetical test value, not market evidence'} for k,v in values.items()}}]}

class EvidenceChecks(unittest.TestCase):
    def check_bad(self,edit):
        d=fixture(); edit(d)
        with self.assertRaises(m.InputError): m.validate(d,Path('.'))
    def test_capacity_arithmetic(self):
        r=m.validate(fixture(),Path('.'))['scenarios'][0]; self.assertEqual(m.Decimal(r['served_accounts']),12); self.assertEqual(m.Decimal(r['annualized_revenue']),14400)
    def test_unknown_not_zero(self):
        d=fixture(); v=d['scenarios'][0]['inputs']['reachable_fraction']; v.update(value=None,basis='unknown'); r=m.validate(d,Path('.'))['scenarios'][0]; self.assertEqual(r['status'],'incomplete'); self.assertNotIn('annualized_revenue',r)
    def test_vendor_cannot_be_observed(self): self.check_bad(lambda d:d['claims'][0].update(classification='observed'))
    def test_observation_schema_is_not_truth_grade(self):
        d=fixture(); d['sources'][0]['kind']='observation'; d['claims'][0]['classification']='observed'; self.assertEqual(m.validate(d,Path('.'))['status'],'consistent')
    def test_future_source(self): self.check_bad(lambda d:d['sources'][0].update(retrieved='2026-10-08'))
    def test_stale_warns(self):
        d=fixture(); d['sources'][0]['freshness_days']=2; self.assertEqual(m.validate(d,Path('.'))['warnings'][0]['status'],'stale')
    def test_missing_source_reference(self): self.check_bad(lambda d:d['claims'][0].update(source_ids=['absent']))
    def test_measured_needs_evidence(self): self.check_bad(lambda d:d['scenarios'][0]['inputs']['eligible_accounts'].update(basis='measured'))
    def test_fraction_over_one(self): self.check_bad(lambda d:d['scenarios'][0]['inputs']['reachable_fraction'].update(value='1.01'))
    def test_negative_value(self): self.check_bad(lambda d:d['scenarios'][0]['inputs']['capacity_accounts'].update(value='-1'))
    def test_extreme_exponent(self): self.check_bad(lambda d:d['scenarios'][0]['inputs']['eligible_accounts'].update(value='1e999999'))
    def test_boolean_horizon(self): self.check_bad(lambda d:d['scenarios'][0].update(horizon_months=True))
    def test_duplicate_ids(self): self.check_bad(lambda d:d['sources'].append(copy.deepcopy(d['sources'][0])))
    def test_path_traversal(self): self.check_bad(lambda d:d['sources'][0].update(archive='../private.txt'))
    def test_hash_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'vendor.txt').write_bytes(b'fixture'); self.assertEqual(m.validate(fixture(),root,True)['sources'],1)
            (root/'vendor.txt').write_bytes(b'changed')
            with self.assertRaisesRegex(m.InputError,'archive hash mismatch'): m.validate(fixture(),root,True)
    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'run'; root.mkdir(); target=Path(tmp)/'outside'; target.write_bytes(b'fixture'); (root/'vendor.txt').symlink_to(target)
            with self.assertRaisesRegex(m.InputError,'escapes'): m.validate(fixture(),root,True)
    def test_cli_duplicate_keys_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'input.json'; p.write_text('{"as_of":"2026-10-07","as_of":"2026-10-07"}')
            r=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('competitive_evidence.py')),str(p)],capture_output=True,text=True)
            self.assertEqual(r.returncode,2); self.assertEqual(r.stdout,''); self.assertIn('duplicate JSON key',r.stderr); self.assertNotIn('Traceback',r.stderr)
    def test_cli_good(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'input.json'; p.write_text(json.dumps(fixture())); r=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('competitive_evidence.py')),str(p)],capture_output=True,text=True); self.assertEqual(r.returncode,0); self.assertEqual(json.loads(r.stdout)['status'],'consistent')

if __name__=='__main__': unittest.main()
