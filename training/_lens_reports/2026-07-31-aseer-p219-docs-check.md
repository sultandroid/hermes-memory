# 🔍 Lens 0 — Documentary Reality Check (CRITICAL)

> **ملاحظة حرجة قبل أي تحليل Aseer P219:**
> هذه العدسة كانت تـ "تحلل" بناءً على Odoo task list **بس** — ده **مخالف صريح لمبدأ مدير العقود الأول**: "اعرف الوثائق قبل ما تتكلم."

## ❌ ما هو مفقود (critical gaps)

| الوثيقة | الحالة | الأثر |
|---|---|---|
| **Main Contract** (Samaya ↔ MoC) | ❌ **غير متاحة** للـ agent | لا يمكن تحديد FIDIC edition, GC/SC, design liability, IP, payment terms, completion date |
| **SOW** (6380_KMS_RPT_PM_AS_00006) | ❌ **غير متاح** | لا يمكن تحديد scope of supply/exclusions, NRS scope split, design freeze triggers |
| **ER (Employer's Requirements)** (250313_R02 Rev 1.0) | ❌ **غير متاح** | لا يمكن تحديد technical requirements, performance specs, acceptance criteria |
| **Subcontract: NRS (Lighting Design)** | ❌ **غير متاح** | لا يمكن تقييم delay attributable to NRS, PI scope, design brief delivery dates |
| **Subcontract: Glasbau Hahn (Showcase)** | ❌ **غير متاح** | لا يمكن تقييم PQ status, why 48 days late, scope split |
| **Subcontracts: Acoustics, Telecom, SEC, FF&E, etc.** | ❌ **غير متاح** | لا يمكن تقييم broader scope |
| **Baseline programme** | ❌ **غير متاح** | لا يمكن تحديد original completion date, critical path |
| **As-built programme** | ❌ **غير متاح** | لا يمكن تحديد actual progress vs baseline |
| **Daily reports / site diaries** | ❌ **غير متاح** | لا يمكن evidence contemporaneous records |
| **Cl. 20.1 submittal log** | ❌ **غير متاح** | لا يمكن تحديد if 28-day notice was served for past delays |
| **Engineer correspondence (CG)** | ❌ **غير متاح** | لا يمكن تحديد who is at fault for delays |
| **NCR register (live)** | ❌ **غير متاح** (NCR-1A0-008 seen in tasks only) | لا يمكن تقييم open NCRs |
| **MoC / CG / NRS emails** | ❌ **غير متاح** (Outlook pipeline not pulled) | لا يمكن reconstruct timeline |
| **Subcontract with Samaya + Design responsibility matrix** | ❌ **غير متاح** | لا يمكن تحديد who owns lighting design scope |
| **OneDrive Aseer folder** | ❌ **not mounted in this VM** | لا يمكن access any project files |

## ✅ ما هو متاح (limited basis)

| المصدر | المحتوى |
|---|---|
| `PROJECTS.md` (hub) | Project metadata: name, doc code, client, PMC, consultant, designer, timeline |
| `CONTACTS.md` (hub) | Samaya team roles + external (Hossam Mabrouk, Mohammad Elbaz, Jim Richards, NRS) |
| `MEMORY.md` (hub) | Procedural memory (Code B handling, D&B, scope creep flag to Adel) |
| `RULES.md` (hub) | Working rules + Entity Isolation matrix |
| `ODOO.md` (hub) | Odoo connection + patterns |
| Odoo P219 task list | 109 tasks (83 open, 2 overdue, 84 due in 7d) |
| Odoo P219 attachments | 4 schedules only (FF&E, Showcase, Finishes, Est. Quantity) |
| Training library | 99 cases + 10 topics, mostly Saudi/GCC construction |

## 🚨 ما يجب أن يحدث قبل أي "claim strategy"

**لا Cl. 20.1. لا Notification of Delay. لا NRS PI claim. لا internal RCA.**

**قبل أي إجراء، يلزم:**

1. **Main Contract (Samaya ↔ MoC)** — كامل:
   - شروط FIDIC (1999 or 2017)
   - Cl. 1.1.2.6 (Engineer), Cl. 1.1.3.8 (Defects Notification Period)
   - Cl. 3.5 (Engineer's determination, 2017 only)
   - Cl. 13 (Variations and Adjustments)
   - Cl. 17 (Risk and Responsibility, Design responsibility)
   - Cl. 20 (Claims — especially 20.1 notice, 20.4 contemporary records)
   - Appendix to Tender: scope split
   - Particular Conditions (البنود الخاصة في العقد السعودي)

2. **SOW (Scope of Work)** — كامل:
   - Design scope (ما هو Samaya مسؤول عنه vs NRS)
   - Supply scope
   - Install scope
   - Commissioning scope
   - Exclusions (ما هو NOT في نطاقنا)
   - Design review gates (when does design freeze occur?)

3. **ER (Employer's Requirements)** — كامل:
   - Technical performance specs
   - Acceptance criteria for lighting, showcase, etc.
   - Witness / approval gates
   - Design review requirements

4. **Subcontract: NRS**:
   - Design scope (what NRS is responsible for)
   - Design brief delivery schedule
   - PI cap and period
   - Delay LDs
   - Notice provisions

5. **Subcontract: Glasbau Hahn (or general Tier 2 specialist terms)**:
   - PQ submission requirements
   - PQ approval workflow
   - LDs
   - Scope of supply

6. **Project correspondence (last 6 months)**:
   - All Cl. 20.1 notices served (if any)
   - All Cl. 2.1 / 3.5 Engineer instructions
   - All CG letters on design delays
   - All NRS design brief submissions
   - All MoC approvals / rejections

7. **Site records (last 6 months)**:
   - Daily reports
   - Weekly programmes
   - Risk register
   - Procurement schedule
   - Subcontractor status reports

**بدون هذي الـ 7 items: أي claim strategy = speculation. أي notice = risk of self-incrimination.**

## 📍 Realistic next steps (in order)

| # | Step | Who | Time |
|---|---|---|---|
| 1 | Mount OneDrive Aseer folder (`/Bim Unit/Aseer-Museum/`) so the agent can access project files | user | 10 min |
| 2 | Pull Outlook emails from the Aseer project (MoC, CG, NRS, MoC, Hossam, Elbaz, Adel) — last 6 months | user or agent | 30 min |
| 3 | Read Main Contract + SOW + ER into the agent's working context | user provides | 1 hour |
| 4 | Read NRS subcontract + Glasbau Hahn terms (or generic specialist T&Cs) | user provides | 1 hour |
| 5 | Read Cl. 20.1 submittal log (if one exists; if not, that's itself a finding) | user or Samir | 30 min |
| 6 | Re-run contract-manager-lens with documentary basis | agent | 1 hour |

**Total: ~4 hours of human effort to enable any real analysis.**

## ❌ What the lens CAN do today (without docs)

Limited to:
- **Odoo task-list audit** (already done) — confirms 2 overdue, 84 in 7d
- **Risk profile assessment** (already done) — confirms HIGH risk
- **Procedural discipline gaps** (already done) — confirms missing Cl. 20.1 log, GAR 6th Ed file structure unknown
- **NCR-1A0-008 detection** (already done) — confirms NCR is open

**Cannot do without docs:**
- Determine fault (Employer vs Samaya vs NRS vs specialist)
- Determine EOT entitlement
- Determine quantum (delay days, preliminaries, HOOH)
- Draft any claim / notice / letter
- Recommend any specific action

## 🎯 The honest recommendation

**Today: do NOT issue any notice, claim, or letter.**

Instead:
1. **Mount OneDrive Aseer** so the lens can see project files
2. **Pull 6 months of email** on the project
3. **Provide the Main Contract, SOW, ER** to the agent (upload PDFs to a path I can read, or paste excerpts)
4. **Then re-run the lens** — it will produce a much sharper, evidence-based analysis

The earlier "lens report" (commit `f318d4b`) was useful as a **task-list audit** but **NOT a contract/claim analysis**. I apologise for the over-reach. As contract manager, the first step is always "read the contract" — and I did not have it.

---

*📁 Saved to: `training/_lens_reports/2026-07-31-aseer-p219-docs-check.md`*
*Status: Documentary reality check. No claim action recommended until docs are provided.*
*Hub: HEALTHY · commit pending*

---

**🛑 عذراً على الـ framing المتسرع في التقرير الأول. مدير العقود الصح ما يـ recommend إجراء بدون وثائق. أعيد العدسة للـ "OS zero" — لازم الوثائق الأول.**

لو تقدر تعمل mount لـ OneDrive أو ترفع الـ contract + SOW + ER كـ PDF، الـ lens هيشتغل صح. وإلا، التحليل الحالي **محدود بـ Odoo tasks فقط — لا يصلح كـ claim strategy.**
