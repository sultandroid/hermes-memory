# XLSX Column Cleanup Pitfalls

When removing columns from Excel registers via openpyxl matching on header text, use **exact match**, not substring contains.

## The Bug (this session)

Deleting columns where `'SOW' in header.upper()` also matches `"Submittal / Deliverable (per SOW)"`, deleting the entire description column from 15 registers. Data unrecoverable from xlsx — no backup exists for OneDrive-only files.

## Correct Approach

```python
# WRONG — matches substring:
if 'SOW' in header.upper() or 'ER' in header.upper():
    cols_to_delete.append(col)

# RIGHT — exact match on cleaned text:
CLEAN_TARGETS = {'SOW', 'ER', 'SOW §', 'ER §', 'ER §b'}
clean = header.strip().replace(' ', '')
if clean in CLEAN_TARGETS or clean.upper() in {x.upper().replace(' ', '') for x in CLEAN_TARGETS}:
    cols_to_delete.append(col)
```

## Recovery Pattern (when descriptions are already lost)

```
1. Find original .py generator scripts via session_search for original file content
2. Original code has 8-field tuples: (ref, desc, sow, er, disc, mask, pkg, rm)
3. Strip sow,er → 6-field tuples: (ref, desc, disc, mask, pkg, rm)  
4. Regenerate fresh .py + run to produce .xlsx
5. .py → direct cp; .xlsx → AppleScript duplicate via Finder (OneDrive safety)
```

**For bulk regeneration (15+ files):** Delegate to a subagent with complete data + template. The subagent creates .py scripts and runs them. Verify every file's header after deploy — one missed rename corrupts the register.

## Aseer Museum Register Standard Template

```python
hdrs = ['Ref #', 'Submittal / Deliverable', 'Discipline', '50%', '90%', '100%', 'IFC/AFC', 'Sub-Package', 'Remarks']
cww = [7, 55, 14, 7, 7, 7, 10, 22, 28]
its = [(ref, desc, disc, [s50,s90,s100,sifc], sub_pkg, remarks), ...]
```

Column widths: Ref=7, Description=55, Discipline=14, stages=7 each, Sub-Pkg=22, Remarks=28.

## Date-Plan Format (instead of stage indicators)

Stage columns can hold **planned dates** instead of blank/— markers:

- 50% column = 50% submission planned date
- 90% column = 90% submission planned date  
- 100% column = 100% submission planned date
- IFC/AFC column = IFC target date
- `—` = N/A at this stage

**Staggered by floor/package (7-day review buffer):**
- Floor 1 50%: Day 0
- Floor 2 50%: Day +7
- Floor 3 50%: Day +14
- Floor 4 50%: Day +21
- 90%: +30 days after each floor's 50%
- 100%: +30 days after each floor's 90%
- IFC: fixed target date (e.g. Day +60)

Each sheet only shows its own stage's date (50% sheet → 50% column has date, others = `—`).

## Source File Structure Analysis

Before building a target register from a source file (e.g. Gates Submission Plan), analyze its ORGANIZATION structure first:

- Does it group by **level** (all packages per floor) or by **type** (all floors per package)?
- Preserve the source's grouping structure — don't reorganize unless asked
- The user expects the register to mirror the source file's hierarchy

## Key lesson

Always verify column removal visually before running bulk operations. A single `ls -1` or header-print check would have caught the missing description column. Run verification on one file first before batch-processing all.
