---
name: project-plan-management
category: project-management
title: Project Plan Management — Markdown Library & Compliance System
description: Convert project management plans (DMP, PEP, BEP, HSE, PQP, SMP, Risk, Procurement, Resource, Communication, Stakeholder, Mobilization) from PDF/Word to structured Markdown, build a consolidated cross-plan analysis, and design a compliance automation system.
triggers:
  - User asks to store all project plans in Markdown format
  - User asks to convert plans from PDF/Word to Markdown
  - User asks to build a compliance system from project plans
  - User asks to find overlaps, conflicts, or gaps across plans
  - User asks to create a plan library in a PM repository
  - User asks to automate plan compliance checking
---

# Project Plan Management — Markdown Library & Compliance System

Load this skill when the task involves converting project management plans to Markdown, building a plan library, creating cross-plan consolidated analysis, or designing a compliance automation system.

## 1. Plan Inventory — Standard Set

For a construction/museum fit-out project (D&B), the standard plan set includes:

| # | Plan | Doc Code Prefix | Typical Sections |
|---|------|----------------|------------------|
| 01 | **DMP** — Design Management Plan | PL-0029 | Project context, contractual framework, design control, scope summary, technical specs, BIM, testing, handover |
| 02 | **Stakeholder** — Stakeholder Management Plan | PL-0020 | Identification, analysis, engagement planning, communication requirements, RACI, integration |
| 03 | **Communication** — Communication Plan | PL-0018 | Objectives, communication matrix, meeting protocols, reporting cadence, escalation, channels |
| 04 | **HSE** — HSE Plans (10+ sub-plans) | PL-0036 to PL-0054 | Site security, welfare, fire prevention, emergency response, temp electrical, heat stress, lifting ops, training, etc. |
| 05 | **PEP** — Project Execution Plan | PL-0015 | Project overview, org chart, phases, design integration, procurement, construction, quality, HSE, risk, handover |
| 06 | **BEP** — BIM Execution Plan | PL-0015 Att | PIR, EIR, MIDP, TIDPs, LOD matrix, CDE structure, clash detection, approval workflow |
| 07 | **Mobilization** — Mobilization Plan | MI-0001 / ZD-0051 | Phases, personnel, equipment, temporary facilities, site establishment, HSE, demobilization |
| 08 | **Risk** — Risk Management Plan | — | Risk approach, RBS, identification, qualitative/quantitative analysis, response planning, register format |
| 09 | **Procurement** — Procurement Plan | PQ-0096 | Strategy, make-or-buy, contract types, RFQ→award process, vendor prequalification, schedule |
| 10 | **Resource** — Resource Management Plan | PL-0030 | OBS, roles & responsibilities, resource calendars, team development, resource leveling |
| 11 | **Quality (PQP)** — Project Quality Plan | PL-0055 | QMS framework, document control, design QC, procurement quality, ITP, NCR, audits, handover quality |
| 12 | **SMP** — Sustainability Management Plan | 47718_SMP | Sustainability policy, SBC 1001 compliance, energy/water/materials IEQ, construction sustainability |

## 2. Directory Structure

```
03_Plans/
├── 01_DMP/              # Design Management Plan
├── 02_Stakeholder/      # Stakeholder Management Plan
├── 03_Communication/    # Communication Plan
├── 04_HSE/              # HSE Plans (one file per sub-plan)
├── 05_PEP/              # Project Execution Plan
├── 06_BEP/              # BIM Execution Plan
├── 07_Mobilization/     # Mobilization Plan
├── 08_Risk/             # Risk Management Plan
├── 09_Procurement/      # Procurement Plan
├── 10_Resource/         # Resource Management Plan
├── 11_Quality/          # Project Quality Plan
├── 12_SMP/              # Sustainability Management Plan
└── 99_Consolidated/     # Cross-plan analysis + compliance system
```

## 3. Markdown Conversion Pattern

### 3.1 YAML Frontmatter (every plan file)

```yaml
---
last_updated: YYYY-MM-DD
owner_agent: <agent name>
status: active | superseded | closed
source: <doc number or OneDrive path>
doc_code: MOC-MUS-ASE-1K0-PL-XXXX
revision: Rev.XX
cg_status: A | B | C | D | Submitted
---
```

### 3.2 Source Extraction

- **PDFs**: Use `pymupdf` (Python) to extract text. Copy PDFs to `/tmp/` first to avoid OneDrive lock issues.
- **DOCX**: Use `python-docx` or extract via `pandoc`.
- **Existing MD**: Copy directly from archive folders.
- **Empty/0-byte PDFs**: These are OneDrive placeholder files. Find the real file in the repo's `00_Project_Charter/` (text extracts) or use the OneDrive web UI to download.
- **Verify extraction completeness**: After extracting a PDF, check line count vs page count. Rule of thumb: ~40-50 lines per page for text-heavy PDFs. If the extract is suspiciously short (e.g. 358 lines for 72 pages), re-extract with `pdftotext -layout`.

### 3.3 Structure Rules

- **Tables over paragraphs** — every requirement, role, schedule, or matrix becomes a Markdown table.
- **Source traceability** — every claim links to an approved source (ER, SOW, Contract clause, approved submittal).
- **Section numbering** — match the original document's section structure where possible.
- **CG status** — include the approval status (Code A/B/C/D) and date.
- **Cross-references** — link to other plans in the library (e.g., "see DMP §6 for BIM requirements").

### 3.4 Parallel Conversion (via delegate_task)

For large plan sets (10+ plans), delegate conversion to parallel sub-agents:

```python
# Pattern: one sub-agent per plan or per plan group
delegate_task(
    goal="Create comprehensive [Plan Name] Markdown document...",
    context="Source files at [paths], project context, key requirements..."
)
```

Each sub-agent should:
1. Read source files (PDF text, existing MD, reference docs)
2. Read project context (AGENTS.md, existing registers)
3. Write structured Markdown with YAML frontmatter
4. Include tables for all structured data
5. Reference other plans where applicable

## 4. Consolidated Analysis

After all plans are converted, create a cross-plan analysis document with the following sections:

### 4.1 Plan Inventory & Coverage

List every plan with file count, line count, and status. Map each plan to PMBOK knowledge areas to assess coverage completeness.

### 4.2 Overlaps to Identify

| Overlap Type | Example | Resolution |
|-------------|---------|------------|
| Same requirement in multiple plans | Document control in DMP, Communication, PQP, BEP, PEP, Resource | Reference the governing plan; de-duplicate |
| Same role in multiple plans | Project Manager in PEP, Resource, RACI | Ensure consistent role definition |
| Same process in multiple plans | Change control in DMP, Contract, Quality | Identify which plan governs |
| Same deliverable in multiple plans | As-built drawings in DMP, PEP, PQP, BEP | Map to single handover checklist |

**Common overlap clusters found in practice:**
- Document control / CDE management — appears in 6+ plans (DMP, Comm Plan, PEP, BEP, PQP, Resource)
- Design review & approval — appears in 4 plans (DMP, PEP, PQP, Comm Plan)
- Quality control & inspection — appears in 5 plans (PQP, DMP, PEP, Procurement, BEP)
- Testing & commissioning — appears in 5 plans (DMP, PEP, PQP, Comm Plan, SMP)
- Handover deliverables — appears in 6 plans (DMP, PEP, PQP, BEP, Comm Plan, SMP)
- Risk management — appears in 5 plans (RMP, PEP, Procurement, Resource, Mobilization)

