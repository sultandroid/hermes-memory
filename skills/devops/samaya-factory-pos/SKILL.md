---
name: samaya-factory-pos
title: Samaya Factory — PO Reports & Cashout
description: Build, update, and maintain Samaya Factory purchase order reports (cashout, POs not received) from Odoo 18 data.
triggers:
  - User says "update the POs report" or "update cashout report" for Samaya Factory
  - User asks about Factory POs, credit suppliers, or cash requirements
  - User says "report by project" or "group by project" — build the per-project-group report using vendor reference
  - User provides a هام file to cross-check against Odoo
  - User provides a supplier account statement PDF (Saba Najd, Mada Aljezera, etc.)
  - User mentions "vendor reference" or "partner_ref" for project grouping
---

# Samaya Factory — PO Reports & Cashout

## Data Source
Odoo 18 at `samayainv.odoo.com`.

### Factory Project IDs (5 projects)
| ID | Name | Notes |
|----|------|-------|
| 244 | Samaya Factory | Main factory project |
| 161 | مصنع سمايا - المدينة المنورة | Madinah factory |
| 302 | Odoo Factory Requests | Internal factory requests |
| 307 | نقل المصنع في أودوو | Factory migration project |
| 315 | Factory — Standard Template | Template project |

**Always check ALL 5 project IDs** when querying factory POs. The skill previously only tracked #244, missing ~35 POs from the other 4 projects.

## SSL Fix (macOS Python 3.13+)
```bash
SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") python3 script.py
```

## Fetching POs from Odoo
**Must fetch ALL and filter in Python** — Odoo 18 crashes on `project_id` in `search_read` domains.

```python
FACTORY_PROJECT_IDS = {161, 244, 302, 307, 315}

all_pos = call('purchase.order', 'search_read', [[]],
    {'fields': fields, 'limit': 5000, 'order': 'date_order desc'})  # ~2045 total as of Aug 2026
factory_pos = [p for p in all_pos
    if p.get('project_id') and p['project_id'][0] in FACTORY_PROJECT_IDS]
```

### Factory Supplier POs (non-factory projects)
Factory suppliers (صبا نجد, مدى الجزيرة, العمالة الخارجية, etc.) also serve other Samaya projects. When the user asks for "all factory POs", include these too — they represent factory vendor activity across the company.

```python
FACTORY_SUPPLIER_IDS = {2427, 5603, 5606, 5608, 5677, 5744, 5749, 5750, ...}
supplier_pos = [p for p in all_pos
    if p.get('project_id') and p['project_id'][0] not in FACTORY_PROJECT_IDS
    and p.get('partner_id') and p['partner_id'][0] in FACTORY_SUPPLIER_IDS]
```

As of Aug 2026: **321 factory project POs** (2,039,919.79 SAR) + **125 factory supplier POs** (469,461.32 SAR) = **446 total** (2,509,381.11 SAR).

## Filter Rules (confirmed with user)
- **Include:** All Factory POs from the هام file (or all unpaid Factory POs)
- **Include draft POs** when cross-checking a هام file — Factory draft POs from the هام list need to be included in the check even though they're not yet in `purchase`/`done` state
- **Exclude:** Zero-amount POs, credit suppliers
- **Credit suppliers** handled via periodic statements — show only balance totals, never individual POs
- Include draft/cancelled/invoiced POs if user wants them
- **هام file cross-check:** When user provides a هام file, compare every PO against Odoo. List included POs with descriptions from the file, and show excluded POs with reasons (other project, zero amount, credit supplier). Use a focused script (not the full cashout script) to avoid timeout — just fetch PO names + project_id + state + partner_id + amount_total.

### Credit Supplier Partner IDs
| Supplier | Odoo ID |
|---|---|
| مؤسسة مدى الجزيرة للتجارة (Mada Aljezera) | 2427 |
| صبا نجد- Saba Najad (1224) | 5603 |

### Credit Supplier Statement — Coverage Scope

Supplier account statements (كشف حساب) are issued to **Samaya Holding** (parent company), not just Factory project 244. This causes a gap between statement total and Factory-only Odoo POs.

| Supplier | Statement Balance (Jul 2026) | Factory Odoo POs Total | Gap Reason |
|---|---|---|---|
| صبا نجد | 158,574.27 SAR | ~30,200 SAR (4 POs) | Statement includes all Samaya projects, not just Factory |
| مدى الجزيرة | 35,564.38 SAR | ~63,188 SAR (18 POs) | Same — statement period may not align with Odoo query range |

