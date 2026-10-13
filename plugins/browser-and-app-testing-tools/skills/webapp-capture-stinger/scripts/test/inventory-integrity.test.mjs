import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync, execFileSync } from 'node:child_process';
import { redactCapture, redactText } from '../lib/redaction.mjs';
import { validateTheme, safeMember } from '../inventory/validation.mjs';
const scripts = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const catalog = JSON.parse(fs.readFileSync(path.join(scripts, '../references/shadcn-catalog.json')));
const theme = () => ({ capturedTheme:'dark', themes:{dark:Object.fromEntries(catalog.themeTokens.filter(k=>k!=='radius').map(k=>[k,{value:'#123456',source:'measured',reason:'observed role'}])),light:null},radius:{value:'8px',reason:'observed'},fonts:{sans:'Inter',mono:'monospace',icons:'none observed'},customTokens:[],decisions:[],gaps:['No light capture'] });
const scratch = () => fs.mkdtempSync(path.join(os.tmpdir(), 'inventory-integrity-'));
const put = (p,v) => { fs.mkdirSync(path.dirname(p), {recursive:true,mode:0o700}); fs.writeFileSync(p, typeof v==='string'||Buffer.isBuffer(v)?v:JSON.stringify(v), {mode:0o600}); };
const run = (file, env) => spawnSync(process.execPath,[path.join(scripts, file)],{env:{...process.env, CAPTURE_CONFIG:'',...env},encoding:'utf8'});
test('redacts every metadata string and key, encoded secrets and URL values',()=>{
 const cfg={redact:{patterns:['secretword']}};
 const value=redactCapture(cfg,{secretword:'secretword',title:'secretword',css:'url(https://user:pass@example.test/a?token=other#private)',nested:[{label:'%73ecretword',html:'<input value="private" data-token="private">'}],apiKey:'not-a-pattern'});
 const text=JSON.stringify(value); assert.ok(!text.includes('secretword')); assert.ok(!text.includes('private')); assert.ok(!text.includes('user:pass')); assert.ok(!text.includes('not-a-pattern')); assert.match(text,/REDACTED/);
 assert.equal(redactText(cfg,'/a?name=private&x=stuff'),'/a?name=[REDACTED]&x=[REDACTED]');
 assert.throws(()=>redactCapture(cfg,{secretword:1,'[REDACTED]':2}),/duplicate/);
 assert.equal(redactText({},'/avatar#synthetic-secret-fragment'),'/avatar#[REDACTED]');
 assert.equal(redactText({redact:{patterns:['fixture_secret']}},'%2566ixture_secret'),'[REDACTED-ENCODED]');
 assert.equal(redactText({},'<a href="/route#access_token=synthetic-secret">safe</a>'),'<a href="/route#[REDACTED]">safe</a>');
 assert.equal(redactText({},'color: #abcdef; background: #12345678;'),'color: #abcdef; background: #12345678;');
 assert.equal(redactText({},'<input value=synthetic-secret>'),'<input value=[REDACTED]>');
 assert.equal(redactText({redact:{patterns:['fixture_secret']}},'&#x66;ixture_secret'),'[REDACTED-ENCODED]');
 assert.equal(redactCapture({}, {'access%2554oken':'synthetic-marker'})['access%2554oken'],'[REDACTED]');
 let encoded='fixture_secret';for(let i=0;i<8;i++)encoded=encodeURIComponent(encoded.replace(/^f/,'%66'));assert.match(redactText({redact:{patterns:['fixture_secret']}},encoded),/REDACTED/);

});
test('accepts complete measured theme and refuses empty/incomplete/unsafe themes',()=>{
 assert.deepEqual(validateTheme(theme(),catalog),[]); assert.ok(validateTheme({},catalog).length);
 const bad=theme(); delete bad.themes.dark.primary; assert.ok(validateTheme(bad,catalog).some(x=>x.includes('primary')));
 const injection=theme(); injection.customTokens=[{name:'x;}',dark:'#123456',reason:'observed'}]; assert.ok(validateTheme(injection,catalog).length);
 const proposed=theme(); proposed.themes.light={...proposed.themes.dark}; assert.ok(validateTheme(proposed,catalog).some(x=>x.includes('proposed')));
 const malformed=theme(); malformed.radius.reason=3; assert.ok(validateTheme(malformed,catalog).length);
});
test('member paths refuse traversal and symlink ancestors',()=>{
 const root=scratch(); try { put(path.join(root,'safe','x.txt'),'ok'); assert.equal(safeMember(root,'safe/x.txt'),path.join(root,'safe/x.txt'));
 assert.throws(()=>safeMember(root,'../outside')); fs.symlinkSync(path.join(root,'safe'),path.join(root,'link')); assert.throws(()=>safeMember(root,'link/x.txt'),/linked/);
 } finally {fs.rmSync(root,{recursive:true,force:true});}
});
function mapFixture(root, prop='default', values=theme()) {
 put(path.join(root,'ledger.json'),{components:[{name:'button',instances:1,layer:'primitive',kind:'button'}]});
 put(path.join(root,'shadcn/batches/batch-01.json'),[{name:'button'}]);
 put(path.join(root,'shadcn/batches/map-01.json'),[{name:'button',strategy:'direct',shadcn:[{component:'button',props:{variant:prop}}],install:['button'],confidence:'high'}]);
 put(path.join(root,'shadcn/theme.json'),values); fs.mkdirSync(path.join(root,'_raw'),{recursive:true,mode:0o700});
}
test('shadcn CLI fails before writes for empty theme and multivalue props',()=>{
 const root=scratch(); try {
 mapFixture(root,'default',{}); let result=run('inventory/shadcn-build.mjs',{RAW:path.join(root,'_raw')}); assert.equal(result.status,1); assert.ok(!fs.existsSync(path.join(root,'shadcn/shadcn-map.json')));
 mapFixture(root,'default | outline'); result=run('inventory/shadcn-build.mjs',{RAW:path.join(root,'_raw')}); assert.equal(result.status,1); assert.match(result.stdout,/one exact/); assert.ok(!fs.existsSync(path.join(root,'shadcn/globals.css')));
 mapFixture(root); result=run('inventory/shadcn-build.mjs',{RAW:path.join(root,'_raw')}); assert.equal(result.status,0,result.stderr); assert.match(fs.readFileSync(path.join(root,'shadcn/globals.css'),'utf8'),/--primary: oklch/); assert.equal(fs.statSync(path.join(root,'shadcn/globals.css')).mode & 0o777,0o600);
 const config=JSON.parse(fs.readFileSync(path.join(scripts,'capture.config.example.json'),'utf8')); config.app.name='Fixture */\n@import url(https://example.invalid/x);\n/*'; config.output.inventory=root; const configFile=path.join(root,'capture.json');put(configFile,config);
 result=run('inventory/shadcn-build.mjs',{RAW:path.join(root,'_raw'),CAPTURE_CONFIG:configFile});assert.equal(result.status,0,result.stderr); const css=fs.readFileSync(path.join(root,'shadcn/globals.css'),'utf8');assert.ok(!css.replace(/\/\*[\s\S]*?\*\//g,'').includes('@import'));
 fs.chmodSync(path.join(root,'shadcn'),0o755); result=run('inventory/shadcn-build.mjs',{RAW:path.join(root,'_raw')}); assert.notEqual(result.status,0); assert.match(result.stderr,/private/);
 } finally {fs.rmSync(root,{recursive:true,force:true});}
});
function handoffFixture(root) {
 put(path.join(root,'ledger.json'),{components:[{name:'button',path:'components/button/',kind:'button',layer:'primitive'}],unassigned:[]});
 const c=path.join(root,'components/button'); put(path.join(c,'component.md'),'# button\nhttps://example.test/x?token=hidden'); put(path.join(c,'code.html'),'<button>test</button>'); put(path.join(c,'styles.json'),{default:{}});put(path.join(c,'assets.json'),{apiKey:'hidden',iconFonts:['Example Icons']});
 // Valid one-pixel PNG; KEEP_PNG makes no decoder or new dependency necessary.
 put(path.join(c,'screenshots/variant-01.png'),Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aT7cAAAAASUVORK5CYII=','base64'));
 fs.mkdirSync(path.join(root,'_raw'),{recursive:true,mode:0o700});
}
test('handoff refuses missing files, links and existing outputs; valid ZIP has complete manifest',()=>{
 const root=scratch(); try {
 handoffFixture(root); const raw=path.join(root,'_raw'), out=path.join(root,'result.zip'); fs.unlinkSync(path.join(root,'components/button/styles.json'));
 let result=run('inventory/design-handoff.mjs',{RAW:raw,OUT:out,KEEP_PNG:'1'}); assert.notEqual(result.status,0); assert.ok(!fs.existsSync(out));
 put(path.join(root,'components/button/styles.json'),{}); fs.symlinkSync(path.join(root,'components/button/code.html'),path.join(root,'components/button/linked.html'));
 result=run('inventory/design-handoff.mjs',{RAW:raw,OUT:out,KEEP_PNG:'1'}); assert.notEqual(result.status,0); assert.ok(!fs.existsSync(out)); fs.unlinkSync(path.join(root,'components/button/linked.html'));
 result=run('inventory/design-handoff.mjs',{RAW:raw,OUT:out,KEEP_PNG:'1'}); assert.equal(result.status,0,result.stderr); assert.equal(fs.statSync(out).mode & 0o777,0o600);
 const entries=execFileSync('unzip',['-Z1',out],{encoding:'utf8'}).trim().split('\n'); const manifestName=entries.find(n=>n.endsWith('/handoff-manifest.json'));
 const manifest=JSON.parse(execFileSync('unzip',['-p',out,manifestName],{encoding:'utf8'})); for (const file of manifest.files) { const entry=entries.find(n=>n.endsWith("/"+file.path)); const bytes=execFileSync("unzip",["-p",out,entry]); assert.equal(bytes.length,file.bytes); assert.equal(createHash("sha256").update(bytes).digest("hex"),file.sha256); } assert.equal(manifest.componentCount,1); assert.equal(manifest.components.length,1); assert.ok(manifest.files.every(f=>entries.some(n=>n.endsWith('/'+f.path))));
 const assets=execFileSync('unzip',['-p',out,entries.find(n=>n.endsWith('/components/button/assets.json'))],{encoding:'utf8'}); assert.ok(!assets.includes('hidden'));
 for (const malicious of ['\\..\\..\\escape.txt','unsafe:stream.txt','control'+String.fromCharCode(1)+'.txt','CON.txt']) { const asset=path.join(root,'assets',malicious);put(asset,'unsafe'); const badZip=path.join(root,'bad.zip'); result=run('inventory/design-handoff.mjs',{RAW:raw,OUT:badZip,KEEP_PNG:'1'});assert.notEqual(result.status,0);assert.match(result.stderr,/portable/);assert.ok(!fs.existsSync(badZip)); fs.unlinkSync(asset); }
 const evidence=path.join(root,'evidence.json'); put(evidence,{accessToken:'synthetic-marker', nested:{refresh_token:'another-marker'}, link:'https://example.test/a?key=url-marker'});
 const contextZip=path.join(root,'context.zip'); result=run('inventory/design-handoff.mjs',{RAW:raw,OUT:contextZip,KEEP_PNG:'1',HANDOFF_FILES:evidence}); assert.equal(result.status,0,result.stderr);
 const contextEntries=execFileSync('unzip',['-Z1',contextZip],{encoding:'utf8'}).trim().split('\n'); const context=execFileSync('unzip',['-p',contextZip,contextEntries.find(n=>n.endsWith('/context/evidence.json'))],{encoding:'utf8'}); assert.ok(!context.includes('synthetic-marker')); assert.ok(!context.includes('another-marker')); assert.ok(!context.includes('url-marker')); assert.match(context,/REDACTED/);
 const before=fs.readFileSync(out); result=run('inventory/design-handoff.mjs',{RAW:raw,OUT:out,KEEP_PNG:'1'}); assert.notEqual(result.status,0); assert.deepEqual(fs.readFileSync(out),before);
 } finally {fs.rmSync(root,{recursive:true,force:true});}
});
