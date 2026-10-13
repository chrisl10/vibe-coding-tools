/** @param {unknown} value @returns {string | null} */
export function parseId(value) {
  return typeof value === 'string' && /^[A-Za-z0-9_-]{1,64}$/.test(value) ? value : null;
}
/** @param {unknown} value @returns {string | null} */
export function parseTitle(value) {
  if (typeof value !== 'string') return null;
  const title = value.trim();
  return title.length > 0 && title.length <= 120 ? title : null;
}
/** @param {{id: string, title: string}} row @returns {{id: string, title: string}} */
export function toNoteDTO(row) { return { id: row.id, title: row.title }; }
