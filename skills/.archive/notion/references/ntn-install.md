# ntn CLI Installation (macOS)

## Quick Install

```bash
curl -fsSL https://ntn.dev | NTN_INSTALL_DIR="$HOME/.local/bin" bash
```

> **Why `NTN_INSTALL_DIR`?** The default target `/usr/local/bin/ntn` requires `sudo`.
> Set it to a user-writable directory like `~/.local/bin` to avoid permission prompts.

## Environment Setup

Add to `~/.hermes/.env`:

```
# ntn reads NOTION_API_TOKEN (NOT NOTION_API_KEY)
export NOTION_API_TOKEN=***  
export NOTION_KEYRING=0                          
export NOTION_WORKSPACE_ID="<workspace-uuid>"    
export PATH="$HOME/.local/bin:$PATH"             
```

## Find Workspace ID

```bash
curl -s "https://api.notion.com/v1/users" \
  -H "Authorization: Bearer *** \
  -H "Notion-Version: 2025-09-03" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for u in d['results']:
    if u.get('type') == 'bot' and u.get('workspace_name'):
        print('Workspace:', u.get('workspace_name'))
        print('Workspace ID:', u.get('workspace_id'))
"
```

## Verification

```bash
ntn --version
ntn api v1/users | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d[\"results\"])} users')"
```

## Token Format

| Tool | Required Format | Source |
|------|----------------|--------|
| curl / REST API | `secret_...` | Notion integrations page |
| ntn CLI | `ntn_...` | Same integration page |

## Troubleshooting

**"No workspace selected" error:** Set `NOTION_WORKSPACE_ID` in environment.

**"Public API request failed (400)":** Try `ntn api v1/users` for basic connectivity first.

**Token confusion:** If curl works but ntn doesn't, check you're using the right token format for each tool.
