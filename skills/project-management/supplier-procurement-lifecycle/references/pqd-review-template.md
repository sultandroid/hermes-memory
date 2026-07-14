# PQD Review — Worked Example (Al Kalas International, Aseer Museum, 2026)

Reference worked example for the **Phase 3b-i: PQD Review (Received) — Gap-and-Red-Flag Triage** subsection of the `supplier-procurement-lifecycle` skill.

This file shows the full output of a real PQD review for a 288-page civil-materials-testing-lab PQD delivered for a museum-fitout procurement. Use it as a tone/structure/red-flag-catalog reference for any future PQD review.

---

## Context

- **Task:** "Extract and review the PQD for Smith from [WhatsApp tmp]/AKI PQD.pdf. Return a structured plain-text review (sections: Company Info, Experience, Technical, QA/QC, Red Flags, Recommendation)."
- **File delivered:** `AKI PQD.pdf` — 288 pages, 125 MB, PDF 1.7, created with PDF24 (Word-export).
- **Project context:** Aseer Regional Museum — supplier prequalification review (museum/heritage fit-out scope).
- **Mismatch signal:** user asked for "Smith" but the file is for "Al Kalas International" (a civil materials testing lab in Riyadh). Handled by flagging the mismatch at the top of the review, not by silent substitution.

## What the review produced

The full plain-text review (saved to `/tmp/aki_pqd_review.txt`) is reproduced below as the worked example. The structure follows the 6-section template from the skill, with the naming-mismatch banner at the top, the verdict at the end, and 10 numbered red flags in between.

