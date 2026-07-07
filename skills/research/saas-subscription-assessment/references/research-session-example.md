# GLM Coding Plan Research — Worked Example

This is the research session that inspired the `saas-subscription-assessment` skill. The vendor is Zhipu AI (Chinese AI company), their product is the GLM Coding Plan subscription.

## Context

User asked: "what about GLM Coding Plan?" — wanting to know if it fits their workflow (Hermes Agent + opencode-go with DeepSeek V4 Flash).

## Research chain (in order of attempts)

### 1. Direct vendor site: FAIL
- `zhipu.ai` / `open.bigmodel.cn` — curl returned SSR but it was a React SPA, no pricing data
- `bigmodel.cn/pricing` — timed out or returned empty

### 2. Major search engines: BLOCKED
- Google → CAPTCHA
- DuckDuckGo → CAPTCHA
- Bing → Cloudflare challenge

### 3. GitHub community repos: SUCCESS
Searched `api.github.com/search/repositories?q=GLM+Coding+Plan&per_page=5`

Found:
- `supertiny99/dify-plugin-zhipuai-coding` — Dify plugin for GLM Coding Plan. README contained:
  - Full list of supported models (GLM-5.1, 5-Turbo, 5, 4.7, 4.6, 4.5, 4.5-Air)
  - Context window sizes (200K/128K)
  - Capability table (streaming, tool calling, thinking mode, structured output)
  - API endpoint: `https://open.bigmodel.cn/api/coding/paas/v4`
- `CNSeniorious000/zai-coding-plan-dashboard` — usage dashboard. README revealed quota structure (token limits per 5 hours, MCP usage per month)
- `KiwiGaze/glm-for-copilot` — VS Code extension. README contained:
  - Coding Plan vs Standard API comparison
  - Regional endpoints table (International vs Mainland China)
  - Model availability per API mode
  - Feature descriptions

### 4. Official docs subdomain: SUCCESS
`docs.z.ai/coding-plan/overview` — Mintlify docs site, accessible via browser:
- Advantages/benefits section
- Supported tools list (Claude Code, Cline, OpenCode)
- All plans support Vision, Web Search MCP, Web Reader MCP, Zread MCP

### 5. Browser on vendor SPA: SUCCESS
`z.ai` (international portal) — browsed to the pricing page:
- Found actual prices for Lite/Pro/Max tiers
- Monthly vs Quarterly vs Yearly pricing toggles
- Feature bullet lists per tier
- Model comparison: GLM-5.2 #1 Open-Source on LMArena Code

### 6. Official pricing page: PARTIAL
`https://z.ai/pricing` returned 404 on the docs site, but the main site had the pricing rendered in the browser snapshot.

## Key findings extracted

| Plan | Monthly | Yearly | Target |
|------|---------|--------|--------|
| Lite | $18 | $12.60/mo | Small repos |
| Pro | $72 | $50.40/mo | Mid repos |
| Max | $160 | $112/mo | Large repos |

Models: GLM-5.2 (200K ctx, 128K out), tool calling, thinking mode, vision.
Integration: works with Claude Code, Cline, OpenCode, VS Code.

## What made the research work

1. **GitHub was the key** — the vendor's own site was slow/hidden behind login, but community repo READMEs documented everything
2. **Docs subdomain** (`docs.z.ai`) was more accessible than the main marketing site
3. **Browser tool** was essential for the SPA pricing page with interactive billing toggles
4. **Cross-referencing** — the Copilot extension README had the clearest "Coding Plan vs Standard API" comparison
