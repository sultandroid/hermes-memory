---
name: cg-submittal-review-checklist
description: "Pre-submission review checklist for ANY submittal, built from all CG common comments, 36 lessons learned, and reviewer profiles. Run before sending anything to CG to avoid the recurring Code C/D rejection patterns."
tags:
  - cg
  - submittal
  - checklist
  - pre-submission
  - review
  - quality-gate
---

# CG Submittal Review Checklist

## Trigger

Use this skill whenever the user asks to:
- "check if this rev complies with all comments"
- "review this submittal before sending to CG"
- "make a checklist for reviewing submittals"
- "is this ready to submit?"
- "forecast CG response" (pair with `cg-analysis-and-lessons`)

This is the **pre-submission quality gate**. It exists because the project has a documented recurring failure: documents resubmitted to CG without closing prior comments, or submitted with explanations instead of physical evidence, earning repeated Code C/D (LL-017, LL-018, LL-023, Structural DD 2x, PEP 2x, DMP, BMS).

## The Core Rule (from lessons learned)

> **Never resubmit to CG without confirming ALL previous CG comments are closed, with physical evidence — not explanations, not promises, not "under preparation".**

If any prior comment is answered with a promise or a reference instead of evidence, the resubmission will return Code C again. This is the single most common root cause on this project.

## How to Run the Review

1. **Get the CG comments** — the previous Code C/D rejection (verbatim) + any CRS sheet. Extract from the PDF/CRS, not from memory.
2. **Get the revised package** — the new Rev folder contents.
3. **Map each CG comment to evidence in the revised package.** For each comment, find the actual content change (not an annotation about the change).
4. **Run the Universal checklist** (Section A) on the whole package.
5. **Run the type-specific checklist** (Section B) matching the submittal type.
6. **Run the reviewer-specific checks** (Section C) for the named CG reviewer.
7. **Run the closure gate** (Section D) — the mandatory CRS/comment closure check.
8. **Report** — table of each comment: COMPLIED / PARTIAL / NOT COMPLIED, with the evidence found (or the gap).

## Section A — Universal Checklist (ALL submittals)

These are the 10 recurring rejection patterns (from `cg_rejection_patterns.md`). If any fails, DO NOT SUBMIT.

### A0 — Document Control / Metadata (the formal package identity)

CG rejects submittals for missing or inconsistent document-control metadata before even reading the content. Check every document in the package:

| # | Check | What CG looks for |
|---|-------|-------------------|
| A0.1 | **Submittal name / title** | Matches the register and the submission plan exactly (e.g. "AV Package Part II - Detailed Design 50% Gate"). No abbreviated or renamed titles. |
| A0.2 | **Submittal type** | Correct type declared (Document Submittal / Drawing / Material Submittal / Prequalification / Method Statement / Plan). Matches the register's type column. |
| A0.3 | **Document number** | Present, correct, project-prefixed (e.g. `MOC-MUS-ASE-1E0-1G-0002`). Matches the register and the cover. No typos, no missing prefix. |
| A0.4 | **Revision** | Correct Rev label (Rev 01, not R01 or Rev 0). Consistent across cover, TOC, every page footer, and filename. |
| A0.5 | **Date** | Present and current. Matches the submission date. No stale dates from a prior revision. |
| A0.6 | **References** | Related documents and previous revisions listed (CG comment: "always mention the related list of documents and previous revisions"). |
| A0.7 | **Title block** | Complete on every drawing/sheet: project, doc no., rev, date, sheet title, scale, drawn/checked/approved. |
| A0.8 | **Discipline** | Correct discipline code (1E0 = Electrical/AV, 1C0 = Structural, 1A0 = Arch, etc.). |
| A0.9 | **Stamp** | Signed and stamped by the responsible party (AV Specialist Contractor, designer, etc.). CG comment 7 explicitly requires this. |
| A0.10 | **QA/QC review** | Documents reviewed by QA/QC before submission (CG comment 6 explicitly requires this). |
| A0.11 | **Cover page** | Concise, CG-relevant only: doc ref, revision, date, supersedes statement, reference docs. No verbose change descriptions or internal notes. |
| A0.12 | **Revision history table** | Shows only actual CG submissions, not internal drafts. |
| A0.13 | **Consistency across package** | Doc number, rev, date, and title identical on cover, TOC, footers, and filename. A mismatch anywhere is an immediate rejection signal. |
| A0.14 | **Sequential numbering** | Per Sundus Alfeer directive — submittals numbered sequentially by discipline. |

