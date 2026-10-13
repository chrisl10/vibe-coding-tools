# Billing records and estimates

Inspect invoices and payment receipts separately. Normalize party names only where evidence establishes the relationship. Never count a receipt as an additional invoice. Record currency, tax, voids, credits, due dates and payment status; absence of a receipt is not proof of nonpayment.

The optional parser handles a limited email-body pattern and a limited invoice/receipt PDF pattern. Supply `--processed-json FILE --pdf-dir DIR --email-vendor NAME --email-senders ADDRESS [ADDRESS ...] --pdf-vendor NAME --out DIR`. Sender and vendor names are mandatory case inputs. These patterns extract USD-style amounts only; handle other currencies separately and do not combine them. Outputs are `email_invoices.json`, `pdf_invoices.json` and `invoice_texts.json`. These are extracts to review, not complete validated financial records.

The extrapolator accepts `--email-invoices FILE --pdf-invoices FILE --out FILE`. It estimates missing monthly cycles between observed endpoints of the same service and price. Do not extrapolate a single observation, overlapping price eras or an unproved billing schedule. The helper refuses multiple observed prices for one service. Establish and split verified billing eras before a new estimation run. No final-cycle extension is automatic. Synthetic UNK rows remain DERIVED estimates.

The workbook helper takes the same two input flags, `--extrapolated FILE --project-name NAME --out FILE`, and optional `--commits FILE --git-by-month FILE`. It produces an invoice summary and available detail sheets. Counts vary with input; it does not guarantee 51 tabs or all proposed report views. Read its outputs and check totals against source records.

Use only reviewed values in the renderer input. Each estimate block sets `estimate: true`, uses DERIVED or HYPOTHESIS and names its source IDs. Do not call a market comparison, estimate or billed-versus-activity difference an established loss.
