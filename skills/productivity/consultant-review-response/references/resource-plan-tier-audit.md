# Tier Table Audit — Project Management Plan Staffing Tables

Audit a tiered resource/staffing table (Tier 2 Discipline Leads, Tier 1 Management, Tier 3 Modelers) against project data sources and PMBOK standards. Used for the Aseer Museum Resource Management Plan and similar.

## Trigger Phrases

- "audit this table :Tier 2 / Discipline Leads"
- "check tier table against KPR"
- "audit according [contractor name] side"
- "review staffing table against project data"

## Reference Documents (in order of authority)

| # | Source | What It Contains | How to Find |
|---|--------|------------------|-------------|
| 1 | **Stakeholder Plan (latest Rev)** — PL-0020 | Authoritative T2 codes, role definitions, org categories | `Docs/02_Plans_and_Procedures/02.13_Stakeholder_Plan/` |
| 2 | **Key Personnel Register** — KP-0001 | Names, approval codes (A/B/C/D), dates, location | Odoo task 3022 description or Aconex |
| 3 | **CG CRS (Comments Resolution Sheet)** | Directives about specific roles (e.g. "IT/Data must be T1 not T3", "need Interior Designer") | Email archive, CG_STATUS.md |
| 4 | **PMBOK 6th Ed. §9.1-9.6** | Required table columns for roles & responsibilities | `02_Plans_and_Procedures/reference/PMBOK_Complete_Reference.md` or 07_Guidelines |
| 5 | **Contract SOW / ER** | Contractual role obligations (e.g. SOW §5.5 required disciplines) | `Contracts/` directory |

## Audit Methodology

### Step 1: Extract the Table from the HTML

Read the plan HTML to extract all Tier 2 rows. Build a working matrix:

| # | Role | Name | Description | Type (FT/Specialist) |
|---|------|------|-------------|---------------------|

### Step 2: Cross-Reference Against Stakeholder Plan (SMP Rev03+)

For each row, check SMP's Tier 2 section (architecture, structural, MEP, FLS, ICT, exhibition, conservation, etc.):

- Does the SMP list this role at this tier level?
- Does the SMP's T2 code description match the table's role scope?
- Are there SMP T2 roles **missing** from the table?

**Key SMP T2 categories for Aseer Museum:**
- T2-01: Principal Structural Eng
- T2-02/03: MEP Specialist + Coordinator
- T2-04: Fire & Life Safety Specialist
- T2-14: Architecture / Interior (NRS)
- T2-15: ICT/Security System Integrator
- T2-19: Scenographer
- T2-20: Conservation Consultancy
- T2-21: Interior Designer (Samaya fit-out oversight)
- T2-22: MEP Design Agency
- T2-07: Showcases
- T2-12/17: Samaya Factory (suppliers)

### Step 3: Cross-Reference Against Key Personnel Register

For each named person:

- Is the person in the KPR? What PQ code?
- What approval code? (A=Approved, B=Approved w/Comments, C=Revise & Resubmit)
- Location listed?
- CV status (submitted / pending / not yet)?

Flag when:
- Person has Code C in KPR but table shows no caveat
- Person has Code B but table says "Approved" without noting "with Comments"
- CV is marked "submittal-pending" in SMP but missing from table notes

### Step 4: Cross-Reference Against CG CRS

Search the CG Comments Resolution Sheet (from Stakeholder Plan or email archive) for directives about staffing:

Examples from Aseer CG CRS:
- CRS-01/02/03/06: IT/Security must be T1 (full-time), not T3 or T2 — split into T1-07 (Samaya specialist) vs T2-15 (System Integrator)
- CRS-12: Interior Designer required for fit-out oversight — Samaya set T2-21
- CRS-09/10: Structural Eng scope per ER §3.10, CV submittal pending
- CRS-13: Samaya Factory suppliers pending CG approval
- CRS-16: Procurement Manager added as T1-08

### Step 5: PMBOK Standard Table Completeness

