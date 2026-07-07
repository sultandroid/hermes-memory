---
name: hermes-profiles
description: "Manage and troubleshoot Hermes Agent profiles — creation, diagnostics, config repair, switching, and verification."
version: 1.0.0
created_by: agent
---

# Hermes Profiles

Use when a Hermes profile is broken (missing config, won't load, doctor flags it), when setting up a new profile, or when switching/routing between profiles.

## Profile structure

Hermes profiles live in `~/.hermes/profiles/<name>/`. The `default` profile is an exception — it lives at the root `~/.hermes/` itself, not in `profiles/default/`.

Each profile directory contains:
- `config.yaml` — REQUIRED. Full Hermes config. Without it the profile won't initialize.
- `.env` — API keys and secrets.
- `SOUL.md` — Personality prompt.
- `profile.yaml` — Metadata (description, auto flag).
- `skills/` — Profile-specific skills.
- `memories/` — Profile-specific memory files.
- `sessions/` — Profile session store (state.db).
- `cron/`, `logs/`, `plans/`, `workspace/` — Subdirectories.

## Diagnostics

Run these first when a profile doesn't work:

```bash
# Check profile list and state
hermes profile list

# Show profile details
hermes profile show <name>

# Full system health check (reports missing config, migration needed)
hermes doctor

# Auto-fix what's possible (config migration, missing dirs)
hermes doctor --fix
```

### What to look for in doctor output

| Symptom | Meaning | Fix |
|---------|---------|-----|
| `⚠ missing config` | Profile has no `config.yaml` | Create one (see below) |
| `⚠ Config version N, expected M` | Config schema is outdated | `hermes doctor --fix` or `hermes config migrate` |
| Profile not shown in `list` | Missing profile directory or corrupt profile.yaml | Check directory exists; validate YAML |

## Fixing a missing config.yaml

When `hermes doctor` reports a profile with `⚠ missing config`:

1. **Create config.yaml** by copying the default profile's config and tailoring:
   - Model/default provider
   - Terminal settings (cwd, backend)
   - Profile-specific toolset restrictions

2. **Minimum viable config.yaml** — use the default profile's config as a template. Key sections to preserve: `_config_version`, `model`, `agent`, `terminal`, `display`, `delegation`, `compression`, `cron`, `memory`, `toolsets`.

3. **Verify the fix**:
   ```bash
   hermes doctor | grep -A 3 "Profiles"
   hermes profile show <name>
   ```
   The profile should now show a model and no missing-config warning.

## profile.yaml YAML pitfalls

`~/.hermes/profiles/<name>/profile.yaml` is a small YAML metadata file. Common issues:

- **Multi-line descriptions** — wrap in quotes to avoid indentation breaks:
  ```yaml
  # WRONG — YAML folds the continuation line
  description: Long description spanning
    multiple lines
  # RIGHT — quoted string stays on one logical line
  description: "Long description spanning multiple lines"
  description_auto: false
  ```

- **Indentation** — `description_auto` must be at column 0, same as `description`.

Verify with:
```bash
python3 -c "import yaml; yaml.safe_load(open('$HOME/.hermes/profiles/<name>/profile.yaml')); print('✓ valid')"
```

## Setting the sticky default profile

`hermes profile use <name>` sets which profile loads when `hermes` is invoked without `-p`:

```bash
hermes profile use default   # default profile (root ~/.hermes)
hermes profile use moqtana   # moqtana profile
```

Verify with `hermes profile list` — the `◆` marker indicates the active sticky default.

## Profile listing

```bash
hermes profile list
```

Output columns: Profile name, Model/Provider, Gateway status, Alias, Distribution. The `◆` prefix marks the sticky default.

If the list shows no model for a profile, the profile lacks a valid `config.yaml` or `model.default` is unset.

## Config migration

When `hermes config check` reports an outdated config version:

```bash
# Auto-migrate (preserves custom settings)
hermes doctor --fix

# Or run migration standalone
hermes config migrate
```

Migration may grow the config file with new default sections. Verify no corruption after:
```bash
python3 -c "import yaml; yaml.safe_load(open('$HOME/.hermes/config.yaml')); print('✓ config valid')"
```

## Verification checklist

After fixing a broken profile:

- [ ] `hermes doctor` — no `⚠ missing config` or migration warnings
- [ ] `hermes profile list` — profile shows model/provider
- [ ] `hermes profile show <name>` — all fields populated
- [ ] Config YAML validates: `python3 -c "import yaml; yaml.safe_load(open('.../config.yaml'))"`
- [ ] Profile YAML validates (same check on profile.yaml)

## References

- `hermes-agent` skill (bundled) — CLI reference for all profile commands
- `hermes-model-provider-troubleshooting` — model/provider-specific config issues
