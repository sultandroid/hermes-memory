---
name: project-initializer
description: Initialize new BIM projects with complete Aseer-standard folder structure and default Excel registers. Creates all subfolders, empty register files with cover pages, PROJECT_MEMORY.md, and odoo structure.
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [bim, project-setup, initialization, folder-structure, registers]
    related_skills: [samaya-technical-office, project-register-manager]
---

# Project Initializer — New BIM Project Setup

## When to Use
- User says "new project" or "create project folder for..."
- User says "initialize project" or "setup [project name]"
- A new project needs the standard BIM folder structure

## 🔴 IMPORTANT: Check Existing Structure First

Before creating anything, check if the project already exists. If it does, find the existing folder and ONLY create missing folders — do NOT duplicate or overwrite anything. Never delete existing data.

## Exact mkdir Commands

### Step 1: Get Project Info
Ask the user (or extract from context):
- Project name (English + Arabic)
- Project code (if any)
- BIM directory name

### Step 2: Create Folder Structure
Run this exact set of mkdir commands:

```bash
PROJ="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/[PROJECT_DIR]"

# Top-level folders
mkdir -p "$PROJ/As-Built Docs"
mkdir -p "$PROJ/B.O.Q"
mkdir -p "$PROJ/Completed Tender Package From NRS"
mkdir -p "$PROJ/Contracts"
mkdir -p "$PROJ/Design Files"
mkdir -p "$PROJ/Email_Archive"
mkdir -p "$PROJ/Invoices"
mkdir -p "$PROJ/MOBILIZATION"
mkdir -p "$PROJ/Reports & Meetings"
mkdir -p "$PROJ/Scripts/notes" "$PROJ/Scripts/output" "$PROJ/Scripts/plans"
mkdir -p "$PROJ/Specs & Datasheet/GENERAL SPECIFICATIONS" "$PROJ/Specs & Datasheet/Project Codes"
mkdir -p "$PROJ/Time Schedules"

# Submittals (no apostrophe)
mkdir -p "$PROJ/Submittals/Arch" "$PROJ/Submittals/AV Drawings" "$PROJ/Submittals/BIM"
mkdir -p "$PROJ/Submittals/Consultant Submittel Review" "$PROJ/Submittals/Design Submital"
mkdir -p "$PROJ/Submittals/DOCS" "$PROJ/Submittals/Life and Safety" "$PROJ/Submittals/Mep"
mkdir -p "$PROJ/Submittals/Reports" "$PROJ/Submittals/Showcases" "$PROJ/Submittals/Struc"
mkdir -p "$PROJ/Submittals/Title Block"

# Revit Files
mkdir -p "$PROJ/Revit Files/Cad" "$PROJ/Revit Files/Clash Reports" "$PROJ/Revit Files/Excel Sch"
mkdir -p "$PROJ/Revit Files/fbx" "$PROJ/Revit Files/FBX_RVT"
mkdir -p "$PROJ/Revit Files/Nwc" "$PROJ/Revit Files/Nwd" "$PROJ/Revit Files/Nwf"
mkdir -p "$PROJ/Revit Files/Pdf" "$PROJ/Revit Files/Refrences" "$PROJ/Revit Files/Rfa"
mkdir -p "$PROJ/Revit Files/Rvt"

# Docs numbered subfolders
for i in 00 01 02 03 04 05 06 07 08 09 10 11 12; do
  case $i in
    00) name="Project_Charter";;
    01) name="Contracts_and_ER";;
    02) name="Plans_and_Procedures";;
    03) name="Submittals";;
    04) name="RFIs";;
    05) name="SIs";;
    06) name="Authority_Submissions";;
    07) name="Reports";;
    08) name="Meeting_Minutes";;
    09) name="Registers";;
    10) name="Test_and_Inspection";;
    11) name="Correspondence";;
    12) name="Compliance_and_Audit";;
  esac
  mkdir -p "$PROJ/Docs/${i}_${name}"
done
mkdir -p "$PROJ/Docs/99_Archive" "$PROJ/Docs/99_Reference"

# odoo
mkdir -p "$PROJ/odoo/01_Initiation" "$PROJ/odoo/02_DD_Stage" "$PROJ/odoo/03_Procurement"
mkdir -p "$PROJ/odoo/04_Manufacturing" "$PROJ/odoo/05_Execution" "$PROJ/odoo/06_Handover"
```

### Step 3: Create PROJECT_MEMORY.md
Create a basic PROJECT_MEMORY.md with project info placeholder.

### Step 4: Create Default Register Files
Use `~/.hermes/scripts/register_generator.py` to create the initial register set in `Docs/09_Registers/`:
```bash
python3 ~/.hermes/scripts/register_generator.py "[PROJECT_DIR]" --force
```

### Step 5: Populate Report Templates from Aseer Reference Project
⚠️ **CRITICAL: Do NOT create generic templates from scratch.** The user's standard is to copy the bilingual (Arabic/English) report templates from the Aseer Museum project, which has the canonical set.

Copy the following template files from the Aseer project into the new project:

