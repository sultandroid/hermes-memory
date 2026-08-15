# Active MOs Report — Actual Hours + Days Since Start

How to build the factory "active manufacturing orders" report with the two
columns the user wants:
- **الساعات (Hours)** = ACTUAL hours from workorders (not expected).
- **اليوم (Days)** = days elapsed since the MO's `date_start`.

## Odoo query pattern

Fetch active MOs (progress / confirmed / to_close), then per MO sum its
workorder durations.

```python
mos = models.execute_kw(db, uid, key, 'mrp.production', 'search_read',
    [[('state', 'in', ['progress', 'confirmed', 'to_close'])]],
    {'fields': ['id', 'name', 'product_id', 'product_qty', 'state',
                'date_start', 'date_finished', 'workorder_ids',
                'x_studio_justification_1'],
     'order': 'date_start asc'})

rows = []
for m in mos:
    wos = models.execute_kw(db, uid, key, 'mrp.workorder', 'search_read',
        [[('production_id', '=', m['id'])]],
        {'fields': ['name', 'duration_expected', 'duration', 'state']})
    exp_h = sum(w.get('duration_expected') or 0 for w in wos) / 60
    act_h = sum(w.get('duration') or 0 for w in wos) / 60
    ds = m.get('date_start')
    days = (datetime.now() - datetime.fromisoformat(str(ds)[:19])).days if ds else '?'
    done_wos = sum(1 for w in wos if w.get('state') == 'done')
    rows.append([m['name'], m['product_id'][1], m['product_qty'], m['state'],
                 str(ds)[:10], days, round(exp_h, 1), round(act_h, 1),
                 f"{done_wos}/{len(wos)}",
                 (m.get('x_studio_justification_1') or '').strip()])
```

## Justification field (user-requested column)

The MO **justification** lives in Odoo on `mrp.production` as the Studio field
**`x_studio_justification_1`** (type `char`, label "justification"). Add it to the
`fields` list and read it as `m.get('x_studio_justification_1')`. It is sparsely
populated — on 15-08-2026 only 13 of 35 active MOs had a value; the rest are
blank. Do not assume it is filled; the column will be mostly empty.

## ⚠️ Pitfalls (Odoo mrp.workorder)

- **`duration_actual` does NOT exist.** Valid duration fields are:
  `duration_expected` (planned), `duration` (actual, minutes), `duration_unit`,
  `duration_percent`, `time_ids`. Using `duration_actual` throws
  `ValueError: Invalid field 'duration_actual'`.
- `duration` is in **minutes** → divide by 60 for hours.
- Actual hours come from `duration`, NOT `duration_expected`. An MO can be
  `to_close` with all workorders done but `duration_expected = 0` (3D print
  orders show huge actual hours like 697h, 250h, 245h).
- `date_start` may be `False` on some workorders even when production has one —
  handle with a `or 0` / `if ds` guard.

## Report format used (14-08-2026, 29 active MOs)

Table columns: الأمر | المنتج | كمية | الحالة | بدأ | **يوم** | **ساعات فعلية**
Order by `date_start asc` (oldest first). Flag outliers:
- Oldest still zero-hours (not really started) → oldest active order
- Highest actual hours → most consumed
- `confirmed` with 0h/0 workorders → not started at all

Sample rows (for a 14-08-2026 report): FA/WH/SWH/00001 = 267 days/0h (stuck);
WH/MO/00537 = 44 days/697h (highest consumption); WH/MO/00339 = 159 days/245h.

## Excel output (user preference, 15-08-2026)

The user wants this report as an **Excel file**, not a Telegram table. Build it
with openpyxl and save to
`samaya-profile/04_Financial/manufacturing_orders/active_mos_report.xlsx`.

Columns (Arabic headers): الأمر | المنتج | الكمية | الحالة | بدأ | يوم |
ساعات متوقعة | ساعات فعلية | أوامر عمل | **التبرير (Justification)**.
- State labels: progress=قيد التنفيذ, confirmed=مؤكد, to_close=للإغلاق.
- Styling: navy `1F3864` header / white bold text, freeze `A3`, auto-filter
  `A2:J{last}`.
- Highlight: red fill = stuck (≥200 days AND 0 actual hours); amber fill =
  ≥200 actual hours.
- The justification column is mostly empty (see above) — that is expected.

A working generator lives at `~/.hermes/tmp/mo_report_excel.py` (recreate if
needed; it is a one-off, not yet committed to the repo).

## Delivery

Resolved 15-08-2026: the report is a **repo Excel file** (path above), not a
daily Telegram message. Not yet scheduled as a cron — regenerate on demand.
