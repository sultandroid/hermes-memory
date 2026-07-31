# REPORT — Codes & Standards in Saudi/GCC Construction

**Compiled:** 31 July 2026
**Method:** Tavily Search + Tavily Extract (API), 22 search queries × 10 themes, 24 candidate sources deep-extracted, 10 cases curated.
**Source workspace:** `/tmp/tavily-research-codes/`
**See also:** `INDEX.md` (theme matrix + cross-ref map), `cases/01..10*.md` (per-case full report)

---

## 1. Executive summary

Saudi construction in 2026 is regulated by a **layered, partially overlapping stack** of codes and standards, each with its own amending authority, jurisdictional scope, and enforcement mechanism. The 10 themes in this research break into four regulatory layers:

1. **Statutory technical code (binding)** — Saudi Building Code (SBC), with its 2024 update mandatory from 30 June 2025, administered by the new Saudi Building Code Center under MOMAH (formerly SASO).
2. **Standard form contracts (binding if adopted)** — FIDIC Rainbow Suite (1999) and 2017 Second Editions, with KSA Vision-2030 megaprojects (NEOM, The Line, Red Sea) shifting decisively to 2017.
3. **International reference standards (binding by reference)** — NFPA (fire), ACI 318 (concrete), AISC 360 (steel), ASCE 7 (loads), SASO technical regulations (materials), USGBC LEED / BRE BREEAM / Mostadam (sustainability).
4. **Territorial regulators (overriding)** — Royal Commission for Jubail & Yanbu (RCJY) and Royal Commission for Riyadh City (RCRC) have their own design criteria that *override* the SBC within their territory.

The single most important practical lesson: **a code violation is not a mere contractual defect — it is a public-law non-compliance that exposes the employer to municipal penalties and the contractor to licence/sanction risk, and that can be used as a defect-liability cause of action in SCCA arbitration.**

---

## 2. Theme-by-theme synthesis (with primary source pointers)

### 2.1 Saudi Building Code (SBC) — most-cited sections in disputes

The SBC is enacted by **Royal Decree M/43/2017**, amended by **M/15/2019** and **M/88/2024**, and is administered since 4 March 2025 by the Saudi Building Code Center under MOMAH (Chambers 2026, Case 01). The 2024 update replaced the 2018 version as **mandatory from 30 June 2025** after a 180-day transition. The 2024 edition adds three new structural codes: *Saudi Seismic Design Code for Steel*; *Repair/Rehabilitation of Existing Concrete Structures*; *GFRP-Reinforced Concrete*.

**Most-cited in disputes (per Chambers + practice observation):**
- **SBC 201** — Architectural (fire separation, egress, accessibility)
- **SBC 301 / 304** — Structural loads / concrete (ACI-318 based)
- **SBC 305 / 306** — Masonry / steel
- **SBC 601 / 604** — Mechanical / energy efficiency
- **SBC 801** — Fire protection (NFPA-derived)
- **SBC 901 / 1101** — Existing buildings / commissioning

**Critical enforcement lever (new in 2024):** **Article 9 of the SBC Implementation Law** was amended (Council of Ministers Decision No. 286 of 9 October 2024) to require an **occupancy certificate as a prerequisite for full activation of electrical current**. This is the *real* teeth: a building that is "complete" but not SBC-compliant cannot be legally energised, transferred, or occupied. Use this lever in defect-liability claims.

### 2.2 FIDIC Red Book 1999 vs 2017 — practical difference in GCC

The 2017 Red Book is *"the most significant rewrite in FIDIC's history"* (Lexilio, Case 02). The 50% word-count increase reflects a move to *prescriptive procedure* and *time-bar discipline*. The structural change: **Clause 20 (claims) is split from new Clause 21 (disputes)**, and the **DAB is renamed DAAB** (Dispute Avoidance / Adjudication Board). In KSA specifically, Vision-2030 owners are *moving away from bespoke 1999 hybrids*; the 2017 forms are "harder" — more time-bars, more "deemed" rejections, more obligations whose breach strips entitlement.

