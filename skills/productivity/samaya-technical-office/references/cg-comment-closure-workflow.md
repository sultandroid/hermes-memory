# CG Comment Closure Workflow — Samaya Technical Office

## Purpose

Systematic process for closing management plans and technical documents to CG (Consultant/Contract Administrator) review comments. Applicable to Aseer Regional Museum and other Samaya projects under CG review.

## CG Response Codes

| Code | Meaning | Action Required |
|------|---------|-----------------|
| A | Approved — No comments | File and close |
| B | Approved with comments | Address comments in next submission (advisory) |
| C | Revise and Resubmit | Every comment mandatory — revise and resubmit for re-review |
| D | Rejected | Complete re-submission required |

## CG Team (Aseer Museum)

| Reviewer | Email | Role |
|----------|-------|------|
| Mohammad Elbaz | melbaz@cg.com.sa | Acting PM — primary reviewer |
| Mahmoud Afifi | mafifi@cg.com.sa | Project Management |
| Mohamed Elroby | melroby@cg.com.sa | MEP / Technical |
| Sundus Alfeer | salfeer@cg.com.sa | NCR / QHSE |
| Yasser Zaki | yzaki@cg.com.sa | Aconex system |

## Workflow Steps

### Step 1 — Locate the CG Reply

CG replies are filed under each plan's `02_CG_Responses/` folder. Alternative locations:

| Location | Path Pattern |
|----------|-------------|
| Plan folder | `02_Plans_and_Procedures/02.X_PlanName/02_CG_Responses/` |
| Email attachments | `Aseer-Museum/Email_Archive/Attachments/` |
| Email attachments (alt) | `Aseer-Museum/Email_Archive/_attachments/` |
| IFC packages | `Docs/03_Submittals/03.2_IFC_Packages/MOC-MUS-ASE-1E0-IFC-XXXX/` |
| CG response inventory | `Email_Archive/cg_response_docs_inventory.json` |

File naming: `PL-XXXX_RevXX_CG_Reply_CodeX.pdf` or `MOC-MUS-ASE-XXXX-PL-XXXX-REVXX REPLY.pdf`

### Step 2 — Extract Comments

Read the CG reviewer's comments table from the reply PDF. Typical structure:
- Comment number
- Reference section/clause
- Reviewer comment text
- Required action

**Code C**: Every comment must be addressed — no optional items.
**Code B**: Comments are advisory — can accept, modify, or reject with justification.

### Step 3 — Prepare Response per Comment

For each CG comment, one of three responses:

| Response | When to Use | Action |
|----------|-------------|--------|
| **Accept** | Comment is valid and improves the plan | Update the plan document to implement |
| **Accept with modification** | Comment intent is right but approach needs adjustment | Propose alternative that addresses the intent |
| **Reject with justification** | Comment is based on misunderstanding or contradicts scope/standards | Reference a specific clause, code, or contractual scope item |

Track in a response table:

```markdown
| # | Section | CG Comment | Response | Action Taken | Status |
|---|---------|------------|----------|-------------|--------|
| 1 | 3.2 | Add stakeholder communication matrix | Accepted | Added Table 3.1 as communication matrix | ✅ Closed |
| 2 | 4.1 | Clarify escalation procedure | Accepted with modification | Added escalation flowchart (Fig 4.1) per project org structure | ✅ Closed |
| 3 | 5.0 | Remove reference to outdated standard | Rejected | Reference is contractual requirement per ER §2.4.D — retained with footnote | ✅ Closed |
```

### Step 4 — Update Plan Document

- Increment revision: Rev.01 → Rev.02, etc.
- Apply accepted changes directly to document content
- Mark changed sections (revision clouding, underline, or [Rev.02] tags)
- Update the document's revision history table

### Step 5 — Update CG_STATUS.md

In the plan's `02_CG_Responses/CG_STATUS.md`:

```markdown
## Status Overview
- 🔴 **Code C:** 0 active | ✅ **Closed:** 1
- Last resubmission: YYYY-MM-DD (PL-XXXX Rev.02)

## Resubmission Details
| Date | Rev | Status | Notes |
|------|-----|--------|-------|
| 2026-05-25 | Rev.01 | 🔴 Code C — 8 comments | Original submission |
| 2026-06-05 | Rev.02 | 🟡 Resubmitted | All 8 comments addressed |
```

### Step 6 — Submit Through Official Channel

- Samaya's submission conduit is **Hesham Abdelhameed** (74+ documents submitted to CG Feb-May 2026)
- Response letter (on letterhead) addresses the CG reviewer directly
- Include the comment response table as an appendix
- Attach the revised plan document

### Step 7 — Follow Through

- Confirm receipt of resubmission with Hesham
- Code C resubmissions typically get priority re-review (7-14 days)
- If no response after 7 days, send a follow-up email to the CG reviewer
- Track status changes in the Master CG Register at `02_Plans_and_Procedures/CG_Response_Register.md`

## OneDrive Lock Pitfall

When OneDrive file provider is stuck ("Resource deadlock avoided"), CG reply PDFs cannot be read. Workarounds:

1. **`find -newermt`** on attachment directories to see which files exist (metadata only)
2. **`ls -lt`** on `Email_Archive/Attachments/` to list recent PDFs by date
3. **Session history** — previous CG audit sessions may have the comment content cached
4. **Fix**: Restart OneDrive (`killall OneDrive`) or wait for sync to recover

## Aseer Museum — Current Items in Progress (as of June 2026)

| Plan | Code | CG Date | Comments | Status |
|------|------|---------|----------|--------|
| PL-0018 Communication Plan | 🔴 C | May 25 | 8 comments from melbaz | Filed, awaiting response |
| PL-0020 Stakeholder Plan | ⚪ | — | No CG response yet | Submitted Rev.01, waiting |
| MA-0006 Showcase Materials | 🔴 C | Apr 29 | CG comments from melbaz | Reply filed Apr 29 |
| IFC-0008 AV Drawings | 🟡 | Apr 28 | CG response — UNREAD | Package filed, needs review |
