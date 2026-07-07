# HTML Sheet-Audit Notes

Session-tested patterns for validating multi-sheet A4 HTML documents.

## Sheet Counting

HTML documents often use `<div class="sheet">` but add modifier classes such as `cover`, `compact`, or `tight`. A naive `class="sheet"` substring match undercounts sheets.

Correct pattern:
```python
sheet_opens = re.findall(r'<div[^>]*class="sheet[^"]*"', c)
sheets = len(sheet_opens)
```

This matches:
- `<div class="sheet">`
- `<div class="sheet cover">`
- `<div class="sheet compact tight">`

## CSS Whitespace

CSS property checks must normalize whitespace. `page-break-after: always;` (with a space) is valid CSS but fails a literal `page-break-after:always` substring check.

Preferred approach (regex, preserves original source):
```python
if not re.search(r'page-break-after\s*:\s*always', c):
    issues.append("Missing page-break-after:always")
```

Alternative (normalize then check):
```python
c_nospace = c.replace(' ', '').replace('\t', '').replace('\n', '')
if 'page-break-after:always' not in c_nospace:
    ...
```

## Continuation-Sheet Footers

When an appendix or figure spans multiple sheets, the continuation sheets sometimes omit the standard `pg-footer`. Cover sheets also legitimately lack footers.

Correct check:
```python
footer_count = len(re.findall(r'<footer[^>]*class="pg-footer"', c))
cover_count  = len(re.findall(r'<div[^>]*class="sheet\s+cover[^"]*"', c))
expected_footers = sheets - cover_count
if footer_count != expected_footers:
    issues.append(f"Sheets missing footers: {sheets} sheets ({cover_count} cover) but {footer_count} pg-footer blocks (expected {expected_footers})")
```

## Project-Fact / Role Audit

For project Method-of-Statement and report HTML, validate named roles against the current project facts before issuing:

1. Extract plain text: strip `<script>`, `<style>`, and tags.
2. Search for named signatories (`Eng\. X`, `Dr\. Y`) in QC sign-off blocks.
3. Cross-check each named role against the project team list:
   - Project Director
   - QA/QC Manager
   - BIM Manager / BIM Lead
   - Technical Office Manager
   - Project Engineer
   - HSSE Manager
   - Document Controller
4. Flag mismatches (departed staff, acting titles that no longer apply, outdated org names).
5. Also verify immutable project facts: client name, contractor, location, building area/levels, and equipment model numbers.

When a role is vacant, blank the signatory name (`—`) while keeping the title so Document Control can fill it later.

## Schedule / Programme Alignment Audit

For MOS documents that include a schedule or timeline (scan rounds, construction phases, deliverable windows), validate the dates against the **current approved project programme** rather than a generic "Week 1..N" axis.

### Steps

1. Locate the current baseline/master programme (common paths: `Docs/02_Plans_and_Procedures/02.8_Master_Programme/` or `09_Correspondence/`; look for files named `*Baseline_Schedule*`, `*Master_Programme*`, `*Project_Schedule*`).
2. Read with `openpyxl` if `pandas` is unavailable:
   ```python
   import openpyxl
   wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
   ```
3. Extract key dates:
   - Mobilisation / site access
   - Demolition / remediation start and end
   - MEP / structure / finishes start and end
   - Substantial completion / handover
   - As-built documentation window
4. Compare each phase in the MOS schedule table / Gantt chart to the programme.
5. Flag mismatches such as:
   - MOS assumes Week 1 of project but programme is already at Week 24+
   - Scan round scheduled before mobilisation or after handover
   - Generic durations used where programme milestones are fixed
6. Update the MOS to use programme-aligned language:
   - Replace "Week 1" with actual month/date windows
   - Replace "post-demolition" with "early Sep 2026 (post-demolition)"
   - Add a note citing the programme source file
7. Redraw Gantt axes in months (Jun–Nov 2026) rather than abstract week numbers when the project is already underway.

### Pitfall: Confusing Project Start with MOS Start

A common error is writing "Round A = Week 1" meaning "first week of the project". If the MOS is written months after NTP, Week 1 is in the past. Always anchor scan rounds to **calendar dates or current programme activities**, not elapsed project weeks, unless the document is explicitly a pre-NTP planning study.
