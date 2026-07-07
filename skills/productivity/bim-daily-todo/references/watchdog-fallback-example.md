# Watchdog-Only Fallback — Worked Example (June 1, 2026)

## Context

This session documented the first complete end-to-end run of the watchdog-only fallback when **all** OneDrive CSV/xlsx registers were dataless stubs (not synced locally). The cron job generated a valid bilingual daily TODO from `watchdog_state.json` + audit metadata alone.

## Initial State

| Check | Result |
|-------|--------|
| `python3 -c "with open('Register_ASEER_Professional.csv')..."` | `[Errno 11] Resource deadlock avoided` |
| `file Asher_Regional_Museum_Log.xlsx` | `ERROR: cannot read (Resource deadlock avoided)` |
| `find ... -name "Register_ASEER*"` | No results — file doesn't exist on disk |
| `ls -la Email_Archive/` | Empty directory (0 items) |
| `ls -la Docs/09_Registers/` | Files exist but all return deadlock |
| `file Technical_Office_Master_Log.xlsx` | Deadlock |
| `python3 -c "with open(path)..."` on Zamzam Submittal's LOG | Deadlock |
| `file` on individual xlsx files under Zamzam | `empty` |

**Verdict:** Both Failure Mode A (files don't exist at the CSV paths) and Failure Mode B (files at real paths are OneDrive-locked).

## Files That Were Tracked in `watchdog_state.json`

**Aseer Museum (last 30 days):** 680 files, mostly:
- `Design Files/Design Management Plan Rev C02 _ Aseer Museum.pdf` (May 18)
- `Design Files/Package_Part 2/.../Galleries & Auxiliary Spaces_rev A/BF_rev A/...` (May 17) — gallery exhibition .md verification files
- `Design Files/Package_Part 2/VERIFICATION_Fire_Safety_Sustainability.md` (May 17)
- Various C3, C4, D7, D8 verification markdown files
- Pre-existing structural/MEP design drawings (dated much earlier)

**Zamzam Museum (last 7 days):** 339 files, all from May 27, primarily:
- Furniture drawings: 67 sheets (FR-101 through FR-116)
- Wall finish drawings: 29 sheets (WF-101 through WF-103)
- Flooring drawings: 39 sheets (FL-101 through FL-103)
- Partition drawings: 40 sheets (PR-101 through PR-105)
- Skirting drawings: 33 sheets (SKR-101 through SKR-102)
- A&V coordination: 14 sheets
- Submittal log: `LOG list of Submittals for NWC (Zamzam Museum).xlsx`
- Structure/coordination: 3 sheets
- As-built, stair details, BOQ: remaining

**Zamzam Visitor Center (last 30 days):** 3 files from May 27:
- `P0639-Zamzam Visitor Center-R03.rar` (revised drawing package)
- `LOG list of Submittals for NWC (Visitors Center).xlsx`
- `P083-Zamzam Visitors Center_Architectural Design Development 09-April-2024.pdf`

## Priority Decision Rules Applied

| Signal | Rule | Outcome |
|--------|------|---------|
| `SI-CG-ASEER-007` mentioned in project index stakeholders | Known open SI → 🔴 HIGH | Created item #1 |
| `Design Management Plan Rev C02` — a management plan | Management plan approval → 🔴 HIGH | Created item #2 |
| `VERIFICATION_Fire_Safety_Sustainability.md` | HSE/Fire → 🔴 HIGH | Created item #3 |
| `LOG list of Submittals for NWC (Zamzam Museum).xlsx` | Submittal log → 🟡 MEDIUM | Created item #4 |
| `P0639-Zamzam Visitor Center-R03.rar` | Design package → 🟡 MEDIUM | Created item #5 |
| Missing 7 register types from audit report | Known gap → 🟡 MEDIUM | Created item #6 |
| 67x Furniture sheets in batch | Bulk shop drawing upload → 🟡 MEDIUM (1 item) | Created item #7 |
| 68x Wall+Flooring in batch | Bulk finish drawing upload → 🟡 MEDIUM (1 item) | Created item #8 |
| 73x Partition+Skirting in batch | Bulk partition drawing upload → 🟡 MEDIUM (1 item) | Created item #9 |
| 680 gallery exhibition .md files | Archive docs → 🟢 LOW | Created item #10 |
| `LOG list of Submittals for NWC (Visitors Center).xlsx` | Follow-up → 🟢 LOW | Created item #11 |
| 14 A&V sheets | Coordination review → 🟢 LOW | Created item #12 |

## Deduplication Strategy

- **Batch uploads** (339 Zamzam files from same day) → grouped by category (furniture, wall finish, flooring, etc.) with sheet counts
- **Same-day identical-type files** → single line item with range (e.g., "FR-101 to FR-116")
- **.md verification files** (680 Aseer gallery docs) → single "Package_Part 2 Docs" item
- **Files mentioned in audit report** (missing registers, open SIs) → single line each

## Output Caveat

The final output included the header line:
```
⚠️ CSV email registers on OneDrive are offline (dataless stubs — not synced locally). TODO based on watchdog file tracking + audit data.
```

This is critical — it sets user expectations that the TODO is inferred, not based on actual email register entries.

## Lessons for Future Sessions

1. **File categorization by name pattern** is reliable — AutoCAD/Revit sheet naming conventions (FR-xxx, WF-xxx, FL-xxx) map cleanly to construction categories.
2. **Counts add credibility** — saying "67 furniture sheets" is more useful than "furniture drawings received".
3. **Project index stakeholders section** contains undocumented open items — always check the `stakeholders` array in `bim_project_index.json` for SI numbers, DMP revision numbers, and other buried context.
4. **Audit report missing register types** → directly maps to actionable tasks.
5. **The `file` command on OneDrive files** reliably distinguishes "empty" (dataless stub) from "cannot read" (locked by sync engine) — use both diagnostics.
6. **Riyadh timezone** must be explicitly used: `TZ="Asia/Riyadh" date` — the cron host macOS time may differ.
