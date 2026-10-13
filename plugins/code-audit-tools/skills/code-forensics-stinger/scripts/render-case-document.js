'use strict';
const { DOCUMENT_KINDS, readCaseFacts, parseCli, writePrivateOutput } = require('./case-input');

const FICTIONAL_NOTICE = 'FICTIONAL TRAINING EXAMPLE: all parties, events, and amounts are invented.';
const REVIEW_NOTICE = 'DRAFT FOR HUMAN/COUNSEL REVIEW. No legal conclusions or privilege status are established by this document.';
const TIER_NOTICE = 'Evidence tiers are supplied by the case author. This renderer does not verify their truth or fetch source material.';
function blockLabel(block) {
  const tier = block.tier === 'HYPOTHESIS' ? 'HYPOTHESIS (UNVERIFIED)' : block.tier;
  return `${block.estimate ? 'ESTIMATE - ' : ''}${tier}; sources: ${block.source_ids.length ? block.source_ids.join(', ') : 'none supplied'}`;
}
function metadata(facts, kind) {
  const lines = [];
  if (facts.fictional) lines.push(FICTIONAL_NOTICE);
  if (kind === 'attorney' || kind === 'pre_litigation') lines.push(REVIEW_NOTICE);
  lines.push(facts.matter.title, `Client: ${facts.matter.client}`, `Prepared by: ${facts.matter.prepared_by}`, `Report date: ${facts.matter.report_date}`, `Matter ID: ${facts.matter.id}`, TIER_NOTICE);
  if (kind === 'pre_litigation') lines.push('Combined pre-litigation review document containing only the supplied sections. No letters are sent automatically.');
  return lines;
}
function markdownEscape(text) {
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/[\\`*_{}\[\]()#+.!|~-]/g, '\\$&');
}
function renderMarkdown(facts, kind) {
  const document = facts.documents[kind];
  const lines = [`# ${markdownEscape(document.title)}`, '', ...metadata(facts, kind).flatMap(text => [markdownEscape(text), ''])];
  for (const section of document.sections) {
    lines.push(`## ${markdownEscape(section.title)}`, '');
    for (const block of section.blocks) {
      lines.push(`**${markdownEscape(blockLabel(block))}**`, '');
      if (block.type === 'paragraph') lines.push(markdownEscape(block.text), '');
      if (block.type === 'bullets') lines.push(...block.items.map(item => `- ${markdownEscape(item)}`), '');
      if (block.type === 'table') {
        lines.push(`| ${block.headers.map(markdownEscape).join(' | ')} |`, `| ${block.headers.map(() => '---').join(' | ')} |`);
        lines.push(...block.rows.map(row => `| ${row.map(markdownEscape).join(' | ')} |`), '');
      }
    }
  }
  lines.push('## Supplied evidence register', '');
  if (!facts.evidence.length) lines.push('No evidence entries supplied.', '');
  for (const source of facts.evidence) lines.push(`- ${markdownEscape(source.id)}: ${markdownEscape(source.title)}; ${markdownEscape(source.uri)}`);
  if (facts.fictional) lines.push('', markdownEscape(FICTIONAL_NOTICE));
  return `${lines.join('\n')}\n`;
}
async function renderDocx(facts, kind) {
  // The case and output path are validated before this dependency is loaded.
  const { Document, Packer, Paragraph, Table, TableRow, TableCell, HeadingLevel, Footer, Header } = require('docx');
  const paragraph = text => new Paragraph({ text, spacing: { after: 120 } });
  const children = [new Paragraph({ text: facts.documents[kind].title, heading: HeadingLevel.TITLE }), ...metadata(facts, kind).map(paragraph)];
  for (const section of facts.documents[kind].sections) {
    children.push(new Paragraph({ text: section.title, heading: HeadingLevel.HEADING_1 }));
    for (const block of section.blocks) {
      children.push(paragraph(blockLabel(block)));
      if (block.type === 'paragraph') children.push(paragraph(block.text));
      if (block.type === 'bullets') children.push(...block.items.map(text => new Paragraph({ text, bullet: { level: 0 } })));
      if (block.type === 'table') children.push(new Table({ rows: [block.headers, ...block.rows].map(row => new TableRow({ children: row.map(text => new TableCell({ children: [paragraph(text)] })) })) }));
    }
  }
  children.push(new Paragraph({ text: 'Supplied evidence register', heading: HeadingLevel.HEADING_1 }));
  if (!facts.evidence.length) children.push(paragraph('No evidence entries supplied.'));
  for (const source of facts.evidence) children.push(paragraph(`${source.id}: ${source.title}; ${source.uri}`));
  const footer = [facts.fictional ? FICTIONAL_NOTICE : TIER_NOTICE];
  if (kind === 'attorney' || kind === 'pre_litigation') footer.push(REVIEW_NOTICE);
  const document = new Document({ creator: facts.matter.prepared_by, title: facts.documents[kind].title, description: 'Case-author-supplied evidence and review draft', sections: [{ headers: facts.fictional ? { default: new Header({ children: [paragraph(FICTIONAL_NOTICE)] }) } : undefined, footers: { default: new Footer({ children: footer.map(paragraph) }) }, children }] });
  return Packer.toBuffer(document);
}
async function runBuilder(kind, argv = process.argv.slice(2)) {
  if (!DOCUMENT_KINDS.includes(kind)) throw new Error('unknown document kind');
  const options = parseCli(argv);
  const facts = readCaseFacts(options.caseFacts);
  if (!facts.documents[kind]) throw new Error(`case-facts is missing selected document ${kind}`);
  const rendered = options.format === 'docx' ? await renderDocx(facts, kind) : renderMarkdown(facts, kind);
  const filename = `${facts.matter.id}-${kind}.${options.format === 'docx' ? 'docx' : 'md'}`;
  const output = writePrivateOutput(options.outDir, filename, rendered);
  process.stdout.write(`${JSON.stringify({ kind, format: options.format, output, fictional: facts.fictional })}\n`);
  return output;
}
module.exports = { FICTIONAL_NOTICE, REVIEW_NOTICE, TIER_NOTICE, blockLabel, renderMarkdown, renderDocx, runBuilder };
