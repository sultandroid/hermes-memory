# MA-0006 Showcase Resubmission — Worked Example

> Aseer Regional Museum · Glasbau Hahn · Showcases Materials
> CG Rejection Code C (15-Apr-2026) → Resubmission Prep (13-Jul-2026)

## The Problem

CG rejected MA-0006 Rev.00 (Showcases Materials by Glasbau Hahn) with Code C. Key complaints:
1. Materials don't comply with specs
2. Anti-reflective glass non-compliant
3. Must follow SI-007 (3D render → material board → IFC)
4. Brass must be patinated
5. **Provide 3 alternative suppliers**

## The Discovery

The Glasbau Hahn reply was **not in the project submittal folder** — it was sitting in Outlook since April 2026.

### Finding supplier replies in Outlook

```sql
-- Search by submittal ref
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
       m.Message_SenderList, m.Message_NormalizedSubject, m.Message_HasAttachment
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%MA-0006%'
ORDER BY m.Message_TimeReceived;
```

Three emails found:
- 21-Apr: Ahmed Salah → Glasbau Hahn (forwarded CG rejection)
- 22-Apr: Ahmed Metwally (Glasbau Hahn) → Ahmed Salah (Guardian Clarity datasheet)
- 29-Apr: Ahmed Metwally → All (formal comments reply sheet)

### Extracting attachments

```bash
osascript -e "
tell application \"Microsoft Outlook\"
    set theMsg to message id <ID>
    set atts to (every attachment of theMsg)
    repeat with att in atts
        set savePath to \"/tmp/\" & (name of att)
        do shell script \"touch \" & quoted form of savePath
        save att in (POSIX file savePath as alias)
    end repeat
end tell
"
```

## The Argument

Glasbau Hahn's 29-Apr-2026 reply sheet + Guardian Clarity datasheet proved:
- Guardian Clarity Neutral: Tvis > 97%, Rvis < 1% — museum grade
- All materials match finishes schedule Material IDs
- Patinated brass samples submitted per FI_ME_01
- Alternative powder-coated metal per NRS recommendation

**CG's "3 alternative suppliers" demand was based on the initial non-compliant submission.** Since technical compliance is now proven, request CG to accept single supplier with technical justification.

## Support Folder Structure

```
09_Submittals/MA-NNNN_Rev01_Support/
├── 01_CG_Rejection_Code_C/           CG rejection letter
├── 02_Supplier_Technical_Reply/      Supplier's comments reply sheet
├── 03_Manufacturer_Datasheet/         Manufacturer's technical datasheet
├── 04_Supporting_Data_Sheets/        All material data sheets (flat, no subdirs)
├── 05_PQ_Approval/                   Original prequalification approval
├── 06_Sample_Board/                  Sample board photo
├── 07_Related_Submittal_Support/     Cross-referenced material support
├── 08_Email_Thread/                  Full email chain (outside support folder for CG)
└── 09_Resubmission_Checklist/        CR Sheet + checklist (outside support folder for CG)
```

## CR Sheet Structure

| # | CG Comment | Reference | Response | Supporting Doc | Status | Remarks |
|---|-----------|-----------|----------|---------------|--------|---------|
| 1 | Materials don't comply | Rejection letter | Supplier reply + 14 data sheets | 02_Supplier_Reply/ + 04_Data_Sheets/ | CLOSED | All materials match finishes schedule |
| 2 | AR glass non-compliant | Rejection letter | Guardian Clarity meets FI_GL_04 spec | 03_Guardian_Datasheet/ | CLOSED | Tvis > 97%, Rvis < 1% |
| 3 | Comply with SI-007 | Rejection letter | NRS approved drawings 19-Jun | 08_Email_Thread/ | CLOSED | SI closed 27-Apr |
| 4 | Brass patinated | Rejection letter | Separate submittal MA-0007 | 07_MA_0007_Support/ | PARTIAL | Look & feel request sent to CG |
| 5 | 3 alternative suppliers | Rejection action | Request single-source acceptance | 02_Supplier_Reply/ + 05_PQ_Approval/ | OPEN | Awaiting CG decision |

## Look & Feel Approval Strategy

When supplier test reports/certifications take time (supplier lead time), but the visual sample is ready:

1. **Request CG to approve LOOK AND FEEL now** — visual appearance, colour, texture
2. Test reports & certifications to follow once received from supplier
3. Alternative samples from local suppliers in parallel
4. Submit outstanding docs as Rev.01 addendum within 30 days

## Separate Submittal Principle

**Do not block one submittal because a related submittal is pending.** Example:
- MA-0006 (showcase materials: glass, silicone, fabric, Corian, lighting, powder coating) — independent of brass
- MA-0007 (patinated brass) — separate submittal, separate rejection
- MA-0006 Rev.01 can proceed without MA-0007 approval

## Key Lessons

