#!/usr/bin/env python3
"""
Multi-project email attachment router.
Scans /tmp/email_attachments/ and routes files to correct OneDrive project folders
based on document-code prefixes in filenames.

Usage:
  python3 /tmp/multi_project_router.py

Add new ROUTES entries as new document codes appear.
"""
import os, shutil, re

STAGING = "/tmp/email_attachments"

ROOTS = {
    "aseer": "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum",
    "zamzam": "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Zamzam -Visitor Center",
    "jabal_omar": "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Jabal Omar - Samaya Scope",
}

# Routing rules: (regex pattern, project_key, dest_subpath)
# Patterns match against the full filename (including email-ID prefix).
# Use document-code patterns (e.g. r"ZD-0085") not email-ID patterns (e.g. r"48608_")
ROUTES = [
    # === ASEER MUSEUM ===
    # CG Responses / Plans
    (r"ZD-0102", "aseer", "04_Docs/02_Plans_and_Procedures/02.2_Project_Execution_Plan/01_Source_Files"),
    (r"ZD-0100", "aseer", "04_Docs/02_Plans_and_Procedures/02.2_Project_Execution_Plan/01_Source_Files"),
    (r"ZD-0086", "aseer", "04_Docs/02_Plans_and_Procedures/02.2_Project_Execution_Plan/01_Source_Files"),
    (r"ZD-0093", "aseer", "04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files"),
    (r"ZD-0094", "aseer", "04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files"),
    (r"ZD-0103", "aseer", "04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files"),
    (r"ZD-0104", "aseer", "04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files"),
    (r"ZD-0106", "aseer", "04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files"),
    (r"ZD-0078", "aseer", "04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files"),
    (r"ZD-0082", "aseer", "04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files"),
    (r"Sustainability", "aseer", "04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files"),
    (r"SMP", "aseer", "04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files"),
    (r"Civil_Defense", "aseer", "04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files"),
    # Design / Electrical
    (r"ZD-0101", "aseer", "03_Design_Files/Electrical/Lighting_Design"),
    (r"ZD-0067", "aseer", "03_Design_Files/Electrical/Fire_Alarm_Suppression"),
    (r"ZD-0084", "aseer", "03_Design_Files/Electrical/Current_Condition_MDP"),
    (r"ZD-0088", "aseer", "03_Design_Files/Electrical/ATS_Assessment"),
    (r"ZD-0089", "aseer", "03_Design_Files/Electrical/Containment_Assessment"),
    (r"ZD-0090", "aseer", "03_Design_Files/Electrical/Current_Condition_MDP"),
    (r"ZD-0091", "aseer", "03_Design_Files/Electrical/Earthing_Lightning"),
    (r"ZD-0092", "aseer", "03_Design_Files/Electrical/UPS_Assessment"),
    (r"COMPLIANCE.*UNDERSTANDING", "aseer", "03_Design_Files/Electrical/Compliance_Understanding"),
    (r"BMS", "aseer", "03_Design_Files/Electrical/BMS"),
    # DD Gate Submittals
    (r"1G-0002", "aseer", "02_Submittals/01_DD_Gate/MEP"),
    (r"1G-0009", "aseer", "02_Submittals/01_DD_Gate/Architecture"),
    (r"1E0-1G-0002", "aseer", "02_Submittals/01_DD_Gate/Electrical"),
    # Prequalifications
    (r"PQ-0136", "aseer", "24_Subcontractors/Furniture_Anaroque/01_Prequalification"),
    (r"PQ-0138", "aseer", "24_Subcontractors/Setwork_Saudi_Emaar/01_Prequalification"),
    (r"PQ-0139", "aseer", "24_Subcontractors/Setwork_BTT/01_Prequalification"),
    (r"PQ-0133", "aseer", "24_Subcontractors/Electrical_PQ/01_Prequalification"),
    (r"PQ-0134", "aseer", "24_Subcontractors/Electrical_PQ/01_Prequalification"),
    (r"PQ-0132", "aseer", "24_Subcontractors/Civil_PQ/01_Prequalification"),
    (r"PQ-0131", "aseer", "24_Subcontractors/Civil_PQ/01_Prequalification"),
    (r"PQ-0130", "aseer", "24_Subcontractors/Civil_PQ/01_Prequalification"),
    # Site Instructions
    (r"SI 01", "aseer", "04_Docs/05_SIs/05.1_Issued_by_CG"),
    (r"SI-", "aseer", "04_Docs/05_SIs/05.1_Issued_by_CG"),
    # Daily Reports
    (r"Daily Report", "aseer", "00_Status/Daily_Reports"),
    (r"Daily Progress", "aseer", "00_Status/Daily_Reports"),
    # Contracts / Invoices
    (r"INV-", "aseer", "00_Contracts/Invoices"),
    (r"INVOICE", "aseer", "00_Contracts/Invoices"),
    (r"Fasah", "aseer", "00_Contracts/Invoices"),
    (r"AGREEMENT.*ICT", "aseer", "00_Contracts"),
    (r"GBH Letter", "aseer", "00_Contracts/Correspondence"),
    # Meeting Minutes
    (r"Minutes Of Metting", "aseer", "00_Status/Meeting_Minutes"),
    (r"MOM", "aseer", "00_Status/Meeting_Minutes"),
    # Demolition / Architecture
    (r"Demolition", "aseer", "03_Design_Files/Architecture/Demolition"),
    (r"MSRA", "aseer", "03_Design_Files/Architecture/Demolition"),
    (r"Dismantling", "aseer", "03_Design_Files/Architecture/Demolition"),
    # FF&E / Flooring
    (r"PORCELAIN", "aseer", "03_Design_Files/FF&E_Material_Boards"),
    (r"GUBI", "aseer", "03_Design_Files/FF&E_Material_Boards"),
    (r"A2742", "aseer", "03_Design_Files/FF&E_Material_Boards"),
    (r"TECHNICAL.*DATA.*SHEET", "aseer", "03_Design_Files/FF&E_Material_Boards"),
    # Audit
    (r"Audit Report", "aseer", "04_Docs/10_Test_and_Inspection"),
    # Design Phase Tracker
    (r"Design_Phase_Deliverables_Tracker", "aseer", "00_Status"),
    (r"MOC-Aseer-Report", "aseer", "00_Status"),
    # SOW / Scope
    (r"SCOPE OF WORK", "aseer", "24_Subcontractors"),
    (r"TransOrient", "aseer", "24_Subcontractors"),
    (r"Appendix A", "aseer", "24_Subcontractors"),
    # TFP Engineering
    (r"TFP_Engineering", "aseer", "04_Docs/02_Plans_and_Procedures/02.2_Project_Execution_Plan/01_Source_Files"),
    # DDD / Design Studies
    (r"DDD-DS", "aseer", "03_Design_Files/Architecture"),
    (r"DS02", "aseer", "03_Design_Files/Architecture"),

    # === ZAMZAM ===
    (r"ZAM-NWC-CTR-DOC", "zamzam", "04_Docs/02_Plans_and_Procedures"),
    (r"ZAM-NWC-CTR-SDR", "zamzam", "04_Docs/02_Plans_and_Procedures"),
    (r"ZAM-NWC-CTR-IR", "zamzam", "04_Docs/10_Test_and_Inspection/IR"),
    (r"ZAM-NWC-CTR-CLR", "zamzam", "04_Docs/10_Test_and_Inspection/Clearance"),
    (r"ZAM-NWC-CTR-MIR", "zamzam", "04_Docs/10_Test_and_Inspection/MIR"),
    (r"فصل خط الحريق", "zamzam", "04_Docs/02_Plans_and_Procedures"),
    (r"مقترح", "zamzam", "04_Docs/02_Plans_and_Procedures"),
    (r"BOQ Mechanical", "zamzam", "00_Contracts/BOQs"),
]


