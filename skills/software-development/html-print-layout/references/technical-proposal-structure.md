# Technical Proposal Structure (A4 Print-Ready HTML)

Common proposal structure for construction/tender projects, built as stacked `.page` divs in a single HTML file with A4 print CSS.

## Standard Page Order (17-page template with BOQ on 2 pages)

| # | Section | Description |
|---|---------|-------------|
| 1 | Cover | Full-bleed design, project title AR+EN, client name + location, scope cards, stats |
| 2 | Table of Contents | 4 category groups with Unicode icons, anchor links to #page-N |
| 3 | Executive Summary | Company overview, project highlights, key differentiators, stat row (updated with loaded pricing total ~4.38M) |
| 4 | Scope of Work | Defined scope, deliverables, gate dimensions (vehicle 6m×8m, pedestrian 1.2m×2.1m), exclusions |
| 5 | Capabilities | Manufacturing capabilities, project references, operating model |
| 6 | Technical Specifications | Overview table: material specs, SBC-Makkah compliance, codes |
| 7 | Data Sheet · Banner & UV Printing | TDS: PVC Frontlit Flex banner 550gsm, UV print ≥1440 dpi |
| 8 | Data Sheet · Cement Board 12mm | TDS: fiber cement board 12mm, fire A1, fixing @ ≤400mm |
| 9 | Material Datasheet: Jotun Epoxy Mastic | TDS: epoxy paint system, application specs |
| 10 | Data Sheet · LED Flood Light | TDS: 300W IP66 flood light, 5000K, electrical specs |
| 11 | Technical Drawings | Reference drawings — structural calculation + hoarding option C (side-by-side or stacked) |
| **12** | **BOQ Part 1** | **Sections 01-04: Steel Structure, Civil Works, Cladding & Finish, Banner & Printing** |
| **13** | **BOQ Part 2** | **Sections 05-07: Lighting, Electrical Works, Doors & Gates + Grand Summary + OH&P note** |
| 14 | Implementation Methodology | 5-phase execution plan (11-week parallel programme) |
| 15 | Project Timeline | Gantt chart with 4-color bars, W0-W12 scale |
| 16 | Company Docs & Certifications | 15 doc-cards in 3-column grid, valid status badges |
| **17** | Payment + Warranty · شروط الدفع والضمان | 4-stage payment milestones, warranty table |
| **18** | General Conditions + Sign-Off · الشروط العامة والتوقيع | 9 terms, closing block, Client + Contractor signatures |

## BOQ Section Structure (Option C — Loaded)

The BOQ matches the Option C - BOQ (Loaded) Excel sheet exactly with 8 sections:

### SECTION 01 — STEEL STRUCTURE · الهيكل المعدني
| # | Item | Unit | Qty | Rate (loaded) | Total |
|---|------|------|-----|---------------|-------|
| 01 | Steel hoarding per m² face | m² | 11,350.4 | 110.50 | 1,254,219.20 |

### SECTION 02 — CIVIL WORKS · الأعمال المدنية
| # | Item | Unit | Qty | Rate | Total |
|---|------|------|-----|------|-------|
| 02 | PRECAST RC footing 2.75×1.50×0.60m, Fcu 300 | pc | 477 | 2,470 | 1,178,190 |

### SECTION 03 — CLADDING & FINISH · الكسوة والتشطيب
| # | Item | Unit | Qty | Rate | Total |
|---|------|------|-----|------|-------|
| 03 | Cement Board 12mm exterior grade | m² | 11,350.4 | 71.50 | 811,553.60 |
| 04 | Joint sealant + cover strip | m | 9,304 | 7.80 | 72,571.20 |
| | **Subtotal** | | | | **884,124.80** |

### SECTION 04 — BANNER & PRINTING · البانر والطباعة
| # | Item | Unit | Qty | Rate | Total |
|---|------|------|-----|------|-------|
| 05 | Printed PVC Frontlit Flex 550gsm | m² | 11,350.4 | 36.40 | 413,154.56 |

