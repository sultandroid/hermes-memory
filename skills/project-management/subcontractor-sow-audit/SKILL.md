---
name: subcontractor-sow-audit
description: Audit subcontractor SOWs against Project SOW, ER, Appendix A/B, and Compliance Matrix. Build 3-layer system (SOW, submission plan, tracker).
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [sow, compliance, audit, subcontractor, aseer]
    related_skills: [compliance-system, subcontractor-procurement, specialist-register]
---

# Subcontractor SOW Compliance Audit

## When to Use

- User asks to audit all subcontractor SOWs against project requirements
- User asks "are all SOWs compliant with the contract?"
- User asks to check what's missing per package
- User asks to build a complete SOW/submission plan/tracker system

## Classification Rule (CRITICAL)

Before auditing, classify each package by TYPE. This determines whether a SOW is needed:

| Type | SOW Needed | Examples |
|------|:----------:|----------|
| **Specialist/contractor** (design, install, consultancy) | ✅ Required | AD Eng, ZNA, Rawasin, GBH, Structural, Acoustic, Fit-Out, MEP Contractor |
| **Supply-only** (materials, equipment) | ⚪ Not needed | Panasonic (AV equipment), FF&E (furniture), Material Testing Lab |
| **Authority service** | 🟡 Minimal scope note | Namaa (licence), Oddy Lab, SEC NOC |
| **Internal** (Samaya staff) | ⚪ Not needed | Project Director, BIM Manager, HSSE Manager |

Do NOT mark supply-only packages as "SOW missing" in the register. Mark them ⚪.

## The 5 Governing Sources

| Source | Abbrev | File | What it covers |
|--------|--------|------|----------------|
| Project SOW | PS | `6380_KMS_RPT_PM_AS_00006` | Package scope, deliverables, exclusions |
| Employer's Requirements | ER | `00_Project_Charter/er_document.md` | Performance criteria, codes, systems |
| Appendix A Interface Matrix | ApxA | `05_Scope/project_sow_appendix_a_b_extraction.md` (may not be filed — check `05_Scope/`) | RACI split between Fit Out and MoC |
| Appendix B Package Map | ApxB | Same file as ApxA | Package recognition and hierarchy |
| Compliance Matrix | CM | `Technical_Office/Compliance_System/compliance_matrix.md` | Spec→supplier→PQ compliance status |

## The 3-Layer System

Every specialist package gets 3 folders in the repo:

| Layer | Path | Content |
|-------|------|---------|
| SOW | `05_Scope/<name>/README.md` | Scope summary, filed SOW docs, exclusions, compliance gaps |
| Submission Plan | `02_Schedule/<name>/README.md` | Planned submissions with dates, review durations, status |
| Submission Tracker | `Technical_Office/Submission_Tracker/<name>/README.md` | Live log of actual submissions and CG responses |

### Status conventions
- ✅ SOW filed in repo (actual documents present)
- 🟢 SOW approved (exists on OneDrive, not yet filed in repo)
- 🟡 Draft RACI only (no formal package SOW)
- ❌ Missing

## Audit Procedure

### Step 1: Read the governing sources
```bash
# Project SOW summary
read_file 05_Scope/sow_summary.md

# ER summary
read_file 05_Scope/er_summary.md

# Appendix A/B extraction (if present; not always filed)
read_file 05_Scope/project_sow_appendix_a_b_extraction.md 2>/dev/null || echo "appendix extraction not filed"

# Compliance Matrix
read_file Technical_Office/Compliance_System/compliance_matrix.md

# SOW/RACI register (existing SOW status per package)
read_file 01_Registers/subcontractor_sow_raci_register.md

# Package register (OneDrive folder map)
read_file 01_Registers/subcontractor_package_register.md

# SOW control system (issue gates)
read_file 03_Plans/15_Subcontractor_Deliverables/subcontractor_sow_control_system.md

# Conflict matrix (open interface issues)
read_file 03_Plans/15_Subcontractor_Deliverables/SOW_RACI_Conflict_Matrix.md
```

