#!/usr/bin/env python3
"""
odoo_connect.py — one-shot XML-RPC connector for the user's two Odoo instances.

Reads credentials from local env files (never hardcoded):
  - Samaya  : ~/.config/samaya/odoo.env   (ODOO_URL, ODOO_DB, ODOO_USER, ODOO_API_KEY)
  - Moqtana : ~/.config/moqtana/odoo.env  (same keys) — falls back to flags/prompt

Usage:
  python3 odoo_connect.py --instance samaya --check
  python3 odoo_connect.py --instance samaya --model res.partner --method search_read \
      --domain '[]' --fields '["name","id"]' --limit 5
  # In your own code:
  from odoo_connect import connect
  uid, models, cfg = connect("samaya")
  ids = models.execute_kw(cfg['db'], uid, cfg['pw'], 'purchase.order', 'search', [[]])
"""
import argparse, json, os, ssl, sys, xmlrpc.client

DEFAULTS = {
    "samaya":  {"env": "~/.config/samaya/odoo.env",
                "url": "https://samayainv.odoo.com",
                "db":  "peerless-tech-samaya-18-0-18447146",
                "user": "sultan@samayainvest.com"},
    "moqtana": {"env": "~/.config/moqtana/odoo.env",
                "url": "http://167.99.224.43:8069",
                "db":  "moqtana",
                "user": "mohamedsultanabbas@gmail.com"},
}

def _load_env(path):
    env = {}
    p = os.path.expanduser(path)
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env

def connect(instance="samaya"):
    """Return (uid, models_proxy, cfg) where cfg has url/db/user/pw."""
    d = DEFAULTS.get(instance)
    if not d:
        raise SystemExit(f"Unknown instance '{instance}'. Use: {', '.join(DEFAULTS)}")
    env = _load_env(d["env"])
    cfg = {
        "url":  env.get("ODOO_URL", d["url"]),
        "db":   env.get("ODOO_DB", d["db"]),
        "user": env.get("ODOO_USER") or env.get("ODOO_LOGIN", d["user"]),
        "pw":   env.get("ODOO_API_KEY") or env.get("ODOO_PASSWORD") or os.environ.get("ODOO_API_KEY", ""),
    }
    if not cfg["pw"]:
        raise SystemExit(
            f"No credential found. Create {d['env']} with ODOO_API_KEY=... "
            f"(API key from Odoo → Settings → Account Security → Developer API Keys), "
            f"or export ODOO_API_KEY in the environment."
        )
    # Use unverified SSL context for HTTPS URLs (Samaya Odoo cert chain issue on macOS)
    if cfg["url"].startswith("https://"):
        ctx = ssl._create_unverified_context()
        transport = xmlrpc.client.SafeTransport(context=ctx)
        common = xmlrpc.client.ServerProxy(f"{cfg['url']}/xmlrpc/2/common", transport=transport)
    else:
        common = xmlrpc.client.ServerProxy(f"{cfg['url']}/xmlrpc/2/common")
    uid = common.authenticate(cfg["db"], cfg["user"], cfg["pw"], {})
    if not uid:
        raise SystemExit(
            "Authentication FAILED (uid is False). Check: (1) ODOO_USER login is exact, "
            "(2) ODOO_API_KEY is a valid API key for that user, (3) ODOO_DB matches the instance."
        )
    if cfg["url"].startswith("https://"):
        models = xmlrpc.client.ServerProxy(f"{cfg['url']}/xmlrpc/2/object", transport=transport)
    else:
        models = xmlrpc.client.ServerProxy(f"{cfg['url']}/xmlrpc/2/object")
    return uid, models, cfg

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", default="samaya", choices=list(DEFAULTS))
    ap.add_argument("--check", action="store_true", help="Just verify auth and exit")
    ap.add_argument("--model"); ap.add_argument("--method", default="search_read")
    ap.add_argument("--domain", default="[]"); ap.add_argument("--fields", default="[]")
    ap.add_argument("--limit", type=int, default=10)
    a = ap.parse_args()

    url = DEFAULTS[a.instance]['url']
    if url.startswith("https://"):
        ctx = ssl._create_unverified_context()
        t = xmlrpc.client.SafeTransport(context=ctx)
        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", transport=t)
    else:
        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    try:
        ver = common.version().get("server_version")
    except Exception as e:
        raise SystemExit(f"Cannot reach server: {type(e).__name__}: {e}")
    uid, models, cfg = connect(a.instance)
    print(f"OK  instance={a.instance}  server={ver}  uid={uid}  db={cfg['db']}")
    if a.check or not a.model:
        return
    kw = {"fields": json.loads(a.fields), "limit": a.limit} if a.method == "search_read" else {}
    res = models.execute_kw(cfg["db"], uid, cfg["pw"], a.model, a.method,
                            [json.loads(a.domain)], kw)
    print(json.dumps(res, ensure_ascii=False, indent=2, default=str))

if __name__ == "__main__":
    main()
