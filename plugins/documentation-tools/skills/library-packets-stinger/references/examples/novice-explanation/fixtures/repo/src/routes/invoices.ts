import { mayReadInvoice } from "../permissions";
import { findInvoice } from "../data/invoices";

export async function readInvoice(request: { userId?: string; workspaceId: string; invoiceId: string }) {
  if (!request.userId) return { status: 401 };
  const permitted = await mayReadInvoice(request.userId, request.workspaceId, request.invoiceId);
  if (!permitted) return { status: 403 };
  const invoice = await findInvoice(request.workspaceId, request.invoiceId);
  if (!invoice) return { status: 404 };
  return { status: 200, invoice };
}
