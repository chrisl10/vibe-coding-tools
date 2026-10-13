import { Suspense } from 'react';
import { notFound } from 'next/navigation';
import { readNote } from '@/lib/notes';
import { parseId } from '@/lib/policy.mjs';
import NoteForm from './note-form';

export default function Page({ params }: { params: Promise<{ id: string }> }) {
  return <Suspense fallback={<p>Loading note...</p>}><Note params={params} /></Suspense>;
}
async function Note({ params }: { params: Promise<{ id: string }> }) {
  const id = parseId((await params).id);
  if (!id) notFound();
  const note = await readNote(id);
  return <NoteForm note={note} />;
}
