# DOCX-to-Markdown Conversion Pattern

## When to Use

Converting project DOCX files (plans, comment response sheets, meeting minutes, narrative reports) to Markdown for the repo.

## Technique

Use `python-docx` to walk `doc.element.body` for interleaved paragraphs and tables in document order.

```python
from docx import Document
from docx.oxml.ns import qn
import re

doc = Document('input.docx')

def get_table_md(table):
    """Convert docx table to markdown, escaping pipes."""
    rows = []
    for row in table.rows:
        cells = [cell.text.strip().replace('\n', ' ').replace('|', ' / ') for cell in row.cells]
        rows.append(cells)
    if not rows:
        return ''
    max_cols = max(len(r) for r in rows)
    for r in rows:
        while len(r) < max_cols:
            r.append('')
    lines = ['| ' + ' | '.join(rows[0]) + ' |']
    lines.append('|' + '|'.join(['---'] * max_cols) + '|')
    for row in rows[1:]:
        lines.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(lines)

def para_to_md(para):
    style = para.style.name
    text = para.text.strip()
    if not text:
        return ''
    formatted = ''
    for run in para.runs:
        rt = run.text
        if not rt:
            continue
        if run.bold and run.italic:
            rt = f'***{rt}***'
        elif run.bold:
            rt = f'**{rt}**'
        elif run.italic:
            rt = f'*{rt}*'
        formatted += rt
    if not formatted:
        formatted = text
    if 'Heading 1' in style:
        return f'\n## {formatted}\n'
    elif 'Heading 2' in style:
        return f'\n### {formatted}\n'
    elif 'Heading 3' in style:
        return f'\n#### {formatted}\n'
    elif 'List' in style:
        return f'- {formatted}'
    elif 'TOC' in style:
        return ''
    else:
        return formatted

# Walk body elements in document order
body = doc.element.body
for element in body:
    if element.tag == qn('w:p'):
        for p in doc.paragraphs:
            if p._element is element:
                md = para_to_md(p)
                if md:
                    print(md)
                break
    elif element.tag == qn('w:tbl'):
        for t in doc.tables:
            if t._element is element:
                table_md = get_table_md(t)
                if table_md:
                    print('\n' + table_md + '\n')
                break
```

## Pitfalls

- **Interleaved tables/paragraphs**: `doc.paragraphs` and `doc.tables` are separate lists. To preserve document order, iterate `doc.element.body` children and match each to its object.
- **Pipe characters in table cells**: Must be escaped or replaced, or the markdown table breaks. Use `replace('|', ' / ')`.
- **List Paragraph style**: May have indentation via `w:ind` XML attribute. Check for sub-items with deeper indent.
- **TOC paragraphs**: Style name contains "TOC". Skip them.
- **Bold/italic runs**: Check `run.bold` and `run.italic` flags per run, wrap in `**` / `*`.
- **Empty paragraphs**: Skip when `text.strip()` is empty.

## Worked Examples from This Session

| DOCX Source | MD Output | Size |
|-------------|-----------|------|
| Mobilization Phase-Rev03.docx | 001_Mobilization_Plan_Rev03.md | 12.7 KB, 5 tables |
| Narrative Report Rev05.docx | 006_Narrative_Report_Rev05.md | 6.9 KB, 2 tables |
| BEP Comment Response Sheet.docx | 015_BEP_Comment_Response.md | 12.7 KB, 3 tables |
| BIM Execution Plan REV 01.docx | 00_BIM_Execution_Plan_REV01.md | 81.4 KB, 107 tables |
