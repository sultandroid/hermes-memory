# Samaya Odoo — Known Users & Team Members

**Instance:** `https://samayainv.odoo.com`
**Database:** `peerless-tech-samaya-18-0-18447146`

## Samaya Users

| ID | Name | Login | Role |
|----|------|-------|------|
| 151 | Sultan Issa | `sultan@samayainvest.com` | Technical Office (المكتب الفني) — main assignee for Aseer tasks |
| 7 | Adel Darwesh | `adel@samayainvest.com` | Project Manager — Aseer Museum |
| 188 | Abdullah Mahfoud | `abdu@samayainvest.com` | Procurement / Tender |
| 162 | Ahmed Salah | `ahmed.salah@samayainvest.com` | Design / Engineering |
| 160 | Ali Abdel Rahman | `ali.abdelrahman@samayainvest.com` | BIM / Design |
| 181 | Khaled Ahmed Al-Obaidi | `k.abeedy@samayainvest.com` | Site coordination |
| 198 | Mohammed Abdul Kareem | `ma.kareem@samayainvest.com` | Procurement |
| 242 | Mohammed Alzeeny | `alzeeny@samayainvest.com` | Supply chain / Tender |
| 153 | Raoof Aldeeb | `raoof@samayainvest.com` | On-site execution |
| 154 | Talha Yousf | `talha.yousaf@samayainvest.com` | Engineering / Design |
| 168 | موسى بابكر الحسن بابكر | `mousa@samayainvest.com` | Manufacturing |

## Query Pattern — Project Tasks by User

```python
import xmlrpc.client

url = 'https://samayainv.odoo.com'
db = 'peerless-tech-samaya-18-0-18447146'
user = 'sultan@samayainvest.com'
api_key = '<from ~/.config/samaya/odoo.env>'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, user, api_key, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Get all tasks for a project
tasks = models.execute_kw(db, uid, api_key, 'project.task', 'search_read',
    [[['project_id', '=', 219]]],                            # Aseer Museum
    {'fields': ['id', 'name', 'stage_id', 'user_ids', 'date_deadline', 'priority'],
     'order': 'stage_id asc', 'limit': 100})

# Get user display names for resolution
models.execute_kw(db, uid, api_key, 'res.users', 'search_read',
    [[['id', 'in', list_of_ids]]],
    {'fields': ['id', 'name', 'login']})

# Group by stage for technical office view
stages = models.execute_kw(db, uid, api_key, 'project.task.type', 'search_read',
    [[]], {'fields': ['id', 'name'], 'order': 'sequence asc'})
stage_map = {s['id']: s['name'] for s in stages}
```

## Related Projects on Samaya

| Project | Odoo ID |
|---------|---------|
| متحف عسير الإقليمى (Aseer Regional Museum) | 219 |
