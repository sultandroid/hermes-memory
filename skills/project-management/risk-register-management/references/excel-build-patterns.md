# Excel Build Patterns — Session-Tested

## Column Layout (must match website table)

Risk Register column order:
A=ID | B=CAT | C=RISK | D=P | E=S | F=SCORE(=D*E) | G=RATING(=IF) | H=STATUS | I=OWNER | J=TARGET | K=CAUSE | L=CONSEQUENCE | M=RESPONSE/ACTION | N=EVIDENCE

Never embed score text in RESPONSE/ACTION — scoring has dedicated columns.

## Dashboard Formula Updates (critical after layout change)

The template Dashboard is formula-driven. When Risk Register columns change, update ALL sections:

| Section | Rows | Old Col | New Col | Description |
|---------|------|---------|---------|-------------|
| Risk Matrix | 9-13 | M (Prob), N (Sev) | D, E | 5x5 count |
| By Rating | 17-20 | C | G | COUNTIF on RATING |
| By Status | 23-25 | E | H | COUNTIF on STATUS |
| Top Owners | 40-49 | F | I | COUNTIF on OWNER |
| Category Counts | 28-35 (col D-E) | B | B (unchanged) | COUNTIF on CAT — only last row changes |

Pattern:
```python
for ri in range(9,14):
    for ci in range(3,8):
        c=dash.cell(ri,ci)
        if c.value and isinstance(c.value,str) and 'Risk Register' in c.value:
            v=c.value
            v=v.replace('$M$10:$M$','$D$10:$D$').replace('$N$10:$N$','$E$10:$E$')
            v=re.sub(r'(\$10:\$[A-Z]+)\$(\d+)',lambda m: m.group(1)+'$'+str(last),v)
            c.value=v
```

NEVER write static values over these sections — the template already has complete formula-based dashboard.

## Dynamic Category Expansion

The template category table (rows 28-35) has only 8 hardcoded categories. Actual data may have more. The percentage sum will be wrong if categories are missing. Replace with a dynamic list:

```python
from collections import Counter
cat_counter = Counter(r.get('category','') for r in risks)
cat_codes = [c for c,_ in cat_counter.most_common()]

# Full category name map
CAT_NAMES = {
    'PRC':'Procurement & Supply Chain', 'COM':'Commercial & Contractual',
    'DES':'Design & Coordination',      'CON':'Construction / Site',
    'APP':'Statutory & Authority Approvals', 'SCH':'Schedule / Programme',
    'CNS':'Conservation & Collection',  'STK':'Stakeholder / CG-PMC',
    'FLS':'Fire & Life Safety',         'HSE':'Health & Safety',
    'LOG':'Logistics & Site Access',    'MEP':'MEP & Building Services',
    'OPS':'Stakeholder & Operations',   'QLT':'Quality',
    'SEC':'ICT & Security',             'SIT':'Site & Existing Conditions',
    'TCH':'Testing, Commissioning & Handover',
}

# Calculate if TOP OWNERS section needs shifting
cat_end_row = 28 + len(cat_codes)
sum_row = cat_end_row
next_free = sum_row + 2  # SUM row + gap

if next_free > 38:
    # Shift TOP OWNERS down. Must unmerge B39:C39 first.
    shift = next_free - 38
    for row in range(55, 38, -1):
        for col in range(1, 5):
            src_v = dash.cell(row, col).value
            if src_v is not None:
                setv(dash.cell(row+shift, col), src_v)
            setv(dash.cell(row, col), None)
    # Fix COUNTIF references: ,B#) -> ,B{current_row})
    for row in range(40+shift, 70):
        c = dash.cell(row, 3)
        if c.value and isinstance(c.value, str) and 'COUNTIF' in c.value:
            c.value = re.sub(r',B\d+\)$', f',B{row})', c.value)

# Write category rows
for idx, code in enumerate(cat_codes):
    row = 28 + idx
    name = CAT_NAMES.get(code, code)
    setv(dash.cell(row, 2), name)
    setv(dash.cell(row, 3), code)
    setv(dash.cell(row, 4), f"=COUNTIF('Risk Register'!$B$10:$B${last},C{row})")
    setv(dash.cell(row, 5), f'=IFERROR(D{row}/$B$5,0)')

# SUM row
setv(dash.cell(sum_row, 4), f'=SUM(D28:D{sum_row-1})')
setv(dash.cell(sum_row, 5), f'=SUM(E28:E{sum_row-1})')
```

The `E` column (percentage of total) SUM equals 100% only when ALL categories present in data are included. Dynamic expansion fixes this.

## Bar Chart Range Update

After dynamic category expansion, update the Bar chart range to match:

```python
cat_end = 28 + len(cat_codes) - 1
for ch in dash._charts:
    from openpyxl.chart import BarChart
    if isinstance(ch, BarChart):
        for s in ch.series:
            if hasattr(s.val, 'numRef') and s.val.numRef:
                s.val.numRef.f = f'Dashboard!$D$28:$D${cat_end}'
            if hasattr(s.cat, 'strRef') and s.cat.strRef:
                s.cat.strRef.f = f'Dashboard!$B$28:$B${cat_end}'
```

The Doughnut chart (risks by rating, rows 17-20) is static — no range update needed.

## Chart Cache Clearing

After formula updates, clear cached chart data so Excel recalculates from formulas on open:

```python
for ch in dashboard._charts:
    if hasattr(ch.series[0],'val') and hasattr(ch.series[0].val,'numRef') and ch.series[0].val.numRef:
        ch.series[0].val.numRef.numCache = None
    if hasattr(ch.series[0],'cat') and hasattr(ch.series[0].cat,'strRef') and ch.series[0].cat.strRef:
        ch.series[0].cat.strRef.strCache = None
```

## Variable Name Collision — #1 Bug

Never use `w` as a loop variable when `w` holds the workbook:

```python
# WRONG — will crash with 'int' object has no attribute 'save'
for col_letter,w in widths.items():
    pass
w.save(...)
```

Use distinct names: `wd`, `width_val`, etc.

Same for `s` — never use it as a loop var when it also holds a worksheet reference.

## Column Widths After Layout Change

Set explicitly based on content type:

```python
widths={'A':12,'B':8,'C':45,'D':6,'E':6,'F':7,'G':8,'H':8,'I':18,'J':12,'K':30,'L':30,'M':35,'N':30}
for cl,wd in widths.items():
    try: rr.column_dimensions[cl].width=wd
    except: pass
```

Narrow for P/S/SCORE (6-7), medium for OWNER/TARGET (12-18), wide for RISK/CAUSE/CONSEQUENCE/EVIDENCE (30-45).
