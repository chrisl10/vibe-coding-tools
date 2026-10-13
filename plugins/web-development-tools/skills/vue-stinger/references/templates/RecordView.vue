<script setup lang="ts">
import { useRecord } from './useRecord'
const props = defineProps<{ id: string }>()
const { record, loading, error, retry } = useRecord(() => props.id)
</script>
<template>
  <main aria-labelledby="record-heading">
    <h1 id="record-heading">Record</h1>
    <p v-if="loading" role="status">Loading record...</p>
    <section v-else-if="error" aria-label="Record load error">
      <p role="alert">{{ error }}</p>
      <button type="button" @click="retry">Try again</button>
    </section>
    <p v-else-if="!record">No record selected.</p>
    <p v-else>{{ record.title }}</p>
  </main>
</template>
