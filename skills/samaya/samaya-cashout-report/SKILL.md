---
name: samaya-cashout-report
title: Samaya Factory Cashout Report — Build from Odoo PO Data
description: Build a formatted Excel cashout report from Samaya Factory (project 244) POs via Odoo XML-RPC. Handles filtering, credit suppliers, Odoo hyperlinks, vendor references, and supplier invoice mapping.
triggers:
  - User says "update PO report" / "cashout report" / "POs report"
  - User says "update the POs reports" for Samaya Factory
  - User attaches a هام file and asks to reconcile with Odoo
  - User asks for a formatted Excel of outstanding POs
  - User says "add PO" / "remove PO" / "fix format" on the cashout report
---

# Samaya Factory Cashout Report

Build a formatted Excel cashout report from Samaya Factory (project 244) POs via Odoo XML-RPC.

## Prerequisites

- Odoo credentials at `~/.config/samaya/odoo.env` (ODOO_URL, ODOO_DB, ODOO_USER, ODOO_API_KEY)
- SSL fix: `SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")`
- Python packages: `openpyxl`, `xmlrpc.client` (stdlib)

## Workflow

### 1. Fetch POs from Odoo

```python
fields = ['name','partner_id','amount_total','date_order','state','project_id','invoice_status','partner_ref']
# ⚠️ project_id in domain causes TypeError on Odoo 18.0+e
all_pos = call('purchase.order', 'search_read', [[]], {'fields': fields, 'limit': 2000})
factory_pos = [p for p in all_pos if p.get('project_id') and p['project_id'][0] == 244]
```

### 2. Filter Logic

| Condition | Action |
|-----------|--------|
| Not project 244 | Exclude |
| amount_total <= 0 | Exclude |
| Credit supplier (partner 2427 or 5603) | Exclude from main list, show as statement balance |
| state == 'cancel' | Exclude |
| User says "delivered but not paid" | Force-include even if invoiced |

**Credit supplier IDs (Samaya Factory):**
- Mada Aljezera: 2427
- Saba Najad: 5603

### 3. Excel Format

**Summary sheet:**
- Navy header bars for sections (OUTSTANDING POs, CREDIT SUPPLIERS)
- 4 columns: Description | Count | Amount | SAR
- Saba Najad breakdown: Opening → Payment (green, negative) → New Invoices → Closing
- Grand Total row: yellow highlight (`FFF3CD`), thick navy border
- Use `Alignment(indent=N)` for indentation (NOT `.indent = N` — AttributeError)
- Row heights: title 30, section headers 24, grand total 30
- Column widths: A=42, B=28, C=20, D=20

**POs Detail sheet:**
- Columns: PO # (clickable Odoo link) | Vendor | Description | Date | Amount | State | Invoice | Notes | Vendor Reference
- Vendor Reference is column I (last), NOT column C — user preference
- PO # hyperlink: `{ODOO_BASE}/web#id={id}&model=purchase.order`
- Notes column: `[supplier IN: ref#]` for mapped supplier invoices
- Alternating row shading
- Yellow total row
- Credit supplier section below with individual POs listed (each with amount + supplier IN ref)
- Excluded list at bottom
- Column widths: A=14, B=38, C=35, D=14, E=16, F=12, G=12, H=30, I=22

### 4. Supplier Invoice Mapping

From Saba Najad statement PDF, map invoice numbers to POs by matching amounts:

```python
supplier_invoices = {
    'P01611': '20414+20415+20416+20417',
    'P01865': '20229',
    'P02026': '20580',
    'P02041': '20653',
    'P02078': '20661',
}
```

### 5. Force-Include Pattern

When user says "delivered but not paid" for POs that show `invoice_status=invoiced`:

```python
FORCE_INCLUDE = {'P01946', 'P02025', 'P02065'}
# Check before other filters
if po['name'] in FORCE_INCLUDE:
    included.append(po)
```

### 6. Page Setup

- Landscape orientation
- `fitToWidth = 1`
- `fitToPage = True`

### 7. Chatter Payment Evidence Check