### Step 2: For each package, check against each source
1. Read the package's SOW (from `05_Scope/<name>/` or OneDrive `24_Subcontractors/<name>/`)
2. Read the governing source requirement
3. Mark: ✅ Compliant · 🟡 Partial · ❌ Non-compliant · ⚪ Not assessed
4. Document specific gaps with source reference

### Step 3: Create/update the 3-layer folders
- `mkdir -p 05_Scope/<name>/` — write README.md with scope summary, filed docs, gaps
- `mkdir -p 02_Schedule/<name>/` — write README.md with planned submissions
- `mkdir -p Technical_Office/Submission_Tracker/<name>/` — write README.md with live log

### Step 4: Update the registers
- `specialist_register.md` — add SOW/Plan columns with folder paths
- `subcontractor_sow_raci_register.md` — update status to "filed in repo"
- `subcontractor_package_register.md` — update with repo file paths

### Step 5: Write the audit report
Save to `Technical_Office/Submission_Tracker/SOW_Compliance_Audit.md`. Structure:
- Per-package section with source-by-source table
- Open interface conflicts (from SOW/RACI Conflict Matrix)
- Compliance gaps affecting specialists
- Roll-up counts
- Priority actions table

## Common Gaps Found in Practice

| Source Ref | Requirement | Often Missing From |
|------------|-------------|-------------------|
| ApxA 4.02 | Lighting spares 1 year (Fit Out R) | ZNA SOW |
| ApxA 2.13 | Media/AV software by MoC (excluded) | Rawasin SOW |
| ApxA 4.01 | AV hardware spares 1 year (Fit Out R) | Rawasin SOW |
| ApxA 2.12, 3.01-3.05 | Content/copyright/translation by MoC | Graphics SOW |
| ER §2.4.D | Oddy testing for all materials | Oddy Lab not appointed |
| ER §3.0 | MEP installation | MEP Contractor not awarded |
| PS §3 | Interactives, setworks, joinery | No specialists appointed |

## Open Interface Conflicts (from SOW/RACI Conflict Matrix)

| ID | Issue | Affected Packages |
|----|-------|-------------------|
| SRC-001 | Fit-Out umbrella vs specialist responsibility | Exhibition Fit-Out + 6 packages |
| SRC-002 | FF&E vs joinery boundary | FF&E, Fit-Out |
| SRC-003 | Rigging vs structural certification | Rigging, Structural |
| SRC-004 | Object mount integration | Showcases, Rigging, Structural |
| SRC-005 | Stramp/terrace boundary | Structural, Landscaping |
| SRC-006 | Authority submission lead | FLS, Structural, Landscaping, MEP |

## Filing SOW Documents from OneDrive

When a SOW exists on OneDrive but not in the repo:

### Step 1: Search all possible locations in priority order

The `24_Subcontractors/` folder is the canonical map, but SOW documents are often in legacy paths. Search in this order:

```bash
# 1. Canonical folder (most recent)
find "/Volumes/MIcro/Work/Aseer-Museum/24_Subcontractors/<name>/" -type f -not -name "._*" | head -20

# 2. Legacy source bank (most reliable for older documents)
find "/Volumes/MIcro/Work/Aseer-Museum/90_Legacy_Source_Bank/07_Subcontractors/" -type f -not -name "._*" \( -iname "*sow*" -o -iname "*scope*" -o -iname "*contract*" -o -iname "*agreement*" -o -iname "*status*" -o -iname "*register*" \) 2>/dev/null | head -20

# 3. Procurement folders (status registers, email DBs)
find "/Volumes/MIcro/Work/Aseer-Museum/90_Legacy_Source_Bank/06_Procurement/General/" -type f -not -name "._*" \( -iname "*sow*" -o -iname "*scope*" -o -iname "*status*" -o -iname "*register*" \) 2>/dev/null | head -20

# 4. Archive scope management
find "/Volumes/MIcro/Work/Aseer-Museum/99_Archive/02_Scope_Management/" -type f -not -name "._*" 2>/dev/null | head -20

# 5. Root-level files in 24_Subcontractors/ (some SOWs are loose PDFs)
find "/Volumes/MIcro/Work/Aseer-Museum/24_Subcontractors" -maxdepth 1 -type f -not -name "._*" 2>/dev/null | head -20

# 6. Broad search by firm name
find "/Volumes/MIcro/Work/Aseer-Museum" -type f -not -name "._*" -iname "*<firm>*" 2>/dev/null | head -20
```