### 4.3 Conflicts to Identify

| Conflict Type | Example | Resolution |
|-------------|---------|------------|
| Different review periods | DMP says 14 calendar days, Communication says 14 working days | Verify against contract/ER — these differ by ~40% |
| Different handover dates | PEP says 01 Mar 2027, all other plans say 30 Sep 2026 | Resolve with PM/Contracts — 5-month gap is critical |
| Different LOD requirements | DMP says LOD 300, BEP requires LOD 350/400 | Update DMP to reference BEP |
| Different approval authorities | DMP says MoC approves sub-consultants, Procurement says no privity to MoC | Reconcile: MoC approves appointment, but contractual relationship is with Contractor only |
| Different terminology | "Design Development" vs "RIBA Stage 3" | Create glossary |
| Parallel audit regimes | PQP defines Samaya quality audits; BEP defines MoC BIM audits | Coordinate audit schedules and share results |

### 4.4 Gaps to Identify

#### Missing Plans
Check for these common missing plans and flag them:
- Schedule Management Plan (no standalone plan; PEP §5 covers scheduling but lacks detail)
- Cost Management Plan (no standalone plan; PEP §14 covers financial management but lacks EVM)
- Change Management Plan (changes handled via contract clauses only)
- Commissioning Plan (DMP §7 covers T&C but no standalone integration plan)
- Security Management Plan (museum security requirements spread across ER and Comm Plan)
- IT/AV Integration Plan (AV/IT systems are critical path but no integration plan)
- Training Plan (handover training required but no standalone plan)

#### Content Gaps Within Plans
For each plan, check for these common missing sections:

| Plan | Common Gaps |
|------|-------------|
| DMP | Design freeze/gate criteria, design change impact assessment, reference to SMP |
| Communication | Crisis communication protocol, handover communication shift, stakeholder feedback measurement |
| PEP | EVM methodology, schedule contingency management, formal change control procedure, lessons learned process |
| BEP | COBie data schema, federation strategy, model review checklist, BCF workflow |
| Mobilization | Demobilization trigger criteria, site handover protocol, interface with HSE plans |
| RMP | Quantitative risk analysis results, risk trigger conditions, risk report format, link to change management |
| Procurement | Supplier performance evaluation criteria, expediting process, logistics plan |
| Resource | Training budget/plan, resource histogram, key person replacement procedure |
| PQP | Supplier quality requirements, off-site fabrication inspection, quality audit schedule |
| SMP | Mostadam scorecard tracking, embodied carbon assessment, waste management plan, sustainability reporting format |

#### Cross-Plan Integration Gaps
Check for missing links between plans:

| Missing Link | Between | Impact |
|-------------|---------|--------|
| Risk register not linked to procurement lead times | RMP ↔ Procurement | Procurement risks not in risk register |
| Quality KPIs not linked to risk triggers | PQP ↔ RMP | Quality failures don't trigger risk escalation |
| Resource plan not linked to mobilization schedule | Resource ↔ Mobilization | Resource ramp-up not aligned |
| Sustainability not in procurement evaluation | SMP ↔ Procurement | Sustainability criteria not in supplier selection |
| BIM deliverables not linked to quality ITPs | BEP ↔ PQP | Model review not integrated with quality inspections |
| Communication SLAs not linked to risk triggers | Comm Plan ↔ RMP | Communication failures don't escalate as risks |
| HSE plans not referenced in mobilization | HSE ↔ Mobilization | HSE setup not coordinated with site establishment |
| Stakeholder changes not linked to communication updates | Stakeholder ↔ Comm Plan | Stakeholder changes don't trigger comm plan updates |

### 4.5 Linked Requirements (Cross-Plan Dependency Chains)

Map the end-to-end dependency chains that span multiple plans:

**Design → Procurement → Construction Chain:**
```
DMP §4 (Scope) → Procurement §7 (Packages) → Procurement §9 (Schedule) → 
Mobilization §9 (Delivery) → PQP §7 (Inspection) → PEP §8 (Installation) → 
DMP §7 / PQP §9 (T&C)
```

**BIM → Quality → Handover Chain:**
```
BEP §3 (MIDP) → BEP §5 (LOD) → BEP §7 (Clash Detection) → 
PQP §6 (Design QC) → BEP §6.6 (Weekly Updates) → DMP §8 / BEP §3 (As-Built)
```

**Risk → Procurement → Schedule Chain:**
```
RMP §4 (RBS) → RMP §9 (Risk Register) → Procurement §11 (Risk Mgmt) → 
Procurement §9 (Schedule) → PEP §5 (Master Schedule)
```

**Stakeholder → Communication → Escalation Chain:**
```
Stakeholder §4 (Engagement) → Stakeholder §6 (Assessment) → 
Communication §3 (Matrix) → Communication §7 (Escalation) → RMP §9 (Risk Register)
```

**Sustainability → Procurement → Quality Chain:**
```
SMP §2.2 (Objectives) → SMP §7 (Materials) → SMP §9 (Sustainable Procurement) → 
Procurement §8 (Evaluation) → PQP §7 (Verification) → SMP §11 (Commissioning)
```

**HSE → Mobilization → Construction Chain:**
```
HSE Plans → Mobilization §12 (HSE Setup) → Mobilization §6 (Site Estab.) → 
PEP §11 (HSE Mgmt) → PQP §9 (HSE Verification)
```

### 4.6 Compliance Obligations Register

After identifying all requirements, build a compliance obligations register organized by category:

| Category | Description | Example Obligations | Typical Count |
|----------|-------------|---------------------|---------------|
| **Contractual** | Derived from contract clauses and ERs | Design liability, PMC review period, IFC certification, sub-consultant approval | ~10 |
| **Regulatory** | Derived from codes and standards | SBC 201/401/501/601/801/1001, NFPA, MOI, CITC, SEC, Oddy Test, Mostadam | ~15 |
| **Quality** | Derived from PQP KPIs | First-time approval ≥85%, NCR closure ≤14 days, ITP hold points 100% | ~8 |
| **Communication** | Derived from Comm Plan SLAs | Report on-time ≥95%, submittal turnaround ≤14 wd, RFI closure ≤7 wd | ~6 |
| **Sustainability** | Derived from SMP targets | VOC ≤0.5 mg/m³, waste diversion ≥60%, gallery T 21±1°C, Mostadam Silver 45+ | ~12 |
| **HSE** | Derived from HSE plans | Fire extinguisher distribution, hot work permits, induction 100%, zero LTI | ~10 |
| **BIM** | Derived from BEP | LOD compliance, weekly model updates, clash reports, as-built model, COBie | ~9 |

Each obligation entry should include: ID, description, source plan, contract/code reference, verification method, and frequency.

## 5. Compliance System Architecture

### 5.1 Data Model

```
Plan → Section → Requirement → Rule → Check → Status
```

