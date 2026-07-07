# Aseer Museum SMP — CG-Facing Document Conventions

## Document Numbering

- Internal path: `MOC-ASEER-SIC-1K0-PL-0020` (Samaya Investment Company)
- CG-facing path: `MOC-MUS-ASE-1K0-PL-0020` (Museum Aseer)
- KPR reference: `MOC-MUS-ASE-1K0-KP-0001`

## Revision Numbering

Only count revisions **formally submitted to CG/MoC**. Internal iterations between submissions must NOT appear in the revision history table.

| Type | Example | Include? |
|------|---------|----------|
| Formal submission | Rev 00 (01-MAR-26) → CODE C | ✅ |
| Formal resubmission | Rev 01 (10-MAY-26) → REVIEW/CRS | ✅ |
| Internal QA draft | Rev 02 (11-MAY-26, 1 day after Rev 01) | ❌ |
| Internal CRS prep | Rev 03 (05-JUN-26) | ❌ |
| Formal resubmission | Rev 02 (16-JUN-26, formal) | ✅ |

## Name Format

- Always use `"Eng."` prefix for engineering personnel: `"Eng. Waris Sultan"` not `"Waris"`
- Revision history: Approved/Prepared columns use full names, not "Samaya PMO" or "Per live KPR"
- QC sign-off: Every row gets an actual person's name

## QC Sign-Off Chain

Standard 4-row structure:
1. QC-01: Technical Office (Prepared by) — Mohamed Sultan
2. QC-02: Document Controller — Hesham Abdelhamid
3. QC-03: QA/QC Manager — Mohamed Samir (on behalf, when vacant)
4. QC-04: Project Director (Approved by) — Eng. Waris Sultan

## Role-Based References in Plan

In the plan body, use role titles, not names. Reference the live KPR for current names:
- `"Per live KPR"` for most roles
- `"Name · Per live KPR"` for approved roles where name is known

Exception: QC Sign-off and Revision History tables need real names.

## CG Disposition Table

### Column Widths (standard)
| Column | Width | Reason |
|--------|-------|--------|
| # | 44px | Short code |
| Round | 65px | "R2 · 2-Jun" |
| CG Comment | 220-250px | Widest — longest text |
| Disposition | 120px | Short response |
| Ref | 50px | Short code |
| Status | 65px | Badge text |
| Route/Scope | 90px | Category name |

### Comment Preservation
CG comment text must be **preserved verbatim** — never summarize, shorten, or rephrase. Even typos (`"Structrual"`, `"seperatly"`, `"experianced"`) are part of the original CG record.

### Status Conventions
- **CLOSED** = CG confirmed resolution (Round 1 items)
- **COVERED** = Addressed in this revision, awaiting CG review (Round 2 SMP-scope)
- **SUBMITTAL-PENDING** = Depends on external submittals (DS/PQD)
- **IN-PROGRESS** = Action underway
- **RE-OPENED** = Closure withdrawn by CG

### No Legend Blocks
Do NOT include Status Legend, Route/Scope definitions, Outstanding Submittals, or Notes below the CG disposition matrix. Column headers are self-explanatory.

## Stakeholder Count Updates

When roles are added/removed, update ALL of these locations:
1. TOC chip (`15 SECTIONS · 24 PAGES · 56 ROLES`)
2. Hub diagram center (`56 stakeholder roles`)
3. Snapshot cards (Tier 1-3, External, OP, Authorities)
4. Bar chart segments
5. Section heading (`headline counts · 56 total roles`)
6. Register total text
7. CG-02 disposition (`Register with 56 roles`)
8. P/I reference text
9. Compliance summary (`56 mapped roles`)
10. TOC line entry

## Abbreviations Section

Place between §1.1 Revision History and §1.2 Document Identification:
- CTR T1 = Contractor Tier 1
- CP = Control Point
- DSN = Design Specialist
- COND = Conditional Specialist
- PI = Power/Interest score
- KPR = Key Personnel Register (live)

## Approval Status Tracking

When updating KPR statuses, distinguish:
- **Approved** = CG/MoC formally accepted (name + date known)
- **Code B** = Approved with comments (conditional approval)
- **Code C** = Revise and Resubmit (NOT approved)
- **Pending submission** = CV/PQD not yet sent to CG
- **Not yet appointed** = Role exists but no person assigned
- **Vacant** = Person left, replacement being hired
- **Nominated** = Person identified, not yet submitted to CG

## File Backup Protocol

Before delegating ANY file manipulation to a subagent:
```bash
cp <target-file> <target-file>.bak
```

Verify backup exists before making the delegate_task call. If the file is overwritten/corrupted, restore from `.bak`.

## Concurrent Version Awareness

Multiple write_file/terminal→python opens of the same Excel/HTML file can cause:
- Lost formatting when a later script writes over a formatted file
- State corruption (openpyxl's `data_only` vs formula mode)
- Duplicate rows or section-level text from string-based insertion

Always verify the file state immediately after each write.
