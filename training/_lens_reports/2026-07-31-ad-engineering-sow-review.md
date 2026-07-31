# 🔍 SOW Review — Samaya ↔ AD Engineering Sub-Contract

> **Lens activated.** 31 July 2026. Focus: **Scope of Work (نطاق العمل)**
> **Priority:** HIGHEST — SOW ambiguities = variations = disputes = cost overruns

---

## 📌 الـ SOW Sources في هذا العقد

| المرجع | المحتوى |
|---|---|
| **Preamble** (P007-009) | "engineering design consultancy, design review, verification and endorsement services" |
| **Article 1** (P010-014) | Contract Documents + Scope of Services (the legal hierarchy) |
| **Article 2** (P015-019) | Obligations of Second Party (الاستشاري) |
| **Article 3** (P020-024) | Obligations of First Party (Samaya) |
| **Tables 0 + 1** | Mechanical + Electrical Disciplines — Target dates + activities |
| **Attachment No. 1** | Technical and Financial Proposal No. 7/2475/26/B.D dated 14 July 2026 (**NOT INCLUDED in this DOCX**) |
| **Table 2** | Payment schedule (Milestones) |

---

## 🔎 SOW Analysis — 9 Critical Questions

### **Q1: هل MEP معرّف بوضوح؟ — ⚠️ RISKY**

| Discipline | في العقد? | في Proposal? | واضح? |
|---|---|---|---|
| Mechanical | ✅ Table 0 | ⚠️ Unknown (not attached) | ⚠️ |
| Electrical | ✅ Table 1 | ⚠️ Unknown | ⚠️ |
| **Public Health (Plumbing)** | ❌ **NOT MENTIONED** | ⚠️ | ❌ |
| **Fire Protection / Sprinkler** | ❌ **NOT MENTIONED** | ⚠️ | ❌ |
| **ELV (Extra-Low Voltage)** | ❌ **NOT MENTIONED** | ⚠️ | ❌ |
| **BMS (Building Management System)** | ❌ **NOT MENTIONED** | ⚠️ | ❌ |
| **HVAC Controls** | ⚠️ Mechanical "validation" only | ⚠️ | ⚠️ |
| **Lifts / Elevators** | ❌ NOT MENTIONED | ⚠️ | ❌ |

**🚨 Critical finding:** The Tables mention only "mechanical validation" and "electrical design basis" — but the **scope of mechanical and electrical is undefined** in the contract body itself. We rely entirely on **Attachment No. 1 (the Proposal)** which is **NOT in this DOCX**.

**Risk:** If the Proposal says "MEP = Mechanical + Electrical + Plumbing" but the contract only says "mechanical + electrical", Samaya could be on the hook for plumbing scope later.

---

### **Q2: ما هو "design review, verification and endorsement"؟**

Preamble (P008): *"engineering design consultancy, **design review, verification and endorsement services**"*

This is the scope. Let me parse it:

| Service | Meaning | In contract? |
|---|---|---|
| **Design consultancy** | Creating the design from scratch | ✅ (Tables 0 + 1) |
| **Design review** | Reviewing existing designs (likely NRS's) | ⚠️ Not specified |
| **Verification** | Checking existing site conditions | ⚠️ "Existing conditions review" mentioned in Tables |
| **Endorsement** | Stamping/sealing the design | ⚠️ Art. 2 (P018) implies obligation to correct own errors |

**🚨 Risk:** "Design review" of NRS's work could mean AD Engineering is **stamping NRS's design** — making AD Engineering liable for NRS's work. Per `scope_summary.md`, NRS is the **Architect of Record** and **stamps = "design intent only" — no construction/coordination/dimensional liability**.

If AD Engineering endorses NRS's design, the **liability allocation becomes blurred**:
- NRS = design intent only
- AD Engineering = "endorsement"
- Samaya = absorbs all design risk under D&B

**Art. 9 (P067) cap = SAR 225k** for AD Engineering. If AD Engineering endorses NRS's MEP-relevant design and it fails on site, **who pays for the rework?** Likely Samaya, because both subs have limited liability.

---

### **Q3: هل التصميم Existing (تأهيل) أو New Build (بناء جديد)؟**

Per Aseer SOW (from the broader repo):
- **Rehabilitation and interior fit-out of an existing 2015 museum facility** (existing structure)
- Survey existing MEP systems + design upgrades

Contract Art. 4 (P027): *"commencing from the latest of the date of signature... receipt of the approved detailed assessment report for **all the existing MEP systems**, approved scope of work clearly defined and clouded on the drawings..."*

Tables 0 + 1: *"**Existing conditions review** & audit (as-builts, existing lighting, controls)"* — but for AD Engineering specifically: *"confirmation of existing conditions... mechanical design basis, gap analysis, specialist information collection"*

**🚨 Risk:** This is **existing-condition design**, which is harder than new build because:
- As-built drawings may not match reality
- Hidden defects (per Main Contract §2 Art. 9 latent defects)
- Coordination with existing live systems

**Art. 4 (P028)** excludes delays due to "inaccurate or incomplete information" — but **who bears the cost of inaccurate existing-condition data?** Not specified.

---

### **Q4: ما هي حدود الموقع / عدد الزيارات؟**

| Item | في العقد? |
|---|---|
| Site visits in scope | ⚠️ Tables mention "site visits" as activity |
| **Number of site visits** | ❌ NOT SPECIFIED |
| Site visit duration | ❌ NOT SPECIFIED |
| Travel reimbursement | ✅ Art. 3 (P024) — "approved travel, accommodation and transportation expenses for site visits" |

**🚨 Risk:** "Site visits" is mentioned as an activity but with **no cap**. AD Engineering could bill unlimited site visits at AD Engineering's "prevailing professional rates" (Art. 7, P058).

---

### **Q5: Authority submissions — من المسؤول؟**

| Authority | Type | AD Engineering scope? |
|---|---|---|
| Civil Defense (الدفاع المدني) | Permit | ❌ NOT MENTIONED |
| Saudi Building Code compliance | Design | ✅ Art. 2 (P017) — "applicable Saudi Building Code" |
| Municipality (البلدية) | Permit | ❌ NOT MENTIONED |
| Royal Commission | NOC | ❌ NOT MENTIONED |
| Power utility (SEC) | NOC | ❌ NOT MENTIONED |

Art. 3 (P024): *"The First Party shall... bear authority, permit, utility and submission fees"*

Art. 2 (P019): *"Technical support to authorities, the project manager or the reviewing entity shall be limited to matters within the agreed Services and shall not constitute a guarantee of approval."*

**🚨 Risk:** AD Engineering will provide "technical support" but **does NOT guarantee authority approval**. If Civil Defense rejects the design, **Samaya bears the consequences** (delay, rework) but AD Engineering has no liability.

---

### **Q6: هل التصميم يغطي فقط DD→IFC أم أيضاً Tender Docs؟**

Tables 0 + 1 final milestone: *"100% Final IFC: Finalization of the design, **specifications, BOQ, BIM models, IFC documentation, final QA/QC, coordination, clash detection, closure of all comments, and issuance of the Final IFC Package for approval.**"*

✅ BOQ included
✅ Specifications included
✅ BIM models included
✅ Clash detection included
✅ Tender Package = "90% Tender Package" mentioned (Mechanical R3C1 / Electrical R2C1)

**Question:** Does "Tender Package" mean AD Engineering produces the **Tender Documents** for the contractor procurement (i.e., the docs the tenderers bid on)?

Or is it just the **Tender Design** (technical specs) without the procurement docs (forms, schedules, conditions)?

**🚨 Risk: ambiguity.** If AD Engineering produces only technical design and Samaya must produce procurement docs separately, that's **a scope gap** that will surface during tendering.

---

### **Q7: Coordination with NRS / Studio ZNA / Glasbau Hahn**

| Specialist | Coordination needed? | In contract? |
|---|---|---|
| **NRS** (Architect) | ✅ Critical (architectural interfaces) | ⚠️ Art. 3 (P023) — "coordinate the Second Party with the architect" — but no obligation on AD Engineering |
| **Studio ZNA** (Lighting) | ✅ Critical (lighting-electrical interface) | ❌ NOT MENTIONED |
| **Glasbau Hahn** (Showcases) | ✅ Critical (showcase-electrical interface) | ❌ NOT MENTIONED |
| **Rawasin** (AV/IT) | ✅ Critical (AV power + data) | ❌ NOT MENTIONED |
| **Nama Consulting** (Fire & Life Safety) | ✅ Critical (FLS design interfaces) | ❌ NOT MENTIONED |

Art. 3 (P023): *"The First Party shall... coordinate the Second Party with the architect, structural consultant, contractor, project manager, reviewing entity, museum consultant and all specialist designers involved in the Project."*

**🚨 Risk:** **Coordination is Samaya's obligation, not AD Engineering's.** Samaya must serve as the hub for all design coordination. If a clash is discovered on site, AD Engineering can argue "you didn't coordinate with Studio ZNA's lighting layout to my electrical layout".

**The contract has no inter-specialist coordination meetings schedule, no BIM coordination protocol, no clash-detection cadence.**

---

### **Q8: Variations — what's in vs out of scope?**

Art. 7 (P056) lists what constitutes a variation:

> *"Variations shall include changes to approved designs, **additional disciplines or deliverables**, additional meetings or site visits, **repeated review cycles**, acceleration, changes in regulations after commencement, **or additional work arising from the acts or delays of other Project participants**."*

**🚨 Critical: "additional disciplines or deliverables"** — if the scope expands (e.g., AD Engineering needs to add plumbing after start), that's a **variation** with additional fees. But the contract is silent on whether such expansion requires written notice + new scope.

**🚨 Critical: "additional work arising from the acts or delays of other Project participants"** — this is broad. If Studio ZNA is late on lighting, and that delays AD Engineering's electrical design, **AD Engineering can claim variation fees** for the resulting delay.

This clause **protects AD Engineering** more than Samaya. Samaya should consider whether to **cap variation fees** or **exclude some categories**.

---

### **Q9: هل التصميم للتشغيل (Operation) مشمول؟**

| Phase | In scope? |
|---|---|
| Concept Design | ❌ NOT IN THIS CONTRACT (was NRS's job) |
| Schematic Design (SD) | ❌ |
| Detailed Design (DD) | ✅ Tables — 50% DD submission |
| Tender Design | ✅ Tables — 90% Tender Package |
| IFC (Issued for Construction) | ✅ Tables — 100% Final IFC |
| Construction Administration / Site Visits | ⚠️ Art. 2 (P017) implies coordination |
| **Commissioning** | ❌ NOT MENTIONED |
| **As-Built Drawings** | ❌ NOT MENTIONED |
| **Operation & Maintenance manuals** | ❌ NOT MENTIONED |
| **Defects Liability Period** | ❌ NOT MENTIONED |

**🚨 Critical gap: No commissioning scope.** Mechanical + Electrical systems typically require commissioning by the designer (or specialist commissioning agent). **If AD Engineering doesn't commission, who does?**

Art. 2 (P019) explicitly excludes: *"construction methods, temporary works, site safety, contractor workmanship, procurement, specialist designs prepared by others, **final construction quantities, or unauthorized alteration or reuse of its Deliverables**"*

**"Final construction quantities" — is this contractor's responsibility? Or AD Engineering's?** Reading it literally, AD Engineering is NOT responsible for construction quantities. **But who produces the as-built BOQ?**

This is a **scope gap** that will cause problems during construction.

---

## 📊 SOW Risk Matrix

| # | SOW Risk | Likelihood | Impact | Severity |
|---|---|---|---|---|
| 1 | Plumbing / Public Health not in scope (gap) | HIGH | HIGH | **CRITICAL** |
| 2 | Fire Protection design not in scope (gap) | HIGH | HIGH | **CRITICAL** |
| 3 | BMS / ELV design not in scope (gap) | MEDIUM | MEDIUM | **HIGH** |
| 4 | "Endorsement" of NRS design unclear | MEDIUM | HIGH | **HIGH** |
| 5 | Existing-condition design risk (latent defects) | HIGH | MEDIUM | **HIGH** |
| 6 | Site visits uncapped | MEDIUM | LOW | **MEDIUM** |
| 7 | Authority submissions (CD, Municipality) unclear | HIGH | HIGH | **CRITICAL** |
| 8 | Tender Package scope (technical only or full?) | MEDIUM | MEDIUM | **MEDIUM** |
| 9 | Coordination with other specialists — Samaya's burden | HIGH | HIGH | **CRITICAL** |
| 10 | Variations "additional disciplines" — open-ended | MEDIUM | HIGH | **HIGH** |
| 11 | Commissioning / As-Built / O&M not in scope | HIGH | HIGH | **CRITICAL** |
| 12 | Schedule misalignment with Main Contract (15/10 vs 30/09) | HIGH | HIGH | **CRITICAL** |

---

## 🎯 الـ SOW Gaps في ترتيب الأولويات

### 🔴 CRITICAL (5 gaps):

| # | Gap | Suggested addition |
|---|---|---|
| 1 | **Plumbing / Public Health** not in scope | Add: *"Public Health (plumbing, drainage, water supply) design is included in the Mechanical Discipline scope"* OR explicitly EXCLUDE if not AD Engineering's |
| 2 | **Fire Protection / Sprinkler** not in scope | Add: *"Fire Protection (sprinkler, suppression) design is included in the Mechanical Discipline"* OR exclude and assign to specialist |
| 3 | **Authority submissions** unclear | Add: *"AD Engineering shall prepare and submit all Civil Defense, Municipality, and utility NOC applications for Mechanical and Electrical scope, including coordination meetings and resubmissions until approval. Approval is not guaranteed."* |
| 4 | **Coordination with NRS / Studio ZNA / Glasbau Hahn** not in scope | Add: *"AD Engineering shall attend weekly BIM coordination meetings; provide interface drawings (MEP-to-architecture, MEP-to-lighting, MEP-to-showcase power); resolve clashes in own discipline."* |
| 5 | **Commissioning / As-Built / O&M manuals** not in scope | Add: *"AD Engineering shall provide: (a) Commissioning specifications for all Mechanical and Electrical systems; (b) As-Built drawing mark-ups based on contractor's red-lines; (c) O&M manuals draft within 30 days of Final IFC acceptance."* |

### 🟡 HIGH (4 gaps):

| # | Gap | Suggested addition |
|---|---|---|
| 6 | **"Endorsement" of NRS design** unclear | Add: *"AD Engineering's 'endorsement' applies only to Mechanical and Electrical elements within its scope. AD Engineering does not endorse architectural, structural, lighting, or showcase designs."* |
| 7 | **Existing-condition design risk** unallocated | Add: *"AD Engineering's scope includes verification of existing MEP systems based on documentation provided by the First Party. AD Engineering is not liable for discrepancies between documented and actual existing conditions unless such discrepancies are reasonably discoverable from the documentation provided."* |
| 8 | **Variations "additional disciplines"** open-ended | Cap variations: *"Variations for 'additional disciplines or deliverables' shall not exceed [20%] of the Contract Price without separate written agreement."* |
| 9 | **BMS / ELV** not in scope | Add: *"Building Management System (BMS) design is included in the Electrical Discipline scope as relates to MEP integration only. Standalone BMS architecture / programming is excluded."* |

### 🟢 MEDIUM (3 gaps):

| # | Gap | Suggested addition |
|---|---|---|
| 10 | **Site visits uncapped** | Add: *"Site visits shall be limited to [X] visits per discipline. Additional site visits require First Party's written approval and shall be treated as variations under Art. 7."* |
| 11 | **Tender Package scope** ambiguous | Add: *"The 'Tender Package' refers to Technical Tender Documents (specifications, BOQ, drawings). Administrative Tender Documents (forms, schedules, conditions of tender) are the First Party's responsibility."* |
| 12 | **"Final construction quantities"** excluded | Clarify: *"Final construction quantities shall be measured by the Contractor and verified by the Quantity Surveyor. AD Engineering shall provide design quantities (BOQ) as a basis, not as a guaranteed final quantity."* |

---

## 🟥 الـ Schedule Misalignment — Critical SOW Issue

**Compare these dates:**

| Milestone | AD Engineering | Aseer Main Contract | Gap |
|---|---|---|---|
| Mobilization | 1 Aug 2026 | Already started 01/12/2025 | OK |
| 50% DD (Mech) | 9 Aug 2026 | — | TBD |
| 50% DD (Elec) | 5 Sep 2026 | — | TBD |
| Material Approval (Mech) | 30 Aug 2026 | — | TBD |
| Material Approval (Elec) | 30 Sep 2026 | — | TBD |
| 90% IFC | 1 Oct 2026 | — | TBD |
| **100% Final IFC** | **15 Oct 2026** | **Termination date 30 Sep 2026** | **15 days late** |
| Construction / Procurement | (needs 100% IFC) | Already running | **Conflicting** |

**🚨 Critical problem:** AD Engineering finishes MEP design **15 days AFTER** Aseer's main contract Termination due-to-default date. **This means:**
- Construction cannot start MEP installation until 16 Oct 2026 (15 days after Aseer deadline)
- Even with EOT_008 (7 months, to 11 May 2027), the design is the bottleneck

**The SOW has a scheduling conflict with the Main Contract timeline.** AD Engineering's NTP and duration need to be **compressed** OR **parallel-tracked** to deliver by 30 September 2026.

**Required SOW amendment:**
> *"The Second Party shall use commercially reasonable efforts to deliver the 100% Final IFC Package by 30 September 2026. The Notice to Proceed shall specify a detailed schedule reflecting this target. The Second Party shall mobilize additional resources as needed to meet this date."*

---

## 💡 SOW Quality Score

| Criterion | Score | Comment |
|---|---|---|
| **Scope definition (MEP)** | 4/10 | "Mechanical + Electrical" only — Plumbing, Fire, BMS not addressed |
| **Services clarity** (Design / Review / Verify / Endorse) | 5/10 | Preamble lists 4 services but body only describes "design" |
| **Deliverables** | 6/10 | 4 milestones, but no detailed deliverable list |
| **Exclusions** | 7/10 | Art. 2 (P019) lists 7 exclusions (good) |
| **Coordination** | 2/10 | Samaya bears all coordination burden |
| **Authority submissions** | 3/10 | AD Engineering "supports" but doesn't "submit" |
| **Commissioning / As-Built / O&M** | 1/10 | Not mentioned at all |
| **Schedule alignment with Main Contract** | 2/10 | 15-day misalignment |
| **Variations** | 6/10 | Defined but broad; no cap |
| **Insurance / PI / LDs** | 2/10 | Cap = Contract Price (useless); no LDs |
| **TOTAL SOW QUALITY** | **38/100** | **POOR — Multiple critical gaps** |

---

## 🎯 الـ 5 SOW Risks اللي لازم تتصحح قبل التوقيع

| # | الـ SOW Risk | الحل |
|---|---|---|
| 🔴 **1** | **Plumbing / Fire / BMS not addressed** | Add explicit scope statement + exclusions OR assign to other specialists |
| 🔴 **2** | **Schedule misalignment** (15/10 vs 30/09) | Compression of duration OR acceleration clause |
| 🔴 **3** | **Authority submissions unclear** | Define AD Engineering's role + obligations |
| 🔴 **4** | **No commissioning / as-built / O&M** | Add post-IFC services |
| 🔴 **5** | **Coordination is Samaya's burden** | Make AD Engineering share coordination obligation with weekly BIM meetings |

---

## 📋 الـ SOW "Must-Add" قبل التوقيع

```
SCHEDULE A — DETAILED SCOPE OF SERVICES

A.1 Inclusions (MEP scope):
  (a) Mechanical Design Basis Report (MDBR)
  (b) HVAC load calculations
  (c) Ductwork and piping layout drawings
  (d) Equipment schedules and specifications
  (e) Public Health (plumbing, drainage, water supply) — [INCLUDED / EXCLUDED]
  (f) Fire Protection (sprinkler, suppression) — [INCLUDED / EXCLUDED]
  (g) BMS integration design — [INCLUDED / EXCLUDED]

A.2 Electrical:
  (a) Electrical load calculations
  (b) Single-line diagrams
  (c) Lighting layout (if separate from Studio ZNA)
  (d) Power distribution layout
  (e) ELV systems (data, telecom, fire alarm interface) — [INCLUDED / EXCLUDED]

A.3 Coordination:
  (a) Weekly BIM coordination meetings with NRS, Studio ZNA, Glasbau Hahn
  (b) Clash detection (own discipline)
  (c) Interface drawings to other disciplines

A.4 Deliverables (post-IFC):
  (a) Commissioning specifications
  (b) As-Built mark-ups (within 30 days of contractor red-lines)
  (c) O&M manuals draft (within 30 days of Final IFC)

A.5 Authority submissions:
  (a) Civil Defense application + coordination
  (b) Municipality application + coordination
  (c) Utility NOC applications (SEC, water, telecom)

A.6 Existing-condition scope:
  (a) Verification based on documentation provided
  (b) Site visits (capped at [X] visits per discipline)
  (c) Survey and gap analysis

A.7 Schedule:
  (a) NTP: [DATE]
  (b) 50% DD: [DATE]
  (c) 90% IFC: [DATE]
  (d) **100% Final IFC: 30 SEPTEMBER 2026 (not 15 Oct)**
```

---

## 📚 Lessons to Save (5 SOW-specific)

1. **"MEP" must be defined explicitly** — Mechanical + Electrical + Plumbing + (sometimes) Fire + BMS. **Don't assume.**
2. **"Endorsement" / "Review" / "Verification"** are 3 different services with 3 different liability profiles
3. **Existing-condition design ≠ new build** — latent defects, as-built discrepancies, hidden coordination issues
4. **Sub-contract schedule must align with Main Contract** — not the other way around
5. **Coordination is shared obligation** — Samaya can't be the hub for all specialist coordination; each sub must engage

---

## ⏰ Recommended Next Steps

| # | الإجراء | الموعد |
|---|---|---|
| 1 | **Get the Proposal** (Attachment No. 1 — Tech + Financial Proposal 7/2475/26/B.D) | **Today** |
| 2 | **Verify with Samaya's QS** ما هي MEP disciplines المطلوبة لـ Aseer (Mech + Elec + Plumbing + Fire + BMS?) | **This week** |
| 3 | **Compare with NRS SOW** — ما هو اللي NRS مسؤول عنه في MEP-related scopes؟ | **This week** |
| 4 | **Coordinate with Studio ZNA** — هل Studio ZNA بتـ design lighting circuits ولا AD Engineering؟ | **This week** |
| 5 | **Coordinate with Nama Consulting (FLS)** — هل Nama بتـ design fire protection؟ | **This week** |
| 6 | **Schedule acceleration proposal** — هل AD Engineering يقدر يضغط الجدول لـ 30/09؟ | **This week** |
| 7 | **DO NOT SIGN** بدون Schedule A (detailed scope) + SOW verification | **Until done** |

---

## 📁 Hub Save Plan

- Save lens report to: `training/_lens_reports/2026-07-31-ad-engineering-sow-review.md`
- Save 5 SOW lessons to: `training/contract-administration/lessons.md`
- Save Schedule A template to: `training/contract-administration/templates/subcontract-detailed-sow-template.md`
- Update Aseer P219 V3.1 Lens 9 with SOW gaps noted
- Commit + push

---

**النتيجة:** الـ SOW فيه **12 risk** و **5 critical gaps** و **schedule misalignment**. **العقد في شكله الحالي **غير قابل للتوقيع**.** يلزم Schedule A مفصّل قبل أي توقيع.