POs may show as unpaid in Odoo bills but actually be paid outside Odoo (from allowance/عهده). Always check chatter for payment evidence before finalizing the cashout amount.

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
| مرفق لكم صورة التحويل | Transfer image attached for you |
| مدفوع من العهده | Paid from allowance (Ibrahim's petty cash) |
| تم الدفع / تم التحويل | Payment/transfer done |
| يرجي ارفاق الفاتورة الضريبية | Please attach tax invoice (payment sent, waiting for invoice) |

**Adjusted totals:** `truly_unpaid = total_unpaid_bill - chatter_evidence_paid`. Report both numbers so user can verify.

**Common POs paid from allowance (عهده):** Small-value POs (under 1,000 SAR) for supplies, paint, stationery — often marked "مدفوع من العهده" in chatter. Paid by Ibrahim Shaaban from workshop allowance, not through Odoo invoice workflow.

### 8. Workshop Purchasing Tracker Update

The workshop purchasing tracker at `.../شراء/ورشة المشتريات.xlsx` lists ALL workshop POs (not just Factory project 244). To update with Odoo payment data:

1. Query Odoo for all POs (state in purchase/done, 2026 onwards)
2. Build a PO lookup dict with bill payment info
3. Load the tracker with `openpyxl`
4. Add 2 new columns: "Odoo Pay State" (col J) and "Odoo Bills" (col K)
5. Color-code: green=paid, yellow=draft_bill, red=no_bill
6. Update title with today's date
7. Save and open

## Pitfalls

- **Odoo domain bugs:** Never use `project_id` or `'in'` operator in `search_read`/`search` domains on Odoo 18.0+e. Fetch all and filter in Python.
- **`'not in'` domain operator crashes** — `[['state','not in',['draft','cancel']]]` causes `TypeError: BaseModel.search_read() got multiple values for argument 'fields'`. Use positive list: `[['state','in',['purchase','done']]]`.
- **`search_read` domain format** — must wrap domain in an extra list: `[domain]` not `domain`. Correct: `models.execute_kw(db, uid, apikey, model, 'search_read', [domain], {'fields': fields})`.
- **`account.move.read()` for bill lookup** — use `read()` with single ID, not `search_read()`, to avoid the `'in'` operator crash: `models.execute_kw(db, uid, apikey, 'account.move', 'read', [inv_id], {'fields': ['name','amount_total','amount_residual','payment_state','state']})`.
- **Limit too low:** Odoo has ~1895 POs total. Use `limit=2000` or higher.
- **Credit suppliers:** User explicitly wants them as statement balances, not individual POs. Do NOT include Mada Aljezera or Saba Najad POs in the main list. Show them as statement balances with opening/payment/closing breakdown.
- **Credit supplier balance from statement PDF, not Odoo:** The balance comes from the supplier's PDF statement, not from summing Odoo POs. Use `pdftotext -layout` to extract the PDF and find the closing balance line.
- **Zero-amount POs:** Always exclude (draft POs with no amount).
- **Cancelled POs:** Exclude.
- **Vendor Reference column:** Use `partner_ref` field from Odoo. Place in column I (last column), NOT column C — user preference.
- **Indent in openpyxl:** Use `Alignment(indent=N)`, NOT `.indent = N` (AttributeError on openpyxl).
- **Number format:** Use `.number_format = '#,##0.00'` for amount cells.
- **User wants to see the file:** Always `open` the file after saving.
- **Force-include delivered-but-not-paid POs:** When user says "they delivery but still not payed", add a `FORCE_INCLUDE` set and check it before other filters. These POs may show `invoice_status=invoiced` in Odoo but the user confirms they haven't been paid.
- **Odoo message_post for comments:** Use `call('purchase.order', 'message_post', [[id]], {'body': '...', 'subject': '...', 'message_type': 'comment', 'subtype_xmlid': 'mail.mt_note'})` to add chatter comments to POs. The `message_post` method is always available even though it doesn't appear in `fields_get`.

## Related Skills

- `odoo` — Odoo connection, field schemas, SSL fix

## Support Files

### References
- `references/saba-najad-statement-2026-07.md` — Full transaction detail from the Saba Najad statement PDF (01 May - 07 Jul 2026), including opening/closing balances and PO-to-invoice mapping.
- `references/odoo-po-comment-workflow.md` — How to add chatter comments to Odoo POs via `message_post` for tracking cashout report references.
