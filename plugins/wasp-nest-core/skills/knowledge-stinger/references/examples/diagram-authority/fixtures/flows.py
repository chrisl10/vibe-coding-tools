"""Synthetic teaching fixtures. No accounts, database, network or payments."""
def read_invoice(actor, invoice, trace):
    trace.append("permission-check")
    if actor["tenant"] != invoice["tenant"]:
        trace.append("return-forbidden")
        return {"status": 403}
    trace.append("read-invoice")
    return {"status": 200, "id": invoice["id"]}


def enqueue_export(actor, queue, trace):
    trace.append("role-check")
    if actor["role"] != "owner":
        trace.append("return-forbidden")
        return {"status": 403}
    queue.append({"kind": "export", "tenant": actor["tenant"]})
    trace.append("queue-accepted")
    return {"status": 202, "state": "queued"}


def consume_export(queue, trace):
    job = queue.pop(0)
    trace.append("worker-start")
    trace.append("export-complete")
    return {"tenant": job["tenant"], "state": "complete"}


def commit_then_notify(rows, notify, trace):
    rows.append({"state": "saved"})
    trace.append("local-commit")
    try:
        notify()
    except RuntimeError:
        trace.append("notify-failed")
        return {"state": "saved", "notification": "failed"}
    trace.append("notify-succeeded")
    return {"state": "saved", "notification": "sent"}
