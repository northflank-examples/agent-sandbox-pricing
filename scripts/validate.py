#!/usr/bin/env python3
"""Check the cost model against prices and worked examples published by the vendors themselves.

Every case below is copied from an official pricing page (URL in the comment). If a
vendor changes its rates, or the model in model.py drifts, these checks fail.

Usage:
    python3 scripts/validate.py
"""

from __future__ import annotations

import sys

from model import Workload, hourly_cost, load

PROVIDERS = {p["id"]: p for p in load()["providers"]}

# (provider, description, workload, published USD amount, tolerance in USD)
CASES: list[tuple[str, str, Workload, float, float]] = []


def case(pid: str, desc: str, w: Workload, published: float, tol: float = 0.0006) -> None:
    CASES.append((pid, desc, w, published, tol))


# Northflank: fixed compute plans, hourly price as listed. https://northflank.com/pricing
for name, vcpu, mem, hr in [
    ("nf-compute-10", 0.1, 0.25, 0.0038), ("nf-compute-100-1", 1, 1, 0.0250), ("nf-compute-100-4", 1, 4, 0.0500),
    ("nf-compute-200", 2, 4, 0.0667), ("nf-compute-200-8", 2, 8, 0.1000), ("nf-compute-400", 4, 8, 0.1333),
    ("nf-compute-200-16", 2, 16, 0.1667), ("nf-compute-400-16", 4, 16, 0.2000), ("nf-compute-800-8", 8, 8, 0.2000),
    ("nf-compute-800-16", 8, 16, 0.2667), ("nf-compute-800-24", 8, 24, 0.3333), ("nf-compute-800-32", 8, 32, 0.4000),
    ("nf-compute-1200-24", 12, 24, 0.4000), ("nf-compute-800-40", 8, 40, 0.4667), ("nf-compute-1600-32", 16, 32, 0.5333),
    ("nf-compute-2000-40", 20, 40, 0.6667), ("nf-compute-32-128", 32, 128, 1.6000), ("nf-compute-32-488", 32, 488, 4.6000),
]:
    case("northflank", f"plan {name} per hour", Workload(1, 60, vcpu, mem), hr, 0.0016)

# E2B: usage calculator example "100 sandboxes x 10 hrs = 1,000 hrs ... Usage Cost $166"
# at the default 2 vCPU / 4 GiB size. https://e2b.dev/pricing
case("e2b", "calculator: 1,000 sandbox-hours at default size", Workload(100, 600, 2, 4), 166, 0.5)

# Runloop: size table (CPU / memory / disk, $/hour). https://docs.runloop.ai/docs/devboxes/configuration/sizes
for name, vcpu, mem, disk, hr in [
    ("X_SMALL", 0.5, 1, 4, 0.0806), ("SMALL", 1, 2, 4, 0.1598), ("MEDIUM", 2, 4, 8, 0.3195),
    ("LARGE", 2, 8, 16, 0.4231), ("X_LARGE", 4, 16, 16, 0.8407), ("XX_LARGE", 8, 32, 16, 1.6760),
]:
    case("runloop", f"size {name} per hour", Workload(1, 60, vcpu, mem, disk), hr)

# Vercel: "Example calculations" table, 10% CPU utilisation, iad1.
# https://vercel.com/docs/vercel-sandbox/pricing
for desc, minutes, vcpu, mem, total in [
    ("Quick test", 2, 1, 2, 0.0018), ("AI code validation", 5, 2, 4, 0.0092),
    ("Build and test", 30, 4, 8, 0.1104), ("Long-running task", 120, 8, 16, 0.8832),
]:
    case("vercel", f"example '{desc}'", Workload(1, minutes, vcpu, mem, cpu_utilisation=0.1), total, 0.0002)

# Sprites: pricing page examples (CPU + memory + hot storage; cold storage excluded,
# because it accrues while the Sprite is not running). https://fly.io/sprites
# Sprites rounds each line item to the cent before summing, so allow up to 3 x half a cent.
# "Claude Code Session": 4 h, averaging 30% of 2 CPUs and 1.5 GB, 5 GB hot storage -> $0.09 + $0.13 + $0.01
case("sprites", "example 'Claude Code Session' (CPU+RAM+hot storage)",
     Workload(1, 240, 2, 1.5, 5, cpu_utilisation=0.3), 0.09 + 0.13 + 0.01, 0.015)
# "Web App": 30 h, averaging 10% of 2 CPUs and 1 GB, 3 GB hot storage -> $0.23 + $0.66 + $0.06
case("sprites", "example 'Web App' (CPU+RAM+hot storage)",
     Workload(1, 1800, 2, 1, 3, cpu_utilisation=0.1), 0.23 + 0.66 + 0.06, 0.015)


def main() -> int:
    failed = 0
    for pid, desc, w, published, tol in CASES:
        p = PROVIDERS[pid]
        hourly = hourly_cost(p, w)
        ours = None if hourly is None else hourly * w.minutes / 60 * w.count
        ok = ours is not None and abs(ours - published) <= tol
        failed += not ok
        ours_s = "n/a" if ours is None else f"${ours:.4f}"
        print(f"{'ok  ' if ok else 'FAIL'} {p['name']:<20} {desc:<52} published ${published:<9.4f} model {ours_s}")
    print(f"\n{len(CASES) - failed}/{len(CASES)} vendor-published figures reproduced")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
