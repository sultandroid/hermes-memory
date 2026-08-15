# Email Intel — Outlook SQLite Backfill (beyond the scan-report window)

The `email_intel_backfill.py` importer only reads `email_scan_*.md` reports, which
start mid-July. To backfill the Email Intel inbox further back (e.g. to April),
pull project-relevant emails directly from the Outlook SQLite DB.

## When to use
- User asks to backfill the Email Intel system to a date before the first
  `email_scan_*.md` report exists.
- The inbox is missing historical project emails that live in Outlook.

## DB
`~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite`

## Recipe

1. **Verify epoch** (mandatory — see main SKILL.md Step 0). This DB uses Unix epoch:
   ```sql
   SELECT Message_TimeReceived, datetime(Message_TimeReceived,'unixepoch','localtime')
   FROM Mail ORDER BY Message_TimeReceived DESC LIMIT 1;
   ```
   Junk rows with `2001-01-01` timestamps exist (near-zero epoch) — ignore them.

2. **Quantify the window** before writing anything:
   ```sql
   SELECT strftime('%Y-%m', datetime(Message_TimeReceived,'unixepoch','localtime')) mon, count(*)
   FROM Mail
   WHERE Message_TimeReceived >= strftime('%s','2026-04-01','localtime')
     AND Message_TimeReceived < strftime('%s','2026-07-15','localtime')
     AND (Message_NormalizedSubject LIKE '%Aseer%' OR ... OR Message_SenderList LIKE '%cg.com.sa%')
   GROUP BY mon ORDER BY mon;
   ```

3. **Run the importer** (in `~/hermes-memory/scripts/email_intel_outlook_backfill.py`):
   ```bash
   python3 scripts/email_intel_outlook_backfill.py --from 2026-04-01 --to 2026-07-15 --dry-run
   python3 scripts/email_intel_outlook_backfill.py --from 2026-04-01 --to 2026-07-15
   ```
   It filters by project-relevant subject/sender patterns, skips known
   non-project senders (ERP, SharePoint, Power Automate, marketing), routes via
   `projects.json`, and writes `{date}-{sender}-{subject}.md` into `inbox/`.

4. **Run the agent pipeline** to process the expanded inbox:
   ```bash
   python3 scripts/email_intel_agent.py --run
   ```

5. **Commit + push** the hub repo (`hermes-memory`).

## Pitfalls
- **The issue detector over-raises.** After a large backfill the issue count
  explodes (306 of 318 were "reply-required" keyword hits). These are raw flags,
  not verified action items — triage against project registers before reporting.
- **Dedup is by exact filename.** The importer skips files that already exist.
  If a prior buggy run stamped wrong dates, you get near-duplicates with
  different date prefixes. Clean by matching `(source, subject-slug)` and keeping
  the correctly-dated file.
- **Backfill date bug (fixed):** the original `email_intel_backfill.py` stamped
  `datetime.now()` instead of the scan file's date, misdating every email. The
  fix reads the date from the `email_scan_YYYY-MM-DD.md` filename. If you see a
  whole batch of inbox files sharing one date, suspect this.
- **Issue `email_ref` bug (fixed):** the agent wrote `inbox/{subject}.md` but real
  files are `{date}-{sender}-{subject}.md`, so refs were broken. The fix matches
  the subject slug against actual inbox filenames. Verify with:
  ```python
  import glob,os,re
  for f in glob.glob('email_intel/issues/*.md'):
      ref=re.search(r'email_ref:\s*(\S+)',open(f).read()).group(1)
      if not os.path.exists('email_intel/'+ref): print('BROKEN',f,ref)
  ```
- **Scripts get deleted by auto-sync.** The `hermes-memory` auto-sync cron
  (`memory_skills_exchange.sh`) has deleted `email_intel_agent.py` /
  `email_intel_backfill.py` more than once. If they're missing, restore from git
  history (`git show <commit>:scripts/email_intel_agent.py`). Check `git log --all -- scripts/email_intel_agent.py` to find the last commit that had them.
