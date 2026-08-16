# HTML Body Strip → Readable Text (with table preservation)

When you pull a full email body via AppleScript `content of theMsg` (returns HTML), strip it to readable text while **preserving table structure** so CG rejection tables, deliverable trackers, and status grids stay legible.

## The pattern

```python
import subprocess, re, html

def get_body(eid):
    s = f'''tell application "Microsoft Outlook"
	set theMsg to message id {eid}
	return content of theMsg
end tell'''
    r = subprocess.run(["osascript", "-e", s], capture_output=True, text=True)
    return r.stdout

def clean(b):
    b = re.sub(r'<br\s*/?>', '\n', b)
    b = re.sub(r'</(p|tr|table|div|li)>', '\n', b)   # block tags -> newline
    b = re.sub(r'</td>', ' | ', b)                    # table cells -> pipe (keeps tables readable)
    b = re.sub(r'<[^>]+>', '', b)
    b = html.unescape(b)
    return [l.strip() for l in b.split('\n') if l.strip()]

print('\n'.join(clean(get_body(50892))))
```

Key choices:
- `</td>` → ` | ` turns each table row into a pipe-delimited line — CG deliverable trackers and status tables read as clean columns instead of a wall of text.
- `</(p|tr|table|div|li)>` → newline separates blocks.
- `html.unescape` resolves `&nbsp;`, `&amp;`, `&#39;` etc.
- Filter empty lines with the list comprehension.

## Reading attachment content

After extraction to `/tmp/email_attachments/`:

- **PDF** → `pdftotext -layout <file> -` (poppler). `-layout` preserves column/table alignment and handles Arabic RTL text. **Do NOT rely on `mdls -name kMDItemTextContent`** — it returns `(null)` on many PDFs (especially scanned or Arabic ones). `pdftotext` is the reliable path.
- **DOCX** → `python3 -c "import docx,sys; d=docx.Document(sys.argv[1]); print(chr(10).join(p.text for p in d.paragraphs if p.text.strip()))" <file>` (python-docx). `textutil -convert txt` also works.

## When to use full body vs preview

`Message_Preview` is capped at **255 chars** — fine for triage, but truncates mid-sentence. Always pull the full body via AppleScript for anything you're acting on: CG status codes (A/B/C/D), rejection reasons, deadlines, deliverable counts. The CG code and reviewer comments are often only in the full body or the attached PDF.

## Worked example (2026-08-16)

- Email 50879 "Overdue & Upcoming Design Deliverables" — full body contained the 12-overdue + 160-further deliverables table (discipline | count | forecast | delay). Preview only showed the intro paragraph.
- Email 50907 BMS Understanding Report — CG code **C - Revise and Resubmit** with 2 numbered comments was in the attached PDF (`pdftotext -layout`), not the preview.
- Email 50916 SPS ICT Understanding Report — content was in the attached `.docx` (python-docx), not the email body.
