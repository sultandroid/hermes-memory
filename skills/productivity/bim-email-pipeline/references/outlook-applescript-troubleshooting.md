# Outlook AppleScript Troubleshooting — May 2026 Findings

## ⚠️ CRITICAL: Inbox Message Order (Discovered May 29, 2026)

**message 1 = NEWEST (today). message N = OLDEST (Jul 2022).**

This is the OPPOSITE of what earlier documentation stated. Verified with:
```bash
osascript -e 'tell application "Microsoft Outlook" to get time received of message 1 of inbox'
# → "Friday, 29 May 2026 at 3:03:38 PM" (today, newest)

osascript -e 'tell app "Microsoft Outlook" to get time received of message (count of messages of inbox) of inbox'
# → "Wednesday, 20 July 2022 at 10:17:38 AM" (oldest)
```

**Correct scan pattern — forward scan only:**
```applescript
repeat with i from 1 to inboxCount
    set msg to message i of inbox
    set msgDt to time received of msg
    if msgDt >= cutoffDate then
        -- process
        set scanned to scanned + 1
    else
        exit repeat  -- all remaining messages are older
    end if
end repeat
```

## Verified Properties

| Expression | Status | Error when wrong |
|---|---|---|
| `time received of msg` | ✅ Works | — |
| `date received of msg` | ❌ Fails | "variable received is not defined" |
| `address of sender of msg` | ❌ Fails | "Can't make into type specifier" |
| `snd = sender of msg` then `address of snd` | ✅ Works | — |
| `message i of inbox` | ✅ Works | — |
| `incoming message` class | ❌ Fails | "Expected class name" |

## AppleScript Reserved Words That Break as Variable Names

| Word | Symptom | Fix |
|------|---------|-----|
| `count` | "Can't set checked to 0" | Use `cnt` or `scanCount` |
| `result` | "The variable result is not defined" | Use `outMsg` or `resultsList` |
| `outLine` (contains `line`) | "Can't set outline to ... Access not allowed" | Use `outRow` or `resultLine` |

Safe naming pattern: prefix with `out` and avoid property keywords. E.g.: `outMsg`, `outTxt`, `resultsList`, `scanCount`, `emailMap`.

## `days` Keyword Compile Error

`(current date) - (31 * days)` compiles fine outside a `tell` block, but `osacompile` rejects it inside `tell application "Microsoft Outlook"`:
```
Expected ',' but found class name. (-2741)
```
**Fix:** use seconds: `31 * 24 * 60 * 60`. Works in both osacompile and osascript.

## Fast Diagnostic Commands

```bash
# Verify direction at session start (MANDATORY)
osascript -e 'tell app "Microsoft Outlook" to get time received of message 1 of inbox'
osascript -e 'tell app "Microsoft Outlook" to get time received of message (count of messages of inbox) of inbox'

# Inbox count
osascript -e 'tell app "Microsoft Outlook" to get count of messages of inbox'

# Get Outlook internal message ID from index
osascript -e 'tell app "Microsoft Outlook" to get id of message 37 of inbox'
```

## Confirmed Working Template (Newest-First, Forward Scan)

Tested May 29, 2026:

```applescript
tell application "Microsoft Outlook"
    set inboxCount to count of messages of inbox
    set cutoffDate to (current date) - (31 * 24 * 60 * 60)
    set resultsList to {}
    set scanLimit to 2000
    set scanned to 0

    repeat with i from 1 to inboxCount
        if scanned >= scanLimit then exit repeat
        try
            set msg to message i of inbox
            set msgDt to time received of msg
            if msgDt >= cutoffDate then
                set msgSubject to subject of msg
                set snd to sender of msg
                set sndName to name of snd
                set sndAddr to address of snd
                set end of resultsList to "i:" & i & "|d:" & (short date string of msgDt) & "|f:" & sndName & "|s:" & msgSubject
                set scanned to scanned + 1
            else
                exit repeat
            end if
        end try
    end repeat

    set outMsg to "scanned:" & scanned & "|found:" & (count of resultsList)
    repeat with e in resultsList
        set outMsg to outMsg & "||" & e
    end repeat
    return outMsg
end tell
```