### Step 2: When no formal SOW PDF exists, file evidence documents

If no formal SOW PDF is found, search for these partial-evidence documents and file them as the best available SOW reference:

| Document Type | What It Provides | Example |
|---------------|-----------------|---------|
| Scope request / engagement letter | Formal scope definition | `SCOPE_REQUEST_NAMA.md` |
| Status register | Deliverable list + progress | `FLS_STATUS_REGISTER.md` |
| Email database | Correspondence trail | `Structural_Email_Database.md` |
| Prequalification submittal | Company capability + scope statement | `Rawasin_PQ-0027_Prequalification.pdf` |
| BOQ / schedule | Technical scope detail | `Rawasin_Technology_BOQ.xlsx` |
| Contract / agreement | Legal scope + exclusions | `ZNA_Consultancy_Agreement_FINAL.pdf` |

### Step 3: Copy to repo

```bash
cp "/Volumes/MIcro/Work/Aseer-Museum/<source_path>" "05_Scope/<name>/<file>"
```

### Step 4: Update registers

1. `05_Scope/<name>/README.md` — add filed docs table with compliance gaps
2. `specialist_register.md` — change SOW status to ✅, add gap notes
3. `subcontractor_sow_raci_register.md` — change status to "filed in repo"
4. `SOW_Compliance_Audit.md` — update the audit

## Pitfalls

