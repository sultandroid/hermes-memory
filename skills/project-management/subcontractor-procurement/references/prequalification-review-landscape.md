# Landscape Subcontractor Prequalification Compliance Sheet

## When to Use
- User provides a landscape/design-build subcontractor prequalification (company profile + PQ letter)
- Need a formal compliance assessment against SCOPE_REQUEST.md, SPEC.md, and project requirements
- Need to grade readiness before proceeding to tender/RFQ
- The subcontractor is a **design+build** entity (covers both design and execution)

## Workflow

### Step 0: Determine Subcontractor Type
Before assessing, determine if the subcontractor is:
- **Design+build** (in-house design team + execution crew) — assess both capabilities separately
- **Design-only** (consultant) — focus on design portfolio, team CVs, design tools
- **Execution-only** (contractor) — focus on equipment, crew size, bonding, past projects

**Pitfall:** Do NOT assume a landscaping firm is execution-only. Many KSA landscaping firms have in-house landscape architects. Check the company profile's org chart and services list before concluding on design capability.

### Step 1: Read All Source Documents

**Primary sources:**
1. `_MANAGER_DASHBOARD/SCOPE_REQUEST.md` — defines what was asked of the subcontractor
2. `_MANAGER_DASHBOARD/SPEC.md` — defines scope, deliverables by stage (50%/90%/100%/IFC)
3. `_MANAGER_DASHBOARD/SITUATION_REPORT.md` — current status, next actions
4. Subcontractor's company profile (PDF) — full company presentation
5. Subcontractor's prequalification letter (PDF) — signed PQ letter

### Step 2: Extract Key Data

**From company profile:**
- Org chart — in-house landscape architects? Engineers? Technicians?
- Services listed — design (2D/3D), installation, maintenance, irrigation?
- Portfolio — number of projects, types (cultural/museum/residential/commercial), client names
- Clients section — Ministry of Culture projects are strongest for museum work
- Company docs — CR, VAT, Chamber, SCA membership, ISO certs, classification cert
- Contact — base city (relevant for mobilization)

**From PQ letter:**
- Scope understanding — does it mention the specific project (Stramp, terrace, museum context)?
- RACI matrix — shows who's responsible for what
- Risk register — shows they've thought about project-specific risks
- Compliance acknowledgment — SBC, HSE, CG process, BIM
- Signature — signed by authorized signatory

### Step 3: Build Compliance Matrix (7 Domains)

| Domain | What to Check | Pass Threshold |
|--------|---------------|----------------|
| **Submission Reqs** | vs SCOPE_REQUEST §5 (profile, portfolio, CVs, BoQ, plant schedule, method statement, signed letter) | ≥5/7 for pass |
| **Design Capability** | In-house landscape architect(s), 2D/3D design services, Stramp/hardscape evidence, plant selection, irrigation design, BIM capability | ≥6/8 for pass |
| **Technical Compliance** | Climate-appropriate species, local stone priority, peat-free planting, Oddy test, SBC/HSE/CG acknowledgment, establishment period commitment | ≥6/8 for pass |
| **Commercial Readiness** | CR valid, VAT, Chamber, SCA, ISO, bonding, insurance — MoC experience is a multiplier | ≥7/10 for pass |
| **Portfolio Fit** | Number of cultural/MoC projects, similarity to museum context (public/cultural not just residential villas) | ≥1 MoC cultural project |
| **Risk Posture** | Risk register quality, mitigation measures identified, acceptance of known project risks | ≥5/7 for pass |
| **Programme Feasibility** | Can they meet the submission deadline? (e.g. 50% design in 3 weeks) | Without this, everything else is moot |

### Step 4: Create the Compliance Sheet

Format as `##_Register/##_Subcontractor_Prequal_Compliance.md` in the repo (markdown, YAML frontmatter):

```yaml
---
last_updated: YYYY-MM-DD
owner_agent: Hermes
status: active
source: OneDrive/.../00_Prequalification/
---
```

**Sections:**
1. **Submission Requirements Compliance** — table mapping SCOPE_REQUEST §5 items to submitted/partial/missing with notes
2. **Design Capability Assessment** — table per capability criterion with evidence and verdict
3. **Technical Compliance** — table per spec/ER/SoW requirement
4. **Commercial & Contractual Readiness** — table per document/credential
5. **Risk Assessment** — table with 6-8 risks, L/I/S ratings, mitigations
6. **Compliance Summary** — domain scores, overall verdict (Pass / Conditional Pass / Fail)
7. **Recommended Next Actions** — numbered list with owner and target date

### Step 5: Verdict Framework

| Score Range | Verdict | Action |
|-------------|---------|--------|
| ≥85% | **Pass** — proceed to tender/RFQ immediately | Issue RFQ with BOQ |
| 65-84% | **Conditional Pass** — pass with ≤6 conditions to resolve | Send conditional acceptance requesting missing items |
| 40-64% | **Conditional Fail** — major gaps but could improve | Request resubmission with specific items |
| <40% | **Fail** — not viable for this project | Reject and move to next candidate |

### Step 6: Conditions-to-Resolve Template

When issuing a conditional pass, structure the follow-up as:

**Priority 1 (blocks tendering):**
1. {Can you deliver 50% design by {date}? — confirm before proceeding}
2. {Specific scope experience e.g. Stramp design}

**Priority 2 (needs before appointment):**
3. Individual CVs for key personnel (landscape architect, irrigation lead)
4. Classification grade — verify covers contract value

**Priority 3 (good to have):**
5. Insurance certificates, bonding capacity
6. BIM coordination capability statement

## Pitfalls

- **Don't assume execution-only** — Many KSA landscape firms have in-house design teams. Read the org chart before concluding. User will correct you if you assume "contractor only" when they're also designers.
- **Don't confuse PQ letter with full submission** — A PQ letter is an expression of interest, not a priced tender. Missing BOQ and plant schedule at this stage is normal.
- **Deadline is the real blocker** — If the 50% design submission is 3 weeks away and no designer is appointed, that's the critical risk, not the quality of the PQ.
- **MoC portfolio is gold** — A subcontractor who has worked on other Ministry of Culture projects (Diriyah Biennale, JAX Wadi, Jeddah Historical District) is significantly stronger than one with only private villa work, even if the villa work is technically good.
- **BIM capability is often missing from landscape PQs** — Landscape firms rarely have Revit/BIM capability. This needs explicit confirmation or a mitigation (Samaya BIM Unit covers LOD 300 coordination).
- **SPEC.md and SCOPE_REQUEST.md are the compliance baseline** — Not the ER/SoW directly for prequal stage. Use the scope documents that were issued to the subcontractor as the source of requirements.
- **Classification grade** — KSA landscape firms may have a SCA classification grade that limits the contract value they can bid on. Always verify before proceeding.