```text
================================================================================
PQD REVIEW — Al Kalas International Company for Materials Testing
("AKI PQD.pdf", 288 pages, rev. 2026 edition)
Project: Aseer Regional Museum — Supplier Prequalification Review
================================================================================

NOTE ON FILING: Task referenced "PQD for Smith" but the file delivered is
"AKI PQD.pdf" — i.e. Al Kalas International, a civil materials testing
laboratory in Riyadh. "Smith" is not mentioned anywhere in the document.
A naming mismatch exists. Review below covers the file as delivered
(Al Kalas International = "AKI").

--------------------------------------------------------------------------------
COMPANY INFO
--------------------------------------------------------------------------------
- Legal name:           Alkalas International Company (LLC, one-person Co.)
- CR National Number:   7053490327
- CR issue date:        25/01/2026
- Status:               Active
- Address:              Building 8174, Wadi Al Hadaar St, Dahiyat Namar
                        Dist, Riyadh 14956, KSA (also 232 m² guideline
                        facility, Riyadh Region)
- VAT Reg No.:          314590438600003 (effective 01/02/2026)
- Civil Defense lic.:   1-002151048-47 (issued 1447/10/27H, valid 1 year)
- HRSD/MOL license:     24925245500
- Nitaqat band:         Platinum (38% Saudization) — verified 24/06/2026
- Monsha'et SME cert.:  26227334841 (valid 30/04/2026 – 30/04/2027)
- ISIC classification:  712034 — Construction & building-materials testing labs
- Listed scope (CR):    Material Testing, Geotechnical Investigation,
                        Equipment Calibration, General Contracting,
                        Equipment Supply, Manpower Supply
- Established:          Newly formed in Saudi Arabia in Jan 2026 (CR).
                        Key personnel all joined Al Kalas between Jan–Mar 2026.
                        No prior corporate history in KSA.
- Stated vision/scale:  27+ services, three depts (Admin, Lab, Geotechnical),
                        four lab sections (Soil, Aggregate, Asphalt, Concrete).
- Management (all Pakistani nationals, all newly appointed at AKI):
    Chairman          Muhammad Younus
    CEO               Basharat Ali         (Jan 2026 –)
    GM                Benyameen Yousaf     (Jan 2026 –)
    QA/QC Manager     Gohar Rehman         (Feb 2026 –)
    Tech. Manager     Muhammad Adeel Anjum (Mar 2026 –)
    Procurement Mgr.  Muhammad Yaqoob      (Jan 2026 –)
    Finance Manager   Ameer Hamza
    HR Manager        Munirah Hamdan Al-Shalawi
    Lab Supervisors   Muhammad Abubakar Yousuf (QMR), Mudassar Hameed
- Website:             www.alkalas.com

--------------------------------------------------------------------------------
EXPERIENCE
--------------------------------------------------------------------------------
- No project reference list, no client list, and no track-record table
  are included anywhere in the 288-page PQD. The "Client Approvals" and
  "Quality Manual" sections in the table of contents are placeholders
  with no content extracted.
- Pre-AKI work history of the proposed team is entirely from Pakistan
  (Rayat Al Najah Civil Lab, ZKB Builders, DESCON Engineering, ATECO KSA,
  Yasin Enterprises, Pioneer Associates, Geo Investigation Services,
  AJQ Enterprises, Bemsol). Only one prior KSA role: ATECO Lab Manager
  (Oct 2024 – Jan 2026) for Technical Manager.
- Project examples cited in CVs are water-supply pipelines, overhead
  water tanks, pile-load tests, geotech boreholes, and access roads.
- No museum, heritage, cultural, exhibition, display-case, AV,
  specialist-fitout, or conservation experience is mentioned anywhere.
  Zero relevance to Aseer Regional Museum scope.

--------------------------------------------------------------------------------
TECHNICAL CAPABILITIES (as offered)
--------------------------------------------------------------------------------
- 27+ services across Soil, Aggregate, Asphalt, and Concrete testing
  (sieve analysis, Atterberg, Proctor, SPT, CBR, UCS, direct/triaxial
  shear, consolidation, permeability, LA abrasion, ACV, AIV, soundness,
  Marshall, bitumen content/density/softening/penetration/viscosity,
  Marshall mix design, concrete compressive/flexural/slump/air-content/
  density, concrete mix design).
- Standards cited: ASTM, AASHTO, BS, SASO.
- Discipline coverage is 100% civil-materials QC; no specialist testing
  (microclimate, RH/T for showcases, lighting photometrics, vibration,
  display-case mock-ups, conservation materials, finishes).

--------------------------------------------------------------------------------
QA / QC & CERTIFICATION
--------------------------------------------------------------------------------
- ISO 9001:2015  (Cert AMER300282, valid 04/04/2026 – 03/04/2027;
  recert 03/04/2029). Scope covers material testing, geotech, equipment
  calibration, vendor/plant/quality inspection, general contracting,
  equipment & manpower supply.
- ISO 14001:2015  (Cert AMER300283, same issuer/validity).
- ISO 45001:2018  (Cert AMER300284, same issuer/validity).
- ISO/IEC 17025:2017  (Cert No. 18581, issued by American Quality System
  Registrars LLC, USAC-accredited. Valid 23/06/2026 – 22/06/2027, 3-year
  cycle. Scope: "Provision of Testing for Construction Materials and
  Geotechnical Investigations").
  -- Note: 17025 accreditation is brand new (first issue 23/06/2026),
     one year old at submission date.
  -- Issuing body is a US-based commercial registrar; not a Gulf/
     Saudi-signatory body (e.g. SASO, GAC, ENAS, or similar).
- Quality Manager (Gohar Rehman, 9 yrs exp.) holds ISO 9001 Lead Auditor
  certificate; "twice faced SAAC audits as Lab Supervisor" — that
  experience is at a previous employer, not Al Kalas.
- Calibration certificates, equipment list, and lab facility photos
  are referenced (sections at end of PDF) but were not extractable
  as text content from the PDF.

--------------------------------------------------------------------------------
RED FLAGS
--------------------------------------------------------------------------------
1.  Wrong supplier / wrong scope. Al Kalas is a civil materials testing
    lab; Aseer Museum scope is specialist fit-out / exhibition / AV /
    lighting / showcase / graphics. AKI's services are tangential at
    best (concrete and soil testing) and irrelevant to the main
    specialist packages. If the PQD was misrouted, this is a non-starter.
2.  Company is brand new in KSA. CR was issued 25/01/2026; all
    management joined in Jan–Mar 2026. Effectively zero operating
    history under this entity. No evidence of a single delivered
    project in Saudi Arabia.
3.  No project reference list. 288-page PQD contains no track record
    table, no client list, no contract values, no completion dates —
    a critical omission for any prequalification.
4.  No equipment list. PQD cites a 232 m² facility and 27+ services but
    does not list a single piece of test equipment with make/model/
    capacity, and no equipment count. Cannot verify capacity.
5.  17025 accreditation is freshly issued (June 2026) by a non-GCC
    accreditation body. Verify acceptance with the Consultant (CG).
    First surveillance audit has not yet occurred.
6.  ISO 9001/14001/45001 issued by "AMERI COQUALITYSTANDARDSREGISTECH
    PVT.LTD" (USA / India). Treat as commercial certifier; not an
    internationally top-tier accreditation. May be acceptable to CG
    but should be verified.
7.  Heavy Pakistani-national staffing (all named managers Pakistani);
    Saudization is 38% (Platinum band) but is achieved on a small
    total headcount — risk if scope requires larger mobilization.
8.  VAT, Nitaqat, Monsha'et certificates all < 6 months old. The
    company is operationally in start-up phase.
9.  Pre-AKI experience of all senior staff is in Pakistan; the only
    in-KSA work referenced is one individual at ATECO. No evidence
    of museum-grade, conservation-grade, or large-infrastructure
    testing in KSA.
10. PQD is a marketing-style company profile. It does not answer
    Aseer Museum PQD's standard prequalification schedule
    (typical sections: legal entity details, similar-project
    experience, key personnel CVs with project references,
    methodology, HSE, QA plan, financial standing, insurance,
    litigation history, current commitments, quality of
    equipment). Almost none of these are present in structured form.

--------------------------------------------------------------------------------
RECOMMENDATION
--------------------------------------------------------------------------------
NOT QUALIFIED for Aseer Regional Museum specialist packages.
The PQD is technically complete as a civil materials testing
laboratory profile but is materially non-compliant with the
museum/heritage/exhibition scope being procured.

Suggested actions:
 (a) Confirm the routing — if "Smith" was the intended PQD, the
     wrong file was supplied.
 (b) If the intent is to prequalify a third-party QC testing
     subcontractor for the museum's concrete/structural packages,
     AKI may be considered ONLY after the following are supplied:
     - Project reference list (≥ 3 KSA projects, last 5 yrs,
       with client, value, scope, dates, contactable referee).
     - Equipment list with make/model/capacity/quantity and
       current calibration certificates.
     - Confirmation that 17025 (Cert 18581) is acceptable to CG
       given the non-GCC issuing body.
     - Audited financials / bank reference.
     - Insurance certificates (Professional Indemnity + GL).
     - Litigation / dispute declaration.
     - HSE plan and Quality Plan specific to the museum scope.
 (c) If AKI is intended for the museum's specialist packages
     (AV, lighting, graphics, showcase, exhibit fitout), it is
     out of scope and should be rejected.

Tone: factual; no data invented. Where information is absent
from the PQD (project list, equipment list, financials), this
is noted as a gap rather than filled in.
================================================================================
```

