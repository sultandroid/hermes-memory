# Bilingual (Arabic/English) Document Template

Use for all Saudi government client submissions (Heritage Commission, MoC, NWC, etc.).

## HTML Structure

```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>Doc Code · Title</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Tajawal','Calibri','Carlito','Arial','Helvetica',sans-serif; }
  /* Same .sheet / .doc-strip / .page-footer as Samaya CV Pack */
  .en { direction: ltr; unicode-bidi: isolate; }  /* for inline English terms */
</style>
</head>
```

## Doc-Strip Format (Bilingual)
```
<DOC-CODE> · Arabic Title · <span class="en">English Title</span> · صفحة NN من NN · Rev NN · YYYY-MM-DD
```

## Content Pattern
Each section: Arabic heading first, then English heading, then content.

```html
<h2>القسم الأول: نبذة عن المشروع</h2>
<h2 class="en">Section 1: Project Overview</h2>
<p>متن عربي هنا...</p>
<p class="en">English text here...</p>
```

## Font Stack
- Primary: Tajawal (Google Fonts) for Arabic
- Fallback: Calibri/Carlito for English
- Numbers: use `.num` class with LTR isolation

## Cover Page
- Arabic title first, large
- English subtitle below, smaller
- Meta-grid labels in Arabic with `.en` class for values
- QC block: أعدها / راجعها / اعتمدها (Prepared/Reviewed/Approved)
