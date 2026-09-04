---
name: factory-operations
title: Samaya Factory Operations — Manager Dashboard & Daily Review
description: Factory manager's daily review workflow — pull MRP orders, POs, and emails from Odoo + Outlook, cross-reference, analyze, and produce decisions. Covers org chart, data sources, analysis patterns, and decision framework.
triggers:
  - User says "كمدير مصنع" / "as factory manager"
  - User asks for factory status / تقرير المصنع
  - User wants to review production + purchasing + communications together
  - User says "احبار ملفات الاداريات" / "ربط المواضيع"
  - User sends a job request form (طلب استحداث وظيفة) or iqama file (إقامات)
  - User asks for offer letters / عروض وظيفية
---

# Samaya Factory Operations — Manager Dashboard

## 🏭 Org Chart (Samaya Factory)

| Role | Person | Responsibility |
|------|--------|---------------|
| **مدير المصنع (Factory Manager)** | محمد سلطان عباس عيسى | Overall factory management, decisions, approvals |
| **مدير الإنتاج (Production Manager)** | رؤوف محمد رضا الديب | Production planning, shop floor, workforce, quality |
| **مدير القسم الفني / 3D** | أحمد عواد فرحات | Technical design, 3D modeling |
| **مدير قسم الفايبر** | عصام إبراهيم عز الدين | Fiberglass production |
| **مشرف الصيانة + مشغل CNC** | محمد خاجا معين الدين | Machine maintenance + CNC operator. Odoo ID 2760, dept Eventech(46), email kmoinuddin24@gmail.com, phone 966551435149, manager Raouf(903) |

**⚠️ Warith Sultan has NO relation to the factory** — he is Aseer Museum project director only.

**⚠️ Odoo job_title reflects the IQAMA (residence permit) role, NOT the real role.** E.g. Moin El-Din is listed "Carpenter" but is actually Maintenance Supervisor + CNC operator. Always confirm the real role with the user before using job_title for maintenance/operator assignments.

## 📡 Data Sources

| Source | What it contains | How to access |
|--------|-----------------|---------------|
| **Odoo MRP** (`mrp.production`) | 502+ manufacturing orders — states, dates, products, quantities | XML-RPC to `samayainv.odoo.com`, credentials at `~/.config/samaya/odoo.env` |
| **Odoo POs** (`purchase.order`) | 321+ factory POs (2M+ SAR) — open, draft, received, cancelled | Same Odoo connection, filter by project 244 (Samaya Factory) |
| **Outlook SQLite** | ~2,063 factory-related emails — from/to Raoof, "مصنع" in subject | `~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite` |

## 📁 PO Classification & Payment Tracking

### Classification by Receipt + Invoice Status

When the user asks to classify POs, run the script at `references/classify_factory_pos.py` (or reproduce its logic):

| Classification | Meaning | Odoo signals |
|---------------|---------|-------------|
| ✅ مستلم كامل + مفوتر | Received + invoiced | `receipt_status=full`, `invoice_status=invoiced` |
| ✅ مستلم كامل + غير مفوتر | Received, not yet invoiced | `receipt_status=full`, `invoice_status≠invoiced` |
| ⏳ مستلم جزئي | Partially received | `receipt_status=pending` |
| ❌ لم يستلم + غير مفوتر | Not received, not invoiced | `receipt_status=false`, `invoice_status≠invoiced` |
| ❌ لم يستلم + مفوتر | Not received but invoiced (anomaly) | `receipt_status=false`, `invoice_status=invoiced` |
| 🗑 ملغي | Cancelled | `state=cancel` |
| 📝 مسودة | Draft | `state=draft` |

### Payment Tracking via Ibrahim Shaaban Emails

**Critical insight:** Payments are often made OUTSIDE Odoo — no invoice recorded in the system. The actual payment record lives in Ibrahim Shaaban's emails (إبراهيم شعبان).

