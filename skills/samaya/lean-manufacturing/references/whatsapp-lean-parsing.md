# WhatsApp Export → Lean Input Parsing (Samaya Factory)

Technique for turning WhatsApp chat `.zip` exports into Lean-system entries. Used 2026-08-08 on the **Samaya Factory** group and the **التركيبات** (installations) group.

## File format
- Export is a `.zip` containing `_chat.txt` (UTF-8, CRLF line endings).
- Line format: `[DD/MM/YYYY, H:MM:SS AM] Sender: message`
- **Critical gotcha:** lines often begin with a Left-to-Right Mark `\u200e` before the `[`, and the time uses a narrow no-break space `\u202f` before AM/PM. A regex anchored with `^\[` silently matches 0 lines.

## Working regex
```python
import re
pat = re.compile(r"\[(\d{2}/\d{2}/\d{4}), ([0-9:]+)[\u202f ]([AP]M)\] (.*?): (.*)$")
# apply to line.strip() — NOT the raw line (LRM prefix)
m = pat.match(line.strip())
```

## Filter to current year
```python
if date.endswith("/2026"):   # export spans 2021→2026, ~48k lines
    messages.append({...})
```

## Classification
Keyword buckets → Lean categories:
- `🔧 Maintenance`: ماكينة/مكينه/عطل/توقف/حزام/موتور/صيانة/cnc/ليزر/منشار/خراب/تسريب
- `🚶 Gemba/Safety`: حادث/اصابة/خطر/سلامة/ممنوع/انذار/مخالفة/حريق/كهربا
- `⚡ Immediate/Process`: تأخير/غلط/خطأ/ناقص/مش موجود/عاجل/مطلوب/نقص/غير مطابق/مقاس
- `💡 Kaizen/Idea`: اقتراح/احسن/افضل/تحسين/توفير/اسرع/فكره
- `🧹 5S/Clean`: نضافه/نظافة/وسخ/مخلفات/زباله/رتب/نظم/فوضى
- `📦 Materials/Stock`: خامة/مواد/مخزن/خشب/حديد/لوح/مسمار/غراء

## Noise filtering (essential)
Raw keyword match is noisy — picks up greetings, Islamic phrases, thanks. Curate with:
```python
NOISE = ["تسلم ياريس","تسلم يامحمد","اللهم","عليه افضل الصلاة","اكيد تسلم","وباركته"]
ACTIONABLE = {  # stricter per-category keywords
  "maintenance": ["موتور","مكينة ليزر","cnc","ليزر","منشار","عطل","تصليح","خراب","توقف","كهرباء","ماكينة","ديسك"],
  "quality": ["غير مطابق","مقاسات","كسر","سقوط","تكسر","غلط","اتكسر"],
  "safety": ["سقوط","خطر","حادث","اصابة","ممنوع","انذار","مخالفة","حريق"],
}
```
Skip any item containing a NOISE phrase; only keep items matching an ACTIONABLE keyword.

## Merge multiple groups
De-dup by `(date, sender, text)` across groups. Save merged JSON to `06_lean_input/merged_whatsapp_2026.json` for traceability.

## Seeding the registers
From the curated items:
- **5 Whys** for recurring problems (dimensions not matching plan, machine breakdowns, material shortage, acoustic panel fall) → `04_5whys/5whys_analysis_2026.md`
- **CI register** entries with owner + deadline + status → `05_continuous_improvement/ci_register.md`
- **PM log** spare-parts rows (e.g. CNC motor repair 23/02, laser down 02/08) → `04_preventive_maintenance/pm_log.md`
- **Kaizen register** ideas → `02_kaizen/kaizen_register.md`

## Key people (for role attribution)
Raouf Eldeeb (Production Mgr), Hassan Albormabaly (Carpentry Sup), Moin El-Din (Maintenance/CNC), Mostafa Mazen Shamsan (Workshop/Store), Ahmed Awwad (3D/Tech), Essam Ibrahim (Fiber Mgr), Mohamed Zarad (Workshop), Mohamed abdeljalil (Installation Sup).
