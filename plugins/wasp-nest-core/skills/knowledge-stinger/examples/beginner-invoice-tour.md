# Where an invoice request goes

> Category: Architecture | Version: 1.0 | Date: October 2026 | Status: Synthetic worked example

This tour helps a new coder follow one invoice request through a small repository and recognize what the visible code cannot establish.

**Related:** [fixture README](../references/examples/novice-explanation/fixtures/repo/README.md), [Accepted invoice contract](../references/examples/novice-explanation/fixtures/repo/contracts/invoice-read.md), [source ledger](../references/examples/novice-explanation/evidence/source-claims.json).

## Where the journey starts

Open [the request handler](../references/examples/novice-explanation/fixtures/repo/src/routes/invoices.ts) first. Its `readInvoice` function receives a user ID, workspace ID and invoice ID. This is the visible entry point for this example, not proof of a deployed web route. [K1]

The handler looks for a user ID before doing anything else. Without one, it returns status 401. With one, it calls `mayReadInvoice`. If that call returns false, it returns 403 before requesting invoice data. [K2]

## How the request reaches data

After a true permission result, the handler calls [the data function](../references/examples/novice-explanation/fixtures/repo/src/data/invoices.ts) with the requested workspace and invoice IDs. The handler contains branches for a missing invoice, 404, and a returned invoice, 200. Those branches are visible source behavior; the supplied data function always throws and does not read a database. [K3]

## Who can read the invoice

The Accepted contract says workspace members may read invoices within their permitted workspace. The permission function's implementation is missing. We can see where the handler asks for permission, but cannot establish which users that function permits or whether it enforces the Accepted contract. A user ID alone does not prove access to any invoice. [K4]

## A limited analogy

Think of a records desk. A person gives their name, asks for a folder and waits for a permission decision before the desk fetches anything. In this fixture, we have the desk's instructions but not the permission clerk's rules, and the file-fetching worker stops with an error. The analogy does not prove the clerk rejects another workspace's request or that records are actually available. [K5, illustration]

## Terms used here

A handler is the function that receives this request. A workspace is one customer area named by the request. Permission means being allowed to read the requested invoice, which is separate from supplying a user ID. A contract records required behavior; Accepted does not mean executed or deployed. [K1, K2, K4]

## Check your understanding

If someone supplies a user ID and another workspace's invoice ID, what visible source would you need before claiming that the request is safely denied?

Reader response: Pending. Understanding: Pending. Application runtime: Unproven.
