# 🚨 AD Engineering Sub-Contract — Insurance Status: CRITICAL

> **User statement (2026-07-31):** "ايه موضوع التامين دا مفيش اتفاق معاهم علي موضوع التامين"
> **Translation:** "What about insurance? There's NO agreement with them on insurance."
> **Impact:** This is a CATASTROPHIC gap that overrides all other SOW considerations.

---

## 🛑 ما يعنيه "مفيش اتفاق تأمين"

### State of Insurance Today (Default)

| Insurance type | Status | Risk |
|---|---|---|
| **Professional Indemnity (PI)** | ❌ **NO agreement** | AD Engineering has NO contractual obligation to maintain PI |
| **Public Liability** | ❌ **NO agreement** | AD Engineering has NO obligation to maintain PL |
| **Workers' Compensation** | ❌ **NO agreement** | AD Engineering's staff injury = potential Samaya liability |
| **Design errors & omissions coverage** | ❌ **NO agreement** | If AD Engineering's design fails → no insurance recovery |
| **Cyber / Data** | ❌ **NO agreement** | BIM files / project data breach — uncovered |

**What this means in practice:**

The contract as drafted (v1) says **nothing about insurance**. Art. 9 limits AD Engineering's liability to SAR 225,000, but:

1. **No insurance backs that liability** — even if a court awards SAR 225k against AD Engineering, **there's no insurance company to pay it**
2. **AD Engineering is a small Co. (per Proposal No. 7/2475/26/B.D)** — may not have the cash to cover a SAR 225k judgment
3. **For losses > SAR 225k** — Samaya bears 100% with **no recovery** from AD Engineering
4. **For design errors** discovered on site after construction — **no insurance coverage at all**
5. **For staff injury** during site visits — **no Workers' Comp** = potential lawsuits against Samaya

---

## 📊 Risk Re-Calibration (Post-User-Statement)

### Original V1 Review Risk Levels

| Risk | V1 Score | Updated Score | Reason |
|---|---|---|---|
| PI Insurance | HIGH | **CRITICAL** | User confirms: no agreement |
| LDs | HIGH | **CRITICAL** | Combined with no PI = no recovery path |
| Schedule misalignment | CRITICAL | **CRITICAL** | Unchanged |
| Authority submissions | CRITICAL | **CRITICAL** | Unchanged |
| Coordination burden | CRITICAL | **CRITICAL** | Unchanged |
| Set-off mechanism | HIGH | **HIGH** | Unchanged |
| Verbal SOW gaps | (new) | **CRITICAL** | Unchanged |

**Net: The sub-contract in current form is UNINSURABLE and UNENFORCEABLE in practice.**

---

## 🎯 What "مفيش اتفاق تأمين" Means Practically

### Samaya's Risk Exposure Today

| Scenario | Likely outcome | Samaya's exposure |
|---|---|---|
| AD Engineering makes a Mech design error → MEP rework costs SAR 500k | AD Engineering liable up to SAR 225k (Art. 9) but **no insurance to back it** | Samaya absorbs SAR 275k+ |
| AD Engineering's Mech review of Samaya-drafted drawings misses an error → SAR 2M rework | AD Engineering denies liability (says it's Samaya's drawing error); no insurance mediation | **Samaya absorbs SAR 2M** |
| AD Engineering's Electrical design causes a fire (insurance claim) | AD Engineering liable up to SAR 225k but **AD Engineering may be insolvent** | Samaya = liable to MoC + insurance claim |
| AD Engineering staff injured during site visit | AD Engineering has NO Workers' Comp | **Samaya may be vicariously liable** |
| Civil Defense rejects design due to AD Engineering error | AD Engineering "supports" but no approval guarantee (Art. 2 P019); no insurance | Samaya bears rework + delay |

### Aggregate Worst Case

If AD Engineering's Mech/Elec design has a critical error that:
- Costs SAR 5M to rework on site
- Triggers SAR 1M Main Contract penalty cascade
- Causes SAR 500k in litigation
- **Total: SAR 6.5M exposure for Samaya**

