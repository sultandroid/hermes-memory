# Lessons Learned Web App — Build & Deploy

## Overview
Interactive web app for the Lessons Learned Register at `samaya-factory.com/aseer/registers/LN/`. Single HTML file, no build tools, fetches live from GitHub raw markdown.

## Source Data
- Repo: `https://raw.githubusercontent.com/sultandroid/aseer-museum-pm/main/03_Plans/11_Quality/lessons_learned_register.md`
- Local: `/Users/mohamedessa/aseer-museum-pm/03_Plans/11_Quality/lessons_learned_register.md`

## Build
Single `index.html` with embedded CSS + JS. Uses:
- `marked.js` from CDN for markdown parsing
- `window.print()` with `@media print` CSS for A4 PDF
- Vanilla JS — no frameworks, no build tools

## Deploy
```bash
# SSH details
HOST=samaya-factory.com
PORT=65002
USER=u517606786
REMOTE_PATH=/home/u517606786/domains/samaya-factory.com/public_html/aseer/registers/LN/

# Create remote dir
ssh -p $PORT $USER@$HOST "mkdir -p $REMOTE_PATH"

# Upload
scp -P $PORT /tmp/lessons-learned-app/index.html $USER@$HOST:$REMOTE_PATH

# Fix permissions
ssh -p $PORT $USER@$HOST "chmod -R 755 $REMOTE_PATH"

# Verify
curl -s -o /dev/null -w "%{http_code}" https://samaya-factory.com/aseer/registers/LN/
```

## Key Design Decisions
- **Live from GitHub** — page fetches markdown on load, always shows latest
- **No build tools** — single HTML file, easy to update
- **Samaya brand** — Navy #1E293B, Gold #C9A84C, Calibri
- **A4 PDF print** — each lesson prints as standalone Samaya-branded document
- **Filters** — by category, status, governing plan
- **Sortable columns** — click column header to sort
