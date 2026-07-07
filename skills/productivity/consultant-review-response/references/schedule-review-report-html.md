# Schedule Review Report — A4 HTML Template

After completing a Primavera P6 schedule audit (see §0b), produce a formal A4 print-ready HTML review report for issue. The report has four pages: cover, findings (2 pages), conclusion + distribution.

## Output location — CRITICAL

**ALWAYS save directly to the project folder, never Desktop or /tmp.** If there's no existing `Schedule_Programme/` subfolder under `10_Plans/`, create one:

```
PROJ_DIR="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/<Project-Name>"
mkdir -p "$PROJ_DIR/10_Plans/Schedule_Programme"
```

Document ref pattern for the report: `<Entity>-<Project>-SCH-RVW-<NNN>` (e.g. `TO-ASEER-SCH-RVW-001`).

## Report Structure

| Page | Section | Content |
|------|---------|---------|
| 1 | Cover | Dark navy cover with project title, doc ref, revision, date, prepared-by, distribution entities |
| 2 | Executive Summary | Severity summary cards (High/Med/Low counts), recommendation box, document control table |
| 2-3 | Findings | One table per finding: Ref | Severity (badge) | Title | Observation + Requirement + Reference |
| 3 | Findings cont'd | Remaining findings |
| 4 | Overall Assessment | Table per schedule aspect (WBS, Design, Procure, Construction, T&C, BIM) with SATISFACTORY/CAUTION/NOT ADEQUATE badges |
| 4 | Conclusion & Recommendation | Qualified acceptance statement, deadline for response |
| 4 | Distribution | Copy-to table |

## Finding Severity Badges

```html
<span class="badge badge-high">HIGH</span>   <!-- #FEE2E2 bg, #B91C1C text -->
<span class="badge badge-med">MEDIUM</span> <!-- #FEF3C7 bg, #92400E text -->
<span class="badge badge-low">LOW</span>    <!-- #DBEAFE bg, #1E40AF text -->
```

## Finding Row Highlight

- HIGH severity rows: `<tr class="highlight">` → `background: #FEF2F2`
- MEDIUM severity rows: `<tr class="med">` → `background: #FFFBEB`
- LOW severity rows: no class (white)

## Each Finding Table Columns

| th | Width | Content |
|----|-------|---------|
| Ref | 22mm | `F-01` etc. |
| Severity | 22mm | Badge + severity text |
| Title | auto | Bold short title |
| colspan=3 | | Observation paragraph, Requirement paragraph, Reference paragraph |

## Summary Cards Grid

4-column grid with count + label. HIGH card gets `border-left: 3px solid #B91C1C`, MED gets `#D97706`, LOW gets `#2563EB`.

## Page Header

```
.left:   <strong>Schedule Review Report</strong><br>
         <Project> &mdash; <Schedule Rev><br>
         <Doc Ref> &middot; Rev A
.right:  Samaya Investment<br>Technical Office
```

## Page Footer

Fixed position at page bottom, 3-column: doc ref / title + rev / page number.

## Recommendation Box

Green background `#F0FDF4` with `border: 1px solid #86EFAC` — wraps the acceptance verdict.

## Aspect Assessment Table

| Aspect | Assessment |
|--------|-----------|
| WBS Structure & Logic | badge-low = SATISFACTORY |
| Design Timeline | badge-med = CAUTION |
| Procurement & Supply Chain | badge-high = NOT ADEQUATE |
| Construction Duration | badge-med = CAUTION |
| Testing, Commissioning & Handover | badge-high = NOT ADEQUATE |
| BIM / COBie Deliverables | badge-med = CAUTION |
| Resource Planning | badge-med = CAUTION |

## Cleaning Up

After moving the file to the project folder, remove any Desktop copy:

```bash
rm ~/Desktop/<filename>.html
```
