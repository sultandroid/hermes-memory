# Samaya BIM Unit — المشاريع الكاملة
> لتعليم وكيل Hermes على جهاز آخر في إدارة مشاريع Samaya Investment

---

## 1. المقدمة — نظرة عامة

Samaya Investment Company (شركة سمايا الإستثمارية) تدير مشاريع متاحف ومراكز زوار تحت **BIM Unit / Technical Office**. المشاريع مقسمة بين:

- **OneDrive-SAMAYAINVESTMENT** ← مشاريع BIM Unit الرئيسية
- **OneDrive-Personal (Tqanny)** ← مشاريع Tqanny المستقلة
- **Moqtana Odoo** ← مشاريع المصنع (مقتنى)
- **Samaya Odoo** ← المشتريات والفواتير للمشاريع

---

## 2. مشاريع BIM Unit (OneDrive-SAMAYAINVESTMENT)

### 2.1 متحف عسير الإقليمي — Aseer Regional Museum (Project 219)

| العنصر | التفاصيل |
|--------|---------|
| **Odoo Project ID** | 219 (Samaya Odoo) |
| **المسار الرئيسي** | `Samaya/Technical Office/Bim Unit/Aseer-Museum/` |
| **دوك كود** | `MOC-MUS-ASE` |
| **العميل** | Ministry of Culture (MoC) 🇸🇦 |
| **PMC** | ACE Moharram Bakhoum |
| **المقاول** | Samaya Investment (Main Contractor — D&B) |
| **استشاري الإشراف** | Consultancy Group (CG) |
| **مصمم العمارة** | NRS (Nissen Richards Studio) — Design Lead |
| **نظام التعاقد** | Design & Build (D&B) — Single Stage |
| **المدة** | من NTP 01-Dec-2025 إلى 07-Sep-2026 |
| **المبنى** | مبني قائم — بني 2015 في أبها، 3 أدوار |

#### نطاق العمل
- تركيب المتحف الداخلي (Exhibition Fit-Out)
- تطوير الـ MEPF
- تركيب المعروضات
- Part 1: RIBA 4 — Exhibition Technical Design
- Part 2: RIBA 4 — Engineering Design (MEPF, Structural, Civil)
- Part 3: Off-Site Fabrication
- Part 4: Enabling Works
- Part 5: RIBA 5 — On-Site Fit-out & Commissioning
- Part 6: RIBA 6 — Handover & Training
- Part 7: Defects Liability Period

#### أطراف رئيسية
| الطرف | الدور | جهة الاتصال |
|-------|-------|-------------|
| NRS | Design Lead (interior arch + scenography) | Nissen Richards Studio |
| CG | Consultant / Supervision | Hossam Mabrouk (hmabrouk@cg.com.sa) |
| CG | Project Manager | Mohammad Elbaz (melbaz@cg.com.sa) |
| Rawasin | AV/IT/Interactives (T2-09) | — |
| Subcon 19 | Interactive Design | — |
| MoC | Client / Employer | — |

#### الاستثناءات (MoC Supply)
| البند | المرجع |
|-------|---------|
| Exhibition text and labels | SOW §2.2 |
| Content research | SOW §2.2 |
| Image copyright and licensing | SOW §2.2 |
| Mounts package | SOW §2.2 |
| AV/Media software and content | SOW §2.2 (الأجهزة من مقاول) |
| Exterior landscape EX1/EX2 | CLAUDE.md |

#### فريق العمل (Samaya)
| الاسم | المعرف | الدور |
|-------|--------|-------|
| Sultan Issa | 151 (Odoo) | Technical Office Manager — DD packages only |
| Mohamed Samir | 564 | Site Execution + Procurement |
| Hani Alghamdi | 478 | Purchasing Lead |
| Hesham Abdelhameed | 163 | Document Control |
| Ahmed Salah | 162 | Project Coordination |
| Ali Abdelrahman | 160 | Technical Office — design only |
| Adel Darwish | 7 | Project Management |
| Mohamed Elshaikh | 157 | Project Planner |

#### الوثائق الأساسية
| الوثيقة | المرجع | الموقع |
|---------|--------|--------|
| Employer's Requirements (ER) | 250313_R02, Rev 1.0 | `Design Files/Package_Part 2/05_AS_ER/` |
| Scope of Work (SOW) | 6380_KMS_RPT_PM_AS_00006 | `Contracts & ER/` |
| DMP (Document Management Plan) | PL-0029 | `Docs/02_Plans_and_Procedures/` |
| Communication Plan | PL-0018 | `Correspondence/` |
| Stakeholder Plan | PL-0020 | `Correspondence/` |

