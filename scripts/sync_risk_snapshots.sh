#!/bin/bash
# Daily snapshot sync: downloads latest risk register snapshots to OneDrive
# Also creates new REV folder each week (Sunday)

BASE="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/04_Registers/05_Submittle"

# Weekly: check if we need a new REV folder (Sunday)
DOW=$(date +%u)
if [ "$DOW" = "7" ]; then
    # Find current REV folder number
    LAST_REV=$(ls -d "$BASE"/REV* 2>/dev/null | grep -oP 'REV\d+' | sort | tail -1)
    if [ -z "$LAST_REV" ]; then
        NEXT_REV="REV01"
    else
        NUM=${LAST_REV#REV}
        NEXT_REV=$(printf "REV%02d" $((10#$NUM + 1)))
    fi
    REV_DIR="$BASE/$NEXT_REV"
else
    # Use existing REV folder
    REV_DIR=$(ls -d "$BASE"/REV* 2>/dev/null | sort | tail -1)
    if [ -z "$REV_DIR" ]; then
        REV_DIR="$BASE/REV01"
    fi
fi

# Create subfolders
mkdir -p "$REV_DIR/01_Master_Risk_Register" "$REV_DIR/02_Design_Risk_Register" "$REV_DIR/03_HSE_Risk_Register" "$REV_DIR/04_AV_Risk_Register"

# Download and replace
for pair in "01_Master_Risk_Register  https://samaya-factory.com/aseer/registers/Risk/EXP-RISK-PRR-2026-012_RevC11_ACTIVE.xlsx  PRR" \
            "02_Design_Risk_Register https://samaya-factory.com/aseer/registers/Risk/DDR/EXP-RISK-DDR-2026-012_RevC11_ACTIVE.xlsx DDR" \
            "03_HSE_Risk_Register    https://samaya-factory.com/aseer/registers/Risk/HSE/EXP-RISK-HSE-2026-011_RevC11_ACTIVE.xlsx HSE" \
            "04_AV_Risk_Register     https://samaya-factory.com/aseer/registers/Risk/AV/EXP-RISK-AV-2026-001_RevC11_ACTIVE.xlsx AVR"; do
    read -r folder url prefix <<< "$pair"
    rm -f "$REV_DIR/$folder/"*.xlsx
    dest="$REV_DIR/$folder/Aseer_Museum_${prefix}_Snapshot_$(date +%Y-%m-%d).xlsx"
    curl -s -o "$dest" "$url"
    echo "Saved $(basename "$dest") ($(wc -c < "$dest") bytes)"
done
