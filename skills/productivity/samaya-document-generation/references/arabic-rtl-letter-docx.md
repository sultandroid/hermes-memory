# Arabic-Only RTL Formal Letter → DOCX (Samaya)

`SamayaDoc` is **English/LTR only**. For an Arabic-only formal letter (خطاب رسمي)
do NOT use `SamayaDoc` — build the docx directly with the RTL helpers. Proven
generators:
- `aseer-museum-pm/_Style-Guides/Doc Style Guide/gen_letter_template.py` (single-subject letter)
- `aseer-museum-pm/03_Plans/08_Risk/LT-0010_print/build_lt_reply_docx.py` (full 11-section reply letter)

## Core RTL helpers (copy from gen_letter_template.py)

- `set_rtl_par(p)` — append `<w:bidi>` to paragraph pPr.
- `style_run(r, text, size, bold, color, rtl)` — set Calibri + complex-script
  `w:rFonts` (`w:ascii`/`w:hAnsi`/`w:cs` all Calibri) AND a per-run `<w:rtl>`
  element. The per-run rtl is what keeps Arabic shaping/ordering stable when a
  paragraph mixes Arabic with embedded English codes (e.g. `MOC-MUS-ASE-LT-0010`).
- `cell_rtl_par(cell, text, ...)` — fill a table cell RTL + right-aligned.
  Pass `[('ar', 'نص'), ('en', 'CODE')]` segments so embedded LTR tokens get
  `rtl=0` runs.
- `make_table(doc, rows, cols, widths_cm)` — fixed-width table with explicit
  `w:tblGrid` + `w:tblW` (sum of widths × 567 twips/cm). A4 portrait usable
  width = **16.5 cm** (margins 2.5L + 2.0R).
- `set_borders(table, color, sz, inside)` — full grid borders.
- `header_row(t, headers, widths)` — navy `#1E293B` header, white 9.5pt bold text.

## Letter structure (order matters, all RTL right-aligned)

1. **Letterhead strip** — 3-col table: right col = Samaya logo + `شركة سمايا
   الاستثمارية` (navy bold), center = `Aseer Regional Museum` (LTR), left =
   `SAMAYA INVESTMENT CO.` (LTR). Navy border sz=8.
2. **Reference block** — 2-col table: `الرقم` (LTR code run), `التاريخ`,
   `الموافق` (Hijri).
3. **Addressee** — `المرسل إليه`, `عنايـــة`, `نسخة إلى` (repeat per CC),
   `المشروع`.
4. **Subject** — single-cell table, light red bg `FDEBD0`, red `#B01E2F` bold
   text, red border sz=6.
5. **Greeting** `السلام عليكم ورحمة الله وبركاته،،،` then body paragraphs.
6. **Numbered sections** — `h2_par` (13pt navy bold, bottom border) + `body_par`
   (11pt, line spacing EXACTLY 14pt, justify, RTL).
7. **Tables** for timelines / pending submissions / support matrices.
8. **Signature** — company name, role, name (real names, Eng. prefix).
9. **Attachments** — numbered list.

## Pitfalls (learned the hard way)

- **Path depth**: a build script inside `03_Plans/08_Risk/LT-0010_print/` is 3
  levels below repo root. `sys.path` and `LOGO` must use `'..','..','..'` to
  reach `_Style-Guides/`. The output path must be `os.path.join(__file__ dir,
  'name.docx')` — do NOT re-append the subdir (double-nesting error).
- **Import `WD_LINE_SPACING`** from `docx.enum.text` — the RTL helpers use
  `WD_LINE_SPACING.EXACTLY`; forgetting it is a NameError.
- **Vision model may not support images** (qwen3.5:397b rejects image input).
  Verify RTL rendering by: (a) convert to PDF via
  `soffice --headless --convert-to pdf`, (b) open the PDF in the browser
  (`browser_navigate file://...pdf`) and use `browser_vision` — the browser
  vision path works even when the direct `vision_analyze` model rejects images.
- **Programmatic RTL check** (no vision needed): count paragraphs/cells whose
  pPr contains `w:bidi`. All body paragraphs and every table cell should be RTL.
