# Verbal Daily Task → Odoo Mapping

Trigger: Technical Office manager (Sultan) lists daily verbal tasks and expects them mapped to Odoo project 219 (Aseer Museum).

## Workflow

### Step 1 — Check Existing Odoo Structure First

Before creating anything, query existing packages and subtasks:

```python
# Get all top-level packages in project 219
pkgs = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
    [[['project_id', '=', 219], ['parent_id', '=', False]]],
    {'fields': ['id', 'name', 'stage_id', 'state', 'progress', 'date_assign', 'date_deadline'],
     'order': 'id asc', 'limit': 80})

# Check subtasks under a specific package
subs = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
    [[['parent_id', '=', package_id]]],
    {'fields': ['id', 'name', 'state', 'progress']})
```

### Step 2 — Categorize Each Task

Three categories emerge when mapping:

| Category | Condition | Action |
|----------|-----------|--------|
| **Already exists, in progress** | Matched by name/code in existing subtasks with state=01_in_progress | Update progress/state after user confirms completion |
| **Already exists, done** | Matched item with state=1_done or 03_approved | **FLAG** — ask user if they want Rev.02 or a fresh task |
| **New task** | No match found in any existing subtask | Create as new subtask under the appropriate package |

### Step 3 — Assign Correct Package

Common package targets for verbal tasks:

| User Says | Odoo Package | Tag |
|-----------|-------------|-----|
| Schedule, plan, procedure, stakeholder, PEP, meeting | `05 — Projects Plans` [2946] | Plans & Procedures [141] |
| BIM, coordination, ACC, model review | `05 — Projects Plans` [2946] | BIM / Coordination [57] or Plans & Procedures [141] |
| NRS drawing, architecture review | `05 — Projects Plans` [2946] or `01 — Architecture` [2938] | R1-RFI-Design-NRS [137] or A1-Architecture [130] |
| Prequalification, specialist, procurement | `00 — Pre-Qualification & Procurement` [3011] | Prequalification [140] |
| Pricing, RFQ | `02 — Pricing & RFQs` [3014] | Prequalification [140] |

### Step 4 — Flag Contradictions

When the user says "initiate X" or "finalize X" but the corresponding item already exists as **1_done**:

- **Do NOT silently create a duplicate.** 
- Flag the existing task and ask: "This already exists as 1_done — do you want a new revision (Rev.02) or is this a different task?"
- Example: Stakeholder Plan PL-0020 Rev.01 already done → ask about Rev.02
- Example: PEP PL-0019 already done → ask about new version

### Step 5 — Present Mapping Before Executing

Show the user a table BEFORE creating/updating anything. Structure:

```
Package: [Name] (ID XXXX)

| # | Task | Action | Details |
|---|------|--------|---------|
| 1 | Task name | Update existing [ID] | Currently PROGRESS=X → update to Y |
| 2 | Task name | New subtask | Tag: T, Assign: UIDs |
```

Also list items needing clarification in a separate section. Wait for user confirmation before any writes.

## Common Patterns From Conversation History

- "Finalize schedule review w/ Elshaikh" → PL-0057-2 already exists at [3207], update progress
- "Invite CG to ACC for BIM review" → new subtask under 05 — Projects Plans, tag BIM / Coordination
- "Review NRS drawing w/ Ali" → new subtask under 05 — Projects Plans, tag R1-RFI-Design-NRS
- "Meeting w/ Eng. Salah for BIM" → new subtask under 05 — Projects Plans, tag BIM / Coordination
- "Push all missing prequalifications" → update existing subtasks under 00 — Pre-Qualification [3011]
- "Push missing specialists" → same pool, focus on Tier 2/3 items at PROGRESS=0.0

## Step 6 — Post-Creation Enrichment from Outlook

After creating Odoo tasks, the user may ask you to find supporting context (login info, attachments, email threads) to enrich a specific task. This is common for tasks like ACC invites, drawing reviews, or meeting preparations.

### Workflow

1. **Search Outlook** using SQLite for relevant emails by keyword (project code, person name, ACC, subject keyword):
   ```sql
   SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
          f.Folder_Name, m.Message_SenderList, m.Message_NormalizedSubject, m.Message_HasAttachment
   FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
   WHERE m.Message_NormalizedSubject LIKE '%CG BIM%' OR ...
   ORDER BY m.Message_TimeReceived DESC;
   ```

2. **Identify the key email** — the one that has the attachment/list the user needs. Prioritize emails from external stakeholders (CG consultants, vendors) over internal forwards.

3. **Extract attachments** via AppleScript (save to /tmp first for processing):
   ```applescript
   tell application "Microsoft Outlook"
       set theMsg to message id <ID>
       set att to first attachment of theMsg
       set savePath to "/tmp/<context_name>/" & name of att
       do shell script "mkdir -p /tmp/<context_name> && touch " & quoted form of savePath
       save att in (POSIX file savePath as alias)
   end tell
   ```

4. **Read the attachment** (Excel/PDF) for actionable data using Python.

