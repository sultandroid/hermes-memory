#!/bin/bash
# Deploy using hostname (IP 92.113.28.249 blocks SSH but hostname works)
APP="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/Completed Tender Package From NRS/07_visualizations/Kimi_Agent_Interactive 3D Material Showcase/app"
cd "$APP"
npm run build 2>&1 | tail -3
cp sync.php dist/sync.php
cd dist
tar czf /tmp/aseer-deploy.tar.gz .
scp -P 65002 -o StrictHostKeyChecking=no /tmp/aseer-deploy.tar.gz u517606786@samaya-factory.com:/home/u517606786/
ssh -p 65002 -o StrictHostKeyChecking=no u517606786@samaya-factory.com "cd /home/u517606786/domains/samaya-factory.com/public_html/build && rm -rf aseer && mkdir aseer && cd aseer && tar xzf /home/u517606786/aseer-deploy.tar.gz && rm /home/u517606786/aseer-deploy.tar.gz && chmod 755 sync.php && echo OK"