#### هيكل المجلدات
```
Aseer-Museum/
├── 01_Contracts_and_ER/
│   ├── 01_Main_Contract/
│   ├── 02_NRS_Contract/
│   └── 03_Subcontracts/
├── 02_Submittals/
├── 03_Design_Files/
├── 04_Invoices/
├── 05_Correspondence/ (Incoming)
├── 06_Meetings/
├── 07_Reports/07.5_Audit_Report/
├── 08_Schedules/
├── 09_Registers/
│   ├── Subcontractor_RFI_Register/
│   ├── Transmittal_Register/
│   └── Submittal_Tracker_IFC_Log/
├── 10_Plans/
├── Docs/
│   ├── 02_Plans_and_Procedures/
│   │   └── 02.5_HSE_Plan/
│   └── 03_Inspection_Requests/
├── Subcontractors/
│   └── NN_Discipline_Contractor/
│       ├── _MANAGER_DASHBOARD/
│       ├── 01_Schedule_and_BOQ/
│       ├── 02_Reference_Drawings/
│       ├── 03_Specifications_and_Standards/
│       ├── 04_Reference_Imagery/
│       ├── 05_Returned_Submittals/
│       ├── 06_RFIs/
│       ├── 07_Approvals/
│       └── Email_Data_Extraction/
├── Email_Archive/
│   └── _aseer_tasks_backlog.md
├── _Project_Memory/
│   ├── PROJECT_MEMORY.md
│   └── DOCUMENT_INDEX.md
└── Scripts/notes/
```

#### الـ Subcontractors (Appendix B)
| الرقم | الاختصاص |
|-------|----------|
| — | Exhibition Fit-Out Contractor |
| — | Model Maker |
| — | Lighting Designer and Supplier |
| — | Graphics Artwork and Production |
| — | AV Hardware Contractor |
| — | Conservation Showcase Contractor |
| — | Specialist Rigging |
| — | FF&E Supplier |
| — | Interactives Contractor |
| — | M&E / MEP |
| — | Fire Life Safety |
| — | Structural Engineering |
| — | Health and Safety |
| — | IT/Data |
| — | Surveyor |
| — | Accessibility |
| — | Architect |
| — | Acoustic |
| — | Interior Design |
| — | Landscape |

---

### 2.2 متحف زمزم — Zamzam Visitor Center

| العنصر | التفاصيل |
|--------|---------|
| **Odoo** | غير معروف (Moqtana? يحتاج تأكيد) |
| **المسار الرئيسي** | `Samaya/Technical Office/Bim Unit/Zamzam - Visitor Center/` |
| **دوك كود** | `ZAM-NWC` |
| **ملاحظات** | يحتوي على Submittal's و Docs |
| **المحتوى** | Design development drawings + landscape |
| **رموز الملفات** | P083, TF2438 |

---

### 2.3 مسجد النور — Masjid Alnoor

| العنصر | التفاصيل |
|--------|---------|
| **المسار الرئيسي** | `Samaya/Technical Office/Bim Unit/Masjid Alnoor/` |
| **دوك كود** | مشروع مسجد في مكة |
| **Project Memory** | موجود — `Docs/00_Project_Charter/PROJECT_MEMORY.md` |
| **ملاحظات** | مشروع منفصل عن عسير وزمزم |

---

### 2.4 غار حراء — Hera' Ghar

| العنصر | التفاصيل |
|--------|---------|
| **المسار الرئيسي** | `Samaya/Technical Office/Bim Unit/Hera' Ghar/` |
| **Project Memory** | موجود — `Docs/00_Project_Charter/PROJECT_MEMORY.md` |

---

### 2.5 متحف الحرمين — El-Haramain Museum

| العنصر | التفاصيل |
|--------|---------|
| **الوصف** | مجسمين: المسجد الحرام (مكة) + المسجد النبوي (المدينة) |
| **رموز الملفات** | MVii (للمجسمات)، MVii Madinah → الحرمين، MVii Makkah → زمزم |
| **موقعها** | متحف خاص بالحرمين (مكة + المدينة) |
| **دوائر** | TP-09-2512-UTT-RP-R01 (تقرير الحواجز) |

---

## 3. مشاريع Tqanny (OneDrive-Personal)

المسار الرئيسي: `OneDrive-Personal(2)/Work/PWork/01_PROJECTS/Tqanny_Projects/`

