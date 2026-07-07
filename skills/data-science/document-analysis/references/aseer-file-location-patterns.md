# Aseer Museum — File Location & Comparison Sheet Extraction

**Context**: Finding and extracting 3D scanner cost comparison data for Aseer Museum Subcontractor 01 (Replica Model Contractor). All paths are under:
`/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/`

## Canonical Project Structure

The main project path is the OneDrive-synced Aseer-Museum directory under `Samaya/Technical Office/Bim Unit/`.

```
Samaya/Technical Office/Bim Unit/
├── Aseer-Museum/                        # Main project folder
│   ├── Subcontractors/
│   │   ├── 01_Replica_Model_Contractor/
│   │   │   ├── 01_Schedule_and_BOQ/      # Cost comparisons often here too
│   │   │   ├── 09_Offers/                 # Vendor proposals
│   │   │   └── 10_Purchasing/
│   │   │       └── 3D Scanner/            # Scanner quotations + comparisons
│   │   │           ├── 3D_Scanner_Cost_Comparison.xlsx  # MAIN comparison sheet
│   │   │           ├── Artec/             # Artec-specific quotes
│   │   │           ├── *quotation*.pdf    # Vendor quotation PDFs
│   │   │           └── *Brochure*.pdf     # Product brochures
│   ├── Design Files/
│   ├── Docs/
│   ├── Invoices/Docs/Email Archive V8/    # Email archives (Arabic folder names)
│   └── Specs & Datasheet/
```

## File Search Strategy (for large OneDrive trees)

The top-level OneDrive root contains ~100+ folders and files. `search_files` (ripgrep) times out at 60s when searching `/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/` broadly.

**Better approach**: use `find` with `-maxdepth` and narrow paths:

```bash
# Quick directory discovery
find "/path/to/Aseer-Museum/" -maxdepth 4 -type d -iname "*scan*" 2>/dev/null

# Search within a known subdirectory only
find "/path/to/Aseer-Museum/" -maxdepth 6 -iname "*scanner*" 2>/dev/null

# Use mdfind (Spotlight) as fallback when OneDrive tree is too large
mdfind -name "scanner" -onlyin "/path/to/Aseer-Museum/" 2>/dev/null
```

## Identifying OneDrive Stub Files

Three distinct OneDrive sync states and how to detect them:

| State | Size | `file` output | `ls -laO` flags | Cause |
|-------|------|---------------|-----------------|-------|
| **Full sync** | Actual size | Actual type | `-rw-r--r--@` | File cached locally |
| **Dataless** | Actual size | Actual type | `compressed,dataless` | File listed but not downloaded |
| **Null stub** | 4 bytes | "ASCII text" | (none) | File cloud-only, never synced |

Detection:
```bash
# Find all 4-byte stubs
find /path -size 4c -exec sh -c 'test "$(cat "$1")" = "null" && echo "$1"' _ {} \;
```

## Extracting Excel Comparison Data (Multi-Sheet)

Comparison sheets typically have 3+ sheets (Summary, Quotes Detail, Contacts & Action):

```python
import openpyxl
wb = openpyxl.load_workbook("/path/to/comparison.xlsx")
for name in wb.sheetnames:
    ws = wb[name]
    print(f"=== Sheet: {name} ===")
    for row in ws.iter_rows(min_row=1, max_row=50, values_only=False):
        vals = [str(c.value) if c.value is not None else '' for c in row]
        print(' | '.join(vals))
```

Key things to watch for:
- **Formula cells** like `="SAR "&TEXT('Quotes Detail'!E10,"#,##0")` — openpyxl returns the formula string unless `data_only=True` is used, but formulas referencing other sheets may still not resolve unless the workbook was previously saved with values.
- **Hundreds separators** — `#,##0` format means prices have commas. Extract numeric values separately via regex if needed.
- **Multi-vendor layout** — each vendor has its own section in the Quotes Detail sheet with different currencies (SAR vs USD).

## Cross-Referencing Outlook Email DB

### Query by Subject

When quotation files are missing locally, find the source email:

```bash
sqlite3 ~/Library/Group\ Containers/UBF8T346G9.Office/Outlook/Outlook\ 15\ Profiles/Main\ Profile/Data/Outlook.sqlite \
  "SELECT Message_TimeSent, Message_NormalizedSubject \
   FROM Mail \
   WHERE Message_NormalizedSubject LIKE '%scanner%' \
      OR Message_NormalizedSubject LIKE '%3d scan%' \
   ORDER BY Message_TimeSent DESC LIMIT 10;"
```