To find actual payments:
1. Query Outlook SQLite for emails FROM Ibrahim Shaaban
2. Filter by payment keywords: `سداد`, `دفع`, `صرف`, `تحويل`, `عهدة`, `مستخلص`, `كشف حساب`, `بنكي`
3. Cross-reference PO numbers mentioned in his email body against Odoo invoice status
4. A PO with `invoice_status=no` or `to invoice` but mentioned in Ibrahim's payment email = **paid outside system**

**Monthly payment summary:** Group Ibrahim's payment emails by month to see cash flow timing.

### Script

A reusable classification script lives at `references/classify_factory_pos.py` in this skill's directory. It:
- Loads all factory POs from the JSON dump
- Queries Outlook SQLite for Ibrahim Shaaban's emails
- Cross-references PO numbers mentioned in his emails
- Produces a full classification report + monthly payment summary

## 🔍 PO-by-PO Review Workflow (كشف رؤوف)

عندما يرسل رؤوف كشف متأخرات، اتبع هذا البروتوكول لكل PO في الكشف:

### خطوات المراجعة لكل PO

1. **استخرج رقم PO** من الكشف
2. **افتح الرابط**: `https://samayainv.odoo.com/odoo/purchase.order/{ID}`
3. **تحقق من الحالة**:
   - `state=purchase` → مؤكد
   - `state=draft` → مسودة (تحتاج اعتماد)
4. **تحقق من الفاتورة**: `invoice_status=invoiced` أم `to invoice` أم `no`
5. **تحقق من الاستلام**: `receipt_status=full` (مستلم) أم `pending` (جزئي) أم `false` (لم يستلم)
6. **اقرأ الشات** — ابحث عن:
   - تذكيرات متابعة صرف من سلطان عيسى `[متابعة الصرف]`
   - طلبات اعتماد `برجاء الاعتماد @Ibrahim Shaaban`
   - تعليقات رؤوف `برجاء سرعة التحويل`
   - تعليقات إبراهيم شعبان `قائمة المهام تم` (يعني تم الدفع خارج النظام)
7. **تحقق من المطابقة** — هل تم إرفاق عرض سعر ومطابقته قبل الاعتماد؟

### التصنيف النهائي لكل PO

| اللون | المعنى | الإجراء |
|-------|--------|---------|
| 🟢 تم الصرف | إبراهيم سجل دفع أو رؤوف أرفق رقم تحويل | لا إجراء |
| 🟡 مؤكد + مستلم + غير مفوتر | المواد وصلت — تأخر صرف | متابعة المالية |
| 🟠 مسودة | لم يعتمد بعد | اعتماد أو إلغاء |
| 🔴 خارج أودو | فواتير مجمعة غير مسجلة | إنشاء PO أو صرف مباشر |
| ⚪ بدون سعر | لم يدخل عرض سعر | تحديد السعر أو إلغاء |

### تنسيق التقرير النهائي

```
**P02264** — امداد التوريد (اخشاب) — 24,828 SAR
https://samayainv.odoo.com/odoo/purchase.order/2264
- الحالة: ✅ مؤكد
- الفاتورة: ❌ غير مفوترة
- الاستلام: ✅ مستلم 2 أغسطس
- المطابقة: ❌ لم تتم
- الشات: تذكير متابعة صرف من سلطان عيسى 2 أغسطس
```

### روابط سريعة للـ POs في كشف رؤوف

عند عرض النتائج، أرسل روابط مباشرة لكل PO مقسمة حسب الأولوية (عاجل / عمالة / مسودات / مؤكدة).

عندما يرسل رؤوف كشف "المتأخرات" (PDF/Excel)، **لا تفترض أنها تأخر توريد**. كشف رؤوف هو عن **تأخر الصرف/الدفع** — المواد غالباً وصلت والمورد مستلمش فلوسه.

### خطوات التحليل

1. **استخراج أرقام POs من الكشف** (يدوياً أو pdftotext)
2. **مقارنة كل PO مع أودو**:
   - `state` — purchase (مؤكد) أم draft (مسودة)؟
   - `invoice_status` — invoiced (مفوتر) أم to invoice (غير مفوتر)؟
   - `receipt_status` — full (مستلم) أم pending (مستلم جزئي) أم false (لم يستلم)؟
