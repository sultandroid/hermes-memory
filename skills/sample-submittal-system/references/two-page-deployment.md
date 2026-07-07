# Two-Page Deployment Pattern

Each sample folder on the server gets TWO HTML pages:

| File | Content | Purpose |
|------|---------|---------|
| `index.html` | Kimi-style folder cover (front + back) | Landing page — for printing physical folder cover |
| `submittal.html` | A4 formal submittal sheet | For formal submission to CG/NRS/PMC |

## Convention History

| Sample | index.html | cover.html | Notes |
|--------|-----------|------------|-------|
| SAM-FIN-PB-001 | A4 submittal | Kimi cover (as `cover.html`) | First sample, Kimi cover was secondary |
| SAM-FIN-SS-001 | A4 submittal | Kimi cover (as `cover.html`) | Followed PB-001 pattern |
| SAM-FIN-SS-002 | Kimi cover | A4 submittal (as `submittal.html`) | User confirmed cover as landing page |

**Rule:** Always confirm with the user which page should be the default (`index.html`). The convention shifted from "submittal first" to "cover first" — do not assume.

## Deploy Steps for Two Pages

```bash
# 1. Prepare deploy directory
mkdir -p /tmp/deploy/{code}/assets

# 2. Copy both pages
cp label.html /tmp/deploy/{code}/index.html   # Kimi cover as default
cp submittal.html /tmp/deploy/{code}/submittal.html  # A4 sheet

# 3. Copy assets (photo, QR, logos)
cp photo-{code}.jpg /tmp/deploy/{code}/
cp qr-{code}.png /tmp/deploy/{code}/
cp -r assets/*.png /tmp/deploy/{code}/assets/

# 4. Tar and pipe to server
tar czf /tmp/deploy.tar.gz -C /tmp/deploy/{code} .
cat /tmp/deploy.tar.gz | ssh -p 65002 u517606786@samaya-factory.com "cat > /home/u517606786/deploy.tar.gz"

# 5. Extract and fix permissions
ssh -p 65002 u517606786@samaya-factory.com "
  cd domains/samaya-factory.com/public_html/build/Samples/{code}
  rm -rf *
  tar xzf /home/u517606786/deploy.tar.gz
  rm /home/u517606786/deploy.tar.gz
  chmod 755 . assets
  chmod 644 index.html submittal.html photo-{code}.jpg qr-{code}.png
  chmod 644 assets/*.png
  find . -name '._*' -delete
  echo 'Deploy OK'
"
```

## Local File Organization

Under `03.3_Material_Submittals/{CODE-PREFIX}/` (e.g. `SAM-FIN-PB/`):

```
SAM-FIN-PB/
├── label.html          ← Kimi cover source (deployed as index.html)
├── submittal.html      ← A4 sheet source (deployed as submittal.html)
├── index.html          ← copy of submittal.html (for local preview)
├── photo-{CODE}.jpg
├── qr-{CODE}.png
└── assets/             ← logos (optional, for local preview)
```
