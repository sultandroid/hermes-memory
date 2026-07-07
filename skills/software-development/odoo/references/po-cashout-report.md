# PO Cashout Report (Samaya Factory — Finance Submission)

Build a consolidated cashout Excel report combining outstanding POs with credit supplier (vendor) statements for submission to the finance department.

## Report Structure

A 4-sheet Excel workbook, **Summary first**:

| Sheet | Content | Purpose |
|-------|---------|---------|
| `Summary` | CASHOUT REQUIREMENTS (POs + Credit Suppliers) + Grand Total + Exclusions | One-page for finance approval |
| `POs Detail` | Full detail per PO with receipt/invoice/bill status | Supporting detail |
| `Mada Aljezera` | Bank statement — مؤسسة مدى الجزيرة (acc 1221009) | Credit supplier reference |
| `Saba Najad` | Supplier statement — مؤسسة صبا نجد للتجارة (1224) | Credit supplier reference |

## Summary Sheet Layout

The Summary sheet is the main page finance opens. **Must include ALL cashout needs** — POs AND credit suppliers (موردين دائنين). The bank and supplier statements are vendor accounts (money Samaya owes), NOT Samaya's own cash. Never show "Bank Balance" or "Shortfall" as metrics.

## Credit Supplier Identity Mapping (Critical)

| Source | Real Entity | Arabic | What It Is |
|--------|-------------|--------|------------|
| Bank statement (acc 1221009) | **Mada Aljezera** | مؤسسة مدى الجزيرة للتجارة | Credit supplier — Samaya owes them |
| Supplier statement (1224) | **Saba Najad** | مؤسسة صبا نجد للتجارة | Credit supplier — Samaya owes them |

**⚠ NEVER label them as "Samaya Investment" or "Samaya Holding"** — these are vendor accounts.

## Data Pipeline

### 1. Query Factory POs

```python
factory_pos = odoo("purchase.order",
    [["project_id", "=", 244], ["state", "in", ["purchase", "done"]]],
    ["id", "name", "partner_id", "date_order", "receipt_status", "invoice_status", "amount_total", "state"])
```

- Project 244 = Samaya Factory
- 🔴 **Only confirmed POs**: `state in ['purchase', 'done']` — NEVER `state not in ['draft', 'cancel']` which includes sent/RFQ POs.

### 2. Fetch Vendor Bills via `invoice_origin`

```python
bill_map = {}
for i in range(0, len(po_names), 50):
    chunk = po_names[i:i+50]
    moves = odoo("account.move",
        [["invoice_origin", "in", chunk], ["state", "!=", "cancel"]],
        ["id", "name", "invoice_origin", "state", "payment_state", "amount_total", "amount_residual"])
    for m in moves:
        bill_map.setdefault(m.get("invoice_origin", ""), []).append(m)
```

**⚠ Do NOT rely on `purchase.order.invoice_ids`** — returns `False` in JSON-RPC. `invoice_origin` on `account.move` is the reliable link.

### 3. Cashout Filter Logic

```python
EXCLUDE_VENDORS = ["مدى الجزيرة", "Saba Najad", "صبا نجد"]
MIN_AMOUNT = 1000

for p in factory_pos:
    if any(x in partner_name for x in EXCLUDE_VENDORS): continue
    if rstat == "full": continue
    if total < MIN_AMOUNT: continue
    if ivst == "invoiced" and has_paid_bill: continue
    if has_paid_bill and abs(total_billed - total) < 0.05 * max(total, 1): continue
    due = max(total - total_billed, 0)
    if due == 0 and not has_paid_bill: due = total
    if due < MIN_AMOUNT: continue
    if p["name"] in PAID_OODOO: continue
    po_list.append({...})
```

### 4. Handle Known Exceptions

```python
PAID_OODOO = {"P00893", "P00744", "P01154", "P01331", "P01289",
              "P01227", "P01222", "P01023", "P00908", "P01587"}
OUTSIDE_ODOO = {"P01094"}
```

**Key:** Odoo's payment state is NOT authoritative. User knowledge outranks Odoo data.

### 5. Forced Draft POs (Odoo — user-confirmed unpaid)

Sometimes POs exist in Odoo as **draft** (not yet confirmed) but the user says they're unpaid and must appear in the cashout report. **Do NOT confuse this with outside-Odoo manual entries** — these POs DO exist in Odoo, just in draft state.

