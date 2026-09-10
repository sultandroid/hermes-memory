# CG Warning Letter Reply (إنذار) — Full Workflow

> Reference file for the "CG Warning Letter Reply" section in SKILL.md.
> Case: LT-08.02 (CG) + LT-0010 (PMC warning), 02-Sep-2026, Aseer Museum. Session 2026-09-09.

## 1. The two-letter chain (verify before replying)

A warning usually arrives as a PAIR issued the same day:
- **CG/Consultant letter** (e.g. LT-08.02) — addressed to the **PMC office**, NOT to the contractor. Content: general delay claims (design %, assessment, mobilization, specialists), a progress figure (e.g. "7.37% after 275 days"), and a 15-day ultimatum for a corrective plan.
- **PMC/PMO letter** (e.g. LT-0010) — the actual warning addressed to the contractor.

**Procedural challenge (strongest opener):** the warning cites no contract article, names no specific breached obligation, identifies no reference program (no Rev number), and was issued the same day as the consultant letter — with zero opportunity for the contractor to see/respond to the consultant letter first. Closing sentence (PM-approved): *"وعليه فإن الإنذار — بهذه الصورة — لا يستوفي مقوماته التعاقدية، ويتعامل معه المقاول على هذا الأساس مع احتفاظه بحقه في الرد على مضمونه حرصاً على مصلحة المشروع."*

## 2. Contract-article verification method (learned this session)

Before citing ANY article, verify against `00_Project_Charter/contract.md`. **The contract.md OCR is REVERSED Arabic** — plain `text.find('النص')` fails. Method:
1. Search the **parallel English clause** (e.g. "Article One: Limitations to the Powers") — always adjacent.
2. Use OCR-tolerant Arabic patterns (املادة instead of المادة, صالحات instead of صلاحيات).
3. Confirm both language versions agree before quoting.

