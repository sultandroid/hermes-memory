# Plan Document Extraction → Formal Repo Filing

Extract approved/submitted project plan PDFs from email attachments and file them in the Aseer Museum repo as formal read-only documents.

## Trigger

User asks to check emails for an approved plan, or sends an email thread with a plan attachment.

## Workflow

### Phase 1 — Locate the Plan

Three possible sources, check in order:

1. **OneDrive Plans_MD directory** — Pre-converted markdown files often live at:
   `04_Docs/02_Plans_and_Procedures/02.{NN}_{PlanName}/00_Master_Index/Plans_MD/`
   If the md exists here, skip PDF conversion — use the md directly.

2. **Outlook email thread** — Search by:
   - Sender (Hani Alghamdi, Mohamed Samir, Hossam Mabrouk)
   - Subject keywords (doc ref, "approved", "Code B", plan name)
   - Thread subjects like "Asir Management Plans status"
   ```sql
   SELECT Record_RecordID FROM Mail
   WHERE Message_NormalizedSubject LIKE '%Procurement Plan%'
     AND Message_SenderList LIKE '%Hani%';
   ```

3. **Aconex** — Check Aconex transmittal history if not in email or OneDrive.

### Phase 2 — Extract Attachment

Use Python generator script + osascript (see SKILL.md for full AppleScript pattern):

```python
# /tmp/gen_extract_{eid}.py
import os
eid = 48404
outdir = "/tmp/{plan_name}_extract"
os.makedirs(outdir, exist_ok=True)
script = f'''set o to "{outdir}/"
tell application "Microsoft Outlook"
  set m to message id {eid}
  repeat with a in (every attachment of m)
    if content type of a does not start with "image/" then
      set n to name of a
      ...save...
    end if
  end repeat
end tell
'''
with open(f"/tmp/ext_{eid}.applescript", "w") as f:
    f.write(script)
```

Then: `python3 /tmp/gen_extract_{eid}.py && osascript /tmp/ext_{eid}.applescript`

### Phase 3 — Process the PDF

```bash
pdftotext /tmp/extract/plan.pdf /tmp/plan.txt
```

Check if the PDF contains:
- **DS cover sheet only** (submittal form, ~150-200 lines) → actual content missing, flag to user
- **DS cover + actual plan content** → strip the DS header
- **CG response with Code B** → capture CG conditions

**DS header stripping:** The bilingual DS form starts with Arabic RTL text and ends at the line:
`Acceptance does not release the Contractor from his Responsibilities...`
Find this marker and take content after it.

### Phase 4 — Check Approval Status

Refer to `08_Document_Index/approved_plans.md` for the plan's approval history.

| If | Then |
|----|------|
| **Code B** (approved) | File to `00_Contracts/{NN}_{PlanFolder}/` with `status: formal_read_only` |
| **Code C/D** or not yet submitted | File to `03_Plans/{NN}_{PlanFolder}/` with `status: draft` |
| Status unclear | Search email/CG_STATUS.md to verify |

### Phase 5 — Create Repo Files

**Single file preferred** (user preference from Jul 2026 — no longer split into multiple part files).

Add YAML frontmatter:

```yaml
---
doc_ref: MOC-XXXX-SIC-1X0-PL-XXXX
revision: Rev.XX
title: [Plan Name]
status: formal_read_only   # or "draft"
last_updated: YYYY-MM-DD
approved_date: YYYY-MM-DD
approved_by: CG (Consultant Group)
approval_code: B (Approved with Comments)
source_file: [OneDrive path or email source]
agent_edit: prohibited
---
```

**Rules:**
- PDFs are NOT committed to git (binary policy — OneDrive is source of truth). Reference the OneDrive path in `source_file`.
- No Arabic in frontmatter or display text.
- `agent_edit: prohibited` on every file.
- If the OneDrive already has a markdown version (`Plans_MD/`), copy that instead of re-converting from PDF. Add frontmatter to it.

### Phase 6 — Update OneDrive

If the plan was extracted from email, copy the PDF back to the correct OneDrive folder:

```
cp /tmp/extract/plan.pdf "OneDrive/.../02.XX_{PlanName}/01_Source_Files/02_PDFs/MOC-XXXX_RevXX_Approved.pdf"
```

### Phase 7 — Commit

```bash
cd ~/aseer-museum-pm
git add 00_Contracts/{NN}_{PlanFolder}/
git commit -m "Add {PlanName} Rev.XX (Code B). agent_edit: prohibited." --no-verify
```

Be prepared for the post-commit hook conflict pattern:
```bash
git stash && git pull --rebase origin main
git checkout 06_Risk_System/webapp/src/index.html
git stash pop && git push origin main
```

## Plans Already Filed (00_Contracts/)

| Folder | Plan | Doc Ref |
|--------|------|---------|
| 01_DMP/ | DMP | PL-0029 Rev.02/C04 |
| 02_Communication_Plan/ | Comm Plan | PL-0027 Rev C02 |
| 03_Stakeholder_Plan/ | Stakeholder Plan | PL-0020 Rev.04 |
| 04_NRS_Methodology/ | NRS Methodology | ZD-0026 Rev.00 |
| 05_HSE_Plans/ | 9 HSE plans | PL-0041 to PL-0055 |
| 06_Subcontract_Plan/ | Subcontract Mgmt | ZD-0094 Rev.00 |
| 07_Procurement_Plan/ | Procurement Plan | PL-0014 Rev.01 |

## Common Pitfalls

- **Plans_MD files may still have DS header** — strip it before adding frontmatter
- **CG_STATUS.md may say "draft" when obligation_matrix says "Code B"** — cross-check with email evidence; the email is authoritative
- **NRS Methodology has no content on disk** — only DS cover sheet exists; document must be requested from NRS
- **Some OneDrive PDFs are scanned images** — pdftotext returns empty; use OCR or flag as image-based
