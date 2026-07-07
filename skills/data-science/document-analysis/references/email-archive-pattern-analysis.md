# Email Archive Pattern Analysis

Analyze email archives (markdown exports) for behavioral patterns, template detection, and AI-generation indicators.

## Use Case

When you have a large email archive (e.g., `.md` files from Outlook downloads, mail clients, or project correspondence logs) and need to understand:
- Who communicates what (sender profiling)
- Whether replies are templated or human-written
- Response time patterns (same-day, next-day, weekends)
- AI-generation indicators in email bodies
- Organizational hierarchy from CC patterns

## Workflow

### 1. Count and list threads

```bash
grep "^## " archive.md | sort -u | wc -l
grep "^## " archive.md | grep -i "keyword" | sort -u
```

### 2. Extract all sender-email patterns

```python
import re

with open("archive.md") as f:
    content = f.read()

# Find all unique From: addresses
froms = re.findall(r'[\w.-]+@[\w.-]+', content)
from collections import Counter
for addr, count in Counter(froms).most_common(30):
    print(f"{count:4d}  {addr}")
```

### 3. Template detection — find repeated body patterns

Split threads by `## ` header, then extract and cluster body openings:

```python
threads = re.split(r'\n(?=## )', content)
bodies = []

for t in threads:
    lines = t.strip().split('\n')
    # Find body start (after Date: line)
    body_start = 0
    for i, l in enumerate(lines):
        if l.startswith('- **Attachments:**') or l.startswith('**Attachments:**'):
            body_start = i + 1
            break
    body = '\n'.join(lines[body_start:]).strip()
    # Get first 80 chars as signature
    opening = body[:80].replace('\n', ' ').strip()
    if opening and len(opening) > 20:
        bodies.append(opening)

from collections import Counter
for phrase, count in Counter(bodies).most_common(20):
    print(f"[{count}x] {phrase}")
```

### 4. Sender profiling per email domain

```python
# Group threads by sender domain
domain_threads = {}
for t in threads:
    if 'cg.com.sa' in t[:500]:  # target domain
        lines = t.strip().split('\n')
        subject = lines[0].replace('## ', '').strip()
        senders = re.findall(r'[\w.-]+@cg\.com\.sa', t[:500])
        domain_threads.setdefault(subject, set()).update(senders)
```

### 5. Response time analysis

Extract CG-sent dates and compare against submission dates to find turnaround times:

```bash
# Find reply timestamps from a specific sender
grep -B3 "target@domain.com" archive.md | grep -i "Date:" | head -20
grep -B3 "target@domain.com" archive.md | grep -i "saturday\|sunday"   # weekend work
```

### 6. Signature standardization

Check whether the same person uses consistent sign-offs:

```bash
grep -h "Best regards\|Regards\|BR," archive.md | grep -i "domain.com" | sort | uniq -c | sort -rn
```

## AI-Generation Indicators in Email Bodies

| Signal | What to look for | Likelihood |
|--------|-----------------|------------|
| **Perfect template reuse** | Same body verbatim across 10+ threads with only ref numbers changing | System template, not AI |
| **Mail-merge formatting** | Classification codes, rigid structure (REF.NO, spaced dashes, fixed capitalization) | Doc control system |
| **Odd spacing** | Space before period, inconsistent caps, punctuation after line break | Template artifact |
| **"Greeting!"** | Exclamation after salutation in formal construction correspondence | Template quirk |
| **Missing characters** | "Externa" vs "External", repeated misspellings in template fields | System typo, not AI |
| **Natural variation** | Different phrasing, contextual references, typos corrected inconsistently | Human-written |
| **Too perfect** | Zero typos, perfect grammar, consistent tone across long text | Possible AI, but rare in construction email bodies |
| **Abrupt style shifts** | Same sender using two distinct formats (one templated, one natural) | System-generated vs personal typing |

**Key insight:** Email bodies in construction project correspondence are almost always templated. The AI question is more relevant for the **attached PDF/Word documents** (technical review comments, reports) than the email cover notes.

## Reference: CG Behavior Analysis (Aseer Museum example)

From weeks 16-23 of the Aseer Museum email archive (~90 CG-sent emails):

**Two distinct formats used by CG:**

| Format | Sender(s) | Template | Used for |
|--------|-----------|----------|----------|
| A - Personalized | melbaz@cg.com.sa | "Dear [Name], Greeting. Kindly find the attached response to submittal [REF]" | Critical items (GBH, DMP, SI) |
| B - Classification | salfeer@cg.com.sa, hmabrouk@cg.com.sa | "Classification-ASE-External-DS-XXXX-XXX / Dear all / Greeting! / Regarding The Museums -Project..." | Routine items (HSE docs, PQ, schedules) |

**Pattern B details (10 emails, 100% identical body):**
```
Classification-ASE-Externa-DS-XXXX-XXXX
Dear all
Greeting!
Regarding The Museums -Project, please Find ATTACHED the requested as per the consultant reply .
[CODE] - [Status]
REF.NO [ref]
```

**Behavioral observations:**
- Weekend replies (Saturdays 3:35 PM, Sundays 8-9 PM) — unusual for Saudi consultant
- "Greeting" (no 's') used 56x vs "Greetings" 43x in week 23 alone — idiosyncratic
- 100% of technical feedback in attached PDFs, never in email body
- Classification code structure: `Classification-ASE-External/Externa-DS-<DISC>-<NUM>`
  - Inconsistent 'l' in External/Externa (6 vs 4 occurrences in week 23)

## Pitfalls

- **Don't confuse mail-merge with AI**: Highly repetitive email bodies are almost always CRM/DMS templates, not AI-generated
- **Markdown headers**: Email archives with `## ` as thread separator — use `\n(?=## )` not just `^## ` for regex splitting when file has leading content
- **Quoted text**: Forwarded/replied email content inside threads pollutes body extraction — skip content after `From:`, `Sent:`, `Subject:` patterns
- **URL-encoded filenames**: Attachment paths in markdown may be URL-encoded (`%20`, `%28`, etc.) — use `urllib.parse.unquote()` when cross-referencing with actual filenames
