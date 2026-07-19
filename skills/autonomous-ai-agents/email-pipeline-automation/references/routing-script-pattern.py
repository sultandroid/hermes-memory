#!/usr/bin/env python3
"""
Reusable routing script pattern for email-pipeline-automation.

Usage:
  1. Copy this file to /tmp/route_attachments.py
  2. Edit the `routes` list with your classification rules
  3. Run: python3 /tmp/route_attachments.py

Rules are evaluated in order — first match wins.
Each rule: (regex_pattern, destination_subfolder_relative_to_project_root)

KEY DESIGN CHOICE: Use document-code-based patterns (e.g. r"ZD-0085")
NOT email-ID-prefixed patterns (e.g. r"48608_.*ZD-0085").
Document codes are reusable across sessions; email IDs are not.
"""
import shutil, os, re

STAGING = "/tmp/email_attachments/"
ROOT = "/Volumes/MIcro/Work/Aseer-Museum/"

# Classification rules: (filename_pattern, destination_subfolder)
# Order matters — first match wins
# Use document codes (SE-, NC-, PQ-, ZD-, 1G-, PL-) not email IDs
ROUTES = [
    # NCRs — route to per-NCR-ID subfolder
    (r"NC-1E0-0010", "04_Docs/10_Test_and_Inspection/10.3_NCRs/NC-1E0-0010/"),
    (r"NC-1M0-005", "04_Docs/10_Test_and_Inspection/10.3_NCRs/NC-1M0-005/"),
    # Safety Instructions
    (r"SE-021", "04_Docs/10_Test_and_Inspection/10.3_NCRs/SE-021/"),
    # Subcontractor Prequalifications
    (r"PQ-0122", "24_Subcontractors/07_Landscaping/01_Prequalification/"),
    (r"PQ-0124", "24_Subcontractors/06_Acoustic/01_Prequalification/"),
    (r"PQ-0120", "24_Subcontractors/08_Laboratory/01_Prequalification/"),
    (r"PQ-0121", "24_Subcontractors/08_Laboratory/01_Prequalification/"),
    # Graphics Specialist SOW (ZD-0085)
    (r"ZD-0085", "24_Subcontractors/04_Graphics_Graphite/01_Scope_of_Work/"),
    # Mechanical Engineer CV / Replacement (ZD-0087)
    (r"ZD-0087", "24_Subcontractors/05_Mechanical_Engineer/01_Scope_of_Work/"),
    # Risk Management Plan (ZD-0093, PL-02.17)
    (r"ZD-0093", "04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files/"),
    (r"PL-02.17", "04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files/"),
    (r"RISK MANAGEMENT PLAN", "04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files/"),
    # Project Execution Plan (ZD-0086)
    (r"ZD-0086", "04_Docs/02_Plans_and_Procedures/02.2_Project_Execution_Plan/01_Source_Files/"),
    # Sustainability Management Plan (ZD-0082)
    (r"ZD-0082", "04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/"),
    # DD Gate - Architecture (1A0-1G-0003/4/5/6)
    (r"1A0-1G-0003", "02_Submittals/01_DD_Gate/Architecture/"),
    (r"1A0-1G-0004", "02_Submittals/01_DD_Gate/Architecture/"),
    (r"1A0-1G-0005", "02_Submittals/01_DD_Gate/Architecture/"),
    (r"1A0-1G-0006", "02_Submittals/01_DD_Gate/Architecture/"),
    # DD Gate - Civil/Structural (1C0-1G-0001)
    (r"1C0-1G-0001", "02_Submittals/01_DD_Gate/Civil/"),
    # DD Gate - MEP/HVAC (1M0-1G-0001)
    (r"1M0-1G-0001", "02_Submittals/01_DD_Gate/MEP/"),
    # Technical Query (TQ-*)
    (r"TQ-0005", "03_Design_Files/Electrical/"),
    # Electrical Assessments
    (r"ZD-0088", "03_Design_Files/Electrical/ATS_Assessment/"),
    (r"ZD-0089", "03_Design_Files/Electrical/Containment_Assessment/"),
    (r"ZD-0090", "03_Design_Files/Electrical/Current_Condition_MDP/"),
    (r"ZD-0091", "03_Design_Files/Electrical/Earthing_Lightning/"),
    (r"ZD-0092", "03_Design_Files/Electrical/UPS_Assessment/"),
    (r"ZD-0067", "03_Design_Files/Electrical/Fire_Alarm_Suppression/"),
    # Contracts (ZNA, MEP agreements)
    (r"ZNA", "00_Contracts/"),
    (r"Aseer Museum MEP Agreement", "00_Contracts/"),
    # Daily Report
    (r"Daily_Report", "00_Status/Daily_Reports/"),
    # Invoice
    (r"INV-4863", "00_Contracts/Invoices/"),
    # Technology BOQ
    (r"Technology BOQ", "03_Design_Files/ICT/"),
    # CV
    (r"CV Puji", "24_Subcontractors/09_General/01_Prequalification/"),
    # Rigging contractor
    (r"Rigging", "24_Subcontractors/10_Rigging/01_Prequalification/"),
    # Landscape contractor
    (r"Existing Site Survey", "24_Subcontractors/07_Landscaping/01_Prequalification/"),
    # Equipment Inspection Reports
    (r"Equipment 00[1-3]", "04_Docs/10_Test_and_Inspection/"),
    # Patinated Brass / Material Finish
    (r"GBH Letter", "03_Design_Files/FF&E_Material_Boards/"),
    (r"MA-0006", "03_Design_Files/FF&E_Material_Boards/"),
    # Material Boards
    (r"MATERIAL-BOARDS", "02_Submittals/01_DD_Gate/Architecture/"),
    # Scenography
    (r"Scenography", "03_Design_Files/"),
    # TFP Engineering Design Check
    (r"TFP_Engineering", "03_Design_Files/Electrical/"),
]

