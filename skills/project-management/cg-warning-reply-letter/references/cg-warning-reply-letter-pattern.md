# CG Warning-Reply — Session Detail Bank (LT-0010 / LT-08.02, Sep-2026)

Condensed verification recipes + pitfalls from the Aseer Museum warning-letter reply session.

## Contract verification recipes

```python
# contract.md is OCR'd Arabic: reversed character order, disconnected letters.
# Search with OCR spellings (صالحات not صلاحيات, املادة not المادة) or find the parallel English text.
text = open('00_Project_Charter/contract.md', encoding='utf-8').read()
# English anchors (reliable): 'Article One: Limitations to the Powers', 'Article Three: Replacement of the Government', 'Partial Withdrawal of the'
# Arabic OCR anchors: 'املادة الثالثة: استبدال ممثل', 'و.    عند الحكومية الجهة موافقة'
```

Duplicate article numbers confirmed in this contract: Article Eighteen appears TWICE — (1) Waiver of Rights in the general section, (2) Partial Withdrawal of the Service — the warning-derivative one is the Partial Withdrawal text: "تنذره الجهة الحكومية لإصلاح أوضاعه خلال خمسة عشر (15) يوماً" (notice + 15-day cure period sits with the Government Entity itself).

Verified clause map for this contract:
- Definition "ممثل الجهة" (contract §definitions, line ~727)
- Sec. 3 (ممثل الجهة) Art. 1 — Limitations to powers; clause (و): representative must obtain Entity consent for any action on duration/cost
- Sec. 3 Art. 1 clause (هـ): representative must respond to any contractor request within 30 days — use for aged-review breaches
- Sec. 3 Art. 3: replacement of representative requires notice to contractor
- Partial Withdrawal Art.: notice + 15-day cure, entity's own power

## Outlook SQLite query (direct letters)

```python
import sqlite3, datetime
db = sqlite3.connect('/tmp/outlook_copy.sqlite')  # copy first — live DB can be locked
rows = db.execute("""
    SELECT Message_NormalizedSubject, Message_TimeSent, Message_DisplayTo, Message_Preview
    FROM Mail WHERE Message_NormalizedSubject LIKE ? OR Message_Preview LIKE ?
    ORDER BY Message_TimeSent DESC LIMIT 10
""", (f'%{term}%', f'%{term}%')).fetchall()
for r in rows:
    print(datetime.datetime.fromtimestamp(r[1]), '|', r[0][:70], '| to:', str(r[2])[:50])
# Timestamps are plain unix. Do NOT add 978307200 or 1904 offsets — dates will show as 2057/1960.
```

Meeting evidence lives in calendar-invite subjects too: "🗓 Landscape specialist TLC -Kick off meeting on August 13, 2026 @ 11:00 AM" — the invite recipient list proves the consultant was personally notified (kills "we didn't know" defenses).

## Aconex export column map (ExportDocs-*.xlsx, sheet 'Docs')

Row 1 = banner ("In case any cell is highlighted..."), row 2 = header. Skip both.
- col1 doc_no, col2 revision, col4 title, col7/8 status code (duplicate columns), col11 registered/submitted date, col12 last-update timestamp (= CG response moment).

Direct LT-xxxx letters never appear on Aconex — verified pattern: LT-0007 (11-Aug formal, 13-Aug revised), LT-0027 (03-Aug to consultant) exist only in Outlook + registers. LT-0028 (supporting pack) IS on Aconex (10-Aug).

## Known-good evidence chains (this project)

**TLC landscaping (disproved "not contracted"):** PQ Code B 23-Jul → kick-off 13-Aug (consultant personally invited via calendar) → SOW ZD-0120 on Aconex 01-Sep (one day before warning) → Code C 05-Sep demanding designer=supplier → design review with CG present 07-Sep → 50% milestone 15-Sep.

**SI-007 sequence freeze (design-delay rebuttal):** Samaya funded 3D first (ZD-0031, 236,250 SAR, Code B) + DMP RACI row 25 assigned 3D to Samaya + requirement originated in CG's own DMP comment C-3a (13-May) + 3D sample ZD-0033 Code B 06-Jun — SI-007 (19-Apr) converted a planned parallel track into a serial gate, freezing architectural DD.

**Vacate/occupancy:** WR-01→WR-11 weekly reports prove 5-month occupation; alternative premises at own cost (letter ref LT-0006, 26-Apr); "records held, shown upon request" phrasing preserves EOT/VO value without stating it.

## Letter-number corrections caught before sending

- Contract: 0010003521 (11 digits — draft had 9).
- Hijri: Sep-2026 = 04/1448 (Rabi' al-Akhir), not 03.
- Aconex count: 800+ (draft had stale 135).
- Timeline events: 20 rows (draft said 21).
- LT-0007 date: 11-Aug = formal submission (Outlook 09:39 + risk register agree); 13/14-Aug = revised signed copy.