1. **Check Outlook first** — supplier replies often sit in email, not the project folder
2. **Extract attachments** — the supplier's reply sheet + manufacturer datasheet are the two key documents
3. **Build the argument** — "3 suppliers" was based on initial non-compliance; technical proof changes the negotiation
4. **Separate submittals** — don't let one Code C block another
5. **Look & feel first** — visual approval can proceed while technical docs catch up
6. **CR Sheet goes to CG** — email thread + checklist stay outside the support folder for direct sending

## GBH Letter 002 — Supplier Advises Against Own Material (Extended Pattern)

When the supplier's formal letter states they do NOT recommend the specified material, this changes the response strategy:

### What GBH Letter 002 contained
- No existing Oddy test reports/certificates available for patinated brass
- Will submit sample for independent Oddy testing in Germany — results expected end of August
- **GBH does NOT recommend patinated brass** for 5 reasons: single-source supply (1 supplier globally), unguaranteed chemical patination results, colour consistency impossible, cross-batch matching difficult, time-consuming manual process
- GBH explicitly requested that patinated brass approval NOT hold shop drawing approval

### How this changed the CR Sheet response

| Before GBH Letter 002 | After GBH Letter 002 |
|----------------------|----------------------|
| "Test reports in progress with supplier" | "GBH confirms NO existing Oddy certs. Supplier advises against this material." |
| "Alternative PVD-coated sample in parallel" | "PVD-coated alternative is the RECOMMENDED path forward, not a fallback." |
| "CG's 2 alternative manufacturers request — working on it" | "Only 1 global supplier exists for patinated brass. 2 alternatives for the SAME material is not feasible. Proposing PVD-coated alternatives instead." |
| "Look & feel approval now, test reports to follow" | Same, but with supplier's own letter as supporting evidence |

### CR Sheet update pattern for GBH Letter 002

1. **Item 4 (Brass finish):** Append "UPDATE 16-Jul-2026: GBH Letter 002 received. [summary of key points]"
2. **Item 5 (MA-0007 strategy):** Replace the "working on it" response with a REVISED PROPOSAL that:
   - States the single-source reality
   - Proposes PVD-coated KSA alternative as primary path
   - References risk PRR-PRC-05 (Score 12, Critical)
3. **New Item 11 (CG 13-Jul request):** Insert a new row addressing Mansour's request for 2 alternative manufacturers, referencing GBH Letter 002 as the source confirming single-source
4. **Status change:** "REQUESTED - awaiting CG reply" → "REVISED - awaiting CG direction"

### Risk register cross-reference

The patinated brass risk was already registered as PRR-PRC-05 (Score 12, Critical) in the Master Risk Register. The CR Sheet should reference this to show the risk is tracked and being managed.

## Canonical File Locations (verified 2026-07-14)

**The same MA-0006 PDF is filed in 10+ locations.** When searching, the **canonical register** is `~/aseer-museum-pm/01_Registers/material_submittal_register.md` (row 24 = MA-0006, status C). The **canonical support package** is:

```
/Users/mohamedessa/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/24_Subcontractors/05_Showcases_Contractor/09_Submittals/MA-0006_Rev01_Support/
```

Sub-folder numbering (1..7) maps to a stable pattern — do NOT rename:
- `01_CG_Rejection_Code_C/` — Rev.00 rejection letter (only `*_Rev00_CG_Rejection.pdf` lives here; Rev.01 itself does NOT exist yet as a PDF)
- `02_Glasbau_Hahn_Technical_Reply/` — supplier's 29-Apr-2026 comments reply
- `03_Guardian_Clarity_Datasheet/` — anti-reflective glass manufacturer datasheet
- `04_Supporting_Data_Sheets/` — 14 manufacturer datasheets FLAT (no subdirs)
- `05_PQ_0063_Approval/` — prequalification Code B approval
- `06_Sample_Board/` — sample board photo
- `07_MA_0007_Brass_Support/` — EDEN patination + CuZn37 brass spec (cross-link to MA-0007)

**Two artefacts must stay in sync:**
- `09_Submittals/MA-0006_Rev01_CR_Sheet.xlsx` — 10-row CR sheet for CG (also duplicated to `06_Correspondence/20260713_MA-0006_Rev01_CR_Sheet.xlsx`)
- `09_Submittals/09_Resubmission_Checklist/MA-0006_Rev01_Checklist.md` — internal checklist of items prepared vs items still needed

