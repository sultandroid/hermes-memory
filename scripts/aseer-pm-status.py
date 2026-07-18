#!/usr/bin/env python3
"""Aseer PM: timestamp-based bidirectional sync.
   Compares last-modified times of PROJECT_MEMORY.md vs Odoo vs repo,
   syncs from whichever source is newer."""

import os, re, ssl, subprocess, sys, hashlib, xmlrpc.client, json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO_DIR = Path.home() / "aseer-museum-pm"
STATUS_FILE = REPO_DIR / "00_Status" / "project_status.md"
STATE_FILE = REPO_DIR / ".sync_state.json"
TODAY = date.today().isoformat()
NOW = datetime.now().strftime("%H:%M")

# ── Odoo ──
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
env = {}
with open(os.path.expanduser("~/.config/samaya/odoo.env")) as f:
    for line in f:
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k] = v
transport = xmlrpc.client.SafeTransport(context=ctx)
common = xmlrpc.client.ServerProxy(f'{env["ODOO_URL"]}/xmlrpc/2/common', transport=transport)
uid = common.authenticate(env["ODOO_DB"], env["ODOO_USER"], env["ODOO_API_KEY"], {})
models = xmlrpc.client.ServerProxy(f'{env["ODOO_URL"]}/xmlrpc/2/object', transport=transport)
DB, PW = env["ODOO_DB"], env["ODOO_API_KEY"]

STAGE_NAMES = {35: "Initiation", 36: "DD", 39: "Procurement",
               659: "Off-site Mfg", 40: "On-site", 479: "Handover", 480: "Cancelled"}

# ── Source: PROJECT_MEMORY.md ──
PM_CANDIDATES = [
    # Primary: CloudStorage (interactive shell)
    Path.home() / "Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/_Project_Memory/PROJECT_MEMORY.md",
    Path.home() / "Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/PROJECT_MEMORY.md",
    # Fallback: symlink (works in cron when CloudStorage is TCC-blocked)
    Path.home() / "OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/_Project_Memory/PROJECT_MEMORY.md",
    Path.home() / "OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/PROJECT_MEMORY.md",
    # Fallback: repo archive copy
    Path("/Users/mohamedessa/aseer-museum-pm/99_Archive/00_Project_Overview/PROJECT_MEMORY.md"),
]
pm_source = None
for p in PM_CANDIDATES:
    if p.is_file():
        pm_source = p
        break
if not pm_source:
    print("❌ ERROR: Cannot read PROJECT_MEMORY.md")
    sys.exit(1)

# ── State management ──
def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"pm_mtime": 0.0, "odoo_write_time": 0.0, "repo_mtime": 0.0}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def get_pm_mtime():
    return pm_source.stat().st_mtime

def get_odoo_mtime():
    """Get the latest write_date across all project 219 tasks."""
    try:
        tasks = models.execute_kw(DB, uid, PW, "project.task", "search_read",
            [[["project_id", "=", 219]], ["write_date"]],
            {"order": "write_date desc", "limit": 1})
        if tasks and tasks[0].get("write_date"):
            dt = datetime.fromisoformat(tasks[0]["write_date"].replace("Z", "+00:00"))
            return dt.timestamp()
    except:
        pass
    return 0.0

def get_repo_mtime():
    """Get last commit timestamp."""
    r = subprocess.run(["git", "log", "-1", "--format=%ct"], cwd=REPO_DIR,
                       capture_output=True, text=True, timeout=10)
    if r.returncode == 0 and r.stdout.strip():
        return float(r.stdout.strip())
    return 0.0

