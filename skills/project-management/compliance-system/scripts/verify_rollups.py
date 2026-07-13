#!/usr/bin/env python3
"""
verify_rollups.py — Recompute the roll-up block in compliance_matrix.md and
compliance_gaps.md against the actual data rows, and report any drift.

Usage:
    python3 verify_rollups.py [--matrix PATH] [--gaps PATH]

Defaults to the canonical Aseer Museum paths. Exits non-zero if the declared
roll-up disagrees with the recomputed value on any line.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

DEFAULT_MATRIX = Path.home() / "aseer-museum-pm/Technical_Office/Compliance_System/compliance_matrix.md"
DEFAULT_GAPS = Path.home() / "aseer-museum-pm/Technical_Office/Compliance_System/compliance_gaps.md"

SECTION_HEADERS = ("Division", "Exhibition-Specific", "Specialist Sub-Contractor")
GAP_ID_PATTERN = re.compile(r"GAP-[A-Z]+-\d+")
EMOJI = {"🟢": 0, "🟡": 0, "🔴": 0, "⚪": 0}


def _data_rows(section: str) -> list[str]:
    rows = []
    for line in section.splitlines():
        if not line.startswith("| "):
            continue
        if line.startswith("|---") or line.startswith("| Req ID") or line.startswith("| Gap ID"):
            continue
        if "|" not in line[2:]:
            continue
        rows.append(line)
    return rows


def compute_matrix(path: Path) -> dict:
    text = path.read_text()
    sections = re.split(r"\n## ", text)
    status = dict(EMOJI)
    total = 0
    gap_ids: set[str] = set()
    for s in sections:
        if not s.startswith(SECTION_HEADERS):
            continue
        for r in _data_rows(s):
            total += 1
            for k in status:
                if k in r:
                    status[k] += 1
                    break
            for gid in GAP_ID_PATTERN.findall(r):
                gap_ids.add(gid)
    return {
        "total": total,
        "status": status,
        "unique_gap_ids": len(gap_ids),
    }


def compute_gaps(path: Path) -> dict:
    text = path.read_text()
    open_section = text.split("## Open Gaps", 1)[1].split("## Resolved Gaps", 1)[0]
    resolved_section = text.split("## Resolved Gaps", 1)[1]
    open_rows = _data_rows(open_section)
    resolved_rows = _data_rows(resolved_section)

    crit_high = sum(1 for r in open_rows if "| Critical |" in r or "| High |" in r)
    in_progress = sum(1 for r in open_rows if "🟡 In Progress" in r)
    return {
        "open": len(open_rows),
        "resolved": len(resolved_rows),
        "crit_high_open": crit_high,
        "in_progress": in_progress,
    }


def _declared_rollup(text: str) -> dict:
    block = re.search(r"## Roll-up\s*\n.*?\| Metric.*?\n(.*?)\n---", text, re.DOTALL)
    if not block:
        return {}
    out = {}
    for line in block.group(1).splitlines():
        if "|" not in line:
            continue
        cols = [c.strip() for c in line.split("|") if c.strip()]
        if len(cols) >= 2:
            try:
                out[cols[0]] = int(cols[-1])
            except ValueError:
                pass
    return out


def check_matrix(path: Path) -> list[str]:
    text = path.read_text()
    computed = compute_matrix(path)
    declared = _declared_rollup(text)
    diffs = []
    if declared.get("Total compliance rows") != computed["total"]:
        diffs.append(
            f"matrix: Total compliance rows declared={declared.get('Total compliance rows')} "
            f"computed={computed['total']}"
        )
    label_map = {"🟢": "Compliant", "🟡": "Partial", "🔴": "Non-compliant", "⚪": "Not assessed"}
    for emoji, count in computed["status"].items():
        declared_key = f"{emoji} {label_map[emoji]}"
        if declared.get(declared_key) != count:
            diffs.append(
                f"matrix: {declared_key} declared={declared.get(declared_key)} computed={count}"
            )
    if declared.get("Open gaps") != computed["unique_gap_ids"]:
        diffs.append(
            f"matrix: Open gaps declared={declared.get('Open gaps')} "
            f"computed={computed['unique_gap_ids']}"
        )
    return diffs


def check_gaps(path: Path) -> list[str]:
    text = path.read_text()
    computed = compute_gaps(path)
    declared = _declared_rollup(text)
    diffs = []
    total_declared = declared.get("Total gaps", 0)
    expected_total = computed["open"] + computed["resolved"]
    if total_declared != expected_total:
        diffs.append(
            f"gaps: Total gaps declared={total_declared} "
            f"computed={computed['open']}+{computed['resolved']}={expected_total}"
        )
    if declared.get("🔴 Open (critical/high)") != computed["crit_high_open"]:
        diffs.append(
            f"gaps: 🔴 Open (critical/high) declared={declared.get('🔴 Open (critical/high)')} "
            f"computed={computed['crit_high_open']}"
        )
    if declared.get("🟡 In Progress") != computed["in_progress"]:
        diffs.append(
            f"gaps: 🟡 In Progress declared={declared.get('🟡 In Progress')} "
            f"computed={computed['in_progress']}"
        )
    if declared.get("🟢 Resolved") != computed["resolved"]:
        diffs.append(
            f"gaps: 🟢 Resolved declared={declared.get('🟢 Resolved')} "
            f"computed={computed['resolved']}"
        )
    return diffs


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    p.add_argument("--gaps", type=Path, default=DEFAULT_GAPS)
    args = p.parse_args()

    diffs: list[str] = []
    if args.matrix.exists():
        diffs.extend(check_matrix(args.matrix))
    if args.gaps.exists():
        diffs.extend(check_gaps(args.gaps))

    if not diffs:
        print("OK — all roll-up values match the table data.")
        return 0
    print("DRIFT detected:")
    for d in diffs:
        print(f"  - {d}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
