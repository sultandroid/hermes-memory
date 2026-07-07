import xmlrpc.client, ssl, os, re

ctx = ssl._create_unverified_context()
t = xmlrpc.client.SafeTransport(context=ctx)
url = "https://samayainv.odoo.com"
db = "peerless-tech-samaya-18-0-18447146"
login = "sultan@samayainvest.com"

env_path = os.path.expanduser("~/.config/samaya/odoo.env")
with open(env_path) as f:
    pw = dict(line.strip().split("=", 1) for line in f if "=" in line and not line.startswith("ODOO_URL") and not line.startswith("ODOO_DB") and not line.startswith("ODOO_USER"))["ODOO_API_KEY"]

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", transport=t)
uid = common.authenticate(db, login, pw, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", transport=t)

PROJECT_ID = 112
USER_ID = 151
STAGE_MFG = 697
STAGE_PROC = 39
STAGE_ONSITE = 40

print("=== Phase 2: Creating Packages ===")
packages = [
    ("01 — VIP Area", STAGE_MFG),
    ("02 — Cafeteria", STAGE_MFG),
    ("03 — Procurement", STAGE_PROC),
    ("04 — Wooden Arch (MO)", STAGE_MFG),
    ("05 — On-site Works", STAGE_ONSITE),
]

package_ids = {}
for name, stage_id in packages:
    pid = models.execute_kw(db, uid, pw, 'project.task', 'create', [{
        'name': name,
        'project_id': PROJECT_ID,
        'stage_id': stage_id,
        'parent_id': False,
        'user_ids': [(4, USER_ID)],
        'state': '01_in_progress',
        'description': '<p>Package: ' + name + '</p>',
    }])
    package_ids[name] = pid
    print("  Created: " + name + " (ID " + str(pid) + ")")

print("Package IDs: " + str(package_ids))
print("Phase 2 done")

# Phase 3
print("\n=== Phase 3: Assigning Subtasks ===")
classification = {
    "01 — VIP Area": [345, 346, 347, 2156, 348],
    "02 — Cafeteria": [339, 340, 341, 342, 343],
    "03 — Procurement": [344],
    "04 — Wooden Arch (MO)": [1489, 2155],
    "05 — On-site Works": [107],
}

for pkg_name, task_ids in classification.items():
    if pkg_name not in package_ids:
        print("  Package '" + pkg_name + "' not found, skipping")
        continue
    pkg_id = package_ids[pkg_name]
    for tid in task_ids:
        models.execute_kw(db, uid, pw, 'project.task', 'write', [[tid], {'parent_id': pkg_id}])
        print("  Moved task " + str(tid) + " to " + pkg_name)

print("Phase 3 done")

# Phase 4: Standardize Names
print("\n=== Phase 4: Standardizing Names ===")

def standardize_name(task):
    original = task['name'] or ''
    name_lower = original.lower().strip()
    mo_match = re.match(r'^(FA/WH/MO|WH/MO|FA/MO)/(\d+)\s*[-–—]\s*(.+)$', original)
    if mo_match:
        code = mo_match.group(1) + '/' + mo_match.group(2)
        title = mo_match.group(3).strip()
        title = title[0].upper() + title[1:] if title else ''
        return code + ' — ' + title
    if name_lower.startswith('manufacturing:'):
        parts = original.split('-', 1)
        if len(parts) > 1:
            code = parts[0].strip()
            title = parts[1].strip()
            return code + ' — ' + (title[0].upper() + title[1:] if title else '')
        return original
    title = original.strip()
    title = re.sub(r'\s+', ' ', title)
    title = title.replace('Rmove', 'Remove').replace('Stracture', 'Structure')
    title = title.replace('ViP-', 'VIP - ').replace('Lover', 'Louver')
    if title and title[0].islower():
        title = title[0].upper() + title[1:]
    return title

all_tasks = []
offset = 0
while True:
    batch = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
        [[['project_id', '=', PROJECT_ID], ['state', '!=', '1_canceled']]],
        {'fields': ['id', 'name'], 'order': 'id ASC', 'limit': 200, 'offset': offset})
    if not batch:
        break
    all_tasks.extend(batch)
    offset += 200

renames = []
for t in all_tasks:
    new_name = standardize_name(t)
    if new_name != t['name']:
        renames.append((t['id'], t['name'], new_name))

if renames:
    print("Renaming tasks:")
    for tid, old, new in renames:
        print("  ID " + str(tid) + ': "' + old + '" -> "' + new + '"')
    for tid, old, new in renames:
        models.execute_kw(db, uid, pw, 'project.task', 'write', [[tid], {'name': new}])
    print("Renamed " + str(len(renames)) + " tasks")
else:
    print("No renames needed")
print("Phase 4 done")

# Phase 5
print("\n=== Phase 5: Kanban Sequence ===")
seq = [("01 — VIP Area", 1), ("02 — Cafeteria", 2), ("03 — Procurement", 3), ("04 — Wooden Arch (MO)", 4), ("05 — On-site Works", 5)]
for name, seq_no in seq:
    if name in package_ids:
        models.execute_kw(db, uid, pw, 'project.task', 'write', [[package_ids[name]], {'sequence': seq_no}])
        print("  Sequence " + str(seq_no) + " -> " + name)
print("Phase 5 done")

# Phase 6
print("\n=== Phase 6: Verify ===")
active = models.execute_kw(db, uid, pw, 'project.task', 'search',
    [[['project_id', '=', PROJECT_ID], ['state', '!=', '1_canceled']]])
mains = models.execute_kw(db, uid, pw, 'project.task', 'search_count',
    [[['project_id', '=', PROJECT_ID], ['parent_id', '=', False], ['state', '!=', '1_canceled']]])
subs = models.execute_kw(db, uid, pw, 'project.task', 'search_count',
    [[['project_id', '=', PROJECT_ID], ['parent_id', '!=', False], ['state', '!=', '1_canceled']]])
print("Total: " + str(len(active)) + ", Main: " + str(mains) + ", Sub: " + str(subs))

parent_ids = list(package_ids.values())
orphans = models.execute_kw(db, uid, pw, 'project.task', 'search',
    [[['project_id', '=', PROJECT_ID], ['parent_id', '!=', False],
      ['parent_id', 'not in', parent_ids], ['state', '!=', '1_canceled']]])
if orphans:
    print("WARNING " + str(len(orphans)) + " orphan tasks: " + str(orphans))
else:
    print("No orphans")

for name, pid in package_ids.items():
    kids = models.execute_kw(db, uid, pw, 'project.task', 'search_count', [[['parent_id', '=', pid]]])
    status = "OK" if kids > 0 else "EMPTY"
    print("  " + status + " " + name + ": " + str(kids) + " subtasks")

print("\nDone!")
