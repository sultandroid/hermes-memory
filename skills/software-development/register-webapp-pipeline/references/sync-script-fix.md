# sync_risk_snapshots.sh — Required Fix

The script at `~/hermes-memory/scripts/sync_risk_snapshots.sh` has **hardcoded stale snapshot filenames** that don't match the current build output.

## Problem

The script downloads from server URLs with filenames like:
```
EXP-RISK-PRR-2026-012_RevC11_ACTIVE.xlsx
```

But after each `build_snapshots.py --bump`, the snapshot number increments (currently 025). The hardcoded URL downloads either a 404 or a stale version if the old file still lives on the server.

## Fix Options

### Option A — Copy from local repo (preferred)
Replace the `curl` download with a local `cp` from the repo's generated snapshots:

```bash
SRC="/Users/mohamedessa/aseer-museum-pm/06_Risk_System/webapp"

for dest_dir, prefix, subpath in \
    "01_Master_Risk_Register  PRR  src" \
    "02_Design_Risk_Register DDR  src/DDR" \
    "03_HSE_Risk_Register    HSE  src/HSE" \
    "04_AV_Risk_Register     AVR  av/src"; do

    read -r folder prefix subdir <<< "$dest_dir"
    latest=$(ls -t "$SRC/$subdir"/EXP-RISK-${prefix}-2026-*_ACTIVE.xlsx 2>/dev/null | head -1)
    if [ -z "$latest" ]; then
        echo "No snapshot found for $prefix"
        continue
    fi
    dst_name="Aseer_Museum_${prefix}_Snapshot_$(date +%Y-%m-%d).xlsx"
    rm -f "$REV_DIR/$folder/"*.xlsx
    cp "$latest" "$REV_DIR/$folder/$dst_name"
    echo "Saved $dst_name ($(wc -c < "$latest") bytes)"
done
```

### Option B — Dynamic URL (if server is authoritative)
Use `ls -t` on the server directory over SCP to discover the latest filename, then download that. More fragile than Option A.

## Also fix: PRR snapshot download uses wrong URL path

The current script downloads PRR from:
```
https://samaya-factory.com/aseer/registers/Risk/EXP-RISK-PRR-...
```
But the correct PRR download path is the same pattern as the others. The URL structure is consistent — just the filename number changes.
