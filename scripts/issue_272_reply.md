Confirmed and partly corrected — thank you for filing this per Rule 11.

**Root cause — verified, agree with the diagnosis:**
- The `digitalhermes` profile directory **does not exist** on this machine (only `default` and `moqtana` are present), so `~/.hermes/profiles/digitalhermes/scripts/aconex_daily_sync.sh` was never on disk.
- No `aconex_daily_sync.sh` exists anywhere under the home tree.
- No Aconex credentials are present in `~/.hermes/.env` (grep returns nothing) or any profile `.env`. This is the real hard blocker for any native Aconex pull — even a browser sync would hit the login wall.
- The current cron manifest (`~/.hermes/cron/jobs.json`) does **not** reference `aconex_daily_sync.sh` at all. The two Aconex-related jobs that actually run are `Daily Aconex Check` (06:00) and `Aconex email sync to repo` (every 6h) — and both are **Outlook-SQLite-query jobs**, not shell-script CDE syncs. So the malformed `scripts/scripts/` path in the issue is historical; today's pipeline never reaches a shell script.

**One correction to the impact statement.** The claim that the register is stale and that "no CG responses / outgoing submissions dated since 2026-08-01" is not accurate. The Outlook-based path has kept `01_Registers/submittal_register.md` current through **2026-08-23**, including CG codes returned well after 08-Aug:
- `1E0-1G-0004` Small & AV Power — CG **Code C** 18-Aug (15 comments, CRS by Elbaz)
- `1A0-ZD-0109` Scenography — Code B 16-Aug (4 CG comments)
- `1M0-1G-0004` HVAC Pkg-02 and `1M0-1G-0003` Condensate — Code **B** 20-Aug
- `1A0-PQ-0145/0146` Interlock (BINOTOT, Al Wajeeh) — Code B 13-Aug
- `1K0-ZD-0071` Resubmitted CVs — submitted 10-Aug

So `submission_alerts.py` will **not** over-flag silence from the CG side — CG throughput is current through 20-Aug. The register frontmatter also logs the Adel-bank sync of 23-Aug. The "22-day gap" applies to **native Aconex CDE data** (transmittals/mail snapshots), which is a separate and narrower loss than the issue implies.

**Plan — revised from the issue's proposal:**
1. **Do not recreate a browser-based shell script.** The working, live pipeline is the Outlook-SQLite cron pair above — it is functioning and keeps registers current. Recreating `aconex_daily_sync.sh` would duplicate that and depend on credentials we don't have.
2. **Aconex native creds are the genuine gap** — add `ACONEX_USER` / `ACONEX_PASS` (or Oracle SSO token) to `~/.hermes/.env`. Until then we cannot pull mail/transmittal beyond what Outlook mirrors, and the native CDE snapshot remains stuck at 2026-08-01.
3. **Backfill** of native Aconex transmittals 02-Aug → 23-Aug only once creds land; most of the workflow transmittals (SIC.-WTRAN/CGP-WTRAN) are already reflected in the register via the Outlook sync, so the backfill is verification, not a rebuild.
4. **Correct the cron manifest** to drop any stale `aconex_daily_sync.sh` reference so the failing path is never invoked again.

I'll action items 2 and 4 (credential request to IT / Aconex project admin, and cron cleanup) and leave this issue open as the tracking record until creds are provisioned.

— Eng. Mohamed Sultan, Technical Office Manager
