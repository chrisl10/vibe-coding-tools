import json,pathlib,subprocess,tempfile,unittest,gzip
ROOT=pathlib.Path(__file__).resolve().parents[5]
HELPER=pathlib.Path(__file__).with_name('bundle-budget-check.ts')
class BundleCases(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=pathlib.Path(self.tmp.name);self.build=self.root/'dist';self.build.mkdir();self.manifest=self.root/'manifest.json'
  for name,data in [('main.js',b'console.log("main");'),('shared.js',b'export const shared=1;'),('lazy.js',b'console.log("lazy");')]: (self.build/name).write_bytes(data)
  self.data={'src/main.tsx':{'file':'main.js','isEntry':True,'imports':['shared','shared'],'dynamicImports':['lazy']},'shared':{'file':'shared.js'},'lazy':{'file':'lazy.js'}}
 def run_helper(self,*extra):
  self.manifest.write_text(json.dumps(self.data));return subprocess.run(['node',str(HELPER),str(self.build),str(self.manifest),'src/main.tsx',*extra],capture_output=True,text=True,timeout=10)
 def test_graph_dedup_and_dynamic(self):
  p=self.run_helper();self.assertEqual(p.returncode,0,p.stderr);r=json.loads(p.stdout);self.assertEqual(r['staticAssetCount'],2);self.assertEqual(r['dynamicEntries'],['lazy']);self.assertEqual(r['verdict'],'MEASURED_NO_BUDGET');self.assertEqual(r['gzipBytes'],sum(len(gzip.compress((self.build/x).read_bytes(),compresslevel=9,mtime=0)) for x in ['main.js','shared.js']))
 def test_budget_exceeded(self):self.assertEqual(self.run_helper('0.001').returncode,1)
 def test_budget_within(self):self.assertEqual(json.loads(self.run_helper('100').stdout)['verdict'],'WITHIN_BUDGET')
 def test_malformed_budget(self):self.assertEqual(self.run_helper('nan').returncode,2)
 def test_invalid_import(self):self.data['src/main.tsx']['imports']=['missing'];self.assertEqual(self.run_helper().returncode,2)
 def test_unsafe_path(self):self.data['shared']['file']='../private.js';self.assertEqual(self.run_helper().returncode,2)
 def test_symlink_escape(self):
  outside=self.root/'private.js';outside.write_text('private');(self.build/'shared.js').unlink();(self.build/'shared.js').symlink_to(outside);p=self.run_helper();self.assertEqual(p.returncode,2);self.assertNotIn('private',p.stderr)
 def test_missing_file(self):(self.build/'shared.js').unlink();self.assertEqual(self.run_helper().returncode,2)
 def test_bad_import_list(self):self.data['src/main.tsx']['imports']={};self.assertEqual(self.run_helper().returncode,2)
 def test_entry_required(self):self.data['src/main.tsx']['isEntry']=False;self.assertEqual(self.run_helper().returncode,2)
 def test_cycle_deduplicates(self):self.data['shared']['imports']=['src/main.tsx'];self.assertEqual(json.loads(self.run_helper().stdout)['staticAssetCount'],2)
 def test_legacy_is_unverified(self):
  p=subprocess.run(['node',str(HELPER),str(self.build)],capture_output=True,text=True,timeout=10);self.assertEqual(p.returncode,2);self.assertIn('UNVERIFIED',p.stderr);self.assertNotIn('PASS',p.stdout)
if __name__=='__main__':unittest.main()
