# Aseer Museum MoM (Minutes of Meeting) PDF Extraction Pattern

**Session:** 2026-07-26  
**Source:** `Adel Darwish's files - 01- Execution Documents/06- Weekly Meeting MOM/*.pdf`  
**Prepared by:** ACE (PMC)  
**Format:** Weekly progress meetings, MoM 02-15 (MoM 01 & 06 missing)

## Document Structure

All MoM PDFs follow a consistent ACE template:

```
MINUTES OF MEETING – NO. XX
Subject: Progress meeting
Current Date: DD-MMM-YYYY
Project: Aseer Museum project
Time: HH:MM - HH:MM PM
Venue: MOC & online
Minutes prepared by: ACE

S/N ATTENDEES REP. COMPANY TITLE
1 Eng. Name               COMPANY    Title
...

SI DUE DATE - Priority POINTS DISCUSSED ACTION BY Statues No. NEXT STEP
1- SECTION NAME:
1.1 High Description...   COMPANY   DATE   Status
```

## Key Extraction Patterns

### 1. MoM Number
```
MINUTES OF MEETING – NO. 15
```
→ Extract via regex: `MINUTES OF MEETING.*?NO\.?\s*(\d+)`

### 2. Date
```
Current Date: 13-Jul-26
```
→ `Current\s+(\d{1,2}-[A-Za-z]{3}-\d{2,4})`

### 3. Time
```
Time 03:00 - 05:00 PM
DTiamtee: 3:00 - 5:00 PM   (OCR artifact for "Time")
```
→ Multiple patterns: `Time\s+([\d:.\s\-APMapm]+)` or `DTiamtee:\s*([\d:.\s\-APMapm]+)`

### 4. Attendee Table
Header: `S/N ATTENDEES REP. COMPANY TITLE` (or `S/N  ATTENDEES REP. COMPANY TITLE` with double space)

Rows follow pattern:
```
1 Eng.Mohamed Farouk ACE - PMC Projects director
2 Eng.Ahmed Ramadan ACE - PMC Project manager
```
Split by 2+ spaces: `re.split(r'\s{2,}', line.strip())`

Count by company: ACE/PMC, CG/Supervision, SAMAYA, MOC

### 5. Section Headers
Numbered sections with colon:
```
1- MOBILIZATION:
2- DESIGN PHASE:
3- MATERIAL:
4- SPECIALIZED PARTIES & PROJECT TEAM:
5- PERMITS:
6- PLANNING:
7- EXECUTION ACTIVITIES:
7- MONITOR AND CONTROL:  (duplicate section number)
8- QS & PAYMENT:
9- HSE:
10- NEXT MEETING:
```

Note: Section numbers can repeat (two "7-"). Use text content to distinguish.

### 6. Action Items within Sections
Pattern:
```
1.1 High Samaya requested...    COMPANY   DATE   Status
```
Three-column table: Item, Priority, Description → Action By, Due Date, Status

## PDF Text Layer Quality

These PDFs have **partial text layers** (created via PostScript → Acrobat Distiller):
- Producer: `PScript5.dll Version 5.2.2` + `Acrobat Distiller`
- Text is extractable but may have OCR artifacts:
  - "Time" → "DTiamtee" 
  - "Current" → "Current " (extra spaces)
  - Numbers like "1.1" may render as "1 1" or "1.1"
  - Arabic text may be mirrored

**Always try PyMuPDF `page.get_text()` first** — it's faster and more accurate than full-page OCR for these.

## Extraction Pipeline (Python)

