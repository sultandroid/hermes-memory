#!/bin/bash
# Memory & Skills Exchange — All Labors Sync
# Runs: every 6 hours via cronjob
# Purpose: Exchange memory and skills between Hermes, Pi, Claude Code, Codex, Kimi, Gemini, OpenClaw, Grok

set -euo pipefail

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
SHARED_DIR="$HOME/.hermes/shared_exchange"
mkdir -p "$SHARED_DIR"

echo "============================================"
echo "Memory & Skills Exchange — $TIMESTAMP"
echo "============================================"

# ─── 1. COLLECT SKILLS FROM ALL AGENTS ───
echo ""
echo "─── Step 1: Collect Skills ───"

collect_skills() {
    local agent="$1" src="$2"
    local dst="$SHARED_DIR/skills/$agent"
    mkdir -p "$dst"
    if [ -d "$src" ]; then
        mkdir -p "$dst"
        rsync -a --delete "$src/" "$dst/" 2>/dev/null
        count=$(find "$dst" -type f -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
        echo "  ✓ $agent: $count skills collected → $dst"
    else
        echo "  ✗ $agent: no skills directory at $src"
    fi
}

collect_skills "hermes" "$HOME/.hermes/skills"
collect_skills "claude" "$HOME/.claude/skills"
collect_skills "codex"  "$HOME/.codex/skills"
collect_skills "kimi"   "$HOME/.kimi/skills"
collect_skills "pi"     "$HOME/.pi/agent/skills"
collect_skills "gemini" "$HOME/.gemini/antigravity/skills"
collect_skills "openclaw" "$HOME/.openclaw/workspace/skills"
collect_skills "grok"   "$HOME/.grok/skills"

# ─── 2. BUILD CONSOLIDATED SKILL INDEX ───
echo ""
echo "─── Step 2: Build Shared Skill Index ───"

SKILL_INDEX="$SHARED_DIR/SKILL_INDEX.md"
printf "# Shared Skill Index — All Labors\nGenerated: %s\n\n## Skills by Agent\n\n" "$TIMESTAMP" > "$SKILL_INDEX"

for agent in hermes claude codex kimi pi gemini openclaw grok; do
    agent_dir="$SHARED_DIR/skills/$agent"
    if [ -d "$agent_dir" ]; then
        printf "### %s\n" "$agent" >> "$SKILL_INDEX"
        find "$agent_dir" -name "SKILL.md" -maxdepth 3 | while read -r skill_file; do
            rel_path="${skill_file#$agent_dir/}"
            category=$(dirname "$rel_path")
            desc=$(grep -m1 "^description:" "$skill_file" 2>/dev/null | sed 's/description: "//;s/"$//')
            printf -- "- **%s** — %s\n" "${category}" "${desc:-No description}" >> "$SKILL_INDEX"
        done
        printf "\n" >> "$SKILL_INDEX"
    fi
done

total_skills=$(find "$SHARED_DIR/skills" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
echo "  ✓ Skill index built: $SKILL_INDEX ($total_skills total skills)"

# ─── 3. COLLECT MEMORY FROM ALL AGENTS ───
echo ""
echo "─── Step 3: Collect Memory ───"

MEMORY_COLLECTION="$SHARED_DIR/MEMORY_COLLECTION.md"
printf "# Memory Collection — All Labors\nGenerated: %s\n\n" "$TIMESTAMP" > "$MEMORY_COLLECTION"

# Helper: append file to collection
append_memory() {
    local label="$1" file="$2" max_lines="${3:-0}"
    if [ -f "$file" ]; then
        printf "\n## %s\n\n" "$label" >> "$MEMORY_COLLECTION"
        if [ "$max_lines" -gt 0 ]; then
            head -"$max_lines" "$file" >> "$MEMORY_COLLECTION"
        else
            cat "$file" >> "$MEMORY_COLLECTION"
        fi
        printf "\n" >> "$MEMORY_COLLECTION"
        echo "  ✓ $label collected"
    fi
}

append_memory "Hermes MEMORY.md" "$HOME/.hermes/memories/MEMORY.md"
append_memory "Hermes USER.md" "$HOME/.hermes/memories/USER.md"
append_memory "Codex memory_summary.md" "$HOME/.codex/memories/memory_summary.md" 100
append_memory "Codex raw_memories.md" "$HOME/.codex/memories/raw_memories.md" 100
append_memory "Codex MEMORY.md" "$HOME/.codex/memories/MEMORY.md" 100
append_memory "Kimi MEMORY.md" "$HOME/.kimi/memories/MEMORY.md"
append_memory "Kimi USER.md" "$HOME/.kimi/memories/USER.md"
append_memory "Kimi HERMES_SOUL.md" "$HOME/.kimi/memories/HERMES_SOUL.md"
append_memory "Pi Agent AGENTS.md" "$HOME/.pi/agent/AGENTS.md" 200
append_memory "Claude Code CLAUDE.md" "$HOME/.claude/CLAUDE.md" 100
append_memory "Gemini GEMINI.md" "$HOME/.gemini/GEMINI.md"
append_memory "OpenClaw MEMORY.md" "$HOME/.openclaw/workspace/MEMORY.md"
append_memory "OpenClaw USER.md" "$HOME/.openclaw/workspace/USER.md"
append_memory "OpenClaw AGENTS.md" "$HOME/.openclaw/workspace/AGENTS.md" 200
append_memory "Grok MEMORY.md" "$HOME/.grok/memory/MEMORY.md"

echo "  ✓ Total memory collection: $(wc -c < "$MEMORY_COLLECTION") bytes"

# ─── 4. GENERATE UNIFIED MEMORY ───
echo ""
echo "─── Step 4: Generate Unified Memory ───"

UNIFIED="$SHARED_DIR/UNIFIED_MEMORY.md"
# Write header directly
cat > "$UNIFIED" << 'HEADEREOF'
# Unified Agent Knowledge Base — Mohamed Essa
# Auto-synced by Memory & Skills Exchange Cronjob
# DO NOT EDIT — Regenerated every 6 hours

HEADEREOF
echo "Generated: $TIMESTAMP" >> "$UNIFIED"
echo "" >> "$UNIFIED"
echo "---" >> "$UNIFIED"
echo "" >> "$UNIFIED"

# Extract key facts from collection — write to temp file first to avoid printf issues
TEMP_FACTS=$(mktemp)
    echo "## User Profile" >> "$UNIFIED"
    echo "" >> "$UNIFIED"
    grep -hE "^Mohamed Essa|^\*\*Mohamed Essa|^Mohamed Sultan" "$MEMORY_COLLECTION" 2>/dev/null | head -5 > "$TEMP_FACTS" || true
    if [ -s "$TEMP_FACTS" ]; then cat "$TEMP_FACTS" >> "$UNIFIED"; else echo "(data in collection)" >> "$UNIFIED"; fi

    echo "" >> "$UNIFIED"
    echo "## Critical Rules" >> "$UNIFIED"
    echo "" >> "$UNIFIED"
    grep -ihE "ALWAYS |CRITICAL|NEVER|ENTITY ISOLATION|zero-tolerance|FIRM RULE|MANDATORY" "$MEMORY_COLLECTION" 2>/dev/null | grep -v "^#" > "$TEMP_FACTS" || true
    if [ -s "$TEMP_FACTS" ]; then cat "$TEMP_FACTS" | head -20 >> "$UNIFIED"; else echo "(data in collection)" >> "$UNIFIED"; fi

    echo "" >> "$UNIFIED"
    echo "## Active Projects" >> "$UNIFIED"
    echo "" >> "$UNIFIED"
    grep -ihE "Aseer|Zamzam|Moqtana|Samaya" "$MEMORY_COLLECTION" 2>/dev/null | grep -v "^#" | grep -v "^$" > "$TEMP_FACTS" || true
    if [ -s "$TEMP_FACTS" ]; then cat "$TEMP_FACTS" | head -20 >> "$UNIFIED"; else echo "(data in collection)" >> "$UNIFIED"; fi

    echo "" >> "$UNIFIED"
    echo "## Key People" >> "$UNIFIED"
    echo "" >> "$UNIFIED"
    grep -ihE "Director|Manager|Engineer|Lead|Coordinator|Consultant|PM " "$MEMORY_COLLECTION" 2>/dev/null | grep -v "^#" | grep -v "^$" > "$TEMP_FACTS" || true
    if [ -s "$TEMP_FACTS" ]; then cat "$TEMP_FACTS" | head -20 >> "$UNIFIED"; else echo "(data in collection)" >> "$UNIFIED"; fi

    echo "" >> "$UNIFIED"
    echo "## Agents & Tools" >> "$UNIFIED"
    echo "" >> "$UNIFIED"
    grep -ihE "claude|codex|kimi|kilo|pi agent|hermes|openclaw|odoo|notion|aconex|telegram" "$MEMORY_COLLECTION" 2>/dev/null | grep -v "^#" | grep -v "^$" > "$TEMP_FACTS" || true
    if [ -s "$TEMP_FACTS" ]; then cat "$TEMP_FACTS" | head -20 >> "$UNIFIED"; else echo "(data in collection)" >> "$UNIFIED"; fi

    echo "" >> "$UNIFIED"
    echo "## Contracts & Documents" >> "$UNIFIED"
    echo "" >> "$UNIFIED"
    grep -ihE "contract|invoice|NRS|MoC|PMC|CG|BOQ|RFP|DMP|RIBA|IFC|NOC" "$MEMORY_COLLECTION" 2>/dev/null | grep -v "^#" | grep -v "^$" > "$TEMP_FACTS" || true
    if [ -s "$TEMP_FACTS" ]; then cat "$TEMP_FACTS" | head -30 >> "$UNIFIED"; else echo "(data in collection)" >> "$UNIFIED"; fi

    echo "" >> "$UNIFIED"
    echo "## Locations" >> "$UNIFIED"
    echo "" >> "$UNIFIED"
    grep -ihE "OneDrive|Library|Documents|\\.hermes|\\.codex|\\.claude|\\.kimi|\\.kilo|\\.pi|\\.openclaw" "$MEMORY_COLLECTION" 2>/dev/null | grep -v "^#" | grep -v "^$" > "$TEMP_FACTS" || true
    if [ -s "$TEMP_FACTS" ]; then cat "$TEMP_FACTS" | head -15 >> "$UNIFIED"; else echo "(data in collection)" >> "$UNIFIED"; fi

    rm -f "$TEMP_FACTS"

echo "  ✓ Unified memory built: $UNIFIED ($(wc -c < "$UNIFIED") bytes)"

# ─── 5. DISTRIBUTE BACK TO EACH AGENT ───
echo ""
echo "─── Step 5: Distribute to Agents ───"

# Claude Code — write unified memory to a SEPARATE file. NEVER append to CLAUDE.md.
# CLAUDE.md is loaded into context every session; the previous append logic had a
# broken dedup (the injected dump contains many "## " headings, so the awk reset its
# flag on the first one and only ever deleted the 2-line header), causing unbounded
# growth — 27 stacked dumps / 410 KB. Overwrite a standalone file instead, mirroring
# how Codex/Kimi receive unified_exchange_memory.md.
mkdir -p "$HOME/.claude"
cp "$UNIFIED" "$HOME/.claude/UNIFIED_EXCHANGE_MEMORY.md"
echo "  ✓ Claude Code: UNIFIED_EXCHANGE_MEMORY.md written (separate file, not CLAUDE.md)"

# Codex — write unified memory
cp "$UNIFIED" "$HOME/.codex/memories/unified_exchange_memory.md"
echo "  ✓ Codex: unified_exchange_memory.md written"

# Kimi — write unified memory
cp "$UNIFIED" "$HOME/.kimi/memories/unified_exchange_memory.md"
echo "  ✓ Kimi: unified_exchange_memory.md written"

# Pi Agent — write memory collection
cp "$MEMORY_COLLECTION" "$HOME/.pi/agent/memory_collection.md"
echo "  ✓ Pi Agent: memory_collection.md written"

# Gemini / Antigravity — write unified memory and memories
mkdir -p "$HOME/.gemini/antigravity/memories"
cp "$UNIFIED" "$HOME/.gemini/antigravity/memories/unified_exchange_memory.md"
if [ -f "$HOME/.hermes/memories/MEMORY.md" ]; then
    cp "$HOME/.hermes/memories/MEMORY.md" "$HOME/.gemini/antigravity/memories/MEMORY.md"
fi
if [ -f "$HOME/.hermes/memories/USER.md" ]; then
    cp "$HOME/.hermes/memories/USER.md" "$HOME/.gemini/antigravity/memories/USER.md"
fi
cp "$UNIFIED" "$HOME/.gemini/GEMINI.md"
echo "  ✓ Gemini: memories updated"

# Hermes — memory collection stored in shared dir (Hermes reads from shared_exchange)
echo "  ✓ Hermes: memory available at $SHARED_DIR"

# OpenClaw — write unified memory to workspace
cp "$UNIFIED" "$HOME/.openclaw/workspace/unified_exchange_memory.md"
if [ -f "$HOME/.hermes/memories/MEMORY.md" ]; then
    cp "$HOME/.hermes/memories/MEMORY.md" "$HOME/.openclaw/workspace/HERMES_MEMORY.md"
fi
if [ -f "$HOME/.hermes/memories/USER.md" ]; then
    cp "$HOME/.hermes/memories/USER.md" "$HOME/.openclaw/workspace/HERMES_USER.md"
fi
echo "  ✓ OpenClaw: unified memory written to workspace"

# Grok — write unified memory to its global MEMORY.md
mkdir -p "$HOME/.grok/memory"
cp "$UNIFIED" "$HOME/.grok/memory/UNIFIED_EXCHANGE_MEMORY.md"
if [ -f "$HOME/.hermes/memories/MEMORY.md" ]; then
    cp "$HOME/.hermes/memories/MEMORY.md" "$HOME/.grok/memory/HERMES_MEMORY.md"
fi
if [ -f "$HOME/.hermes/memories/USER.md" ]; then
    cp "$HOME/.hermes/memories/USER.md" "$HOME/.grok/memory/HERMES_USER.md"
fi
echo "  ✓ Grok: unified memory written to ~/.grok/memory/"

# ─── 6. SUMMARY ───
echo ""
echo "─── Exchange Summary ───"
echo ""
for agent in hermes claude codex kimi pi gemini openclaw grok; do
    count=$(find "$SHARED_DIR/skills/$agent" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
    echo "  $agent: $count skills"
done
echo ""
echo "  Memory collected: $(wc -c < "$MEMORY_COLLECTION") bytes"
echo "  Unified memory:  $(wc -c < "$UNIFIED") bytes"
echo "  Skills total:    $total_skills"
echo ""
echo "============================================"
echo "Exchange Complete — $TIMESTAMP"
echo "============================================"
