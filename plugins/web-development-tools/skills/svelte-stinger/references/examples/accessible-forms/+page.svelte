<!-- Educational same-page form; see guide for version and adapter prerequisites. -->
<script>
  import { enhance } from '$app/forms';
  import { tick } from 'svelte';
  let { form } = $props();
  let pending = $state(false);
  let summary;
  const submit = ({ cancel }) => {
    if (pending) { cancel(); return; }
    pending = true;
    return async ({ result, update }) => {
      try {
        await update({ reset: false });
        if (result.type === 'failure') {
          await tick();
          summary?.focus();
        }
      } finally {
        pending = false;
      }
    };
  };
</script>

<svelte:head><title>Edit display name</title></svelte:head>
<form method="POST" use:enhance={submit} aria-busy={pending}>
  {#if form && !form.success}
    <section tabindex="-1" bind:this={summary} aria-labelledby="form-errors">
      <h2 id="form-errors">Could not save</h2>
      <p>{form.message}</p>
      {#if form.errors?.displayName}
        <a href="#display-name">{form.errors.displayName}</a>
      {/if}
    </section>
  {/if}
  <label for="display-name">Display name (required)</label>
  <p id="name-help">Use 1 to 80 characters.</p>
  <input id="display-name" name="displayName" required maxlength="80"
    value={form?.values?.displayName ?? ''} readonly={pending}
    aria-invalid={form?.errors?.displayName ? 'true' : undefined}
    aria-describedby={form?.errors?.displayName ? 'name-help name-error' : 'name-help'} />
  {#if form?.errors?.displayName}<p id="name-error">{form.errors.displayName}</p>{/if}
  <button type="submit" disabled={pending}>Save name</button>
  <p role="status" aria-live="polite" aria-atomic="true">
    {pending ? 'Saving name...' : form?.success ? form.message : ''}
  </p>
</form>
