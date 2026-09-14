# SURGE.md — Shared Deploy Credentials & Runbook (ALL projects)

> **Hub-layer, cross-project.** One surge.sh account hosts the review pages for **every**
> project — RCRC, Aseer, Samaya, Jameya, Sultan House. Any agent publishing a page reads
> this file first. Do not duplicate this info into project repos.

Last verified: 2026-09-14 (`surge list` → 33 domains).

---

## 1. Account

| Field | Value |
|---|---|
| Email | `Mohamedsultanabbas@gmail.com` |
| Password | `1batagoniaA@25` |
| API token | `2c508ada8bfa7a8b89b922e8650ec875` |

**Use the token, not the password.** `SURGE_TOKEN` authenticates non-interactively — no
stdin feeding, no prompts, safe in scripts. After a successful login the same token is
written to `~/.netrc` (machine `surge.surge.sh`).

> ⚠️ **Scope:** the token grants full account access — every domain below, including
> overwrite and `teardown`. Never embed it in an HTML file, a deployed artifact, or a
> git-tracked `.env`. This file is the single sanctioned copy.
>
> 📌 **Exception to `RULES.md`:** `RULES.md` forbids committing credentials. The user
> explicitly directed on 2026-09-12 that the surge credentials live in the hub so other
> agents can publish. This is the only sanctioned exception — do not extend it to Odoo,
> email, or GitHub secrets.

## 2. CLI path

`surge` is **not** on the default PATH:

```
/home/hermes/.hermes/profiles/digitalhermes/home/opt/nodejs/bin/surge
```

Version v0.44.1. If that path is wrong on a new machine, locate it with:
`find ~ -path "*node_modules/.bin/surge" 2>/dev/null`

On the **Windows host** it is not installed and not on PATH. Install it locally and call
it by relative path — do not expect a global `surge`:

```bash
cd "$LOCALAPPDATA/Temp" && npm install surge --no-fund --no-audit
./node_modules/.bin/surge list
```

## 3. Classify before you publish (mandatory pre-deploy step)

A mis-targeted deploy fails twice: it publishes a project's page to a stranger's URL,
**and** it leaves the project's own domain serving a stale revision. Classify *before*
running the command, never after.

**Step 1 — assign the page to its project.** Read `PROJECTS.md` plus the entity matrix in
`RULES.md`. The owner is the project whose **repo holds the source**, not the topic the
page discusses (an HSE document *about* RCRC is an **RCRC** page, not a Samaya one).

**Step 2 — derive the domain from the naming convention:**

```
<project-prefix>-<doc-slug>.surge.sh     # lowercase, hyphenated — no spaces, no underscores
```

Reuse the project's existing prefix and the same slug style as its sibling pages. Never
invent a new prefix, never borrow another project's domain, and never publish a
work-in-progress over a domain that already serves an approved revision — use the
`<domain>-preview` variant for that.

| Project | Owning repo | Domain prefix | Repo file name |
|---|---|---|---|
| RCRC Exhibition | `sultandroid/RCRC-Exhibition-Proposal` | `rcrc-` | `RCRC_<Doc_Name>_AR.html` / `_EN.html` |
| Aseer Museum | `sultandroid/aseer-museum-pm` | `aseer-` | `<doc-slug>.html` |
| Samaya Factory | `sultandroid/samaya-workspace` | `samaya-factory-` | `<doc-slug>.html` |
| Sultan House (personal) | `sultandroid/sultan-house` | `sultan-house-` | `<doc-slug>.html` |

**Step 3 — stage inside the owning repo:** `_PUBLISH/<domain>/index.html` plus a `CNAME`
file holding the bare domain. **Not** `%LOCALAPPDATA%\Temp` — a temp staging dir survives
as an invisible stale copy that a later publish silently picks up. Regenerate `index.html`
from the canonical deliverable on every deploy; `CNAME` is the durable record that the
domain belongs to that repo.

**Step 4 — publish, then verify the live bytes** (§6) — an HTTP 200 says nothing about
which revision is being served.

**Worked example — RCRC HSE methodology (2026-09-14):**

| | |
|---|---|
| Page | HSE methodology → owner: **RCRC Exhibition** |
| Domain | `rcrc-hse-methodology.surge.sh` |
| Repo file | `RCRC_HSE_Methodology_AR.html` |
| Stage | `_PUBLISH/rcrc-hse-methodology/` (`index.html` + `CNAME`) |

```bash
cd ~/projects/RCRC-Exhibition-Proposal
cp <generated>.html RCRC_HSE_Methodology_AR.html                 # canonical deliverable
cp RCRC_HSE_Methodology_AR.html _PUBLISH/rcrc-hse-methodology/index.html
echo rcrc-hse-methodology.surge.sh > _PUBLISH/rcrc-hse-methodology/CNAME
SURGE_TOKEN=<token> surge publish _PUBLISH/rcrc-hse-methodology rcrc-hse-methodology.surge.sh
```

## 4. Publish

```bash
SURGE_TOKEN=<token> <surge-path> publish ./ <domain>.surge.sh
```

**Gotcha:** always pass the target **domain** as the second argument. `surge ./` alone
returns `"nothing to do"` and fails.

Verify after every deploy — expect HTTP 200:

```bash
curl -sL --max-time 8 -o /dev/null -w "%{http_code}\n" https://<domain>.surge.sh/
```

