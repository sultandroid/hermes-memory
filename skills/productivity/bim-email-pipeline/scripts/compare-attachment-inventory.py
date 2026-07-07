#!/usr/bin/env python3
"""
Compare attachment files in the pipeline staging area against files already
filed in BIM OneDrive folders. Reports which files are new (not yet filed).

Usage:
    python3 compare-attachment-inventory.py

Returns exit 0 if all files accounted for, exit 1 if new files found.
Outputs a CSV summary to stdout and (optionally) a full delta report.
"""

import os, sys, csv
from collections import defaultdict

# ── Configuration ────────────────────────────────────────────────────────────
BIM_BASE = os.path.expanduser(
    "~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit"
)

ATTACHMENTS_DIR = os.path.expanduser(
    "~/Documents/04_Outlook_Connection/mails/attachments"
)

# Project mapping: attachment subdir name → BIM target folder basename
PROJECT_MAP = {
    "aseer_museum": "Aseer-Museum",
    "zamzam_nwc": "Zamzam Museum",
}

# Specific BIM subfolders to check per project (relative to project root)
# Keyed by attachment subdir, value = list of BIM subfolder patterns to walk
CHECK_PATHS = {
    "aseer_museum": [
        "Aseer-Museum/Completed Tender Package From NRS/05_Correspondence_Archive",
        "Aseer-Museum/Completed Tender Package From NRS/04_Specifications_and_BOQ",
        "Aseer-Museum/Reports & Meeting/00_Daily Reports",
        "Aseer-Museum/Design Files/00_Scope_and_Proposals",
        "Aseer-Museum/Subcontractors/14_MEP_Contractor",
        "Aseer-Museum/Docs/00_Admin/99_Images",
    ],
    "zamzam_nwc": [
        "Zamzam Museum/Docs/03_Inspection_Requests",
    ],
}

# Fallback: walk entire project tree for misc attachments
FALLBACK_PROJECTS = {
    "admin_hr": "Aseer-Museum",
    "general": "Aseer-Museum",
    "haramein_ghamamah": "Aseer-Museum",
    "hoarding_signage": "Aseer-Museum",
    "makkah_jabal_omar": "Aseer-Museum",
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def normalize(name: str) -> str:
    """Case-insensitive basename normalization for comparison."""
    return os.path.basename(name).lower().strip()


def collect_bim_filenames(bim_root: str, subdirs: list[str]) -> set[str]:
    """Walk BIM subdir trees and return set of normalized filenames."""
    names: set[str] = set()
    for sub in subdirs:
        full = os.path.join(bim_root, sub)
        if not os.path.isdir(full):
            continue
        for root, dirs, files in os.walk(full):
            for f in files:
                names.add(normalize(os.path.join(root, f)))
    return names


def collect_attachment_files(root: str) -> list[dict]:
    """Walk attachment tree and return list of {rel_path, name, size, mtime}."""
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, root)
            try:
                sz = os.path.getsize(full)
                mt = os.path.getmtime(full)
            except OSError:
                sz = -1
                mt = 0
            results.append({
                "rel_path": rel,
                "name": normalize(f),
                "original_name": f,
                "size": sz,
                "mtime": mt,
            })
    return results

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print(f"BIM base: {BIM_BASE}")
    print(f"Attachments: {ATTACHMENTS_DIR}")
    print()

    # Pre-collect BIM filenames for each project
    bim_names: dict[str, set[str]] = {}
    for proj, subdirs in CHECK_PATHS.items():
        bim_names[proj] = collect_bim_filenames(BIM_BASE, subdirs)
        print(f"  {proj}: {len(bim_names[proj])} BIM filenames loaded")

    # Also load fallback projects
    for proj in FALLBACK_PROJECTS:
        if proj not in bim_names:
            bim_names[proj] = set()

    # Collect attachment files
    att_files = collect_attachment_files(ATTACHMENTS_DIR)
    print(f"\n  Total attachment files: {len(att_files)}")

    # Categorize by project
    by_project: dict[str, list[dict]] = defaultdict(list)
    for af in att_files:
        parts = af["rel_path"].split(os.sep)
        if len(parts) < 2:
            continue
        proj = parts[0]
        by_project[proj].append(af)

    # Compare
    found: list[dict] = []
    new: list[dict] = []

    for proj, files in sorted(by_project.items()):
        known_names = bim_names.get(proj, set())
        # Fallback: if no specific BIM path loaded, check full project tree
        if not known_names:
            fallback_proj = FALLBACK_PROJECTS.get(proj)
            if fallback_proj:
                full_tree = [fallback_proj]  # walk whole project
                known_names = collect_bim_filenames(BIM_BASE, full_tree)
                bim_names[proj] = known_names

        for af in files:
            # Also check the broader BIM tree (any project)
            in_bim = af["name"] in known_names
            if not in_bim:
                # Try across ALL projects as fallback
                for pname, pset in bim_names.items():
                    if af["name"] in pset:
                        in_bim = True
                        break

            if in_bim:
                found.append(af)
            else:
                new.append(af)

    # Report
    print(f"\n{'='*60}")
    print(f"  Already in BIM: {len(found)}")
    print(f"  NEW (not filed): {len(new)}")
    print(f"{'='*60}")

    if new:
        print(f"\n⚠️  {len(new)} NEW FILES — NOT IN BIM:\n")
        writer = csv.writer(sys.stdout)
        writer.writerow(["rel_path", "size_bytes", "modified"])
        import datetime
        for af in sorted(new, key=lambda x: x["rel_path"]):
            dt = datetime.datetime.fromtimestamp(af["mtime"]).strftime("%Y-%m-%d %H:%M")
            writer.writerow([af["rel_path"], af["size"], dt])
        sys.exit(1)
    else:
        print("\n✅ All attachment files are already filed in BIM. Steady state confirmed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
