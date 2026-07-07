# Outlook Topic Search — Broad Keyword Matching Across Inbox

When you need to find emails about a specific **topic** (not just a known sender), you must scan the inbox with broad keyword matching. AppleScript is slow (~1-2 messages/second), so strategy matters.

## Direction (Verified May 29, 2026)

**`message 1 of inbox` = NEWEST (today). `message N` = oldest (Jul 2022).**

Always scan **forward** (1 → inboxCount) for newest-first. Verify at session start:
```applescript
osascript -e 'tell app "Microsoft Outlook" to get time received of message 1 of inbox'
```

## Keyword Strategy

AppleScript `contains` is **case-insensitive** for some terms but not all — match both cases explicitly:

```applescript
if subj contains "AV" or subj contains "av " or subj contains "audio" or subj contains "Audio" or ...
```

### Real Scan Parameters (AV Search, May 29)

| Parameter | Value | Reason |
|-----------|-------|--------|
| Scan depth | 1,500 messages | Covers ~120 days (13 msgs/day × 120 = 1,560) |
| Date cutoff | 120 days | AV project emails span 3-4 months |
| Keywords | ~50 terms | AV, audio, visual, projector, screen, speaker, sound, PA, cinema, media, display, monitor, OCULEAP, rack, amplifier, touch, LED, LCD, HDMI, lens + vendor names (Panasonic, Epson, Samsung, Yamaha, Q-Sys, BrightSign, etc.) |
| False positives | ~100/131 | Power Automate reminders contain "reminder" → no filter needed since they have "Something failed" text → manual ignore |
| Real AV emails found | 31 | From ~6 senders across ~90 days |
| Time to scan 1,500 | ~120-180s | AppleScript + Outlook COM overhead |

**Lesson:** Expect ~2:1 noise-to-signal ratio with broad keyword matching. The value is in **discovering senders and submittals you didn't know about** — the noise is worth filtering manually.

## Proven AppleScript Template

```applescript
-- Topic search with broad keyword matching
tell application "Microsoft Outlook"
    set inboxCount to count of messages of inbox
    set cutoffDate to (current date) - (120 * 24 * 60 * 60)  -- 120 days
    set resultsList to {}
    set scanned to 0
    set maxScan to 1500  -- ~2 min runtime
    
    -- SCAN FORWARD: msg 1 = newest
    repeat with i from 1 to inboxCount
        if scanned ≥ maxScan then exit repeat
        try
            set msg to message i of inbox
            set msgDt to time received of msg
            if msgDt ≥ cutoffDate then
                set subj to subject of msg
                set subjTxt to subj as string
                
                -- Broad keyword matching
                set topicFound to false
                set terms to {"Term1", "term2", "term3", ...}
                repeat with t in terms
                    if subjTxt contains t then
                        set topicFound to true
                        exit repeat
                    end if
                end repeat
                
                if topicFound then
                    -- Capture: index, internal message id, date, sender, attachments, subject
                    set msgId to id of msg
                    ...
                end if
                set scanned to scanned + 1
            end if
        end try
    end repeat
end tell
```

## Key: Internal Message ID vs Index

The `id of msg` (Outlook internal ID) is needed for `bim_download_attachment.applescript`. The sequential index (i) is used for iteration. Conversion:

```bash
osascript -e 'tell app "Microsoft Outlook" to get id of message INDEX of inbox'
# Returns: 34360 (internal ID for index 37 in this inbox on May 29)
```

## AV Search Results (May 29, 2026 — Reference Benchmark)

| Sender | AV Emails | Date Range | Key Docs |
|--------|-----------|------------|----------|
| Hesham Abdelhameed | 5 | 27 Apr–23 May | PQ-0056 (Panasonic), ZD-0038 (CCTV), IFC-0008 (AV IFC), AV Meeting |
| Mutti Ur Rehman | 5 | 30 Mar–12 May | AV Rack Room Location, AV Thermal Loads (power/BTU XLSX) |
| Mohamad Alzeeny | 2 | 1 Apr–12 May | Showcase Type 03 AV, AV Thermal Loads |
| Mohammed Hakami | 4 | 14–16 Apr | NRS AV Comments, PA Sound, AV IFC Package folder share |
| Talha Yousaf | 2 | 17 May | Flying Cinema Drawings |
| Soliman Obiya | 3 | 14–28 Apr | JOCAVI Acoustic Review, AV-related acoustics BOQ |
| Adel Darwish | 1 | 16 May | G6 Saudi Art Test Visual |
| Ahmed Salah | 2 | 1 Apr, 11 May | Showcase Type 03 AV, Updated Visuals |

## When to Use This Technique

- Finding all correspondence about a specific system (AV, acoustics, lighting, showcases)
- Tracing submittal history when a document code is unknown
- Discovering who is working on what topic
- Building a sender list for a topic you need to follow up on

**Don't use when:** You already know the sender and date range — use `outlook-search-by-sender.md` instead (much faster).
