"""Exercise every Python output CLI against overwrite/symlink/private-mode risks."""
import sys
sys.dont_write_bytecode=True
import os,json,tempfile,subprocess,hashlib,stat
from pathlib import Path
from datetime import datetime
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from private_output import write_batch


def main():
 passed=0
 with tempfile.TemporaryDirectory(prefix='forensic-output-guards-') as temp:
  root=Path(temp);inp=root/'inputs';inp.mkdir(mode=0o700)
  (inp/'git.txt').write_text('');(inp/'emails.json').write_text('{"have_date":[]}')
  for n in ['email.json','pdf.json','derived.json']:(inp/n).write_text('[]')
  pdf=inp/'pdf';pdf.mkdir(mode=0o700);mail=inp/'mail';mail.mkdir(mode=0o700)
  (mail/'one.eml').write_text('From: reviewer@example.invalid\nTo: client@example.invalid\nDate: Tue, 06 Oct 2026 10:00:00 +0000\nMessage-ID: <fictional-1@example.invalid>\nSubject: Fixture\n\nFictional body for a private output guard test. No real people.\n')
  source=inp/'packet';source.mkdir(mode=0o700);(source/'fixture.txt').write_text('fictional input')
  def command(kind,out):
   defs={
    'git':('parse_git_log.py',['--input',inp/'git.txt','--out',out],out/'commits.json'),
    'invoices':('parse_invoices.py',['--processed-json',inp/'emails.json','--pdf-dir',pdf,'--email-vendor','Fictional A','--email-senders','reviewer@example.invalid','--pdf-vendor','Fictional B','--out',out],out/'invoice_texts.json'),
    'emails':('parse_emails.py',['--input-dirs',mail,'--out',out],out/'_intermediate/email-meta.json'),
    'xlsx':('build_invoice_xlsx.py',['--email-invoices',inp/'email.json','--pdf-invoices',inp/'pdf.json','--extrapolated',inp/'derived.json','--project-name','Fictional','--out',out/'report.xlsx'],out/'report.xlsx'),
    'derived':('extrapolate_recurring.py',['--email-invoices',inp/'email.json','--pdf-invoices',inp/'pdf.json','--out',out/'derived.json'],out/'derived.json'),
    'zip':('build_master_zip.py',['--src',source,'--project-name','Fictional','--out-dir',out],out/f"Fictional_Forensic_Packet_{datetime.now().strftime('%Y%m%d_%H%M')}.zip")}
   name,args,target=defs[kind];return [sys.executable,'-B',str(HERE/name),*map(str,args)],target
  def run(cmd):return subprocess.run(cmd,capture_output=True,text=True)
  def hashes(out):return {str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file()}
  for kind in ['git','invoices','emails','xlsx','derived','zip']:
   # Successful output; repeat must leave the first batch unchanged.
   out=root/(kind+'-positive');out.mkdir(mode=0o700);cmd,target=command(kind,out)
   result=run(cmd);assert result.returncode==0,(kind,result.stderr)
   files=hashes(out);assert files
   for p in [out,*out.rglob('*')]:assert stat.S_IMODE(p.stat().st_mode)==(0o700 if p.is_dir() else 0o600),(kind,str(p),oct(p.stat().st_mode))
   again=run(cmd);assert again.returncode!=0 and hashes(out)==files,(kind,again.stderr)
   passed+=1;print('PASS',kind,'positive/private modes/duplicate refusal')
   # Existing leaf symlink: outside sentinel untouched and zero earlier outputs.
   out=root/(kind+'-leaf');out.mkdir(mode=0o700);cmd,target=command(kind,out)
   target.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
   sentinel=root/(kind+'-sentinel');sentinel.write_text('unchanged');target.symlink_to(sentinel)
   result=run(cmd);assert result.returncode!=0 and sentinel.read_text()=='unchanged',(kind,result.stderr)
   assert [p for p in out.rglob('*') if p.is_file()]==[target],(kind,list(out.rglob('*')))
   passed+=1;print('PASS',kind,'leaf symlink/batch collision no earlier files')
   # Ancestor symlink points at a private outside directory; nothing is written there.
   outside=root/(kind+'-outside');outside.mkdir(mode=0o700);out=root/(kind+'-alias');out.symlink_to(outside,target_is_directory=True)
   cmd,_=command(kind,out);result=run(cmd);assert result.returncode!=0 and not list(outside.iterdir()),(kind,result.stderr)
   passed+=1;print('PASS',kind,'ancestor symlink refusal')
   # Never silently chmod an unsafe existing user directory.
   out=root/(kind+'-unsafe');out.mkdir(mode=0o755);os.chmod(out,0o755);cmd,_=command(kind,out)
   result=run(cmd);assert result.returncode!=0 and stat.S_IMODE(out.stat().st_mode)==0o755 and not list(out.iterdir()),(kind,result.stderr)
   passed+=1;print('PASS',kind,'unsafe directory refused without chmod')
  # Preserve the archive's earlier source/member symlink boundary.
  zipout=root/'zip-input-guard';zipout.mkdir(mode=0o700)
  (source/'linked.txt').symlink_to(inp/'git.txt')
  cmd,_=command('zip',zipout);result=run(cmd)
  assert result.returncode!=0 and not list(zipout.iterdir());passed+=1;print('PASS zip source member symlink refused')
  batch=root/'batch';batch.mkdir(mode=0o700);last=batch/'last.txt';last.write_text('original')
  try:write_batch({batch/'first.txt':'new',last:'overwrite'})
  except FileExistsError:pass
  else:raise AssertionError('batch must refuse')
  assert not (batch/'first.txt').exists() and last.read_text()=='original';passed+=1;print('PASS shared publisher all-target preflight')
 print(json.dumps({'passed':passed}))

if __name__=='__main__':main()
