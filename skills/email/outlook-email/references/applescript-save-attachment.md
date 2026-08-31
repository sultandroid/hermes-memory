# Saving an Outlook Attachment via AppleScript (working pattern)

**Referenced from:** `email/outlook-email` SKILL.md — "Direct Attachment Extraction" section.
**Prefer this over binary `.olk15MsgAttachment` parsing** when AppleScript is available — it's simpler and preserves the original filename/format.

## The working pattern

The reliable form is a **single `tell` block** with `POSIX file` for the destination path:

```applescript
osascript -e 'tell application "Microsoft Outlook"' \
  -e 'set m to message id 52279' \
  -e 'set att to first attachment of m' \
  -e 'set p to POSIX file "/tmp/ID_Report_Mansour.pdf"' \
  -e 'save att in p' \
  -e 'end tell'
```

## Pitfall — the string-path form fails with -2700

The naive one-liner that passes a **plain string path** to `save att in` throws:

```applescript
# FAILS: error -2700
osascript -e 'tell application "Microsoft Outlook" to set m to message id 52279' \
  -e 'tell application "Microsoft Outlook" to set att to first attachment of m' \
  -e 'tell application "Microsoft Outlook" to save att in "/tmp/ID_Report_Mansour.pdf"'
```

Two things break it:
1. **`save att in "<string>"`** — Outlook expects a file object, not a string. Wrap the path in `POSIX file`.
2. **Separate `tell application` blocks** — the `att` object reference does not survive across separate `tell` blocks. Keep the whole operation inside ONE `tell application "Microsoft Outlook" ... end tell`.

## Getting the attachment name first

To know what you're saving (and pick the right extension), read the attachment name before saving:

```applescript
osascript -e 'tell application "Microsoft Outlook" to set m to message id 52279' \
  -e 'tell application "Microsoft Outlook" to get name of every attachment of m'
# e.g. returns: ID Report.pdf
```

## Verify after save

```bash
ls -la /tmp/ID_Report_Mansour.pdf   # confirm non-zero size
pdftotext -layout /tmp/ID_Report_Mansour.pdf - | head   # confirm it's a real PDF
```

## When AppleScript is unavailable

Fall back to binary parsing of the `.olk15MsgAttachment` file — see `references/olk15-attachment-parsing.md` (base64 payload after the `base64\r\r` marker). Note the `-1741` permission error (Automation > allow Terminal to control Outlook) also blocks `save att in`.
