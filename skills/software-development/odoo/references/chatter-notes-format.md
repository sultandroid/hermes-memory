# Chatter Notes Format — Mandatory Rules

## Core Rule

Post notes to Odoo chatter (`message_post`) as **plain text only** — no icons, no tags, no markdown.

## Do's and Don'ts

| ✅ Correct | ❌ Wrong |
|-----------|---------|
| `[تأكيد المخزن] تم استلام هذا الأمر على مخزن المصنع لكن طلب الشراء (P02247) يخص مشروع: جبل عمر — وليس المصنع.` | `⚠️ تم استلام هذا الأمر على @مخزن المصنع لكن طلب الشراء (P02247) لا يخص المصنع — المشروع: **جبل عمر**` |
| `[PO Update] PO P02256 is now confirmed. Total: 10,292.50 SAR.` | `✅ PO P02256 confirmed! @all check it out` |
| `تم تحديث حالة الطلب إلى معتمد.` | `🔄 تم تحديث حالة الطلب إلى ✅ معتمد` |

## Rules

1. **No emoji/icons** — no ⚠️ ✅ ❌ 🔄 ❓ 🗑 📝 ⏳
2. **No tags/mentions** — no @username, @all, @everyone
3. **No markdown** — no **bold**, *italic*, `code`, ~~strikethrough~~
4. **No HTML formatting** — wrap in `<p>` tags only if needed for Odoo rendering
5. **Short and direct** — like a human message, not a system notification
6. **Arabic first** for Arabic-speaking users, then English if needed

## Python Implementation

```python
# Correct way to post a note
models.execute_kw(ODOO_DB, uid, ODOO_KEY, 'stock.picking', 'message_post',
    [picking_id], {
        'body': '<p>[تأكيد المخزن] تم استلام هذا الأمر على مخزن المصنع لكن طلب الشراء (P02247) يخص مشروع: جبل عمر — وليس المصنع.</p>',
        'message_type': 'comment'
    })
```

## Why

The user explicitly stated:
- "الملاحظه المكتوبه فالشاتر كلها اوسمه غير مقرؤه" — tags/icons are unreadable
- "اسلوب وضع الملاحظات فالشاتر اتفقنا انه يكون مختصر جدا بدون ايكونات بدون اوسمه يكون مثل الانشان" — notes must be short, no icons, no tags, like a human message
