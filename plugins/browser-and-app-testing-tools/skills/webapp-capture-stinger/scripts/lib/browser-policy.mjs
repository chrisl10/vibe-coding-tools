// Exact request grants keep capture reads separate from approved setup actions.
import { createHash } from "node:crypto";
export const bodyDigest = (body) => createHash("sha256").update(body || "").digest("hex");
const scopes = new WeakMap();
const safe = new Set(["GET", "HEAD", "OPTIONS"]);
const destructivePath = /(?:^|[\/_-])(?:logout|signout|delete|remove|reset|revoke|restart|purchase|pay|transfer|publish)(?=$|[\/_-])/i;
export function canonicalCapturePath(pathname) {
  let decoded = String(pathname);
  for (let level = 0; level < 4 && decoded.includes("%"); level++) {
    try { decoded = decodeURIComponent(decoded); } catch { throw new Error("capture path has malformed or ambiguous encoding"); }
  }
  if (decoded.includes("%") || !decoded.startsWith("/") || decoded.startsWith("//") || /[\\?#\x00-\x1f\x7f]/.test(decoded)) throw new Error("capture path has malformed or ambiguous encoding");
  // Normalize decoded dot segments before testing known destructive endpoints.
  return new URL(decoded, "http://capture.invalid").pathname.replace(/%20/g, " ");
}
export function isSafeCapturePath(pathname) {
  try { return !destructivePath.test(canonicalCapturePath(pathname)); } catch { return false; }
}
export function validateRequestGrants(grants = [], { reads = false } = {}) {
  if (!Array.isArray(grants)) throw new Error("request grants must be an array");
  for (const grant of grants) {
    if (grant.approved !== true || !/^\/(?!\/)/.test(grant.path || "") ||
        /[?#]/.test(grant.path) || !/^[a-f0-9]{64}$/.test(grant.bodySha256 || "") ||
        (reads ? grant.method !== "POST" || !["rest-read", "graphql-query"].includes(grant.kind) : !["POST", "PUT", "PATCH", "DELETE"].includes(grant.method))) {
      throw new Error("request grant requires approved=true, exact path, method and bodySha256");
    }
  }
  return grants;
}
export function requestAllowed(cfg, request, page) {
  const url = new URL(request.url());
  const same = url.origin === cfg.app.origin;
  if (request.isNavigationRequest() && !same) return false;
  const method = request.method().toUpperCase();
  if (!isSafeCapturePath(url.pathname)) return false;
  if (safe.has(method)) return true;
  if (!same || url.search) return false;
  const bodyBytes = typeof request.postDataBuffer === "function" ? (request.postDataBuffer() || Buffer.alloc(0)) : Buffer.from(request.postData() || "", "utf8");
  let body;
  try { body = new TextDecoder("utf-8", { fatal: true }).decode(bodyBytes); } catch { return false; }
  const match = (g) => g.approved === true && g.path === url.pathname && g.bodySha256 === bodyDigest(bodyBytes);
  if (method === "POST") {
    const grant = (cfg.network?.readPost || []).find((g) => g.method === "POST" && ["rest-read", "graphql-query"].includes(g.kind) && match(g));
    if (grant) {
      let parsed;
      try { parsed = JSON.parse(body); } catch { parsed = null; }
      const graphqlShape = parsed && typeof parsed === "object" &&
        (Array.isArray(parsed) || Object.hasOwn(parsed, "query") || Object.hasOwn(parsed, "operationName") || Object.hasOwn(parsed, "extensions"));
      if (grant.kind === "rest-read") {
        // REST read grants support a JSON object only. Form bodies, opaque text,
        // encoded GraphQL and GraphQL-shaped fields are never treated as REST.
        const hasGraphqlKeys = (value) => {
          if (!value || typeof value !== "object") return false;
          return Object.entries(value).some(([key, entry]) => /^(?:query|operationName|extensions|persistedQuery)$/i.test(key) || hasGraphqlKeys(entry));
        };
        return parsed !== null && typeof parsed === "object" && !Array.isArray(parsed) && !graphqlShape && !hasGraphqlKeys(parsed) && !/\b(?:mutation|subscription|persistedQuery)\b/i.test(body);
      }
      if (!parsed || Array.isArray(parsed) || typeof parsed.query !== "string" || parsed.extensions) return false;
      const query = parsed.query.replace(/#[^\n]*/g, "").trim();
      // One explicit named or unnamed read operation, with no opaque persisted
      // query hash or batched operation. Conservative keyword checks fail closed.
      return /^query\b/.test(query) && query.endsWith("}") &&
        (query.match(/\bquery\b/g) || []).length === 1 &&
        !/\b(?:mutation|subscription)\b/i.test(query);
    }
  }
  try { if (typeof request.frame === "function" && request.frame().page() !== page) return false; } catch { return false; }
  return (scopes.get(page) || []).some((g) => g.method === method && match(g));
}
export async function withApprovedRequests(cfg, page, plan, action) {
  if (plan.approved !== true || !["local", "seeded"].includes(plan.environment)) throw new Error("write scope requires explicit local/seeded approval");
  if (plan.environment === "local" && !["localhost", "127.0.0.1", "[::1]"].includes(new URL(cfg.app.origin).hostname)) throw new Error("local mutation scope requires loopback origin");
  const grants = validateRequestGrants(plan.requests || []);
  if (scopes.has(page)) throw new Error("nested mutation scopes are refused");
  scopes.set(page, grants);
  try { return await action(); } finally { scopes.delete(page); }
}
