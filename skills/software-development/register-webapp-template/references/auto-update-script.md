# Auto-Update Script Pattern — Register Web Apps

When a register web app's data comes from a repo markdown file, wire a daily cron to rebuild and redeploy automatically.

## Script Structure

Place at `~/.hermes/scripts/update-{name}-app.sh`

```bash
#!/bin/bash
set -e

REPO="/Users/mohamedessa/aseer-museum-pm"
MARKDOWN="$REPO/03_Plans/11_Quality/lessons_learned_register.md"
APP="/tmp/lessons-learned-app"
INDEX="$APP/index.html"
SERVER="u517606786@samaya-factory.com"
REMOTE_PATH="/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/LN/index.html"
SSH_OPTS="-o StrictHostKeyChecking=no"
SSH_PORT="65002"

# Python parser reads markdown, rebuilds JSON array, replaces in HTML
python3 << 'PYEOF'
# ... parsing logic ...
PYEOF

scp $SSH_OPTS -P $SSH_PORT "$INDEX" "$SERVER:$REMOTE_PATH"
curl -s -o /dev/null -w "%{http_code}" https://samaya-factory.com/build/aseer/registers/LN/
```

## Key Parsing Logic (Python)

```python
# Find LL- rows in pipe-delimited table
for line in md.split('\n'):
    if 'LL-' not in line or not line.strip().startswith('|'):
        continue
    if line.strip().startswith('| ---') or line.strip().startswith('| #'):
        continue
    parts = [p.strip() for p in line.split('|')]
    if len(parts) < 13: continue

    # Find LL-ID by scanning parts (not hardcoded index)
    ll_idx = next(i for i, p in enumerate(parts) if p.startswith('LL-'))

    # Map emoji status
    status_raw = parts[ll_idx + 9]
    if '🔴' in status_raw: status = 'Open'
    elif '🟡' in status_raw: status = 'In Progress'
    elif '🟢' in status_raw: status = 'Closed'

    # Clean values
    def clean(s):
        s = s.replace('**', '').replace('*', '')
        s = s.replace('§', 'Section ')
        return s.strip()

    lesson = {
        "id": ll_id,
        "date": parts[ll_idx + 1],
        "source": clean(parts[ll_idx + 2]),
        # ... etc
    }

# Replace JSON array in HTML using marker-based find
start_marker = 'const LESSONS = '
end_marker = '];'
start_idx = html.find(start_marker)
end_idx = html.find(end_marker, start_idx)
array_start = html.index('[', start_idx)
array_end = end_idx + len(end_marker)
new_html = html[:array_start] + compact + html[array_end:]
```

## Cron Registration

```bash
cronjob action=create name="{name}-auto-update" \
  schedule="0 13 * * *" \
  script="update-{name}-app.sh" \
  no_agent=true
```

## Reference Implementation

`~/.hermes/scripts/update-lessons-app.sh` — working script for the Lessons Learned register.
