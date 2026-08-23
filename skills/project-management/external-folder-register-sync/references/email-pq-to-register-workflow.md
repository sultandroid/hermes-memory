# Email PQ/Attachment Batch → Filing → Knowledge Extraction

Worked pattern (2026-07-26 PQ extraction, 27 emails → 46 files) for processing
a batch of email attachments into the repo.

## 1. Extract attachments (AppleScript generator)

Outlook is locked; use AppleScript. Generate one `.applescript` per email id
(keep under ~700-byte body limit), batch 5-6 per terminal call:

```python
for eid in ids:
    script = f'''set o to "/tmp/pq_attachments/"
tell application "Microsoft Outlook"
    set m to message id {eid}
    repeat with a in (every attachment of m)
        if content type of a does not start with "image/" then
            set n to name of a
            set my text item delimiters to "/"
            set nParts to text items of n
            set my text item delimiters to "-"
            set n to nParts as string
            set my text item delimiters to ""
            set p to o & "{eid}_" & n
            do shell script "touch " & quoted form of p
            save a in (POSIX file p as alias)
        end if
    end repeat
end tell
'''
```

## 2. Read PDFs to text

```bash
pdftotext -layout file.pdf out.txt   # table layout; falls back to plain if empty
```

Some PDFs are scanned images (CE DoCs, authorization letters) → empty text; flag them, do not assume broken.

## 3. File to OneDrive — OneDrive File Provider blocks ALL writes

See SKILL.md pitfall. Stage the organized structure under `/tmp/` or
`/Volumes/MIcro/Temp/`, write a `_FILE_MAPPING.md` (not `.csv`, gitignored),
open both staging root + OneDrive target in Finder, ask user to drag-drop.

## 4. Update registers

Map extracted files to register rows: CG response code (from email preview +
`pdftotext` of the CG PDF), new PQ refs, vendor entries. Bump `last_updated`
frontmatter. Prefer the repo `document_intake.py` pipeline for bulk intake
(see SKILL.md Pipeline-First Rule).

## 5. Knowledge base from the PDFs

After extraction, delegate 3 parallel sub-agents (one per specialist group) to read
the text extracts and write combined `*_knowledge/*.md` (acoustic, landscaping+labs,
av_vendors_materials). Each entry: company profile, certifications, CG code,
clearance path. File under `Technical_Office/Specialist_Management/pq_knowledge/`.
