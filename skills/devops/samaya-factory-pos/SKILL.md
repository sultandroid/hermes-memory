---
name: samaya-factory-pos
title: Samaya Factory — PO Reports & Cashout
description: Build, update, and maintain Samaya Factory purchase order reports (cashout, POs not received) from Odoo 18 data.
triggers:
  - User says "update the POs report" or "update cashout report" for Samaya Factory
  - User asks about Factory POs, credit suppliers, or cash requirements
  - User provides a هام file to cross-check against Odoo
  - User provides a supplier account statement PDF (Saba Najd, Mada Aljezera, etc.)
---

# Samaya Factory — PO Reports & Cashout

## Data Source
Odoo 18 at `samayainv.odoo.com`, project **244 = Samaya Factory**.

## SSL Fix (macOS Python 3.13+)
```bash
SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") python3 script.py
```

## Fetching POs from Odoo
**Must fetch ALL and filter in Python** — Odoo 18 crashes on `project_id` in `search_read` domains.

```python
all_pos = call('purchase.order', 'search_read', [[]],
    {'fields': fields, 'limit': 2000})  # 1895 total as of Jul 2026
factory_pos = [p for p in all_pos
    if p.get('project_id') and p['project_id'][0] == 244]
```

## Filter Rules (confirmed with user)
- **Include:** All Factory POs from the هام file (or all unpaid Factory POs)
- **Exclude:** Zero-amount POs, credit suppliers
- **Credit suppliers** handled via periodic statements — show only balance totals, never individual POs
- Include draft/cancelled/invoiced POs if user wants them
- **هام file cross-check:** When user provides a هام file, compare every PO against Odoo. List included POs with descriptions from the file, and show excluded POs with reasons (other project, zero amount, credit supplier).

## Credit Supplier Partner IDs
| Supplier | Odoo ID |
|---|---|
| مؤسسة مدى الجزيرة للتجارة (Mada Aljezera) | 2427 |
| صبا نجد- Saba Najad (1224) | 5603 |

## Excel Format
- **Sheet 1: Summary** — Navy `#1F3864` header, total cashout, credit supplier note
- **Sheet 2: POs Detail** — PO#, Vendor, Vendor Reference, Description, Date, Amount, State, Invoice, Notes
- **PO # column** — clickable hyperlink to Odoo PO page: `{ODOO_BASE}/web#id={id}&model=purchase.order`
- **Vendor Reference** — `partner_ref` field from Odoo
- Landscape A4, yellow total rows, alternating row shading, `#,##0.00` for amounts
- Credit supplier section shows balance totals only (not individual POs)
- Excluded POs listed at bottom with reasons

## Output Path
```
~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Orders/2026/0000 اداريات/00 تقارير الاعمال/Samaya_Factory_Cashout_Report_Updated.xlsx
```

## Script
A reusable script lives at `scripts/build_cashout_report.py` in this skill directory. Run:
```bash
SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") \
  python3 ~/.hermes/skills/devops/samaya-factory-pos/scripts/build_cashout_report.py
```

## Linked Files
- `references/odoo-18-domain-quirks.md` — Odoo 18 XML-RPC workarounds
- `scripts/build_cashout_report.py` — reusable report builder

## Pitfalls
- Odoo 18 `search_read` with `project_id` in domain crashes — always fetch all + Python filter
- Odoo 18 `['name','in',list]` domain crashes — same workaround
- `search_read` limit defaults to 500 — set to 2000 to catch old POs
- OneDrive path has Arabic characters — use exact path from `read_file` output