A proper R&R table should have columns for:

| Column | Required? | Notes |
|--------|-----------|-------|
| Role / title | ✅ Always present | |
| Named person | ✅ Usually present | |
| Discipline / scope | ⚠️ Variable | May be in description |
| **Reporting line** | ❌ Common gap | Who does this role report to? |
| **Decision authority** | ❌ Common gap | Level of approval (L1-L4) |
| **Time commitment** | ❌ Common gap | % FTE or stage-specific |
| **Phase / timeline** | ❌ Common gap | When is role active? |
| **Filled status** | ❌ Common gap | Active / Pending / TBC |
| **Location** | ⚠️ Variable | Site / Office / Remote |

### Step 6: Classification Audit

Check each row's "Type" classification:

| Current Label | Correct? | Standard |
|---------------|----------|----------|
| `FT` (Full-Time) | Only if person is Samaya direct employee | Samaya payroll staff |
| `Specialist` | External consultant/subcontractor | Not on Samaya payroll |
| Consultant should NOT be `FT` | ⚠️ Common error | Ahmed Gad (Structural) marked FT but is consultant T2-01 |
| T2 roles should not include T1 roles | ⚠️ Common error | HSSE Manager, IT/Data are T1 management per SMP |

## Framing Guidelines (Critical — User Preferences)

### "Audit from Samaya's Side"

Frame every finding from **Samaya's organizational perspective** as the design-build contractor. Never frame it as the user's personal failure or put them "in a corner."

✅ **Correct**: "Samaya is contractually obligated to provide an Interior Designer for fit-out oversight per CRS-12. This role is missing from Tier 2."
❌ **Wrong**: "You forgot to add the Interior Designer."

✅ **Correct**: "Three SMP-identified T2 specialists (FLS, Scenographer, Conservation) are absent from the table — these are Samaya's appointments needing entries."
❌ **Wrong**: "You didn't include these roles."

✅ **Correct**: "The IT/Data role is classified at T2 but CG explicitly directed IT/Security to be T1 (CRS-01/02). Needs reclassification."
❌ **Wrong**: "You put IT/Data in the wrong tier."

### Client-Facing Language

In report descriptions (cover, headers, revision history), use plain language:

- ❌ "PMBOK-compliant sections: RBS, Physical Resource Management, Resource Control"
- ✅ "Project resource management framework covering team structure, roles, equipment, and risk management procedures"

- ❌ "Draft: PMBOK-conforming Resource Management Plan with org structure, RBS, location matrix"
- ✅ "Draft: Resource Management Plan covering team organisation, personnel allocation, equipment planning, and resource risk management"

### Report Structure

Present findings in this order:

1. **Structural Gaps** — roles Samaya must provide but are missing from table (with SMP T2 codes)
2. **Classification Issues** — wrong tier, wrong type (FT vs Specialist)
3. **Standard Compliance** — missing PMBOK columns (reporting line, authority, timeline)
4. **Accuracy Issues** — stale KPR status, missing caveats, pending submittals

Use tables with columns: # | Role | Current State | Issue | Priority

## Saved Session: Aseer Museum Resource Mgmt Plan Rev C00

| # | Role | Current State | Issue |
|---|------|-------------|-------|
| 1 | IT/Data Lead — Salah Eldin | Tier 2 | SMP has it as T1-07 IT/Security Specialist; T2-15 is System Integrator (separate) — wrong tier |
| 2 | Structural Eng — Ahmed Gad | Type=`FT` | He's T2-01 consultant (not Samaya FT); CV submittal-pending per CRS-10 |
| 3 | MEP Design (AD Engineering) | Merged row | SMP splits into T2-22 (Design Agency, authorship) + T2-02 (MEP Specialist, coordination) — conflated |
| 4 | FLS Specialist (Nama Consulting) | Missing | SMP T2-04, SCD-licensed — Samaya obligation |
| 5 | Scenographer | Missing | SMP T2-19 — NRS (Approved 11-Feb) |
| 6 | Showcases (Glasbau Hahn) | Missing | SMP T2-07 — Approved |
| 7 | Conservation Consultancy | Missing | SMP T2-20 |
| 8 | Interior Designer (fit-out) | Missing | CG CRS-12, SMP T2-21 |
| 9 | ICT/Security System Integrator | Missing | SMP T2-15 |
| 10 | Samaya Factory suppliers | Missing | SMP T2-12/17 |

