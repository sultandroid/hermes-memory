# Email-to-Odoo Task Workflow

End-to-end workflow for creating/updating Odoo tasks from user's verbal task list by cross-referencing Outlook emails, extracting attachments, reading PDFs, and filing to project folders.

## Trigger

User lists verbal tasks for the day. Agent needs to map them to Odoo structure, enrich with email evidence, and file supporting documents.

## Workflow Steps

### 1. Map Verbal Tasks to Existing Odoo Structure

- Query top-level packages: `project.task` → `parent_id=False`, `project_id=219`
- Check existing subtasks under each package to find matching tasks
- Identify whether each verbal task maps to an existing task (update) or needs a new one
- Use the correct parent package:
  - Schedule/planning items → `05 — Projects Plans` (ID 2946, stage 36)
  - Prequal/procurement items → `00 — Pre-Qualification & Procurement` (ID 3011, stage 35)
  - NCRs/SIs from CG about prequal → `00 — Pre-Qualification & Procurement` (stage 35)
  - Technical design deliverables → respective discipline packages `01 — Architecture` etc. (stage 36)

### 2. Verify Assignee Correctness

Before creating/updating, check assignment rules:
- **Sultan [151]** → DD stage technical packages ONLY (plans, specs, design review)
- **Mohamed Samir [564]** → site execution, procurement, prequal sourcing
- **Hani Alghamdi [478]** → purchasing, RFQs, material submittals
- **Hesham [163]** → document control, submissions
- **Ahmed Salah [162]** → coordination, manufacturing orders
- **Ali [160]** → technical office (DD stage technical work)

NCRs, SIs, and prequal-related items belong to the procurement team (Samir + Hani), NOT Sultan.

### 3. Search Outlook for Related Emails

- Query Outlook SQLite for document codes and keywords
- Key tables: `Mail` JOIN `folders` on `Record_FolderID`
- Common subject codes: `SI-CG-ASEER-*`, `NCR-*`, `PL-*`, doc prefixes like `MOC-MUS-ASE-*`
- Full preview: `substr(Message_Preview, 1, 1500)`

### 4. Extract Attachments (AppleScript)

```applescript
tell application "Microsoft Outlook"
    set theMsg to message id <ID>
    set atts to (every attachment of theMsg)
    set outFolder to "/tmp/<project>/"
    do shell script "mkdir -p " & quoted form of outFolder
    repeat with att in atts
        set attName to name of att
        set savePath to outFolder & attName
        do shell script "touch " & quoted form of savePath
        set saveFile to POSIX file savePath as alias
        save att in saveFile
    end repeat
end tell
```

### 5. Read PDF Content

```bash
pdftotext /tmp/<project>/file.pdf - | head -2000
```

Extract: issuance date, sender, required actions, current status, CG response/comments, contract references.

### 6. Copy Files to Project Folder (NEVER /tmp paths)

```bash
cp /tmp/<project>/file.pdf "/path/to/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/09_Correspondence/"
```

Use the project structure:
- Correspondence → `09_Correspondence/`
- Plans & Procedures → `Docs/02_Plans_and_Procedures/`
- Submittals → `02_Submittals/`

**CRITICAL: Always reference the project-relative path in Odoo task descriptions, never /tmp.** Format: `Samaya/Technical Office/Bim Unit/Aseer-Museum/<subfolder>/<filename>`

### 7. Update Odoo Task with Full Context

Build a rich HTML description including:
- Source email (sender, date, subject)
- Document summary (what the NCR/SI/plan requires)
- Timeline of key events
- Current status (from CG response if available)
- File path reference
- Required actions

Also update:
- `state` based on actual status (not placeholder defaults)
- `date_assign` / `date_deadline` to real dates (not contract-end placeholders)
- `user_ids` to correct assignees (not auto-defaults)
- `tag_ids` to appropriate tags (Prequalification vs Plans & Procedures)
- `progress` to reflect actual completion level

### 8. Update Existing Related Tasks

- Review sibling tasks under the same parent for stale statuses
- Update schedule-review tasks with current deadlines
- Push prequal items with fresh dates

## Pitfalls

- **File paths**: Never use `/tmp/...` in Odoo descriptions — always project-relative paths
- **Assignee defaults**: Never leave Sultan as sole assignee for prequal/NCR/SI tasks — route to Samir + Hani
- **Placeholder dates**: `2026-09-07` is the contract end date used as a default — replace with real dates
- **Task states**: `03_approved` on an NCR means the document was filed, NOT that the NCR is resolved — verify actual CG response before setting state
- **Package placement**: NCRs and SIs about prequal/procurement go under `00 — Pre-Qualification & Procurement` (ID 3011, stage 35 Initiation), NOT under `05 — Projects Plans`

## Related Workflows

- `references/stakeholder-register-from-email.md` — Keep the Key Personnel Register and Stakeholder Register up to date by searching Outlook for appointments, departures, CV submissions, and prequalifications. Run this alongside the email-to-Odoo workflow when the user asks about updating stakeholder records.