- **Plan**: A management plan document (DMP, PEP, etc.) with code, version, status, category
- **Section**: A chapter/section within the plan (numbered, with parent for nesting)
- **Requirement**: A specific obligation with description, source_ref, category, priority, compliance_type (automated/manual/hybrid), verification_method, and linked_requirement_ids for cross-plan dependencies
- **Rule**: Machine-readable version of the requirement with rule_type, logic (type, field, operator, value, unit), parameters (source, collection, filter), schedule, and auto_resolve flag
- **Check**: A single evaluation result with status (pass/fail/warning/pending/error/not_applicable/overridden), actual_value, expected_value, evidence links, and override tracking
- **Status**: Pass/Fail/Warning/Pending/Error/Not Applicable/Overridden

### 5.2 Rule Types

| Rule Type | Description | Example | Evaluation Strategy |
|-----------|-------------|---------|-------------------|
| **duration_check** | Verifies a duration is within limits | "14 calendar day review period" | Compare timestamps |
| **status_check** | Verifies a status equals expected value | "Submittal status = Approved" | Compare status field |
| **count_check** | Verifies count meets threshold | "≥ 85% first-time approval rate" | Count + percentage |
| **threshold_check** | Verifies numeric value within range | "VOC ≤ 0.5 mg/m³" | Compare numeric value |
| **boolean_check** | Verifies a condition is true/false | "ITCA is independent of Contractor" | Check boolean field |
| **date_check** | Verifies a date is on/before deadline | "Handover by 30 Sep 2026" | Compare dates |
| **cross_ref_check** | Verifies consistency across data sources | "Risk register includes procurement risks" | Cross-reference IDs |
| **composite_check** | Combines multiple sub-checks | "All handover deliverables complete" | Aggregate sub-checks |

### 5.3 Rule Definition Format (YAML)

Each rule is a YAML file with these sections:

```yaml
rule_id: "R-{PLAN}-{NNN}"
version: 1
enabled: true

metadata:
  plan: "{Plan Name}"
  plan_code: "{Document Code}"
  section: "{Section Number and Title}"
  requirement: "{Requirement text}"
  source: "{Source Reference}"
  priority: "critical|high|medium|low"
  category: "approval|quality|document|schedule|compliance|communication|resource|risk|sustainability|hse"

evaluation:
  type: "duration_check|status_check|count_check|threshold_check|boolean_check|date_check|cross_ref_check|composite_check"
  data_source: "aconex|odoo|register|bcf|manual"
  collection: "{data collection name}"
  filter:
    field: "value"
  fields:
    start: "{start field}"
    end: "{end field}"
  condition:
    operator: "eq|neq|gt|gte|lt|lte|in|between"
    value: "{expected value}"
    unit: "{unit if applicable}"

actions:
  on_pass:
    - type: "update_status"
      target: "compliance_dashboard"
      status: "pass"
  on_fail:
    - type: "create_alert"
      severity: "critical|high|medium|low"
      channel: "email|dashboard|slack"
      recipients: ["email@example.com"]
    - type: "create_odoo_task"
      project: "Aseer Museum"
      task_type: "corrective_action|preventive_action|verification_task"
      priority: "urgent|high|normal|low"
      assignee: "role_name"
      due_in_days: 2
  on_warning:
    - type: "create_alert"
      severity: "warning"
      channel: "dashboard"

schedule:
  type: "daily|weekly|monthly|on_event|on_demand"
  time: "HH:MM"
  timezone: "Asia/Riyadh"
```

### 5.4 Rule Categories by Plan (Estimated Counts)

| Plan | Rule Category | Example Rules | Est. Count |
|------|--------------|---------------|------------|
| DMP | Design Control | Review period, IFC certification, NOC type, scope change | 25 |
| DMP | Technical | Code compliance, MasterSpec tailoring, ER override | 15 |
| Stakeholder | Engagement | Engagement gap closure, KPI achievement | 12 |
| Communication | Reporting | Report on-time, SLA compliance, Aconex usage | 15 |
| HSE | Safety | Fire extinguisher distribution, hot work permits, induction | 20 |
| PEP | Integration | WBS completeness, interface management, assumptions | 18 |
| BEP | BIM | LOD compliance, weekly model updates, clash reports | 15 |
| Mobilization | Resources | Site office readiness, personnel deployment, HSE induction | 12 |
| RMP | Risk | Register updates, review cadence, contingency tracking | 10 |
| Procurement | Supply Chain | Lead time, bidder minimum, MoC approval | 18 |
| Resource | Staffing | Histogram accuracy, training completion | 8 |
| PQP | Quality | First-time approval rate, NCR closure, ITP hold points | 20 |
| SMP | Sustainability | VOC limits, Oddy test, waste diversion, Mostadam score | 15 |
| **Total** | | | **~213** |

### 5.5 Integration Points

| System | Integration | Purpose | Technology |
|--------|------------|---------|------------|
| **Odoo** | Task creation per requirement | Each requirement → Odoo task with deadline, assignee, checklist | Odoo XML-RPC / REST API |
| **Aconex (CDE)** | Submittal data fetch | Verify review periods, NOC types, submittal completeness | Aconex REST API |
| **Submittal Register** | Cross-reference doc codes | Verify each required submittal exists and is approved | Excel/MD parser |
| **Risk Register** | Link risks to plan requirements | Risk non-compliance → risk register entry | RMP data model |
| **Compliance Dashboard** | Real-time status per plan | Green/amber/red per plan, per section, per requirement | React + FastAPI |

### 5.6 Odoo Task ↔ Check Status Synchronization

| Odoo Task Status | Compliance Check Impact |
|-----------------|------------------------|
| `draft` | Check status remains `fail` |
| `in_progress` | Check status → `warning` (acknowledged) |
| `done` | Re-run check; if pass → `pass`; if still fail → escalate |
| `cancelled` | Check status → `fail` (override required) |

### 5.7 Dashboard Views

| View | Content | Purpose |
|------|---------|---------|
| **Project Overview** | Overall pass rate, per-plan bars, critical failure count | Executive summary |
| **Plan Detail** | Per-section rule status table with pass/fail/warning | Drill-down investigation |
| **Timeline/Trend** | 30-day compliance trend line | Track improvement/decline |
| **Action Items** | Open issues grouped by severity with Odoo task links | Daily action management |

### 5.8 Implementation Roadmap

| Phase | Weeks | Activities | Milestone |
|-------|-------|------------|-----------|
| 1 — Foundation | 1–4 | Rule repo, data model, plan parser, rule generator, rule store, basic rule types, schedule checker | 50 core rules running daily |
| 2 — Integration | 5–8 | Aconex API connector, Odoo API connector, submittal register parser, task generation, bidirectional sync, alert engine | Full integration, 100+ rules |
| 3 — Dashboard | 9–12 | FastAPI backend, React frontend (4 views), auth, deployment | Full dashboard live, 213 rules |
| 4 — Optimization | 13–16 | Rule tuning, auto-resolve, composite rules, cross-ref rules, performance, docs, training | System fully operational |

### 5.9 Technology Stack

