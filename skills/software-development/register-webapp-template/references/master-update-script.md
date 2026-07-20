# Master Register Auto-Update Script

Location: `~/.hermes/scripts/update-all-registers.sh`

## What it does

Rebuilds and deploys ALL register web apps from their repo source data. Runs on:
- Every `git commit` (via `.git/hooks/post-commit`)
- Daily at 1 PM KSA (via cron job `register-auto-update`)

## Current registers

| Register | Source file | Deploy path |
|----------|------------|-------------|
| Lessons Learned (LN) | `03_Plans/11_Quality/lessons_learned_register.md` | `/aseer/registers/LN/` |
| Risk Register | `06_Risk_System/webapp/src/index.html` (built from JSON) | `/aseer/registers/Risk/` |

## Adding a new register

1. Build the web app at `/tmp/{name}-app/index.html`
2. Add a section to `update-all-registers.sh` following the LN pattern
3. Add the deploy path to the verification loop
4. Commit — the post-commit hook picks it up automatically

## SSH details

- Host: samaya-factory.com
- Port: 65002
- User: u517606786
- Remote base: `/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/`
- Key-based auth only

## Verification

After deploy, the script checks HTTP 200 for each register. If any fails, the script exits non-zero and the cron/hook logs the failure.
