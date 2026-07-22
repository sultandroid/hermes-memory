---
name: subcontractor-sow-audit
description: Audit subcontractor SOWs against Project SOW, ER, Appendix A/B, and Compliance Matrix. Build 3-layer system (SOW, submission plan, tracker).
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [sow, compliance, audit, subcontractor, aseer]
    related_skills: [compliance-system, subcontractor-procurement, specialist-register]
---

# Subcontractor SOW Compliance Audit

## When to Use

- User asks to audit all subcontractor SOWs against project requirements
- User asks "are all SOWs compliant with the contract?"
- User asks to check what's missing per package
- User asks to build a complete SOW/submission plan/tracker system

## The 5 Governing Sources

| Source | Abbrev | File | What it covers |
|--------|--------|------|----------------|
| Project SOW | PS | `6380_KMS_RPT_PM_AS_00006` | Package scope, deliverables, exclusions |
| Employer's Requirements | ER | `00_Project_Charter/er_document.md` | Performance criteria, codes, systems |
| Appendix A Interface Matrix | ApxA | `03_Plans/15_Subcontractor_Deliverables/project_sow_appendix_a_b_extraction.md` | RACI split between Fit Out and MoC |
| Appendix B Package Map | ApxB | Same file as ApxA | Package recognition and hierarchy |
| Compliance Matrix | CM | `Technical_Office/Compliance_System/compliance_matrix.md` | Spec→supplier→PQ compliance status |

## The 3-Layer System

Every specialist package gets 3 folders in the repo:

| Layer | Path | Content |
|-------|------|---------|
| SOW | `03_Scope/<name>/README.md` | Scope summary, filed SOW docs, exclusions, compliance gaps |
| Submission Plan | `02_Schedule/<name>/README.md` | Planned submissions with dates, review durations, status |
| Submission Tracker | `Technical_Office/Submission_Tracker/<name>/README.md` | Live log of actual submissions and CG responses |

### Status conventions
- ✅ SOW filed in repo (actual documents present)
- 🟢 SOW approved (exists on OneDrive, not yet filed in repo)
- 🟡 Draft RACI only (no formal package SOW)
- ❌ Missing

## Audit Procedure

### Step 1: Read the governing sources
```bash
# Project SOW summary
read_file 03_Scope/sow_summary.md

# ER summary
read_file 03_Scope/er_summary.md

# Appendix A/B extraction
read_file 03_Plans/15_Subcontractor_Deliverables/project_sow_appendix_a_b_extraction.md

# Compliance Matrix
read_file Technical_Office/Compliance_System/compliance_matrix.md

# SOW/RACI register (existing SOW status per package)
read_file 01_Registers/subcontractor_sow_raci_register.md

# Package register (OneDrive folder map)
read_file 01_Registers/subcontractor_package_register.md

# SOW control system (issue gates)
read_file 03_Plans/15_Subcontractor_Deliverables/subcontractor_sow_control_system.md

# Conflict matrix (open interface issues)
read_file 03_Plans/15_Subcontractor_Deliverables/SOW_RACI_Conflict_Matrix.md
```

### Step 2: For each package, check against each source
1. Read the package's SOW (from `03_Scope/<name>/` or OneDrive `24_Subcontractors/<name>/`)
2. Read the governing source requirement
3. Mark: ✅ Compliant · 🟡 Partial · ❌ Non-compliant · ⚪ Not assessed
4. Document specific gaps with source reference

### Step 3: Create/update the 3-layer folders
- `mkdir -p 03_Scope/<name>/` — write README.md with scope summary, filed docs, gaps
- `mkdir -p 02_Schedule/<name>/` — write README.md with planned submissions
- `mkdir -p Technical_Office/Submission_Tracker/<name>/` — write README.md with live log

### Step 4: Update the registers
- `specialist_register.md` — add SOW/Plan columns with folder paths
- `subcontractor_sow_raci_register.md` — update status to "filed in repo"
- `subcontractor_package_register.md` — update with repo file paths

