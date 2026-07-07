# June 14, 2026 — Daily TODO Output (2-Line Arabic Format)

Produced by the cron job at 8:00 AM Riyadh on Sunday June 14, 2026.

## Data Sources Used

| Source | Status | Notes |
|--------|--------|-------|
| Aseer CSV (`Register_ASEER_Professional.csv`) | ✅ Readable (284 rows) | Stale — latest entries May 28. No entries in last 7 days |
| Zamzam CSV (`Project_Log_...زمزم.csv`) | ✅ Readable (983 rows) | Stale — latest entries March 31. No entries in last 7 days |
| Watchdog state (`~/.hermes/scripts/.watchdog_state.json`) | ✅ Used (4.6MB) | 131 files changed since June 11 |

## Key Decisions

- **Aseer register**: Active items from May 19-28 used as backlog since no June entries exist
- **Zamzam register**: No recent entries → relied entirely on watchdog for Zamzam items
- **Consolidation**: Grouped related SDR plans into single items (e.g. "HSE Notices: 3 plans", "Fire + Emergency: 2 plans")
- **Format**: 2-line format with Arabic script actions
- **Capping**: 15 items total (6 HIGH + 6 MEDIUM + 3 LOW)

## Full Output

```
📋 *DAILY TODO — 2026-06-14*
الإجمالي: *15* بند

🔴 *HIGH PRIORITY (6)*
1. [🏛️ متحف عسير] RFQ — ماسح Artec Space Spider (تصنيع النسخ)
   اعتماد عرض السعر | RFP | 25 مايو
2. [🏛️ متحف عسير] خدمات التصميم الميكانيكي — عرض Bluehaus
   اتخاذ قرار | IR | 20 مايو
3. [🏛️ متحف عسير] خطة الوقاية من الحريق (PL-0036) + خطة الطوارئ (PL-0041)
   مراجعة واعتماد (2) | SDR (حريق/طوارئ) | 24 مايو
4. [🏛️ متحف عسير] مستندات السلامة: لوحة البلاغات (ZD-0044) + أمن الموقع (PL-0040) + البيئة (SC-0035)
   مراجعة واعتماد (3) | SDR (سلامة) | 25 مايو
5. [🏛️ متحف عسير] خطة إدارة الكهرباء المؤقتة (PL-0043)
   مراجعة واعتماد | SDR (كهرباء) | 25 مايو
6. [🏛️ متحف عسير] خطة رعاية العمال (PL-0037)
   مراجعة واعتماد | SDR (عمال) | 20 مايو

🟡 *MEDIUM PRIORITY (6)*
1. [🕋 متحف زمزم] عرض سعر رقم 3451 — متحف زمزم (وصل 13 يونيو)
   مراجعة عرض السعر | RFP | 13 يونيو
2. [🏛️ متحف عسير] ملفات تصميم جديدة — 13 RFI/TQ/عروض (11-12 يونيو)
   مراجعة الملفات الجديدة | Design Drop | 12 يونيو
3. [🕋 متحف زمزم] SDR-AR-033 Rev.00 — تقديم معماري
   مراجعة التقديمة | SDR | 09 يونيو
4. [🏛️ متحف عسير] تقديمة 11 — رسومات واجهات العرض (SC_01/SC_02) معتمدة من NRS
   مراجعة | SDR | 25 مايو
5. [🏛️ متحف عسير] تعليمات موقع (SI-007) + تقييم BMS (RP-0039) + مواقع كاميرات (ZD-0038)
   مراجعة (3) | SI/SDR | 21 مايو
6. [🏛️ متحف عسير] الجدول الزمني المحدث GBH + خطة إدارة أصحاب المصلحة (PL-0020)
   مراجعة/اعتماد | SCH/SDR | 13 مايو

🟢 *LOW PRIORITY (3)*
1. [🏛️ متحف عسير] G11/G13 — تنسيق الإضاءة والصوت والتكييف
   مراجعة رسومات التنسيق | GEN | 28 مايو
2. [🏛️ متحف عسير] فاتورة NRS-SAM-2026-004 — معالجة الدفع
   معالجة الدفع | مالي | 28 مايو
3. [🏛️ متحف عسير] اختبار العرض البصري G6 + رسومات واجهات العرض المحدثة
   مراجعة | GEN/SDR | 15 مايو
```

## Watchdog Files (Changed June 11-14)

131 files changed since June 11. Key groupings:

| Group | Count | Date | Classification |
|-------|-------|------|----------------|
| RFIs/TQs (MOC-ASEER-SIC-1A0-TQ-*, RFI-*) | 8 files | Jun 11 | Design Drop → MEDIUM |
| 3D scanner quotations (Artec, Faro, Ray, RTC360) | 5 files | Jun 12 | RFP → HIGH |
| Aseer Communication Plan RevC02 | 1 file | Jun 13 | DOC → MEDIUM |
| Zamzam Quotation NO.3451 | 1 file | Jun 13 | RFP → MEDIUM |
| Zamzam SDR-AR-033 Rev.00 | 1 file | Jun 9 | SDR → MEDIUM |
| Structural design study (Arabic proposal) | 1 file | Jun 12 | RFP → HIGH |
| Product compliance / infrastructure utilities | 2 files | Jun 12 | GEN → LOW |
| Zamzam wall tiles (PCP + PDF) | 3 files | Jun 7 | MAR → LOW |
