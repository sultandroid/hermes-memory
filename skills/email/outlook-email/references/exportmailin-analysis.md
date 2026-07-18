# ExportMailIn Excel Analysis Workflow

When the user sends an Outlook export (ExportMailIn-*.xlsx) — a spreadsheet of recent emails — use this workflow to extract new transmittals and update repo registers.

## Trigger

User sends an `.xlsx` file named `ExportMailIn-*.xlsx` or says "شوفت الاميلات ؟" (did you see the emails?) and attaches a file.

## Workflow

### Phase 1 — Read the export

Use `read_file` on the cached document path. The xlsx auto-extracts to a readable table with columns:

| Column | Content |
|--------|---------|
| Attachments | Yes/No |
| Mail No | Aconex transmittal ref (SIC.-WTRAN-XXXXX or CGP-WTRAN-XXXXX) |
| Subject | Email subject line |
| Date | DD/MM/YYYY |
| From | Sender name |
| From Organization | Company |
| Recipients | Who it was sent to |
| Type | Workflow Transmittal |

### Phase 2 — Classify each row

| Signal | Classification |
|--------|---------------|
| `CGP-WTRAN-` prefix | **CG Final response** — already reviewed by CG, has a code (A/B/C/D) |
| `SIC.-WTRAN-` prefix | **Samaya outgoing submission** — sent to CG, awaiting response |
| Subject contains `Final` | CG has issued a decision on this item |
| Subject contains `Prequalification` or `PQ-` | Specialist prequalification submission |
| Subject contains `Assessment Report` | Existing-systems assessment/evaluation |
| Subject contains `CV` | Personnel change / key personnel submission |
| Subject contains `Scope of Work` or `SOW` | Specialist scope definition |

### Phase 3 — Compare against existing repo

Search the repo for each Mail No / subject to determine if already tracked:

```bash
# Check if a transmittal is already in the repo
rg -l "CGP-WTRAN-000157" /path/to/repo/
rg -l "BMS Specialist.*GITCO" /path/to/repo/
```

Also check `email_scan_*.md` files under `03_Plans/08_Risk/reviews/` — these are the daily email scan logs.

### Phase 4 — Identify delta

Items that exist in the export but NOT in the repo are the delta. Group by register:

| Register File | What to add |
|---------------|-------------|
| `prequalification_register.md` | New PQ submissions (PQ-0123+) |
| `assessment_evaluation_register.md` | New assessment reports + Final CG responses |
| `submittal_register.md` | New submittals + Final CG responses |
| `email_scan_<date>.md` | New Aconex transmittals in the info table |

### Phase 5 — Update registers

For each register, append rows with:
- Mail No / Aconex ref
- Subject (English translation if Arabic)
- Date
- Status code (if Final response: A/B/C/D; if outgoing: U/For Review)
- Source note: `ExportMailIn 2026-07-18`

### Phase 6 — Commit

Single commit with summary of how many new items were added and which files changed.

## Pitfalls

- **Same export may be sent twice.** Check if the file content is identical to a previously processed export before re-processing. Compare the date in the filename or the "Generated On" cell.
- **Export is CC-only.** The user's export filter is "My mail only:True, Unread Mail:True, Recipient Type:CC" — this means it only shows emails where the user was CC'd, not To. Items where the user was the direct recipient won't appear.
- **Not all items are new.** Some items in the export may already be tracked in the repo from a previous scan. Always cross-reference before adding.
- **Subject line may differ from doc code.** The export subject is the email subject, not the document number. Match by Aconex transmittal number (SIC.-WTRAN-XXXXX / CGP-WTRAN-XXXXX) which is in the Mail No column.
- **Date format is DD/MM/YYYY.** Parse accordingly when writing to registers.
