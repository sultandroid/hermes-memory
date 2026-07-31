---
id: 006
slug: 12d-synergy-cde-iso-19650-workflow-guide
theme: "6 — Common Data Environment (CDE) — ISO 19650-2 workflow"
title: "The Ultimate Guide to the Common Data Environment (CDE)"
year: 2024
authors: "12d Synergy Knowledge Team — vendor-authoritative guide on ISO 19650 information management process"
publisher: "12d Synergy (12dsynergy.com) — CDE vendor; the guide is also the companion piece to 12d Synergy's ISO 19650 guide and reflects PD 19650-0:2019 (BSI)"
url: "https://www.12dsynergy.com/guides/common-data-environment"
retrieved: 2026-07-31
verification: verified-via-tavily
---

# Case 006 — 12d Synergy CDE Guide (ISO 19650-2 four-state workflow)

## Quick Facts
- **Theme(s)**: 6 (Common Data Environment workflow — the four-state ISO 19650-2 information-delivery process), 2 (BEP / information-container specification)
- **Year**: 2024 (vendor-page version; cites PD 19650-0:2019 BSI transition guide and refers to "national annexes" of ISO 19650-2)
- **Authors**: 12d Synergy Knowledge Team (vendor guide written by CDE-practitioner authors; structurally follows ISO 19650-2 clauses)
- **Publisher / Source**: 12d Synergy — CDE vendor; widely cited in GCC consultancy practice as a clear, vendor-neutral exposition of the four-state CDE workflow
- **URL**: <https://www.12dsynergy.com/guides/common-data-environment>
- **Format**: Online guide (chapter-format long-form)

## Summary
The 12d Synergy CDE guide explains the four-state information workflow prescribed by ISO 19650-2 — Work-in-Progress (WIP) → Shared → Published → Archived — and the role of the CDE as the controlling "source of truth" for a project. It emphasises that information may pass between WIP and Shared states several times before being eventually Published, that Published information is what is relied upon contractually, and that Archived information aggregates into the Asset Information Model (AIM) for the operations phase. The guide is explicit that, in case of legal dispute, "an audit trail of information development and exchange is captured across the delivery and operation of a built asset" — a direct contractual justification for the CDE. The guide provides the working-language around the WIP status code convention (S0 default), the role of the CDE administrator(s), and the project/asset information models required by ISO 19650-2.

## Direct Quote (verbatim from source)
> "An audit trail of information development and exchange is captured across the delivery and operation of a built asset."

> "Information is progressively developed through a managed process, with permissions controlled accordingly by the CDE. … information may pass between WIP and Shared states several times before being eventually Published."

> "Archived information is read-only and only accessible to the appointing party and the CDE administrator(s). When the information requirements are satisfied, the information is archived and aggregated into the asset information model (AIM) for the ongoing operation and maintenance of the asset."

## Source
12d Synergy Knowledge Team (2024). *The Ultimate Guide to the Common Data Environment (CDE).* 12d Synergy. <https://www.12dsynergy.com/guides/common-data-environment>.

## Lesson Extracted
1. **The four-state workflow is contractual**: WIP / Shared / Published / Archived is not a vendor preference — it is ISO 19650-2. A dispute over a "model file we relied on" turns on whether the file was in Published status and who authorised the status change. The audit trail in the CDE decides.
2. **CDE admin role is the gatekeeper of liability**: Only the CDE administrator(s) control publication/archival. Where a project has no named CDE admin (or the contractor's BIM manager self-publishes), the audit trail is compromised and the limitation-of-liability defence fails.
3. **"Published = relied upon"** is the test, not the filename: Many contractors defend fabrication-from-model by reference to the latest named file. ISO 19650-2 says: reliance flows from Published status — and a model never Published was never authorised for fabrication.
4. **Archived information is the AIM**, and only the appointing party + CDE admins can read it. The contractor's entitlement to AIM data after handover (for defects rectification, O&M) must be contractually confirmed in the BEP — otherwise the contractor's defence on latent-defect claims is eviscerated by lack of access.
5. **WIP ↔ Shared iteration is normal**: A BEP that sets a single WIP-to-Published pass assumes perfect drawings on first iteration — the more common path is multiple WIP ↔ Shared revisions. The CDE workflow must support this iteratively; failure to do so means issues are forced into "either publish or stay in WIP" decisions, both bad.

## How to use this in a BIM-coordination playbook
Use this as the one-page reference document opposing counsel can hand to a non-BIM-specialist adjudicator. The four-state workflow is the contractual lingua franca — agreements or evidence that contradict it are bad evidence. Pre-emptively: appoint a named CDE administrator at the contract-preliminaries stage.

## Verification trail
- Tavily search query used: `Common Data Environment CDE ISO 19650-2 workflow`
- Raw search saved at: `/tmp/tavily-research-bim/raw/search-06-common-data-environment-cde-iso-19650-2-workflow.json`
- Raw extract saved at: `/tmp/tavily-research-bim/raw/extract-08-www-12dsynergy-com-guides-common-data-environment.json`
- Direct quotes cross-checked against `raw_content` of that file (anchors "audit trail of information development and exchange", "WIP and Shared states several times before being eventually Published", "Archived information is read-only" all hit).