Verified article map (Contract 0010003521):
| Claim | Article | Location anchor |
|---|---|---|
| "ممثل الجهة" definition | Definitions section | "املعين الشخص" near line 731 |
| Representative appointment/replacement notice | **Sec. 3, Art. 3** | "استبدال ممثل الجهة" line ~2249 |
| Partial withdrawal (إنذار = Government Entity's right) | **Art. 18** | "تنذره الجهة الحكومية" line ~4156 (NOT the Waiver-of-Rights Art. 18 at line 1634 — two articles share the number; cite by title) |
| Rep must obtain Entity consent for duration actions | **Sec. 3, Art. 1, clause (f/و)** | "تمديد مدة تنفيذ" line ~2200 |
| 30-day reply obligation | **Sec. 3, Art. 1, clause (e/هـ)** | "30 يوم" line ~2195 |

## 3. Date verification hierarchy (the LT-0007 lesson)

Direct letters (LT-xxx to Ministry) **never enter Aconex**. When a letter's date is disputed across registers (letters register said 13-Aug, risk register said 11-Aug, draft said 11-Aug):
1. **Outlook SQLite is authoritative for direct letters**: copy to /tmp, query `Mail` table, `Message_NormalizedSubject LIKE '%LT-0007%'`, `Message_TimeSent` is a standard unix epoch. Found: original 11-Aug 09:39 (to Ministry) vs revised 13-Aug (to PMC) — **the letter date = the original send**.
2. **Aconex export `last update` column** = when a CG code response was logged (NOT the snapshot date). E.g. ZD-0120: submitted 01-Sep, Code C logged 05-Sep 11:37 — three days AFTER the warning letter. A claim like "rejected the day before the warning" must be corrected to the actual sequence.
3. **Risk register "formally submitted" notes** corroborate but rank below the email timestamp.

## 4. Claim-by-claim evidence table (the reply's engine)

Build a delay-impact annex mapping EVERY warning claim to evidence:

| Warning claim | Counter-evidence | Verified source |
|---|---|---|
| "Site assessment incomplete" | ZD-0114 CG comments require ETABS confirmation AFTER cloud survey (Code B 05-Aug) + core test FAIL 20.7/35 MPa (latent Employer risk) + ZD-0106 dismantle approval only 25-Aug | submission DB latest codes |
| "Design % low" | SI-007 serial-gate froze parallel tracks; contractor had funded 3D first (ZD-0031, SAR 236,250, Code B); requirement originated in CG's own DMP comment C-3a | si_register + DMP |
| "7.37% progress" | Design weight in price schedule = 4.81% (SAR 3,133,611) — a % ABOVE design weight proves progress BEYOND design, not behind | WR-16 payment schedule |
| "Landscape specialist not contracted" | TLC PQ-0127 Code B 23-Jul; SOW ZD-0120 submitted 01-Sep (day before warning); Code C 05-Sep; reservation = scope expansion to supply-and-install without contract basis | submission DB |
| Penalty implication | Contract has NO stage-based penalties — verify against Annex 4 before asserting | contract.md |

## 4b. Verified factual anchors (Aseer LT-0010/LT-08.02 — confirmed during 09/10-Sep review)

All verified against primary sources; safe to cite:

- **LT-0007 = 2026/08/11** — Outlook original 09:39 to merghani.ahmed; revised 13-Aug 17:13 to PMC Farouk. Registers saying 13/14-Aug refer to the revised letter; the original send wins.
- **LT-0028 (EOT supporting docs) = 2026/08/10, IN Aconex** — unlike LT-0007/27 (direct letters). Useful supplementary Aconex citation.
- **30-day rule (Sec.3 Art.1 هـ)** — verbatim "يجب على ممثل الجهة الرد خلال مدة لا تتجاوز 30 يوماً". Count awaiting>30d from submission DB for impact (248 as of 09-Sep snapshot).
- **TLC chain (Aconex-verified)**: PQ-0127 Code B 23-Jul → SOW ZD-0120 submitted 01-Sep (day BEFORE warning) → Code C logged 05-Sep (AFTER warning) → kick-off design review 07-Sep with CG/PMC present (recorded in `00_Status/2026-09-07_MoC_Coordination_Meeting/README.md` — proves contractor active post-warning, turns CG attendance into testimony against their own claim).
- **CG's actual ZD-0120 comment was "separate designer/supplier tables"** — phrase the letter as "إدراج أعمال التوريد ضمن نطاق المتعاقد المصمم" (inserting supply into the designer's scope), NOT "CG demanded full supply+execute scope" — CG may argue they only asked for table separation.
- **Timeline table = 20 rows** — say "20 حدثاً" not 21.
- **SP-0007/SP-0008 (mobilization) NOT in Aconex or Adel bank** — never cite with date/number unless the original transmittal exists; soften or drop.
- **العرجاني = Employer-side PM** (owner role; CG-side PM was Mansour Alrezeni acting). His appointment letter strengthens the "no representative notified" argument (4 PMs counting owner side).

## 4c. Pattern-of-conduct framing (generalizable rebuttal upgrade)

When a warning claim ("contractor didn't hire specialist X") is contradicted by active submittals that CG itself returned, frame it as a PATTERN, not an incident:

> "وهذا النمط في التعامل — إعادة التقديمات النشطة للتعديل بتوسيع نطاقها، في الوقت الذي يُتَّهم فيه المقاول بالتأخر — يتكرر في أكثر من بند"

This converts a defensive rebuttal into evidence of consultant conduct and invites the Ministry to re-read the whole warning through that lens. Keep every specialist chain fully dated (PQ → SOW → CG response → kickoff) so the pattern is audit-proof. Keep unrelated topics (landscaping vs mobilization) as SEPARATE paragraphs — gluing them into one long sentence muddles both points.

## 4d. Styling iterations the user rejected (do not repeat)

