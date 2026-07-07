---
name: key-personnel-cv-submittal-pack
title: Key Personnel CV Submittal Pack — Aseer Museum & Samaya Projects
description: Create formal CV submittal packs for project key personnel following the standard project template. HTML-only output (no PDF — user generates from browser). All DC-controlled fields left blank.
triggers:
  - User asks to create CV submittal pack, CV submission pack, or key personnel submittal
  - User says "make CVs Submittles package"
  - User says "CV submittal" for a team in the Aseer Museum project
  - Adding new personnel to the Key Personnel Register that need a formal pack
---

# Key Personnel CV Submittal Pack — Aseer Museum (Project 3092)

## Template Source

The HTML template lives at:
```
Docs/09_Registers/Key_Personnel_Register/CVs/_archive/HTML/ASR-SAM-KP-CV-PACK-SUST-001.html
```
Use this as the exact reference for structure, CSS, and layout. Do NOT invent a different format.

## Naming Convention

- **Folder:** `Docs/09_Registers/Key_Personnel_Register/CVs/Sustainability Team/`
- **File name:** `{Team Name} · Key Personnel CV Submittal Pack.html`
- **Existing example:** `Samaya Sustainability · Key Personnel CV Submittal Pack · ASR-SAM-KP-CV-PACK-SUST-001.pdf` (the existing pack has a doc number suffix — new packs omit this)

## Document Title & Team Name

- **Title tag:** `{Team Name} · Key Personnel CV Submittal Pack`
- **h1 (cover):** `{Team Name}`
- **doc-strip header:** `{Team Name} · Key Personnel CV Submittal Pack · Page XX of YY`
- **ToC section header:** `{Team Name} — Aseer Regional Museum`
- **Mission Brief:** Each person gets an individual role-based title, but the team name in the mission brief body should use `{Team Name}` consistently

All packs that are part of the same umbrella (e.g. Samaya Sustainability) must use the **same team name** across all packs. Do not invent different names for different sub-teams unless they are truly separate organisations.

## What NOT to Include — DC Handles These

DO NOT fill in any document control metadata:
- **Doc No.** — leave blank (entire cell can be removed from meta-grid and DC block)
- **Revision** — leave blank (remove cell from DC block)
- **Issue Date** — leave blank (remove cell from DC block)
- **Rev + date in doc-strip headers** — do not include `· Rev XX · YYYY-MM-DD` suffix

The Document Controller assigns these. Never add placeholders like `[TBD]` or `[TBD by DC]` — just remove the field entirely or leave it empty.

## PDF Generation

**Do NOT generate PDFs.** The user prints to PDF from their browser (Chrome headless or manual). Only produce the HTML file.

## Document Structure

| Page | Content |
|------|---------|
| 01 | Cover page: logo strip, title, meta-grid (Project/Contract, Submitted to, Issued by, Reference, Status), DC block (empty DC fields removed), QC Sign-Off block, Contents line |
| 02 | Table of Contents — Personnel Summary by Role table |
| 03–04 | Person 1 CV: Part 1 (Professional Summary, Mission Brief, Coordination Scope, Core Competencies, Skills) + Part 2 (Professional Experience, Education, Certifications, Languages) |
| 05–06+ | Person 2 CV: same structure |

Each person gets 2 pages minimum. Use 3 pages only if experience is extensive (e.g. 35+ year career).

## Critical: Mission Brief Accuracy

The **Aseer Regional Museum · Mission Brief** section is the most scrutinised field. It MUST be tailored to the person's actual scope per their proposal. Rules:
- Read the person's actual proposal/quotations PDF to extract their real scope
- Do NOT use generic "Samaya Sustainability Team" boilerplate
- Each person's role, responsibilities, and reporting line must reflect their contract/proposal
- Reference the correct SoW clause (typically §13.9) and compliance framework (Mostadam / SBC 1001)
- If the person is from a sub-consultant (e.g. SG Group), name their company in the role title

## Copying CV Content

Extract text from the person's existing CV PDF using:
```bash
pdftotext "/path/to/CV.pdf" - 2>/dev/null
```

Key sections to fill per person:
- **Name, role, contact** (phone, email, location, key certifications)
- **Professional Summary** — 3-5 sentence career overview from their CV
- **Mission Brief** — see accuracy rules above
- **Aseer Coordination Scope** — 4-6 bullet points of their project responsibilities
- **Core Competencies** — comma-separated list of skills
- **Technical Skills & Software**
- **Professional Experience** — employer, title, dates, key projects (from CV)
- **Education** — degrees, institutions, years
- **Certifications & Languages**

## Logos

Logos are at `../_assets/logos/` relative to the Sustainability Team folder:
- `moc.png` (MoC / Employer)
- `pmc_ace.png` (ACE Moharram Bakhoum / PMC)
- `cg.png` (Consultancy Group / Consultant)
- `samaya.png` (Samaya Investment / Main Contractor)

## QC Sign-Off (standard across all packs)

| Role | Name |
|------|------|
| Prepared By | Eng. Mohamed Sultan — Samaya Technical Office Manager |
| Review By QC | Eng. Abd Elmohaymen Medhat — Samaya QA/QC Manager |
| Approved By | Eng. Adel Darwish — Samaya Acting Project Director |

## Project Reference Data

- **Project:** Aseer Regional Museum · Project 3092
- **Contract:** 0010003521 (MoC ↔ Samaya)
- **Submitted to:** CG — Eng. Mohammed Elbaz (Acting PM) · Abdrabo Shahin (Sr Structure Engineer)
- **Issued by:** Samaya Investment — via Samaya Technical Office
- **Reference:** KP Reg MOC-ASEER-SIC-1K0-KP-0001 · DMP §5.1.2 · SoW §5.5 · §13.7 / §13.8
- **Status text:** "Pending CG review and onward MoC approval. Once approved, KP cannot be removed without prior written MoC approval."

## Pitfalls

- **Do NOT add doc numbers, revision, or dates** — DC fills these. Remove the entire cell from meta-grid and DC block rather than leaving it empty.
- **Do NOT generate PDFs** — user does that from browser. Only deliver HTML.
- **Mission Brief must be per-proposal accurate** — the user will check against actual quotation/proposal PDFs. Do not guess or use generic text.
- **All sub-team packs under the same umbrella (e.g. Sustainability) must share the SAME team name** — do not use different names like "Aseer Sustainability Consultancy" vs "SAS Sustainability Framework" if they're all under Samaya Sustainability.
- **Each person's role in Mission Brief must be specific to their actual contract scope** — a sustainability advisor who does reporting/advisory gets a different brief from a sustainability expert who does design-phase technical work.
