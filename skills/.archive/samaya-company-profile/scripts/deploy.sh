#!/usr/bin/env bash
# deploy.sh — Full deploy to samaya-factory-profile.surge.sh
# Run from anywhere. Cleans and rebuilds from v6/ source.
set -euo pipefail

V6="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile/v6"

echo "=== 1. Clean deploy directory ==="
rm -rf /tmp/samaya-profile-deploy
mkdir -p /tmp/samaya-profile-deploy

echo "=== 2. Copy HTML ==="
cp "$V6/index.html" /tmp/samaya-profile-deploy/index.html

echo "=== 3. Fix paths (../assets/ -> assets/) ==="
python3 -c "
p = '/tmp/samaya-profile-deploy/index.html'
with open(p) as f:
    c = f.read()
c = c.replace('../assets/', 'assets/')
with open(p, 'w') as f:
    f.write(c)
"

echo "=== 4. Copy CSS ==="
cp -R "$V6/css/" /tmp/samaya-profile-deploy/css/

echo "=== 5. Copy referenced assets ==="
python3 "$(dirname "$0")/copy-deploy-assets.py"

echo "=== 6. Deploy to Surge ==="
cd /tmp/samaya-profile-deploy
surge --project ./ --domain samaya-factory-profile.surge.sh

echo "=== 7. Verify ==="
curl -so /dev/null -w "HTTP %{http_code}\n" https://samaya-factory-profile.surge.sh/