| # | المجلد | اسم المشروع | ملاحظات |
|---|--------|-------------|---------|
| 01 | `01_Darin_Visitor_Center` | مركز زوار دارين (قلعة دارين) | Odoo Moqtana - proj 1039 |
| 02 | `02_Shobra` | شبرا | — |
| 03 | `03_Albiaa` | البيعة | — |
| 04 | `04_Al_Faw` | مركز زوار الفاو | عنده PROJECT_MEMORY.md |
| 05 | `05_Alrakaa_Center` | مركز الرقعة | — |
| 06 | `06_Antara_Rock` | صخرة عنترة | — |
| 07 | `07_Said_Alshohadaa` | سعيد الشهداء | — |
| 08 | `08_Tabuk_Castle` | قلعة تبوك | — |

كل مشروع له نفس الهيكل:
```
NN_ProjectName/
├── 00_Admin/
├── 01_CLIENT_INPUTS/
├── 02_Submittals/
├── 03_Design/
├── 04_Drawings/
├── 05_Specifications/
├── 06_BIM/
├── 07_Meetings/
├── 08_Schedules/
├── 09_Site/
├── 10_Calculations/
├── 11_Standards_&_References/
└── 99_Templates/
```

---

## 4. أكواد المشاريع — Document Code Cross-Reference

### رموز الترميز
| الكود | المشروع |
|-------|---------|
| `MOC-MUS-ASE` | Aseer Museum (متحف عسير) |
| `A2742` | Aseer Museum (رقم عقد NRS) |
| `M2742-*` | Aseer Museum (NRS series) |
| `MOC-Asser-SIC-*` | Aseer Museum (خطأ إملائي متكرر من NRS) |
| `ZAM-NWC` | Zamzam Visitor Center |
| `P083` | Zamzam Museum |
| `TF2438*` | Zamzam Museum |
| `MVii` | El-Haramain Museum (حراء للحرمين) — مدني = الحرمين، مكي = زمزم |
| `MVii Madinah` | مجسم المسجد النبوي |
| `MVii Makkah` | مجسم المسجد الحرام (في زمزم) |

### تنسيق الرمز الكامل (Aseer Museum)
```
MOC-MUS-ASE-[ORIGINATOR]-[TYPE]-[SEQUENCE]
```

| الجزء | المعنى | أمثلة |
|-------|--------|-------|
| MOC | Ministry of Culture | ـ |
| MUS | Museum project | ـ |
| ASE | Aseer region | ـ |
| Originator: 1KH | Samaya HSE/planning | PL, SC |
| Originator: 1K0 | Samaya wider | PL, ZD, RP |
| Originator: 1A0 | NRS (design) | ZD, MA, TQ |
| Originator: 1C0 | Civil works | IR |
| Originator: 1E0 | Electrical | PQ, ZD, MS |
| Originator: 1M0 | Mechanical | PL, ZD |
| Type: PL | Plan / Procedure | HSE plans |
| Type: ZD | Drawing / Design | Shop drawings |
| Type: SC | Submittal / Compliance | HSE submittals |
| Type: IR | Inspection Request | Site inspections |
| Type: TQ | Technical Query / RFI | Questions to CG |
| Type: RP | Report | Assessment reports |
| Type: MA | Material Approval | Sample boards |
| Type: PQ | Prequalification | Vendor pre-qual |
| Type: MS | Method Statement | Installation methods |
| Type: SH | Schedule | Programme |

---

## 5. Odoo — Project & Stage Structure

### Samaya Odoo Instance
| الحقل | القيمة |
|-------|--------|
| **URL** | `https://samayainv.odoo.com` |
| **Database** | `peerless-tech-samaya-18-0-18447146` |
| **User** | `sultan@samayainvest.com` |
| **Project 219** | Aseer Museum |

### Stage IDs (أودو — مشروع عسير)
| ID | الاسم | الاستخدام |
|----|-------|-----------|
| 35 | 01 Initiation | Prequal, studies, S00101 |
| 36 | 02 DD Stage | Design, plans, specialist pkgs |
| 39 | 03 Procurement | SC-01, material approvals |
| 659 | 04 Off-site Manufacturing | Replica, mfg orders |
| 40 | 05 On-site Work | Construction, site |
| 479 | 06 Handover | As-built, snagging |

