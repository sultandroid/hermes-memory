---
name: supplier-procurement-lifecycle
category: project-management
description: "Complete supplier/vendor/contractor lifecycle management for construction/BIM projects. Covers entity research (intake), proposal evaluation, prequalification document design, capability profile creation, and subcontractor dossier management. Designed for Samaya / Tqanny portfolio, supports bilingual AR/EN workflows."
version: 1.3.0
author: Hermes Agent
platforms: [macos]
metadata:
  hermes:
    tags: [supplier, vendor, procurement, prequalification, proposal-evaluation, subcontractor, entity-intake, construction, samaya]
    related_skills: [evm-analysis-chart, project-deliverable-audit, samaya-proposals]
prerequisites:
  commands: [python3, pdfplumber, tesseract, claude]
  python_packages: [PyMuPDF, python-docx, pdfplumber, openpyxl]
---

# Supplier Procurement Lifecycle

This umbrella skill covers the complete lifecycle of external parties in construction/BIM projects — from initial discovery through evaluation, prequalification, and ongoing subcontractor management.

## Lifecycle Overview

```
Entity Discovery → Proposal Evaluation → Prequalification → Subcontractor Dossier
    (intake)        (evaluate bids)      (design docs)      (ongoing mgmt)
```

Each phase is a labeled subsection below. Load this skill whenever you encounter a new company, need to evaluate a proposal, create prequalification documents, or populate a subcontractor folder.

---

## Phase 1: Entity Intake (absorbed from entity-intake)

Onboard a new project entity (company, contractor, supplier). Covers web research, cloud portfolio mapping, and documentation.

### When to Use

- User mentions a new project/entity name you don't recognize
- A new folder appears in Tqanny_Projects or Moqtana projects
- User says "this is not [other entity] project" — entity isolation signal

### Workflow

**Phase 1a: Identify the Entity**
- Extract entity name (Arabic + English) from PDF logos, folder names, file names
- Check project number/code in Tqanny_Projects (e.g., `/010`)
- Entity isolation: Ask "Is this [EntityName] or [OtherEntity]?" — if corrected, note prominently

**Phase 1b: Web Research (4 Sources Minimum)**
Use DuckDuckGo (not Google — captcha-prone). Search Arabic and English names.

| Source | What to extract |
|--------|----------------|
| DuckDuckGo | Search result snippets, URLs (`curl -sL "https://duckduckgo.com/html/?q=<query>"`) |
| LinkedIn | Company description, size, sectors, year (meta description tag) |
| Company website | Products, services, about page (check `/en/` and `/ar/` URLs) |
| Social media | Instagram bio, Facebook, X bio |

Extract: full name (AR + EN), parent company, years in market, factories/offices, products, client sectors, social handles.

**Phase 1c: Cloud Portfolio Mapping**
If the entity has a Google Drive folder:
1. Navigate with browser tool to the folder URL
2. Extract row data via `browser_console` JS: `Array.from(document.querySelectorAll('[role=row]')).map(r => r.textContent.trim())`
3. Classify folders by sector (residential, hospitality, commercial, government, healthcare)
4. Note shortcuts vs shared folders

**Phase 1d: Create Portfolio MD**
File: `Tqanny_Projects/[NNN]/ENTITY_NAME_PORTFOLIO.md`
Structure: entity header → Drive link → portfolio table by sector → local file inventory → entity isolation note

**Phase 1e: Save to Memory**
Keep under 250 chars: entity name + project number, isolation note, key facts, what needs development.

### Trigger Prequalification

If the entity is a supplier/manufacturer/contractor needing prequalification docs, proceed to **Phase 3** (Prequalification Package Design).

### Pitfalls

- Google Drive requires login for full visibility — note "requires login" if critical folders invisible
- DuckDuckGo may rate-limit — wait or use different User-Agent
- ole.sa and similar Saudi sites have broken English pages — use Arabic URL path
- Entity isolation is critical — if user corrects "this is NOT Samaya", state it clearly in portfolio MD and memory
- LinkedIn meta descriptions are the most reliable single source for company facts
- DO NOT create a new skill for every entity — entity facts go to memory, technique stays in this umbrella

See `references/outline-enterprise-intake.md` for a complete worked example.

---

## Phase 2: Proposal Evaluation (absorbed from proposal-evaluation)

Evaluate vendor/consultant technical and commercial proposals against project scope (SoW, ER). Extract PDFs, cross-reference scope items, score weighted criteria, generate markdown evaluations and Excel comparison files.

**Prerequisite**: A well-defined SCOPE_REQUEST.md (or equivalent) must exist for the subcontractor. See `references/mep-designer-scope-template.md` for a reusable MEP designer scope definition pattern — build the scope document before evaluating offers against it.

### When to Load

- User sends PDF proposals/quotations and asks for evaluation
- User asks "قيم العرض دا" / "compare these proposals"
- User wants vendor comparison against SoW/ER requirements
- User references a quotation they received but the PDF is not on disk — you need to find it in Outlook first

### Pre-Step: Find Quotation Emails in Outlook

Before evaluating a proposal, you may need to locate the quotation email first. Samaya uses Microsoft Exchange/Outlook. The Outlook SQLite DB is at:

```
~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite
```

**Key columns in `Mail` table:**
- `Message_NormalizedSubject`, `Message_SenderAddressList`, `Message_Preview`, `Message_HasAttachment`, `Message_TimeSent` (Mac absolute time), `Message_PartiallyDownloaded`, `Record_RecordID`
- Convert time: `datetime(Message_TimeSent + 978307200, 'unixepoch')`

**Search strategy (try in order):** See `references/outlook-quotation-discovery-patterns.md` for the full reference — search ordering, chain reading, download state detection, and OneDrive stub handling.

#### Yesterday's-Email Discovery Pattern

When the user says "check yesterday's emails" for a specific subcontractor/project:

```sql
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       f.Folder_Name as folder,
       m.Message_SenderList as sender,
       m.Message_NormalizedSubject as subject,
       m.Message_HasAttachment as att,
       substr(m.Message_Preview, 1, 500) as preview
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE date(m.Message_TimeReceived, 'unixepoch', 'localtime') = date('now', '-1 day', 'localtime')
  AND (m.Message_NormalizedSubject LIKE '%<keyword>%' OR m.Message_SenderList LIKE '%<keyword>%')
ORDER BY m.Message_TimeReceived ASC;
```

Then extract ALL attached PDFs from those email IDs using AppleScript (touch-before-save pattern from outlook-email skill) and read them with pdftotext before evaluating.

**Key pitfall:** Do NOT report 4-byte OneDrive stubs (content="null") as found files. They are inaccessible cloud stubs. Note the path and advise opening Outlook to save the attachment.

### Workflow

**Step 1: Extract Proposals**
```bash
pdftotext -layout "path/to/proposal.pdf" /tmp/proposal.txt
```

**Step 2: Identify Reference Scope**
- SoW (Scope of Work) — sections like §13.9 Sustainability, §13.3 IAQ
- ER (Employer Requirements) — sections like §2.4D, §3.7
- SMP / Project Plan — Rev reference (e.g., Rev C04)

**Step 3: Build Evaluation Criteria**

| Category | What to assess |
|----------|---------------|
| Project Understanding | Does proposal demonstrate understanding of this specific project? |
| Scope Coverage | Does it cover all required phases (design → procurement → fabrication → construction → handover)? |
| Methodology | Advisory-only or hands-on? Site visits? Field presence? |
| Team | Number of named experts, CVs, location, commitment |
| Commercial | Fixed vs monthly, predictability, what's included/excluded |
| Risk | What risks fall on contractor vs vendor |

**Step 4: Site Visit Verification — CRITICAL**
- Search the exact proposal text for keywords: site, visit, field, trip, travel, mobilization
- Quote the exact sentences with page/section numbers
- If zero mentions of site presence, state that explicitly

**Step 5: Critical Review (When Asked for Weaknesses/Contradictions)**

If user says "طلع منه نقاط الضعف والخلل والتناقض":

1. **Extract contradictions** — pricing model inconsistencies, VAT treatment errors, scope claims vs assumptions, numerical errors (missing digits, wrong totals)
2. **Identify AI-generation markers** — generic company name, placeholder experts ("Expert 1", "Expert 2"), AI-typical phrasing ("comprehensive", "robust", "seamless", "end-to-end"), no legal entity name
3. **Verify VAT/Tax validity** — non-KSA entities cannot charge Saudi VAT. If they list VAT but are based abroad → fraudulent or mistaken
4. **Check travel cost attribution** — who pays for site visits?
5. **Assess team credibility** — named experts with CVs vs placeholders
6. **Contradiction severity classification:**
   - 🔴 High: lump-sum vs time-based, VAT include vs exclude, wrong totals
   - 🟡 Medium: scope contradictions (Oddy managed but excluded)
   - 🟢 Low: editorial (typos, missing table columns)

**Step 6: Generate Outputs**

Per-proposal markdown evaluation + multi-sheet Excel comparison (use openpyxl):
- **Sheet 1** — Scope Understanding Comparison
- **Sheet 2** — Detailed Scope Matrix (RAG coloring: green `C6EFCE`, red `FFC7CE`, yellow `FFEB9C`)
- **Sheet 3** — Recommendation, conditions, risk notes
- **Sheet 4** — Cost Comparison (optional: multiple durations with breakeven point)

