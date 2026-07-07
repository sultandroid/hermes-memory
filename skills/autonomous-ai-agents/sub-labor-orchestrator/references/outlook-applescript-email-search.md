# Outlook AppleScript Email Search Patterns

Proven patterns for searching Microsoft Outlook inbox via AppleScript (macOS). Extracted from sessions with 18,000+ message inboxes at Samaya BIM Unit.

## Fundamentals

### Inbox Ordering (Confirmed May 2026)
- `message 1 of inbox` = **NEWEST** (today)
- `message N of inbox` = OLDEST (July 2022 in a 18,092-message inbox)
- Always scan **forward** (i=1 to N) for recent emails
- Exit when message date falls below cutoff

### Getting Outlook Internal IDs
The `bim_download_attachment.applescript` uses `message id <ID> of mail folder "Inbox"` — this requires the **Outlook internal message ID**, not the index position.

```
tell application "Microsoft Outlook"
    set msgId to id of message 37 of inbox
    -- returns "34360" (internal ID)
end tell
```

## Basic Search: By Sender

```applescript
-- Find emails from a specific sender in the last N days
tell application "Microsoft Outlook"
    set inboxCount to count of messages of inbox
    set cutoffDate to (current date) - (31 * 24 * 60 * 60)  -- ~31 days
    set resultsList to {}
    set scanLimit to 2000
    
    repeat with i from 1 to inboxCount
        if scanned ≥ scanLimit then exit repeat
        try
            set msg to message i of inbox
            set msgDt to time received of msg
            
            if msgDt ≥ cutoffDate then
                set snd to sender of msg
                try
                    set sndName to name of snd
                    set sndAddr to address of snd
                end try
                
                -- Match against sender name or email
                if sndName contains "Hesham" or sndAddr contains "hesham" then
                    set msgId to id of msg
                    -- collect results...
                end if
                set scanned to scanned + 1
            else
                exit repeat  -- past cutoff, stop
            end if
        end try
    end repeat
end tell
```

## Keyword Search: By Subject (Broad Match)

Use when the sender is unknown but you need to find emails by topic. **AppleScript `contains` is case-sensitive** — include both cases.

```applescript
-- Check subject for AV-related keywords
set subjText to ((subject of msg) as string)
set isAV to false

-- List of case-sensitive keywords to check
if subjText contains "AV" or subjText contains "av " or ¬
   subjText contains "audio" or subjText contains "Audio" or ¬
   subjText contains "visual" or subjText contains "Visual" or ¬
   subjText contains "projector" or subjText contains "Projector" or ¬
   subjText contains "screen" or subjText contains "Screen" or ¬
   subjText contains "speaker" or subjText contains "Speaker" or ¬
   subjText contains "sound" or subjText contains "Sound" or ¬
   subjText contains "display" or subjText contains "Display" or ¬
   subjText contains "monitor" or subjText contains "Monitor" or ¬
   subjText contains "OCULEAP" or subjText contains "cinema" or ¬
   subjText contains "technology" or subjText contains "Technology" or ¬
   subjText contains "rack" or subjText contains "Rack" or ¬
   subjText contains "amplifier" or subjText contains "Amplifier" or ¬
   subjText contains "lens" or subjText contains "Lens" or ¬
   subjText contains "HDMI" or subjText contains "LED" or ¬
   subjText contains "Panasonic" or subjText contains "Epson" or ¬
   subjText contains "Samsung" or subjText contains "Yamaha" or ¬
   subjText contains "Q-Sys" or subjText contains "BrightSign" or ¬
   subjText contains "multimedia" or subjText contains "Multimedia" then
    set isAV to true
end if
```

## Performance Characteristics

| Scan Size | Messages | Time | Notes |
|-----------|----------|------|-------|
| 100 newest | 100 | ~5s | Good for "recent emails from X" |
| 500 | 500 | ~30s | Covers ~3-4 weeks |
| 1,500 | 1,500 | ~120-180s | Covers ~4 months; may timeout |
| 3,000 | 3,000 | >300s | Likely to timeout; avoid |

**Limitations:**
- 180-second timeout is common for scans over 1,500 messages
- Use `background=true` + `notify_on_complete=true` for long scans
- Or split into batches: 500 at a time with progress tracking

## Noise Filtering

When scanning for project emails, filter out known noise senders:
- `Microsoft Power Automate` — "Sending reminder: Something failed"
- `3DXTECH` — filament/promotional emails
- `ClickUp Team` — tool consolidation promos
- `Read Support` — report reminders
- `FJDynamics` / `FJD Trion` — scanner firmware updates
- `SharePoint Online` — anonymous access link notifications (unless relevant)

## Complete Download Pattern

To download attachments from a found email:

1. Get the Outlook internal ID: `id of message <INDEX> of inbox`
2. Use the existing `bim_download_attachment.applescript`:
   ```
   osascript ~/.hermes/scripts/bim_download_attachment.applescript "Inbox" "<MSG_ID>" "<ATT_NAME>" "/tmp/path/"
   ```
3. Or download directly in AppleScript:
   ```
   save att in POSIX file "/tmp/path/file.pdf"
   ```

## Known Issues

- `date received of msg` → **DOES NOT WORK** — use `time received of msg` instead
- `address of sender of msg` → **DOES NOT WORK** — use `snd = sender of msg` then `address of snd`
- Variable names `count`, `result` conflict with AppleScript keywords — rename to `cnt`, `outMsg`
- `osacompile` may report false errors for `(current date) - (31 * days)` — use `(31 * 24 * 60 * 60)` (seconds) instead, which works at runtime
- SMTP/Exchange connection latency adds ~50-100ms per message iteration
