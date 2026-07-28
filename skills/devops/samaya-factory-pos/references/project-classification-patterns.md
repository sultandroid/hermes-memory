# Project Classification Patterns (from Vendor Reference)

When the user asks to group Samaya Factory POs by project, extract the project name from the `partner_ref` (vendor reference) field. The field contains Arabic/English project names embedded in free-form text.

## Regex Patterns (ordered by priority — first match wins)

These are defined in `def classify_ref(ref)` in `scripts/build_factory_by_project.py`.

| Pattern | Group Label | Example Matches |
|---------|-------------|-----------------|
| `Jalal.*(?:Jabal Omer\|جبل عمر)` | Jalal & Jamal - Jabal Omer | "Jalal & Jamal - Jabal Omer - طلب شراء دهانات" |
| `Maalim.*(?:Jabal Omer\|جبل عمر)` | Maalim Al-Haramein - Jabal Omer | "Maalim Al-Haramein- Jabal Omer - عمالة خارجية" |
| `متاجر الغمامة` | متاجر الغمامة | "متاجر الغمامة - متجر الهدايا - اخشاب" |
| `متجر الهدايا.*(?:معالم الحرمين\|جبل عمر)` | متجر الهدايا - معالم الحرمين | "متجر الهدايا - معالم الحرمين- جبل عمر - قشرة سنديان" |
| `متحف عسير` | متحف عسير الإقليمي | "متحف عسير الإقليمى - طلب شراء لحديد السور" |
| `متحف القرآن\|القران الكريم` | متحف القرآن الكريم | "متحف القرآن الكريم - فريمات خشب سوليد" |
| `متحف خير الخلق` | متحف خير الخلق | "متحف خير الخلق - بوديوم حفل التدشين" |
| `متحف الغمامة` | متحف الغمامة | "متحف الغمامة - المرحلة الأولي - ريش خاصه بمكائن السي ان سي" |
| `متحف معالم المسجد الحرام\|معالم المسجد الحرام` | متحف معالم المسجد الحرام | "متحف معالم المسجد الحرام - جبل عمر - مكة المكرمة" |
| `زمزم\|Zamzam` | Zamzam - متحف زمزم | "مشروع زمزم" |
| `هدايا طيبه` | متجر هدايا طيبة | "مجسمات ثري دي لمشاريع هدايا طيبه" |
| `غار حراء\|المركز الإعلامي\|حراء` | المركز الإعلامي - حراء | "مصاريف تشغيلية - نقل وتركيب غار حراء" |
| `جبل عمر` | جبل عمر (عام) | Catch-all for generic Jabal Omer references |
| `المصنع\s*-?\s*(?:كشف\|مستلزمات\|مواد\|طلب\|جلفزات\|مصاريف)?` | المصنع (تشغيلي) | "المصنع - طلب شراء بيرنج و شفاطات" |
| `مصاريف بدل اعاشة\|بدل اعاشة\|مصاريف تشغيلية\|مصروفات الإعاشة` | مصاريف تشغيلية | Operational expenses |
| `عمالة خارجية` | عمالة خارجية | Outsourced labor |
| `مدفوع من العهده\|مدفوع م العهده\|مدفوعه` | عهدة إبراهيم | Paid from Ibrahim's allowance (58 POs) |
| `Expenses Statement` | مصاريف تشغيلية | "Expenses Statement-كشف حساب مصروفات" |
| `Outsorce\|عمالة` | عمالة خارجية | "Outsorce Labor - Makkah" |

## Key Observations

- **58 POs** (~30,423 SAR) have `مدفوع من العهده` — these are small-value POs paid from Ibrahim's petty cash. They show as unpaid in Odoo but are actually settled.
- The المصنع (تشغيلي) group (14 unpaid POs) contains factory-operational items — bearings, machine coolant, gloves, running costs.
- The `partner_ref` field is the ONLY reliable place to determine which real-world project a Factory PO serves. The Odoo `project_id` is always 244 (Samaya Factory).

## Adding New Patterns

When a new project name appears in vendor references, add it to both:
1. The `classify_ref()` function in the script
2. This reference file

New patterns should be added ABOVE the catch-all patterns (جبل عمر (عام) and أخرى / Other) to ensure specificity wins.
