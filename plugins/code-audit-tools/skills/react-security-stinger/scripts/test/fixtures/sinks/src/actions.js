'use server';
export async function updateRole(userId, role) { await db.users.update(userId, { role }); }
