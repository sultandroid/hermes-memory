# Nous Portal / API Provider Setup

Session-derived detail on the two distinct NousResearch provider paths in Hermes.

## Built-in `nous` provider (OAuth)

The **nous** provider name in Hermes uses OAuth device code flow via `portal.nousresearch.com`.

```bash
hermes auth add nous     # opens browser for device-code login
```

If OAuth credentials already exist at `~/.hermes/shared/nous_auth.json`, the command rehydrates them without a fresh login.

**Verification:**
```bash
hermes auth list | grep nous
# should show: device_code   oauth   device_code ←
```

**Test:**
```bash
hermes chat -q "OK" --provider nous --model nousresearch/hermes-4-70b
```

OAuth is preferred when the user has a Nous subscription — it routes at provider/subscriber pricing rather than OpenRouter markup.

## Custom `nous-api` provider (API key)

API keys with the `sk-nous-` prefix can be used via the Nous inference gateway at `https://inference-api.nousresearch.com/v1`. This endpoint is OpenRouter-proxied — it exposes the full OpenRouter model catalog (266+ models) but at OpenRouter pricing.

### Setup

1. Add the key to `.env`:
   ```bash
   NOUS_API_KEY=sk-nous-...
   ```

2. Add a custom provider entry in `~/.hermes/config.yaml`:
   ```yaml
   providers:
     nous-api:
       name: Nous API
       api: https://inference-api.nousresearch.com/v1
       key_env: NOUS_API_KEY
       transport: chat_completions
       default_model: nousresearch/hermes-4-70b
       models:
         nousresearch/hermes-4-70b: {}
         nousresearch/hermes-4-405b: {}
         deepseek/deepseek-v4-flash: {}
         deepseek/deepseek-v4-pro: {}
   ```

3. Verify the endpoint is reachable and the key works:
   ```bash
   curl -s "https://inference-api.nousresearch.com/v1/models" \
     -H "Authorization: Bearer $NOUS_API_KEY" | python3 -m json.tool | head -20
   ```

### Pitfalls

- **Model naming**: `nousresearch/hermes-4-70b` — NOT `nousresearch/hermes-4` (the latter does not exist in the catalog).
- **Namespace**: Due to OpenRouter proxying, all model IDs use the `provider/model` format from OpenRouter (e.g., `deepseek/deepseek-v4-pro`, `moonshotai/kimi-k2.7-code`).
- **Dual provider confusion**: If both `nous` (OAuth) and `nous-api` (API key) appear in the model list, remove the unwanted one with `hermes auth remove nous <index>` and clean up stale `providers:` YAML entries. The built-in `nous` name may still appear in the picker — it's part of Hermes core and cannot be removed, but it will show as unauthenticated.
- **Key truncation risk**: When writing API keys via `execute_code`, the system redacts keys in display output but the actual variable retains the full value. For bash commands, prefer file-based input or `hermes auth add` with `--api-key` to avoid shell quoting issues with special characters.
- **Inference URL**: Must be `https://inference-api.nousresearch.com/v1` — `api.nousresearch.com` does not resolve (NXDOMAIN). The correct DNS is a Railway.app hostname behind `inference-api.nousresearch.com`.
