# SysLeaders Access & Data Extraction

## Login
- **URL:** `https://www.sysleaders.com/samaya/index.php?module=users/login`
- **Username:** `sultan`
- **Password:** `1batagoniaA`

## Navigation Structure
After login, the main sidebar has these relevant sections:
- **Projects → Projects** — project list (34 active), search by name/ID
- **Projects → Tasks** — task list with labor costs per BOQ item
- **Operation Management → Purchasing Orders** — PO list with project filter
- **Operation Management → Expenses Statement** — expense/labor statements (often blank)
- **Operation Management → Order Items** — raw materials/items detail

## Finding a Project's SysLeaders ID
The project ID appears in PO URLs: `path=49-421` means project 49, item 421.
Rateeb (متجر التمور) = project 49.
Other projects have different IDs — discover by filtering POs by project name.

## Extracting POs for a Project

### Step 1: Navigate to POs page
```
https://www.sysleaders.com/samaya/index.php?module=items/items&path=49
```
(Replace 49 with the project ID)

### Step 2: Filter by project
Use the combobox (Project dropdown) — type the project name in Arabic (e.g., "التمور" for Rateeb). Press Enter to apply.

### Step 3: Extract PO list via JS console
```javascript
Array.from(document.querySelectorAll('table tbody tr'))
  .filter(r => r.querySelector('td') && !r.textContent.includes('No Records'))
  .map(row => {
    const cells = row.querySelectorAll('td');
    return {
      orderNo: cells[2]?.textContent?.trim().split('\n')[0] || '',
      project: cells[3]?.textContent?.trim() || '',
      status: cells[4]?.textContent?.trim() || '',
      date: cells[5]?.textContent?.trim() || '',
      cost: cells[7]?.textContent?.trim() || '',
      url: cells[2]?.querySelector('a')?.href || ''
    };
  }).filter(r => r.orderNo)
```

### Step 4: Get PO items
Click into each PO (Order Items tab), then extract:
```javascript
Array.from(document.querySelectorAll('table tbody tr'))
  .filter(r => r.querySelector('td') && !r.querySelector('th'))
  .map(row => {
    const cells = row.querySelectorAll('td');
    if (cells.length < 3) return null;
    return {
      item: cells[2]?.textContent?.trim()?.substring(0, 60) || '',
      qty: cells[3]?.textContent?.trim() || '',
      estCost: cells[5]?.textContent?.trim() || '',
      total: cells[7]?.textContent?.trim() || ''
    };
  }).filter(Boolean)
```

## Labor Costs
SysLeaders labor data lives in:
1. **Tasks page** — per-BOQ labor costs (`Labor Cost` column in task list)
2. **Expenses Statement** — may show labor entries (often blank, try `?module=items/expenses_statement&path=49`)
3. **Archived Excel files** — `tasks_{Project}.xlsx` in `_Archive/{Project}/` has BOQ-level labor

Fallback: use the archived Factory Cost Analysis (FCA) files which have aggregate labor by job type.

## Known Project Names in SysLeaders
| English | Arabic (SysLeaders) | ID |
|---------|---------------------|----|
| Rateeb Store | JN-Rateeb-Shop متجر التمور | 49 |
| Khair Al-Khalq Store | Khair Al-Khalq Store | — |
| Khair Al-Khalq Exhibition | Khair Al-Khalq Exhibition | — |

## Pitfalls
- Project search uses Arabic names, not English — "التمور" not "Rateeb"
- The `expenses_statement` page often loads blank — fall back to archived data
- PO item tables may need the "Order Items" tab clicked before they render
- Browser console extraction is more reliable than snapshot parsing for large tables
