# Stale stub vs real EDEADLK — diagnostic transcript (2026-07-24, Aseer 02.17 RMP)

**Source session:** RMP REV01 sync. User said the morning's RMP was finalised and asked to update the repo and the latest RMP version. I was given the DOCX via the chat; it was the **stale REV00**. After confirming the working copy was on Micro, I edited it and rendered new PDF + HTML.

## What "stale stub" looked like

```text
$ ls -la "$OneDrive_Path/MOC-MUS-ASE-1KH-PL-02.17_Risk_Management_Plan.docx"
-rw-r--r--@ 1 mohamedessa  staff  111514 Jul 24 13:38 ...  # looks real
$ unzip -l "$OneDrive_Path/...docx"
Archive:  .../MOC-MUS-ASE-1KH-PL-02.17_Risk_Management_Plan.docx
  End-of-central-directory signature not found.
```

vs the same file on Micro:

```text
$ ls -la /Volumes/MIcro/Work/Aseer-Museum/04_Docs/.../Rev01/MOC-MUS-ASE-1KH-PL-02.17_Risk_Management_Plan_REV01.docx
-rwx------@ 1 mohamedessa  staff  122258 Jul 24 15:18 ...  # newer, larger, real bytes
$ unzip -l .../Rev01/...docx
Archive:  ...MOC-MUS-ASE-1KH-PL-02.17_Risk_Management_Plan_REV01.docx
  Length      Date    Time    Name
      590  01-01-1980 00:00   _rels/.rels
     1471  01-01-1980 00:00   word/_rels/document.xml.rels
   ...  (valid zip parts)
```

## What `brctl status` said

```text
<3{8}G.c{1}m.r{5}e.C{13}s[130] background {client:idle server:full-sync|fetched-recents|fetched-favorites|ever-full-sync sync:oob-sync-ack last-sync:2026-07-18 08:56:01.887, caught-up, token:unkown-token-size:34 ...}
>>> SYNC DISABLED (app not installed)
```

`SYNC DISABLED (app not installed)` was the smoking gun. The OneDrive app was uninstalled/broken for that subtree; the file metadata is preserved but no real content is being delivered.

## What I tried first (and why they failed)

| Attempt | Result | Why |
|---|---|---|
| `cp "$OneDrive" /tmp/rmp-final.docx` | `Resource deadlock avoided`, 0-byte file | OneDrive stub race |
| `python3 open("...", "rb").read()` | `[Errno 11] Resource deadlock avoided` (3 attempts) | Same |
| `textutil -convert txt -stdout "$OneDrive"` | `Error reading ... The file ... couldn't be opened` | Same |
| Re-try after 30 s sleep | Same | Stale stub, not transient EDEADLK |
| Quit OneDrive, wait, retry | Same | `brctl` shows the sync client is gone for this folder |

## What worked

1. Asked the user "Maybe you will find in micro volume" hint → looked in `/Volumes/MIcro/Work/Aseer-Museum/...`
2. Found a `Rev01/` subfolder on Micro with the 24-Jul-15:18 file (newer, valid zip).
3. Read with `python-docx` (`from docx import Document; doc = Document(path)`) — succeeded.
4. Patched 10 table cells (Revision, Date, doc control row, snapshot, distribution, register structure, status summary) using `python-docx` with run-aware text replacement.
5. Re-rendered PDF via `pandoc input.docx -o output.pdf`.
6. Re-rendered HTML via `pandoc input.docx -o output.html`.
7. Wrote back to Micro (the source-of-edit) with `cp`.
8. Tried OneDrive write — **succeeded** on the second attempt (the lock had cleared in the meantime).
9. The HTML file's OneDrive write continued to fail with EDEADLK even after retries; left the new HTML on Micro and noted it in the final report.

## Key takeaways

- **Stale stub ≠ real EDEADLK.** Real EDEADLK retries succeed. Stale stubs never do (until the sync client is healthy). Differentiate via `brctl status` and the file mtime.
- **The Micro path is the live working copy** for the `04_Docs/` subtree when OneDrive is unhealthy. Treat as such. Do not assume "Micro = stale" — that rule applies to `04_Plans/` and `.pi-tmp/`, not `04_Docs/`.
- **User hints are the fastest signal.** "Maybe you will find in micro volume" was a 3-word hint that saved 5+ failed probe attempts.
- **OneDrive file locks are per-file and can clear independently.** The DOCX write succeeded on the second attempt; the HTML write kept failing for the rest of the session. They have separate locks.

## Commands that worked (clean, in order)

```bash
# 1. Diagnose
brctl status 2>&1 | grep -i "sync disab"
lsof "$OneDrive_Path" 2>&1 | head -3
unzip -l "$OneDrive_Path" 2>&1 | head -3

# 2. Find working copy
ls -la /Volumes/MIcro/Work/Aseer-Museum/04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files/03_Word/

# 3. Read with python-docx
python3 -c "from docx import Document; doc = Document('/Volumes/MIcro/.../Rev01/...docx'); print(len(doc.tables))"

# 4. Patch (script in /tmp/patch_rmp_rev01.py)

# 5. Re-render PDF + HTML
pandoc /tmp/rmp-rev01-updated.docx -o /tmp/rmp-rev01-updated.pdf
pandoc /tmp/rmp-rev01-updated.docx -o /tmp/rmp-rev01-html.html

# 6. Write back to Micro (always works)
cp /tmp/rmp-rev01-updated.docx /Volumes/MIcro/.../Rev01/...

# 7. Try OneDrive, with one retry
cp /tmp/rmp-rev01-updated.docx "$OneDrive_Path/MOC-MUS-ASE-1KH-PL-02.17_Risk_Management_Plan_REV01.docx"
# If it fails: sleep 30, retry once. If still fails, leave on Micro and report.
```

## When this pattern will fire again

- After any OneDrive client update, app crash, or partial uninstall
- After macOS upgrades that touch the filesystem provider
- When the user takes a long break (their laptop sleeps, OneDrive client state diverges)
- When the user switches Wi-Fi networks repeatedly (sync state churn)

The pattern is per-machine and per-OneDrive-account. Same machine, same account → same problem recurring. The recovery steps are stable.
