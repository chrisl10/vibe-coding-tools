#!/usr/bin/env python3
"""Static archive/body/link checks only. Does not compile or execute Vue."""
from pathlib import Path
import hashlib, json, re
root = Path(__file__).resolve().parents[1]
ledger = json.loads((root / 'references/research/source-ledger.json').read_text())
source_map = {row['id']: row for row in ledger['sources']}
for row in ledger['sources']:
    data = (root / 'references/research' / row['raw']).read_bytes()
    body = data.split(b'\n\n', 1)[1]
    assert hashlib.sha256(data).hexdigest() == row['archive_sha256'], row['id']
    assert hashlib.sha256(body).hexdigest() == row['body_sha256'], row['id']
    assert row['url'].startswith(('https://vuejs.org/', 'https://router.vuejs.org/', 'https://test-utils.vuejs.org/'))
    assert row['retrieved_at'] and row['body_bytes'] == len(body)
claims = json.loads((root / 'references/research/body-claims.json').read_text())
for claim in claims:
    path = root / 'references/research' / source_map[claim['source_id']]['raw']
    assert claim['quote'] in path.read_text().split('\n\n', 1)[1], claim
checked_links = 0
for path in root.rglob('*.md'):
    content = path.read_text()
    # Local authored prose links, excluding code fences and remote source links.
    content = re.sub(r'```.*?```', '', content, flags=re.S)
    for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', content):
        if '://' in target: continue
        target = target.split('#', 1)[0]
        if not target: continue
        assert (path.parent / target).exists(), (path, target)
        checked_links += 1
print(json.dumps({'status': 'PASS', 'sources': len(source_map), 'body_claims': len(claims),
                  'local_links': checked_links, 'scope': 'archive hashes, exact source body anchors and authored Markdown links',
                  'vue_runtime': 'NOT_RUN', 'sfc_compile': 'NOT_RUN', 'typecheck': 'NOT_RUN'}))