### Citation Rule

Every comparative claim MUST cite the source: page number, section heading, exact quote. If documents are OneDrive-locked, extract from what you have and note the limitation.

### Procurement Folder Organization

When organizing collected quotations into a project folder, use this standard structure:

```
<Category_Name>/
├── 01_Quotations/       # Vendor proposals, pricing sheets
├── 02_Reference/        # Product spec sheets, brochures, datasheets
└── README.md            # Summary table: vendor, model, status, file location
```

**Distinguish clearly between LiDAR scanning services (terrestrial building survey) and handheld 3D scanner equipment purchase.** They serve different purposes:
- Scanning services → dedicated category folder (e.g. `Lidar_Scanning_Services/01_Quotations/`)
- Equipment purchase → subcontractor's `10_Purchasing/` directory (e.g. `01_Replica_Model_Contractor/10_Purchasing/3D Scanner/`)

See `references/outlook-quotation-discovery-patterns.md` for vendor patterns and folder examples.
See `references/zna-lighting-quotation-gap-analysis.md` for a worked example of the full email-discovery → extraction → gap-analysis → contract-readiness workflow (Aseer Museum lighting designer).
See `references/contract-readiness-assessment.md` for the final synthesis step — combining proposal gaps + CG comments + scope split + fee re-baseline into a go/no-go recommendation.

### Excel Comparison Sheet Standards (Samaya)

When creating comparison/recommendation spreadsheets:

- **Use formulas, not static text** — totals = SUM of line items, VAT = total × 0.15, grand total = subtotal + VAT
- **Number formats** — use `#,##0" SAR"` so Excel treats them as numbers, not text strings
- **No empty/placeholder cells** — truly blank where N/A, don't write "--" or "N/A" into empty fields
- **Balanced tabs** — if one vendor gets a software options tab, every vendor with software gets one
- **Recommendation sheet** — short bullet reasons + cost comparison table + 1-line conclusion. No verbose executive summaries or AI-sounding paragraphs
- **Color scheme** — dark navy header (`#1F3864`), white text, alternating row fills (`#E9EFF7`), yellow total rows (`#FFF2CC`), clean thin borders (`#B4C6E7`)
- **Freeze panes** — always freeze header row so labels stay visible when scrolling
- **Orientation** — landscape, fit to page width

### Payment Schedule Structuring & Negotiation

When a subcontractor's commercial proposal includes a payment schedule, it is rarely aligned to the project's actual approval gates. Design consultants especially tend to front-load payments based on their internal design progress (e.g., 40% at "90% design complete") rather than submittal-register milestones.

#### When to Use

- A subcontractor's payment milestones are based on their internal progress %, not project milestones
- The schedule is front-loaded (e.g., 40%+ paid before submittal approvals)
- Stage 5 (IFC/AFC construction support) is listed as an optional extra
- Stage 6 (as-built/handover) is missing or "not costed"

#### Workflow

**Step 1: Extract the Vendor's Proposed Schedule**

From the proposal PDF or email, extract the milestone structure:

```
Vendor's proposal:  Mobilisation 10% → 50% design 20% → 90% design 40% → 100% 30%
```

Calculate what % of fee is paid before submittals are actually approved by CG/NRS.

**Step 2: Build a Counter-Proposal Tied to Submittal Register Gates**

Map each payment to a specific deliverable approval milestone from the project's submittal register:

| # | Milestone | Trigger (Submittal Register Item) | % | Amount |
|---|---|---|---|---|
| 1 | Mobilisation | Signed appointment + action plan + CRS submitted | 10% | £X |
| 2 | 50% Design | LG-001, LG-002 approved by CG/NRS | 15% | £X |
| 3 | 90% Design | All LG items (LG-001 to LG-0NN) approved | 30% | £X |
| 4 | 100% Design | All design deliverables finalised and IFC-ready | 25% | £X |
| 5 | IFC/AFC | Approved IFC package + design certification | 15% | £X |
| 6 | Stage 6 / Final | As-built verification + commissioning witness complete | 5% | £X |

**Key principle:** The 90% milestone should NOT exceed 30% of total fee. If the vendor proposes 40%+ at 90%, they are being paid more than half before the design is approved — this removes their incentive to complete.

**Step 3: Push Back on Stage 5 (IFC/AFC) as Optional Extra**

Construction support (shop drawing review, RFI responses, mock-up review) is a **standard professional service**, not separate scope. If the subcontractor lists Stage 5 as optional:

- Argue: "Without Stage 5, there is no mechanism to verify installed work matches approved design — this is a professional obligation, not an option"
- Counter-propose: Include in base fee. If they insist on separate line, negotiate down to ~10-15% of total fee (not 50%)
- Reference: Industry standard is ~10-15% of design fee for construction support

**Step 4: Require Stage 6 to Be Costed**

If the proposal says "Stage 6 — Not costed":
- Minimum requirement: as-built design verification + commissioning witness
- Aftercare (seasonal re-focus, POE, DLP) can be call-off arrangement
- Allocate ~5% of total fee for Stage 6 in the schedule

**Step 5: Address Payment Terms**

Check for:
- Payment window (e.g., "15 days from invoice" — tight but standard)
- Stop-work clause ("stop work if unpaid" — common but push to align with main contract)
- Rate lock (annual adjustment → cap rates for project duration)
- LD clause (missing → add back-to-back with main contract)
- Insurance requirements (missing → add PI ≥ £1M, PL ≥ £2M)

#### Common Subcontractor Payment Schedule Patterns

| Pattern | Risk | Counter |
|---------|------|---------|
| 10/20/40/30 (front-loaded 90%) | HIGH — 70% paid before IFC | Cap 90% milestone at 30% |
| 100% on design completion | MEDIUM — no holdback for IFC/AFC | Split into 4-5 milestones |
| Stage 5 as "optional extra" | HIGH — no construction support | Include in base fee |
| Stage 6 "not costed" | HIGH — no as-built verification | Add 5% line item |
| No mobilisation | LOW — but check if scope can start without payment | Accept or add 5-10% mobilisation |

**When the vendor's response includes line-item exclusions on the submittal register (e.g., "LG-005 coordination only", "LG-011 not in scope"):**

- Accept concessions that shift execution to another party (RCP coordination → MEP, cabling details → M&E)
- Push back on design-intent items only the lighting/design specialist can provide (exit signage coordination, performance criteria for specialist subcontractors, conservation specs)
- Document the accepted concessions clearly so the project scope split is unambiguous

### Scope Carve-Out Response Strategy

When a subcontractor responds with a list of items they consider "not in our scope" or "coordination only," use this framework to decide which to concede vs. push back.

#### Assessment Framework