## Pitfalls this example realised (lesson log)

These pitfalls all manifested in this session and are now captured in the skill's "Pitfalls" section. They are listed here in the order they were encountered.

1. **File-name / asked-name mismatch** (red flag #1) — user said "Smith", file is "AKI". Flagged at top, not silently substituted.
2. **Placeholder sections in TOC with no body content** — the PQD's TOC lists "Client Approvals", "Quality Manual", "Facilities & Lab Equipment", "Equipment Calibration Certificates" but the actual pages were either blank or image-only with no extractable text. Treated as a red flag ("PQD claims section X is included but extracted content is empty").
3. **No project reference list** (red flag #3) — 288-page PQD has zero project list. This is the single biggest red flag for any prequalification; the verdict is "Not Qualified" on this alone.
4. **No equipment list with make/model/capacity** (red flag #4) — vendor claims 27+ services and a 232 m² lab but lists no equipment. Capacity is unverifiable.
5. **Fresh ISO/IEC 17025 with no surveillance audit** (red flag #5) — first issue June 2026, surveillance not yet done. Required explicit verification step ("verify acceptance with CG").
6. **Non-GCC 17025 accreditor** (red flag #5/6) — "American Quality System Registrars" is US-based, not a Gulf/Saudi signatory (SASO, GAC, ENAS). GCC acceptance is uncertain.
7. **ISO 9001/14001/45001 from commercial certifier** (red flag #6) — "AMERI COQUALITYSTANDARDSREGISTECH PVT.LTD" is a US/India commercial certifier, not top-tier. Caveat applied.
8. **Heavy single-nationality management** (red flag #7) — all 5 named senior managers are Pakistani. Acceptable in principle but flagged.
9. **All certificates < 12 months old** (red flag #8) — VAT (01/02/2026), Nitaqat (24/06/2026), Monsha'et (30/04/2026), every cert under 6 months old. Company in start-up phase.
10. **Pre-supplier experience ≠ supplier experience** (red flag #9) — QA/QC Manager's 9 years at ZKB Builders / DESCON is at those companies, not at AKI. AKI gets zero credit for it.
11. **Wrong-scope mismatch** (red flag #1) — civil materials testing lab, not a museum-fitout specialist. Strongest reject signal; flagged first.

## What was intentionally NOT done

- **No OCR of the placeholder sections** — the "Equipment Calibration Certificates" and "Quality Manual" sections at the back of the PDF were image-only. We did not OCR them. We noted them as "embedded scans, not extractable as text" and recommended the user provide a text source.
- **No invented project list** — the PQD had no project list, so the review's "Experience" section says "No project reference list" rather than fabricating one. Hard rule.
- **No made-up equipment specs** — same reason for the "Technical" section.
- **No inflated verdict** — the verdict is "NOT QUALIFIED" for the museum's specialist scope, not "qualified with conditions". The scope mismatch is a deal-breaker, not a fixable gap.

## Reuse pattern

To replicate this style for any future PQD review:

1. Copy the template from the skill's Phase 3b-i Step 7.
2. Run the 7-step workflow (naming check → TOC map → 6 buckets extract → scope alignment → red-flag catalog → verdict → output).
3. Save the output to `/tmp/<supplier>_pqd_review.txt` and present the same content inline to the user.
4. Always flag naming mismatches at the top.
5. Always include the "Tone: factual; no data invented" closing line in the review file.
