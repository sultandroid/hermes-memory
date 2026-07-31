#!/bin/bash
# hub_health_check.sh — daily pre-sync health check for the hermes-memory hub
# Runs: 10:00 Cairo daily (before memory_skills_exchange.sh)
# On failure: exit 1 + Telegram alert via hermes_notify.sh
# On success: write .last_sync, exit 0

set -uo pipefail

# ─── Locate hub via git, not $HOME (cron has different $HOME) ───
HUB_DIR="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$HUB_DIR" ]; then
    # Fall back to scanning likely locations
    for candidate in \
        "$HOME/hermes-memory" \
        "$HOME/.hermes/profiles/$(basename "${HOME:-/root}")/home/hermes-memory" \
        "/home/hermes/hermes-memory" \
        "/home/hermes/.hermes/profiles/digitalhermes/home/hermes-memory"; do
        if [ -d "$candidate/.git" ]; then HUB_DIR="$candidate"; break; fi
    done
fi
[ -z "$HUB_DIR" ] && { echo "FATAL: cannot locate hermes-memory hub (no git repo found)"; exit 2; }

# ─── Locate hermes_notify.sh (path varies by install) ───
NOTIFY=""
for n in \
    "$HOME/.hermes/profiles/$(basename "${HOME:-/root}")/home/hermes-memory/scripts/hermes_notify.sh" \
    "$HOME/.hermes/profiles/digitalhermes/home/hermes-memory/scripts/hermes_notify.sh" \
    "$HOME/.hermes/scripts/hermes_notify.sh" \
    "/home/hermes/.hermes/profiles/digitalhermes/home/hermes-memory/scripts/hermes_notify.sh" \
    "$HUB_DIR/scripts/hermes_notify.sh"; do
    [ -x "$n" ] && NOTIFY="$n" && break
done

# ─── Locate Hermes skills home (also varies by profile) ───
HERMES_SKILLS=""
for p in \
    "$HOME/.hermes/profiles/$(basename "${HOME:-/root}")/home/.hermes/skills" \
    "$HOME/.hermes/profiles/digitalhermes/home/.hermes/skills" \
    "$HOME/.hermes/skills"; do
    [ -d "$p" ] && HERMES_SKILLS="$p" && break
done

STATE_FILE="$HUB_DIR/.last_sync"
LOG="$HUB_DIR/.hub_health.log"

mkdir -p "$HUB_DIR"
: > "$LOG"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }
fail() { log "FAIL: $*"; FAIL=1; }
ok()   { log "OK:   $*"; }

FAIL=0

# ─── 1. Hub reachable + clean ───
log "=== Hub health check (hub: $HUB_DIR) ==="
cd "$HUB_DIR" || fail "Cannot cd to hub"
if git pull --no-rebase --ff-only origin main >>"$LOG" 2>&1; then
    ok "Hub pulled clean"
else
    fail "git pull failed (likely conflict or offline)"
fi
if git diff --quiet && git diff --cached --quiet; then
    ok "Working tree clean"
else
    log "WARN: uncommitted local changes (will be stashed by sync engine)"
fi

# ─── 2. Top-level memory files present ───
for f in USER.md RULES.md MEMORY.md PROJECTS.md AGENTS.md CONTACTS.md ODOO.md; do
    if [ -f "$HUB_DIR/$f" ]; then
        ok "Found $f"
    else
        fail "MISSING top-level file: $f"
    fi
done

# ─── 3. Unified memory exists and is recent ───
UM="$HUB_DIR/unified/UNIFIED_MEMORY.md"
if [ -f "$UM" ]; then
    age_days=$(( ( $(date +%s) - $(stat -c %Y "$UM" 2>/dev/null || echo $(date +%s)) ) / 86400 ))
    if [ "$age_days" -gt 7 ]; then
        log "WARN: UNIFIED_MEMORY.md is $age_days days old (>7)"
    else
        ok "UNIFIED_MEMORY.md age: $age_days days"
    fi
else
    fail "Missing unified/UNIFIED_MEMORY.md"
fi

# ─── 4. No unresolved conflict markers ───
# Match git conflict markers ONLY at start of line (^<<<<<<<, ^=======, ^>>>>>>>)
conflicts_found=$(grep -rEln '^<<<<<<< |^=======$|^>>>>>>> ' "$HUB_DIR" --include='*.md' 2>/dev/null || true)
if [ -n "$conflicts_found" ]; then
    fail "Unresolved git conflict markers in: $conflicts_found"
else
    ok "No conflict markers"
