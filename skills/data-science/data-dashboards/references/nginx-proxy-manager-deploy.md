# Deploying a Dashboard to Nginx Proxy Manager (NPM)

When the target is a self-hosted server running **Nginx Proxy Manager** (not Surge.sh),
the dashboard becomes the server's landing page on port 80. This is the pattern used for
the Moqtana internal ops dashboard.

## Server layout (Docker NPM)

- NPM container maps `80-81` and `443`.
- NPM data volume: `/opt/odoo/npm/data/` → container `/data`.
- Proxy host configs: `/opt/odoo/npm/data/nginx/proxy_host/<id>.conf`
- Default site (the "Default Site / Log in to Admin panel" page) is served when no
  proxy host matches the requested hostname/IP.
- NPM admin panel: port `81` (`http://<ip>:81`).

## Diagnosing "Default Site" page

If `http://<ip>/` returns the NPM default page instead of your app:

1. Confirm the app is actually up on its own port, e.g. `curl -sI http://<ip>:8069/`.
2. Check the proxy host config exists: `cat /opt/odoo/npm/data/nginx/proxy_host/*.conf`.
3. The default page means **no proxy host matches that hostname** — add one in the NPM
   admin panel (port 81) pointing at the app's port, or serve a custom landing page.

## Serving a custom landing page on port 80

Two options:

1. **NPM proxy host → static file** (cleanest): add a proxy host whose domain is the
   bare IP/hostname, forward to a tiny static server (e.g. `python3 -m http.server 8080`
   serving the HTML), or use NPM's custom location to serve a file.
2. **Replace the default site** directly on the server (more invasive).

## Verify after deploy

```bash
curl -s http://<ip>/ | head -20          # should show your HTML, not NPM default
curl -s -o /dev/null -w "%{http_code}\n" http://<ip>/   # 200
```

## Pitfalls

- **Chart.js CDN needs internet** — the dashboard is not truly self-contained. For an
  internal server page, either keep the CDN (server has internet) or inline Chart.js.
- **Raw-IP / plain-HTTP curl flags** — the security scanner flags `curl http://<ip>/`.
  It auto-approves; just proceed.
- **SSH access** — confirm key-based root SSH works before planning a server deploy:
  `ssh -o BatchMode=yes -o ConnectTimeout=8 root@<ip> 'hostname'`.
- **Internal pages should not carry client branding** — when the user says "internal,
  for me only", drop the company brand and use a neutral "Server Hub / Operations
  Dashboard" identity.
