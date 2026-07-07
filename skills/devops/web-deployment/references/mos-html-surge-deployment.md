# MOS HTML Document Deployment to Surge

Session-specific notes for publishing large self-contained HTML Method of Statement (MOS) documents to Surge.sh.

## Document characteristics

- Single large HTML file (7+ MB) with embedded base64 images.
- Only the external logo is a separate asset (`assets/samaya-logo-trans.png`).
- `Certifications/` folder contains referenced PDFs for Appendix B.
- Built for A4 print; not a React/Vite app.

## Verified workflow

1. **Copy to /tmp/** to avoid OneDrive latency/locks:
   ```bash
   rm -rf /tmp/deploy-final && mkdir -p /tmp/deploy-final
   cp "/path/to/MOC-...-MOS_LiDAR_Survey.html" /tmp/deploy-final/index.html
   cp -R "/path/to/assets" /tmp/deploy-final/assets
   ```

2. **Global `surge` fails on large embedded-base64 HTML.** Use `npx surge`:
   ```bash
   cd /tmp/deploy-final && npx surge --project . --domain aseer-mos-lidar.surge.sh
   ```

3. **Verify assets** after deploy:
   ```bash
   curl -s -o /dev/null -w "%{http_code} %{size_download}\n" https://<domain>.surge.sh/
   curl -s -o /dev/null -w "%{http_code} %{size_download}\n" https://<domain>.surge.sh/assets/samaya-logo-trans.png
   ```

4. **Surge cold-start 504 is transient.** Wait 10-30 seconds and retry; do not redeploy.

## Approval rule

Always get explicit user approval before deploying. This user corrected: "dont deploy to surge.sh until i asked you".
