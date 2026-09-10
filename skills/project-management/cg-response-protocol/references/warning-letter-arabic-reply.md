# Warning-Letter Arabic Reply — Session Addendum (LT-08.02, 2026-09-09)

Lessons from drafting the reply to CG warning letter MOC-MUS-ASE-LT-08.02 (Aseer Museum).
Base patterns live in `warning-letter-delay-rebuttal.md`; this file covers what that session ADDED.

## 1. Reply language = the CG letter's language (Arabic)

CG warning letters at Aseer are issued in Arabic. The reply MUST be in Arabic —
not English with an Arabic translation appended. User correction was explicit:
"خلي النص نفسه بالعربي احنا هانرد علي خطابهم الي بالعربي بالعربي".

Workflow: draft AR as the PRIMARY deliverable (saved as separate repo file
`*_AR.md`); keep the EN version only as an internal reference annex. Never send
an English reply to an Arabic letter.

## 2. Humanization pass — "من انسان بدون اي علامات من الذكاء الاصطناعي"

After the structured draft, rewrite to engineer voice. Concretely:

- Replace English enumerated headers (2.2.1, "Net:", "Key argument") with
  أولاً / ثانياً / ثالثاً… and flowing numbered paragraphs.
- Delete AI-fingerprint connectives: "وهنا ملاحظة جوهرية:", "Net:", bold-in-
  mid-sentence emphasis, "بشكل جوهري", summary restatements.
- Break long compound sentences into short declarative ones.
- Open like a real Samaya letter: "إشارة إلى خطابكم المذكور أعلاه…" not
  "نشهد بأننا استلمنا" (legalized tone).
- Keep EVERY number and doc reference — humanize the prose, never the evidence.
- Result reads like Eng. Sultan dictated it. Verify by reading aloud: if any
  sentence sounds like a consultant's brief, rewrite it.

## 3. PM dictation integration (voice-note workflow)

Eng. Sultan dictates strategy as informal Arabic speech (possibly transcribed
roughly, e.g. "سما على" = "سمايا"). When integrating:

1. Decode intent, not words — each rambling paragraph = one letter section.
2. Known dictation-to-section mappings from LT-08.02:
   - "حجز الخارج من الطابق / تسرب الطابق" → site-occupancy rebuttal + lease VO
   - "الانتهاء من أعمال التقييم… الإزالة… الناس تكون بره" → assessment needed
     vacated building; cloud survey accuracy required element dimensions;
     ZD-0106 dismantling approval was the legal gate
   - "الـ sequence بتاع خطاب الاستشارة" → SI-007 serial-gate argument
   - "NCR بتاع… الأعمال اللي بيتم تنفيذها بشكل صحيح" → NCRs address executed
     non-conforming works, NOT delayed works — separate mechanisms; mixing them
     is a procedural error to call out
   - "كاميرتين غير موجودة في التقديم المعتمد… جنيريتور… الكهرباء الموجودة في
     الموقع… التسعير بناءً على هذا" → added items = extra cost out of scope;
     electricity approved for ASSESSMENT phase only (state precisely)
   - "تلات شهور تصميم… برر التلات شهور للـ site assessment" → CG's own proposal
     had a 3-month assessment window; design evaluation before its end is
     premature
   - "مفيش غرامات على مرحلية" → contract has NO stage-based penalties
   - "طلب التمديد… مستحق… recovery plan خلال العشر أيام" → EOT + recovery plan
     inside the 15-day window, cooperation without admitting fault
3. Close objection doors proactively: pre-empt the counter-arguments CG would
   raise (e.g. "you submitted the LiDAR late" → PQ cycle + failed first
   subcontractor + ZD-0106 gate chronology). Anticipate, cite, close.

## 4. Organized repo thread (mandatory shape)

Every warning-letter reply gets this repo footprint BEFORE content polish:

1. `03_Plans/08_Risk/<date>_reply-draft_<ref>_AR.md` — Arabic reply (primary)
2. `03_Plans/08_Risk/<date>_reply-draft_<ref>.md` — English internal ref
3. `03_Plans/08_Risk/<date>_delay-impact-table_<ref>.md` — claim-by-claim annex
4. `09_Agent_Workspace/discussions/<date>_<topic>.md` — organized discussion:
   letter summary, PM directives table (numbered, sourced), draft status
   matrix, evidence chain, open items with owners/dates, cross-links
5. Row in `09_Agent_Workspace/discussions/INDEX.md` (append only)
6. Row in `01_Registers/letters_register.md` (LT-08.02, status "Open — Reply
   due <date>")
7. Section in `00_Status/action_items.md` with CW-prefixed IDs
8. GitHub Issue on sultandroid/aseer-museum-pm labelled `known-issue` with the
   checklist; link back from the discussion file (AGENTS Rule 11)
9. Live preview page on Surge (RTL Arabic, `<meta refresh>`) + a cron (30m)
   that rebuilds from the repo file so PM edits appear automatically
10. Commit + push each step (AGENTS rule: always push)

## 5. Letter-structure pattern that passed PM review

Arabic formal letter, Samaya voice, this order:

1. Header block: رقم/تاريخ/إلى (Alrezeni)/صورة إلى (PMC Farouq)/مشروع/موضوع
2. السلام عليكم + إشارة to the warning letter ref/date
3. Reframe: "تصحيح واقع الأحداث كما هي موثقة" — cooperate, correct the record
4. Claim-by-claim rebuttal (أولاً/ثانياً/…) each: claim → documented reality →
   refs (Aconex transmittal IDs, letter refs, report numbers)
5. Corrective actions already running (numbered, owner, date) — "بدأ هذا
   الأسبوع" beats promises
6. حفظ الحقوق — EOT pending, occupancy delay, latent conditions, lease costs;
   "لا يُفسر أي مما ورد… على أنه تنازل"
7. Close: commitment + joint working session offer
8. Doc-control block + attachments list

Key sentence patterns that worked:
- "الفترة المشار إليها كتأخير… استُهلكت في دورة اعتمادات مفروضة بالتوازي مع
  تنفيذ المقاول لنفس المسار المطلوب" — neutral fact, no accusation
- "ولا يجوز الجمع بين الاثنين في معالجة واحدة" — procedural correction
- "ويحتفظ المقاول بكافة حقوقه قانوناً وتعاقداً" — reserved rights close

## 6. Evidence-refresh before sending

ALWAYS drop the newest Aconex export and rebuild `submission.db` before
citing any submittal code in the reply (AGENTS Rule 10a). In LT-08.02 this
flipped three cited documents in Samaya's favour (cloud survey U→B,
PQ-0122 C→B) and one against (ZD-0116 pending→C). Stale citations are the
fastest way to hand CG a counter-attack.

## 7. Live-review page pattern

For PM review of an Arabic draft: build an RTL HTML page (`dir="rtl"`,
Tahoma), sections: AR reply → annex table → EN reference, gold badge with
last-updated stamp, `<meta refresh>` for live view, Surge domain
`aseer-lt0802-reply.surge.sh`, cron rebuilds every 30m reading the REPO file
(not /tmp copies) so repo edits auto-publish.