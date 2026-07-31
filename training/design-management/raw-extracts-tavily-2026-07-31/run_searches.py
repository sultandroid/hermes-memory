#!/usr/bin/env python3
"""Run all 10 theme searches through Tavily Python SDK and save raw output per query.

For each theme we run one primary query and (where useful) a secondary angle. Each
saved raw file is keyed by theme number for downstream extraction.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

from tavily import TavilyClient

RAW_DIR = Path("/tmp/tavily-research-design-mgmt/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

api_key = os.environ.get("TAVILY_API_KEY")
if not api_key:
    raise SystemExit("TAVILY_API_KEY not set")

client = TavilyClient(api_key=api_key)

# (theme_number, primary_query, secondary_query)
searches = [
    (1, "RIBA Plan of Work Saudi Arabia construction adoption",
        "RIBA Plan of Work 2020 overview stages design management"),
    (2, "design freeze disputes construction FIDIC",
        "design freeze construction contractor claim delay Saudi GCC"),
    (3, "design change variation order FIDIC Saudi construction",
        "Al Tamimi variation order construction FIDIC"),
    (4, "designer's professional indemnity insurance cap GCC construction",
        "architect professional liability limitation period Saudi Building Code"),
    (5, "technical design submittal approval dispute Saudi construction",
        "design approval consultant employer rejection FIDIC"),
    (6, "as-built drawings handover construction defects liability GCC",
        "as-built drawings contractor obligation final account"),
    (7, "value engineering construction risk balance Saudi",
        "value engineering cost saving change order construction GCC"),
    (8, "constructability review pre-construction design check",
        "constructability review contractor design risk Saudi"),
    (9, "design coordination meetings DCM frequency construction",
        "design coordination meeting BIM LOD 300 350 GCC"),
    (10, "multi-discipline design coordination failure MEP structural",
        "MEP structural coordination clash detection BIM Saudi construction"),
]

# Authoritative sources we'll prefer to bias
PRIORITY_DOMAINS = [
    "tamimi.com", "pinsentmasons.com", "pinsentmasons.com/out-law",
    "sadr.org", "scciarb.org", "scca.org.sa",
    "hkacompetition.com", "hka.com", "stonehaven.uk",
    "nissenrichardsstudio.com",
    "atkinsglobal.com", "atkinsrealis.com",
    "keo.com", "idom.com", "burohappold.com",
    "riba.org", "architecture.com",
    "meed.com", "thenationalnews.com", "arabnews.com",
    "fenwickelliott.com", "mayerbrown.com", "reedsmith.com",
    "kluwerarbitrationblog.com", "acerislaw.com", "kabinelaw.com",
    "nortonrosefulbright.com",
]

for theme_no, primary, secondary in searches:
    for label, query in [("primary", primary), ("secondary", secondary)]:
        outfile = RAW_DIR / f"theme{theme_no:02d}_{label}.json"
        if outfile.exists():
            print(f"skip {outfile.name}")
            continue
        try:
            res = client.search(
                query=query,
                max_results=8,
                search_depth="advanced",
                include_raw_content="markdown",
                include_answer=False,
            )
            outfile.write_text(json.dumps(res, indent=2, ensure_ascii=False))
            n = len(res.get("results", []))
            print(f"[theme {theme_no:02d}/{label}] {n} results -> {outfile.name}")
        except Exception as e:
            print(f"[theme {theme_no:02d}/{label}] ERROR {e}")
        time.sleep(0.5)

print("\nDone.")
