#!/usr/bin/env python3
"""
EMAIL INTEL BACKFILL IMPORTER v1.0
==================================
Reads legacy email-scan reports (email_scan_*.md) from project repos,
extracts (sender, subject) pairs from their tables, and creates
individual normalized email files in email_intel/inbox/ so the
email_intel_agent can process them.

Usage:
  python3 email_intel_backfill.py --scan-dir <path> [--dry-run]
  python3 email_intel_backfill.py --all            # scan all known project repos
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

HUB = Path(__file__).resolve().parent.parent
INTEL = HUB / "email_intel"
INBOX = INTEL / "inbox"
CONTACTS_FILE = INTEL / "contacts.json"
PROJECTS_FILE = INTEL / "projects.json"

# Known project repos on this box
KNOWN_REPOS = {
    "aseer-museum-pm": "/home/hermes/aseer-museum-pm",
    "samaya-workspace": "/home/hermes/.hermes/profiles/digitalhermes/home/samaya-workspace",
    "october129-building": "/home/hermes/.hermes/profiles/digitalhermes/home/october129-building",
    "sultan-house": "/home/hermes/.hermes/profiles/digitalhermes/home/sultan-house",
    "school-mobility-child-safety": "/home/hermes/.hermes/profiles/digitalhermes/home/school-mobility-child-safety",
    "samaya-costing-pricing": "/home/hermes/.hermes/profiles/digitalhermes/home/samaya-costing-pricing",
    "samaya-odoo-ops": "/home/hermes/.hermes/profiles/digitalhermes/home/samaya-odoo-ops",
}

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

def extract_email(s):
    m = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", s or "")
    return m.group(0).lower() if m else None

def extract_name(s):
    # strip email, keep name part
    s = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "", s or "")
    s = re.sub(r"[()]", "", s).strip()
    return s or "unknown"

def route_to_project(subject, sender, projects):
    text = f"{subject} {sender}".lower()
    for p in projects.get("projects", []):
        for dom in p.get("email_domains", []):
            if sender and sender.endswith(dom.lower()):
                return p["id"]
        for kw in p.get("keywords", []):
            if kw.lower() in text:
                return p["id"]
    return None

def parse_table_rows(lines):
    """Extract (sender, subject) pairs from markdown table rows."""
    rows = []
    for line in lines:
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        # skip header/separator rows
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue
        if all(c.lower() in ("#", "time", "sender", "subject", "type", "action", "register", "doc", "code", "from", "note", "file", "folder", "id", "ref", "description", "email", "status", "summary", "decision", "item", "detail", "metric", "count", "project", "emails", "attachments", "routed", "total", "key", "findings", "contracts", "agreements", "design", "submittals", "plans", "procedures", "ncr", "subcontractor", "prequal", "status", "reports", "procurement", "material", "board", "cg", "correspondence", "aconex", "transmittals", "registers", "updated", "filtered", "out", "items", "flagged", "user", "attention", "other", "post-scan", "additions", "new", "submissions", "contract", "eot", "key", "correspondence", "invoices", "nrs", "jim", "richards", "other", "projects", "zamzam", "jabal", "omar", "al", "galal", "gamal", "files", "routed", "onedrive", "repo", "pipeline", "ran", "document", "intake", "comms", "registers", "docs", "no", "new", "git", "changes", "processed", "existing", "files", "without", "modifications", "filtered", "out", "non-project", "erp", "pos", "salary", "leave", "tickets", "visa", "sharepoint", "link", "notifications", "saudi", "wood", "expo", "cityscape", "global", "fjdynamics", "webinar", "n8n", "mcp", "server", "rhino3dzine", "3dxtch", "roboze", "ops", "car", "requests", "rest", "house", "technician", "transport", "power", "automate", "reminders", "cognito", "forms", "instagram", "visitor", "registration", "metric", "count", "total", "emails", "scanned", "project-critical", "identified", "non-project", "filtered", "attachments", "extracted", "routed", "to", "project", "folders", "aconex", "transmittals", "info", "only") for c in cells if c):
            continue
        rows.append(cells)
    return rows

def find_sender_subject(cells, contacts):
    """Given a table row, find the sender and subject cells by header position."""
    # 1. Look for a cell that matches a known contact name/email
    for c in cells:
        c_lower = c.lower()
        for ct in contacts.get("contacts", []):
            if ct.get("email", "").lower() in c_lower or ct.get("name", "").lower() in c_lower:
                return c, None  # subject resolved later
    # 2. Look for an email address
    for c in cells:
        if extract_email(c):
            return c, None
    # 3. Look for a name-like cell (letters, no long numbers, not a doc code)
    for c in cells:
        if re.search(r"[A-Za-z\u0600-\u06FF]{3,}", c) and not re.search(r"\d{4,}", c) and len(c) < 40:
            # skip pure doc-code cells
            if re.search(r"(MOC|ZD|PQ|IR|NCR|SI|RFI|LT|INV|SIC|CGP|WTRAN|ZAM|ASR|NC-|PRR|DDR)", c, re.I):
                continue
            # skip folder-path cells (e.g. "00_Contracts/", "`01_Registers/x.md`", "02.1_Project_Execution_Plan/")
            if re.search(r"`", c) or re.search(r"/", c) or re.search(r"\d{2}[._][A-Za-z_]+", c):
                continue
            # skip date-like cells (e.g. "06-Aug", "11:40", "2026-08-06")
            if re.search(r"\d{1,2}-[A-Za-z]{3}", c) or re.search(r"\d{1,2}:\d{2}", c) or re.search(r"\d{4}-\d{2}-\d{2}", c):
                continue
            # skip numeric-count cells (e.g. "11 files", "57 files", "48 files")
            if re.fullmatch(r"[\d\s,.-]+(files?|emails?|attachments?|docs?)?", c.strip(), re.I):
                continue
            # skip common non-sender values (type/status/action cells)
            if c.lower() in ("time", "meeting", "hvac", "submittal", "submittal request",
                             "progress report", "info only", "info", "logged", "duplicate",
                             "routed", "appended", "added", "action item", "action items",
                             "pending", "review", "awaiting", "closed", "approved", "rejected",
                             "revise", "resubmit", "no att", "no attachments", "aconex",
                             "transmittal", "info", "only", "ncr", "invoice", "rfq", "sow",
                             "contract", "agreement", "plan", "report", "letter", "email",
                             "cg", "nrs", "ace", "moc", "zd", "pq", "ir", "si", "rfi", "lt",
                             "inv", "weekly", "daily", "status", "update", "submission",
                             "design", "procurement", "material", "meeting / workshop",
                             "minutes of meeting", "drawing update", "audit report",
                             "plan submission", "design package", "site instruction",
                             "compliance report", "risk / status", "design coordination",
                             "supplier inquiry", "marketing", "filtered out", "none",
                             "no project-critical", "no emails", "no action", "—", "-"):
                continue
            return c, None
    return None, None

def resolve_subject(cells, sender):
    """Pick the subject cell: the longest cell that isn't the sender."""
    best = None
    for c in cells:
        if c == sender:
            continue
        if len(c) > (len(best) if best else 0):
            best = c
    return best

