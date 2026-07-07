# GitHub Memory Sync — Full Setup Guide

> Set up automatic memory syncing from Hermes to GitHub for multi-agent, multi-device sharing.

## Prerequisites

- GitHub account with `gh` CLI authenticated (`gh auth status`)
- Hermes agent running on the device
- Git configured: `git config --global user.name "..." && git config --global user.email "..."`

## Step 1: Create the Repo (one-time)

```bash
# Create the repo structure
mkdir -p /tmp/hermes-memory && cd /tmp/hermes-memory
git init

# Add core memory files
cp ~/.hermes/memories/MEMORY.md .
cp ~/.hermes/memories/USER.md .
cp ~/.hermes/scripts/memory_skills_exchange.sh scripts/memory_exchange.sh && chmod +x scripts/memory_exchange.sh

# Create .gitignore
echo -e "ODOO_CREDENTIALS.md\n.gitignore\n.DS_Store" > .gitignore

# Push
git add -A && git commit -m "Initial commit"
gh repo create <repo-name> --public --push --source=.
```

## Step 2: Create the Sync Script

Location: `~/.hermes/scripts/memory_github_sync.sh`

```bash
#!/bin/bash
set -euo pipefail

REPO="$HOME/hermes-memory"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

cd "$REPO"
git pull --rebase origin main 2>/dev/null || true

# Update memory files
cp "$HOME/.hermes/memories/MEMORY.md" "$REPO/MEMORY.md"
cp "$HOME/.hermes/memories/USER.md" "$REPO/USER.md"

# Run exchange script for multi-agent sync
if [ -f "$HOME/.hermes/scripts/memory_skills_exchange.sh" ]; then
    bash "$HOME/.hermes/scripts/memory_skills_exchange.sh" 2>/dev/null || true
    if [ -f "$HOME/.hermes/shared_exchange/UNIFIED_MEMORY.md" ]; then
        mkdir -p "$REPO/unified"
        cp "$HOME/.hermes/shared_exchange/UNIFIED_MEMORY.md" "$REPO/unified/UNIFIED_MEMORY.md"
    fi
fi

# Sync full reference files (if they exist)
for f in ODOO_FULL.md PROJECTS_FULL.md; do
    [ -f "$HOME/.hermes/hermes-agent/samaya_${f%_FULL.md}_reference.md" ] && \
        cp "$HOME/.hermes/hermes-agent/samaya_${f%_FULL.md}_reference.md" "$REPO/$f"
done

if git diff --quiet && git diff --cached --quiet; then
    echo "No changes"
else
    git add -A && git commit -m "Auto-sync $TIMESTAMP" && git push origin main
fi
```

## Step 3: Create the Cron Job

```bash
chmod +x ~/.hermes/scripts/memory_github_sync.sh
```

Then call `cronjob(action='create', script='memory_github_sync.sh', schedule='every 2h', no_agent=True, name='Memory GitHub Sync')`

## Step 4: Clone on Another Device

```bash
git clone https://github.com/<user>/<repo>.git ~/hermes-memory
cp ~/hermes-memory/MEMORY.md ~/.hermes/memories/MEMORY.md
cp ~/hermes-memory/USER.md ~/.hermes/memories/USER.md
# Repeat Step 3 on this device if it has agents to sync
```

## Verification

```bash
# Check last sync
cd ~/hermes-memory && git log --oneline -3

# Run manually
bash ~/.hermes/scripts/memory_github_sync.sh

# List cron jobs
cronjob(action='list')
```