**Protocol:**
1. Query Odoo for the PO by name (any state, not just purchase/done)
2. Fetch the real vendor name and amount from the Odoo record
3. Add to `po_list` with `due = total` (no bills, since draft POs have no linked invoices)
4. Mark `rs = "Draft — Unpaid"`, `bills = "Draft PO — user confirmed unpaid"`

```python
for forced_name in ["P02025", "P02030"]:
    fr = odoo("purchase.order", [["name","=",forced_name]],
               ["name","partner_id","date_order","amount_total","state","receipt_status","invoice_status"])
    if fr:
        f = fr[0]
        fvend = f.get("partner_id",["",""]); fvend_name = fvend[1] if isinstance(fvend,(list,tuple)) else str(fvend)
        po_list.append({
            "po": f["name"], "vendor": fvend_name,
            "date": (f.get("date_order") or "")[:10],
            "total": f["amount_total"] or 0, "due": f["amount_total"] or 0,
            "rs": "Draft — Unpaid",
            "bills": "Draft PO — user confirmed unpaid"})
```

**Known instances:** P02025 (مورد مواد متنوعه, 36,030 SAR), P02030 (Outsorce Labor, 16,556 SAR).

### 6. Manual / Outside-Odoo POs

User may request POs that don't exist in Odoo at all. Add as manual entries immediately with 0 SAR and "TBD — Outside Odoo" vendor:

```python
manual_pos = [
    {"po":"P01740","vendor":"TBD — Outside Odoo","date":"","total":0,"due":0,
     "rs":"Unpaid","bills":"Manual entry — user-confirmed unpaid"},
]
po_list.extend(manual_pos)
```

**Protocol:** Query Odoo first. If not found, add to report right away. Do NOT block asking for amounts.

## Excel Construction

### ⚠ PatternFill Syntax

Installed openpyxl requires **keyword-only arguments**:

```python
# ✅ CORRECT
YELLOW = PatternFill(fill_type="solid", start_color="FFF2CC")
# ❌ WRONG — TypeError: Fill() takes no arguments
YELLOW = PatternFill("solid", fgColor="FFF2CC")
```

### Style Tokens

```python
NAVY = "1F4E79"; RED = "C00000"; AMBER = "BF8F00"
HDR_F = Font(bold=True, color="FFFFFF", size=10)
SUB_F = Font(bold=True, size=11, color=NAVY)
TITLE_F = Font(bold=True, size=16, color=NAVY)
AMT_FMT = '#,##0.00'
```

- **No emoji/icons/AI fingerprints** — use color fills
- **Calibri** font, clean professional
- **Big items (>5K SAR)** highlighted yellow

### Summary Metrics

```python
mada_bal = 40280.86; saba_bal = 88746.27
grand_total = total_due + mada_bal + saba_bal

metrics = [
    ("Outstanding POs", f"{len(po_list)} POs — {total_due:,.2f} SAR"),
    ("Credit Supplier — Mada Aljezera", f"{mada_bal:,.2f} SAR"),
    ("Credit Supplier — Saba Najad", f"{saba_bal:,.2f} SAR"),
    ("", ""),
    ("TOTAL CASHOUT REQUIRED", f"{grand_total:,.2f} SAR", RED),
]
```

## Output Path

```
/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/
Samaya/Orders/2026/0000 اداريات/00 تقارير الاعمال/
Samaya_Factory_Cashout_Report.xlsx
```

## Key Pitfalls

1. **`invoice_ids` on purchase.order unreliable** — use `account.move.invoice_origin`.
2. **Draft bills ≠ paid** — treat as outstanding unless user confirms.
3. **sent-state POs are RFQs** — Use `state in ['purchase','done']`, never `state not in ['draft','cancel']`. Known: P01814, P01816.
4. **P01587 pattern**: `total > 1K` but `due < 1K` — user considers paid.
5. **Close Excel before writing** — openpyxl corrupts open files.
6. **Float comparison** — use `abs(residual) < 0.05`.
7. **PatternFill keyword args** — `fill_type="solid", start_color="XXXXXX"`.
8. **Credit suppliers NOT Samaya's accounts** — belong in Credit Suppliers section.
9. **Outside-Odoo POs** — add immediately, don't block for amounts.
10. **Forced draft POs may exist in Odoo** — query by name with no state filter, fetch real data. Don't confuse with outside-Odoo manual entries.
11. **Odoo JSON-RPC auth needs UID lookup** — always call `common.login(db, email, key)` first to get the numeric UID. Never pass email directly as UID — that raises `ValueError: invalid literal for int()`.
