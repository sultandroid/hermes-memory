---
name: po-approval-workflow
title: PO Approval Workflow — مطابقة عروض الأسعار قبل الاعتماد
description: Before approving any Purchase Order, match quotations against PO lines, verify totals, check price ranges, update product costs, and add supplier info. Enforces the pre-approval checklist.
triggers:
  - User says "اعتماد أمر شراء" / "approve PO"
  - User says "مطابقة عروض الأسعار" / "match quotations"
  - User asks to review a PO before approval
  - PO approval workflow check
---

# PO Approval Workflow — مطابقة عروض الأسعار

## 🚫 القاعدة الأساسية

**لا يتم اعتماد أي أمر شراء قبل استيفاء جميع بنود المطابقة التالية.**

## ✅ قائمة المطابقة الإلزامية (قبل الاعتماد)

| # | البند | الوصف | المسؤول |
|---|-------|-------|---------|
| 1 | **عرض سعر** | طلب عرض سعر من المورد (PDF/صورة) وإرفاقه في الشات | المشتري |
| 2 | **مطابقة الأسعار** | مقارنة أسعار العروض مع أسعار البنود في أودو — يجب التطابق | المشتري |
| 3 | **مطابقة الإجمالي** | التأكد من أن إجمالي أمر الشراء = مجموع بنوده = إجمالي عرض السعر | المشتري |
| 4 | **رنج السعر** | التأكد من أن سعر الوحدة ضمن المعدل الطبيعي مقارنة بـ standard_price | المشتري |
| 5 | **تحديث الخامة** | تحديث list_price في product.template بسعر الشراء الجديد | المشتري |
| 6 | **إضافة المورد** | إضافة المورد في seller_ids للخامة (product.supplierinfo) | المشتري |
| 7 | **تعليق في الشات** | كتابة تأكيد المطابقة في شات الأمر قبل طلب الاعتماد | المشتري |

## 🔍 خطوات المطابقة التفصيلية

### 1. عرض السعر
- استلام عرض سعر من المورد (PDF، صورة واتساب، إيميل)
- رفع العرض في شات أمر الشراء

### 2. مطابقة الأسعار
```
لكل بند في PO:
  سعر_العرض == price_unit في order_line
  الكمية == product_qty
```

### 3. مطابقة الإجمالي
```
مجموع (price_subtotal) == amount_total في PO
مجموع (price_subtotal) == إجمالي عرض السعر
```

### 4. رنج السعر الطبيعي
```
لكل بند:
  standard_price (التكلفة السابقة) ← مرجع
  price_unit (سعر الشراء الجديد) ← يجب أن يكون ضمن ±20% من standard_price
  لو الفرق كبير → استفسار من المشتري
```

### 5. تحديث سعر الخامة في أودو

**الخطوات في واجهة أودو:**
1. افتح المنتج من رابط `product.product/{ID}` (موجود في بنود أمر الشراء)
2. اذهب إلى tab **"General Information"**
3. حقل **"Sales Price"** (`list_price`) ← أدخل `price_unit` (سعر الشراء الجديد)
4. **Save**

**أو عبر XML-RPC:**
```python
models.execute_kw(db, uid, pw, 'product.product', 'write',
    [[product_id]], {'list_price': price_unit})
```

**لماذا؟** — عشان سعر الخامة في أودو يعكس آخر سعر شراء، وده مهم لـ:
- تقييم المخزون
- حسابات التكلفة
- تقارير الربحية
- منع شراء نفس الخامة بسعر مختلف بدون مراجعة

### 6. إضافة المورد للخامة في أودو

**الخطوات في واجهة أودو:**
1. افتح المنتج من رابط `product.product/{ID}`
2. اذهب إلى tab **"Purchase"**
3. تحت **"Vendors"** (`seller_ids`) ← **"Add a line"**
4. أدخل:
   - **Vendor**: اسم المورد (اختيار من القائمة)
   - **Product Name**: اسم المنتج عند المورد (كما في عرض السعر)
   - **Product Code**: كود المنتج عند المورد (كما في عرض السعر)
   - **Price**: `price_unit` (سعر الوحدة من أمر الشراء)
   - **Delivery Lead Time**: مهلة التوريد بالأيام
   - **Min Quantity**: 1 (أو الحد الأدنى للطلب)