### Package IDs الرئيسية
| ID | الاسم | المرحلة |
|----|-------|---------|
| 3011 | 00 — Pre-Qualification & Procurement | Init (35) |
| 3014 | 02 — Pricing & RFQs | Init (35) |
| 2945 | 00 General | DD (36) |
| 2938 | 01 Architecture | DD (36) |
| 2939 | 02 Structural | DD (36) |
| 2940 | 03 MEP & IT | DD (36) |
| 2941 | 04 Life Safety | DD (36) |
| 2946 | 05 Projects Plans | DD (36) |
| 3013 | S00101 Contract Scope | Procurement (39) |

### Tag IDs
| المعرف | الوسم |
|--------|-------|
| 140 | Prequalification |
| 141 | Plans & Procedures |
| 130 | A1-Architecture |
| 132 | S1-Structure |
| 133 | M1-MEP |
| 134 | L1-Life Safety |

---

## 6. OneDrive — هيكل المجلدات الكامل

### المسار الرئيسي للتخزين
```
~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/
└── Samaya/
    ├── Technical Office/
    │   └── Bim Unit/
    │       ├── Aseer-Museum/           ← المشروع الرئيسي
    │       │   └── ... (كما فوق في §2.1)
    │       ├── Zamzam - Visitor Center/
    │       │   ├── Submittal's/
    │       │   └── Docs/
    │       ├── Masjid Alnoor/
    │       │   └── Docs/00_Project_Charter/
    │       └── Hera' Ghar/
    │           └── Docs/00_Project_Charter/
    ├── Orders/
    │   └── 2026/031 Factory Task Tracker/
    └── _Style-Guides/
        ├── Doc Style Guide/
        └── samaya-rfi-style-guide/
```

### المسار الثانوي (Tqanny)
```
~/Library/CloudStorage/OneDrive-Personal(2)/Work/PWork/01_PROJECTS/Tqanny_Projects/
├── 01_Darin_Visitor_Center/
├── 02_Shobra/
├── 03_Albiaa/
├── 04_Al_Faw/
├── 05_Alrakaa_Center/
├── 06_Antara_Rock/
├── 07_Said_Alshohadaa/
├── 08_Tabuk_Castle/
├── DOCs/
├── Organization Chart/
└── Tenders/
```

---

## 7. Skills — الـ Skills المطلوبة للوكيل الجديد

### Core Skills (لازم تنقل)
| الاسم | المسار | الوصف |
|-------|--------|-------|
| **odoo** | `skills/software-development/odoo/` | الاتصال والتعامل مع أودو |
| **odoo-task-injection** | `skills/productivity/odoo-task-injection/` | إنشاء المهام في أودو |

### BIM Unit Skills
| الاسم | المسار | الوصف |
|-------|--------|-------|
| **samaya-technical-office** | `skills/productivity/samaya-technical-office/` | كل workflows الـ Technical Office |
| **project-email-archive** | `skills/productivity/project-email-archive/` | أرشفة الإيميلات |
| **bim-email-pipeline** | `skills/productivity/bim-email-pipeline/` | تصنيف الإيميلات حسب المشروع |
| **bim-daily-todo** | `skills/productivity/bim-daily-todo/` | المهام اليومية |
| **bulk-file-organization** | `skills/productivity/bulk-file-organization/` | تنظيم الملفات |
| **subcontractor-folder-setup** | `skills/productivity/subcontractor-folder-setup/` | إنشاء مجلدات المقاولين |
| **project-register-manager** | `skills/productivity/project-register-manager/` | إدارة سجلات Excel |
| **subcontractor-package-creation** | `skills/productivity/subcontractor-package-creation/` | إنشاء حزم المقاولين |
| **supplier-procurement-lifecycle** | `skills/productivity/supplier-procurement-lifecycle/` | دورة المشتريات |

### Other Useful Skills
| الاسم | الوصف |
|-------|--------|
| **evm-analysis-chart** | تحليل القيمة المكتسبة |
| **design-schedule-management** | إدارة جداول التصميم |
| **consultant-review-response** | مراجعة ردود الاستشاريين |
| **cv-submittal-pack** | حزم السير الذاتية |
| **nano-pdf** | تعديل PDF |
| **ocr-and-documents** | استخراج النص من PDF |
| **html-print-layout** | تنسيق HTML للطباعة |

---

## 8. الإيميلات — Outlook Setup

### قاعدة بيانات Outlook SQLite
```bash
# موقع قاعدة البيانات
~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite
```

