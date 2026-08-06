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

**⚠️ Warith Sultan has NO relation to the factory** — he is Aseer Museum project director only.

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

## 📊 Report Template

Save to `samaya-profile/00_Admin/factory_manager_report_YYYY-MM-DD.md`:

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

## 🏪 Inventory Monitoring System

### Architecture

**Odoo is READ-ONLY + chatter notes only.** No programmatic modifications, no field additions, no automations without explicit permission. All data is read from Odoo via XML-RPC; all processing and storage happens in the `samaya-profile` repo.

### Scripts

| Script | Location | Purpose | Schedule |
|--------|----------|---------|----------|
| `mo_monitor.py remind` | `~/.hermes/scripts/mo_monitor.py` | Check MOs without materials, post reminder in chatter | Every 2 days, workdays 8am-5pm |
| `mo_monitor.py weekly` | same | Generate Word report + JSON snapshot | Weekly (Saturday) |
| `mo_monitor.py check` | same | Quick health check (no materials, negative stock, low stock) | On demand |

### MO Compliance Monitoring

**Reminder rule:** Every 2 workdays (Sat-Thu, 8am-5pm), check MOs in `progress`/`confirmed` state that are older than 2 days with no `move_raw_ids`. Post a plain-text reminder in the chatter:

```
🔔 تذكير بصرف المواد
يرجى تسجيل المواد الخاصة بأمر التصنيع {MO_NAME}
المنتج: {PRODUCT}
الكمية: {QTY}
تاريخ البدء: {DATE}
ملاحظة: لا يمكن إغلاق أمر التصنيع بدون تسجيل المواد ووقت مراكز العمل
```

**Deduplication:** Before posting a new reminder, delete any previous reminder containing the marker `__REMINDER_MARKER__` from the same MO's chatter. This prevents spam.

**Blocked close:** MOs in `to_close` state without `move_raw_ids` get a warning posted. The system does NOT programmatically block the close — it only notifies.

### PO Payment Tracking (via Odoo Chatter)

**Key insight:** Ibrahim Shaaban (إبراهيم مصطفى شعبان, partner ID 4870) records actual payments in Odoo PO chatter comments, NOT as invoices. His comments include:
- "مرفق لكم صورة التحويل" (transfer receipt attached)
- "برجاء تحويل مبلغ X" (please transfer amount X)
- "قائمة المهام تم" (task done — payment completed)

**To find actual payments:**
1. Query `mail.message` for each factory PO (project 244)
2. Filter by `author_id = 4870` (Ibrahim Shaaban)
3. Check body for payment keywords: `دفع`, `سداد`, `صرف`, `تحويل`, `عهدة`
4. Cross-reference: a PO with `invoice_status=no` or `to invoice` but with Ibrahim's payment comment = **paid outside Odoo**

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
| `references/job-offer-letters.md` | Workflow for generating factory job offer letters from request form + iqama file |

## ⚠️ Pitfalls

- **Warith Sultan is NOT factory-related** — do not involve him in factory decisions
- **Mohamed Sultan = Factory Manager** (not just Tech Office) — make decisions, don't just report
- **Raoof = Production Manager** — he runs the shop floor, reports issues, requests materials
- **Odoo project_id domain bug** — never use `project_id` in `search_read` domain; fetch all and filter in Python
- **Outlook SQLite is the ONLY email source** — do NOT use Gmail IMAP for factory emails
- **Credit suppliers** (Saba Najad, Mada Aljezera) are statement balances, not individual POs
- **Don't confuse tickets with violations** — helpdesk ticket closures are HR actions, not disciplinary records
