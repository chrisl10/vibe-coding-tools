'use server';
import { redirect } from 'next/navigation';
import { renameNote } from '@/lib/notes';
import { AccessFailure } from '@/lib/adapter';
import { parseId, parseTitle } from '@/lib/policy.mjs';

export type RenameState = { message: string | null };
export async function rename(_previous: RenameState, formData: FormData): Promise<RenameState> {
  const id = parseId(formData.get('id'));
  const title = parseTitle(formData.get('title'));
  if (!id || !title) return { message: 'Enter a valid title.' };
  try {
    await renameNote(id, title);
  } catch (error) {
    if (error instanceof AccessFailure) return { message: 'This note is unavailable.' };
    throw error;
  }
  // No shared cache in this bounded read. Add invalidation only after guide03.
  redirect(`/notes/${id}`);
}
