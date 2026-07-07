# Outlook Quotation Discovery — Vendor Patterns

How to find quotation/proposal emails in Outlook's SQLite database for Samaya BIM projects.

## Database Location & Schema

```
~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite
```

**Key table:** `Mail`
**Key columns:**

| Column | Type | Notes |
|--------|------|-------|
| `Record_RecordID` | INTEGER | Primary key |
| `Message_NormalizedSubject` | TEXT | Search here first |
| `Message_SenderAddressList` | TEXT | Sender email |
| `Message_Preview` | TEXT | First ~200 chars of body — search when subject fails |
| `Message_HasAttachment` | BOOLEAN | 1 = has attachment |
| `Message_PartiallyDownloaded` | BOOLEAN | 0 = body local, attachment may still be server-only |
| `Message_TimeSent` | INTEGER | Mac absolute time (seconds since 2001-01-01) |

**Time conversion:**
```sql
SELECT datetime(Message_TimeSent + 978307200, 'unixepoch') AS sent, ...
```

## Search Strategy (Try in Order)

| Priority | Query Pattern | Why |
|----------|--------------|-----|
| 1 | `Subject LIKE '%<brand>%'` | Direct match if brand name is known (Faro, Leica, Artec, MAPTEC) |
| 2 | `Sender LIKE '%<domain>%'` | Distributors use their own domain, not the brand's |
| 3 | `Preview LIKE '%<product>%'` | Product model names often only in the body |
| 4 | `Subject LIKE '%scan%' AND HasAttachment=1` | Catch-all for scanning-related quotations |
| 5 | `Subject LIKE '%quot%' AND HasAttachment=1` | Broad quotation search — filter results manually |

## Reading the Full Email Chain

Once you find one email in the thread, get the full chronology:

```sql
SELECT Record_RecordID, Message_TimeSent, Message_NormalizedSubject,
       Message_SenderAddressList, Message_HasAttachment,
       substr(Message_Preview,1,200)
FROM Mail
WHERE Message_NormalizedSubject LIKE '%<thread keyword>%'
ORDER BY Message_TimeSent;
```

Typical chain pattern: `Initial Request → Demo Scheduling → Demo Confirmation → QUOTATION (with attachment) → Follow-up`

The quotation email (with attachment) is usually near the end of the chain. The last email without attachment is typically a follow-up or confirmation.

## Attachment & Download State

```sql
SELECT Message_HasAttachment, Message_PartiallyDownloaded, Message_DownloadState
FROM Mail WHERE Record_RecordID = <ID>;
```

| HasAttachment | PartiallyDownloaded | DownloadState | Meaning |
|---------------|-------------------|---------------|---------|
| 1 | 0 | 3 | Email body local, **attachment on Exchange server** — not downloadable |
| 1 | 0 | 2 | Both body and attachment local |
| 0 | — | — | No attachment |

When attachment is server-only:
- The user must **open Outlook and click the attachment** to force download
- Outlook may auto-save it to OneDrive as a **4-byte stub file**
- Ask the sender to re-send if it can't be accessed

## Extracting Attachments from Outlook Cache

When `Message_PartiallyDownloaded=0` and `Message_HasAttachment=1`, the attachment may still be stored in Outlook's local cache even if not shown as "downloaded."

### Find Attachment Block IDs

```sql
SELECT hex(b.BlockID), b.BlockTag, b.PathToDataFile
FROM Blocks b
JOIN Mail_OwnedBlocks m ON m.BlockID = b.BlockID
WHERE m.Record_RecordID = <RECORD_ID>
ORDER BY m.BlockTag;
```

The `PathToDataFile` column gives relative paths like `Message%20Attachments/35/GUID.olk15MsgAttachment` — resolve against:
```
~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/
```

### Extract PDF from .olk15MsgAttachment

These files have a proprietary header followed by base64-encoded content starting with `JVBER` (base64 for `%PDF`):

```python
import base64, re

with open('file.olk15MsgAttachment', 'rb') as f:
    data = f.read()

# Find base64 PDF start
idx = data.find(b'JVBER')
if idx >= 0:
    b64_text = data[idx:].decode('ascii', errors='ignore')
    b64_clean = re.sub(r'[^A-Za-z0-9+/=]', '', b64_text)
    pdf_data = base64.b64decode(b64_clean)
    with open('output.pdf', 'wb') as out:
        out.write(pdf_data)
```

Typical file sizes (examples from real Faro attachments):
- `Quotation Faro Blink.pdf` ~ 681 KB (665 KB after decode)
- `Revised_Quotation Faro Focus Premium 200m.pdf` ~ 748 KB (731 KB)
- `11816_Brochure_Blink_AECO_Ltr_AM_ENG.pdf` ~ 4.4 MB (4.2 MB)

When searching the filesystem for quotation PDFs, stubs look like real files but are empty:

```bash
file "path/to/file.pdf"         # Returns "ASCII text" for stub, "PDF document" for real
cat "path/to/file.pdf"          # Content is just "null"
stat -f%z "path/to/file.pdf"    # Exactly 4 bytes
```

**Do NOT** report stub files as "found" or copy them. They are inaccessible. Instead, note the path and advise the user to force OneDrive sync or open in a browser.

Also check the creation date — stubs from the same minute likely came from the same sync event.

## Vendor Email Patterns (Aseer Museum)

### LiDAR Scanning Services (Terrestrial Building Survey)

These vendors provide on-site laser scanning of the building structure (as-built capture).

| Brand | Email Domain | Contact | Subject Pattern |
|-------|-------------|---------|-----------------|
| **Faro** (distributor: ARSSAD ALKHALIJ) | `arssadalkhalij.com` | Mohamed El Hanafi (sales-manager@) | `Faro Focus Premium Scanning for 4000 sqm mostly Indoor Scanning` |
| **Leica** (distributor: SITML) | `sitml.com` | Khabab, A. Ali (aali@) | `Leica RTC360 Lidar Scanning for 4000 sqm mostly Indoor Scanning` |

### Handheld 3D Scanners (Equipment Purchase for Replica Making)

These are equipment purchase quotations for small-object scanning in the replica workshop.

| Brand | Email Domain | Contact | Subject Pattern |
|-------|-------------|---------|-----------------|
| **Shining3D** (via MAPTEC) | `maptec.ae` | MAPTEC sales | `High precision 3d scanner for museum- MAPTEC` |
| **Artec** (via 3DME) | `3d-me.com` | Omar Bittar | `RFQ — Artec Space Spider \| Aseer Regional Museum — Replica Fabrication Project` |
| **Creaform** (via GDS Middle East) | `gdsmiddleeast.com` | GDS sales | `RFQ — Creaform HandySCAN 307 \| Aseer Regional Museum — Replica Fabrication Project` |

## Procurement Folder Organization Pattern

When creating a new folder to organize quotations for a procurement category, use this structure:

```
<Category_Name>/
├── 01_Quotations/       # Vendor proposals, pricing sheets
├── 02_Reference/        # Product spec sheets, brochures, datasheets
└── README.md            # Summary table: vendor, scanner, status, file location
```

The README.md should include:
- A table listing each vendor with model, status (✅/⏳), and which file has the quote
- A brief description of what's being procured

**Distinguish between:**
- **LiDAR scanning services** (hiring someone to scan the building) — Faro Focus, Leica RTC360
- **Equipment purchase** (buying a scanner) — Shining3D FreeScan, Artec Spider, Creaform Go!SCAN

They serve different purposes and go in different folders: scanning services under a dedicated category, equipment purchase under the relevant subcontractor's `10_Purchasing/` directory.
