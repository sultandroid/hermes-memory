# Plan-Level CG Comment Audit Against Contractual Obligations

## When to Use

CG returns a management plan (SMP, DMP, HSE Plan, QMP, etc.) with Code C (Revise and Resubmit) and a list of comments. Before drafting responses, audit each comment against the actual contractual obligations (ER, SoW, SBC, contract) to determine:

- Is the CG comment valid (grounded in a real obligation)?
- Is the comment already addressed in the submitted document?
- What specific action is needed to close it?
- Is this scope creep? (new deliverable, cost impact, schedule impact)

## Workflow

### 1. Extract CG Comments

From the submittal PDF cover sheet + CG response sheet:

```
pdftotext "/path/to/submittal.pdf" /tmp/extracted.txt
```

Read the cover sheet first — it has the submittal number, revision, date, and CG status. Then read the CG comments section (usually after the cover sheet).

### 2. Map Each Comment to ER/SoW/SBC

For each CG comment, find the exact contractual clause that gives rise to it:

| Source | Where to find it |
|--------|-----------------|
| ER (Employer's Requirements) | `99_Archive/01_Integration_Management/Project_Charter/er_document.txt` (OCR of the ER PDF) |
| SoW (Scope of Work) | `99_Archive/01_Integration_Management/Project_Charter/scope_of_work.txt` |
| SBC 1001 | Referenced in ER section 2.0 as applicable code |
| Contract | `00_Contracts/00_Contract_Summary.md` |

Key ER sections for sustainability plans:
- **ER section 2.4D** — Sustainability & Environmental Performance (material compliance, low-VOC, Oddy test)
- **ER section 2.7** — General Cleaning (sustainability requirements for cleaning operations)
- **ER section 3.7.VIII** — Client sustainability initiative, energy efficiency, green building adherence
- **ER section 3.7.XIII** — Applicable Codes (Mostadam Manual listed as Code #2 — no specific certification level)

### 3. Check the Submitted Document

Read the submitted plan (extracted from the same PDF) and check each CG comment against what the plan actually says. Use three statuses:

| Status | Meaning |
|--------|---------|
| Missing | Comment is valid and plan does not address it at all |
| Partially addressed | Comment is valid but plan only partially covers it |
| Addressed in principle | Plan covers the general area but does not cite the specific ER/SoW clause |
| Addressed | Plan fully addresses the comment with specific references |

### 4. Triage Into Three Lanes (Scope Creep Protection)

Not all CG comments are equal. Before sending instructions to the specialist, triage each comment:

| Lane | Criteria | Action | Example |
|------|----------|--------|---------|
| Comply | Contractual obligation, no cost/schedule impact | Add to plan, no pushback | MOSTADAM prerequisites table, cleaning sustainability |
| Comply (limited) | Contractual obligation but scope-limited — we define criteria, others implement | Add criteria to plan, state who implements | Sustainability SPECS (we define, NRS implements) |
| Push back | Not a contractual obligation, or has cost/schedule impact | Do NOT include. Prepare separate proposal if CG insists | Exhibition sustainability strategy (not in ER/SoW as standalone deliverable) |

### 5. Determine Priority

| Priority | Criteria |
|----------|----------|
| High | Comment blocks approval (Code C driver), relates to a mandatory ER/SoW clause, or requires NRS/designer input |
| Medium | Procedural or documentation comment, can be addressed in a revision without external input |
| Low | Clarification or preference comment, not a hard requirement |

### 6. Produce the Audit

Structure as a table:

```
| # | CG Comment | ER/SoW Reference | Obligation | SMP Rev00 Status | Action Required | Priority |
|---|-----------|-----------------|-----------|-----------------|----------------|----------|
| 1 | ... | ER section 3.7.XIII | ... | Missing | ... | High |
```

Add a summary section with:
- Total comments, broken down by status
- Key findings (patterns, critical gaps)
- Key ER/SoW references used

### 7. User Review Gate — Do NOT Send Directly

**The CR sheet is a collaborative document, not a dispatch.** After producing the audit table and CR sheet:

1. **Present both files to the user** — open them in the editor or show the key decisions
2. **Flag the decisions the user needs to make** — especially push-back items (scope creep) and any comments where the response strategy has options
3. **Wait for user confirmation** before sending to the specialist
4. **Do NOT send the CR sheet to the specialist** without the user reviewing it first

The user explicitly corrected: "I didnt send the CR sheet please open we have to work on it again to send to fida" — meaning the CR sheet is reviewed and potentially modified by the user before it goes out.

### 8. Produce the CR Sheet for the Specialist

For each comment, provide copy-paste instructions:

```
## CG Comment N — [Title]

| Field | Detail |
|-------|--------|
| CG Comment | [exact text] |
| ER/SoW Reference | [clause] |
| Our Obligation | On our shoulder / Push back — [reason] |
| Cost Impact | None / Minor / Yes — [amount] |
| Schedule Impact | None / Yes — [duration] |
| Action for Fida | [specific copy-paste instructions] |
| Response to CG | [exact text to use] |
```

### 8. Add New Risks to Risk Register

For each push-back item, add a risk to the project risk register:

| Risk ID | Category | Risk Event | P | S | Score | Mitigation |
|---------|----------|-----------|--|---|-------|------------|
| PRR-SMP-001 | COM | CG may insist on exhibition sustainability strategy as condition of SMP approval | 3 | 2 | 6 (Medium) | Prepare position paper showing coverage in existing SMP. If CG insists, submit separate proposal. |
| PRR-SMP-002 | PRC | CG may reject SASO equivalent and demand Energy Star/WaterSense | 2 | 2 | 4 (Medium) | Proactively specify SASO equivalent. If rejected, provide cost comparison and request VO. |

## Key ER/SoW References for SMP Audits

| Reference | Content | When to cite |
|-----------|---------|-------------|
| ER section 2.4D | Sustainability & Environmental Performance — material compliance, low-VOC, Oddy test, designer compliance certificate | Material compliance, VOC, Oddy comments |
| ER section 2.7 | General Cleaning — compliance with sustainability requirements and targeted points/guidelines | Cleaning sustainability comments |
| ER section 3.7.VIII | Compliance with client sustainability initiative, energy efficiency standards, green building adherence | Client initiative, energy efficiency comments |
| ER section 3.7.XIII | Applicable Codes — Mostadam Manual listed as Code #2 | Mostadam-related comments |
| SoW section 1.5 | Applicable Codes — includes Oddy testing, British Museum certification | Oddy test comments |
| SoW section 2.1 | Exhibition design (RIBA Stage 4) and off-site fabrication scope | Exhibition sustainability comments |
| SBC 1001 | Saudi Green Building Code — referenced in ER as applicable code | Energy, water, IEQ, materials, waste comments |

## Critical Finding Pattern: MOSTADAM Certification Level

The ER lists "Mostadam Manual" as an applicable code but does **not** specify any certification target level (Bronze/Silver/Gold). This is a common source of CG comments. The correct position:

> SMP should be compliance-based, not certification-based: comply with SBC 1001 and Mostadam Manual as referenced in the ER — no commitment to any specific rating level.

Any references in the SMP to a specific Mostadam level should be removed unless contractually required.

### CG Asking for Credit Selection Criteria

If the SMP includes a Yes/No MOSTADAM credit selection table and CG asks for selection criteria/rationale:

| Situation | Response |
|-----------|----------|
| SMP has a Yes/No credit selection table | **Remove the table entirely.** The table implies we are pursuing certification. Since no certification level is contractually required, there are no credits to select. The table invites exactly this question. |
| CG asks for rationale per credit | **Push back.** "The MOSTADAM credit matrix is an informational reference showing the relationship between project scope and MOSTADAM D+C credits. Since no specific certification level is contractually required per ER section 3.7.XIII, there are no credits to select or criteria to define. The table is provided for awareness only." |
| CG insists on keeping the table | Add a note: "Credit selection is based on project scope and applicable code requirements per ER section 3.7.XIII. No specific certification level is contractually required." |

**Do NOT** add a rationale column or fill rows with justifications — that implies we are pursuing certification, which we are not. The best move is to remove the table so it stops inviting the question.

## Pitfalls

- **Do not assume the CG comment is valid.** Always check the actual ER/SoW text. CG sometimes asks for things beyond the contractual scope.
- **Do not assume the ER specifies a Mostadam certification level.** It lists the Manual as an applicable code only. Committing to a level (Bronze/Silver) without contractual basis creates liability.
- **Check the ER OCR text directly** — the ER summary in the repo may be incomplete. The full OCR is at `er_document.txt`.
- **SMPs written as general construction plans** will miss exhibition-specific sustainability (showcase materials, AV sustainability, artefact conservation). This is a common gap.
- **Energy Star / WaterSense** is not explicitly in the ER but is a reasonable extension of SASO Energy Efficiency Standards (ER section 3.7.XIII). CG will ask for it — prepare to comply.
- **Cleaning sustainability (ER section 2.7)** is often overlooked in SMPs. The ER explicitly requires cleaning operations to comply with sustainability requirements.
- **NRS review** is required per ER section 2.4 approval framework. If the SMP has not been reviewed by the lead designer, that is a valid CG comment.
- **Exhibition sustainability strategy** is NOT a named deliverable in ER/SoW. If CG asks for it as a standalone document, it is scope creep. Offer a subsection in the SMP instead.
- **SASO equivalent is acceptable** for Energy Star/WaterSense per ER section 3.7.XIII. Do not commit to US-only certification unless CG explicitly rejects SASO.
- **MOSTADAM credit selection table invites CG questions.** If the SMP has a Yes/No credit matrix and no certification is required, remove the table entirely. It implies we are pursuing certification and will generate comments asking for rationale. The table is for awareness only — if it causes questions, it is doing more harm than good.