# ── Milestone text → Odoo task IDs ──
MILESTONE_MAP = [
    (r"AD ENGINEERING APPOINTED", [3067, 3215]),
    (r"Patinated Brass.*APPROVED", [3148]),
    (r"MA-0007.*APPROVED", [3148]),
    (r"Sustainability Manager APPOINTED", [2947]),
    (r"Executive MOM.*Issued", [3009]),
    (r"CG Responses Received", [2961, 2975, 3021]),
    (r"Rawasin.*EXECUTED", [3043]),
    (r"3D Render.*Code B", [2983]),
    (r"ZD-0033.*Code B", [2983]),
    (r"Lighting.*Code B", [3090]),
    (r"ZD-0056.*Code B", [3090]),
    (r"Structural.*Loading Plans", [2998]),
    (r"HVAC.*submittal", [1073, 3156]),
    (r"Stage 3 Audit", [1715]),
    (r"NRS Invoice.*4848", [3010]),
    (r"3D Scanning.*RFQ", [2878, 3015]),
    (r"Interactive Specialist", [3053, 3065]),
    (r"Life Safety.*Code C", [2891, 3005, 3050]),
    (r"Fire Pump.*NFPA", [3079, 3080]),
    (r"ITC.*Variation", [3067, 3215]),
    (r"DMP.*cycle", [2960]),
    (r"Glasbau Hahn", [3095, 3096, 3097, 3238]),
    (r"Showcase.*Code B", [3095, 3096]),
    (r"Time Schedule.*rejected", [3027, 3028]),
    (r"PL-0057.*rejected", [3027, 3028]),
    (r"Programme Extension", [3027, 3030]),
    (r"PMC weekly.*presentation", [3009]),
    (r"MS-0016.*LiDAR.*Approved", [3296]),
    (r"Method of Statement.*LiDAR", [3296]),
    (r"Studio ZNA.*fee.*approved", [3089, 3090]),
    (r"IT Engineer CVs", [3058, 3059]),
    (r"Monthly HSE Report", [2965]),
    (r"ZD-0033", [2983]), (r"ZD-0034", [2983]),
    (r"ZD-0050", [2999]), (r"ZD-0056", [3090]),
    (r"ZD-0060", [2980, 3292]),
    (r"IFC-0004", [2891, 3005]), (r"IFC-0005", [2989]),
    (r"IFC-0006", [2990]), (r"IFC-0007", [2991]),
    (r"IFC-0008", [3004]),
    (r"PL-0018", [2961]), (r"PL-0019", [3019, 3212]),
    (r"PL-0020", [3021, 3211]), (r"PL-0029", [2960]),
    (r"PL-0057", [3027, 3028, 3029, 3030, 3235]),
    (r"NRS.*drawings", [1700]), (r"NRS.*submitted", [1700]),
    (r"Daily.*Report", [3008]),
]

def find_odoo_ids(text):
    ids = set()
    for pattern, task_ids in MILESTONE_MAP:
        if re.search(pattern, text, re.IGNORECASE):
            for tid in task_ids:
                ids.add(tid)
    return sorted(ids)

