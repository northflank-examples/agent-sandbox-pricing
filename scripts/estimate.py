#!/usr/bin/env python3
"""Estimate the compute cost of your own sandbox workload across providers.

Example:
    python3 scripts/estimate.py --sandboxes 100 --minutes 60 --vcpu 2 --memory 4 --cpu-busy 0.25

Prints list-price estimates for compute plus disk while running (no free credits,
egress or persistent storage) and the cheapest published plan that fits your concurrency.
"""

from __future__ import annotations

import argparse

from model import Workload, hourly_cost, load, pick_tier, workload_cost


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sandboxes", type=int, default=100, help="total sandboxes run (default 100)")
    ap.add_argument("--minutes", type=float, default=60, help="wall-clock minutes per sandbox (default 60)")
    ap.add_argument("--vcpu", type=float, default=2, help="vCPUs per sandbox (default 2)")
    ap.add_argument("--memory", type=float, default=4, help="GiB RAM per sandbox (default 4)")
    ap.add_argument("--disk", type=float, default=10, help="GB disk per sandbox (default 10)")
    ap.add_argument("--cpu-busy", type=float, default=0.25,
                    help="fraction of runtime the CPU is busy, 0-1 (default 0.25). "
                         "Only affects active-CPU and usage-billed providers.")
    ap.add_argument("--concurrency", type=int, default=None, help="sandboxes running at once (default: all)")
    args = ap.parse_args()

    w = Workload(args.sandboxes, args.minutes, args.vcpu, args.memory, args.disk, args.cpu_busy, args.concurrency)
    providers = sorted(load()["providers"], key=lambda p: workload_cost(p, w) or 1e9)

    print(f"\n{w.count} sandboxes x {w.minutes:g} min, {w.vcpu:g} vCPU / {w.memory_gib:g} GiB / "
          f"{w.disk_gb:g} GB disk, CPU {w.cpu_utilisation:.0%} busy, "
          f"{w.concurrency or w.count} concurrent\n")
    print(f"{'Provider':<22}{'per sandbox-hr':>16}{'compute total':>16}   plan that fits")
    print("-" * 100)
    for p in providers:
        h, t = hourly_cost(p, w), workload_cost(p, w)
        h_s = f"${h:.4f}" if h is not None else "n/a"
        t_s = f"${t:,.2f}" if t is not None else "n/a"
        print(f"{p['name']:<22}{h_s:>16}{t_s:>16}   {pick_tier(p, w)}")
    print("\nList prices from data/pricing.json; verify against each provider's pricing page.\n")


if __name__ == "__main__":
    main()
