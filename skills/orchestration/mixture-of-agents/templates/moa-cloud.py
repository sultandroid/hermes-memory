#!/usr/bin/env python3
"""Cloud Mixture-of-Agents orchestrator — OpenRouter-compatible.

Same architecture as local moa.py, but hits cloud chat-completion APIs.
Works with any provider that exposes OpenAI-compatible /chat/completions:
  - OpenRouter (https://openrouter.ai/api/v1)
  - Groq      (https://api.groq.com/openai/v1)
  - OpenAI    (https://api.openai.com/v1)
  - Together  (https://api.together.xyz/v1)

Usage:
  export OPENROUTER_API_KEY=sk-or-...
  export MOA_BASE_URL=https://openrouter.ai/api/v1
  python moa-cloud.py "Your question"
  python moa-cloud.py --provider groq "Your question"

Config: ./config-cloud.yaml
"""
import argparse, asyncio, os, sys, time
from pathlib import Path
import httpx, yaml

CFG = Path(__file__).parent / "config-cloud.yaml"

def load_cfg():
    with CFG.open() as f:
        return yaml.safe_load(f)

def get_env(name, default=None):
    v = os.environ.get(name, default)
    if not v:
        print(f"Missing env var: {name}", file=sys.stderr)
        sys.exit(2)
    return v

async def chat(client, base_url, api_key, model, system, user, timeout, retries=2):
    """Call /chat/completions. Returns (text, elapsed_s, err)."""
    t0 = time.perf_counter()
    last_err = None
    for attempt in range(retries + 1):
        try:
            r = await client.post(
                f"{base_url}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    "temperature": 0.6,
                    "max_tokens": 2048,
                },
                timeout=timeout,
            )
            if r.status_code == 429 and attempt < retries:
                await asyncio.sleep(2 ** attempt)
                continue
            r.raise_for_status()
            text = r.json()["choices"][0]["message"]["content"].strip()
            return text, time.perf_counter() - t0, None
        except Exception as e:
            last_err = str(e)
            if attempt < retries:
                await asyncio.sleep(2 ** attempt)
    return "", time.perf_counter() - t0, last_err

async def run_proposers(client, base, key, cfg, tier, user):
    proposers = cfg["roles"][f"proposers_{tier}"]
    tasks = [chat(client, base, key, p["model"], p["system"], user, cfg["timeouts"]["proposer_s"]) for p in proposers]
    return list(zip(proposers, await asyncio.gather(*tasks)))

async def run_router(client, base, key, cfg, user):
    return await chat(client, base, key, cfg["roles"]["router"]["model"], cfg["roles"]["router"]["system"], user, cfg["timeouts"]["router_s"])

async def run_aggregator(client, base, key, cfg, user, proposer_outputs):
    agg = cfg["roles"]["aggregator"]
    block = "\n\n".join(
        f"--- Response {i+1} (from {p['model']}) ---\n{txt}"
        for i, (p, (txt, _, _)) in enumerate(proposer_outputs) if txt
    ) or "(All proposers failed.)"
    prompt = f"Original question:\n{user}\n\nMultiple responses to synthesize:\n{block}\n\nProduce ONE final answer."
    return await chat(client, base, key, agg["model"], agg["system"], prompt, cfg["timeouts"]["aggregator_s"])

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", nargs="?")
    ap.add_argument("--force-tier", choices=["simple", "complex"])
    ap.add_argument("--no-aggregate", action="store_true")
    ap.add_argument("--provider", choices=["openrouter", "groq", "openai", "together"], default="openrouter")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    base_urls = {
        "openrouter": "https://openrouter.ai/api/v1",
        "groq": "https://api.groq.com/openai/v1",
        "openai": "https://api.openai.com/v1",
        "together": "https://api.together.xyz/v1",
    }
    keys = {
        "openrouter": "OPENROUTER_API_KEY",
        "groq": "GROQ_API_KEY",
        "openai": "OPENAI_API_KEY",
        "together": "TOGETHER_API_KEY",
    }
    base = os.environ.get("MOA_BASE_URL") or base_urls[args.provider]
    key = get_env(keys[args.provider])

    prompt = args.prompt or sys.stdin.read().strip()
    if not prompt:
        print("No prompt.", file=sys.stderr); sys.exit(1)

    cfg = load_cfg()
    async with httpx.AsyncClient() as client:
        tier = args.force_tier
        if not tier:
            router_text, router_t, err = await run_router(client, base, key, cfg, prompt)
            tier = "complex" if "complex" in router_text.lower() else "simple"
            if err: tier = "complex"
            if args.verbose:
                print(f"[router] {router_t:.2f}s -> {tier!r}", file=sys.stderr)
        if args.verbose:
            print(f"[tier] {tier}", file=sys.stderr)

        proposer_results = await run_proposers(client, base, key, cfg, tier, prompt)
        for p, (txt, t, err) in proposer_results:
            if args.verbose:
                print(f"[{p['model']}] {t:.2f}s {'OK' if txt else f'ERR {err}'}", file=sys.stderr)

        if args.no_aggregate:
            for p, (txt, _, _) in proposer_results:
                print(f"\n=== {p['model']} ===\n{txt or '(empty)'}")
            return

        agg_text, agg_t, err = await run_aggregator(client, base, key, cfg, prompt, proposer_results)
        if err:
            for _, (txt, _, _) in proposer_results:
                if txt: print(txt); return
            print(f"Aggregator error: {err}", file=sys.stderr); sys.exit(2)
        if args.verbose:
            print(f"[aggregator] {agg_t:.2f}s", file=sys.stderr)
        print(agg_text)

if __name__ == "__main__":
    asyncio.run(main())