# ── Sync: PROJECT_MEMORY.md → Odoo ──
def push_memory_to_odoo(state):
    """Push new milestones from PROJECT_MEMORY.md Section 0 to Odoo."""
    text = pm_source.read_text(encoding="utf-8", errors="replace")
    current_hash = hashlib.md5(text.encode()).hexdigest()
    hash_file = REPO_DIR / ".last_project_memory_hash"
    previous_hash = hash_file.read_text().strip() if hash_file.exists() else ""

    if current_hash == previous_hash:
        return state, []

    # Extract Section 0
    lines = text.split("\n")
    in_sec0 = False
    sec0_lines = []
    for line in lines:
        if re.match(r"^## 0\.", line):
            in_sec0 = True
            sec0_lines.append(line)
            continue
        if in_sec0:
            if re.match(r"^## \d+\.", line) or re.match(r"^## [A-Z]", line):
                break
            sec0_lines.append(line)
    sec0_text = "\n".join(sec0_lines)

    prev_sec0_file = REPO_DIR / ".last_project_memory_sec0.md"
    prev_sec0 = prev_sec0_file.read_text() if prev_sec0_file.exists() else ""

    hash_file.write_text(current_hash)
    prev_sec0_file.write_text(sec0_text)

    if not prev_sec0:
        return state, []

    # Diff
    old_lines = set(prev_sec0.split("\n"))
    new_lines = set(sec0_text.split("\n"))
    added = new_lines - old_lines

    odoo_updates = {}
    for line in sorted(added):
        stripped = line.strip()
        if not stripped or not stripped.startswith("|"):
            continue
        is_completed = "✅" in stripped or "🟢" in stripped
        task_ids = find_odoo_ids(stripped)
        for tid in task_ids:
            if tid not in odoo_updates:
                odoo_updates[tid] = {"reason": stripped[:100], "completed": is_completed}

    updated = 0
    for tid, info in odoo_updates.items():
        try:
            task = models.execute_kw(DB, uid, PW, "project.task", "read",
                [[tid], ["progress", "stage_id", "name"]])
            if not task:
                continue
            if info["completed"] and (task[0].get("progress") or 0.0) < 1.0:
                models.execute_kw(DB, uid, PW, "project.task", "write",
                    [[tid], {"progress": 1.0}])
                updated += 1
                print(f"  ✅ Odoo #{tid}: set 100% — {info['reason']}")
        except Exception as e:
            print(f"  ⚠️ Odoo #{tid}: {e}")

    if updated:
        state["odoo_write_time"] = datetime.now().timestamp()
    return state, odoo_updates

# ── Fetch Odoo tasks ──
def fetch_all_tasks():
    tasks = models.execute_kw(DB, uid, PW, "project.task", "search_read",
        [[["project_id", "=", 219]],
         ["id", "name", "parent_id", "stage_id", "progress", "date_deadline", "user_ids"]],
        {"order": "parent_id asc, id asc", "limit": 500})
    result = {}
    for t in tasks:
        result[t["id"]] = {
            "name": t["name"],
            "parent_id": t["parent_id"][0] if t["parent_id"] else 0,
            "stage_id": t["stage_id"][0] if t["stage_id"] else 0,
            "stage_name": STAGE_NAMES.get(t["stage_id"][0] if t["stage_id"] else 0, "Unknown"),
            "progress": t["progress"] or 0.0,
            "deadline": t["date_deadline"][:10] if t["date_deadline"] else "",
            "user_ids": t["user_ids"] or [],
        }
    return result

def build_tree(tasks):
    tree = {}
    for tid, t in tasks.items():
        pid = t["parent_id"]
        if pid not in tree:
            tree[pid] = []
        tree[pid].append(tid)
    return tree

def parent_progress(tasks, tree, pid):
    kids = tree.get(pid, [])
    if not kids:
        return tasks[pid]["progress"]
    vals = [tasks[k]["progress"] for k in kids]
    return sum(vals) / len(vals) if vals else 0.0

DISCIPLINES = {
    2945: "00 — General", 2938: "01 — Architecture", 2939: "02 — Structural",
    2940: "03 — MEP & IT", 2941: "04 — Life Safety", 2946: "05 — Projects Plans",
    3086: "06 — Model Maker", 3089: "07 — Lighting", 3092: "08 — Graphics",
    3095: "09 — Showcases", 3062: "10 — Rigging", 3063: "11 — FF&E",
    3064: "12 — Exhibition Fit-Out", 3065: "13 — Interactives", 3066: "14 — FLS",
    3067: "15 — MEP Designer", 3068: "16 — CITC", 3069: "17 — Acoustic",
    3297: "18 — 3D Viz",
}

CRITICAL_ISSUE_TASKS = {
    "SI-CG-ASEER-007": [2983, 2980],
    "IFC-0004 Life Safety Code C": [2891, 3005, 3050],
    "Fire Pump Room NFPA": [3079, 3080],
    "ITC Variation Claim": [3067, 3215],
    "DMP Cycle": [2960],
    "Glasbau Hahn Showcases": [3095, 3096, 3097, 3238],
    "Time Schedule Rejected": [3027, 3028],
    "PMC Weekly Status": [3009],
    "Programme Extension": [3027, 3030],
    "Interactive Specialist CRITICAL": [3053, 3065],
}

