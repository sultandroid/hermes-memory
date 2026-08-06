# Self-Hosted GitHub Actions Runner (macOS)

## When to Use

When GitHub Actions workflows fail to deploy to shared hosting (Hostinger, cPanel) on non-standard SSH ports because GitHub-hosted runners cannot reach the server. The fix is a self-hosted runner on the local MacBook.

## Root Cause

GitHub Actions runners (ubuntu-latest, macos-latest) cannot reach `samaya-factory.com:65002` — the non-standard SSH port is blocked by GitHub's egress or Hostinger's firewall. The deploy workflow uses `runs-on: [self-hosted, macbook]` but no runner was registered.

## Installation (macOS, Apple Silicon)

```bash
# 1. Get registration token (expires in 60 min)
TOKEN=$(curl -s -L -X POST \
  -H "Authorization: token $(gh auth token)" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/runners/registration-token" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# 2. Download and extract
mkdir -p ~/actions-runner && cd ~/actions-runner
curl -o actions-runner-osx-arm64-2.322.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.322.0/actions-runner-osx-arm64-2.322.0.tar.gz
tar xzf actions-runner-osx-arm64-2.322.0.tar.gz

# 3. Configure (unattended mode)
./config.sh --url https://github.com/$OWNER/$REPO \
  --token "$TOKEN" \
  --name "sultan-macbook" \
  --labels "macbook,osx-arm64" \
  --work _work \
  --unattended

# 4. Install as LaunchAgent (user-level, no sudo)
./svc.sh install $USER

# 5. Start
./svc.sh start
```

## Verification

```bash
gh api repos/$OWNER/$REPO/actions/runners --jq '.runners[] | {name, status, labels}'
# Expected: status = "online"
```

## Workflow YAML

The deploy workflow must use matching labels:

```yaml
jobs:
  deploy:
    runs-on: [self-hosted, macbook]
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: ./deploy.sh
```

## Pitfalls

- **Token expires in 60 min** — generate fresh before each `config.sh` call
- **LaunchAgent vs sudo** — `./svc.sh install $USER` creates user-level LaunchAgent at `~/Library/LaunchAgents/actions.runner.*.plist`. No password needed. Use `sudo ./svc.sh install` only for system-level daemon.
- **Runner offline after reboot** — LaunchAgent starts on login only. If Mac reboots without login, runner stays offline. Configure auto-login or use system daemon.
- **Labels must match exactly** — workflow `runs-on` labels must match runner labels. Mismatch = runner never picked up.
- **Multiple repos** — each repo needs its own runner directory. Use `--name` to distinguish.
- **SSH still works from this Mac** — the self-hosted runner runs on the same machine that has SSH keys configured for Hostinger. Verify with `ssh -p 65002 -o ConnectTimeout=5 u517606786@samaya-factory.com "echo OK"` before assuming the runner can deploy.
