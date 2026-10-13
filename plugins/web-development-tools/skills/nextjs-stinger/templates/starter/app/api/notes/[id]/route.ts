import { readNote } from '@/lib/notes';
import { AccessFailure } from '@/lib/adapter';
import { parseId } from '@/lib/policy.mjs';

const headers = { 'Cache-Control': 'private, no-store' };
export async function GET(_request: Request, context: { params: Promise<{ id: string }> }) {
  const id = parseId((await context.params).id);
  if (!id) return Response.json({ error: 'Invalid request' }, { status: 400, headers });
  try {
    return Response.json(await readNote(id), { headers });
  } catch (error) {
    if (error instanceof AccessFailure) return Response.json({ error: 'Access unavailable' }, { status: error.status, headers });
    throw error;
  }
}
