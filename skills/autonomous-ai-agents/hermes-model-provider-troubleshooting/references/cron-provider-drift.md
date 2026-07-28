# Cron Job Provider Drift — Diagnosis & Fix

## Symptom

A cron job that was created under provider X fails after the user switches to provider Y:

```
RuntimeError: Skipped to prevent unintended spend: global inference config drifted since this job was created (provider 'ollama-cloud' -> 'opencode-go'), and this job is unpinned. No inference call was made. To run on the new config, pin it explicitly: `cronjob action=update job_id=8933383a0d68 provider=<provider> model=<model>` (or pin the original values to keep them).
```

## Root Cause

When a cron job is created without an explicit `provider`/`model`, Hermes stores the then-current global provider implicitly. If the user later changes the global provider (e.g. via `hermes model` or config edit), the pinned job has a mismatch. Hermes blocks execution to prevent unintended spend on a different provider than the job was designed for.

## Fix Options

### Option A: Re-pin to the original provider (preserve original intent)

```bash
cronjob action=update job_id=<ID> provider=<ORIGINAL_PROVIDER>
```

Example:
```bash
cronjob action=update job_id=8933383a0d68 provider=ollama-cloud
```

Then verify:
```bash
cronjob action=list  # check provider field is set
```

### Option B: Pin to the new current provider (follow the user's latest choice)

```bash
cronjob action=update job_id=<ID> provider=<NEW_PROVIDER>
```

## Prevention

Always pin a provider explicitly when creating cron jobs that use an LLM:

```bash
cronjob action=create schedule="..." prompt="..." provider=ollama-cloud model=deepseek-v4-flash
```

This makes the job robust to future provider switches.

## Affected Jobs

List all current cron jobs and check which ones have `provider: null` (unpinned — at risk):

```bash
cronjob action=list
```

Jobs with `model: null, provider: null` are unpinned and will drift if the global provider changes.