The `Message_TimeSent` values are Unix timestamps with Mac's 978307200 epoch offset:
- Convert via: `datetime(Message_TimeSent + 978307200, 'unixepoch')`
- Attachment files may be in `Message Attachments/` subdirectory (numeric ID folders)

### Query by Sender Domain

To find emails from a specific company/domain (e.g. Faro distributor Arsad Al-Khalij):

```bash
sqlite3 ...Outlook.sqlite \
  "SELECT Message_TimeSent, Message_NormalizedSubject FROM Mail \
   WHERE Message_SenderAddressList LIKE '%arssad%' \
      OR Message_SenderAddressList LIKE '%sitml%' \
   ORDER BY Message_TimeSent DESC;"
```

### Query by Message Preview (body content)

When the subject doesn't contain the keyword but the email body does:

```bash
sqlite3 ...Outlook.sqlite \
  "SELECT Record_RecordID, Message_TimeSent, Message_NormalizedSubject \
   FROM Mail \
   WHERE Message_Preview LIKE '%Faro laser%' \
      OR Message_Preview LIKE '%terrestrial scan%';"
```

### Search Raw Message Source Files (deep body search)

When the `Message_Preview` field is truncated or doesn't contain the search phrase, grep the raw `.olk15MsgSource` files directly. These are stored in `/Message Sources/` as numeric subdirectories (RecordID / 1000 for the folder):

```bash
# Find all message sources containing a keyword
grep -rl "Faro\\|Blink\\|Focus Premium" ~/Library/Group\ Containers/UBF8T346G9.Office/Outlook/Outlook\ 15\ Profiles/Main\ Profile/Data/Message\ Sources/ 2>/dev/null

# Extract readable text from a specific source file
strings ~/.../Message\ Sources/81/51E5CF14-....olk15MsgSource | head -200

# Extract pricing or key info from a source file
strings ~/.../Message\ Sources/81/51E5CF14-....olk15MsgSource | grep -i "price\\|sar\\|usd\\|total\\|quote" | head -10
```

Caveats:
- `.olk15MsgSource` files are **binary containers** — use `strings` not `cat`
- The RecordID → folder mapping is: `folder = RecordID / 1000` (integer division)
- Not all records have corresponding source files; message types (meetings, etc.) may live elsewhere
- `strings` output includes MIME headers, base64 blobs, and routing metadata — filter with relevant keywords

### Combined Workflow for Missing Attachments

When a quotation file exists as a cloud stub (4 bytes, content="null") and no matching subject line found:

1. **Find the stub**: `find /path -size 4c -exec sh -c 'test "$(cat "$1")" = "null" && echo "$1"' _ {} \;`
2. **Extract likely filename keywords** from the stub filename (e.g. "Faro Blink", "Focus Premium")
3. **Query Outlook** for those keywords across subject, preview, and sender fields
4. **If still not found**, grep the raw message source files for the keyword
5. **Check meeting/calendar notes** — the Faro quotation was discovered via a Read.ai meeting report, not a direct email
6. **Fallback**: trigger OneDrive sync by opening the stub in Finder (`open /path/to/stub.pdf`)

## Known Vendor Quotation Locations (SC-01 Replica)

| Vendor | Product | Quotation File | Location |
|--------|---------|---------------|----------|
| MAPTEC (Riyadh) | Shining3D FreeScan COMBO+ | `Shining 3D FreeScan Combo + quotation (1).pdf` | 10_Purchasing/3D Scanner/ |
| GDS Middle East (Dammam) | Creaform Go!SCAN SPARK | `QT_Creaform Scanner.pdf` | 10_Purchasing/3D Scanner/ |
| 3D Middle East (Riyadh/Dubai) | Artec Space Spider II | `00556 SAMAYA Investment spider 2.pdf` | 10_Purchasing/3D Scanner/Artec/ |
| Faro Technologies | Faro Focus Premium 200m | `Revised_Quotation Faro Focus Premuim 200m.pdf` | OneDrive root (stub — not synced) |
| Faro Technologies | Faro Blink | `Quotation Faro Blink.pdf` | OneDrive root (stub — not synced) |
