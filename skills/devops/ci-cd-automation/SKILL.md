---
name: ci-cd-automation
description: Set up and manage CI/CD pipelines — self-hosted GitHub Actions runners on macOS, workflow YAML patterns, deploy automation, and cron-based auto-deploy for static sites on shared hosting.
tags:
  - github-actions
  - self-hosted-runner
  - ci-cd
  - macos
  - deployment
  - automation
---

# CI/CD Automation

Set up and manage CI/CD pipelines for projects hosted on GitHub with deployment to shared hosting (Hostinger, cPanel). Covers self-hosted runners, workflow YAML patterns, and cron-based auto-deploy.

## Trigger

User asks to:
- Set up auto-deploy on commit/push
- Install a self-hosted GitHub Actions runner
- Fix deploy failures from GitHub Actions
- Create a CI/CD workflow for a project

## Self-Hosted Runner (macOS ARM64)

### When to Use

GitHub-hosted runners cannot reach non-standard SSH ports (e.g. Hostinger port 65002), private networks, or local resources. A self-hosted runner on the local machine resolves this.

### Installation

```bash
# 1. Get registration token (expires ~60 min)
TOKEN=$(curl -s -L -X POST \
  -H "Authorization: token $(gh auth token)" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/runners/registration-token" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# 2. Download and extract runner
mkdir -p ~/actions-runner && cd ~/actions-runner
curl -o actions-runner-osx-arm64-2.322.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.322.0/actions-runner-osx-arm64-2.322.0.tar.gz
tar xzf actions-runner-osx-arm64-2.322.0.tar.gz

# 3. Configure (unattended — no prompts)
./config.sh --url https://github.com/$OWNER/$REPO \
  --token $TOKEN \
  --name "machine-name" \
  --labels "macbook,osx-arm64" \
  --work _work \
  --unattended

# 4. Install as LaunchAgent (auto-start on boot, no sudo needed)
./svc.sh install $(whoami)
./svc.sh start

# 5. Verify
gh api repos/$OWNER/$REPO/actions/runners --jq '.runners[] | {name, status, labels}'
# Expected: status = "online"
```

### Workflow YAML

The workflow must use `runs-on: [self-hosted, <label>]` to target the runner:

```yaml
jobs:
  deploy:
    runs-on: [self-hosted, macbook]  # matches labels from config
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh
```

### Pitfalls

- **Token expires in ~60 min** — generate just before configuring, not ahead of time
- **`sudo ./svc.sh install` requires password** — use `./svc.sh install $(whoami)` instead to install as a user-level LaunchAgent
- **Runner shows "offline" initially** — wait 3-5 seconds after `./svc.sh start` and re-check. Needs a heartbeat cycle to register
- **LaunchAgent persists across reboots** — auto-starts on user login. No need to re-run install after reboot
- **Multiple repos need separate runner directories** — each repo gets its own `~/actions-runner-<repo>/` directory
- **Runner logs** — check `~/Library/Logs/actions.runner.<org>-<repo>.<name>/` for diagnostics
- **Workflow secrets** — SSH keys for deploy targets must be stored as GitHub secrets (e.g. `HOSTINGER_SSH_KEY`). The runner reads them as `${{ secrets.SECRET_NAME }}`

## GitHub Actions Workflow Patterns

### Deploy-on-Push (static site to shared hosting)

```yaml
name: Auto-Deploy
on:
  push:
    branches: [main]
    paths:
      - 'source/**'
      - '.github/workflows/deploy.yml'
  workflow_dispatch:

jobs:
  deploy:
    runs-on: [self-hosted, macbook]
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: |
          cd source && npm ci && npm run build
      - name: Deploy
        run: |
          ./deploy.sh
```

### Scheduled Build + Deploy (cron)

```yaml
on:
  schedule:
    - cron: '0 13 * * *'  # daily 13:00
  workflow_dispatch:
```

### Key considerations for self-hosted runners

| Factor | Implication |
|--------|-------------|
| **Network access** | Runner has full local network — can SSH to internal servers, access local DBs |
| **File system** | Can read/write local files, OneDrive, etc. |
| **Secrets** | Store SSH keys, API tokens as GitHub secrets — runner reads them at runtime |
| **Concurrency** | One runner = one job at a time. Multiple repos share the same runner queue |
| **Power/sleep** | MacBook must stay awake. Consider `caffeinate` or disable sleep |

## Cron-Based Auto-Deploy (no GitHub Actions)

For projects where GitHub Actions is unavailable or the self-hosted runner is offline, use a local cron job that checks for changes and deploys:

```bash
# ~/.hermes/scripts/auto-deploy.sh
#!/bin/bash
REPO="$HOME/project-repo"
cd "$REPO"
git fetch origin main
if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]; then
  git pull --rebase origin main
  ./deploy.sh
fi
```

Schedule via Hermes cron:
```bash
cronjob(action='create', schedule='every 15m', script='auto-deploy.sh', no_agent=True)
```

## Related Skills

- `samaya-factory-deploy` — Hostinger-specific deploy commands, paths, and permissions
- `web-deployment` — general static site deployment (Surge, SSH, SCP)
- `github` — general GitHub workflow (PRs, issues, auth)

## Reference Files

- `references/self-hosted-runner-macos.md` — full installation transcript with troubleshooting
