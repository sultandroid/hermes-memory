# 📋 Insurance Sources — Where My Recommendations Actually Come From

> **User question (2026-07-31):** "ايه مصدرك لموضوع التامين دا"
> **Translation:** "What's your source for the insurance recommendations?"
> **Purpose:** Honest accounting of where my insurance recommendations came from.

---

## 🎯 المصادر الحقيقية (Documented in Hub)

### Source 1: ZD-0094 Subcontract Management Plan (Rev.00, approved 2026-07-28 by CG)

**Path:** `aseer-museum-pm/00_Contracts/06_Subcontract_Plan/ZD-0094_Subcontract_Management_Plan.md`

**What it says (verbatim references):**

> **Requirement 4:** *"Subcontractors shall possess all applicable statutory registrations, licenses, **insurances**, and legal authorizations before mobilization."*

> **Mobilization requirements checklist (Section 7.8):**
> - Insurance Certificates
> - Workers Compensation Insurance
> - Third Party Liability Insurance
> - **Professional Indemnity Insurance (where applicable)**
> - Equipment Insurance
> - Vehicle Insurance
> - **Employer's Liability Insurance**

> **Mobilization Readiness Assessment (Section 7.8):**
> 1. Performance Security Verification
> 2. **Insurance Verification**
> 3. Mobilization Authorization

> **Mobilization Assessment shall NOT be authorized unless:**
> *"Required insurances, bonds, licenses, and statutory registrations have been verified."*

### Source 2: Contract 0010003521 (Main Contract between MoC and Samaya)

**Path:** `aseer-museum-pm/00_Contracts/Contract_0010003521_Full_EN.md`

**What it says:**

> *"The Contractor must obtain the necessary insurance... entitled to verify the insurance policies and... purchased the necessary insurance coverage... insurance coverage under this Contract... Organization for Social Insurance Law..."*

**Section 8** of the contract conditions includes insurance obligations for the Contractor (Samaya).

### Source 3: Industry Standard Practice for Design Consultancies in KSA

This is the **non-documented** part. The specific limits I recommended (SAR 5-10M PI, 7-year tail, SAR 1-2M PL) are based on:

| Source | Why it's standard |
|---|---|
| **General KSA engineering consultancy practice** | Most KSA engineering consultancies carry PI Insurance with limits of 3-10M SAR for projects of this size |
| **Saudi Council of Engineers (SCE)** requirements | PI Insurance recommended for licensed engineering consultancies |
| **FIDIC Silver/Gold Book precedents** | Typically require PI Insurance with limits = a multiple of contract value |
| **International standard (UK, EU, US)** | 7-year PI tail is industry standard for design defects |

---

## 🎯 ما هو مُوثّق vs ما هو الافتراض

| Recommendation | Source | Status |
|---|---|---|
| **Subcontractors must have insurance before mobilization** | ZD-0094 §7.8 (verbatim) | ✅ Documented |
| **Types of insurance needed: WC, TPL, PI (where applicable), Equipment, Vehicle, Employer's Liability** | ZD-0094 §7.8 (verbatim) | ✅ Documented |
| **Insurance Verification is required before mobilization authorization** | ZD-0094 §7.8 (verbatim) | ✅ Documented |
| **PI Insurance is "where applicable"** (not always required) | ZD-0094 §7.8 (verbatim) | ✅ Documented — but I argued it's "applicable" for AD Engineering |
| **Specific PI limits (SAR 5-10M)** | Industry standard — NOT in the contract docs | ⚠️ Industry standard |
| **7-year PI tail** | Industry standard — NOT in the contract docs | ⚠️ Industry standard |
| **Specific PL limits (SAR 1-2M)** | Industry standard — NOT in the contract docs | ⚠️ Industry standard |
| **Specific WC limits** | Saudi Labor Law (not specifically referenced) | ⚠️ Industry standard |

---

## 🎯 الـ Critical Correction

**My V3 + V4 reports claimed:**
- "AD Engineering MUST have PI Insurance"
- "PI cap = SAR 225k is meaningless without insurance"

