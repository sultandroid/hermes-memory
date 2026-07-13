#!/usr/bin/env python3
"""
check_pq_sequence.py — Find the actual next free PQ number by reading BOTH the
markdown register and the OneDrive folder index. Catches the drift where Aconex
synced a new PQ (e.g. PQ-0111) but the markdown register hasn't been updated
yet, or where two sources disagree on the next number.

Usage:
    python3 check_pq_sequence.py [--register PATH] [--onedrive PATH]

Defaults to the Aseer Museum paths. Prints the next free PQ number and lists
the highest sequence seen in each source so you can spot drift.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

DEFAULT_REGISTER = Path.home() / "aseer-museum-pm/01_Registers/prequalification_register.md"
DEFAULT_ONEDRIVE = Path("/Users/mohamedessa/OneDrive - SAMAYA INVESTMENT/Adel  Darwish's files - 01- Execution Documents/07- Pre-Qualification Submittal")

PQ_RE = re.compile(r"MOC-(?:MUS-ASE|Asser-SIC|Asser-SAM)[A-Z0-9]+-PQ-(\d{3,4})")
ONEDRIVE_FOLDER_RE = re.compile(r"^(\d{1,4})-\s*MOC-.*-PQ-(\d{3,4})")


def parse_register(path: Path) -> list[int]:
    if not path.exists():
        return []
    nums: list[int] = []
    for line in path.read_text().splitlines():
        for m in PQ_RE.findall(line):
            nums.append(int(m))
    return sorted(set(nums))


def parse_onedrive(path: Path) -> list[int]:
    if not path.exists():
        return []
    nums: list[int] = []
    for entry in path.iterdir():
        if not entry.is_dir():
            continue
        m = ONEDRIVE_FOLDER_RE.match(entry.name)
        if m:
            nums.append(int(m.group(2)))
    return sorted(set(nums))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    p.add_argument("--onedrive", type=Path, default=DEFAULT_ONEDRIVE)
    args = p.parse_args()

    reg_nums = parse_register(args.register)
    od_nums = parse_onedrive(args.onedrive)

    reg_max = max(reg_nums) if reg_nums else 0
    od_max = max(od_nums) if od_nums else 0
    overall_max = max(reg_max, od_max)

    in_reg_only = sorted(set(reg_nums) - set(od_nums))
    in_od_only = sorted(set(od_nums) - set(reg_nums))

    print(f"Register highest PQ: PQ-{reg_max:04d}  ({len(reg_nums)} unique PQs)")
    print(f"OneDrive  highest PQ: PQ-{od_max:04d}  ({len(od_nums)} unique PQ folders)")
    print(f"Suggested next free:  PQ-{overall_max + 1:04d}")
    if in_reg_only:
        print(f"\nIn register but not OneDrive (drift): {in_reg_only[:20]}{'...' if len(in_reg_only) > 20 else ''}")
    if in_od_only:
        print(f"In OneDrive but not register (drift): {in_od_only[:20]}{'...' if len(in_od_only) > 20 else ''}")
    if not in_reg_only and not in_od_only:
        print("\nRegister and OneDrive agree.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
