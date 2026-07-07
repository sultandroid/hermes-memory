# Plan: Project Register Creation & File MD Caching System

## Problem
- Many BIM projects lack Excel tracking registers (Submittal Log, Drawing Register, BOQ, etc.)
- Scanning project files to extract metadata is expensive (labor tokens)
- Information about project stakeholders (client, consultant, contractor) is scattered across files

## Solution: Two-Phase System

---

## Phase A: File MD Caching (Foundation)

### Concept
Every time a file is scanned/analyzed by a labor, create a **sidecar .md file** with extracted metadata. Next time the same file is encountered, read the MD cache instead of re-scanning.

### MD Cache Format
```
path/to/file.pdf.md
---
file: original_filename.pdf
type: Submittal
date: 2026-05-28
project: Aseer Museum
code: ASR-SAM-KP-CV-PACK-SITE-001
subject: "Key Personnel CV Submittal Pack"
parties: [Samaya, CG, MoC]
revision: Rev 01
status: Submitted
checksum: abc123...
summary: 2-3 sentence description
---
```

### Storage Location
Sidecar `.pdf.md` files stored alongside originals:
```
BIM/Project/Subfolder/file.pdf
BIM/Project/Subfolder/file.pdf.md    ← cache
```

Benefits:
- Zero re-scan cost
- grep-able metadata
- Version control friendly
- Works offline

### Python Library: `pymdown` or `python-frontmatter`
Use `python-frontmatter` (pip: `python-frontmatter`) for YAML frontmatter parsing/writing — lightweight, no heavy deps.

### Workflow
1. Labor analyzes file → extracts metadata
2. Writes `.pdf.md` sidecar with YAML frontmatter + body summary
3. Watchdog phase 2-5 reads cache if exists, skips re-analysis

---

## Phase B: Project Register Creation

### Process for Each Project Without Registers

#### Step 1: Discover Project Identity
Scan project files (MD files, CONSTITUTION.md, PROJECT_MEMORY.md, emails, contracts) to extract:
- **Client/Owner** (e.g., NWC for Zamzam, MoC for Aseer)
- **Main Contractor** (Samaya Investment)
- **Design Consultant** (Wael Al-Masri, NRS, etc.)
- **Project Manager / Consultant** (CG, ACE PMC, etc.)
- **Project codes** (P0639, ID121, etc.)
- **Scope summary** (what the project covers)

#### Step 2: Create Standard Register Set
For each project, create the relevant Excel registers:

| Register | Contents | Created For |
|---|---|---|
| **Submittal Log** | All submittals (DOC, MAR, SDR, RFI, etc.) | Every project |
| **Drawing Register** | All drawings with rev control | Projects with CAD/Revit |
| **Material Register** | Materials submitted/approved | Projects with MARs |
| **RFI Log** | All RFIs raised | Every project |
| **Invoice Register** | All invoices received | Projects with financials |
| **Contract Register** | All contracts/POs | Every project |
| **BOQ** | Bill of Quantities | Projects with BOQ data |

#### Step 3: Populate from MD Cache + Existing Files
- Read all `.pdf.md` sidecar files in the project
- Extract structured data into the appropriate register
- For files without MD cache, scan them (labor) → create cache → add to register

#### Step 4: Standard Register Template
```
Header Row:
Date | Document Code | Title/Subject | Type | From | To | Status | File Path | Remarks

Data Row:
2026-05-28 | ASR-SAM-KP-CV-001 | Key Personnel CV Submittal | Submittal | Samaya | CG | Submitted | Docs/file.pdf | Rev 01
```

---

## Phase C: Skill Creation

Create a skill `project-register-manager` that codifies:
1. How to scan a project and discover its identity
2. How to create MD sidecar files
3. How to create/update Excel registers
4. Standard register templates
5. How to read existing MD cache

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Labor Workflow                            │
│                                                             │
│  New File Detected                                          │
│    ├─ Has .md cache? → Read cache (fast)                     │
│    └─ No cache → Analyze file → Write .pdf.md cache          │
│                                                             │
│  Register Update                                             │
│    ├─ Read all .md caches in project                         │
│    ├─ Map data to register columns                           │
│    ├─ Append new row to Excel register                       │
│    └─ Save                                                   │
│                                                             │
│  New Project (No Registers)                                  │
│    ├─ Scan project identity files (MD, contracts, etc.)      │
│    ├─ Create standard register set with project info          │
│    ├─ Populate from existing .md caches                      │
│    └─ Ready for ongoing updates                              │
└─────────────────────────────────────────────────────────────┘
```

## Technology Choices
- **Frontmatter parsing:** `python-frontmatter` (`pip install python-frontmatter`)
- **Excel manipulation:** `openpyxl` (already installed)
- **Labor:** Claude Code for analysis, Kimi for lightweight tasks
- **Storage:** Sidecar .md files alongside originals

## Implementation Order
1. Install `python-frontmatter`
2. Create MD cache writer/reader utility
3. Create skill `project-register-manager`
4. Test: pick one project without registers, scan it, create registers
5. Integrate with watchdog (Phase 2-5)
