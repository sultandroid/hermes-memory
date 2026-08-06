# Odoo 18 — Stock & MRP Quirks (Aug 2026)

## stock.location search_read crash

`search_read` with `['id', 'in', factory_locs]` in the domain causes:
```
ValueError: not enough values to unpack (expected 3, got 2)
```
This is caused by the `stock_barcode` module overriding `_search`. Workaround: fetch all locations and filter in Python, or use a simpler domain.

## mrp.production — project_id distribution

MOs are NOT concentrated in one project. As of Aug 2026:
- Jalal & Jamal - Jabal Omer: 14
- متاجر الغمامة: 12
- Samaya Factory: 12
- متجر الهدايا - معالم الحرمين: 9
- HR Office Alsully: 7
- celebrating Silver Jubilee: 7
- Plus 20+ other projects

Always fetch all MOs and filter in Python when project-specific.

## Factory Stock Locations

| ID | Name | Usage |
|----|------|-------|
| 45 | Factory | internal |
| 46 | Stock (under Factory) | internal |
| 47 | Input (under Factory) | internal |
| 51 | Pre-Production (under Factory) | internal |
| 77 | Digital printing (under Factory) | internal |
| 78 | 3D Lab (under Factory) | internal |

Production consumption destinations: [15, 98] (Production virtual locations)

## Raw Materials Categories

Two root categories:
- **#356**: `Raw materials` (under `All`)
- **#700**: `Raw Materials` (top-level, no parent)

Together they cover 60 subcategories and ~953 products (Aug 2026).

Key subcategories: MDF, Plywood, Solid Wood, Wood Veneer, Paint (with 12 sub-types), steel (with 10 sub-types), Acrylic Sheet, Chemical and Glue, Fabric, Foam, Aluminum, Edge Banding, Resin&Fiber, etc.

## Consumables Categories (for monthly distribution)

| ID | Name |
|----|------|
| 220 | Consumables |
| 221 | Abrasives |
| 222 | Cutting Tools |
| 223 | Fasteners |
| 224 | Structural Anchoring Components |
| 225 | Packaging Materials |
| 226 | Welding Consumables |
| 353 | PPE & Safety |
| 354 | Eye Protection |
| 355 | Hand Protection |
| 396 | Tools |
| 397 | Hand Tools |
| 398 | Pneumatic Tools |
| 399 | Power Tools |
| 400 | Spray Equipment |

## PO Chatter — Payment Evidence Detection

Ibrahim Shaaban (Odoo partner ID: 4870, email: i.shaaban@samayainvest.com) records payments in PO chatter. Key patterns:

- "مرفق لكم صورة التحويل" — transfer image attached (proof of payment)
- "قائمة المهام تم" — task completed (payment done)
- "برجاء تحويل مبلغ X" — request to transfer amount X
- "يرجي ارفاق الفاتورة الضريبية" — payment sent, waiting for tax invoice

As of Aug 2026: 174 of 321 factory POs have payment evidence in chatter. 147 have none.

## Monthly Payment Volume (from chatter, Aug 2026)

| Month | Comments | Est. Amount |
|-------|----------|-------------|
| 2026-07 | 47 | ~320K SAR |
| 2026-06 | 60 | ~558K SAR |
| 2026-05 | 46 | ~465K SAR |
| 2026-04 | 22 | ~164K SAR |
| 2026-03 | 30 | ~156K SAR |
