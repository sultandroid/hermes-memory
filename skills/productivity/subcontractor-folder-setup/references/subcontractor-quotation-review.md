# Subcontractor Quotation Review — Scope Compliance Check

## Trigger

User asks to review a subcontractor quotation/proposal against project contract documents (ER, SOW, DMP).

## Workflow

### Phase 1 — Gather Source Documents

1. **Find the quotation email** — search Outlook SQLite by sender domain or subject keywords
   ```sql
   SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
          f.Folder_Name, m.Message_SenderList, m.Message_NormalizedSubject
   FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
   WHERE m.Message_SenderAddressList LIKE '%vendor.com%'
      OR m.Message_NormalizedSubject LIKE '%lighting%'
   ORDER BY m.Message_TimeReceived;
   ```

2. **Extract attachments** via AppleScript (write .scpt file, run with osascript — avoid heredoc issues)

3. **Read the quotation** with `pdftotext` — identify: proposed fee, scope of work, exclusions, payment schedule, terms, validity period

### Phase 2 — Establish the Correct Baseline (CRITICAL)

**Always use the approved/submitted scope of work (SOW) as the baseline** — never an internal revision unless explicitly instructed.

Check what was actually approved:
- Was the SOW submitted to CG? What's the doc code (e.g., `ZD-0056`)?
- What status did CG return? (Code A/B/C/D)
- Did the user cross-reference internally before submission?

**Pitfall: Don't grade against a draft internal revision.** If a Rev 01 was prepared but never submitted, it's not the contract baseline. The approved document is the one that went through formal review.

### Phase 3 — Cross-Reference Against Contract Documents

Compare the quotation against:

| Document | What to Check |
|---|---|
| **Employer's Requirements (ER)** | Performance criteria, codes, standards, specific deliverables (e.g., emergency lighting §3.6) |
| **Scope of Work (SOW)** | Specific sections per discipline (e.g., §6.22.3 lighting design, §8.8 lighting installation, §11 handover) |
| **Design Management Plan (DMP)** | BIM/LOD requirements, submittal stages, approval gates |
| **NRS Methodology** | Review procedures, SLA timelines |

### Phase 4 — Gap Classification

For each gap found, classify it:

| Label | Meaning | Action |
|---|---|---|
| **ZNA scope gap** | Missing deliverable that IS in the subcontractor's scope | Request addition + fee adjustment |
| **Other party gap** | Missing item that belongs to another contractor (MEP, BIM specialist, etc.) | Remove from this subcontractor's register — do NOT mention to them |
| **Scope split change** | Baseline assumed different party does the work | Update internal registers; don't burden subcontractor with it |

**Pitfall: Don't tell the subcontractor about other contractors' scope.** The scope split is an internal management concern. Telling them "you don't do X, the MEP Contractor does X" creates confusion. Their SOW already defines what they do.

### Phase 5 — Payment Schedule Alignment

Compare the proposed payment schedule against our submittal register gates:

| Proposed (time-based) | Required (deliverable-based) |
|---|---|
| Commencement | Mobilization (on signed appointment + action plan) |
| 50% internal progress | Approved 50% Design submittal |
| 75% internal progress | Approved 90% Design submittal |
| 100% internal progress | Approved 100% Design + IFC/AFC |

Rebalance percentages so:
- Mobilization: 10% max
- Design stages: 60-75% cumulative
- IFC/AFC: 10-15%
- Final/stage 6 close-out: 5%

### Phase 6 — Document Pack Preparation

When preparing to finalize the contract:

| Document | Source | Notes |
|---|---|---|
| **SOW** (approved) | The subcontractor's own submitted document — NOT an internal revision | Don't send a different SOW |
| **DMP** (approved) | From CG/NRS-approved version | Reference document |
| **CG response** (if applicable) | From email attachments | For awareness only |
| **Submittal register** | Updated with this subcontractor's deliverables only | For payment milestones |
| **Subcontractor's own quotation** | Extracted from emails | For their reference |

### Phase 7 — Draft Correspondence

Keep the email focused on what the subcontractor actually needs to act on:
- Confirm acceptance of scope
- Provide action plan (if CG asked for it)
- Accept/counter-propose payment schedule
- Submit contract draft

Do NOT include:
- Other contractors' responsibilities
- Internal scope split discussions
- Internal register updates

## Pitfalls

- **Grading against the wrong baseline** is the #1 error. Always confirm which SOW was actually submitted and approved, not which one was drafted but never issued.
- **Scope split leakage** — mentioning MEP Contractor, BIM specialist, or other parties in correspondence with the subcontractor is unnecessary and confusing.
- **Payment schedule mismatch** — subcontractors typically propose time-based milestones. We need deliverable-based tied to submittal register approval gates. This is the main negotiation point.
- **Missing the full email thread** — always check subject-thread history for earlier discussions (scope questions, BIM scope, CV reviews) that may already resolve apparent gaps.
- **Cloud file stubs** — OneDrive files may show 0 bytes locally. Extract attachments from Outlook emails instead of relying on synced files.
