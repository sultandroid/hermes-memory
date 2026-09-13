# SURGE.md — Shared Deploy Credentials & Runbook (ALL projects)

> **Hub-layer, cross-project.** One surge.sh account hosts the review pages for **every**
> project — RCRC, Aseer, Samaya, Jameya, Sultan House. Any agent publishing a page reads
> this file first. Do not duplicate this info into project repos.

Last verified: 2026-09-12 (re-login + `surge list` → 26 domains).

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

## 3. Publish

```bash
SURGE_TOKEN=<token> <surge-path> publish ./ <domain>.surge.sh
```

**Gotcha:** always pass the target **domain** as the second argument. `surge ./` alone
returns `"nothing to do"` and fails.

Verify after every deploy — expect HTTP 200:

```bash
curl -sL --max-time 8 -o /dev/null -w "%{http_code}\n" https://<domain>.surge.sh/
```

## 4. Interactive login (only after a token rotation)

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

## 5. Live domains (26)

### RCRC — proposal + governing docs
```
rcrc-exhibition-proposal.surge.sh      rcrc-design-management-plan.surge.sh
rcrc-content-methodology.surge.sh      rcrc-execution-methodology.surge.sh
rcrc-flowchart-fixed.surge.sh          rcrc-flowchart-preview.surge.sh
rcrc_train_preview.surge.sh
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

## 6. Source-of-truth rule

Surge hosts a **review copy**. The authoritative source is the project repo (HTML +
generator scripts). Edit → regenerate → publish. Never hand-edit the deployed copy; the
next deploy overwrites it.

Arabic / RTL pages: Cairo for Arabic, RTL direction, project's doc style guide.
User preference: HTML review on surge **first**, DOCX only after approval.

## 7. Useful commands

```bash
SURGE_TOKEN=... surge list                       # all domains + last-deploy age
SURGE_TOKEN=... surge publish ./dist <domain>.surge.sh
SURGE_TOKEN=... surge token                      # rotate (update this file after)
SURGE_TOKEN=... surge teardown <domain>.surge.sh # destroy a domain
```

## 8. Coordination warning

Deploy times reveal concurrent agent activity. Before publishing a shared domain, run
`surge list` — if it was deployed minutes ago, another agent may be mid-edit on the same
page. Coordinate rather than overwrite blindly.
