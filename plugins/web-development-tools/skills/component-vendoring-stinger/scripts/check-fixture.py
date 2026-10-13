#!/usr/bin/env python3
"""Bounded synthetic notice/hash checks; not a target license scanner."""
from pathlib import Path
import hashlib,json,tempfile,shutil
base=Path(__file__).resolve().parents[1]/'examples'
def inspect(root,manifest):
    errors=[]
    if not (root/manifest['license_path']).is_file(): errors.append('missing license')
    for group in ('files','protected_notices'):
        for entry in manifest[group]:
            p=root/entry['path']
            if not p.is_file(): errors.append('missing '+entry['path'])
            elif hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']: errors.append('hash drift '+entry['path'])
    return errors
manifest=json.loads((base/'fictional-provenance.json').read_text())
assert not inspect(base,manifest)
results={'intact_fixture':'PASS'}
for name,target,operation,expected in [('removed_notice','fixture/LICENSE.txt','delete','missing license'),('modified_notice','fixture/LICENSE.txt','change','hash drift fixture/LICENSE.txt'),('source_drift','fixture/component.txt','change','hash drift fixture/component.txt')]:
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);shutil.copytree(base/'fixture',root/'fixture');p=root/target
        if operation=='delete': p.unlink()
        else: p.write_text(p.read_text()+'changed\n')
        assert expected in inspect(root,manifest)
        results[name]='REJECTED_AS_EXPECTED'
print(json.dumps({'scope':'synthetic fixture only','cases':results},indent=2))
