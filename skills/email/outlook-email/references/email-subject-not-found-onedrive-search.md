# Email Subject Not Found → Search OneDrive Submittal Tree

When the user references an email by subject (e.g. "Speaker Coverage Review Request") and the
subject does NOT exist in Outlook SQLite, do NOT conclude it's missing. The document is often
already filed in the OneDrive submittal tree under a different name, and the email may be a
notification or the subject may differ.

## Workflow

1. **Search Outlook first** (subject + preview LIKE, cross-folder). If nothing, don't stop.
2. **Search the OneDrive submittal tree by keyword** — the file is usually filed under a
   descriptive folder name, not the email subject:
   ```bash
   find "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum" \
     -iname "*speaker*" -o -iname "*coverage*" -o -iname "*acoustic*" 2>/dev/null
   ```
   Also search `~/Downloads`, `~/Desktop`, `~/Documents` for the keyword.
3. **Search the repo** (`aseer-museum-pm`) for the keyword in filenames AND content
   (`grep -ril "<keyword>"`). The repo's `Technical_Office/Submission_Tracker/AV_IT/` often names
   the deliverable (e.g. "Speaker Coverage Analysis (per gallery)").
4. **Confirm the file** with `file` + `pdfinfo` before reading.

## Worked example (2026-08-24)

- User: "check this mail: Speaker Coverage Review Request" → no such subject in Outlook.
- Found at: `.../Aseer-Museum/02_Submittals/3.1_DD Doucments AV/Speackers Coverage/Speaker Coverage.pdf`
  (note the typo "Speackers" in the folder name — search by keyword, not exact path).
- The file was `AC-RPT-001 Rev R01` — a 12pp acoustic review report, not an email.

## Pitfall — OneDrive EDEADLK on the found file

The found PDF may be a cloud stub. `cp` fails with `fcopyfile failed: Resource deadlock avoided`
and `pdfinfo`/`pdftotext` report "Couldn't find trailer dictionary" / "May not be a PDF file".
This is the File Provider lock, not a corrupt file. Workarounds in order:
- Try `pdftotext`/`pdfinfo` **directly on the OneDrive path** (read-only sometimes works where `cp` fails).
- If the drawing is a CAD plot (image-based), `pdftotext` returns empty even when readable — render
  the title block with `pdftoppm` and read it visually.
- If truly EDEADLK, the user must open the file in Finder to hydrate it, then retry.
