---
name: key-personnel-cv-pack
title: Key Personnel CV Submittal Pack — Aseer Museum Project
description: Create formal CV submittal packs for project key personnel following the branded HTML template. Used for CG/MoC personnel approval submissions across all teams (BIM, MEP, Site, Sustainability).
triggers:
  - User asks to create/submit CV submittal pack for a team
  - User asks to add new team members to Key Personnel Register
  - User asks to prepare personnel documentation for CG/MoC review
  - User references the "CV pack template" or "CV submittal pack" format
---

# Key Personnel CV Submittal Pack — Aseer Museum Project

## Overview

Formal CV submittal packs are required for all key personnel before MoC approval. Existing packs sit at:

```
Docs/09_Registers/Key_Personnel_Register/CVs/{Team Name}/
```

HTML source files (user generates PDFs via Chrome — do NOT convert to PDF yourself).

## Template Structure

### File Naming
```
{Team Name} · Key Personnel CV Submittal Pack.html
```
No document numbers in the filename — leave `[TBD]` in the DC block for the Document Controller.

### Document Structure (Pages)

| Page | Content |
|------|---------|
| p.01 | Cover + Document Control + QC Sign-Off |
| p.02 | Table of Contents — Personnel Summary by Role |
| p.03–04 | CV 01 Part 1 & 2 |
| p.05–06 | CV 02 Part 1 & 2 (if second person) |

### Template Elements

Every page has:
- **doc-strip**: `{Team Name} · Key Personnel CV Submittal Pack · Page XX of Y · Rev 00 · YYYY-MM-DD`
- **logo-strip**: 4 logos (MoC/Employer, ACE /PMC, CG/Consultant, Samaya/Main Contractor)
- **Cover**: h1 = team name, subtitle = "Aseer Regional Museum · Project 3092"
- **meta-grid**: Project/Contract, Submitted to (CG contacts), Issued by (Samaya TO), Reference (KP Reg, DMP, SoW), Doc No. (`[TBD by DC]`), Status
- **DC block**: Document Control table + QC Sign-Off (Mohamed Sultan/TO Mgr, Abd Elmohaymen Medhat/QC Mgr, Adel Darwish/Proj Dir)
- **Summary table** (p.02): #, Name, Project Role, Page

### CV Page Format (2 pages per person)

**Part 1**: Name + role, contact bar, Professional Summary, **Mission Brief** (see below), Coordination Scope, Core Competencies, Technical Skills

**Part 2**: Continued header, Professional Experience (role by role with employer, dates, location), Education, Certifications, Languages

## ⚠ CRITICAL RULES

### Team Name MUST Be "Samaya Sustainability"
Both the h1 and title tag must use `Samaya Sustainability` — **NOT** the specific consultancy/team name. This keeps naming consistent with the existing SUST-001 pack (Dr. Ehab Foda). The user corrected this explicitly.

### Mission Brief MUST Be Identical Across All Team Members
Do NOT write person-specific mission briefs. Use one unified `Samaya Sustainability Team` mission brief for all CVs in the pack:

```
<b>Samaya Sustainability Team.</b> Reports to the Samaya Acting Project Director (Eng. Adel Darwish). Provides specialised sustainability expertise in support of the Aseer Regional Museum Sustainability Strategy per <b>SoW §13.9</b> and Employer's Requirements <b>Mostadam / SBC 1001</b> compliance. Coordinates across all design phases with the Samaya Technical Office (Eng. Mohamed Sultan), the in-house BIM Unit (Dr. Waleed Salah), and the NRS Design Lead / Architect of Record on passive design, envelope thermal performance, daylighting, water efficiency, landscape sustainability, embodied-carbon tracking, and IFC sustainability sign-off via the Aconex Project Master Log.
```

### No Document Numbers
Use `[TBD]` in the DC block "Document No." field and `[TBD by DC]` in the meta-grid "Doc No." field. The Document Controller assigns numbers.

### HTML Source Only
Provide HTML source files only — do NOT convert to PDF. The user generates PDFs themselves via Chrome headless.

## Workflow

### Step 1: Extract CV Content
Use `pdftotext` to extract text from the team members' PDF CVs.

### Step 2: Build HTML from Template
Copy the existing pack's HTML (`_archive/HTML/ASR-SAM-KP-CV-PACK-SUST-001.html`) as the base. Modify:
- Title tag → `Samaya Sustainability · Key Personnel CV Submittal Pack`
- doc-strip → consistent team name prefix
- h1 → `Samaya Sustainability`
- meta-grid + DC block → `[TBD by DC]` / `[TBD]`
- Table of Contents → list all team members
- CV pages → replace with extracted content for each person

### Step 3: Place in Correct Folder
```
Docs/09_Registers/Key_Personnel_Register/CVs/Sustainability Team/
```
Alongside the existing packs.

### Step 4: Create Odoo Task
Create a sub-task under "Projects Plans" (parent task) in the Aseer Museum project:
- Task name: "Sustainability" (or team name)
- Stage: 02 Design Development (DD) Stage (ID 36 on Samaya Odoo)
- Parent: Projects Plans task
- Description: HTML timeline with deliverables and pending items

## Reference IDs

| Item | Value |
|------|-------|
| Project | Aseer Regional Museum · Project 3092 |
| Contract | 0010003521 (MoC ↔ Samaya) |
| KP Register | MOC-ASEER-SIC-1K0-KP-0001 |
| BEP | MOC-ASEER-SIC-1K0-PL-0015 Code B |
| Submitted to | CG — Eng. Mohammed Elbaz (Acting PM) · Abdrabo Shahin (Sr Structure Engineer) |
| Samaya TO Mgr | Eng. Mohamed Sultan |
| QC Manager | Eng. Abd Elmohaymen Medhat |
| Acting Proj Dir | Eng. Adel Darwish |
| Logos | `Docs/09_Registers/Key_Personnel_Register/CVs/_assets/logos/` (moc.png, pmc_ace.png, cg.png, samaya.png) |
