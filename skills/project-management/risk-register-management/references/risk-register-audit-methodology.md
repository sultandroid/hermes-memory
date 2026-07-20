# Risk Register Audit — Evidence Verification Methodology

## When to Use

- User asks to "audit" or "verify" the risk register
- User asks to "cross-reference" risk entries against evidence
- A new revision of the risk register (C11, C12, etc.) needs validation before publication
- Suspicious or unverifiable evidence references need investigation

## Methodology — 6-Step Evidence Audit

### Step 1 — Read the full risk register

Read the complete risk register MD file. Note the total count, snapshot summary (Open/Watch/Mitigated/Closed), and severity distribution. These should match the actual entries — flag any mismatch immediately.

### Step 2 — Read ALL supporting registers in the repo

Before touching OneDrive, exhaust the repo's own registers. Every evidence reference in the risk register should appear in at least one of these:

| Register | File | What it covers |
|----------|------|----------------|
| NCR Register | `01_Registers/ncr_register.md` | Non-conformance reports, their status, linked risks |
| Submittal Register | `01_Registers/submittal_register.md` | All submittals (PQ, MA, ZD, IFC, MS, DD gates) with CG codes |
| RFI/TQ Register | `01_Registers/rfi_register.md` | Technical queries and requests for information |
| Drawing Register | `01_Registers/drawing_register.md` | All project drawings with RACI |
| Prequalification Log | `Technical_Office/Specialist_Management/prequalification_log.md` | Specialist PQ status |
| Master Programme | `02_Schedule/master_programme.md` | Baseline dates, milestones, progress |
| Submission Plan Risk | `02_Schedule/submission_plan_risk_assessment.md` | Design submission risks and critical path |
| Treatment Files | `03_Plans/08_Risk/treatment/` | Per-risk treatment plans (may have different owners/dates than the register) |

### Step 3 — Explore the OneDrive bank for physical evidence

Navigate to the Adel Darwish (or equivalent document controller) OneDrive folder. The standard folder structure is:

```
Adel Darwish's files - 01- Execution Documents/
├── 01- Letters/ (IN/CG, IN/MOC, OUT/CG, OUT/MOC — numbered subfolders)
├── 02. DOC - Document Submittal/
├── 03. SD  SHOP DRAWING/
├── 04- Daily Report/
├── 05- Request For Information-RFI/ (TQ-005 through TQ-026)
├── 06- Weekly Meeting MOM/ (MoM-02 through MoM-15)
├── 07- Pre-Qualification Submittal/ (PQ-001 through PQ-125)
├── 08- Material Submittal MA/ (Architectural/MA-0001 through MA-0007, Electrical/)
├── 09- Method Statement MWS/ (MS-001 through MS-016)
├── 10- CG Site Instruction SI/ (SI-01 through SI-20)
├── 11- IFC Drawing/ (IFC-0001 through IFC-0008)
├── 12- NCR/ (NCR-01 through NCR-11)
├── 13- Weekly Report/
├── 14- Inspection Request (IR)/
├── 15- Start New Activity (SNA)/
├── 16- Safety Notices/
├── 17- SOR/
├── 18- MIR/
├── 19- Weekly HSE Reports/
└── 20- DDD/ (AR, ELE, ME, ci — DD gate packages)
```

### Step 4 — Cross-reference every evidence claim

For each risk entry, extract the evidence column and verify each reference:

| Reference Type | Where to Check | What to Verify |
|----------------|----------------|----------------|
| `ZD-00XX` (general docs) | Submittal register + OneDrive 02. DOC folder | Is the ZD number listed? What's its CG code? |
| `PQ-00XX` (prequalifications) | Prequalification log + OneDrive 07- folder | Is the PQ submitted? What's its CG code? Is it MoC-approved? |
| `MA-00XX` (material submittals) | Submittal register + OneDrive 08- folder | What's the CG code? Is there an Approval subfolder? |
| `NC-XXXXX` (NCRs) | NCR register + OneDrive 12- folder | Is the NCR open/closed? Does the folder exist? |
| `SI-XX` (site instructions) | OneDrive 10- folder | Does the SI folder exist? Is it open/closed? |
| `IFC-000X` | Submittal register + OneDrive 11- folder | What's the CG code? How many revisions? |
| `TQ-00XX` (technical queries) | RFI register + OneDrive 05- folder | Is the TQ open/closed? Does the folder exist? |
| `MoM-XX` (meeting minutes) | OneDrive 06- folder | Does the MoM PDF exist? |
| `LT-00XX` (letters) | OneDrive 01- Letters/OUT/CG/ | Does the letter folder exist? |
| `project_status` | Repo project_status.md | Does the claim match the status file? |
| `look_ahead` | Repo look_ahead.md | Does the claim match the look-ahead? |
| `master_programme` | Repo master_programme.md | Does the claim match the programme? |

