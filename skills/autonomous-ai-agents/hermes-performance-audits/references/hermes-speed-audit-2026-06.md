# Hermes speed audit example — 2026-06

Session pattern: user asked to audit Hermes settings to make it faster without affecting quality, then said “fix all”.

## Observed config highlights

- `model.default: gpt-5.5`
- `model.provider: openai-codex`
- `agent.reasoning_effort: low`
- `display.streaming: true` but `streaming.enabled: false`
- `display.tool_progress: all`
- `display.persistent_output_max_lines: 80`
- `display.busy_ack_detail: true`
- `display.credits_notices: true`
- `display.turn_completion_explainer: true`
- `cron.max_parallel_jobs: null`
- 12 active cron jobs; several scheduled together at 09:00/16:00
- `hermes config check` reported config version update available

## Safe command set applied

```bash
stamp=$(date +%Y%m%d-%H%M%S)
mkdir -p ~/.hermes/backups
cp ~/.hermes/config.yaml ~/.hermes/backups/config.yaml.$stamp.speed-audit.bak
cp ~/.hermes/cron/jobs.json ~/.hermes/backups/cron-jobs.json.$stamp.speed-audit.bak

hermes config set streaming.enabled true
hermes config set display.tool_progress new
hermes config set display.busy_ack_detail false
hermes config set display.turn_completion_explainer false
hermes config set display.credits_notices false
hermes config set display.persistent_output_max_lines 40
hermes config set agent.service_tier priority
hermes config set cron.max_parallel_jobs 2
hermes config set prompt_caching.cache_ttl 1h
hermes config migrate
```

## Cron fixes that mattered

- `script: "bim_watchdog.py --once"` failed because Hermes treated the whole value as a filename.
- Fix: create a wrapper script and point cron `script` to the wrapper filename only.
- The watchdog itself accepted `--scan`, not `--once`; verify script arguments by running the wrapper manually.
- `cronjob(action="run")` schedules an immediate run; it does not mean the run has completed. Wait for a gateway tick and re-check `hermes cron list` for `last_status`.
- After gateway restart/config migration, verify both:

```bash
hermes gateway status
hermes cron status
```

If `cron status` says gateway is not running, run `hermes gateway start`; launchd can be unloaded even when the plist exists.

## OneDrive/cloud-file write pattern

When a cron script writes to a OneDrive/iCloud path, direct `wb.save(target)` or `os.replace(tmp, target)` can fail if the existing file is a dataless/cloud placeholder or locked by sync:

- Save workbook to a temp `.xlsx` first.
- Prefer temp in the same directory for same-volume replace.
- Retry `os.replace` with short backoff.
- If the target remains inaccessible, write/keep a dated fallback file beside it and return that path so the cron job succeeds and the generated artifact is preserved.

Python pattern:

```python
fd, tmp = tempfile.mkstemp(prefix='.name_', suffix='.xlsx', dir=out_dir)
os.close(fd)
try:
    wb.save(tmp)
    for attempt in range(5):
        try:
            os.replace(tmp, out)
            return out
        except OSError:
            time.sleep(2 * (attempt + 1))
    fallback = os.path.join(out_dir, f"name_updated_{date.today().isoformat()}.xlsx")
    os.replace(tmp, fallback)
    print(f"OneDrive target locked/unavailable, wrote fallback: {fallback}")
    return fallback
finally:
    if os.path.exists(tmp):
        os.remove(tmp)
```

## Avoid-list used

- Do not downgrade `gpt-5.5` or provider just for speed.
- Do not reduce retries just for faster failure.
- Do not disable memory/compression/security.
- Do not globally remove tools needed for normal work.
- Do not disable environment probe/LSP without a targeted test.

## Restart note

- CLI config changes: start a new Hermes session.
- Gateway-visible changes: run `hermes gateway restart`, then `hermes gateway status` and `hermes cron status`.
