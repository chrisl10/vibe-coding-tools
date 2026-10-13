# Communication records

`scripts/parse_emails.py` accepts `--input-dirs` followed by one or more directories and `--out` for a private working directory. Inspect the source and its output against representative records before using it for a case. It reads nested EML messages and produces working Markdown and intermediate JSON.

Deduplication and thread grouping are aids, not evidence of completeness. Preserve originals, missing dates, attachments and quoted-message context. Do not assume a shared subject proves a single conversation. Record extracted source coordinates and check each quotation against its original.

Do not infer a principal's role from frequency alone. Populate each party profile from this matter's records. Source IDs in the final renderer input identify specific messages or exhibits; the renderer does not read or verify the underlying messages.
