# Source-Backed Section 5 Reconciliation

Use this protocol when converting factory-cost targets into worker timesheets, PO materials, logistics, and other expenses.

## Core principle

Matching the accounting target is not proof. Separate:

1. **Source-backed detail** — direct worker, PO, fleet, feeding, subcontract, or expense evidence.
2. **Documented allocation** — supported by an approved split, transfer, formula, or allocation note.
3. **Unsupported bridge** — the balance needed to reach the accounting target when evidence is absent.

Never label an unsupported bridge as BOQ labor, overhead, logistics, materials, or another real cost category merely because it makes the total match.

## Required reconciliation table

For each Section 5 line show:

| Field | Meaning |
|---|---|
| Accounting target | Amount in the main final workbook |
| Gross source-backed amount | Sum of real records before allocation |
| Approved allocation | Supported additions/deductions only |
| Unsupported bridge | Residual with no documentary basis |
| Detail total | Arithmetic result |
| Variance | Detail total minus target |
| Evidence status | Complete / Partial / Pending |

A zero arithmetic variance with an unsupported bridge remains **Pending**, not reconciled.

## Labor rules

- Prefer project exports containing date, worker, trade, hours, rate, cost, and task description.
- Verify `Cost = Hours × Rate` per row.
- Treat subcontract labor separately and cite its contract/reference.
- Aggregate FCA trade totals are corroboration, not worker-level timesheets.
- A generated or expanded labor register with repeated 9-hour rows, generic project descriptions, or rates conflicting with the project export must not replace the authoritative project export.
- If the Section 5 labor target exceeds verified timesheets plus supported subcontract labor, label the remainder `Unsupported Section 5 labor balance — pending evidence`.
- Do not call the remainder `BOQ Labor Allocation` unless task-level labor components demonstrably sum to it.

## PO/material rules

- Show every real PO line: PO number, date, status, supplier/requester, approver, description, quantity, unit, unit cost, and line total.
- Verify each line as `Qty × Unit Cost` and reconcile line sums to the PO header.
- If gross verified POs exceed the Section 5 materials target, do not proportionally reduce lines or invent shared overhead.
- Show the difference as `Pending allocation reduction` until an approved project/shared-factory allocation basis exists.
- Preserve gross PO evidence even when the accounting target is lower.

## Logistics and other-cost rules

- List only source-backed feeding, fleet, transport, subcontract, and factory-expense records.
- A fleet request without an amount proves movement, not cost.
- Keep Section 1 accounting items out of Section 5 even if they look factory-related.
- If verified other costs do not reach the target, isolate the residual as `Unsupported other-cost balance — pending evidence`.

## Section 1 exclusion check

Compare against every accounting row, not only common examples. Typical exclusions include:

- External site labor
- AC units and air curtains
- Cashier/POS equipment
- Gypsum subcontract works
- Site crane or transport already booked in accounting
- Accounting paint/material purchases
- Acrylic, tools, worker meals, wood, steel mesh, tile labor, formica pressing, cleaning equipment, and consumables already in Section 1

Also disclose outgoing/incoming reallocations relevant to the project, even though they are not duplicated in the Section 5 detail.

## Workbook acceptance criteria

- Separate sheets for labor, PO materials, other costs, reconciliation, and source register.
- Formula-based row calculations and totals.
- Exact source path plus sheet/cell or JSON key for every supported record.
- Explicit evidence status on every Section 5 line.
- Correct main-workbook cell references; verify rather than infer row numbers.
- If formula caches are blank, open/recalculate with a spreadsheet engine before client delivery, or warn that non-calculating readers may display blank totals.
- Never call a workbook client-ready while a material unsupported bridge remains.

## Pre-existing workbook audit (before building new detail)

Before constructing a new Section 5 detail workbook, audit the existing Factory_Details.xlsx for these common defects:

1. **Hardcoded labor subtotal** — the subtotal row may be a hardcoded number that does not match the sum of its own detail rows. Use `openpyxl` with `data_only=False` to detect hardcoded totals vs formulas. In Rateeb, the subtotal (36,286) was hardcoded and did not match 1,382 detail rows (269,439).

2. **Flat adjustment with zero detail** — materials and expenses sheets may contain only `Materials Adjustment: 30,239` or `Expenses Adjustment: 19,871.36` with no PO numbers, no expense records, and no breakdown. A detail sheet with zero real rows is not a detail sheet.

3. **Unfiltered labor register** — the labor timesheet may contain records for ALL projects, not just the target project. Filter by project name/description in the task column before summing. Verify the subtotal matches the filtered sum.

4. **Missing PO line-item units** — the SysLeaders source does not record units for PO line items. Set the unit column to `Not recorded` rather than inferring labels like `sheet`, `roll`, `pcs`, or `drum`.

5. **Reconciliation sheet blank** — the reconciliation sheet may have no accounting target, no source totals, no variance, and no approval status. Populate it with real values before calling the workbook complete.

## Two-output pattern

Maintain two distinct outputs when evidence is incomplete:

1. **Internal evidence workbook** — exact source paths/cells, unsupported bridges, allocation status, and reconciliation controls. This is the working document.
2. **Client export** — clean presentation with source references reduced to document/PO/reference identifiers. No internal filesystem paths, DB plans, or diagnostic notes.

Do not create or label a client-ready export while a material unsupported bridge remains. Clean presentation must never conceal an evidence gap or turn a `Pending` line into `Complete`.

## Rateeb worked control example

Rateeb Section 5 target:

- Labor: SAR 36,287.00
- Materials: SAR 30,239.00
- Other: SAR 19,871.36
- Total: SAR 86,397.36

Verified evidence found during the sample build:

- Five worker-level records: SAR 5,508.00
- Subcontract labor `CONT-0042`: SAR 4,938.00
- Labor unsupported bridge: SAR 25,841.00
- Three POs / 13 lines gross: SAR 39,969.50
- Materials pending allocation reduction: SAR 9,730.50
- Verified feeding and transport: SAR 876.00
- Other-cost unsupported bridge: SAR 18,995.36

This example ties arithmetically but remains evidence-incomplete. Use it as a control pattern, not as approval of the unsupported balances.