> **Pitfall — metadata vs reality:** A PDF that says "Rev A - Issued to CG" on its cover does NOT mean it was submitted. Cross-check the register status column (Draft/Open/Answered/Closed) before asserting submission status. The register is ground truth, not the PDF cover.

| # | Check | Rejection pattern it prevents | Source lesson |
|---|-------|-------------------------------|---------------|
| A1 | **All required appendices attached?** (checklists, training records, risk assessments, signatures) | Incomplete submission (10+ occurrences) | LL-002, LL-008 |
| A2 | **NRS review report attached?** (for design deliverables) | Missing specialist endorsement (6+) | LL-007, SMP C-1 |
| A3 | **ER/SoW clause references cited?** | Non-compliance with specs (8+) | LL-002, LL-003 |
| A4 | **Cross-disciplinary coordination verified?** (loads vs structural, MEP vs arch, AV vs lighting) | Cross-disciplinary gaps (4+) | LL-010, LL-028 |
| A5 | **Sequential numbering per Sundus Alfeer directive?** | Submission organisation | LL-008 |
| A6 | **Document format complete?** (doc number, date, revision, references, title block) | Format rejection (CG comment 6) | AV 1G-0002 |
| A7 | **Signed and stamped by the responsible party?** (specialist contractor, designer) | Missing signature/stamp (CG comment 7) | AV 1G-0002 |
| A8 | **QA/QC reviewed before submission?** | CG explicitly demands QA review | LL-017, LL-018 |
| A9 | **No placeholders / "to be confirmed" / "under preparation"?** | CG flags incomplete content | LL-006 |
| A10 | **No AI fingerprints / symbols?** (no em dash, arrow, section symbol, emoji) | Professional format | hermes-quality-assurance |
| A11 | **Revision history shows only actual CG submissions?** | Stale/wrong revision labels | hermes-quality-assurance |
| A12 | **Cover page concise, CG-relevant only?** | Cover page bloat | hermes-quality-assurance |
| A13 | **No unapproved personnel names?** (role only if not formally approved) | Liability — CG holds Samaya to unapproved names | cg-response-protocol |

## Section B — Type-Specific Checklist

### B1. Material Submittals (MA)
| # | Check | Source |
|---|-------|--------|
| B1.1 | **Minimum 3 suppliers provided?** (single-source = Code C/D) | LL-001, LL-002, LL-020, LL-025 |
| B1.2 | Manufacturer certificates of conformity? | LL-002 |
| B1.3 | Fire-rated test reports? | MA-0007 |
| B1.4 | **Oddy test results** (museum-grade materials)? | LL-003, MA-0007 |
| B1.5 | VOC and off-gassing test reports? | MA-0007 |
| B1.6 | MSDS included? | MA-0007 |
| B1.7 | Chemical composition data? | MA-0007 |
| B1.8 | Physical samples submitted? | MA-0006 |
| B1.9 | Anti-reflective glass spec compliant (Tvis/Rvis)? | LL-002 |
| B1.10 | Material matches the approved finishes schedule? | MA-0006 |

### B2. Prequalifications (PQ)
| # | Check | Source |
|---|-------|--------|
| B2.1 | **3 museum project references?** | LL-008, LL-020 |
| B2.2 | Company profile + ISO certs? | LL-008 |
| B2.3 | Key personnel CVs? | PL-0020 |
| B2.4 | Organisational chart? | PL-0020 |
| B2.5 | Correct tier classification (T1/T2/T3)? | PL-0020 |
| B2.6 | KSA-based engineer (if required)? | PL-0020 |
| B2.7 | **Certificates valid (not expired)?** (CR/Chamber/MMH) | LL-008 |
| B2.8 | Detailed methodology included? | LL-008 |
| B2.9 | **≥2 suppliers per scope?** (challenge any single-source PQ) | LL-025 |

