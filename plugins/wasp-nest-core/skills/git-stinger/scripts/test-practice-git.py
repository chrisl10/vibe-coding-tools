import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT=Path(__file__).with_name('practice-git.py')
spec=importlib.util.spec_from_file_location('practice',SCRIPT);practice=importlib.util.module_from_spec(spec);spec.loader.exec_module(practice)

class PracticeBoundaries(unittest.TestCase):
    def test_filters_inherited_git_routes(self):
        with patch.dict(os.environ,{'GIT_DIR':'outside','GIT_WORK_TREE':'outside','GIT_INDEX_FILE':'outside','GIT_CONFIG_COUNT':'1','GIT_CONFIG_KEY_0':'user.name','GIT_CONFIG_VALUE_0':'outside','GIT_SSH_COMMAND':'outside'}):
            env=practice.isolated_environment()
            self.assertFalse(any(k in env for k in ['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_CONFIG_COUNT','GIT_CONFIG_KEY_0','GIT_CONFIG_VALUE_0','GIT_SSH_COMMAND']))
            self.assertEqual(env['GIT_CONFIG_GLOBAL'],os.devnull);self.assertEqual(env['GIT_CONFIG_NOSYSTEM'],'1')
    def test_existing_caller_files_remain_untouched_with_hostile_routes(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);sentinel=root/'caller.txt';sentinel.write_bytes(b'caller-owned bytes\x00\xff')
            before={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            with patch.dict(os.environ,{'GIT_DIR':str(root/'wrong.git'),'GIT_WORK_TREE':str(root),'GIT_INDEX_FILE':str(root/'wrong-index'),'GIT_CONFIG_GLOBAL':str(root/'wrong-config')}):
                result=practice.exercise()
            after={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(before,after);self.assertTrue(result['passed']);self.assertTrue(result['checks']['no_remotes'])
    def test_missing_git_stops_without_installation(self):
        with patch.object(practice.shutil,'which',return_value=None):
            with self.assertRaisesRegex(practice.PracticeError,'no installation performed'):practice.exercise()
    def test_unsupported_version_stops(self):
        with patch.object(practice.subprocess,'run',return_value=subprocess.CompletedProcess([],0,'git version 2.22.0','')):
            with self.assertRaisesRegex(practice.PracticeError,'2.23 or newer'):practice.exercise()
    def test_no_repo_argument_or_arbitrary_target(self):
        result=subprocess.run([sys.executable,str(SCRIPT),'--repo','unowned'],capture_output=True,text=True)
        self.assertEqual(result.returncode,2);self.assertIn('unrecognized arguments',result.stderr)
    def test_no_run_only_help(self):
        result=subprocess.run([sys.executable,str(SCRIPT)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0);self.assertIn('--run',result.stdout)
if __name__=='__main__':unittest.main()
