export function collect({ stateId, withVars, redactPatterns, iconPattern }) {
  const REDACT = redactPatterns.map((p) => new RegExp(p, "gi"));
  const redact = (s) => REDACT.reduce((acc, re) => acc.replace(re, "[REDACTED]"), s);
  const STYLE_KEYS = [
    "display", "position", "color", "backgroundColor", "backgroundImage", "borderTopColor",
    "borderTopWidth", "borderTopStyle", "borderRadius", "boxShadow", "outlineStyle",
    "fontFamily", "fontSize", "fontWeight", "lineHeight", "letterSpacing", "textTransform",
    "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "gap", "opacity", "cursor",
    "width", "height", "fontVariationSettings",
  ];
  const INTERACTIVE = new Set(["BUTTON", "A", "INPUT", "SELECT", "TEXTAREA", "SUMMARY", "LABEL"]);
  const ROLES = new Set([
    "button", "tab", "tablist", "switch", "checkbox", "radio", "combobox", "listbox", "option",
    "menu", "menuitem", "dialog", "alert", "status", "progressbar", "slider", "table", "row",
    "navigation", "tooltip", "badge", "link", "searchbox", "textbox",
  ]);
  const transparent = (c) => c === "rgba(0, 0, 0, 0)" || c === "transparent";

  const visible = (el, r, cs) =>
    r.width >= 8 && r.height >= 8 && cs.visibility !== "hidden" && cs.display !== "none" && +cs.opacity > 0.02;

  const iconNames = (el) =>
    [...el.querySelectorAll("*")].filter((i) => new RegExp(iconPattern).test(String(i.className)))
      .map((i) => i.textContent.trim())
      .filter(Boolean);

  const shape = (el, depth) => {
    if (depth === 0) return "";
    return [...el.children]
      .slice(0, 12)
      .map((c) => {
        const isIcon = new RegExp(iconPattern).test(String(c.className?.baseVal ?? c.className ?? ""));
        const tag = isIcon ? "ICON" : c.tagName;
        const inner = shape(c, depth - 1);
        return inner ? `${tag}(${inner})` : tag;
      })
      .join(",");
  };

  const stats = {};
  const bump = (k, v) => {
    if (!v || v === "none" || v === "normal" || v === "0px") return;
    stats[k] ??= {};
    stats[k][v] = (stats[k][v] || 0) + 1;
  };

  const clean = (t) => (t || "").replace(/\s+/g, " ").trim().slice(0, 100);
  const HEAD = "h1, h2, h3, h4, [role=heading]";
  const outsideSidebar = (h) => !h.closest("aside, nav");
  const pageTitle = clean([...document.querySelectorAll("h1")].find(outsideSidebar)?.innerText);
  // Nearest section heading: walk up ancestors, take the last heading that precedes el.
  const headCache = new WeakMap();
  const sectionHeading = (el) => {
    for (let a = el.parentElement, depth = 0; a && depth < 8; a = a.parentElement, depth++) {
      let list = headCache.get(a);
      if (!list) headCache.set(a, (list = [...a.querySelectorAll(HEAD)]));
      const inSidebar = !!el.closest("aside, nav");
      const hs = list.filter(
        (h) => !el.contains(h) && (inSidebar || outsideSidebar(h)) && h.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING,
      );
      if (hs.length) return clean(hs.at(-1).innerText);
    }
    return "";
  };
  const fieldLabel = (el) => {
    if (el.labels?.length) return clean(el.labels[0].innerText);
    const by = el.getAttribute("aria-labelledby");
    if (by) return clean(by.split(" ").map((id) => (el.getRootNode().getElementById?.(id) || document.getElementById(id))?.innerText).join(" "));
    const prev = el.previousElementSibling;
    return prev && ["LABEL", "SPAN", "P"].includes(prev.tagName) ? clean(prev.innerText) : "";
  };
  const candidates = [];
  let probe = 0;
  const all = [];
  let shadowRoots = 0, truncated = false;
  const walk = (root) => {
    for (const el of root.querySelectorAll("*")) {
      if (all.length >= 10000) { truncated = true; return; }
      all.push(el);
      if (el.shadowRoot) { shadowRoots++; walk(el.shadowRoot); }
    }
  };
  walk(document.body);
  for (const el of all) {
    if (["SCRIPT", "STYLE", "NOSCRIPT", "TEMPLATE", "svg", "path", "BR"].includes(el.tagName)) continue;
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    if (!visible(el, r, cs)) continue;

    const hasOwnText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
    if (hasOwnText) {
      bump("color", cs.color);
      bump("fontFamily", cs.fontFamily);
      bump("fontSize", cs.fontSize);
      bump("fontWeight", cs.fontWeight);
      bump("lineHeight", cs.lineHeight);
      bump("letterSpacing", cs.letterSpacing);
      bump("typeStyle", `${cs.fontSize}/${cs.lineHeight} ${cs.fontWeight} ${cs.textTransform}`);
    }
    if (!transparent(cs.backgroundColor)) bump("backgroundColor", cs.backgroundColor);
    if (cs.backgroundImage !== "none") bump("backgroundImage", cs.backgroundImage.slice(0, 160));
    if (parseFloat(cs.borderTopWidth) > 0 && cs.borderTopStyle !== "none") {
      bump("borderColor", cs.borderTopColor);
      bump("borderWidth", cs.borderTopWidth);
    }
    bump("borderRadius", cs.borderRadius);
    bump("boxShadow", cs.boxShadow);
    for (const k of ["paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "marginTop", "marginBottom", "gap"]) {
      bump("spacing", cs[k]);
    }

    // Component candidate heuristics.
    const role = el.getAttribute("role") || "";
    const tag = el.tagName;
    const interactive = INTERACTIVE.has(tag) || ROLES.has(role);
    const boundary =
      !transparent(cs.backgroundColor) ||
      cs.backgroundImage !== "none" ||
      (parseFloat(cs.borderTopWidth) > 0 && cs.borderTopStyle !== "none") ||
      cs.boxShadow !== "none";
    const structural = ["TABLE", "THEAD", "TH", "UL", "OL", "NAV", "HEADER", "ASIDE", "DIALOG", "H1", "H2", "H3", "H4", "HR", "IMG", "PROGRESS"].includes(tag);
    const iconOnly = new RegExp(iconPattern).test(String(el.className));
    if (!(interactive || (boundary && r.width >= 16 && r.height >= 16) || structural || iconOnly)) continue;
    if (r.width > innerWidth * 0.98 && r.height > innerHeight * 0.9) continue; // page shells

    const style = {};
    for (const k of STYLE_KEYS) style[k] = cs[k];
    const classes = String(el.className?.baseVal ?? el.className ?? "")
      .split(/\s+/)
      .filter(Boolean);
    const id = `${stateId}-${probe++}`;
    el.setAttribute("data-ui-probe", id);
    const region = el.closest("aside, nav") ? "sidebar" : el.closest("header") ? "header" : "main";

    candidates.push({
      id,
      tag,
      role,
      type: el.getAttribute("type") || "",
      region,
      classes,
      shape: shape(el, 2),
      style,
      context: {
        page: pageTitle,
        section: redact(sectionHeading(el)),
        label: redact(fieldLabel(el)),
        parentText: redact(clean(el.parentElement?.innerText).slice(0, 80)),
      },
      text: el.getAttribute("type") === "password" ? "[REDACTED]" : redact((el.innerText || el.value || el.getAttribute("aria-label") || "").trim().replace(/\s+/g, " ").slice(0, 120)),
      ariaLabel: el.getAttribute("aria-label") || "",
      title: el.getAttribute("title") || "",
      state: el.getAttribute("data-state") || el.getAttribute("aria-selected") || el.getAttribute("aria-checked") || (el.disabled ? "disabled" : ""),
      iconMetadata: [...(iconOnly ? [el] : []), ...el.querySelectorAll("*")].filter((i) => new RegExp(iconPattern).test(String(i.className?.baseVal ?? i.className ?? ""))).slice(0, 8).map((i) => ({ glyph: i.textContent.trim(), fontFamily: getComputedStyle(i).fontFamily, fontVariationSettings: getComputedStyle(i).fontVariationSettings })),
      icons: iconNames(el).slice(0, 8).concat(iconOnly ? [el.textContent.trim()] : []),
      images: [...(tag === "IMG" ? [el] : el.querySelectorAll("img"))].slice(0, 4).map((i) => i.getAttribute("src")),
      svgCount: el.querySelectorAll("svg").length,
      rect: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) },
      html: redact(el.outerHTML.replace(/ data-ui-probe="[^"]*"/g, "").slice(0, 3000)),
    });
  }

  let vars = null;
  if (withVars) {
    const names = new Set();
    const rules = {};
    for (const ss of document.styleSheets) {
      let rs;
      try { rs = ss.cssRules; } catch { continue; }
      const walk = (list, media) => {
        for (const rule of list) {
          if (rule.style && rule.selectorText) {
            for (const n of rule.style) {
              if (!n.startsWith("--") || n.startsWith("--tw-")) continue;
              names.add(n);
              const sel = media ? `${media} ${rule.selectorText}` : rule.selectorText;
              (rules[sel] ??= {})[n] = rule.style.getPropertyValue(n).trim();
            }
          }
          if (rule.cssRules) walk(rule.cssRules, rule.conditionText || rule.name || media);
        }
      };
      walk(rs, "");
    }
    const cs = getComputedStyle(document.documentElement);
    const resolved = {};
    for (const n of [...names].sort()) resolved[n] = cs.getPropertyValue(n).trim();
    vars = { resolved, bySelector: rules, htmlClass: document.documentElement.className };
  }

  return { candidates, stats, vars, capture: { deviceScaleFactor: window.devicePixelRatio, screenshotScale: "device", viewport: { width: innerWidth, height: innerHeight } }, title: document.title, path: location.pathname + location.search, coverage: { openShadowRoots: shadowRoots, domElements: all.length, domLimit: 10000, truncated, limitations: ["Closed shadow roots, canvas interiors and unopened interactive states are not inspectable."] } };
}

