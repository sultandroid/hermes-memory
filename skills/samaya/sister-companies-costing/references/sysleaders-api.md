# SysLeaders API Access (curl-based)

SysLeaders data is loaded via AJAX/DataTables — the HTML pages are shells, data comes from API endpoints. Use curl with CSRF token + session cookie.

## Authentication Flow

### Step 1: Get CSRF token from login page
```bash
curl -s -c /tmp/sysleaders_cookies.txt \
  'https://www.sysleaders.com/samaya/index.php?module=users/login' \
  | grep -o 'form_session_token.*value="[^"]*"' | grep -o 'value="[^"]*"' | cut -d'"' -f2
```

### Step 2: Login with CSRF token
```bash
TOKEN="<extracted_token>"
curl -s -L -c /tmp/sysleaders_cookies.txt -b /tmp/sysleaders_cookies.txt \
  -X POST \
  -d "username=sultan&password=1batagoniaA&form_session_token=${TOKEN}" \
  'https://www.sysleaders.com/samaya/index.php?module=users/login&action=login'
```

### Step 3: Extract new token from dashboard
The token updates after login — grep for `token=` in the response.

## API Endpoints

### POs Listing (DataTable AJAX)
```
POST /samaya/index.php?module=items/listing
Content-Type: application/x-www-form-urlencoded

reports_id=780
reports_entities_id=49
path=49
page=1
redirect_to=report_780
listing_container=entity_items_listing780_49
```

Returns HTML table rows with PO data. Extract PO paths from `href="...path=X-Y"` links.

### PO Detail
```
GET /samaya/index.php?module=items/info&path=49-378
```
Returns PO info page. Items are loaded via subentity — the main page only has info table. For items, use the subentity listing or navigate in browser.

### Report IDs by Entity
| Report ID | Entity | Content | Path |
|-----------|--------|---------|------|
| 780 | 49 | POs listing | `path=49` |
| 646 | 49 | Tasks listing (Progress, Status, Priority, Product Name, Assign to) | `path=49` |
| 79 | 28 | Subentity tasks (Labor cost, Project) | `path=21-282/79` |
| 787 | 49 | POs detail (Order No, Status, Estimated Cost) | `path=49` |
| 786 | 48 | Samples (Samples No, Sample Name, Remark, Action Code) | `path=49` |
| 1047 | 72 | Expenses (Category, Amount, Remarks, ST.NO.) | `path=72` |

POST to `module=items/listing` with: `reports_id={RID}&reports_entities_id={EID}&path={PATH}&page=1&redirect_to=report_{RID}&listing_container=entity_items_listing{RID}_{EID}`

### Project Entity IDs
Rateeb (JN-Rateeb-Shop) = entity 282, path 49. Other projects need discovery via the POs listing filter dropdown.

### SysLeaders Web API (browser-based)
For interactive data extraction, use the browser tool:
1. Login at `https://www.sysleaders.com/samaya/index.php?module=users/login` (user: `sultan`, pass: `1batagoniaA`)
2. Navigate to Projects → search by Arabic name (e.g. "التمور" for Rateeb)
3. Click project → find subentity listing containers in the page HTML
4. Use `browser_console` to extract table data via DOM queries
5. The project info page at `module=items/info&path=21-{entity_id}` shows all subentity containers

## DataTable Parameters
The `load_items_listing()` JS function sends these POST params:
- `reports_id`: report template ID (780 = POs)
- `reports_entities_id`: entity path number
- `path`: entity path
- `page`: page number
- `listing_container`: DOM container ID
- `redirect_to`: navigation target

## Curl Helper (Python)
```python
def curl(url, post_data=None):
    import subprocess, tempfile, os
    tmp = tempfile.mktemp(suffix='.html')
    cmd = ["curl", "-s", "-L", "--compressed",
           "-b", "/tmp/sysleaders_cookies.txt",
           "-c", "/tmp/sysleaders_cookies.txt",
           "-o", tmp,
           "-H", "User-Agent: Mozilla/5.0"]
    if post_data:
        cmd.extend(["-X", "POST", "-d", post_data])
    cmd.append(url)
    subprocess.run(cmd, timeout=30)
    with open(tmp) as f: return f.read()
```

## Pitfalls
- **Use `-o <file>` not `capture_output`** — Python subprocess truncates large HTML
- **CSRF token on one line with `form_session_token`** — regex: `form_session_token.*?value="([^"]+)"`
- **Path 49 is the entity path, 282 is the entity ID** — listing API uses path=49
- **Session cookie path** must be `/samaya/` — set by curl cookie jar
- **DataTables loads via POST**, not GET — must include all form fields
- **No standard REST API** — no JSON endpoints, parse HTML tables
- **cPanel database access** is faster than scraping for labor data — see `sysleaders-database.md`
- **MySQL remote port 3306 is CLOSED** — only localhost via phpMyAdmin
- **SSH port 22 is CLOSED** — no direct MySQL connection