| Layer | Recommended | Alternative (Lighter) |
|-------|-------------|----------------------|
| Backend | Python 3.11+ / FastAPI | Same |
| Database | PostgreSQL | SQLite |
| Rule Engine | Custom Python + JSON Schema | Same |
| Task Queue | Celery + Redis | APScheduler (in-process) |
| Frontend | React + Next.js | Streamlit |
| Charts | Chart.js | — |
| CDE Integration | Aconex REST API | — |
| Odoo Integration | Odoo XML-RPC / REST API | — |
| CI/CD | GitHub Actions | — |
| Monitoring | Prometheus + Grafana | — |
| Containerization | Docker + Docker Compose | Single server |

## 6. Critical Rule — Repo is Single Source of Truth

**The PM repo (`~/aseer-museum-pm/03_Plans/`) is the single source of truth for all plan content.** OneDrive HTML/DOCX files are derived outputs, not authoritative sources.

### 6.1 Before Editing Any Plan File

1. **READ the repo version first** — check `~/aseer-museum-pm/03_Plans/<NN_Plan>/<plan_name>.md`
2. **Check `08_Document_Index/approved_plans.md`** for CG approval status and revision history
3. **Check `08_Document_Index/00_compliance_system.md`** for the master obligations register
4. **Only then** edit the OneDrive HTML/DOCX if needed — but the repo MD is the canonical version

### 6.2 Framing Alignment

The repo SMP uses a **code-compliance-based approach**, not a rating-target approach:
- "strategic pivot from a rating-target approach to a code-compliance-based approach"
- "While Mostadam practices are followed for excellence, final certification is subject to ministerial review and is not treated as a contractual performance bond"
- Silver 45+ is a "trajectory" / "readiness" target, not the primary framing

**Never use points-chasing language** (SILVER/GOLD targets, "stretch goals", "credit pool", "~X points") as the primary framing. Always lead with code compliance (SBC 1001 + Mostadam Manual), then reference certification trajectory as secondary.

### 6.3 Human Tone — No AI Fingerprints

**This user strongly prefers documents that read like a human engineer wrote them.** Every plan, register, and deliverable must be scrubbed of AI-sounding language before delivery.

#### 6.3.1 Symbols to Remove

| Symbol | Replace With | Example |
|--------|-------------|---------|
| `§` | "Section" or "Clause" | `SBC 1001 Section 4` not `SBC 1001 §4` |
| `→` | "to" or "through" | `Design to Commissioning` not `Design → Commissioning` |
| `—` (em dash) | ` - ` (space-hyphen-space) | `SBC 1001 - Saudi Green Building Code` |
| `·` (middle dot) | `, ` or ` / ` | `energy, water, materials` not `energy·water·materials` |

#### 6.3.2 Prose Rules

- **No "shall be"** — use active voice: "We keep a register" not "A register shall be maintained"
- **No "establishes the framework"** — just say what the document does
- **No "strategic pivot"** or "paradigm shift" — plain language
- **No "overarching"** — remove it
- **No "comprehensive"** — remove it or replace with specific description
- **No "in accordance with"** — use "per" or "to"
- **No "as per"** — use "per"
- **No "demonstrably"** — remove it
- **Short sentences** — break long clauses into separate sentences
- **Active voice** — "The designer certifies" not "It is certified by the designer"
- **Plain language** — "cuts environmental impact" not "minimises environmental impact through resource efficiency"

#### 6.3.3 Authenticity Touches

- Add **a few small typos** (5-8 across a 900-line document) — missing 's', transposed letters, double spaces. Not too many, just enough to feel human.
- Inconsistent capitalization is OK in a few places
- Use contractions: "it's" not "it is", "we're" not "we are"
- Write like an engineer talking to another engineer, not a consultant writing a report

#### 6.3.4 DOCX Fix Pattern (Preserve Consultant's Language)

When fixing a consultant's existing DOCX (e.g., Fida's SMP), **do not rewrite the whole document**. Instead:

1. **Identify only the problems** — waste diversion 75%→60%, Oddy 49-day→14-day, points-chasing language
2. **Edit the XML directly** — use zipfile + xml.etree.ElementTree to find and replace exact `<w:t>` element text
3. **Preserve everything else** — keep the consultant's language, formatting, tables, and structure intact
4. **Generate a CR Register Excel** (not Markdown) listing each change with contractual basis

The XML patching approach:
```python
import zipfile, tempfile, shutil, xml.etree.ElementTree as ET

with zipfile.ZipFile(src, 'r') as z:
    xml = z.read('word/document.xml').decode('utf-8')

# Find exact w:t elements and replace
xml = xml.replace(
    '<w:t>Old text here</w:t>',
    '<w:t>New text here</w:t>'
)

# Write back preserving all other files
tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
with zipfile.ZipFile(src, 'r') as zin:
    with zipfile.ZipFile(tmp.name, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'word/document.xml':
                zout.writestr(item, xml.encode('utf-8'))
            else:
                zout.writestr(item, data)
shutil.move(tmp.name, out)
```

### 6.4 ER/SoW Compliance Only Rule

When setting targets or resolving contradictions in the SMP, **comply with ER and SoW only**:
- **Waste diversion**: 60% (SBC 1001 §8, ER §2.4D) — NOT 75% (Mostadam stretch)
- **Oddy aging**: 14-day at 60°C (SoW §1.5, ER §2.4D) — NOT 49-day (Mostadam recommendation)
- **Mostadam tier**: No contractual mandate. Certification subject to ministerial review per SoW §13.9.
- **Rating targets**: Remove all Silver/Gold/Platinum point targets from primary framing. Keep as aspirational trajectory only.

### 6.4 SMP Contradiction Resolution Workflow

When a sustainability consultant (e.g., Fida Noor) submits a scope reduction register that contradicts their own SMP:

1. **Audit** each proposed change against ER, SoW, and DMP — produce item-by-item verdict (Accept / Reject / Partial)
2. **Generate CR Register** as an **Excel file** (not Markdown) with columns: #, Section, Change, Reason/Contractual Basis, Fida Status (☐ Accept / ☐ Reject)
3. **Fix the document** to align with repo's code-compliance framing
4. **Send both** the CR Register Excel + fixed document to the consultant for approval
5. **Update Odoo** task 2947 with progress and link to files

### 6.5 CR Register Format (User Preference)

CR registers for consultant review must be **Excel files**, not Markdown:
- Navy `#1F3864` header with white text
- Columns: #, Section, Change, Reason/Contractual Basis, Fida Status
- Landscape A4, alternating row shading
- Freeze panes on header row
- Each item has ☐ Accept / ☐ Reject checkbox for the consultant to mark

### 6.3 When Editing OneDrive HTML/DOCX

- The repo MD is authoritative — align the HTML/DOCX to match the repo, not the other way around
- After editing, verify by grepping for prohibited framing patterns (SILVER/GOLD as primary targets, points-chasing language)
- Update `CG_STATUS.md` in the OneDrive folder to reflect current status
- Log the work in Odoo task 2947 (Sustainability) with progress update

## 6.6 Post-Approval Plan Audit — Checking Against Latest Project Data

When a plan has been approved (Code A/B) but time has passed, new stakeholders, roles, and requirements emerge that the approved plan doesn't reflect. Before reporting on a plan's accuracy, always audit it against the latest project data.

### Trigger