- **User wants ALL output in English only** — no Arabic text in responses. Translate Arabic subject lines, sender names, and document titles to English when displaying.
- **SOW exists on OneDrive but not in repo** — the SOW register may say "package SOW exists" meaning it's on OneDrive. Check `24_Subcontractors/<name>/` before marking as missing.
- **Supply-only packages don't need SOWs** — Panasonic (AV equipment), FF&E (furniture), Material Testing Lab are supply-only. Mark them ⚪, not ❌.
- **Appendix A exclusions are often not documented in package SOWs** — MoC responsibilities (text, media, copyright, mounts) must be explicitly excluded in each package SOW.
- **Spares obligations** — ApxA 4.01-4.03 assign 1-year spares to Fit Out for AV, lighting, and interactives. These are often missing from package SOWs.
- **Interface conflicts block SOW finalisation** — 6 open conflicts (SRC-001 through SRC-006) need PM decisions before affected SOWs can move from draft to approved.
- **Compliance gaps are not the same as SOW gaps** — a package can have a compliant SOW but still have an open compliance gap (e.g. AD Engineering SOW is compliant, but GAP-MEP-001 for MEP installer remains).
- **The 3-layer system is empty by default** — creating the folders and READMEs is the first pass. Populating them with actual content (filed SOW PDFs, real submission dates, CG response logs) is the ongoing work.
- **ICT/CITC Telecom Engineer SOW is a scope request, not an award** — `MOC-MUS-ASE-SAM-SOW-SC-014_R00` (issued 2026-06-07) covers telecom/data/fibre design + STC FTTH compliance + approvals, but the ICT Designer & Supplier is still TBD (🔴, action Mohammed Hakami + Hani Alghamdi). The `24_Subcontractors/06_ICT/` folder holds only prequal equipment datasheets (MediaCast, Netgear switches) — no supplier appointed. Don't mark it "SOW missing"; it's a draft scope request awaiting supplier identification. Full detail in `references/ict-citc-telecom-sow.md`.
- **SOW docx files are readable via python-docx** — formal SOWs are often `.docx` (e.g. the CITC SOW). Use `python3 -c "from docx import Document; ..."` to dump paragraphs + tables rather than assuming PDF.
- **A "Draft" internal SOW is not contractually locked** — the Landscaping (TLC) case showed a Draft RACI SOW (`21_Landscaping_Specialist_SOW_RACI_Draft.md`, header "Do not issue until... complete") was bundled into a contract sent for signature while still unapproved. A draft SOW does not become the binding scope just because it's attached to a contract bundle. Verify the SOW is signed by both parties or explicitly an exhibit before treating scope as fixed.
- **Cross-check contract scope vs quoted/exhibit SOW line-by-line** — the TLC dispute arose because the contract listed "Revit model updates" as in-scope while TLC's own quoted SOW excluded it; the PM had "accepted TLC's SOW" (excludes) yet sent a contract that includes. Any deliverable appearing in one but not the other is a signature-blocking conflict. Resolve every disputed item (model updates, BOQ, review cycles, exclusions) explicitly IN or OUT, never implied. Full case: `references/tlc-landscape-sow-dispute.md`.
- **Interactives are NOT screens/AV, and there are 6, not 1** — The Interactive SOW (`MOC-MUS-ASE-1KH-SOW-INT-001`) was drafted for ET_09.03 only, but the official `6930_Aseer_Tactile & Manual Interactives Schedule` lists **6 interactives** project-wide. Only `09.03_HI_01` (G9 Sensory) is a true electronic/hybrid interactive (sensors, scent, DALI/DMX, show-control) that belongs under Rawasin's AV/Interactive umbrella; the other five (building blocks, mural blocks, tactile replicas, rubbing) are **physical/manual/tactile** and belong under Replicas/Models + Setworks, NOT Rawasin. Classify via the Exhibit Schedule's separate columns (Media ID = screen/AV vs Tactile/Manual ID) — an exhibit with no Media ID has no screen. When submitting the SOW to CG, strip the RFP/pre-qualification framing (Rawasin is an executed sister co, not a tender) and add a SCOPE BOUNDARY note clarifying the specialist integrates onto (does not fabricate) the physical exhibits. **User directive (2026-08-23): the SOW MUST be comprehensive across all 6 interactives, not left as G9-only** — and the interactive specialist does NOT fabricate models/glass/joinery/metalwork (all by others). Full classification: `references/aseer-interactives-scope-classification.md`; full python-docx editing technique + NRS RFI evidence chain for the museum-wide rewrite: `references/aseer-interactives-scope-editing.md`.
- **CG double-gate on specialists** — after kick-off, CG independently demands the specialist's own **SOW + Understanding Report + Contact Data**. A signed contract does not satisfy this; the specialist must produce its own scope/understanding deliverables. Missing these blocks design progress regardless of contract status.

## Closing a Disputed Specialist SOW (reusable pattern)

When a specialist dispute blocks signing (TLC case: Revit listed in the contract, excluded in the quoted SOW), do NOT just re-issue the draft. Build a **clean, signable SOW** that forces every disputed deliverable into an explicit binary decision. The dispute survived because items were "implied" — fix by making them choices the PM can tick.

**Technique — explicit IN/OUT resolution clause per disputed item:**
1. List each disputed deliverable (Revit/BIM model, BOQ, review cycles, exclusions, interior planters) as its own clause.
2. For each give exactly two options `[IN SCOPE]` / `[OUT OF SCOPE]` plus the concrete consequence of each (e.g. IN → native Revit updates at Concept/90%/IFC; OUT → PDF/CAD only, Revit coordination by others).
3. Add a bold NOTE: "Select and strike one. An unsigned/blank field is NOT agreed." A blank SOW with the field open must not be treated as agreed.
4. Payment: link to defined milestones (see the CLIENT-PROTECTIVE section below before choosing SUBMISSION vs APPROVAL — the preference here is APPROVAL-gated, protecting the client).
5. End with a signature/acceptance table for both parties.

