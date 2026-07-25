# DRR (Design Discipline Register) Extraction Script

> Reference for `risk-register-management`. Working openpyxl recipe for the "Designer Risk Register (DRR)" sheet — different from the PRR sheet, with its own column layout and ID scheme.

## Where the DDR sheet lives

Inside the master C-numbered workbook. The exact sheet name varies slightly across revisions; look for any of:

- `Designer Risk Register (DRR)`
- `Design Discipline Risk Register`
- `DDR`

(For Aseer Museum C11 the exact name is `Designer Risk Register (DRR)`.)

## Column layout (DRR)

The DDR has its own column structure — do NOT assume the same indices as the PRR sheet. Verified on Aseer Museum C11 (2026-07-19):

| Col | Index | Field |
|-----|-------|-------|
| A | 0 | # (row number) |
| B | 1 | Risk ID (e.g. `PR-Q-001`, `DB-S-001`) |
| C | 2 | RBS Category (TEC / SCH / EXT / PRO / QA / COM) |
| D | 3 | Risk Event (what could happen) |
| E | 4 | Cause (root cause / trigger) |
| F | 5 | Impact (consequence) |
| G | 6 | Prob (1-5) |
| H | 7 | Impact (1-5) |
| I | 8 | PxI (score) |
| J | 9 | Severity band (Low / Medium / High / Critical) |
| K | 10 | Response Strategy (Mitigate / Accept / etc.) |
| L | 11 | Response Action (often ends with `\| Risk Score: N (BAND)`) |

The PRR sheet, by contrast, has its header at row 3 with col 1=Risk ID, col 3=Date Identified, col 4=Category — different structure, different header position.

## Header rows

The DDR sheet has **2 title rows + 1 header row = skip 3 rows**. The first title row is `ASEER MUSEUM OF ART - DESIGNER RISK REGISTER (DRR)`, the second is empty, the third is the column headers.

## Working extraction script

```python
from openpyxl import load_workbook
from pathlib import Path
import json
from collections import Counter

FILE = "/path/to/Aseer_Museum_Risk_Register_C<rev>_<date>.xlsx"
wb = load_workbook(FILE, read_only=True, data_only=True)
ws = wb["Designer Risk Register (DRR)"]

risks = []
for i, row in enumerate(ws.iter_rows(values_only=True), 1):
    if i <= 3: continue  # skip 2 title rows + header
    if not row or all(v is None for v in row): continue
    if not row[1] or row[1] == "Risk ID" or not isinstance(row[1], str):
        continue
    risks.append({
        "id": row[1],
        "category": row[2],
        "title": row[3],
        "cause": row[4],
        "consequence": row[5],
        "probability": row[6],
        "impact": row[7],
        "score": row[8],
        "rating": row[9],
        "response_strategy": row[10],
        "response_action": row[11] if len(row) > 11 else None,
    })

cat_counts = Counter(r["category"] for r in risks)
sev_counts = Counter(r["rating"] for r in risks)

out = {
    "project": "Aseer Regional Museum",
    "contract": "0010003521",
    "register": "Designer Risk Register (DDR/DRR)",
    "source": f"Aseer_Museum_Risk_Register_C<rev>_<date>.xlsx (Designer Risk Register (DRR) sheet)",
    "revision": "C<rev>",
    "register_date": "<YYYY-MM-DD>",
    "scoring": {"probability": "1-5", "impact": "1-5", "matrix": "PxI"},
    "rbs_categories": {
        "TEC": "Technical (design)",
        "SCH": "Schedule",
        "EXT": "External (stakeholder/authority)",
        "PRO": "Procurement",
        "QA": "Quality",
        "COM": "Commercial"
    },
    "category_counts": dict(cat_counts),
    "severity_counts": dict(sev_counts),
    "total": len(risks),
    "last_updated": "YYYY-MM-DD",
    "risks": risks
}

out_path = "06_Risk_System/generated/drr_risks.json"
Path(out_path).parent.mkdir(parents=True, exist_ok=True)
Path(out_path).write_text(json.dumps(out, indent=2, ensure_ascii=False))
print(f"Wrote {out_path}: {len(risks)} risks")
```

## Companion CSV (for Excel pivot)

```python
import csv
with open("06_Risk_System/generated/drr_register_C<rev>.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["#", "Risk ID", "Category", "Rating", "Score", "P", "I",
                "Title", "Cause", "Consequence", "Response Strategy", "Response Action"])
    for i, r in enumerate(risks, 1):
        w.writerow([i, r["id"], r["category"], r["rating"], r["score"],
                    r["probability"], r["impact"], r["title"], r["cause"],
                    r["consequence"], r["response_strategy"], r["response_action"]])
```

## Common errors

- **BadZipFile** — OneDrive stub. See `references/onedrive-locked-excel-recovery.md`.
- **KeyError on sheet name** — verify the exact sheet name with `wb.sheetnames` first; it's been spelled `DDR`, `Design Discipline Risk Register`, `Designer Risk Register (DRR)` across different revisions.
- **Header-row offset** — DDR has 2 title rows; PRR has 2. The `i <= 3: continue` skip is specific to DDR. For PRR, the header is also at row 3 but the column mapping is different.
- **IndexError on row[11]** — older DRR sheets may not have a response_action column. Guard with `if len(row) > 11`.