### SECTION 05 — LIGHTING · الإضاءة
| # | Item | Unit | Qty | Rate | Total |
|---|------|------|-----|------|-------|
| 06 | LED Flood Light 300W | pc | 711 | 364 | 258,804 |

### SECTION 06 — ELECTRICAL WORKS · أعمال الكهرباء والتمديدات
| # | Item | Unit | Qty | Rate | Total |
|---|------|------|-----|------|-------|
| 07 | Floodlight wiring in galv. conduit | m | 7,106.8 | 41.60 | 295,642.88 |
| 08 | Distribution panel MCB/MCCB | pc | 10 | 4,550 | 45,500 |
| | **Subtotal** | | | | **341,142.88** |

### SECTION 07 — DOORS & GATES · الأبواب والبوابات
| # | Item | Unit | Qty | Rate | Total |
|---|------|------|-----|------|-------|
| 09 | Truck/vehicle access gate | pc | 1 | 8,450 | 8,450 |
| 10 | Pedestrian access gate | pc | 1 | 2,340 | 2,340 |
| | **Subtotal** | | | | **10,790** |

### SECTION 08 — ADDITIONAL & SAFETY · أعمال إضافية وسلامة (when NOT distributed)
| # | Item | Unit | Qty | Rate | Total |
|---|------|------|-----|------|-------|
| 11 | Safety signage | pc | 29 | 156 | 4,524 |
| 12 | Mobilization / site cleanup | lot | 1 | 32,500 | 32,500 |
| | **Subtotal** | | | | **37,024** |

### GRAND TOTALS (7-section, Section 08 distributed)
| Line | Value |
|------|-------|
| Grand Total excl. VAT (with OH&P) | **4,377,449.44** |
| VAT 15% | **656,617.42** |
| **Grand Total incl. VAT** | **5,034,066.86** |

## Last Page Splitting (Payment → Sign-Off Split)

When page 17 (containing Payment + Warranty + General Conditions + Sign-off) exceeds A4, split into two balanced pages:

| Page | Content |
|------|---------|
| **17** | Payment Terms (4 milestones) + Warranty Table |
| **18** | General Conditions + Closing Block + Client Signature + Contractor Signature |

### Split points and rules
1. **Natural boundary**: split between the warranty table and the General Conditions section
2. **Closing block**: "وتفضلوا بقبول فائق التحية والاحترام" belongs on the LAST page, right before signatures
3. **Both signatures on last page**: Client (الطرف الأول) + Contractor (الطرف الثاني) — two separate `.sign` divs
4. **Order**: General Conditions → `<div class="rule">` → Closing → `<div class="rule">` → Client Signature → Contractor Signature
5. **TOC updates**: Payment stays page 17, Terms moves to page 18, Signature moves to page 18
6. **Page 16 (Company Docs)**: Keep documents-only — no closing block, no signature. All sign-off content goes to page 18.

### Sign-off block structure
```html
<div class="closing" style="margin-bottom:16px">
  <div class="ar">وتفضلوا بقبول فائق التحية والاحترام</div>
  <div class="co">سمايا الاستثمارية — Samaya Investment</div>
  <div class="w">www.samayainvest.com · الرياض، المملكة العربية السعودية</div>
</div>

<div class="rule"></div>

<div class="sign">
  <div class="sign-card">
    <div class="role">Client · الطرف الأول</div>
    <div class="party">شركة الغربية للتطوير والاستثمار المحدودة<span class="en">Al Gharbia Development &amp; Investment Co. Ltd.</span></div>
    <div class="sign-line"></div>
    <div class="sign-fields">
      <div class="f">الاسم · Name<span></span></div>
      <div class="f">التاريخ · Date<span></span></div>
      <div class="f" style="grid-column:1/-1">التوقيع والختم · Signature &amp; Stamp<span></span></div>
    </div>
  </div>
</div>

<div class="sign">
  <div class="sign-card">
    <div class="role">Contractor · الطرف الثاني</div>
    <div class="party">سمايا الاستثمارية<span class="en">Samaya Investment</span></div>
    <div class="sign-line"></div>
    <div class="sign-fields">
      <div class="f">الاسم · Name<span></span></div>
      <div class="f">التاريخ · Date<span></span></div>
      <div class="f" style="grid-column:1/-1">التوقيع والختم · Signature &amp; Stamp<span></span></div>
    </div>
  </div>
</div>
```

