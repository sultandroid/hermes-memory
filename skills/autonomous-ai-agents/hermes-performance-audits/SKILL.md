---
name: hermes-performance-audits
description: Audit and tune Hermes Agent settings for lower latency without degrading output quality.
version: 1.0.0
created_by: agent
---

# Hermes Performance Audits

Use when the user asks to make Hermes faster, reduce latency, speed up responses, or audit Hermes settings while preserving quality.

## Goal

Improve real or perceived speed without changing the quality-critical model/reasoning path unless the user explicitly accepts the tradeoff.

## Workflow

1. Treat Hermes docs/source as authoritative, but do not edit bundled or hub-installed skills.
2. Inspect current state before recommending changes:
   - `hermes config path`
   - `hermes config`
   - `hermes status --all`
   - `hermes tools list`
   - `hermes config check`
   - `hermes cron list` when gateway/cron is active
   - process list for stale Hermes/gateway workers when latency is reported
3. Delegate at least one independent audit/QC pass for substantive tuning work.
4. Classify recommendations:
   - Safe/no-quality-loss
   - Safe but cost/operational caveat
   - Risky/quality-affecting — avoid unless user approves
5. Prefer recommendations first. Do not mutate config unless the user asked to apply changes.
6. If applying config or cron changes, back up first:
   - `stamp=$(date +%Y%m%d-%H%M%S)`
   - `mkdir -p ~/.hermes/backups`
   - `cp ~/.hermes/config.yaml ~/.hermes/backups/config.yaml.$stamp.speed-audit.bak`
   - `cp ~/.hermes/cron/jobs.json ~/.hermes/backups/cron-jobs.json.$stamp.speed-audit.bak` when cron exists
7. After gateway restart/reload, verify the scheduler is actually alive:
   - `hermes gateway status`
   - `hermes cron status`
   - If `hermes cron status` says gateway is not running, run `hermes gateway start` and re-check; launchd may need reloading after config migration/restart.
8. Tell the user which changes need a new CLI session or gateway restart.

## Safe speed levers

These generally do not degrade answer quality:

- Enable true streaming when display streaming is on but `streaming.enabled` is false.
- Reduce UI/rendering noise:
  - lower `display.tool_progress` from `all` to `new` or `off`
  - reduce `display.persistent_output_max_lines`
  - disable cosmetic notices such as `display.credits_notices` and `display.turn_completion_explainer`
  - disable `display.busy_ack_detail` if the user values terse output
- Use provider priority/fast tier when supported, e.g. `agent.service_tier: priority`; note possible higher cost or provider ignoring it.
- Limit background contention:
  - set a small `cron.max_parallel_jobs` when many cron jobs fire together
  - fix or pause duplicate/erroring cron jobs
  - add narrow `enabled_toolsets` to agent-backed cron jobs
  - convert deterministic cron jobs to `no_agent: true` scripts where appropriate
  - for script-only cron jobs, keep `script` as a filename/path only; put arguments in a wrapper script if needed because `script: "foo.py --arg"` is treated as a literal missing filename
  - after `cronjob(action="run")`, wait for the gateway tick and verify `last_status`; the tool only schedules the immediate run
- Keep terminal local/persistent when already configured; local backend is usually fastest for macOS CLI use.
- For cron scripts writing into OneDrive/iCloud paths, avoid direct overwrite failures by writing a temp file, retrying replacement, and returning a dated fallback output path if the cloud placeholder remains locked/unavailable. This keeps the cron job successful while preserving the generated artifact.
- Run `hermes config migrate` only after backup/review when `hermes config check` reports an outdated config version.

## Avoid unless quality tradeoff is accepted

- Downgrading `model.default` or switching provider solely for speed.
- Lowering `agent.reasoning_effort` below the established quality/speed balance.
- Lowering `agent.api_max_retries`; it only helps failed calls and reduces reliability.
- Disabling memory globally.
- Disabling compression or making it much more aggressive without testing context retention.
- Globally disabling toolsets that the user relies on.
- Disabling `agent.environment_probe`, `agent.coding_context`, or `lsp.enabled` blindly; these may protect correctness.
- Disabling security/safety features such as secret redaction or Tirith purely for speed.

## Reporting format

Keep it short:

- Current quality-critical settings
- Ranked safe changes with exact `hermes config set ...` commands
- Items to fix separately, especially cron/process contention
- Explicit avoid-list
- Restart requirements
- One-line note of verification/labor used

## Reference

- `references/hermes-speed-audit-2026-06.md` — condensed example audit findings and safe command set from a real session.