5. **Copy to project folder** — immediately move the file from /tmp to the correct project folder path (under OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/<Project>/). Choose the subfolder:
   - `09_Correspondence/` — incoming correspondence from external parties
   - `10_Plans/` — plan documents
   - `Subcontractors/` — subcontractor-related
   - Root project folder — if no specific subfolder fits

   ⚠ **CRITICAL: NEVER reference /tmp paths in Odoo task descriptions.** Always copy the file to the project folder first, then reference the project-relative path.

6. **Update the Odoo task description** with extracted context + the project folder path, NOT a /tmp path. Uses the `description` (HTML) field:
   ```python
   models.execute_kw(db, uid, pw, 'project.task', 'write', [[task_id], {
       'description': '<h3>Title</h3><p><b>Source:</b> ...</p><table>...</table>'
   }])
   ```

### Example from Session
- Task: BIM-001 — Invite CG to ACC BIM Model Review
- Email found: "CG BIM USERS" from Mohammad Elbaz (melbaz@cg.com.sa)
- Attachment: `CG BIM users.xlsx` with 10 CG users
- Action: Extracted the xlsx, read with openpyxl, formatted the 10 users as an HTML table, wrote it into the task's `description` field in Odoo. Copied file from /tmp to `Samaya/Technical Office/Bim Unit/Aseer-Museum/09_Correspondence/` before referencing.

### NCR Task Placement Rule

Non-Conformance Reports (NCRs) must be placed under the package that matches their subject, NOT under "05 — Projects Plans":

| NCR Subject | Correct Package | Assignee |
|-------------|----------------|----------|
| Failure to submit prequal, material samples, or delivery schedule | `00 — Pre-Qualification & Procurement` [3011] | Mohamed Samir [564] or Hani [478] |
| HSE, safety violations | `05 — Projects Plans` [2946] (HSE plans subfolder) | Hesham or HSE team |
| Technical/design non-conformance | Discipline package (e.g., `01 — Architecture` [2938]) | Sultan [151] or Ali [160] |
| Site execution issues | `00 — Site Fabrication & Installation` [3018] or relevant [REF] package | Mohamed Samir [564] |

If an NCR lands in the wrong package, move it and reassign. Sultan is the Technical Office manager, NOT the prequal/procurement owner — NCRs about prequal failures belong to Mohamed Samir + Hani.

### Advanced Enrichment: NCR / Formal Document Processing

When the user asks about an NCR task and how to update it, the full workflow involves extracting the NCR PDF, cross-referencing with the Outlook email thread, and updating Odoo.

#### Step-by-step

1. **Identify the NCR emails in Outlook** — usually two: the original NCR from CG (Hossam Mabrouk, attachment=1) and Samaya response (Adel Darwish forwarding). Query both:

   ```sql
   SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
          f.Folder_Name, m.Message_SenderList, substr(m.Message_Preview, 1, 500)
   FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
   WHERE m.Message_NormalizedSubject LIKE '%NC-1A0-008%'
   ORDER BY m.Message_TimeReceived;
   ```

2. **Extract the NCR PDF** from CG email:
   ```applescript
   tell application "Microsoft Outlook"
       set theMsg to message id <ID>
       set att to first attachment of theMsg
       set savePath to "/tmp/ncr_attachment/" & name of att
       do shell script "mkdir -p /tmp/ncr_attachment && touch " & quoted form of savePath
       save att in (POSIX file savePath as alias)
   end tell
   ```

3. **Parse PDF with pdftotext** — extract: Non-Conformance description, Required Actions, References, Deadlines, signature sections (blank = not yet responded):
   ```bash
   pdftotext /tmp/ncr_attachment/<NCR>.pdf -
   ```

4. **Analyze thread for status:** date issued, deadline to reply, was Samaya response a formal corrective action or acknowledgment? Check if Root Cause / Proposed Corrective Action / QA/QC Manager signature sections are blank.

5. **Move task to correct package** if mis-placed (common: under 05 - Projects Plans when it should be under 00 - Pre-Qualification):
   ```python
   models.execute_kw(db, uid, pw, 'project.task', 'write', [[task_id], {
       'parent_id': 3011,              # correct package
       'stage_id': 35,                 # Initiation
       'user_ids': [(4, 564), (4, 478)],  # M. Samir + Hani
       'tag_ids': [(6, 0, [140])],     # Prequalification tag
       'date_deadline': deadline_from_pdf,
   }])
   ```

6. **Copy NCR PDF to project folder** (NEVER /tmp in descriptions):
   `Samaya/Technical Office/Bim Unit/Aseer-Museum/09_Correspondence/<NCR>.pdf`

7. **Update Odoo task description** with structured HTML: NCR ref, issuer, date, deadline, non-conformance description, required actions as ordered list, contract references, timeline, which signature sections are still blank, project path to filed PDF.

## Pitfalls

- **Don't create duplicates** — always search Odoo first, including by partial name match (`'=ilike'`)
- **Don't silently overwrite** — if a plan is already 1_done but user says "initiate", ask
- **Don't guess package** — when ambiguous, tag under 05 — Projects Plans (it's the catch-all for coordination/management tasks)
- **Always state what package a new subtask goes under** — the user needs to verify the placement
