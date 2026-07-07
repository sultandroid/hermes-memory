# PO Not-Received Tracker (Samaya Factory Workshops)

Build a filtered Excel tracker of POs that are **not fully received** for Samaya Factory workshops. The overall category is "Not Fully Received" — this includes POs that are pending receipt, have no receipt recorded, or are partially received.

## 🔴 CRITICAL: Terminology — "Not Fully Received" vs "Not Received"

The user corrected this distinction explicitly. **"Not Fully Received" is the umbrella category.** Within it, there are three distinct sub-statuses:

| Live Odoo Value | Display Label | Meaning |
|----------------|--------------|---------|
| `'pending'` | **Not Received** | In progress, waiting for delivery — receipt process has started |
| `'False'` / `None` | **Not Recorded** | No receipt activity started at all — no receipt has been entered |
| `'partial'` | **Partially Received** | Some line items received, others pending |

The sheet name in Excel should be **"Not Fully Received"**, not "Not Received" (which is just one sub-status).

## 🔴 CRITICAL: Use Live Odoo API for Receipt Status — Don't Trust Export Files

The Odoo export files (.xlsx) are **stale snapshots** — receipt_status in the exports frequently shows "Not Received" when Odoo already shows "Fully Received". The user will flag this: *"why you still add lines its already fully received on the system."*

**Correct pattern: use export files for vendor/project/item descriptions ONLY, then overlay live receipt_status and state from Odoo API via JSON-RPC.**

See the "Live Status Overlay" section below for the exact query pattern.

## Data Sources + Live Odoo Overlay

### Source Files (for vendor/project/description metadata only)

Two Odoo export files at `Samaya/Orders/2026/` (organized under `06_Samaya_Factory/Odoo/`):

| File | Key Columns | Notes |
|------|-------------|-------|
| `Confirmed POs.xlsx` | Order Reference, Vendor, Total, Receipt Status, Project, Buyer, Order Deadline, Vendor Reference, Deliver To | Covers all POs across all projects |
| `Purchase Order (purchase.order) (2).xlsx` | Same + Product/Name column for item descriptions | More detailed per-line items |

## Filtering Logic (with Live Status)

Focus on **Samaya Factory** POs only — those where `Project = "Samaya Factory"` OR `Buyer = "SAMAYA WORKSHOP"`. Then overlay live Odoo data for receipt_status and state:

```python
# Step 1: Filter from export data (metadata)
is_factory = "factory" in project.lower() or "workshop" in buyer.lower()

# Step 2: Overlay live Odoo receipt_status
live = live_data.get(po_name, {})
live_rs = live.get('receipt_status', '')
live_state = live.get('state', '')

# Step 3: Apply all filters
if live_state in ('cancel', 'draft', 'sent'):      # skip drafts/cancelled
    continue
if live_rs == 'full':                                # skip fully received
    continue
if any(x in vendor.lower() for x in                  # skip excluded vendors
       ['مدى الجزيرة', 'saba najad', 'صبا نجد']):
    continue
```

## Live Status Overlay — Query Odoo for Current Receipt Status

Instead of using the export file's receipt status, query Odoo live via JSON-RPC:

```python
import requests

url = "https://samayainv.odoo.com"
db = "peerless-tech-samaya-18-0-18447146"
user = "sultan@samayainvest.com"
api_key = "<from ~/.config/samaya/odoo.env>"

# Authenticate
r = requests.post(f"{url}/jsonrpc", json={
    "jsonrpc": "2.0", "method": "call",
    "params": {"service": "common", "method": "login", "args": [db, user, api_key]},
    "id": 1
}, verify=False, timeout=15)
uid = r.json().get('result')

# Batch query by PO name (batch size ≤ 200)
po_refs = ['P01358', 'P01151', ...]  # all PO names from the export
r2 = requests.post(f"{url}/jsonrpc", json={
    "jsonrpc": "2.0", "method": "call",
    "params": {
        "service": "object", "method": "execute_kw",
        "args": [db, uid, api_key, 'purchase.order', 'search_read',
            [[['name', 'in', po_refs]]],
            {'fields': ['id', 'name', 'receipt_status', 'state', 'date_order', 'create_date']}
        ]
    },
    "id": 2
}, verify=False, timeout=30)
live_results = r2.json().get('result', [])

# Build lookup maps
po_id_map = {r['name']: r['id'] for r in live_results}
po_rs_map = {r['name']: str(r.get('receipt_status', '')) for r in live_results}
po_state_map = {r['name']: r.get('state', '') for r in live_results}
```

### State Filtering (Must Exclude Drafts)

The export file may include RFQ/draft entries. Filter them out using the live `state` field:

| state value | Meaning | Include in tracker? |
|-------------|---------|-------------------|
| `'purchase'` | Confirmed PO | ✅ Yes |
| `'done'` | Locked/Completed | ❌ No (fully processed) |
| `'draft'` | RFQ (not confirmed) | ❌ No |
| `'cancel'` | Cancelled | ❌ No |
| `'sent'` | RFQ sent to vendor | ❌ No |

```python
# Skip cancelled/draft
if live_state in ('cancel', 'draft', 'sent'):
    continue
```

### Receipt Status Mapping (Live API Values — Three Sub-Statuses)

Live Odoo `receipt_status` field uses **different values** than the export file. Map them to three distinct labels — do NOT collapse them:

| Live API Value | Export File Label | Tracker Label | Include? |
|----------------|-------------------|---------------|----------|
| `'full'` | `Fully Received` | — (removed) | ❌ No |
| `'pending'` | `Not Received` | `Not Received` | ✅ Yes — receipt started but nothing received yet |
| `'False'` (Python bool) | `(blank)` | `Not Recorded` | ✅ Yes — no receipt entered at all, needs attention |
| `'partial'` | `Partially Received` | `Partially Received` | ✅ Yes — partial receipt done |

