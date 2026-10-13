// Original pure boundary helpers. No Vue runtime is needed for these functions.
export interface RecordItem { id: string; title: string }
export function decodeRecord(input: unknown): RecordItem {
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error('Invalid response')
  const candidate = input as { id?: unknown; title?: unknown }
  if (typeof candidate.id !== 'string' || !candidate.id || candidate.id.length > 128 ||
      typeof candidate.title !== 'string' || candidate.title.length > 120) throw new Error('Invalid response')
  return { id: candidate.id, title: candidate.title }
}
export function titleError(value: string): string | null {
  const title = value.trim()
  if (!title) return 'Enter a title.'
  if (title.length > 120) return 'Use 120 characters or fewer.'
  return null
}
