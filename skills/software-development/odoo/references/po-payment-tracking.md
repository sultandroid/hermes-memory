# PO Payment & Chatter Tracking (Samaya Odoo)

## Finding Linked Invoices/Bills for a PO

Bills linked to a purchase order are found on `account.move` using `invoice_origin` field (contains the PO name like "P01927"):

```python
invoices = models.execute_kw(db, uid, pw, "account.move", "search_read",
    [[["invoice_origin", "=", po_name]]],
    {"fields": ["id", "name", "state", "payment_state", "amount_total", "invoice_date", "ref"]})
```

**Key field locations:**
- `payment_state` exists on **`account.move`** (not on `purchase.order`)
  - Values: `'paid'`, `'not_paid'`, `'in_payment'`, `'reversed'`
- `invoice_status` exists on `purchase.order` — values: `'no'`, `'to invoice'`, `'invoiced'`
- `billing_status` does **NOT** exist on `purchase.order`
- `payment_state` does **NOT** exist on `purchase.order`

## Reading Chatter/Messages on a PO

PO chatter messages are stored in `mail.message` model with `model='purchase.order'` and `res_id=<po_id>`:

```python
messages = models.execute_kw(db, uid, pw, "mail.message", "search_read",
    [[["model", "=", "purchase.order"], ["res_id", "=", po_id]]],
    {"fields": ["id", "subject", "body", "author_id", "message_type", "date"], "limit": 10})
```

The `author_id` returns `[id, display_name]` tuple.

Also check `mail.activity` for to-do items completed by specific users.

## PO Notes Field

The `notes` field on `purchase.order` is HTML. It often contains payment terms, delivery instructions, or requisition references. Extract text:

```python
notes = r.get("notes", "") or ""
```

## Common PO States

| State | Meaning |
|-------|---------|
| `draft` | RFQ / not yet confirmed |
| `purchase` | Confirmed purchase order |
| `done` | Fully received/invoiced |
| `cancel` | Cancelled |

## Ibrahim Shaaban — Payment Confirmation via Chatter

Ibrahim Shaaban (User ID 169, `i.shaaban@samayainvest.com`, Partner ID 5521) is the finance/settlement user on Samaya Odoo. His comments on PO chatter indicate payment status.

**Find his messages on a PO:**
```python
# First find PO ID
records = models.execute_kw(db, uid, pw, "purchase.order", "search_read",
    [[["name", "=", "P01927"]]], {"fields": ["id"]})
po_id = records[0]["id"]

# Get all messages, filter by author
messages = models.execute_kw(db, uid, pw, "mail.message", "search_read",
    [[["model", "=", "purchase.order"], ["res_id", "=", po_id]]],
    {"fields": ["id", "body", "author_id", "date"], "order": "date ASC"})
for msg in messages:
    author = msg.get("author_id", ["", ""])
    if "shaaban" in (author[1] or "").lower():
        body = msg.get("body", "") or ""
        # Check content
```

### Three Comment Types & Their Meanings

| Pattern (Arabic) | Translation | Meaning |
|---|---|---|
| `مرفق لكم صورة التحويل` | "Transfer receipt attached" | ✅ **PAID** — Payment has been transferred. Verify with bill `payment_state='paid'` if bill exists |
| `قائمة المهام تم` | "Task list done" | 🟡 **Task completed** — likely processed but may not be actual payment. Check for separate transfer receipt message |
| `يرجي ارفاق الفاتورة الضريبية` | "Please attach tax invoice" | ⏳ **Incomplete** — payment sent but waiting for supplier invoice |

**Confidence levels:**
- **"صورة التحويل" + bill `payment_state='paid'`** → Confirmed paid (green)
- **"صورة التحويل" only, no bill** → Transfer made, bill not yet created (green/yellow)
- **"قائمة المهام تم" only** → Task marked done, not necessarily paid (yellow)
- **No comment** → No action taken (white)

### Full Payment Verification Workflow

```python
def check_payment_status(models, db, uid, pw, po_name):
    """Check full payment status of a PO including chatter evidence."""
    po = models.execute_kw(db, uid, pw, "purchase.order", "search_read",
        [[["name", "=", po_name]]],
        {"fields": ["id", "amount_total", "state", "invoice_status"]})
    if not po: return None
    r = po[0]
    po_id = r["id"]

    # 1. Check invoices
    inv_paid = False
    invoices = models.execute_kw(db, uid, pw, "account.move", "search_read",
        [[["invoice_origin", "=", po_name]]],
        {"fields": ["state", "payment_state", "amount_total"]})
    for inv in invoices:
        if inv.get("payment_state") == "paid":
            inv_paid = True

    # 2. Check Ibrahim's chatter
    messages = models.execute_kw(db, uid, pw, "mail.message", "search_read",
        [[["model", "=", "purchase.order"], ["res_id", "=", po_id]]],
        {"fields": ["body", "author_id", "date"], "order": "date ASC"})

    ibrahim_transfer = False
    ibrahim_task_done = False
    for msg in messages:
        author = msg.get("author_id", ["", ""])
        if "shaaban" in (author[1] or "").lower():
            body = (msg.get("body") or "")
            if "صورة التحويل" in body:
                ibrahim_transfer = True
            elif "قائمة المهام" in body and "تم" in body:
                ibrahim_task_done = True

    # 3. Determine final status
    if inv_paid or ibrahim_transfer:
        return "paid"        # Green
    elif ibrahim_task_done:
        return "task_done"   # Yellow
    else:
        return "pending"     # White
```

## Workshop Purchasing Tracker (Daily Cron Update)

This user runs a daily purchasing tracker at 2:00 PM KSA that auto-updates from Odoo.

### Tracker File Location
```
/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Orders/2026/0000 اداريات/شراء/workshop_purchasing_tracker.xlsx
```

### Update Script
`~/.hermes/scripts/workshop_purchasing_update.py` — standalone script that:
1. Connects to Samaya Odoo via XML-RPC
2. Queries 15 POs for current price, state, invoice status
3. Checks chatter for Ibrahim Shaaban payment messages
4. Builds color-coded Excel (green=paid, yellow=task done, white=pending)
5. Adds direct links `https://samayainv.odoo.com/web#id={id}&model=purchase.order&view_type=form`

### Cron Job
- Runs daily at 14:00 KSA
- Cron ID: `502da3ee5b5c` (workshop-purchasing-tracker)
- `no_agent=True` (script-only, no LLM)
- Script path: `workshop_purchasing_update.py` under `~/.hermes/scripts/`