### Common pitfalls
- **Orphaned doc cards**: when moving content between pages, leftover `<div class="doc-card">` without a wrapping `<div class="docs-grid">` breaks the layout. Always remove the entire grid block.
- **Client sig duplication**: الطرف الأول should appear only ONCE in the entire document. If it was on page 16 before the split, it must be removed from page 16 when adding it to page 18.
- **Closing block duplication**: وتفضلوا بقبول should appear exactly ONCE — on the last page. If previously on page 16, remove it from there.
- **The `.sign` CSS class needs a closing `</div>`**: a common error is `<div class="sign">` with no matching `</div>` before the footer.

## Section 08 Cost Distribution (pro-rata redistribution)

When the user says "we distributed section 8", it means mobilization (25,000) + signage (3,480 = 28,480 base cost) are spread across all 10 priced items pro-rata:

```
Distribution factor = 28480 / 3338788.80 ≈ 0.00853
New rate = base_rate × (1 + 0.00853) = base_rate × 1.00853
```

After distribution:
- Section 08 is REMOVED entirely
- All 10 remaining items' rates increase by ~0.853%
- Grand total REMAINS 4,377,449.44
- Grand Summary now has **7 rows** (not 8)
- Example: Steel 110.50 → 111.44

### When user says "update again i changed in the excel"
Re-read the Excel — user may have tweaked formulas. The rates will shift slightly (e.g., 111.44 → something slightly different). Update every rate, total, and the grand summary. Section 08 stays removed.

## Grand Summary Table (8-section or 7-section format)

### 8-section format (with Section 08)
```html
<thead><tr><th>#</th><th>القسم · Section</th><th>الوحدة</th><th>الكمية</th><th>قبل الضريبة (SAR)</th><th>شامل الضريبة (SAR)</th></tr></thead>
<tbody>
  <tr><td>1</td><td>Steel Structure</td><td>م²</td><td>11,350.4</td><td>1,254,219.20</td><td>1,442,352.08</td></tr>
  <tr><td>2</td><td>RC Footings</td><td>عدد</td><td>477</td><td>1,178,190</td><td>1,354,918.50</td></tr>
  <tr><td>3</td><td>Cladding & Finish</td><td>م²/م</td><td>—</td><td>884,124.80</td><td>1,016,743.52</td></tr>
  <tr><td>4</td><td>Banner & Printing</td><td>م²</td><td>11,350.4</td><td>413,154.56</td><td>475,127.74</td></tr>
  <tr><td>5</td><td>Lighting</td><td>عدد</td><td>711</td><td>258,804</td><td>297,624.60</td></tr>
  <tr><td>6</td><td>Electrical Works</td><td>م/عدد</td><td>—</td><td>341,142.88</td><td>392,314.31</td></tr>
  <tr><td>7</td><td>Doors & Gates</td><td>عدد</td><td>2</td><td>10,790</td><td>12,408.50</td></tr>
  <tr><td>8</td><td>Additional & Safety</td><td>—</td><td>—</td><td>37,024</td><td>42,577.60</td></tr>
</tbody>
<tfoot>
  <tr class="sub"><td colspan="4">Total (excl. VAT)</td><td>4,377,449.44</td><td>—</td></tr>
  <tr class="vat"><td colspan="4">VAT 15%</td><td>656,617.42</td><td>—</td></tr>
  <tr class="grand"><td colspan="5">GRAND TOTAL (incl. VAT)</td><td>5,034,066.86</td></tr>
</tfoot>
```

