'use server';
export async function deleteNote(id: string) {
  await db.notes.delete(id);
}