- User asks "check the [Plan Name] according to latest information"
- A plan was approved weeks/months ago and you need to verify it's still current
- New subcontractors, consultants, or team members have been appointed since plan approval

### Audit Sources (in order)

| Source | What to Check | Location |
|--------|---------------|----------|
| **PROJECT_MEMORY.md** | Latest status updates section — new appointments, role changes, new requirements | `00_Project_Charter/PROJECT_MEMORY.md` or `99_Archive/00_Project_Overview/PROJECT_MEMORY.md` |
| **CG_STATUS.md** (plan folder) | Latest CG response, open comments, resubmission status | `03_Plans/<NN_Plan>/CG_STATUS.md` |
| **Plan audit files** | PMBOK/RIBA gap analysis, residual open gaps | `03_Plans/<NN_Plan>/` — audit `.md` files |
| **Plan source files** | The actual plan document (HTML/DOCX/PDF) | `03_Plans/<NN_Plan>/01_Source_Files/` |
| **Submittal dashboard** | Code C/D items, recently approved items | PROJECT_MEMORY.md submittals section |
| **specialist_register.md** | Tier 1-2 specialist register with MoC approval status | `Technical_Office/Specialist_Management/specialist_register.md` |
| **resource_management_plan.md** | Full team org chart with names, statuses, reporting lines | `03_Plans/10_Resource/resource_management_plan.md` |
| **Review_Email_to_Fida.md** | Adel Darwish's instructions on role naming/titles | `03_Plans/12_SMP/Review_Email_to_Fida.md` |

**CRITICAL: Cross-reference every name against at least two repo sources.** PROJECT_MEMORY.md is a high-level summary and can be wrong on titles, names, and role distinctions (e.g., "Sustainability Manager" vs "Sustainability Specialist", "Adel Darwish" vs "Waris Sultan" as PD).

### Audit Dimensions

#### 1. New Stakeholders / Roles

Cross-reference the plan's stakeholder register against PROJECT_MEMORY.md's latest updates. Look for:

| Signal | What It Means |
|--------|---------------|
| "APPOINTED" | New role exists — add to register, define engagement cadence |
| "REPLACED" | Role holder changed — update org chart, role description |
| "CONTRACT EXECUTED" | New subcontractor — add as T1/T2 specialist |
| "CRITICAL GAP" | Role vacant — add placeholder with TBC status |
| "LEFT" | Role departed — remove or mark as vacated |

#### 2. New Engagement Requirements

Check for new mandates from CG, PMC, or MOC:

| Signal | Impact on Plan |
|--------|----------------|
| "PMC mandates weekly submission" | Add new deliverable to Communication Plan section |
| "CG new numbering system" | Update document control references |
| "CVs requested" | Recruitment in progress — update role status |
| "New reporting format" | Update report templates and cadence |

#### 3. Residual Audit Gaps

Check the plan's PMBOK/RIBA audit file for open gaps. These are non-blocking but should be tracked:

| Severity | Action |
|----------|--------|
| Medium | Note as improvement opportunity for next revision |
| Low | Note as nice-to-have; not urgent |

### Output Format

Present findings as a structured table with:

| Category | Finding | Impact | Action Required |
|----------|---------|--------|-----------------|
| New Stakeholder | AD Engineering (MEP Designer) appointed Jun 21 | Add to register as T1/T2 | Update register, define engagement |
| New Requirement | PMC weekly status presentations mandated | Add to Communication Plan | Add new weekly deliverable |
| Org Change | Project Director replaced | Update org chart | Replace name, update role |
| Residual Gap | Value-Proposition Map missing | Medium | Add in next revision |

### Verdict

| Verdict | Criteria |
|---------|----------|
| Current | No new stakeholders/requirements since approval |
| Needs Minor Update | 1-3 new stakeholders/requirements — register update only |
| Needs Revision | 4+ new stakeholders/requirements, or org chart change, or new CG comments |

### Pitfalls

- **Don't assume the plan is stale just because it's old.** Check actual changes against the plan's content — some plans are comprehensive enough to absorb new roles without structural changes.
- **Don't miss the "LEFT" signal.** When a key person departs (e.g., Project Director), the org chart and RACI need updating even if a replacement is named.
- **Don't forget the Interactive Specialist gap.** A critical vacancy (e.g., Interactive Designer with no replacement) needs a placeholder in the register even if the role isn't filled yet.
- **CG_STATUS.md may be outdated.** The plan's CG status file may not reflect the latest approval. Cross-check against PROJECT_MEMORY.md's submittals dashboard.
- **The plan may have been approved under a different doc code.** Check both PL-0020 and ZD-0020 variants — the numbering scheme may have changed between submission rounds.
- **PROJECT_MEMORY.md is NOT authoritative for personnel names/titles.** It's a high-level summary and can be wrong. Every name must be verified against at least two repo sources:
  - `Technical_Office/Specialist_Management/specialist_register.md` — authoritative for specialist roles
  - `03_Plans/10_Resource/resource_management_plan.md` — authoritative for management roles
  - `03_Plans/12_SMP/Review_Email_to_Fida.md` — contains Adel Darwish's title corrections (e.g., "Sustainability Specialist" not "Manager")
- **"Sustainability Manager" vs "Sustainability Specialist"** — Adel Darwish explicitly instructed "Sustainability Specialist" to avoid creating a dedicated Key Personnel position. PROJECT_MEMORY.md still says "Manager" — don't trust it.
- **Project Director vs Projects Director** — Waris Sultan is project-level PD (Exhibitions). Adel Darwish is Samaya-level Projects Director. They are different roles. The plan should show Waris as PD.
- **Sub-agent output must be verified against repo sources.** Sub-agents don't have access to specialist_register.md or resource_management_plan.md unless you pass them in context. After the sub-agent produces the Rev N+1 HTML, grep for every name and verify against the authoritative sources above.

### Reference

See `references/stakeholder-plan-post-approval-audit.md` for a worked example (Aseer Museum Stakeholder Plan ZD-0020 Rev.02, approved Jun 18-24, audited Jul 13 with 6 new stakeholders identified).

See `references/plan-audit-scmp-zd-0094.md` for a worked example (Subcontract Management Plan ZD-0094 Rev.00 — 12 issues found, verdict: NOT READY for submission).

## 6.7 Producing a Plan Revision (Rev N+1)

After the post-approval audit identifies changes needed, produce the revision systematically.

### Workflow

