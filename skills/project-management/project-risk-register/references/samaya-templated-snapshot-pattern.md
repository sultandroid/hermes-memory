# Samaya-Templated Risk Register Snapshot — Build Pattern

This file describes the A4-portrait, Samaya-styled xlsx **snapshot** variant of
the risk register. It is the **downloadable Excel version** of a register page on
the live webapp — same data, Samaya branding, governance-grade formatting.

When the user asks for a snapshot, an Excel export, a register "with cover and
header", or a register that "matches the Samaya style", use this pattern.

## When to Use This Variant

- The user wants a **client-facing** / **governance** xlsx (not an internal
  working register) — used to send to CG, PMC, the client, or to print for
  review meetings
- The data has multiple **per-register sources** (PRR, DDR, HSE, AV) and
  the snapshot should be **scoped to one register** with its own scoring scale
- The user wants **versioned snapshots** (e.g. `EXP-RISK-PRR-2026-006_RevC11_ACTIVE.xlsx`)
  for a project archive / audit trail
- A live **webapp** for the same register exists and the user wants the
  download button to produce a styled xlsx, not a raw export

## When NOT to Use

- The register is purely internal and the user just wants a working Excel
  (use the **Full** or **Phase** variant)
- The user needs a **formula-driven interactive** register where editing
  one cell cascades to others (use the **Formula-Driven** variant)
- The user needs a **subcontractor-specific** register (use **Subcontractor**)
- The user just wants to see risks in conversation (use a markdown table)

## Workbook Structure (3 sheets, in this order)

### 1. Dashboard

Layout (rows reserved for cover, then matrix, then tables, then charts):

- **Rows 1-3** — Cover block (A:G merged, navy):
  - A1: register name (e.g. `ASEER REGIONAL MUSEUM  —  Master Risk Register (PRR)`)
  - A2: `Doc No. EXP-RISK-<REG>-<YYYY>   ·   Contract: 0010003521   ·   Rev C11   ·   ACTIVE`
  - A3: `Snapshot No. NNN   ·   Date: YYYY-MM-DD   ·   Time: HH:MM (Asia/Riyadh)   ·   Source: <URL>`
- **Rows 5-6** — 6-card KPI strip (B:G, one card per column, single-cell width):
  - B5: TOTAL, C5: CRITICAL, D5: HIGH, E5: MEDIUM, F5: LOW, G5: OPEN
  - Each card: 18pt bold white text on band color (Navy / Critical / High / Medium / Low / Dark Gray)
  - Row 6: label in same fill, 9pt bold white
- **Row 8** — QR code (top-left, A8, 110px square) + Samaya logo (top-right, G8, 28px tall)
- **Row 9** — caption under QR: `Scan to open live register → <URL>` in 8pt italic muted gray
- **Rows 11+** — Risk matrix heatmap:
  - Row 11: section title "RISK MATRIX" (B:J merged)
  - Row 12: header row `P ↓ / S →` navy cell, then `S1 | S2 | S3 | S4` (or `S1..S5` for DDR)
  - Rows 13-16 (PRR, P=4→1) or 13-17 (DDR, P=5→1): each row labelled `Pn`, then 4 or 5 cells
  - Each cell: count of risks at that (P,S), color-coded by band (Critical/High/Medium/Low)
  - **Always use the P×I score to determine the band**, not the P or S alone:
    - 4×4 PRR: Critical ≥12, High 8-11, Medium 4-7, Low ≤3
    - 5×5 DDR: Critical ≥16, High 10-15, Medium 5-9, Low ≤4
- **Rows after matrix** — "BY RATING" table (band, count) with tinted fills
- **Rows below** — "BY STATUS" table, "EXPOSURE BY CATEGORY" table, "TOP OWNERS" table
- **Charts** — Doughnut (severity split) and Bar (category exposure) placed beside/below the tables

### 2. Risk Register

12 columns: `ID | Cat | Rating | Score | Status | Owner | Target | Risk Event | Cause | Consequence | Response | Evidence`

- Header row 11, navy fill, white bold 9.5pt, wrap_text=True
- Data rows 12+, sorted by rating (Critical→Low) then score desc
- Rating column: color-coded (Critical deep red, High dark orange, Medium amber, Low green), white bold text
- Freeze pane at A12, auto-filter on A11:L<last>
- Repeat header row on every print page (`ws.print_title_rows = "11:11"`)
- A4 portrait, fitToWidth=1, margins 2cm/1.5cm