```python
import fitz
import re

def extract_mom(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = ""
    for page in doc:
        text = page.get_text()
        if text.strip():
            all_text += text + "\n\n"
    
    data = {
        'mom_number': None,
        'date': None,
        'time': None,
        'venue': None,
        'prepared_by': None,
        'attendees': [],
        'next_meeting': None,
        'sections': {}
    }
    
    # MoM number
    m = re.search(r'MINUTES OF MEETING.*?NO\.?\s*(\d+)', all_text, re.IGNORECASE)
    if m: data['mom_number'] = int(m.group(1))
    
    # Date
    for pat in [r'Current\s+(\d{1,2}-[A-Za-z]{3}-\d{2,4})',
                r'Current Date:\s*(\d{1,2}-[A-Za-z]{3}-\d{2,4})']:
        m = re.search(pat, all_text)
        if m: data['date'] = m.group(1); break
    
    # Time
    for pat in [r'Time\s*:?\s*([\d:.\s\-APMapm]+)',
                r'DTiamtee:\s*([\d:.\s\-APMapm]+)']:
        m = re.search(pat, all_text)
        if m: data['time'] = m.group(1).strip(); break
    
    # Venue
    m = re.search(r'Venue\s+(.+?)\n', all_text)
    if m: data['venue'] = m.group(1).strip()
    
    # Prepared by
    m = re.search(r'Minutes prepared by\s+(.+?)\n', all_text)
    if m: data['prepared_by'] = m.group(1).strip()
    
    # Attendees - find table after header
    attendee_idx = all_text.find('S/N ATTENDEES')
    if attendee_idx < 0:
        attendee_idx = all_text.find('ATTENDEES REP. COMPANY TITLE')
    if attendee_idx >= 0:
        subtext = all_text[attendee_idx:]
        # Stop at Notes, SI, POINTS, or Priority
        for stop in ['\nNotes', '\nSI ', '\nPOINTS', '\nPriority', '\n\n\n']:
            e = subtext.find(stop)
            if e >= 0: subtext = subtext[:e]; break
        
        for line in subtext.split('\n')[1:]:  # skip header
            line = line.strip()
            if not line: continue
            parts = re.split(r'\s{2,}', line)
            if len(parts) >= 4 and parts[0].isdigit():
                data['attendees'].append({
                    'sn': parts[0],
                    'name': parts[1].strip(),
                    'company': parts[2].strip(),
                    'title': parts[3].strip()
                })
    
    # Next meeting
    for pat in [r'next meeting is scheduled for\s+(.+?)(?:\.|$)',
                r'Next Meeting\s*\n\s*(.+?)(?:\n\s*\n|\nNotes|\n\d|$)']:
        m = re.search(pat, all_text, re.IGNORECASE | re.DOTALL)
        if m: data['next_meeting'] = m.group(1).strip(); break
    
    # Sections - numbered headers
    section_splits = re.split(r'\n(\d+[-–]\s*[A-Z\s&]+):', all_text)
    # section_splits[0] = before first, then alternating header, content, header, content...
    if len(section_splits) > 1:
        for i in range(1, len(section_splits), 2):
            header = section_splits[i].strip()
            content = section_splits[i+1] if i+1 < len(section_splits) else ""
            # Clean content
            for stop in ['\nNotes', '\nSI ', '\nPOINTS', '\nPriority', '\nS/N ATTENDEES']:
                idx = content.find(stop)
                if idx >= 0: content = content[:idx]
            data['sections'][header] = content.strip()
    
    doc.close()
    return data
```

## Formatting for Repository

Target output matches `00_Status/meeting_minutes.md` style:

```markdown
## MoM No. 15 — 13-Jul-26

| Field | Value |
| --- | --- |
| Subject | Progress meeting |
| Date / Time | 13-Jul-26 · 3:00–5:00 PM |
| Venue | MOC & online |
| Prepared by | ACE (PMC) |
| Attendees | 27 — ACE/PMC ×6, CG/Supervision ×11, Samaya ×10 |
| Next meeting | Monday 20-Jul-2026, 3:00 PM |

### Key points by section

**1 · Mobilization** — **80%**. Outstanding: security cameras, elec & water supply (target 20-Jul). Meeting/sample/storage rooms **Done**.

**2 · Design Phase** — Showcase package Rev3 to be submitted 16-Jul...
```

## Section Name Mapping

