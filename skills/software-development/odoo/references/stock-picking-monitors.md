# Idempotent Stock-Picking Monitors (Warehouse Watchdogs)

Lesson from the Samaya factory warehouse monitor (`~/.hermes/scripts/factory_warehouse_monitor.py`).

## Problem
A "wrong warehouse" monitor flags stock pickings whose `location_dest_id` lands on a warehouse that doesn't match the PO's project. But `location_dest_id` is the **initial landing spot only** — goods are usually moved afterward via internal transfers (`FA/WH/INT/xxxxx`). A monitor keyed on `location_dest_id` alone:
- Re-flags receipts that were already corrected (transferred to the right warehouse) on every run.
- Re-posts a chatter note each time, spamming the picking.

## Fix pattern
Dedupe before re-flagging/re-posting: query the picking's chatter for an existing marker note.

```python
# stock.move has NO quantity_done — use 'quantity' (quantity_done lives on stock.move.line)
mv = models.execute_kw(DB, uid, K, 'stock.move', 'read', [move_id],
    {'fields': ['product_id', 'product_uom_qty', 'quantity',
                'location_id', 'location_dest_id', 'state']})[0]

# Dedupe: already flagged?
msgs = models.execute_kw(DB, uid, K, 'mail.message', 'search_read',
    [[['model', '=', 'stock.picking'],
      ['res_id', '=', picking_id],
      ['body', 'ilike', MARKER]]],
    {'fields': ['id'], 'limit': 1})
already_noted = bool(msgs)
```

## Critical pitfall
Match the **actual marker text already posted** on the picking, not a string you invent for the fix. In the real data the existing notes read `تأكيد مخزن المصنع:` (no brackets). If the fix searches for `[تأكيد المخزن]` (invented), it won't match the real notes and the monitor keeps re-flagging. Read the existing chatter bodies first, extract the real marker, then dedupe on that.

## Verify current stock, not the picking's destination
Trace where goods actually are via `stock.move` history or `stock.quant` — never trust `location_dest_id` on a done receipt. Example flow found in Samaya data (POs P02297/P02298, both project 244 = Samaya Factory):

```
SAMYA/IN/00195 (P02297) -> SAMYA/Stock -> FA/WH/INT/00006 -> Factory/3D Lab/Stock -> FA/WH/INT/... -> Factory
SAMYA/IN/00194 (P02298) -> SAMYA/Stock -> FA/WH/INT/00008 -> Factory/3D Lab/Stock -> ... -> Factory
```

`stock.quant` domain note: filter `[['product_id','in',ids]]` (no location constraint) returns 0 when the goods have since been consumed/moved — check `stock.move` flow rather than concluding the goods are absent.

## Odoo 18 field quirk
`stock.move` has NO `quantity_done` field. Using it in `read`/`search_read` raises `ValueError: Invalid field 'quantity_done' on model 'stock.move'`. Use `quantity` (done qty) and `product_uom_qty` (ordered qty). `quantity_done` only exists on `stock.move.line`.