**Correct approach:** Show the statement balance as a single line in the Credit Suppliers sheet with "Statement balance — covers all Samaya projects." Cross-reference Factory-only Odoo POs separately. Never add statement balance to the Factory cashout required column.

## Report by Project Group (from Vendor Reference)

When the user asks to organize Factory POs **by project** (not by Odoo project ID), extract the project name from the **vendor reference** (`partner_ref` / `partner_ref` field on each PO). This field contains descriptive text like "Jalal & Jamal - Jabal Omer - طلب شراء دهانات" — the project name is embedded at the start.

### Extraction approach

Use regex classification, **not** an Odoo project field. The `partner_ref` text is free-form but follows patterns:

```python
import re
def classify_ref(ref):
    ref = (ref or '').strip()
    if not ref: return 'غير محدد / Unspecified'
    patterns = [
        (r'Jalal.*(?:Jabal Omer|جبل عمر)', 'Jalal & Jamal - Jabal Omer'),
        (r'Maalim.*(?:Jabal Omer|جبل عمر)', 'Maalim Al-Haramein - Jabal Omer'),
        (r'متاجر الغمامة', 'متاجر الغمامة'),
        (r'متجر الهدايا.*(?:معالم الحرمين|جبل عمر)', 'متجر الهدايا - معالم الحرمين'),
        (r'متحف عسير', 'متحف عسير الإقليمي'),
        (r'متحف القرآن|القران الكريم', 'متحف القرآن الكريم'),
        (r'متحف خير الخلق', 'متحف خير الخلق'),
        (r'متحف الغمامة', 'متحف الغمامة'),
        (r'متحف معالم المسجد الحرام|معالم المسجد الحرام', 'متحف معالم المسجد الحرام'),
        (r'زمزم|Zamzam', 'Zamzam - متحف زمزم'),
        (r'هدايا طيبه', 'متجر هدايا طيبة'),
        (r'غار حراء|المركز الإعلامي|حراء', 'المركز الإعلامي - حراء'),
        (r'جبل عمر', 'جبل عمر (عام)'),
        (r'المصنع\s*-?\s*(?:كشف|مستلزمات|مواد|طلب|جلفزات|مصاريف)?', 'المصنع (تشغيلي)'),
        (r'مصاريف بدل اعاشة|بدل اعاشة|مصاريف تشغيلية|مصروفات الإعاشة', 'مصاريف تشغيلية'),
        (r'عمالة خارجية', 'عمالة خارجية'),
        (r'مدفوع من العهده|مدفوع م العهده|مدفوعه', 'عهدة إبراهيم'),
        (r'Expenses Statement', 'مصاريف تشغيلية'),
        (r'Outsorce|عمالة', 'عمالة خارجية'),
    ]
    for pat, label in patterns:
        if re.search(pat, ref, re.UNICODE):
            return label
    return 'أخرى / Other'
```

### Report structure

- **Sheet 1: By Project** — one row per project group showing: unpaid count, unpaid total, bill-paid, chatter-paid, credit supplier allocation (مدى / صبا), and **Total Needed** (unpaid + credit suppliers for that group)
- **Sheet 2: Detail** — all POs listed under project-group headers, with credit supplier rows (مدى / صبا) per group in purple fill, showing their PO count and total

### Execution

Use the dedicated script:
```bash
SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") \
  python3 ~/.hermes/skills/devops/samaya-factory-pos/scripts/build_factory_by_project.py
```

Output path:
```
.../Samaya/Orders/2026/0000 اداريات/00 تقارير الاعمال/Samaya_Factory_PO_By_Project.xlsx
```

### Performance notes

- The by-project script uses **limited bill lookups** (reads up to 3 invoices per PO) to avoid timeout.
- With 268 Factory POs it completes in ~60-120s. If it times out, increase terminal timeout to 300s.
- The script filters out credit supplier POs from the main data and handles them via `credit_by_group` separately — this avoids double-counting.

## Excel Format
- **Sheet 1: Summary** — Navy `#1F3864` header, total cashout, credit supplier note
- **Sheet 2: POs Detail** — PO#, Vendor, Vendor Reference, Description, Date, Amount, State, Invoice, Notes
- **PO # column** — clickable hyperlink to Odoo PO page: `{ODOO_BASE}/web#id={id}&model=purchase.order`
- **Vendor Reference** — `partner_ref` field from Odoo. Place as the LAST column (not column C) — user preference
- Landscape orientation: `ws.page_setup.orientation = 'landscape'`, `ws.page_setup.fitToWidth = 1`, `ws.page_setup.fitToPage = True`
- Number format for amounts: `'#,##0.00'`
- For indented cells: use `Alignment(indent=N)` (NOT `.indent = N` — AttributeError)
- Fonts: Calibri 10pt body, Calibri 11pt bold white headers, navy background
- Yellow total rows, alternating row shading
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