### 3. Action Plan

7 columns: `Risk ID | Cat | Rating | Action | Owner | Due | Status`

- Header row 11, same styling as Register
- One row per open action across all risks
- Rating column color-coded
- Auto-filter on header row
- "No discrete actions recorded" placeholder row if `len(actions) == 0`

## Page Header (every sheet)

Samaya Chart Framework §2 page header layout (left/center/right):

```python
ws.oddHeader.left.text   = "Samaya Investment · Technical Office"
ws.oddHeader.left.size   = 8
ws.oddHeader.left.color   = "64748B"  # GRAY_MUTED
ws.oddHeader.center.text = f"Snapshot No. {snapshot_no}"
ws.oddHeader.right.text  = f"{doc_no}  ·  Rev {revision}  ·  {status}  ·  {register}  ·  {page_url}"
# (size=8, color=GRAY_MUTED on all)
```

## Page Footer (every sheet)

```python
ws.oddFooter.left.text   = "RESTRICTED · Project use only"
ws.oddFooter.center.text = f"Generated {now.strftime('%Y-%m-%d %H:%M')}"
ws.oddFooter.right.text  = "Page &P of &N"   # Excel's auto page numbering
```

## Samaya Palette (apply across all sheets)

| Token | Hex | Use |
|-------|-----|-----|
| NAVY | `1E293B` | Headers, H1, table header fill |
| RED | `B01E2F` | Accent borders, logo (external) |
| GRAY_ALT | `F1F5F9` | Alternating row fill (every other row) |
| GRAY_BORDER | `CBD5E1` | Table borders |
| GRAY_MUTED | `64748B` | Header/footer text, secondary text |
| DARK_GRAY | `334155` | Secondary headings |
| WHITE | `FFFFFF` | Text on colored fills |

| Band | Fill | Use |
|------|------|-----|
| Critical | `B91C1C` | Heatmap, KPI card fill, Rating cell |
| High | `C2410C` | same |
| Medium | `B45309` | same |
| Low | `15803D` | same |
| Open count | `334155` (DARK_GRAY) | KPI card fill for OPEN count |

## Typography

- **Calibri** everywhere (Windows + macOS + LibreOffice compatible)
- Cover A1: 18pt bold NAVY
- Cover A2: 10pt bold NAVY
- Cover A3: 9pt GRAY_MUTED
- KPI value (row 5): 18pt bold WHITE on band color
- KPI label (row 6): 9pt bold WHITE
- Table header: 9.5pt bold WHITE on NAVY
- Table data: 9pt DARK_GRAY (NAVY for ID/Score cells)
- All cells `wrap_text=True` for evidence/cause/consequence text
- All cells `vertical='top'`

## Cover Block — Required Fields (Samaya Chart Framework §2)

| Field | Format | Example |
|-------|--------|---------|
| Title | `ASEER REGIONAL MUSEUM  —  <Register Name>` | `... — Master Risk Register (PRR)` |
| Doc Strip | `Doc No. <EXP-RISK-...-YYYY>   ·   Contract: <N>   ·   Rev <NN>   ·   <STATUS>` | `...   ·   Rev C11   ·   ACTIVE` |
| Snapshot Meta | `Snapshot No. <NNN>   ·   Date: YYYY-MM-DD   ·   Time: HH:MM (Asia/Riyadh)   ·   Source: <URL>` | `Snapshot No. 006   ·   Date: 2026-07-24   ·   Time: 22:50 (Asia/Riyadh)   ·   Source: https://...` |
| QR Caption | `Scan to open live register → <URL>` (8pt italic muted gray) | — |

## Snapshot Numbering Convention (per Samaya Chart Framework §1.4)

`EXP-RISK-<REG>-<YYYY>-<NNN>_Rev<rev>_<status>.xlsx`

Examples:
- `EXP-RISK-PRR-2026-006_RevC11_ACTIVE.xlsx`
- `EXP-RISK-DDR-2026-004_RevC11_ACTIVE.xlsx`

`NNN` auto-increments per register, tracked in a small JSON file:

```json
{
  "PRR": {"last_snapshot": 6, "doc_no": "EXP-RISK-PRR-2026", "status": "ACTIVE"},
  "DDR": {"last_snapshot": 4, "doc_no": "EXP-RISK-DDR-2026", "status": "ACTIVE"}
}
```

