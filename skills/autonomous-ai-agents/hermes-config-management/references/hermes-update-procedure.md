# Hermes Update — Verified Procedure (git install, macOS)

Verified 2026-09-11: v0.19.0 (2026.7.20, `01b04519`) → v0.21.1 (2026.9.7, `45a6101f`), 16,194 commits.

## 1. Check whether an update is needed

```bash
hermes --version            # prints version + upstream short SHA + install method/dir
hermes update --check       # fetches and prints "N commits behind origin/main" or "Already up to date."
```

`--check` fetches (network) but does not install. Safe to run any time.

Also useful for context on what's coming:
```bash
cd ~/.hermes/hermes-agent && git log -1 --format='%h %ad %s' --date=short origin/main
git status --porcelain | head -10   # untracked files in the install dir (update does not touch these)
```

## 2. Run the update

**Pitfall — do NOT use `nohup`/`disown`/`setsid`/trailing `&`.** Hermes rejects shell-level
background wrappers in foreground mode. Use the tracked background runner instead:

```
terminal(background=true, notify_on_complete=true, command="cd ~/.hermes/hermes-agent && hermes update 2>&1")
```

The update takes several minutes (fetch + rebase + pip install + web UI build + desktop check +
skill sync). `process(action="wait", timeout=300)` usually returns it inside one call; `exit_code: 0`
is the success signal. Note: a `wait` that times out returns the log so far and the process keeps
running — poll again rather than assuming failure.

## 3. What the update does (observed order)

1. Fetches upstream + origin
2. Rebase/pull to `origin/main`
3. Python deps reinstall
4. **Rebuilds the web UI** (`hermes_cli/web_dist` — many `✓ built in N s` lines)
5. Checks the desktop app (`✓ Desktop app up to date`)
6. `✓ Code updated!` + refreshes the model catalog cache from the checkout
7. **Syncs bundled skills to ALL profiles** — reported per profile, e.g.
   `default: +12 new, ↑9 updated, ~7 user-modified` / `moqtana: +12 new, ↑33 updated`
8. Checks config for new options (`✓ Configuration is up to date`)
9. `✓ Update complete!`

## 4. Verify after the update

```bash
hermes --version                     # new version + SHA
grep -n 'default:' ~/.hermes/config.yaml | head -2   # config preserved (model.default intact)
pgrep -af 'venv/bin/hermes gateway' | head -3        # gateway alive
hermes update --check                # should print "Already up to date."
```

## Behaviour notes worth reporting to the user

- **The gateway is restarted/killed by `hermes update`.** The chat session usually survives
  (the gateway respawns and keeps handling inbound messages), but any in-flight agent run is lost.
- **`~user-modified` skills are preserved** — the sync reports how many local edits it left alone.
  It does not overwrite them.
- **Untracked files at the install-dir root** (scratch `.md`/`.txt`/`.json` dumps) are untouched by
  the update; they are not a blocker.
- **No restart needed for the CLI** — a fresh `hermes` invocation picks up the new version. A running
  gateway may need a cycle to expose new features; check `~/.hermes/logs/gateway.log` tail to confirm
  it is still processing (`inbound message:` / `response ready:` lines).
- The update also removes aborted-fetch pack temp files (`removed N aborted-fetch pack temp file(s)`).

## Profiles affected

Skill sync and update apply to the whole install, so **every profile** (default, moqtana, …) is
updated at once. Config under `~/.hermes/profiles/<name>/` is per-profile and is not merged across.
