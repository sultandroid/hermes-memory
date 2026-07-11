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
- **Empty/0-byte PDFs**: These are OneDrive placeholder files. Find the real file in the repo's `99_Archive/` or use the OneDrive web UI to download.

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

## 6. Pitfalls

- **OneDrive placeholder files (0 bytes)**: PDFs in OneDrive may appear as 0-byte files when accessed via the local filesystem. Always check file size before attempting to read. Use the repo's `99_Archive/` copies or download from OneDrive web.
- **PDF extraction quality**: `pymupdf` may produce garbled text from scanned PDFs. For scanned documents, use OCR (tesseract) or extract from the DOCX source instead.
- **Plan version tracking**: Multiple revisions exist (R00, R01, R02). Always use the latest approved version (Code A or B) as the source. Mark superseded revisions in the frontmatter.
- **Cross-plan consistency**: When one plan references another (e.g., DMP references BEP), ensure the referenced plan exists and the section numbers match.
- **Sub-agent context limits**: Each sub-agent gets its own context. Pass all relevant project context (AGENTS.md rules, project data, source paths) explicitly — don't assume the sub-agent knows the project.
- **File size from embedded images**: Don't embed base64 images in Markdown. Use `[Image: description](path)` references instead.
