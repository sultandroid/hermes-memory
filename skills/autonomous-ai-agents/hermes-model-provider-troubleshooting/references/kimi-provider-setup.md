# Kimi / Moonshot Provider Setup

Session-derived detail for adding a Kimi (Moonshot AI) provider to Hermes.

## Key characteristics

| Aspect | Detail |
|--------|--------|
| Endpoint | `https://api.moonshot.cn/v1` (China region) |
| Key prefix | `sk-kimi-` |
| Env var | `KIMI_API_KEY` |
| Transport | `chat_completions` |
| Base URL note | The `.env` template also lists `https://api.kimi.com/coding/v1` for coding-specific usage, but standard chat completions route through `api.moonshot.cn/v1` |

## Full config entry

```yaml
providers:
  kimi:
    api: https://api.moonshot.cn/v1
    default_model: kimi-k2.5
    key_env: KIMI_API_KEY
    models:
      kimi-k2.5: {}
      kimi-k2.5-preview: {}
      kimi-k2.5-32k: {}
      kimi-k2.5-128k: {}
      moonshot-v1-8k: {}
      moonshot-v1-32k: {}
      moonshot-v1-128k: {}
    name: Kimi
    transport: chat_completions
```

## Known models

- **kimi-k2.5** — primary coding model
- **kimi-k2.5-preview** — preview variant
- **kimi-k2.5-32k / 128k** — extended context window versions
- **moonshot-v1-8k / 32k / 128k** — legacy Moonshot models

## Tips

- The existing `.env` template often has Kimi commented out — look for `# KIMI_API_KEY=` and uncomment+set rather than appending a duplicate.
- Keys are 72 characters long with `sk-kimi-` prefix.
- `hermes config check` does NOT validate custom providers added via the `providers:` YAML section — verify by reading the parsed config with `yaml.safe_load()`.
- Terminal output redacts secrets (`***`), but the underlying file has the real value — use `xxd ~/.hermes/.env | grep KIMI` to confirm the raw bytes.
