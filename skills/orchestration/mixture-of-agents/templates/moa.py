#!/usr/bin/env python3
"""Local Mixture-of-Agents orchestrator over Ollama HTTP API.

Usage:
  pip install --user httpx pyyaml
  python moa.py "What is the capital of France?"
  python moa.py --force-tier complex "Compare PostgreSQL and SQLite for analytics"
  echo "prompt" | python moa.py -

Config: ./config.yaml (same dir)
"""
import argparse, asyncio, sys, time
from pathlib import Path
import httpx, yaml

CFG = Path(__file__).parent / "config.yaml"
OLLAMA = "http://localhost:11434"

def load_cfg():
    with CFG.open() as f:
        return yaml.safe_load(f)

async def chat(client, model, system, user, timeout):
    """Call Ollama /api/chat. Returns (text, elapsed_s, err)."""
    t0 = time.perf_counter()
    try:
        r = await client.post(
            f"{OLLAMA}/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "stream": False,
                "options": {"temperature": 0.6, "num_ctx": 8192},
            },
            timeout=timeout,
        )
        r.raise_for_status()
        text = r.json().get("message", {}).get("content", "").strip()
        return text, time.perf_counter() - t0, None
    except Exception as e:
        return "", time.perf_counter() - t0, str(e)

async def run_proposers(client, cfg, tier, user):
    proposers = cfg["roles"][f"proposers_{tier}"]
    tasks = [chat(client, p["model"], p["system"], user, cfg["timeouts"]["proposer_s"]) for p in proposers]
    return list(zip(proposers, await asyncio.gather(*tasks)))

async def run_router(client, cfg, user):
    return await chat(client, cfg["roles"]["router"]["model"], cfg["roles"]["router"]["system"], user, cfg["timeouts"]["router_s"])

async def run_aggregator(client, cfg, user, proposer_outputs):
    agg = cfg["roles"]["aggregator"]
    block = "\n\n".join(
        f"--- Response {i+1} (from {p['model']}) ---\n{txt}"
        for i, (p, (txt, _, _)) in enumerate(proposer_outputs) if txt
    ) or "(All proposers failed.)"
    prompt = f"Original question:\n{user}\n\nMultiple responses to synthesize:\n{block}\n\nProduce ONE final answer."
    return await chat(client, agg["model"], agg["system"], prompt, cfg["timeouts"]["aggregator_s"])

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", nargs="?")
    ap.add_argument("--force-tier", choices=["simple", "complex"])
    ap.add_argument("--no-aggregate", action="store_true")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    prompt = args.prompt or sys.stdin.read().strip()
    if not prompt:
        print("No prompt.", file=sys.stderr); sys.exit(1)

    cfg = load_cfg()
    async with httpx.AsyncClient() as client:
        tier = args.force_tier
        if not tier:
            router_text, router_t, err = await run_router(client, cfg, prompt)
            tier = "complex" if "complex" in router_text.lower() else "simple"
            if err: tier = "complex"  # safe default
            if args.verbose:
                print(f"[router] {router_t:.2f}s -> {tier!r}", file=sys.stderr)
        if args.verbose:
            print(f"[tier] {tier}", file=sys.stderr)

        proposer_results = await run_proposers(client, cfg, tier, prompt)
        for p, (txt, t, err) in proposer_results:
            if args.verbose:
                print(f"[{p['model']}] {t:.2f}s {'OK' if txt else f'ERR {err}'}", file=sys.stderr)

        if args.no_aggregate:
            for p, (txt, _, _) in proposer_results:
                print(f"\n=== {p['model']} ===\n{txt or '(empty)'}")
            return

        agg_text, agg_t, err = await run_aggregator(client, cfg, prompt, proposer_results)
        if err:
            for _, (txt, _, _) in proposer_results:
                if txt: print(txt); return
            print(f"Aggregator error: {err}", file=sys.stderr); sys.exit(2)
        if args.verbose:
            print(f"[aggregator] {agg_t:.2f}s", file=sys.stderr)
        print(agg_text)

if __name__ == "__main__":
    asyncio.run(main())
