# Machine / Equipment Cost Trace Protocol

Use this protocol for project or portfolio reconciliation of equipment and machinery across final, current/restructured, original, archived, email-extract, management, and `_Archive/Project_Extras` workbooks.

## Evidence standard

Report confirmed workbook cells, source cells, reference/description/amount matches, formula-supported allocations, proven transfers/duplicates, and explicit gaps. A similar amount, common ratio, or plausible project relationship is not a documentary bridge.

## Procedure

1. **Inventory finals first.** Identify each main final workbook and do not substitute `Section5_Detail.xlsx`. Record missing main finals as completeness gaps.
2. **Extract final rows.** Capture reference, description, amount, formula, sheet, and exact cell. Search all sheets because equipment can be reclassified under construction, MEP, tools, materials, plumbing, or miscellaneous.
3. **Trace final to source.** Search current/restructured, original, archive, email-extract, Project_Extras, and management workbooks by reference, normalized description, and exact amount. Prefer the earliest row-level transaction source; use management files as corroboration.
4. **Trace source to final.** Reverse the search to identify omitted or reclassified source equipment.
5. **Test exact amounts portfolio-wide.** Emit full matching rows with coordinates. Backup/archive/email copies are provenance, not duplicates. A duplicate requires the same identifiable transaction to be included under more than one canonical project scope.
6. **Verify formulas.** Load with `data_only=False` and `data_only=True`; inspect raw worksheet XML when a disputed formula may be misreported as a value. Arithmetic validity does not supply missing invoice/reference evidence.
7. **Verify both sides of transfers.** Require source reference/description/amount, outgoing record, receiving record, and transfer note. A split is confirmed when destination components sum exactly to the source. If only one side exists, quantify both the recorded movement and unsupported residual.
8. **Reconcile balances.** Distinguish omitted, transferred, reclassified, rounded, duplicated, and unsupported lump-sum balances.

## Portfolio canonicalization

Define the counting basis before calculating totals:

- Choose one canonical raw transaction set per project. Prefer the current/restructured workbook's dedicated Equipment sheet when it has row-level references and amounts; otherwise use the earliest original or Project_Extras evidence.
- When a main sheet and extracted Equipment sheet repeat the same references/descriptions/amounts, count the transaction once.
- Choose only the main final workbook as canonical final evidence.
- Use explicit `معدات` / `Equipment` / `تجهيزات (Equipment)` classifications for the primary control total. Trace equipment-like Construction/MEP/tools/materials rows separately rather than silently changing the total's scope.
- Calculate canonical raw, canonical final, and `final - raw` per project; sum only those per-project totals for the portfolio.
- State exclusions before reporting `final/raw` retention percentage.
- A generic final lump sum without item references, invoice, voucher, or allocation note is unresolved even when close to the raw total.
- Save broad scans to JSON/CSV before summarizing; console output may truncate large match sets.

## Classification cautions

Distinguish actual machines from kiosks, used containers, temporary facilities, rented equipment, consumable tools, and operating supplies. Preserve workbook classification in the arithmetic and flag questionable classifications separately.

## Reporting format

Organize by project and include:

- canonical raw and final paths;
- sheet and exact cell/range;
- item reference, description, and amount;
- source and final totals and difference;
- status: exact match, transfer, split, reclassified, duplicate, omitted, or unexplained;
- portfolio raw total, final total, difference, and clearly defined scope.

Keep confirmed evidence separate from gaps. Avoid recommendations unless requested.
