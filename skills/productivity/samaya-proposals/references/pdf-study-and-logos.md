# Reference: PDF Study + Logo Collection Workflow

## PDF Text Extraction
```bash
# Method 1: pdftotext (layout-preserving)
pdftotext -layout "input.pdf" - | head -500  # extract first 500 lines

# Method 2: PyMuPDF (Python, best for mixed layouts)
python3 -c "
import fitz
doc = fitz.open('input.pdf')
for page in doc:
    txt = page.get_text()
    if txt.strip():
        print(f'--- Page {page.number+1} ---')
        print(txt)
doc.close()
"

# Method 3: Bulk extraction of all PDFs in folder
python3 -c "
import fitz, os, glob
for f in glob.glob('**/*.pdf', recursive=True):
    doc = fitz.open(f)
    out = '/tmp/pdf_study/' + os.path.splitext(os.path.basename(f))[0] + '.md'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as fout:
        for p in doc:
            txt = p.get_text()
            if txt.strip():
                fout.write(f'## Page {p.number+1}\n\n{txt.strip()}\n\n')
    print(f'{f}: {len(doc)} pages extracted')
    doc.close()
"
```

## Kimi Summarization (when user says "ask kimi")
```bash
# Pipe extracted text to Kimi for summarization
pdftotext -layout "file.pdf" - | kimi -p "Create a comprehensive markdown summary. Include all specs, quantities, materials, dimensions, equipment lists, and technical data. Output ONLY the markdown." --print -y 2>/dev/null

# Or pass the extracted MD file content
cat /tmp/pdf_study/file.md | kimi -p "Summarize this exhibition design document — focus on key specs, materials, equipment, and experience requirements" --print -y 2>/dev/null
```

## Logo Collection
```bash
# Find Samaya logo
find ~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya -name "*samaya*logo*" -type f 2>/dev/null | head -5
# Path: ./Docs/Branding/Samaya-Logo.png (191×71 RGBA PNG)

# Find client logo — download from website
curl -sL "https://www.rcrc.gov.sa" | grep -oiE '(src|href)="[^"]*logo[^"]*"' | head -5

# Convert PNG to base64 data URI
python3 -c "
import base64
with open('logo.png', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
print(f'data:image/png;base64,{b64}')
" > /tmp/logo_data_uri.txt

# Embed in HTML
# <img src="data:image/png;base64,BASE64_HERE" alt="Client Logo" style="height:40px">
```

## Designer Identification
Check the project PDFs/scenographic drawings for the designer/scenographer name:
- Look for title blocks in PDF pages: "SCENOGRAPHER:", "DRAWN BY:", "DESIGNER:"
- Common exhibition designers for KSA: Boris Micka Associates (BMA), various lighting designers like Ada Bonadei
- Once identified, find their logo from their website: `curl -sL "https://designer-site.com" | grep -oiE 'logo[^"]*\.(svg|png)' | head -5`