### B3. Design Documents (ZD/IFC/DD)
| # | Check | Source |
|---|-------|--------|
| B3.1 | **PDD approved first?** (IFC sequence rule: PDD → 3D Render → Material Board → IFC) | LL-005, LL-028, LL-033 |
| B3.2 | NRS sign-off attached? | LL-007 |
| B3.3 | BIM coordination documented? | LL-028 |
| B3.4 | Sustainability criteria stated? | SMP |
| B3.5 | Cross-discipline interface register? | LL-010 |
| B3.6 | **Physical evidence, not promises?** (site tests DONE, not promised) | LL-006, Structural DD |
| B3.7 | Object list locked (for showcases)? | LL-019 |
| B3.8 | Structural sign-off before IFC? | LL-028 |
| B3.9 | **Project-specific, not generic?** (named hardware, real schedules, real calculations) | AV 1G-0002, Venugopal |
| B3.10 | Sequence of operation / control narrative (for control systems)? | AV 1G-0002 |
| B3.11 | I/O + command list, protocol schedule (for control systems)? | AV 1G-0002 |
| B3.12 | Rack-by-rack equipment schedule + mfr power data (for UPS/power)? | AV 1G-0002 |
| B3.13 | Selected switch model + port count + PoE budget + VLAN-to-device schedule (for networks)? | AV 1G-0002 |

### B4. HSE Plans
| # | Check | Source |
|---|-------|--------|
| B4.1 | **Electrical/technical data separated into standalone submittal?** | LL-004, 1KH-PL-0043 |
| B4.2 | All appendices (checklists, training records, risk assessments)? | 1KH-PL-0037 |
| B4.3 | Signatures on all required pages? | 1KH-PL-0037 |
| B4.4 | Medic details included (Worker Welfare)? | 1KH-PL-0037 |
| B4.5 | Waste management compliance (segregation/tracking)? | LL-026 |

### B5. Programme / Schedule
| # | Check | Source |
|---|-------|--------|
| B5.1 | Cost loading included? | LL-027, NC-CG-001 |
| B5.2 | EVM curves included? | LL-027 |
| B5.3 | Manpower histograms included? | LL-027 |
| B5.4 | Milestones agreed with MoC? | LL-029 |
| B5.5 | Recovery plan stays inside contractual completion date? | ZD-0104 |

### B6. Site-Test / Physical-Work Submittals (IR, core tests, boreholes)
| # | Check | Source |
|---|-------|--------|
| B6.1 | **IR filed AFTER the physical work is done?** (never before) | CG 6-step sequence |
| B6.2 | Method Statement + drawings showing exact test locations? | CG 6-step |
| B6.3 | SNA (Start New Activity) filed? | CG 6-step |
| B6.4 | Third-party testing agency prequalified? | CG 6-step |
| B6.5 | Test report + close-out of comments? | CG 6-step |

## Section C — Reviewer-Specific Checks

Run the checks for the named CG reviewer (from `cg_reviewer_profiles.md`). If reviewer unknown, prepare to the strictest standard.

| Reviewer | Focus | Pre-empt by |
|----------|-------|-------------|
| **Venugopal Poyakkara Veetil** (AV/IT/ELV) | Rejects generic docs. Wants project-specific control architecture, interface matrix, selected switch models with port counts/PoE/fibre, exhibit-by-exhibit control with device lists + alarm matrices, supported UPS load calcs with rack-by-rack schedules, signed/stamped docs | B3.9–B3.13, A6, A7 |
| **Mansour Alrezeni** | Code enforcer. Submit only what spec says. No alternatives/splits. Requires 3 suppliers, full certs | B1.1–B1.8 |
| **Gaby Khoury** (Showcases) | Drawing completeness + material submittal. All details incorporated, mechanism illustrations, access panel dims, electrical/AV outlets, structural calcs | B1, B3 |
| **Mohamed Magdy** (Mechanical) | SBC code refs, ergonomic standards, assessment report completeness | B3 |
| **Abdrabo Shahin** (Structure) | Contractual/SoW detail, SI refs, RACI, coordination interfaces | A3, A4 |
| **Eslam Metwally** (Electrical) | Load calcs, cable schedules, earthing details | B3.12 |
| **Anwar Sadat** (HSE) | HSE content only; rejects embedded technical data | B4.1 |
| **Maged Zamzam** (Sr Arch) | BIM coordination, environmental sustainability | B3.3, B3.4 |

