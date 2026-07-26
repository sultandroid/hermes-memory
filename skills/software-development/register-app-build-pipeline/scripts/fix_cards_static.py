#!/usr/bin/env python3
"""
Post-process a built register page to fix register cards.
Run after the build script to correct which card shows as "current".

Usage:
    python3 fix_cards_static.py path/to/built/index.html
"""
import json, re, sys

path = sys.argv[1]
with open(path) as f:
    html = f.read()

m = re.search(r'const RISK = ({.*?});', html, re.DOTALL)
data = json.loads(m.group(1))
current_reg = 'AVR' if data.get('is_av') else 'HSE' if data.get('is_hse') else 'DDR' if data.get('is_ddr') else 'PRR'

cards = [
    {'code': 'PRR', 'name': 'Master Risk Register', 'desc': 'Project Risk Register (PRR)',
     'doc': 'ASR-SAM-RMP-001', 'rev': 'C12',
     'href': '../' if current_reg != 'PRR' else '',
     'stats': '61 risks \u00b7 18 categories'},
    {'code': 'DDR', 'name': 'Design Discipline Register', 'desc': 'DDR',
     'doc': 'ASR-SAM-DDR-001', 'rev': 'C11',
     'href': ('../' if current_reg != 'PRR' else '') + 'DDR/',
     'stats': '79 risks \u00b7 6 categories'},
    {'code': 'HSE', 'name': 'HSE Risk Register (Fit-Out)', 'desc': 'HSE',
     'doc': 'ASR-SAM-HSE-001', 'rev': 'C11',
     'href': ('../' if current_reg != 'PRR' else '') + 'HSE/',
     'stats': '41 risks \u00b7 1 category'},
    {'code': 'AVR', 'name': 'AV & Multimedia Register', 'desc': 'AVR',
     'doc': 'ASR-SAM-AVR-001', 'rev': 'C11',
     'href': ('../' if current_reg != 'PRR' else '') + 'AV/',
     'stats': '12 risks \u00b7 6 categories'},
]

parts = []
for c in cards:
    is_cur = c['code'] == current_reg
    if is_cur:
        parts.append(f'''    <div class="reg-card reg-current">
      <div class="reg-head"><span class="reg-badge">current</span><span class="reg-code">{c['code']}</span></div>
      <div class="reg-title">{c['name']}</div>
      <div class="reg-sub">{c['desc']}  -  <span class="reg-doc">{c['doc']}</span>  -  Rev {c['rev']}</div>
      <div class="reg-stats" id="regStats"></div>
      <div class="reg-foot">{c['stats']}  -  you are here</div>
    </div>''')
    else:
        parts.append(f'''    <a class="reg-card" href="{c['href']}">
      <div class="reg-head"><span class="reg-code">{c['code']}</span></div>
      <div class="reg-title">{c['name']}</div>
      <div class="reg-sub">{c['desc']}  -  <span class="reg-doc">{c['doc']}</span>  -  Rev {c['rev']}</div>
      <div class="reg-stats">{c['stats']}</div>
      <div class="reg-foot">Open sub-register  to </div>
    </a>''')

cards_html = '  <div class="registers" id="registers">\n' + '\n'.join(parts) + '\n  </div>'
# Find the registers div by counting nested divs (not regex)
start_marker = '<div class="registers" id="registers">'
start_idx = html.find(start_marker)
if start_idx < 0:
    print("ERROR: registers div not found", file=sys.stderr)
    sys.exit(1)

depth = 0
end_idx = start_idx
while end_idx < len(html):
    if html[end_idx:end_idx+4] == '<div':
        depth += 1
        end_idx += 4
    elif html[end_idx:end_idx+6] == '</div>':
        depth -= 1
        end_idx += 6
        if depth == 0:
            break
    else:
        end_idx += 1

html = html[:start_idx] + cards_html + html[end_idx:]

with open(path, 'w') as f:
    f.write(html)

print(f"Fixed cards for {current_reg}")
