# DOCX XML Patching — Fix Specific Text Without Regenerating

When you need to fix specific text strings in an existing .docx (e.g. change "75%" to "60%" in Fida's document) without regenerating the whole file, patch the XML directly inside the zip.

## Why Not python-docx?

`python-docx` can only find text in paragraphs, not in table cells with complex formatting. For documents with heavy tables (Fida's SMP has 20+ tables), `python-docx` often returns 0 matches because the text lives in runs inside table cells that the library doesn't traverse the same way.

## Technique: Direct XML Edit

A .docx file is a ZIP archive. The document content lives in `word/document.xml`. Edit that XML directly:

```python
import zipfile, shutil, tempfile

src = 'original.docx'
out = 'fixed.docx'

# Read XML
with zipfile.ZipFile(src, 'r') as z:
    xml = z.read('word/document.xml').decode('utf-8')

# Fix specific text strings
# Use exact w:t element content — grep for <w:t>...text...</w:t>
xml = xml.replace(
    '<w:t>Old text to replace</w:t>',
    '<w:t>New text</w:t>'
)

# Write back
tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
tmp.close()

with zipfile.ZipFile(src, 'r') as zin:
    with zipfile.ZipFile(tmp.name, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'word/document.xml':
                zout.writestr(item, xml.encode('utf-8'))
            else:
                zout.writestr(item, data)

shutil.move(tmp.name, out)
```

## Finding the Right Text to Replace

First, find the exact `w:t` element content:

```python
import zipfile, re

with zipfile.ZipFile(src, 'r') as z:
    xml = z.read('word/document.xml').decode('utf-8')

# Find all w:t elements containing your target text
for m in re.finditer(r'<w:t[^>]*>[^<]*TARGET_TEXT[^<]*</w:t>', xml):
    print(m.group())
```

This shows the exact string including XML entities (`&amp;ge;` for `≥`, `&amp;` for `&`).

## Pitfalls

- **XML entities**: `≥` in the rendered text is `&amp;ge;` in the XML. Search for the encoded form.
- **`xml:space="preserve"`**: Some w:t elements have this attribute. Include it in your match: `<w:t xml:space="preserve"> text </w:t>`
- **Split runs**: Long text may be split across multiple `<w:r>` elements. Each `<w:t>` contains a fragment. You can only replace within a single `<w:t>`, not across runs.
- **Backup first**: Always keep the original. A bad XML replacement can corrupt the file.
- **Verify**: After replacement, check the file opens in Word and the fix is visible.