This collapses an open "confusion" (Waris's word) into a single tick-box the PM can decide. Generator: `scripts/gen_landscape_sow.py` in `aseer-museum-pm` (uses the SamayaDoc template — import it from the repo copy `/Users/mohamedessa/aseer-museum-pm/_Style-Guides/Doc Style Guide/`, NOT the OneDrive path which can deadlock).

**Make specialist SOWs GENERIC / supplier-agnostic.** Do NOT write a SOW tied to a single firm (e.g. "for TLC"). Frame it as "the Landscape Specialist selected through the procurement process". This lets one SOW serve any candidate and prevents a draft from becoming firm-specific leverage. User correction 2026-08-21: "Dont make the sow for TLC exactly make it generally for any supplier."

**Embed CG/comments as REQUIREMENTS, not as a firm's exclusions.** CG's landscape submission package requirements (landscape general layout; planting plans & schedule; irrigation drawings + hydraulic calcs; hardscape coordination; drainage/waterproofing; tech specs & material submittals; multi-discipline coordination; + specialist's own SOW/Understanding Report/Contact Data) belong in the SOW as a mandatory "Consultant (CG) Requirements — applicable to ANY supplier" section. This simultaneously satisfies the CG double-gate and keeps the doc reusable.

**NEVER put internal repo references in a client-facing SOW.** User correction 2026-08-21: "Dont mention or refere to any internal refrences like any md file." A formal SOW delivered to a supplier must NOT cite repo paths (`02_Schedule/...md`, `Technical_Office/Submission_Tracker/...`), GitHub repo names, or internal register files. Keep only contract-facing references: document numbers (e.g. 6380_KMS_RPT_PM_AS_00006), CG codes (CG-01..), deliverable refs (L-D-L-001). If you want to note the tracking mechanism, say generically "each submission is tracked with its actual date and CG response code (A/B/C/D)" — no path. Also drop any `.md` mention from tables and notes. The generator script's own `OUT=` path is fine (it's code, not content).

**Trust the actual source document, not the repo README summary.** The repo `README.md` for a package is a condensed summary and can be WRONG or STALE vs the real bid/contract. In the TLC case the summary said "SAR 175,000 / 3 stages" but the ACTUAL `Revised_TLC_Landscape_Proposal.docx` (Samaya-authored 08-Aug-2026) and the real TLC Rev.2 offer PDF (email 50632) showed **SAR 120,000 / 20 working days / 10-30-30-30 upon APPROVAL / 4 stages (90% IFC = Shop Drawing Package) / Revit excluded in exchange for the price cut**. Before generating a SOW, READ the source .docx/.pdf directly (python-docx for .docx; for scanned/image PDFs use pdftoppm + tesseract or vision). The summary also dropped exclusions present in the real offer (O&M manuals, material procurement/testing/mock-ups, shop-drawing prep beyond 90% IFC).
- Some of these dropped exclusions CONFLICT with CG/mandatory requirements (e.g. CG's Handover batch needs O&M manuals, but the bid excludes them). Flag those as additional express-agreement decision items, not silent exclusions.

**Complete dispute-proof document architecture (the real goal).** User correction 2026-08-21: *"the goal is to reach a complete document that lacks nothing and causes no future disputes"* — NOT a document that matches one supplier's bid. Beyond the IN/OUT clauses above, build the sections that preempt whole classes of claim: (1) **Physical scope & boundaries** (which areas/zones — prevents boundary disputes, e.g. Stramp/Al-Bahar/terrace/hard-soft interface); (2) **Client-supplied data responsibilities** (who provides survey/cloud/geotech — prevents "no data" delay claims); (3) **Interface & coordination matrix** (lighting/structural/irrigation/MEP + who owns each — the biggest claim source); (4) **Change & variation mechanism** (any change must be agreed in writing before work, else no payment — kills scope-creep); (5) **Compliance & sustainability** (codes, climate-suitable planting, evidence); (6) **IP & handover** (outputs become Samaya's on final payment + project-only licence). Combined with payment, duration, review-cycle cap, and signature, this yields a 16–18-section SOW. Section inventory for a worked landscape example: `references/generic-landscape-sow-workflow.md`.\n\n**Do NOT blindly copy a bidder's quoted exclusions into the client's SOW.** 3D renders / Revit / BOQ appear as exclusions in the *supplier's* offer — that is the bidder shedding scope, not a client decision. Instead, surface them as explicit IN/OUT decision clauses so the PM owns the choice rather than inheriting the bidder's cost-shaving. The 3D-renders row in the landscape SOW was flagged as a mistake because it had been copied verbatim from TLC's proposal; it became a "Deliverables Requiring Express Agreement" row instead. Full section-by-section template: `references/generic-landscape-sow-workflow.md`.

**CLIENT-PROTECTIVE SOW (user's core requirement — 2026-08-21).** The user IS the client/employer (Samaya). He made explicit: *"أنا عايز أحمي نفسي مش المقاول"* ("I want to protect MYSELF, not the contractor"). So the SOW is a contract of obligation ON the contractor, NOT a "fair"/both-parties document. Write every disputed term to favour Samaya and close the contractor's escape hatches. This OVERRIDES the earlier neutral "explicit IN/OUT choice" framing — do NOT hand the bidder a menu of exclusions to tick. Specific client-protective defaults, all confirmed this session:

- **Disputed deliverables LOCKED IN, not optional.** Put Revit/BIM, 3D renders, BOQ, and O&M manuals in a table marked **INCLUDED in the fixed fee**, with: "the Specialist has no unilateral right to exclude any of these; if it contends an item is not covered by its quoted fee it must state so in writing BEFORE signing; failure to do so gives rise to no additional payment." (Do NOT let the bidder choose IN/OUT.)
- **Unlimited review cycles within the fee.** With a CG that rejects often (Code C/D), capping reviews at two lets the contractor bill every resubmission. State: "the fixed fee covers an UNLIMITED number of review cycles/resubmissions until CG and Samaya approval; no additional payment."
- **Full IP ASSIGNMENT, not a licence.** Give Samaya irrevocable full ownership of all deliverables (incl. copyright) + warranty of originality + **indemnity** against infringement + delivery in editable native formats. NOT a "non-exclusive licence" (that lets the contractor resell the design).
- **Best-available-data obligation on the contractor.** Require it to *"proceed with the best available data and record assumptions in writing; it shall not suspend work pending data; a delay claim is valid only after written notice naming the specific datum + a reasonable remedy time."* This defeats "no data" stall tactics.
- **Physical boundaries by the ANNEXED drawings, never an assumed list.** Do NOT list scope areas from memory (Stramp/Al-Bahar/terrace...). Reference *"the issued architectural drawings and scoping plan in Annex 1, which take precedence over any description"* and attach an Annex 1 drawing register. Prevents boundary disputes (SRC-005-style).
- **Variation mechanism.** Any change must be agreed in writing before work begins; work without a written instruction gives no additional payment. Kills scope-creep.
- **No internal references in the client-facing SOW** (repo `.md` paths, tracker paths, GitHub names) — keep only contract-facing refs (doc numbers, CG codes, deliverable refs).

Reference workflow with full section-by-section of the client-protective 17-section landscape SOW: `references/generic-landscape-sow-workflow.md`.

**SOW DOCX generation pitfalls (SamayaDoc template):**
- `add_table` param is `col_widths_cm=`, NOT `widths_cm=` (typo throws `unexpected keyword`).
- `add_body(..., align=...)` takes `docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER`, not the string `"center"` (ValueError).
- The repo `.gitignore` blocks committing `.docx` (no-binaries rule). Commit the generator script; store the SOW on the tracked folder path; reference it in README, don't git-add the docx.

**Set milestone dates from TODAY'S tracker, not a baseline plan.** User correction 2026-08-21: review the current project tracker to know the timing — the project is already late and not all design months remain. Do NOT copy D-55/D-85/IFC dates from a stale submission-plan .md into a live contract. Past milestone dates make the liquidated-damages clause unenforceable and the contract unexecutable. Pull today's actual position from 00_Status/project_status.md and master_programme.md (contract effective 01-Dec-2025, handover 30-Sep-2026, 303 days, already deep in elapsed time) before fixing any Target/Acceptance date.

**Client-protective terms can be commercially un-bankable — flag the trade-off, don't silently pick.** The strongest client-protective default (UNLIMITED review cycles + payment on APPROVAL) plus locking a deliverable INTO the fee that the bidder explicitly EXCLUDED (Revit) is contractually strong but commercially suicidal: a rational bidder either refuses or inflates the price. The TLC case is exactly this — TLC's Rev.2 offer (120,000 SAR) excluded Revit; locking it into that fee means they will not sign, repeating the very dispute the SOW was meant to close. When this appears, STOP and give the user the three options rather than silently choosing one: (A) deliverable OUT of fee — matches the bidder, they'll sign; (B) deliverable as an OPTION at a pre-agreed rate — protects client, keeps deal alive; (C) deliverable INCLUDED — client-strongest, bidder likely refuses. Also fix the LD rate and any retention BEFORE signature — "rate to be stated later" is a hole a procurement/PM review will reject.

## Email-Scan-to-Conflict-Detection Workflow

When the user asks to "find any conflicts" after a batch email scan, follow the workflow in `references/cross-specialist-conflict-detection.md`:
1. **Phase 1-2** — SQLite query for specialist/subcontractor emails (2-month window) + extract CG codes from preview
3. **Phase 3** — Download attachments. AppleScript `save` returns -2700; the reliable route is reading the raw `.olk15MsgAttachment` blob under `Message Attachments/` and base64-decoding the PDF out of it (filenames are in the blob's first ~2 KB of MIME headers; scope the search by mtime window, not full-tree grep). Scanned offers need vision (pdftotext returns 0 bytes). Full recipe: `references/outlook-attachment-extraction.md`.
3. **Phase 4** — Read documents (pdftotext/textutil/openpyxl, delegate parallel sub-agents)
4. **Phase 5** — Cross-reference against specialist_register.md, prequalification_register.md, subcontractor_package_register.md
5. **Phase 6** — Detect 5 conflict types: scope overlap, all-suppliers-rejected, contradictory CG, material non-compliance, unclear scope boundary
6. **Phase 7** — Report: CG summary table → 🔴 Conflicts → 🟡 Risks → ✅ Actions

**Key conflict patterns to watch for:**
- **BMS scope** — 4 claimants (GITCO, SPS, Rawasin, JADCO) — no single strategy
- **Setwork suppliers** — all 3 rejected same day (BTT, Saudi Emaar, Tannah) — no approved supplier
- **Material compliance** — GUBI porcelain failed 3 spec requirements (R9 vs R10, PEI 3 vs PEI 4, chemical resistance)
- **AV Design** — rejected even though Rawasin has an executed contract — design rework needed, not contract
- **Subcontract Management Plan** — rejected (D) — no approved governance framework for managing subs

## Verification

After completing an audit:
1. Verify all 3 folders exist for each package: `ls -d 03/Scope/*/`, `ls -d 02/Schedule/*/`, `ls -d Technical_Office/Submission_Tracker/*/`
2. Verify `specialist_register.md` has SOW/Plan columns with correct paths
3. Verify `SOW_Compliance_Audit.md` roll-up counts match the actual data
4. Run `git status` to confirm all new files are tracked
