# BIM Unit Project Information Search

Search strategy for finding project scope, content, and status information across Samaya BIM Unit project folders.

## Folder Structure Pattern

```
Bim Unit/
├── {Project Name}/
│   ├── Email_Archive/       ← sorted archived emails (YAML frontmatter + limited body)
│   ├── _Unsorted_Emails/
│   │   └── Email_Archive/   ← often MORE COMPLETE than sorted archive
│   ├── Submittal's/
│   │   ├── Arch/
│   │   ├── Mep/
│   │   └── Struc/
│   ├── Design Files/
│   │   └── {date}/
│   ├── Docs/
│   ├── As-Built Docs/
│   ├── B.O.Q/
│   ├── Contracts/
│   ├── Invoices/
│   ├── Reports & Meeting/
│   ├── Revit Files/
│   │   ├── Pdf/
│   │   ├── Rvt/
│   │   └── ...
│   ├── Specs & Datasheet/
│   └── Time Scheduales/
```

## Search Priority

1. **Email subject lines first** — `ls Email_Archive/` reveals project scope, parties, and timeline from filenames
2. **`_Unsorted_Emails/Email_Archive/`** — often contains fuller email content including replies with scope descriptions
3. **Submittal PDFs** — may contain project report/scope docs (try `pdftotext`, may be image-only)
4. **Design Files** — location plans, CAD exports
5. **Docs/PROJECT_EMAILS.md** — some projects have a summary file
6. **Specs & Datasheet/GENERAL SPECIFICATIONS/** — CSI-format specs (usually not project-specific)

## Pitfalls

- **`.bak` OneDrive backup may have zeroed-out files** — many `.md` email archives in the `.bak-*` directory contain `\u0000` null bytes. The actual content was never synced. Use the live OneDrive path instead.
- **Email archives are frontmatter only** — body content is often truncated. Attachment descriptions (not content) may be in the body. Key info (scope, pricing, designs) is in attachments (PDF/DWG) not captured as text.
- **PDFs are image-based** — frequent with Illustrator/InDesign exports. `pdftotext` returns empty. Need OCR (pymupdf → tesseract) or view the actual PDF.
- **DWG files** — no text extraction path without AutoCAD. Filename and metadata only.
- **OneDrive `compressed,dataless` files** — show as 4-byte "null" stubs. Hydrate via `open` (Preview) before reading.

## Email Subject Clues for Scope Discovery

Email subject patterns that reveal project content:

| Pattern | What it tells you |
|---------|-------------------|
| `طلب تسعير {الموقع} {الدور}` | Pricing request for a specific floor/zone |
| `معرض {الموضوع}` | Exhibition name/theme |
| `مشروع منطقة استقبال {المعرض}` | Reception area for an exhibition |
| `تصميمات ابواب ({المشروع})` | Door designs for a project |
| `{مادة/عمل} {المعرض/المشروع}` | Specific material/work for a project |
| `Al {Name} Exhibition_MEK` | Reference to Mimar Interiors design scope |
| `الرسومات التنفيذيه {لـ} {المشروع}` | Execution/Shop drawings |

## Email Body Reading

When reading archived emails via `read_file`, the format is:

```
# {Subject}

- **Date:** ...
- **From:** ...
- **Archived:** ...
- **RecordID:** ...
- **Attachments:** Yes (see Attachments folder)

---

{email body text}
```

For emails with only frontmatter and no body, the attachment content is stored separately and not accessible as text. Look for related email threads with "RE:" or "Fw:" prefixes that may reference the same attachment.

## Known Project Directories

```
Bim Unit/
├── Aseer-Museum/
├── Jabal Al-Noor Dispatch Building - Makkah/   ← Holy Quran Museum
├── Khair El-Khalq Museum/
├── Zamzam Museum/
├── El-Haramain Museum/
├── El-Ghamama Museum/
├── Al Galal & Al Gamal Meuseum/
└── ... (~20+ projects)
```

## Example Search Workflow

```
1. ls "Bim Unit/{Project}/Email_Archive/" | sort       → scan email subjects
2. ls "Bim Unit/{Project}/_Unsorted_Emails/Email_Archive/" | sort  → check for fuller content
3. check Submittal's/ for report PDFs
4. pdftotext on any PDF with "RPT" or "report" in filename
5. check Design Files/ for location/scope plans
6. search_files across project root for specific terms
```
