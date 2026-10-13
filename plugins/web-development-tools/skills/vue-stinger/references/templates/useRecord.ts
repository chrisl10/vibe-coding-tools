// Adapt the accepted endpoint and decoder; this is not an application scaffold.
import { ref, watch, readonly } from 'vue'
import { decodeRecord, type RecordItem } from './model'
export function useRecord(id: () => string | undefined) {
  const record = ref<RecordItem | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const reload = ref(0)
  watch([id, reload], async ([value], _old, onCleanup) => {
    const controller = new AbortController()
    let current = true
    onCleanup(() => { current = false; controller.abort() })
    record.value = null; error.value = null; loading.value = false
    if (!value) return
    loading.value = true
    try {
      const response = await fetch(`/api/records/${encodeURIComponent(value)}`, { signal: controller.signal })
      if (!response.ok) throw new Error('Request failed')
      const decoded = decodeRecord(await response.json())
      if (current) record.value = decoded
    } catch {
      if (current) error.value = 'Could not load this record. Try again.'
    } finally {
      if (current) loading.value = false
    }
  }, { immediate: true })
  return { record: readonly(record), loading: readonly(loading), error: readonly(error), retry: () => { reload.value++ } }
}
