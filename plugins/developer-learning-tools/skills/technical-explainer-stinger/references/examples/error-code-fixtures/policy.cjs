async function readInvoice(actor, invoice, read) {
  if (!actor || actor.workspace !== invoice.workspace) {
    return {status: "denied"};
  }
  const data = await read(invoice.id);
  return {status: "allowed", data};
}
module.exports = {readInvoice};
