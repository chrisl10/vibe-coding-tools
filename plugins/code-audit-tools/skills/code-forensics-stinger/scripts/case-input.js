'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const DOCUMENT_KINDS = Object.freeze(['master', 'agency', 'attorney', 'plain_language', 'pre_litigation']);
const MAX_INPUT_BYTES = 2 * 1024 * 1024;
const own = (object, key) => Object.prototype.hasOwnProperty.call(object, key);
function fail(message) { throw new Error(message); }
function object(value, label, keys, required = keys) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) fail(`${label} must be an object`);
  for (const key of Object.keys(value)) if (!keys.includes(key)) fail(`${label}: unknown key ${key}`);
  for (const key of required) if (!own(value, key)) fail(`${label}: missing ${key}`);
}
function string(value, label, max = 20000) {
  if (typeof value !== 'string' || !value.trim() || value.length > max) fail(`${label} must be nonempty text of at most ${max} characters`);
  if (/[\u0000-\u001f\u007f-\u009f]/u.test(value)) fail(`${label} contains control characters`);
  for (let i = 0; i < value.length; i++) {
    const code = value.charCodeAt(i);
    if (code >= 0xd800 && code <= 0xdbff) {
      if (++i >= value.length || value.charCodeAt(i) < 0xdc00 || value.charCodeAt(i) > 0xdfff) fail(`${label} contains invalid Unicode`);
    } else if (code >= 0xdc00 && code <= 0xdfff) fail(`${label} contains invalid Unicode`);
  }
  return value;
}
function list(value, label, min, max) {
  if (!Array.isArray(value) || value.length < min || value.length > max) fail(`${label} must contain ${min} to ${max} entries`);
}
function identifier(value, label, matter = false) {
  string(value, label, 64);
  if (!(matter ? /^[a-z0-9]+(?:-[a-z0-9]+)*$/ : /^[A-Za-z0-9]+(?:[_-][A-Za-z0-9]+)*$/).test(value)) fail(`${label} must be a safe identifier`);
}
function validateCaseFacts(value) {
  object(value, 'case', ['schema_version', 'matter', 'fictional', 'evidence', 'documents']);
  if (value.schema_version !== 1) fail('schema_version must be 1');
  if (typeof value.fictional !== 'boolean') fail('fictional must be an explicit boolean');
  object(value.matter, 'matter', ['id', 'title', 'client', 'prepared_by', 'report_date']);
  identifier(value.matter.id, 'matter.id', true);
  for (const field of ['title', 'client', 'prepared_by']) string(value.matter[field], `matter.${field}`, 500);
  const date = value.matter.report_date;
  if (typeof date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(date) || date.slice(0, 4) === '0000') fail('matter.report_date must be a real ISO date (YYYY-MM-DD)');
  const parsedDate = new Date(`${date}T00:00:00.000Z`);
  if (!Number.isFinite(parsedDate.getTime()) || parsedDate.toISOString().slice(0, 10) !== date) fail('matter.report_date must be a real ISO date (YYYY-MM-DD)');
  list(value.evidence, 'evidence', 0, 1000);
  const evidenceIds = new Set();
  for (const [index, item] of value.evidence.entries()) {
    object(item, `evidence[${index}]`, ['id', 'title', 'uri']);
    identifier(item.id, `evidence[${index}].id`);
    if (evidenceIds.has(item.id)) fail(`duplicate evidence id ${item.id}`);
    evidenceIds.add(item.id);
    string(item.title, `evidence[${index}].title`, 500);
    string(item.uri, `evidence[${index}].uri`, 2000);
  }
  object(value.documents, 'documents', DOCUMENT_KINDS, []);
  if (Object.keys(value.documents).length === 0) fail('documents must contain at least one document');
  let totalBlocks = 0;
  for (const [kind, document] of Object.entries(value.documents)) {
    object(document, `documents.${kind}`, ['title', 'sections']);
    string(document.title, `${kind}.title`, 500);
    list(document.sections, `${kind}.sections`, 1, 100);
    for (const [index, section] of document.sections.entries()) {
      const label = `${kind}.sections[${index}]`;
      object(section, label, ['title', 'blocks']);
      string(section.title, `${label}.title`, 500);
      list(section.blocks, `${label}.blocks`, 1, 1000);
      for (const [blockIndex, block] of section.blocks.entries()) {
        const at = `${label}.blocks[${blockIndex}]`;
        const baseKeys = ['type', 'tier', 'source_ids', 'estimate'];
        const contentKeys = block?.type === 'paragraph' ? ['text'] : block?.type === 'bullets' ? ['items'] : block?.type === 'table' ? ['headers', 'rows'] : [];
        if (!contentKeys.length) fail(`${at}: type must be paragraph, bullets, or table`);
        object(block, at, [...baseKeys, ...contentKeys], ['type', 'tier', 'source_ids', ...contentKeys]);
        if (!['PROVEN', 'DERIVED', 'HYPOTHESIS'].includes(block.tier)) fail(`${at}: invalid evidence tier`);
        if (own(block, 'estimate') && typeof block.estimate !== 'boolean') fail(`${at}.estimate must be boolean`);
        if (block.estimate === true && block.tier === 'PROVEN') fail(`${at}: an estimate cannot be PROVEN`);
        list(block.source_ids, `${at}.source_ids`, block.tier === 'HYPOTHESIS' ? 0 : 1, 1000);
        const references = new Set();
        for (const id of block.source_ids) {
          identifier(id, `${at}.source_ids`);
          if (!evidenceIds.has(id)) fail(`${at}: unknown evidence id ${id}`);
          if (references.has(id)) fail(`${at}: duplicate source id ${id}`);
          references.add(id);
        }
        if (block.type === 'paragraph') string(block.text, `${at}.text`);
        if (block.type === 'bullets') {
          list(block.items, `${at}.items`, 1, 200);
          block.items.forEach((item, i) => string(item, `${at}.items[${i}]`));
        }
        if (block.type === 'table') {
          list(block.headers, `${at}.headers`, 1, 20);
          block.headers.forEach((item, i) => string(item, `${at}.headers[${i}]`, 500));
          list(block.rows, `${at}.rows`, 1, 1000);
          block.rows.forEach((row, i) => {
            list(row, `${at}.rows[${i}]`, block.headers.length, block.headers.length);
            row.forEach((item, j) => string(item, `${at}.rows[${i}][${j}]`));
          });
        }
        if (++totalBlocks > 2000) fail('case contains too many blocks');
      }
    }
  }
  return value;
}
function safeAbsolute(input, label) {
  if (typeof input !== 'string' || !input || /[\u0000-\u001f\u007f]/u.test(input)) fail(`${label} must be a safe path`);
  if (input.split(/[\\/]/).includes('..')) fail(`${label} cannot contain traversal`);
  return path.resolve(input);
}
function permittedAlias(candidate, stat) {
  if (process.platform !== 'darwin' || !stat.isSymbolicLink()) return false;
  const aliases = { '/tmp': '/private/tmp', '/var': '/private/var', '/etc': '/private/etc' };
  return own(aliases, candidate) && path.resolve(path.dirname(candidate), fs.readlinkSync(candidate)) === aliases[candidate];
}
function inspectPath(absolute, allowMissing = false) {
  let current = path.parse(absolute).root;
  const pieces = absolute.slice(current.length).split(path.sep).filter(Boolean);
  for (const piece of pieces) {
    current = path.join(current, piece);
    let stat;
    try { stat = fs.lstatSync(current); } catch (error) {
      if (allowMissing && error.code === 'ENOENT') return;
      throw error;
    }
    if (stat.isSymbolicLink() && !permittedAlias(current, stat)) fail(`symlink path refused: ${current}`);
    if (current !== absolute && !stat.isDirectory() && !permittedAlias(current, stat)) fail(`non-directory ancestor refused: ${current}`);
  }
}
function readCaseFacts(filename) {
  const absolute = safeAbsolute(filename, 'case-facts');
  inspectPath(absolute);
  const before = fs.lstatSync(absolute);
  if (!before.isFile() || before.size > MAX_INPUT_BYTES) fail('case-facts must be a regular JSON file of at most 2 MiB');
  const fd = fs.openSync(absolute, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW || 0));
  let text;
  try {
    const opened = fs.fstatSync(fd);
    if (!opened.isFile() || opened.dev !== before.dev || opened.ino !== before.ino) fail('case-facts changed during read');
    const bytes = Buffer.alloc(MAX_INPUT_BYTES + 1);
    let count = 0;
    while (count < bytes.length) {
      const got = fs.readSync(fd, bytes, count, bytes.length - count, null);
      if (got === 0) break;
      count += got;
    }
    if (count > MAX_INPUT_BYTES) fail('case-facts exceeds 2 MiB');
    text = new TextDecoder('utf-8', { fatal: true }).decode(bytes.subarray(0, count));
  } finally { fs.closeSync(fd); }
  inspectPath(absolute);
  let data;
  try { data = JSON.parse(text); } catch { fail('case-facts must contain valid JSON'); }
  return validateCaseFacts(data);
}
function parseCli(argv) {
  const parsed = { format: 'docx' };
  const names = { '--case-facts': 'caseFacts', '--out-dir': 'outDir', '--format': 'format' };
  const seen = new Set();
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    if (!own(names, flag) || seen.has(flag) || !argv[index + 1] || argv[index + 1].startsWith('--')) fail('usage: --case-facts FILE --out-dir DIR [--format docx|markdown]');
    seen.add(flag);
    parsed[names[flag]] = argv[index + 1];
  }
  if (!parsed.caseFacts || !parsed.outDir) fail('usage: --case-facts FILE --out-dir DIR [--format docx|markdown]');
  if (!['docx', 'markdown'].includes(parsed.format)) fail('format must be docx or markdown');
  parsed.outDir = safeAbsolute(parsed.outDir, 'out-dir');
  inspectPath(parsed.outDir, true);
  return parsed;
}
function directoryIdentity(directory) {
  inspectPath(directory);
  const stat = fs.lstatSync(directory);
  if (!stat.isDirectory()) fail('out-dir must be a directory');
  if ((stat.mode & 0o777) !== 0o700 || (typeof process.getuid === 'function' && stat.uid !== process.getuid())) fail('existing out-dir must be user-owned mode 0700; choose a fresh private workspace');
  return { dev: stat.dev, ino: stat.ino, real: fs.realpathSync(directory) };
}
function ensureDirectory(directory) {
  inspectPath(directory, true);
  const missing = [];
  let current = directory;
  while (!fs.existsSync(current)) { missing.push(current); current = path.dirname(current); }
  for (const candidate of missing.reverse()) {
    inspectPath(path.dirname(candidate));
    fs.mkdirSync(candidate, { mode: 0o700 });
    inspectPath(candidate);
  }
  return directoryIdentity(directory);
}
function sameDirectory(directory, identity) {
  const now = directoryIdentity(directory);
  if (now.dev !== identity.dev || now.ino !== identity.ino || now.real !== identity.real) fail('out-dir changed during write');
}
function writePrivateOutput(directory, filename, content) {
  if (path.basename(filename) !== filename || !/^[a-z0-9_-]+\.(?:docx|md)$/.test(filename)) fail('unsafe output filename');
  const identity = ensureDirectory(directory);
  const destination = path.join(directory, filename);
  if (fs.existsSync(destination) || (() => { try { fs.lstatSync(destination); return true; } catch (error) { if (error.code === 'ENOENT') return false; throw error; } })()) fail('output already exists; refusing overwrite');
  const temporary = path.join(directory, `.case-document-${crypto.randomBytes(16).toString('hex')}.tmp`);
  let fd;
  let linked = false;
  try {
    sameDirectory(directory, identity);
    fd = fs.openSync(temporary, fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL | (fs.constants.O_NOFOLLOW || 0), 0o600);
    fs.writeFileSync(fd, content);
    fs.fsyncSync(fd);
    fs.closeSync(fd); fd = undefined;
    sameDirectory(directory, identity);
    fs.linkSync(temporary, destination); // Atomic publication without overwriting an existing file.
    linked = true;
    sameDirectory(directory, identity);
  } finally {
    if (fd !== undefined) fs.closeSync(fd);
    // Only remove our temporary file while the directory still has its original identity.
    try { sameDirectory(directory, identity); fs.unlinkSync(temporary); } catch (error) { if (error.code !== 'ENOENT' && !linked) throw error; }
  }
  return destination;
}
module.exports = { DOCUMENT_KINDS, MAX_INPUT_BYTES, validateCaseFacts, readCaseFacts, parseCli, safeAbsolute, inspectPath, writePrivateOutput };
