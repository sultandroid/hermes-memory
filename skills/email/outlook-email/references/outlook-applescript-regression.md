# Outlook 16.90+ AppleScript Property Access Regression

## The Bug

On Outlook 16.90+ (macOS), direct property access on `message id N` objects fails:

```applescript
set m to message id 49107
set msub to subject of m
-- ERROR: Can't make |subject| of incoming message id 49107 into type specifier (-1700)
```

This affects ALL property reads: `subject`, `time received`, `has attachment`, `sender`, `content`, `plain text content`. The error is NOT a syntax issue — the same syntax works on older Outlook versions.

## Root Cause

The `message id N` accessor returns an object whose property-access path is broken in the 16.90+ AppleScript dictionary. The object exists (you can read `id of m`), but you cannot read any other property through it.

## Reliable Workaround

Use `item N of (every message of mail folder id <FOLDER_ID>)` instead:

```applescript
-- WORKS on all versions:
set msgs to (every message of mail folder id 114)  -- 114 = Inbox
set m to item 1 of msgs
set msub to subject of m  -- OK
set mtime to time received of m  -- OK
set matt to has attachment of m  -- OK
```

## Scanning Recent Inbox Messages (Proven Pattern)

```applescript
tell application "Microsoft Outlook"
    set msgs to (every message of mail folder id 114)
    set out to ""
    repeat with m in msgs
        set out to out & (id of m) & "|" & (subject of m) & "|" & (time received of m) & "|" & (has attachment of m) & linefeed
        if (count of paragraphs of out) > 10 then exit repeat
    end repeat
    return out
end tell
```

## Python Generator for Individual Scripts (Alternative)

When the loop approach hits the ~700-byte AppleScript body limit, generate individual scripts per message index:

```python
import subprocess, os

outdir = "/tmp/inbox_scan"
os.makedirs(outdir, exist_ok=True)

for i in range(1, 11):
    path = outdir + "/m" + str(i) + ".applescript"
    with open(path, "w") as f:
        f.write('tell application "Microsoft Outlook"\n')
        f.write('set msgs to (every message of mail folder id 114)\n')
        f.write('set m to item ' + str(i) + ' of msgs\n')
        f.write('return (id of m) & "|" & (subject of m) & "|" & (time received of m) & "|" & (has attachment of m)\n')
        f.write('end tell\n')
```

Then run: `osascript /tmp/inbox_scan/m1.applescript`

## Key Discovery Method

To find the Inbox folder ID:
```applescript
osascript -e 'tell application "Microsoft Outlook" to return id of inbox'
# Returns: 114
```

## What NOT to Do

- Do NOT retry `message id N` with different syntax — it's a runtime regression, not a syntax issue
- Do NOT use `properties of m` — this also fails with `Can't get every property` (-1728)
- Do NOT use `osascript -e` one-liners with `message id N` — they hit the same regression
- Do NOT try to close/reopen Outlook — the regression persists across restarts
