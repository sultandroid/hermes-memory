# Published-doc / local-source sync

When the user asks for an edit to a document that exists BOTH as a local HTML source and as a published build (Surge domain, shared-hosting path, or a PDF rendered from either), prove the two are the same document before editing. This is a pre-flight step, not an optional check.

## Why this is needed

Samaya document builds are frequently assembled on a different host (or in an ephemeral staging directory that is cleaned up) and published without the source being written back to OneDrive. The local file is then an **older, thinner build** while the domain serves the current one. Any edit applied to the local file is invisible in what the user reads, prints, or sends — and reporting "done" is a false completion.

The same drift happens in reverse when a document is reworked locally and published from `/tmp`, leaving the OneDrive copy untouched.

## Pre-flight recipe

### 1. Fetch every live page and compare to its local source

```bash
for u in index.html doc-a.html doc-b.html; do
  printf "%-20s " "$u"
  curl -sL -o "/tmp/live_$u" -w "%{http_code} " "https://<domain>.surge.sh/$u"
  wc -c < "/tmp/live_$u"
done
```

Then md5 both sides in Python:

```python
import subprocess, hashlib, os

def fetch(url):
    return subprocess.run(["curl", "-sL", "--max-time", "60", url],
                          capture_output=True).stdout

for page, local_path in [("index.html", "_PUBLISH/index.html"),
                         ("doc-a.html", "_BMA/Doc_A_AR.html")]:
    pv = fetch(f"https://preview-domain.surge.sh/{page}")
    pd = fetch(f"https://prod-domain.surge.sh/{page}")
    loc = open(local_path, "rb").read()
    same = lambda b: "same" if hashlib.md5(b).hexdigest() == hashlib.md5(loc).hexdigest() else "DIFF"
    print(f"{page:<18}{len(pv):>9}{len(pd):>9}{len(loc):>9}  pv:{same(pv)} pd:{same(pd)}")
```

The three-way print (preview / production / local) is worth the extra call: it exposes `preview != prod` in the same pass, which is common on the Samaya Surge account. A page can 404 on one domain and 200 on the other; a path can serve different builds on each.

### 2. When sizes disagree, diff the body text

Size alone does not prove divergence — a build that inlines the brand logo and fonts as base64 runs roughly 2x a build that references them. Compare the extracted body text:

```python
import re, difflib

def bodytext(s):
    b = re.search(r'<body[^>]*>(.*)</body>', s, re.S).group(1)
    b = re.sub(r'<(style|script).*?</\1>', '', b, flags=re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', b)).strip()

lo, lt = bodytext(local_html), bodytext(live_html)
print("local body chars", len(lo), "live body chars", len(lt))
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, lo, lt).get_opcodes():
    if tag != 'equal':
        print(tag, '| LOCAL:', repr(lo[i1:i2][:200]), '|| LIVE:', repr(lt[j1:j2][:200]))
```

Read the opcodes as a content ledger: `delete` runs are content the local file has that live does not (a whole paragraph, a section's activity rows); `insert` runs are content live has that local lacks (a reworked section, extra RACI rows). A long `delete` of a whole subsection is conclusive — the local file is a different build, not a cosmetic variant.

## Divergence signals table

| Signal | Meaning |
|---|---|
| Live bytes `>= 1.8x` local bytes | Usually base64 inlining (benign) OR a fuller build. Confirm with the body diff before deciding. |
| Same byte count, same md5 | Local == live. Safe to edit. |
| Live has sections/paragraphs absent from local | Local is an older build. Live is the working document. |
| Local has sections live lacks | Local is a newer un-published draft, or a fork. Ask which is master. |
| Path 404 on preview, 200 on prod | Domains serve different builds. Probe both before quoting a link. |
| AR file and EN file disagree on structure | Languages are edited separately; expect one revision ahead. |
| `SURGE_DEPLOY.md` / `publish_surge.sh` byte sizes don't match live | The deploy manifest is stale, not the deploy. Trust live bytes; fix the manifest. |

## What to do

**Local == live** → edit in place normally (backup as `.bak-<reason>` first).

**Live is ahead, no local source exists** → STOP. Do not edit the local file, and do not "sync" by overwriting either side. Report the divergence to the user as a table (file / bytes / what differs), state plainly that the on-disk copy is not what is live, and present the recovery options:

1. Pull the live page back as the canonical source (keep the stale file as `.bak-<reason>`), so local == live and all later edits land on real text.
2. User drops the true source file from the machine that built it.
3. Bring the lagging language/build up to parity before editing anything else.

Ask which build is master; write nothing until the user answers. Overwriting on your own initiative destroys whoever's build is live.

## Verify you can find a build before claiming it is missing

Before reporting "no local source exists", search by a string that only the newer build contains (a reworked clause, a new section heading) across every candidate root — the org OneDrive, personal OneDrive, Desktop, Downloads, Documents, `/tmp`, `~/tmp`, and `.hermes/cache`. Walk with a Python loop that catches read errors per file: on OneDrive, the vast majority of files raise `EDEADLK` ("Resource deadlock avoided"), so a `try/except: continue` loop with an error counter is the reliable scanner, and a hit count of zero after such a run is a real negative only if the error count is small relative to files scanned.

Also check the builder scripts and staging directories: a per-document build script in the repo (e.g. a RACI-merge script that rewrites both language files) is evidence a build step exists, and the script's own path constant tells you which root the build ran against.
