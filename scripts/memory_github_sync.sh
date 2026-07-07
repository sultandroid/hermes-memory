#!/bin/bash
# Memory + Skills Sync to GitHub — runs every 2 hours
set -euo pipefail

REPO="$HOME/hermes-memory"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "============================================"
echo "Memory + Skills Sync to GitHub — $TIMESTAMP"
echo "============================================"

# 1. Pull latest (avoid conflicts)
cd "$REPO"
git pull --rebase origin main 2>/dev/null || echo "Nothing to pull"

# 2. Update MEMORY.md from Hermes
cp "$HOME/.hermes/memories/MEMORY.md" "$REPO/MEMORY.md" 2>/dev/null || echo "No MEMORY.md"
cp "$HOME/.hermes/memories/USER.md" "$REPO/USER.md" 2>/dev/null || echo "No USER.md"

# 3. Run exchange script to update UNIFIED_MEMORY.md
if [ -f "$HOME/.hermes/scripts/memory_skills_exchange.sh" ]; then
    bash "$HOME/.hermes/scripts/memory_skills_exchange.sh" 2>/dev/null || true
    if [ -f "$HOME/.hermes/shared_exchange/UNIFIED_MEMORY.md" ]; then
        mkdir -p "$REPO/unified"
        cp "$HOME/.hermes/shared_exchange/UNIFIED_MEMORY.md" "$REPO/unified/UNIFIED_MEMORY.md"
    fi
fi

# 4. Sync ODOO.md if reference updated
if [ -f "$HOME/.hermes/hermes-agent/samaya_odoo_hermes_setup.md" ]; then
    cp "$HOME/.hermes/hermes-agent/samaya_odoo_hermes_setup.md" "$REPO/ODOO_FULL.md" 2>/dev/null || true
fi
if [ -f "$HOME/.hermes/hermes-agent/samaya_projects_reference.md" ]; then
    cp "$HOME/.hermes/hermes-agent/samaya_projects_reference.md" "$REPO/PROJECTS_FULL.md" 2>/dev/null || true
fi

# 5. Sync ALL skills to GitHub repo
echo "Syncing skills..."
mkdir -p "$REPO/skills"
rsync -a --delete "$HOME/.hermes/skills/" "$REPO/skills/" 2>/dev/null || cp -R "$HOME/.hermes/skills/" "$REPO/skills/" 2>/dev/null

# 6. Sync scripts
echo "Syncing scripts..."
mkdir -p "$REPO/scripts"
rsync -a --delete "$HOME/.hermes/scripts/" "$REPO/scripts/" 2>/dev/null || cp -R "$HOME/.hermes/scripts/" "$REPO/scripts/" 2>/dev/null

# 7. Commit and push
cd "$REPO"
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to commit"
else
    git add -A
    git commit -m "Auto-sync $TIMESTAMP"
    git push origin main
    echo "✅ Memory + Skills synced to GitHub"
fi

echo "============================================"