| PDF Section | Repo Display Name |
|-------------|-------------------|
| MOBILIZATION | 1 · Mobilization |
| DESIGN PHASE / DESIGN | 2 · Design Phase / 2 · Design |
| MATERIAL | 3 · Material |
| SPECIALIZED PARTIES & PROJECT TEAM | 4 · Specialized parties & project team |
| PERMITS | 4 · Permits / 5 · Permits |
| PLANNING | 5 · Planning / 6 · Planning |
| EXECUTION ACTIVITIES | 6 · Execution / 7 · Execution Activities |
| MONITOR AND CONTROL | 7 · Monitor & Control |
| QS & PAYMENT | 8 · QS & Payment |
| HSE | 9 · HSE |
| NEXT MEETING | 10 · Next Meeting |

Note: Section numbers shift between MoMs (e.g., Permits moves from 4→5 as new sections insert).

## Pitfalls

1. **Duplicate section numbers** — MoM 15 has two "7-" (Execution Activities + Monitor and Control). Distinguish by content.
2. **Time field OCR artifact** — "Time" → "DTiamtee" in newer MoMs. Match both patterns.
3. **Attendee table format varies** — Early MoMs use `S/N ATTENDEES REP. COMPANY TITLE`, later ones use `S/N  ATTENDEES` (double space). Split on 2+ spaces.
4. **Date format inconsistency** — "13-Jul-26" vs "06-Jul-26" vs "29-Jun-26". Normalize to DD-MMM-YY.
5. **Missing MoMs** — MoM 01 and 06 not in Adel's bank. Note gaps in repo.
6. **Text layer vs OCR** — For MoM 02-05 (older), text layer is clean. MoM 07+ have partial OCR artifacts. Always try text layer first.
7. **Next meeting parsing** — "Monday, 20 Jul 2026, at 03:00 PM" format. Use flexible regex.
8. **Company name normalization** — "ACE - PMC" → "ACE/PMC", "CG - Supervision" → "CG/Supervision", "SAMAYA - Main Contractor" → "Samaya".

## MoM Inventory (Adel's Bank)

| File | MoM # | Date | Sections Found |
|------|-------|------|----------------|
| 02- WEEKLY MEETING 02 (05-01-2026).pdf | 2 | 5-Jan-2026 | Mobilization, Design, Project team, Permits, Document control |
| 03- WEEKLY MEETING 03 (12-01-2026).pdf | 3 | 12-Jan-2026 | Mobilization, Design, Project team, Document control |
| 04- WEEKLY MEETING 04 (19-01-2026).pdf | 4 | 19-Jan-2026 | Mobilization, Design, Project team, Document control |
| 05- WEEKLY MEETING 05 (26-01-2026).pdf | 5 | 26-Jan-2026 | Mobilization, Design, Project team, Document control, QS & PAYMENT |
| 06- WEEKLY MEETING 07 (16-02-2026).pdf | 7 | 16-Feb-2026 | Mobilization, Design, Project team, Permits, Planning, Monitor, Document control, QS |
| 08- WEEKLY MEETING 08 (23-02-2026).pdf | 8 | 23-Feb-2026 | ... |
| 09- WEEKLY MEETING 09 (03-03-2026).pdf | 9 | 2-Mar-2026 | ... |
| 10- WEEKLY MEETING 10 (11-05-2026).pdf | 10 | 11-May-2026 | 10 full sections |
| 11- ASEER WEEKLY MEETING 11 (18-05-2026).pdf | 11 | 18-May-2026 | 10 full sections |
| 12- ASEER WEEKLY MEETING 12 (09-06-2026).pdf | 12 | 9-Jun-2026 | 10 full sections |
| 13- ASEER WEEKLY MEETING 13 (29-06-2026).pdf | 13 | 29-Jun-2026 | 10 full sections |
| 14- ASEER WEEKLY MEETING 14 (06-07-2026).pdf | 14 | 6-Jul-2026 | 10 full sections |
| 15- ASEER WEEKLY MEETING 15 (13-07-2026).pdf | 15 | 13-Jul-2026 | 11 sections (includes MATERIAL) |

Total: 13 PDFs (MoM 02-05, 07-15). Gaps: MoM 01, MoM 06.