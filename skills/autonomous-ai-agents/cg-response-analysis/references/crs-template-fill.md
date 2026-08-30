# CRS Template Structure & Programmatic Fill (openpyxl)

Reverse-engineered from `Technical_Office/Compliance_System/templates/CRS_TEMPLATE_BLANK.xlsx` (sheet `CRS`). Use this to build a Comment Resolution Sheet for any Code C submittal without hand-typing rows.

## Template layout (verified 2026-08-29)

**CRITICAL — labels vs values are in DIFFERENT cells.** The template has a label column (A/I) and a value column (D/K). Writing a value into a label cell (A5/A6/A7/I5/I6/I7) overwrites the label and leaves the value cell empty — this is the #1 header bug. Fill the VALUE cells only:

| Cell | Field | Example |
|---|---|---|
| D4 | PROJECT NAME (value) | `Project to rehabilitate and equip museum displays for the third regional museum (Aseer)` |
| D5 | CRS NUMBER (value) | `CRS-1A0-1G-0012-01` |
| H5 | Rev. (value) | `01` |
| K5 | DATE (value) | `29-Aug-2026` |
| D6 | DOCUMENT No. (value) | `MOC-MUS-ASE-1A0-1G-0012` |
| H6 | Rev. (value) | `00` |
| K6 | DISCIPLINE (value) | `Architectural` |
| D7 | DOCUMENT TITLE (value) | full title |
| K7 | DOCUMENT TYPE (value) | `Specifications (Master Format)` |

The LABELS (`PROJECT NAME`, `CRS NUMBER`, `DATE`, `DOCUMENT No.`, `DISCIPLINE`, `DOCUMENT TITLE`, `DOCUMENT TYPE`, `Rev.`) already live in A4/A5/I5/A6/I6/A7/I7/G5/G6 — do NOT touch them. Merged ranges: `D4:H4`, `D5:F5`, `K5:R5`, `D6:F6`, `K6:R6`, `D7:H7`, `K7:R7` (write to the top-left anchor of each).

**Header merge pitfall — `C10:D10`.** The "Sheet" header is merged across C10:D10, which leaves column D empty and looks broken. Unmerge it and set `C10 = 'Sheet'`, `D10 = None`:
```python
ws.unmerge_cells('C10:D10')
ws['C10'] = 'Sheet'
ws['D10'] = None
```

**CRITICAL — do NOT incrementally patch a corrupted header; rebuild from a clean template.** When the header/merges get into a broken state (empty column D, labels overwritten, data shifted), the incremental fixes (unmerge one range, `delete_cols`, shift headers) compound the damage: `delete_cols(4,1)` shifts the data columns so the reply/reply_by values land in the wrong cells and get lost. The reliable recovery is:
1. Load the **clean template** fresh (`CRS_TEMPLATE_BLANK.xlsx`).
2. `ws.unmerge_cells(str(mc))` for **every** merged range first (clean slate).
3. Re-write labels + values to the correct anchor cells, re-merge, then fill data rows.
Do not try to surgically repair a file you already mangled — start over from the template.

**MergedCell read-only error.** Writing to a non-anchor cell of a merged range raises `AttributeError: 'MergedCell' object attribute 'value' is read-only`. Two fixes: (a) write to the top-left anchor cell only, or (b) `unmerge_cells` the range first, then write. When you need to move a header, unmerge everything, clear the row, then re-merge at the new positions.

Data rows start at **row 11**. Column map:
- A = No. (e.g. `G1`, `S1`)
- B = Initial (e.g. `CG`)
- C = Sheet — **this is the CG's original page number**, not a generic 1/2. Map each comment to the page in the CG's response PDF where it appears (e.g. G1–G10 → 1, S1 → 3, S2 → 4 … S21 → 23 for a one-section-per-page PDF). Traceability to the reviewer's own document is the point.
- E = Reviewer Comment (verbatim CG text) — merged E:I
- J = Originator Reply (our response) — merged J:O
- P = Reply By (owner)
- Q = Reply Status by Reviewer (`Closed` / `Open`) — merged Q:R

Merged ranges per data row: `E:I`, `J:O`, `Q:R`. Set `wrap_text` + `vertical=top` on comment/reply cells, `center` on No/Initial/Sheet/Status.

## Fill pattern (openpyxl)

