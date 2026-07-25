---
name: macos-onedrive-recovery
description: "Recover from OneDrive files-on-demand failures on macOS — distinguish 'Resource deadlock' (transient EDEADLK, retry) from 'stale stub' (0-byte or non-zip files when sync is disabled); use the Micro volume as a working-copy fallback. Load when cp/openpyxl/textutil fails on OneDrive paths, or the user mentions Micro/USB/external volume."
version: 1.0.0
created_by: agent
---

# macOS OneDrive Recovery

Use when working with files in `~/Library/CloudStorage/OneDrive-...` (or any OneDrive mount point) on macOS and reads/writes fail in confusing ways. Covers the two failure modes that look similar but have different fixes, and the fallback to a local working copy.

## The two failure modes

| Mode | File on disk | Behaviour | Recovery |
|---|---|---|---|
| **Transient EDEADLK** | Real bytes, just briefly locked | `cp` fails with `Resource deadlock avoided`, retries succeed within 15-60 s | `sleep 30; retry` |
| **Stale stub** (Files-on-Demand not hydrated) | Real-looking size, fake content | `unzip -l` says "End-of-central-directory signature not found"; `openpyxl` raises `BadZipFile`; `textutil` errors; `cat` shows PDF binary header | Read from the working copy on the Micro volume (or the user's external backup drive), edit there, write back when OneDrive lock clears |

**Diagnose first.** A 0-byte file or a fresh EDEADLK is one thing. A file with a real-looking size (15 KB, 79 KB, 471 KB) that won't unzip is the stub. Don't waste 5+ tool calls retrying — check `brctl status` for `SYNC DISABLED (app not installed)`, then go straight to the working-copy path.

```bash
# Quick diagnostic
lsof "$PATH" 2>&1 | head -3                # is a real app holding it?
ls -la "$PATH"                              # real size or 0?
unzip -l "$PATH" 2>&1 | head -3             # valid zip?
brctl status 2>&1 | grep -i "sync disab"   # is the client broken?
```

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
3. **Read from the working copy.** Use tools appropriate to the file type:
   - DOCX → `python-docx` (`from docx import Document`)
   - PDF → `pdftotext -layout` (poppler, in `/opt/homebrew/bin/`)
   - XLSX → `openpyxl.load_workbook(read_only=True, data_only=True)`
   - HTML → `textutil -convert txt -stdout` or just `cat`
4. **Edit on the working-copy path** (Micro, repo, or wherever the source is). Use `write_file`, `patch`, or a `python` script that opens the file in place.
5. **Re-render derived artefacts** (PDF from DOCX via `pandoc`, etc.) to `/tmp/`, then `cp` to Micro or the repo.
6. **Try to write back to OneDrive** — single attempt, with one retry after a 30 s wait. If the second attempt fails, leave the new file on the working-copy path and tell the user.
7. **Log what happened** so the next session knows. Mention the OneDrive state in your final reply.

## What NOT to do

- Do not `cat > /path/to/OneDrive/...` to "force write past the lock" — you'll create a 0-byte file and confuse the next session.
- Do not assume Micro is stale just because it's mounted on a different volume. Check mtimes.
- Do not `rm` the OneDrive stub as "cleanup" — OneDrive will re-create it on the next sync.
- Do not loop a 5-attempt retry on EDEADLK. One retry after 30 s is enough; if it still fails, switch paths.
- Do not push to git from a Micro file without re-staging to the repo on the main volume first — git tracks inodes, not paths, and a move across volumes can surprise.

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

## Reference files

- `references/stale-stub-vs-realdeadlk.md` — full diagnostic transcript, including `brctl status` output, exact error messages, and recovery steps for the 02.17 RMP case.
