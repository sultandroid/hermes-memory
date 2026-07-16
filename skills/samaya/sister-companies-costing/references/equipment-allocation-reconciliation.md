# Equipment and Inter-Project Allocation Reconciliation

Use this reference when auditing machine/equipment totals across Sister Companies workbooks.

## Core rule

Never treat a final equipment total as valid merely because its formula adds correctly. Reconcile every final row to an original row or an approved two-sided transfer.

For each equipment item, capture:

- Source project and source workbook/sheet/cell
- Original item/reference number
- Description and original amount
- Destination project(s)
- Allocation basis and percentage
- Outgoing transfer cell
- Matching incoming transfer cell
- Unallocated balance
- Evidence status: Confirmed / Hypothesis / Unsupported

Required equation:

`Original amount = sum(confirmed destination allocations) + unallocated balance`

## Audit sequence

1. Inventory canonical source costing files using `references/source-folder-mapping.md`.
2. Extract all rows from sheets named `معدات`, `معدات (Equipment)`, or `Equipment`.
3. Extract final equipment sheets and linked main-summary formulas.
4. Match rows by item number first, then description and amount.
5. Track transfers on both sides. An outgoing transfer without a matching receiving row is incomplete.
6. Keep shared invoices in an `Unallocated Shared Equipment` control account until their breakdown is supported.
7. Reject generic balancing rows such as `معدات وأجهزة متنوعه` when they lack reference, voucher, supplier, formula, or transfer note.
8. Distinguish the accounting allocation convention from the actual beneficiary named in the invoice description.
9. Verify raw and final portfolio totals separately; do not silently mix direct equipment, shared equipment, or construction rows reclassified as equipment.
10. Inspect raw workbook XML when formula-vs-hardcoded status is disputed. Cached values from `data_only=True` are not formula evidence.

## Allocation pitfalls

- Area allocation must be explicit. If rounded percentages are used, record both the exact area ratio and rounded ratio; they may differ by a few SAR.
- Do not infer that a separate project transaction forms part of a shared invoice merely because the description is similar.
- Never use a final hardcoded amount as evidence for its own source.
- Do not allocate an invoice to a project not named as a beneficiary without approval.
- Kiosks, containers, cables, tools, smoke detectors, POS devices, and consumables require classification review before treating them as capital equipment.

## Case pattern: shared equipment item

A shared item may appear under one project even when its description names other shops. The defensible report must show:

| Field | Treatment |
|---|---|
| Original source amount | Preserve exactly once |
| Confirmed outgoing transfer | Record against source project |
| Matching incoming transfer | Record against recipient project |
| Unresolved remainder | Keep unallocated, never fabricate a destination |
| Candidate related transactions | Label hypothesis until a documentary bridge exists |

## Session evidence: cafe item #6

Source: project 03 item `#6`, SAR 189,894.01, described as equipment for iced-coffee and Arabic-coffee shops.

- Confirmed outgoing transfer to Ice Coffee: SAR 30,952.72.
- No receiving-side Ice main workbook entry was present.
- Unresolved balance: SAR 158,941.29.
- The recorded amount equals rounded 16.3%, apparently derived from Qahwatna/Hira areas; the complementary 83.7% was omitted from final workbooks.
- The source description does not establish Hira as beneficiary, so the area split is an accounting convention, not proof of ownership.
- Hira SAR 33,056.00 was unsupported: hardcoded, no reference/voucher/formula, no raw-row combination, no transfer bridge.

## Client-ready correction policy

- Rebuild equipment sheets from source rows; do not patch merged legacy sheets.
- Include item number, description, date, amount, supplier/voucher, source project, destination project, and transfer reference.
- Remove unsupported balancing amounts.
- Do not distribute unresolved shared balances until the invoice/quotation breakdown or written allocation approval is available.
- Validate every equipment-sheet total against the main summary and the portfolio transfer register.
