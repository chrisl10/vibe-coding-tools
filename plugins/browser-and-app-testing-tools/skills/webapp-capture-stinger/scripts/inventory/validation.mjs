import fs from "node:fs";
import path from "node:path";
export function noLinks(target) {
  let current = path.resolve(target);
  for (;;) {
    try { if (fs.lstatSync(current).isSymbolicLink()) {
      const alias = process.platform === "darwin" && ["/tmp", "/var", "/etc"].includes(current);
      if (!alias || fs.realpathSync(current) !== `/private${current}`) throw new Error("refusing linked handoff path");
    } } catch (e) { if (e.code !== "ENOENT") throw e; }
    const parent = path.dirname(current); if (parent === current) break; current = parent;
  }
}
export function portableMember(relative, directory = false) {
  if (typeof relative !== "string" || !relative || /[\\:\x00-\x1f\x7f-\x9f<>"|?*]/.test(relative) || path.isAbsolute(relative) || path.win32.isAbsolute(relative)) throw new Error("handoff member must have a portable relative name");
  const value = directory && relative.endsWith("/") ? relative.slice(0, -1) : relative;
  const parts = value.split("/");
  if (parts.some((part) => !part || part === "." || part === ".." || /[. ]$/.test(part) || /^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)/i.test(part))) throw new Error("handoff member contains an unsafe portable path segment");
  return relative;
}
export function safeMember(root, relative, directory = false) {
  portableMember(relative, directory);
  if (typeof relative !== "string" || !relative || relative.includes("\\") || relative.includes("\0") || path.isAbsolute(relative) || path.win32.isAbsolute(relative) || relative.split("/").some((x) => x === ".." || x === ".")) throw new Error("handoff member must be a contained relative path");
  const file = path.resolve(root, relative);
  if (!file.startsWith(path.resolve(root) + path.sep)) throw new Error("handoff member escapes inventory");
  noLinks(file); const st = fs.statSync(file);
  if (directory ? !st.isDirectory() : !st.isFile()) throw new Error("handoff member has wrong file type");
  return file;
}
export function validateTheme(theme, catalog) {
  const errors = [];
  const plain = (v) => v && typeof v === "object" && !Array.isArray(v);
  const hex = (v) => typeof v === "string" && /^#[0-9a-f]{6}([0-9a-f]{2})?$/i.test(v);
  if (!plain(theme) || !["light", "dark"].includes(theme.capturedTheme)) return ["theme.capturedTheme must be light or dark; rerun THEME-INSTRUCTIONS.md"];
  if (!plain(theme.themes)) return ["theme.themes must contain the captured theme tokens"];
  for (const mode of ["light", "dark"]) {
    const values = theme.themes[mode];
    if (mode !== theme.capturedTheme && values == null) continue;
    if (!plain(values)) { errors.push(`theme.themes.${mode} must be an object`); continue; }
    if (mode !== theme.capturedTheme && values.proposed !== true) errors.push(`uncaptured ${mode} values require proposed:true`);
    for (const key of catalog.themeTokens.filter((t) => t !== "radius")) {
      const token = values[key];
      if (!plain(token) || !hex(token.value) || typeof token.source !== "string" || !token.source.trim() || typeof token.reason !== "string" || !token.reason.trim()) errors.push(`${mode}.${key} requires hex value, source and reason`);
    }
    for (const key of Object.keys(values)) if (key !== "proposed" && !catalog.themeTokens.includes(key)) errors.push(`unknown theme token ${key}`);
  }
  if (!plain(theme.radius) || !/^\d+(\.\d+)?px$/.test(theme.radius.value || "") || (typeof theme.radius.reason !== "string" || !theme.radius.reason.trim())) errors.push("radius requires a nonnegative px value and reason");
  if (!plain(theme.fonts) || ["sans", "mono", "icons"].some((k) => typeof theme.fonts[k] !== "string" || !theme.fonts[k].trim())) errors.push("fonts must supply observed sans, mono and icons strings (use none observed when absent)");
  for (const key of ["decisions", "gaps"]) if (!Array.isArray(theme[key]) || theme[key].some((v) => typeof v !== "string")) errors.push(`${key} must be an array of strings`);
  if (!Array.isArray(theme.customTokens)) errors.push("customTokens must be an array");
  const names = new Set();
  for (const token of Array.isArray(theme.customTokens) ? theme.customTokens : []) {
    if (!plain(token) || !/^[a-z][a-z0-9-]*$/.test(token.name || "") || names.has(token.name) || catalog.themeTokens.includes(token.name)) { errors.push("custom token names must be unique safe names outside the catalog"); continue; }
    names.add(token.name);
    const captured = theme.capturedTheme;
    if (!hex(token[captured]) || (typeof token.reason !== "string" || !token.reason.trim())) errors.push(`${token.name} requires captured hex value and reason`);
    for (const key of ["dark", "light", "foregroundDark", "foregroundLight"]) if (token[key] !== undefined && !hex(token[key])) errors.push(`${token.name}.${key} must be hex`);
  }
  return errors;
}
