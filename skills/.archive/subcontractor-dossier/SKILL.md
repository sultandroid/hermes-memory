---
name: subcontractor-dossier
description: >-
  Populate a subcontractor's structured folder with all related files from across the project,
  search email archives, compile a status register, and update main project registers.
  For engineering/construction BIM project folders (Aseer Museum standard).
---

# Subcontractor Dossier — File Gathering & Register Update

## When to use
- User asks to "copy here and update registers" for a subcontractor
- User asks to "gather all docs" for a specific discipline/trade
- User asks to "populate" or "fill" a subcontractor folder
- Any 13_XX_Contractor directory that is empty or needs organising
- A new subcontractor folder needs populating with existing project documents

## CRITICAL RULES

1. **NEVER regenerate existing SCOPE_REQUEST.md** — patch or append only. The user's scope document preserves contract structure.
2. **Verify entity isolation** — Aseer-Museum files go to Aseer-Museum subcontractor folders. Do NOT cross projects (especially Tqanny vs Samaya).
3. **Deduplicate** — skip files that already exist in the target (same filename + size). The same DWG/PDF may exist in 4+ source locations.
4. **Preserve source structure** — copy files, don't move them. The originals stay in their project folders.
5. **Report what was done** — always provide a count: files copied, by subfolder, total size, and any gaps.

## Standard folder structure

Every subcontractor under `Subcontractors/13_XX_Name/` should have:

```
01_Schedule_and_BOQ/       — pricing, BOQs, schedules
02_Reference_Drawings/     — reference CAD/PDF drawings, as-builts
  Existing_AsBuilt/        — pre-existing drawings
03_Specifications_and_Standards/ — specs, discipline files, standards
04_Reference_Imagery/      — photos, reference images
05_Returned_Submittals/    — submitted packages, CG/NRS comments
06_RFIs/                   — technical queries specific to this sub
07_Approvals/              — approved stamped drawings, permits
  Email_Extracts/          — relevant email threads copied here
  Stamped_*                — stamped package sets
SCOPE_REQUEST.md           — scope definition (typically pre-exists)
<DISCIPLINE>_STATUS_REGISTER.md — comprehensive status (CREATED by this skill)
```

## Search sources (in priority order)

| Source | Path pattern | What to look for |
|--------|-------------|------------------|
| Submittals | `Submittals/` | IFC packages, material submittals, NRS comments |
| Design Files | `Design Files/`, `Design Files (Stage 04)/` | CAD drawings, design packages |
| As-Built Docs | `As-Built Docs/` | Existing as-built record drawings |
| Completed Tender Package | `Completed Tender Package From NRS/` | NRS-stamped drawings, bid packages |
| Email Archive | `Email_Archive/`, `Scripts/output/email_bodies/` | Email chains with CG/subcontractor |
| Docs | `Docs/02_Plans/`, `Docs/03_Submittals/`, `Docs/07_Reports/` | Plans, studies, submittals |
| Scripts/notes | `Scripts/notes/` | Extracted knowledge notes |
| Correspondence | `Correspondence/` | Formal letters, SI documents |
| Contracts | `Contracts/` | Signed agreements |
| Invoices | `Invoices/` | Payment records |
| odoo | `odoo/` | Odoo task records |
| Subcontractors | `Subcontractors/` | Cross-reference other subs for interfaces |

## Search commands (use delegate_task for parallelism)

### 1. Find discipline-related files across project
```bash
find "$BASE" -iname '*KEYWORD*' -o -iname '*ABBREV*' -o -iname '*REFCODE*' | head -100
```

Search for:
- Full name (e.g. "fire life safety", "fire alarm")
- Abbreviation (e.g. "FLS")
- Reference codes (e.g. "IFC-0004", "PL-0036", "PQ-0025")
- Contractor name (e.g. "Nama", "Namaa", "Nama Consulting")
- Standards (e.g. "NFPA", "SBC 801", "Civil Defense")

### 2. Search email archive
```bash
find "$BASE/Email_Archive/" -name '*.md' | xargs grep -li 'TERM1\\|TERM2' 2>/dev/null
```

### 3. Search extracted email bodies (MORE RELIABLE than Email_Archive .md files)
```bash
# Main email body extracts
find "$BASE/Scripts/output/email_bodies/" -name '*.txt' | xargs grep -li 'TERM' 2>/dev/null
# CG-specific response extracts (IFC reviews, SI responses)
find "$BASE/Scripts/output/email_bodies/cg_responses/" -name '*.txt' | xargs grep -li 'TERM' 2>/dev/null
```

**Why this matters:** Individual email .md files listed in PROJECT_EMAILS.md may not exist on disk. The actual email body text is often in `Scripts/output/email_bodies/` as `.txt` extracts. Always check these directories — they contain the full email chains including CG comments, cover letters, and technical responses.

### 4. Check PROJECT_EMAILS.md index
```bash
grep -in 'TERM' "$BASE/PROJECT_EMAILS.md"
```

### 5. Search inside specific folders
```bash
# As-Built Docs
find "$BASE/As-Built Docs" -iname '*TERM*' 2>/dev/null

# Completed Tender Package
find "$BASE/Completed Tender Package From NRS/" -iname '*TERM*' 2>/dev/null

# Submittals
find "$BASE/Submittals/" -iname '*TERM*' 2>/dev/null
```

## Copy strategy