3. **فحص الشات** — هل فيه تذكير متابعة صرف من سلطان عيسى؟
4. **فحص تعليقات إبراهيم شعبان** — هل سجل دفع خارج النظام؟

### التصنيف النهائي

| الحالة | المعنى | الإجراء |
|--------|--------|---------|
| مستلم + غير مفوتر | ✅ المواد وصلت — تأخر صرف | متابعة المالية للصرف |
| لم يستلم + مؤكد | ❌ المورد ما جابش الخامة | متابعة المورد |
| مسودة | ⬜ لم يعتمد بعد | اعتماد أو إلغاء |
| بدون سعر | ⬜ لم يدخل عرض سعر | تحديد السعر أو إلغاء |
| غير موجود في أودو | ❌ فواتير مجمعة خارج النظام | إنشاء PO أو صرف مباشر |

### مثال — كشف رؤوف 4 أغسطس 2026

```
21 بنداً في الكشف
20 PO موجود في أودو
1 فاتورة مجمعة (مدي الجزيرة 37,854 ريال — خارج أودو)
8 مسودات (3 عمالة = 89,226 ريال)
12 مؤكدة (كلها مستلمة + غير مفوترة = تأخر صرف)
1 مفوتر فقط (P02113 — لؤلؤة السلي)
```

### الفرق الجوهري

- **تأخر توريد** = المورد ما جابش الخامة → نادر في كشف رؤوف
- **تأخر صرف** = المالية ما دفعتش للمورد → هذا هو الغالب في كشف رؤوف

## 🔄 Daily Review Workflow

### Phase 1: Collect (run in parallel via delegate_task)

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  MRP Orders     │  │  Factory POs     │  │  Emails (30d)   │
│  - All states   │  │  - Open/draft    │  │  - From Raoof   │
│  - Dates        │  │  - Top amounts   │  │  - To Raoof     │
│  - Overdue      │  │  - Credit supp.  │  │  - "مصنع" subj  │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         └────────────────────┼────────────────────┘
                              ▼
                    ┌──────────────────┐
                    │  Cross-reference │
                    │  & Analyze       │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │  Decisions       │
                    └──────────────────┘