- Hand-written CSS "inspired by" the official template → REJECTED ("you didn't follow the samaya project doc style guide"). Always extract the official `<style>` block VERBATIM from an existing approved doc (e.g. `03_Plans/02_Stakeholder/...Rev04....html`) plus its Google Fonts `<link>`, and layer RTL letter overrides on top of the official `:root` vars.
- Content overflowing a single `.page` div → REJECTED twice ("الملف ضرب", "مش مقسم صفحات"). Two working patterns: (a) official fixed `.page { height: 297mm; page-break-after: always }` with content SPLIT at section boundaries into multiple `<section class="page">` wrappers, each with its own page-header + pg-footer; (b) flowing document with `@page` margins + `break-inside: avoid` on tables + `break-after: avoid` on headings. Never one giant page div.
- Justified Arabic text → "rivers" of white gaps. Right-align always.
- **Duplicate raw paragraph block left in the HTML** below the styled version (from the received docx paragraphs) → user saw stale blank dates ("لسه زي ماهو الفقره حتي ماحطيت التاريخ") despite the styled block being correct. Root cause: the verbatim docx conversion included the old header as plain `<p>` rows that survived every restyle. After every rebuild, grep for BOTH variants (`grep -c "الرقم:"`) and for leftover `__` placeholders; delete the raw duplicate before deploying.
- Broken nested tags (`<span class="lbl">الرقم:</strong>` — stray closing tag inside the span) silently corrupt rendering — verify after tag edits.
- Header block design: PM wanted the ref/date + addressee + cc + project + subject compressed into ONE solid styled block (header-meta-block) with every field filled — "لا تترك بيانات ناقصه". No scattered paragraphs.

## 5. PM-corrected workflow preferences (embed in every future reply)

## 5. PM-corrected workflow preferences (embed in every future reply)

0. **Explain legal phrases on request** — PM asks "يعني ايه الجمله دي؟" for any procedural/legal formulation; always be ready to break it down plainly (e.g. the "addressed to PMC not to the contractor" sentence = the warning rests on a document the contractor was never formally served, issued same-day with no reply window).

1. **Paragraph-by-paragraph review** — PM explicitly rejected whole-document review ("نجيب فقرة فقرة نتكلم عليها"). Present: sub-claim verdicts (✅/⚠️) + evidence + proposed fix. **Wait for approval BEFORE merging.**
2. **1:1 fidelity to received drafts** — when a draft arrives (docx), convert it verbatim; additions go in labeled green blocks ("إضافة مقترحة:"), never silent rewrites.
3. **No monetary values in the letter** — "records kept, shown upon request". Value stays internal for the EOT/VO file.
4. **Fill every date; remove unfilled placeholders** — no `[الاسم/المنصب]` shipped; drop the line until the value arrives.
5. **Hijri month must be computed, not copied from the draft** — Sept 2026 = Rabi' al-Akhir **04/1448** (draft had wrong 03/1448). Anchor: 1 Rabi' II 1448 ≈ 2026-08-14.
6. **Contract number digit-count matters**: 0010003521 (11 digits) — received draft had 9 (10003521).
7. **Verify addressee identity** — a draft named "عبدالرحمن العرجاني" as Ministry PM, not in any record; confirmed by PM he IS the Employer-side PM (different from CG/PMC PM Mansour Alrezeni). Wrong-name letters lose credibility.
8. **"More than 800 submissions"** beats a stale exact count — the Aconex DB grows every snapshot (was 135 in an old export, 826 actual). Use "أكثر من N" with the current floor.

## 6. Repo artifacts & deployment

- Reply MD: `03_Plans/08_Risk/<date>_reply-draft_LT-<ref>_AR.md` (submission) + EN internal reference
- Delay impact annex: `03_Plans/08_Risk/<date>_delay-impact-table_LT-<ref>.md`
- Discussion: `09_Agent_Workspace/discussions/<date>_cg-warning-lt<ref>-reply.md` + INDEX row
- Letters register row (status "Open — Reply due DD-MMM") + action items (CW-*) + GitHub issue
- Live preview: Surge domain (aseer-lt0802-reply.surge.sh pattern), 30-min republish cron
- Cross-link everything per AGENTS.md Rule 12

## 7. RTL letter styling (Samaya HTML print template)

See the Arabic-RTL subsection added to `samaya-html-print-template.md` knowledge (this skill's sister): right-align (never justify), IBM Plex Sans Arabic, section-boundary pagination with break-inside:avoid, single header-meta-block with no blank fields, duplicate-block grep after every rebuild.