# Register Log Reading Pattern

## When to use
Any time a plan document references another project document by number (Master Programme, DMP, BEP, HSE Plan, etc.) and needs to state its current status.

## File location
`Docs/09_Registers/_Master_Register_Index/Register Log.xlsb`

## Library
```python
# pip install pyxlsb  (NOT xlrd — .xlsb is binary Excel, xlrd only supports .xls)
from pyxlsb import open_workbook
import datetime

with open_workbook('path/to/Register Log.xlsb') as wb:
    # Search ALL sheets — docs may appear in any sheet
    for sn in wb.sheets:
        with wb.get_sheet(sn) as ws:
            for i, row in enumerate(ws.rows()):
                vals = [str(c.v) for c in row]
                line = ' '.join(vals)
                if 'SH-006' in line or 'DOC-NUMBER-HERE' in line:
                    print(f'[{sn}] R{i}: {vals}')
```

## Excel date serial conversion
```python
serial = 46151  # from cell value
real_date = datetime.date(1899, 12, 30) + datetime.timedelta(days=int(serial))
# 46151 -> 2026-05-09
```

## Status codes (column in register)
| Code | Meaning |
|------|---------|
| A | Approved |
| B | Approved as Noted |
| C | Revise & Resubmit |
| D | Under Review |
| E | Rejected |
| U | Under Review |

## Row structure (Document Submittals sheet)
Each row has multiple submission cycles as column groups:
- R0: Date Received | Forwarded to Client | Returned | Status | Days
- R1: Date Received | Forwarded to Client | Returned | Status | Days
- R2: ... (same pattern)
- R3: ... 
- R4: ...
- Current Status (final column area)

## Worked example: Master Programme MOC-ASEER-0PS-SH-006

Found in sheet " Document Submittals" (note leading space in sheet name), row 17:

| Rev | Submitted | Returned | Status |
|-----|-----------|----------|--------|
| R0  | 15-Jan-2026 | 25-Jan-2026 | C (Revise & Resubmit) |
| R1  | 23-Feb-2026 | 05-Mar-2026 | C |
| R2  | 04-Apr-2026 | 05-May-2026 | B (Approved as Noted) |
| R3  | 09-May-2026 | — | U (Under Review) |

The plan had "resubmitted after Code C" — actual status is "Under Review since 09-May-2026".

## OneDrive note  
Direct `openpyxl.load_workbook()` on OneDrive `.xlsb` files may timeout with `TimeoutError`. Use `pyxlsb.open_workbook()` which reads via a different path and handles OneDrive cloud files better. If still timing out, use `terminal` with `python3 -c` which has better timeout handling than `execute_code`.

## Plan Reference Verification Workflow

When a plan document references other project documents by number (Master Programme, DMP, BEP, HSE Plan, etc.), verify ALL references against the Register Log Document Submittals tab:

1. **Extract all MOC-XXX-XXX-XXXX-XN-XXX-NNNN pattern doc numbers** from the plan HTML (grep for `MOC-`)
2. **Search the Document Submittals tab** for each number. Most plan/procedure references are in this tab.
3. **Verify exact match** — check that the doc number prefix, series, discipline code, and sequential number all match
4. **Cross-reference the description column** — same description = same document
5. **Note any prefix pattern transitions**: Older docs use `MOC-ASEER-SIC-1K0-PL-XXXX`, newer docs use `MOC-MUS-ASE-1K0-PL-XXXX`. The transition occurs around PL-0028/0029. The plan's own doc number should follow the CURRENT convention for its age.
6. **Report discrepancies** — wrong prefix, wrong sequential number, or doc not found in the register

## File version note
The master register file is `Register Log.xlsb` in `Docs/09_Registers/_Master_Register_Index/`. The user may share a copy named `Register Log (N).xlsx` — this has the same data but `.xlsx` format (readable with `openpyxl` instead of `pyxlsb`). The sheet structure is identical regardless of format.

## Document numbering convention
From the Register Log Document Submittals tab, the document numbering scheme is:

- **Project code**: `MOC-MUS-ASE` (current) or `MOC-ASEER-SIC` (older/transitional). The plan cover should use the CURRENT convention.
- **Discipline code**: `1K0` (general/management), `1A0` (architectural), `1E0` (electrical), `1M0` (mechanical), `1KH` (HSE), `0PS` (planning/schedule), `0Q0` (quality), `1C0` (civil), `1V0` (survey), `0L0` (legal/commercial)
- **Doc type code**: `PL` (plan), `RP` (report), `ZD` (general doc), `SP` (specification), `TP` (test plan), `QT` (quantity take-off), `TR` (test report), `CO` (commercial), `SH` (schedule), `SC` (HSE deliverable), `MA` (material submittal), `SNA` (starting new activity), `IR` (inspection request), `KP` (key personnel)
- **Sequential number**: 4-digit, starting at 0001. Plans run from PL-0001 (Mobilization Plan) through PL-0057 (last in register). New plans get the next available PL number.

## Pitfalls
- Sheet names may have leading/trailing spaces (e.g. " Document Submittals" not "Document Submittals")
- The register uses serial dates, not ISO dates — must convert
- Some rows have empty submission cycles — only filled columns are meaningful
- The "Current Status" column at the end is the authoritative current status
- **File format**: The master is `.xlsb` (use `pyxlsb`), copies shared as `.xlsx` (use `openpyxl`). Do NOT use `xlrd` for either format.
- **Prefix mismatch**: A doc number on the filesystem filename may differ from the Register Log entry. The Register Log is the authoritative reference — always prefer its doc number over the filename on disk.
- **Plan covers use the user's preferred prefix**: The plan HTML may use `MOC-ASEER-SIC-1K0-PL-00XX` (user's choice) even though the register could have it as `MOC-MUS-ASE-1K0-PL-00XX`. This is a user preference — flag it but don't change without direction.