```bash
ASEER="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum"
PROJ="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/[PROJECT_DIR]"

# Create sub-folder structure for reports
mkdir -p "$PROJ/Docs/07_Reports/07.1_Progress_Reports"
mkdir -p "$PROJ/Docs/07_Reports/07.2_QAQC_Reports"
mkdir -p "$PROJ/Docs/07_Reports/07.3_Clash_Reports"

# Copy bilingual template files (each has .md + .xlsx pair)
cp "$ASEER/Docs/07_Reports/07.1 Progress Reports/_TEMPLATE_Weekly_Progress_Report.md" \
   "$PROJ/Docs/07_Reports/07.1_Progress_Reports/_TEMPLATE_Weekly_Progress_Report.md"
cp "$ASEER/Docs/07_Reports/07.1 Progress Reports/_TEMPLATE_Weekly_Progress_Report.xlsx" \
   "$PROJ/Docs/07_Reports/07.1_Progress_Reports/_TEMPLATE_Weekly_Progress_Report.xlsx"
cp "$ASEER/Docs/07_Reports/07.2 QA-QC Reports/_TEMPLATE_QAQC_Log.md" \
   "$PROJ/Docs/07_Reports/07.2_QAQC_Reports/_TEMPLATE_QAQC_Log.md"
cp "$ASEER/Docs/07_Reports/07.2 QA-QC Reports/_TEMPLATE_QAQC_Log.xlsx" \
   "$PROJ/Docs/07_Reports/07.2_QAQC_Reports/_TEMPLATE_QAQC_Log.xlsx"
cp "$ASEER/Docs/07_Reports/07.3 Clash Reports/_TEMPLATE_Clash_Report.md" \
   "$PROJ/Docs/07_Reports/07.3_Clash_Reports/_TEMPLATE_Clash_Report.md"
cp "$ASEER/Docs/07_Reports/07.3 Clash Reports/_TEMPLATE_Clash_Report.xlsx" \
   "$PROJ/Docs/07_Reports/07.3_Clash_Reports/_TEMPLATE_Clash_Report.xlsx"
```

After copying, **adapt each template** to the new project:
- In `.md` files: replace `مشروع متحف عسير الإقليمي` → new project Arabic name, `Aseer Regional Museum` → new project English name, project-specific reference codes
- In `.xlsx` files: open in Excel and update title/header references (or copy as-is and edit on first use)

Also create the 16 standard register subfolders matching Aseer's system:
```bash
for reg in AV_Interface_Register BCF_Register Design_Risk_Register Drawing_Register \
           Key_Personnel_Register Master_Register_Index Material_Sample_Register_MSR \
           Penetration_Register Procurement_Schedule Project_Risk_Register Specialist \
           Subcontractor_Prequalification_Register Subcontractor_RFI_Register \
           Submittal_Tracker_IFC_Log Transmittal_Register VE_Register; do
  mkdir -p "$PROJ/Docs/09_Registers/$reg"
done
```

### Step 6: Create PROJECT_MEMORY.md (bilingual)
Create a bilingual (Arabic/English) PROJECT_MEMORY.md with project info:
- Arabic text leading, English following
- Project name, client, consultant, contractor, scope, phase
- Use the Aseer PROJECT_MEMORY.md as a reference for section structure

### Step 7: Bilingual Document Template

When creating project documents (PEP, VE reports, audit reports):
- Arabic is the LEAD language (RTL)
- English follows (LTR)
- Use `<html lang="ar" dir="rtl">`
- Font stack: `'Tajawal','Calibri','Carlito',sans-serif`
- Load `samaya-technical-office` skill for the full bilingual document standard
- Use `.sheet` framing, `.doc-strip`, `.meta-grid`, `.qc-block`, `.logo-strip`
- Include auto-paginate JavaScript
- Reference `PEP_PROJECT_EXECUTION_PLAN.rev0*.html` for the exact Samaya template style
- **Preferred generation method:** Python `execute_code` (fast, reliable, immune to model-switch interruptions). See `references/audit-report-structure.md` under `samaya-technical-office` for the 11-domain audit framework template.
- **When to use Claude Code:** For PhD-depth content (lifecycle cost analysis, risk heatmaps) — generate content with Claude, wrap in Python HTML shell.

### Step 8: Update Project Index
Add the new project to `~/.hermes/scripts/bim_project_index.json`.

## Verification
After setup, verify:
- [ ] All top-level folders exist
- [ ] Submittals/ has 12 subfolders
- [ ] Docs/ has numbered 00-12 + 99 subfolders
- [ ] Docs/07_Reports/ has 07.1/.2/.3 subfolders with TEMPLATE files copied
- [ ] Docs/09_Registers/ has 16+ register subfolders + Excel register files
- [ ] Revit Files/ has 12 subfolders
- [ ] Scripts/ has notes/output/plans
- [ ] Specs & Datasheet/ has GENERAL SPECIFICATIONS + Project Codes
- [ ] odoo/ has 01-06
- [ ] PROJECT_MEMORY.md exists (bilingual)

## Pitfalls

- **Do NOT create generic templates from scratch.** Always copy from the Aseer project's existing bilingual templates.
- **Adapt, don't just copy.** After copying templates, update project name, codes, and references.
- **Check both .md and .xlsx template pairs.** The markdown is the bilingual form; the xlsx is the working spreadsheet.
