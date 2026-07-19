#!/usr/bin/env python3
"""Fix YAML frontmatter issues found by audit_frontmatter.py.

Usage:
    python3 scripts/fix_frontmatter.py

Fixes:
1. Adds YAML frontmatter to files with none (critical)
2. Adds missing fields to files with partial frontmatter (medium)
3. Fixes invalid status values
4. Quotes source values containing colons that break YAML parsing

Uses path-based heuristics to infer reasonable defaults for:
- source (directory path)
- owner_agent (Hermes)
- status (active, draft, or archived based on path)
"""

import os
import yaml
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = date.today().isoformat()
VALID_STATUSES = {"active", "draft", "superseded", "closed", "archived"}

TARGET_DIRS = [
    "00_Status", "01_Registers", "03_Plans", "05_Comms",
    "08_Document_Index", "Technical_Office", "09_Agent_Workspace",
    "00_Command_Center", "02_Schedule", "04_Cost", "00_Project_Charter",
]


def has_frontmatter(content):
    return content.startswith("---")


def parse_frontmatter(content):
    """Extract YAML frontmatter from content. Returns (fields_dict, body_start_line, fm_end_line)."""
    if not content.startswith("---"):
        return None, 0, 0

    lines = content.split("\n")
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return None, 0, 0

    fm_text = "\n".join(lines[1:end_idx])
    try:
        fields = yaml.safe_load(fm_text)
        if not isinstance(fields, dict):
            return None, end_idx + 1, end_idx
        return fields, end_idx + 1, end_idx
    except yaml.YAMLError:
        return None, end_idx + 1, end_idx


def infer_source(filepath):
    """Infer a reasonable source for a file based on its path."""
    relpath = os.path.relpath(filepath, REPO)
    parts = relpath.split(os.sep)

    if len(parts) >= 2 and parts[0] == "03_Plans":
        return f"03_Plans/{parts[1]}/"
    if parts[0] == "Technical_Office" and len(parts) >= 2:
        return f"Technical_Office/{parts[1]}/"
    if parts[0] in ("08_Document_Index", "09_Agent_Workspace", "05_Comms",
                     "00_Project_Charter", "00_Command_Center", "02_Schedule"):
        return f"{parts[0]}/"
    return relpath


def infer_owner(filepath):
    return "Hermes"


def infer_status(filepath):
    relpath = os.path.relpath(filepath, REPO)
    parts = relpath.split(os.sep)
    if parts[0] == "99_Archive":
        return "archived"
    if "Draft_SOW_RACI" in parts or "drafts" in parts:
        return "draft"
    return "active"


def add_frontmatter(content, filepath):
    """Add YAML frontmatter to content that has none."""
    source = infer_source(filepath)
    owner = infer_owner(filepath)
    status = infer_status(filepath)

    fm = f"""---
last_updated: {TODAY}
owner_agent: {owner}
status: {status}
source: {source}
---

"""
    return fm + content


def fix_missing_fields(content, filepath, missing_fields, invalid_status=None):
    """Add missing fields to existing frontmatter and fix invalid status."""
    lines = content.split("\n")

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return content

    fm_text = "\n".join(lines[1:end_idx])
    try:
        fields = yaml.safe_load(fm_text)
        if not isinstance(fields, dict):
            fields = {}
    except yaml.YAMLError:
        fields = {}

    if "last_updated" in missing_fields:
        fields["last_updated"] = TODAY
    if "owner_agent" in missing_fields:
        fields["owner_agent"] = infer_owner(filepath)
    if "status" in missing_fields:
        fields["status"] = infer_status(filepath)
    if "source" in missing_fields:
        fields["source"] = infer_source(filepath)
    if invalid_status:
        fields["status"] = "active"

    # Rebuild frontmatter preserving field order
    field_order = ["last_updated", "owner_agent", "status", "source"]
    other_fields = {k: v for k, v in fields.items() if k not in field_order}

    new_fm_lines = ["---"]
    for f in field_order:
        if f in fields:
            val = fields[f]
            # Quote values with colons to prevent YAML parse errors
            if isinstance(val, str) and ":" in val and not val.startswith('"'):
                val = f'"{val}"'
            new_fm_lines.append(f"{f}: {val}")
    for f, v in other_fields.items():
        new_fm_lines.append(f"{f}: {v}")
    new_fm_lines.append("---")

    new_fm = "\n".join(new_fm_lines)
    body = "\n".join(lines[end_idx + 1:])
    return new_fm + "\n\n" + body


def main():
    all_files = []
    for d in TARGET_DIRS:
        dirpath = os.path.join(REPO, d)
        if not os.path.isdir(dirpath):
            continue
        for root, dirs, files in os.walk(dirpath):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in files:
                if f.endswith(".md"):
                    all_files.append(os.path.join(root, f))

    all_files.sort()

    fixed_critical = []
    fixed_medium = []
    errors = []

    for fp in all_files:
        relpath = os.path.relpath(fp, REPO)

        try:
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            errors.append((relpath, str(e)))
            continue

        if not has_frontmatter(content):
            new_content = add_frontmatter(content, fp)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_content)
            fixed_critical.append(relpath)
            print(f"[FIXED-CRITICAL] {relpath}")
            continue

        fields, _, _ = parse_frontmatter(content)
        if fields is None:
            continue

        missing = []
        for field in ["last_updated", "owner_agent", "status", "source"]:
            if field not in fields or fields[field] is None:
                missing.append(field)

        invalid_status = None
        if "status" in fields and fields["status"] is not None:
            status_val = str(fields["status"]).strip().lower()
            if status_val not in VALID_STATUSES:
                invalid_status = fields["status"]

        if missing or invalid_status:
            new_content = fix_missing_fields(content, fp, missing, invalid_status)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_content)
            fixed_medium.append(relpath)
            details = []
            if missing:
                details.append(f"missing: {missing}")
            if invalid_status:
                details.append(f"invalid status: {invalid_status}")
            print(f"[FIXED-MEDIUM] {relpath} — {'; '.join(details)}")

    print(f"\n=== FIX SUMMARY ===")
    print(f"Critical fixes (added frontmatter): {len(fixed_critical)}")
    print(f"Medium fixes (added fields / fixed status): {len(fixed_medium)}")
    print(f"Errors: {len(errors)}")

    if errors:
        print(f"\nErrors:")
        for path, err in errors:
            print(f"  {path}: {err}")


if __name__ == "__main__":
    main()