Use `cp -v` for each file and create subdirectories as needed. For duplicates across multiple source locations, skip or deduplicate by selecting the most authoritative copy (prefer stamped/approved versions over raw files, prefer newer revisions).

### Mapping source to target

| Source folder | Target folder |
|--------------|---------------|
| Design Files/*fire*/*sprinkler* etc | 02_Reference_Drawings/Existing_AsBuilt/ |
| As-Built Docs/*fire*/*alarm* | 02_Reference_Drawings/Existing_AsBuilt/Fire_Alarm_DWGs/ |
| Submittals/* | 05_Returned_Submittals/ |
| Docs/03_Submittals/* | 05_Returned_Submittals/ |
| Docs/07_Reports/*STUDY* | 03_Specifications_and_Standards/ |
| Specs & Datasheet/* | 03_Specifications_and_Standards/ |
| Email attachments | 05_Returned_Submittals/ or relevant folder |
| Email body extracts | 07_Approvals/Email_Extracts/ |
| Stamped drawings | 07_Approvals/Stamped_* |
| RFI files | 06_RFIs/ |
| Approved documents | 07_Approvals/ |

## Create the STATUS_REGISTER.md

Create a comprehensive register with these sections:

```markdown
# DISCIPLINE Contractor — Status Register
**Project:** Aseer Regional Museum | **Contractor:** NAME
**Register ID:** XXX | **Updated:** DATE

## 1. Deliverables Summary
Table of all scope items from SCOPE_REQUEST.md with RAG status

## 2. File Inventory
By subfolder, list files with descriptions and sizes

## 3. Critical Open Issues
RAG-rated table of blockers and open items

## 4. Deliverables Progress (per RIBA tree if applicable)
Reference codes and status

## 5. Key Emails
Date | Subject | Ref | Key Detail

## 6. Email Thread Detail (for critical submissions)
Full chain: who → whom, dates, key CG/consultant positions. Include exact CG wording for Code C/D rejections — the language often reveals hidden process gates.

## 7. Contractor Engagement Status
| Item | Status | Evidence |
|------|--------|----------|
| MoC/Authority Pre-approval | ✅/❌ | Ref number + date |
| Site work performed | ✅/❌ | Document refs |
| Formal SoW/Contract signed | ✅/❌ | Location in Contracts/ |
| Design deliverables | X% produced | Count vs total |

## 8. Knowledge Gaps & Next Steps
Actions with owners and timelines
```

## Update main project registers

After populating the subcontractor folder:
1. **PROJECT_MEMORY.md** — update subcontractor count, add contractor to org chart, note IFC status
2. **RFI_REGISTER.md** — add any new FLS-specific RFIs found
3. **RIBA Deliverable Tree** — update RAG status for discipline items

## Key pitfalls

- **Email .md files may not exist on disk** — PROJECT_EMAILS.md index lists paths that may be planned but never created. Actual content is in `Scripts/output/email_bodies/` and `Email_Archive/hesham_archive_may2026.md`
- **CG comments contain hidden process gates** — always read the full CG comment chain, not just the Code letter (A/B/C/D). CG may require cross-discipline approvals (e.g. "FLS Consultant endorsement required before IFC review" or "Project Design Drawings must be approved first"). These process gates often explain WHY a Code C persists across resubmissions. Extract the exact CG wording into the status register.
- **Contractor may be approved but not contracted** — Nama Consulting was MoC-approved (PQ-0025, Feb 2026) and had done site survey work (IR-0001), but no formal SoW/contract existed. This means 0% design deliverables despite the contractor being "active". Check Contracts/ folder and note this in the register.
- **Email body extracts > email .md files** — PROJECT_EMAILS.md lists email paths that often don't exist as files. The real email text is in `Scripts/output/email_bodies/` as `.txt` extracts. Always check both locations.
- **Duplicates across source folders** — the same file often appears in 3-4 locations (Submittals/, Email_Archive/_attachments/, Docs/03_Submittals/). Pick one authoritative copy.
- **SCOPE_REQUEST.md** is the truth source for deliverables — cross-reference all findings against it
- **Contractor/ directory may have 0 matching files** — this is information too (means no engagement yet)
- **Use delegate_task for parallelism** — search project folders, emails, and other sources simultaneously (up to 3 parallel sub-agents)
- **Tqanny/Samaya separation** — NEVER cross paths between Tqanny and Samaya OneDrive folders. Verify ownership before moving/copying files.

## Verification checklist

- [ ] All 7 subdirectories exist (even if empty)
- [ ] Reference drawings copied from Design Files + As-Built Docs + Completed Tender Package
- [ ] Submittals copied from Submittals/ + Docs/03_Submittals/
- [ ] Specifications from Specs & Datasheet/
- [ ] Email extracts from Scripts/output/email_bodies/ (not just Email_Archive/)
- [ ] Approved/stamped drawings from Completed Tender Package
- [ ] SCOPE_REQUEST.md exists
- [ ] STATUS_REGISTER.md created with all sections
- [ ] PROJECT_MEMORY.md updated (subcontractor count + notes)
- [ ] 01_Schedule_and_BOQ and 04_Reference_Imagery may be empty if not available

## Reference files
- `references/fls-dossier-example.md` — Real-world Aseer FLS dossier run: source discovery order, pitfalls discovered, final stats (88 files, 193MB)
- `references/fls-email-cg-analysis-2026-06-03.md` — CG comment process-gate analysis example: hidden cross-discipline approval requirements in Code C responses