# ── Generate status ──
def generate_status(tasks, tree, odoo_updates):
    lines = []
    lines.append("---")
    lines.append(f"last_updated: {TODAY}")
    lines.append("owner_agent: Hermes")
    lines.append("status: active")
    lines.append(f"source: Odoo Project 219 (live sync {TODAY})")
    lines.append("---\n")
    lines.append("# Project Status — Aseer Regional Museum\n")
    lines.append("## Snapshot\n")
    lines.append("| Attribute | Value |")
    lines.append("|-----------|-------|")
    lines.append(f"| Total Tasks | {len(tasks)} |")
    completed = sum(1 for t in tasks.values() if t["progress"] >= 1.0)
    in_progress = sum(1 for t in tasks.values() if 0 < t["progress"] < 1.0)
    not_started = sum(1 for t in tasks.values() if t["progress"] == 0.0)
    lines.append(f"| Completed | {completed} |")
    lines.append(f"| In Progress | {in_progress} |")
    lines.append(f"| Not Started | {not_started} |")
    if odoo_updates:
        lines.append(f"| Odoo Updated | {len(odoo_updates)} tasks from PROJECT_MEMORY.md |")
    lines.append("")

    lines.append("## Discipline Health\n")
    lines.append("| Discipline | Progress | Stage |")
    lines.append("|-----------|----------|-------|")
    for pid, label in sorted(DISCIPLINES.items()):
        t = tasks.get(pid, {})
        pct = int(parent_progress(tasks, tree, pid) * 100)
        stage = t.get("stage_name", "?")
        icon = "✅" if pct == 100 else ("🟡" if pct >= 50 else ("🔴" if pct > 0 else "⚪"))
        lines.append(f"| {icon} {label} | {pct}% | {stage} |")
    lines.append("")

    lines.append("## Critical Active Issues\n")
    lines.append("| # | Issue | Odoo Tasks | Progress |")
    lines.append("|---|-------|------------|----------|")
    for i, (issue, task_ids) in enumerate(CRITICAL_ISSUE_TASKS.items(), 1):
        progs = [tasks.get(tid, {}).get("progress", 0) for tid in task_ids]
        avg_prog = int(sum(progs) / len(progs) * 100) if progs else 0
        names = " · ".join(tasks.get(tid, {}).get("name", f"#{tid}")[:40] for tid in task_ids if tid in tasks)
        icon = "✅" if avg_prog == 100 else ("🟡" if avg_prog >= 50 else "🔴")
        lines.append(f"| {i} | {icon} {issue} | {names} | {avg_prog}% |")
    lines.append("")

    lines.append("## Recent Milestones\n")
    recent = [t for tid, t in tasks.items() if t["progress"] >= 1.0 and t["parent_id"] != 0]
    if recent:
        for t in recent[:10]:
            lines.append(f"- ✅ **{t['name'][:80]}**")
    else:
        lines.append("- No tasks at 100%")
    lines.append("")

    lines.append("## Deadlines\n")
    lines.append("| Task | Deadline | Progress |")
    lines.append("|------|----------|----------|")
    now = date.today()
    deadline_tasks = [(tid, t) for tid, t in tasks.items() if t["deadline"] and t["progress"] < 1.0]
    deadline_tasks.sort(key=lambda x: x[1]["deadline"])
    for tid, t in deadline_tasks[:15]:
        dl = t["deadline"]
        try:
            delta = (date.fromisoformat(dl) - now).days
            flag = "🔴 OVERDUE" if delta < 0 else ("🟡 Due soon" if delta <= 3 else "📅")
        except:
            flag = "📅"
        lines.append(f"| {t['name'][:60]} | {dl} {flag} | {int(t['progress']*100)}% |")
    lines.append("")

    if odoo_updates:
        lines.append("## Odoo Updates (from PROJECT_MEMORY.md)\n")
        lines.append("| Odoo ID | Task | Action |")
        lines.append("|---------|------|--------|")
        for tid, info in sorted(odoo_updates.items()):
            tname = tasks.get(tid, {}).get("name", "?")
            action = "✅ Set 100%" if info["completed"] else "📝 Referenced"
            lines.append(f"| {tid} | {tname[:60]} | {action} |")
        lines.append("")

    lines.append("---")
    lines.append(f"*Auto-generated {TODAY} {NOW} — {len(tasks)} tasks synced*")
    return "\n".join(lines)

