import 'server-only';

export type Identity = { userId: string; tenantId: string };
export type NoteRow = { id: string; title: string; tenantId: string };
export class AccessFailure extends Error {
  constructor(public readonly status: 401 | 403 | 404) { super('Access unavailable'); }
}
// Replace only with the selected provider/backend contract. Never trust submitted identity.
export async function requireIdentity(): Promise<Identity> {
  throw new AccessFailure(401);
}
export async function findReadableNote(_identity: Identity, _id: string): Promise<NoteRow | null> {
  throw new Error('Selected backend adapter has not been implemented');
}
// Must atomically constrain user permission, tenant and resource ID in the write.
export async function updateWritableNote(_identity: Identity, _id: string, _title: string): Promise<boolean> {
  throw new Error('Selected backend adapter has not been implemented');
}
