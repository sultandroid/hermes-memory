# Arabic-RTL DOCX generation for Samaya formal letters

When the PM asks for a Word (.docx) version of a formal Arabic letter (in addition to / instead of the HTML surge draft), generate it with python-docx using the RTL letter pattern. Proven on LT-08.02/LT-0010 reply (Sep-2026).

## Reusable script pattern

Base it on `_Style-Guides/Doc Style Guide/gen_letter_template.py` (the RTL-correct letter generator). Key helpers to copy:

- `set_rtl_par(p)` — appends `<w:bidi>` to paragraph pPr (whole-paragraph RTL).
- `style_run(r, text, size, bold, color, rtl)` — sets Calibri + complex-script `w:rFonts` (ascii/hAnsi/cs) + per-run `<w:rtl>` so Arabic shaping/ordering is stable. This is the fix for "direction keeps changing."
- `cell_rtl_par(cell, text, ...)` — fills a table cell RTL + right-aligned; accepts `[('ar', ...), ('en', ...)]` segment lists so embedded English codes (MOC-MUS-ASE-...) render LTR inside Arabic.
- `make_table(doc, rows, cols, widths_cm)` — fixed-width table with explicit `w:tblGrid` + `w:tblW` (sum of widths ≈ 16.5 cm usable for A4 portrait with 2.5L/2.0R margins). Set `tblLayout=fixed` + `allow_autofit=False`.
- `set_borders(table, color, sz, inside)` — full grid borders.
- `header_row(t, headers, widths)` — navy `1E293B` header, white 9.5pt bold text.
- `body_par(doc, text, ...)` — RTL justified body, line spacing Exactly 14pt (Arabic glyphs are taller), Calibri 11pt.
- `h2_par(doc, text)` — RTL right-aligned section heading, 13pt bold navy + bottom border.

## Letter structure (order)

1. Letterhead strip: 3-col table — right col = Samaya logo + Arabic company name (RTL), center = English project name, left = English company. Navy border.
2. Reference block: 2-col table (label RTL right / value LTR run) — الرقم / التاريخ / الموافق.
3. Addressee: 2-col table — المرسل إليه / عناية / نسخة إلى / المشروع.
4. Subject: single-cell table, light-red `FDEBD0` fill + red `B01E2F` border, bold red text.
5. Greeting + body paragraphs.
6. Numbered sections (أولاً → حادي عشر) with h2 headings.
7. Data tables (timeline, pending submissions, support matrix) — navy header, alternating `F1F5F9`/white rows.
8. Signature block (company + role + name).
9. Attachments list.

## Pitfalls

- **Import path:** the script lives N levels deep (e.g. `03_Plans/08_Risk/LT-0010_print/`), so `sys.path` to the style guide and the logo path need `'..' * depth` — count the levels. `samaya_doc_template.py` and `logos archives/samaya-logo-trans.png` are at repo root `_Style-Guides/`.
- **Output path:** use `os.path.join(os.path.dirname(__file__), 'name.docx')` — do NOT re-append the repo-relative path (double-nesting bug).
- **Missing import:** `WD_LINE_SPACING` must be imported from `docx.enum.text` (used for `line_spacing_rule = EXACTLY`).
- **Verify after build:** reopen with python-docx and assert (a) body paragraphs carry `<w:bidi>`, (b) every table cell is RTL, (c) table row/col counts match expected. Then convert to PDF via `soffice --headless --convert-to pdf` and eyeball page 1 (logo, RTL alignment, no broken shaping).
- **Vision check:** the default model may not support image input — if `vision_analyze`/`browser_vision` fails with "model does not support image input," fall back to programmatic verification (bidi counts, table structure) + a browser render of the PDF page 1.
- **Keep the HTML surge draft and the DOCX in sync** — same content, two formats. When the PM edits the letter, regenerate both.
