#!/bin/bash
# generate-new-sample.sh — scaffold a new sample submittal folder
# Usage: ./generate-new-sample.sh TYPE MATERIAL NUM "Name" "SUBMITTAL_REF"
#   TYPE codes: FIN MAT FAB MTL STN WDN GLS LTH PNM
# Set SAMPLES_DIR env var or run from samples directory

set -euo pipefail
SAMPLES_DIR="${SAMPLES_DIR:-$(pwd)}"
TYPE_CODE="${1:-FIN}"; MATERIAL_CODE="${2:-XX}"
NUM="${3:-001}"; NAME="${4:-Unnamed-Sample}"; SUBMITTAL_REF="${5:-}"
CODE="SAM-${TYPE_CODE}-${MATERIAL_CODE}-${NUM}"
FOLDER="${CODE}-${NAME}"
[[ "$TYPE_CODE" =~ ^(FIN|MAT|FAB|MTL|STN|WDN|GLS|LTH|PNM)$ ]] || { echo "Invalid type"; exit 1; }
[ -d "$SAMPLES_DIR/$FOLDER" ] && { echo "Exists: $FOLDER"; exit 1; }

mkdir -p "$SAMPLES_DIR/$FOLDER"
qrencode -o "$SAMPLES_DIR/$FOLDER/qr-${CODE}.png" -s 12 -m 2 "https://samaya-factory.com/Samples/${CODE}"
echo "  QR → qr-${CODE}.png"

# sample.json
cat > "$SAMPLES_DIR/$FOLDER/sample.json" <<JSONEOF
{"code":"${CODE}","name":"${NAME}","type_code":"${TYPE_CODE}","material_code":"${MATERIAL_CODE}","folder_size":"240x330mm","date_added":"$(date +%Y-%m-%d)","status":"Active","web_url":"https://samaya-factory.com/Samples/${CODE}"$( [ -n "$SUBMITTAL_REF" ] && echo ",\"submittal_ref\":\"${SUBMITTAL_REF}\"" )
}
JSONEOF

# Label from template
T="$SAMPLES_DIR/TEMPLATE-LABEL-24x33cm.html"
if [ -f "$T" ]; then
  sed "s|SAM-FIN-PB-001|${CODE}|g; s|MOC-MUS-ASE-1A0-MA-0007|${SUBMITTAL_REF}|g" "$T" > "$SAMPLES_DIR/$FOLDER/label.html"
fi

# Base64-embed images
/usr/bin/env python3 -c "
import base64, os, re
f='$SAMPLES_DIR/$FOLDER'
h=open(f+'/label.html').read()
for a in ['src','href']:
  for m in re.finditer(a+'=\"([^\"]+\\.(jpg|jpeg|png))\"',h,re.I):
    p=os.path.join(f,os.path.basename(m.group(1)))
    if os.path.exists(p):
      b=base64.b64encode(open(p,'rb').read()).decode()
      x='jpeg' if m.group(2)in('jpg','jpeg')else m.group(2)
      h=h.replace(m.group(0),a+'=\"data:image/'+x+';base64,'+b+'\"')
open(f+'/label.html','w').write(h)
print('  Images embedded.')
"
echo "  Label → label.html"
echo "Next: drop photo-${CODE}.jpg + datasheet + test-report in $FOLDER/"
