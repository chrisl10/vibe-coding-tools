// Educational adapter contract, not a deployable route by itself.
// locals.formWriter must come from trusted server integration, never form data.
// Its writeAuthorized method must recheck identity, tenant/resource permission
// and duplicate-operation policy atomically. No adapter means no mutation.
import { fail } from '@sveltejs/kit';

export const actions = {
  default: async ({ request, locals }) => {
    const writer = locals.formWriter;
    if (!writer) return fail(503, { message: 'Saving is unavailable.', errors: {}, values: {} });
    if (!(await writer.mayEdit())) {
      return fail(403, { message: 'You do not have permission to save this record.', errors: {}, values: {} });
    }
    let submitted;
    try { submitted = await request.formData(); }
    catch { return fail(400, { message: 'The submitted form could not be read.', errors: {}, values: {} }); }
    const entries = submitted.getAll('displayName');
    const name = entries.length === 1 && typeof entries[0] === 'string'
      ? entries[0].trim() : '';
    if (!name || name.length > 80) {
      return fail(422, {
        message: 'Check the name field.',
        errors: { displayName: 'Enter a name of 1 to 80 characters.' },
        values: { displayName: name.slice(0, 80) }
      });
    }
    // No user/tenant/role IDs are accepted from this form.
    // Do not catch redirect/error control flow in a broad success handler.
    // Adapter must return a durable outcome; never turn a thrown error into success.
    const saved = await writer.writeAuthorized({ displayName: name });
    if (saved.kind === 'forbidden') {
      return fail(403, { message: 'Permission changed. Nothing was saved.', errors: {}, values: {} });
    }
    if (saved.kind === 'conflict') {
      return fail(409, { message: 'This record changed. Reload before saving.', errors: {}, values: { displayName: name } });
    }
    if (saved.kind !== 'saved') throw new Error('Unrecognized form writer outcome');
    return { success: true, message: 'Name saved.', errors: {}, values: { displayName: name } };
  }
};
