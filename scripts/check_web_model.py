#!/usr/bin/env python3
"""Check that the web estimator's cost model (web/model.js) matches scripts/model.py.

Runs both models over a grid of workloads for every provider and fails on any
difference. Requires Node.js 18+.

Usage:
    python3 scripts/check_web_model.py
"""

from __future__ import annotations

import itertools
import json
import subprocess
import sys
from dataclasses import asdict

from model import ROOT, Workload, hourly_cost, load, pick_tier, workload_cost


def workloads() -> list[Workload]:
    grid = itertools.product(
        [1, 100, 1000],            # count
        [0.5, 5, 60, 1440, 43800],  # minutes
        [0.1, 0.5, 1, 2, 3, 4, 8, 16, 64],  # vcpu
        [0.25, 2, 4, 6, 12, 32, 512],  # memory_gib
        [0, 10, 20, 50, 100],         # disk_gb
        [0.05, 0.25, 1.0],         # cpu_utilisation
        [None, 5, 150, 2000],      # concurrency
    )
    return [Workload(*args) for args in grid]


def main() -> int:
    providers = load()["providers"]
    ws = workloads()
    payload = {
        "providers": providers,
        "workloads": [{**asdict(w), "memory_gib": w.memory_gib, "disk_gb": w.disk_gb} for w in ws],
    }
    res = subprocess.run(
        ["node", str(ROOT / "web" / "parity.mjs")],
        input=json.dumps(payload), capture_output=True, text=True, check=True,
    )
    js = json.loads(res.stdout)

    failures = 0
    for w, row in zip(ws, js):
        for p, got in zip(providers, row):
            want = {"hourly": hourly_cost(p, w), "total": workload_cost(p, w), "tier": pick_tier(p, w)}
            for key in ("hourly", "total"):
                a, b = want[key], got[key]
                same = (a is None and b is None) or (a is not None and b is not None and abs(a - b) <= 1e-9 * max(1, abs(a)))
                if not same:
                    failures += 1
                    print(f"FAIL {p['id']} {key}: python={a} js={b} for {w}")
            if want["tier"] != got["tier"]:
                failures += 1
                print(f"FAIL {p['id']} tier: python={want['tier']!r} js={got['tier']!r} for {w}")
    checks = len(ws) * len(providers) * 3
    print(f"{checks - failures}/{checks} web-model checks match scripts/model.py")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
