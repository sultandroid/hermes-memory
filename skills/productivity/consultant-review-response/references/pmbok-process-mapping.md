# PMBOK Process Mapping — Aseer Museum Project Plans

Reference for cross-referencing project plans against PMBOK 6th Ed. processes.
Source: `Docs/02_Plans_and_Procedures/reference/PMBOK_Complete_Reference.md`

## PMBOK 6th Ed. — Project Resource Management (9.1–9.6)

### 9.1 Plan Resource Management (Planning)

| Element | What CG Expects | 07_Guideline | Example Plan Section |
|---------|----------------|--------------|---------------------|
| Resource categories | Human, equipment, material, facility clearly defined | 01_Resource_Identification | §2 Scope / §3.1 RBS |
| RBS (Resource Breakdown Structure) | Hierarchical resource decomposition by category | 01_Resource_Identification | §3.1 RBS (add if missing) |
| RACI / RAM | Roles mapped to deliverables with R/A/C/I codes | 03_Roles_Responsibilities | Separate 02.9_RACI; cross-reference required |
| Authority levels | L1–L4 delegation table (who can approve what) | 03_Roles_Responsibilities | Add if missing |
| Org chart | Multi-level with reporting lines | 04_Project_Organization_Charts | §3 Org Structure |
| Competency requirements | Qualifications per role (SCE, certification) | 03_Roles_Responsibilities | Add if missing |
| "Living Document" clause | Periodic review, trigger-based revision, phase transitions | Cross-cutting CG requirement | §10 Plan Governance |
| Compliance declaration | Statement addressing prior CG directives | Cross-cutting (CommPlan #1) | §10 Plan Governance |
| Escalation matrix | L1-L4 escalation ladder for issues | Cross-cutting (CommPlan #5) | §10 Plan Governance |
| Glossary/legends | All abbreviations defined | Cross-cutting (DMP #1) | §2 Definitions |

### 9.2 Estimate Activity Resources (Planning)

| Element | What CG Expects | 07_Guideline | Example Plan Section |
|---------|----------------|--------------|---------------------|
| Resource requirements by WBS | Quantity, skill, duration per deliverable | 01_Resource_Identification | §5 Headcount Curve |
| Basis of estimates | Explain how resource numbers were derived | Implicit | Add if missing |
| Resource quantities schedule | Materials linked to BOQ | 01_Resource_Identification | Add if missing |
| Equipment/plant estimates | Type, quantity, duration | 06_Physical_Resource_Management | Add if missing |

### 9.3 Acquire Resources (Executing)

| Element | What CG Expects | 07_Guideline | Example Plan Section |
|---------|----------------|--------------|---------------------|
| Acquisition methods | Internal, subcontract, purchase, rental defined | 02_Resource_Acquisition | §7.3 Sub-Contractors |
| Mobilization lead times | Per-resource-type lead times | 02_Resource_Acquisition | §4 Mobilization Timeline |
| Resource calendars | When each resource is available | Implicit | Add if missing |
| Virtual team management | Protocol for remote team members | Implicit | §6 Location Matrix |
| Subcontract onboarding | NDA, prequalification, CV verification | 02_Resource_Acquisition | §7.3 |
| Physical resource assignments | Equipment/material tracking | 06_Physical_Resource_Management | §6.4 Physical Resource Mgmt |

### 9.4 Develop Team (Executing)

| Element | What CG Expects | 07_Guideline | Example Plan Section |
|---------|----------------|--------------|---------------------|
| Team formation approach | Tuckman stages (Forming→Storming→Norming→Performing→Adjourning) | 05_Team_Resource_Management | §7.5 |
| Training plan | Induction + ongoing training matrix | 05_Team_Resource_Management | §7.4 |
| Team charter | Vision, values, protocols, ground rules | 05_Team_Resource_Management | §7.5 |
| Co-location strategy | HQ vs site vs remote coordination | Implicit | §6 Location Matrix |
| Performance indicators | Schedule, quality, safety, collaboration | 05_Team_Resource_Management | §8.2 KPIs |
| Team building | Activities for cross-team cohesion | 05_Team_Resource_Management | Add if missing |

### 9.5 Manage Team (Executing)

| Element | What CG Expects | 07_Guideline | Example Plan Section |
|---------|----------------|--------------|---------------------|
| Performance feedback | Review cycle (daily/weekly/monthly) | 05_Team_Resource_Management | §7.5 |
| Issue log for resources | Track resource issues | 07_Resource_Control | §8.3 Risk Register |
| Conflict resolution | 4-step escalation (peer→manager→PM→PD) | 05_Team_Resource_Management | §7.5 |
| Recognition & rewards | Milestone achievements, safety awards | 05_Team_Resource_Management | Add if missing |
| Health, wellbeing, welfare | Labor law compliance, heat stress, fatigue | 05_Team_Resource_Management | §7.5 |

### 9.6 Control Resources (M&C)

| Element | What CG Expects | 07_Guideline | Example Plan Section |
|---------|----------------|--------------|---------------------|
| Plan vs actual comparison | Table with metrics, source, frequency | 07_Resource_Control | §9.1 |
| Variance analysis | Compare baselines, identify causes, assess impact | 07_Resource_Control | §9.2 |
| Corrective actions | Issue→action mapping table | 07_Resource_Control | §9.3 |
| Monitoring tools | Histograms, S-curves, EVM, dashboards | 07_Resource_Control | §9.4 |
| Resource reporting | Daily/weekly/monthly report schedule | 07_Resource_Control | §9.5 |
| Change control | 5-step process for resource changes | 07_Resource_Control | §9.6 |
| Physical Resource Register | Equipment/material inventory tracking | 06_Physical_Resource_Management | §6.4 |
| Release procedure | Formal demobilization with checklist | 08_Resource_Release_Criteria | §8.1 / §8.5 |

## CG Recurring Patterns (Cross-Plan)

These gaps appear in CG reviews across multiple plans. Always check:

| Pattern | Originated In | What CG Expects |
|---------|-------------|-----------------|
| **Living Document clause** | HSE #4-6, CommPlan #8 | Periodic review, trigger-based revision, phase transition mechanism |
| **Compliance statement** | CommPlan #1 | Formal statement addressing all prior CG directives from cross-cutting plans |
| **Named personnel** | HSE #3 | All key roles filled with named persons, not blanks |
| **Escalation matrix** | CommPlan #5 | Clear escalation ladder for disputes/issues |
| **Glossary/legends** | DMP #1 | All abbreviations and symbols defined |
| **Phase transitions** | CommPlan #8, HSE | How the plan adapts at each project phase boundary |
| **QC/Review loop** | DMP #4 | Explicit quality control illustration in process flows |
| **Authority compliance** | HSE #1, DMP | SCE/MoMRAH registration, KSA regulatory references |

## Severity Taxonomy for Gaps

| Severity | Meaning | Example |
|----------|---------|---------|
| **Code C** | CG has previously rejected other plans for missing this | Living document clause, compliance statement, escalation matrix |
| **High** | CG would flag as a formal comment | Blank key personnel names, missing phase transition mechanism |
| **Medium** | CG would note but may not block approval | Missing SCE registry, acting PD without timeline |
| **Low** | Minor completeness issue | Missing glossary, unsigned fields |

## Companion Documents a Plan Should Reference

- **Key Personnel Register**: `MOC-ASEER-SIC-1K0-KP-0001`
- **Master Programme**: `MOC-ASEER-0PS-SH-00X` (note revision and if under resubmission)
- **RACI**: separate doc at `02.9_RACI`
- **DMP**: `MOC-MUS-ASE-1K0-PL-0029`
- **BEP**: `MOC-ASEER-SIC-1K0-PL-0015`
- **PEP**: `MOC-ASEER-SIC-1K0-PL-TBD`
- **HSE Plan**: `MOC-ASEER-SIC-1K0-PL-0010`
- **Contract**: ref number/code
- **SoW / ER**: Employer's Requirements document