## Section D — Mandatory Closure Gate (resubmissions)

**Run this BEFORE any resubmission.** This is the documented recurring failure (LL-017, LL-018, LL-023, Structural DD 2x, PEP 2x, DMP, BMS).

1. **Every CG comment from the previous round has a response?** (CRS Originator Reply column filled)
2. **Each response is physical evidence** (test report, approved drawing, completed study, manufacturer data) — NOT an explanation, reference, or "under preparation"?
3. **Any item still pending is explicitly deferred in a cover note** with a commitment date?
4. **Internal QA review completed and signed off** (Quality Team + PM) before submission?
5. **Minimum 3-day internal review** for major documents (PEP, plans, DD)?
6. **Prior consultant comments incorporated** (e.g. GITCO, NRS) before resubmission?

If any of 1–4 fails → **DO NOT SUBMIT.** Hold until cleared.

## Section E — Forecast the CG Response

After the review, forecast the likely code (pair with `cg-analysis-and-lessons`):

| If the package... | Predicted code |
|-------------------|----------------|
| Closes all comments with evidence, no generic content | **B** (Approved with comments) |
| Still generic, missing named hardware/schedules/calcs, or any comment answered with explanation | **C** (Revise & Resubmit) |
| Missing a demanded document entirely, or out of sequence | **C or D** |

## Output Format

Present the review as a table:

```
| # | CG Comment | Status | Evidence in Rev package / Gap |
|---|------------|--------|-------------------------------|
| 1 | [verbatim intent] | COMPLIED / PARTIAL / NOT COMPLIED | [file + what it shows, or what's missing] |
```

Then a bottom line: READY TO SUBMIT / NOT READY, with the specific blockers.

## Pitfalls

- **Do not trust the CRS "Closed" status.** A comment marked Closed in the CRS may not have actual evidence in the revised document. Verify the content change exists.
- **"Noted" is not compliance.** A reply of "Noted" to a technical comment (e.g. "demonstrate audibility") does not close it. CG wants the demonstration.
- **Generic documents are the #1 AV rejection.** If a doc says "typical", "recommended", "where required" without naming the actual project hardware/schedules, it will be rejected by Venugopal.
- **A demanded document that doesn't exist in the package = automatic C.** Check the file list against every CG-cited document name.
- **Explanations vs evidence:** "The rack elevation is an AV standard document" is an explanation. A rack-by-rack equipment schedule with manufacturer power data is evidence. Only the latter closes a comment.
- **Scope-deferral is not compliance.** "UPS one-line is not in our scope, electrical team provides it" may be true, but CG still wants the AV load evidence. Provide what IS in scope completely.
- **Check the actual file, not the folder name.** A folder may contain a doc with a similar name that is NOT the one CG cited (e.g. CMS doc ≠ Control UI & Fault Monitoring doc).
- **Verify the Zyxel/selected switch model appears in the network doc** — a CRS reply claiming it was reconciled is worthless if the model name is absent from the document (grep it).
- **Numbering gaps** (e.g. "Item 8 skipped") are easy CG catches — verify section numbering is complete.
- **Never submit with a promise of future work** (LL-006). Execute the site investigation / test first, then submit the evidence.

## Related Skills

- `cg-response-protocol` — CRS creation, comment triage, stage-boundary handling
- `cg-analysis-and-lessons` — rejection patterns, reviewer profiles, forecast engine, lessons register
- `hermes-quality-assurance` — document format, AI-fingerprint, personnel-name, revision-history checks
- `submittal-register-gap-analysis` — auditing registers against consultant comments
