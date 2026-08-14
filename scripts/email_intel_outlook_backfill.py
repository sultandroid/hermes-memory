#!/usr/bin/env python3
"""
EMAIL INTEL OUTLOOK BACKFILL v1.0
=================================
Pulls project-relevant emails directly from the Outlook SQLite DB for a
date window and writes normalized .md files into email_intel/inbox/ so the
email_intel_agent can process them.

Usage:
  python3 email_intel_outlook_backfill.py --from 2026-04-01 --to 2026-07-15 [--dry-run]
"""
import argparse
import json
import os
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

HUB = Path(__file__).resolve().parent.parent
INTEL = HUB / "email_intel"
INBOX = INTEL / "inbox"
PROJECTS_FILE = INTEL / "projects.json"

DB = os.path.expanduser(
    "~/Library/Group Containers/UBF8T346G9.Office/Outlook/"
    "Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite"
)

# Project-relevant subject/sender patterns (Aseer + Samaya + other projects)
PROJECT_PATTERNS = [
    r"aseer", r"museum", r"moc", r"cg\.com\.sa", r"nissenrichards", r"ace",
    r"zd-\d", r"pq-\d", r"ir-\d", r"ncr", r"si-\d", r"rfi", r"lt-\d",
    r"tq-\d", r"ifc", r"inv-\d", r"zamzam", r"zam-nwc", r"jabal", r"omar",
    r"samaya", r"متحف", r"متاحف", r"عمارة", r"مصنع",
]

# Senders that are never project-relevant (marketing/ERP/notifications)
NON_PROJECT_SENDERS = [
    "erp-samaya", "erp-samaya", "sharepoint online", "microsoft power automate",
    "canonical", "leap", "extra", "3dxtch", "kopperfield", "parasoleil",
    "neko lighting", "read ai", "read assistant", "aconex notification",
    "your friends at", "eXtra", "fjdynamics", "cognito", "instagram",
    "saudi wood expo", "bluebeam", "cityscape", "visitor",
]

def slugify(s):
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    return re.sub(r"\s+", "-", s)[:60]

def extract_email(s):
    m = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", s or "")
    return m.group(0).lower() if m else None

def extract_name(s):
    s = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "", s or "")
    s = re.sub(r"[()]", "", s).strip()
    return s or "unknown"

def is_project_relevant(subject, sender):
    text = f"{subject} {sender}".lower()
    if any(np in sender.lower() for np in NON_PROJECT_SENDERS):
        return False
    return any(re.search(p, text) for p in PROJECT_PATTERNS)

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

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--from", dest="from_date", required=True)
    p.add_argument("--to", dest="to_date", required=True)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    projects = json.loads(PROJECTS_FILE.read_text(encoding="utf-8"))
    from_ts = int(datetime.strptime(args.from_date, "%Y-%m-%d").timestamp())
    to_ts = int(datetime.strptime(args.to_date, "%Y-%m-%d").timestamp())

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        SELECT Message_TimeReceived, Message_SenderList, Message_NormalizedSubject
        FROM Mail
        WHERE Message_TimeReceived >= ? AND Message_TimeReceived < ?
        ORDER BY Message_TimeReceived ASC
    """, (from_ts, to_ts))
    rows = cur.fetchall()
    conn.close()

    print(f"Total emails in window: {len(rows)}")
    written = 0
    skipped = 0
    for ts, sender, subject in rows:
        if not subject:
            continue
        if not is_project_relevant(subject, sender):
            skipped += 1
            continue
        date = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        sender_email = extract_email(sender)
        sender_name = extract_name(sender)
        ident = sender_email or sender_name or "unknown"
        fname = f"{date}-{slugify(ident)}-{slugify(subject)}.md"
        dest = INBOX / fname
        if dest.exists():
            skipped += 1
            continue
        project = route_to_project(subject, sender, projects)
        content = (
            f"From: {sender_name} <{sender_email or 'no-email'}>\n"
            f"Subject: {subject}\n"
            f"Date: {date}\n"
            f"Project: {project or 'unrouted'}\n"
            f"Source: outlook-sqlite-backfill\n"
            f"Status: backfilled\n\n"
            f"Backfilled from Outlook SQLite. Original sender: {sender}\n"
            f"Subject: {subject}\n"
        )
        if not args.dry_run:
            dest.write_text(content, encoding="utf-8")
        written += 1
        print(f"  + {fname} [{project or 'unrouted'}]")

    print(f"\n=== Done. {written} written, {skipped} skipped (non-project/dup). ===")

if __name__ == "__main__":
    main()
