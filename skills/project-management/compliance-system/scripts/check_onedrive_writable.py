#!/usr/bin/env python3
"""OneDrive writable-tree check for Aseer Museum submittal filing.

Run before any new file operation in OneDrive to confirm the canonical
BIM unit tree is writable. Exits non-zero (with diagnostic) if it isn't.

Usage:
    python3 ~/.hermes/skills/project-management/compliance-system/scripts/check_onedrive_writable.py

Returns:
    exit 0 — all canonical trees writable
    exit 1 — at least one tree is not writable (do not file here)

Output: prints one line per tree checked. Last line is the summary.
"""
import os
import sys
import tempfile

CANONICAL_TREES = [
    # (label, absolute path)
    ("PQ folder (canonical)",
     "/Users/mohamedessa/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/02_Submittals/09_Prequalifications"),
    ("AV sub-contractor BOQ folder",
     "/Users/mohamedessa/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/24_Subcontractors/04_AV_IT_Contractor/01_Schedule_and_BOQ"),
    ("Aseer BIM root",
     "/Users/mohamedessa/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum"),
]

# For reference only — should NOT be writable from this session.
KNOWN_BLOCKED = [
    ("Adel Darwish PQ folder (do NOT use)",
     "/Users/mohamedessa/OneDrive - SAMAYA INVESTMENT/Adel  Darwish's files - 01- Execution Documents/07- Pre-Qualification Submittal"),
]


def check_writable(label, path):
    """Return (ok, message) — does this path exist and accept touch+rm?"""
    if not os.path.isdir(path):
        return False, f"MISSING — directory does not exist: {path}"
    try:
        # touch test
        probe = os.path.join(path, ".write_test_" + str(os.getpid()))
        with open(probe, "w") as f:
            f.write("x")
        os.remove(probe)
        return True, "writable"
    except (PermissionError, OSError) as e:
        return False, f"NOT WRITABLE ({type(e).__name__}: {e})"


def main():
    print("=" * 72)
    print("Aseer Museum — OneDrive writable-tree check")
    print("=" * 72)

    fail = 0
    for label, path in CANONICAL_TREES:
        ok, msg = check_writable(label, path)
        flag = "OK  " if ok else "FAIL"
        print(f"  [{flag}] {label}")
        print(f"        {path}")
        print(f"        → {msg}")
        if not ok:
            fail += 1

    print()
    print("Reference (blocked — do NOT file here):")
    for label, path in KNOWN_BLOCKED:
        ok, msg = check_writable(label, path)
        expected = "NOT WRITABLE" if not ok else "WRITABLE (unexpected!)"
        flag = "OK  " if not ok else "WARN"
        print(f"  [{flag}] {label}")
        print(f"        {path}")
        print(f"        → {msg} — expected: {expected}")
        if ok:
            fail += 1  # surprising — warn

    print("=" * 72)
    if fail == 0:
        print("All canonical trees writable — proceed with filing.")
        return 0
    else:
        print(f"{fail} tree(s) failed — do NOT file; fall back to _FILE_PLAN.md.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