# Sections whose table rows are NOT real emails (skip them)
NON_EMAIL_SECTIONS = [
    "filtered out", "files routed", "registers updated", "aconex transmittal",
    "summary", "key findings", "items flagged", "items requiring", "other projects",
    "repo pipeline", "post-scan additions", "invoices", "nrs", "other",
    "filtered", "routed to onedrive", "files routed to onedrive", "registers",
    "pipeline", "aconex", "transmittals",
]

def process_scan_file(path, projects, contacts, dry_run):
    """Extract emails from one email_scan_*.md file, section-aware."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()
    extracted = []
    current_section = ""
    for line in lines:
        # track current section heading
        if line.startswith("#"):
            current_section = line.lstrip("#").strip().lower()
            continue
        if not line.strip().startswith("|"):
            continue
        # skip rows in non-email sections
        if any(s in current_section for s in NON_EMAIL_SECTIONS):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        # skip header/separator rows
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue
        # skip rows marked as filtered/marketing/non-project in ANY column
        row_text = " ".join(cells).lower()
        if any(k in row_text for k in ["filtered out", "marketing", "non-project", "newsletter", "commercial sales"]):
            continue
        sender, _ = find_sender_subject(cells, contacts)
        if not sender:
            continue
        subject = resolve_subject(cells, sender)
        if not subject:
            continue
        # skip obvious non-email rows
        if "aconex" in sender.lower() or "transmittal" in subject.lower():
            continue
        if any(k in subject.lower() for k in ["filtered out", "non-project", "marketing", "newsletter"]):
            continue
        # skip pure-numeric / summary rows
        if re.fullmatch(r"[\d\s,.-]+(files?|emails?|attachments?)?", subject.strip(), re.I):
            continue
        if re.fullmatch(r"[\d\s,.-]+", subject.strip()):
            continue
        # skip folder-path rows
        if re.search(r"(^|/)\d{2}_[A-Za-z_/]+", subject) or re.search(r"\d{2}_[A-Za-z_]+", subject):
            continue
        # skip summary-metric rows
        if re.search(r"(total|scanned|identified|extracted|routed|filtered)\b.*\d", subject, re.I):
            continue
        # skip header-ish cells
        if subject.lower() in ("subject", "sender", "type", "action", "note", "summary", "source", "status", "email", "doc", "file", "folder", "id", "ref", "description", "from", "code", "detail", "item", "metric", "count", "project", "total", "key", "findings", "other", "new", "submissions", "contract", "eot", "correspondence", "invoices", "registers", "updated", "filtered", "out", "items", "flagged", "user", "attention", "aconex", "transmittals", "info", "only", "no", "attachments", "routed", "files", "routed", "onedrive", "repo", "pipeline", "ran", "document", "intake", "comms", "docs", "git", "changes", "processed", "existing", "without", "modifications", "none", "no", "project-critical", "emails", "in", "the", "last", "6h", "scanned", "identified", "non-project", "filtered", "extracted", "to", "project", "folders", "aconex", "transmittals", "info", "only"):
            continue
        extracted.append({"sender": sender, "subject": subject})
    return extracted

def write_inbox_email(sender, subject, project, source_file, dry_run):
    """Write a normalized email file to inbox/."""
    sender_email = extract_email(sender)
    sender_name = extract_name(sender)
    # Use name as identifier when no email present (legacy scans often lack emails)
    ident = sender_email or sender_name or "unknown"
    date = datetime.now().strftime("%Y-%m-%d")
    fname = f"{date}-{slugify(ident)}-{slugify(subject)}.md"
    dest = INBOX / fname
    if dest.exists():
        return None
    content = (
        f"From: {sender_name} <{sender_email or 'no-email'}>\n"
        f"Subject: {subject}\n"
        f"Date: {date}\n"
        f"Project: {project or 'unrouted'}\n"
        f"Source: {source_file}\n"
        f"Status: backfilled\n\n"
        f"Backfilled from legacy email scan report. Original sender: {sender}\n"
        f"Subject: {subject}\n"
    )
    if not dry_run:
        dest.write_text(content, encoding="utf-8")
    return dest

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--scan-dir", help="scan a specific repo dir for email_scan_*.md")
    p.add_argument("--all", action="store_true", help="scan all known project repos")
    p.add_argument("--dry-run", action="store_true", help="no writes")
    args = p.parse_args()

    projects = load_json(PROJECTS_FILE, {"projects": []})
    contacts = load_json(CONTACTS_FILE, {"contacts": []})

    # collect scan files
    scan_files = []
    if args.scan_dir:
        d = Path(args.scan_dir)
        scan_files = sorted(d.rglob("email_scan_*.md"))
    elif args.all:
        for repo, path in KNOWN_REPOS.items():
            d = Path(path)
            if d.exists():
                scan_files.extend(sorted(d.rglob("email_scan_*.md")))
    else:
        print("Specify --scan-dir <path> or --all")
        sys.exit(1)

    if not scan_files:
        print("No email_scan_*.md files found.")
        return

    print(f"Found {len(scan_files)} email scan files.")
    total_emails = 0
    new_contacts = 0
    for sf in scan_files:
        emails = process_scan_file(sf, projects, contacts, args.dry_run)
        if not emails:
            continue
        print(f"\n  {sf.name}: {len(emails)} emails")
        for em in emails:
            project = route_to_project(em["subject"], em["sender"], projects)
            dest = write_inbox_email(em["sender"], em["subject"], project, sf.name, args.dry_run)
            if dest:
                total_emails += 1
                print(f"    + {dest.name} [{project or 'unrouted'}]")
            # add unknown senders to contacts
            sender_email = extract_email(em["sender"])
            if sender_email and not any(c.get("email") == sender_email for c in contacts.get("contacts", [])):
                contacts["contacts"].append({
                    "email": sender_email,
                    "name": extract_name(em["sender"]),
                    "role": "unknown",
                    "project": project,
                    "trust": "unknown",
                    "reply_speed": "unknown",
                    "notes": f"Backfilled from {sf.name}",
                })
                new_contacts += 1

    if not args.dry_run:
        save_json(CONTACTS_FILE, contacts)
        print(f"\n=== Done. {total_emails} emails written to inbox/, {new_contacts} new contacts added. ===")
    else:
        print(f"\n=== DRY RUN. Would write {total_emails} emails, add {new_contacts} contacts. ===")

if __name__ == "__main__":
    main()