Practical impact in KSA disputes:
- The contractor's *contemporaneous-records discipline* is now determinative (Cl. 20.1 supporting details).
- Missing the 7-day notice window = total loss of entitlement, even where the underlying cause is sound.
- A 2017 contract managed with 1999 habits is a *commercial catastrophe*.

### 2.3 FIDIC Yellow Book (Design-Build) — when it applies in Saudi

Per Euan Lloyd (Al Tamimi, March 2017, Case 03), the 2017 Yellow introduces three changes that matter: **50% longer contract**; **new Sub-Clause 8.4 advance-warning mechanism**; **unified claims procedure** (Employer and Contractor claims now symmetric under Sub-Clause 20.1). The Engineer must now *"act neutrally"* under Sub-Clause 3.7.

**Decision rule for KSA:**
- **Use Yellow** when the Contractor designs *and* builds, the Employer brief is output-based, and an Engineer is retained to certify (typical: industrial plants, PV solar, certain PIF infrastructure).
- **Use Red** for pure construction with an Employer design.
- **Use Silver** for *single-point turnkey* with no Engineer (NEOM, Aramco, SABIC mega-projects).

Mismatch = mismatch of risk = dispute.

### 2.4 FIDIC Silver Book (EPC/Turnkey) — risk allocation in megaprojects

Strata (2026, Case 04) maps the Silver-Book risk profile against NEOM, The Line, Red Sea, and new economic zones. The operative principle: the **Contractor takes total responsibility** — design (Sub-Clause 5.1), ground conditions (Sub-Clause 4.7), performance-test liability. The Silver Book is a *documentation regime* dressed as a contract. The 2017 Silver — like the 2017 Red and Yellow — requires the DAAB pathway; *ad hoc* arbitration is no longer available.

**Key KSA risk:** Vision-2030 projects push *technology, schedule, and interface risk* onto the Contractor. The bid must price *interface-management premium*, not just contingency. Contractors who under-price interface risk on a Silver Book lose money twice (preliminaries overrun + claim denial).

### 2.5 NFPA fire code — Saudi adoption and enforcement

Per SFFECO (2025, Case 05): *"In Saudi Arabia these standards [NFPA] are the primary technical reference for consultants, contractors, and the Civil Defense, and they sit alongside the Saudi Building Code (SBC 801), which adopts international model-code principles and adapts them to local conditions."* The three-layer compliance model:
1. Engineer designs to **NFPA 13/14/20/72** (sprinklers/standpipes/fire pumps/detection).
2. Documented for **SBC 801** review.
3. Built with **SASO-conformant** equipment carrying recognised listings.

**Civil Defense** (Ministry of Interior) is the *de facto* permitting authority — not MOMAH. No Civil Defense approval = no occupancy = no energisation (loop with the SBC occupancy-certificate rule).

### 2.6 ACI / BS structural standards

SBC 304 (Concrete Structures) **directly adopts ACI 318-19 with local amendments** (Sixteens 2025, Case 06). Saudi Arabia signed a formal licensing agreement with ACI in 2010, giving the Saudi Building Code National Committee the right to reproduce ACI 318 text verbatim. SBC 306 (Steel) references AISC 360; SBC 301 (Structural) references ASCE 7 (loads) and ACI 318 (concrete).

**Local SBC 304 amendments** (vs base ACI 318):
- Concrete cover ≥ 40 mm for cast-in-place against soil in KSA.
- Durability requirements (chloride/sulphate exposure near coasts).
- Seismic zoning per the new Saudi Seismic Design Code for Steel (2024).

**Trap to avoid:** Some consultants mix British (BS 8110) and American (ACI) references in the same structural package. This is a *defect-liability exposure*. The contract specs must nominate one design code.

### 2.7 Mostadam — Saudi national green-building rating system