### Step 5: Write the audit report
Save to `Technical_Office/Submission_Tracker/SOW_Compliance_Audit.md`. Structure:
- Per-package section with source-by-source table
- Open interface conflicts (from SOW/RACI Conflict Matrix)
- Compliance gaps affecting specialists
- Roll-up counts
- Priority actions table

## Common Gaps Found in Practice

| Source Ref | Requirement | Often Missing From |
|------------|-------------|-------------------|
| ApxA 4.02 | Lighting spares 1 year (Fit Out R) | ZNA SOW |
| ApxA 2.13 | Media/AV software by MoC (excluded) | Rawasin SOW |
| ApxA 4.01 | AV hardware spares 1 year (Fit Out R) | Rawasin SOW |
| ApxA 2.12, 3.01-3.05 | Content/copyright/translation by MoC | Graphics SOW |
| ER §2.4.D | Oddy testing for all materials | Oddy Lab not appointed |
| ER §3.0 | MEP installation | MEP Contractor not awarded |
| PS §3 | Interactives, setworks, joinery | No specialists appointed |

## Open Interface Conflicts (from SOW/RACI Conflict Matrix)

| ID | Issue | Affected Packages |
|----|-------|-------------------|
| SRC-001 | Fit-Out umbrella vs specialist responsibility | Exhibition Fit-Out + 6 packages |
| SRC-002 | FF&E vs joinery boundary | FF&E, Fit-Out |
| SRC-003 | Rigging vs structural certification | Rigging, Structural |
| SRC-004 | Object mount integration | Showcases, Rigging, Structural |
| SRC-005 | Stramp/terrace boundary | Structural, Landscaping |
| SRC-006 | Authority submission lead | FLS, Structural, Landscaping, MEP |

## Filing SOW Documents from OneDrive

When a SOW exists on OneDrive but not in the repo:

```bash
# Find the SOW files
find "/Volumes/MIcro/Work/Aseer-Museum/24_Subcontractors/<name>/" -type f -not -name "._*" | head -20

# Copy to repo
cp "/Volumes/MIcro/Work/Aseer-Museum/24_Subcontractors/<name>/<file>" "03_Scope/<name>/<file>"
```

Then update:
1. `03_Scope/<name>/README.md` — add filed docs table
2. `specialist_register.md` — change SOW status to ✅
3. `subcontractor_sow_raci_register.md` — change status to "filed in repo"
4. `SOW_Compliance_Audit.md` — update the audit

## Pitfalls

- **SOW exists on OneDrive but not in repo** — the SOW register may say "package SOW exists" meaning it's on OneDrive. Check `24_Subcontractors/<name>/` before marking as missing.
- **Appendix A exclusions are often not documented in package SOWs** — MoC responsibilities (text, media, copyright, mounts) must be explicitly excluded in each package SOW.
- **Spares obligations** — ApxA 4.01-4.03 assign 1-year spares to Fit Out for AV, lighting, and interactives. These are often missing from package SOWs.
- **Interface conflicts block SOW finalisation** — 6 open conflicts (SRC-001 through SRC-006) need PM decisions before affected SOWs can move from draft to approved.
- **Compliance gaps are not the same as SOW gaps** — a package can have a compliant SOW but still have an open compliance gap (e.g. AD Engineering SOW is compliant, but GAP-MEP-001 for MEP installer remains).
- **The 3-layer system is empty by default** — creating the folders and READMEs is the first pass. Populating them with actual content (filed SOW PDFs, real submission dates, CG response logs) is the ongoing work.

## Verification

After completing an audit:
1. Verify all 3 folders exist for each package: `ls -d 03/Scope/*/`, `ls -d 02/Schedule/*/`, `ls -d Technical_Office/Submission_Tracker/*/`
2. Verify `specialist_register.md` has SOW/Plan columns with correct paths
3. Verify `SOW_Compliance_Audit.md` roll-up counts match the actual data
4. Run `git status` to confirm all new files are tracked
