# Inventory Tracking System — Samaya Factory

## Design

Track raw materials stock by combining three Odoo data sources:
1. **Stock Quants** — current on-hand quantity per product per factory location
2. **Stock Moves (incoming)** — from vendor/supplier to factory stock (PO receipts)
3. **Stock Moves (outgoing)** — from factory stock to production (MO consumption)

### Formula
```
Available = On Hand - Reserved
Coverage Days = On Hand / (Outgoing 12m / 365)
```

### Consumables Distribution
Consumables (categories 220-226, 353-355, 396-400) are NOT tracked per MO. Instead:
- Total consumables received per month ÷ total MOs completed that month = cost per MO
- Applied to both open and completed MOs in the same month

## Key Locations

| ID | Name | Usage |
|----|------|-------|
| 45 | Factory | internal |
| 46 | Stock | internal |
| 47 | Input | internal |
| 51 | Pre-Production | internal |
| 77 | Digital printing | internal |
| 78 | 3D Lab | internal |
| 15 | Production | production (consumption destination) |
| 98 | Production | production (consumption destination) |

## Key Categories

### Raw Materials (60 subcategories, ~953 products)
Root IDs: 356 (under All), 700 (top-level)

Major groups: MDF, Plywood, Solid Wood, Wood Veneer, Paint (12 sub-types), steel (10 sub-types), Acrylic Sheet, Chemical & Glue, Fabric, Foam, Aluminum, Edge Banding, Resin & Fiber

### Consumables (15 categories)
IDs: 220, 221, 222, 223, 224, 225, 226, 353, 354, 355, 396, 397, 398, 399, 400

## Script
`scripts/inventory_system.py` in the samaya-factory-pos skill.

Usage:
```bash
SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") \
  python3 ~/.hermes/skills/devops/samaya-factory-pos/scripts/inventory_system.py
```

Output: `~/.hermes/tmp/inventory_report.json`

## Known Issues (Aug 2026)
- 27 products with negative stock (Odoo data issue — needs physical inventory)
- 170 products with zero stock that had movement in last 12 months (need reorder)
- Only 299 of 953 raw materials have positive stock
- Stock moves total 40M+ units incoming vs 5K outgoing — likely UoM mismatch in data
