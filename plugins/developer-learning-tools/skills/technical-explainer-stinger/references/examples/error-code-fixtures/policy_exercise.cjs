const assert = require("node:assert/strict");
const {readInvoice} = require("./policy.cjs");
(async () => {
  const calls = [];
  const read = async id => { calls.push(id); return "invoice data"; };
  assert.deepEqual(await readInvoice({workspace: "A"}, {workspace: "B", id: "i1"}, read), {status: "denied"});
  assert.equal(calls.length, 0);
  assert.deepEqual(await readInvoice(null, {workspace: "A", id: "i1"}, read), {status: "denied"});
  assert.deepEqual(await readInvoice({workspace: "A"}, {workspace: "A", id: "i1"}, read), {status: "allowed", data: "invoice data"});
  assert.deepEqual(calls, ["i1"]);
  await assert.rejects(readInvoice({workspace: "A"}, {workspace: "A", id: "i1"}, async () => { throw new Error("fixture read failed"); }), /fixture read failed/);
  console.log("PASS: 6 fixture assertions; in-memory callback only");
})().catch(error => { console.error(error); process.exitCode = 1; });
