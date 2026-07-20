#!/bin/bash
# Auto-update Lessons Learned web app from repo markdown
# Runs daily via cron. Reads the markdown, rebuilds index.html, deploys.

set -e

REPO="/Users/mohamedessa/aseer-museum-pm"
MARKDOWN="$REPO/03_Plans/11_Quality/lessons_learned_register.md"
APP="/tmp/lessons-learned-app"
INDEX="$APP/index.html"
SERVER="u517606786@samaya-factory.com"
REMOTE_PATH="/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/LN/index.html"
SSH_OPTS="-o StrictHostKeyChecking=no"
SSH_PORT="65002"

echo "[$(date)] Lessons Learned auto-update starting..."

# 1. Verify markdown exists
if [ ! -f "$MARKDOWN" ]; then
    echo "ERROR: Markdown file not found at $MARKDOWN"
    exit 1
fi

# 2. Parse lessons from markdown and rebuild index.html
# The app template is at $APP/index.html — we need to update the LESSONS array
# Strategy: extract the data rows from the markdown table and rebuild the JS array

python3 << 'PYEOF'
import re, json, os

md_path = os.path.expanduser("~/aseer-museum-pm/03_Plans/11_Quality/lessons_learned_register.md")
app_path = "/tmp/lessons-learned-app/index.html"

with open(md_path, "r") as f:
    md = f.read()

# Parse the lessons table - find rows with LL- pattern
lessons = []
for line in md.split('\n'):
    if 'LL-' not in line:
        continue
    # Only process pipe-delimited table rows
    if not line.strip().startswith('|'):
        continue
    # Skip header/separator rows
    if line.strip().startswith('| ---') or line.strip().startswith('| #'):
        continue
    
    parts = [p.strip() for p in line.split('|')]
    # Table rows have leading/trailing empty strings from pipe syntax
    # Expected: ['', '#', 'LL-ID', 'Date', 'Source', 'Category', 'RootCause', 'Impact', 'Corrective', 'Preventive', 'Owner', 'Status', 'GovPlan', 'LinkedRisk', '']
    if len(parts) < 13:
        continue
    
    # Find the LL-ID in the parts
    ll_id = ''
    ll_idx = -1
    for i, p in enumerate(parts):
        if p.startswith('LL-'):
            ll_id = p
            ll_idx = i
            break
    
    if not ll_id:
        continue
    
    # Map status emoji to text
    status_raw = parts[ll_idx + 9] if len(parts) > ll_idx + 9 else ''
    if '🔴' in status_raw or 'Open' in status_raw:
        status = 'Open'
    elif '🟡' in status_raw or 'In Progress' in status_raw:
        status = 'In Progress'
    elif '🟢' in status_raw or 'Closed' in status_raw:
        status = 'Closed'
    else:
        status = status_raw.strip()
    
    # Clean up values: remove ** markers, replace § with Section
    def clean(s):
        s = s.replace('**', '').replace('*', '')
        s = s.replace('§', 'Section ')
        return s.strip()
    
    lesson = {
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
    }
    
    lessons.append(lesson)

if not lessons:
    print("ERROR: No lessons parsed from markdown")
    exit(1)

print(f"Parsed {len(lessons)} lessons from markdown")

# Read the app template
with open(app_path, "r") as f:
    html = f.read()

# Replace the LESSONS array
lessons_json = json.dumps(lessons, indent=2, ensure_ascii=False)
# Indent each lesson on one line for compactness
compact = json.dumps(lessons, ensure_ascii=False)

# Find and replace the LESSONS array - use marker-based approach
start_marker = 'const LESSONS = '
end_marker = '];'
start_idx = html.find(start_marker)
end_idx = html.find(end_marker, start_idx)
if start_idx == -1 or end_idx == -1:
    print("ERROR: Could not find LESSONS array in template")
    exit(1)

# Find the actual start of the array (after '= ')
array_start = html.index('[', start_idx)
array_end = end_idx + len(end_marker)

new_html = html[:array_start] + compact + html[array_end:]

# Update the UPDATED constant
today = __import__('datetime').datetime.now().strftime('%d %B %Y')
new_html = re.sub(
    r"const UPDATED = '.*?';",
    f"const UPDATED = '{today}';",
    new_html
)

with open(app_path, "w") as f:
    f.write(new_html)

print(f"Updated index.html with {len(lessons)} lessons, dated {today}")
PYEOF

# 3. Deploy to server
echo "Deploying to $SERVER..."
scp $SSH_OPTS -P $SSH_PORT "$INDEX" "$SERVER:$REMOTE_PATH"

# 4. Verify
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://samaya-factory.com/build/aseer/registers/LN/)
echo "Server response: $HTTP_CODE"

if [ "$HTTP_CODE" = "200" ]; then
    echo "[$(date)] Lessons Learned auto-update completed successfully"
else
    echo "[$(date)] WARNING: Server returned $HTTP_CODE"
fi