Status codes (per Chart Framework §1.4): `DRAFT | IFR | IFA | IFC | APPROVED | ACTIVE | SUPERSEDED`. Default for snapshots that match the live register is `ACTIVE`.

## QR Code Generation

Use `segno` (or `qrcode`):

```python
import segno
qr = segno.make(url, error="m")  # error correction 'm' = ~15% redundancy
tmp = Path("/tmp/_snapshot_qr.png")
qr.save(str(tmp), scale=4, border=1)
img = XLImage(str(tmp))
img.width = 110
img.height = 110
ws.add_image(img, "A8")
```

Place at `A8` on every sheet's cover. The image is **always** the live page URL
of that register (e.g. `https://samaya-factory.com/aseer/registers/Risk/` for PRR
or `.../Risk/DDR/` for DDR).

If `segno` is missing: `pip3 install segno` or fall back to a `data:image/gif`
placeholder (the build continues, but the cover has no QR — log a warning).

## Samaya Logo

Source: `https://samaya-factory.com/assets/logos/samaya-logo-trans.png` (always
public, no auth) or the local copy at `<repo>/_Style-Guides/logos archives/samaya-logo.png`.

```python
LOGO_PATH = repo / "_Style-Guides" / "logos archives" / "samaya-logo.png"
img = XLImage(str(LOGO_PATH))
img.height = 28
img.width = int(28 * (img.width / img.height))
ws.add_image(img, "G8")
```

Place at `G8` (top-right of cover). If the file is missing, skip silently — the
cover still has QR + KPI strip, just no logo.

## Build Pipeline

```python
# build_snapshots.py
def main():
    today, now_time = now_ksa()  # Asia/Riyadh
    # 1. Load PRR + DDR JSON
    prr = json.loads(PRR_JSON.read_text())
    ddr = json.loads(DDR_JSON.read_text())
    # 2. Build PRR snapshot
    build(prr, str(PRR_XLSX),
          page_url="https://samaya-factory.com/aseer/registers/Risk/",
          register="Master Risk Register (PRR)",
          doc_no="EXP-RISK-PRR-2026",
          doc_ref="ASR-SAM-RMP-001",
          revision="C11", status="ACTIVE", total=len(prr["risks"]), scale=4)
    # 3. Build DDR snapshot (scale=5 for P×I 1-5)
    ddr_data = normalise_ddr(ddr)
    build(ddr_data, str(DDR_XLSX),
          page_url="https://samaya-factory.com/aseer/registers/Risk/DDR/",
          register="Design Discipline Register (DDR)",
          doc_no="EXP-RISK-DDR-2026",
          doc_ref="ASR-SAM-DDR-001",
          revision="C11", status="ACTIVE", total=len(ddr["risks"]), scale=5)
    # 4. Rename to versioned file name
    prr_n = next_snapshot_no("PRR") - 1
    prr_named = PRR_XLSX.parent / f"EXP-RISK-PRR-2026-{prr_n:03d}_RevC11_ACTIVE.xlsx"
    PRR_XLSX.rename(prr_named)
    # similar for DDR
```

The `build()` function lives in `build_xlsx.py` and is **shared** across all
register pages. It takes `data, out_path, **kwargs` and returns the saved
path. Per-page configuration goes in kwargs (`page_url`, `register`, `doc_no`,
`doc_ref`, `revision`, `status`, `total`, `scale`).

## Deploy Order (deploy.sh)

```bash
cd 06_Risk_System/webapp
python3 build_snapshots.py   # writes per-register xlsx FIRST
python3 build_risk.py         # discovers latest PRR xlsx via glob, embeds in HTML
python3 build_ddr.py          # discovers latest DDR xlsx via glob, embeds in HTML
rsync -avz --delete \
  -e "ssh -p 65002 -o StrictHostKeyChecking=no" \
  ./src/ u517606786@samaya-factory.com:/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/Risk/
```

**Why snapshots first:** `build_risk.py` and `build_ddr.py` use
`glob.glob("src/EXP-RISK-*-2026-NNN_Rev<rev>_<status>.xlsx")` to find the
latest snapshot and embed its name in the HTML's Excel button. If snapshots
run *after* the HTML, the glob finds nothing and the HTML points at a stale
fallback name (404 on the server).

## Common Mistakes (this variant specifically)

### 🔴 `Workbook()` default sheet auto-renames second `create_sheet("Dashboard")`

