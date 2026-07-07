# Medical Lab Report OCR — Arabic/English Pipeline

Extract structured data from hospital lab report photos/PDFs (mixed Arabic/English), update a historical Excel tracker, and generate an HTML trend dashboard with Chart.js.

## Tools

```bash
brew install tesseract tesseract-lang       # OCR engine + Arabic
pip3 install pillow pytesseract openpyxl    # Python deps
```

## OCR Pattern for Medical Reports

### Step 1: OCR the image

```python
from PIL import Image
import pytesseract

img = Image.open('/path/to/lab_report.jpg')
img = img.convert('L')  # grayscale — improves OCR accuracy
text = pytesseract.image_to_string(img, lang='ara+eng')
```

### Step 2: Parse structured fields

Medical reports have predictable sections. Parse by scanning for known markers:

```python
# Common markers in Arabic/English lab reports
def extract_value(text, markers):
    """Find first number after any of the marker strings."""
    for marker in markers:
        if marker in text:
            # Find the numeric value near the marker
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if marker in line:
                    # Try current line for a number, then next line
                    for check in [line, lines[i+1] if i+1 < len(lines) else '']:
                        nums = re.findall(r'[\d]+[.,\d]*', check.replace(',', ''))
                        if nums:
                            return float(nums[0])
    return None

results = {
    'cholesterol': extract_value(text, ['CHOLESTEROL', 'الكوليسترول']),
    'triglycerides': extract_value(text, ['TRYGLYCERIDES', 'الدهون الثلاثية']),
    'hdl': extract_value(text, ['HDL']),
    'ldl': extract_value(text, ['LDL', 'cholesterol']),
    'creatinine': extract_value(text, ['CREATININE', 'الكرياتينين']),
    'sgpt': extract_value(text, ['SGPT', 'ALT', '58.10']),
    'b12': extract_value(text, ['B12', 'cyanocobalamin']),
    'tsh': extract_value(text, ['TSH', 'Thyroid']),
    'd3': extract_value(text, ['D3', 'VITAMIN D', 'Vitamin D']),
}
```

### Step 3: Extract CBC (Complete Blood Count)

CBC results appear in a tabular format. Extract by matching each test name:

```python
cbc_map = {
    'WBC': (4, 11), 'RBC': (4.5, 6), 'Hemoglobin': (13.5, 17.5),
    'Hematocrit': (37, 53), 'MCV': (76, 96), 'MCH': (26, 34),
    'MCHC': (32, 36), 'RDW': (40.05, 47.81), 'Platelets': (150, 450),
    'MPV': (6.5, 12),
}
for test_name, (ref_low, ref_high) in cbc_map.items():
    val = extract_value(text, [test_name, test_name.upper()])
    if val:
        print(f'{test_name}: {val} (ref {ref_low}-{ref_high})')
```

### Step 4: Parse test date from report header

```python
date_match = re.search(r'(\d{2})[-/](\d{2})[-/](\d{4})', text)
if date_match:
    day, month, year = date_match.groups()
    test_date = f'{year}-{month}-{day}'  # YYYY-MM-DD
```

## Updating the Historical Excel

Maintain a `Blood_Analysis_History.xlsx` with columns: Test Name, Normal Range, then one date column per test. Append new results to the latest column.

```python
import openpyxl
from datetime import datetime

wb = openpyxl.load_workbook('Blood_Analysis_History.xlsx')
ws = wb.active

# Find the last column with data
last_col = ws.max_column
new_col = last_col + 1

# Write the new date
ws.cell(row=2, column=new_col).value = datetime.now()

# Write each test result to its row
row_map = {
    'cholesterol': 3, 'creatinine': 4, 'triglycerides': 5,
    'hdl': 7, 'ldl': 8, 'sgpt': 10,
    'b12': 13, 'tsh': 14, 'd3': 15,
}
for test_name, row in row_map.items():
    if test_name in results and results[test_name] is not None:
        ws.cell(row=row, column=new_col).value = results[test_name]

# Add CBC rows if they don't exist
cbc_start_row = 17  # after existing data
# ... write CBC rows

wb.save('Blood_Analysis_History.xlsx')
```

## Generating the HTML Dashboard

Create an HTML dashboard with Chart.js for trend visualization:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
```

**Chart pattern** — one line per metric with reference range overlays:

```javascript
const dates = ['Jun 2018', 'Aug 2018', 'May 2019', 'Oct 2021', 'May 2024', 'May 2025', 'Dec 2025', 'Jun 2026'];
const data = [278, 223, 241.89, 224, 234, 230, 239.45, 227.59];

new Chart(ctx, {
  type: 'line',
  data: {
    labels: dates,
    datasets: [
      { label: 'Cholesterol', data, borderColor: '#8b5cf6', fill: true, tension: .3 },
      { label: 'Upper limit', data: Array(dates.length).fill(200),
        borderColor: '#ef4444', borderDash: [6,3], pointRadius: 0, fill: false }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: { y: { beginAtZero: false } }
  }
});
```

**Dashboard sections to include:**
1. Patient info header (name, file#, DOB, hospital, test date)
2. Summary badges (color-coded: 🔴 high, 🟢 normal, 🔵 low)
3. Trend charts (Cholesterol, Triglycerides, HDL, LDL) with ref range lines
4. Current results table (Lipid Profile, CBC, Hormones) with status + trend arrows
5. Summary & recommendations section

## Pitfalls

1. **Arabic/English mixed OCR is noisy** — tesseract produces garbled characters in the other script. Parse by looking for English uppercase keywords first (CHOLESTEROL, HDL, LDL), fall back to Arabic markers.
2. **Date format confusion** — DD/MM/YYYY vs MM/DD/YYYY. Arabic medical reports use DD/MM/YYYY. Python's `datetime.strptime` may misinterpret. Always confirm from context (e.g., the report date vs collection date).
3. **Garbled images** — Some report pages (barcode labels, signature lines, Arabic-only sections) produce near-unreadable OCR. Skip these — the structured data is on other pages.
4. **Multi-page reports** — CBC on page 1, Chemistry on page 2, Hormones on page 3. OCR each image separately and merge results.
5. **Reference ranges vary by lab** — Always extract the ref range from the report (printed next to each result) rather than using hardcoded values.
6. **Chart.js requires internet CDN** — for offline use, download chart.js locally and reference it via `file:///`.
