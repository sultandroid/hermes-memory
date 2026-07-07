# Subcontractor Scope Compliance Audit

## When to use
A subcontractor (designer or supply/install) submits a scope proposal. You need to check it against the **formal project documents** before internal sign-off or client submission.

## Source documents to collect

| Document | Location pattern | Purpose |
|----------|-----------------|---------|
| **ER** — Employer's Requirements | `03_Specifications_and_Standards/*ER*.pdf` or `Package_Part 2/05_...` | Defines what the Employer mandates (service life, standards, performance) |
| **SOW** — Scope of Work | `*Scope of Work*.pdf` or `Package_Part 2/` | Defines what the Contractor commits to deliver, per RIBA stage |
| **DMP** — Design Management Plan | `02.1_DMP/*PL-0029*` | RACI matrix, deliverable pipelines, interface register, stage gates |
| **NRS Methodology (ZD-0026)** | `02.6_NRS_Methodology/*ZD-0026*` | NRS design-intent review SLA, approval workflows (NOTE: source content often not on disk — only CG cover sheet. Check Aconex.) |
| **SCOPE_REQUEST** (if Samaya issued one) | `Subcontractors/<Trade>/SCOPE_REQUEST.docx` | Samaya's own RFQ — the baseline the sub is responding to |
| **Subcontractor proposal** | `Subcontractors/<Trade>/00_Scope_of_Work/` or `Design Files/00_Scope_and_Proposals/` | What's being evaluated |
| **Responsibility Matrix** (if exists) | `00_Scope_of_Work/*SCOPE_SPLIT*` | Demarcation between design sub and supply/install sub |

## Extraction method

1. **PDF text extraction** — `pdftotext <pdf> <output.txt>`. Each doc can be 3K–15K lines.
2. **Keyword grep** — search for "lighting", "exhibition lighting", "lighting design", "luminaire", "control", "DALI", "emergency", "BIM", "conservation", etc. (adapt keywords per trade).
3. **Read markdown summaries** — check `Scripts/notes/` or `Scripts/output/ms_file_previews/` for already-extracted summaries before re-extracting full PDFs.
4. **Check existing analysis files** — search for `*_Summary.md`, `*_Analysis.md`, `*_Audit.md` under the project.

## ⚠️ Scope boundary check (CRITICAL — do before labelling anything a "gap")

**Only label something a gap if it is actually the subcontractor's contractual responsibility.** External dependencies are NOT sub gaps.

| Item often mis-attributed | Actual owner | Common mistake |
|---------------------------|-------------|----------------|
| BIM / Revit authoring | **Radiance Group** (Samaya scope) | Wrongly listed as lighting designer gap |
| BMS / DALI control engineering & programming | **MEP designer** or specialist controls vendor | Wrongly listed as lighting designer gap |
| Supply, manufacture, installation, commissioning | **ERCO / iGuzzini** (S&I subcontractor, not designer) | Wrongly listed as designer gap |
| Emergency lighting hardware compliance | S&I contractor (designer provides design/calc only) | Confusing design vs install responsibility |
| Power feeds, containment, SLD | MEP designer (Bluehaus / AD Engineering) | Confusing lighting design with electrical infrastructure |
| MEP design (consultancy) | **18_MEP_Designer** (consultant, e.g. Bluehaus/AD Eng) | Confused with MEP installation contractor |
| MEP installation (S&I) | **12_MEP_Installation** (construction contractor, RFQ 10-May-2026) | Confused with MEP design consultant |

**Key principle: MEP has TWO subcontractors** just like lighting:
- **Design consultant** (folder 18_MEP_Designer) — produces design, calculations, specifications, BOQ
- **Installation contractor** (folder 12_MEP_Installation) — supplies, installs, commissions, warrants

Same applies to lighting: **StudioZNA** (design, folder 04/01_Designer) + **ERCO/iGuzzini** (S&I, folder 04/02_Supply_and_Install). Never conflate the two.

### Aseer Museum scope chain (design consultant → specialist subs)

Three-tier chain, NOT flat. When NRS says something is outside their scope, check T2 allocation before labelling it a procurement gap:

```
MOC (client)
  └── PMC (ACE-MB)
        └── CG (Consultancy Group)
              └── Samaya (Main Contractor)
                    ├── NRS (Design Consultant, A2742) — exhibition design only
                    ├── Rawasin (AV/IT/Interactives) ← T2-09, sister co, EXECUTED
                    ├── Glasbau Hahn (showcases)
                    └── [other T2 specialists]
```

