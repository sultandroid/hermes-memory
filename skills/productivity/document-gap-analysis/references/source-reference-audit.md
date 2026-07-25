# Source-Reference Audit — Worked Example

## Context

Audited a summary DOCX (`ASM_Design_Management_and_BIM_Execution_Plan_Summary.docx`) against its 3 cited source documents:

| Source | Code | Actual path found |
|--------|------|------------------|
| PEP Rev 04 | PL-0015 | `02.3_PEP/01_Source_Files/01_HTML/00_PEP_Plan_Rev04.html` |
| DMP Rev C03 | PL-0013 | `02.2_BEP_MIDP_TIDP/01_Source_Files/02_PDFs/MOC-ASEER-SIC-1K0-PL-0013.pdf` — but actual DMP was at `02.1_DMP/01_Source_Files/03_Word/...` |
| BEP Rev 01 | PL-0021 | `02.2_BEP_MIDP_TIDP/01_Source_Files/03_Word/00-BIM-Execution-Plan-REV 01.docx` |

## Systematic Issues Found

### 1. Wrong Section References (5 of 6 BEP refs wrong)

| Summary claimed | Actual BEP section |
|----------------|-------------------|
| BEP sec 3 | BEP sec 2.1 |
| BEP sec 5 | BEP sec 4 |
| BEP sec 7 | BEP sec 2.3 + 8.7 |
| BEP sec 8 | BEP sec 7 |
| BEP sec 9 | BEP sec 6 |

### 2. Content Not Found in Source

| Summary claimed source | What it said | Reality |
|-----------------------|-------------|---------|
| DMP sec 4,5,6,7 | ICE wheel, INT interfaces, turnaround times | None of these exist in DMP |
| BEP sec 3 | 7 BIM objectives with metrics | BEP has 6 generic objectives without metrics |
| BEP sec 5 | Aconex as CDE | Aconex not mentioned in BEP at all. BEP uses Autodesk BIM 360/Docs |
| BEP sec 9 | KPI targets K-1/K-5/K-7/K-8 | BEP Table 104 has different KPIs entirely |
| PEP sec 21 | C1-C5 communication hierarchy | PEP uses Comms Cadence Ladder (Daily/Weekly/Monthly) |
| PEP sec 19/20 | Status codes D/E/F/U | PEP only defines A/B/C |

### 3. Outdated Personnel Data

- "Eng. Adel Darwish" as Acting PD — should be Eng. Waris Sultan per SMP Rev03 (05-Jun-26)
- "Eng. Jim (NRS)" — should be Eng. Jim Richards
- "Arch BIM Lead Anwar AlRishani" — SMP Rev03 lists Ali Abdelrahman Mostafa

### 4. Software Version Mismatch

- Summary said "2025+". BEP specifies Revit/Navisworks/ReCap 2026.

### 5. Gate Sequence Error

- G3 (Shop Drawing Approval) listed at W28, which is 4 weeks before G2 (IFC Release) at W32. Shop drawings derive from IFC — G3 must come after G2.

## Correction Workflow Used

1. Search filesystem for source documents by code (PL-0015, PL-0013, PL-0021) and by name (PEP, DMP, BEP)
2. For HTML sources: grep for section headings, then read surrounding context
3. For DOCX sources: use python-docx to extract paragraphs and tables
4. Build a verdict table per claim (MATCH/MISMATCH/NOT_FOUND)
5. Update each halftone annotation with:
   - Correct section reference
   - Direct quote from source where possible
   - Caveat where Summary differs from source
   - No symbols (no sec, use "sec"; no arrows, use plain text)

## Annotation Style Template

```
Ref: {source_code} ({source_name}) sec {actual_section} ({context_note}).
{Source quote if applicable}
{Caveat if summary differs from source}
```

Example:
```
Ref: PL-0015 Rev 04 (PEP) sec 20. PEP states: "Drawing Register lists ~567 rows but only ~158
are at Rev A status — large reconciliation gap." Numbers approximate per PEP.
```

## Additional Findings from Session 2026-07-25

### Approval Status Verification

| Source | Status | Can cite as? |
|--------|--------|-------------|
| PEP Rev 04 (PL-0015) | "For CG Approval" | No — cite as "(submitted, under CG review)" |
| BEP Rev 01 (PL-0021) | Code B 17-Mar-2026 | Yes — approved with comments |
| DMP Rev C03 (PL-0013) | Not verified | Check frontmatter |
| CG Submittal (ZD-0006) | Code B 12-Jul-2026 | Yes — baseline schedule approved |
| Contract 0010003521 | Signed and effective | Yes — fully approved |

### Use Formal MD Files, Not Raw HTML

The repo stores source documents as:
- `03_Supplementary/00_PEP_Plan_Rev04.md` — structured MD with frontmatter (status, revision, date)
- `03_Supplementary/` or `reference/` folders for other docs
- Raw HTML files in `01_Source_Files/01_HTML/` — harder to search, may embed content in SVG/CSS

Always check for the MD equivalent first. Frontmatter metadata is critical for determining approval status.

### CG Status Codes — Only A/B/C/D Exist

The CG submittal form (MOC-MUS-ASE-1K0-ZD-0006) defines only 4 codes:
- A: Approved
- B: Approved with comments
- C: Revise and Resubmit
- D: Rejected

Codes E, F, U are internal project codes, not CG codes. Never claim E/F/U as CG-defined.

### KPI Targets — Not in Any Source Document

K-coded targets (K-1, K-3, K-5, K-7, K-8) were searched across PEP, BEP, DMP, and all accessible project plans. None exist. They are internal to the Summary document only. Attribute as "internal to this Summary, not from any project plan."

### Key Lessons from This Session

1. Verify approval status before citing — unapproved docs get "(submitted)" qualifier
2. Use formal MD files from repo, not raw HTML
3. CG codes A/B/C/D only — E/F/U are internal
4. KPI targets may not exist in any source document — verify all K-coded claims
5. CR M-14 and similar CG finding codes may reference documents not found in accessible repo — mark as unverified
