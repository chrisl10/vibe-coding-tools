// Sanitize every exported string, including metadata keys and encoded URL values.
const SECRET_KEY = /^(password|token|secret|authorization|cookie|api[-_]?key|access[-_]?token|refresh[-_]?token|client[-_]?secret|id[-_]?token|session[-_]?token|private[-_]?key|credential)$/i;
const ENCODED = /%[0-9a-f]{2}|&(?:#(?:x[0-9a-f]+|\d+)|[a-z][a-z0-9]+);/i;
const MAX_DECODE_ROUNDS = 6;
function decodeRound(value) {
  const named = { amp:'&', quot:'"', apos:"'", lt:'<', gt:'>', nbsp:'\u00a0' };
  const entities = value.replace(/&(#(?:x[0-9a-f]+|\d+)|[a-z][a-z0-9]+);/gi, (_, code) => {
    if (code.startsWith('#')) {
      const n = /^#x/i.test(code) ? parseInt(code.slice(2),16) : Number(code.slice(1));
      if (!Number.isInteger(n) || n < 0 || n > 0x10ffff || (n >= 0xd800 && n <= 0xdfff)) throw new Error('unsupported encoded capture value');
      return String.fromCodePoint(n);
    }
    if (!Object.hasOwn(named,code.toLowerCase())) throw new Error('unsupported encoded capture entity');
    return named[code.toLowerCase()];
  });
  return entities.replace(/(?:%[0-9a-f]{2})+/gi, (encoded) => decodeURIComponent(encoded));
}
function decodedKey(value) {
  let current = value;
  for (let i=0;i<MAX_DECODE_ROUNDS && ENCODED.test(current);i++) current = decodeRound(current);
  if (ENCODED.test(current)) throw new Error('capture key exceeds six decoding rounds');
  return current;
}
export function redactText(cfg, value) {
  const patterns = (cfg?.redact?.patterns || []).map((p) => new RegExp(p, 'gi'));
  const apply = (s) => patterns.reduce((v, re) => v.replace(re, '[REDACTED]'), s);
  const scrub = (value) => {
    let text = String(value);
    text = text.replace(/https?:\/\/[^\s"'<>)]*/gi, (raw) => {
      try { const u = new URL(raw); u.username = ''; u.password = '';
        for (const key of [...u.searchParams.keys()]) u.searchParams.set(key, '[REDACTED]');
        if (u.hash) u.hash = '[REDACTED]';
        return u.toString();
      } catch { return '[REDACTED-URL]'; }
    });
    // URI fragments are private metadata. The slash/attribute boundaries keep CSS hex colors intact.
    text = text.replace(/(^|[\s"'(=])((?:\/|\.{1,2}\/)[^\s"'<>?#)]*)(#[^\s"'<>)]*)/g, '$1$2#[REDACTED]');
    text = text.replace(/(\b(?:href|src)\s*=\s*)(["'])(.*?)\2/gis, (_, prefix, quote, uri) => `${prefix}${quote}${uri.includes('#') ? uri.slice(0,uri.indexOf('#'))+'#[REDACTED]' : uri}${quote}`);
    if (/^[a-z0-9._/-]+#[^\s]+$/i.test(text)) text = text.slice(0,text.indexOf('#'))+'#[REDACTED]';
    text = text.replace(/([?&][^=\s&"'<>]+)=([^&\s"'<>]*)/g, '$1=[REDACTED]');
    text = text.replace(/((?:value|data-(?:token|secret|password|credential|key)|nonce)\s*=\s*)(["'])(.*?)\2/gis, '$1$2[REDACTED]$2');
    text = text.replace(/(\b(?:value|data-(?:token|secret|password|credential|key)|nonce)\s*=\s*)(?!["'])([^\s"'<>]+)/gi, '$1[REDACTED]');
    text = text.replace(/data:[^\s"'<>)]*/gi, '[REDACTED-DATA-URL]');
    text = text.replace(/(bearer\s+)[a-z0-9._~+\/-]+/gi, '$1[REDACTED]');
    text = text.replace(/(["']?\b(?:password|token|secret|authorization|cookie|api[-_]?key|access[-_]?token|refresh[-_]?token|client[-_]?secret|id[-_]?token|session[-_]?token|private[-_]?key|credential)["']?\s*[:=]\s*)(["'])(.*?)\2/gis, '$1$2[REDACTED]$2');
    text = text.replace(/(\b(?:password|token|secret|authorization|cookie|api[-_]?key|access[-_]?token|refresh[-_]?token|client[-_]?secret|id[-_]?token|session[-_]?token|private[-_]?key|credential)\s*[:=]\s*)(?!["'])([^\s"',;<>}\]]+)/gi, '$1[REDACTED]');
    return apply(text);
  };
  const original = String(value), clean = scrub(original);
  let probe = original;
  // Inspect decoded values without turning escaped source text into executable markup.
  try {
    for (let i=0;i<MAX_DECODE_ROUNDS && ENCODED.test(probe);i++) {
      probe = decodeRound(probe);
      if (scrub(probe) !== probe) return '[REDACTED-ENCODED]';
    }
    if (ENCODED.test(probe)) return '[REDACTED-ENCODING-LIMIT]';
  } catch { return '[REDACTED-UNSUPPORTED-ENCODING]'; }
  return clean;
}
export function redactCapture(cfg, value) {
  if (typeof value === 'string') return redactText(cfg, value);
  if (Array.isArray(value)) return value.map((entry) => redactCapture(cfg, entry));
  if (value && typeof value === 'object') {
    const out = Object.create(null);
    for (const [key, entry] of Object.entries(value)) {
      const safe = redactText(cfg, key);
      if (Object.hasOwn(out, safe)) throw new Error('redaction creates duplicate metadata keys; capture cannot be exported safely');
      let secret;
      try { secret = SECRET_KEY.test(decodedKey(key)); } catch { secret = true; }
      out[safe] = secret ? '[REDACTED]' : redactCapture(cfg, entry);
    }
    return out;
  }
  return value;
}