def clean_filename(fname):
    """Strip email ID prefix from filename."""
    return re.sub(r"^\d+_", "", fname)


def route_file(fname, staging_dir):
    src = os.path.join(staging_dir, fname)
    if not os.path.isfile(src):
        return None
    for pattern, project, subpath in ROUTES:
        if re.search(pattern, fname, re.IGNORECASE):
            root = ROOTS.get(project)
            if not root:
                continue
            dst_dir = os.path.join(root, subpath)
            os.makedirs(dst_dir, exist_ok=True)
            clean_name = clean_filename(fname)
            dst = os.path.join(dst_dir, clean_name)
            if os.path.exists(dst):
                base, ext = os.path.splitext(clean_name)
                dst = os.path.join(dst_dir, f"{base}_dup{ext}")
            shutil.copy2(src, dst)
            return (project, subpath, clean_name, os.path.getsize(dst))
    return None


def main():
    results = {"aseer": [], "zamzam": [], "jabal_omar": [], "unrouted": []}
    for fname in sorted(os.listdir(STAGING)):
        fpath = os.path.join(STAGING, fname)
        if not os.path.isfile(fpath):
            continue
        # Skip images
        if fname.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".mp4", ".glb")):
            continue
        result = route_file(fname, STAGING)
        if result:
            proj, sub, clean, size = result
            results[proj].append((clean, sub, size))
        else:
            results["unrouted"].append(fname)

    print("=== ROUTING RESULTS ===")
    for proj in ["aseer", "zamzam", "jabal_omar"]:
        print(f"\n--- {proj.upper()} ({len(results[proj])} files) ---")
        for fname, sub, size in sorted(results[proj]):
            print(f"  {fname} -> {sub} ({size//1024}KB)")

    print(f"\n--- UNROUTED ({len(results['unrouted'])} files) ---")
    for f in results["unrouted"]:
        print(f"  {f}")


if __name__ == "__main__":
    main()
