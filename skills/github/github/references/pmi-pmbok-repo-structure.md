# PMI PMBOK Repository Structure for Construction/Museum Projects

## When to Use

When creating a GitHub repository for a construction, museum, or infrastructure project organized by PMI PMBOK knowledge areas rather than by file type or discipline.

## Folder Structure

```
{project-name}-pm/
├── README.md
├── .gitignore
├── 00_Project_Overview/
│   ├── PROJECT_MEMORY.md
│   └── project_scope_summary.md
├── 01_Integration_Management/
│   ├── Project_Charter/
│   ├── DMP_Design_Management_Plan/
│   └── Change_Management/
├── 02_Scope_Management/
│   ├── Architecture/
│   ├── MEP/
│   ├── AV_IT/
│   ├── Structural/
│   ├── Exhibition/
│   └── SOW_Scope_of_Work/
├── 03_Schedule_Management/
│   ├── Master_Programme/
│   ├── Submission_Schedules/
│   └── Progress_Reports/
├── 04_Cost_Management/
│   ├── BOQ/
│   ├── Invoices/
│   └── Budget/
├── 05_Quality_Management/
│   ├── QA_QC_Plans/
│   ├── Specifications/
│   └── Inspection_Reports/
├── 06_Resource_Management/
│   ├── HR_CVs/
│   ├── Mobilization/
│   └── Subcontractors/
├── 07_Communications_Management/
│   ├── Correspondence/
│   ├── Meeting_Minutes/
│   └── Email_Archive_Index/
├── 08_Risk_Management/
│   ├── Risk_Registers/
│   ├── HSE_Plans/
│   └── Mitigation_Plans/
├── 09_Procurement_Management/
│   ├── Contracts/
│   ├── Proposals/
│   └── Prequalifications/
└── 10_Stakeholder_Management/
    ├── RACI_Matrix/
    ├── Stakeholder_Plan/
    └── Approvals/
```

## PMI PMBOK Knowledge Area Mapping

| Folder | PMBOK Area (6th Ed) | PMBOK Domain (7th Ed) |
|--------|---------------------|----------------------|
| 01_Integration_Management | Integration Management | Planning, Delivery |
| 02_Scope_Management | Scope Management | Planning |
| 03_Schedule_Management | Schedule Management | Planning, Delivery |
| 04_Cost_Management | Cost Management | Planning, Delivery |
| 05_Quality_Management | Quality Management | Delivery |
| 06_Resource_Management | Resource Management | Team, Delivery |
| 07_Communications_Management | Communications Management | Stakeholder, Delivery |
| 08_Risk_Management | Risk Management | Uncertainty |
| 09_Procurement_Management | Procurement Management | Delivery |
| 10_Stakeholder_Management | Stakeholder Management | Stakeholder |

## .gitignore for Construction Projects

```
# CAD/BIM files
*.dwg
*.dxf
*.rvt
*.rfa
*.rte
*.rft
*.dgn
*.nwd
*.nwf
*.nwc

# Design files
*.skp
*.3dm
*.3ds
*.max
*.c4d
*.blend

# Large binaries
*.pdf
*.zip
*.7z
*.rar
*.tar.gz

# Environment
.venv/
venv/
.env
__pycache__/
*.pyc
.DS_Store
Thumbs.db

# Office temp files
~$*
*.tmp
```

**Note:** For PDFs under 5MB that are key management documents (DMP, SOW, contracts), use Git LFS or include them directly. For large PDFs, create markdown summary files instead.

## README Template

```markdown
# {Project Name} — Project Management Repository

**Client:** {Client} | **Contractor:** {Contractor}
**Status:** {Current phase}

## Project Overview

{2-3 sentence description}

## Repository Structure

This repository is organized by the 10 PMI PMBOK Knowledge Areas (6th Edition), mapped to PMBOK 7th Edition domains. Each knowledge area folder contains discipline-specific subfolders where applicable.

| Folder | PMBOK Area | Contents |
|--------|-----------|----------|
| 00_Project_Overview | — | Project memory, scope summary |
| 01_Integration_Management | Integration | DMP, project charter, change management |
| 02_Scope_Management | Scope | SOWs by discipline, drawing lists |
| 03_Schedule_Management | Schedule | Master programme, submission schedules, progress reports |
| 04_Cost_Management | Cost | BOQ, invoices, budget |
| 05_Quality_Management | Quality | QA/QC plans, specifications, inspection reports |
| 06_Resource_Management | Resources | HR/CVs, mobilization, subcontractors |
| 07_Communications_Management | Communications | Correspondence, meeting minutes, email archive |
| 08_Risk_Management | Risk | Risk registers, HSE plans, mitigation plans |
| 09_Procurement_Management | Procurement | Contracts, proposals, prequalifications |
| 10_Stakeholder_Management | Stakeholder | RACI matrix, stakeholder plan, approvals |

## Key Contacts

| Role | Name | Organization |
|------|------|-------------|
| {Role} | {Name} | {Org} |

## Current Status

{Key milestones, open issues, next actions}
```

## Workflow

1. Create repo: `gh repo create {name} --private --description "..." --clone`
2. Create folder structure (use `mkdir -p` for all 10 areas + subfolders)
3. Copy key documents from project OneDrive/SharePoint into appropriate folders
4. For large PDFs (>5MB), create markdown summary files instead of copying the PDF
5. Write README.md with project overview, PMI mapping, contacts, status
6. Write .gitignore excluding CAD/BIM binaries
7. `git add . && git commit -m "Initial commit: {Project} PM repository organized by PMI PMBOK knowledge areas" && git push`

## Pitfalls

- **25GB+ project folders cannot be pushed directly** — only include key management documents (DMP, SOW, registers, contracts, reports). Exclude CAD, Revit, and raw design files.
- **OneDrive EDEADLK** — When copying from OneDrive paths, write to `/tmp/` first, then copy to the repo directory. OneDrive file locks cause `cp` to hang.
- **PDFs bloat the repo** — For large PDF collections, include only the latest revision of key documents. Create markdown summaries for the rest.
- **Subagent timeout on large repos** — Creating the structure and copying files for a 1,000+ file repo may take 10+ minutes. The subagent may time out at 600s. Check if the commit was made before the timeout — partial progress is normal.
