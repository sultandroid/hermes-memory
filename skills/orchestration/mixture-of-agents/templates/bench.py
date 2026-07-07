#!/usr/bin/env python3
"""Smoke + latency bench for moa.py or moa-cloud.py."""
import subprocess, time, sys
from pathlib import Path

QUERIES = [
    ("simple",  "Define the word 'serendipity' in one sentence."),
    ("complex", "Compare PostgreSQL and SQLite for a read-heavy local analytics app. List trade-offs."),
    ("code",    "Write a Python function that returns the n-th Fibonacci number using memoization."),
    ("ambig",   "Should we ship this feature today or wait for QA? Give a balanced view."),
]

# Auto-pick orchestrator: prefer cloud if available
script = Path(__file__).parent / ("moa-cloud.py" if (Path(__file__).parent / "moa-cloud.py").exists() else "moa.py")
print(f"Using: {script.name}\n")

for label, q in QUERIES:
    print(f"\n{'='*60}\n[{label}] {q}\n{'='*60}")
    cmd = ["python3", str(script), "-v", "--force-tier", "complex" if label != "simple" else "simple", q]
    t0 = time.perf_counter()
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    dt = time.perf_counter() - t0
    print(f"--- wall {dt:.2f}s ---")
    print(r.stdout)
    if r.stderr:
        print("STDERR:", r.stderr[-300:])