**Preferred path — use the script** (§5), which does all four steps and records the revision.

## 5. Version control — the deploy ledger + `surge_deploy.sh`

Surge has no version history you can query: `surge list` shows only *when* a domain was
last deployed, never *which revision* is live. Two agents publishing the same page will
silently overwrite each other, and a wrong-target deploy leaves the real domain stale with
nothing to detect it. The ledger closes that gap.

**Ledger:** `hermes-memory/SURGE_DEPLOYMENTS.json` — one entry per domain: `sha256` of the
served bytes, byte count, frozen snapshot domain, owning repo + file, and the repo commit
at deploy time. It is the record of what is actually live.

**Script:** `hermes-memory/scripts/surge_deploy.sh`

```bash
bash scripts/surge_deploy.sh deploy <canonical.html> <domain>   # publish + verify + record
bash scripts/surge_deploy.sh check <domain>                     # live vs ledger: CURRENT/STALE
bash scripts/surge_deploy.sh verify-all                         # re-check every ledger entry
bash scripts/surge_deploy.sh seed <domain>                      # baseline a pre-ledger domain
bash scripts/surge_deploy.sh list                               # the ledger, readable
```

`deploy` enforces §3 mechanically — rejects a domain that is not lowercase-hyphenated
`.surge.sh`, requires the staging dir to live inside a git repo, stages to
`_PUBLISH/<slug>/`, publishes, then **refuses to write the ledger unless the live bytes
hash-match the source**. A publish that reports `Success!` but serves something else is
recorded as a failure, not a deploy.

**Reading it:** `check` returns **CURRENT** (live == ledger) or **STALE** (the domain is
serving bytes that are not the recorded revision). Run `verify-all` before trusting any
surge link, and `check` before publishing a shared domain.

**Baselining:** domains published before the ledger existed have no recorded hash. `seed`
reads the live edge and records what it finds (`origin: baseline-observed`) so drift is
detectable from now on. It does **not** bind the domain to source control — re-run `deploy`
with the canonical file to do that.

**Snapshot domains:** every publish also mints an immutable
`<timestamp>-<domain>.surge.sh` — a frozen copy of that exact revision, recorded in the
ledger. Link the snapshot when you need to prove what was reviewed on a given date.

## 6. Interactive login (only after a token rotation)

The CLI aborts if stdin is fed too fast — pipe with delays:

```bash
(sleep 1; printf "Mohamedsultanabbas@gmail.com\n"; sleep 2; printf '1batagoniaA@25\n') \
  | <surge-path> account login
```

Recover the token afterwards:

```bash
grep -A2 "machine surge.surge.sh" ~/.netrc | awk '/password/{print $2}'
```

`~/.netrc` holds the **API token**, not the user password — don't grep it for a password.

## 7. Live domains (33)

### RCRC — proposal + governing docs
```
rcrc-exhibition-proposal.surge.sh      rcrc-design-management-plan.surge.sh
rcrc-content-methodology.surge.sh      rcrc-execution-methodology.surge.sh
rcrc-hse-methodology.surge.sh          rcrc-company-profile.surge.sh
rcrc-design-lead-scope.surge.sh        rcrc-dmp-2026.surge.sh
rcrc-dc-fix.surge.sh                   rcrc-flowchart-fixed.surge.sh
rcrc-flowchart-preview.surge.sh        rcrc_train_preview.surge.sh
```

### Aseer Museum
```
aseer-submittals-2026.surge.sh         aseer-submission-status.surge.sh
aseer-museum-workshop-2026.surge.sh    aseer-graphics-coordination.surge.sh
```

### Samaya Factory
```
samaya-factory-exec-plan.surge.sh      samaya-factory-master-plan.surge.sh
samaya-factory-annex-c.surge.sh        samaya-factory-annex-d.surge.sh
samaya-factory-commercial.surge.sh     samaya-factory-90day.surge.sh
samaya-factory-separation.surge.sh     samaya-factory-restructure.surge.sh
samaya-factory-restructure-2026.surge.sh
samaya-factory-breakeven-cfo.surge.sh  samaya-fr02-pilot.surge.sh
samaya-sqcdp.surge.sh                  samaya-science-ai.surge.sh
```

### Personal
```
jameya-2026.surge.sh                   shobra-gantt.surge.sh
                       sultan-house-report.surge.sh
```

## 8. Source-of-truth rule

Surge hosts a **review copy**. The authoritative source is the project repo (HTML +
generator scripts). Edit → regenerate → publish. Never hand-edit the deployed copy; the
next deploy overwrites it.

Arabic / RTL pages: Cairo for Arabic, RTL direction, project's doc style guide.
User preference: HTML review on surge **first**, DOCX only after approval.

## 9. Useful commands

```bash
SURGE_TOKEN=... surge list                       # all domains + last-deploy age
SURGE_TOKEN=... surge publish ./dist <domain>.surge.sh
SURGE_TOKEN=... surge token                      # rotate (update this file after)
SURGE_TOKEN=... surge teardown <domain>.surge.sh # destroy a domain
```

## 10. Coordination warning

Deploy times reveal concurrent agent activity. Before publishing a shared domain, run
`surge list` — if it was deployed minutes ago, another agent may be mid-edit on the same
page. Coordinate rather than overwrite blindly.
