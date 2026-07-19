# Clean Copy Generation — Sister Companies Factory Cost Details

## When to use
User says "make clean copy" or "final copy" for a Factory_Cost_Details file.

## Process

### 1. Source the data from Section5_Factory_Details (not the working copy)
The `Section5_Factory_Details/` folder has the most complete version with genuine labor records. The `00_Organized_13_Project_Factory_Reconciliation/` working copy may have been modified. Always read from `Section5_Factory_Details/` as the source.

### 2. Determine project date range
- Project start: 01/01/2022 (default for Sister Companies)
- Project end: 12/12/2024 (default)
- Real data range: min/max dates from Labour Timesheet real attendance rows

### 3. Build clean copy structure
- **Labour Timesheet**: title row + column headers + data rows
  - Real rows first (in original order)
  - Then forecast rows distributed from project start to day before first real record
  - Then real rows
  - Then forecast rows from day after last real record to project end
- **Materials & POs**: title row + column headers + real PO rows only
- **Keep Other Expenses sheet** — do NOT remove it. The clean copy has 3 sheets: Labour Timesheet, Materials & POs, Other Expenses.
- No Summary or Gap_Analysis sheets (those go in the full version only)

### 4. Date redistribution for forecast rows
```python
# Before real data
days_before = (real_start - proj_start).days
step = max(1, days_before // 200)
for day_offset in range(0, days_before, step):
    dt = proj_start + timedelta(days=day_offset)
    date_str = dt.strftime('%d/%m/%Y')

# After real data
days_after = (proj_end - real_end).days
step = max(1, days_after // 200)
for day_offset in range(1, days_after + 1, step):
    dt = real_end + timedelta(days=day_offset)
```

### 5. Date parsing (MM/DD vs DD/MM)
Source data uses MM/DD/YYYY format. Try `datetime(year, month, day)` first, fall back to `datetime(year, day, month)`.

### 6. File naming
- New file: `{Project}_Factory_Cost_Details_Clean.xlsx`
- Same directory as the original Factory_Cost_Details.xlsx
- Original file is NOT modified

### 7. Verification
- Check date range spans project start to project end
- Check first 5 and last 5 rows for correct date ordering
- Check Materials & POs has only real PO rows (no forecast)
