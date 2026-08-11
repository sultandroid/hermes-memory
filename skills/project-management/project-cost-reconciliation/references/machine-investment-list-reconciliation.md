# Machine / Equipment Investment List Reconciliation

Pattern for verifying a claimed total in a feasibility-study machine/equipment
list (e.g. Altamioz "طلبات_الدراسة مصنع جديد" workbooks) and flagging the
per-unit vs line-total ambiguity.

## The core ambiguity: Qty × Price vs Price-as-line-total

A machine list has columns `Qty | Estimate Price`. The grand total may be built
either way:

- **Price column summed only** (line-total semantics) — each price is the total
  for that line regardless of qty.
- **Price × Qty summed** (per-unit semantics) — each price is per machine.

These differ hugely when qty > 1. Always test BOTH before accepting a total.

## Verification recipe (openpyxl)

1. **Read the total cell's formula** with `data_only=False` to see exactly which
   rows/columns it sums. Don't trust the displayed number.
   ```python
   ws = wb['المعتمد في الدراسة']
   for r in ws.iter_rows(min_row=1, max_row=92):
       if any('الإجمالي' in str(v) if v else False for v in [c.value for c in r]):
           print([c.value for c in r])  # shows =G5+G6+... formula
   ```
2. **Recompute the formula range** with `data_only=True`:
   ```python
   tot = sum(ws.cell(row=r, column=7).value
             for r in range(5, 91)
             if isinstance(ws.cell(row=r, column=7).value, (int, float)))
   ```
3. **Compute the alternative** (price × qty) and compare. If they diverge, the
   sheet is internally inconsistent about semantics.
4. **Check the formula's start row** — a formula that starts at row N may be
   silently excluding existing/legacy machines above it. Compare against the
   source sheet's department totals to find the gap.

## What to report

- State whether the claimed total is **arithmetically correct** (it usually is —
  the formula sums what it sums).
- Flag the **semantic risk**: if qty>1 lines look like per-unit prices, the true
  capex is far higher than the stated total. List the worst offenders (qty ×
  price) explicitly.
- Flag **inconsistent treatment of "Exist" machines**: some depts exclude them
  (new-investment-only), others include them. Ask whether the study covers new
  machines only or the full installed base.
- Offer a per-line reconciliation table (qty × price vs line-total, flagging
  each qty>1 line) as the deliverable back to the requester.

## Example (Madinah Factory, 2026-08)

- Approved sheet total cell = `=G5+G6+...+G90` (price column only, 68 rows) = **7,827,351** — arithmetically correct.
- Source `Machine List` dept totals = **10,087,351** → gap **2,260,000** = existing
  wood machines (Homage 700k, CNC Drilling 450k, Edge banding 380k, CNC Panel Saw
  400k, Table Saw/Planner/Thicknesser/Spindle/BandSaw/pvc ≈ 330k) excluded by the
  formula's start row.
- If qty>1 lines are per-unit, true total ≈ **219.6M** (Concrete 3D printer 2×1M,
  35 small 3D printers @105k = 3.675M, 5 spraying machines @180k, etc.).
- Two lines (Roller conveyor qty 700 @150k, Hand/Power tools qty 200 @500k) are
  clearly line-totals, not per-unit — proving the sheet mixes both semantics.
