#!/usr/bin/env python3
"""
Reusable routing script pattern for email-pipeline-automation.

Usage:
  1. Copy this file to /tmp/route_attachments.py
  2. Edit the `routes` list with your classification rules
  3. Run: python3 /tmp/route_attachments.py

Rules are evaluated in order — first match wins.
Each rule: (regex_pattern, destination_subfolder_relative_to_project_root)
"""
import shutil, os, re

staging = "/tmp/email_attachments/"
root = "/Volumes/MIcro/Work/Aseer-Museum/"

routes = [
    # NCR / Safety Instructions
    (r"48614_.*SE-021", "04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/"),
    # Prequalifications
    (r"48613_.*PQ-0124", "24_Subcontractors/AME_Acoustic/01_Prequalification/"),
    (r"48577_.*PQ-0122", "24_Subcontractors/50_Landscaping/01_Prequalification/"),
    (r"48531_.*PQ-0120", "24_Subcontractors/99_Materials_Testing_Lab/01_Prequalification/"),
    (r"48533_.*PQ-0121", "24_Subcontractors/99_Materials_Testing_Lab/01_Prequalification/"),
    # Design Gateway Submittals (1G-)
    (r"48598_.*1M0-1G-0001", "02_Submittals/01_DD_Gate/HVAC/"),
    (r"48581_.*1M0-1G-0001", "02_Submittals/01_DD_Gate/HVAC/"),
    (r"48561_.*1M0-1G-0001", "02_Submittals/01_DD_Gate/HVAC/"),
    (r"48595_.*1C0-1G-0001", "02_Submittals/01_DD_Gate/Structural/"),
    (r"48606_.*1A0-1G-0004", "02_Submittals/01_DD_Gate/Architecture/"),
    (r"48604_.*1A0-1G-0003", "02_Submittals/01_DD_Gate/Architecture/"),
    (r"48601_.*1A0-1G-0003", "02_Submittals/01_DD_Gate/Architecture/"),
    (r"48558_.*1A0-1G-0005", "02_Submittals/01_DD_Gate/Architecture/"),
    (r"48575_.*1A0-1G-0006", "02_Submittals/01_DD_Gate/Architecture/"),
    (r"48570_.*1A0-1G-0006", "02_Submittals/01_DD_Gate/Architecture/"),
    # Design Studies / Reports (ZD-)
    (r"48592_.*ZD-0091", "03_Design_Files/Electrical/"),
    (r"48586_.*ZD-0090", "03_Design_Files/Electrical/"),
    (r"48572_.*ZD-0088", "03_Design_Files/Electrical/"),
    (r"48580_.*ZD-0067", "03_Design_Files/MEP/"),
    (r"48608_.*ZD-0085", "24_Subcontractors/Graphics_Specialist/01_Scope_of_Work/"),
    (r"48603_.*ZD-0085", "24_Subcontractors/Graphics_Specialist/01_Scope_of_Work/"),
    (r"48602_.*ZD-0085", "24_Subcontractors/Graphics_Specialist/01_Scope_of_Work/"),
    (r"48560_.*ZD-0082", "04_Docs/02_Plans_and_Procedures/02.2_Sustainability_Plan/01_Source_Files/"),
    (r"48562_.*ZD-0087", "03_Design_Files/General/"),
    # Risk Management Plan
    (r"48578_.*Risk", "04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files/"),
    (r"48552_.*Risk", "04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files/"),
    # Daily Reports
    (r"48555_.*Daily", "00_Status/Daily_Reports/"),
    # Invoices
    (r"48530_.*INV-4863", "00_Contracts/Invoices/"),
    # Door Technical Review
    (r"48522_.*Door", "03_Design_Files/Architecture/"),
    # Technology BOQ
    (r"48550_.*BOQ", "24_Subcontractors/AV_IT/08_RFP_and_Proposals/"),
    # Rigging contractor
    (r"48546_.*Rigging", "24_Subcontractors/10_Rigging_Specialist/08_RFP_and_Proposals/"),
    # Landscape contractor
    (r"48547_.*landscape", "24_Subcontractors/50_Landscaping/08_RFP_and_Proposals/"),
]

copied = []
skipped = []

for fname in os.listdir(staging):
    fpath = os.path.join(staging, fname)
    if not os.path.isfile(fpath) or os.path.getsize(fpath) == 0:
        skipped.append((fname, "empty or directory"))
        continue
    if fname.endswith(".eml"):
        skipped.append((fname, "email forward, not document"))
        continue

    matched = False
    for pattern, dest in routes:
        if re.search(pattern, fname):
            dst_dir = os.path.join(root, dest)
            os.makedirs(dst_dir, exist_ok=True)
            dst_path = os.path.join(dst_dir, fname)
            shutil.copy2(fpath, dst_path)
            copied.append((fname, dest))
            matched = True
            break
    if not matched:
        skipped.append((fname, "no matching route"))

print(f"Copied: {len(copied)}")
for f, d in copied:
    print(f"  OK  {f} -> {d}")
print(f"\nSkipped: {len(skipped)}")
for f, r in skipped:
    print(f"  --  {f} ({r})")