**Trace responsibility:** (1) Who claimed "not my scope"? NRS = design consultant only. (2) Check T2 allocation table. (3) Check distribution list CCs for routing clues (Shihab = Rawasin = AV/interactives). (4) Only call it a procurement gap if no T2 party exists AND no CC clue.

| Claim from NRS | Actual owner | T2 |
|---|---|---|
| Interactive design (G9) | Rawasin | T2-09 |
| AV design | AVD (MoC-appointed) | T2-10 |
| Exhibition lighting | ZNA | T2-06 |
| Showcases | Glasbau Hahn | T2-07 |
| Acoustic design | iAcoustics / Acoustic Specialist | SC-0019 |
| Graphics production | Graphics subconsultant | T2-17 |
| Setworks/joinery | NRS themselves | T2-08 |

**Rule:** If the sub's scope document explicitly excludes something AND another party is assigned in the Responsibility Matrix, it is NOT a gap — it is a documented handoff. Track it as a dependency/risk, not a gap.

## Compliance checklist (per trade)

For each requirement in the ER/SOW/DMP, assess:

| Score | Meaning |
|-------|---------|
| ✅ Covered | Explicitly addressed in proposal scope |
| ⚠️ Gap — minor | Mentioned but missing detail, standard reference, or deliverable format |
| ❌ Gap — critical | Missing entirely, and no other party assigned |
| ⬛ Out of scope (documented) | Excluded AND handed off to another party per matrix — NOT a gap |
| ❓ Cannot verify | Source doc not on disk (e.g., ZD-0026 content missing) |

### Common gap categories to flag (sub's actual responsibility only)

1. **Standards not cited** — ER specifies specific BS/EN/IEC/NFPA codes. Check each against sub's scope.
2. **Service life compliance** — ER has a service-life table (Light Fixtures 20yr, Emergency Lighting 25yr, etc.). Sub often doesn't address this.
3. **Conservation lux/UV caps** — Museum projects require specific CIE 157:2004 lux ceilings per object sensitivity class. Verify sub addresses this.
4. **Interface Register** — DMP usually has an appendix (e.g., AV/Lighting/Setworks Interface Register). Check if sub acknowledges it.
5. **Review SLA** — Sub should commit to a response turnaround for design-intent reviews (e.g., 5 working days).

## Output format

Produce a **3-section report** followed by a **prioritised action list**:

### 1. Overall Verdict
Brief summary: "Substantially compliant — X% aligned. No scope overlap. Y minor wording gaps."

### 2. Detailed Compliance Table
Requirement → sub's coverage → status (✅/⚠️/❌/⬛/❓). Group by source document (ER, SOW, DMP).

### 3. Critical Gaps / Dependencies to Close
Two sub-sections:

| Severity | Label | Meaning |
|----------|-------|---------|
| 🔴 Critical | **Sub gap** | Missing deliverable the sub must provide — blocks sign-off |
| 🔴 Critical | **External dependency** | Not the sub's fault, but must be resolved separately (e.g., MEP contract not awarded) |
| 🟡 Medium | Minor wording addition needed | Standard reference, service life statement — not a re-negotiation |
| 🟢 Low | Informational | Interface register, review SLA — can be added to appointment letter |

### 4. Prioritised Action List ("So what do I do?")

**CRITICAL** — the user ALWAYS wants this section. A compliance review without "so what do I do next?" is incomplete. Numbered actions, each with:
- Clear owner (You / Procurement / PM / etc.)
- Urgency badge (🔴 🔴External / 🟡 / 🟢)
- Concrete next step, not a vague recommendation

Example:
1. 🔴 **Award MEP designer (Bluehaus/AD)** — their scope must explicitly include DALI/DMX panel engineering + BMS programming. This unlocks the control system. | Owner: You
2. 🟡 **Approve sub scope internally** — sign off. Minor wording gaps handled in appointment letter. | Owner: You
3. 🟢 **Issue RFQ to S&I sub** — can't price until Stage 4 deliverables from designer are approved. | Owner: Procurement

**Common action patterns for museum subs:**
| Phase | Action |
|-------|--------|
| Design consultant | Sign off → appointment letter with minor conditions → Stage 4 deliverables |
| S&I sub | Wait for designer Stage 4 BOQ → RFQ → award |
| MEP designer | Award separately — controls engineering is NOT in lighting designer scope |
| BIM | Hand ZNA CAD/DWG to Radiance Group for Revit modeling — BIM is Samaya scope |
| Control engineering | Ensure MEP/controls vendor picks up BMS/DALI programming explicitly |

