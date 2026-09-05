# Reading the FULL email body / metadata (beyond SQLite preview)

`Message_Preview` in the `Mail` table only stores the first ~250 chars. There is NO `Body` column. The full body lives in a proprietary binary blob (`PathToDataFile` → `.olk15Message`), which is not text-extractable.

## Reliable way — AppleScript `content`

Returns the full HTML body:

```bash
osascript -e 'tell application "Microsoft Outlook"' \
  -e 'set m to message id <Record_RecordID>' \
  -e 'set s to content of m' \
  -e 'return s' -e 'end tell'
```

Pipe through `python3 -c "import sys; print(sys.stdin.read())"` if you need the rendered text among the HTML markup. If the output is Word-style HTML, the message text lives inside `<div class="WordSection1">` — scrape from there.

## Metadata beyond preview (already in the Mail table — no body needed)

- `Message_DisplayTo` — plain-To recipients
- `Message_CCRecipientAddressList` — CC recipients
- `Message_SenderList` / `Message_SenderAddressList` — sender

Use these to tell WHOM an email is addressed (e.g. "is this for me or am I just on CC?") without extracting the body. `PathToDataFile` → `Messages/<NN>/<GUID>.olk15Message` under the Outlook Data folder — confirms presence but is not readable text.

## Decision aid

For action-item emails addressed to someone else with you on CC: check `Message_DisplayTo` before assuming the action is yours. When the user asks to open an email "for discussion" and the recipient is a third party (e.g. a PM addressing Adel, user on CC), say so explicitly and identify the real decision-owner up front.