With insurance: Samaya pays SAR 225k (AD Engineering's cap) + insurance absorbs the rest = Net SAR 225k exposure
**Without insurance: Samaya pays the full SAR 6.5M (or whatever judgment)**

---

## 💡 What AD Engineering's Insurance Should Look Like (Industry Standard)

For a **SAR 225k design contract on a SAR 74.9M museum project**, AD Engineering should typically carry:

| Insurance type | Standard minimum | Why |
|---|---|---|
| **Professional Indemnity (PI)** | **SAR 5-10M** per claim / aggregate | Covers design errors that cause property damage or economic loss |
| **PI Period** | **7 years** after completion | Latent defects can emerge years later |
| **Public Liability** | **SAR 2-5M** per occurrence | Covers third-party injury / property damage |
| **Workers' Compensation** | Per Saudi Labor Law | Covers AD Engineering's staff injury on site |
| **Cyber Liability** | **SAR 500k-1M** | Covers data breach / BIM file loss |

**PI is the critical one.** Without PI, **the entire sub-contract is exposed.**

---

## 📋 Required Actions — Insurance Negotiations

### Option A: AD Engineering procures PI Insurance (PREFERRED)

| Step | Action | Owner |
|---|---|---|
| 1 | AD Engineering obtains PI Insurance quote from KSA-licensed insurer | AD Engineering |
| 2 | Samaya reviews PI terms: scope, limits, exclusions, retroactive date | Samaya Legal + Insurance broker |
| 3 | PI Certificate delivered to Samaya before NTP | AD Engineering |
| 4 | PI maintained for project duration + 7 years after | AD Engineering |

**Cost:** PI premium for a consultancy of this size is typically **1-3% of contract value** = SAR 2,250-6,750. **Negligible.**

**Timeline:** PI typically takes 2-4 weeks to procure for a new project.

### Option B: Samaya procures PI Insurance and adds AD Engineering as insured

| Step | Action | Owner |
|---|---|---|
| 1 | Samaya's insurance broker adds AD Engineering to project PI policy | Samaya Insurance |
| 2 | AD Engineering's scope is covered under Samaya's master PI | — |
| 3 | AD Engineering pays proportionate premium (or Samaya absorbs) | TBD |

**Pros:** Faster, controlled
**Cons:** Samaya bears insurance admin; AD Engineering may not have direct incentive to maintain quality

### Option C: Insurance is NOT procured — TERMINATE the verbal agreement

If AD Engineering refuses to procure PI:
- The verbal agreement should be **immediately terminated**
- Samaya should **pursue alternative MEP designers** (e.g., extend ITC contract, or find another qualified consultancy)
- Document the termination properly to avoid any "we had an agreement" claim

**This is the hard option but it's the only responsible one** if PI can't be secured.

---

## 🔄 Impact on Verbal SOW (Re-Analyzed)

| Verbal SOW item | Insurance impact |
|---|---|
| **Mech: Samaya drafts, AD Engineering reviews + approves** | PI must cover AD Engineering's review/stamping liability on Samaya-drafted drawings |
| **Elec: AD Engineering full responsibility** | PI must cover AD Engineering's design + production |
| **Shop Drawing Reviews (NEW)** | PI must cover construction-phase review liability |
| **IFC 100% Approval** | PI must cover approval decisions on Mech (from Samaya drafts) + Elec (from AD Engineering) |

**All 7 verbal SOW items require PI coverage.**

---

## 📝 Insurance Clause — Must-Add to Contract

```
ARTICLE 9.X — INSURANCE

X.1 The Second Party shall, at its own cost, procure and maintain throughout
    the duration of this Agreement and for a period of seven (7) years after
    Final IFC acceptance, the following insurances with insurers licensed
    in the Kingdom of Saudi Arabia:

    (a) Professional Indemnity Insurance with a limit of not less than
        SAR [5,000,000] per claim and in aggregate, covering design
        errors, omissions, and professional negligence arising from the
        Services performed under this Agreement;

    (b) Public Liability Insurance with a limit of not less than
        SAR [2,000,000] per occurrence;

    (c) Workers' Compensation Insurance covering all personnel of the
        Second Party in compliance with Saudi Labor Law;

    (d) [Cyber Liability Insurance with a limit of SAR [500,000] — optional]

X.2 The Second Party shall deliver to the First Party a Certificate of
    Insurance evidencing the above coverages before the commencement of
    Services (Notice to Proceed).

X.3 The Second Party shall provide evidence of renewal of each policy
    not less than thirty (30) days before expiry.

X.4 The Professional Indemnity Insurance shall:
    (a) Cover all Services performed under this Agreement, including
        but not limited to design production, design review and stamping
        of drawings prepared by the First Party, IFC approval, and
        Shop Drawing Reviews during construction;
    (b) Have a retroactive date not later than the date of this Agreement;
    (c) Cover claims made during the seven (7) year period after
        Final IFC acceptance.

X.5 The First Party shall be named as an additional insured under
    the Public Liability policy.

X.6 Failure to maintain the required insurances shall constitute a
    material breach of this Agreement, entitling the First Party to
    suspend Services and/or terminate under Art. 10.
```

---

## 🎯 Updated Next Steps

| # | Action | Deadline | Owner |
|---|---|---|---|
| 🔴 1 | **STOP** any verbal commitment to AD Engineering | **Today** | Sultan |
| 🔴 2 | **Demand PI Insurance proof** from AD Engineering | **This week** | Sultan |
| 🔴 3 | **If PI available**: Schedule A + Insurance clause inserted → Sign | **Within 2 weeks** | Sultan + Legal |
| 🔴 4 | **If PI NOT available**: Terminate verbal agreement, find alternative | **This week** | Sultan |
| 🔴 5 | **Verify** AD Engineering's VAT registration + tax compliance | **This week** | Finance |
| 🔴 6 | **Cross-check** with Samaya's insurance broker — does the project policy cover sub-consultants automatically? | **This week** | Insurance |
| 🔴 7 | **Document** the verbal SOW in writing (this lens report) and circulate to AD Engineering for confirmation | **Today** | Sultan |

---

## 💬 What to Tell AD Engineering Today

> "شكراً على الـ verbal agreement. قبل ما نوقّع الـ contract، نطلب منكم:
> 1. **شهادة PI Insurance** سارية (SAR 5M / 7 سنوات)
> 2. **شهادة Public Liability** (SAR 2M)
> 3. **Workers' Compensation** per Saudi Labor Law
> 
> لو الأرقام دي مش متاحة، خلونا نتناقش البديل (Samaya تضيفكم على الـ project policy) أو نأجل التوقيع لحد ما تتوفروا.
> 
> **بدون PI Insurance، Samaya مش هتقدر توقّع.**

---

## 📚 Lessons to Save (Insurance gap)

1. **"No PI Insurance = no sub-contract"** — every design sub-contract on a critical-path design service needs PI
2. **"PI Cap without PI Insurance is meaningless"** — a SAR 225k cap means nothing if AD Engineering can't pay or isn't insured
3. **"Insurance must be verified before signing"** — verbal confirmation or future commitment is insufficient
4. **"Stamping Samaya-drafted drawings requires PI coverage"** — verify PI scope explicitly
5. **"Shop Drawing Reviews during construction require PI"** — design + construction phase both need coverage
6. **"Industry standard: 1-3% of contract value = PI premium"** — for SAR 225k, expect SAR 2-5k PI cost
7. **"PI Insurance retroactive date = date of contract"** — protects against earlier errors
8. **"PI 7-year tail = mandatory for design defects"** — latent defects emerge years after construction

---

## 📁 Hub Update Plan

1. **Update** `training/_lens_reports/2026-07-31-ad-engineering-sow-review.md` to flag insurance as CRITICAL gap
2. **Update** `training/_lens_reports/2026-07-31-ad-engineering-verbal-sow.md` to add insurance as gating condition
3. **Save** new file `training/_lens_reports/2026-07-31-ad-engineering-insurance-gap.md`
4. **Save** Insurance clause template to `training/contract-administration/templates/subcontract-insurance-clause-template.md`
5. **Save** 8 new lessons to `training/contract-administration/lessons.md`
6. **Update** Aseer P219 V3.1 Lens 9 with insurance gaps noted
7. **Commit + push**

---

## 🎯 The Final Verdict

**Is the sub-contract signable today?**

# ❌ **NO — absolutely not.**

**Reasons:**
1. ❌ **No PI Insurance agreement** (CRITICAL — user-confirmed)
2. ❌ Verbal SOW not codified in Schedule A
3. ❌ 7-day schedule misalignment (15 Oct vs 30 Sep)
4. ❌ Coordination clauses missing
5. ❌ LDs + retention + performance bond missing
6. ❌ Set-off mechanism not verified
7. ❌ Mech: split responsibility liability allocation undefined

**What needs to happen in the next 7 days:**
1. ✅ AD Engineering submits PI Insurance proof
2. ✅ Samaya's insurance broker confirms project policy coverage of sub-consultants
3. ✅ Schedule A drafted (covering 7 verbal SOW items + insurance clause)
4. ✅ Schedule acceleration proposed (30 Sep target)
5. ✅ Liability allocation clause added
6. ✅ Set-off balance verified
7. ✅ Legal review (Art. 9, 10, 11)

**If PI Insurance is NOT available within 7 days:** Terminate the verbal agreement and find an alternative MEP designer.

---

*This is not a "hurry up and sign" situation. The lack of insurance means Samaya is exposed to unlimited liability on a SAR 225k contract — that math doesn't work.*