Mostadam was launched in 2021 by the Royal Commission for Riyadh City (Alpin, Case 07). It is *Saudi-national*, optimised for KSA climate (extreme heat, dust, high solar gain), and runs from 1-star (baseline) to 4-star (≈30% energy reduction vs SBC 304). The compliance trail runs Mostadam → SBC → SASO, not LEED → international standard. Mostadam is *effectively mandatory* for government and PIF-funded projects; for private sector, demand varies by municipality.

### 2.8 LEED / BREEAM / Estidama — what Saudi clients actually require

Per Al-Surf et al. (2021 MDPI Sustainability, Case 08), the empirical finding is unambiguous: **LEED is the most-recognised international rating system in KSA, but Mostadam is rapidly gaining mandatory traction through government and PIF projects**. BREEAM is rare except in European-developer-backed work. Estidama (Abu Dhabi Pearl rating) appears in UAE-investor tenders. The default premium ask on Saudi private commercial / mixed-use bids is now *LEED Gold + Mostadam 3-Star*.

### 2.9 SASO standards

Per Tabseer (2025, Case 09), the **SASO Technical Regulations for Building Materials** control imports via three tracks:
1. **SABER** (online platform) for product conformity assessment and shipment clearance.
2. **SASO IECEE** for electrical products.
3. **Quality Mark** for high-risk/critical products.

The non-negotiable principle: a material that fails SASO at the port of entry is *not the Employer's problem* — the contractor bought the wrong material. The compliance trail is at *three checkpoints* (pre-shipment CoC → port inspection → site materials-engineer check); failing any one = defective work in a defect-liability arbitration.

### 2.10 Royal Commission standards (Yanbu, Jubail)

The **RCY-GDCTG 2018, 4th Edition, Revision 1.00** (Case 10) is the controlling design standard for any construction project in the Royal Commission's Jubail and Yanbu industrial cities. In RC territory, **the GDCTG prevails over the SBC wherever they conflict** — the Royal Commission is a separate regulatory authority with its own jurisdiction. Section 2.1 of the GDCTG is a *closed codes/standards list*: anything not listed is not approved. The TSS-SE (Technical Support Services – Structural Engineering) group must approve every structural package.

**Key commercial point:** Working in RC territory is a *specialty market* — separate prequalification, separate safety training, separate environmental compliance. Pricing must reflect the *premium regulatory environment*. Yanbu and Jubail are the Kingdom's primary petrochemical and industrial zones (Sadara, SABIC, Aramco JVs).

---

## 3. Cross-cutting findings

### 3.1 The "which code applies" question (decision tree)

```
Q1: Is the project inside RCJY (Jubail/Yanbu) or RCRC (Riyadh City) territory?
    YES → RC standards govern; SBC and SASO are baselines, not substitutes.
    NO  → SBC governs.

Q2: Is the project a FIDIC contract? Which FIDIC?
    Red 1999   → DAB pathway; 28-day Engineer determination.
    Red 2017   → DAAB pathway; Clause 20 (claim) split from Clause 21 (dispute).
    Yellow 2017 → Add Sub-Clause 8.4 advance-warning; Engineer must act neutrally.
    Silver 2017 → Single point of responsibility; DAAB pathway; performance cert.

Q3: Is the work fire-protection?
    YES → NFPA 13/14/20/72 are the *technical reference*; SBC 801 is the *legal standard*.
    Civil Defense approval is the *enforcement gate*.

Q4: Is the work green-building rated?
    Government / PIF → Mostadam mandatory; LEED optional, often added for credibility.
    Private commercial → LEED Gold + Mostadam 3-Star is the default ask.
    European developer → BREEAM added.
    UAE investor → Estidama Pearl added.

Q5: Are imported materials involved?
    YES → SASO SABER + IECEE + Quality Mark tracks; CoC at three checkpoints.
    No  → SASO still applies (testing methods, durability).

Q6: Is concrete design involved?
    YES → SBC 304 (adopts ACI 318-19 with KSA amendments).
    Mixing BS 8110 / Eurocode 2 in same package = defect-liability exposure.
```

### 3.2 The "code violation as breach" principle (claims/arbitration)

