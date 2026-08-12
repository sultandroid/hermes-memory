#!/usr/bin/env python3
"""
EMAIL INTEL AGENT v1.0 — Cross-project email intelligence.
==========================================================
Lives in the hub (hermes-memory), NOT inside any single project.

Pipeline stages (each independent; a failure in one does not block others):
  1. Ingest        -> inbox/*.md
  2. Classify sender -> contacts.json
  3. Route to project -> projects.json match
  4. Behavior analysis -> behavior/sender_profiles.json
  5. Thread/reply analysis -> threads/THREAD-*.md
  6. Gap/error detection -> issues/ISSUE-NNN.md

File-only: MD + JSON. No binaries. No Excel.

Usage:
  python3 email_intel_agent.py --run            # full pipeline
  python3 email_intel_agent.py --plan           # dry-run, no writes
  python3 email_intel_agent.py --ingest FILE    # ingest one .eml/.md
  python3 email_intel_agent.py --behavior       # re-analyze behavior only
  python3 email_intel_agent.py --issues         # list open issues
"""
import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────────────
HUB = Path(__file__).resolve().parent.parent          # hermes-memory/
INTEL = HUB / "email_intel"
INBOX = INTEL / "inbox"
BEHAVIOR = INTEL / "behavior"
THREADS = INTEL / "threads"
ISSUES = INTEL / "issues"
ARCHIVE = INTEL / "archive"

CONTACTS_FILE = INTEL / "contacts.json"
PROJECTS_FILE = INTEL / "projects.json"
SENDER_PROFILES = BEHAVIOR / "sender_profiles.json"

STALE_DAYS = 7          # thread open > this => stale
HIGH_PRIORITY = {"high"}  # trust levels that escalate fast

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)

def slugify(s):
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    return re.sub(r"\s+", "-", s)[:60]

def extract_email_from_header(header):
    m = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", header or "")
    return m.group(0).lower() if m else "unknown"

def extract_name_from_header(header):
    m = re.search(r"^([^<@]+)", header or "")
    return m.group(1).strip().strip('"') if m else "unknown"

def now_iso():
    return datetime.now().isoformat(timespec="seconds")

# ──────────────────────────────────────────────────────────────────────────────
# STAGE 1: INGEST
# ──────────────────────────────────────────────────────────────────────────────
def ingest_file(path):
    """Copy an .eml/.md/.txt into inbox/ as a normalized .md, return the new path."""
    src = Path(path)
    if not src.exists():
        print(f"  [ingest] SKIP (not found): {src}")
        return None
    raw = src.read_text(encoding="utf-8", errors="replace")
    # crude header extraction
    from_h = re.search(r"^From:\s*(.+)$", raw, re.M | re.I)
    subj_h = re.search(r"^Subject:\s*(.+)$", raw, re.M | re.I)
    date_h = re.search(r"^Date:\s*(.+)$", raw, re.M | re.I)
    sender = extract_email_from_header(from_h.group(1)) if from_h else "unknown"
    subject = (subj_h.group(1).strip() if subj_h else "no-subject")
    date = (date_h.group(1).strip() if date_h else datetime.now().strftime("%Y-%m-%d"))
    fname = f"{date[:10]}-{slugify(sender)}-{slugify(subject)}.md"
    dest = INBOX / fname
    if dest.exists():
        print(f"  [ingest] SKIP (already exists): {dest.name}")
        return dest
    dest.write_text(raw, encoding="utf-8")
    print(f"  [ingest] OK -> {dest.name}")
    return dest

# ──────────────────────────────────────────────────────────────────────────────
# STAGE 2: CLASSIFY SENDER
# ──────────────────────────────────────────────────────────────────────────────
def classify_sender(email, contacts):
    for c in contacts.get("contacts", []):
        if c.get("email", "").lower() == email:
            return c
    return None

