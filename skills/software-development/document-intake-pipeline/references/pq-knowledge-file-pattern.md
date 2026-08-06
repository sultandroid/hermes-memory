# PQ Knowledge File Pattern — Batch Conversion to Structured MD

When you receive multiple prequalification (PQ) PDFs for a project and need to convert them into structured knowledge files in the repo, use this pattern.

## When to Use

- Multiple PQ PDFs arrive (email attachments, OneDrive, Aconex) for different suppliers/trades
- User asks to "read and convert PQ documents to MD knowledge files"
- Need a searchable, structured reference for supplier prequalification status, CG comments, and clearance paths

## Workflow

### Step 1: Identify the PQ PDFs

Look for filenames matching the pattern `*PQ-*` in the source directory. Each PQ typically has:
- A cover sheet (PQ submittal form with CG status code and comments)
- Attached company profile / catalog pages

### Step 2: Extract Text (with Fallback Chain)

```bash
# Primary: pdftotext
pdftotext "file.pdf" /tmp/output.txt

# Fallback 1: layout mode
pdftotext -layout "file.pdf" /tmp/output.txt

# Fallback 2: PyMuPDF (handles many corrupted PDFs)
python3 -c "
import fitz
doc = fitz.open('file.pdf')
text = ''.join(page.get_text() for page in doc)
doc.close()
with open('/tmp/output.txt', 'w') as f: f.write(text)
print(f'{len(text)} chars')
"

# Fallback 3: pdfminer
python3 -c "
from pdfminer.high_level import extract_text
text = extract_text('file.pdf')
with open('/tmp/output.txt', 'w') as f: f.write(text)
print(f'{len(text)} chars')
"

# Fallback 4: pdfplumber (table-heavy PDFs)
python3 -c "
import pdfplumber
with pdfplumber.open('file.pdf') as pdf:
    text = '\n'.join(p.extract_text() or '' for p in pdf.pages)
    with open('/tmp/output.txt', 'w') as f: f.write(text)
    print(f'{len(text)} chars')
"
```

**Always check output file size** — a 0-byte or tiny output means extraction failed even if exit code was 0.

### Step 3: Classify by Trade

Group the PQ PDFs by their discipline code from the submittal number:

| Code | Discipline | Example |
|------|-----------|---------|
| 1A0 | General / Architectural | Setwork, furniture suppliers |
| 1C0 | Structural / Civil | Rigging, lifting specialists |
| 1E0 | Electrical | Audio, electrical suppliers |
| 1M0 | Mechanical | HVAC, plumbing suppliers |
| 1K0 | Specialist | AV, IT, security suppliers |

### Step 4: Extract Key Fields from Each PQ

From the cover sheet (always extractable even if body is image-based):

| Field | Location in PQ form |
|-------|-------------------|
| Submittal No | Top of form (e.g. MOC-MUS-ASE-1A0-PQ-0139) |
| Submittal Date | Next to submittal no |
| Revision No | Usually 00 for first submission |
| Description | "Prequalification Document for [scope]" |
| Supplier Name | "Subcontractor:" field |
| CG Status Code | A/B/C/D in the approval status section |
| CG Comments | "CG Comments:" section |
| Prepared By | Project Manager (usually Eng.Mohamed Waris) |
| CG Reviewer | Name in "Revision By:" field (e.g. Mansour Alrezeni, Abdrabo Shahin) |

### Step 5: Create Knowledge Files by Trade Category

Organize into one `.md` file per trade category (not one per supplier). Structure:

```markdown
---
last_updated: YYYY-MM-DD
owner_agent: Hermes
status: active
source: [list of PQ submittal numbers]
---

# [Trade Category] — PQ Knowledge

## PQ-NNNN — [Supplier Name]

**CG Code:** [A/B/C/D] | **Submitted:** [Date] | **Scope:** [Description]

### Company Profile
- **Company:** [Full legal name]
- **Website:** [URL if available]
- **Founded:** [Year]
- **HQ:** [Location]
- **Key facts:** [Factory size, employees, certifications, etc.]

### Scope Offered
- [Bullet list of products/services offered]

### CG Comments
> **Status:** Code [X] — [Approved/Approved AS Noted/Revise and Re-submit/Disapproved]
> **Comments:**
> 1. [CG comment 1]
> 2. [CG comment 2]

### Path to Clearance
1. [Action item 1 to address CG comments]
2. [Action item 2]

### Relevant Docs
| File | Description |
|------|-------------|
| MOC-MUS-ASE-XXX-PQ-NNNN | [Brief description + size] |
```

### Step 6: CG Status Code Meanings

| Code | Meaning | Action Required |
|------|---------|-----------------|
| A | Approved | No further action |
| B | Approved AS Noted | Address minor comments, resubmit |
| C | Revise and Re-submit | Major revisions needed per CG comments |
| D | Disapproved | Supplier rejected — cannot proceed |

### Step 7: Common CG Comment Patterns for PQs

- **"Lacks relevant experience in similar projects"** (Code D) — supplier is rejected, no resubmission path
- **"Submit supporting documents, references, scope of work"** (Code C) — supplier needs to provide evidence
- **"Missing legal documents (Chamber of Commerce, GOSI)"** (Code C) — administrative gap
- **"Provide organizational structure with key personnel CVs"** (Code C) — team depth gap
- **"Define scope of work in detail"** (Code C) — scope clarity gap

### Pitfalls

- **Corrupted PDFs are common** — many project PDFs have broken xref tables. Always use the fallback chain and check output file size
- **Cover sheet text is almost always extractable** even when the body (catalog pages) is image-based. Don't assume a short extraction means the PDF is empty
- **Identical CG comments across multiple PQs** — when multiple suppliers for the same trade are submitted together, CG often copies the same comments. Group them in one file
- **Company profile content may be image-only** — catalog pages, product photos, and certificates are often embedded as images. Text extraction will only get the cover sheet
- **Some PQ PDFs are genuinely corrupted** — if ALL extraction tools fail (Unexpected EOF, object is not a stream), the PDF must be re-sourced from the sender