**Timeout notes (running manually):**
- `new_pos_last_3_days.py` — fast, ~10s
- `update_workshop_tracker.py` — **slowest**, can take 120-300s due to Odoo chatter reads on each PO. Set terminal timeout >= 300 when running interactively.
- `build_cashout_report.py` — **depends on limit setting.** With `limit=200`: ~10-30s. With `limit=2000` (needed for full scan of 268 Factory POs): can take 120-300s because of per-PO `account.move.read()` bill lookups. Set timeout >= 300 for full scans.

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
- `references/credit-supplier-statement-update.md` — workflow for supplier statement PDF cross-referencing
- `references/factory-suppliers.md` — comprehensive factory supplier list with Odoo IDs, names, and top-10 by volume
- `references/workshop-vendors.md` — comprehensive workshop vendor name list
- `references/project-classification-patterns.md` — regex patterns to extract project group from vendor reference
- `references/inventory-system.md` — inventory tracking system design (raw materials + consumables distribution)
- `scripts/build_cashout_report.py` — reusable report builder (Factory cashout by payment status)
- `scripts/build_factory_by_project.py` — report builder grouped by project (from vendor reference), with credit supplier rows per project
- `scripts/update_workshop_tracker.py` — updates workshop purchasing tracker with Odoo payment data
- `scripts/new_pos_last_3_days.py` — detects new POs created recently
- `scripts/inventory_system.py` — inventory tracking: raw materials stock + MO consumption + consumables monthly distribution

## Pitfalls
- Odoo 18 `search_read` with `project_id` in domain crashes — always fetch all + Python filter
- Odoo 18 `['name','in',list]` domain crashes — same workaround
- **`'not in'` domain operator crashes** — `[['state','not in',['draft','cancel']]]` causes `TypeError`. Use positive list: `[['state','in',['purchase','done']]]`
- **`search_read` domain format** — wrap domain in extra list: `[domain]` not `domain`. Correct: `models.execute_kw(db, uid, apikey, model, 'search_read', [domain], {'fields': fields})`
- **`account.move.read()` for bill lookup** — use `read()` with single ID, not `search_read()`, to avoid the `'in'` operator crash
- **Per-PO bill lookup is SLOW at scale.** Strategies if it times out:
  1. Increase terminal timeout to 300s
  2. Use a **fast bill check** (read up to 3 invoices per PO) to avoid full chatter read — reduces from 300s to ~60-120s for 268 POs
  3. Batch all invoice IDs into one `search_read` (deduplicate) avoiding N individual RPC calls
  4. Skip bill lookup entirely for draft POs (no bills yet)
- **Force-include pattern:** When user says "delivered but not paid" for POs showing `invoice_status=invoiced`, use a `FORCE_INCLUDE` set checked before other filters
- **PO number typos in هام files:** Factory sometimes writes PO numbers with typos (e.g. `PO2084` instead of Odoo's `P02084`). Check both `P0` and `PO` prefixes, verify vendor reference text matches
- **هام item without PO:** When a هام item has no matching PO in Odoo (e.g. item 22: قشرة سنديان, ~9,000 SAR estimate), note it as an estimate that needs a PO created. Related POs may exist for different amounts
- **XLSX cached reads:** `read_file` on a regenerated xlsx may show stale data. Verify with openpyxl `load_workbook`, or just open the file
- OneDrive path has Arabic characters — use exact path from `read_file` output
- `search_read` limit defaults to 500 — set to 2000 to catch old POs. As of Aug 2026 there are ~2045 total POs, so use `limit=5000` to be safe.
- **`project_id` in search_read results** is a list `[id, name]` — always access via `po['project_id'][0]` for the ID. The `id` is at index 0, `name` at index 1. Never assume it's a plain int.
- **5 factory projects, not 1** — always check all 5 IDs: {161, 244, 302, 307, 315}. Using only #244 misses ~35 POs.
- **Workshop vendor list** — when filtering workshop POs by vendor name, use the comprehensive list in `references/workshop-vendors.md`
- **Script limit mismatch:** `build_cashout_report.py` hard-codes `limit=200` but needs `limit=2000`. ~268 Factory POs as of Jul 2026
- **Co-located files:** The output directory also contains `Factory-Tasks-Tracker-YYYY-MM.html` (separate system). Don't overwrite
