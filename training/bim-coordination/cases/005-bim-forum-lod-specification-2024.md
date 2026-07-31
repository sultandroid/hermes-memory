---
id: 005
slug: bim-forum-lod-specification-2024
theme: "4 — LOD (Level of Development) disputes"
title: "Level of Development (LOD) Specification"
year: 2024
authors: "BIM Forum — practitioners' authoring group drawing on AIA G202-2013 BIM Protocol Form (basic LOD definitions) and CSI Uniformat 2010 (organisation)"
publisher: "BIM Forum (bimforum.org) — North-American practitioners' body; the 2025 LOD Spec Official version was posted on the resource page in December 2024 / January 2025"
url: "https://bimforum.org/resource/lod-level-of-development-lod-specification"
retrieved: 2026-07-31
verification: verified-via-tavily
---

# Case 005 — BIM Forum LOD Specification (2024 edition)

## Quick Facts
- **Theme(s)**: 4 (LOD / Level of Development disputes — the cross-reference between LOD and contractual entitlement to model reliance)
- **Year**: 2024 (page dated "Tuesday, December 31, 2024"; downloads to the 2025 LOD Spec Official version)
- **Authors**: BIM Forum practitioner authoring group
- **Publisher / Source**: BIM Forum — industry LOD Spec authority; this is the de facto North-American LOD reference, adopted by reference in many GCC construction contracts via the AIA G202-2013 / G201-2007 family
- **URL**: <https://bimforum.org/resource/lod-level-of-development-lod-specification>
- **Format**: Industry specification / model-element reference (downloadable zip)

## Summary
The BIM Forum LOD Specification is the cross-AEC industry reference that defines what a recipient of a model can rely on at each Level of Development from LOD 100 (conceptual) through LOD 500 (as-built / verified). The specification extends the AIA G202-2013 BIM Protocol Form's basic LOD definitions into a CSI Uniformat-organised catalogue of model-element expectations. Its contractual function is the answer to one of the most common disputes in BIM-coordinated projects: "what was the contractor obligated to deliver at LOD 300, and what can the employer rely on?" Without the LOD Spec, parties argue about whether a "model" is geometrically complete or only approximately complete — a foundational issue when a downstream trade fabricates from the model and a clash is later discovered.

## Direct Quote (verbatim from source)
> "The *Level of Development (LOD) Specification* is a reference that enables practitioners in the AEC Industry to specify and articulate with a high level of clarity the content and reliability of Building Information Models (BIMs) at various stages in the design and construction process. The *LOD Specification* utilizes the basic LOD definitions developed by the AIA for the *AIA G202-2013 Building Information Modeling Protocol Form* and is organized by CSI Uniformat 2010."

> "It defines and illustrates characteristics of model elements of different building systems at different Levels of Development. This clear articulation allows model authors to define what their models can be relied on for, and allows downstream users to clearly understand the usability and the limitations of models they are receiving."

## Source
BIM Forum (2024/2025). *Level of Development (LOD) Specification — 2025 LOD Spec Official version.* BIM Forum. <https://bimforum.org/resource/lod-level-of-development-lod-specification>.

## Lesson Extracted
1. **LOD is a reliance concept, not a geometry concept**: A LOD 300 model element is one the author can guarantee is geometrically and dimensionally accurate — not merely detailed. Where a contractor fabricates from a LOD 200 model, they are fabricating on the author's risk.
2. **Contract integration via AIA G202**: Many FIDIC / GCC bespoke BIM-clauses incorporate the LOD Spec by reference but inconsistent across packages (one sub-contractor on LOD 350, another on LOD 400). The dispute crystallises around these deltas — A3-1 baseline each model element at LOD 400 and one at LOD 300 in a clash → which party owns the resolution?
3. **The LOD matrix is the entitlement firewall**: In a SCCA / DIAC arbitration, the contractor's entitlement to "rely on the model" depends on the LOD specification in the contract. Specifying LOD 300 for a slab-edge detail means the contractor can rebid the steel reinforcement, but cannot reject the slab geometry.
4. **LOD drift is the most common claim vector**: Designers typically release at LOD 200-300; the LOD Spec anticipates drift (LOD 350 between design and construction). Without a contractual drift protocol, the contractor absorbs the gap as variation. The LOD Spec provides the language for "we delivered at LOD 350, not LOD 400 as you claim."
5. **Saudi/GCC tender language misses the point**: KSA government tenders increasingly require "BIM Level 2" without specifying per-element LOD — the LOD Spec is the missing link. Practitioners preparing tender submissions should append a per-element LOD matrix (akin to §4 of the Specification) to discharge the obligation meaningfully.

## How to use this in a BIM-coordination playbook
When faced with a fabricated-from-model dispute, the first pleading paragraph should cite the LOD Spec definition and tabulate the contractual LOD for each model element at issue. The LOD Spec — together with the IFC file's underlying properties — provides the audit trail that determines who relied on what.

## Verification trail
- Tavily search query used: `BIM LOD Level of Development dispute FIDIC`
- Raw search saved at: `/tmp/tavily-research-bim/raw/search-04-bim-lod-level-of-development-dispute-fidic.json`
- Raw extract saved at: `/tmp/tavily-research-bim/raw/extract-15-bimforum-org-resource-lod-level-of-development-lod-specification.json`
- Direct quotes cross-checked against `raw_content` of that file (anchors "usability and the limitations of models", "Level of Development (LOD) Specification" both hit).
