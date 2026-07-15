# SOW Writing Tone & Technical Depth — User Corrections

This file records two user corrections from the Rigging SOW generation (July 2026) that any future SOW generation must avoid.

## Correction 1: "why no details"

First SOW had only 5 scope items, generic descriptions, no technical standards with code numbers, no material tier tables, no ITP hold points, no RACI evidence from Appendix A.

**Minimum table sizes enforced by user:**
- Included scope: 11 items (SOW-01 to SOW-11)
- Technical standards: 11 codes (SBC 301, AISC 360, ACI 318, ASCE 7, ASTM E488, BS EN 13155, ASTM B117, ASTM G82, AWS D1.1, SBC 801, SBC 201)
- Material tiers: 6 materials x 3 tiers (Tier A/B/C) + 10 banned items with reasons
- Interface matrix: 9 coordination partners
- Deliverables: 11 items with doc codes (RG-001 to RG-010)
- RACI: 11 activities x 6 parties
- ITP hold points: 8 (HP-01 to HP-08)
- Programme: 8 milestones
- Preferred manufacturers: 11 suppliers

## Correction 2: "write like humman engineer"

First SOW used corporate third-person language. User wanted plain engineer-to-engineer tone.

**What changed between v1 (rejected) and v3 (accepted):**

| v1 Corporate Style | v3 Engineer Style |
|---|---|
| "The Specialist Rigging Contractor is responsible for the engineering, supply, installation, inspection, and certification of..." | "You design, supply, install, test, and certify... In plain language: you design, supply, and install every structural fixing..." |
| "Rigging design coordination, load paths, fixing strategy" | "Design coordination: work out load paths and fixing strategy with the structural engineer" |
| "Seismic restraints per SBC 301" | "Seismic restraints: design and install bracing per SBC 301. Every suspended light and speaker needs seismic tie-downs. Get calcs reviewed." |
| "Interface Matrix" | "Who you coordinate with" |
| "ITP Hold Points" | Hold point table with notes like "Plan your programme accordingly." |
| "Banned Materials" | Plain list with reasons: "Zinc-plated steel inside showcases — causes galvanic corrosion and metal migration." |
| "Included Scope" | "What the Rigging Contractor Does" |
| "Exclusions" | "What You Don't Do" |
| "Open Items Before Issue" | "Stuff We Still Need to Sort Out" |

**Formatting rules from this session:**
- Use SamayaDoc template, not raw python-docx (user said "fix format follow samaya doc format")
- Header/footer via create_header/create_footer
- H1 uppercase navy, H2 numbered navy, H3 dark gray
- Table headers navy #0F172A, alternating rows #F8FAFC
- Symbol cleanup mandatory (smart quotes, em-dashes, accented chars)
- All stakeholder names proper: Samaya Investment, Ministry of Culture (MoC), Consultancy Group (CG), ACE Moharram-Bakhoum (PMC), Nissen Richards Studio (NRS)
