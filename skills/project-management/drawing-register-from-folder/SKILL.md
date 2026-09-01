---
name: drawing-register-from-folder
description: Turn a raw DD submittal folder (mixed submitted sheets + CAD working files + consultant review PDFs) into a single-sheet file/drawing register. Extract consultant approval codes from EN/AR review PDF pairs.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [registers, drawing-register, submittal, bim, document-control, pdf]
    related_skills: [project-register-manager]
---

# Drawing Register From Submittal Folder

Pattern for when the user asks "list all files inside <folder> and make a register"
for a DD/submittal folder that mixes **submitted sheets**, **CAD source/working files**,
and **consultant review PDFs**. Complement to `project-register-manager` (which tracks
SOW/ER deliverables); this one builds the register FROM the filesystem contents.

## When to use
- A `3.x_DD Documents <Disc>` submittal folder needs a file/drawing inventory + register.
- Folder is flat-ish with a few subfolders (PDF / CAD / Docs) and a "Not marked" / working set.

## Workflow
1. **Enumerate everything** (direct `os.walk`/`find`, NOT a labor CLI). Keep the full
   relative path — it becomes the Location/Notes column so files stay traceable.
2. **Inspect the PDFs before writing rows.** For each PDF run `fitz.open()` and dump
   page-0 text to identify: sheet/floor/level, drawing number, and whether it is a
   submitted layout vs a reference doc. (Sample: `python3 -c "import fitz; doc=fitz.open('f.pdf'); print(doc[0].get_text())"`.)
3. **Extract review status from consultant approval PDFs.** These follow the
   "APPROVAL REQUEST — REVIEW RESULT" template (NAMA Alamal, CG, MoC etc.) and pair
   as `*_Review_EN.pdf` + `*_Review_AR.pdf`. Pull: Discipline, Submittal, Receiving date,
   **Review result code (A/B/C/D)**, sign-off names/dates, and the numbered comments.
   Record the same code on both the EN and AR rows.
4. **Categorize into sections** (life-safety worked example):
   - `PDF — FLOOR PLANS` (escape/FA plans, one row per floor)
   - `PDF — <SYSTEM> LAYOUTS (MOC SERIES)` (per-floor MOC-ASE-* sheets)
   - `CAD — SOURCE / WORKING FILES` (master .dwg, .bak, per-sheet PNG renders, screenshots, logo blocks, plot.log)
   - `DOCS — CONSULTANT REVIEW & STANDARDS` (EN/AR review pairs + reference standards)
   - Logos/blocks/`Thumbs.db`/etc → fold into CAD or a notes-only tail, mark `Ref`, ignore system files.
5. **Register format** (1 data sheet, auto-filter + frozen header, navy header row):
   `Ref #` (sequential e.g. `LS-001`), `Drawing / File Title`, `Drawing #`,
   `Discipline` (`FLS` / `ME/FF` / `ME/FA` / `SE` / `Arch` / `Asset` / `Ref`),
   `Sheet Format` (1A0 PDF / DWG / PNG / PDF), `Stage` (DD 50% / DD Review / Reference / Working),
   `Status` (A/B/C/D, `—` for working/ref), `Location`, `Notes`.
6. Save the generator `.py` beside the register so the next revision is a re-run, not a rebuild.

## Pitfalls
- Distinguish **submitted sheets** (floor-plan PDFs, MOC-series layouts) from **working
  files** (screenshots, logo blocks, `Thumbs.db`, `plot.log`) — do not report working
  clutter as submittals. Mark the latter `Stage=Working/Ref`.
- Different disciplines can carry different review codes in one folder (e.g. FF, FA,
  SE all Code C) — one row per review doc, code per row, never merge.
- `Thumbs.db`, `.DS_Store`, `plot.log` are throwaway — include them with a
  "system file — ignore" note rather than omitting silently, so the row count matches reality.
- EN/AR pairs are duplicates of the same decision — keep both but identical status;
  cite the EN for comment detail.
