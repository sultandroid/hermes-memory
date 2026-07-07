# Design Schedule Compression Strategy

## When to Use

The planner's design schedule duration exceeds the contract-allowable design window. You need to compress the schedule without violating contract terms.

## Strategy Components

### 1. Single Combined Design Phase (ER §2.4)

ER §2.4 states: *"For expediency, the design phase for this D&B contract shall be combined into a single Design Development & Construction Documentation phase."*

This eliminates the structural separation between DD and CD phases that some planners assume, saving 2-3 weeks.

### 2. Direct-to-IFC Mechanism (ER §2.4)

ER §2.4: *"The Contractor may consider some elements of the design to be able to proceed straight to IFC stage."*

Application: Classify all design elements into two tracks:
- **Direct-to-IFC** — code-governed commodities, BOH items, like-for-like replacements
- **Staged Route** — exhibition design items needing aesthetic/conservation review

Classification scheme:
| Class | Definition | Example | Review Saved |
|-------|-----------|---------|:-----------:|
| A | Fully defined in Stage 3 | Standard finishes from Pre-Appt design | 2 reviews (50%+90%) |
| B | Code-governed commodity | Fire sealant, EMT, gypsum board | 2 reviews |
| C | Like-for-like replacement | FCU same duty/size | 2 reviews |
| D | Auxiliary/BOH outside SI-007 | Plant room doors | 2 reviews |

### 3. Rolling Wave Decomposition

Split staged-route packages into two waves to avoid an unrealistic single handover:

| Wave | Packages | Rationale |
|------|----------|-----------|
| **Early** | Graphics, Lighting, FF&E, Acoustics, CITC | Lower coordination dependency, fewer interfaces |
| **Late** | Showcases, Scenography, AV, Gallery Finishes | Need mock-ups, material board approval, more CG interaction |

### 4. External Dependency Tracking

Some packages depend on external tracks outside the design schedule. These MUST be shown as parallel external arrows with EOT trigger tags, not internal activities:

- SI-CG-ASEER-007 Material Board (gallery finishes)
- Civil Defense approval (FLS, Stramp, fire pump)
- Municipality approval (Stramp, external works)
- MoC content delivery (AV software, object labels, mounts)
- Glasbau Hahn showcase shop drawings

### 5. Continuous BIM Clash Run

ER §2.4.B certification requires "reviewed and approved by a suitably qualified, experienced and registered engineer." This implies a clash-free federated model. Schedule a continuous BIM coordination task across W1-W9 (not just a single milestone) to ensure the certification is defensible.

## Typical 10-Week Design Schedule

| Week | Direct-to-IFC Track | Staged Route Track |
|:----:|:-------------------:|:-----------------:|
| 1 | Submit element list to CG for approval | Start 50% design |
| 2 | Await CG list approval | Continue 50% design |
| 3 | Prepare IFC packages for 32 elements | Submit 50% for CG review |
| 4-5 | CG conformance review (14 cd) | CG 50% review |
| 6 | NOC → procure direct elements | Incorporate CG comments → develop IFC |
| 7 | — | Submit IFC (early wave) |
| 8-9 | — | CG IFC review + submit IFC (late wave) |
| 10 | — | NOC on all packages |

## Requirements for Success

| # | Requirement | Owner | Deadline |
|---|-------------|-------|----------|
| 1 | CG approves Direct-to-IFC element list | CG | W2 |
| 2 | FLS Strategy NOC obtained | CG/Authorities | W2 |
| 3 | All 32 elements IFC-ready (drawings + certs + material submittals) | Tech Office | W3 |
| 4 | BIM model clash-free and certified per ER §2.4.B | BIM Unit | W3 |
| 5 | NRS delivers 50% design on time | NRS | W3 |
| 6 | CG adheres to 14 calendar day review cycle | CG | Ongoing |
| 7 | SI-007 resolved or ring-fenced — gallery finishes progression not blocked | CG | W4 |

## Fallback If CG Rejects Direct-to-IFC

If CG rejects the list (in full or >5 elements): immediately register EOT, rebaseline to a full staged route, and submit each package individually under ER §2.4 rather than as a consolidated list. The list approach is for convenience; the right to Direct-to-IFC per element exists in ER §2.4 regardless.
