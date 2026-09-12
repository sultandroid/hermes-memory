# Cron Job Provider/Model Drift — Diagnosis & Fix

## Symptom

A cron job fails at runtime with:

```
RuntimeError: Skipped to prevent unintended spend: global inference config drifted since this job was created (provider 'X' -> 'Y'; model 'A' -> 'B'), and this job is unpinned. No inference call was made.
```

Hundreds of consecutive failures can appear, across many jobs at once, immediately after a
`model.default` / `model.provider` change.

## Root cause — and why the old remedy is wrong

When a job is created without an explicit `provider`/`model`, Hermes stores the then-current
global values as a **creation snapshot**. An old build shipped a fail-closed guard: any unpinned
job whose snapshot no longer matched the live global default raised this error instead of running,
to avoid spending on an unintended provider.

That guard was reversed. On a current build the **snapshot is the job's effective pin** — an
unpinned job keeps running on the model/provider it was created with and logs one INFO line per
differing axis. A global model switch no longer stops any job.

**Therefore: seeing this RuntimeError means the process executing the job is running pre-fix code.**
It is a stale-build symptom, not a configuration fault. Do not start by editing job pins.

## Diagnose the fleet (execution ledger)

```bash
cd ~/.hermes
sqlite3 cron/executions.db "select status, count(*) from executions group by status;"
# failures grouped by kind — one dominant repeated error is the tell
sqlite3 cron/executions.db "select substr(coalesce(error,''),1,110) e, count(*) from executions where status='failed' group by 1 order by 2 desc;"
# blast radius + window
sqlite3 cron/executions.db "select count(distinct job_id) from executions where error like '%drifted%';"
sqlite3 cron/executions.db "select min(claimed_at), max(claimed_at) from executions where error like '%drifted%';"
sqlite3 cron/executions.db ".schema executions"   # columns: id, job_id, status, claimed_at, error
```

Compare the drift window start against the date the global model was changed — they should match.

Also list which jobs are unpinned (`model: null, provider: null`) and their stored snapshots:

```bash
python3 -c "
import json
jobs=json.load(open('/Users/mohamedessa/.hermes/cron/jobs.json'))
jobs=jobs if isinstance(jobs,list) else jobs.get('jobs',jobs)
for j in (jobs.values() if isinstance(jobs,dict) else jobs):
    print(j.get('job_id'), '|', (j.get('model_snapshot'), j.get('provider_snapshot')), '| pin=', j.get('model'))
"
```

Cost note: the failure raises before any inference call, so no spend occurred — say so plainly.

## Fix — update and restart, then verify with one job

1. **Update Hermes** (`hermes update`) to pull the snapshot-as-pin behaviour.
2. **Restart the gateway from outside its process tree.** A gateway process that survived the
   update keeps the old modules in memory, so the fix is not live until the PID changes. See
   *Stale gateway after `hermes update`* in `hermes-config-management`.
3. **Re-run one affected job and confirm it executes:**

```bash
cronjob action=run job_id=<JOB_ID>
```

```bash
sqlite3 ~/.hermes/cron/executions.db "select status, substr(coalesce(error,'OK'),1,80) from executions order by rowid desc limit 3;"
```

`running`/`completed` with a real API call count = fixed. A sub-second `failed` with `API calls: 0`
means the old code is still loaded — the restart did not take.

## When re-pinning IS the right move

Only when the user explicitly wants a job moved off its creation snapshot (typically because the
snapshot names a provider they no longer use):

```bash
cronjob action=update job_id=<JOB_ID> provider=<PROVIDER> model=<MODEL>
```

Bulk-pinning every affected job as the blanket response is the pre-fix remedy and is wrong: it
rewrites job intent the user did not ask to change and buries the real cause.

## Prevention

Pin provider + model explicitly at creation for any job that must never follow a global switch:

```bash
cronjob action=create schedule="..." prompt="..." provider=<PROVIDER> model=<MODEL>
```

Leaving both unset is safe on a current build (the snapshot pins it) — but the snapshot is frozen
at creation, so an unpinned job will never pick up a model upgrade on its own. Choose deliberately.
