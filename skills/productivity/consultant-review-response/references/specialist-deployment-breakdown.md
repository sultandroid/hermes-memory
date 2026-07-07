# Specialist Deployment Breakdown — NRS vs SAMAYA Responsibility Mapping

**Trigger:** Incoming formal correspondence (CG consultant, NRS, PMC) requests clarification on which specialist/engineering positions are covered by NRS (Design Lead) vs SAMAYA (Main Contractor).

**Sources to cross-reference:**
- SOW §5.5 (Staffing and Deployments) — mandatory specialist positions list
- CG directive email from Engr. Mohammad Elbaz (23 Apr 2026) — same list sent to SAMAYA
- NRS Contract Appendex A — NRS Responsibility Matrix defining their scope
- NRS Resource Schedule — NRS's own team roles (Director, Associate, Senior Designer, Designer)
- 24_Subcontractors/README.md — SAMAYA's specialist contractor register
- NRS Contract Study (Aseer_NRS_Contract_Study.html) — fee structure, scope breakdown

## Core Principle

**NRS is Design Lead/AoR** — their scope is:
1. Stage 4: IFC CAD package for interior architecture + 3D scenography (768K SAR)
2. Stage 5: Off-site fabrication review & sign-off (270K SAR)
3. Stage 5-6: On-site review & stamp (171K SAR)

NRS does NOT provide specialist contractors. NRS provides **design coordination and integration** — they create base designs (setworks, showcases, graphics panels) that specialist contractors build upon. Specialist contractors are engaged by SAMAYA.

## Position Mapping Template

Use this two-column format in the response:

### Positions Covered Under NRS Design Scope
| Position | Basis |
|---|---|
| Principal Design Engineer | NRS Director/Associate per resource schedule |
| Setworks/Joinery design integration | NRS §4.2 item 7 — 78 setworks dwgs delivered |
| Showcase design intent | NRS §4.2 item 8 — 17 showcase dwgs delivered |
| Interactive design intent | NRS §4.2 item 12 — design intent only |
| Graphic panel design | NRS — graphics & panel housing drawings (21 dwgs) |

### Positions Provided by SAMAYA (Specialist Contractors)
| Position | SAMAYA Engagement | Status | SMP Ref |
|---|---|---|---|
| Audio Visual Hardware Specialist | Rawasin | Active | T2-05 |
| Mechanical & Electromechanical Interactives | Interactive Design Contractor | Pre-qual pending | T2-09 |
| Setworks/Joinery Specialist (fab) | Samaya Factory | Pre-qual pending | T2-08 |
| Models & Props Specialist | Replica & Model Contractor | Pending — waiting object research from client | T2-17 |
| Graphic Artwork Specialist | Samaya-Graphic | Pre-qual pending | T2-11 |
| Lighting Specialist | Studio ZNA | Active | T2-06 |
| Showcase Specialist | Glasbau Hahn | Active | T2-07 |
| MEP Designer | MEP Designer (ITC) | Active | T2-03 |
| MEP Contractor | MEP Contractor | Active | T2-02 |
| Testing & Commissioning Manager | To be deployed (post-D60) | TBD | T2-18 |
| FLS Specialist Engineer | Nama Consulting (MoC-approved) | Active | T2-04 |
| Cafe Terrace Shade (fab) | Samaya Factory | Pending | T2-12 |
| Landscaping Specialist | Evergreen | Pre-qual in progress | T2-13 |
| Structural Engineer | Eng. Ahmed Gad — CV submitted | CV submitted | T2-01 |
| Quality Team | SAMAYA internal + sub-QA/QC | Partial | T2-18 |
| IT/Security Specialist (full-time site) | To be deployed per CRS-01 | TBD | T1-07 |
| ICT/Security System Integrator | TBD | TBD | T2-15 |
| Accessibility Consultant | NRS (Eng. Jim) | Conditional | T3-08 |
| Design & BIM Manager | NRS design coordination; Samaya BIM Manager (Dr. Waleed Salah) | Active | T1-03 |

## Workflow