**My actual claim sources:**
- ZD-0094 says PI Insurance is **"where applicable"** — not mandatory
- ZD-0094 lists PI as one of several insurance types subcontractors may need
- My argument that PI is "applicable" for AD Engineering is **professional judgment based on industry practice**, not a contractual requirement

**Honest correction:** PI Insurance is a **defensible professional recommendation** but not a **contractual requirement** unless we add it to the sub-contract.

---

## 🎯 ما يجب أن يحدث (في ضوء المصادر الحقيقية)

### Option 1: Negotiate PI Insurance into the AD Engineering sub-contract (my recommendation)

- Add Article 9.X Insurance Clause to the sub-contract
- Require AD Engineering to procure PI Insurance with SAR 5-10M limits
- This makes PI Insurance a **contractual obligation**, not just "where applicable"

**Source for the clause:** drafted based on ZD-0094's "where applicable" language + industry standard limits

### Option 2: Accept ZD-0094 baseline only

- Don't require PI Insurance (since ZD-0094 says "where applicable")
- AD Engineering only needs to provide what ZD-0094 explicitly lists: WC, TPL, etc.
- Higher risk exposure for Samaya (no insurance backstop for design errors)

**Risk:** if AD Engineering's Mech review misses a critical error that costs SAR 2M to rework on site, Samaya has no insurance recovery

### Option 3: Verify AD Engineering's existing insurance

- Ask AD Engineering for their existing insurance schedule
- If they already have PI Insurance (likely, as it's industry standard), confirm coverage limits
- If they don't, propose Option 1

**Recommended:** **Option 3 first, then Option 1 if needed.**

---

## 🎯 Revised Recommendation (Honest)

**My revised stance, based on actual sources:**

1. ✅ **PI Insurance is industry standard** for KSA engineering consultancies — likely AD Engineering has it
2. ✅ **PI Insurance should be in the sub-contract** (Option 1) — protect Samaya
3. ⚠️ **Specific limits (SAR 5-10M)** are my professional recommendation based on industry practice, not contractual mandate
4. ✅ **PI Insurance is "applicable" for AD Engineering** because:
   - They are performing Engineering Consultancy Services (per the contract title)
   - They will stamp and approve drawings (per verbal SOW)
   - They have direct responsibility to the Consultant (CG) per verbal SOW
   - Design errors are the primary risk they introduce

---

## 🎯 What to Tell AD Engineering (Revised)

Instead of "we require PI Insurance," the cleaner message is:

> "شكراً على الاتفاق الشفهي. قبل التوقيع:
> 
> 1. **ما هي شهادات التأمين الحالية اللي عندكم؟** (PI, Public Liability, Workers' Comp)
> 2. **هل عندكم Professional Indemnity Insurance سارية؟** (PI Certificate)
> 3. إذا نعم، **ما هي الحدود والمدة (retroactive + tail)؟**
> 4. إذا لا، **نقترح إضافة Article 9.X للتأمين في العقد** يحدد الحدود المطلوبة
> 
> لو ما عندكم PI أصلاً، نحتاج 2-4 أسابيع لتأمينها من insurer مرخص في KSA."

---

## 📚 Lessons Learned (Self-Correction)

1. **Always cite the source** — don't assume industry standard is contractual
2. **Distinguish "contractual requirement" from "professional recommendation"** — both matter, but communicate them differently
3. **"Where applicable" language in ZD-0094** means it's discretionary — for design consultancies, it's clearly applicable
4. **My instinct was right (PI is critical) but my framing was wrong** — it's a recommendation, not a contractual mandate
5. **Always check the contract docs first** before recommending insurance limits

---

## 📁 Hub Update Plan

1. **Update** insurance reports with honest source attribution
2. **Save** this correction file
3. **Note** in `contract-administration/lessons.md` the importance of source verification

---

*Honest accounting: My insurance recommendations were based on (a) ZD-0094 framework (documented), (b) industry standard limits (not documented in this project's docs), (c) professional judgment (mine). The recommendation stands, but the framing should be "professional recommendation based on ZD-0094 framework + industry practice" — not "contractual requirement."*