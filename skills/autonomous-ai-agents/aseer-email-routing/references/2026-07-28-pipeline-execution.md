# Pipeline Execution — 2026-07-28

## Key Lesson
**Never report a pipeline run as "ok" without reading the output and processing the attachments.** Full workflow:

1. Run pipeline → read SQLite scan results
2. Identify emails with attachments → extract via AppleScript
3. **Read the extracted files** (understand content, not just filenames)
4. Route to OneDrive BIM subfolders (strip email ID prefix from filenames)
5. Update repo registers based on document content
6. Commit + push
7. Then report what was found and what changed

## Emails Processed (7 with attachments)

| ID | Doc Ref | Subject | Discipline | Routed To |
|----|---------|---------|------------|-----------|
| 49475 | 1M0-ZD-0100 | Mechanical Submittal Plan / Gate 1-DD | MEP | `02_Submittals/` |
| 49496 | 1M0-1G-0002 | Plumbing DD Drawings — 50% Gateway | MEP | `02_Submittals/01_DD_Gate/MEP/` |
| 49477 | 1A0-1G-0011 | Arch Viz 3D Shots — Ground Floor | Arch | `02_Submittals/01_DD_Gate/Architecture/` |
| 49478 | 1A0-1G-0010 | Arch Viz 3D Shots — First Floor | Arch | `02_Submittals/01_DD_Gate/Architecture/` |
| 49479 | 1A0-1G-0006 Rev.01 | Arch Viz Material Board — GF | Arch | `02_Submittals/01_DD_Gate/Architecture/` |
| 49480 | 1A0-1G-0004 Rev.01 | Arch Viz Material Board — LGF | Arch | `02_Submittals/01_DD_Gate/Architecture/` |
| 49481 | 1A0-1G-0003 Rev.01 | Arch Viz Material Board — Basement | Arch | `02_Submittals/01_DD_Gate/Architecture/` |

All submitted by Hesham Abdelhameed 28-Jul-2026, Rev 00 or Rev.01. Status: **U** (with CG).

## Git Quirk
Post-commit hook regenerates `06_Risk_System/webapp/src/index.html` after every commit. This conflicts with `git pull --rebase`. Fix: `git checkout index.html` before each rebase continue.