# Zamzam project files — route separately
ZAMZAM_ROUTES = [
    (r"ZAM-NWC", "/Volumes/MIcro/Work/Zamzam-Visitor-Center/"),
]

def find_route(filename):
    for pattern, dest in ROUTES:
        if re.search(pattern, filename, re.IGNORECASE):
            return dest
    return None

def find_zamzam_route(filename):
    for pattern, dest in ZAMZAM_ROUTES:
        if re.search(pattern, filename, re.IGNORECASE):
            return dest
    return None

copied = []
skipped = []
errors = []

for f in sorted(os.listdir(STAGING)):
    src = os.path.join(STAGING, f)
    if not os.path.isfile(src):
        continue
    if f.endswith('.eml'):
        skipped.append((f, "eml copy"))
        continue

    # Check Zamzam first
    zamzam_dest = find_zamzam_route(f)
    if zamzam_dest:
        dst_dir = zamzam_dest
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, f)
        try:
            shutil.copy2(src, dst)
            copied.append((f, dst_dir))
        except Exception as e:
            errors.append((f, str(e)))
        continue

    # Aseer routing
    dest = find_route(f)
    if dest:
        dst_dir = os.path.join(ROOT, dest)
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, f)
        try:
            shutil.copy2(src, dst)
            copied.append((f, dst_dir))
        except Exception as e:
            errors.append((f, str(e)))
    else:
        skipped.append((f, "no matching route"))

print(f"=== ROUTING RESULTS ===")
print(f"Copied: {len(copied)}")
for f, d in copied:
    print(f"  OK  {f} -> {d}")
print(f"\nSkipped: {len(skipped)}")
for f, r in skipped:
    print(f"  --  {f} ({r})")
print(f"\nErrors: {len(errors)}")
for f, e in errors:
    print(f"  ERR {f}: {e}")
