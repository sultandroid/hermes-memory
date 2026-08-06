---
name: macos-onedrive-recovery
description: "Recover from OneDrive files-on-demand failures on macOS — distinguish 'Resource deadlock' (transient EDEADLK, retry) from 'stale stub' (0-byte or non-zip files when sync is disabled) and 'write-block' (File Provider TCC restricts ALL writes to non-Finder processes); use the Micro volume as a working-copy fallback, or stage organized files to /tmp/ for manual Finder drag. Load when cp/openpyxl/textutil fails on OneDrive paths, or the user mentions Micro/USB/external volume."
version: 1.0.0
created_by: agent
---

# macOS OneDrive Recovery

Use when working with files in `~/Library/CloudStorage/OneDrive-...` (or any OneDrive mount point) on macOS and reads/writes fail in confusing ways. Covers the three failure modes that look similar but have different fixes, and the fallback to a local working copy.

## Bypass techniques that sometimes work

When standard `cp`, `ditto`, `rsync`, `dd`, and `strings` all fail with EDEADLK, these techniques may work. Try in this order:

### 1. `cp -c` (clonefile/APFS copy-on-write)

```bash
cp -c "/path/to/OneDrive/file.xlsx" /Volumes/MIcro/.pi-tmp/work/
```

`cp -c` uses APFS clonefile(2) which can bypass the File Provider lock in some cases where regular `cp` (which uses fcopyfile) cannot. **Not universal** — it worked for one file in a session but failed for others in the same directory. Worth exactly one attempt before falling back to the retry-loop or reboot.

### 2. Python retry-loop with `io.BytesIO`

Read the file into memory via Python with retries, then parse from the in-memory buffer:

```python
import time, io

path = '/path/to/OneDrive/file.xlsx'
for attempt in range(10):
    try:
        with open(path, 'rb') as f:
            data = f.read()
        # Parse from memory — bypasses the lock for the parser
        import openpyxl
        wb = openpyxl.load_workbook(io.BytesIO(data), data_only=True)
        # ... use wb normally
        break
    except OSError as e:
        if 'Resource deadlock' in str(e):
            time.sleep(2)
            continue
        raise
```

This works because the `open()` call is the only point of contact with the locked file. Once the bytes are in memory, the parser never touches the filesystem again. The retry loop (up to 10 attempts with 2 s delay) usually succeeds within 4-6 attempts as the File Provider lock is transient at the read level. **Does not work during write-block** — only for reads.

### 3. `ditto --norsrc`

```bash
ditto --norsrc "/path/to/OneDrive/file.xlsx" /tmp/copy.xlsx
```

`--norsrc` skips extended attributes and resource forks, which can sometimes avoid the lock. Rarely works — try before the retry-loop, not after.

### 5. Generate from template instead of copying (best for locked template files)

When the locked file is a **template** (DOCX, XLSX, HTML) that can be regenerated programmatically, skip the copy entirely:

- **DOCX**: Use `samaya_doc_template.py` (at `_Style-Guides/Doc Style Guide/samaya_doc_template.py`) to generate a fresh branded document
- **XLSX**: Use `openpyxl` to create a new workbook with the same structure
- **HTML**: Recreate from known brand specs

This avoids the OneDrive lock entirely and produces a clean file. Only works when the file is a template/starter, not when it contains unique data.

```python
# Example: generate Samaya DOCX instead of copying locked OneDrive file
import sys
sys.path.insert(0, '_Style-Guides/Doc Style Guide')
from samaya_doc_template import SamayaDoc

doc = SamayaDoc()
doc.create_header('Project Name', 'REF-001', 'DOC', 'A', 'Aug 2026')
doc.add_h1('DOCUMENT TITLE')
doc.add_body('Content here.')
doc.save('/tmp/Generated_Template.docx')
```

When all shell-level copy methods fail, AppleScript's Finder `duplicate` command can sometimes bypass the lock because Finder uses a different I/O path:

