'use client';
import { useActionState } from 'react';
import { rename } from './actions';

export default function NoteForm({ note }: { note: { id: string; title: string } }) {
  const [state, action, pending] = useActionState(rename, { message: null });
  return <form action={action}>
    <input type="hidden" name="id" value={note.id} />
    <label>Title <input name="title" defaultValue={note.title} maxLength={120} required /></label>
    <p aria-live="polite">{state.message}</p>
    <button type="submit" disabled={pending}>{pending ? 'Saving...' : 'Save'}</button>
  </form>;
}
