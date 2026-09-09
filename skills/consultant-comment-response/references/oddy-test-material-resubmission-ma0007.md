# Oddy-Test Material Resubmission — MA-0007 Patinated Brass (Aseer Museum)

## Context
- Submittal: **MOC-MUS-ASE-1A0-MA-0007** — Patinated Brass, by Glasbau Hahn (GBH)
- Status: Code C (Revise & Resubmit), 02-Jul-2026, reviewer Mansour Alrezeni
- Contract: Aseer Regional Museum 0010003521 (lump-sum D&B)
- Supporting refs: GBH Letter 002 (16-Jul-2026), PRR-PRC-05 (Critical risk), SI-008

## CRITICAL: Material manufacturer vs fabricator (the #1 recurring correction)
**The patinated brass MATERIAL is manufactured by Eden-Design GmbH (Iserlohn, Germany) — EDEN BRONZE™, a solid brass (CuZn) base chemically bronzed and patinated. Glasbau Hahn (GBH) is ONLY the approved showcase FABRICATOR (PQ-0063, Code B), not the material manufacturer.**

This split drives EVERY cert attribution. When CG asks for a material-level document, the issuer is **Eden-Design**, NOT Glasbau Hahn:
- **MSDS** (patination chemicals) → Eden-Design
- **VOC test** (from the lacquer/coating) → Eden-Design
- **Off-gassing** → Eden-Design
- **Fire-rated report** → Eden-Design (brass is non-combustible; cert "for the record" only)
- **Chemical composition** (CuZn37/C27200) → KME datasheet (the brass substrate supplier)

GBH is only named for **showcase fabrication**. Do NOT write "to be issued by Glasbau Hahn" for any material cert — the user corrects this every time. The earlier reference file wrongly said "all GBH lead-time" and "manufacturer (PQ-0063 Code B, single source)" — both wrong; GBH is the fabricator, Eden-Design is the manufacturer.

## The decisive blocker: Oddy test (museum-grade material compatibility)
The main Code C driver was the missing **Oddy test**. It came back **PASS**:
- Report **T2607222**, NonaChem GmbH (Ladenburg, Germany), on behalf of Glasbau Hahn, dated **21-Aug-2026**
- Method: DIN EN 60068-2-2:2008-05, 60 °C, 28 days, ~100% RH
- Sample: Patinated brass, double determination (1-1, 1-2), 18 coupons tested
- Result: **P (Permanent)** on all three coupons — Ag (sulphur), Cu (chlorides/oxides), Pb (organic acids); blank value clean

A passed Oddy test is the **strongest single piece of evidence** to flip a museum-material MAR from Code C toward B/A.

## Compliance vs pending status (template for the CRS)

| Category | Items | Status |
|---|---|---|
| **COMPLIED** | NRS comments/docs · all applications · manufacturer (Eden-Design) · **Oddy test PASS** | ✅ green |
| **PENDING** | VOC · off-gassing · chemical composition · fire-rated report · MSDS | ⏳ amber — Eden-Design lead-time |
| **PARTIAL** | 2 alternatives: Option A (IGP 591T PARKOUR powder coat, per NRS) submitted; Option B (PVD, KSA) in development | ⚠️ amber |

## The split-track strategy (recurring, reusable)
When a finish/material test timeline would otherwise hold up fabrication:
1. **Split approval into two independent tracks:**
   - **Track A** — shop drawings + showcase materials (MA-0006), unaffected by finish → approve independently
   - **Track B** — the finish/material itself (MA-0007), test in progress → separate
2. Frame the passed test as the decisive fix; **request Rev.01 approval (Code B/A) now**; remaining certs follow as **Rev.02 addendum** — don't hold the whole package on Eden-Design lead-time.
3. Specified finish is **not substituted** — the 2 alternatives are presented as *supplementary options for CG reference* (per NRS recommendation + local supplier development), not replacements.

## Applications that must be addressed (not just showcases)
Per the Code C comment "address all applications", pull the FULL finishes-schedule brass items, not only showcase elements:
- **FI_ME_01** — walls, main gallery doors, door reveals, setworks (display units/frames, AV), reception desk — 2mm patinated brass, patinated + lacquered, dark patination
- **FI_ME_03** — floorbox trims — brushed metal, patinated brass
- **FI_GR_11** — wayfinding signage — 2mm patinated brass, CNC cut
- **FI_ST_03** — reception feature wall — limestone with patinated brass detailing, fine brush hammered/patinated

Source: approved Finishes Schedule `6930` (Rev A, 21/02/25). Supplier per schedule = "TBC Locally Sourced"; GBH is the approved specialist.

## Control-sample framing (the user's preferred angle for the alternatives comment)
When CG asks for "2 alternative samples", the user's preferred framing is that the specified material is the **control sample** because the project has not yet submitted one for that raw material. This turns the alternatives request into a reference exercise, not a substitution threat:
- State: "The patinated brass finish (Eden-Design GmbH) is proposed as the **control sample** for this material, as no control sample has yet been submitted for this raw material on the project."
- Then list the alternatives as **supplementary reference choices only, not a substitution** of the control sample.

## Supplier sample bank (build it up — it strengthens the reply)
The user accumulates physical samples from multiple sources for the same material/finish. List them all in the reply as "available for reference" — it shows supply security + price competition + local support:
- **Patinated brass** — Eden-Design (Germany) = control sample; Chinese supplier (same spec); local KSA supplier (same spec); same finish on **Stainless Steel 304** from a Chinese supplier (may suit certain applications)
- **Anodised aluminium** — Alutecta (Germany) via Glasbau Hahn, 4 finishes (Antic 6, Antic brushed, E6 C33 brushed, E6 C34 brushed); Chinese supplier; local KSA supplier
- **Option A** — IGP 591T PARKOUR dark bronze powder coating (data sheet attached; previously submitted with MA-0006, 15-Apr-2026, per NRS recommendation RFI-008/TQ-0016)
- **Option B** — PVD-coated brass finish (sample under development, ~30 days)

## Reply style: bullet points, humanized (user preference)
For the alternatives/comment replies the user wants **bullet points, not paragraphs**, and **humanized** natural engineer voice. Structure:
- Short intro line ("Noted. Here's where we stand on the patinated brass material:")
- Grouped bullets under bold sub-headers (Control sample / Patinated brass samples / Anodised aluminium sample / Supplementary options)
- Each bullet one fact, no template phrasing, no inflated counts
- Close with the "not a substitution" line

## Oddy clause references (for citations)
- **ER §6.11** — exhibition spaces, non-deleterious to objects
- **SoW §13.29** — non-pre-approved materials only
(These are the correct clause anchors for Oddy compliance replies — see the 0e pitfall in SKILL.md; do not cite ER §2.4.)

## CRS generation notes
- For an MA-type material submittal CRS, the compliance matrix (CG comment → response → evidence → status COMPLIED/PENDING/PARTIAL + colour) is more useful than the designer-vs-contractor staging table used for plan reviews.
- Brand colours: navy `1F3864` header / white text, gold `D8A600` accents, green `E2EFDA` = COMPLIED, amber `FFF2CC` = PENDING/PARTIAL.
- Status labels as plain text: COMPLIED / PENDING / PARTIAL. No emoji, no AI fingerprints (see SKILL.md CRITICAL rules).