```python
import openpyxl
from openpyxl.styles import Alignment, Border, Side

wb = openpyxl.load_workbook('Technical_Office/Compliance_System/templates/CRS_TEMPLATE_BLANK.xlsx')
ws = wb['CRS']

# header fills (see table above)
ws['D4'] = '...'; ws['A5'] = '...'; ws['G5'] = '01'; ws['I5'] = '...'
ws['A6'] = '...'; ws['G6'] = '00'; ws['I6'] = '...'
ws['A7'] = '...'; ws['I7'] = '...'

thin = Side(style='thin', color='000000')
border = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical='top', horizontal='left')
center = Alignment(wrap_text=True, vertical='center', horizontal='center')

start_row = 11
for i, (no, initial, sheet, comment, reply, reply_by, status) in enumerate(comments):
    r = start_row + i
    ws.cell(r, 1, no).alignment = center
    ws.cell(r, 2, initial).alignment = center
    ws.cell(r, 3, sheet).alignment = center
    ws.cell(r, 5, comment).alignment = wrap
    ws.cell(r, 10, reply).alignment = wrap
    ws.cell(r, 16, reply_by).alignment = wrap
    ws.cell(r, 17, status).alignment = center
    for c in (1, 2, 3, 5, 10, 16, 17):
        ws.cell(r, c).border = border
    ws.merge_cells(start_row=r, start_column=5, end_row=r, end_column=9)
    ws.merge_cells(start_row=r, start_column=10, end_row=r, end_column=15)
    ws.merge_cells(start_row=r, start_column=17, end_row=r, end_column=18)
    # DO NOT hardcode height=60 — see "Formatting" below; auto-calc instead.

wb.save('02_CG_Responses/CRS_<DOC>_Rev01.xlsx')
```

## Formatting (MANDATORY — the user rejects the default fill as "format not good")

The template's default column widths are too narrow for real reply text, and a fixed row height truncates long replies. The user will bounce the file back with "format not good" if you skip this. Apply ALL of these before saving:

1. **Widen the text columns.** Comment spans E:I, reply spans J:O. Set each of E,F,G,H,I,J,K,L,M,N,O to width 18 (≈90 chars comment, ≈108 chars reply). Set P (Reply By) to 22, Q and R (Status) to 12.
2. **Auto-calculate row height** from wrapped line count — never a fixed 60px. Estimate lines by word-wrapping against the column char width, then `height = max(20, lines * 14 + 6)`:
   ```python
   def est_lines(text, width_chars):
       if not text: return 1
       lines, cur = 1, 0
       for w in text.split():
           if cur + len(w) + 1 > width_chars:
               lines += 1; cur = len(w)
           else:
               cur += len(w) + 1
       return lines
   # per row: max(est_lines(comment, 90), est_lines(reply, 108))
   ```
3. **Font size 11** (Calibri). The default renders ~8pt and is unreadable.
4. **Color-code the status cell** (Q): green fill `C6EFCE` + dark-green bold font `006100` for `Closed`; red fill `FFC7CE` + dark-red bold font `9C0006` for `Open`. Plain text, no emoji.

## User's final formatting (manual edits — match these, 2026-08-29)

The user manually re-tuned the file after the agent build. Future CRS builds should apply these directly instead of the defaults above:

| Element | User's final value (override the defaults) |
|---|---|
| Status fill — Closed | `E7F3E8` (softer green, not `C6EFCE`) |
| Status font — Closed | `3F6B46` (muted green, not `006100`) |
| Status fill — Open | `FCE8E6` (softer red, not `FFC7CE`) |
| Status font — Open | `9C3D36` (muted red, not `9C0006`) |
| Originator Reply cell (I) | **Bold** (the reply text is bold; comment cell D stays regular) |
| Header labels (A4/A5/A6/A7/I4/I5/I6/I7/A10/B10/C10/P10) | Arial 11 bold |
| Header label fill | `CC9900` (gold/orange) on label cells only (A4, A8, etc.) — value cells (D4, K5…) have no fill |
| Body font | Calibri 10 (unchanged) |
| Row heights | Manually tuned per row (32 / 45 / 58 / 71) rather than uniform auto-calc — the user prefers tighter rows for short replies |

The user's status colors are the **Google-Sheets-style muted palette** (`E7F3E8`/`3F6B46` green, `FCE8E6`/`9C3D36` red), not the brighter Excel palette. Use these muted tones.

## Render-verify before delivering (soffice → pdftoppm → vision)

The user opens the file in Excel and judges it visually. Verify the layout yourself first:

```bash
soffice --headless --convert-to pdf --outdir /tmp <file>.xlsx
pdftoppm -png -r 100 -f 1 -l 2 /tmp/<file>.pdf /tmp/crs_page
# then vision_analyze /tmp/crs_page-1.png asking: text cut off? columns wide enough? rows tall enough?
```

Note: the vision model's OCR will misread header values (dates, project names) at low render resolution — trust the openpyxl cell values (`ws['D4'].value` etc.), not the OCR text, for content correctness. Use vision only for *layout* (truncation, column width, row height, color), not for content accuracy.

## Staged-evidence argument (key for spec-stage Code C)

When CG returns a **specifications** submittal Code C demanding test reports / certificates / warranties / mock-ups, the correct technical reply is that these are **Material Approval (MAR) / pre-installation stage deliverables**, not spec-stage deliverables. The specification's job is to *state the required criteria* (NRC, DCOF, fire class, compressive strength, VOC limits); the evidence is submitted later by approved suppliers.

Reply pattern:
1. **Embed the criteria** into each spec section (so they become contractually binding).
2. **Commit to the evidence** at the correct later stage per the Submission Plan / ITP.
3. Request CG agreement to this staged delivery (avoids front-loading MAR work into DD).

