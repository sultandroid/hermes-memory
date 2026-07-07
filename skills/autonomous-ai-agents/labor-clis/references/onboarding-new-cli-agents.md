# Onboarding New CLI Agents into Labor Army

When a new CLI agent is installed on the system (e.g., Pi Agent, a new AI coding assistant), this workflow integrates it as a deployable labor in the army.

## Steps

### 1. Detect and verify the installation

```bash
which <agent-name>
<agent-name> --help          # shows available commands
<agent-name> --version       # version check
```

Check how it was installed (npm, brew, pip, etc.):
```bash
npm list -g | grep <agent>   # npm global
brew list | grep <agent>     # homebrew
pip list | grep <agent>      # python
```

### 2. Identify the correct binary path

Node.js tools installed via `npm -g` have symlinks in `~/.npm-global/bin/`. Python tools in `~/.local/bin/` or a venv. Find the real path:

```bash
ls -la $(which <agent>)
# → lrwxr-xr-x ... -> ../lib/node_modules/@scope/package/dist/cli.js
```

### 3. Check default provider/model config

```bash
cat ~/.<agent>/config.json 2>/dev/null || cat ~/.config/<agent>/*.yaml 2>/dev/null
```

Note the default provider so print-mode invocations use the right one.

### 4. Determine print/non-interactive mode

Test print mode:

```bash
echo "Test task: list files in /tmp" | <agent> -p "Test task" 2>&1
```

If `-p` flag doesn't exist, try `--print`, `--quiet`, or stdin pipe equivalents.

### 5. Create/update AGENTS.md (the agent's persistent context file)

Each CLI agent has its own persistent context file (analogous to CLAUDE.md or AGENTS.md):

- **Claude Code**: `~/Library/Application Support/Claude/claude.md` (global) or `PROJECT_ROOT/CLAUDE.md` (local)
- **Codex**: `~/Library/Application Support/Codex/codex.md` (or project `.codexcontext.md`)
- **Pi Agent**: `~/.pi/agent/AGENTS.md`
- **Kimi**: `~/.config/kimi/context.md` (varies by version)
- **Gemini**: `~/.config/gemini/context.md`

The context file should contain:
- User profile (name, role, communication style)
- Projects and entities
- Available labor CLIs (so it knows its army)
- Workflow pipeline
- Critical rules (entity isolation, 3-perspective reporting, labor naming)
- Infrastructure access (OneDrive paths, Odoo credentials location)

**If the file already has comprehensive context**, add only the Commander Role section defining it as orchestrator and listing its deployable labors.

### 6. Create briefing file for direct instruction

For first-time onboarding via print mode:

```bash
cat /path/to/briefing.md | <agent> -p "Read this briefing and confirm understanding. List: 1) Your role, 2) Available labors, 3) Key rules" --name "Onboarding Session"
```

The briefing file should cover at a minimum:
- The agent's role (worker vs commander)
- Available labors to delegate to
- Default workflow pipeline
- Key reporting rules
- Entity isolation rules

### 7. Update the labor-clis skill

Once verified:
- Add the new labor to the Available Labors table in `labor-clis/SKILL.md`
- Write the invocation pattern
- Save to memory as an available labor CLI

## Verification Checklist

After onboarding, the agent should be able to answer:
- [ ] Its role (worker vs commander)
- [ ] Names of all labor CLIs it can use
- [ ] The default workflow pipeline
- [ ] The 3-perspective reporting rule
- [ ] The entity isolation rule