## Email deliverable template

When the review is requested via email, reply with:

```
Subject: RE: [Sub Name] Scope of Work — Compliance Review

Dear Team,

We completed a full cross-reference of [Sub]'s proposal against the ER, SOW, DMP, and NRS Methodology.

Overall finding: [Substantially compliant / Not compliant] — [X]% alignment. [No / Minor / Major] scope overlap or missing deliverables.

Compliance summary:
[Table: Doc → alignment % → notes]

[If applicable: No scope overlap — the two-subcontractor model is cleanly demarcated.]

Minor gaps identified (X items, all wording additions — not re-negotiations):
1. ...
2. ...

[If applicable: Outside [Sub]'s scope (must be resolved separately):]
- Item A → assigned to [party], not yet awarded
- Item B → assigned to [party]

Recommendation: [Approve and proceed / Hold pending resolution of critical gaps].

Ready for client submission once conditions are appended.
```

## Pitfalls

- **ZD-0026 source often missing** — the NRS Design Methodology PDF was approved (Code B) but the actual document body is frequently not archived on local disk. Only CG cover sheet exists. Note this in the report and recommend pulling from Aconex.
- **StudioZNA proposals** — received via email (1-Jun-2026). Check `Design Files/00_Scope_and_Proposals/` and `Subcontractors/04_Lighting_Contractor/00_Scope_of_Work/01_Designer_Subcontractor/`. The extracted markdown summary (`Aseer_2026_SCOPE_Summary.md`) may exist alongside the PDF.
- **Scope_Split matrix may be newer than sub proposal** — the Responsibility Matrix (if drafted) may reflect a refined two-subcontractor model not yet agreed with the sub. Compare against what the sub actually proposed, not just against the matrix.
- **ER and SOW live in multiple copies** — the ER might exist in both `Subcontractors/<Trade>/` and `Package_Part 2/`. Version-check dates before using.
- **Two-subcontractor model** — for museum lighting, the design consultancy (StudioZNA) and the supply/install (ERCO/iGuzzini) are separate. Do NOT conflate. The same applies to MEP: 12_MEP_Installation (S&I contractor) vs 18_MEP_Designer (design consultant). Both follow the same design→install split.
- **Folder numbering** — subcontractors are numbered 01–18. Keep numbering clean when adding new folders. Archive dead/disputed entries under `_ARCHIVE/`. If a number conflicts (e.g., 14_MEP_Contractor overlapped 14_Rigging_Contractor), renumber to the next available (18 in that case).
- **After the compliance matrix, always produce a prioritised action list.** The user wants "so what do I do next?" — not just a review report.
- **When the user corrects a gap attribution, do not argue.** If they say "X is not Y's scope," verify immediately and update. The user knows their subcontractor structure better than you do.

## Contracts folder convention

When reorganizing `Contracts/` (or discovering it needs cleanup), use this standard structure:

```
Contracts/
├── 01_Main_Contract/            # EPC / main contract (e.g. 0010003521) + ER + SOW
├── 02_<Party>_Contract/         # Per-party, e.g. 02_NRS_Contract
│   ├── 01_Signed_Agreements/    # Signed contracts, insurance certs, SOW matrices
│   ├── 02_Proposals_and_Quotes/ # Technical/financial proposals, cash flows
│   ├── 03_Analysis_Reports/     # Any md/html analysis files (NOT contracts, but kept w/ party)
│   └── 04_Invoices/             # Invoices from that party
├── 03_GBH_Showcase_Contract/    # Other party contracts (sequential numbering)
├── 04_MEP_Contract/             # MEP design contract files
├── 05_Purchase_Orders/          # All POs (P00737, P01180, etc.)
├── 06_Proposals_and_Quotes/     # Miscellaneous quotes not specific to one party
├── 07_Subcontractor_Register/   # Prequalification registers
└── 99_Stubs_and_Duplicates/     # Zero-byte stubs, duplicates found during cleanup
```

- Remove empty source folders (e.g., old `Project Contract/`, `MEP/`)
- Merge NSR analysis files into `02_NRS_Contract/03_Analysis_Reports/` — they are submittal/RFI analyses, not contractual documents, but keeping them under the party context preserves traceability
