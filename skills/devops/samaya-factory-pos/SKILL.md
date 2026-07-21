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

## Chatter Payment Evidence Detection

POs may show as unpaid in Odoo bills but actually be paid outside Odoo (from workshop allowance/عهده by Ibrahim Shaaban). Always check chatter before finalizing cashout.

**How to read chatter (via message_ids):**
```python
po_full = models.execute_kw(db, uid, apikey,
    'purchase.order', 'read', [po_id],
    {'fields': ['name', 'message_ids']})
msg_ids = po_full[0].get('message_ids', [])
for mid in msg_ids[:15]:
    msg = models.execute_kw(db, uid, apikey,
        'mail.message', 'read', [mid],
        {'fields': ['body', 'date']})
    body = msg[0].get('body', '')
    if body:
        clean = re.sub(r'<[^>]+>', '', body).strip()
```

**Payment evidence keywords (Arabic):**
| Keyword | Meaning |
|---------|---------|
| صورة التحويل | Transfer image (proof of payment) |
| مرفق لكم صورة التحويل | Transfer image attached |
| مدفوع من العهده | Paid from allowance (Ibrahim's petty cash) |
| تم الدفع / تم التحويل | Payment/transfer done |
| يرجي ارفاق الفاتورة الضريبية | Payment sent, waiting for tax invoice |

**Known chatter-paid POs (paid outside Odoo):** P01924, P01939, P01894, P01977 — these have transfer images in chatter or "مدفوع من العهده" note. Maintain this set and update as new evidence emerges.

**Adjusted cashout:** `truly_unpaid = total_unpaid_bill - chatter_evidence_paid`. Report both numbers so user can verify.

## Daily Cron Job

A cron job runs daily at 2:00 PM KSA to refresh both reports. It:
1. Runs `build_cashout_report.py` — refreshes Factory POs with bill + chatter payment status
2. Runs `update_workshop_tracker.py` — updates workshop purchasing tracker with Odoo payment data
3. Runs `new_pos_last_3_days.py` — checks for new POs
4. Delivers a formatted summary to all channels (Telegram + CLI)

The cron job is named "Factory PO Daily Update" and delivers to `all` channels.

## New POs Detection

To find new POs in the last N days:
```python
three_days_ago = (date.today() - timedelta(days=3)).isoformat()
domain = [['date_order', '>=', three_days_ago]]
rows = call('purchase.order', 'search_read', [domain],
    {'fields': fields, 'limit': 50})
```
Filter for Factory (project 244) or workshop vendors using the workshop vendor list. New POs are typically in `draft` state and not yet included in the cashout report.

## Linked Files
- `references/odoo-18-domain-quirks.md` — Odoo 18 XML-RPC workarounds
- `references/workshop-vendors.md` — comprehensive workshop vendor name list
- `scripts/build_cashout_report.py` — reusable report builder
- `scripts/update_workshop_tracker.py` — updates workshop purchasing tracker with Odoo payment data
- `scripts/new_pos_last_3_days.py` — detects new POs created recently

## Pitfalls
- Odoo 18 `search_read` with `project_id` in domain crashes — always fetch all + Python filter
- Odoo 18 `['name','in',list]` domain crashes — same workaround
- **`'not in'` domain operator crashes** — `[['state','not in',['draft','cancel']]]` causes `TypeError: BaseModel.search_read() got multiple values for argument 'fields'`. Use positive list instead: `[['state','in',['purchase','done']]]`
- **`search_read` domain format** — must wrap domain in an extra list: `[domain]` not `domain`. Correct: `models.execute_kw(db, uid, apikey, model, 'search_read', [domain], {'fields': fields})` — the extra `[]` around domain is critical.
- **`account.move.read()` for bill lookup** — use `read()` with single ID, not `search_read()`, to avoid the `'in'` operator crash: `models.execute_kw(db, uid, apikey, 'account.move', 'read', [inv_id], {'fields': ['name','amount_total','amount_residual','payment_state','state']})`
- `search_read` limit defaults to 500 — set to 2000 to catch old POs
- OneDrive path has Arabic characters — use exact path from `read_file` output
- **Workshop vendor list** — when filtering workshop POs by vendor name, use the comprehensive list in `references/workshop-vendors.md`. The list covers all known workshop suppliers (carpentry, paint, fiber, metal, upholstery, wood, veneer, outsourcing, expenses).