This is the same argument used in the Showcases CRS (`1G-0009_Showcases_CRS_Rev01.md`) — "COMPLIED AT 50% DD LEVEL … full detail to follow in shop drawings / IFC package."

## CRS ownership & signatures — one CRS per discipline, no cross-signing

Each discipline has its **own** DD package, its **own** CG reviewer, and its **own** CRS. Do NOT cross-sign or fold another discipline's specialist into a CRS that isn't theirs.

| Discipline | DD package folder | CG reviewer | CRS signatories |
|---|---|---|---|
| Architectural | `Arch DD Package 29-6-26` | Maged Zamzam | Prepared=TO, Reviewed=NRS, Approved=PM |
| Structural | `3.2_DD Doucments Structure` | Abdrabo Shahin | its own CRS (1C0-1G-0001) |
| MEP / Mech / Elec / Lighting | `3.3` / `3.4` / `3.5` | their own | their own |

**Rule:** an Architectural CRS is signed by the Technical Office + NRS + PM only. The sustainability specialist (Fida) and structural engineer do NOT sign the architectural CRS — they have their own packages. If CG insists a specialist "reviewed" the spec (G3-type), add a "Reviewed by Sustainability: M. Fida Noon" line as a *reviewer*, not a *signatory* — never make them the owner of the architectural spec.

**The rebuttal for "specialists must review the architectural spec" (G1/G2/G3):** the lead designer (NRS) *sets* the performance requirements; specialists *deliver against* them — not the reverse. Cite ZD-0026 (Code B) Comment 2 (NRS owns architectural design, Samaya TO is central coordinator incl. acoustics) + Comment 3 (review chain Supplier/TO → Samaya → NRS → CG, no specialist in the chain). G1 ("specialized team") = internal review → COMPLIED; G2 ("acoustics specialist") = NOT APPLICABLE (contradicts ZD-0026); G3 ("sustainability specialist") = COMPLIED (Fida reviewed the Low-VOC/Mostadam sections).

## Status convention

- `Closed` = responded, no further action.
- `Open` = deliberately left open because we are asking CG for clarification (e.g. "confirm the specific design requirements the display case specs must satisfy"). Do NOT mark a vague CG comment "Closed" — flag it Open and ask CG to specify.

## Audit-first: classify CG comments, don't blindly "COMPLIED" everything

The user's core correction this session: **do not mark every CG comment "COMPLIED/Closed".** Before filling the CRS, audit each comment against the governing docs and classify it. The correct reply vocabulary is:

| Verdict | When | Reply wording |
|---|---|---|
| **FULLY EXISTS** | The demand is already written in the spec | Cite the exact clause (e.g. "Sec 2.01") — "already specified, no revision required" |
| **MOSTLY EXISTS** | Most of it is there, 1–2 items missing | Cite what exists + name the missing item and where to add it |
| **NOT APPLICABLE AT SPEC STAGE** | Evidence (test reports/certs/mock-ups) is a later-stage deliverable | Cite SoW §6.11 / §13.12 |
| **NOT APPLICABLE** | Contradicts an approved doc (e.g. ZD-0026 roles) | Cite the contradicting approved doc |
| **NOTED** | Boilerplate statement of principle (G5/G7-type) | "statement of principle, no revision required" |
| **OPEN** | Downstream of an unresolved design (e.g. showcase Code C) | Link to the blocking submittal |

**The decisive technique — diff CG demands against the actual spec text.** Extract each spec `.docx` to text, then grep each CG-requested value/term against it. This session it revealed CG's Code C was ~90% already-written (only 11 genuinely-missing items across 21 sections). The CRS reply then cites the clause number for every "exists" item instead of re-writing. This is far stronger than a generic "COMPLIED" and directly supports the push-back.

**Governing docs to cite (Aseer):**
- **ER §2.4** — PMC review is conformance-only, not technical review; design liability stays with Contractor. This is the master clause for pushing back on CG overreach.
- **SoW §6.11–6.17** — product data/certs/test reports are IFC-package submittals, "shall not be submitted independently" → wrong-stage for spec.
- **SoW §13.12 + ER §2.4.F** — mock-ups per Mockups Schedule, construction phase → wrong-stage for spec.
- **ZD-0026 (NRS Methodology, Code B)** — Comment 2: NRS owns architectural design, Samaya TO is central coordinator (acoustics included); Comment 3: review chain Supplier/TO → Samaya → NRS → CG (no specialist in the chain). Use this to rebut "specialist must review the architectural spec" — the lead designer sets requirements, specialists deliver against them, not the reverse.

**Oddy test scope (recurring correction):** Oddy is a conservation test for materials **inside/near display voids** (in contact with artifacts), NOT all materials. CG's own wording ("materials used inside display voids") is correctly scoped. ER §6.11 ("non-deleterious to museum-grade objects") is the governing principle; SoW §8.1 ("all materials") is overly broad and must be read in context.
