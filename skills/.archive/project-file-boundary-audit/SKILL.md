---
name: project-file-boundary-audit
description: Detect and resolve cross-project file contamination in Samaya BIM/TO project folders by examining naming conventions, consultant codes, drawing numbering, and project-scope cross-references.
triggers:
  - "this file doesn't belong here"
  - "clean up project folders"
  - "هذا الملف لا يتبع هذا المشروع"
  - "نظف مجلدات المشروع"
  - "wrong project folder"
  - "file in the wrong museum folder"
  - cross-project contamination / Aseer ↔ Zamzam mix-up
  - routine QA of Samaya BIM project directories
---

# Project File Boundary Audit

Audit project folders for files that don't belong — files from Project A sitting in Project B's directory.

> ⚠️ **Entity isolation (read first):** NEVER move files between Samaya ↔ Moqtana / Tqanny / Sada_Uhud, or between any two projects, without explicit user confirmation. Always verify ownership first; report, then ask before any move/copy.

## Trigger

- User says "this file doesn't belong here" / "هذا الملف لا يتبع هذا المشروع"
- User asks to "clean up project folders" / "نظف مجلدات المشروع"
- User reports confusion about duplication across project folders
- Routine QA of Samaya BIM project directories

## Methodology

### 1. Identify the suspected file(s)

Get the file path, name, and source folder. Key attributes to note:
- Prefix codes (e.g., `A2742-`, `ZNA3297`, `GHM-SAM-ZZ-MED`)
- Consultant/designer references (e.g., `NRS`, `Goppion`, `Glasbau Hahn`, `Hasenkamp`)
- Drawing discipline codes (`SC_01` for Showcase, `SDW-` for Shop Drawings)
- Type/ID numbering (`Type 2`, `ID.Nr. 08.03`, `Type 01`)
- Project code in filename (`MOC-ASEER-` vs `ZZ-` for Zamzam)

### 2. Cross-reference with project scope

**Aseer Museum (Project 3092):**
- Exhibition Designer: NRS (Nissen Richards Studio)
- Showcase codes: SC_01, SC_02 (Shop Drawings), Type 1/2/3, ID.Nr. xx
- Drawing prefix: A2742-18xx (1800_Showcases discipline)
- NRS submittal files: `*_NRS_comments_*stamped.pdf`
- Submittal 07 = Freestanding Cases
- Other consultants: Glasbau Hahn (showcases), BCG (MEP), OTIS, Obeikan Glass

**Zamzam Museum (ID 121/P0639):**
- Exhibition/Design: GHM, Goppion, Hasenkamp
- Drawing prefix: `GHM-SAM-ZZ-`, `A22-71-KZC-ID-DRW-`
- NO NRS involvement
- Sub-streams: Visitor Center construction, Pathway Rehabilitation fit-out, Tafweej Center

### 3. Confirm project mismatch

Search the **correct** project's folders for matching/similar files — if the naming pattern, consultant code, or drawing discipline matches the other project's known structure, the file is misplaced.

### 4. Action

- Report the finding with evidence (file name patterns, consultant cross-reference)
- Offer to move or copy to correct project folder
- Update memory with new cross-contamination patterns discovered

## Pitfalls

- ⚠️ **OneDrive stubs** — many files appear as 0-byte stubs (not synced locally). Use `find` and `ls -la` to check actual sizes before concluding a file is empty.
- ⚠️ **Same consultant for multiple projects** — e.g., Goppion provides showcases for both Aseer and Zamzam. Cross-reference drawing codes, not just consultant name.
- ⚠️ **Cross-copied reference files** — PM teams sometimes intentionally copy reference PDFs between projects. Check if the file is a reference copy vs. a project deliverable.
- ⚠️ **Zero-tolerance entity isolation**: Never move files between Samaya ↔ Moqtana/Tqanny/Sada_Uhud without user confirmation. Always verify ownership.

## Reference

See `references/aseer-zamzam-patterns.md` for the specific Aseer→Zamzam showcase contamination pattern.
