# SysLeaders Project Registry

Mappings between Sister Company projects and SysLeaders entity IDs.

## Discovered Projects

| Code | Name | entity_id | path | JN | Area (m2) |
|------|------|-----------|------|----|-----------|
| 10 | Rateeb Store (متجر رطيب) | 282 | 49 | JN-Rateeb-Shop | 42 |

## How to Discover New Projects

1. Log in to https://www.sysleaders.com/samaya
2. Go to Projects → in-progress-Projects
3. Search for the project name
4. Inspect the table row for the project ID in links
5. Or: navigate to Operation Management → Purchasing Orders, filter by project, note the `path` parameter in the URL

## PO Reports

| reports_id | Entity |
|-----------|--------|
| 780 | Purchasing Orders |

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `module=users/login` | GET | Login page (CSRF token) |
| `module=users/login&action=login` | POST | Authenticate |
| `module=items/listing` | POST | DataTable listing (POs, tasks) |
| `module=items/info&path=X-Y` | GET | PO detail page |
| `module=items/work_centers` | GET | Labor rates (Work Centers) |

## Rateeb POs (Sample)

| PO | Date | Cost (SAR) | Status | Items |
|----|------|-----------|--------|-------|
| PO00378 | 13/05/23 | 36,124.50 | Delivered | 8 |
| PO00382 | 20/05/23 | 2,053.00 | Delivered | 3 |
| PO00393 | 25/07/23 | 1,792.00 | Delivered | 2 |
| **Total** | | **39,969.50** | | **13** |
