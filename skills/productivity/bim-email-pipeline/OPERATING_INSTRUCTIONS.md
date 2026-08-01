# 📧 BIM Email Pipeline — Operating Instructions for Mac Agent

> **Target agent:** The agent running on macOS (Mohamed Essa's MacBook)
> **Purpose:** Read Outlook emails + attachments, classify by project, extract decisions/actions, distribute to repo sections
> **Pipeline:** `bim_email_pipeline.py` (v2.1) + `bim_fetch_emails.applescript` + `bim_download_attachment.applescript`
> **OneDrive BIM Unit:** `/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/`
> **Hub repo:** `sultandroid/hermes-memory` (cross-project)
> **Project repos:** `aseer-museum-pm`, `samaya-workspace`, `RCRC-Exhibition-Proposal`, etc.

---

## 1. الـ Pipeline Flow (كيفية القراءة)

### Step 1 — Fetch New Emails

Run `bim_fetch_emails.applescript` (or the pipeline via `bim_email_pipeline.py`).

The AppleScript checks Outlook folders:
- **Inbox** — all incoming
- **Aseer Museum** — project-specific folder (if configured)
- **CG / Consultant** — consultant correspondence
- **MoC** — Ministry of Culture correspondence
- **NRS** — designer correspondence
- **Samaya Internal** — internal team emails

**Output:** JSON file with email metadata (subject, sender, date, body preview, attachments list).

### Step 2 — Classify by Project + Category

For each email, classify using this matrix:

| Project | Category | Repo destination |
|---|---|---|
| **Aseer Museum (P219)** | Contract / VO / EOT | `aseer-museum-pm/04_Letters/` |
| | Design / Drawings | `aseer-museum-pm/02_CG_Responses/` |
| | RFI / Submittals | `aseer-museum-pm/05_RFIs/` |
| | Risk / NCR | `aseer-museum-pm/06_Risk_System/` |
| | Schedule / Programme | `aseer-museum-pm/02_Schedule/` |
| | Cost / Payment | `aseer-museum-pm/04_Cost/` |
| | Comms / General | `aseer-museum-pm/05_Comms/` |
| | Decisions | `aseer-museum-pm/00_Decisions/` |
| **Samaya Factory (244)** | Operations | `samaya-workspace/` (root) |
| | Procurement | `samaya-workspace/` |
| | HR / Staff | `samaya-workspace/` |
| **RCRC Exhibition (324)** | Tender | `RCRC-Exhibition-Proposal/` |
| | Design | `RCRC-Exhibition-Proposal/` |
| **Cross-project** | Training / Lessons | `hermes-memory/training/` |
| | Skills | `hermes-memory/skills/` |
| | Contacts | `hermes-memory/CONTACTS.md` |
| | Memory | `hermes-memory/MEMORY.md` |

### Step 3 — Download Attachments

Run `bim_download_attachment.applescript` for each attachment.

**Attachment types and how to handle them:**

| Type | Action | Destination |
|---|---|---|
| **PDF** (contract, letter, drawing, submittal) | Extract text via PyPDF2 / pymupdf | Project repo subfolder per category |
| **DOCX** (letter, report, SOW) | Extract text via python-docx | Project repo subfolder per category |
| **XLSX** (BOQ, schedule, register) | Extract data via openpyxl | Project repo subfolder per category |
| **DWG** (CAD drawing) | Note metadata only (cannot parse on Mac easily) | Project repo subfolder + note "DWG — view in CAD" |
| **PDF of drawing** | Extract text if available; note drawing number | Project repo subfolder |
| **Image (PNG/JPG)** | Note metadata; cannot extract text | Project repo subfolder + note "Image — visual only" |

### Step 4 — Extract Decisions + Action Items

For each email, extract:

1. **Decisions made** (who decided what, when)
2. **Action items** (who must do what, by when)
3. **Directives** (instructions from MoC/CG/NRS)
4. **Deadlines** (new dates, extensions, milestones)
5. **Risks** (new risks, risk changes)
6. **Lessons** (what went wrong, what worked)

**Output format:**

```markdown
## Email: [Subject]
**From:** [Sender] → **To:** [Recipients]
**Date:** [Date]
**Category:** [Project/Category]
**Attachments:** [List]

### Summary
[2-3 sentence summary]

### Decisions
- [Decision 1]
- [Decision 2]

### Action Items
- [ ] [Action 1] — Owner: [Name] — Due: [Date]
- [ ] [Action 2] — Owner: [Name] — Due: [Date]

### Directives
- [Directive 1]
- [Directive 2]

### Deadlines / Milestones
- [Date]: [Milestone]

### Risks
- [Risk 1] — Status: [Open/Closed]

### Lessons
- [Lesson 1]
```

### Step 5 — Distribute to Repo Sections

For each classified email, write to the correct repo section:

#### Aseer Museum PM (`aseer-museum-pm/`)

| Section | What goes there | File naming |
|---|---|---|
| `00_Decisions/` | Any decision made by MoC, CG, NRS, or Samaya | `YYYY-MM-DD_subject.md` |
| `02_CG_Responses/` | CG review comments, approvals, rejections | `CG_YYYY-MM-DD_subject.md` |
| `04_Letters/` | Formal letters (MoC, CG, NRS) | `LET_MOC_NNN.md` or `LET_CG_NNN.md` |
| `05_Comms/` | General correspondence, meeting minutes | `COMMS_YYYY-MM-DD_subject.md` |
| `05_RFIs/` | RFIs and responses | `RFI_NNN.md` |
| `06_Risk_System/` | Risk-related emails, NCRs | `RISK_YYYY-MM-DD_subject.md` |
| `02_Schedule/` | Schedule updates, programme changes | `SCHED_YYYY-MM-DD_subject.md` |
| `04_Cost/` | Cost-related, payment, VO pricing | `COST_YYYY-MM-DD_subject.md` |
| `09_Agent_Workspace/` | Agent analysis, summaries, working notes | `AGENT_YYYY-MM-DD_subject.md` |

#### Samaya Workspace (`samaya-workspace/`)

| Section | What goes there | File naming |
|---|---|---|
| Root | Factory operations, procurement, HR | `YYYY-MM-DD_subject.md` |
| `reports/` | Reports, analyses | `REPORT_YYYY-MM-DD_subject.md` |

#### RCRC Exhibition (`RCRC-Exhibition-Proposal/`)

| Section | What goes there | File naming |
|---|---|---|
| Root | Tender-related emails | `TENDER_YYYY-MM-DD_subject.md` |

#### Hermes Memory (Cross-Project)

| Section | What goes there | File naming |
|---|---|---|
| `training/` | Lessons learned (cross-project) | Per topic folder |
| `CONTACTS.md` | New contacts, role changes | Append with `[YYYY-MM-DD]` |
| `MEMORY.md` | Cross-project procedural memory | Append with `[YYYY-MM-DD]` |
| `PROJECTS.md` | Project status changes | Append with `[YYYY-MM-DD]` |

---

## 2. الـ Classification Rules (مهم جداً)

### Rule 1 — Project First

Always classify by project first, then category. If an email mentions multiple projects, create a file in each project's repo with a cross-reference.

### Rule 2 — Formal Letters vs Informal Emails

| Type | How to handle |
|---|---|
| **Formal letter** (numbered, with letterhead) | Save to `04_Letters/` with proper naming (`LET_MOC_NNN.md` or `LET_CG_NNN.md`) |
| **Informal email** (no letterhead, conversational) | Save to `05_Comms/` or `09_Agent_Workspace/` |
| **Meeting minutes** | Save to `05_Comms/` with `MINUTES_YYYY-MM-DD_subject.md` |
| **RFI** | Save to `05_RFIs/` with `RFI_NNN.md` |

### Rule 3 — Attachments

For each attachment:
1. Download to `~/Downloads/_email_attachments/`
2. Extract text (if PDF/DOCX/XLSX)
3. Save extracted text to the same repo section as the email
4. Note the attachment filename in the email's markdown file
5. If the attachment is a **contract, SOW, or ER** — save to `00_Contracts/` or `00_Project_Charter/`

### Rule 4 — Decisions

Any email that contains a decision (from MoC, CG, NRS, or Samaya management) must be:
1. Saved to `00_Decisions/` as a separate file
2. Cross-referenced in the email's markdown file
3. If the decision affects the contract (VO, EOT, scope change), also note in `00_Contracts/00_Contract_Summary.md`

### Rule 5 — Action Items

Extract action items with:
- Owner (who)
- Action (what)
- Deadline (when)
- Status (open/closed)

Update the action item register in `01_Registers/action_item_register.md` (if it exists) or create a new one.

### Rule 6 — Risks

Any email that mentions a new risk, risk change, or NCR must be:
1. Saved to `06_Risk_System/`
2. Cross-referenced in the risk register (`01_Registers/risk_register.md` or `06_Risk_System/`)

### Rule 7 — Lessons

Any email that reveals a lesson (what went wrong, what worked, a new pattern) must be:
1. Saved to `hermes-memory/training/<topic>/lessons.md` (cross-project)
2. With a timestamp prefix: `[YYYY-MM-DD] New lesson: ...`

---

## 3. الـ Priority Matrix (إيه الأهم)

| Priority | Email type | Action |
|---|---|---|
| 🔴 **CRITICAL** | MoC letters, CG directives, NRS design changes, Contract amendments | Process within 1 hour |
| 🟡 **HIGH** | RFIs, submittals, schedule updates, cost changes | Process within 4 hours |
| 🟢 **MEDIUM** | Meeting minutes, general correspondence, internal team emails | Process within 24 hours |
| 🔵 **LOW** | Newsletters, notifications, CC-only emails | Process within 1 week |

---

## 4. الـ Output Format (لكل إيميل)

```markdown
---
source: email
project: aseer-museum-pm
category: letters
priority: high
date: 2026-08-01
from: "Mohamed Afifi (CG)"
to: "Sultan Issa (Samaya)"
subject: "RE: MEP Design Submission — AD Engineering"
attachments:
  - "AD_Engineering_Proposal_7-2475-26-B-D.pdf"
  - "MEP_Scope_Matrix.xlsx"
---

# Email: RE: MEP Design Submission — AD Engineering

## Summary
CG acknowledges receipt of AD Engineering's proposal and requests clarification on the Mechanical scope split.

## Decisions
- CG confirms AD Engineering is acceptable as MEP designer
- CG requires AD Engineering to submit PI Insurance certificate before NTP

## Action Items
- [ ] Submit AD Engineering PI certificate to CG — Owner: Sultan — Due: 2026-08-07
- [ ] Clarify Mechanical scope split (Samaya drafts vs AD Engineering reviews) — Owner: Sultan — Due: 2026-08-07

## Directives
- CG will not approve NTP until PI certificate is received

## Deadlines / Milestones
- 2026-08-07: PI certificate deadline
- 2026-08-14: Target NTP

## Risks
- AD Engineering PI certificate not yet received — Status: Open

## Lessons
- [2026-08-01] CG requires PI certificate before NTP — this is a new requirement not in the original contract
```

---

## 5. الـ Distribution Script (Automation)

The pipeline already has `bim_email_pipeline.py` which handles Steps 1-3. Steps 4-5 (extraction + distribution) need to be added.

**Proposed addition to the pipeline:**

```python
def extract_decisions(email_body):
    """Extract decisions, actions, directives from email body."""
    # Use regex patterns:
    # - "قررنا" / "decided" / "approved" / "rejected"
    # - "مطلوب" / "required" / "action" / "please"
    # - "تاريخ" / "deadline" / "due" / "موعد"
    # - "خطر" / "risk" / "NCR" / "non-conformance"
    pass

def distribute_to_repo(email_data, project, category):
    """Write email data to the correct repo section."""
    repo_path = get_repo_path(project)
    section_path = get_section_path(repo_path, category)
    filename = generate_filename(email_data, category)
    write_markdown_file(section_path, filename, email_data)
    update_register(project, category, email_data)
```

---

## 6. الـ Cron Schedule

| Time | Activity |
|---|---|
| **Every 2 hours** (08:00-18:00) | Fetch new emails + classify + extract |
| **Daily at 18:00** | Full scan + distribution + register update |
| **Daily at 10:00** | Sync with hub (git push) |

---

## 7. الـ Error Handling

| Error | Action |
|---|---|
| Outlook not running | Launch Outlook via AppleScript |
| OneDrive not synced | Wait 30 seconds, retry |
| Attachment download fails | Log error, skip, retry next cycle |
| Git push fails | Log error, retry next cycle |
| Pipeline lock file exists | Wait 60 seconds, retry (another instance running) |

---

## 8. الـ Testing (Before Going Live)

1. **Test with 1 email** — fetch, classify, extract, distribute
2. **Test with 1 attachment** — download, extract text, save
3. **Test with 1 decision email** — extract decision, save to `00_Decisions/`
4. **Test git push** — commit + push to correct repo
5. **Test cron** — schedule every 2 hours for 1 day

---

## 9. الـ Key Contacts (for classification)

| Name | Role | Project | Email domain |
|---|---|---|---|
| Mohamed Afifi | CG Project Manager | Aseer | @cg-group.com |
| Abdelrahman Al-Arjani | MoC Project Manager | Aseer | @moc.gov.sa |
| Jim Richards | NRS Director | Aseer | @nissenrichardsstudio.com |
| Julie Riley | Studio ZNA Director | Aseer | @studiozna.com |
| Eassa Al Tamimi | AD Engineering CEO | Aseer | @ad-engineering.com |
| Hossam Mabrouk | ACE PMC | Aseer | @ace-mb.com |
| Mohamed Elbaz | CG Engineer | Aseer | @cg-group.com |
| Adel Al-Qahtani | Samaya CEO | All | @samayainvest.com |
| Abdullah Al-Ajmi | Samaya COO | All | @samayainvest.com |
| Mohamed Samir | Samaya Technical Office | All | @samayainvest.com |
| Ali Abdel Rahman | Samaya BIM Manager | All | @samayainvest.com |
| Hani Alghamdi | Samaya Designer | All | @samayainvest.com |

---

## 10. الـ Final Checklist (Before Each Run)

- [ ] Outlook is running
- [ ] OneDrive is synced
- [ ] Pipeline lock file is clear
- [ ] Git repos are up to date (git pull)
- [ ] Enough disk space for attachments
- [ ] Previous run completed successfully (check log)

---

*These instructions are for the Mac agent running the BIM Email Pipeline. The Linux agent (this session) does not have direct access to Outlook or OneDrive.*