# ── Main ──
def main():
    state = load_state()
    pm_mtime = get_pm_mtime()
    odoo_mtime = get_odoo_mtime()
    repo_mtime = get_repo_mtime()

    print(f"📋 **Aseer PM Sync — {TODAY} {NOW}**")
    print(f"📁 Repo: github.com/sultandroid/aseer-museum-pm\n")
    print(f"🕐 **Timestamps:**")
    print(f"  📄 PROJECT_MEMORY.md: {datetime.fromtimestamp(pm_mtime).strftime('%Y-%m-%d %H:%M')}")
    print(f"  🗄️  Odoo last change:  {datetime.fromtimestamp(odoo_mtime).strftime('%Y-%m-%d %H:%M') if odoo_mtime > 1 else 'N/A'}")
    print(f"  📁 Repo last commit:  {datetime.fromtimestamp(repo_mtime).strftime('%Y-%m-%d %H:%M') if repo_mtime > 1 else 'N/A'}")
    print("")

    odoo_updates = []

    # Direction 1: PROJECT_MEMORY.md newer than last Odoo push → push to Odoo
    if pm_mtime > state.get("odoo_write_time", 0):
        print("**→ Direction: PROJECT_MEMORY.md → Odoo** (memory file is newer)")
        state, odoo_updates = push_memory_to_odoo(state)
        if odoo_updates:
            print(f"✅ Pushed {len(odoo_updates)} milestones to Odoo")
        else:
            print("ℹ️ No new milestones to push")
    else:
        print("**→ Direction: Odoo → Repo** (Odoo is newer or equal)")

    # Direction 2: Odoo newer than last repo commit → regenerate repo status
    if odoo_mtime > repo_mtime or odoo_updates:
        print("\n**Regenerating repo status from Odoo...**")
        tasks = fetch_all_tasks()
        tree = build_tree(tasks)
        content = generate_status(tasks, tree, odoo_updates)

        old_content = STATUS_FILE.read_text() if STATUS_FILE.exists() else ""
        if old_content == content:
            print("ℹ️ Status unchanged — no push needed.")
        else:
            STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
            STATUS_FILE.write_text(content)
            subprocess.run(["git", "add", str(STATUS_FILE)], cwd=REPO_DIR, check=True)
            subprocess.run(["git", "commit", "-m", f"Update status: Odoo sync {TODAY}"], cwd=REPO_DIR, check=True)
            pushed = False
            for branch in ["main", "master"]:
                r = subprocess.run(["git", "push", "origin", branch], cwd=REPO_DIR, capture_output=True, text=True)
                if r.returncode == 0:
                    pushed = True
                    break
            print(f"{'✅ Pushed to GitHub' if pushed else '❌ Push failed'}")
    else:
        print("ℹ️ Repo is up to date with Odoo.")

    # Save state
    state["pm_mtime"] = pm_mtime
    state["repo_mtime"] = get_repo_mtime()
    save_state(state)

    # Summary
    tasks = fetch_all_tasks()
    print(f"\n📊 **Summary:** {len(tasks)} tasks · "
          f"✅ {sum(1 for t in tasks.values() if t['progress']>=1.0)} done · "
          f"{sum(1 for t in tasks.values() if 0<t['progress']<1.0)} in progress · "
          f"{sum(1 for t in tasks.values() if t['progress']==0.0)} not started")

if __name__ == "__main__":
    main()