1. **Audit first** — run §6.6 audit to identify all changes needed
2. **Build the revision** — choose the right approach based on scope:

   **Option A: Manual patching (preferred for targeted revisions)**
   
   For revisions that add/update specific rows, counts, and sections without restructuring the whole document:
   
   a. Copy the source Rev N HTML to the target Rev N+1 path
   b. Apply patches in this order (minimizes conflicts):
      - **Phase 1 — Global**: Title, all page headers (`SMP Rev N` → `SMP Rev N+1`), all footers (`Rev N` → `Rev N+1`), date stamps — use `replace_all=true`
      - **Phase 2 — Cover page**: Revision number, description, date
      - **Phase 3 — TOC**: Snapshot card values (role counts, page counts), section descriptions, compliance notice
      - **Phase 4 — Revision history**: Add new Rev N+1 row
      - **Phase 5 — CG Comment Disposition**: Update disposition chip, add new round rows in the **same table** (never split rounds across separate tables)
      - **Phase 6 — Content sections**: Update counts, add new stakeholders to registers, add new interfaces, add new KPIs, add governance notes
      - **Phase 7 — Communication Plan**: Add new reports/meetings, update report counts
      - **Phase 8 — Final verification**: All page numbers sequential, TOC references match, no orphaned sections
   
   **Pitfall — nested `<section>` tags**: When patching page content, verify the replacement doesn't create nested `<section class="page">`. The old content already opens a `<section>`, and if your replacement also starts with `<section>`, you get invalid nesting. Verify with `grep -n '<section class="page"' file.html`.
   
   **Pitfall — replace_all on common numbers**: `replace_all=True` on `/ 23` can hit unintended targets (table cells, SVG text). Verify after.
   
   **Pitfall — TBC status suffix creep**: After adding new TBC stakeholders, verify no status commentary (`— pending`, `⚠ CRITICAL`) was appended. TBC = just TBC.
   
   **Pitfall — page overflow**: Adding 3+ new table rows can push content past A4 height. Check with `grep -n '<section class="page"'` to count pages, then compare content density.

   **Option B: Delegate to sub-agent (for major restructures)**
   
   For revisions that restructure sections, merge/split pages, or rewrite large portions:
   
   - Pass the full audit findings as context
   - The sub-agent reads the current Rev N HTML, applies all changes, writes Rev N+1 HTML
   - The sub-agent also writes a change log

3. **Update supporting files in parallel** while the HTML build runs:
   - `CG_STATUS.md` — update status from Code C/D to ✅ Approved or new status
   - `PROJECT_MEMORY.md` — update the Code C/D item row to reflect resolution
   - `PMBOK_Structure_Audit.md` — update revision number, close any gaps that were addressed
   - Create `RevNN_Change_Log.md` — document every change with rationale
4. **Verify** — check the output for:
   - All new stakeholders added to register
   - Org chart updated
   - Communication plan updated with new requirements
   - Document control updated (rev number, date, revision history)
   - Stakeholder count updated
   - Any gaps from audit that were closed
   - All page numbers sequential and total correct
   - No AI fingerprints (see §6.3)
   - **CRITICAL: Verify every name against repo sources.** Grep the output for every person's name and cross-check against specialist_register.md and resource_management_plan.md. The sub-agent may have used wrong names/titles from PROJECT_MEMORY.md.

### Change Log Format

```markdown
# Rev NN Change Log — [Plan Name]

**Document:** [Doc Code] Rev NN
**Date:** YYYY-MM-DD
**Status:** [Internal update / CG Resubmission / etc.]

## Changes Made

### 1. Document Control
- Rev: NN-1 → **NN**
- Date: [old] → **[new]**
- Added Rev NN row to revision history

### 2. New Stakeholders Added
| Stakeholder | Tier | Reason |
|-------------|------|--------|
| ... | ... | ... |

### 3. Updated Stakeholders
| Previous | Updated | Reason |
|----------|---------|--------|

### 4. [Other section changes]
...

### 5. Supporting Files Updated
- `CG_STATUS.md` — ...
- `PROJECT_MEMORY.md` — ...
- `PMBOK_Structure_Audit.md` — ...

## Remaining Open Gaps
| Gap | Severity | Notes |
|-----|----------|-------|
```

### Pitfalls

- **The sub-agent may take time** — the HTML is large (2000-3000 lines). Don't wait; update supporting files in parallel.
- **The sub-agent may fail silently** — check for the output file. If it doesn't appear, rebuild manually.
- **Don't forget the change log** — it's the audit trail for the next revision.
- **CG_STATUS.md and PROJECT_MEMORY.md must stay in sync** — if the plan was approved, both files need updating. If one says Code C and the other says Approved, that's a contradiction.
- **The plan may have been approved under a different doc code** — check both PL-XXXX and ZD-XXXX variants. The CG may have renumbered between submission rounds.
- **Sub-agents produce wrong revision tables despite existing instructions** — Even when the workflow says "actual submissions only", sub-agents may copy the old revision table with internal drafts. After the sub-agent finishes, grep the revision table and verify: Rev 00 (Code C), Rev 01 (Code C), Rev 02 (Approved), Rev 03 (this submission). No extra rows. If wrong, fix manually.
- **Sub-agents use wrong personnel names from PROJECT_MEMORY.md** — Sub-agents don't have access to specialist_register.md or resource_management_plan.md unless you pass them in context. Even when you do, they may still use PROJECT_MEMORY.md's wrong names. After sub-agent output, grep for every person's name and cross-check against the authoritative sources. Fix any mismatches.
- **Sub-agents add broken asset references** — When versioning an HTML file (Rev N → Rev N+1), the sub-agent copies the old file including `<img src="assets/...">` references. These assets may not exist in the new location. After sub-agent output, grep for `src="assets/` and verify each path exists. If not, either copy the assets or remove the broken image tags.
- **Cover page still verbose after sub-agent** — The sub-agent may add a long change list to the cover page despite instructions. After sub-agent output, check the cover page description. It should only state which revisions it supersedes and which reference docs it aligns with. No change listing. Fix if needed.

## 6.8 Plan Folder Template Initialization

When setting up a new plan library or initializing empty plan subdirectories, create 4 standard files per folder:

| File | Purpose | Key Fields |
|------|---------|------------|
| `README.md` | Folder overview, purpose, owner, status, contract refs | YAML frontmatter + purpose + owner + status + contract references + linked documents |
| `plan_summary.md` | Overview, key dates, approvals | YAML frontmatter + overview + key dates table + approvals required table |
| `checklist.md` | Compliance checklist vs CONSTITUTION | YAML frontmatter + frontmatter compliance table + content compliance table + repo compliance table |
| `approval_log.md` | Approval dates, sign-offs, revision history | YAML frontmatter + revision history + approval sign-offs + CG response history + key decisions |

Two template formats are available. Use the **simple format** (below) for quick initialization, or the **detailed format** (§6.8.1) when the user explicitly requests a richer template with RACI, PMBOK alignment, and decision log sections.

#### Simple Template Pattern (default)

Every file must have YAML frontmatter:
```yaml
---
last_updated: YYYY-MM-DD
owner_agent: <agent name>
status: active
source: 08_Document_Index/00_plan_tracker.md; 03_Plans/99_Consolidated/project_plan_operating_model.md
---
```

### README.md Structure

```markdown
# {NN_Plan} — {Plan Name}

## Purpose

{One-paragraph description of the plan's function}

## Owner

{Role or person responsible}

## Status

{CG status: Code B / Draft / Submitted / etc.}

## Key Contract References

{SoW §X.X; ER §X.X; Contract §X Art. X}

## Linked Documents

- Plan Tracker: `08_Document_Index/00_plan_tracker.md`
- Operating Model: `03_Plans/99_Consolidated/project_plan_operating_model.md`
- Constitution: `CONSTITUTION.md`

## Folder Contents

| File | Purpose |
|------|---------|
| `README.md` | This file — folder overview and purpose |
| `plan_summary.md` | Overview, key dates, approvals |
| `checklist.md` | Compliance checklist vs CONSTITUTION |
| `approval_log.md` | Approval dates, sign-offs, revision history |
```