### Step 5 — Check these specific fields for discrepancies

| Field | What to Verify | Common Issues Found |
|-------|----------------|---------------------|
| **Owner** | Compare risk register owner vs treatment file owner (in `03_Plans/08_Risk/treatment/PRR-XXXX.md`) | Owners often diverge between register and treatment plan |
| **Target Close** | Is it blank? If blank on a Critical/High risk, flag it | 9+ risks commonly have blank target close dates |
| **P × S Score** | Does the numeric score match the severity label? | Usually correct if formula-driven, but verify |
| **Status** | Does "Closed" have a close date? Does "Mitigated" have evidence? | Closed risks should have a target close date in the past |
| **NCR Count** | Count actual open NCRs from NCR register | Register often understates the count (says "7+" when 10+ exist) |
| **SI Count** | Count actual SI folders in OneDrive | Register often understates (says "15" when 20 exist) |
| **ZD References** | Check submittal register for the ZD number | Some ZD references (ZD-0076, ZD-0082, ZD-0056) may not exist in any register |
| **Snapshot Totals** | Count Open/Watch/Mitigated/Closed entries manually | Should match the summary table |

### Step 6 — Report findings in a structured format

```
# Risk Register Audit Report

**Audit date:** YYYY-MM-DD
**Register:** path/to/risk_register.md
**Evidence sources:** [list of registers and OneDrive folders checked]

## Summary
| Metric | Value |
|--------|-------|
| Risks audited | N/N |
| Discrepancies found | N |
| Risks with no issues | N |

## Discrepancies Found

### DISCREPANCY N — Risk X (PRR-XXXX) — [Brief title]
| Field | Register Says | Evidence Shows | Correct Value |
|-------|--------------|---------------|---------------|
| [field] | [register value] | [evidence value] | [corrected value] |

## Additional Observations (Not Discrepancies)
- Risks with blank target close dates (list them)
- Risks with target close = today that need status review
- Evidence references that exist but need register entries added

## Evidence Verification Summary
Table showing each referenced document, whether it was found in OneDrive, and its status.
```

## Pitfalls

- **ZD references are the most common gap.** The risk register often cites ZD-00XX numbers that don't appear in the submittal register. These may be documents that were never formally submitted through CG channels. Flag them as unverifiable.
- **NCR counts drift.** The risk register may say "7 NCRs open" but the actual NCR register shows 10+. Always count from the NCR register, not the risk register's own claim.
- **SI counts drift similarly.** Count actual SI folders in OneDrive, don't trust the risk register's number.
- **Owner mismatch between register and treatment file.** The treatment file (`03_Plans/08_Risk/treatment/PRR-XXXX.md`) is the source of truth for response actions. If the owner differs, the register should be updated to match.
- **Blank target close dates are common on Critical/High risks.** Flag these — every risk should have a target close date, especially high-severity ones.
- **Snapshot totals must be manually verified.** The summary table at the top of the register can drift from the actual entries. Count manually.
- **OneDrive folder 10 (NCR-10) may be empty.** The NCR register may note this. Don't assume an empty folder means the NCR doesn't exist — it may mean the document hasn't been filed yet.
- **Some evidence references are consolidated.** The register may say "Consolidated PRR-XXXX" — this means the evidence is shared with another risk entry. Check the linked risk's evidence column.
- **Treatment files may have different owners than the register.** Always cross-reference the owner field in `03_Plans/08_Risk/treatment/PRR-XXXX.md` against the risk register. The treatment file is the source of truth for response actions.
- **Not all ZD references are submittals.** Some ZD numbers may be internal documents that were never formally submitted to CG. They may exist in the repo or OneDrive but not in the submittal register. Check both.
