#!/usr/bin/env python3
"""Audit all .md files in target directories for YAML frontmatter compliance.

Usage:
    python3 scripts/audit_frontmatter.py

Scans all .md files under TARGET_DIRS, checks for:
- YAML frontmatter present (starts with ---)
- Required fields: last_updated, owner_agent, status, source
- Status is one of: active, draft, superseded, closed, archived

Outputs summary + detailed results to stdout, writes audit_report.md.
"""

import os
import re
import yaml
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TARGET_DIRS = [
    "00_Status", "01_Registers", "03_Plans", "05_Comms",
    "08_Document_Index", "Technical_Office", "09_Agent_Workspace",
    "00_Command_Center", "02_Schedule", "04_Cost", "00_Project_Charter",
]

VALID_STATUSES = {"active", "draft", "superseded", "closed", "archived"}
REQUIRED_FIELDS = ["last_updated", "owner_agent", "status", "source"]


def has_frontmatter(content):
    return content.startswith("---")


def parse_frontmatter(content):
    """Extract YAML frontmatter from content. Returns (fields_dict, body_start_line)."""
    if not content.startswith("---"):
        return None, 0

    lines = content.split("\n")
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return None, 0

    fm_text = "\n".join(lines[1:end_idx])
    try:
        fields = yaml.safe_load(fm_text)
        if not isinstance(fields, dict):
            return None, end_idx + 1
        return fields, end_idx + 1
    except yaml.YAMLError:
        return None, end_idx + 1


def audit_file(filepath):
    """Audit a single file. Returns dict of issues."""
    relpath = os.path.relpath(filepath, REPO)
    issues = {
        "path": relpath,
        "has_frontmatter": False,
        "missing_fields": [],
        "invalid_status": None,
        "extra_fields": [],
        "critical": False,
        "medium": False,
    }

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        issues["error"] = str(e)
        return issues

    if not has_frontmatter(content):
        issues["critical"] = True
        return issues

    issues["has_frontmatter"] = True
    fields, _ = parse_frontmatter(content)

    if fields is None:
        issues["critical"] = True
        issues["note"] = "Frontmatter delimiters found but could not parse YAML"
        return issues

    for field in REQUIRED_FIELDS:
        if field not in fields or fields[field] is None:
            issues["missing_fields"].append(field)
            issues["medium"] = True

    if "status" in fields and fields["status"] is not None:
        status_val = str(fields["status"]).strip().lower()
        if status_val not in VALID_STATUSES:
            issues["invalid_status"] = fields["status"]
            issues["medium"] = True

    return issues


def main():
    all_files = []
    for d in TARGET_DIRS:
        dirpath = os.path.join(REPO, d)
        if not os.path.isdir(dirpath):
            print(f"WARNING: Directory not found: {dirpath}")
            continue
        for root, dirs, files in os.walk(dirpath):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in files:
                if f.endswith(".md"):
                    all_files.append(os.path.join(root, f))

    all_files.sort()
    print(f"Total .md files found: {len(all_files)}")

    results = []
    for fp in all_files:
        issues = audit_file(fp)
        results.append(issues)

    total = len(results)
    critical = [r for r in results if r["critical"]]
    medium = [r for r in results if r["medium"] and not r["critical"]]
    clean = [r for r in results if not r["critical"] and not r["medium"]]

    print(f"\n=== AUDIT SUMMARY ===")
    print(f"Total files scanned: {total}")
    print(f"Clean (no issues): {len(clean)}")
    print(f"Critical (no frontmatter): {len(critical)}")
    print(f"Medium (missing fields / invalid status): {len(medium)}")

    if critical:
        print(f"\n--- CRITICAL: Files with NO frontmatter ---")
        for r in critical:
            print(f"  {r['path']}")

    if medium:
        print(f"\n--- MEDIUM: Files with missing/invalid fields ---")
        for r in medium:
            missing = ", ".join(r["missing_fields"]) if r["missing_fields"] else "none"
            inv = f" (invalid status: {r['invalid_status']})" if r["invalid_status"] else ""
            print(f"  {r['path']} — missing: [{missing}]{inv}")

    # Write report
    report_path = os.path.join(REPO, "00_Command_Center", "audit_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"""---
last_updated: {date.today().isoformat()}
owner_agent: Hermes
status: active
source: scripts/audit_frontmatter.py
---

# Frontmatter Audit Report

**Generated:** {date.today().isoformat()}
**Auditor:** Hermes Agent
**Scope:** All .md files in target directories

## Summary

| Metric | Value |
|--------|-------|
| Total Files Scanned | {total} |
| Clean (no issues) | {len(clean)} |
| Critical Issues (no frontmatter) | {len(critical)} |
| Medium Issues (missing fields / invalid status) | {len(medium)} |
| Files Needing Update | {len(critical) + len(medium)} |
""")
    print(f"\nReport written to: {report_path}")
    return results


if __name__ == "__main__":
    main()
