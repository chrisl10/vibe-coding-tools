<script setup lang="ts">
import { computed, ref } from 'vue'
import { titleError } from './model'
const props = defineProps<{ formId: string; initialTitle?: string; pending: boolean; serverError?: string }>()
const emit = defineEmits<{ (event: 'save', title: string): void }>()
// Draft belongs to this instance. A changed initialTitle does not silently overwrite edits.
const title = ref(props.initialTitle ?? '')
const attempted = ref(false)
const error = computed(() => attempted.value ? titleError(title.value) : null)
const inputId = computed(() => `${props.formId}-title`)
const helpId = computed(() => `${props.formId}-help`)
const errorId = computed(() => `${props.formId}-error`)
function submit() {
  if (props.pending) return
  attempted.value = true
  if (!titleError(title.value)) emit('save', title.value.trim())
}
</script>
<template>
  <form @submit.prevent="submit" :aria-busy="props.pending">
    <label :for="inputId">Title</label>
    <p :id="helpId">Use 120 characters or fewer.</p>
    <input :id="inputId" v-model="title" type="text" :disabled="props.pending"
      :aria-invalid="Boolean(error)" :aria-describedby="error ? `${helpId} ${errorId}` : helpId" />
    <p v-if="error" :id="errorId" role="alert">{{ error }}</p>
    <p v-if="props.serverError" role="alert">{{ props.serverError }}</p>
    <button type="submit" :disabled="props.pending">{{ props.pending ? 'Saving...' : 'Save' }}</button>
  </form>
</template>
