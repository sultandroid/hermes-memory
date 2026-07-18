# Public Asset Hosting for Agent Access

## Problem

Agents working on private repos cannot access binary files (logos, images, PDFs) directly — GitHub raw URLs require auth, and the agent's sandbox is separate from the user's filesystem. The agent reports "downloaded successfully" but the file lands in the tool's runtime, not the user's workspace.

## Solution: Host on Public Web Server

Upload binary assets to a public-facing web server (shared hosting, Surge, etc.) so any agent can fetch them via unauthenticated URL.

### Step-by-Step

1. **Create directory on server:**
   ```bash
   ssh -p <port> -o BatchMode=yes user@host "mkdir -p ~/domains/domain.com/public_html/assets/<category>/"
   ```

2. **Upload via SSH pipe** (reliable, avoids SCP hangs):
   ```bash
   cat /path/to/local/file.png | ssh -p <port> -o BatchMode=yes user@host \
     "cat > ~/domains/domain.com/public_html/assets/<category>/file.png"
   ```

3. **Set permissions** (Hostinger/LiteSpeed requires 755):
   ```bash
   ssh -p <port> user@host "chmod -R 755 ~/domains/domain.com/public_html/assets/<category>/"
   ```

4. **Check for .htaccess rewrite** — if the server rewrites all requests to a subdirectory (e.g. `/build/`), upload there instead:
   ```bash
   ssh -p <port> user@host "cat ~/domains/domain.com/public_html/.htaccess"
   # If RewriteRule ^(.*)$ /build/$1 [L], use public_html/build/assets/ instead
   ```

5. **Verify HTTP 200:**
   ```bash
   curl -s -o /dev/null -w "%{http_code}" https://domain.com/assets/<category>/file.png
   ```

### Document in Repo

Add a **Public URL** row to the relevant table in `AGENTS.md` so every agent that reads the repo knows the URL:

```markdown
| **Public URL** (for agents outside this repo) | description | `https://domain.com/assets/<category>/file.png` |
```

Also add a `README.md` in the source folder with the URLs.

### Agent Usage

Agents working outside the repo should download from the public URL:
- `curl -O https://domain.com/assets/<category>/file.png`
- Or reference directly in HTML: `<img src="https://domain.com/assets/<category>/file.png">`

### Pitfalls

- **.htaccess rewrites** — common on Hostinger. Check before uploading, or files 404 despite being on disk.
- **Permissions** — SCP/SSH pipe creates files with 600 permissions. Web server can't read them. Always `chmod -R 755`.
- **CDN cache** — Surge/Cloudflare may take 10-30s to serve new assets. First hit may 504. Wait and retry.
- **Never reference repo path from outside** — agents on other machines/OneDrive/temp dirs must copy the file, not link to the repo path.
