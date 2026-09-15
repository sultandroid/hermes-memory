# Generating a formal bilingual (AR/EN) RFI/TQ as Samaya DOCX

Applies to any formal Aseer document issued to MoC/CG that carries Arabic content.
Build with the SamayaDoc template, then apply the RTL pass below, then verify mechanically.

## Document structure that CG/MoC accept

Six numbered sections, in this order. Do not drop section 4 — the predecessor table is the
evidence that supports EOT and rebuts delay warnings.

1. **Background** — what triggered the request, citing the source (NRS RFI ref, CG submittal
   ref, meeting date).
2. **Design Basis** — the technical facts, then a short contract standing paragraph (Contract
   number, Design Lead/AoR, whether the input is an Employer obligation, changes after Stage 3
   under Contract Article 14).
3. **Requested Confirmation** — bilingual 3-column table: `No. | Required Confirmation |
   المطلوب تأكيده`. One row per ask. Keep asks atomic; a compound ask gets answered partially.
4. **Earlier Requests** — 4-column table `Reference | Date | Subject | Status`, then:
   *"This request consolidates and replaces the above for the specific <scope> covered here.
   Where an earlier request remains open on the common data environment, kindly respond to
   this request and close the earlier one."* Populate only from verified CDE/DB status, never
   from recollection — see the predecessor gate in `rfi-tq-drafting.md`.
5. **Impact of Delay** — programme, long-lead and handover consequences. This is what gets a
   reply; a bare question does not.
6. **Response** — 14-day period stated in both languages.

Then a QC sign-off table: `Role | Name | Title | Organisation` — Prepared (Tech Office Mgr),
Reviewed (Construction Mgr), Quality (QA/QC Mgr), Approved (Projects Director). Titles and
names, never agent names.

## Cover metadata table rows

RFI Reference · Date · Project (with contract number) · From (Samaya Technical Office) ·
To (Employer) · Copy (PMC; Design Lead; CG) · Subject (EN) · الموضوع (AR) · Reference (the
source doc) · Contract Reference · Response Required By.

Discipline code: **1A0** for architectural/showcase items — consistent with the historic TQ
series. Check an existing issued TQ of the same discipline before inventing a code.

## The RTL pass — python-docx has no Arabic support

Arabic typed into `add_body()` / `add_table()` renders left-to-right and visually broken in
Word and LibreOffice unless the attributes are written into the XML. Apply all of it after
building and before `doc.save()`.

**SamayaDoc exposes no `.paragraphs` / `.tables` — the inner document is `doc.doc`.** Walk
`inner.paragraphs` and every cell of every table.

**Run level, on every Arabic run:** `w:rFonts` (first in `rPr`) with `w:cs` set to the Arabic
font — `w:ascii` is not the complex-script font and mis-renders Latin tokens in the same run.
Then `w:rtl`, then `w:szCs` (Arabic sizes from `w:szCs`, not `w:sz`).

**Paragraph level:** add `w:bidi` to `pPr`. **`w:bidi` makes `w:jc` logical, not physical —**
with it set, `jc="right"` renders visually *left*. Use `jc="start"` for flush right, and do
not set `para.alignment` afterwards (python-docx rewrites `w:jc` and overwrites it).

**`pPr` children must be in OOXML schema order or they are silently ignored** — `w:bidi`
belongs before `w:spacing` and `w:jc`. Re-sort after every insertion.

**`w:bidiVisual` is deliberate, never blanket.** It mirrors the whole table so column 1
renders on the right. Apply it only to genuinely bilingual tables (pass their indices) and
strip it from English metadata tables, where it reverses the columns and reads as an error.

**Latin tokens inside Arabic text are the real cause of "broken Arabic".** Fragmented,
re-ordered or mirrored Arabic in a rendered PDF is usually correct Arabic wrapping wrongly
around an embedded token. Word breaks at punctuation inside a token, so `6,400` splits across
two lines and reads as `400.6`. In Arabic runs only: strip thousands separators (`6400 mm`,
not `6,400 mm`), then wrap every Latin/digit token in U+200E LRM so codes such as
`03.05-SC-01` stay in one piece.

**Never verify Arabic by eye or with a vision model.** Vision checks on mixed AR/EN pages
return confident false positives — a translation error that is not there, a numeral reversal
that is not there, "centred" for text that is right-aligned. Convert and measure instead:

```bash
soffice --headless --convert-to pdf --outdir /tmp/out <docx>
```

```python
import fitz
pg = fitz.open(pdf)[0]
for b in pg.get_text('dict')['blocks']:
    for l in b.get('lines', []):
        t = ''.join(s['text'] for s in l['spans'])
        if 'المطلوب' in t:
            print(l['bbox'][0], l['bbox'][2], pg.rect.width, t)
```

A right-aligned Arabic line has `x1` near the page width (~595 pt for A4). The text layer also
proves whether `6,400` survived as one number. Assert every section heading and every cited
reference from `get_text()` before reporting the document as done.

**Confirm the Arabic font is installed** (`ls /Library/Fonts ~/Library/Fonts | grep -i plex`).
If IBM Plex Sans Arabic is absent the renderer substitutes silently, so the PDF you inspect is
not what the user's Word will show — say so rather than treating the render as final.

## Content rules applied to bilingual formal documents

- English dominant; Arabic for the subject line and the ask/answer columns.
- Arabic subject line directly under the English heading, right-aligned.
- No `\n` inside `add_body(text)` — pass one flat string.
- `add_h2(number, text)` uppercases its text, so an Arabic heading there is a no-op; use
  `add_h2_u` or an English heading with the Arabic line beneath.
- Role titles in the body, real names in the sign-off and QC tables, `Eng.` prefix.
- No internal references, agent names, Odoo IDs or repo paths in a client-facing document.