### 7-section format (Section 08 distributed)
Remove row 8. Update all subtotals with redistributed rates. Example after distribution:

| Row | Section | excl. VAT | incl. VAT |
|-----|---------|-----------|-----------|
| 1 | Steel Structure | 1,264,917.74 | 1,454,655.40 |
| 2 | RC Footings | 1,188,240.01 | 1,366,476.01 |
| 3 | Cladding & Finish | 891,666.42 | 1,025,416.38 |
| 4 | Banner & Printing | 416,678.78 | 479,180.60 |
| 5 | Lighting | 261,011.61 | 300,163.35 |
| 6 | Electrical Works | 344,052.84 | 395,660.77 |
| 7 | Doors & Gates | 10,882.04 | 12,514.35 |

## Table of Contents Design Pattern

### 4 category groups with Unicode icons

| Group | Items | Icon |
|-------|-------|------|
| **Project Introduction** · مقدمة المشروع | Cover, Executive Summary | 📋📊 |
| **Technical Scope** · النطاق الفني | Scope, Tech Specs & Datasheets (6-10), Lighting & Technical Drawings (10-11), BOQ | 🔧📐💡📦 |
| **Execution Plan** · خطة التنفيذ | Timeline | 📅 |
| **Company & Commercial** · الشركة والعرض التجاري | Team, Payment, Terms, Signature | 🏢💰⚖️✍️ |

### Icon map
📋 Cover · 📊 Executive Summary · 🔧 Scope · 📐 Tech Specs & Datasheets · 💡 Lighting & Drawings · 📦 BOQ · 📅 Timeline · 🏢 Team · 💰 Payment · ⚖️ Terms · ✍️ Signature

### Key TOC rules
- **Technical Specifications + Material Datasheets are ONE section** — never split them in TOC. TOC shows "6-10".
- **Lighting + Technical Drawings** — one TOC entry under Technical Scope ("10-11"), NOT under Execution Plan.
- TOC count: 11 items (excludes Cover page 1 and TOC page 2).
- **Verify page numbers after every structural edit** — TOC hrefs and toc-page values drift easily.

## Cover Page Background (Print Mode)

```css
@media print {
  .page::before { display: none !important; }  /* hide decorative clouds */
  .cover-wrap::before {
    background: linear-gradient(180deg, #F6F8FC 0%, #EDEEF2 100%) !important;
    display: block !important; content: "" !important;
    opacity: 1 !important;
  }
  .page.cover { background: #fff !important; padding: 0 !important; }
  .cover-wrap { min-height: 1123px !important; }
}
```

## Stale Price References (Check After Every BOQ Update)

After updating loaded/distributed rates, check these stale references:

| Location | Before | After |
|----------|--------|-------|
| Cover scope card: Steel rate | `SAR 85/m²` | `SAR 110.50/m²` (or 111.44 after distribution) |
| Executive Summary stat | `3.37 M SAR (excl. VAT)` | `4.38 M SAR (loaded rates)` |
| BOQ section subtitles | `@ 364` | `@ 367.10` (after distribution) |
| BOQ section subtitles | `@ 110.50` | `@ 111.44` (after distribution) |

## 11-Week Timeline

| Phase | Duration | Weeks | Percent |
|-------|----------|-------|---------|
| Shop Drawings + Approvals | 2 wk | W1-W2 | 10% |
| Steel Fabrication (factory) | 5 wk | W2-W6 | parallel |
| Precast Footings + Civil | 3 wk | W3-W5 | 20% |
| Steel Erection + Cladding + Banner | 5 wk | W5-W9 | 45% |
| LED Lighting + Electrical | 4 wk | W7-W10 | 20% |
| Inspection + Handover | 1 wk | W11 | 5% |
| **Total** | **11 weeks** | | |

Gantt bars: `.gantt-bar.prep` (charcoal), `.exec` (red), `.civ` (amber #D97706), `.elec` (teal #0D9488)
