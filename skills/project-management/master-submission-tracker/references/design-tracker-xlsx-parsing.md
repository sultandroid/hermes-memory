# Parsing the CG Design Phase Deliverables Tracker xlsx

Session-derived pitfalls (2026-08-17) for `scripts/design_tracker_overdue.py` and any future parser of the CG `Design_Phase_Deliverables_Tracker_*.xlsx`.

## Sheet inventory (12-08-2026 version)

| Sheet name (exact, incl. trailing spaces) | Discipline label | Rows |
|---|---|---|
| `Design Deliverables Tracker` | dashboard | 24 |
| `Arch Deliverables` | Architecture | 319 |
| `STR Deliverables ` | Structural | 46 |
| `Mech Deliverables ` | Mechanical | 51 |
| `AV Deliverables` | AV | 46 |
| `scenography Deliverables` | Scenography | 18 |
| `BIM Model Deliverables` | BIM | 17 |
| `Electrical Deliverables` | Electrical | 96 |
| `Exhibition Lighting Deliverable` | Exhibition Lighting | 25 |
| `Low Current & ICT Deliverables ` | Low Current & ICT | 64 |
| `SHOWCASES Deliverables  ` | Showcases | 78 |

**Trailing spaces matter.** `Low Current & ICT Deliverables ` and `SHOWCASES Deliverables  ` have trailing spaces in the sheet name — `wb[sheet]` raises `KeyError` if you don't match them exactly. Copy the names verbatim from `wb.sheetnames`.

## Pitfall 1 — Corrupted sheet dimension (Electrical)

`Electrical Deliverables` reports `max_column = 16384` (XFD) — a corrupted dimension. Iterating `ws.iter_rows()` over the full range explodes output (millions of chars). **Always cap columns** (e.g. `range(1, 16)`) when reading these sheets, or read specific cells by index.

## Pitfall 2 — Status values with trailing punctuation

Status cells contain `"Submitted."` (with a period) and `"In Progress "` (trailing space). Normalize with `.strip().lower()` and include the period variant in the "done" set:
```python
DONE_STATUS = {"submitted", "submitted.", "approved", "code-a", "code-b",
               "code-c", "code-d", "final", "closed", "issued", "b", "c",
               "d", "u", "under review", "approved with comments", ...}
```
Without `"submitted."`, every submitted item is misclassified as overdue.

## Pitfall 3 — Section-header rows repeat titles

Category header rows (e.g. `Earthing, Bonding, Surge & Lightning Protection System`, `Cable Containment System`, `AC Power Layout System`) sit in the same column as drawing titles. Skip rows whose title matches known section headers, or rows where the title cell is the only populated cell in a header-looking row. Otherwise you double-count categories as deliverables.

## Pitfall 4 — Header row is not row 1

The header (with `Forecast Submission Date` / `Status`) is usually row 1, but some sheets have a title/merged block above it. Detect the header row by scanning the first ~6 rows for a cell containing `forecast` or `status` or `drawing`, then map column indices from that row.

## Pitfall 5 — Date formats are inconsistent

Forecast dates appear as real `datetime` objects, `15.08.2026` strings, `29-6-26` strings, and `%d/%m/%Y`. `_parse_date` must try `datetime`/`date` first, then multiple string formats (`%Y-%m-%d`, `%d/%m/%Y`, `%d.%m.%Y`, `%d-%m-%y`, `%d-%m-%Y`).

## Pitfall 6 — The xlsx is gitignored

`.gitignore` has `*.xlsx`, so the tracker Excel is NOT committed to the repo — only the regenerated `.md` is. The parser must locate the xlsx from external dirs (`~/.hermes/cache/documents`, `~/Desktop`, `~/Downloads`, OneDrive) and pick the newest by mtime. The repo's `01_Registers/Design_Phase_Deliverables_Tracker.xlsx` is a stale July copy — don't rely on it.

## Pitfall 7 — `regenerate_design_tracker_md.py` is incomplete

The existing `scripts/regenerate_design_tracker_md.py` only parses Arch/Mech/Str sheets. It does NOT cover Electrical, AV, ICT, Lighting, Showcases, BIM, or Scenography. The committed `design_phase_deliverables_tracker.md` was hand-built for those sections. Don't assume the regen script keeps the whole MD in sync.

## Pitfall 8 — git push conflicts with auto-generated cron files

The repo has cron jobs (register-update, risk webapp) that modify `.sync_state.json`, `06_Risk_System/webapp/src/index.html`, etc. while you work. `git push` will fail with non-fast-forward; `git pull --rebase` will fail with "unstaged changes". Stash the auto-gen files, rebase, pop, and drop the stash — your committed script is safe, only the auto-gen files conflict.