### استعلامات مفيدة
```sql
-- بحث إيميلات حسب المشروع
SELECT Record_RecordID, datetime(Message_TimeReceived, 'unixepoch', 'localtime'),
       Message_SenderList, Message_NormalizedSubject
FROM Mail
WHERE Message_NormalizedSubject LIKE '%Aseer%' OR Message_NormalizedSubject LIKE '%ASE%'
ORDER BY Message_TimeReceived DESC
LIMIT 20;

-- إيميلات من CG
SELECT * FROM Mail
WHERE Message_SenderList LIKE '%cg.com.sa%'
ORDER BY Message_TimeReceived DESC;
```

---

## 9. خطوات نقل المعرفة لجهاز جديد

### 9.1 نسخ الـ Skills
```bash
cd ~/.hermes
tar czf samaya-skills.tar.gz \
  skills/software-development/odoo/ \
  skills/productivity/odoo-task-injection/ \
  skills/productivity/samaya-technical-office/ \
  skills/productivity/project-email-archive/ \
  skills/productivity/bim-email-pipeline/ \
  skills/productivity/bim-daily-todo/ \
  skills/productivity/bulk-file-organization/ \
  skills/productivity/subcontractor-folder-setup/

# نقل الملف للجهاز الآخر
# ثم فك الضغط:
tar xzf samaya-skills.tar.gz -C ~/.hermes/
```

### 9.2 إعداد الـ Odoo
```bash
# ملف الاعتماد
mkdir -p ~/.config/samaya
echo 'ODOO_API_KEY=<password>' > ~/.config/samaya/odoo.env
chmod 600 ~/.config/samaya/odoo.env

# اختبار الاتصال
python3 -c "
import xmlrpc.client, ssl
ctx = ssl._create_unverified_context()
t = xmlrpc.client.SafeTransport(context=ctx)
c = xmlrpc.client.ServerProxy('https://samayainv.odoo.com/xmlrpc/2/common', transport=t)
print(c.version())
"
```

### 9.3 إعداد الـ Memory
انسخ الملفات التالية للوكيل الجديد:
- ملف الـ setup الحالي (هذا الملف)
- جميع PROEJCT_MEMORY.md من المشاريع
- الـ task backlog: `Email_Archive/_aseer_tasks_backlog.md`
- الـ Document Index: `_Project_Memory/DOCUMENT_INDEX.md`

### 9.4 إعداد OneDrive
- ربط OneDrive-SAMAYAINVESTMENT
- ربط OneDrive-Personal
- تأكد من توفر نفس المسارات للمجلدات

---

## 10. ملخص — Key Contacts

| الاسم | المنصب | الإيميل / المعرف |
|-------|--------|-----------------|
| Sultan Issa | Technical Office Manager | `sultan@samayainvest.com` (Odoo uid 151) |
| Mohamed Samir | Site/Procurement | `m.samir@samayainvest.com` (uid 564) |
| Hani Alghamdi | Purchasing | `H.Alghamdi@samayainvest.com` (uid 478) |
| Hesham | Document Control | `hesham.a@samayainvest.com` (uid 163) |
| Ahmed Salah | Coordination | `ahmed.salah@samayainvest.com` (uid 162) |
| Ali Abdelrahman | Tech Office (design) | `ali.abdelrahman@samayainvest.com` (uid 160) |
| Adel Darwish | Project Manager | `adel@samayainvest.com` (uid 7) |
| Mohamed Elshaikh | Planner | `elshaikh@samayainvest.com` (uid 157) |
| Hossam Mabrouk | CG Consultant | `hmabrouk@cg.com.sa` |
| Mohammad Elbaz | CG PM | `melbaz@cg.com.sa` |

---

## 11. الملحق — الوثائق القانونية الأساسية (Aseer)

| المرجع | الوصف | رابط التخزين |
|--------|-------|-------------|
| ER R02 Rev 1.0 | Employer's Requirements (170pp) | `Design Files/Package_Part 2/05_AS_ER/` |
| SOW Rev 00 | Scope of Work (46pp) | `Contracts & ER/` |
| Main Contract | عقد Samaya مع MoC | `Contracts/01_Main_Contract/` |
| Appendix B | Subcontractor packages org chart | `Subcontractors/_assets/Appendix B.pdf` |
| DMP PL-0029 | Document Management Plan | `Docs/02_Plans_and_Procedures/` |
| Communication Plan PL-0018 | خطة التواصل | `Correspondence/` |
| Stakeholder Plan PL-0020 | خطة أصحاب المصلحة | `Correspondence/` |
| BEP | BIM Execution Plan | الصفحة 1308 في أودو |
| DIS_021 | NRS drawing register (243 drawings) | `Design Files/06_Source/` |

---

*آخر تحديث: 13 يونيو 2026*
