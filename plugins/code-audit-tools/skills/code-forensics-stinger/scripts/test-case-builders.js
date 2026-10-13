'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { validateCaseFacts, DOCUMENT_KINDS } = require('./case-input');
const { renderMarkdown, FICTIONAL_NOTICE, REVIEW_NOTICE } = require('./render-case-document');
const fixture = JSON.parse(fs.readFileSync(path.join(__dirname, '../examples/example-case-a/case-facts.json'), 'utf8'));
const work = fs.mkdtempSync(path.join(os.tmpdir(), 'forensic-builders-'));
let count = 0;
const check = (label, operation) => { operation(); count++; process.stdout.write(`PASS ${label}\n`); };
const clone = () => JSON.parse(JSON.stringify(fixture));
const input = path.join(work, 'case.json');
fs.writeFileSync(input, JSON.stringify(fixture));
const entries = { master: 'build_master_report.js', agency: 'build_agency_report.js', attorney: 'build_attorney_memo.js', plain_language: 'build_plain_language.js', pre_litigation: 'build_pre_litigation.js' };
function invoke(kind, args) { return spawnSync(process.execPath, [path.join(__dirname, entries[kind]), ...args], { cwd: work, encoding: 'utf8', env: process.env }); }
function refuse(label, args, pattern = /Case document refused:/) {
 check(label, () => { const result = invoke('master', args); assert.equal(result.status, 1, result.stdout + result.stderr); assert.match(result.stderr, pattern); });
}
for (const kind of DOCUMENT_KINDS) {
 check(`${kind} missing input creates no directory`, () => {
  const out = path.join(work, `absent-${kind}`); const result = invoke(kind, ['--case-facts', path.join(work, 'missing.json'), '--out-dir', out]);
  assert.equal(result.status, 1); assert.equal(fs.existsSync(out), false);
 });
 check(`${kind} selected document required`, () => {
  const facts = clone(); delete facts.documents[kind]; const file = path.join(work, `missing-${kind}.json`); fs.writeFileSync(file, JSON.stringify(facts));
  const out = path.join(work, `selected-${kind}`); const result = invoke(kind, ['--case-facts', file, '--out-dir', out]);
  assert.equal(result.status, 1); assert.match(result.stderr, /missing selected document/); assert.equal(fs.existsSync(out), false);
 });
 for (const format of ['markdown', 'docx']) check(`${kind} actual ${format} output and no overwrite`, () => {
  const out = path.join(work, `${kind}-${format}`); const args = ['--case-facts', input, '--out-dir', out, '--format', format]; const result = invoke(kind, args);
  assert.equal(result.status, 0, result.stderr); const meta = JSON.parse(result.stdout); const bytes = fs.readFileSync(meta.output);
  if (format === 'docx') assert.equal(bytes.subarray(0, 2).toString(), 'PK');
  else { assert.match(bytes.toString(), /FICTIONAL TRAINING EXAMPLE/); assert.match(bytes.toString(), /ESTIMATE/); }
  assert.equal(fs.statSync(meta.output).mode & 0o777, 0o600); assert.equal(fs.statSync(out).mode & 0o777, 0o700);
  const again = invoke(kind, args); assert.equal(again.status, 1); assert.match(again.stderr, /refusing overwrite/); assert.deepEqual(fs.readFileSync(meta.output), bytes);
  assert.equal(fs.readdirSync(out).length, 1);
 });
}
for (const [label, change] of [
 ['unknown root key', v => { v.unexpected = true; }],
 ['missing fictional flag', v => { delete v.fictional; }],
 ['invalid real date', v => { v.matter.report_date = '2026-02-30'; }],
 ['unsafe matter id', v => { v.matter.id = '../other'; }],
 ['duplicate evidence id', v => { v.evidence.push(v.evidence[0]); }],
 ['unknown source', v => { v.documents.master.sections[0].blocks[0].source_ids = ['E-99']; }],
 ['duplicate source', v => { v.documents.master.sections[0].blocks[0].source_ids = ['E-01','E-01']; }],
 ['PROVEN without citation', v => { v.documents.master.sections[0].blocks[0].source_ids = []; }],
 ['PROVEN estimate', v => { v.documents.master.sections[0].blocks[0].estimate = true; }],
 ['unknown evidence tier', v => { v.documents.master.sections[0].blocks[0].tier = 'VERIFIED'; }],
 ['table width mismatch', v => { v.documents.master.sections[0].blocks[2].rows[0].pop(); }],
 ['control text', v => { v.matter.title = '\u0000bad'; }],
 ['invalid Unicode', v => { v.matter.title = '\ud800'; }],
 ['empty text', v => { v.matter.title = ' '; }],
 ['too many evidence entries', v => { v.evidence = Array(1001).fill(v.evidence[0]); }],
 ['no documents', v => { v.documents = {}; }]
]) check(label, () => { const facts = clone(); change(facts); assert.throws(() => validateCaseFacts(facts)); });
refuse('missing CLI arguments', []);
refuse('duplicate CLI flag', ['--case-facts', input, '--case-facts', input, '--out-dir', work]);
refuse('unknown format', ['--case-facts', input, '--out-dir', work, '--format', 'pdf']);
const symlink = path.join(work, 'alias.json'); fs.symlinkSync(input, symlink);
refuse('symlink input', ['--case-facts', symlink, '--out-dir', path.join(work, 'out-alias')], /symlink path refused/);
const target = path.join(work, 'target'); fs.mkdirSync(target); const alias = path.join(work, 'alias'); fs.symlinkSync(target, alias);
refuse('symlink output', ['--case-facts', input, '--out-dir', alias], /symlink path refused/);
refuse('traversal output', ['--case-facts', input, '--out-dir', path.join(work,'nested') + '/../outside']);
const oversized = path.join(work, 'oversized.json'); fs.writeFileSync(oversized, Buffer.alloc(2*1024*1024+1));
refuse('oversized input', ['--case-facts', oversized, '--out-dir', path.join(work, 'oversized')]);
const invalid = path.join(work, 'invalid.json'); fs.writeFileSync(invalid, '{');
refuse('invalid JSON', ['--case-facts', invalid, '--out-dir', path.join(work, 'invalid')]);
const utf = path.join(work, 'invalid-utf.json'); fs.writeFileSync(utf, Buffer.from([0xff]));
refuse('invalid UTF-8', ['--case-facts', utf, '--out-dir', path.join(work, 'invalid-utf')]);
const linkedOut = path.join(work,'destination-symlink'); fs.mkdirSync(linkedOut,{mode:0o700});
const protectedFile = path.join(work,'protected.txt'); fs.writeFileSync(protectedFile,'unchanged');
fs.symlinkSync(protectedFile,path.join(linkedOut,'fictional-workshop-master.md'));
refuse('symlink destination cannot overwrite target',['--case-facts',input,'--out-dir',linkedOut,'--format','markdown'],/refusing overwrite/);
check('symlink target preserved',()=>assert.equal(fs.readFileSync(protectedFile,'utf8'),'unchanged'));
const unsafeOut=path.join(work,'unsafe-existing'); fs.mkdirSync(unsafeOut,{mode:0o755}); fs.chmodSync(unsafeOut,0o755);
refuse('unsafe existing directory refused',['--case-facts',input,'--out-dir',unsafeOut],/user-owned mode 0700/);
check('unsafe directory unchanged',()=>{assert.equal(fs.statSync(unsafeOut).mode & 0o777,0o755);assert.equal(fs.readdirSync(unsafeOut).length,0);});
check('case isolation and no retained defaults', () => {
 const other = clone(); other.fictional = false; other.matter.id = 'another-case'; other.matter.client = 'Independent client';
 for (const doc of Object.values(other.documents)) for (const section of doc.sections) for (const block of section.blocks) {
  if (block.text) block.text = 'Independent supplied text'; if (block.items) block.items = ['Independent item']; if (block.rows) block.rows = [['Independent cell','3']];
 }
 const rendered = renderMarkdown(validateCaseFacts(other), 'master'); assert.match(rendered, /Independent client/); assert.doesNotMatch(rendered, /Meadow Workshop|Vendor A/); assert.doesNotMatch(rendered, new RegExp(FICTIONAL_NOTICE));
});
check('review and hypothesis labels', () => { for (const kind of ['attorney','pre_litigation']) { const text=renderMarkdown(fixture,kind); assert.match(text,/DRAFT FOR HUMAN\/COUNSEL REVIEW/); assert.match(text,/No legal conclusions or privilege status/); assert.match(text,/HYPOTHESIS/); } });
check('Markdown raw HTML cannot execute', () => { const facts=clone(); facts.documents.master.sections[0].blocks[0].text='<script>alert(1)</script>'; const text=renderMarkdown(facts,'master'); assert.doesNotMatch(text,/<script>/); assert.match(text,/&lt;script&gt;/); });
process.stdout.write(JSON.stringify({ passed: count, artifactDirectory: work }) + '\n');