1. **Read the incoming request** — identify if it references SOW §5.5 or CG's staffing directive
2. **Locate the NRS contract scope** — `Aseer-Museum/01_Contracts/02_NRS_Contract/` or the NRS Contract Study at `23_Scripts/notes/Aseer_NRS_Contract_Study.html`
3. **Read the subcontractor register** — `24_Subcontractors/README.md` for the master list
4. **Cross-reference SMP** — read the Stakeholder Management Plan (PL-0020) for Tier IDs and statuses. SMP Rev 03 is current.
5. **Map each position** using the template above — check each subcontractor folder for actual appointment status
6. **Include SMP Ref column** — every position must map to its SMP Tier ID (T1-xx, T2-xx, T3-xx)
7. **Draft the formal reply** with two tables: NRS-covered positions and SAMAYA-provided positions
8. **If the SMP needs updating** (status changes, vendor name corrections):
   a. Make targeted patches to the SMP HTML file
   b. Bump Rev (e.g., 02→03), add revision history entry
   c. Deploy to `samaya-factory.com/build/technical-office/` via SSH pipe
9. **Key caveat in reply:** All specialist contractors engage under SAMAYA as main contractor — no privity with NRS, CG, or MoC. NRS reviews/stamps specialist submittals per contract.

## Key References on Disk

| Data | Path |
|---|---|
| NRS Contract Study | `Aseer-Museum/23_Scripts/notes/Aseer_NRS_Contract_Study.html` |
| NRS Scope vs Deliverables | `Aseer-Museum/23_Scripts/notes/Aseer_NRS_Scope_vs_Deliverables.html` |
| NRS EV Analysis | `Aseer-Museum/23_Scripts/notes/NRS_Review_Work_EV_Analysis.md` |
| Subcontractor Register | `Aseer-Museum/24_Subcontractors/README.md` |
| Stakeholder Management Plan Rev 03 | `Aseer-Museum/04_Docs/02_Plans_and_Procedures/02.13_Stakeholder_Plan/01_Source_Files/01_HTML/MOC-MUS-ASE-1K0-PL-0020_Rev03_Stakeholder_Management_Plan.html` |
| Deployed SMP (web) | `https://samaya-factory.com/build/technical-office/stakeholder-management-plan.html` |
| CG Staffing Directive (23 Apr 2026) | `Aseer-Museum/04_Docs/00_Admin/SAMAYA Staffing and Deployments as per contract obligations._1.eml` |

## Pitfalls

- **NRS does not employ the specialist staff** — NRS's resource schedule only has 7 roles (Director, 2 Associates, 2 Senior Designers, 2 Designers). Do not map specialist positions directly to NRS unless explicitly in their scope.
- **"Covered by NRS" means design coordination, not contracting** — NRS produces design intent drawings (setworks, showcases, graphics) which specialist contractors develop into shop drawings. NRS then reviews/stamps those shop drawings.
- **Some specialist roles overlap with SAMAYA's internal team** — Design & BIM Manager is split: NRS provides design coordination, SAMAYA provides BIM Manager as a separate role.
- **Accessibility Consultant = NRS** — SMP T3-08 lists NRS (Eng. Jim) as conditional. Do NOT mark as "to be procured."
- **Cafe Terrace Shade is split** — design by NRS, fabrication/installation by Samaya Factory. SMP T2-12.
- **ICT/Security is two separate roles** — T1-07 (full-time site-based IT/Security Specialist, TBD) and T2-15 (ICT/Security System Integrator, TBD). Do NOT conflate with CITC/CST authority liaison (T3-09).
- **Replica & Model pending client data** — Status "pending — waiting object research from client," not just "pending CG/MoC approval."
- **Graphics = Samaya-Graphic** — not "Samaya Graphit" or generic "Graphics Contractor."
- **Setworks/Joinery fab = Samaya Factory** — not Exhibition Fit-Out Contractor. NRS does the design; Samaya Factory does the fabrication.
- **Testing & Commissioning Manager is a future role** — Not yet deployed. Mark as "To be deployed at construction phase (post-D60)."
- **Never cite unapproved KPR names in formal response** — positions not yet CG-approved should show status as "submission in progress" not named individuals.
- **Cross-reference SMP Rev 03 for Tier IDs** — always include SMP Ref column in the response table. CG expects traceability to the approved Stakeholder Management Plan.
