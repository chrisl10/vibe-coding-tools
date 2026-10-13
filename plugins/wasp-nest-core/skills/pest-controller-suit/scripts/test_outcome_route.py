import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('outcome_route',Path(__file__).with_name('outcome-route.py'))
route=importlib.util.module_from_spec(spec);spec.loader.exec_module(route)

class OutcomeDiscovery(unittest.TestCase):
    def setUp(self):
        self.data={'outcomes':[
            {'id':'O001','outcome':'Understand a technical post','bucket':'Learning','bucket_id':'B01','capability_group':'technical-explainer','state':'PROPOSED'},
            {'id':'O031','outcome':'Set a SaaS price','bucket':'Business math','bucket_id':'B03','capability_group':'saas-pricing','state':'PROPOSED'},
            {'id':'O106','outcome':'Improve a repository','bucket':'Repository health','bucket_id':'B08','capability_group':'repo-modernization','state':'PROPOSED'}]}
    def test_explanation_alias(self):
        result=route.discover(self.data,'explain technical post')
        self.assertEqual(result['candidates'][0]['id'],'O001')
        self.assertEqual(result['candidates'][0]['state'],'PROPOSED')
        self.assertIn('unverified',result['availability'])
    def test_repo_alias(self):self.assertEqual(route.discover(self.data,'improve my repo')['candidates'][0]['id'],'O106')
    def test_bucket_boundary(self):self.assertEqual(route.discover(self.data,'SaaS price',bucket='B01')['candidates'],[])
    def test_unmatched_does_not_invent(self):self.assertEqual(route.discover(self.data,'quantum telescope')['candidates'],[])
    def test_bad_input(self):
        for query in ('',' '*3,'x'*2001,None):
            with self.subTest(query=repr(query)[:20]),self.assertRaises(ValueError):route.discover(self.data,query)
    def test_limit(self):
        for value in (0,21,True,1.5):
            with self.subTest(value=value),self.assertRaises(ValueError):route.discover(self.data,'price',value)
    def test_no_state_promotion(self):self.assertEqual(route.discover(self.data,'price')['candidates'][0]['state'],'PROPOSED')

if __name__=='__main__':unittest.main()