**Parallel bank — Adel Darwish's archive** at `~/OneDrive - SAMAYA INVESTMENT/Adel  Darwish's files - 01- Execution Documents/08- Material Submittal MA/Architectural/06 -MOC-MUS-ASE-1A0-MA-0006/` contains the same material with an `Approval/` subfolder and a Form-MS xlsx. Cross-check Adel's bank against the canonical support folder when discrepancy is suspected.

**Other locations where the MA-0006 PDF is also parked** (search these if the canonical is missing): `04_Docs/03_Submittals/`, `04_Docs/03_Submittals/03.3_Material_Submittals/15_Showcases_Conservation/01_NRS_Specs/`, `12_Procurment/General/08_Exhibition_FitOut_Contractor/QA_Oddy_Testing/05_Returned_Submittals/`, `16_Email_Archive/_attachments/`, `23_Scripts/output/attachments_staging/MA-0006/`, `24_Subcontractors/08_Exhibition_FitOut_Contractor/QA_Oddy_Testing/05_Returned_Submittals/`.

## Full 10-Comment CR Sheet Structure

The 5-comment pattern (above) covers only CG rejection items. The **real** CR sheet for MA-0006 Rev.01 has 10 items because PQ-0063 conditions are treated as additional comments:

| # | Source | Comment Theme | Typical Status |
|---|--------|---------------|----------------|
| 1-3 | CG Rejection Letter (15-Apr) | Materials non-compliance, AR glass, SI-007 | CLOSED via supplier reply + datasheets |
| 4-5 | CG Rejection Letter | Patinated brass (→ MA-0007), 3 alternative suppliers | PARTIAL / OPEN (negotiate single-source) |
| 6 | MA-0007 Code C (02-Jul) | Test reports, certifications, 2 alternatives for brass | REQUESTED — awaiting CG reply on Look & Feel |
| 7 | PQ-0063 Condition #1 | Conservation test certificates (Oddy 14-day, ALL internal materials) | OPEN — 21-day extension requested |
| 8 | PQ-0063 Condition #2 | HVAC/electrical/humidity integration shop drawings | OPEN — 14-day extension, needs AD Engineering |
| 9 | PQ-0063 Condition #5 | Full-scale on-site mock-up prior to bulk supply | OPEN — commitment made (Type 3 Al Muftaha, 5200x1000x978) |
| 10 | PQ-0063 Condition #6 | Permanent on-site technical team from Glasbau Hahn | OPEN — post-approval (Glasbau Hahn confirmed) |

**Key insight:** items 7-10 come from the **PQ-0063 prequalification approval** (Code B, 03-Mar-2026), not from the CG rejection letter. They were carried forward as conditions that the original Rev.00 MA submission never fully closed. The CR sheet must list them as separate items, not bundle them under a generic "fulfil PQ conditions" line.

**Cross-discipline blocker:** Item 8 (HVAC/elec/humidity shop drawings) depends on **AD Engineering** as the MEP designer. Track this as a separate dependency in the RIBA Stage 4 deliverable tree — it is the longest-tail item on the Rev.01 critical path.

## Rev.01 Status (as of 2026-07-13)

- **Rev.01 has NOT been issued to CG** as a PDF
- CR sheet + checklist are dated 2026-07-13 — submission is staged, not sent
- The 6 OPEN items (items 4 partial + 6, 7, 8, 9, 10) need either (a) closure before issue, or (b) cover-letter commitment to close post-approval
- **Critical-path risk:** the 169-row procurement Excel (`ASM_Material_Procurement_Schedule_ARCH.xlsx`) lists 13 showcase lines all submittal-rejected under MA-0006 with delivery target 2027-12-03 — 14 months AFTER the 30-Sep-2026 contract handover. MA-0006 Rev.01 must be issued + approved fast or it becomes the showcase installation's binding constraint.

## First Submission Baseline (MA-0006 Rev.00)

The first submission already had all technical data sheets complete. The resubmission is about responding to CG's open conditions, not adding missing TDS.

| Material | Data Sheet Submitted |
|----------|-------------------|
| Silicone sealant | Dow Corning 993 TDS |
| Silicone sealant | EGO TDS |
| Brass (patinated) | CuZn37 spec + EDEN Patination |
| Silicone gasket | BSP Sipro 60 Shore A |
| Corian | Corian Spec Data |
| Fabric | Hallingdal 65 (Kvadrat) specs |
| Glass (AR) | Guardian Clarity 55.4 |
| Glass back paint | Peter Lacke datasheet |
| Glass hood motor-pump | Ergoswiss Pumps |
| Lighting | ATTO-S spec + Atto |
| Powder coating | Akzonobel + IGP 591T PARKOUR |
| Labels/samples | GBH Labels_Sample_2 |
| + sample board PDF | |

**CG closed items 1-3** (materials compliance, glass, SI-007) — those were accepted.

**What's still open from CG (Rev.00 rejection):**
- Item 6: 3 alternative suppliers (for glass/Guardian)
- Item 7: Conservation/Oddy test certificates
- Item 8: Shop drawings HVAC/electrical/humidity
- Item 9: Full-scale mock-up
- Item 10: On-site GBH team

**What's new in Rev.01 resubmission:**
- The **CR Sheet** addressing all CG comments
- The **split strategy** — brass finish separated to Track B so materials + shop drawings can proceed
- No new data sheets needed — all 14 materials were already complete and accepted
