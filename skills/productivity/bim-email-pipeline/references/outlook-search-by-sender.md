# Outlook Search by Sender (AppleScript)

Pattern for searching Outlook inbox for emails from a specific sender within a date range. Developed May 29, 2026 while searching for Hesham Abdelhameed's emails.

## Key Discovery: Inbox Direction

**Outlook inbox is NOT consistently ordered.** On Mohamed's machine (verified May 29):
- `message 1` = **newest** (today)
- `message N` = **oldest** (Jul 2022)

This can vary by Outlook version, sort setting, or folder. **Always verify first:**

```bash
osascript -e 'tell app "Microsoft Outlook" to get time received of message 1 of inbox'
osascript -e 'tell app "Microsoft Outlook" to get time received of message (count of messages of inbox) of inbox'
```

## Generic Sender Search Template

```applescript
-- Search Outlook inbox for emails from a specific sender in a date range
tell application "Microsoft Outlook"
    set inboxCount to count of messages of inbox
    set cutoffDate to (current date) - (31 * days)  -- ~1 month
    set targetSender to "Hesham"  -- partial name or email to match
    set resultsList to {}
    set scanLimit to 2000
    set scanned to 0

    -- Scan forward from msg 1 (newest) if msg 1 = today
    repeat with i from 1 to inboxCount
        if scanned ≥ scanLimit then exit repeat
        try
            set msg to message i of inbox
            set msgDt to time received of msg

            if msgDt ≥ cutoffDate then
                set msgSubject to subject of msg
                set snd to sender of msg
                try
                    set sndName to name of snd
                on error
                    set sndName to ""
                end try
                try
                    set sndAddr to address of snd
                on error
                    set sndAddr to ""
                end try

                -- Match sender name or address (case-insensitive)
                if sndName contains targetSender or sndAddr contains targetSender then
                    set end of resultsList to "ID:" & i & "|DATE:" & (short date string of msgDt) & "|FROM:" & sndName & "|ADDR:" & sndAddr & "|SUBJ:" & msgSubject
                end if
                set scanned to scanned + 1
            else
                exit repeat
            end if
        on error errMsg
            -- skip problematic messages
        end try
    end repeat

    set output to "SCANNED:" & scanned & "|FOUND:" & (count of resultsList) & "|"
    repeat with e in resultsList
        set output to output & "|EMAIL|" & e
    end repeat
    return output
end tell
```

## Getting Outlook Internal Message IDs (For Attachment Download)

The `bim_download_attachment.applescript` requires the **Outlook internal message ID**, not the sequential index.

To get the internal ID from an index:
```bash
osascript -e 'tell app "Microsoft Outlook" to get id of message INDEX of inbox'
```

Example (verified May 29, 2026):
- Index 37 → internal ID 34360
- Index 54 → internal ID 34377
- Index 87 → internal ID 34410

Use this mapping when you need to download attachments from specific messages.

## Batch Download Pattern

For downloading multiple attachments from multiple emails, write one AppleScript with multiple `message id` blocks:

```applescript
tell application "Microsoft Outlook"
    set dlDir to "/tmp/aseer_attachments/"
    
    -- Message ID 34377 (index 54) - 7 attachments
    set f to mail folder "Inbox"
    set m to message id 34377 of f
    repeat with a in every attachment of m
        save a in POSIX file (dlDir & name of a)
    end repeat
    
    -- Message ID 34410 (index 87) - 5 attachments
    set m2 to message id 34410 of f
    repeat with a in every attachment of m2
        save a in POSIX file (dlDir & name of a)
    end repeat
end tell
```

**Note:** `save a in POSIX file "/path/to/file.pdf"` works reliably. The output path MUST be outside any OneDrive mount to avoid "Resource deadlock avoided" errors. Always save to `/tmp/` first, then copy to the OneDrive destination.

## Date Arithmetic: `days` vs Seconds

```applescript
-- WORKS at runtime (osascript), FAILS at compile time (osacompile) inside `tell app` blocks:
set cutoffDate to (current date) - (31 * days)

-- WORKS everywhere — use seconds instead:
set cutoffDate to (current date) - (31 * 24 * 60 * 60)
```

The `days` keyword is a reserved class name in AppleScript. Inside a `tell application` block, `osacompile` may reject it with "Expected ',' but found class name". Using explicit seconds (`24 * 60 * 60`) avoids this and is portable across both `osascript` and `osacompile`.

## Notes

- `time received of msg` ✓ — works reliably
- `date received of msg` ✗ — returns error
- Sender properties: `name of sender` for display name, `address of sender` for email
- Both can fail on some messages — wrap in try/on error blocks
- The `subject of msg` may contain Arabic text — AppleScript handles it fine
- For large inboxes (18K+), cap scan with `scanLimit` and use `exit repeat` on date cutoff
- Always use `(current date) - (N * days)` for relative dates — AppleScript's absolute date parsing is finicky
