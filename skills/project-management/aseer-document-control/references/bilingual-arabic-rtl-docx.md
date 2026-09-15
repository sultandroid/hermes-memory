# Bilingual AR/EN DOCX — Arabic RTL in python-docx

Use when a formal document carries Arabic runs — an Arabic subject line, a bilingual ask column, an Arabic closing paragraph. Each item below was a real defect in rendered output; apply all of them, then verify by rendering.

## 1. Run level — `w:rtl` + complex-script font

Arabic will not shape or order correctly without a run-level RTL flag. Set it per run, only on runs that actually contain Arabic:

```python
def has_ar(t):
    return any("\u0600" <= c <= "\u06FF" for c in t)

def _rtl_run(run, ar_font="IBM Plex Sans Arabic"):
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts'); rPr.insert(0, rFonts)
    rFonts.set(qn('w:cs'), ar_font)          # complex-script font
    rtl = OxmlElement('w:rtl'); rtl.set(qn('w:val'), '1'); rPr.append(rtl)
    sz = OxmlElement('w:szCs')               # complex-script size, or Arabic renders at default
    sz.set(qn('w:val'), str(int((run.font.size or Pt(11)).pt * 2)))
    rPr.append(sz)
```

`w:rtl` applies to the complex-script (Arabic) portion of the run; Latin text in the same run is unaffected, which is what a bilingual line needs.

## 2. Paragraph level — `w:bidi`, inserted in SCHEMA ORDER

`w:bidi` must precede `w:spacing` / `w:jc` / `w:rPr`. python-docx `append()` puts it last, and **Word silently ignores mis-ordered pPr children** — the paragraph then renders LTR with no error, which is very hard to diagnose. Re-sort after inserting:

```python
PPR_ORDER = ['w:pStyle','w:keepNext','w:keepLines','w:pageBreakBefore','w:framePr',
 'w:widowControl','w:numPr','w:suppressLineNumbers','w:pBdr','w:shd','w:tabs',
 'w:suppressAutoHyphens','w:kinsoku','w:wordWrap','w:overflowPunct','w:topLinePunct',
 'w:autoSpaceDE','w:autoSpaceDN','w:bidi','w:adjustRightInd','w:snapToGrid','w:spacing',
 'w:ind','w:contextualSpacing','w:mirrorIndents','w:suppressOverlap','w:jc',
 'w:textDirection','w:textAlignment','w:textboxTightWrap','w:outlineLvl','w:divId',
 'w:cnfStyle','w:rPr','w:sectPr','w:pPrChange']

def normalize_pPr(pPr):
    kids = list(pPr)
    for k in kids: pPr.remove(k)
    for k in sorted(kids, key=lambda e: PPR_ORDER.index('w:'+e.tag.split('}')[-1])
                  if 'w:'+e.tag.split('}')[-1] in PPR_ORDER else len(PPR_ORDER)):
        pPr.append(k)
```

## 3. Alignment — with `w:bidi` set, `jc` is LOGICAL, not physical

**The trap that costs the most time.** With `w:bidi` present, `jc="right"` means the logical end of the line, which renders **visually LEFT**. To right-align Arabic you need the logical *start*:

```python
jc = pPr.find(qn('w:jc')) or (lambda e: (pPr.append(e), e)[1])(OxmlElement('w:jc'))
jc.set(qn('w:val'), 'start')     # NOT 'right'
```

Set `para.alignment = None` first — a python-docx alignment value writes a competing `jc`.

## 4. Table direction — `w:bidiVisual`, only on bilingual tables

`bidiVisual` flips a whole table's column order. Apply it **only** to tables whose headers are Arabic (the bilingual ask table). An English key/value metadata table must stay LTR. If you applied it globally, remove it:

```python
for i, table in enumerate(doc.doc.tables):
    tblPr = table._tbl.tblPr
    if i in rtl_tables:
        if tblPr.find(qn('w:bidiVisual')) is None:
            tblPr.append(OxmlElement('w:bidiVisual'))
    else:
        el = tblPr.find(qn('w:bidiVisual'))
        if el is not None: tblPr.remove(el)
```

Walk `doc.doc.tables` / `doc.doc.paragraphs` — a SamayaDoc wrapper exposes the `Document` as `.doc` and has no `.tables` / `.paragraphs` of its own.

## 5. Mixed AR/EN in one paragraph — wrap Latin runs in LRM

A code or number inside an Arabic run gets reordered. Wrap Latin and digit tokens in U+200E (LRM) so bidi treats each as one isolated LTR unit:

```python
LRM = "\u200e"
LATIN_TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9.\-×/]*[A-Za-z0-9]")
DIGIT_GROUP = re.compile(r"\d[\d,]*\d")
text = DIGIT_GROUP.sub(lambda m: LRM + m.group(0).replace(",", "") + LRM, text)
text = LATIN_TOKEN.sub(lambda m: LRM + m.group(0) + LRM, text)
```

Two ordering rules that matter:

- Strip thousands separators inside Arabic runs. Word breaks the line at the comma, so `6,400` spans two lines and reads as `400.6`.
- Run the **digit-group pass before the Latin pass**. Otherwise the Latin pass consumes `6,400` as a single token and the comma survives the strip.

## Verification — measure, do not eyeball

A vision pass on the rendered image reports Arabic as "mirrored", "garbled" or "wrong word order" even when the underlying text is correct, and it has also asserted numeral reversals that were not present. **Verify from the PDF text layer and line coordinates, which are ground truth:**

```python
import fitz, glob, subprocess, shutil, os
out = "/tmp/rfi_pdf"; shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
subprocess.run(["soffice","--headless","--convert-to","pdf","--outdir",out,*glob.glob("outbox/*.docx")], capture_output=True)
d = fitz.open(sorted(glob.glob(out+"/*.pdf"))[0])
for b in d[0].get_text("dict")["blocks"]:
    for l in b.get("lines", []):
        txt = "".join(s["text"] for s in l["spans"])
        if any("\u0600" <= c <= "\u06FF" for c in txt):
            print(f"x0={l['bbox'][0]:.1f} x1={l['bbox'][2]:.1f} pageW={d[0].rect.width:.0f} | {txt[:70]}")
```

Read the numbers: `x1` at the right page edge = correctly right-aligned; `x0` at the left edge while `w:bidi` is set = the logical/physical `jc` trap of item 3. A code intact in the text layer means bidi handling is correct regardless of what a screenshot reader claims. Then render a PNG and check for overlap and clipping — page geometry still matters; only the Arabic *reading* must be judged from the text layer.

## Fonts

If the specified Arabic font is not installed, LibreOffice substitutes and the preview is not representative. Setting `w:cs` in the file is still correct — the document renders properly wherever the font is installed. Do not switch fonts because a preview looks wrong; report that the font is missing instead.

## Batch generation

Generate each document in a loop over a data dict and write into an `outbox/` folder; keep the per-document content as structured data (title EN/AR, asks as `[no, EN, AR]`) so a re-render after a formatting fix does not require editing prose.