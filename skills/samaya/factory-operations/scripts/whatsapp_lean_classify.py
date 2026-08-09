#!/usr/bin/env python3
"""Classify Lean input items from WhatsApp exported chat (_chat.txt).

Usage: python3 whatsapp_lean_classify.py <chat.txt> [start_year]
  - Parses WhatsApp media/export text format (handles LRM unicode prefix)
  - Filters to recent year (default 2026)
  - Categorizes each message into Lean buckets (Maintenance/Gemba/Immediate/
    Kaizen/5S/Materials) by Arabic keyword
  - Prints per-category counts + top senders + samples
  - Saves full JSON to <chat>.lean.json next to the source

Known-good sender names (Samaya groups): Raouf Eldeeb (Production Mgr),
Hassan Albormabaly (Carpentry Sup), Moen Aldeen (Maintenance/CNC),
Mostafa Mazen Shamsan (Workshop/Store), Ahmed Awwad (3D/Tech),
Essam Ibrahim (Fiber Mgr), Mohamed abdeljalil (Installation Sup).

Pitfall: WhatsApp export lines begin with a Left-to-Right Mark (\u200e) —
a raw `^\[` regex matches ZERO lines. Must strip the line (or \u200e) BEFORE
matching, and the AM/PM separator uses narrow no-break space (\u202f), not a
regular space. This is the classic "parsed 0 lines" bug.
"""
import re, json, sys, os
from collections import Counter

CHAT = sys.argv[1] if len(sys.argv) > 1 else "_chat.txt"
START_YEAR = sys.argv[2] if len(sys.argv) > 2 else "2026"

# WhatsApp line: [DD/MM/YYYY, H:MM:SS AM/PM] Sender: text
# - LRM \u200e may prefix the line
# - AM/PM separator is narrow no-break space \u202f
PAT = re.compile(r"\[(\d{2}/\d{2}/\d{4}), ([0-9:]+)[\u202f ]([AP]M)\] (.*?): (.*)$")

CATS = {
    "🔧 Maintenance": ["ماكينة","مكينه","عطل","خلل","توقف","حزام","موتور","مضخة","صيانة",
                        "cnc","ليزر","منشار","فشل","خراب","تسريب","المبرد","ديسك","سلم"],
    "🚶 Gemba/Safety": ["حادث","اصابة","خطر","سلامة","انذار","مخالفة","ممنوع","حريق","كهربا","سقوط","كسر"],
    "⚡ Immediate/Process": ["تأخير","غلط","خطأ","خطا","ناقص","مش موجود","فاضل","عاجل","مطلوب",
                             "نقص","استعجل","بسرعه","غير مطابق","مقاس"],
    "💡 Kaizen/Idea": ["اقتراح","احسن","افضل","تحسين","توفير","اسرع","نعمل","فكره","فكرة"],
    "🧹 5S/Clean": ["نضافه","نظافة","وسخ","مخلفات","زباله","رتب","نظم","فوضى","نشاره"],
    "📦 Materials/Stock": ["خامة","خامه","مواد","مخزن","خشب","حديد","بورسلين","لوح","مسمار",
                            "غراء","الومنيوم","اكريليك","زجاج"],
}

# Noise phrases that cause false positives (greetings/thanks/religious)
NOISE = ["تسلم ياريس","تسلم يامحمد","اللهم","عليه افضل الصلاة","اكيد تسلم","وباركته"]

KEY_PEOPLE = {
    "Raouf Eldeeb": "Production Mgr (رؤوف)",
    "Hassan Albormabaly": "Carpentry Sup",
    "Moen Aldeen": "Maintenance/CNC",
    "Mostafa Mazen Shamsan": "Workshop/Store",
    "Ahmed Awwad": "3D/Tech",
    "Essam Ibrahim": "Fiber Mgr",
    "Mohamed Zarad": "Workshop",
    "Mohamed abdeljalil": "Installation Sup",
}

messages = []
with open(CHAT, encoding="utf-8") as f:
    for line in f:
        m = PAT.match(line.strip())  # strip BEFORE match — kills the \u200e bug
        if m:
            date, time, ap, sender, text = m.groups()
            if date.endswith("/" + START_YEAR):
                messages.append({"date": date, "sender": sender.strip(), "text": text.strip()})

print(f"{START_YEAR} messages: {len(messages)}")

def classify(text):
    t = text.lower()
    if "omitted" in t and len(t) < 30:
        return None
    if any(n in t for n in NOISE):
        return None
    return [c for c, kws in CATS.items() if any(k.lower() in t for k in kws)]

results = {c: [] for c in CATS}
for msg in messages:
    for c in classify(msg["text"]) or []:
        results[c].append({**msg, "role": KEY_PEOPLE.get(msg["sender"], "Worker/Other")})

for cat, items in results.items():
    print(f"\n## {cat} — {len(items)}")
    print("  senders:", dict(Counter(i["sender"] for i in items).most_common(6)))

out = CHAT + ".lean.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\nSaved: {out}")
