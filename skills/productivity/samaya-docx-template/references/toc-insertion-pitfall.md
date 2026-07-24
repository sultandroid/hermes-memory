# TOC Insertion Pitfall — DOCX Editing

When inserting new paragraphs into a DOCX that has a Table of Contents (TOC), **new content inserted between TOC entries inherits `toc` style** and appears in the TOC as garbage entries.

## Correct pattern

```python
# Find the last TOC paragraph
toc_end = 0
for i, p in enumerate(doc.paragraphs):
    if p.style.name.startswith('toc'):
        toc_end = i

# Insert new content AFTER the TOC block
insert_point = toc_end + 1
# Use insert_paragraph_before() on the paragraph AFTER the TOC
new_p = doc.paragraphs[insert_point].insert_paragraph_before('')
new_p.style = doc.styles['Normal']
run = new_p.add_run('New content here')
run.font.size = Pt(10)
```

## Wrong pattern (causes TOC contamination)

```python
# Inserting between TOC entries — new paragraphs inherit toc style
new_p = doc.paragraphs[5].insert_paragraph_before('')  # Inside TOC block
```

## Verification

After inserting, check that no body-text paragraphs have `toc` style:

```python
for i, p in enumerate(doc.paragraphs):
    if i > toc_end and p.style.name.startswith('toc'):
        p.style = doc.styles['Normal']  # Fix any that slipped through
```

## Root cause

`insert_paragraph_before()` creates a new paragraph that inherits the style of the paragraph it was inserted before. If that reference paragraph has `toc` style, the new one does too. Always insert before the first non-TOC paragraph after the TOC block, not before a TOC entry.
