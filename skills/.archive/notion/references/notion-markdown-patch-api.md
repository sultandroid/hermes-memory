# Notion Markdown PATCH API — ntn CLI Patterns

## API Endpoint

`PATCH /v1/pages/{page_id}/markdown`

This endpoint allows inserting, replacing, or updating page content as Markdown.

## Body Structure

All operations require:
```json
{
  "type": "<operation_type>",
  "<operation_type>": {
    "content": "... markdown string ..."
  }
}
```

### Operation Types

| Type | Effect | Use Case |
|------|--------|----------|
| `insert_content` | Appends content at the **end** of the page | Adding new sections without disturbing existing content, databases, or child pages |
| `replace_content` | Replaces **all** page content | ⚠️ WARNING: This deletes ALL child databases. Notion will block it listing what would be deleted. |

### INSERT_CONTENT (safest — appends, does not delete)

```bash
ntn api v1/pages/{page_id}/markdown -X PATCH \
  -d '{"type":"insert_content","insert_content":{"content":"## New Section\n\n- Item 1\n- Item 2"}}'
```

Or use a JSON file:
```bash
ntn api v1/pages/{page_id}/markdown -X PATCH -d "$(cat /tmp/update.json)"
```

### REPLACE_CONTENT (dangerous — deletes everything not included)

```json
{
  "type": "replace_content",
  "replace_content": {
    "new_str": "... full page markdown ...",
    "allow_deleting_content": false
  }
}
```

Notion will reject unless you include existing child pages via `<database url="...">` tags.

### Troubleshooting

- **Error: "body.type should be defined"** — Add `"type": "insert_content"`.
- **Error: "body.insert_content should be defined"** — Markdown goes under `insert_content.content` (not `insert_content.markdown`).
- **Error: "body.replace_content.new_str should be defined"** — `replace_content` uses `new_str`, NOT `content`.
- **Error: "Would delete N child page(s)"** — Switch to `insert_content` or include child pages as `<database>` tags.

### Key Lessons
1. **Always try `insert_content` first** — safest, appends without deleting.
2. **Read the error message fully** — Notion returns detailed validation errors telling you exactly which field is missing.
3. **`insert_content.content` is a plain markdown string**, not a JSON array of blocks.
