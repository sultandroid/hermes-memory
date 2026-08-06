# CRS Template Location

## Approved Blank Template

The approved blank CRS template is hosted at:

- **Web:** https://samaya-factory.com/templates/crs/
- **Direct download:** https://samaya-factory.com/templates/crs/CRS_TEMPLATE_BLANK.xlsx
- **OneDrive:** `04_Docs/09_Registers/CRS_Templates/CRS_TEMPLATE_BLANK.xlsx`

## All Templates Index

All Samaya approved blank templates are at:

- **https://samaya-factory.com/templates/**

Includes: CRS, DOCX, RFI, A4 print HTML, QAQC log, Clash report, Weekly progress report, Structural penetration register.

## Agent Workflow

When the user says "create CRS" or "make a CRS sheet":

1. **Fetch the blank template immediately** from `https://samaya-factory.com/templates/crs/CRS_TEMPLATE_BLANK.xlsx` — do NOT ask which template, do NOT describe the format, do NOT ask for confirmation
2. **Save as** `CRS_[DocRef]_Rev[XX].xlsx` in `02_CG_Responses/`
3. **Fill header block** (rows 1-7): PROJECT NAME, CRS NUMBER, DOCUMENT No., DOCUMENT TITLE, DISCIPLINE, DATE, Rev
4. **Fill data rows** (row 11+): No., Initial, Sheet/Ref, Code, Reviewer Comment, Originator Reply, Reply By, Status
5. **Present to user for review** — do NOT send to CG or specialist without user approval
6. **Do NOT get sidetracked** by other tasks (risk register updates, merge conflicts, template hosting) before completing the CRS — the CRS is the primary deliverable

## Pitfalls

- **Do not ask the user which template to use** — the blank template is the only approved one
- **Do not describe the format** — just fetch and fill it
- **Do not start other tasks** (risk updates, file hosting, git operations) before delivering the CRS
- **OneDrive deadlock** — if OneDrive files fail to copy (Resource deadlock avoided), quit OneDrive first or use Python shutil after a delay

## Format Reference

8 columns (A-H): No., Initial, Sheet/Ref, Code, Reviewer Comment, Originator Reply, Reply By, Status

- Code C: red fill (#B01E2F), white bold text
- Status Closed: green fill (#C6EFCE), green text
- All cells: thin black borders, Calibri 9pt body, 10pt bold headers
- Write values BEFORE merging cells
