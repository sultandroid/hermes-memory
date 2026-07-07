# RACI-Driven Scope Realignment Workflow (CG Comment #4)

When CG returns a submittal with Code C and Comment #4 requiring a RACI matrix, follow this per-party workflow to realign all subcontractor scopes.

## Trigger
- CG Comment #4 on any MEP-related submittal (e.g., MOC-MUS-ASE-MEP-ZD-0068)
- RACI Matrix is the authoritative source for all R/A/C/I assignments

## Workflow

### 0. Read the RACI First
Extract all R/A/C/I assignments per party before touching any scope document. The RACI covers:
- Design Coordination (DC-01 to DC-08)
- Power & Containment (PC-01 to PC-06)
- Lighting Systems (LS-01 to LS-05)
- AV Systems (AV-01 to AV-08)
- BMS/ICT (BM-01 to BM-07, IC-01 to IC-05)
- Fire & Life Safety Interfaces (FL-01 to FL-05)
- Existing Systems Survey (ES-01 to ES-05)
- Testing & Commissioning (TC-01 to TC-05)
- Documentation & Handover (DH-01 to DH-06)

### 1. AD Engineering (MEP Designer) — Full Scope Rewrite
**Action:** Update scope document to R02 with RACI alignment note.

**Remove from AD scope:**
- ELV/Low-Current (ACS, CCTV, intercom, MATV, BMS network) — BMS/ICT specialist leads
- PAVA system — BMS/ICT specialist leads
- Existing Services Survey — Namaa leads (AD=I only)
- Construction Support (submittal review, RFIs, site inspections, FAT, commissioning) — Samaya=R, AD=I
- Telecom/IT subconsultant management — BMS/ICT specialist leads, AD=C
- BIM modelling — AD provides CAD, Samaya BIM Unit models
- Lighting calculations — ZNA leads all lighting design

**Narrow/clarify:**
- Electrical: AD provides power supply, containment, emergency lighting, and DALI control system design only
- Fire Protection: Remove PAVA. Keep sprinkler, fire alarm, clean agent, kitchen suppression, extinguisher schedule, fire stopping. Add smoke management, fire damper coordination, emergency lighting with FA zones
- ELV section → rename to "Power & Containment Coordination for Specialist Systems"
- Telecom/IT → rename to "Telecom/IT Support" — server room/MDF layout, ICT cable routing, environmental monitoring only
- BIM: Keep excluded, clarify AD provides coordinated 2D CAD for Samaya BIM Unit

**Add new items from RACI:**
- MEP Spatial Coordination (risers/shafts, ceiling voids, structural openings, plant rooms, LOD 300/350 input)
- Fire & Life Safety Interfaces (smoke management damper control, fire damper access panels, emergency lighting with FA zones)
- AV heat load calculation for HVAC sizing (AV-03)

**Update Offer Appraisal section:**
- Remove old gap analysis table (based on old scope)
- Replace with note that scope has been realigned per RACI

**Bump version** (R01→R02), update date, add RACI alignment note in header.

### 2. ZNA Lighting Designer — Scope Review Document
**Action:** Create a review document (not a full rewrite — ZNA has a signed contract).

**ZNA's R role (per RACI):**
- LS-01: Lighting design — general, gallery, accent, ambient → ZNA=R
- LS-05: LUX calculations & lighting performance verification → ZNA=R

**ZNA's C role (per RACI):**
- LS-02: Lighting control system (DALI) — ZNA provides design intent/control philosophy, AD does engineering
- LS-03: Emergency lighting & exit signs — ZNA provides fixture requirements, AD does engineering
- LS-04: Lighting power supply & containment — ZNA=I (informed only)

**Key check:** CG may have already rejected ZNA's attempt to limit lighting controls to "Design Intent only" — verify and note in review.

**Gaps to flag:**
1. ZNA's original fee proposal may have tried to limit lighting controls — check if CG rejected this
2. ZNA scope should reference coordination with AD for power supply/containment (LS-04) and BMS/ICT for DALI integration (BM-02)
3. ZNA should provide LUX calculations as a deliverable (LS-05)
4. ZNA should coordinate emergency lighting fixture requirements with AD (LS-03)

### 3. BMS/ICT Specialist — New Scope Document
**Action:** Generate a new scope document (no existing file).

**BMS scope (R per RACI):**
- BM-01: BMS architecture & points schedule
- BM-02: BMS + DALI integration (coordinate with ZNA)
- BM-03: BMS + fire alarm integration (coordinate with AD)
- BM-04: BMS + PAVA integration (coordinate with RAWASIN)
- BM-05: BMS + access control
- BM-06: BMS network backbone & IP scheme
- BM-07: BMS graphics & HMI

