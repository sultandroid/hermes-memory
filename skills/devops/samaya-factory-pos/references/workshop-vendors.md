# Workshop Vendors — Samaya Factory PO Filtering

Comprehensive list of vendor names used to identify workshop/factory POs when `project_id` filtering is insufficient. These vendors supply carpentry, paint, fiber, metal, upholstery, wood, veneer, outsourcing, and expenses for the Samaya Factory.

## Core Workshop Vendors (Arabic)

| Vendor Name (Arabic) | Type | Notes |
|---|---|---|
| ورشة مفاهيم خشبية للنجارة | Carpentry workshop | Upholstery, furniture |
| شركة الاخشاب الفاخرة للمقاولات | Wood/veneer supplier | Natural veneer |
| شركة امداد التوريد الحديثة للتجارة | Wood/MDF supplier | Modern Imdad Co |
| شركة الشعبية الاولى التجارية | Site finishing | On-site finishing works |
| شركة جفن الالوان للتجارة | Paint/acrylic | Acrylic sheets, paints |
| دهانات الجزيرة | Paint supplier | |
| شركة الواح الخليج التجاري | Composite panels | |
| شركة خليجنا للتجارة | Upholstery supplies | |
| مؤسسة التوتنجي للتجارة | Wood frames | AL-Totongy Trading |
| شركة جي 4 تيك | IT/display fabrication | G4 TECH |
| مؤسسة اثمان العاصمه للتجارة | Connectors/hardware | |
| مؤسسة صروح الخالدية التجارية | Pipes/materials | |
| شركة انظمة الرنين المتقدمة للتجارة | Glass/display stands | |
| شركة عبدالعزيز رشيد الرشيد التجارية | Adhesives/glue | |
| مؤسسة آرت آند ستيشنري | Stationery/art supplies | Arta And Stationery |
| مصنع شركة اعمال الابتكار للصناعة | Marble fabrication | |
| مؤسسة مدى الجزيرة للتجارة | Metal pipes/tubes | Credit supplier |
| صبا نجد- Saba Najad | Paints/materials | Credit supplier |
| شركة ندرة للمعدات الصناعية | Industrial equipment | Nudrah Industrial Equipment |
| مؤسسة التحويل الفني | Technical conversion | Altahwel Alfani Est |
| شركة دار النجارة للتجارة | Carpentry trade | Dar Alnajara |
| شركة وصف الجزيرة للتجارة لاقمشة | Upholstery fabrics | |
| مؤسسة الفن الذهبي للمعدات الصناعية | Industrial equipment | |
| Nerfa Est. مؤسسة نيرفا التجارية | LED lighting | |
| وقت النجوم للبلاستيك | Plastic products | |
| شركة ديار الهمة للتجارة | General supplies | |
| شركة قلف سباروز تريدينج | Acrylic/signage | Gulf Sparrows Trading |
| شركة واجهات ذكية للتجارة | Smart facades | ZMCO |
| شركة نسيم الصفوة المتقدمه | General supplies | Naseem |
| شركة دار الفاء للتجارة للجلوود | Wood/glue | |
| شركة ديار الهمة للتجارة | General supplies | |
| مؤسسة همسات النيل للتجارة | General supplies | |
| المعدات المتينه -DIMAC | Industrial equipment | Machine cleaning fluid |
| Creative Consultant-مستشار الابداع | Adhesives/glue | |
| مؤسسة فوزي بن محمد الهندي التجارية | Machine maintenance | Laser machine repair |

## Core Workshop Vendors (English/Latin)

| Vendor Name | Type | Notes |
|---|---|---|
| Sigma Machines | Laser/engraving machines | Fiber laser marking machine |
| AMAZON ONLINE | Online purchases | Tools, paint, tablets |
| Outsorce Labor | Labor outsourcing | Makkah/Jeddah site labor |
| Outsorce Labor - Makkah- Ahmed Mukhtar | Labor outsourcing | |
| Outsorce Labor - Makkah- Mohammed | Labor outsourcing | |
| Expenses Statement-كشف حساب مصروفات | Expense reimbursement | Staff expenses, allowances |
| Bodour Abdul Rehman Ibrahim Al Shamrani TRD EST | Printer/supplies | |

## Python Filter Code

```python
workshop_vendors = [
    'ورشة', 'مفاهيم خشبية', 'نجارة', 'دهان', 'فايبر', 'حدادة', 'تنجيد',
    'اخشاب', 'قشرة', 'المنشار', 'النجارة', 'مصنع', 'Sigma Machines', 'AMAZON ONLINE',
    'Outsorce Labor', 'Expenses Statement', 'Bodour Abdul Rehman', 'ندرة', 'امداد التوريد',
    'الشعبية الاولى', 'انظمة الرنين', 'التوتنجي', 'جي 4 تيك', 'اثمان العاصمه',
    'صروح الخالدية', 'الاخشاب الفاخرة', 'خليجنا', 'جفن الالوان', 'الواح الخليج',
    'آرت آند ستيشنري', 'اعمال الابتكار', 'عبدالعزيز رشيد', 'التحويل الفني',
    'دار النجارة', 'وصف الجزيرة', 'الفن الذهبي', 'نيرفا', 'وقت النجوم',
    'ديار الهمة', 'قلف سباروز', 'واجهات ذكية', 'نسيم الصفوة', 'دار الفاء',
    'همسات النيل', 'المتينه', 'Creative Consultant', 'فوزي بن محمد',
    'Bodour Abdul Rehman', 'Sigma Machines', 'AMAZON ONLINE',
    'Outsorce Labor', 'Expenses Statement'
]

def is_workshop_po(po):
    partner = po.get('partner_id', ['', ''])
    pname = partner[1] if isinstance(partner, list) and len(partner) > 1 else ''
    pname_lower = pname.lower()
    return any(kw.lower() in pname_lower for kw in workshop_vendors)
```

## Usage

When the user asks to check/update workshop POs:
1. Fetch all POs from Odoo (state in `['purchase','done']`, 2026 onwards)
2. Filter: `project_id == 244` (Factory) OR `is_workshop_po(po)` (workshop vendor)
3. Deduplicate by PO id (a PO can be both Factory and workshop)
4. Cross-reference bills via `account.move.read()` for real payment status
5. Update the workshop purchasing tracker (`ورشة المشتريات.xlsx`) with Odoo Pay State and Bills columns