```

### Phase 2: Analyze — Key Questions

**Production (MRP):**
- How many orders in each state? (done / progress / draft / confirmed / to_close / cancel)
- Which orders have been in "progress" the longest? (oldest date_start)
- Which drafts have been sitting the longest without starting?
- Are there orders "to_close" that are actually finished but not closed in system?

**Purchasing (POs):**
- How many open POs? Total amount?
- Which vendors have the highest outstanding?
- Are there draft POs that should be confirmed or cancelled?
- Credit suppliers (Saba Najad, Mada Aljezera) — what's their current balance?

**Communications (Emails):**
- Any new violation reports from Raoof?
- Any purchase requests / urgent material needs?
- Any HR actions (hiring, termination, overtime)?
- Any maintenance issues (roof leaks, equipment breakdown)?
- Any customer/contractor communications?

### Phase 3: Cross-Reference & Connect

Look for patterns across sources:
- **Draft MOs + related PO not placed** → material shortage blocking production
- **Raoof email about urgent need + PO still draft** → bottleneck in purchasing
- **Overtime requests + production backlog** → capacity issue
- **Violation reports + same employee repeated** → escalating discipline needed
- **Maintenance issue + no PO for repair** → asset risk

### Phase 4: Produce Decisions

For each connected issue, produce a clear decision:
1. **Action** — what to do (meeting, approve, escalate, order, repair)
2. **Who** — responsible person
3. **When** — deadline
4. **Priority** — urgent / high / medium / low

## 📊 Daily Manager Report — AUTOMATED (cron)

The daily report is now **auto-generated** by cron job `f49274e17cde` (daily 08:00, deliver=origin).

**Pipeline:**
1. `~/.hermes/scripts/factory_daily_report.py` fetches sections 1-3 live:
   - **MRP** state counts from Odoo `mrp.production` (limit 2000)
   - **Factory POs** from `purchase.order` filtered by `FACTORY_PROJECT_IDS = {161, 244, 302, 307, 315}` + `FACTORY_SUPPLIER_IDS` (same sets as `fetch_factory_pos_v2.py`), plus top-5 vendors by open outstanding
   - **Raoof emails** last 30 days from Outlook SQLite (`Message_SenderList LIKE '%Raoof%'`)
2. The cron agent writes section 4 (القرارات) by cross-referencing the data, saves to `samaya-profile/00_Admin/factory_manager_report_YYYY-MM-DD.md`, commits to git (date in commit msg), and replies with an Arabic summary.

**Report structure (4 sections):** 1️⃣ MRP counts · 2️⃣ PO totals + open/draft + top vendors · 3️⃣ Raoof emails · 4️⃣ Decisions (action/who/when/priority).

**To regenerate manually:** `python3 ~/.hermes/scripts/factory_daily_report.py` (prints sections 1-3 as markdown; section 4 is a placeholder the agent fills).

**Pitfall:** the script's `fetch_raoof_emails` uses `Message_SenderList LIKE '%Raoof%'` — the Outlook column is `Message_RecipientList` (NOT `Message_Recipients`, which doesn't exist). Raoof's sender names include "Raoof Eldeeb", "raoofeldeeb", "raoof@technose.net", "Raoof Aldeeb".

### Legacy manual template (pre-automation reference)

```markdown
# تقرير مدير المصنع — YYYY-MM-DD

## 1️⃣ أوامر التصنيع (MRP) — N أمر
| الحالة | العدد |
|--------|:-----:|

## 2️⃣ أوامر الشراء (POs)
| البند | العدد | الإجمالي (SAR) |

## 3️⃣ الإيميلات — آخر 30 يوم
### من رؤوف:
### إلى رؤوف:

## 4️⃣ القرارات
1. ...
```

## 📐 Lean Manufacturing System (`samaya-profile/03_Workshop/lean/`)

A deployable Lean system lives in the repo at `03_Workshop/lean/`. It bundles 5 integrated tools plus preventive maintenance:

| Tool | Folder / File | Frequency |
|------|---------------|-----------|
| Gemba Walk | `01_gemba_walk/` (checklist + log) | Daily 15-30 min |
| Kaizen | `02_kaizen/` (form + register) | Weekly |
| 5S | `03_5s/` (audit checklist + scores) | Weekly |
| 5 Whys | `04_5whys/5whys_form.md` | On every problem |
| Preventive Maintenance | `04_preventive_maintenance/` | Weekly per machine |
| Continuous Improvement | `05_continuous_improvement/ci_register.md` + Excel | Continuous |
| Lean Input (seed) | `06_lean_input/` (register + raw JSON) | From WhatsApp/email |

**Gemba triage rule (user-corrected):** ~90% of walk observations are *immediate process fixes* (execution errors, delays, wrong layout) → fix on the spot, mark "⚡ immediate action", close same day. Only *recurring* problems get a 5 Whys analysis; only *improvement ideas* become Kaizen cards. Don't force every observation through a Kaizen/5-Whys funnel — that's overhead the user rejected.

**Lean scope discipline (user-corrected):** Lean tracks machine **downtime, efficiency, capacity** — NOT machine asset value / cost / depreciation. Asset value is accounting, not Lean. Do not add cost tracking to Lean registers.

**PM checklists are machine-specific** — checks differ by machine type. Chiller water (level/temp/leaks/distilled-water change), belts (tension/cracks/age), lenses & mirrors (clean/no-crack/no-coating-peel), assist gas, nozzle, exhaust. CO2 laser checks lenses+mirrors; fiber laser checks focus lens + protective window (replaced most often). See `references/cnc_laser_machines.md` for the machine inventory.

**Odoo hosting consideration:** The same structure maps cleanly to Odoo — one Project "Lean Manufacturing" with 3 stages (جديد/قيد التنفيذ/مغلق) and tags for the tool type (Gemba/Immediate/Kaizen/5-Whys/5S). 5S scoring can live in Quality module. Preventive maintenance maps to the Maintenance module (real PM schedules fix the "no PM system" 5-Whys root cause). User prefers to build/collect data on the repo first, then decide on Odoo — don't jump to Odoo.

## 🏪 Inventory Monitoring System

### Architecture

**Odoo is READ-ONLY + chatter notes only.** No programmatic modifications, no field additions, no automations without explicit permission. All data is read from Odoo via XML-RPC; all processing and storage happens in the `samaya-profile` repo.

### Scripts

| Script | Location | Purpose | Schedule |
|--------|----------|---------|----------|
| `mo_monitor.py remind` | `~/.hermes/scripts/mo_monitor.py` | Check MOs without materials, post reminder in chatter | Every 2 days, workdays 8am-5pm |

### MO Compliance Monitoring

**Reminder rule:** Every 2 workdays (Sat-Thu, 8am-5pm), check MOs in `progress`/`confirmed` state that are older than 2 days with no `move_raw_ids`. Post a plain-text reminder in the chatter:

```
يرجى تسجيل المواد المستهلكة ووقت مراكز العمل.
```

**⚠️ Chatter note content (user-mandated):** The note sits ON the MO's own chatter page, so **do NOT** repeat the MO name, product, or quantity — it is redundant clutter the user rejects. The exact format above is final; do not add "أمر التصنيع {MO_NAME}", "المنتج:", "الكمية:", "تاريخ البدء:", or "قبل إغلاقه" back in. The user explicitly said "نظف وحدث ولا تكرر الاخطاء ابدا".

**Deduplication:** Before posting a new reminder, delete any previous reminder containing the marker `__REMINDER_MARKER__` from the same MO's chatter. This prevents spam.

**Blocked close:** MOs in `to_close` state without `move_raw_ids` get a warning posted. The system does NOT programmatically block the close — it only notifies.

### PO Payment Tracking (via Odoo Chatter)

**Key insight:** Ibrahim Shaaban (إبراهيم مصطفى شعبان) records actual payments in Odoo PO chatter comments, NOT as invoices. **His Odoo USER id is 5521** (filter `mail.message.author_id = 5521`); 4870 is his PARTNER id — the author filter on `mail.message` needs the user id, not partner id.

**To find actual payments (learned 2026-08-18):**
1. Query `mail.message` for each factory PO (project 244), filter `author_id = 5521`, `message_type = 'comment'`
2. **Distinguish real transfers from task completions** — this is the critical step:
   - 💰 **ACTUALLY PAID:** body contains `صورة التحويل` / `صورة تحويل الدفعة` (transfer screenshot attached). E.g. "مرفق لكم صورة التحويل" → paid. Often followed by Raoof uploading the tax invoice.
   - ✅ **TASK DONE ONLY:** body contains `قائمة المهام تم` OR is **empty** → this is a `mail.activity` completion (approval workflow), NOT proof of a transfer. Empty-body messages are usually activity completions, not payments.
3. **Check `attachment_ids`** on empty-body messages before concluding — transfer screenshots may be attached without body text. Inspect attachment filenames.
4. **Cross-check project ownership:** a factory-linked PO is only a "factory payment" if `project_id ∈ {161, 244, 302, 307, 315}`. Factory-supplier POs on OTHER projects (Maalim Al-Haramein/Jabal Omar, admin tickets) are not factory payments.
5. Cross-reference: a PO with `invoice_status=no`/`to invoice` but with Ibrahim's `صورة التحويل` comment = **paid outside Odoo**.

**Report format for "paid today" answers:** group into (a) 💰 مدفوع فعلاً (transfer screenshot in chatter) with PO + vendor + amount + the quoted chatter evidence, (b) ✅ قائمة مهام "تم" (task complete, no transfer proof), and flag (c) which are genuinely factory project vs other projects.

### Inventory Snapshot

Run `mo_monitor.py weekly` to generate:
- **Word report** → `samaya-profile/00_Admin/weekly_report_YYYYMMDD.docx`
- **JSON snapshot** → `samaya-profile/00_Admin/inventory_snapshot.json`

The report covers:
1. New MOs this week (with material recording status)
2. Completed MOs this week
3. Violations: MOs without materials, MOs without BoM
4. Stock alerts: negative stock, low stock (<5), zero stock with movement
5. Pending POs without full receipt

### Consumables Distribution

Consumables (categories: Consumables, PPE & Safety, Tools) are distributed monthly across all MOs completed in that month:

```
Cost per MO = Total consumables received in month / Number of MOs completed in month
```

This is calculated in the weekly report but not written back to Odoo.

### Raw Material Categories (for filtering)

Only materials under `Raw materials` / `Raw Materials` category tree (60+ subcategories including MDF, Plywood, Steel, Paint, Wood Veneer, Acrylic, Chemical & Glue, Fabric, Foam, etc.) are tracked. Consumables categories are excluded from stock alerts.

## Warehouse Receipt Monitoring (Wrong Warehouse Detection)

### The Cron Job

A cron job (job_id `03d25c46e1d1`) runs daily at 6:00 AM to detect receipts on `FA/WH/FA` (Factory Warehouse) that genuinely don't belong to the factory.

**Classification logic (corrected):**
1. Get all stock pickings on FA/WH/FA (location_dest_id = 45) in last 7 days
2. For each, get the origin field → PO reference
3. Look up the PO's project_id in Odoo
4. If project_id = 244 (Samaya Factory) → correct receipt, skip
5. If project_id != 244 → wrong warehouse, flag it

**Script location:** `~/.hermes/scripts/factory_warehouse_monitor.py`

### Chatter Notes Format

Notes posted to Odoo chatter must be:
- Plain text only — no icons, no tags, no markdown formatting
- Short and direct, like a human message
- Example: `[تأكيد المخزن] تم استلام هذا الأمر على مخزن المصنع لكن طلب الشراء (P02247) يخص مشروع: جبل عمر (Maalim Al-Haramein) — وليس المصنع.`

### How to Verify Manually

1. Open the receipt: `https://samayainv.odoo.com/web#id={picking_id}&model=stock.picking&view_type=form`
2. Check the "Source Document" (origin) field → PO number
3. Open the PO: `https://samayainv.odoo.com/web#id={po_id}&model=purchase.order&view_type=form`
4. Check the "Project" field → if Samaya Factory (244), the receipt is correct

