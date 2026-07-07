# Submittal Review Workflow — Consultant Drawing Packages Against Reviewer Comments

Methodology for reviewing consultant-submitted drawing packages (PDFs) against specific PMC/reviewer comments, producing structured MD audit reports per discipline and a consolidated master CG compliance summary.

## Trigger

- Submittal received from consultant (NRS, etc.) for formal review
- PMC/CG sends review comments that need mapping against actual drawings
- User says "review all packages" / "let your soldiers read the PDFs"
- Pre-workshop prep with CG/PMC to discuss drawing quality and compliance

## Prerequisites

- **Document Issue Register** (Excel) — the authoritative list of expected drawings with descriptions
- **CG/PMC review comments** — email, formal comment log, or meeting minutes
- **Actual PDF files** on disk, organized by discipline folders

## Workflow

### Phase 1 — Inventory & Mapping

1. **Read the Document Issue Register** — extract all drawing entries: drawing number, title, scale, revision
2. **Map actual PDFs on disk** — walk each discipline folder, list all existing PDFs (both stamped and unstamped)
3. **Cross-reference** — flag missing drawings, corrupted files (0-byte PDFs), numbering gaps
4. **Group into disciplines** — create logical batches (GA Plans, Elevations, Ceilings, Walls, Showcases, Details, Specs, etc.)

### Phase 2 — Dispatch Subagents with Rich Context

For each discipline batch, delegate to a subagent with this context packet:

```
## CONTEXT PACKET per discipline

### Drawing Register Entries (excerpted)
Drawing number | Title | Scale | Description

### Actual PDF file paths (absolute)
Full paths to stamped and unstamped PDFs

### Reviewer Comments to Assess Against
CG #1 — Title Block Compliance
CG #2 — Drawing Numbering (ISO)
CG #3a — Internal Elevation Quality
...etc.

### Output
- MD report per discipline
- Per-drawing content summary
- Assessment against each relevant reviewer comment
- Title block and stamp status
- Cross-reference errors
```

**Key context elements to include:**
- The reviewer's exact text (so subagent can evaluate compliance against it)
- Both register descriptions AND actual file paths (so subagent can find and read PDFs)
- Expected output format

### Phase 3 — PDF Content Extraction

Subagents use `pdftotext` (from poppler) to extract text from CAD-generated PDFs:

```bash
pdftotext <input.pdf> -          # raw text to stdout
pdftotext -layout <input.pdf> -  # preserve positioning (good for schedules)
pdfinfo <input.pdf>               # metadata: page count, size, date
```

Vector-heavy CAD PDFs may have minimal extractable text. The register descriptions compensate: subagents know what SHOULD be on each drawing and can assess text evidence against expectations.

For image-based PDFs (scanned, rendered): use `tesseract` OCR as fallback.

Criteria to check per drawing:
- **Title block**: project name, drawing number, revision, submittal number, stamps
- **Content**: What elements are shown? Dimensions? Hatch patterns? Type marks? Legends?
- **Coverage**: All floors/sheet series accounted for?
- **Cross-references**: Do references to other drawings resolve correctly?
- **Consistency**: Uniform presentation style across same discipline?

### Phase 4 — Per-Discipline MD Reports

Save each report to `audit/NN_DisciplineName/report.md` with:

- **Coverage table**: drawing number → title → revision → stamp status → completeness → issues
- **Assessment against each relevant reviewer comment**: compliant/partially/non-compliant with evidence
- **Quality rating**: A (excellent) through F (failing)
- **Issues found**: with severity (CRITICAL, HIGH, MEDIUM, LOW)

### Phase 5 — Consolidated Master Summary

One subagent reads all per-discipline reports and produces two files in `audit/00_Summary/`:

1. **MASTER_CG_COMPLIANCE_REVIEW.md** — executive summary per CG comment, detailed findings mapping, cross-cutting issues, priority action register, overall package assessment

2. **CG_ACTION_CHECKLIST.md** — quick-reference table: CG Ref | Issue | Status | Criticality | Responsible | Action Required | Timeframe

### Phase 6 — Review with User

The user can then open the MD reports and walk through them in a workshop, referencing audit findings without re-reading PDFs.

## Audit Folder Structure Convention

```
audit/
├── 00_Summary/
│   ├── MASTER_CG_COMPLIANCE_REVIEW.md
│   └── CG_ACTION_CHECKLIST.md
├── 01_GA_Plans_Sections/report.md
├── 02_Internal_Elevations/report.md
├── 03_Ceilings_RCP/report.md
├── 04_Walls_Linings/report.md
├── 05_Floor_Finishes/report.md
├── 06_Showcases/report.md
├── 07_Freestanding_Walls/report.md
├── 08_Setworks_Partitions/report.md
├── 09_Furniture_Retail/report.md
├── 10_Stairs_Details/report.md
├── 11_External_Details/report.md
├── 12_Washrooms_Doors_Lifts/report.md
├── 13_Graphics_Housing/report.md
├── 14_Painted_Finishes/report.md
├── 15_Specs/report.md
└── 16_3D_Visualizations/report.md
```

