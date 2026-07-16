# Cafe Machine and Equipment Cost Audit

Use this reference when auditing machine/equipment amounts across Sister Companies cafe workbooks.

## Audit sequence

1. Inventory every expected cafe project **main** workbook under `_Final/Qahwitna comp_`; record missing files and do not mistake a `Section5_Detail.xlsx` workbook for the main costing workbook. Locate original, restructured, FCA, email-extract, project-extra, and archived costing workbooks.
2. Open the final workbook with formulas preserved (`data_only=False`). For disputed formula cells, inspect raw XLSX XML (`xl/worksheets/sheetN.xml`) because document extraction or cached-value reads may hide formulas. Use `data_only=True` separately when cached calculated values are needed.
3. Extract from every Equipment/Machines sheet:
   - cell address
   - reference/item number
   - description
   - amount
   - formula and precedents
   - transfer source/destination
4. Search **all final sheets**, not only Equipment/Machines. A source equipment item may have been reclassified under tools, plumbing, materials, or miscellaneous.
5. Trace each hardcoded component to an original row with description, amount, voucher/invoice, date, and exact workbook/sheet/cell.
6. Reverse the trace: enumerate source equipment/machine lines and locate each in the finals. This catches omissions and reclassifications that final-to-source tracing misses.
7. Reconcile the final equipment total to its source register. A mathematically correct `SUM` does not validate unsupported component values. Calculate source amount, final amount, and balance per item.
8. Search all project workbooks for the same reference, normalized description, and exact numeric amount to detect duplicates and incomplete inter-project transfers. Emit the full matching row with coordinates. Repeated backup/archive/email-extract copies are provenance copies, not cross-project duplicates.
9. For allocations, prove the percentage and original base amount. Check that outgoing and incoming project records mirror each other. A common reduction ratio is not an explained allocation without a formula, percentage, transfer note, or other documentary bridge.
10. Separate actual cafe machines from kiosk/container/temporary-facility/tools classifications; flag classification for management confirmation rather than silently treating all as equipment.
11. Report supported, unsupported, duplicated, transferred, reclassified, omitted, rounded, and missing-reciprocal entries. Keep confirmed evidence separate from gaps; do not add recommendations or modify files unless explicitly requested.

## Formula verification pitfall

A prior audit initially reported formula cells as hardcoded because an extraction/cached-value view did not expose formulas. Raw XML later confirmed:

- summary cell linked to the Equipment total
- Equipment total used `SUM(component cells)`
- only the component values were hardcoded

Therefore, before calling a total hardcoded, verify with both openpyxl `data_only=False` and raw workbook XML.

## Evidence standard

An amount is supported only when a source row provides at least a meaningful reference or voucher plus matching description and amount. Labels such as “miscellaneous equipment” without reference, invoice, supplier, voucher, or calculation remain unsupported even when included in a correct total formula.

## Inter-project transfer control

For any transfer:

- identify original item and total
- prove allocation percentage/calculation
- verify outgoing entry in source project
- verify corresponding incoming entry in destination project
- ensure it is excluded from the source project’s retained cost where applicable

An outgoing transfer without a corresponding incoming destination record is incomplete.