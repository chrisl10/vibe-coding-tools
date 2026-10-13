import 'server-only';
import { AccessFailure, requireIdentity, findReadableNote, updateWritableNote } from './adapter';
import { toNoteDTO } from './policy.mjs';

export async function readNote(id: string) {
  const identity = await requireIdentity();
  const row = await findReadableNote(identity, id);
  if (!row || row.tenantId !== identity.tenantId) throw new AccessFailure(404);
  return toNoteDTO(row);
}
export async function renameNote(id: string, title: string) {
  const identity = await requireIdentity();
  if (!(await updateWritableNote(identity, id, title))) throw new AccessFailure(404);
}