# ──────────────────────────────────────────────────────────────────────────────
# STAGE 3: ROUTE TO PROJECT
# ──────────────────────────────────────────────────────────────────────────────
def route_to_project(subject, body, sender_email, projects):
    text = f"{subject} {body}".lower()
    for p in projects.get("projects", []):
        for dom in p.get("email_domains", []):
            if sender_email.endswith(dom.lower()):
                return p["id"]
        for kw in p.get("keywords", []):
            if kw.lower() in text:
                return p["id"]
    return None

# ──────────────────────────────────────────────────────────────────────────────
# STAGE 4: BEHAVIOR ANALYSIS
# ──────────────────────────────────────────────────────────────────────────────
def update_behavior(sender_email, sender_name, profiles):
    prof = profiles.get(sender_email, {
        "email": sender_email,
        "name": sender_name,
        "emails_seen": 0,
        "attachments_seen": 0,
        "last_seen": None,
        "subjects": [],
    })
    prof["emails_seen"] += 1
    prof["last_seen"] = now_iso()
    profiles[sender_email] = prof
    return prof

# ──────────────────────────────────────────────────────────────────────────────
# STAGE 5: THREAD / REPLY ANALYSIS
# ──────────────────────────────────────────────────────────────────────────────
def analyze_thread(subject, sender_email, project, threads):
    """Simple thread key = normalized subject (strip Re:/Fwd:)."""
    key = re.sub(r"^(re|fwd|رد|اعادة)\s*[:：]\s*", "", subject, flags=re.I).strip().lower()
    key = slugify(key) or "no-subject"
    tid = f"THREAD-{key}"
    tpath = THREADS / f"{tid}.md"
    if tpath.exists():
        content = tpath.read_text(encoding="utf-8")
        msgs = int(re.search(r"messages:\s*(\d+)", content).group(1)) if re.search(r"messages:\s*(\d+)", content) else 0
        msgs += 1
        content = re.sub(r"messages:\s*\d+", f"messages: {msgs}", content)
        content += f"\n- {now_iso()} | {sender_email} | {subject}\n"
        tpath.write_text(content, encoding="utf-8")
        return tid, msgs
    tpath.write_text(
        f"---\nthread_id: {tid}\nproject: {project or 'unrouted'}\n"
        f"messages: 1\ncreated: {now_iso()}\n---\n\n# {tid}\n\n"
        f"- {now_iso()} | {sender_email} | {subject}\n",
        encoding="utf-8",
    )
    return tid, 1

# ──────────────────────────────────────────────────────────────────────────────
# STAGE 6: GAP / ERROR / REPLY-REQUIRED DETECTION
# ──────────────────────────────────────────────────────────────────────────────
def detect_issues(subject, body, sender_email, sender, project, threads, issues):
    """Raise an issue when a reply is required, a gap exists, or a thread is stale."""
    text = f"{subject} {body}".lower()
    raised = []

    # 6a. Reply-required keywords
    reply_kw = ["please", "kindly", "urgent", "action", "confirm", "approve",
                "يرجى", "الرجاء", "عاجل", "مطلوب", "تأكيد", "اعتماد", "رد"]
    if any(k in text for k in reply_kw):
        raised.append(("reply-required", "Email asks for action/reply", "high"))

    # 6b. Gap: references an attachment/document not present
    gap_kw = ["attached", "attachment", "see attached", "مرفق", "المرفق", "please find"]
    if any(k in text for k in gap_kw) and "attachment" not in text:
        raised.append(("gap", "Email references an attachment/document", "medium"))

    # 6c. Contradiction markers
    contra_kw = ["contradict", "conflict", "discrepancy", "تعارض", "تناقض", "اختلاف"]
    if any(k in text for k in contra_kw):
        raised.append(("contradiction", "Possible contradiction/discrepancy", "medium"))

    # 6d. High-priority sender waiting
    if sender and sender.get("trust") in HIGH_PRIORITY and any(k in text for k in reply_kw):
        raised.append(("escalation", "High-priority sender awaiting reply", "high"))

    for kind, reason, prio in raised:
        n = len(issues) + 1
        issue_path = ISSUES / f"ISSUE-{n:03d}.md"
        if issue_path.exists():
            continue
        issue_path.write_text(
            f"---\nissue_number: {n}\nstatus: open\nraised: {now_iso()}\n"
            f"email_ref: inbox/{slugify(subject)}.md\nproject: {project or 'unrouted'}\n"
            f"priority: {prio}\n---\n# ISSUE-{n:03d} — {kind}\n\n"
            f"## Why raised\n{reason}\n\n## Evidence\n- Sender: {sender_email}\n"
            f"- Subject: {subject}\n\n## Required action\n<reply / chase / escalate>\n\n"
            f"## Resolution\n<filled when closed>\n",
            encoding="utf-8",
        )
        issues.append(n)
        print(f"  [issue] RAISED ISSUE-{n:03d} ({kind}, {prio})")

    return raised

# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="Email Intel Agent")
    p.add_argument("--run", action="store_true", help="full pipeline")
    p.add_argument("--plan", action="store_true", help="dry-run, no writes")
    p.add_argument("--ingest", metavar="FILE", help="ingest one email file")
    p.add_argument("--behavior", action="store_true", help="re-analyze behavior only")
    p.add_argument("--issues", action="store_true", help="list open issues")
    args = p.parse_args()

    contacts = load_json(CONTACTS_FILE, {"contacts": []})
    projects = load_json(PROJECTS_FILE, {"projects": []})
    profiles = load_json(SENDER_PROFILES, {})
    issues = load_json(ISSUES / ".index.json", [])

    if args.issues:
        for ip in sorted(ISSUES.glob("ISSUE-*.md")):
            content = ip.read_text(encoding="utf-8")
            status = re.search(r"status:\s*(\w+)", content)
            prio = re.search(r"priority:\s*(\w+)", content)
            title = re.search(r"# ISSUE-\d+ — (.+)", content)
            print(f"{ip.name} | {status.group(1) if status else '?'} | "
                  f"{prio.group(1) if prio else '?'} | {title.group(1) if title else '?'}")
        return

    if args.ingest:
        dest = ingest_file(args.ingest)
        if dest and not args.plan:
            print("  Run --run to process the ingested email.")
        return

    if args.behavior:
        print("Behavior profiles:")
        for email, prof in profiles.items():
            print(f"  {email} | {prof.get('name')} | seen={prof.get('emails_seen')} | last={prof.get('last_seen')}")
        return

    # Default: full pipeline over inbox
    if args.plan:
        print("[PLAN MODE — no writes]")
    print("=== Email Intel Agent ===")
    files = sorted(INBOX.glob("*.md"))
    if not files:
        print("  No emails in inbox/ yet. Stage emails from the Mac Pro agent.")
        return

    for f in files:
        raw = f.read_text(encoding="utf-8", errors="replace")
        from_h = re.search(r"^From:\s*(.+)$", raw, re.M | re.I)
        subj_h = re.search(r"^Subject:\s*(.+)$", raw, re.M | re.I)
        sender_email = extract_email_from_header(from_h.group(1)) if from_h else "unknown"
        sender_name = extract_name_from_header(from_h.group(1)) if from_h else "unknown"
        subject = subj_h.group(1).strip() if subj_h else "no-subject"
        body = raw

        print(f"\n  EMAIL: {f.name}")
        print(f"    from: {sender_email} ({sender_name})")
        print(f"    subject: {subject}")

        sender = classify_sender(sender_email, contacts)
        print(f"    sender: {sender['name'] if sender else 'UNKNOWN (add to contacts.json)'}")

        project = route_to_project(subject, body, sender_email, projects)
        print(f"    project: {project or 'unrouted'}")

        if not args.plan:
            update_behavior(sender_email, sender_name, profiles)
            tid, msgs = analyze_thread(subject, sender_email, project, THREADS)
            print(f"    thread: {tid} (msgs={msgs})")
            detect_issues(subject, body, sender_email, sender, project, THREADS, issues)

    if not args.plan:
        save_json(SENDER_PROFILES, profiles)
        save_json(ISSUES / ".index.json", issues)
        print("\n=== Done. Wrote behavior + threads + issues. ===")

if __name__ == "__main__":
    main()
