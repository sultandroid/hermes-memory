# Aseer Email Archive — Categorization Decision Tree

Generated during the Aseer Museum (Project 3092) archive migration. This is the exact logic used to classify 308 flat files into 12 categories. Use as a reference when migrating any Samaya project email archive.

## Priority Order (first match wins)

### 1. MOC Document Codes (explicit overrides) → DOC
Any file containing these MOC prefixes → `DOC`:
- `MOC-MUS-ASE-1K0-PL-xxxx` → DOC (plans: DMP, Comm Plan, Fire Prevention, Workers Welfare, Site Security)
- `MOC-MUS-ASE-1KH-SC-xxxx` → DOC (HSE Deliverables)
- `MOC-MUS-ASE-1E0-MS-xxxx` → DOC (Method Statements)
- `MOC-MUS-ASE-1E0-PQ-xxxx` → DOC (Vendor approvals)
- `MOC-MUS-ASE-1A0-ZD-xxxx` → DOC (Renders, samples, audit reports, demolition plans)
- `MOC-MUS-ASE-1K0-ZD-0030` → DOC (Glasbau Hahn presentation)

### 2. Material Submissions → MAR
- `MA-xxxx` in filename (showcases materials, finishes)

### 3. Site Inspections / As-Built → IR
- `1V0-IR-xxxx` pattern (site survey, As-Built verification by Namaa)
- MEP Design Services requests / proposals
- AV Meeting / AV Drawing submissions

### 4. Site Instructions → SI
- `SI-CG-ASEER-007` pattern (any revision, Rev.01, Rev.02)

### 5. Schedules → SCH
- `0PS-SH-xxxx` pattern (time schedules)
- `GBH` + `time schedule` in filename
- `جدول الكميات` (BOQ schedule)

### 6. Shop / IFC Drawings → SDR
- `IFC-xxxx` pattern in filename (IFC drawing packages)

### 7. Requests for Information → RFI
- `RFI` anywhere in filename (uppercase)
- `GBH RFIs #x` pattern
- `Project Query Tracker`
- `Open RFIs`

### 8. Technical Proposals / Price Quotes → RFP
- `Artec` (replica fabrication RFQs)
- `RFQ` (uppercase)
- `JOCAVI` / `Bluehaus` (vendor quotes)
- `مقارنة عروض اسعار` (price comparison)
- `حافظات العرض` (showcases pricing)
- `P01112` (price requests)
- `MEP Design Services` proposals

### 9. Meeting / Progress Reports → REP
- `🗓` calendar emoji prefix in filename
- `ReadAI_Weekly_Recap`
- `Weekly Kickoff`
- `التقرير اليومي` (daily report)

### 10. Catch-All → GEN
Everything else. This is correct and expected. GEN is NOT a failure state — it is the category for:
- Car / transport requests (`طلب سيارة`, `نقل مواد`, `نقل فنيين`)
- Personnel requests (`طلب توفير فنيين`)
- Anonymous access link notifications
- Odoo task assignment / comment notifications
- Hourly Notifications / ASEER INTERNAL
- Price comparisons, contractor selection (before formal RFP)
- Company profiles, NRS/Nissen Richards correspondence
- `Undeliverable` bounce notifications
- `Accepted` / Stage 4 remarks (review acknowledgments)
- Internal design coordination (`أعمال الجرافيك`, `المواصفات العامة`)
- `Core Samples`, `Type 3 showcases` discussion

## GEN is Normal — Do Not Over-Classify

Active projects generate far more coordination traffic (logistics, personnel, access) than formal submittals. A GEN folder of 100–200 files with 50–100 formal submittals in coded folders is a healthy archive. The goal is that everything is findable and dated — not that GEN is empty.

## Actual Aseer Distribution (May 2026 migration)

| Category | Count | Notes |
|---|---|---|
| GEN | 134 | Administrative, logistics, Odoo notifications |
| DOC | 54 | Plans, DMPs, HSE, invoices, vendor approvals |
| RFP | 33 | Artec RFQs, price comparisons, Bluehaus, JOCAVI |
| REP | 29 | Weekly/BIM meetings, daily reports, kickoffs |
| IR | 18 | MEP services, site survey, AV drawings |
| SDR | 14 | IFC drawing packages (Showcases, Flooring, Life Safety, etc.) |
| RFI | 10 | Technical queries, GBH RFIs |
| SCH | 8 | GBH time schedules, BOQ schedule |
| SI | 5 | SI-CG-ASEER-007 (all revisions) |
| MAR | 3 | Showcase material submissions |
| WIR | 0 | No work initiation requests yet |
| MIR | 0 | No on-site material inspections yet |
| **Total** | **308** | |

## Dashboard Generation (Python)

```python
import csv, html as html_mod
from pathlib import Path
from collections import defaultdict, OrderedDict
from datetime import datetime

CAT_NAMES = OrderedDict([
    ('DOC','تقديم مستندات'), ('IR','طلبات استلام الأعمال'),
    ('MAR','اعتماد مواد وعينات'), ('MIR','فحص مواد بالموقع'),
    ('RFP','مقترحات فنية'), ('RFI','استفسارات'),
    ('SI','ملاحظات الموقع'), ('SCH','الجداول الزمنية'),
    ('SDR','المخططات التنفيذية'), ('WIR','طلبات بدء الأعمال'),
    ('REP','التقارير والخطط'), ('GEN','رسائل عامة'),
])

cat_colors = {
    'DOC':'#2ecc71','IR':'#1d9bf0','MAR':'#f59e0b','MIR':'#34d399',
    'RFP':'#7c3aed','RFI':'#ef4444','SI':'#06b6d4','SCH':'#84cc16',
    'SDR':'#f97316','WIR':'#a78bfa','REP':'#ec4899','GEN':'#4b5563'
}
```

See `Dashboard_مشروع متحف عسير الإقليمي.html` in the project folder for the complete dark-theme template.