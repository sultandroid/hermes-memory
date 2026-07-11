# Sender Blank via `osascript -e` One-Liners

## Problem

When using the bash loop pattern to scan Outlook messages:

```bash
snd=$(osascript -e "tell application \"Microsoft Outlook\" to set sr to sender of message $i of mail folder id 114; return name of sr" 2>/dev/null)
```

`snd` is always empty string, even though the message exists and has a valid sender. The `sender` property's Mail Recipient record doesn't serialize to text in one-liner mode.

## Root Cause

`osascript -e` serializes AppleScript records differently than file-based `osascript`. The `sender` property returns a `Mail Recipient` object (a record, not a string). In one-liner mode, the record serialization fails silently — the `name` property of the recipient is never extracted.

## Workaround

Use a short `.applescript` file on disk for sender extraction:

```bash
# Write this to /tmp/get_senders.applescript:
# tell application "Microsoft Outlook"
#     set sr to sender of message 1 of mail folder id 114
#     return (name of sr) as text & "|" & (address of sr) as text
# end tell

osascript /tmp/get_senders.applescript
# Returns: "Jim Richards|jim.r@nissenrichardsstudio.com"
```

## Two-Phase Pattern (Recommended)

Phase 1: Get subjects + times via fast bash loop (one-liners work for these):
```bash
for i in $(seq 1 30); do
  subj=$(osascript -e "tell application \"Microsoft Outlook\" to get subject of message $i of mail folder id 114" 2>/dev/null)
  tme=$(osascript -e "tell application \"Microsoft Outlook\" to get time received of message $i of mail folder id 114" 2>/dev/null)
  echo "$i|$tme|$subj"
done
```

Phase 2: Get senders for the same range via a single file-based script:
```applescript
tell application "Microsoft Outlook"
    set ids to {1, 2, 3, ..., 30}
    set out to {}
    repeat with i in ids
        set iv to (i as integer)
        set snd to ""
        set sadr to ""
        try
            set sr to sender of message iv of mail folder id 114
            set snd to (name of sr) as text
            set sadr to (address of sr) as text
        end try
        set end of out to (iv as text) & "|" & snd & "|" & sadr
    end repeat
    return out
end tell
```

## Affected Properties

This blank-serialization issue affects:
- `sender` (Mail Recipient record) — **always blank** in one-liner mode
- `has attachment` (boolean) — **always blank** in one-liner mode
- `read status` — unreliable in all modes

Properties that DO work in one-liner mode:
- `subject` — returns text
- `time received` — returns formatted date string
- `id` — returns integer
- `unread count of inbox` — returns integer (folder-level only)