## ⚠️ Critical Rules

- **Odoo is READ-ONLY** — never add fields, automations, or programmatic modifications without explicit permission
- **Chatter notes are OK** — posting comments to `mail.message` via `message_post` is allowed
- **All data lives in samaya-profile repo** — reports, JSON snapshots, scripts
- **No execute_code in cron jobs** — use `no_agent=True` with a script path instead

## 🔗 Related Skills

- `samaya-cashout-report` — Detailed Excel cashout report from Odoo POs
- `factory-violations` — Employee violation management (disciplinary memos)
- `odoo` — Odoo connection, field schemas, SSL fix
- `samaya-docx-template` — SamayaDoc class for DOCX generation (used by offer letters)

## 📎 Reference Files

| File | Purpose |
|------|---------|
| `references/raoof-delay-report-2026-08-04.md` | Example delay report analysis from Raoof |
| `references/mo-hours-days-report.md` | Build active-MOs report: actual hours (workorder `duration`/60) + days since `date_start`. Includes the `mrp.workorder` field pitfalls (`duration_actual` doesn't exist; `duration` is minutes) |
| `references/job-offer-letters.md` | Workflow for generating factory job offer letters from request form + iqama file |
| `references/cnc_laser_machines.md` | CNC/Laser machine inventory from Odoo + PM check categories per machine type |
| `references/whatsapp-hr-context.md` | Use WhatsApp `_chat.txt` export as the source for factory HR/termination/salary decisions (Odoo hr.employee is thin); Saudi Labor Law Art. 75 notice periods |
| `references/overtime-followup-email.md` | Draft HR follow-up email on delayed overtime: cite facts (strike/refusal timeline) + Odoo helpdesk ticket numbers (#2611 June, #2755 July open) |
| `references/unified-employee-db-and-cost-study.md` | Build the unified employee DB keyed by biotime (merge salaries + biotime + violations + OT) + the factory-separation monthly cost study. Covers the `employees_full_details.csv` Odoo export as authoritative salary source, the empty-package pitfall, and the OneDrive OT-folder deadlock |
| `scripts/whatsapp_lean_classify.py` | Classify Lean input items from WhatsApp `_chat.txt` export (handles LRM/unicode quirks) |

## ⚠️ Pitfalls

- **Warith Sultan is NOT factory-related** — do not involve him in factory decisions
- **Mohamed Sultan = Factory Manager** (not just Tech Office) — make decisions, don't just report
- **Raoof = Production Manager** — he runs the shop floor, reports issues, requests materials
- **Odoo project_id domain bug** — never use `project_id` in `search_read` domain; fetch all and filter in Python
- **Outlook SQLite is the ONLY email source** — do NOT use Gmail IMAP for factory emails
- **Credit suppliers** (Saba Najad, Mada Aljezera) are statement balances, not individual POs
- **Don't confuse tickets with violations** — helpdesk ticket closures are HR actions, not disciplinary records
- **Odoo job_title = iqama role, not real role** — confirm real role (esp. for maintenance/CNC operators) with the user before relying on it
- **Odoo hr.employee is thin for factory workers** — the sultan@samayainvest.com account (uid 151) can't read `identification_id, gender, birthday, marital, country_id, notes, contract_id` (needs "Employees / Officer: Manage all employees"). For HR/termination/salary context, use the WhatsApp `_chat.txt` export instead — see `references/whatsapp-hr-context.md`
- **User-supplied Odoo employee IDs can be wrong** — always `search` by name and confirm the record matches the person before acting (e.g. user said "سهيل رقم 898" but 898 is a different inactive employee; سهيل is 1629). See `references/whatsapp-hr-context.md`
- **`hire_date` (char) is the hire field, NOT `date_of_hire`** — `date_of_hire` and `work_location` don't exist on `hr.employee` (raise "Invalid field"). `create_date` is record-creation, not hire date. Service length for these workers comes from the WhatsApp chat, not Odoo.
- **Authoritative salary source = `DATA/employees_full_details.csv`** (the Odoo export the user downloaded — 545 employees, factory 64). Its `الباكدج` (package) column is EMPTY; only `الراتب الأساسي` is populated. Report basic salary and note package is higher. `employees.json` keys are inconsistent (mix of odoo_id and biotime) — match by name, not key. See `references/unified-employee-db-and-cost-study.md`.
- **Lean ≠ asset accounting** — track downtime/efficiency/capacity, never machine value/cost. Don't force every Gemba observation through Kaizen/5-Whys (most are immediate fixes)
- **WhatsApp export parse bug** — lines start with `\u200e` LRM; strip line before regex, else you get "parsed 0 lines". Use `scripts/whatsapp_lean_classify.py`
- **MO monitor script has 3+ copies** — `~/.hermes/scripts/mo_monitor.py`, `~/.hermes/skills/samaya/factory-operations/scripts/mo_monitor.py`, `~/samaya-workspace/INVENTORY/scripts/monitor_mo_materials.py`, plus copies in `shared_exchange/` and `hermes-memory/`. Editing the chatter note template in ONE copy is not enough — a stale verbose template in another copy will re-post the old format. Update all copies together whenever the note format changes.