Discipline subfolders are numbered 01-16 for consistent ordering regardless of alphabet. The audit folder lives at the same level as the submittal folders (alongside, not inside).

## CG Drawing Review Contacts (Aseer Museum)

| Name | Role | Email | Organization | Notes |
|------|------|-------|-------------|-------|
| Maged Zamzam | Senior Architect & QC Core Team | mzamzam@cg.com.sa | CG (PMC) | Primary reviewer for architectural DD drawings and scenography |
| Hossam Mabrouk | — | hmabrouk@cg.com.sa | CG (PMC) | General CG correspondence, NCRs, PQ evaluations |

## CG Criticality Taxonomy (Drawing Compliance Actions)

The priority/criticality levels used in CG action checklists for drawing reviews:

| Level | Definition | Deadline | Color |
|-------|-----------|----------|-------|
| **P0-CRITICAL** | Blocks CG approval — must fix before resubmission | Before resubmission | Red |
| **P1-HIGH** | Significant non-compliance — should fix before resubmission | Before resubmission | Orange |
| **P2-MEDIUM** | Important but may be tracked as open comments | Before resubmission or next issue | Yellow |
| **LOW** | Minor hygiene issue — fix when convenient | As available | Green |

**Statistical summary format for CG_ACTION_CHECKLIST.md:**

```
### Priority Count
| Priority | Count |
|----------|-------|
| P0-CRITICAL | N actions |
| P1-HIGH | N actions |
| P2-MEDIUM | N actions |
| LOW | N actions |
| **TOTAL** | **N actions** |

### Quick Stats
- **Drawings compliant with all CG comments:** X of ~NNN
- **CG comments fully compliant:** X of N
- **Total missing/problematic drawings:** N+
- **Unstamped drawings:** N+
- **Most critical single issue:** [description]
- **Most widespread issue:** [description]
```

## Forwarding CG Comments to Designer (NRS)

When CG review comments are received and need to be forwarded to the design consultant (NRS):

1. **Map CG comments to design responsibility** — which comments belong to NRS scope vs Samaya internal (title blocks, stamps, document control)
2. **Draft forwarding email** with CG's exact comment text preserved (do not rewrite or summarize)
3. **Add action table** mapping each comment to required NRS action
4. **Attach the MASTER_CG_COMPLIANCE_REVIEW.md** or CG's original email as reference
5. **Set realistic deadline** based on NRS contract review turnaround (3 working days per Art. 5.5) and resubmission urgency

**Typical forwarding email structure:**
- Subject: `FW: [CG Ref] — DD Drawing Review Comments — Aseer Museum`
- Body: Brief context paragraph + table of comments + required action + deadline
- Include all original CG attachments

## Key Reviewer Comment Categories (Aseer Museum CG Template)

These reoccur across submittal reviews. Map each to its evaluation criteria:

| CG Ref | Topic | Evaluation Criteria |
|--------|-------|-------------------|
| CG #1 | Title Block Compliance | Approved template? Reference log complete? Submittal number valid? |
| CG #2 | Drawing Numbering (ISO) | DMP/BEP coding? Naming convention consistent? |
| CG #3a | Internal Elevations | Hatch patterns + Type Marks + legends? Dimensions (overall + detail)? Fixtures/joinery/opening shown? |
| CG #3b | Floor Finish Plans | Construction joints removed at DD? Hatch clarity? Type marks linked to legend? |
| CG #3c | Reflected Ceiling Plans | Background clutter removed? Ceiling-only + coordinated MEP? Ceiling-to-wall relationship shown? |
| CG #4 | Building Sections | Minimum 4 sections? Updated to current design? In approved title block? All elements labelled? |
| CG #5 | 3D Entourage Figures | Saudi national dress only? No Gulf/Emirati figures? |
| CG #6 | Missing/Unstamped Drawings | All drawings match register? All stamped? Latest title block? |

## Pitfalls

- ⚠️ **Subagents write to relative paths** — the working directory inside a subagent may not be what you expect. Always use **absolute paths** for file output in subagent context.
- ⚠️ **Vector PDFs have minimal extractable text** — many CAD PDFs are mostly vector graphics with only title block text extractable. The register descriptions are your primary content guide.
- ⚠️ **Split reports across subfolders** — don't put 16 reports in one folder. The numbered structure keeps it navigable.
- ⚠️ **3D view entourage verification requires human visual check** — no PDF extraction can determine if figures wear Thobe/Abaya vs Gulf dress. Flag this for manual inspection.
- ⚠️ **Subagent max concurrency is 3** — batch disciplines into groups of 3 for parallel dispatch.
- ⚠️ **pdftotext may not be installed** — verify with `which pdftotext` first; install poppler if missing (`brew install poppler` on macOS).
- ⚠️ **Corrupted PDFs (0 bytes)** — handle these explicitly in audit reports rather than silently skipping.
