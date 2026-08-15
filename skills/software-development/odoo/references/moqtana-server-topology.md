# Moqtana Server Topology — 167.99.224.43

DigitalOcean droplet running Odoo 18 Community (DB `moqtana`) behind Nginx Proxy Manager.

## Ports
| Port | Service | Notes |
|------|---------|-------|
| 80   | Nginx Proxy Manager (default site) | Returns "Default Site / Log in to Admin panel" for any host with no proxy host configured |
| 81   | NPM Admin panel | Login to configure proxy hosts |
| 8069 | Odoo | Direct Odoo access; works without NPM |

## Diagnosing "Default Site" / "Log in to the Admin panel" page
When a user opens `http://167.99.224.43/` (or a domain) and sees the NPM default
"Congratulations! You've successfully started the Nginx Proxy Manager" page, it
means **no proxy host is configured** for that hostname/IP on port 80. Odoo itself
is fine — reach it directly on `:8069`.

## Fix
In NPM admin (`:81`), create a Proxy Host:
- Domain Names: `odoo.moqtana.sa` (or the domain in use)
- Forward Hostname/IP: `127.0.0.1` (or `167.99.224.43`)
- Forward Port: `8069`
- Websockets Support: ON (required for Odoo)

## Verification
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://167.99.224.43/        # 200 = NPM default site
curl -s -o /dev/null -w "%{http_code}\n" http://167.99.224.43:8069/  # 200 = Odoo up
```
