// WCAG sRGB contrast math. DOM coverage and paint uncertainty are reported by the runner.
export function composite(front, back) {
  if (![front, back].every((x) => Array.isArray(x) && x.length === 4 && x.every(Number.isFinite))) throw new Error("invalid RGBA");
  const alpha = front[3] + back[3] * (1 - front[3]);
  if (!alpha) return [0, 0, 0, 0];
  return [...front.slice(0, 3).map((c, i) => (c * front[3] + back[i] * back[3] * (1 - front[3])) / alpha), alpha];
}

export function luminance(rgb) {
  if (!Array.isArray(rgb) || rgb.length < 3 || rgb.slice(0, 3).some((n) => !Number.isFinite(n) || n < 0 || n > 255)) throw new Error("invalid sRGB");
  const linear = rgb.slice(0, 3).map((n) => (n /= 255) <= 0.04045 ? n / 12.92 : ((n + 0.055) / 1.055) ** 2.4);
  return linear[0] * 0.2126 + linear[1] * 0.7152 + linear[2] * 0.0722;
}

export function contrastRatio(front, back) {
  const a = luminance(front), b = luminance(back);
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
}

export function assessContrast(item) {
  const unknown = [...(item.unknown || [])];
  if (!item.foreground || !item.background || item.background[3] < 0.999) unknown.push("opaque colors were not resolved");
  const large = item.kind === "text" && (item.fontSize >= 24 || (item.fontSize >= 18.6666666667 && item.fontWeight >= 700));
  const threshold = item.kind === "text" && !large ? 4.5 : 3;
  const criterion = item.kind === "text" ? "WCAG 2.1/2.2 SC 1.4.3" : "WCAG 2.1/2.2 SC 1.4.11";
  if (unknown.length) return { ...item, criterion, threshold, large, status: "unmeasured", reasons: [...new Set(unknown)] };
  const displayed = composite(item.foreground, item.background);
  const ratio = contrastRatio(displayed, item.background);
  return { ...item, criterion, threshold, large, ratio, displayedForeground: displayed, status: ratio >= threshold ? "pass" : "fail" };
}
