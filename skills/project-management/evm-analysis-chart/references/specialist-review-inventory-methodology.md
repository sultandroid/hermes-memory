# Specialist Review Inventory — EV Calculation Methodology

## Source of Truth

Use project registers (Excel) for item counts, NOT filesystem scanning:

1. **Drawing Register** — gives total expected drawings per specialist package
2. **Submittal Tracker / IFC Log** — gives submittal items per discipline with status
3. **Stamped packages in filesystem** — search for NRS-stamped or NRS-reviewed PDFs

## Per-Package Counting

For each specialist package:
- Count **total expected items** from register (e.g., SLF = 20 items)
- Count **NRS-reviewed items** from filesystem evidence (e.g., 6 items with NRS comments/stamps)
- Calculate % = NRS-reviewed / total

## EV Calculation — Two Methods

### Method A: Simple Proportional (Item Count)
```
bracket_ev = bracket_amount × (nrs_reviewed_items / total_items)
```
- Simple but ignores effort weighting
- 45/365 = 12.3% of 115K bracket = ~14K

### Method B: Effort-Weighted (Per-Package)
```
package_ev = bracket_amount × (pkg_weight% × pkg_completion%)
```
- More accurate when some packages need heavy review and others are light
- 5 packages × per-package EV = ~15K

### Critical Rule

**You must verify the method is consistent.** Don't say "45 of 365 items reviewed" (12.3%) alongside "EV = 9K" (7.8% of bracket). State:
- If using Method A: "SAR 14K — 12.3% of specialist bracket (45 of 365 items)"
- If using Method B: "SAR 15K — effort-weighted (13% of bracket value)"

## Fallback When No Register Exists

In some projects, no centralized register lists total items per specialist package. If the user cannot provide one:

1. **Estimate from subcontractor directories** — count files per subcontractor folder but note these include correspondence, RFIs, and non-drawing files. The count is an upper bound, not precise.
2. **Estimate from the specialist status report** — if one exists (e.g., Specialist_Packages_Status_Report.html), it may list "Files" counts per package. Note these are total files in directories, not expected review items.
3. **Use judgment-based estimates** — propose item counts based on project knowledge and mark them as "Est." in the table header. Add a footnote: "Item counts are estimates — no verified source register exists."
4. **Default to Method B (effort-weighted)** when totals are uncertain — weigh by observed review effort rather than claiming a false precision.

### Example (NRS Aseer Museum)
No register existed for specialist package item counts. The "Items" column used estimates (20, 73, 25, etc.) without a documented source. The user asked "are the nos correct?" — answer was "undocumented estimates." The fix: added a footnote and used effort-weighted EV (Method B) to avoid false precision.