```python
rs = str(o.get('receipt_status', ''))
if rs == 'full':
    continue  # fully received — skip
elif rs == 'pending':
    label = 'Not Received'      # receipt in progress
elif rs in ('partial', 'partially_received'):
    label = 'Partially Received' # partial
else:
    label = 'Not Recorded'      # False/None — no receipt started
```

### ⚠ Buyer ID Field Bug in JSON-RPC

The `buyer_id` field (a `res.users` many2one) causes a **search_read error** when included in the fields list through JSON-RPC:
```
TypeError: BaseModel.search_read() got multiple values for argument 'fields'
```

**Do NOT include `buyer_id` in the fields list** when using JSON-RPC `search_read`. If you need buyer info, either:
1. Query buyer info in a separate call on the `res.users` model
2. Get buyer info from the export files (which already have the display name)
3. Only query fields that are safe: `['id', 'name', 'receipt_status', 'state', 'partner_id', 'amount_total', 'date_order']`

`project_id` IS safe to query via JSON-RPC. The bug is specific to `buyer_id`.

PO numbers link directly to the purchase order form view in Samaya Odoo:

```python
# ✅ CORRECT — uses internal database ID, opens the exact PO form
odoo_id = 1358  # look this up via API
url = f"https://samayainv.odoo.com/web#id={odoo_id}&model=purchase.order&view_type=form"

# ❌ WRONG — using search= with the reference number opens a blank new PO form
```

### Step 1: Look Up Internal IDs via Odoo JSON-RPC API

Use the `purchase.order` model's `name` field (which stores the P01358 reference) to search for internal IDs:

```python
import requests

payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "object",
        "method": "execute_kw",
        "args": [
            db, uid, api_key,
            'purchase.order',
            'search_read',
            [[['name', 'in', po_refs_list]]],  # list of PO refs like ['P01358', 'P01151']
            {'fields': ['id', 'name']}
        ]
    },
    "id": 1
}
r = requests.post("https://samayainv.odoo.com/jsonrpc", json=payload, verify=False, timeout=15)
results = r.json().get('result', [])
po_map = {r['name']: r['id'] for r in results}
```

### Step 2: Build Hyperlinks in Excel

```python
odoo_id = po_id_map.get(po['po'])
if odoo_id:
    po_url = f"https://samayainv.odoo.com/web#id={odoo_id}&model=purchase.order&view_type=form"
cell.hyperlink = po_url
cell.font = Font(color="0563C1", underline="single")  # blue underlined link
```

**Fallback:** If the ID isn't found in Odoo (very rare), use the list-view search URL instead:
`https://samayainv.odoo.com/web#model=purchase.order&view_type=list&search={po_ref}`

## Excel Format

- **Sheet name**: `"Not Fully Received"` (NOT "Workshop POs" — the user corrected this)
- **Columns**: `#`, `PO#`, `Vendor`, `Items`, `Total (SAR)`, `Creation Date`, `Deadline`, `Receipt Status`, `Project`
- **Column widths**: `[5, 14, 45, 60, 14, 14, 14, 22, 40]`
- **Creation Date**: sourced from `date_order` field in live Odoo data (fallback: `create_date`)
- **Color coding by status**: Yellow (`FFF2CC`) = Not Received, Pink (`FCE4EC`) = Partially Received, Green (`E8F5E9`) = Not Recorded (blank/no receipt)
- **PO# hyperlink**: uses internal Odoo ID: `https://samayainv.odoo.com/web#id={id}&model=purchase.order&view_type=form`
- **Auto-filter** on all columns, frozen header row
- **Number format** `#,##0.00` for totals
- **Summary section**: total count, outstanding amount, breakdown by status (Not Received / Not Recorded / Partially Received)

## OneDrive Save Path

```
Samaya/Orders/2026/0000 اداريات/00 تقارير الاعمال/Samaya_Factory_Workshop_POs_Not_Received.xlsx
```

## Deduplication

Both export files may contain overlapping PO records. Merge by PO number — prefer data from `Confirmed POs.xlsx` as primary, supplement with `Product/Name` descriptions from `Purchase Order (purchase.order).xlsx`.

## ⚠ Pitfall: Stale Export Data

The export files are snapshots that can be **days or weeks old**. Receipt status frequently changes in Odoo after the export was taken. Common scenario: you filter for "Not Received" in the export, build a tracker showing 48 POs, but Odoo live data shows only 22 are actually pending — the rest were already received.

**Always verify counts:**
```python
# After building the tracker, compare:
export_count = len(export_not_received)   # 48
live_count = len(live_not_received)       # 22
# If different by 20+, the exports are stale
```

**User reaction if you miss this:** *"why you still add lines its already fully received on the system"* — direct correction. Fix by querying live receipt_status and always filtering by `state != 'cancel'` and `receipt_status != 'full'`.

## Status Legend (Live Odoo Values)

| Live API Value | Tracker Label | Meaning | Include? |
|----------------|---------------|---------|----------|
| `'pending'` | `Not Received` | PO confirmed, nothing received | ✅ Yes |
| `'full'` | `Fully Received` | All items received | ❌ Removed |
| `'False'`/`None` | `Not Recorded` | No receipt processed yet | ✅ Yes — needs attention |

## Vendor Filtering

When the user asks to exclude specific vendors, check by substring in the vendor name (lowercased):

```python
v = vendor.lower()
excluded = 'مدى الجزيرة' in v or 'saba najad' in v or 'صبا نجد' in v
```