The default `Workbook()` creates an empty sheet. Renaming it to "Dashboard"
and then calling `wb.create_sheet("Dashboard")` creates a **second** sheet
that openpyxl auto-renames to "Dashboard1". The HTML button then points at
**Dashboard1** (not the visible "Dashboard" tab).

**Fix:** pass the default sheet explicitly:
```python
dash = wb.active
dash.title = "Dashboard"
build_dashboard_sheet(wb, data, ..., ws=dash)  # not create_sheet inside
```

### 🔴 KPI strip with 2-col merged cards

`ws.merge_cells("A5:B5")` then `ws["B5"]` is a `MergedCell` (read-only).
Iterating `B5, C5, D5...` to write the next card fails.

**Fix:** use single-column cards (one KPI per column, no merging):
```python
for i, (label, val, fill) in enumerate(kpis):
    col = get_column_letter(i + 2)  # B..G
    ws[f"{col}5"].value = val
    ws[f"{col}5"].fill = PatternFill("solid", fgColor=fill)
    # ... rest of styling
```

### 🔴 Hard-coded snapshot number in build_risk.py

`xlsx_name = "EXP-RISK-PRR-2026-006..."` breaks on next deploy when NNN
advances to 007. Use a glob:

```python
import glob
candidates = sorted(HERE.glob("src/EXP-RISK-PRR-2026-*_ACTIVE.xlsx"))
xlsx_name = candidates[-1].name if candidates else "fallback.xlsx"
```

### 🔴 Glob path with `HERE.parent` instead of `HERE`

`build_risk.py` is at `06_Risk_System/webapp/build_risk.py`. `HERE` is
`06_Risk_System/webapp/`. The snapshot is at
`06_Risk_System/webapp/src/...`. Glob from `HERE.glob("src/...")`, NOT from
`HERE.parent.glob("src/...")`.

### 🔴 `Workbook()` sheets list ordering

After build, `wb.sheetnames` must be `['Dashboard', 'Risk Register', 'Action Plan']`
in that order — `Risk Register` comes first in many Excel "open file" dialogs
and is the expected landing page for a project register. If you
`create_sheet("Dashboard")` first then `create_sheet("Risk Register")` then
`create_sheet("Action Plan")`, you get a stray empty sheet at the start.

**Fix:** use the default active sheet as Dashboard, then `create_sheet` the
other two, then `wb.active = 0` to make Dashboard the default.

### 🔴 Scoring scale mismatch between registers

PRR uses P×S 1-4 (max 16), DDR uses P×I 1-5 (max 25). If you build DDR with
`scale=4`, the matrix is too small for P=5 / I=5 risks — those cells stay
empty (visually correct) but the band calculation breaks (max P×I 5×5=25
is Critical ≥16, not 12). Always pass `scale=5` for DDR.

## Reference implementation

See `06_Risk_System/webapp/build_xlsx.py` in `sultandroid/aseer-museum-pm` for
the full implementation (~750 lines, well-commented). The functions are:

- `_apply_page_setup(ws)` — A4 portrait, margins, fitToWidth
- `_border(thin, color)` — standard thin border
- `_font(size, bold, italic, color, name)` — Samaya font helper
- `_counts_by_rating/satus/category/owner(risks)` — tally helpers
- `_load_logo(ws, anchor)` — embed Samaya logo
- `_load_qr(ws, anchor, url, size_px)` — embed QR code
- `_set_header_footer(ws, **kwargs)` — page header/footer
- `_cover_block_with_open(ws, **kwargs)` — cover rows 1-9
- `_dashboard_sheet(wb, data, **kwargs)` — Dashboard sheet
- `_register_sheet(wb, data, **kwargs)` — Risk Register sheet
- `_action_plan_sheet(wb, data, **kwargs)` — Action Plan sheet
- `_footer(ws, at_row, last_col, ...)` — sheet footer
- `build(data, out_path, **kwargs)` — public entry point

See also `06_Risk_System/webapp/build_snapshots.py` for the
counter-and-rename flow, and `06_Risk_System/webapp/deploy.sh` for the
end-to-end deploy.

For OneDrive and Hostinger pitfalls specific to this workflow (e.g. the
"Resource deadlock" loop on `cp`, the lowercase-`ddr` 404 cache, the OneDrive
0-byte stub that returns the SHA of empty), see
`macos-onedrive-recovery` skill and its `references/stale-stub-vs-realdeadlk.md`.
