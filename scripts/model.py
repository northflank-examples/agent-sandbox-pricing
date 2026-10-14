"""Cost model shared by generate.py and estimate.py.

Billing models (see comparisons/billing-models.md):

  allocated         - pay for reserved vCPU and memory for the whole runtime
  request_or_usage  - pay for max(reserved, actually used); priced as allocated here
  active_cpu        - pay for memory for the whole runtime, CPU only while busy
  usage             - pay for CPU time and memory actually consumed

Providers that only sell fixed sizes list them under compute.fixed_sizes; the
cheapest size that fits the requested vCPU and memory is billed.

All costs are list prices for compute plus disk billed while running. Plan fees are reported separately by
pick_tier(); free credits, egress and persistent storage are excluded.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load() -> dict:
    return json.loads((ROOT / "data" / "pricing.json").read_text())


@dataclass
class Workload:
    count: int
    minutes: float
    vcpu: float
    memory_gib: float
    disk_gb: float = 0
    cpu_utilisation: float = 1.0
    concurrency: int | None = None

    @classmethod
    def from_scenario(cls, s: dict) -> "Workload":
        return cls(
            count=s["count"],
            minutes=s["minutes"],
            vcpu=s["vcpu"],
            memory_gib=s["memory_gib"],
            disk_gb=s.get("disk_gb", 0),
            cpu_utilisation=s.get("cpu_utilisation", 1.0),
            concurrency=s.get("concurrency"),
        )


def billed_size(p: dict, w: Workload) -> tuple[float, float] | None:
    """The (vCPU, GiB) actually billed for a requested size, or None if no size fits."""
    c = p["compute"]
    if c.get("fixed_sizes"):
        fits = [s for s in c["fixed_sizes"] if s["vcpu"] >= w.vcpu and s["memory_gib"] >= w.memory_gib]
        if not fits:
            return None
        best = min(fits, key=lambda s: s["vcpu"] * c["cpu_per_vcpu_hour"] + s["memory_gib"] * c["memory_per_gib_hour"])
        return best["vcpu"], best["memory_gib"]
    # Some providers force a minimum memory:vCPU ratio, so you pay for more RAM than you need.
    return w.vcpu, max(w.memory_gib, w.vcpu * (c.get("min_memory_gib_per_vcpu") or 0))


def hourly_cost(p: dict, w: Workload) -> float | None:
    """Compute cost of one sandbox for one hour of wall-clock runtime."""
    c = p["compute"]
    if c["cpu_per_vcpu_hour"] is None or c["memory_per_gib_hour"] is None:
        return None
    size = billed_size(p, w)
    if size is None:
        return None
    billed_vcpu, billed_mem = size
    if c["model"] in ("active_cpu", "usage"):
        billed_vcpu = billed_vcpu * w.cpu_utilisation
    billed_disk = max(0.0, w.disk_gb - (c.get("disk_free_gb") or 0))
    return (
        billed_vcpu * c["cpu_per_vcpu_hour"]
        + billed_mem * c["memory_per_gib_hour"]
        + billed_disk * (c.get("disk_per_gb_hour") or 0)
    )


def workload_cost(p: dict, w: Workload) -> float | None:
    per_hour = hourly_cost(p, w)
    if per_hour is None:
        return None
    min_seconds = p["billing"].get("minimum_billed_seconds") or 0
    hours = max(w.minutes / 60, min_seconds / 3600)
    return w.count * (hours * per_hour + (p["compute"].get("per_sandbox_fee") or 0))


def _limit(value) -> float | None:
    """Plan limits: a number, None (not published) or "unlimited" (documented as no limit)."""
    return None if value in (None, "unlimited") else value


def pick_tier(p: dict, w: Workload) -> str:
    """Cheapest published plan whose concurrency and session limits fit the workload."""
    concurrency = w.concurrency or w.count
    session_hours = w.minutes / 60
    tiers = sorted(p["plans"]["tiers"], key=lambda t: t["monthly_fee"])

    def fits_concurrency(t: dict) -> bool:
        max_sbx, max_vcpu = _limit(t["max_concurrent_sandboxes"]), _limit(t["max_concurrent_vcpu"])
        if max_sbx is not None and concurrency > max_sbx:
            return False
        if max_vcpu is not None and concurrency * w.vcpu > max_vcpu:
            return False
        return True

    def label(t: dict) -> str:
        fee = "no plan fee" if t["monthly_fee"] == 0 else f"${t['monthly_fee']:,}/mo"
        return f"{t['name']} ({fee})"

    candidates = [t for t in tiers if fits_concurrency(t)]
    if not candidates:
        return p["plans"].get("custom_tier") or "Contact sales"
    fully = [t for t in candidates if _limit(t["max_session_hours"]) is None or session_hours <= t["max_session_hours"]]
    if fully:
        t = fully[0]
        note = "" if p["platform"].get("limits_published", True) else " ⚠ limits not published"
        return label(t) + note
    # Nothing fits the session length: take the longest-session plan (cheapest on ties).
    t = min(candidates, key=lambda t: (-(_limit(t["max_session_hours"]) or 0), t["monthly_fee"]))
    return f"{label(t)} ⚠ max session {t['max_session_hours']:g} h; restart or {p['plans'].get('custom_tier', 'contact sales')}"