fi

# ─── 5. sync_conflicts.md queue state ───
SC="$HUB_DIR/sync_conflicts.md"
if [ -f "$SC" ] && [ -s "$SC" ]; then
    # Count real entries under ## Pending (skip the template placeholder under "## Resolved" / header)
    in_pending=0
    unaddressed=0
    while IFS= read -r line; do
        case "$line" in
            "## Pending") in_pending=1; continue ;;
            "## Resolved") in_pending=0; continue ;;
        esac
        if [ "$in_pending" = 1 ] && echo "$line" | grep -qE '^\s*-\s*\[ \]\s+\S'; then
            unaddressed=$((unaddressed + 1))
        fi
    done < "$SC"
    if [ "$unaddressed" -gt 0 ]; then
        fail "sync_conflicts.md has $unaddressed unaddressed conflict(s) under ## Pending"
    else
        ok "sync_conflicts.md present (no open entries under ## Pending)"
    fi
else
    ok "No sync_conflicts.md (clean state)"
fi

# ─── 6. Agent skills homes reachable ───
# Hermes skills is special — it lives at ~/.hermes/profiles/<active>/skills/ (sibling of home/)
# not under home/. Resolve by looking at what the sync engine actually reads from
if [ -z "$HERMES_SKILLS" ]; then
    for p in \
        "$HOME/.hermes/skills" \
        "$(dirname "$HUB_DIR")/../skills" \
        "/home/hermes/.hermes/profiles/digitalhermes/skills" \
        "/home/hermes/.hermes/profiles/$(basename "${HOME:-root}")/skills"; do
        [ -d "$p" ] && HERMES_SKILLS="$p" && break
    done
fi

AGENTS=(
    "hermes:${HERMES_SKILLS:-/home/hermes/.hermes/profiles/digitalhermes/skills}"
    "claude:$HOME/.claude/skills"
    "codex:$HOME/.codex/skills"
    "kimi:$HOME/.kimi/skills"
    "pi:$HOME/.pi/agent/skills"
    "gemini:$HOME/.gemini/antigravity/skills"
    "openclaw:$HOME/.openclaw/workspace/skills"
    "grok:$HOME/.grok/skills"
    "kilo:$HOME/.kilo/skills"
)
for entry in "${AGENTS[@]}"; do
    name="${entry%%:*}"
    path="${entry#*:}"
    if [ -d "$path" ]; then
        count=$(find "$path" -name 'SKILL.md' 2>/dev/null | wc -l | tr -d ' ')
        ok "Agent $name: $count skills at $path"
    else
        log "INFO: Agent $name skills dir not present at $path (ok if not installed)"
    fi
done

# ─── 7. Last sync recency ───
if [ -f "$STATE_FILE" ]; then
    last=$(cat "$STATE_FILE")
    last_epoch=$(date -d "$last" +%s 2>/dev/null || echo 0)
    if [ "$last_epoch" -gt 0 ]; then
        age_hours=$(( ( $(date +%s) - last_epoch ) / 3600 ))
        if [ "$age_hours" -gt 26 ]; then
            fail "Last sync $age_hours hours ago (>26h)"
        else
            ok "Last sync $age_hours hours ago"
        fi
    else
        log "WARN: .last_sync present but unparseable: $last"
    fi
else
    log "INFO: no .last_sync yet (first run)"
fi

# ─── 8. Cron job present (best-effort) ───
if crontab -l 2>/dev/null | grep -q 'hub_health_check\|memory_github_sync\|memory_skills_exchange'; then
    ok "Cron job for hub sync present"
else
    log "WARN: no hub-sync cron job found in crontab (will be installed)"
fi

# ─── 9. Telegram notify reachability ───
if [ -n "$NOTIFY" ] && [ -x "$NOTIFY" ]; then
    ok "hermes_notify.sh: $NOTIFY"
else
    log "INFO: hermes_notify.sh not found or not executable (alerts disabled)"
fi

# ─── Result ───
echo "" | tee -a "$LOG"
if [ "$FAIL" -eq 0 ]; then
    log "=== HEALTHY ==="
    date '+%Y-%m-%d %H:%M:%S' > "$STATE_FILE"
    exit 0
else
    log "=== UNHEALTHY — sending alert ==="
    if [ -n "$NOTIFY" ] && [ -x "$NOTIFY" ]; then
        "$NOTIFY" telegram "⚠️ Hub health check FAILED on $(hostname). See $LOG" || log "alert send failed"
    fi
    exit 1
fi