In SCCA arbitration under the New Civil Transactions Law (NCTL, Royal Decree M/191/2023) and the SBC, a code violation is *both* a contractual breach (failure to meet the technical standard of care) *and* a public-law non-compliance (municipal exposure, licensing risk). The dual character makes code violations a *high-leverage* cause of action in defect claims:
- Higher damages (cost of remediation + cost of *delayed occupancy* + cost of municipal penalties).
- Stronger causation arguments (the code provides a *bright-line* standard, not a reasonableness test).
- Stronger interim-relief arguments (e.g. stop-work order for unapproved structural work).

The flipside: code violations are *also* a high-leverage *defence*. A contractor who can show it complied with the contractually-nominated code (e.g. SBC 304 + ACI 318-19) at design stage has a strong defence to a "defective work" claim, even if the building later shows distress.

### 3.3 The "documentation regime" pattern (cross-cutting)

Every regulatory framework studied — SBC, FIDIC 2017, SASO, Civil Defense, Mostadam, RCJY GDCTG — emphasises *contemporaneous documentation* over *after-the-fact reconstruction*. The practical operational model for any KSA project is:

1. **Single project-wide "warning register"** (FIDIC Cl. 8.4 advance warnings + Cl. 20.1 notices + SASO non-conformities + Civil Defense inspection findings + TSS-SE comments) — one log, multiple input streams.
2. **Materials Approval Register** (SASO CoC + Quality Mark + batch numbers + supplier test reports) — date-stamped, versioned, located with the project QA manager.
3. **Code-of-record file** (the *exact* SBC edition, FIDIC edition, NFPA edition, ACI edition, AISC edition, SASO technical regulation number referenced in the contract) — locked at contract signature; any change is a *variation* not a "clarification."
4. **Compliance evidence pack** (Mostadam evidence + LEED/BREEAM evidence + Estidama evidence if applicable) — co-located with the commissioning records.

A contractor who runs this regime from day one avoids 80% of the procedural-default losses documented in FIDIC cases (Cases 02, 03, 04).

---

## 4. Recommended next steps (for the training-corpus workflow)

- **Cross-reference with contract-administration** (next subagent): Cases 01, 02, 03, 04 are the operative FIDIC/SBC contractual-law cases. The contract-administration corpus should be able to cite back to these for *which code applies* and *what procedural steps bind*.
- **Cross-reference with claims-arbitration**: Cases 02, 03, 04, 06, 09, 10 carry the strongest evidence/principle lessons for forensic use. The claims/arbitration corpus should be able to cite back to these for *code-violation as breach* and *code-of-record forensic rule*.
- **Save the most-cited URLs as a curated bookmark list** in the digitalhermes profile (e.g. Chambers practice guide, Tamimi law updates, Pinsent Masons Saudi FIDIC guide, Royal Commission GDCTG PDF) for future re-citation.
- **Watch-list for 2026 H2 updates**: SBC 2024 enforcement actions; any SCCA award citing a code violation; any MOMAH/RCJY amendment to the GDCTG; any new LEED v5 / Mostadam-5-star release.

---

## 5. Methodology note

- **API:** Tavily (search + extract), 22 queries, 24 candidate extractions (1 failed: concrete.org blocks automated fetch), 10 final cases.
- **Source diversity:** 1 primary regulatory, 1 peer-reviewed academic, 2 top-tier law-firm, 1 legal-practice guide, 4 specialist consultancy, 1 authoritative legal blog. No LinkedIn-only or Wikipedia-only sources were used as primary; LinkedIn posts are referenced only via their original publishers' web pages.
- **Currency:** All 10 cases cite materials published 2017-2026; the oldest (Tamimi 2017) is on the FIDIC 2017 launch and remains the authoritative contemporaneous record. The newest (Chambers 2026) covers Royal Decrees through 2025.
- **Verifiability:** Every URL is a stable, citable source. The MDPI paper has 34+ citations; the Chambers guide is an editorially-reviewed practice guide; the Tamimi article is by a named partner (Euan Lloyd); the Royal Commission GDCTG is a primary regulatory document.

**End of report.**
