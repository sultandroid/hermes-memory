# Locating & Extracting a Specific Outlook Attachment by Content (no AppleScript save)

When AppleScript `save att in` fails (error -2700, common on Outlook 16.90+ and for
multi-part/PDF attachments), the `.olk15MsgAttachment` file sits under a **random GUID
filename** in `Message Attachments/` — you cannot guess the path from the email. You locate
it by **content**, then base64-decode directly.

## Why this is needed

- The `Mail_OwnedBlocks`→`Blocks` join gives a path, but the GUID filename does NOT match
  anything in the message file, and `grep -rl` across the whole `Message Attachments/` tree is
  impractically slow.
- The GUID embedded in the `.olk15Message` (`com.adobe.pdfapplication/pdff_<GUID>`) is NOT the
  same as the `.olk15MsgAttachment` filename — do not waste time matching it.

## Worked pattern (used successfully to get the real TLC Rev.2 offer PDF)

### Step 1 — locate the target by a unique reference string, restricted to recent attachments

```bash
BASE=~/Library/Group\ Containers/UBF8T346G9.Office/Outlook/Outlook\ 15\ Profiles/Main\ Profile/Data
find "$BASE/Message Attachments" -type f -newermt "2026-08-09" 2>/dev/null | while read f; do
  if head -c 2000 "$f" 2>/dev/null | grep -qE "3304-001|TLC_Offer|Design_TLC"; then
    echo "HIT: $f ($(stat -f%z "$f") bytes)"
  fi
done
```

Use a **short, unique string from the attachment filename** (doc ref like `3304`, or a
substring of the filename). `-newermt` bounds the scan so it completes fast. Multiple hits =
multiple copies; pick any.

2. **Identify the real filename** from the header (`.olk15MsgAttachment` begins with MIME
   headers that contain `Content-type: application/pdf; name="<real name>";`):

```bash
head -c 1500 "$F" | strings | grep -iE "name=|content-type|filename"
```

3. **Base64-decode by the `JVBERi0` marker** (base64 of `%PDF-`), not by the
   `Content-transfer-encoding` offset. The binary header + headers mean the PDF body may start
   mid-file; `JVBERi0` is unambiguous:

```python
import os, re, base64
raw = open(f, 'rb').read()
i = raw.find(b'JVBERi0')                    # 'JVBERi0' == base64('%PDF-')
b64 = re.sub(rb'[^A-Za-z0-9+/=]', b'', raw[i:])   # strip \r\n / stray chars
data = base64.b64decode(b64)
open('/tmp/out.pdf', 'wb').write(data)      # starts with b'%PDF-'
```

3. **Read it** — a scanned/image offer yields empty `pdftotext`; render pages to images and
   OCR / vision-read:
```bash
pdfinfo /tmp/out.pdf | grep -i pages          # page count
pdftoppm -f N -l N -r 150 -jpeg /tmp/out.pdf /tmp/pg
tesseract /tmp/pg-N.jpg - 2>/dev/null
```

## When to prefer this over AppleScript
- `save` returns -2700 for that attachment (esp. large/multi-part PDFs).
- The email came from a sender whose attachments repeatedly fail extraction.
- You only need ONE specific document and want to skip the per-message AppleScript loop.

## IMPORTANT — try the correct AppleScript form FIRST (2026-08-31)
A `-2700` error is often NOT a real Outlook limitation — it is a **syntax bug** in the
AppleScript. The naive form (string path + separate `tell` blocks) fails with -2700, but the
**single-`tell` + `POSIX file`** form works reliably:

```applescript
osascript -e 'tell application "Microsoft Outlook"' \
  -e 'set m to message id 52279' \
  -e 'set att to first attachment of m' \
  -e 'set p to POSIX file "/tmp/out.pdf"' \
  -e 'save att in p' \
  -e 'end tell'
```

Two fixes: (1) wrap the destination in `POSIX file` (not a bare string), and (2) keep the
whole operation inside ONE `tell application "Microsoft Outlook" ... end tell` — the `att`
object reference does not survive across separate `tell` blocks. Read the attachment name
first (`get name of every attachment of m`) to pick the right extension. Only fall back to
binary parsing if this correct form still errors. See `references/applescript-save-attachment.md`.
