# Plan Document Code Registration Workflow

When a new project plan document code is assigned or an existing plan's code is corrected, update ALL of these locations in the repo to keep codes consistent.

## Source of Truth

The plan's document code appears on the submittal transmittal form (DS form) or the plan cover page. Always verify against the submitted PDF, not the folder name alone.

## Locations to Update

### 1. Plan Tracker
File: `08_Document_Index/00_plan_tracker.md`

Update the plan's row with correct ref, rev, CG status, and date.

### 2. Plan Index MD File
File: `08_Document_Index/plan_{SHORTNAME}.md`

Update YAML frontmatter: `ref`, `doc_code`, `revision`, `date`, `cg_status`.

### 3. Reference Files
Files: `04_Docs/02_Plans_and_Procedures/reference/ref_{PLAN_NAME}.md`

Update the doc code and revision. These reference files are used by cross-document links.

### 4. Manager Lane Dashboards
Files: `10_Manager_Lanes/*/dashboard.md`

Each dashboard has a "Governing Sources" section listing plans relevant to that lane. Search for the plan by name and update its code.

### 5. SMP CR Sheet (if applicable)
File: `01_Source_Files/Rev01/SMP_CR_Sheet_Rev01.xlsx`

If the CR sheet references the plan by name (e.g. "Procurement Plan"), update to include the correct document code.

### 6. Obligation Matrix
File: `08_Document_Index/obligation_matrix.md`

Update the plan's row with its code, owner, and CG status.

### 7. Related Plan MD Files
Other plans that reference this plan (e.g. DMP referencing BEP) may have hardcoded codes in their text. Search the repo for the old code.

## Search Pattern

```bash
# Find all files referencing the old plan code
rg "MOC-ASEER-SIC-1K0-PL-0011" /Users/mohamedessa/aseer-museum-pm/
```

Then for each match, determine if it's a reference that needs updating.

## Verification

After updating, run:
```bash
rg "{NEW_DOC_CODE}" /Users/mohamedessa/aseer-museum-pm/ --count
```
Expected: all instances should show the new code with consistent revision.