- **Content source**: when converting an existing HTML letter (e.g. a surge
  page) to DOCX, parse the HTML with a regex walker (h2/p/table) to extract the
  exact ordered content — don't hand-retype. `web_extract` may truncate; curl
  the page and parse locally.

## Confirm the letter's STRATEGY before building (user iterates heavily)

Before generating any formal reply letter, confirm the framing — the user will
rework addressee/signature/scope repeatedly, and building first wastes a pass:

- **Addressee & CC** — who is it TO (MoC vs PMC vs CG) and who is CC'd? A
  "rights-preserving reply, not escalation" letter may go to the PMC (e.g.
  Eng. Farouk) with CG on CC, NOT to the Ministry/PM. Ask explicitly.
- **Signer** — who signs (CEO / GM / PM)? Real name + role. The user may refer
  to the signer by a nickname (e.g. "أبو معاذ" = the CEO) — map it to the real
  name before putting it in the signature block.
- **Escalation vs rights-preserving** — is this a formal escalation, or a reply
  that implicitly preserves all rights and answers the other party's letter
  "as if contractual" without escalating? This changes tone and the addressee.
- **Withdrawal window** — if the other party's letter grants a deadline (e.g.
  PMC's 15-day window to exercise partial/full withdrawal of works), the reply
  should acknowledge it implicitly without conceding fault.
- **"New version" requests** — when the user says "هانعمل نسخه جديده" (make a
  new copy), they mean a fresh build with a different addressee/scope, not an
  edit of the current one. Rebuild the docx with the new framing.

## Structural pattern: general statement in intro, detail in numbered section

When a specific rebuttal (e.g. the TLC landscaping-contract point) is raised in
the intro, the user prefers: a **one-line general statement** in the intro
("خطاب الاستشاري تضمن معلومات غير دقيقة لا تتفق مع سجل التقديمات، وسيرد الرد
بالتفصيل في البند خامساً") and the **full detail moved into the relevant
numbered section** (e.g. خامساً (5) التعاقد مع المتخصصين). Do not leave a long
detailed paragraph in the intro — it reads as "دخيل" (intrusive).

## Fact-checking letter references (before finalising)

Verify every letter/submittal reference against the authoritative registers —
the user will ask "هل هذا صحيح؟" (is this correct?) on each one:

- **Letter numbers/dates** → `05_Comms/correspondence_register.md` +
  `01_Registers/letters_register.md`.
- **Submittal codes (A/B/C/D)** → `08_Document_Index/submission.db` (single
  source of truth, latest-revision-wins). If a ref is not in the DB, say "not
  in current register" — do NOT state a code.
- **Date-ambiguity trap**: a register may show the date an email was *found*
  (e.g. LT-0027 listed 05-Jul in correspondence_register) vs the letter's
  actual issue date (03-Aug per letters_register / backfill analysis). Always
  cross-check the letters register / backfill analysis before trusting a date.
- **Cross-source confirmation**: a fact is "correct" only when two independent
  sources agree (e.g. a letter's own reply text + a backfill analysis). Report
  the confirming sources in a small table when the user asks to verify.

## Contractual note (Aseer LT-08.02 context)

The "consultant/PMC reviews only for contractual conformance, not technical
review" clause lives in **SoW §6.6** and **ER §2.4** (also summarized in
`99_Archive/01_Integration_Management/DMP_Design_Management_Plan/02_Contractual_Framework.md`
§2.2.A). Exact wording: *"Reviews at all stages by PMC are only for contractual
conformance with ERs. These reviews do not constitute any form of technical
review. Technical review shall be undertaken by Contractor's nominated
designer."*

**Double-edged — cite with care:**
- **For Samaya:** it weakens CG's authority to impose technical-review comments
  / rejections beyond conformance (supports the LT-08.02 argument that CG
  exceeded its role).
- **Against Samaya:** ER §2.4.B places ALL design liability on the Contractor
  (single point of responsibility). Do NOT cite it as an excuse for delay — it
  will rebound and confirm the Contractor owns design errors.

