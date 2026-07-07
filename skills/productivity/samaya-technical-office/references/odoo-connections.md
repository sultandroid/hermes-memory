# Odoo Connections — Samaya BIM Unit

## Instance 1: Samaya Investment (DEFAULT)
| Detail | Value |
|---|---|
| **URL** | `https://samayainv.odoo.com` |
| **DB** | `peerless-tech-samaya-18-0-18447146` |
| **User** | `sultan@samayainvest.com` (uid 151) |
| **Version** | Odoo 18.0+e |
| **Creds file** | `~/.config/samaya/odoo.env` (mode 600) |
| **API key field** | `ODOO_API_KEY` (currently using password) |

## Instance 2: Dawam Tech (on request only)
| Detail | Value |
|---|---|
| **URL** | `https://dawam-tech.odoo.com` |
| **DB** | `dawam-tech` |
| **User** | `sultan@dawamtech.com` (uid=2) |
| **Version** | Odoo 19.0+e |
| **Claude memory** | `~/.claude/projects/*/memory/reference_odoo_dawam.md` |

## XML-RPC Boilerplate (Python)
```python
import xmlrpc.client, ssl, certifi
ctx = ssl.create_default_context(cafile=certifi.where())
transport = xmlrpc.client.SafeTransport(context=ctx)
common = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/common', transport=transport)
uid = common.authenticate(DB, USER, PWD, {})
M = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/object', transport=transport)
```

## Key Odoo Models Used
- `project.project` — projects
- `project.task` — tasks
- `sale.order.line` — quotation lines (Dawam)
- `product.template` — products (Dawam)
- `res.users` — users/employees

## Task Management
- **Mark done:** `state = '1_done'` — do NOT change stage_id
- **Set deadline:** `date_deadline = 'YYYY-MM-DD'`
- **Query my tasks:** search with `[['user_ids', 'in', [uid]]]`

## Verification Pattern
After any write operation, read back the record to confirm the change took effect.