### plan_summary.md Structure

```markdown
# {Plan Name} — Plan Summary

## Overview

{One-paragraph description}

## Key Dates

| Event | Date | Status |
|-------|------|--------|
| Draft Complete | TBD | Pending |
| Internal Review | TBD | Pending |
| CG Submission | TBD | Pending |
| CG Approval | TBD | Pending |

## Approvals Required

| Approver | Role | Status |
|----------|------|--------|
| PMC (ACE Moharram-Bakhoum) | Reviewing Authority | Pending |
| CG (Consultant Group) | Technical Approval | Pending |
| MoC (Ministry of Culture) | Final Authority | Pending |

## Linked Documents

- Contract: {SoW §X.X; ER §X.X; Contract §X Art. X}
- Constitution: `CONSTITUTION.md`
- Plan Tracker: `08_Document_Index/00_plan_tracker.md`
```

### checklist.md Structure

Three compliance tables:
1. **Frontmatter Compliance** — `last_updated`, `owner_agent`, `status`, `source`
2. **Content Compliance** — purpose defined, owner identified, contract articles referenced, source traceability, no AI clichés, British English, active voice, no emoji
3. **Repository Compliance** — markdown format, no binary files, append-only, entity isolation, cross-references

### approval_log.md Structure

```markdown
## Revision History

| Rev | Date | Author | Status | Notes |
|-----|------|--------|--------|-------|
| C01 | TBD | {Owner} | Draft | Initial draft |

## Approval Sign-Offs

| Approver | Role | Date | Decision | Reference |
|----------|------|------|----------|-----------|
| PMC | Reviewing Authority | TBD | Pending | |
| CG | Technical Approval | TBD | Pending | |
| MoC | Final Authority | TBD | Pending | |

## CG Response History

| Submission Ref | Rev | Date | CG Code | Comments |
|---------------|-----|------|---------|----------|
| {Doc Ref} | {Rev} | TBD | Pending | — |
```

### Batch Creation Pattern

For 15+ plan folders, use a Python script to generate all files at once:

```python
plans = [
    ("01_DMP", "Design Management Plan", "Design Lead (NRS)", "Code B",
     "SoW §6.22; ER §2.4; Contract §4 Art. 2",
     "Establish design control procedures per RIBA 4 / LOD 400 compliance."),
    # ... all 15 plans
]

for folder, name, owner, status, refs, purpose in plans:
    # Write README.md, plan_summary.md, checklist.md, approval_log.md
    # Each with YAML frontmatter + plan-specific content
```

### Pitfalls

- **Existing READMEs may use a different format** (e.g., folder structure index instead of plan metadata). Check before overwriting — some folders already have READMEs that serve a different purpose.
- **Plan status must match the plan tracker** (`08_Document_Index/00_plan_tracker.md`). Don't guess — read the tracker first.
- **Contract references must be specific** — cite exact SoW/ER/Contract sections, not generic "Contract §4".
- **Owner field should use the role title** (e.g., "BIM Manager (Dr. Waleed Salah)") not just the person's name, so the template stays valid if personnel changes.
- **Approval log starts with current revision** — don't leave it empty. Fill in the known revision from the plan tracker.

#### 6.8.1 Detailed Template Format (advanced)

Use this format when the user explicitly requests a richer template with RACI, PMBOK alignment, decision log, and compliance tracking. This format was specified for a 16-folder initialization across 03_Plans/.

**README.md YAML frontmatter:**
```yaml
---
title: [PLAN_NAME] — [Full Plan Title]
owner_agent: [Responsible Discipline/Agent]
last_updated: YYYY-MM-DD
status: draft | in-review | approved | active
access: read-write
compliance_ref: CONSTITUTION.md §3
---
```

**README.md body:**
```markdown
# [PLAN_NAME] — [Plan Title]

## Metadata

| Attribute | Value |
|-----------|-------|
| Plan Name | [XX_DescriptiveTitle] |
| Owner Agent | [Name/Role] |
| Status | 🟡 Draft (ready for population) |
| Last Updated | YYYY-MM-DD |
| Approval Status | ⏳ Pending PMC Review |
| Contract Reference | SoW §[X.X] / ER Section [X] |

## Purpose

[1-2 sentence description of this plan's purpose per PMBOK framework]

## Key Dates (Estimated)

| Milestone | Date | Status |
|-----------|------|--------|
| Draft Completion | TBD | ⏳ |
| Internal Review | TBD | ⏳ |
| Stakeholder Review | TBD | ⏳ |
| PMC Approval | TBD | ⏳ |
| Implementation | TBD | ⏳ |

## Linked Documents

- Primary: [Link to relevant register or charter section]
- Secondary: [Cross-reference to related plans]
- Supporting: [Reference to OneDrive/Aconex location]

## Contents Index

See files in this directory:
- plan_summary.md — Executive summary & key decisions
- checklist.md — Compliance checklist vs CONSTITUTION + PMBOK
- approval_log.md — Approval dates and sign-offs

---

Status: 🟡 To Be Populated — Awaiting plan content development
```

**plan_summary.md YAML:**
```yaml
---
title: "[PLAN_NAME] — Summary"
owner_agent: "[Agent]"
last_updated: YYYY-MM-DD
status: draft
---
```

Sections: Executive Overview (placeholder), Key Responsibilities (RACI table with Role/Activity/Level columns), Critical Success Factors (3 checkboxes), Known Constraints, Approval Chain table.

**checklist.md YAML:**
```yaml
---
title: "[PLAN_NAME] — Compliance Checklist"
owner_agent: "[Agent]"
last_updated: YYYY-MM-DD
status: active
---
```

Sections:
1. **CONSTITUTION Compliance** — 7 checkboxes (one per compliance workflow step)
2. **PMBOK Knowledge Area Alignment** — 9 checkboxes (Scope, Time, Cost, Quality, Resource, Communications, Risk, Procurement, Stakeholder)
3. **Document Quality Standards** — 6 checkboxes (YAML frontmatter, owner agent, status, cross-links, tables, all sections populated)
4. **Approval Gates** — 3 checkboxes (Draft, Review, Approval)

Footer: `Overall Compliance: 🟡 50% (To Be Completed)`

**approval_log.md YAML:**
```yaml
---
title: "[PLAN_NAME] — Approval Log"
owner_agent: "[Agent]"
last_updated: YYYY-MM-DD
status: active
---
```

Sections:
1. **Approval History** — table with Date, Version, Approver, Status, Comments
2. **Decision Log** — 2 template Decision entries (Date, Decision, Rationale, Approved By, Impact, Status)
3. **Change Requests** — table with Date, Change, Requested By, Status, Resolution

Footer: `Approval Status: 🟡 Draft — Awaiting first review`

**Batch creation for detailed format:** Delegate to a sub-agent via `delegate_task` with the full plan data array and the exact template strings from this section. The sub-agent creates all 64 files (16 folders × 4 files) in a single pass.