```applescript
tell application "Finder"
    set src to POSIX file "/path/to/OneDrive/file.xlsx" as alias
    set dst to POSIX file "/Volumes/MIcro/.pi-tmp/work/" as alias
    duplicate src to dst
end tell
```

**Caveats:**
- This command **hangs indefinitely** (no timeout) if the lock is persistent — the terminal tool will time out after 15-30s with no output
- It creates a 0-byte file on the destination if it fails silently
- Only worth one attempt. If it hangs, kill it and move to reboot
- The 0-byte file it leaves behind is harmless — just overwrite it later

## The four failure modes

| Mode | File on disk | Behaviour | Recovery |
|---|---|---|---|
| **Transient EDEADLK** | Real bytes, just briefly locked | `cp` fails with `Resource deadlock avoided`, retries succeed within 15-60 s | `sleep 30; retry` |
| **Stale stub** (Files-on-Demand not hydrated) | Real-looking size, fake content | `unzip -l` says "End-of-central-directory signature not found"; `openpyxl` raises `BadZipFile`; `textutil` errors; `cat` shows PDF binary header | Read from the working copy on the Micro volume (or the user's external backup drive), edit there, write back when OneDrive lock clears |
| **Write-block** (File Provider TCC) | Fully local, readable | ALL write methods fail with `Operation not permitted`: `cp`, `mv`, `ditto`, `cat >`, `mkdir`, Python `open('wb')`, AppleScript Finder `duplicate`/`move`. Creating new files or dirs also blocked. | Stage files to non-OneDrive volume (MICro, /tmp/), open both Finder windows, tell user to drag manually. Only Finder and OneDrive app can write. |
| **Persistent EDEADLK** (kernel-level File Provider lock) | Real bytes, locked at kernel level | `cp`, `dd`, `rsync`, `ditto`, `strings`, `cat`, `file`, Python `open()`, `os.read()` ALL fail with `Resource deadlock avoided`. Even after `kill -9` of all OneDrive processes (`OneDrive`, `OneDrive Sync Service`, `OneDrive Finder Extension`) and `launchctl bootout` of the sync service. `lsof` shows no process holding the file. `brctl status` says "Path is outside of any CloudDocs app library". | **Only reboot clears this lock.** The lock is held by the macOS File Provider kernel extension, not a user-space process. No amount of process killing (`kill -9`, `killall -9 OneDrive*`), launchctl unloading, or brctl eviction will release it. After reboot, read files before OneDrive re-establishes its sync session. Alternative: use the OneDrive/SharePoint web UI in browser to download files, or ask the user to copy files manually via Finder to a non-OneDrive volume (Micro, Desktop, /tmp/). |

**Diagnose first.** A 0-byte file or a fresh EDEADLK is one thing. A file with a real-looking size (15 KB, 79 KB, 471 KB) that won't unzip is the stub. Don't waste 5+ tool calls retrying — check `brctl status` for `SYNC DISABLED (app not installed)`, then go straight to the working-copy path. If `cp file /path/to/OneDrive/` fails with `Operation not permitted` but the source file is readable, this is the write-block — don't retry, use the Finder-drag workaround instead.

```bash
# Quick diagnostic
lsof "$PATH" 2>&1 | head -3                # is a real app holding it?
ls -la "$PATH"                              # real size or 0?
unzip -l "$PATH" 2>&1 | head -3             # valid zip?
brctl status 2>&1 | grep -i "sync disab"   # is the client broken?
# Write-block diagnostic (try to write a test file)
touch "$(dirname "$PATH")/.od_write_test" 2>&1
# → "Operation not permitted" = write-block active
```

### Special case: OneDrive-stored Python modules

When a `.py` file on OneDrive is a stale stub (null bytes), **importing it as a Python module** fails with `SyntaxError: source code string cannot contain null bytes` or the file reads as all `\x00` bytes. This is the same stale-stub failure mode but manifests at import time rather than at read time.

**Detection:**
```bash
# Quick check — does the file have real Python content?
head -c 200 /path/to/onedrive/template.py | xxd | head -3
# All 0000 0000 0000 0000 = stale stub
```

**If the template file is essential** (e.g., SamayaDoc class for branded DOCX generation):
1. Force OneDrive to sync: `open` the folder in Finder and click the file
2. If sync is permanently stuck or the file cannot be downloaded, **replicate the styling manually** in python-docx using known brand specs
3. Document the fallback in a reference file so future sessions don't retry the same dead end

**Example:** The SamayaDoc template (`samaya_doc_template.py`) at 19KB with all-null content is a stale stub. The fix is manual Samaya-style replication — documented in `bim-technical-documentation` skill's `references/samaya-docx-generation-tbd-fill.md`.

## Micro volume as working-copy fallback

Many Aseer Museum / Samaya workflows keep a manual backup on `/Volumes/MIcro/Work/Aseer-Museum/` (or another external volume). It mirrors the OneDrive tree but with a `Work/` prefix:

- OneDrive: `~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/.../Aseer-Museum/04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files/03_Word/MOC-MUS-ASE-1KH-PL-02.17_Risk_Management_Plan.docx`
- Micro:   `/Volumes/MIcro/Work/Aseer-Museum/04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files/03_Word/Rev01/MOC-MUS-ASE-1KH-PL-02.17_Risk_Management_Plan_REV01.docx`

The Micro path is **not** a stale cache. When the user says "the morning's file is on Micro" or "check the USB" or similar, treat Micro as the live working copy and OneDrive as the read-only mirror.

**Caveat:** some Micro paths are NOT a working copy — they are stale agent scratch. Specifically:
- `/Volumes/MIcro/.pi-tmp/` and `/Volumes/MIcro/.aseer-tmp/` — agent scratch dirs, safe to ignore / overwrite
- `/Volumes/MIcro/Work/Aseer-Museum/04_Plans/` — older repo mirror, no longer the live source
- `/Volumes/MIcro/Work/Aseer-Museum/04_Docs/...` (under the `04_Docs/` tree) — this **is** the live working copy, treat as such

**Decision rule for the Micro `Work/` tree:** if the file's mtime is **after** the corresponding OneDrive file's mtime, Micro is the live source. Read from Micro, edit on Micro, write back to OneDrive only after the lock clears.

## Write-block workaround: staging to /tmp/ for Finder drag

When the File Provider write-block is active and you need to deliver organized files into OneDrive:

1. **Stage files in a structured directory** under `/tmp/<job>_filed/` or `/Volumes/MIcro/Temp/<job>/`, organized by destination folder (e.g., one sub-folder per PQ ref). Do not use OneDrive as the staging area — every write attempt will fail.
2. **Include a FILE_MAPPING.csv** in the staging directory so the user can see which file goes where.
3. **Open both locations in Finder**:
   ```bash
   open /tmp/<job>_filed/
   open "/path/to/OneDrive/target/folder/"
   ```
4. **Tell the user to drag** each sub-folder from the source window into the corresponding OneDrive target folder. The user reports this works after confirming they know the destination.

**Do NOT attempt to open the staged files directly in Finder as a copy mechanism** — the `open` command from terminal opens files in Preview, which does NOT bypass the write-block.

## Recovery procedure

1. **Identify the failure mode** (see diagnostic above). 30 s wait is cheap; 5 retries are not.
2. **If stale stub:** find the working copy:
   - Check the Micro volume: `ls -la /Volumes/MIcro/Work/Aseer-Museum/04_Docs/...`
   - Check the user's other backup locations if you know them (project README, memory)
   - Check the **git repo** — many workflows stage source files in a `source/` or
     `references/` directory under the project's git repo, as a deterministic
     non-OneDrive mirror. Example: `06_Risk_System/source/C11_reference/` in
     `sultandroid/aseer-museum-pm`. The repo is a third-tier fallback when both
     OneDrive and Micro are unavailable or stale.
   - Ask the user. Don't guess. They may be editing on a remote desktop, on a different machine, or have a version you don't know about.
3. **If write-block:** stage organized files to `/tmp/<job>_filed/` with a mapping CSV, open both Finder windows, and tell the user to drag. Do not waste retries on cp/mv/ditto.
4. **Read from the working copy.** Use tools appropriate to the file type:
   - DOCX → `python-docx` (`from docx import Document`)
   - PDF → `pdftotext -layout` (poppler, in `/opt/homebrew/bin/`)
   - XLSX → `openpyxl.load_workbook(read_only=True, data_only=True)`
   - HTML → `textutil -convert txt -stdout` or just `cat`
5. **Edit on the working-copy path** (Micro, repo, or wherever the source is). Use `write_file`, `patch`, or a `python` script that opens the file in place.
6. **Re-render derived artefacts** (PDF from DOCX via `pandoc`, etc.) to `/tmp/`, then `cp` to Micro or the repo.
7. **Try to write back to OneDrive** — single attempt, with one retry after a 30 s wait. If the second attempt fails, leave the new file on the working-copy path and tell the user.
8. **Log what happened** so the next session knows. Mention the OneDrive state in your final reply.

## What NOT to do

- Do not `cat > /path/to/OneDrive/...` to "force write past the lock" — you'll create a 0-byte file and confuse the next session.
- Do not assume Micro is stale just because it's mounted on a different volume. Check mtimes.
- Do not `rm` the OneDrive stub as "cleanup" — OneDrive will re-create it on the next sync.
- Do not loop a 5-attempt retry on EDEADLK. One retry after 30 s is enough; if it still fails, switch paths.
- Do not push to git from a Micro file without re-staging to the repo on the main volume first — git tracks inodes, not paths, and a move across volumes can surprise.
- **Do not retry writes to OneDrive during write-block.** One attempt is diagnostic; a second after 30 s proves persistence. Every subsequent attempt wastes tool calls. The File Provider TCC restriction will not lift during a session — only Finder/manual drag works.
- Do not attempt to script around the write-block with AppleScript Finder `duplicate` or `move` — these also fail with error -8004. The block is at the kernel extension level, not the application level.

## User-hint patterns

When the user says any of these, treat as strong signal that OneDrive is the wrong read source:

- "check the micro volume", "look on the USB", "find it on the working copy"
- "it's on the external drive"
- "the OneDrive copy is stale / locked / out of date"
- A one-word hint like "Micro" in response to "where is the file?"

When you see such a hint, go straight to the Micro path. Don't re-probe OneDrive.

## Related skills

- `outlook-email` — references `references/onedrive-edeadlk.md` for the read-side EDEADLK. This skill covers the **stale stub** failure, which is different and not addressed there.
- `email-pipeline-automation` — has a pitfall that says `/Volumes/MIcro/Work/Aseer-Museum/` is stale. That is true for the `04_Plans/` and `.pi-tmp/` subtrees, **wrong** for `04_Docs/`. Read this skill before believing the email-pipeline-automation pitfall about Micro.
- `hermes-config-management` — `references/gateway-polling-conflict-recovery.md` covers a different OneDrive problem (the gateway service can't restart from inside the agent). Unrelated to file recovery, but same family of "stuck state" issues.
- `document-analysis` — covers the **OneDrive-locked DOCX** fallback: when even `python-docx` fails with EDEADLK on a locked DOCX, Python's `zipfile.ZipFile` + regex tag-strip may bypass the lock. Also covers `com.apple.provenance` xattr detection for OneDrive placeholder `.md` files, and the `open` hydration workaround for DOCX (same pattern as PDFs).

## Reference files

- `references/stale-stub-vs-realdeadlk.md` — full diagnostic transcript, including `brctl status` output, exact error messages, and recovery steps for the 02.17 RMP case.