## KPR-to-HTML Cross-Reference Workflow

When updating an HTML plan document to match the live KPR (Key Personnel Register):

### Step 1: Read the KPR Excel

The KPR is at `Docs/09_Registers/13_Key_Personnel_Register/Aseer_Museum_Key_Personnel_Register.xlsx`.
Three sheets: `Cover`, `Key Personnel`, `Summary`.

**OneDrive lock workaround:** `execute_code` sandbox may fail with `TimeoutError` or `BadZipFile` on OneDrive-synced xlsx files. Use `terminal` with `python3 -c "..."` directly — it has better file handle timeout tolerance. If that also fails, the file may need to be opened in Excel first to force sync.

```python
import openpyxl
wb = openpyxl.load_workbook('path/to/KPR.xlsx', data_only=True)
ws = wb['Key Personnel']
# Columns: Tier, Role, Name, Years Exp, Discipline, Authority Reg, CV Ref, MoC Approval Status, MoC Approval Date, Notes
```

### Step 2: Classify Each KPR Entry

| KPR Status | HTML Treatment |
|------------|---------------|
| `Approved` / `Approved (pending formal notification)` | Show entity name + "Approved [date]" |
| `Approved with Comments (Code B)` | Show entity name + "Code B approved [date]" |
| `Pending submission` | Show "—" + "Pending submission" |
| `C - Revise and Resubmit` | Show "—" + "Code C — revise & resubmit" |
| `Vacant` / `Not yet appointed` | Show "Vacant" or "TBC" |
| `Pending - not yet approved by CG` | Show "—" + "Pending CG approval" |
| `Nominated - pending approval` | Show entity + "Nominated — pending approval" |

**Critical rule:** Only show individual person names for entries with Approved/Code B status. All pending entries show "—" — never a person's name. Entity/firm names (AD Engineering, ZNA Studio, Nama Consulting, Glasbau Hahn, NRS) are OK to show if the firm is approved even if individual names within are not.

### Step 3: Patch the HTML

Use targeted `patch()` calls — never regenerate the full HTML. Common areas to fix:

1. **Tier 1 org chart cards** — one card per KPR Tier 1 role (6 roles: PD, CM, BIM Mgr, HSSE Mgr, QA/QC Mgr, T&C Mgr)
2. **Tier 2 table rows** — one row per KPR Tier 2 specialist role
3. **Tier 3 table rows** — ITCA + Fire-Proofing Contractor (KPR Tier 3)
4. **Location Matrix** — rows must match KPR roles exactly
5. **Phase Loading Matrix** — rows must match KPR roles exactly
6. **Document Sign-Off** — Checked by / Reviewed by should be "—" if those roles are pending in KPR
7. **Subcontractor table** — remove individual contact names (Julie Riley, etc.) if not KPR-approved; keep firm names

### Step 4: Entity Name Corrections

Always use the exact entity name from the KPR, not approximations:

| Wrong (in HTML) | Correct (per KPR) |
|-----------------|-------------------|
| Nama Al Amal | Nama Consulting |
| Glassbühne | Glasbau Hahn |
| AD Engineering Co. — M. Moustafa · Dubai · A. Omar · Dubai | AD Engineering Co. · Dubai (remove individual names) |

### Step 5: Verify No Stale Names Remain

After patching, run a `search_files` regex scan for all previously-removed individual names to confirm zero matches in the HTML file. Only document-control operational names (Prepared by, Issued by) may remain.