**ICT scope (R per RACI):**
- IC-01: Structured cabling design (fibre + copper)
- IC-03: WiFi access point locations & coverage
- IC-04: ICT cable routing & segregation (shared R with AD)
- IC-05: Telecom room environmental monitoring (C role)

**Also responsible for:**
- FL-01: Fire alarm + BMS shutdown sequences
- FL-05: PAVA + fire alarm integration
- TC-02: BMS point-to-point commissioning
- TC-03: ICT network testing
- TC-05: Integrated systems testing

**Not responsible for:**
- Power supply to BMS/ICT panels (AD)
- Server room/MDF layout (shared AD/BMS/ICT)
- AV systems (RAWASIN)
- Lighting fixture design (ZNA)

### 4. Namaa — Existing Systems Survey Scope
**Action:** Generate or update scope document.

**Namaa's R role (per RACI):**
- ES-01 to ES-05: HVAC, electrical, fire alarm/BMS, structural survey, site assessment report
- FL-01 to FL-05: Fire & life safety interface surveys
- TC-05: Integrated systems testing support

**Check for existing surveys:**
- HVAC survey may already be done by JEDI International
- Fire fighting survey may already be done by NAFCO
- If so, Namaa's role = obtain existing reports, verify coverage, fill gaps, consolidate into site assessment report

### 5. CITC Telecom Engineer — Scope Update
**Action:** Update scope to R01, align with RACI.

**Key change:** CITC Telecom Engineer is now a sub-consultant to the BMS/ICT Specialist, not a standalone subcontractor managed by AD.

**Remove from CITC scope:**
- BMS network (controllers, gateways, IP allocation) — BMS/ICT specialist scope
- Separate security network (CCTV, access control) — BMS/ICT specialist scope
- Rack room design (servers, switches, UPS, cooling) — shared AD/BMS/ICT scope

**Keep/narrow:**
- STC FTTH compliance: fibre termination, splitter cabinets, patch panels, ONT locations
- Structured cabling design — coordinate with BMS/ICT Specialist
- DEMARC/MPOE coordination with STC
- CITC registration and STC approval support
- FTTH design package for STC approval

**Update workflow:**
- All technical submissions go through BMS/ICT Specialist first, then Samaya
- CITC/STC submissions coordinated through BMS/ICT Specialist

**Add RACI matrix inside the scope document:**
- Include a RACI reference table in the scope document itself showing the CITC role (C) vs BMS/ICT role (R) for each relevant interface item (IC-01, IC-03, IC-04, IC-05, STC/CITC items)
- This makes the document self-contained — the reader doesn't need to open a separate RACI file
- Format: 5-column table (RACI Ref, Interface Activity, CITC Role, BMS/ICT Role, AD Role) with R/A/C/I legend below

### 6. RAWASIN (AV Specialist) — Confirm Only
**Action:** For information only — scope unchanged per RACI.

**RAWASIN's R role:**
- AV-01 to AV-08: AV rack room, cable routing, control system, audio, display, show control

**C role:**
- AV-03: Provide heat load data to AD for HVAC sizing
- TC-04, TC-05: AV commissioning, integrated systems testing

## Email to Project Team

Draft a single email covering all parties with:
- Per-party summary (3-5 lines each, no icons/emoji)
- Deliverable table with deadlines
- Attachments list

**Tone:** Directive but collaborative. This is scope realignment, not re-negotiation.

**Deadlines:**
- AD, ZNA, RAWASIN: 5 working days for confirmation
- BMS/ICT, Namaa: 10 working days for proposal + CVs

## Pitfalls
- **ZNA has a signed contract** — don't rewrite their scope, create a review document instead
- **Namaa already has an existing scope** — do not treat Namaa's scope as "new." They are already engaged. The RACI realignment is a confirmation exercise, not a new scope creation. Use "confirm scope alignment" language, not "new scope issued."
- **Namaa may already have existing survey reports** (JEDI for HVAC, NAFCO for fire fighting) — verify before writing full survey scope. If reports exist, Namaa's role = obtain, review, verify coverage, fill gaps, consolidate into site assessment report.
- **CITC Telecom Engineer is a sub-consultant** — update workflow to route through BMS/ICT Specialist, not directly to Samaya
- **AD's old scope may claim BMS/ICT/PAVA/ELV** — AD's draft SOW often overreaches into specialist territory. The RACI is the authority, not AD's proposal
- **BMS/ICT may not have a subcontractor folder yet** — create scope in _MANAGER_DASHBOARD until a folder is established
- **No icons/emoji in any generated document** — use plain text only for status indicators
- **Email summaries: concise per-party, not verbose tables** — when drafting the project team email, use 3-5 line summaries per party. Do not include full RACI reference tables in the email body. The attachments carry the detail.
