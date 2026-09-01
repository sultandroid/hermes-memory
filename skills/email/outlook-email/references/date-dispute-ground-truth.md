# Resolving date/timeline disputes from the Outlook SQLite DB (ground truth)

When a consultant/vendor disputes a project date (kick-off, contract award, submission
deadline) in an email thread, do NOT take either side's word — establish ground truth
from the Outlook SQLite DB before drafting a reply. The DB is authoritative for what
was actually sent/received and when.

## Workflow

1. Find the disputed event's emails by sender + subject keyword:
   ```bash
   DB="$HOME/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite"
   sqlite3 -separator ' ||| ' "$DB" \
     "SELECT Record_RecordID, datetime(Message_TimeReceived,'unixepoch','localtime'), Message_SenderList, Message_NormalizedSubject \
      FROM Mail WHERE (Message_SenderAddressList LIKE '%<domain>%' OR Message_SenderList LIKE '%<name>%') \
      AND Message_NormalizedSubject LIKE '%<keyword>%' ORDER BY Message_TimeReceived;"
   ```
2. For the earliest relevant email, pull the full body via AppleScript to read the
   actual wording (e.g. "officially proceed to the next stage" = kick-off date):
   ```bash
   osascript -e 'tell application "Microsoft Outlook"
   set m to message id <RecordID>
   set c to content of m
   return c
   end tell' > /tmp/msg.html
   # then strip HTML:
   # python3 -c "import re,html; t=open('/tmp/msg.html').read(); t=re.sub(r'<style.*?</style>','',t,flags=re.S); t=re.sub(r'<head.*?</head>','',t,flags=re.S); t=re.sub(r'<br[^>]*>','\n',t); t=re.sub(r'</p>','\n',t); t=re.sub(r'<[^>]+>','',t); t=html.unescape(t); print(t.strip())"
   ```
3. Cross-check the timeline: earliest email from the party, contract-signing emails,
   and the disputed milestone. The party's own negotiation emails often show THEY
   delayed signing (e.g. rejecting amendments), which shifts blame for a late start.

## Pitfalls

- **Don't assert dates you didn't verify.** If you relay a date from the user's own
  email back to them as fact, and the counterparty then disputes it, the user will
  (rightly) push back. Always trace the date to a source record (an email in the DB,
  a contract file) before stating it as ground truth. When the user says "you gave me
  that date," check whether it came from their own prior email — acknowledge the
  source honestly, then verify against the DB rather than arguing.
- **OneDrive docx/PDF may be EDEADLK-locked.** Contract files under
  `~/Library/CloudStorage/...` often fail to open (Errno 11). The Outlook SQLite DB
  is usually the more reliable source for dates than the locked contract files.
  Prefer the DB; fall back to `pdftotext`/OCR only if the file materializes.

## Worked example (Aseer Museum / AD Engineering, Sep 2026)

AD Engineering disputed Samaya's kick-off date (25 Jun 2026) claiming it was 21 Jul
and that the contract only finalized 17 Aug. Ground truth from the DB:

| Date | Event | Evidence |
|------|-------|----------|
| 25 Jun 2026 | Samaya kick-off email to AD | "Kick-off & Next Stage Approval - MEP Design Services" — "officially proceed to the next stage" |
| 1 Jul | AD sends draft electrical SOW | |
| 13 Jul | First mechanical submissions | |
| 20 Jul | AD rejects contract amendments | "unable to accept the proposed amendments" |
| 6–9 Aug | Contract signed | AD signed/stamped 9 Aug |
| 17 Aug | Samaya sends final signed contract | |

Conclusion: Samaya mobilized AD on 25 Jun; the late contract signing was due to AD's
own negotiation delays (rejecting amendments on 20 Jul), not Samaya. AD was shifting
the start date to shrink its responsibility window.
