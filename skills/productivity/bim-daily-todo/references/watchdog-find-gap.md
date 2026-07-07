# Watchdog + find Gap (June 2026)

## Finding: `find -newermt` discovers files that watchdog_state.json misses

On Jun 12, 2026, the watchdog returned only **5 Zamzam files** in the 7-day window. A concurrent `find -newermt` scan of the same directory tree returned **additional files** not present in the watchdog index:

| File | Watchdog says | Find says | 
|------|--------------|-----------|
| Zamzam BOQ xlsx files | ❌ missing | ✅ Jun 9-12 |
| Quotation NO.3451 PDF | ❌ missing | ✅ Jun 8-12 |
| WhatsApp screenshots | ❌ missing | ✅ Jun 8 |

The watchdog is updated daily (Jun 12 04:19 timestamp) but appears to have coverage gaps for certain Zamzam subdirectories (B.O.Q/, Docs/From_Root/, Docs/03_Inspection_Requests/).

## Recommendation

Always supplement the watchdog query with a `find -newermt` scan:

```bash
# For Zamzam
find '/OneDrive/.../Zamzam Museum' -type f -newermt '7 days ago' 2>&1 | \
  grep -v '.DS_Store' | grep -iv 'backup\|\.dat\|temp' | head -40

# For Aseer
find '/OneDrive/.../Aseer-Museum' -type f -newermt '7 days ago' 2>&1 | \
  grep -v '.DS_Store' | grep -iv 'backup\|\.dat\|temp' | head -40
```

The `find` scan works on OneDrive stubs (metadata-only). Cross-reference results against the watchdog to catch files the index missed.

## Root Cause (Speculative)

The watchdog likely indexes files during a scheduled scan, but certain subdirectory trees may be excluded or not fully traversed if the scan encounters locked/dataless stub directories. The `find` command uses fresh filesystem metadata every time and is not subject to indexing-age gaps.

## Impact

Without the find fallback, this session would have missed:
- **1 HIGH-priority item**: Zamzam Quotation NO.3451 (RFP — decision required)
- **1 LOW-priority item**: Zamzam BOQ updates
