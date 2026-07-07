# Batch Date Shifting for Submittal Registers

Use when user asks to shift all dates by N days (e.g., "start from June 29" instead of June 28).

## One-liner regex replace on all .py scripts

```python
import os, re
from datetime import datetime, timedelta

SCRIPTS = '/path/to/scripts'
date_pat = re.compile(r'(\d{2})/(\d{2})/(\d{4})')
N = 1  # days to shift

def shift_date(m):
    day, mon, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
    dt = datetime(year, mon, day) + timedelta(days=N)
    return dt.strftime('%d/%m/%Y')

for fname in os.listdir(SCRIPTS):
    if not fname.endswith('.py'):
        continue
    fp = os.path.join(SCRIPTS, fname)
    with open(fp, 'r') as f:
        content = f.read()
    new_content = date_pat.sub(shift_date, content)
    if new_content != content:
        with open(fp, 'w') as f:
            f.write(new_content)
        print(f'Shifted: {fname}')
```

## Then regenerate xlsx and deploy

1. Run each .py script to regenerate .xlsx
2. Copy .xlsx to OneDrive via Finder (AppleScript)
3. Check save paths — some scripts use `/tmp/{name}.xlsx`, others use `/tmp/FFE_Dated.xlsx`
4. Verify sample dates after deploy
