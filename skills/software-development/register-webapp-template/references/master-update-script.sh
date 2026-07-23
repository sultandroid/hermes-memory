#!/bin/bash
# Master register auto-update: rebuilds and deploys ALL register web apps
# Runs after every commit via post-commit hook, and daily via cron
# Location: ~/.hermes/scripts/update-all-registers.sh

set -e

REPO_DIR="/Users/mohamedessa/aseer-museum-pm"
SERVER="u517606786@samaya-factory.com"
REMOTE_BASE="/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers"
SSH_OPTS="-o StrictHostKeyChecking=no"
SSH_PORT="65002"

echo "[$(date)] Register auto-update starting..."

# ============================================================
# 1. Lessons Learned Register (LN)
# ============================================================
echo "--- Lessons Learned (LN) ---"
MARKDOWN_LN="$REPO_DIR/03_Plans/11_Quality/lessons_learned_register.md"
APP_LN="/tmp/lessons-learned-app"
INDEX_LN="$APP_LN/index.html"

if [ -f "$MARKDOWN_LN" ]; then
    python3 << 'PYEOF'
import re, json, os, datetime

md_path = os.path.expanduser("~/aseer-museum-pm/03_Plans/11_Quality/lessons_learned_register.md")
app_path = "/tmp/lessons-learned-app/index.html"

with open(md_path) as f:
    md = f.read()

lessons = []
for line in md.split('\n'):
    if 'LL-' not in line or not line.strip().startswith('|'):
        continue
    if line.strip().startswith('| ---') or line.strip().startswith('| #'):
        continue
    parts = [p.strip() for p in line.split('|')]
    if len(parts) < 13:
        continue
    ll_id = ''
    ll_idx = -1
    for i, p in enumerate(parts):
        if p.startswith('LL-'):
            ll_id = p; ll_idx = i; break
    if not ll_id:
        continue

    def clean(s):
        s = s.replace('**', '').replace('*', '')
        s = s.replace('\u00a7', 'Section ')
        return s.strip()

    status_raw = parts[ll_idx + 9] if len(parts) > ll_idx + 9 else ''
    if '\U0001f534' in status_raw or 'Open' in status_raw:
        status = 'Open'
    elif '\U0001f7e1' in status_raw or 'In Progress' in status_raw:
        status = 'In Progress'
    elif '\U0001f7e2' in status_raw or 'Closed' in status_raw:
        status = 'Closed'
    else:
        status = status_raw.strip()

    lessons.append({
        "id": ll_id,
        "date": parts[ll_idx + 1].strip() if len(parts) > ll_idx + 1 else '',
        "source": clean(parts[ll_idx + 2]) if len(parts) > ll_idx + 2 else '',
        "category": clean(parts[ll_idx + 3]) if len(parts) > ll_idx + 3 else '',
        "rootCause": clean(parts[ll_idx + 4]) if len(parts) > ll_idx + 4 else '',
        "impact": clean(parts[ll_idx + 5]) if len(parts) > ll_idx + 5 else '',
        "correctiveAction": clean(parts[ll_idx + 6]) if len(parts) > ll_idx + 6 else '',
        "preventiveAction": clean(parts[ll_idx + 7]) if len(parts) > ll_idx + 7 else '',
        "owner": clean(parts[ll_idx + 8]) if len(parts) > ll_idx + 8 else '',
        "status": status,
        "governingPlan": clean(parts[ll_idx + 10]) if len(parts) > ll_idx + 10 else '',
        "linkedRisk": parts[ll_idx + 11].strip() if len(parts) > ll_idx + 11 else ''
    })

if not lessons:
    print("ERROR: No lessons parsed")
    exit(1)

with open(app_path) as f:
    html = f.read()

compact = json.dumps(lessons, ensure_ascii=False)
start_marker = 'const LESSONS = '
end_marker = '];'
start_idx = html.find(start_marker)
end_idx = html.find(end_marker, start_idx)
if start_idx == -1 or end_idx == -1:
    print("ERROR: LESSONS array not found")
    exit(1)

array_start = html.index('[', start_idx)
array_end = end_idx + len(end_marker)
new_html = html[:array_start] + compact + html[array_end:]

# Validate critical JS structure
if 'const lessons = LESSONS.slice()' not in new_html:
    print("ERROR: const lessons = LESSONS.slice() missing from template")
    exit(1)
if 'function filtered()' not in new_html:
    print("ERROR: function filtered() missing from template")
    exit(1)

today = datetime.datetime.now().strftime('%d %B %Y')
new_html = re.sub(r"const UPDATED = '.*?';", f"const UPDATED = '{today}';", new_html)

with open(app_path, 'w') as f:
    f.write(new_html)

print(f"Rebuilt LN: {len(lessons)} lessons, dated {today}")
PYEOF

    echo "Deploying LN..."
    scp $SSH_OPTS -P $SSH_PORT "$INDEX_LN" "$SERVER:$REMOTE_BASE/LN/index.html"
else
    echo "SKIP: LN markdown not found"
fi

# ============================================================
# 2. Risk Register
# ============================================================
echo "--- Risk Register ---"
BUILD_RISK="$REPO_DIR/06_Risk_System/webapp/build_risk.py"
if [ -f "$BUILD_RISK" ]; then
    echo "Building Risk register from source..."
    cd "$REPO_DIR/06_Risk_System/webapp"
    python3 build_risk.py 2>&1 || echo "WARNING: Risk build script failed"
    if [ -f "src/index.html" ]; then
        scp $SSH_OPTS -P $SSH_PORT "src/index.html" "$SERVER:$REMOTE_BASE/Risk/index.html"
        echo "Deployed Risk register"
    fi
else
    echo "SKIP: Risk build script not found"
fi

# ============================================================
# 3. Future registers - add new ones here
# ============================================================

# ============================================================
# Verification
# ============================================================
echo "--- Verification ---"
for reg in LN Risk; do
    CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://samaya-factory.com/build/aseer/registers/$reg/" 2>/dev/null || echo "000")
    echo "  $reg: HTTP $CODE"
done

echo "[$(date)] Register auto-update completed"
