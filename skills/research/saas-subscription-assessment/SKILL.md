---
name: saas-subscription-assessment
description: Evaluate SaaS/API subscriptions — multi-pronged pricing research, feature comparison, fit assessment, and buy/don't-buy recommendation.
category: research
---

# SaaS Subscription Assessment

Use when the user asks "Should I subscribe to X?", "Is X worth it?", "Compare X vs Y", "What about [product name]?", or any other product/plan evaluation question about a SaaS, API, or subscription service.

## Multi-pronged research approach

When search engines are blocked (common), use this fallback chain:

1. **Direct vendor site** — `curl` the pricing page first (some return SSR HTML even if it's a SPA marketing page)
2. **Official docs** — many vendors have `docs.<vendor>.com` or a developer portal that documents pricing, quota limits, and supported models outside the marketing SPA
3. **GitHub community** — search `https://api.github.com/search/repositories?q=<vendor>+<product>` or `<product-name>+client/plugin`. Community-maintained READMEs often contain:
   - Exact pricing (plans, tiers, monthly/annual)
   - Model lists and capability tables
   - Integration requirements and endpoints
   - Migration guides, migration warnings, and legacy plan info
   - Real user reviews in README endorsements
4. **Browser for SPA pages** — use `browser_navigate` + `browser_snapshot` for sites rendered by React/Next.js that curl can't parse. Interact with billing toggles (monthly vs yearly) and plan feature lists
5. **API endpoints** — some SPA sites load pricing data from public JSON API endpoints (`/api/pricing`, `/api/plans`) that can be hit directly

## Comparison framework

Present findings as:

| Aspect | Product being evaluated | User's current setup |
|--------|----------------------|---------------------|
| Cost (mo/yr) | $X / $Y | $Z |
| Model/feature quality | ... | ... |
| Key capabilities | ... | ... |
| Limits/quotas | ... | ... |
| Integration fit | ... | ... |

End with a **clear recommendation**: Buy / Skip / Conditional, with the rationale tied to the user's specific workflow.

## Reference files

- [research-session-example.md](references/research-session-example.md) — worked example from the GLM Coding Plan research session showing the multi-pronged fallback chain in action.

## Pitfalls

- **Chinese vendor sites** (bigmodel.cn, etc.) frequently time out from international IPs — skip straight to GitHub community repos and docs subdomains
- **SPA sites** (React/Next.js) don't render via `curl` — use the browser tool or look for a separate docs subdomain (`docs.<vendor>.com`)
- **Pricing behind login wall** — check docs pages, community READMEs, or third-party integration repos instead; these often document pricing without authentication
- **Always understand the user's current stack first** before evaluating a product — the fit assessment is relative to what they already have
- **"Free" tiers with usage caps** — don't assume free means unlimited; check for rate limits, token caps, and model restrictions
- **Don't trust vendor self-reported benchmarks alone** — cross-reference with community experience and third-party leaderboards (LMArena, etc.)
- **Regional pricing** — some vendors (especially Chinese) have different pricing for international vs mainland China regions; check which endpoint you're looking at

## Related skills

- `product-research` — for physical/industrial products (complementary, not overlapping)
- `spike` — for throwaway technical validation of a tool/API rather than pricing research
