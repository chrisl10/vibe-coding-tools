// Constructed framework-neutral contract. Not ICU parsing or app integration.
const locales = Object.freeze({'en-US': 'ltr', ar: 'rtl'});
export function resolveLocale(input) {
  let tag;
  try { tag = Intl.getCanonicalLocales(input)[0]; } catch { return 'en-US'; }
  return Object.hasOwn(locales, tag) ? tag : 'en-US';
}
export function direction(locale) {
  if (!Object.hasOwn(locales, locale)) throw new Error('unsupported locale');
  return locales[locale];
}
export function validateResource(resource) {
  if (!resource || Object.getPrototypeOf(resource) !== Object.prototype) throw new Error('resource object required');
  const keys = Object.keys(resource).sort();
  if (keys.join(',') !== 'itemCount,save') throw new Error('resource key contract');
  const safeText = text => {
    if (typeof text !== 'string' || !text.trim() || /[<>]/u.test(text)) throw new Error('text resource required');
  };
  safeText(resource.save);
  if (/[{}]/u.test(resource.save)) throw new Error('save placeholders forbidden');
  const forms = resource.itemCount;
  if (!forms || Object.getPrototypeOf(forms) !== Object.prototype || !Object.hasOwn(forms, 'other')) throw new Error('other branch required');
  for (const [category, text] of Object.entries(forms)) {
    if (!['zero','one','two','few','many','other'].includes(category)) throw new Error('plural category contract');
    safeText(text);
    if (!text.includes('{count}') || text.replaceAll('{count}', '').match(/[{}]/u)) throw new Error('count placeholder contract');
  }
  return resource;
}
export function itemMessage(resource, locale, count) {
  validateResource(resource); direction(locale);
  if (!Number.isFinite(count) || count < 0) throw new Error('invalid count');
  const category = new Intl.PluralRules(locale).select(count);
  return (resource.itemCount[category] ?? resource.itemCount.other)
    .replaceAll('{count}', new Intl.NumberFormat(locale).format(count));
}
export function moneyParts(amount, currency, locale) {
  direction(locale);
  if (!Number.isFinite(amount) || !['USD','EUR'].includes(currency)) throw new Error('money contract');
  return new Intl.NumberFormat(locale, {style:'currency', currency}).formatToParts(amount);
}
export function instantParts(date, timeZone, locale) {
  direction(locale);
  if (!(date instanceof Date) || !Number.isFinite(date.getTime()) || !['UTC','America/New_York'].includes(timeZone)) throw new Error('instant contract');
  return new Intl.DateTimeFormat(locale, {timeZone, calendar:'gregory', hourCycle:'h23', year:'numeric', month:'2-digit', day:'2-digit',hour:'2-digit',minute:'2-digit'}).formatToParts(date);
}
