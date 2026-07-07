# Samaya Factory Cashout Report — Build Workflow

## Purpose
Generate an Excel cashout report for Samaya Factory (Odoo project 244) showing unpaid POs, credit supplier balances, and summary.

## Data Source
- Odoo 18 at `samayainv.odoo.com` (XML-RPC)
- Credentials: `~/.config/samaya/odoo.env`
- SSL fix: `SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")`

## Key Odoo Queries

### All Factory POs (project 244)
```python
# search_read with project_id in domain can crash Odoo 18
# Use two-step approach:
all_pos = call('purchase.order', 'search_read', [[]], {'fields': fields, 'limit': 500})
factory_pos = [p for p in all_pos if p.get('project_id') and p['project_id'][0] == 244]
```

### Unpaid Factory POs
```python
unpaid = [p for p in factory_pos
    if p['state'] == 'purchase' and p.get('invoice_status') in ('to invoice', 'no')]
```

### Credit Supplier Filtering
- Mada Aljezera: partner_id = 2427
- Saba Najad: partner_id = 5603

## Excel Format
- 4 sheets: Summary, POs Detail, Mada Aljezera, Saba Najad
- Navy (#1F3864) headers, yellow total rows, alternating row shading
- Landscape A4, fit to width
- Number format: `#,##0.00`

## Non-Factory POs to Exclude
When updating the report, verify each PO's `project_id`. Common non-Factory POs that get mixed in:
- POs for Jalal & Jamal (166), Ghamama Museum (136), Maalim Al-Haramein (176), Quran Museum (137), Tafweej Center Zamzam (229)

## Script
Location: `/tmp/build_cashout_report.py` (regenerate as needed)
Run: `SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") python3 /tmp/build_cashout_report.py`