5. **Save**

**أو عبر XML-RPC:**
```python
# أولاً: تأكد إن المورد مش مضاف قبل كده
existing = models.execute_kw(db, uid, pw, 'product.supplierinfo', 'search',
    [[['product_tmpl_id', '=', product_tmpl_id], ['partner_id', '=', partner_id]]])
if not existing:
    models.execute_kw(db, uid, pw, 'product.supplierinfo', 'create', [{
        'product_tmpl_id': product_tmpl_id,
        'partner_id': partner_id,
        'product_name': vendor_product_name,  # اسم المنتج عند المورد
        'product_code': vendor_product_code,  # كود المنتج عند المورد
        'price': price_unit,
        'delay': lead_time_days,
        'min_qty': 1,
    }])
else:
    # تحديث السعر والبيانات إذا المورد موجود
    models.execute_kw(db, uid, pw, 'product.supplierinfo', 'write',
        [existing, {
            'price': price_unit,
            'product_name': vendor_product_name,
            'product_code': vendor_product_code,
        }])
```

**لماذا؟** — عشان:
- في المرة الجاية لما نشتري نفس الخامة، أودو يقترح المورد تلقائياً
- نقارن أسعار الموردين بسهولة
- منع شراء من مورد جديد بدون تسجيله

### 7. تأكيد المطابقة
نشر تعليق في شات PO:
```
✅ تمت المطابقة:
- عرض السعر مرفق
- الأسعار متطابقة
- الإجمالي متساوي
- السعر ضمن الرنج الطبيعي
- تم تحديث سعر الخامة
- تم إضافة المورد
```

## 📊 مثال عملي — P02264 (امداد التوريد)

| المنتج | الكمية | سعر الوحدة | الإجمالي | standard_price | مطابق؟ |
|--------|:-----:|:----------:|:--------:|:-------------:|:------:|
| Sweden Solid Wood | 1 | 1,700 | 1,700 | 2,392 | ✅ |
| MDF FR 7 mm | 65 | 75 | 4,875 | 19 | ⚠️ فرق كبير |
| MDF FR 18 mm | 65 | 120 | 7,800 | 115 | ✅ |
| MDF 18 mm عادي | 65 | 73 | 4,745 | 65 | ✅ |
| MDF 7 mm عادي | 65 | 38 | 2,475 | 38 | ✅ |
| **الإجمالي** | | | **24,828** | | |

## ⚠️ ملاحظات
- **Odoo READ-ONLY** — تحديث list_price و seller_ids مسموح به لأنه بيانات تسعير وليس هيكل نظام
- **لا اعتماد بدون مطابقة** — أي PO يتم اعتماده بدون مطابقة يعتبر خطأ إجرائي
- **بأثر رجعي** — يتم تطبيق القاعدة على جميع POs المستقبلية + تصحيح السابقة عند الحاجة

## 🔗 Related Skills
- `factory-operations` — umbrella skill for factory management, PO classification, payment tracking, and PO-by-PO review workflow (كشف رؤوف)
- `odoo` — Odoo connection, field schemas, SSL fix

## ⚠️ Pitfalls
- **خدمة (عمالة) لا تحتاج مطابقة** — POs من نوع Outsource Labor / عمالة خارجية لا ينطبق عليها تحديث سعر خامة أو إضافة مورد. فقط اعتماد + صرف.
- **العهدة (كشف مصروفات)** — POs من نوع كشف مصروفات نقدية لا تحتاج مطابقة أسعار. فقط اعتماد + صرف.
- **عرض السعر لازم يكون مرفق في الشات** — بدون عرض سعر، لا يمكن المطابقة. اطلب من المشتري إرفاقه قبل البدء.
- **vendor product name و vendor product code** — إجباري عند إضافة المورد للخامة. خذها من عرض السعر نفسه.
- **المواد قد تكون مستلمة قبل الاعتماد** — في بعض POs، المواد بتوصل قبل ما تعتمد أنت. هذا خطأ إجرائي. المطابقة لازم تكون قبل الاعتماد مش بعد الاستلام.
