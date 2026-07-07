# Search & Discovery Patterns

Systematic techniques for finding user content by recency, workspace structure, or partial name — compensating for the Notion API's lack of date-based search filters.

## Strategy: Discover All Accessible Items

The Notion search API (`POST /v1/search`) supports `query=""` to return **all items** the integration can see (capped at 100 by default — paginate with `start_cursor` for more).

```bash
ntn api v1/search query=""
# Returns all pages + databases shared with the integration
```

Each result includes `created_time`, `last_edited_time`, `object` type, `parent` (for hierarchy), and properties with the title.

## Strategy: Filter by Date Client-Side

No API parameter for date range — scrape all items and filter by timestamp in Python:

```python
# After getting all results
recent = [r for r in results
          if r.get('created_time','') >= '2026-06-01'
          or r.get('last_edited_time','') >= '2026-06-01']
```

**Use `last_edited_time`** (not just `created_time`) — the user may have modified an existing page yesterday.

## Strategy: Explore Workspace Hierarchy

Follow parent chains to understand where databases live in the page tree:

1. **Get a database's parent:**
   ```bash
   ntn api v1/data_sources/{data_source_id}
   # Returns parent.type (page_id or database_id) + parent ID
   ```
2. **Get a page's parent:**
   ```bash
   ntn api v1/pages/{page_id}
   # Returns parent.type + parent ID
   ```
3. **Distinguish database vs data source ID:**
   - `database_id` → use as `parent: {"database_id": "..."}` when creating pages
   - `data_source_id` → use in `POST /v1/data_sources/{id}/query`
   - Both may differ for the same Notion database
   - To get the data_source_id from a database page, check `parent.data_source_id`

## Strategy: Find All Databases in Workspace

```bash
ntn api v1/search filter[value]=data_source filter[property]=object
# Returns all databases with their title, parent, and IDs
```

## Strategy: Query a Database for Recent Entries

```bash
ntn api v1/data_sources/{data_source_id}/query -X POST
# Returns up to 100 entries — filter client-side by timestamp
```

For large databases, use server-side sort:
```bash
echo '{"sorts": [{"property": "Created time", "direction": "descending"}], "page_size": 25}' | \
  ntn api v1/data_sources/{data_source_id}/query -X POST --json -
```

## Pitfalls

### ntn + python pipe breaks on special chars
❌ `ntn api ... | python3 -c "import json; ..."` — Arabic text, control chars, or large JSON can break the pipe with `JSONDecodeError: Expecting value: line 1 column 1`

✅ **Workaround:** save to temp file first, then Python reads the file:
```bash
ntn api v1/search query="" > /tmp/notion_results.json
python3 -c "
import json
with open('/tmp/notion_results.json') as f:
    d = json.load(f)
    # process d['results']...
"
```

### 404 despite page existing
The page/database is **not shared** with your integration. Fix: open the page in Notion → `...` → `Connect to` → select your integration name.

### Searching for Arabic terms
Search API handles Arabic characters fine (`قيد`, `اجتماع`, `محضر`), but results are limited to items the integration can see. Most user's actual content pages may not be shared.

## Quick Recipe: "Find what the user did in Notion yesterday"

```bash
ntn api v1/search query="" > /tmp/notion_all.json
python3 -c "
import json
with open('/tmp/notion_all.json') as f:
    d = json.load(f)
yesterday = '2026-06-01'
for r in d.get('results', []):
    if r.get('created_time','')[:10] >= yesterday or r.get('last_edited_time','')[:10] >= yesterday:
        props = r.get('properties', {})
        title = ''
        for k, v in props.items():
            if v.get('type') == 'title':
                arr = v.get('title', [])
                if arr:
                    title = arr[0].get('plain_text', '')
        print(f\"{r.get('created_time','')[:10]} | {r.get('last_edited_time','')[:10]} | {title[:120]}\")
"
```

If nothing appears, the user's content is likely in pages/databases not shared with the integration. Ask the user to share the target page, or check if the content lives under a top-level page that needs connecting.
