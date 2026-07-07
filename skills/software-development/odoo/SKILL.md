---
name: odoo
title: Odoo — Query & Manage Moqtana / Samaya Odoo 18
description: Use when querying, creating, or troubleshooting records on the Moqtana (factory) or Samaya (purchasing) Odoo 18 instances via XML-RPC.
triggers:
  - User asks about Odoo data (projects, products, users, HR, invoices)
  - User wants to configure/change Odoo settings
  - User reports Odoo access issues
  - User asks about Odoo scripts or deployment
  - User says "make PO" / "RFQ" / "create purchase order" in Odoo
  - User asks for software subscription licensing procurement
---

# Odoo — Query & Manage Moqtana / Samaya Odoo 18

## ⚠️ SSL Certificate — XML-RPC on macOS

Python 3.13+ on macOS may fail with `SSL: CERTIFICATE_VERIFY_FAILED`. Fix:

```bash
SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") python3 script.py
```

## ⚠️ Odoo 18 Field Name Quirks

`mrp.production` uses different field names than some docs suggest:

| Wrong (doesn't exist) | Correct |
|---|---|
| `date_planned_start` | `date_start` |
| `date_planned_finished` | `date_finished` |

`purchase.order` has `project_id` on the **header**. `analytic_distribution` only on `purchase.order.line`.

See `references/odoo-18-field-schemas.md` for full field lists.

## ⚠️ Odoo 18 Domain Quirks (CRITICAL)

`project_id` in `search_read` domains and `['name','in',list]` domains **crash Odoo 18**. Always fetch all records and filter in Python, or use the two-step `search` + `read` pattern. See `references/odoo-18-domain-quirks.md` for full details and code examples.

## 🔴 CRITICAL: لا تلخبط بين الشركات — Never Confuse Instances

This user operates **two separate Odoo instances** for **two separate companies**. Getting it wrong triggers immediate user frustration.

**🚫 HARD RULE: Never query Moqtana Odoo unless the user explicitly mentions it by name.** Even if you can't find what you need on Samaya, ask the user before touching Moqtana. The user's directive: "this is samaya odoo not moqtana odoo dont use moqtana for any task until i mention you".

**The most common mistake:** Aseer Museum (متحف عسير الإقليمى) looks like a museum project → you instinctively query Moqtana. **WRONG.** Aseer lives on Samaya Odoo, project ID 219.

## Connecting to Odoo instances with SSL/certificate issues

When direct `xmlrpc.client` connection fails with `CERTIFICATE_VERIFY_FAILED` or `400 BAD REQUEST`:

1. Use `ssl.create_default_context()` with `check_hostname = False` and `verify_mode = ssl.CERT_NONE`.
2. Always use the root URL (e.g. `https://odoo.moqtana.sa`), **not** `/odoo` or any web path.
3. Try the standard XML-RPC endpoint: `/xmlrpc/2/common`.
4. Test multiple database names if the first fails (`moqtana`, `odoo`, `production`).
5. Confirm the exact login (email vs username) — some instances require the Google/Microsoft login email.

Successful pattern (Moqtana Odoo 18):
```python
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=ctx)
uid = common.authenticate(db, username, password, {})
```

**Quick rule of thumb:**
- **Samaya Odoo** = سمايا (main co.) — POs, procurement, invoices, **ALL museum/exhibition projects** including Aseer, Replica, etc. Default to Samaya for ALL task creation.
- **Moqtana Odoo** = مصنع (factory) — manufacturing, inventory, HR, company-internal projects. **Do NOT use unless user says "اودو المصنع" or "Moqtana" explicitly.**
- User says "اودو سمايا" → Samaya. User says "اودو المصنع" → Moqtana.
- **When in doubt about which instance a project belongs to: ask the user before querying, don't guess. Never try Moqtana as a fallback.**

**⚠ If the user says "لا تلخبط بين الشركات" — you confused which Odoo instance to use. Stop and re-check.**

## Quick Connect (proven helper — use this first)

`scripts/odoo_connect.py` handles auth for both instances. It reads credentials from
local env files (`~/.config/samaya/odoo.env`, `~/.config/moqtana/odoo.env`) — never hardcoded.

**⚠ CLI only supports `search_read`, `search`, and `read` methods.** For `create`/`write`/`unlink`, see `references/odoo-cli-limitations-and-direct-python.md`.

**⚠ `--method read` expects integer record IDs, NOT a domain.** Use `--method search_read` for domain-based queries. Passing `--domain` with `read` will fail with `IndexError`.

```bash
# Verify the connection (Samaya):
python3 scripts/odoo_connect.py --instance samaya --check
#   → OK  instance=samaya  server=18.0+e  uid=151  db=peerless-tech-samaya-18-0-18447146

# Read records directly from the CLI:
python3 scripts/odoo_connect.py --instance samaya --model purchase.order \
  --method search_read --domain '[]' --fields '["name","partner_id","amount_total","state"]' --limit 5

# Or import in your own script:
#   from odoo_connect import connect
#   uid, models, cfg = connect("samaya")
#   models.execute_kw(cfg['db'], uid, cfg['pw'], 'purchase.order', 'search', [[]])
```

**If connection fails:** the helper prints the exact cause (server unreachable / bad API key /
wrong DB / missing env file) with the fix. The Samaya credential is an **API key** (Odoo →
Settings → Account Security → Developer API Keys), stored as `ODOO_API_KEY` in the env file.
Requires Python 3 only (stdlib `xmlrpc.client` — no pip install needed).

## At a Glance — Pick the Right Instance First

| | **Moqtana** (factory) | **Samaya** (main co.) |
|---|---|---|
| URL (direct) | `http://167.99.224.43:8069` | `https://samayainv.odoo.com` |
| URL (web, HTTPS) | `https://odoo.moqtana.sa` | — |
| Web login flow | Navigate to `odoo.moqtana.sa` → website frontend → click "Sign in" → Odoo login form (Email + Password) | Direct Odoo login page at samayainv.odoo.com |
| DB | `moqtana` | `peerless-tech-samaya-18-0-18447146` |
| Use for | Projects, mfg, inventory, HR, sales | POs, RFQs, invoices, accounting |
| Auth login | `mohamedsultanabbas@gmail.com` | `sultan@samayainvest.com` |
| Password source | user supplies at runtime | `~/.config/samaya/odoo.env` (user supplies) |
| User aliases | "اودو المصنع", "factory Odoo" | "اودو سمايا" |

**⚠ "اودو سمايا وليس اودو المصنع" = Samaya, NOT Moqtana.** Both use XML-RPC at `/xmlrpc/2/common` (auth) + `/xmlrpc/2/object` (data). Confirm the instance before any write op. Never hardcode passwords — they are supplied at use time.

**⚠ Aseer Museum (متحف عسير الإقليمى, project 219) is on SAMAYA Odoo, NOT Moqtana.** Despite being a museum project, it lives under Samaya's Odoo with POs and procurement. "Use for: Projects" in the table above points at Moqtana generally, but Aseer is the exception. Always check which instance a project actually lives on before querying.

## ⚠ Language: English Only for Output

**All Odoo queries, task names, and project descriptions must be in English.** When the user says "english only" after you showed Arabic text — that means fix it immediately and do not show Arabic in future output. This includes:
- Project names in search results — if they're stored in Arabic, translate/romanize for display
- Task names — keep as-is in the DB but present with English descriptions
- Error messages and status reports — always English

## Browser-Based Interaction (Moqtana Odoo)

For Moqtana Odoo, some operations are better done via the browser UI than XML-RPC (e.g., viewing Kanban boards, adding subtasks inline, checking progress percentages).

### Login Flow (Moqtana)
1. Navigate to `https://odoo.moqtana.sa` → website frontend loads with Moqtana branding
2. Click **"Sign in"** link (usually ref=e20) → Odoo login form appears
3. Enter Email: `mohamedsultanabbas@gmail.com` + Password (user supplies at runtime)
4. Click **"Log in"** → Odoo dashboard loads

### ⚠ Password Handling
- The password (`1batagoniaA`) must be entered by the user at runtime — **DO NOT persist it to disk** without explicit user consent
- The `~/.config/moqtana/odoo.env` file should NOT be created automatically
- If the user provides the password, use it in the current session only
- If they want it saved, they'll tell you explicitly

### Navigation Pattern (Browser)
1. Click **"Project"** in the top navbar → Projects Kanban view
2. Locate the project card (e.g., `1039 — Darin Visitor Center (قلعة دارين)`)
3. Click the card → opens project task Kanban (stages as columns)
4. Click a task card → opens task form view (side panel or full form)

### Adding a Subtask (Browser)
1. Open the parent task (e.g., `1. [Architecture Design]`)
2. Click the **"Sub-tasks"** tab in the task form
3. Click **"Add a line"** button — a new row appears with editable cells
4. Type the subtask title (e.g., `1.2 Award to Design Office`) in the title textbox
5. Click **"Save manually"** button (appears when edit mode is active)
6. The sub-task counter auto-updates (e.g., from `1 / 1 (100%)` to `1 / 2 (50%)`)

### Sub-task Numbering Convention
- **Package tasks**: `1. [Architecture Design]`, `2. [Electrical Design]`, etc.
- **Subtasks**: `1.1 Prepare technical proposal...`, `1.2 Award to Design Office`
- Subtask counter shows `completed / total` and percentage
- Checkbox column marks completion status
- Assignee can be set per subtask

### ⚠ Browser Limitations
- The initial "Sign in" click navigates through the Moqtana website frontend — the resulting login form (Email + Password fields) may have different ref IDs each session
- Snapshot may return empty page briefly after login — navigate to `/odoo/` again to reach the dashboard
- The project list uses Kanban columns (stages) — tasks under different stages appear in different columns
- The save button only appears when the form is in edit mode (after "Add a line" or other edit triggers)

## Odoo Instances — Two Distinct Systems

This user operates TWO separate Odoo instances. **Do NOT confuse them.**

### Moqtana Odoo (Factory / Project Management)
- **URL (direct):** `http://167.99.224.43:8069` (DigitalOcean droplet)
- **URL (web, HTTPS):** `https://odoo.moqtana.sa` (Nginx Proxy Manager — primary access via browser)
- **Web login flow:** Navigate to `odoo.moqtana.sa` → website frontend → click "Sign in" → Odoo login form (Email + Password)
- **Database:** `moqtana`
- **Primary use:** Project management, manufacturing, inventory, HR, sales
- **Company:** Moqtana Museums & Consultancy (مقتنى للمشاريع)
- **Auth:** Admin email from `~/Documents/01_Odoo/assets/company_data.md`
- **API:** XML-RPC at `/xmlrpc/2/common` and `/xmlrpc/2/object`
- **Alias in user speech:** "اودو المصنع", "Moqtana Odoo", "factory Odoo"

### Samaya Odoo (Main Company — Purchasing & Invoicing)
- **URL:** `https://samayainv.odoo.com`
- **Database:** `peerless-tech-samaya-18-0-18447146`
- **Primary use:** Purchase Orders, invoices, main company accounting
- **Company:** Samaya Investment (شركة سمايا الإستثمارية)
- **Auth:** Admin email `sultan@samayainvest.com` — password from `~/.config/samaya/odoo.env`
- **API:** XML-RPC at `/xmlrpc/2/common` + `/xmlrpc/2/object` (same pattern as Moqtana)
- **Alias in user speech:** "اودو سمايا", "Samaya Odoo"

**⚠ CRITICAL:** When the user says "اودو سمايا وليس اودو المصنع" they mean Samaya Odoo (samayainv.odoo.com) NOT the factory Moqtana instance. Verify which instance before executing any Odoo operation. Default for project management tasks is Moqtana; default for purchasing/invoicing is Samaya.

## Samaya Odoo — Purchase Order Creation (with Arabic Details)

Purchase Orders in Samaya Odoo use the standard `purchase.order` model via XML-RPC.

`references/samaya-odoo-reference.md` — compact reference sheet of all key IDs (currencies, taxes, categories, UOM, projects, vendors).
`references/odoo-task-fields-discovered.md` — `progress` scale (0.0-1.0 not 0-100), `state` options, `display_mark_as_done_primary`, `date_assign`, SSL cert bypass, Kanban subtask filter, task creation checklist.

### Key Reference IDs (Samaya Odoo)

| Item | ID | Notes |
|------|----|-------|
| Currency SAR | 150 | NOT 1 (1 = USD) — verify after create, update if needed |
| 15% Purchase Tax | 5 | Use for PO lines (supplier's 15% VAT) |
| Subcontracts category | 640 | Use for service/consulting procurement |
| UOM Units | 1 | Standard unit of measure |
| Project: متحف عسير الإقليمى | 219 | Aseer Museum project ID |

### PO Creation Pattern (Service/Subcontract)

```python
# 1. Create service product (if new)
product_id = models.execute_kw(db, uid, password, 'product.product', 'create', [{
    'name': 'أعمال الدراسات والتصميم الإنشائي لمتحف عسير الدولي',
    'type': 'service',
    'categ_id': 640,            # Subcontracts
    'lst_price': 15000.0,
    'standard_price': 15000.0,
    'uom_id': 1,
    'uom_po_id': 1,
}])

# 2. Create PO with full Arabic notes
po_id = models.execute_kw(db, uid, password, 'purchase.order', 'create', [{
    'partner_id': 2640,          # Vendor ID
    'project_id': 219,           # متحف عسير الإقليمى
    'date_order': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'currency_id': 150,          # SAR
    'payment_term_id': 4,        # 30 Days (or customize via notes)
    'origin': 'عرض سعر رقم 26519 - 19 مايو 2026',
    'notes': """<div style="direction: rtl;">
<h4>نطاق الأعمال</h4>
<ul>
<li>المرحلة الأولى – دراسة وتحليل المبنى القائم</li>
<li>المرحلة الثانية – دراسة التعديلات المطلوبة</li>
</ul>
<h4>شروط الدفع:</h4>
<ul>
<li>60% دفعة مقدمة عند توقيع العقد</li>
<li>40% عند الانتهاء والتسليم النهائي</li>
</ul>
</div>""",
    'order_line': [(0, 0, {
        'product_id': product_id,
        'name': 'وصف تفصيلي للخدمة',
        'product_qty': 1.0,
        'product_uom': 1,
        'price_unit': 15000.0,
        'taxes_id': [(6, 0, [5])],   # 15% Purchase Tax
    })]
}])
```

### ⚠ PO Pitfalls
- **Currency:** Default is USD (ID 1). Always set `currency_id: 150` for SAR explicitly after creation if the default is wrong.
- **Notes are HTML:** Use `<div style="direction: rtl;">` for Arabic text rendering.
- **Two-installment payments:** Odoo may not have a built-in "60% + 40%" payment term. Document the payment schedule in `notes` (HTML field) rather than relying on `payment_term_id`.
- **PO state:** Created PO is in `draft` state. The user confirms and approves from the Odoo UI.
- **Arabic-only text preference:** For formal document fields (notes, descriptions, origin), avoid mixing English/Latin characters within Arabic sentences. The user reported that mixed scripts cause display/rendering issues ("الجملة بتقلب"). Write numbers as Arabic words (خمسة عشر ألف instead of 15000). Use pure Arabic text in all note and description fields.

## Samaya Odoo — Supplier & RFQ Creation

For procurement workflows beyond basic PO creation (supplier research → create supplier → create product → create RFQ → PO), see:

`references/samaya-odoo-procurement-workflow.md`

### Quick: Supplier Creation
VAT (Tax ID) is **required** for company-type partners in KSA localization. Use a placeholder if unknown.

### Quick: RFQ Creation
RFQs are `purchase.order` in `draft` state. Use USD (ID 1) for international suppliers (no tax), SAR (ID 150) for KSA suppliers (with 15% Purchase Tax ID 5).

## Infrastructure

| Item | Value |
|---|---|
| Host | `167.99.224.43` (DigitalOcean droplet, 1 vCPU / 2 GB / 50 GB) |
| Web domain (HTTPS) | `https://odoo.moqtana.sa` — Nginx Proxy Manager frontend. Login flow: browse domain → website frontend → click "Sign in" → Odoo login (Email + Password) |
| Stack | Docker Compose at `/opt/odoo` — services `odoo` (container `odoo_app`), `db` (postgres:15 `odoo_db`), `npm` (Nginx Proxy Manager) |
| DB | `moqtana` (full Community suite + `l10n_sa`, `base_automation`, `project_mrp`/`mrp_account`) |
| Ports | 8069 (Odoo HTTP), 81 (NPM admin), 80/443 (NPM proxy) |
| Local mirror | `/Users/mohamedessa/Documents/01_Odoo` (config, scripts, data) |
| Playbook | `MOQTANA_ODOO_SETUP.md` (full deployment doc) |
| Scripts | `/Users/mohamedessa/Documents/01_Odoo/scripts/` — 17 idempotent `odoo shell` reproduction scripts (run order in its `README.md`) |

## Authentication Methods (in priority order)

### 1. SSH → Docker exec (most capable)
SSH to the droplet, then:
```bash
cd /opt/odoo
docker compose exec -T odoo odoo shell -d moqtana --log-level=warn < script.py
```
⚠ SSH access currently blocked from this machine (no valid key). User must provide SSH key or password.

### 2. XML-RPC API (Samaya — SSL cert workaround)

Samaya Odoo (`samayainv.odoo.com`) uses HTTPS with a certificate chain that macOS Python's built-in SSL may not trust. Bypass with `ssl._create_unverified_context()`:

```python
import xmlrpc.client, ssl

ctx = ssl._create_unverified_context()
transport = xmlrpc.client.SafeTransport(context=ctx)

common = xmlrpc.client.ServerProxy('https://samayainv.odoo.com/xmlrpc/2/common', transport=transport)
uid = common.authenticate(db, login, password, {})

models = xmlrpc.client.ServerProxy('https://samayainv.odoo.com/xmlrpc/2/object', transport=transport)
```

For Moqtana (HTTP, no SSL issue):
```python
common = xmlrpc.client.ServerProxy('http://167.99.224.43:8069/xmlrpc/2/common')
uid = common.authenticate('moqtana', 'admin', '<password>', {})
```

### 3. JSON-RPC API (direct — preferred when XML-RPC has SSL cert issues on macOS)

macOS Python's built-in SSL may not trust the Odoo server's certificate chain. When XML-RPC fails with `[SSL: CERTIFICATE_VERIFY_FAILED]`, use JSON-RPC with `requests(verify=False)`:

```python
import requests

url = "https://samayainv.odoo.com"
db = "peerless-tech-samaya-18-0-18447146"
user = "sultan@samayainvest.com"
api_key = "<from ~/.config/samaya/odoo.env>"

# 1. Authenticate
auth = {
    "jsonrpc": "2.0", "method": "call",
    "params": {"service": "common", "method": "login", "args": [db, user, api_key]},
    "id": 1
}
r = requests.post(f"{url}/jsonrpc", json=auth, verify=False, timeout=15)
uid = r.json().get('result')
if not uid:
    print(f"Auth failed: {r.text[:200]}")

# 2. Execute operations (search_read, create, write, etc.)
payload = {
    "jsonrpc": "2.0", "method": "call",
    "params": {
        "service": "object",
        "method": "execute_kw",
        "args": [
            db, uid, api_key,
            'purchase.order',
            'search_read',
            [[['name', 'in', ['P01358', 'P01151']]]],
            {'fields': ['id', 'name', 'partner_id', 'amount_total', 'state']}
        ]
    },
    "id": 2
}
r = requests.post(f"{url}/jsonrpc", json=payload, verify=False, timeout=15)
results = r.json().get('result', [])

# Build a PO-reference → internal-ID map for hyperlinks
po_id_map = {r['name']: r['id'] for r in results}
```

**⚠ SSL Warning Suppression:** `verify=False` produces `InsecureRequestWarning` from urllib3. This is cosmetic — the data still flows over HTTPS, just without local cert validation. Acceptable for our macOS environment where Python can't verify the Odoo server's cert.

**Key differences from XML-RPC:**
- Uses `requests.post(url/jsonrpc)` with JSON payload, not `xmlrpc.client.ServerProxy`
- Same `execute_kw` args format as XML-RPC (db, uid, key, model, method, args, kwargs)
- Returns standard JSON response `{"jsonrpc":"2.0","result":[...],"id":2}`
- No custom SSL transport needed — `verify=False` is cleaner than `ssl._create_unverified_context()`

### 4. JSON-RPC API (via web session — fallback)
Login via web form first to get session cookie, then call `/web/dataset/call_kw`.

### 5. Database Backup (fallback — needs master password)
Master password (`admin_passwd` from `config/odoo.conf`) is required for `dump`, `duplicate_database`, etc.
If it fails with "Access Denied", the password was changed after deployment.

## Browser SPA Fallback → Use XML-RPC for Admin Config

The Odoo web client is a JS SPA. The accessibility snapshot often returns empty pages for the backend dashboard. When the browser tool can't render the UI:

**Switch to XML-RPC API** (`xmlrpc.client` from stdlib) for admin/config operations instead of fighting the browser. This works for:
- Reading/creating/updating `ir.mail_server` (outgoing email)
- Reading/updating `ir.config_parameter` (system settings)
- CRUD on any model

Connection pattern:
```python
import xmlrpc.client
url = 'http://167.99.224.43:8069'
db = 'moqtana'
user = 'mohamedsultanabbas@gmail.com'
pw = '<user-provided-at-runtime>'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, user, pw, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
```

## Email / SMTP Configuration via XML-RPC

Configure outgoing mail servers without the browser UI.

### Outgoing Mail Server (`ir.mail_server`)

Fields:
| Field | Type | Value for smtp-relay.gmail.com |
|-------|------|-------------------------------|
| `name` | char | "Moqtana ERP" |
| `smtp_host` | char | "smtp-relay.gmail.com" |
| `smtp_port` | integer | 587 |
| `smtp_encryption` | selection | `'starttls'` (NOT `'ssl'` or `'none'`) |
| `smtp_user` | many2one (False) | `False` for empty/no auth |
| `smtp_pass` | char (False) | `False` for empty/no auth |
| `from_filter` | char | "erp@moqtana.sa" — only emails matching this from-address use this server |
| `active` | boolean | True |

```python
# Check existing
models.execute_kw(db, uid, pw, 'ir.mail_server', 'search_read',
    [[]], {'fields': ['id', 'name', 'smtp_host', 'smtp_port', 'smtp_encryption', 'smtp_user', 'from_filter']})

# Create
models.execute_kw(db, uid, pw, 'ir.mail_server', 'create', [{
    'name': 'Gmail SMTP Relay (Moqtana)',
    'smtp_host': 'smtp-relay.gmail.com',
    'smtp_port': 587,
    'smtp_encryption': 'starttls',
    'smtp_user': False,
    'smtp_pass': False,
    'from_filter': 'erp@moqtana.sa',
}])

# Update
models.execute_kw(db, uid, pw, 'ir.mail_server', 'write',
    [[server_id], {'smtp_host': 'smtp-relay.gmail.com'}])
```

### Email System Parameters (`ir.config_parameter`)

These system-wide parameters control email routing:

| Key | Value (for Moqtana) | Importance |
|-----|---------------------|------------|
| `mail.default.from` | `erp@moqtana.sa` | **Required** — default sender address |
| `mail.catchall.domain` | `moqtana.sa` | **Required** — domain for catch-all aliases |
| `mail.bounce.domain` | `moqtana.sa` | Optional — where bounces go |

Check and fix:
```python
params_to_fix = {
    'mail.catchall.domain': 'moqtana.sa',
    'mail.default.from': 'erp@moqtana.sa',
    'mail.bounce.domain': 'moqtana.sa',
}
for key, value in params_to_fix.items():
    param_id = models.execute_kw(db, uid, pw, 'ir.config_parameter', 'search', [[('key', '=', key)]])
    if param_id:
        models.execute_kw(db, uid, pw, 'ir.config_parameter', 'write', [[param_id[0]], {'value': value}])
    else:
        models.execute_kw(db, uid, pw, 'ir.config_parameter', 'create', [{'key': key, 'value': value}])
```

### ⚠ Pitfalls
- `smtp_encryption` accepts `'starttls'`, `'ssl'`, or `'none'` — **case-sensitive**. `'STARTTLS'` won't work.
- `smtp_user` and `smtp_pass` must be `False` for empty (Python `False`, not the string `"False"`). Setting them to `""` (empty string) is equivalent.
- The `from_filter` controls which outbound email addresses match this server. If emails are sent from `info@moqtana.sa` but the filter is `erp@moqtana.sa`, they won't route through this server.
- DigitalOcean blocks outbound SMTP on ports 25/465/587. `smtp-relay.gmail.com` works because it's Google's relay (not a direct SMTP submission) — it only accepts from authorized Google Workspace domains.
- Company email (`res.company`) and `mail.default.from` should be consistent. Moqtana company email is `info@moqtana.sa` but outgoing ERP emails use `erp@moqtana.sa`.

## Successful Query Pattern (XML-RPC)

This is the verified working approach when SSH is unavailable:

```python
import xmlrpc.client

url = 'http://167.99.224.43:8069'
db = 'moqtana'
login = 'mohamedsultanabbas@gmail.com'  # from assets/company_data.md
password = '<user-provided-password>'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, login, password, {})

if uid:
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    records = models.execute_kw(db, uid, password, 'project.project', 'search_read', [[]], {
        'fields': ['id', 'name', 'user_id', 'partner_id', 'stage_id', 'date_start', 'date'],
        'order': 'id asc'
    })
```

Key points:
- Admin login is the **email** from `company_data.md`, not `admin`
- XML-RPC endpoint: `/xmlrpc/2/common` for auth, `/xmlrpc/2/object` for data
- Use `execute_kw` with model name, method, args, kwargs
- Fields with m2o relationships return `[id, display_name]` tuples
- JSON-RPC via `/web/dataset/call_kw` also works but needs session cookie + CSRF token

## Local Project Folders (Tqanny)

The user's working project repository is at:
```
/Users/mohamedessa/Library/CloudStorage/OneDrive-Personal(2)/Work/PWork/01_PROJECTS/Tqanny_Projects/
```

Folder convention: `NN_ProjectName` (e.g. `01_Darin_Visitor_Center`, `04_Al_Faw`).
Each project folder has a standard subfolder structure:
```
00_Admin/  01_CLIENT_INPUTS/  02_Submittals/  03_Design/  04_Drawings/
05_Specifications/  06_BIM/  07_Meetings/  08_Schedules/  09_Site/
10_Calculations/  11_Standards_&_References/  99_Templates/
```

Active Tqanny project folders (as of 2026-06-01):
| # | Folder | Name |
|---|--------|------|
| 01 | `01_Darin_Visitor_Center` | Darin Visitor Center |
| 02 | `02_Shobra` | Shobra |
| 03 | `03_Albiaa` | Albiaa |
| 04 | `04_Al_Faw` | Al Faw Visitor Center (has PROJECT_MEMORY.md) |
| 05 | `05_Alrakaa_Center` | Alrakaa Center |
| 06 | `06_Antara_Rock` | Antara Rock |
| 07 | `07_Said_Alshohadaa` | Said Alshohadaa |
| 08 | `08_Tabuk_Castle` | Tabuk Castle |

Non-project folders: `DOCs/`, `Organization Chart/`, `Tenders/`

These folders are the source of truth for which projects exist; Odoo projects should be created/updated to match this list.

## Creating Records via XML-RPC

### Projects

```python
pid = models.execute_kw(db, uid, password, 'project.project', 'create', [{
    'name': '01 — Project Name',
    'stage_id': 5,          # Portfolio stage ID (see stage reference)
    'user_id': 2,           # Project manager (Mohamed Essa)
    'partner_id': 14,       # Client/partner
    'description': 'Project description copied from folder analysis'
}])
```

New projects automatically inherit the 8 task stages (Brief & Discovery → Concept Design → Design Development → Procurement & Tender → Off-site Manufacturing → Installation & Fitout → Snagging & Commissioning → Handover & Closeout) from the template via the automation rule (script `08_new_project_template_automation.py`). **Tasks and milestones are NOT auto-copied** — you must create them explicitly.

### 🔴 CRITICAL: Decompose User Prompts into Proper Task Structure

When the user gives a prompt to create or update tasks, you must **analyze and decompose** the prompt into distinct activities — do NOT lump multiple activities into one task.

**Rule:** One task = one deliverable/activity. If the user describes work involving different activities, create **separate tasks**.

Example: "submit showcase material sample and coordinate Navisworks/4D simulation" → 2 tasks:
- `SC-003 — Submit showcase material sample` (Stage 39 Procurement)
- `SC-004 — Navisworks / 4D simulation coordination` (Stage 36 DD)

**Every task and subtask MUST have `date_assign` and `date_deadline`.** The user will flag any task missing dates — "planning with no planning without dates."

**KSA Work Week:** Friday and Saturday are the weekend. Never set `date_deadline` on Friday or Saturday. If a deadline falls on Friday → move to Thursday; Saturday → move to Sunday.

**Deadlines must align with the baseline programme.** The user corrected: *"you make deadline date so far always — we should comply with baseline programme and we already late."* Rules:
- Deadlines must be aggressive and reflect actual programme urgency — typically 2-5 working days
- Never set arbitrary 15+ day deadlines
- Check the project baseline programme first for the actual milestone dates
- If the programme is tight (it always is), set tighter deadlines
- Example: a task starting Monday should finish by Thursday, not next month

**When writing task updates, update ALL relevant fields together — not just some:**
- Include: `name`, `description`, `stage_id`, `state`, `progress`, `date_assign`, `date_deadline`
- Never update only `name` without also updating `description` and `stage_id`

### Task Restructuring Procedure (Entire Project)

When asked to restructure all tasks in a project (e.g., convert flat task list to MAIN→SUB hierarchy):

1. **Read all tasks** in the project: `search_read` with `fields=['id', 'name', 'parent_id', 'stage_id', 'user_ids', 'state']`
2. **Analyze and categorize**: Group tasks by type/function. Manufacturing projects → by product type (Furniture, Walls, Display Cases, etc.). Design projects → by discipline (Architecture, Structural, MEP, Lighting, etc.)
3. **Create MAIN package tasks** for each category, with serial numbering: `01 — Category Name`, `02 — Category Name`, etc.
4. **Move existing tasks** under their corresponding MAIN package by setting `parent_id` to the package ID
5. **Check for orphans**: verify no tasks remain as main tasks that should be subtasks (count main tasks and review)
6. **Flatten sub-sub-tasks**: Check for depth-3 nesting (tasks whose parent is itself a subtask). Move them directly under the package: `{'parent_id': package_id}`.\n7. **Re-sequence by status**: Order subtasks so active items appear first. In-progress → done → cancelled. Assign sequence in increments of 10 to leave gaps for future insertions.\n   ```python\n   kids = sorted(kids, key=lambda k: (0 if k['state']=='01_in_progress' else 1 if k['state']=='1_done' else 2, k['id']))\n   for i, k in enumerate(kids):\n       models.execute_kw(db, uid, pw, 'project.task', 'write', [[k['id']], {'sequence': (i+1)*10}])\n   ```\n8. **Set Kanban order**: assign `sequence` field values (1, 2, 3...) matching the serial numbers so Kanban displays in order\n9. **Verify**: re-read the full tree to confirm all tasks are correctly nested

**Stage assignment rules for manufacturing/fit-out projects:**
- Manufacturing items (production orders, fabrication) → Stage 659 (Off-site Manufacturing)
- Procurement items (BOQ, PO, shop drawings, material samples) → Stage 39 (Procurement)
- Design/engineering items (architectural, MEP, graphics, civil defense) → Stage 36 (DD)
- Always match the stage to the nature of the task, not just keep defaults

### Kanban Ordering via Sequence Field

Tasks in Kanban view are ordered by the `sequence` field (lower = first). After restructuring, set sequence values to match serial numbering:

```python
serial_seq = {
    3240: 1,  # 01 — Category
    3241: 2,  # 02 — Category
    # ...
}
for tid, seq in serial_seq.items():
    models.execute_kw(db, uid, pw, 'project.task', 'write', [[tid], {'sequence': seq}])
```

**⚠ `ir.actions.act_window` does NOT have an `order` field in Odoo 18 cloud instances.** Attempting to read/write `order` on action models will raise `ValueError: Invalid field 'order'`. Kanban ordering is entirely controlled by `project.task.sequence` — no action-level override exists in Samaya Odoo. If Kanban shows wrong order, the issue is always duplicate/invalid sequence values, not the action configuration.

**⚠ Action IDs are instance-specific.** The numeric IDs of `ir.actions.act_window` records (e.g. 506, 517) vary per Odoo installation. Never hardcode them across instances. To discover the correct IDs for each instance:

```python
action_ids = models.execute_kw(db, uid, pw, 'ir.actions.act_window', 'search',
    [[['res_model', '=', 'project.task']]])
actions = models.execute_kw(db, uid, pw, 'ir.actions.act_window', 'read',
    [action_ids], {'fields': ['id', 'name', 'view_mode', 'domain']})
```

### Batch Subtask Sequencing

When sequencing hundreds of subtasks across 30+ parent packages, process each parent's children by their current display order and assign sequence values in increments of 10:

```python
parents = models.execute_kw(db, uid, pw, 'project.task', 'search',
    [[['project_id', '=', 219], ['parent_id', '=', False]]])

for pid in parents:
    kids = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
        [[['parent_id', '=', pid]]],
        {'fields': ['id', 'sequence'], 'order': 'sequence ASC, id ASC'})
    
    for i, kid in enumerate(kids):
        new_seq = (i + 1) * 10
        if kid['sequence'] != new_seq:
            models.execute_kw(db, uid, pw, 'project.task', 'write',
                [[kid['id']], {'sequence': new_seq}])
```

This is the safe pattern for 250+ tasks — 10-series gaps let you manually insert items later.

### BOQ-to-Odoo Mapping Workflow

When mapping a project's BOQ against Odoo tasks:

1. **Read the latest BOQ** (find in project folder under `B.O.Q/` or `01_Schedule_and_BOQ/`)
2. **Categorize BOQ items** by division (DIV 5 = Steel, DIV 6 = Wood, DIV 8 = Doors, DIV 9 = Finishes, DIV 12 = Furniture, Electrical, Signage, etc.)
3. **Map each BOQ category** to existing Odoo packages:
   - Paint items → check if Painting package exists (create if missing)
   - Cladding/ceiling items → Walls, Cladding & Ceiling package
   - Furniture items → Furniture package
   - Signage/LED items → Screens, Signage & LED package
   - Doors → Doors & Glass package
   - Electrical items → create Electrical package if missing
4. **Identify gaps**: BOQ items with no corresponding Odoo task → create new tasks
5. **Present mapping** as a table showing: BOQ Category → Odoo Package → Coverage (✅/⚠/❌)

**Projects and their OneDrive folder paths (Samaya BIM Unit):**

| Odoo ID | Name | Folder Path |
|---------|------|-------------|
| 219 | Aseer Museum | `Aseer-Museum/` |
| 166 | Jalal & Jamal - Jabal Omer | `Jabal Omar- Retails 01 Hadaya Teiba الجلال و الجمال (GND FL)/` |
| 176 | Maalim Al-Haramein - Jabal Omer | `Jabal Omar- Retails 02 Hadaya Teiba معالم الحرمين (BASS FL)/` |
| 121 | Zamzam Museum | `Zamzam -Visitor Center/` |
| 139 | Kher Elkhalek Museum | (check under BIM Unit root) |

When creating any task:
```python
tid = models.execute_kw(db, uid, pw, 'project.task', 'create', [{
    'name': 'Task name',
    'project_id': 219,
    'stage_id': 36,
    'parent_id': parent_id,
    'user_ids': [(4, uid)],
    'state': '1_done',          # or 01_in_progress / 02_changes_requested / 03_approved
    'progress': 1.0,            # 0.0-1.0 scale (NOT 0-100!)
    'date_assign': '2026-06-10', # submission or start date
    'date_deadline': '2026-06-10', # completion or review date
    'display_mark_as_done_primary': True,  # ⚠ UI-only — ignored via API (see pitfall below)
    'tag_ids': [(4, 140)],      # many2many to project.tags
    'description': '<p>Notes</p>',
}])\n```

**Searching for existing tasks by name:**
```python
# Case-insensitive substring match
tasks = models.execute_kw(db, uid, pw, 'project.task', 'search',
    [[['project_id', '=', 219], ['name', '=ilike', '%PL-0057%']]])
# Find tasks under a specific parent
kids = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
    [[['parent_id', '=', parent_id]]],
    {'fields': ['id', 'name', 'state', 'progress']})
```

**Finding users to assign:**
```python
users = models.execute_kw(db, uid, pw, 'res.users', 'search_read',
    [[['login', '=ilike', '%hesham%']]],
    {'fields': ['id', 'name', 'login']})
```

**Date-based task queries (today's assignments/deadlines):**
```python
from datetime import datetime
today = datetime.now().strftime('%Y-%m-%d')

# Tasks assigned or due today (OR across two date fields):
tasks = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
    [[['project_id', '=', 219], '|',
      ['date_assign', '=', today],
      ['date_deadline', '=', today]]],
    {'fields': ['id', 'name', 'stage_id', 'user_ids', 'state', 'progress',
                'date_assign', 'date_deadline', 'parent_id'],
     'order': 'date_assign ASC'})

# Tasks created today:
ctasks = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
    [[['project_id', '=', 219],
      ['create_date', '>=', today],
      ['create_date', '<=', today + ' 23:59:59']]],
    {'fields': ['id', 'name', 'stage_id', 'state']})
```

**Counting tasks:**
```python
main_count = models.execute_kw(db, uid, pw, 'project.task', 'search_count',
    [[['project_id', '=', 219], ['parent_id', '=', False]]])
sub_count = models.execute_kw(db, uid, pw, 'project.task', 'search_count',
    [[['project_id', '=', 219], ['parent_id', '!=', False]]])
```

See `references/odoo-task-hierarchy.md` for the two-level hierarchy pattern, task creation examples, restructuring procedures, and baseline date computation.\nSee `references/odoo-task-fields-discovered.md` for the full field reference including progress scale, tag IDs, and user assignment rules.

### Tasks

```python
tid = models.execute_kw(db, uid, password, 'project.task', 'create', [{
    'name': 'Task name',
    'project_id': 14,           # Odoo project ID
    'stage_id': 12,             # Task stage ID (see stage reference)
    'user_ids': [(4, 2)],       # Assignee — NOTE: user_ids (many2many), NOT user_id!
}])
```

⚠ **Critical field quirk**: The assignee field on `project.task` is `user_ids` (many2many to `res.users`), NOT `user_id`. Use `[(4, user_id)]` syntax for the x2m command (4 = "add to relation").

### Task State (Status)

`project.task` has a `state` field (selection) that controls the task's status badge. Use this to mark tasks done/approved/needs-changes without moving them to a different stage:

```python
# Available selection values (Samaya Aseer project):
# '01_in_progress'     → In Progress (default)
# '02_changes_requested' → Changes Requested
# '03_approved'        → Approved
# '1_done'             → Done
# '1_canceled'         → Cancelled
# '04_waiting_normal'  → Waiting

# Mark as done:
models.execute_kw(db, uid, pw, 'project.task', 'write', [[task_id], {
    'state': '1_done'
}])

# Mark as needs revision:
models.execute_kw(db, uid, pw, 'project.task', 'write', [[task_id], {
    'state': '02_changes_requested'
}])
```

There is also an `is_closed` (boolean) field — set to `True` when the task is fully closed.

### Task Hierarchy Convention (MAIN / SUB Only — Two Levels)

**All projects follow a strict two-level hierarchy.** The intermediate "Stage Package" level (50% Design Package, 90% Design Package, etc.) was removed in a restructuring on 2026-06-15 — deliverables sit directly under their main package.

```
MAIN TASK     → parent_id=False        → visible in Kanban as its own card
└── SUBTASK   → parent_id=Package ID   → hidden (inside parent's Sub-tasks tab)
```

| Level | parent_id | Kanban | Use For |
|-------|-----------|--------|---------|
| MAIN | False | Visible card | Packages, standalone items: "07 — Lighting (SC-02)" |
| SUBTASK | Package ID | Hidden (inside parent) | Deliverables: "LG-001 — Lighting design concept" |

**Pattern (all packages must match this):**

```
MAIN: 07 — Lighting (SC-02)
  ├── LG-001 — Lighting design concept
  ├── LG-002 — Lighting plans and elevations
  └── (no 50%/90%/100%/IFC intermediate tasks)
```

**⚠ NEVER create "Stage Package" intermediate tasks (50% Design Package, 90% Design Package, etc.).** Put deliverables directly under the main package.

### Task Naming Convention

Names must be **standardized and native** — not literal copies of user speech:

```
[MAIN]       NN — [Package Title]               e.g. "05 — Projects Plans"
[SUB]        DOC-CODE — [Standardized Title]     e.g. "PL-0057 — Time Schedule Cost Proposal"
[SUB-SUB]    DOC-CODE-N — [Specific Task]        e.g. "PL-0057-2 — Project Schedule Review (w/ Elshaikh)"
```

**Rules:**
- Document code first (`PL-0057`, `ZD-0056`, `MS-0015`) when applicable
- Em-dash (`—`) separator
- Capitalized standard title — NOT the raw email subject line
- Parenthetical for people/context: `(w/ Elshaikh)`, `(C status)`
- No leading numbering in subtask names (that's the parent's job)

### Mandatory Fields Per Task Creation

Every task MUST include ALL of the following — failing any will get corrected:

```python
tid = models.execute_kw(db, uid, pw, 'project.task', 'create', [{
    'name': 'DOC-CODE — Standardized Title',      # See naming convention above
    'project_id': 219,
    'stage_id': 36,                                # Correct stage per task type
    'parent_id': parent_id or False,               # MAIN=False, SUB=Package ID
    'user_ids': [(4, user_id), (4, user_id)],      # Always assign to correct team member(s)
    'tag_ids': [(4, tag_id)],                      # Plans & Procedures=141, Prequalification=140, etc.
    'date_assign': 'YYYY-MM-DD',
    'date_deadline': 'YYYY-MM-DD',
    'state': '01_in_progress',                     # 1_done / 03_approved / 02_changes_requested
    'progress': 0.5,                               # 0.0-1.0 scale
    'display_mark_as_done_primary': True,     # ⚠ UI-only — ignored via API (see pitfall)
    'description': (
        '<h3>Title</h3>'
        '<p><b>Context:</b> Why this task exists, what it relates to</p>'
        '<p><b>Attendees/Assignees:</b> Role-based names</p>'
        '<p><b>Status:</b> Current progress note</p>'
        '<p><b>Ref:</b> Related documents, files, or source</p>'
    ),
}])
```

**Also write a log entry** to the project backlog file:
```
Email_Archive/_aseer_tasks_backlog.md
# Append a table row with: ID | Level | Name | Parent | Assigned | Dates | Tags | Progress
```

## Batch Subtask Creation

When adding 20+ plan documents as subtasks under a parent task, create them in a loop:

```python
tasks = [
    ('Plan Name 1', 'Description with CG status', '1_done'),
    ('Plan Name 2', 'Description', '02_changes_requested'),
]
for name, desc, state in tasks:
    tid = models.execute_kw(db, uid, pw, 'project.task', 'create', [{
        'name': name,
        'project_id': 219,
        'stage_id': 36,          # DD Stage (verify ID per project)
        'parent_id': parent_id,  # Parent task ID
        'user_ids': [(4, uid)],
        'state': state,
        'description': f'<p>{desc}</p>',
    }])
```

### Parent/Child Task Pattern — "Projects Plans"

When creating a planning/documentation parent task with subtasks (e.g., "Projects Plans" → "Sustainability"):

```python
# Stage ID 36 = "02 Design Development (DD) Stage" (Samaya Aseer project)
# Check the actual stage ID first — it varies per project instance

# 1. Create parent task (Projects Plans)
parent_id = models.execute_kw(db, uid, pw, 'project.task', 'create', [{
    'name': 'Projects Plans',
    'project_id': 219,       # Aseer Museum
    'stage_id': 36,           # DD Stage
    'description': f'Main task for project plans management.\n\nCreated: {today}',
}])

# 2. Create sub-task with timeline in HTML description
sub_id = models.execute_kw(db, uid, pw, 'project.task', 'create', [{
    'name': 'Sustainability',  # team/discipline name
    'project_id': 219,
    'stage_id': 36,
    'parent_id': parent_id,
    'description': '<h3>Timeline</h3><ul><li><b>YYYY-MM-DD</b> — Description of work done</li></ul>',
}])
```

⚠ **Sub-tasks use `parent_id`** (many2one to project.task), NOT a different field.

### Partners (Clients)

```python
pid = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
    'name': 'هيئة التراث — Heritage Commission',
    'company_type': 'company',
    'country_id': 189,          # Saudi Arabia
    'phone': '+966 11 000 0000',
    'email': 'info@example.sa',
}])
```

Country ID for Saudi Arabia is `189` in the standard Odoo 18 dataset.

## Stage ID Reference

### Portfolio Stages (`project.project.stage`)

| ID | Name | Sequence | Folded |
|----|------|----------|--------|
| 1 | Lead / Enquiry | 10 | No |
| 5 | Tender / Bid | 20 | No |
| 6 | Awarded | 30 | No |
| 2 | In Progress | 40 | No |
| 7 | On Hold | 50 | No |
| 3 | Completed | 60 | Yes |
| 4 | Lost / Cancelled | 70 | Yes |

### Task Stages (`project.task.type`)

| ID | Name | Sequence |
|----|------|----------|
| 9 | Brief & Discovery | 10 |
| 10 | Concept Design | 20 |
| 11 | Design Development | 30 |
| 12 | Procurement & Tender | 40 |
| 17 | Off-site Manufacturing | 45 |
| 14 | Installation & Fitout | 60 |
| 15 | Snagging & Commissioning | 70 |
| 16 | Handover & Closeout | 80 |

Use stage ID `12` (Procurement & Tender) for tasks during tender/bid phase. Use `9` (Brief & Discovery) for very early-stage pre-award tasks. Move to `10`/`11` as design progresses.

## Custom Fields via XML-RPC

Custom fields can be created programmatically on any model using `ir.model.fields`. This does NOT require enabling debug mode — it works with any user who has the "Technical Features" group (which the admin superuser has).

**Critical**: `model_id` must be the integer ID from `ir.model`, NOT the model name string. Find it first:

```python
model = models.execute_kw(db, uid, password, 'ir.model', 'search_read',
    [[['model', '=', 'project.project']]], {'fields': ['id', 'name']})
# → [{'id': 701, 'name': 'Project'}]
```

Then create the field:
```python
field_id = models.execute_kw(db, uid, password, 'ir.model.fields', 'create', [{
    'model_id': 701,             # Numeric ID from ir.model (NOT 'project.project'!)
    'name': 'x_project_code',     # Field name — must start with x_ for custom fields
    'field_description': 'Project Code',
    'ttype': 'char',              # One of: char, integer, float, boolean, date, datetime, many2one, text, selection, etc.
    'state': 'manual',            # 'manual' = custom user-created field
    'required': False,
    'size': 20,                   # Only for char fields
}])
```

The field is immediately available for read/write — no server restart needed:
```python
models.execute_kw(db, uid, password, 'project.project', 'write', [[proj_id], {'x_project_code': 'CODE-001'}])
records = models.execute_kw(db, uid, password, 'project.project', 'read', [[proj_id]], {'fields': ['id', 'x_project_code']})
```

## Project Code Convention

See `references/project-codes.md` for the full project code register. The naming convention follows the document reference codes already established in each project's RFP/ER/SOW documents:

- Museum/VC projects: `**CITY-VC` or `**CITY-VIC` (e.g. DAR-VIC, SHO-VIC, TAB-VC)
- Archaeological centers: `**CITY-ARC` (e.g. ARA-ARC)
- Heritage sites: `**CITY-SQ` (e.g. SAH-SQ)

When generating a new code, search the project's existing document refs (RFP/ER/SOW filenames) for the established abbreviation.

## Odoo → Local Folder Mapping (Odoo Tasks MD)

After creating Odoo projects and tasks, create a local mapping file for each project:

1. Create `Odoo Tasks/` subfolder in the project's local directory
2. Create `Odoo_Tasks_Map.md` with project metadata (code, Odoo ID, stage, manager, direct URL) and a table of all tasks with their stages and status
3. This gives the user a local reference that stays synced with the folder structure

```python
md_content = f'''# Project Name

| Field | Value |
|-------|-------|
| **Project Code** | `CODE` |
| **Odoo Project ID** | `{pid}` |
| **Stage** | Current Stage |
| **Odoo URL** | `http://167.99.224.43:8069/web#id={pid}&model=project.project&view_type=form` |

## Odoo Tasks ({count})

| # | Task | Stage | Status |
|---|------|-------|--------|
| 1 | Task name | Brief & Discovery | 🔴 Pending |
'''
```

## Task Stage Management (`project.task.type`)

Create custom task stages and link them to specific projects. Stages appear as columns in the task Kanban view.

### Creating a Stage

```python
# Create a new stage and link it to project(s) in one call
stage_id = models.execute_kw(db, uid, password, 'project.task.type', 'create', [{
    'name': '05 On Site Work',
    'sequence': 4,              # Column order in Kanban
    'project_ids': [(6, 0, [309])],  # (6, 0, [ids]) = SET relation
}])
```

⚠ **Accepted fields on `project.task.type`:** `name`, `sequence`, `project_ids`, `fold` (folded/collapsed in Kanban), `description`. The `description` field does NOT exist on `project.task.type` — passing it will raise `ValueError: Invalid field 'description'`.

### Linking an Existing Stage to a Project

```python
# (4, id) = ADD to relation
models.execute_kw(db, uid, password, 'project.task.type', 'write', [stage_id, {
    'project_ids': [(4, 309)]
}])
```

X2M command reference:
- `(0, 0, vals)` — create new record inline
- `(4, id)` — add existing record to relation
- `(6, 0, [ids])` — replace all with the given IDs (set)

### Moving Tasks Between Stages

```python
# Move one or more tasks to a different stage
models.execute_kw(db, uid, password, 'project.task', 'write', [
    [task_id_1, task_id_2, ...],  # list of task IDs
    {'stage_id': new_stage_id}
])
```

This is useful when reclassifying tasks (e.g., from Design Development to On Site Work).

## Task Investigation & Evidence-Based Update

When a user asks about work done on a specific task (e.g. "update ID 3215 with efforts we have done"), use this workflow to find real evidence before updating:

### Phase 1 — Search for evidence

```python
# 1. Search past sessions for the task ID or related keywords
# (Use the session_search tool, not execute_code)
# session_search(query="3215 MEP Designer scope", limit=5)
#
# 2. Search related documents on the filesystem — SCOPE_REQUEST, SPEC, SITUATION_REPORT etc.
# search_files(path=project_path, pattern="MEP Designer", file_glob="*.md")
#
# 3. Check Outlook for related emails (sender, subject, doc code)
# sqlite3 the Outlook DB with doc codes or keywords
#
# 4. Read the actual evidence files to confirm what was produced
# read_file(project_subcon_folder/_MANAGER_DASHBOARD/SITUATION_REPORT.md)
```

### Phase 2 — Compile description

Build the task description as structured HTML with:
- **Status line** (what was achieved)
- **Bullet list of actual files produced** (path + what they contain)
- **Bullet list of procurement/candidate status** (who's involved, current state)
- **Key references** (paths/folder links)
- Cite exact doc codes, dates, candidate names — never vague claims

```python
desc = """<h3>Prepare Final Scope of Work — MEP Designer Consultant</h3>

<p><b>Status:</b> Complete — comprehensive scope document produced.</p>

<p><b>Work Completed:</b></p>
<ul>
<li><b>SCOPE_REQUEST.md</b> — 12 scope sections covering Mechanical, Electrical,
Plumbing, Fire Protection, ELV, Telecom/IT, Existing Services Survey, etc.</li>
<li><b>SCOPE_REQUEST.docx</b> — A4 print-ready formal document</li>
<li><b>SITUATION_REPORT.md</b> — Executive summary with candidate comparison</li>
<li><b>MOC-ASEER-SAM-SOW-SC-013_R00_Scope_of_Work_MEP_Designer.docx</b> — Formal SOW</li>
</ul>

<p><b>Current Procurement Status:</b></p>
<ul>
<li>ITC — contract ON HOLD (variation claim)</li>
<li>3 candidates: AD Engineering, Bluehaus, SG Group</li>
</ul>

<p><b>Key References:</b></p>
<ul>
<li><code>Subcontractors/13_MEP_Designer/_MANAGER_DASHBOARD/</code></li>
</ul>"""
```

⚠ **Never use `/tmp` paths in descriptions** — always reference the final OneDrive project path (see pitfall above).

### Phase 3 — Update the task

```python
models.execute_kw(db, uid, pw, 'project.task', 'write', [[task_id], {
    'state': '1_done',          # or 03_approved / 02_changes_requested
    'progress': 1.0,            # 0.0-1.0 scale
    'display_mark_as_done_primary': True,         # ⚠ UI-only — ignored via API
    'description': desc,        # HTML description from Phase 2
    'date_assign': '2026-06-13',
    'date_deadline': '2026-06-14',
}])

# Verify the update:
v = models.execute_kw(db, uid, pw, 'project.task', 'read',
    [[task_id]], {'fields': ['state', 'progress', 'display_mark_as_done_primary']})
print(f"Verified: state={v[0]['state']}, progress={v[0]['progress']}")
```

**Pitfall:** `progress` may not persist in the same `write` call as `state` + `description`. If progress reverts to 0.0 after the first write, issue a second `write` call targeting only `progress`. `display_mark_as_done_primary` is a **UI-only computed field** — it cannot be set via XML-RPC and always returns `False` from the API regardless of what value is written. The real done indicator is `state='1_done'`. Verified across all done tasks in the project — all show `display_mark_as_done_primary=False` via API even though the UI shows the checkmark. Do not waste retries on it.

### ⚠ CG Comment Disposition Status Taxonomy (Stakeholder Plan / Disposition Matrices)

When tracking CG comments in disposition tables, use these statuses consistently:

| Status | Badge | Meaning | When to Use |
|--------|-------|---------|-------------|
| **COVERED** | `badge-low` | Addressed in this revision, awaiting CG review | SMP-scope items where the plan has been updated to address the comment but CG hasn't reviewed the new revision yet |
| **CLOSED** | `badge-pass` | Confirmed by CG in a prior revision | Round 1 comments that CG explicitly accepted. **NEVER** mark a Round 2 item CLOSED unless CG has reviewed and approved it. |
| **SUBMITTAL-PENDING** | `badge-high` | Depends on external submission (CV, PQD, DS) | Items that need a document transfer, prequalification package, or separate submittal — not resolved within the plan itself |
| **IN-PROGRESS** | `badge-low` | Action underway | Items where work is actively in progress but not yet complete |
| **RE-OPENED** | `badge-critical` | Closure withdrawn | A previously closed item that was re-opened because the evidence didn't support closure |

**Rules:**
- Round 1 comments (CG-01 to CG-08): keep CLOSED — CG confirmed these in prior reviews
- Round 2 CRS SMP-scope items: use **COVERED**, not CLOSED (CG hasn't reviewed latest Rev)
- Items requiring external submittals (CV, PQD): use **SUBMITTAL-PENDING**
- **Never change the CG's original comment text** — typos, grammar, formatting preserved exactly. Only the Disposition/Action column is ours to write.
- The status legend block (listing all statuses with explanations) is **not needed** in the plan. The table headers + badge colors are sufficient. Remove it if present.
- **Revision History shows only formal submissions.** Internal iterations (QC blocks, intermediate drafts never sent to CG) do not belong. Only submissions with a transmittal email, DS number, or CG response.
- **QC Sign-off table pattern:** Always show real names (not "Per live KPR") in the QC table. Chain: Prepared By (Technical Office) → Registered (Doc Controller) → Reviewed (QA/QC) → Approved (PD). Names: Mohamed Sultan (Tech Office), Hesham Abdelhamid (Doc Control), Mohamed Samir on behalf (QA/QC), Eng. Waris Sultan (PD).
- **TOC should show sections + pages + roles only.** No CG comment counts, no submittal statuses.

### "Name · Per live KPR" Pattern (In-Plan Personnel References)

For roles with approved personnel in the plan's stakeholder register, use this format:

```
Name · Per live KPR
```

Example: `Eng. Mohamed Ahmed · Per live KPR` (HSSE Manager)

Rules:
- If name is known and approved → show Name + "· Per live KPR"
- If TBC/vacant → show the vacancy status alone (no "· Per live KPR")
- The live KPR is the authoritative source for current names — plan references it but doesn't duplicate

### Revision History Rules

- Only formal submissions: if there's no email evidence of submission to CG/MoC, it was internal
- Internal iterations (QC checks, intermediate drafts) are excluded from the revision table
- The revision number should skip internal versions (e.g. Rev 00 → Rev 01 → Rev 02 where Revs 02-03 were internal is consolidated to Rev 02 being the formal resubmission)
- Real names for Prepared by and Approved by columns — not "Samaya PMO"

### Preserving Excel Formatting During Updates

**CRITICAL: Never rebuild a formatted Excel file from scratch.**
- The user's registers use a unified template with logos, merged cells, colored headers, and specific column widths
- Use openpyxl to copy VALUES only from updated data to the formatted template
- Restore from backup (.bak) if formatting is accidentally lost, then re-apply only data value changes
- Never use a subagent to "rebuild" an Excel file — it will strip all formatting
- Steps: (1) Open backup file (has formatting), (2) Open working file (has corrected data), (3) Copy cell values only from working → backup, (4) Save as final

### ⚠ CG Review Code Reference (Aseer/Samaya Document Submittals)

CG reviews documents using a 4-tier code system on the Document Submittal form:

| Code | Meaning | Task Impact |
|------|---------|-------------|
| **A** | Approved | ✅ Task done — close it |
| **B** | Approved As Noted / with Comments | 🟢 Task done but document has minor notes — mark done/approved |
| **C** | Revise & Re-submit | 🔴 **NOT done** — task stays in_progress. Needs revision and resubmission to CG. |
| **D** | Disapproved / Rejected | ❌ NOT done — needs full rework. |

**Critical rule:** Never mark a task as done just because a revised version has been prepared internally. Code C or D means the task remains open until CG approves (Code A or B). Always verify the actual CG response before closing.

### 🔴 Post-Session Update Rule

After EVERY work session (coding, design, research, document review, etc.):
1. **Update the related Odoo task** — APPEND to existing description with new work completed, progress %, state. Follow the Task Description Rules above.
2. **Log timesheet** via `account.analytic.line` — session duration in hours
3. This applies automatically — the user should not need to ask

### ⚠ Task Description Rules

**Hard rules when writing descriptions:**

- **Project-oriented only** — state facts about the project, nothing about AI or subagents
- **No AI fingerprints** — no "CG comments addressed", "directly addresses comment #1", "per subagent", or similar meta-commentary
- **No icons or emoji** in the HTML
- **Easy English** — grade 6 level, short sentences
- **Short bullet lists** with concrete deliverables. Not explanations
- **Never mention our own process** — no "I did X", "we prepared Y". Just state the deliverable

**Always APPEND to existing description, never replace:**

```python
# 1. Read current description first
current = models.execute_kw(db, uid, pw, 'project.task', 'read', [[task_id]], {'fields': ['description']})
old_desc = current[0].get('description', '')

# 2. Build new content
new_block = '<h4>Update - YYYY-MM-DD</h4><p><b>Done:</b></p><ul><li>Deliverable 1</li><li>Deliverable 2</li></ul><p><b>Next:</b></p><ul><li>Next step</li></ul>'

# 3. Append
updated_desc = old_desc + new_block if old_desc else new_block
models.execute_kw(db, uid, pw, 'project.task', 'write', [[task_id], {'description': updated_desc}])
```



### 🔴 Telegram Approval Required Before Any Update

**Do NOT update any Odoo task without prior Telegram approval.** Steps:

1. Send a Telegram message to the user (home channel `5832026231`) with:
   - Project name
   - Task ID and name
   - Proposed changes (what fields, what values)
2. Ask explicitly for approval
3. **Wait for confirmation** before executing
- After approval, update the task AND log a timesheet entry

## Task descriptions — format rules (user preference)

When updating `project.task` descriptions via Odoo XML-RPC:

- **Project-oriented only** — describe what happened on the project, not what AI agents did or what instructions were given.
- **No AI fingerprints** — never mention "CG comments were addressed", "subagent created", "I have updated", or any meta-commentary about the document creation process.
- **No icons or emoji** — no checkmarks, stars, arrows, progress dots. Plain text only.
- **Easy English, Level 6 max** — short sentences (15-22 words), simple vocabulary.
- **Short bullet lists** — use `<ul><li>` in HTML description field if multiple items.
- **Action-oriented** — state what was Done and what is Next. No commentary about how it was done.

Example correct format:
```python
desc = (
    '<h3>Sustainability - CG Approved Fida as Manager</h3>'
    '<p><b>26 Jun 2026:</b> SOW draft sent to PD Waris for review. Commercial TBC.</p>'
    '<p><b>Done:</b></p><ul>'
    '<li>SOW for Fida drafted and sent to PD</li>'
    '</ul>'
    '<p><b>Next:</b></p><ul>'
    '<li>Finalise commercial terms with Fida</li>'
    '<li>Submit to CG via DC after PD approval</li>'
    '</ul>'
)
```

This applies to ALL write operations: state changes, progress, descriptions, dates, reassignments, and timesheet logging.

### Periodic Status Monitoring (Cron Job)

For ongoing overdue-task tracking across ALL projects:
- **Schedule:** every 2 hours
- **Scope:** ALL projects on Samaya Odoo
- **Checks:** tasks in `01_in_progress` or `02_changes_requested` where `date_deadline < today` (overdue) or `date_deadline = today`
- **Report:** group by project, show task ID, name, deadline, state
- **Delivery:** `telegram:5832026231` (user's Telegram DM)
- **Tools:** `['terminal']` only — read-only, never update

### Adding Chatter Notes (`message_post`)

To add a progress note or status update to the task chatter (not the description field):

```python
msg_id = models.execute_kw(db, uid, pw, 'project.task', 'message_post',
    [task_id], {
        'body': '[YYYY-MM-DD] Description of what was done or status update.',
        'subject': 'Brief subject line (optional)',
        'message_type': 'comment',       # 'comment' = visible note, 'notification' = system note
    })
```

**Why use `message_post` vs `write` on `description`?**
- `message_post` writes to the **chatter** — visible in the task's message history thread, preserves a timeline of updates
- `write` on `description` appends to the **description field** — good for formal deliverable tracking
- Pattern: use `message_post` for progress/status updates, use `description` append for deliverable completion

### ⏱ Timesheet Logging

### Timesheet Logging

After completing work on an Odoo task, log session time via `account.analytic.line`:

```python
from datetime import datetime
# NOTE: Odoo records timesheets in MINUTES, not hours!
# 60 = 1 hour, 90 = 1.5 hours, 30 = 30 min, 120 = 2 hours
ts_id = models.execute_kw(db, uid, pw, 'account.analytic.line', 'create', [{
    'task_id': task_id,
    'project_id': 219,
    'unit_amount': 90,           # MINUTES! 90 = 1.5 hours
    'name': 'Description of work done',
    'date': datetime.now().strftime('%Y-%m-%d'),
}])
```
```

**Rules:** meaningful `name` description, current date, float hours. If no task exists, create one first.

### ⚠ Pitfalls — Timesheets & Progress

- **Timesheet `unit_amount` is in MINUTES, not hours.** Always use minutes: 60 = 1 hr, 120 = 2 hrs, 240 = 4 hrs. Never use decimal hours (1.0, 2.5).

- `progress` may not persist in the same `write` call as `state` + `description`. If it reverts to 0.0, issue a second `write` targeting only `progress`.
- `display_mark_as_done_primary` is a UI-only computed field — cannot be set via API. Real done indicator is `state='1_done'`.
- **Raw API key parsing in `execute_code` can fail if `.env` has `***` placeholders. Use `from odoo_connect import connect` instead.
- **Don't use `ConfigParser` on `.env` files** — The Samaya Odoo credential file (`~/.config/samaya/odoo.env`) uses `KEY=VALUE` format without INI section headers. Python's `configparser.ConfigParser().read()` will fail with `MissingSectionHeaderError`. Read as plain key=value pairs: `dict(line.strip().split('=', 1) for line in f if '=' in line)`. Or use `scripts/odoo_connect.py` which handles this correctly.

**See also:** `references/cg-review-response-workflow.md` for the end-to-end pattern (email → review → Odoo task → timesheet).

### 📋 Plan vs Register Separation

When updating project documents, follow this rule:

| Document | Contains | Authority |
|----------|----------|-----------|
| **Plan** (SMP, PEP, DMP, etc.) | **Roles, responsibilities, interfaces, procedures** | Updated via revision cycle |
| **Register** (KPR, Stakeholder Register, etc.) | **Actual names, approval dates, CV refs, statuses** | Live document — updated continuously |

**Rules:**
- Plans define **what** the role does — never embed individual names. Reference the live register: "Per live KPR."
- Registers track **who** holds the role, approval status, CV references, and dates.
- When personnel change, update the register — not the plan. The plan only gets a new revision when role definitions or procedures change.
- Exception: Notable departures/appointments can be noted in the revision history of the plan but the name lives in the register.
- **Revision History shows only formal submissions.** Internal iterations (QC blocks, intermediate drafting rounds that were never sent to CG) do not belong in the revision history table. Only submissions with a transmittal email, DS number, or CG response go in. Rule: if there's no email evidence of submission, it was internal.
- **CG Comment text is sacred.** In disposition matrices, the CG Comment column must contain the EXACT text from the CG response PDF — typos, grammar, formatting preserved. Never summarize, rewrite, or "clean up" what the CG wrote. Only the Disposition/Action column is ours to write.
- **Plan documents reference live registers for names.** The QC Sign-off table (§1.3) and Revision History (§1.1) are exceptions — these need real names (who prepared, who reviewed, who approved). Use the user's name for prepared-by, their team members for review/approval.

### ⚠ Pre-Flight Check Before Marking Done (Avoid False Closures)

Before setting state=`1_done` or `03_approved`, always verify:

1. **Read the actual CG response** (PDF in the document's `02_CG_Responses/` folder) — do not rely on task names like "Finalization" or assumptions
2. **Check the approval code on the DS form** — if Code C or D, the task is NOT done
3. **Check if the revised version was actually submitted** — search Outlook emails and the project folder for transmittal/submission evidence
4. **Check Outlook for follow-up emails** — search for the document code after the last known CG response date
5. **Only close when** CG has issued Code A or B, or the resubmission cycle is complete with no remaining CG action

**Pitfall:** A task named "Finalization" or "Rev.02" means preparing the revision, submitting it, AND getting CG approval. The document may be prepared internally (70% complete) but the task isn't done until CG signs off.

**Where to find CG responses:**
```
Docs/02_Plans_and_Procedures/[plan_folder]/02_CG_Responses/
  ├── CG_STATUS.md                          ← summary of all CG responses for that document
  ├── MOC-MUS-ASE-1K0-PL-XXXX_Rev01_CG_Response_YYYY-MM-DD.pdf  ← CG response PDF
  └── *CRS*.xlsx                            ← Comments Resolution Sheet (detailed)
```

### Trigger
Use this workflow when the user says:
- "update ID N with work done on it"
- "what's the status of task X?"
- "check the memory and update task Y"

Do NOT use for creating new tasks or bulk imports — those have their own workflows above.

### Domain Format for `search` vs `search_read`

⚠ **Key difference in execute_kw domain nesting:**

```python
# search_read — domain is ONE level: [['field', '=', 'value']]
models.execute_kw(db, uid, pw, 'project.task.type', 'search_read',
    [[['name', '=', '05 On Site Work']]], {'fields': ['id']})

# search — domain is wrapped the SAME way: [['field', '=', 'value']]
ids = models.execute_kw(db, uid, pw, 'project.task.type', 'search',
    [[['name', '=', '05 On Site Work']]])

# Both expect: [[domain_list]] — a list containing one domain list
```

The `search` method takes the domain as its first positional arg, just like `search_read` does. Both use the same nesting: `[[[condition1, op, value], [condition2, op, value]]]`.

## Batch Analysis → Odoo Mapping Workflow

When asked to "map folder projects to Odoo" or "add projects to Odoo":

1. **Analyze all project folders** in parallel via `delegate_task` (max 3 concurrent per batch, 2 batches for 8 projects)
2. For each project determine: stage (from portfolio stages), client, scope, key deliverables, pending items, existing document refs for project codes
3. **Batch 1: Create client partners** — check if they exist first (`res.partner', 'search'`), create missing ones
4. **Batch 2: Create projects** — with `name` (bilingual AR/EN), `stage_id`, `user_id`, `partner_id`, `description`
5. **Batch 3: Create tasks** — per project based on folder analysis, focused on current-stage deliverables. Use `user_ids` (many2many, NOT `user_id` — see field quirk in note above)
6. **Batch 4: Set project codes** — via `x_project_code` custom field
7. **Batch 5: Create local MD mapping** — `Odoo Tasks/Odoo_Tasks_Map.md` in each project folder
8. Verify all counts match expected totals

The 8 Tqanny project folders are at:
```
/Users/mohamedessa/Library/CloudStorage/OneDrive-Personal(2)/Work/PWork/01_PROJECTS/Tqanny_Projects/
```
Standard subfolder convention: `00_Admin/`, `01_CLIENT_INPUTS/`, `02_Submittals/`, `03_Design/`, etc.

New projects created without a local folder (e.g. Urwa Palace) should get a folder created in the same location following the `NN_Name` convention if possible, at minimum with the `Odoo Tasks/` subfolder.

### Kanban View — Subtasks Appear as Separate Cards

In Odoo 18's default project task Kanban view, **subtasks appear as separate cards** alongside parent tasks. This is the default behavior — subtasks are NOT automatically nested/grouped under their parent in the Kanban.

**Fix:** Add `('parent_id', '=', False)` to the action's domain to filter out subtasks:

```python
# Action [506] = Project's Tasks (Kanban) — opened when you click a project
# Action [517] = Project's tasks (List view version)
models.execute_kw(db, uid, pw, 'ir.actions.act_window', 'write', [[506], {
    'domain': "[('project_id', '=', active_id), ('display_in_project', '=', True), ('parent_id', '=', False)]"
}])
models.execute_kw(db, uid, pw, 'ir.actions.act_window', 'write', [[517], {
    'domain': "[('project_id', '=', active_id), ('display_in_project', '=', True), ('parent_id', '=', False)]"
}])
```

After this change:
- Kanban shows **only parent tasks** (packages like `1. [Architecture Design]`, `2. [Electrical Design]`)
- Subtasks are still accessible inside each parent's form view → **Sub-tasks** tab
- The "Sub-tasks" actions (id=525/507) remain unchanged and continue to filter for subtasks

⚠ **Note:** This modifies the action's domain globally — it affects ALL projects, not just one. This is intentional since the convention is that subtasks are managed through the parent task's sub-tasks tab, not as standalone cards.

Check the currently configured actions (IDs are instance-specific — discover per install):
```python
action_ids = models.execute_kw(db, uid, pw, 'ir.actions.act_window', 'search',
    [[['res_model', '=', 'project.task']]])
actions = models.execute_kw(db, uid, pw, 'ir.actions.act_window', 'read',
    [action_ids], {'fields': ['id', 'name', 'domain', 'context', 'view_mode']})
```

Key actions for project task views (⚠ IDs vary per Odoo installation — Samaya instance uses different IDs than Moqtana):

| Purpose | Moqtana ID (reference) | Samaya ID (Aseer instance) |
|---------|----------------------|--------------------------|
| Tasks (Kanban) | 506 | 416 |
| Tasks (List variant) | 517 | 427 |
| All Tasks (global) | 512 | 1500 |
| My Tasks | 511 | 1493 |
| Sub-tasks | 525 | 435 |
| Sub-tasks (alt) | 507 | 417 |

## ⚠ Common Pitfalls

- **Orphan subtasks with deleted parent**: Tasks whose `parent_id` points to a package that no longer exists. Detect via:
  ```python
  orphans = [t for t in all_tasks if t['parent_id'] and t['parent_id'][0] not in pkg_ids]
  ```
  Reassign to the correct existing package. Common cause: a package was deleted without reassigning its children first.
- **Non-package main tasks after restructuring**: Any main task (`parent_id=False`) whose name doesn't start with `NN —` (e.g. `01 — Furniture`) is likely an orphan. Audit by comparing against known package name patterns.
- **Depth-3 nesting**: Odoo allows unlimited task nesting, but projects follow a strict 2-level convention (Package → Subtask). Sub-sub-tasks (Package → Subtask → Deep-subtask) should be flattened by setting `parent_id` directly to the package.
- **Re-sequence by status**: After batch-moving tasks, re-sequence so active items appear first: in-progress → done → cancelled. Use increment-of-10 spacing.
- **Stale local credentials**: Passwords in the local mirror (`config/odoo.conf`, `docker-compose.yml`) may have been changed on the live server after deployment. Always verify before assuming they work.
- **CSRF required for web login**: `/web/login` returns a CSRF token that must be submitted with the login POST.
- **PostgreSQL not exposed externally**: Port 5432 is Docker-internal only — no direct psql from outside.
- **SMTP blocked**: DigitalOcean blocks outbound SMTP (ports 25/465/587). `smtp-relay.gmail.com` on port 587 works because it's Google's authorized relay, not direct SMTP submission.
- **Browser SPA renders empty pages**: The Odoo web client is a JS SPA. After login, the accessibility snapshot may show "(empty page)". Navigate to `/odoo/` directly or use XML-RPC API for admin tasks instead of trying the browser.
- **Email system params point to wrong domain**: `mail.catchall.domain` and `mail.default.from` must match the company's actual domain (e.g., `moqtana.sa`), not an old provider domain. Fix via `ir.config_parameter` write.
- **SMTP encryption value is case-sensitive**: `smtp_encryption` accepts `'starttls'`, `'ssl'`, `'none'` (lowercase). `'STARTTLS'` or `'TLS'` won't match.
- **from_filter restricts email routing**: The SMTP server's `from_filter` field only matches outgoing emails from that address. If the filter is `erp@moqtana.sa` but emails are sent from `info@moqtana.sa`, they won't use this server.
- **Scripts need container copy**: For data-heavy scripts, copy the file into the container first: `docker cp file.csv odoo_app:/tmp/`.
- **Task assignee field**: `project.task` uses `user_ids` (many2many), NOT `user_id`. Use `[(4, user_id)]` syntax.
- **Default admin password**: The `admin_passwd` in odoo.conf is the database *management* master password, NOT the admin user's login password. The actual superuser login is an email address from `company_data.md`, not `admin` — do NOT attempt `common.authenticate(db, 'admin', pwd, {})`.
- **API timeout on bulk operations**: Creating many records (30+ tasks) in a single XML-RPC call batch may timeout. Consider splitting into smaller batches or using `execute_kw` with `create` on a multi-record vals list.
- **Complex domain expressions**: Domains like `[['project_ids', 'in', [309]]]` may fail depending on the model's domain parser version. If a search returns empty and you expected results, try a simpler domain first (`[]`), then narrow down. See `references/odoo-cli-limitations-and-direct-python.md` for proper JSON formatting.
- **`|` (OR) prefix operator requires flat 3-element tuples at domain level, not nested tuples**: The `|` prefix operator in Odoo domains consumes the NEXT TWO conditions from the same list level. Example CORRECT formats:
  ```python
  # CORRECT — `|` as a 3-element tuple at the list level:
  [('|', ('name', 'ilike', 'nama'), ('name', 'ilike', 'namaa'))]
  # OR — as a flat list of lists:
  [['|', ['name', 'ilike', 'nama'], ['name', 'ilike', 'namaa']]]
  
  # WRONG — wrapping AND/OR operators inside a nested tuple:
  [['|', ('name', 'ilike', 'nama'), ('name', 'ilike', 'namaa')]]
  # This fails because the outer list treats `'|'` as a leaf value,
  # then the tuples `('name', 'ilike', 'nama')` unpack as 3-element domains,
  # but the list iteration sees `'|' + 2 tuples = 3 items` and expects
  # each to be a 3-element domain — '|' is only 1 element -> ValueError
  ```
  For chained OR across 3+ conditions, prefix operators stack left-to-right:
  ```python
  [('|', ('|', ('name', 'ilike', 'a'), ('name', 'ilike', 'b')), ('name', 'ilike', 'c'))]
  # Reads as: (a OR b) OR c
  ```
  When in doubt, build the domain step by step and test with `search_count` before `search_read`.
- **Aseer Museum (متحف عسير الإقليمى) is on Samaya Odoo, NOT Moqtana**: Project ID 219 lives at `https://samayainv.odoo.com`, not the Moqtana droplet. Despite being a museum project (which the \\"Use for\\" table associates with Moqtana), Aseer is the exception. Use Samaya API key from `~/.config/samaya/odoo.env`. The user will correct you immediately if you query Moqtana for Aseer.
- **Contractor scope items get `[REF]` prefix**: When adding contractor baseline schedule items (construction phases, procurement submittals) that Samaya doesn't directly manage, prefix with `[REF]` and place in their proper stage (Procurement 39, On-site 40, Handover 479), NOT Initiation (35). These remain visible in Kanban but are clearly marked as reference.
- **Non-DD packages need proper stage assignment**: Initiation (35), Procurement (39), Manufacturing (659), On-site (40), Handover (479). Never leave non-DD items in stage 35 just because they were created first.
- **File references in task descriptions must point to project folders, never /tmp**: When updating Odoo task descriptions with file references (attachments extracted from Outlook, generated PDFs, etc.), always reference the final project-relative path under the OneDrive-SAMAYAINVESTMENT project structure (e.g., `Samaya/Technical Office/Bim Unit/Aseer-Museum/09_Correspondence/filename.pdf`). Never use `/tmp/...` paths — the user considers them invalid. Copy files from temp to the appropriate project subfolder first, then reference that path in the description.
- **`project.tag` model does NOT exist**: Querying `project.tag` returns `Fault 2: "Object project.tag doesn't exist"`. Tags are stored in `project.tags` (plural) if it exists on your instance. For Samaya Odoo, tag IDs are used via the `tag_ids` field on `project.task` — you can set them but cannot independently query the tag table.
- **Use `fields_get` to discover available fields on any model** before writing code that assumes a field exists. This saved a bug where `ir.actions.act_window`'s `order` field doesn't exist on this Odoo 18 instance:
  ```python
  fields_info = models.execute_kw(db, uid, pw, 'ir.actions.act_window', 'fields_get',
      [[]], {'attributes': ['string', 'type', 'help']})
  for fname, finfo in sorted(fields_info.items()):
      print(f"{fname:30s} type={finfo['type']:15s} {finfo['string']}")
  ```
  This works for ANY model — `project.task`, `res.users`, `purchase.order`, etc. Particularly useful when dealing with Odoo cloud instances that may have different fields than self-hosted or demo instances. Use `ir.model` to discover available models if uncertain.
- **Verify personnel against PROJECT_MEMORY.md before naming in task descriptions**: SMP Rev03 may be stale — staff leave (e.g. QA/QC Manager Abdelmohaimen Medhat left). Always check `Aseer-Museum/PROJECT_MEMORY.md` §0 for current personnel status before writing names into Odoo task descriptions or plans. Use role-based references ("QA/QC Manager") for departed staff, never names.
- **`search_count` is available for counting**: Use `models.execute_kw(db, uid, pw, 'project.task', 'search_count', [[domain]])` to get a count without fetching records. Same domain format as `search`. Useful for dashboard summaries (`main tasks vs subtasks`).
- **Cashout report**: Build multi-sheet Excel (Summary + POs Detail + Mada Aljezera + Saba Najad). Summary MUST include credit suppliers section (موردين دائنين) alongside POs, with a GRAND TOTAL. See `references/po-cashout-report.md` for full filter logic (state=purchase/done, total≥1K, due≥1K, paid-PO exclusions, credit supplier mapping, **forced-draft-PO pattern**, UID auth requirement) and PatternFill keyword-arg syntax for macOS openpyxl.
- **Stage IDs vary per project**: The numeric ID for "Procurement" in one project may differ in another. Always query the target project's stages via `project.task.type.search_read` or inspect used stages from existing tasks before writing `stage_id` in cross-project scripts. Example: project 112 uses stage 697 "off-Site Manufactring" while 166/176 use stage 659 "04 Off-site Manufacturing" — same work category, different IDs. Always discover, never assume.
- **Dual Off-site Manufacturing stages**: Some Samaya projects (e.g. ID 112) use stage 697 for production orders while others use stage 659. Query both because picking the wrong stage lands tasks in a different Kanban column. Use the pre-flight query pattern from `odoo-task-restructure` Phase 0 to discover actual stage IDs before writing.
- **Duplicate Manufacturing Order tasks**: A single MO (e.g. FA/WH/MO/00041) can appear as two separate Odoo tasks — one created by the factory automation and another manually added. Before marking one as duplicate, check `description` for chatter comments showing actual work progress. Consolidate by merging descriptions into the active task and canceling the orphan.
- **Design document → Odoo audit workflow**: When cross-referencing museum exhibition design PDFs against Odoo tasks, see `references/design-doc-to-odoo-audit.md` for the full workflow (extract items → audit → create missing → restructure).

## Known Users

### Moqtana Odoo Users

| User | Login | Role |
|---|---|---|
| Bassem Hanbla | `basem@moqtana.sa` | Sales Manager |
| Jaber Almahdi | `Designer@moqtana.sa` | Design Director |
| Abdullah Mohamed | `abdullah@moqtana.sa` | Projects Manager |
| Abdullah alshojaa | `musaab.ed@moqtana.sa` | Projects & Sales Coordinator |
| **Admin (superuser)** | **`mohamedsultanabbas@gmail.com`** | **Full access** |

### Samaya Odoo Users — Factory Setup (Kiwan)

| ID | Name | Login | Role |
|----|------|-------|------|
| 196 | Muhammad Kiwan | `kiwan@samayainvest.com` | **Factory ERP setup** — Accounting, CRM, Invoices, Quotations, Work Centers, Manufacturing Ops, Inventory, Purchase, Reports |

### Samaya Odoo Users (Aseer Project Team)

| ID | User ID | Login | Role |
|---|---|---|---|
| Sultan Issa | 151 | `sultan@samayainvest.com` | **Technical Office Manager** — DD stage technical packages ONLY (Architecture, Structural, MEP, Life Safety, Plans, Specialist pkgs). NOT project manager. |
| Mohamed Samir | 564 | `m.samir@samayainvest.com` | Site execution + procurement — construction phases, site fabrication, manufacturing, specialist prequal sourcing |
| Hani Alghamdi | 478 | `H.Alghamdi@samayainvest.com` | Purchasing lead — pricing, RFQs, S00101 contract, PR material submittals, procurement |
| Hesham Abdelhameed | 163 | `hesham.a@samayainvest.com` | Document Control — submittals, daily reports, documentation flow |
| Ahmed Salah | 162 | `ahmed.salah@samayainvest.com` | Project coordination — manufacturing orders |
| Ali Abdelrahman | 160 | `ali.abdelrahman@samayainvest.com` | Technical Office — DD stage technical work ONLY (NOT prequal, NOT procurement, NOT site) |
| Adel Darwish | 7 | `adel@samayainvest.com` | Project management |
| Mohammed Elshaikh | 157 | `elshaikh@samayainvest.com` | Project Planner — schedule review, planning |

### Assignment rules (learned from user corrections — DO NOT violate):
- **Sultan (Tech Office Mgr)** → DD stage technical packages ONLY. NOT project manager.
- **Prequal / procurement** → Hani + Mohamed Samir. Technical office (Ali) does NOT handle prequal.
- **Site work** (construction phases, site fabrication, handover) → Mohamed Samir (NOT Hesham, NOT Sultan)
- **Procurement submittals** → Hani + Samir
- **DD stage technical work** → Sultan + Ali (Technical Office)
- **Material submittals from baseline schedule** → Hani + Samir
- **Contractor scope reference items** → prefix with `[REF]`, place in proper stage (39/40/479), assign to Samir (site) or Hani (procurement)
- **Document control / daily reports** → Hesham
- **Coordination / manufacturing orders** → Ahmed Salah
- **Schedule review / planning** → Sultan + Mohamed Elshaikh (Project Planner)

> **⚠ Admin login source**: The admin credentials are documented in `assets/company_data.md` in the local mirror (NOT in `odoo.conf` or any script). The Odoo config file's `admin_passwd` is the *database management* master password, not the user login. The superuser's login email is `mohamedsultanabbas@gmail.com` — do NOT try `admin` as the login for XML-RPC authenticate.

## Setup on a New Device

When setting up Odoo access on a new Hermes agent, the comprehensive reference file is at:
`~/.hermes/hermes-agent/samaya_odoo_hermes_setup.md`

This file (generated 2026-06-13) contains all 13 sections: connection boilerplate, project 219 structure, task creation templates, PO creation, search patterns, procurement workflow, skills list, 10 pitfalls, folder structure, and step-by-step setup.

### Credential File Setup
```bash
mkdir -p ~/.config/samaya
cat > ~/.config/samaya/odoo.env << 'EOF'
ODOO_URL=https://samayainv.odoo.com
ODOO_DB=peerless-tech-samaya-18-0-18447146
ODOO_USER=sultan@samayainvest.com
ODOO_API_KEY=*** 600 ~/.config/samaya/odoo.env
```

### Connection Test
```bash
python3 -c "
import xmlrpc.client, ssl
ctx = ssl._create_unverified_context()
t = xmlrpc.client.SafeTransport(context=ctx)
c = xmlrpc.client.ServerProxy('https://samayainv.odoo.com/xmlrpc/2/common', transport=t)
print(c.version())
"

All scripts live at `/Users/mohamedessa/Documents/01_Odoo/scripts/` with run order in `scripts/README.md`.

| # | Script | Purpose |
|---|---|---|
| 01 | `01_inject_uom.py` | 6 UoM categories / 128 units |
| 02 | `02_inject_categories.py` | MasterFormat + Raw Materials categories |
| 03 | `03_track_inventory_default.py` | `is_storable` default = False |
| 04 | `04_auto_internal_reference.py` | Auto `default_code` from category |
| 05 | `05_import_raw_materials.py` | Import 1,452 raw materials catalog |
| 06 | `06_configure_project_template.py` | Template project for Design & Build fit-out |
| 07 | `07_offsite_manufacturing_stage.py` | Off-site Manufacturing stage |
| 08 | `08_new_project_template_automation.py` | New project → copy stages+milestones |
| 09-12 | `09..12_attendance*.py` | Attendance fields, views, default project, report |
| 13 | `13_hr_org.py` | Departments, jobs, employee tags |
| 14 | `14_activity_types.py` | 16 fit-out activity types |
| 15 | `15_project_portfolio_stages.py` | Project pipeline stages |
| 16 | `16_invoice_template.py` | Premium bilingual invoice redesign |
| 17 | `17_themed_reports.py` | SO/MO themed reports |

## Excel Data Preparation for Odoo Master Data Imports

Before importing master data (raw materials, products, UOMs) into Odoo via scripts like `05_import_raw_materials.py`, the Excel source data often needs standardization.

### Approach — Category Prefix Standardization

**User preference: HIGH-LEVEL category buckets, not granular sub-categories.** When raw material names have inconsistent or overly specific prefixes, standardize them into broad groups:

| Code | High-Level | Includes |
|------|-----------|----------|
| WDM | Wood Materials | Solid wood, MDF, MFC, plywood, veneer, particle board, edge banding |
| MTL | Metal Materials | All steel shapes, aluminum, copper, sheet metal, perforated sheet |
| PNT | Painting Materials | All paint types, primers, thinners, putty, stains, acrylic paint |
| PKG | Packing Materials | Packaging material |
| PRT | Printing/Fabrication | 3D printing, resin, acrylic sheet, forex, printing materials |
| HDW | Hardware/Infrastructure | Electrical, plumbing, insulation, adhesive, chemicals |
| ACC | Accessories/Fasteners | Fasteners, tapes, hinges, gift material, stationery |
| TLE | Tiles & Flooring | Tiles, flooring |
| FBR | Fabric & Textiles | Fabric, carpet, leather, foam |
| TLS | Tools & Sundry | Signage material, wax |
| GEN | General | Miscellaneous |

### Workflow

**Phase 1 — Prefix → Code Transformation**

1. **Analyze existing prefixes**: Extract unique first segment (before ` - `) from the Name column, count occurrences
2. **Propose high-level grouping**: Present to user for approval (prefer 8-15 buckets, not 50+)
3. **Build prefix→code mapping** in Python dict, sorted by descending key length so longer prefixes match first (e.g. `steel round bar` before `steel`)
4. **Transform all name columns** (Name, English Name) — Arabic names typically don't need prefix changes
5. **Verify** no item is left unmapped; check counts by new code
6. **Save as new file** (e.g. `Product_raw_materials_standardized.xlsx`), keep original untouched

**Phase 2 — Native Naming (CRITICAL)** 

After prefix→code transformation, names still need native/standard cleanup. **Codes DO NOT belong in the Name column.** They go in a separate Category column (e.g. Col5).

Rules:
1. **Strip all codes from Names** — `"PNT - Ditto Staircases..."` → `"Ditto Staircases..."` (code `PNT` goes to Category column)
2. **Prepend material type naturally** when the name is just dimensions or cryptic — `"40+40"` → `"MS Angle 40x40"`, `"10 mm - Clear"` → `"Acrylic Sheet 10 mm - Clear"`
3. **Detection patterns for non-descriptive names**:
   - Dimension-only: starts with measurement pattern (`40+40`, `10x10`, `10mm`, `(40)`, `50*50`, `1"x2"`, numbers+units)
   - Too short: single-word < 10 chars (`1`, `10`, `صاج`, `gum`)
   - Cryptic: just numbers/symbols with no material context
4. **Fix pattern**: Take the original raw prefix (before code transformation) and prepend it as a natural word with a space separator, NOT an em-dash. E.g. `"Steel Sheet 40x40"` not `"STE - 40+40"`
5. **Keep original file untouched** — save standardized data to a new file
6. **Verify after fixing**: re-scan all names — no codes, no bare-dimension items left

See `references/excel-data-prep-for-odoo-imports.md` for the full native naming script and detection logic.

### Script Pattern (openpyxl)

```python
import openpyxl
from collections import Counter

PREFIX_MAP = {
    'solid wood': 'WDM',
    'steel': 'MTL',
    'steel shs': 'MTL',
    # ... all prefixes mapped to their code
}
sorted_prefixes = sorted(PREFIX_MAP.keys(), key=lambda x: -len(x))

def transform_prefix(text):
    if not text: return text
    lower = text.lower().strip()
    for prefix in sorted_prefixes:
        if lower.startswith(prefix):
            rest = text[len(prefix):]
            return f"{PREFIX_MAP[prefix]}{rest}"
    return text

wb = openpyxl.load_workbook(src)
ws = wb.active
for row in range(2, ws.max_row + 1):
    for col in [2, 3]:  # Name, English Name columns
        val = ws.cell(row=row, column=col).value
        if val:
            new = transform_prefix(val)
            if new != val:
                ws.cell(row=row, column=col).value = new
wb.save(dst)
```

See `references/excel-data-prep-for-odoo-imports.md` for the full working script used in the Samaya raw materials standardization.

**Pitfall**: Some prefixes may not match — always run a `Counter` after transformation on the first segment and check for any unexpected codes or untransformed items. Lexan Sheet and similar edge cases slip through if the map is incomplete.

### Excel Formatting: No Emoji / Icons / Decorative Symbols

The user explicitly corrected: "always dont use icons and AI finger prints on my files." When creating Excel files for this user:

- **No emoji characters** in any cell value — replace status markers with plain words
- **No icons, decorative symbols, or "AI fingerprints"** — use color fills (green/yellow/red PatternFill) to indicate status instead of icon characters
- **Clean professional formatting** — Calibri font, gray-blue headers (2F5496), thin borders, no colored text
- **Valid for any generated Excel** — whether cost comparisons, Odoo exports, or custom reports

## Contract-to-Register Classification (Specialist vs Contractor vs Authority)

When comparing contract requirements (e.g. Appendix B of the SOW) against the Key Personnel Register, use this **three-bucket classification** to avoid mixing types:

### Three Categories

| Bucket | Definition | Examples | KPR Action |
|--------|-----------|----------|------------|
| **Samaya Internal** | Samaya employees or Samaya-owned entities | Project Director, BIM Manager, Samaya Graphit, Samaya Factory | Keep as-is — internal headcount |
| **Samaya Hires** | External consultants, subcontractors, or suppliers that Samaya must appoint | AD Engineering (MEP design), ZNA (lighting), Glasbau Hahn (showcases), Rawasen (AV) | Keep — these are procurement items |
| **Authority** | Government/regulatory roles — NOT Samaya's responsibility to hire | SEC-Approved Electrical Eng, MOI Security Consultant, CITC Telecom Engineer, Municipality Structural Eng | **Remove from KPR** or flag clearly as authority role |

### Designer vs Contractor/Installer Split

Many contract items combine both design and installation in one title (e.g. "Lighting Designer and Supplier", "Graphics Artwork and Production Contractor"). In practice these are often **two separate entities**:

| Role | Designer (Specialist) | Contractor/Installer |
|------|----------------------|---------------------|
| Lighting | ZNA — design consultant | **M&E Contractor** — fixture supply & install |
| M&E | AD Engineering — design only | **M&E Contractor** — install works + FLS + lighting |
| FLS | Nama Consulting — design only | **M&E Contractor** — install (same as above) |
| AV Hardware | NRS (overall) + AVD (MoC, software) | Rawasen — supply & install |
| Interactives | Lumotion — software design (pending) | Rawasen — mechanical fabrication & install |
| Showcases | NRS reviews | Glasbau Hahn — supply & install ✅ combined |
| Graphics | Samaya Graphit — design | Samaya Graphit — produce & install ✅ combined |
| Models & Props | Samaya Factory — Replica Dept design | Samaya Factory — produce & install ✅ combined |

**Rule:** If the contract title says "Designer and Supplier" or "Designer and Contractor", check with the user whether one entity does both or if they're split. Logically, a design consultant ≠ an installation contractor in most cases.

### Methodology Steps

1. **Read the contract appendix** — extract every role/package line by line with PDF text positioning
2. **Identify the column group** — Specialist Contractor Packages (left column) vs Individual Specialists (right column) vs Management (header rows)
3. **For each item, ask:**
   - Is this a Samaya hire or an Authority role?
   - Is this one entity doing both design + install, or two separate entities?
   - Which KPR row maps to the Designer side? Which maps to the Installer side?
4. **Classify each into one of three buckets** and update the KPR accordingly
5. **Remove rows that are Authority roles** (not Samaya's hire) — note them in the task description but delete from KPR
6. **Do NOT add rows for items not required from Samaya** (e.g. FF&E Supplier may be an owner-direct item)
7. **Clean up** — after splitting, verify no rows remain misclassified or redundant

- **Close Excel files before writing with openpyxl** — If the target .xlsx is open in Excel, openpyxl's `wb.save()` will fail silently or corrupt the file. Close the file first, then write. The user explicitly flagged this: "always when need to write in file already opened close it first and then write or update and reopen."
- **KPR pending rows need ACTION notes** — Every row with status "Not yet appointed", "Pending CG approval", or "Vacant" must have a clear `ACTION:` prefix in the Notes column describing what's needed to move it forward (e.g. "ACTION: Submit PQD + 2 alternative vendors per CG CRS comment 11"). This makes the register actionable, not just descriptive.
- **Personnel changes may come from user knowledge before email** — The user sometimes knows about appointments/departures before formal email notification. When they mention a new person (e.g. "Waris is the new Project Director"), update the KPR even without email evidence, but flag the status as "pending formal notification" and the date as approximate.

### Pitfalls

- **"Designer and Supplier" titles are traps** — always verify if one entity does both. The user will correct you if you assume combined when they're split, or vice versa. When in doubt, present both possibilities and let the user clarify each item.
- **Authority roles look like KPR entries** — "MOI-Approved Security Consultant" sounds like a hire but MOI is the regulator, not a procurement item. These need to be removed from the KPR or clearly flagged.
- **Don't add rows for scope not required from us** — e.g. FF&E Supplier may be an owner-supplied item. Let the user tell you what's in Samaya's scope.
- **After classification, check for leftover orphan rows** — the user will ask "did you remove unnecessary rows?" as a final verification step.

## References

`references/odoo-auth-troubleshooting.md` — detailed session notes on authentication failures and recovery patterns (added on first auth failure).

`references/samaya-odoo-procurement-workflow.md` — complete procurement pipeline for Samaya Odoo: supplier creation, product creation, RFQ creation patterns, currency conventions (USD/SAR), and partner/product-ID reference tables. Covers Replica Project SC-01 procurement pattern.

`references/samaya-odoo-factory-setup.md` — creating a separate factory company entity (res.company + res.partner), setting up implementation tasks under Project 302 (Odoo Factory Requests), task assignment patterns for Sultan and Kiwan.

`references/samaya-odoo-users.md` — known Samaya Odoo users (IDs, names, roles), plus query patterns for project tasks grouped by stage. Includes the Aseer Museum (project 219) task listing method used for technical office queries.

`references/odoo-task-hierarchy.md` — two-level hierarchy (MAIN→SUB), task creation, restructuring procedures, baseline date mapping.

`references/email-to-odoo-task-workflow.md` — end-to-end workflow: verbal task list → Odoo mapping → Outlook cross-reference → attachment extraction → PDF reading → Odoo status update → file filing to project folders.

`references/contract-compliance-gap-analysis.md` — workflow for reading contract appendices (e.g. Appendix B specialist packages), mapping against KPR and Stakeholder Plan, identifying gaps (Covered/Partial/Missing), and updating registers. Use when user asks to compare contract requirements against project registers.

`references/kpr-maintenance-pattern.md` — KPR status labels, approval dates, action tracking, personnel change workflow, and Excel write safety rules.

`references/stakeholder-register-from-email.md` — workflow for updating the Key Personnel Register and Stakeholder Register from email evidence: Outlook queries for appointments/departures/CV submissions, cross-referencing, and Excel/project-memory updates.

`references/po-vendor-lookup.md` — batch lookup of PO vendor/price/state by PO name field, Odoo URL format for hyperlinks, zero-value handling, state mapping.

- `references/po-payment-tracking.md` — invoice/bill payment status, chatter message analysis (Ibrahim Shaaban "transfer receipt" vs "task done" patterns), full PO payment verification workflow, and the daily workshop purchasing tracker cron job (2:00 PM KSA). Includes script install path at `~/.hermes/scripts/workshop_purchasing_update.py`.
- `references/po-not-received-tracker.md`
- `references/po-cashout-report.md` — consolidated PO cashout report with bill cross-reference, filter logic, and multi-sheet Excel (طلب صرف + bank statement + supplier statement) for finance-department cashout requests — building a filtered Excel tracker of Samaya Factory workshop POs not fully received, from Odoo export data. Includes filtering logic (project=buyer), Odoo hyperlink format, OneDrive save path, and deduplication pattern.
- `references/quran-museum-projects.md` — Samaya Odoo projects related to the Holy Quran Museum and Hira Cultural District (Jabal Al-Noor). Lists project IDs, stages, managers, and current task structure for first floor fit-out. Reference when working on the Quran Museum complex.