| Factor | Concede (Accept Exclusion) | Push Back (Require Inclusion) |
|--------|---------------------------|-------------------------------|
| **Who else can cover it?** | Another appointed subcontractor clearly covers it | No other party in the contract chain covers it |
| **CG/consultant comment?** | Not mentioned by CG | CG Code B specifically requires it (Comment #1, #6, etc.) |
| **Design dependency** | Execution detail (cable routing, shop dwg production) | Design-intent decision (lux levels, CCT, conservation criteria) |
| **Effort** | Significant scope addition requiring major fee adjustment | Standard deliverable, minimal effort (narrative summary, coordination input) |

#### Worked Decision Matrix (Lighting Designer Example)

| Exclusion | Decision | Rationale |
|-----------|----------|-----------|
| Exit signage specs | **Push back** (coordination minimum) | CG #1 requires it; no other party specifies exhibition-space exit signs |
| Design narrative report | **Push back** (brief summary) | DMP requirement (CG #5); minimal effort — documents existing design approach |
| Elevations/sections | **Concede if deferred** to 90%+ stage | OK to issue later, not a gap |
| Showcase lighting (coordination only) | **Concede** with conditions | Set performance criteria (CRI/CCT/lux) for showcase specialist to follow; designer reviews for visual consistency |
| RCP coordination with other services | **Concede** | MEP designer / contractor handles ceiling coordination |
| Cabling information | **Concede** | M&E covers detailed routing; designer provides control topology + load requirements as input |
| Site focusing direction | **Push back** | SOW §8.8 explicitly requires "final light balancing and focusing by lighting specialist consultant" |
| O&M / spares data | **Push back** | SOW §6.22.3 contract deliverable; designer must state maintenance requirements |

#### Response Template

When drafting the reply email addressing scope carve-outs:

1. **Acknowledge** — acknowledge receipt of their response
2. **Categorise** — table mapping each exclusion to the requirement source
3. **Concede** — state which exclusions you accept and how the gap will be covered by another party
4. **Push back** — for items the CG requires, state they are not negotiable and must be included in the base fee
5. **Request confirmation** — ask them to revise scope or provide fee adjustment for added items

Template structure (email body):

```
Scope Items You Have Marked as Excluded

[Table: Item | Your Position | Our Position | Source]

Payment Schedule

[Table comparing their proposal vs your counter-proposal with £ amounts]

Stage 5 — IFC/AFC Construction Support
[State position: include in base fee or propose reduced fee]

Stage 6 — As-Built / Aftercare
[Request cost for minimum scope]

Action Plan
[State timeline for providing programme]

Submittal Register Comments
[Address their line-item comments individually: accept, counter, or escalate]
```

### Pitfalls

- Don't evaluate against certification standards if user says they're not required
- Don't claim site presence without quoting the proposal text
- Don't use different evaluation criteria across proposals — same matrix for all
- Don't overlook VAT legality — non-KSA consultants cannot charge Saudi VAT
- Don't assume "lump-sum" means fixed price — some claim lump-sum but are time-based with cap
- AI-generated proposals are increasingly common — check for contradictions, unnamed entities, generic language
- **No AI fluff in recommendation sheets** — Mohamed explicitly rejects verbose prose. Keep it bullet-granular: cost table → why bullets → conclusion.
- **Design-only vs installer split is a common negotiation point** — specialist designers (lighting, AV, FLS) typically design only, with installation by the M&E Contractor. When a designer excludes installation items, verify another party is contracted to execute them before conceding.
- **Front-loaded payment schedules are the norm in initial proposals** — always counter with submittal-register-tied milestones. The 90% milestone should NEVER exceed 30% of total fee.
- **"Not costed" means "we haven't thought about it" not "it's free"** — always require a cost for any missing stage (especially Stage 6 handover/as-built).
- **Subcontractor reply may arrive with "on leave until X"** — note the return date and schedule your reply accordingly. The draft sits in their inbox; do not chase until after the leave period unless urgent.

See `references/worked-example-sustainability.md` for a complete evaluation session (Aseer Museum sustainability consultancy).

### Technical Offer Gap Analysis — Detailed Scope Comparison

When a single subcontractor's technical offer needs detailed comparison against a comprehensive SCOPE_REQUEST (not multiple-vendor scoring), use this method. It detects gaps in scope, role, timeline, deliverables, and compliance.

#### When to Use

- User sends a technical offer/proposal from one vendor and asks for gap analysis against the SCOPE_REQUEST
- Pre-procurement: verify a shortlisted vendor's scope before recommending award
- Post-receipt: provide ammunition for negotiations or scope clarification requests

#### Workflow

#### Step A: Extract Offer Content
- For scanned PDFs: use PyMuPDF to render pages, then vision-capable agent or OCR for extraction
- For text PDFs: pdftotext -layout, then grep/pattern-match for discipline headings
- Flag missing text early (scanned PDF, garbled tables) and compensate with fallback extraction

**⚠️ Chronology check — subcontractor SOW may be stale.** Samaya's Technical Office may have issued a Rev 01 (or higher) of the SOW after the subcontractor submitted their quotation. Always check the subcontractor's `00_Scope_of_Work/` folder for Samaya-authored `.md` or `.docx` SOW files with a revision date LATER than the quotation date. These represent scope refinements the subcontractor hasn't priced. Include these in the gap analysis as "Scope added by Samaya revision — not in vendor's base quote." Cross-reference against the quotation's stated scope items to catch every unbudgeted deliverable.

**Step B: Pre-Check — Role Alignment (check FIRST)**

Before any line-by-line comparison, identify the offer's stated role:

| Offer Says | Means | Red Flag? |
|-----------|-------|-----------|
| "Design Verification and Endorsement" | Third-party checker, not producer | 🔴 Verifier — can't produce original designs |
| "Independent Engineering Design Firm" | May not take EoR responsibility | 🟡 Confirm Lead Designer status |
| "MEP Engineering Design Consultancy" | Design producer | ✅ Aligned |

If the offer states a role mismatch (verifier vs. producer), flag this as the **primary critical gap** — no amount of line-item coverage fixes the wrong service model.

**Step C: Build Section-by-Section Coverage Matrix**

Create a table mapping every SCOPE_REQUEST subsection against the offer's coverage:

| # | SCOPE_REQUEST Section | Offer Coverage | Gap Severity |
|---|----------------------|----------------|-------------|
| 2.1 | Mechanical | Partial — HVAC covered, missing BMS points, AV coordination | MODERATE |
| 2.4 | Fire Protection | Partial — sprinklers covered, missing clean agent, kitchen hood | HIGH |
| 2.8 | Existing Services Survey | **COMPLETELY MISSING** | CRITICAL |

**Step D: Rate Gaps by Severity**

| Severity | Criteria | Example | Action |
|----------|----------|---------|--------|
| 🔴 **CRITICAL** | Role mismatch, entirely absent scope sections, explicit exclusion of core deliverables | No existing services survey, BIM excluded, construction support excluded | Deal-breaker unless remediated |
| 🟠 **HIGH** | Missing major subsystems, timeline incompatible, regulatory gaps | No CITC-registered telecom, no clean agent, no external works | Requires specific addendum |
| 🟡 **MODERATE** | Partial coverage, missing detail, insufficient specificity | ELV missing MATV/intercom, SEC coordination detail | Negotiable with clarification |
| 🟢 **LOW** | Minor omissions, good coverage overall | Plumbing mostly covered, some documentation gaps | Acceptable |

**Step E: Timeline / Programme Compatibility Check**

Map the offer's proposed schedule against the project's actual timeline:

| Aspect | Offer | Project Needs | Gap |
|--------|-------|---------------|-----|
| Model | Sequential review cycles | Fast-track overlapping gates | 🔴 |
| Duration | 45+45 working days for 2 review cycles | 19 weeks for 50→90→100→IFC production | 🟠 |
| Gates | No concept of 50/90/100 | Explicit design gates per contract | 🔴 |
| Fast-track | Not mentioned | Backbone IFC at 50% gate for procurement | 🔴 |
| Site survey | Not a milestone | Existing services survey required first | 🔴 |

**Step F: Deliverables Matrix**

Table comparing SCOPE_REQUEST-required deliverables vs. what the offer includes:

| SCOPE_REQUEST Deliverable | Offer Includes? | Note |
|---------------------------|----------------|------|
| Site survey report + capacity validation | ❌ Missing | |
| 50% Design drawings + specs | ❌ Not defined | Offer uses different nomenclature |
| BIM Revit models LOD 300+ | ❌ Excluded | Explicitly stated out of scope |
| As-built drawings | ❌ Missing | |
| O&M manuals | ❌ Missing | |

**For commercial-gap analysis (single vendor, pre-contract):** Extend this to include fee status per deliverable group and whether the quoted fee covers it:

| Scope Item | In ZNA Quote? | Fee Covers? | Source |
|------------|---------------|-------------|--------|
| Stage 4 — Technical Design | ✅ £21,227 | ⚠️ Partial — 8 deliverables added by Samaya Rev01 SOW not in base scope | Project SOW Rev01 §4 |
| Stage 5 — Shop dwg review + site focusing | ⚠️ £10,875 optional, site focusing NOT included | ❌ No | SOW §8.8 mandates focusing |
| Stage 6 — Handover & aftercare | ❌ Missing | ❌ No | SOW §11, ER §2.7 |
| BIM authoring LOD 300 | ❌ Not mentioned | ❌ No | BEP / DMP |

**Step G: Regulatory Compliance Check**

For KSA projects, verify the offer covers:
- SBC compliance (all sections — 201, 401, 601, 701, 801)
- CITC registration (for telecom scope)
- SEC coordination (power tie-in)
- STC FTTH guidelines (if applicable)
- Civil Defense / MOI requirements
- SASO / SABER (where relevant)

**Step H: Check CG Review Status (Aseer/Samaya projects)**

Before finalising the gap analysis, check if the subcontractor's scope document was submitted to CG (Consultant/Government) for review:

1. Search Outlook for the submittal doc code (e.g. `MOC-MUS-ASE-1E0-ZD-0056`) in subject or attachments
2. Identify the CG response Code:
   - **Code A** — Approved (no further action)
   - **Code B** — Approved with Comments (CRS needed — cross-reference CG comments against proposal)
   - **Code C** — Revise & Re-submit (proposal cannot proceed as-is)
   - **Code D** — Disapproved
3. If Code B: map each CG comment to the proposal scope section. Identify which are covered, which need ZNA confirmation
4. If Code C/D: report that the proposal is blocked and cannot proceed to contract

**Key:** CG comments may add requirements not in the original ER/SOW (e.g., CG comment #3 requiring a dated action plan, #8 requiring meetings/site visits). These become additional conditions for the subcontractor's scope.

**Step I: Synthesise Contract Readiness**

Combine all findings into a single go/no-go recommendation:

| Dimension | Status |
|---|---|
| Proposal scope gaps | ✅ / ⚠️ / ❌ |
| CG comment coverage | ✅ / ⚠️ / ❌ |
| Scope split alignment | ✅ / ⚠️ / ❌ |
| Fee reasonableness | ✅ / ⚠️ / ❌ |
| Terms alignment | ✅ / ⚠️ / ❌ |
| **Overall verdict** | **GO / CONDITIONAL / NO-GO** |

If CONDITIONAL: list specific conditions (revised fee, added deliverables, LD clause) that must be met before contract.

If fee re-baselining is needed: estimate the revised total when scope items are added/removed:

| Item | Original Quote | Adjustment | Revised Estimate |
|---|---|---|---|
| Stage 4 | Original fee | +added deliverables | ~estimate |
| Stage 5 | Original fee | Removed/produced items | ~estimate |
| Stage 6 | — | Added scope | ~estimate |
| **Total** | | | **~revised total** |

**Step J: Summary & Recommendation**

1. **Verdict** (Accept / Revise / Reject)
2. **Critical finding** (one sentence)
3. **Gap severity counts** (X critical, Y high, Z moderate, W low)
4. **Conditions for acceptance** (if conditional)
5. **Next action** (draft reply, prepare CRS, etc.)

#### Pitfalls

- **Role mismatch is the silent killer** — an offer that looks comprehensive on paper but is structured as verification/review cannot produce original designs. This invalidates the whole comparison.
- **Offer may be internally inconsistent** — templated from a design proposal but described as verification (e.g., payment milestones referencing "Schematic Design" but scope says "verification only")
- **Scanned PDFs are unreliable** — headers/footers and table content often lost during OCR. Accept ~85% extraction accuracy.
- **AI-generated offers are increasingly common** — look for placeholder names, generic phrasing ("comprehensive", "robust", "end-to-end"), and contradictory exclusions
- **Timeline is the hardest gap to fix** — compressed programmes need overlap, acceleration, and early IFC gates. An offer proposing sequential review cannot adapt.
- **Construction support exclusions are non-negotiable** — if the offer explicitly excludes site/construction-phase services, you need a separate contract for post-IFC support.
- **BIM exclusion is NORMAL for designer sub-consultants** — Samaya BIM Unit handles BIM from 2D CAD. Do NOT flag BIM exclusion as a gap unless the SCOPE_REQUEST explicitly requires the designer to produce BIM models. Most designer offers will exclude BIM, and this is correct per Samaya's operating model.
- **Existing services survey is often missing** — many MEP designer offers skip the condition/record survey of existing building services (capacity validation, visual inspection, tagging). This is a CRITICAL gap because design cannot start without knowing what's already installed. Always check this specifically.
- **Gallery environmental/acoustic conditioning is a specialized gap** — MEP designers may cover standard HVAC but miss the museum-specific gallery environment requirements (stable RH, acoustic isolation, air quality for conservation). Flag this as a separate scope item, distinct from general HVAC coverage.

See `references/worked-example-ad-engineering-offer-gap-analysis.md` for a full worked example (Aseer Museum MEP Designer offer review).

---

## Phase 3: Prequalification Package Design (absorbed from supplier-prequalification + prequalification-profile-development)

Design prequalification submission documents and professional capability profiles for Saudi industrial/manufacturing/construction companies. Covers company research, PDF extraction, document creation (DOCX/MD/HTML), photo extraction, and Claude-driven design.

### ⚠️ CRITICAL TIMING RULE — Prequal BEFORE Design

Prequalification must complete BEFORE 50% design starts. Design teams need to know which vendors/suppliers are approved so they reference real products, not generic "TBC" specs.

**Sequence:**
```
Prequalification ──→ 50% Design ──→ Material Submittals ──→ 90% Design
     (done)        (known vendors)   (prequalified submit)   (approved materials)
```

Specialized museum trades (AV, showcase, lighting, scenography) need prequal EARLIEST — their design depends on knowing the vendor's product range, lead times, and integration requirements.

**Consequence of skipping**: 50% design uses generic specs → material submittals get rejected → 90% design rework → schedule slip. Always push prequal to run during or before the assessment phase, parallel with mobilization.

### When to Use

- Entity intake (Phase 1) identified gaps in prequalification documents
- User asks to "develop prequalification" for a supplier/manufacturer
- Need to create capability statements, checklists, or compliance matrices
- Need a professional printable company profile (HTML/DOCX)

### Distinction from Phase 1

Phase 1 (Entity Intake) covers **research** — understanding who the entity is. Phase 3 covers **design** — creating submission-ready documents.

### Workflow

**Phase 3a: Gather Source Data**

Collect from entity-intake output + additional sources:
- Corporate profile PDF — CR number, GOSI, VAT, factory location, certifications, project references
- Company website — products, services, team
- LinkedIn — description, sectors served, years in market
- Google Drive portfolio — project list, client names, photo/media

**Phase 3b: Create 4 Core Document Types**

| Folder | Document | Purpose |
|--------|----------|---------|
| `01_Submission_Document/` | PREQUALIFICATION_SUBMISSION_DOCUMENT | Main 8-section submission |
| `02_Checklists/` | FACTORY_PREQUALIFICATION_CHECKLIST | Tailored for manufacturer (not generic subcon) |
| `03_Capability_Statement/` | COMPANY_CAPABILITY_STATEMENT | Professional company overview |
| `04_Compliance/` | COMPLIANCE_MATRIX_TEMPLATE | Project-fillable compliance matrix |

**Key differentiator:** These are **MANUFACTURER-FACTORY focused**, not subcontractor-focused. Include industrial license, SASO/SABER, production capacity & equipment list, factory zones, local content (LCWA/ICP), Nitaqat/Saudization, Saudi Building Code compliance.

**Format:** `.md` for readability + `.docx` (python-docx) for professional submission.

**Phase 3c: Design HTML Capability Profile (Critical — use Claude Code)**
```bash
claude -p 'Create A4 landscape capability profile...' --max-turns 25
```

Design mandates:
- English-led bilingual (English heading first, Arabic smaller below)
- Google Fonts: Inter (headings), Plus Jakarta Sans (body)
- Logo + real photos from source PDF as base64 data URIs
- A4 Landscape: `@page { size: 297mm 210mm landscape; margin: 0 }`
- 7-page structure: Cover, About, Manufacturing, Products, Portfolio, Quality, Why Us
- Print button: `onclick="window.print()"`
- Self-contained: all CSS inline, all images as base64 data URIs

**Phase 3d: Saudi Arabia Specific Requirements**

Must include: Commercial Register (CR) with industrial classification, Zakat & Tax certificate, GOSI certificate, Nitaqat/Saudization %, Chamber of Commerce, SASO/SABER, Saudi Building Code (SBC), LCWA/ICP registration, Etimad, ISO 9001/14001/45001, Industrial license, Municipality license, Civil Defense approvals.

**Phase 3e: Image Embedding Pattern**
```python
import base64, fitz
doc = fitz.open('corporate.pdf')
# ... extract images
def uri(data, mime='image/jpeg'):
    return f'data:{mime};base64,' + base64.b64encode(data).decode()
# Write HTML with __PLACEHOLDER__ tokens, then replace
```

### Phase 3b-i: Fill Engineer-Provided Compliance Sheets

When the Engineer provides their own compliance Excel format (e.g. `064023 - INTERIOR ARCHITECTURAL WOODWORK.xlsx`, `061000 - ROUGH CARPENTRY.xlsx`), **fill that format** — do NOT create a new one. The user has explicitly corrected this: "he said you have to fill our compliance sheet dont make new one."

#### When to Use

- Engineer/Consultant sends a compliance Excel template with spec text already embedded
- User says "fill their compliance sheet" or "update the compliance sheet"
- Rev02 or later revision arrives with new datasheets from the supplier team

#### Engineer's Format Structure

| Column | Content | Who fills |
|--------|---------|-----------|
| No. | Clause number | Pre-filled by Engineer |
| Section | Section reference | Pre-filled by Engineer |
| Specifications | Full spec text (e.g. "Density: 700-850 kg/m³") | Pre-filled by Engineer |
| Manufacturer / Supplier Statement | Achieved value + product name | **We fill** |
| Compliance | ✓ / △ / — | **We mark** |
| Remarks | Source file reference, notes | **We fill** |

#### Workflow

**Step 1: Inventory new evidence** — list all new datasheets/PDFs in the Rev folder. Classify each by what spec clause it addresses.

**Step 2: Extract achieved values** — use `pdftotext -l 3` to get key numerical data from each datasheet. Focus on:
- Physical properties (density, MOR, MOE, IB, thickness swelling, screw holding)
- Fire test results (FSI, SDI, class rating, test standard)
- Formaldehyde/emission data
- Material grade/classification
- Standards cited (ASTM, BS EN, EN, etc.)

**Step 3: Map each datasheet to spec clauses** — for each clause in the Engineer's sheet, find the matching achieved value from the datasheets. If a clause has no matching evidence, mark it as pending.

**Step 4: Fill Manufacturer/Supplier Statement** — write the actual achieved value and product name. Format: `[Value] ([product name], [manufacturer])`. Example: `800.8 kg/m³ (Verdo FR MDF, Danube)`

**Step 5: Mark Compliance** — use these rules:

| Mark | Meaning | When |
|------|---------|------|
| ✓ | Compliant | Achieved value meets or exceeds spec requirement |
| △ | Partial | Value exists but standard/format differs (e.g. EN vs ASTM), or manufacturer declaration still needed |
| — | Pending | To be confirmed at shop drawing / material selection stage |

**Step 6: Add Remarks** — always include the source file path (relative to submission root) and any caveat. Example: `Verdo FR MDF TDS — Rev02/التقديم 14-7/Data sheet/TDS FR MDF E0 NAUF CARB P2 -B.pdf`

**Step 7: Critical compliance check** — before marking ✓, verify the achieved value ACTUALLY meets the spec. Common pitfalls:
- **Fire class mismatch**: Spec says Class A (FSI ≤25) but product is Class B (FSI 35) → mark △, not ✓. Note the alternative acceptance path if one exists (e.g. BS 476 Class 0 coating system).
- **Standard mismatch**: Spec cites ASTM E84 but datasheet gives EN 13501-1 → mark △, note the standard difference.
- **Irrelevant datasheets**: Lighting/LED datasheets in a woodwork submission → flag as not relevant, do not include.

#### Pitfalls

- **Do NOT create a new compliance sheet** — the Engineer's format is the authoritative one. Fill their columns, don't restructure.
- **Do NOT copy old compliance data blindly** — Rev02 may have new evidence that changes △→✓ or reveals new gaps (e.g. Verdo FR MDF is Class B, not Class A).
- **Do NOT mark ✓ for fire compliance when the product is Class B and spec requires Class A** — note the gap and the alternative acceptance path (e.g. Ritver coatings provide BS 476 Class 0).
- **Irrelevant datasheets happen** — the Ola team may include unrelated products (LED strips, lighting). Exclude them from the compliance mapping.
- **Image-only PDFs** (SS 304 sheet, scanned certs) cannot be text-extracted — note as "image-based, needs visual verification."
- **The Engineer's format already has the spec text** — you only fill 3 columns: Statement, Compliance, Remarks. Do not modify the spec text column.
- **Fire compliance is the most common gap** — always check the actual FSI/SDI numbers against the spec's class requirement. A "Class B" product does not satisfy a "Class A" spec unless an alternative standard is explicitly accepted.

See `references/compliance-sheet-fill-pattern.md` for a worked example (Outline Enterprise Rev02 compliance update with Verdo FR MDF, Ritver coatings, and fire class gap analysis).

### Phase 3b-ii: Prequalification Profile Compliance Assessment

Evaluate a received company profile/prequalification dossier against the project's scope documents (SCOPE_REQUEST.md, SPEC.md, SoW, ER) to determine suitability and identify gaps.

#### When to Use

- A subcontractor submits a company profile for prequalification
- User asks "check if this complies with project specs"
- Need to decide whether to shortlist, reject, or request supplementary information

#### Workflow

**Step 1: Verify File Placement**

Check if the profile is already filed in the correct subcontractor folder. Compare MD5 hashes between Downloads and the target folder to avoid duplicates.

**Step 2: Read Project Requirements**

Read these documents in order:
1. `_MANAGER_DASHBOARD/SCOPE_REQUEST.md` — scope brief, submission requirements, portfolio criteria (≥3 similar projects, museum/cultural preferred)
2. `_MANAGER_DASHBOARD/SPEC.md` — deliverable breakdown by stage, coordination interfaces
3. `03_Specifications_and_Standards/` — SoW sections and ER extracts relevant to the trade
4. `01_Schedule_and_BOQ/` — BOQ items to understand scale and complexity

**Step 3: Extract Profile Data**

Use `pdftotext` to extract the profile content. Key data points:

| Data Point | What to look for |
|------------|------------------|
| Company registration | CR number, Ministry of Commerce, VAT cert |
| Portfolio | Project names, clients, sectors, scale |
| Team | Named roles, qualifications, depth |
| Certifications | ISO, Saudi Contractors Authority, Classification |
| Services offered | Design, supply, install, maintain |
| Geographic experience | Regions, climates, altitudes |

**Step 4: Gap Analysis Against Requirements**

Build a compliance table:

| Requirement (from SCOPE_REQUEST/SPEC) | Profile Evidence | Status |
|---|---|---|
| Portfolio: ≥3 museum/cultural/high-profile | List of projects with client names | ✅ / ⚠️ / ❌ |
| Aseer region / high-altitude experience | Projects in Abha, Taif, or similar | ✅ / ⚠️ / ❌ |
| Key personnel (Landscape Architect, etc.) | Named roles in org chart | ✅ / ⚠️ / ❌ |
| Hardscape + softscape capability | Services listed, portfolio examples | ✅ / ⚠️ / ❌ |
| Irrigation design | Irrigation technicians, past projects | ✅ / ⚠️ / ❌ |
| Commercial registration | CR number, Chamber of Commerce | ✅ / ⚠️ / ❌ |
| Certifications | ISO, SCA, Classification | ✅ / ⚠️ / ❌ |

**Step 5: Assess Scale & Complexity Fit**

Compare the profile's largest past projects against the project's scale:
- If all past projects are private villas and the project is a museum → scale mismatch
- If past projects are in lowland coastal cities and the project is high-altitude → climate/region gap
- If team is 1-2 people and the project needs multi-disciplinary coordination → depth concern

**Step 6: Recommend Supporting Documents**

When the profile has gaps, recommend specific project documents the sub can use to strengthen their submission. This is NOT a rejection — it's a constructive path to compliance.

| Gap | Supporting Document to Give Them | Why |
|-----|----------------------------------|-----|
| No museum/cultural portfolio | SCOPE_REQUEST.md + SPEC.md | Shows them the exact scope so they can map their relevant experience |
| No high-altitude experience | ER extracts (existing services, climate data) | Lets them propose a plant sourcing plan from local nurseries |
| Thin team | SoW §6.22.4(xv) — Horticulture/Landscape Design | Shows the full deliverable scope so they can propose adequate team |
| No weight loading experience | Stramp layout drawing + structural report | Lets them demonstrate structural coordination capability |
| No O&M manual sample | Submittal Register | Shows them what deliverables are expected |

**Step 7: Verdict**

| Verdict | Criteria | Action |
|---------|----------|--------|
| **Recommended** | Meets all requirements, strong portfolio | Proceed to offer stage |
| **Conditional** | Gaps exist but addressable with supporting docs | Send supporting docs + request supplementary submission |
| **Not recommended for sole appointment** | Major gaps (no museum experience, wrong climate zone, wrong scale) | Keep on file as potential execution subcontractor under a design lead; recommend they partner with a qualified design consultant |

**Step 8: Document the Assessment**

Save the assessment to `_MANAGER_DASHBOARD/PREQUALIFICATION_ASSESSMENT.md` with:
- Compliance table
- Gap analysis
- Supporting documents recommended
- Verdict and recommendation

#### Pitfalls

- **Same file in Downloads and target folder** — always MD5-check before moving. If identical, it's already filed.
- **Profile may look competent but wrong sector** — a residential landscaping contractor may have good credentials but zero museum/cultural experience. This is the most common gap.
- **High-altitude horticulture is a real constraint** — Aseer (Abha ~2,200m) has a unique microclimate. A contractor with only coastal/Jeddah experience cannot simply transplant their plant palette.
- **Team depth vs project complexity** — a 1-person Landscape Architect + 2 Engineers is thin for a project requiring design, shop drawings, installation supervision, and 90-day establishment period simultaneously.
- **Supporting docs are not a guarantee** — giving the sub the SCOPE_REQUEST and SoW helps them submit better, but it doesn't create museum experience they don't have. Be honest about fundamental gaps.
- **"Supporting documents" vs "rejection"** — frame the recommendation constructively. The sub may be a good execution partner even if not the right design lead.

### Phase 3b-i: PQD Review (Received) — Gap-and-Red-Flag Triage

The inverse of Phase 3b: instead of designing a prequalification document to send out, you receive a PQD PDF and produce a structured plain-text review with a verdict. This is the most common PQD task in practice — a 50–300 page company profile arrives via email/WhatsApp/OneDrive, and you need to answer "qualified / conditional / reject?" within a few hours.

#### When to Use

- User forwards a PQD / company profile PDF and asks for a review
- Aseer Museum-style prequalification triage (other consultants like NRS, CG, ICR use 6-section review templates)
- Need a go/no-go recommendation backed by cited evidence from the PQD

#### Workflow

**Step 1: Verify the file is what was requested — naming-mismatch check**

The #1 triage signal: do the file name and the asked-for company match the actual content? Mismatches are common when PQDs are forwarded out-of-order or via shared folders.

```bash
cp "/path/to/<USER-REFERENCED-FILE>.pdf" /tmp/pqd.pdf
pdftotext -layout -enc UTF-8 /tmp/pqd.pdf /tmp/pqd.txt
grep -inE "<asked-name>|company name|legal name|cr.{0,5}number|national.{0,5}number" /tmp/pqd.txt | head -10
```

| Mismatch Type | Signal | Action |
|---|---|---|
| User asked for "PQD for Smith" but file is "AKI PQD.pdf" and content is "Al Kalas International" | File name + content both disagree with the asked-for name | **Flag the mismatch at the top of the review** — do not silently substitute. Ask user to confirm the routing. |
| User asked for "PQD for X" and content is X | Aligned | Proceed |
| User asked for "PQD for X" and content is X's parent/sister company | Related entity | Note as related-party, not a mismatch |

**Step 2: Map the PQD's table of contents to its real content**

Many vendor PQDs list sections in the cover page TOC that are then **empty placeholders** (image-only, scan-only, or simply not filled in). Cross-check TOC vs. actual page content.

```bash
grep -inE "^(SECTION|CHAPTER|PHASE|PART|KEY PERSONS|EQUIPMENT|CLIENT|QUALITY|FACILITIES|CALIBRATION|PROJECT REFERENCE|PROJECTS COMPLETED)" /tmp/pqd.txt
```

Common PQD sections that are often placeholder-only in vendor submissions:
- "Client Approvals / List of Clients" — usually a cover page with no list
- "Project Reference List" — often absent
- "Equipment List" — cover image only, no make/model/capacity/count
- "Quality Manual" — TOC entry, no body
- "Facilities & Lab Equipment" — photographs, no text content
- "Equipment Calibration Certificates" — embedded scans, not extractable as text

For any placeholder section, **flag it as "PQD claims section X is included but extracted content is empty"**. Do NOT invent content to fill the gap.

**Step 3: Extract the 6 required data buckets**

Use `pdftotext -layout` for text-based PDFs (works for Word-exported vendor PQDs). For scanned/image-based PQDs, fall back to PyMuPDF + tesseract OCR per `document-analysis` skill.

| Bucket | What to look for | Typical location in PQD |
|---|---|---|
| **Company Info** | CR national number, VAT reg, Civil Defense lic, Nitaqat band, factory/office address, establishment year, management names, ownership structure | First 5–15 pages, "Company Profile" / "About Us" / "Legal Documents" sections |
| **Experience** | Project reference list (client, scope, value, date, role), pre-PQD history of key personnel | "Projects Completed" / "Project Reference" / "Key Personnel CVs" sections |
| **Technical** | Services offered, standards cited (ASTM/BS/EN/ISO), test methods, equipment list, methodology | "Services" / "Technical Capabilities" / "Disciplines" sections |
| **QA/QC** | ISO 9001/14001/45001, ISO/IEC 17025, sector-specific certs (SASO, SABER, ENAS, GAC, NABL, A2LA), audit history, calibration program | "Quality Manual" / "ISO Certificates" / "Accreditation" sections |
| **Red Flags** | Synthesised from gaps, mismatches, accreditation scope, project-less PQD, fresh-entity, non-GCC accreditor | Cross-cutting — derived from the four buckets above |
| **Recommendation** | Not Qualified / Conditional / Qualified, with cited reasons and a list of supplementary documents required for any conditional path | Last section of the review |

**Step 4: Cross-check the supplier's declared scope vs. the project scope**

The most common reject cause: supplier's stated services have **zero overlap** with the project scope. Example patterns:

| Project Scope | Wrong Supplier Type | Why reject |
|---|---|---|
| Museum / heritage / exhibition fit-out (AV, lighting, graphics, showcase, scenography) | Civil materials testing lab | No museum-grade work in 288-page PQD |
| Concrete & structural QC subcontractor | Architectural designer | Wrong service model (design vs. test) |
| MEP design consultant | Equipment vendor | No design team, only supply |
| Specialist fit-out subcontractor | General contractor with no specialist team | No specialist depth |

**Always state the alignment check explicitly** in the review: "Supplier scope (X) vs. project scope (Y) → aligned / tangential / misaligned."

**Step 5: Red-flag catalog (reuse across PQD reviews)**

Build up a personal list of red-flag patterns. Common ones:

1. **File-name / company-name mismatch** — user asked for "Smith", file is for "Al Kalas" or "AKI". Flag at top, do not silently proceed.
2. **Wrong scope** — supplier's services have zero overlap with project scope. The strongest reject signal.
3. **Brand-new entity in KSA** — CR issued < 6 months, all senior staff joined within the same month, no track record. Acceptable for some scenarios (e.g. local-content preference) but not for prequal of complex specialist scopes.
4. **No project reference list** — vendor PQDs almost always *claim* a "Projects Completed" section. If it's a placeholder or absent, this is a major gap. A PQD without a project list cannot be qualified.
5. **No equipment list** — vendor claims 27+ services and a 232 m² lab but lists zero equipment with make/model/capacity. Capacity is unverifiable.
6. **Fresh ISO/IEC 17025** — first issue < 12 months ago. First surveillance audit not yet completed. Verify acceptance with the Consultant (CG) — they often require at least one clean surveillance audit on file.
7. **Non-GCC 17025 accreditor** — issuing body is US/India/UK commercial registrar (e.g. "American Quality System Registrars", "AMERI COQUALITY"). Not a Gulf/Saudi signatory (SASO, GAC, ENAS, Dubai Accreditation Center, etc.). CG may or may not accept — verify.
8. **ISO 9001/14001/45001 from low-tier commercial certifier** — certs from a body with no IAF/MLA accreditation. Same GCC-acceptance caveat.
9. **Heavy single-nationality management** — all 5 named senior managers are the same nationality. Fine in principle but flag for projects requiring a more diverse leadership profile or specific national presence.
10. **All certificates < 12 months old** — VAT, Nitaqat, Monsha'et, ISO — every cert issued in the last 6 months. The company is in start-up phase; verify they can sustain operations.
11. **No KSA-track-record for senior staff** — all CV experience is from home country. Only one person has prior KSA experience. Risk on KSA-specific compliance.
12. **Marketing-style PQD** — pages of glossy company prose, but missing the structured prequalification schedule sections: legal entity details, similar-project experience, key personnel CVs with project references, methodology, HSE, QA plan, financial standing, insurance, litigation history, current commitments. The PQD is technically complete as a brochure but materially non-compliant with the project's prequalification requirements.
13. **Placeholder sections with no content** — see Step 2. The most common: empty "Client Approvals" / "Project Reference" / "Equipment List" pages that are present in the TOC but blank in the body.
14. **PQD mismatch with project language** — PQD is in Arabic only, project SOW is bilingual, or vice versa. Not a reject but flag for follow-up.

**Step 6: Synthesise the verdict**

| Verdict | Criteria | Action |
|---|---|---|
| **NOT QUALIFIED** | Wrong scope, brand-new with no track record, no project list + no equipment list, fresh + non-GCC 17025 with no surveillance, multiple high-severity red flags | Reject. List specific gaps so the user can confirm. |
| **CONDITIONAL** | Mostly aligned, but missing 1–2 critical items (e.g. project list, equipment list, financials) | Recommend shortlisting **only after** the listed items are supplied. |
| **QUALIFIED** | Aligned scope, demonstrable track record, valid GCC-acceptable certs, named KSA-experienced team | Recommend award subject to standard contract terms. |

**Step 7: Output the review in plain text**

The standard output format is a single plain-text file with the 6 sections from Step 3, in the order: Company Info → Experience → Technical → QA/QC → Red Flags → Recommendation. Use this template:

```
================================================================================
PQD REVIEW — <Supplier Legal Name> ("<filename>", <N> pages, <rev>)
Project: <Project Name> — Supplier Prequalification Review
================================================================================

NOTE ON FILING: <state any name/scope/routing mismatch up front>

--------------------------------------------------------------------------------
COMPANY INFO
--------------------------------------------------------------------------------
- Legal name:           ...
- CR National Number:   ...
- ...

--------------------------------------------------------------------------------
EXPERIENCE
--------------------------------------------------------------------------------
- <no project list, no client list, no track-record table>
- <pre-PQD history of named senior staff>
- <any project examples cited in CVs>
- <sector relevance verdict>

--------------------------------------------------------------------------------
TECHNICAL CAPABILITIES (as offered)
--------------------------------------------------------------------------------
- <services list with disciplines>
- <standards cited>
- <scope coverage vs. project scope>

--------------------------------------------------------------------------------
QA / QC & CERTIFICATION
--------------------------------------------------------------------------------
- <ISO 9001/14001/45001 with cert numbers and validity>
- <ISO/IEC 17025 with cert number, validity, issuing body, scope>
- <auditor history / surveillance status>
- <Quality Manager credentials>

--------------------------------------------------------------------------------
RED FLAGS
--------------------------------------------------------------------------------
1. <flag, evidence, severity>
2. ...

--------------------------------------------------------------------------------
RECOMMENDATION
--------------------------------------------------------------------------------
<NOT QUALIFIED / CONDITIONAL / QUALIFIED>
<one-paragraph rationale>
<suggested actions: (a) confirm routing, (b) request supplementary docs, (c) reject>

Tone: factual; no data invented. Where information is absent from the PQD
(project list, equipment list, financials), this is noted as a gap rather
than filled in.
================================================================================
```

Save the review to `/tmp/<supplier>_pqd_review.txt` so the user can copy it directly into a project folder, email reply, or assessment register.

**Tone rule** — same as the Samaya recommendation sheets: no AI fluff, no verbose prose. Bullet-granular facts, cited evidence, verdict at the end. The user explicitly rejects verbose framing; the verdict and the red-flag list are what the user reads.

**No-data-invented rule** — if a section (project list, equipment list, financials) is absent, say "absent" or "placeholder", do not invent content. This is a hard rule across all PQD reviews. A review that invents data to fill gaps is worse than one that flags them.

#### Pitfalls

- **Naming mismatch is a routing problem, not a content problem** — when the user asks for "PQD for Smith" but the file is for "AKI", flag the mismatch prominently at the top of the review. Do not silently substitute. The user may have a real reason for the routing, or it may be a clerical mistake — let them decide.
- **Placeholder sections are vendor PQD's most common gap** — almost every vendor PQD lists "Client Approvals" and "Project Reference" in the TOC. Verify with text extraction that the section actually has content. If the only text is a section header with no entries, it's a placeholder.
- **Scanned / image-only PQD sections cannot be assessed** — if a section (e.g. "Equipment Calibration Certificates", "Quality Manual") is image-only, note it as "embedded scans, not extractable as text". Do NOT OCR the whole PQD just to read an equipment list — ask the user to provide the section as a text source.
- **PQD covers a 232 m² lab but no equipment list** — capacity claim is unverifiable. Flag as a red flag, not a fact.
- **Don't accept "Nitaqat Platinum" as evidence of company size** — Nitaqat band is based on Saudization rate, not headcount. A 5-person company can be Platinum at 38% Saudization. Always pair Nitaqat band with explicit headcount.
- **Don't accept "ISO 9001:2015" without checking the cert body** — a PQD with an ISO 9001 cert from a non-IAF-member body is functionally equivalent to no cert. List the issuing body explicitly.
- **Don't accept pre-supplier experience as the supplier's experience** — if a QA/QC Manager lists 9 years of experience at "ZKB Builders" and "DESCON Engineering Limited", that experience is at those companies, not at AKI. AKI gets zero credit for it on the AKI track-record.
- **No "N/A" or "TBD" in your review** — if a section is absent, write "absent" or "not provided". If a fact is unknown, say "not stated in PQD". Don't use placeholders in the review itself.
- **Mark everything you can't verify** — if a PQD claims a project reference but you cannot verify it (e.g. no client name, no date, no scope), note it as "unverifiable claim" not as a project reference.

See `references/pqd-review-template.md` for a full worked example of an Aseer Museum PQD review (Al Kalas International, 288 pages, 6-section structure) with all pitfalls realised. Use as a reference for tone, structure, and red-flag catalog.

### Submittal Statement Drafting (AV Prequal Packages)

When writing the submittal statement for an AV equipment prequalification package, keep it **very short**. The user explicitly rejected verbose framing. Pattern:

> **Submittal Statement — [Supplier] [Equipment] Prequalification Package**
>
> This prequalification is for the **[equipment purpose]** to the Aseer Museum AV system, in compliance with the approved project specifications. Equipment types and technical specs ([key models]) match the approved DHD AV design.
>
> **Details:**
> - Supplier: [Name] ([role])
> - Contractor: Rawasin Media Production (AV contractor)
> - Proposed Ref: MOC-MUS-ASE-1K0-PQ-NNNN
>
> **Provided files:**
> [numbered list]

No explanation, no context paragraph, no quantity variance notes. Just the statement and the file list.

See `references/av-prequal-compliance-pattern.md` for the full workflow including design compliance check, quantity variance handling, and register update.
See `references/compliance-sheet-template.md` for the multi-sheet compliance workbook template — supplier product vs project requirements cross-reference (6 sheets, RAG status, gap analysis). Use this when a supplier submits products/documents and you need to assess compliance against the project's contract requirements (spec list, PQ register, design research, scope docs).

### Profile Content Structure (7 Pages)

| Page | Content | Image |
|------|---------|-------|
| 1 — Cover | Full-bleed navy, company name, stats, tagline | Hero factory photo (opacity 0.10-0.15) |
| 2 — About | Company overview, CR, GOSI, factory location, ISO certs | Factory building photo |
| 3 — Manufacturing | Production capacity, equipment, 5 zones | Factory floor photo |
| 4 — Products | 5 categories with icons, 4-step service flow | Product gallery (4 photos) |
| 5 — Portfolio | Project table by sector, key clients strip | — |
| 6 — Quality | ISO, SASO/SABER, SBC, Local Content cards, QC flow | QC lab photo |
| 7 — Why Us | 6 differentiator grid + contact CTA | — |

### DOCX Generation Pattern
```python
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
doc = Document()
# Set font, add headings, tables, save
```

See `references/technical-proposal-pages.md` for the full 24-page A4 portrait page inventory and design specs. See `references/outline-enterprise-prequal.md` for a complete worked example.

---

## Phase 4: Subcontractor Dossier (absorbed from subcontractor-dossier)

Populate a subcontractor's structured folder with all related files from across the project, search email archives, compile a status register, and update main project registers. For engineering/construction BIM project folders (Aseer Museum standard).

### When to Use

- User asks to "copy here and update registers" for a subcontractor
- User asks to "gather all docs" for a specific discipline/trade
- Any `13_XX_Contractor` directory that is empty or needs organising
- A new subcontractor folder needs populating with existing project documents

### Critical Rules

1. **NEVER regenerate existing SCOPE_REQUEST.md** — patch or append only
2. **Verify entity isolation** — Aseer-Museum files go to Aseer-Museum folders. Do NOT cross projects
3. **Deduplicate** — skip files already in target (same filename + size)
4. **Preserve source structure** — copy files, don't move them
5. **Report what was done** — always provide count of files copied, by subfolder, total size, and gaps

### Standard Subcontractor Folder Structure

```
01_Schedule_and_BOQ/       — pricing, BOQs, schedules
02_Reference_Drawings/     — reference CAD/PDF drawings, as-builts
  Existing_AsBuilt/        — pre-existing drawings
03_Specifications_and_Standards/ — specs, discipline files, standards
04_Reference_Imagery/      — photos, reference images
05_Returned_Submittals/    — submitted packages, CG/NRS comments
06_RFIs/                   — technical queries specific to this sub
07_Approvals/              — approved stamped drawings, permits
  Email_Extracts/          — relevant email threads
  Stamped_*                — stamped package sets
SCOPE_REQUEST.md           — scope definition (typically pre-exists)
<DISCIPLINE>_STATUS_REGISTER.md — comprehensive status (CREATED by this skill)
```

### Search Sources (in priority order)

| Source | Path pattern | What to look for |
|--------|-------------|------------------|
| Submittals | `Submittals/` | IFC packages, material submittals, NRS comments |
| Design Files | `Design Files/` | CAD drawings, design packages |
| As-Built Docs | `As-Built Docs/` | Existing as-built record drawings |
| Completed Tender Package | `Completed Tender Package From NRS/` | NRS-stamped drawings |
| Email Archive | `Email_Archive/`, `Scripts/output/email_bodies/` | Email chains with CG/subcontractor |
| Docs | `Docs/02_Plans/`, `Docs/07_Reports/` | Plans, studies, submittals |
| Contracts | `Contracts/` | Signed agreements |
| Invoices | `Invoices/` | Payment records |

**Key discovery:** Individual email .md files listed in PROJECT_EMAILS.md often don't exist on disk. Actual email body text is in `Scripts/output/email_bodies/` as `.txt` extracts. Always check both locations.

### Copy Strategy

| Source | Target |
|--------|--------|
| Design Files/*fire*/*sprinkler* etc | 02_Reference_Drawings/Existing_AsBuilt/ |
| Submittals/* | 05_Returned_Submittals/ |
| Docs/07_Reports/*STUDY* | 03_Specifications_and_Standards/ |
| Email body extracts | 07_Approvals/Email_Extracts/ |
| Stamped drawings | 07_Approvals/Stamped_* |
| RFI files | 06_RFIs/ |

### Create the STATUS_REGISTER.md

Sections:
1. **Deliverables Summary** — table of all scope items from SCOPE_REQUEST.md with RAG status
2. **File Inventory** — by subfolder, list files with descriptions and sizes
3. **Critical Open Issues** — RAG-rated table of blockers and open items
4. **Deliverables Progress** — per RIBA tree if applicable
5. **Key Emails** — date, subject, ref, key detail
6. **Email Thread Detail** — for critical submissions, full chain with exact CG wording
7. **Contractor Engagement Status** — MoC pre-approval, site work, contract signed, design deliverables %
8. **Knowledge Gaps & Next Steps** — actions with owners and timelines

### Create _CONTRACT_STATUS.md (one-page contract snapshot)

Place this file in the **subcontractor folder root** (NOT inside subfolders). It gives anyone browsing the folder an immediate answer to 'is this contracted?':

### Purchasing Info Pack from Designer Specs

When a designer (e.g. NRS) issues technical specifications for hardware items and Purchasing needs to source suppliers:

1. **Extract specs** — Identify the NRS spec documents (e.g. L20 Doors, P21 Ironmongery) and hardware schedules (e.g. A2742-1960/1961)
2. **Compile requirements** — List all hardware items, finishes (Grade 316 satin SS), standards (EN/SBC/UL/NFPA), quantities per door type
3. **Cross-reference brand datasheets** — ASSA ABLOY, Schlage, Halspan, Moralt, Hilti are reference brands, not specified
4. **Create purchasing folder** (`10_Purchasing/` under the subcontractor):
   - `01_NRS_Specs/` — original NRS spec PDFs
   - `02_Datasheets/` — manufacturer datasheets
   - `03_Drawings/` — door schedules, ironmongery schedules, type drawings
   - `README.md` — purchasing summary (or styled .docx per Samaya document style guide)
5. **Document what Purchasing needs to do** — contact 2-3 suppliers, get Grade 316 SS pricing, fire certs, lead times
6. **State clearly: no brand is mandated** — it's a performance spec. Contractor proposes, NRS approves.

See `references/purchasing-info-pack-doors.md` for a worked example (door hardware for Aseer Museum).

```
# Contract Status — [Trade] ([Contractor Name])

| Field | Value |
|---|---|
| **Contractor** | Full legal name |
| **Contract executed?** | ✅ YES / ❌ NOT YET / 🔴 ON HOLD |
| **Contacts** | Name (email), Name, Name |
| **Scope** | One-line scope summary |
| **Status** | Active / Pre-contract / On hold |
| **Next action** | Single concrete next step |
| **Last updated** | YYYY-MM-DD |
```

Create this file for every subcontractor folder that has a known status, even if the answer is "not yet made". The file replaces the need to dig into PROJECT_MEMORY or a dashboard to find the basic contract position.

### Subcontractor Folder Audit (Bulk)

Audit ALL existing subcontractors to ensure each has the standard structure, SOW, and SitRep. Run this when user asks "make sure all subs are properly set up" or after adding several new subs.

#### Workflow

1. **Define standard** — the 9 standard dirs + SCOPE_REQUEST.md + SITUATION_REPORT.md
2. **Walk all subs** — list every folder under `Subcontractors/` excluding `_ARCHIVE`, `_assets`
3. **Check each sub for:**
   - Presence of all 9 standard dirs
   - `SCOPE_REQUEST.md` exists
   - `_MANAGER_DASHBOARD/SITUATION_REPORT.md` exists
   - Any BOQ/schedule content in `01_Schedule_and_BOQ/`
   - File count (empty folders are suspicious)
4. **Identify numbering conflicts** — same `NN_` prefix used by two different subs
5. **Fix conflicts** — non-trade/material subs get `NNb_` suffix (e.g. `10b_Purchasing_Patinated_Brass`)
6. **Create missing items** — generate SCOPE_REQUEST.md from Subcontractor Prequal Register + SoW refs; create standard dirs; create SITUATION_REPORT.md

#### Cross-reference with Key Personnel Register

After fixing structures, audit the `Key_Personnel_Register.xlsx` against the subcontractor list:
- Every Tier 2 Design Specialist in the register should have a corresponding subcontractor folder
- Every subcontractor folder for a design specialist should have a row in the register
- Missing entries → insert rows (use openpyxl with `insert_rows` + style copy)
- Update summary sheet (total roles, tier counts, pending count)
- Bump revision number on Cover sheet

#### SCOPE_REQUEST.md generation pattern

When creating from the Subcontractor Prequal Register markdown:
```
From register:    B-06 Lighting → SoW §8.8 → Exhibition lighting design
To SCOPE_REQUEST: Identity block → 1. Purpose → 2. Scope (design/supply/install/commission) → 3. Reference docs
```

#### Pitfalls
- Duplicate numbers (`10_Oddy` + `10_Purchasing`) cause confusion — use `NNb_` suffix for material/purchasing subs, keep `NN_` for trade subs
- Some subs have extra dirs (e.g. `00_Scope_of_Work`, `08_Material_Submittals`, `10_Purchasing`, `RFP`) — these are fine, don't remove them
- Empty sub folders with no files but standard structure were created by `ensure_structure` — add at least SCOPE_REQUEST.md + SITUATION_REPORT.md to make them meaningful
- SCOPE_REQUEST.md for material suppliers (not design subs) is shorter — skip the design scope, focus on supply specs, delivery, certifications

### Create/Update _MANAGER_DASHBOARD/SITUATION_REPORT.md

Each subcontractor with significant activity gets an executive dashboard:

```
# [TRADE] EXECUTIVE SUMMARY (MANAGER'S VIEW)
**Status Date:** YYYY-MM-DD

## 1. PROJECT HEALTH CHECK
- Bullet points on design maturity, procurement, approvals, critical dependencies

## 2. CRITICAL ISSUES & ACTIONS REQUIRED
| Item | Description | Management Action |
|---|---|---|

## 3. TIMELINE SNAPSHOT
- Key dates in reverse chronological order

## 4. ENGAGEMENT STATUS TABLE
| Item | Status |
|---|---|
| Contract executed | ✅/❌ |
| Design deliverables | 🟡/🟢/🔴 |
| etc. |
```

### Update PROJECT_MEMORY.md §0 Status Section

Add or update a **§0 LATEST STATUS UPDATES** section at the top of PROJECT_MEMORY.md with a compact table of the current state of each key subcontractor/issue:

```
## 0. LATEST STATUS UPDATES (YYYY-MM-DD)

| Change | Detail |
|---|---|
| **Contractor A** | Contract ✅ EXECUTED. Contacts: ... |
| **Contractor B** | Contract ❌ NOT YET MADE. Under review. |
| **Contractor C** | Contract 🔴 ON HOLD — variation claim. New one being negotiated. |
```

This keeps the top of the file as a one-glance status board. Update it every time subcontractor status changes.

### Update Main Project Registers

After populating the subcontractor folder:
1. **PROJECT_MEMORY.md** — update subcontractor count, add to org chart, note IFC status
2. **RFI_REGISTER.md** — add any new RFIs found
3. **RIBA Deliverable Tree** — update RAG status for discipline items

For structured Excel registers (Key Personnel Register, Subcontractor Register, etc.), use openpyxl to insert rows, copy styles, and update summary counts. See `references/excel-register-update-pattern.md` for the full workflow.

### Key Pitfalls

- **Email .md files may not exist on disk** — PROJECT_EMAILS.md index lists paths that may never have been created. Actual content is in `Scripts/output/email_bodies/` as `.txt` extracts
- **CG comments contain hidden process gates** — always read the full CG comment chain, not just the Code letter. CG may require cross-discipline approvals (e.g. "FLS Consultant endorsement required before IFC review")
- **Contractor may be approved but not contracted** — verify Contracts/ folder. 0% design deliverables despite contractor being "active" is a common finding
- **Duplicates across source folders** — the same file appears in 3-4 locations. Pick one authoritative copy
- **Use `delegate_task` for parallelism** — search project folders, emails, and other sources simultaneously (up to 3 parallel sub-agents)
- **Cascade status updates everywhere** — when the user corrects a subcontractor's contract status (e.g. "actually it's EXECUTED not pre-qualified"), update ALL of: `_CONTRACT_STATUS.md`, `_MANAGER_DASHBOARD/SITUATION_REPORT.md`, `AV_STATUS_REGISTER.md` (or equivalent), `PROJECT_MEMORY.md §0`, `Scripts/notes/stakeholders.md`, and persistent memory. A single-source update leaves stale copies that confuse future sessions. Search for the old status string across the project to catch every occurrence.

See `references/fls-dossier-example.md` for a real-world Aseer FLS dossier run (88 files, 193MB) with source discovery order and pitfalls discovered.
See `references/av-subcontractor-dossier-pattern.md` for AV/IT subcontractor folder structure (NMK/Q-Sys), UUID duplicate detection, and product datasheet organization.

---

## Phase 5: RFI / Query Tracker Analysis

Analyze a subcontractor's or designer's RFI/query register to extract open items, identify patterns, and generate an action list for the next meeting.

### When to Use

- User shares a Query Tracker / RFI Register (Excel, DOCX, PDF)
- User asks "any new knowledge? any action needed?"
- Before a progress meeting where open RFIs need to be chased

### Workflow

**Step 1: Read the Register**
Extract all rows. Note: document date, total items, open vs closed counts, priority distribution.

**Step 2: Categorize Open Items**

| Category | What to flag |
|---|---|
| **No response entered** | Blank response column — weeks old, owner has not replied |
| **High priority & Open** | Immediate escalation needed |
| **Links to known blockers** | RFI references a known SI, NCR, or variation claim |
| **Ties to un-contracted scope** | RFI about ZNA lightbox but ZNA not yet contracted |

**Step 3: Generate Action Table**

Present as a prioritised table with concrete next steps:

| Priority | RFI # | Issue | Action | Owner |
|---|---|---|---|---|

**Step 4: Cross-Reference Against Project State**

- If a subcontractor is not yet contracted, flag any RFI referencing that scope
- If a contractor is on hold, flag any RFI blocked by that dependency
- If a new personnel fact was discovered, note it

### Output Format

The analysis must end with a prioritised action list answering "so what do I do now?" — not just a summary matrix.

### Cross-Reference RFIs Against Current Contract Status

A critical adjacent step: check whether any open RFI references scope from a subcontractor whose contract status is unresolved:

| If an RFI mentions... | But... | Then flag it as |
|---|---|---|
| ZNA lightbox detail (RFI #47) | ZNA contract NOT YET MADE | Blocked — unresolved scope ownership |
| AV room location (RFI #19) | AV/IT contract just executed, designer not onboarded | Dependency — pending designer mobilisation |
| MEP ductwork/sizing (RFIs #1,2,7) | MEP designer ON HOLD (variation claim) | Blocked — dependent on new contract |

This cross-reference turns a simple RFI list into a **project health diagnosis** — it links open technical queries to the commercial/procurement blockers that prevent them from being answered.

### File Register Index Analysis

When a project's file index CSV or register is shared (e.g., to demonstrate delivery volume):

**Step 1: Read the header and sample**
```python
import csv
with open(path) as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i < 5: print(row)
```

**Step 2: Compute summary stats**

| Metric | Method |
|---|---|
| Total files | Count rows |
| By category | `collections.Counter(row['Category'] for row in reader)` |
| By extension | Same pattern on `Extension` column |
| Date range | Collect `Modified` column, sort |
| Files with issues | Filter `Issues` column non-empty |

**Step 3: Answer the question behind the data**

A file register is usually shared to prove one of:
- *"We've delivered substantial work"* → cite PDF + DWG count (the reviewable deliverables)
- *"There are quality issues"* → cite the Issues column (spelling errors, duplicates)
- *"The package is stale"* → compare Latest date against current date

**Example output (NRS File Register Index):**
```
19,166 files, 1,707 PDFs + 1,081 DWGs delivered. 40 files with quality issues
(Asser→Aseer misspelling, duplicate files). Latest file: 2026-06-06.
```
