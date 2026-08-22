# Aseer RFI.xlsx — Workshop No. 1 Register Structure

The master RFI register at
`OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/04_Docs/04_RFIs/RFI.xlsx`
is a single-sheet (Sheet1) register titled "RFI sheet - Aseer Regional Museum Workshop No. 1".
It is NOT a classic submittal register — it is a **discipline-blocked coordination log** used for
point-by-point discussion of fabrication/interface inquiries (Showcase contractor / Glasbau Hahn,
AV, lighting, graphics, etc.).

## File facts
- Single sheet `Sheet1`, header at **row 4** (row 1 = title, row 3 = column headers).
- ~565 rows in file, **~524 real data rows** after trimming trailing empties.
- **32 MB** on disk — large due to embedded photos in the "Photo if available" column. This
  exceeds the 20 MB Telegram attachment limit — pull it from the path, never ask the user to upload.
- `RFI_Samaya_Coordination.xlsx` and `00_Registers/A2742-10.05-004 RFI Traker.docx` are the
  companion coordination log / tracker but often locked by OneDrive (`Resource deadlock avoided`).

## Column layout (11 cols)
| Col | Header | Notes |
|-----|--------|-------|
| A | Subject | block header — repeated on first row of each block |
| B | No. | block-local numbering, RESTARTS at 1 per block |
| C | Question | the RFI body |
| D | Photo if available | images (source of the 32 MB size) |
| E | SAMAYA Response | essentially never filled |
| F | CG Response | filled for a handful |
| G | PMC Response | the actively-populated column |
| H | Answer | rarely filled |

Response-status counts (2026-08): PMC filled on ~47 rows, CG on ~1, SAMAYA on ~0, Answer on ~1.
PMC answers are terse/repetitive boilerplate:
- "Impact on showcase dimensions and specifications prior to fabrication." (~35x)
- "Subject to advice and confirmation."
- "Content to be provided by the End User."
- "Subject to project Specs." / "Valid"

## Block structure (subject → count)
The sheet is grouped into **discipline blocks**, each re-numbering from No. 1:
URGENT Object List (7), A/V Design (5), Show cases (4), Art Commission (2), Object List (2),
Tactile & Manual Interactives (7), Graphic (2), Structural Design Inquiries (1),
ICT/Security Design Inquiries (1), Lightbox Coordination (2), Lighting Decision (2),
Interior Design Decision (6), Showcase (6). Plus ~480 unlabeled rows under the Object-List style
queries (per-object dimension/weight data requests across galleries G3/G8/G11/G12).

Each block is demarcated by the Subject cell being re-set; rows after it inherit via `None`
until the next Subject cell. `Showcase` blocks exist with **empty Question cells** (rows 124–160)
— a staging area that was left blank.

## Adding a NEW RFI (e.g. "Coordination - Mounts & Art Handling")
The user may supply a coordination/interface RFI (MoC-appointed Mount Contractor & Art Handlers,
sequence of display-cases/mounts/installation, rigging scope per SOW Sec 2.2 + Interface
Responsibility Matrix + Sec 13.31). This is NOT a design decision — it is pure interface/coordination.
**Best placement: a NEW block** `Coordination - Mounts & Art Handling`, No. 1 — same single-decision
block style as `Structural Design Inquiries` / `ICT/Security`. Do NOT bury it inside "Showcase"
(its topic is interface, not showcase design).
Before writing, confirm with the user: RFI number/code (Aconex/GBH ref), date, sender. Optionally
add a Remarks column to hold the SOW section references.

## Reading pattern
Extract with openpyxl on system Python 3.13 (`terminal python3 -c ...`), `data_only=True`.
Group by consecutive Subject runs to reconstruct blocks; `Counter` over Subject values gives the
discipline mix; count non-empty per response column for status health.
