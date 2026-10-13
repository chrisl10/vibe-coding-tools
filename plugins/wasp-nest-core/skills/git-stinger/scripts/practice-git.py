#!/usr/bin/env python3
"""Exercise basic Git only in a newly created disposable synthetic repository."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

class PracticeError(Exception):
    pass

def isolated_environment():
    env={key:value for key,value in os.environ.items() if not key.startswith('GIT_')}
    env.update({'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':os.devnull,'GIT_TERMINAL_PROMPT':'0','LC_ALL':'C'})
    return env

def exercise():
    git=shutil.which('git')
    if not git: raise PracticeError('Existing Git executable is unavailable; no installation performed.')
    env=isolated_environment()
    version=subprocess.run([git,'--version'],env=env,capture_output=True,text=True,timeout=10)
    if version.returncode: raise PracticeError('Existing Git version check failed.')
    match=re.search(r'(\d+)\.(\d+)',version.stdout)
    if not match or tuple(map(int,match.groups())) < (2,23):
        raise PracticeError('Practice requires installed Git 2.23 or newer for switch and restore; no installation performed.')
    checks={};transcript=[]
    with tempfile.TemporaryDirectory(prefix='wasp-git-practice-') as directory:
        created=Path(directory).resolve();repo=created/'repo';repo.mkdir();hooks=created/'empty-hooks';hooks.mkdir();templates=created/'empty-template';templates.mkdir()
        def run(*args):
            if not repo.is_dir() or repo.parent.resolve()!=created:
                raise PracticeError('Practice directory ownership check failed.')
            command=[git,'-c','user.name=Practice','-c','user.email=practice@example.invalid','-c','commit.gpgSign=false','-c','tag.gpgSign=false','-c','core.hooksPath='+str(hooks),*args]
            result=subprocess.run(command,cwd=repo,env=env,capture_output=True,text=True,timeout=10)
            transcript.append({'git_arguments':list(args),'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
            if result.returncode: raise PracticeError('Synthetic Git command failed: '+args[0]+'; '+result.stderr.strip())
            return result.stdout
        run('init','--template='+str(templates),'.');run('symbolic-ref','HEAD','refs/heads/practice')
        note=repo/'note.txt';note.write_bytes(b'first draft\n')
        checks['untracked_status']=run('status','--porcelain')=='?? note.txt\n'
        run('add','--','note.txt')
        checks['staged_addition']='+first draft' in run('diff','--cached','--no-ext-diff','--no-textconv','--','note.txt')
        run('commit','-m','practice: first snapshot');baseline=run('rev-parse','HEAD').strip()
        checks['clean_commit']=run('status','--porcelain')==''
        note.write_bytes(b'second draft\n')
        checks['unstaged_change']='+second draft' in run('diff','--no-ext-diff','--no-textconv','--','note.txt')
        run('add','--','note.txt')
        checks['staged_change']='+second draft' in run('diff','--cached','--no-ext-diff','--no-textconv','--','note.txt')
        run('restore','--staged','--','note.txt')
        checks['unstage_preserves_working_bytes']=note.read_bytes()==b'second draft\n' and run('diff','--cached','--no-ext-diff','--no-textconv','--','note.txt')==''
        backup=created/'note-byte-backup.txt';backup.write_bytes(note.read_bytes())
        run('restore','--worktree','--','note.txt')
        checks['restore_preserves_backup']=note.read_bytes()==b'first draft\n' and backup.read_bytes()==b'second draft\n'
        if run('status','--porcelain')!='':raise PracticeError('Synthetic tree unexpectedly dirty before branch lesson.')
        run('switch','-c','lesson');note.write_bytes(b'lesson draft\n');run('add','--','note.txt');run('commit','-m','practice: lesson snapshot')
        run('switch','practice')
        checks['branch_keeps_baseline']=note.read_bytes()==b'first draft\n' and run('rev-parse','HEAD').strip()==baseline
        checks['branch_pointers_visible']='lesson' in run('branch','--list')
        run('switch','--detach','lesson');note.write_bytes(b'detached draft\n');run('add','--','note.txt');run('commit','-m','practice: detached snapshot');detached=run('rev-parse','HEAD').strip()
        run('switch','practice');reflog=run('reflog','--format=%H').splitlines()
        checks['reflog_contains_detached_commit']=detached in reflog
        checks['reflog_commit_inspected']=run('show',detached+':note.txt')=='detached draft\n'
        run('branch','recovered',detached);run('switch','recovered')
        checks['recovered_branch_has_expected_bytes']=note.read_bytes()==b'detached draft\n' and run('rev-parse','HEAD').strip()==detached
        checks['final_clean_status']=run('status','--porcelain')==''
        checks['no_remotes']=run('remote')==''
        result={'scope':'synthetic disposable repository only','git_version':version.stdout.strip(),'checks':checks,'passed':all(checks.values()),'transcript':transcript,'cleanup':'only task-created temporary directory removed after report capture','limitations':'Does not prove learner comprehension or safety/correctness of any user-repository recovery.'}
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',action='store_true',help='Run synthetic local commits in a newly created disposable repository.')
    args=parser.parse_args()
    if not args.run:
        parser.print_help();return 0
    try: result=exercise()
    except (PracticeError,OSError,subprocess.TimeoutExpired) as error:
        print(json.dumps({'passed':False,'scope':'synthetic disposable repository only','error':str(error)}));return 1
    print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
