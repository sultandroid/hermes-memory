# PO Scope Extraction from Odoo — Deliverable Audit

When auditing subcontractor deliverables, the submittal register shows what *Samaya expects* but only the signed PO shows what was *contracted*. Extract PO scope directly from Odoo to compare.

## Workflow

### Step 1: Find the Partner (Vendor)

```python
partners = M.execute_kw(DB, uid, PWD, 'res.partner', 'search_read',
    [[('name', 'ilike', 'nama')]],   # or use exact name
    {'fields': ['id','name','email','supplier_rank'], 'limit': 5})
```

If no partner found → vendor was never set up in Odoo. Strongest signal of non-engagement.

### Step 2: Find Purchase Orders

```python
pos = M.execute_kw(DB, uid, PWD, 'purchase.order', 'search_read',
    [[('partner_id', '=', partner_id)]],
    {'fields': ['id','name','date_order','amount_total','state','notes','invoice_status'],
     'limit': 10})
```

Or find by PO reference number:

```python
pos = M.execute_kw(DB, uid, PWD, 'purchase.order', 'search_read',
    [[('name', '=', 'P01167')]],
    {'fields': [...], 'limit': 5})
```

### Step 3: Extract Order Lines (Deliverable Items)

```python
lines = M.execute_kw(DB, uid, PWD, 'purchase.order.line', 'search_read',
    [[('order_id', '=', po_id)]],
    {'fields': ['id','product_id','name','product_qty','price_unit','price_subtotal']})
```

Each line represents a service/deliverable. The `name` field contains the Arabic description.

### Step 4: Parse PO Notes for Payment Milestones

PO notes often contain the payment schedule in HTML. Strip HTML to reveal deliverable milestones:

```python
import re, html
notes = po.get('notes','') or ''
clean = re.sub(r'<[^>]+>', '\n', notes)
clean = re.sub(r'\n+', '\n', clean)
clean = html.unescape(clean).strip()
# Now parse payment milestones:
# 1. First milestone - SAR X,XXX upon receiving X
# 2. Second milestone - SAR X,XXX upon Y
```

Payment milestones define what must be delivered at each stage. Compare against the submittal register to see if the PO scope is narrower.

### Step 5: Check Linked Bills

```python
bills = M.execute_kw(DB, uid, PWD, 'account.move', 'search_read',
    [[('invoice_origin', '=', 'P01167')]],
    {'fields': ['id','name','invoice_date','amount_total','state','payment_state']})
```

- `invoice_origin` = PO reference number
- `state` = 'posted' means confirmed; 'draft' means pending
- `payment_state` = 'paid' or 'not_paid'

### Step 6: Check Attachments

```python
atts = M.execute_kw(DB, uid, PWD, 'ir.attachment', 'search_read',
    [[('res_model', '=', 'purchase.order'), ('res_id', '=', po['id'])]],
    {'fields': ['id','name','datas_fname','mimetype'], 'limit': 10})
```

### Step 7: Compare PO Scope vs Register

Create a scope-split table with three columns:

| PO Line / Payment Milestone | Register Items Covered | Gap Items |
|----------------------------|----------------------|-----------|
| Safety plans (SAR 47,826) | FL-001 (partial) | FL-002 through FL-036 |
| CD approval (SAR 8,696) | FL-026 | FL-027, FL-028, FL-029 |
| Conformity cert (SAR 4,348) | — | FL-030 through FL-036 |
| Survey + as-built (SAR 20,000) | FL-032 | All coordination items |

## Concrete Worked Example: Namaa Consulting (مكتب نماء الاعمال للاستشارات الهندسيه)

### Partner Details
- Found in Odoo as a vendor
- MoC-approved via PQ-0025 (Feb 2026)
- Prequalification PQ-0096 (Jun 2026) for renovation license

### POs Found

| PO | Date | Amount | State | Scope |
|----|------|--------|-------|-------|
| P01167 | 08 Feb 2026 | SAR 70,000.01 | purchase | Fire safety plans + CD approval + conformity cert |
| P01449 | 02 Apr 2026 | SAR 23,000.00 | purchase | Surveying + as-built drawings update |

### P01167 Line Items
| Line | Description | Amount |
|------|-------------|--------|
| 1 | عمل مخططات السلامة (Fire safety plans) | SAR 47,826.09 |
| 2 | إعتماد الدفاع المدني (CD approval) | SAR 8,695.65 |
| 3 | شهادة مطابقة الاعمال (Conformity cert) | SAR 4,347.83 |

### P01167 Payment Milestones (from PO Notes)
| Payment | Milestone | Amount |
|---------|-----------|--------|
| 1st | Upon receiving architectural drawings | SAR 7,000 |
| 2nd | Upon receiving the plans | SAR 24,500 |
| 3rd | After CD approval | SAR 24,500 |
| 4th | After conformity certificate | SAR 7,000 |
| 5th | After final delivery | SAR 7,000 |

### P01449 Line Items
| Line | Description | Amount |
|------|-------------|--------|
| 1 | أعمال الرفع المساحي وتحديث AS-BUILT | SAR 20,000 |

### P01449 Bills
| Bill | Date | Amount | Status |
|------|------|--------|--------|
| BILL/2026/04/0099 | 22 Apr 2026 | SAR 4,600 | posted, paid |

### Scope Split Against FLS Register (36 items)

| Category | In PO | GAP |
|----------|-------|-----|
| A - FLS STRATEGY | FL-001 (partial) | FL-002, FL-003, FL-004, FL-005, FL-006 |
| B - ACTIVE FIRE PROTECTION | — | FL-007 through FL-012 (6 items) |
| C - PASSIVE FIRE PROTECTION | — | FL-013 through FL-018 (6 items) |
| D - FLS COORDINATION | — | FL-019 through FL-024 (6 items) |
| E - COMMISSIONING | FL-025, FL-026 | FL-027, FL-028, FL-029 |
| F - QA/HANDOVER | FL-032 | FL-030, FL-031, FL-033 through FL-036 |

**Result: 32 of 36 items (89%) are NOT contracted.** The POs cover only CD submission + as-built survey, not full FLS design.

### Payment Status
- P01167: 1 draft bill (SAR 7,000) — not yet paid
- P01449: 1 paid bill (SAR 4,600) — partial payment of 20% (first milestone)

## Key Signals

| Signal | Meaning |
|--------|---------|
| No partner record in Odoo | **Not commercially engaged** — strongest indicator |
| Partner exists but POs in draft/purchase with no bills | **Engaged but work not yet started** |
| POs in 'purchase' state with paid bills | **Work has started** — check scope vs register |
| PO scope is a subset of register | **Partial engagement** — additional PO needed for full scope |
| No POs at all + task in 'Initiation' | **Stuck pre-award** — need to onboard commercially |