**Pitfalls for detailed format:**
- Has more YAML fields (`title`, `access`, `compliance_ref`) than the simple format — don't omit them
- Status indicators: use 🟡 for "Draft", ⏳ for "Pending", ✅ for "Complete" — keep consistent across all 4 files
- When delegating to a sub-agent, pass the exact template strings as context — the sub-agent should not invent its own format
- Verify a sample folder's output after the sub-agent finishes

### 6.9 Populating Existing Templates with Real Data

When templates already exist with placeholder data ("TBD", "Pending") and need to be filled with actual project data, follow this extraction workflow. This is distinct from §6.8 (creating empty templates) — here the templates already exist and need their placeholders replaced with real values.

#### Data Sources (in order of authority)

| Source | What It Provides | Location |
|--------|-----------------|----------|
| **Plan Tracker** | CG status, doc ref, revision, owner, priority, next action | `08_Document_Index/00_plan_tracker.md` |
| **Actual plan files** | Purpose/scope descriptions, section structure, contract references | `03_Plans/<NN_Plan>/<plan_name>.md` |
| **CG status files** | Approval history, CG comment details, reviewer names | `03_Plans/<NN_Plan>/CG_STATUS.md` (if exists) |
| **Change logs** | Revision history, new stakeholders, org changes | `03_Plans/<NN_Plan>/RevNN_Change_Log.md` (if exists) |
| **AGENTS.md** | Project facts, team roster, contract value, handover date | Repo root `AGENTS.md` |

#### Extraction Pattern

For each plan folder, extract these fields from the sources above:

| Template Field | Source | Extraction Rule |
|----------------|--------|-----------------|
| **Purpose** | Plan file §1 or README | First paragraph of the actual plan document. Include section count and scope breadth. |
| **Owner** | Plan tracker + plan file frontmatter | Role title first, person name in parentheses if known. E.g., "BIM Manager (Dr. Waleed Salah)" |
| **Status** | Plan tracker CG status column | Exact CG code + qualifier. E.g., "Code B — Approved w/ comments" or "Draft — Not yet submitted to CG" |
| **Doc Ref** | Plan tracker ref column | Full document code. E.g., "MOC-MUS-ASE-1K0-PL-0029" |
| **Contract Refs** | Plan file frontmatter or §2 | Specific SoW/ER/Contract sections. E.g., "SoW §6.22; ER §2.4; Contract §4 Art. 2" |
| **Key Dates** | Plan tracker + plan file revision history | Actual submission/approval dates, not "TBD". For draft plans, note the planned submission week. |
| **Approval History** | Plan tracker + CG status files | Every revision with date, author, CG code, and key comments. Include Code C/D history for plans that went through revision cycles. |
| **CG Response History** | Plan tracker | Submission ref, revision, date, CG code, summary of comments. |
| **Key Decisions** | Plan tracker + change logs | Major milestones: approval dates, submission dates, conflict resolutions. |

#### Batch Update Pattern

For 15+ plan folders, process in a single pass:

1. **Read the plan tracker** once — it has all 15 plans' status, refs, owners, and CG codes
2. **Read each plan's actual files** — extract purpose, scope, section structure, contract refs
3. **Read CG status files** where they exist — extract approval history and comment details
4. **Write all 4 template files** per folder in one batch

Each file gets:
- YAML frontmatter with `last_updated`, `owner_agent`, `status`, `source:` pointing to actual plan files
- Real plan purpose/scope descriptions from source documents
- Actual document reference numbers and revision codes
- Real CG status codes and dates from the plan tracker
- Named owners (not generic roles where known)
- Actual approval history with dates and CG response codes
- Contract references specific to each plan

#### What to Replace in Templates

| Old Placeholder | Replace With |
|----------------|--------------|
| `TBD` in Key Dates | Actual date or "TBD (Week of DD-Mon)" for planned submissions |
| `Pending` in Status | Actual CG code: "Code B — Approved", "Draft — Not yet submitted", "Submitted — Awaiting response" |
| `TBD` in Approval Log | Actual revision code, date, author, and CG code from plan tracker |
| Generic "Owner" | Named role + person: "BIM Manager (Dr. Waleed Salah)" |
| Generic contract refs | Specific sections: "Contract §4 Art. 13; ER §3.2; SoW §6.21; DMP §5.3" |
| Empty Key Decisions | Actual milestones: approval dates, submission dates, conflict resolutions |

#### Verification

After populating all templates:
1. Spot-check 3-5 folders — verify status, owner, and doc ref match the plan tracker
2. Verify approval log revision history matches the plan tracker's per-plan rows
3. Check that draft plans have "Pending" CG status and approved plans have actual dates
4. Ensure every file has valid YAML frontmatter (no unclosed `---` blocks)

#### Additional Pitfalls for Template Population

- **CG status files may be in a different folder** — some plans have `CG_STATUS.md` in the plan folder (e.g., 02_Stakeholder), others don't. Check with `ls` before assuming.
- **Plan files may have multiple sections** — the purpose description should reflect the full scope (e.g., "Covers 14 sections including...") not just the first paragraph.
- **Some plans are internal control systems, not CG-submitted** — e.g., 15_Subcontractor_Deliverables. These don't have CG codes or submission dates. Mark as "Active — Operational" with a note about their internal nature.
- **HSE folder contains 12+ sub-plans** — the overarching HSE plan is Code B approved, but individual sub-plans range from Code B to Code D. The approval log must reflect this mixed status, not a single blanket status.
- **Plan tracker may have more detail than individual plan files** — the tracker is the authoritative source for CG status, revision codes, and next actions. Always prefer the tracker over plan file frontmatter for status information.

## 7. Pitfalls

- **OneDrive placeholder files (0 bytes)**: PDFs in OneDrive may appear as 0-byte files when accessed via the local filesystem. Always check file size before attempting to read. Use the repo's `99_Archive/` copies or download from OneDrive web.
- **PDF extraction quality**: `pymupdf` may produce garbled text from scanned PDFs. For scanned documents, use OCR (tesseract) or extract from the DOCX source instead.
- **Plan version tracking**: Multiple revisions exist (R00, R01, R02). Always use the latest approved version (Code A or B) as the source. Mark superseded revisions in the frontmatter.
- **Cross-plan consistency**: When one plan references another (e.g., DMP references BEP), ensure the referenced plan exists and the section numbers match.
- **Sub-agent context limits**: Each sub-agent gets its own context. Pass all relevant project context (AGENTS.md rules, project data, source paths) explicitly — don't assume the sub-agent knows the project.
- **File size from embedded images**: Don't embed base64 images in Markdown. Use `[Image: description](path)` references instead.
- **Cover page verbosity**: The cover page description should only state which revisions it supersedes and which reference docs it aligns with. Do NOT list every change (new stakeholders, new requirements, count changes) on the cover — that information belongs in the revision history table and the change log. CG reviewers don't need internal change details on the cover.
- **Revision history — actual submissions only**: The revision history table must show only actual submissions to CG, not internal drafts. If Rev 00 was submitted (Code C), Rev 01 was submitted (Code C), and Rev 02 was submitted (Approved), the table should show exactly those 3 rows. Internal working drafts (e.g., an 11-May draft that was never submitted) must not appear as separate rows. The revision number in the table must match the actual submission count, not the internal draft count.
