#!/usr/bin/env /usr/bin/python3
"""
Add rows to existing BIM project registers (non-destructive append).

Usage:
  1. Edit the ROWS dict below to define what to add per register
  2. Run: /usr/bin/python3 /Users/mohamedessa/.hermes/skills/productivity/bim-project-register/scripts/add_rows_to_registers.py

Caveat:
  - Only use this for registers that ALREADY have their header row in place.
  - For registers with 0 data rows and NO header, use fix_empty_register.py instead.
"""
import openpyxl
import os

REG_PATH = "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/El-Ghamama Gift Shop(2)/Docs/09_Registers"

# ── Configure rows to add below ───────────────────────────────────────────────
# Format: ("Register.xlsx", "DataSheetName", [col1, col2, ...])

ROWS_TO_ADD = [
    # Example:
    # (
    #     "Submittal_Register.xlsx", "Submittal",
    #     ["2025-11-05", "SUB-010", "HVAC SD Layout - Final",
    #      "Shop Drawing", "Samaya Investment", "Client",
    #      "Submitted", "-", "Submittals/Mep/HVAC/", "HVAC layout drawings"]
    # ),
]

# ── Runner ───────────────────────────────────────────────────────────────────
def append_row(sheet_path, data_sheet_name, row_data):
    wb = openpyxl.load_workbook(sheet_path)
    ws = wb[data_sheet_name]
    ws.append(row_data)
    wb.save(sheet_path)
    print(f"  ✓ {os.path.basename(sheet_path)}")

if not ROWS_TO_ADD:
    print("No rows configured. Edit this script and add entries to ROWS_TO_ADD.")
else:
    for reg_file, sheet_name, row in ROWS_TO_ADD:
        path = os.path.join(REG_PATH, reg_file)
        append_row(path, sheet_name, row)
    print("\nAll rows added.")