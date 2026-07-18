# RFI / Correspondence Review — Pre-Send Checklist

Review bilingual (AR/EN) formal correspondence before sending to CG/PMC/MoC. Covers RFIs, TQs, formal letters, and submittal cover letters.

## Trigger

User sends a DOCX/PDF of a formal letter, RFI, or TQ and asks "review this before sending" or "راجع هذا الخطاب".

## Review Axes (in order)

### 1. Document Reference

| Check | Common Error | Fix |
|-------|-------------|-----|
| RFI ref format | `MOC-MUS-ASE-SIC-1G0-TQ-0027` | `MOC-MUS-ASE-1A0-TQ-0027` — discipline code `1A0` (Arch), not `SIC-1G0` |
| Discipline code | Wrong discipline for the subject | Graphics = `1A0` (Arch), not `1G0` (General) |
| Sequence number | Duplicate or gap | Check `rfi_register.md` for last used number |

**Aseer Museum ref format:** `MOC-MUS-ASE-{Discipline}-{TYPE}-{####}`
- Types: TQ (Technical Query), RFI, ZD (General), PL (Plan), PQ (Prequalification)
- Discipline: 1A0=Arch, 1C0=Civil, 1E0=Electrical, 1M0=Mechanical, 1K0=General, 1L0=Landscape

### 2. Contract References

| Check | Common Error | Fix |
|-------|-------------|-----|
| SoW citation | `ER 2.5` for content-related query | `SoW §2.2` (Scope Exclusions — text/content by MoC) |
| Clause format | `SoW 6.22.1` (no §) | `SoW §6.22.1` or `SoW Clause 6.22.1` |
| Relevance | Citing BIM clause for content request | Only cite the clause that directly supports the request |
| Open queries | `open query TQ-0026` | Verify TQ-0026 is still OPEN in `rfi_register.md` |

**Key contract references for content-related RFIs:**
- `SoW §2.2` — Scope Exclusions: exhibition text, object labels, copyright, imagery by MoC
- `SoW §6.22.1` — Graphic Design scope (text parameters, labelling, image treatment)
- `SoW §8.14` — MoC-provided content and materials

### 3. Signatory / Sender

| Check | Common Error | Fix |
|-------|-------------|-----|
| PM title | `Project Manager` | `Projects Director` (Adel Darwish is PD, not PM) |
| Arabic title | `مدير المشروع` | `مدير المشروعات` |
| Person name | Wrong PM | Waris Sultan = Project Director (Exhibitions) from 13-Jun; Adel Darwish = Projects Director (Interim) |

**Current team (SMP Rev03, 05-Jun-26):**
- PD (Exhibitions): Eng. Waris Sultan (from 13-Jun)
- Projects Director (Interim): Eng. Adel Darwish
- Technical Office Manager: Eng. Mohamed Sultan (user)

### 4. Content Completeness

| Check | What to Verify |
|-------|---------------|
| Items listed | Each requested deliverable has: what, format, language, deadline |
| Deadlines | Match the project's DD gate schedule (50% DD, 90% DD, kick-off) |
| Contractual basis | Each item traces to a contract clause (SoW, ER, DMP) |
| Open queries referenced | Previous related TQ/RFI is cited (e.g., TQ-0026 for content research) |
| Response deadline | 14 calendar days per ER §2.4 — calculate from send date |

### 5. Language & Tone

| Check | Guideline |
|-------|-----------|
| Bilingual balance | AR and EN carry equal weight — both versions say the same thing |
| Diplomatic phrasing | `Samaya kindly requests` / `يسرنا استلام المحتوى على دفعات` — not demanding |
| No AI fingerprints | No `seamlessly`, `cutting-edge`, `robust`, `bespoke`, `§` symbol, emoji |
| Active voice | `Samaya requests` not `It is requested that` |
| British English | colour, programme, centre, metre, organise |

### 6. Table Format (if present)

| Check | Guideline |
|-------|-----------|
| Columns | #, Required Content / Format, المحتوى المطلوب / الصيغة, Needed By / مطلوب بحلول |
| Deadlines | Match project milestones (Before 50% DD, Before 90% DD, Before kick-off, Earliest) |
| Arabic alignment | Right-to-left in DOCX tables — verify after edit |

## Common Corrections Found in Practice

| Issue | Occurrence | Fix |
|-------|-----------|-----|
| Wrong RFI ref | Graphics RFI had `SIC-1G0` instead of `1A0` | Use discipline code matching the subject matter |
| Wrong contract ref | `ER 2.5` (BIM clause) cited for content request | Use `SoW §2.2` (Scope Exclusions) |
| PM vs PD title | `Project Manager` used for Adel Darwish | He is Projects Director (Interim) |
| Arabic title mismatch | `مدير المشروع` | `مدير المشروعات` |

## DOCX Editing (python-docx)

When corrections are needed, edit the DOCX directly using `python-docx`:

```python
from docx import Document

doc = Document(path)

# Edit table cells
table = doc.tables[0]
cell = table.cell(row, col)
for p in cell.paragraphs:
    for run in p.runs:
        if 'old_text' in run.text:
            run.text = run.text.replace('old_text', 'new_text')

# Edit body paragraphs
for p in doc.paragraphs:
    if 'old_text' in p.text:
        for run in p.runs:
            if 'old_text' in run.text:
                run.text = run.text.replace('old_text', 'new_text')

doc.save(path)
```

**Pitfall:** `patch` tool does NOT work on `.docx` files (binary format). Always use `python-docx` via terminal or execute_code.

## Verification After Edit

1. Re-read the DOCX and confirm all corrections applied
2. Check Arabic text didn't get corrupted (RTL rendering)
3. Verify table alignment preserved
4. Report the changes made in a table: # | Before | After
