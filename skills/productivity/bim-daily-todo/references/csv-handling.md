# Aseer CSV Handling Reference

## File Location

```
/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/Docs/Email Archive/مشروع متحف عسير الإقليمي/Register_ASEER_Professional.csv
```

## CSV Quirks

### Issue: `read_file` Adds Line Number Prefixes

`read_file()` returns content with `N|` prefixes on each line:
```
     1|Date,Ref,Category,From,To,Subject,Action,Remarks,Status
     2|2026-05-25,ASE-EMAIL-34352,RFP,...
```

This **breaks `csv.DictReader`** because the first field becomes `1|Date` instead of `Date`.

**Workaround**: Use `terminal("cat <path>")` piped to `io.StringIO`:

```python
from hermes_tools import terminal
import csv, io

result = terminal('cat "/path/to/file.csv"')
csv_text = result["output"]
reader = csv.DictReader(io.StringIO(csv_text))
entries = list(reader)  # clean parse, correct headers
```

### Issue: DOS `\r\n` Line Endings

The Aseer CSV uses Windows-style `\r\n` line endings. Without stripping `\r`, the last field of every row gets a trailing `\r` — e.g. `Active\r` instead of `Active`. This silently breaks `status == 'Active'` comparisons.

**Fix:** Strip `\r` before parsing:

```python
with open(path, 'r') as f:
    raw = f.read().replace('\r\n', '\n')
reader = csv.DictReader(io.StringIO(raw))
```

### Issue: Embedded Commas in Quoted Fields

The `Remarks` field contains free-text with commas, enclosed in double quotes:
```
Reviewed / Reply Sent,"Glad to have our meeting today, and it will be my pleasure...",Active
```

`csv.DictReader` handles this correctly — just use it with `io.StringIO`.

## Fields

| Field | Type | Example |
|-------|------|---------|
| Date | YYYY-MM-DD | `2026-05-25` |
| Ref | String | `ASE-EMAIL-34352` or numeric `29398` (Open entries) |
| Category | Code | `RFP`, `SDR`, `SI`, `IR`, `GEN`, `DOC`, `SCH` |
| From | Email | `omar.bittar@3d-me.com` |
| To | Email(s) | Semicolon-separated list |
| Subject | String | Email subject or task title |
| Action | String | `Reviewed / Reply Sent`, `Review`, `Process Payment` |
| Remarks | String | Arabic or English notes — may contain commas |
| Status | Enum | `Active`, `Archived`, `Open` |

## Open vs Active Status

| Status | Meaning | Ref Format | Action Field |
|--------|---------|------------|--------------|
| `Active` | Email entry needing attention | `ASE-EMAIL-NNNNN` | Past tense (`Reviewed / Reply Sent`) |
| `Open` | NRS new/untouched entry | Numeric (`29398`) | Imperative (`Review`, `Process Payment`) |
| `Archived` | Done — file record only | Empty or Ref | `Document / File record` |

Both `Active` and `Open` are actionable. Never exclude `Open`.

## Entry Counts (Typical)

- Total rows: ~284 (growing)
- Active entries in last 7 days: 9–12
- Open entries: 3 (very recent, may change)
- Archived file-records: bulk of the file (older items)
