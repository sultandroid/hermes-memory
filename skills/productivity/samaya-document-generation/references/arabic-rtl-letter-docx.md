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
