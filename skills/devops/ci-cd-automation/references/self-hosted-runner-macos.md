# Self-Hosted GitHub Actions Runner on macOS (Apple Silicon)

Install a self-hosted runner on macOS (osx-arm64) so GitHub Actions workflows can access local resources (SSH to Hostinger, local files, etc.).

## When to Use

- GitHub Actions workflows need to SSH to a server on a non-standard port (e.g. `samaya-factory.com:65002`)
- Workflows need access to local files or tools not available on GitHub-hosted runners
- The workflow's `runs-on` specifies `[self-hosted, macbook]` or similar custom labels

## Installation

### 1. Get a registration token

```bash
curl -s -L -X POST \
  -H "Authorization: token $(gh auth token)" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/OWNER/REPO/actions/runners/registration-token"
```

### 2. Download and configure

```bash
mkdir -p ~/actions-runner && cd ~/actions-runner
curl -o actions-runner-osx-arm64-2.322.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.322.0/actions-runner-osx-arm64-2.322.0.tar.gz
tar xzf actions-runner-osx-arm64-2.322.0.tar.gz

./config.sh --url https://github.com/OWNER/REPO \
  --token <TOKEN> \
  --name "sultan-macbook" \
  --labels "macbook,osx-arm64" \
  --work _work \
  --unattended
```

### 3. Install as a launch agent (auto-start on boot)

```bash
# As current user (no sudo needed):
./svc.sh install mohamedessa
./svc.sh start
```

### 4. Verify

```bash
gh api repos/OWNER/REPO/actions/runners --jq '.runners[] | {name, status, labels}'
# Expected: status="online", labels include "self-hosted", "macOS", "ARM64", "macbook", "osx-arm64"
```

## Workflow YAML

The workflow must use matching labels:

```yaml
jobs:
  deploy:
    runs-on: [self-hosted, macbook]
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh
```

## Pitfalls

- **Token expires in ~1 hour** — the registration token from the API is short-lived. Generate it immediately before `config.sh`.
- **`sudo ./svc.sh install` fails on macOS** — macOS requires a user-level launch agent, not a system service. Use `./svc.sh install <username>` instead.
- **Runner stays "offline" for a few seconds** after `svc.sh start`. Poll the API after 3-5 seconds.
- **Labels must match exactly** — the workflow's `runs-on` labels must match the runner's configured labels. `[self-hosted, macbook]` matches a runner with both `self-hosted` (built-in) and `macbook` (custom) labels.
- **The runner runs as the user who installed it** — it has access to that user's SSH keys, config files, and credentials. This is intentional (enables SSH deploys) but means any workflow on this repo can access those credentials.
- **LaunchAgent persists across reboots** — auto-starts on user login. No need to re-run install after reboot.
- **Runner logs** — check `~/Library/Logs/actions.runner.<org>-<repo>.<name>/` for diagnostics.
