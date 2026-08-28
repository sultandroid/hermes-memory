# Locating attachment bytes: the `Message Attachments/<NN>/` directory

When AppleScript `save` fails (Outlook 16.90+ `-2700`, 0-byte files) AND the
`Mail_OwnedBlocks`/`Blocks` join returns no rows, the attachment bytes are still
on disk — in the `Message Attachments/` directory, keyed by the same numeric
subdir as the email's `.olk15Message`.

## Key facts (verified 2026-08-27)

1. **`.olk15Message` is a binary pointer, NOT the attachment container.** A CG
   response email's `.olk15Message` is only ~44 KB and contains the MIME
   headers (`Content-Type: application/pdf`, `filename=...`) but **no** `%PDF`
   or `JVBERi0` base64 payload. Searching it for PDF magic bytes returns
   nothing. The body (UTF-16LE) is recoverable from it, but the attachment
   bytes are not.

2. **`Mail_OwnedBlocks`/`Blocks` join is unreliable in BATCH, but works PER-EMAIL.** For a batch of 25 emails with `Message_HasAttachment=1`, a single `WHERE Record_RecordID IN (...)` query returned rows for only 2 (51859, 51864). But querying a CG response email **individually** (e.g. `WHERE Record_RecordID=51831`) DID return its 2 attachment paths. **Rule: query the join per-email, not in a batch `IN (...)` list** — a batch that returns few/no rows does NOT mean the attachment is missing. The per-email query is the authoritative mapping to the real `.olk15MsgAttachment` path.

3. **The real attachment bytes live in `Message Attachments/<NN>/`.** The
   numeric `<NN>` matches the subdir of the email's `PathToDataFile`
   (`Messages/<NN>/<uuid>.olk15Message` → `Message Attachments/<NN>/`). Each
   `.olk15MsgAttachment` file there is a MIME container with a base64 PDF
   payload starting at the `JVBERi0` magic marker.

## Workflow

```python
# email_id -> numeric subdir (from the Mail.PathToDataFile = Messages/<NN>/...)
targets = {51831: "95", 51833: "193", ...}

DATA = ".../Outlook 15 Profiles/Main Profile/Data"
for eid, d in targets.items():
    dpath = os.path.join(DATA, "Message Attachments", d)
    for f in glob.glob(os.path.join(dpath, "*.olk15MsgAttachment")):
        data = open(f, 'rb').read()
        idx = data.find(b'JVBERi0')          # PDF base64 magic
        if idx < 0: continue
        j = idx
        while j < len(data) and (chr(data[j]).isalnum() or data[j] in (43,47,61,10,13,32)):
            j += 1
        b64 = b''.join(data[idx:j].split())
        pdf = base64.b64decode(b64, validate=False)
        if pdf[:4] == b'%PDF':
            open(f"/tmp/att/{eid}.pdf", 'wb').write(pdf)
```

## Pitfalls

- **The `Message Attachments/<NN>/` dir is SHARED across many emails**, not
  just the target. Scanning it for `JVBERi0` yields dozens of false-positive
  PDFs from unrelated messages in the same numeric bucket. You cannot tell
  which PDF belongs to which email from the dir alone — the mapping is
  `Mail_OwnedBlocks` (when it works) or the MIME `filename=` header inside
  each `.olk15MsgAttachment`. Use the filename header to pick the right one.
- **Do not overwrite the same output path in a loop** — the naive
  `open(f"{label}_{count}.pdf")` with `count` reset per file overwrites
  earlier results. Use a unique per-file counter or the MIME filename.
- **Do not `grep -rl` the whole `Message Attachments/` tree to find a doc ref** — it times out (hundreds of thousands of files, >300s). Resolve via the per-email `Mail_OwnedBlocks JOIN Blocks` query, or `find` by the attachment GUID extracted from the `.olk15Message` strings (the GUID appears in the MIME `filename=`/content-id region).
- **`touch`-created 0-byte files pollute the attachment dir.** When AppleScript `save` fails, the `do shell script "touch ..."` step still creates 0-byte `.olk15MsgAttachment` files in `Message Attachments/<NN>/` with today's mtime. When scanning for "recent" attachments, filter these out (they're the ones you just created) — don't mistake them for the real attachment.
- **AppleScript `save` failing (-2700) is a known Outlook 16.90+ regression**,
  not a missing attachment. Fall back to this directory scan before declaring
  the attachment unrecoverable.
- **Aconex/CDE notification emails** (sender `Aconex Notification`) carry no
  inline attachment at all — `Message_HasAttachment=0` and no `Message
  Attachments` entry. Those are CDE syncs, not genuine attachment failures.
