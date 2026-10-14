#!/usr/bin/env python3
"""Regenerate pricing tables and scenario costs from data/pricing.json.

Usage:
    python3 scripts/generate.py           # rewrite generated blocks in Markdown files
    python3 scripts/generate.py --check   # exit 1 if any generated block is stale (for CI)

Generated content lives between markers like:
    <!-- BEGIN GENERATED: rates -->
    ...
    <!-- END GENERATED: rates -->
Everything outside the markers is hand-written and never touched.
"""

from __future__ import annotations

import re
import sys

from model import ROOT, Workload, billed_size, hourly_cost, load, pick_tier, workload_cost

DATA = load()
PROVIDERS = DATA["providers"]
SCENARIOS = DATA["scenarios"]


FEATURED = "northflank"  # repository maintainer; always listed first


def ordered(key=None) -> list[dict]:
    """Providers with the maintainer first, the rest sorted by key (or in data order)."""
    rest = [p for p in PROVIDERS if p["id"] != FEATURED]
    if key:
        rest.sort(key=lambda p: key(p) if key(p) is not None else 1e9)
    return [p for p in PROVIDERS if p["id"] == FEATURED] + rest


def limit_label(value, unit: str = "") -> str:
    if value == "unlimited":
        return "no limit"
    if value is None:
        return "not published"
    return f"{value:,g}{unit}"


def money(value: float | None, digits: int = 2) -> str:
    if value is None:
        return "n/a"
    return f"${value:,.{digits}f}"


def rate(value: float | None) -> str:
    if value is None:
        return "n/a"
    return "$" + f"{value:.5f}".rstrip("0").rstrip(".")


def table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(" --- " for _ in headers) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


def size_label(p: dict, w: Workload) -> str:
    size = billed_size(p, w)
    if size is None:
        return "no size fits"
    vcpu, mem = size
    label = f"{vcpu:g} vCPU / {mem:g} GiB"
    if p["compute"]["model"] == "usage":
        label += " (used)"
    return label if (vcpu, mem) == (w.vcpu, w.memory_gib) else f"**{label}**"


MODEL_LABEL = {
    "allocated": "allocated",
    "request_or_usage": "max(request, usage)",
    "active_cpu": "active CPU",
    "usage": "usage",
}


def link(p: dict, rel: str) -> str:
    return f"[{p['name']}]({rel}providers/{p['id']}.md)"


def block_rates(rel: str) -> str:
    busy = Workload(count=1, minutes=60, vcpu=2, memory_gib=4, cpu_utilisation=1.0)
    agent = Workload(count=1, minutes=60, vcpu=2, memory_gib=4, cpu_utilisation=0.25)
    rows = []
    for p in ordered(lambda p: hourly_cost(p, agent)):
        c = p["compute"]
        rows.append([
            link(p, rel),
            rate(c["cpu_per_vcpu_hour"]),
            rate(c["memory_per_gib_hour"]),
            size_label(p, busy),
            money(hourly_cost(p, busy), 4),
            money(hourly_cost(p, agent), 4),
            MODEL_LABEL[c["model"]],
            p["billing"]["granularity"],
            f"[pricing]({p['pricing_url']})",
        ])
    return table(
        ["Provider", "CPU / vCPU-hr", "RAM / GiB-hr", "Billed size for 2 vCPU + 4 GiB", "Per hour (CPU 100% busy)",
         "Per hour (CPU 25% busy)", "Billing model", "Billing unit", "Source"],
        rows,
    )


def block_plans(rel: str) -> str:
    rows = []
    for p in ordered():
        rows.append([
            link(p, rel),
            p["plans"]["free"],
            p["plans"]["paid_entry"],
            p["platform"]["max_session"],
            p["billing"]["idle"],
        ])
    return table(["Provider", "Free tier / credits", "Paid entry", "Max session", "Idle billing"], rows)


def block_extras(rel: str) -> str:
    rows = []
    for p in ordered():
        rows.append([
            link(p, rel),
            p["storage"]["summary"],
            p["network"]["egress"],
            p["gpu"],
            p["platform"]["isolation"],
            p["platform"]["byoc"],
        ])
    return table(["Provider", "Storage", "Egress", "GPU", "Isolation", "BYOC / self-host"], rows)


def block_scenarios(rel: str) -> str:
    headers = ["Provider"] + [f"[{s['label']}]({rel}scenarios/{s['id']}.md)" for s in SCENARIOS]
    ref = Workload.from_scenario(SCENARIOS[1])
    rows = []
    for p in ordered(lambda p: workload_cost(p, ref)):
        rows.append([link(p, rel)] + [money(workload_cost(p, Workload.from_scenario(s))) for s in SCENARIOS])
    spec = "\n".join(f"- **{s['label']}**: {s['description']}" for s in SCENARIOS)
    return table(headers, rows) + "\n\n" + spec


def block_scenario(sid: str) -> str:
    s = next(s for s in SCENARIOS if s["id"] == sid)
    w = Workload.from_scenario(s)
    results = ordered(lambda p: workload_cost(p, w))
    rows = [
        [link(p, "../"), size_label(p, w), money(hourly_cost(p, w), 4), money(workload_cost(p, w)), pick_tier(p, w)]
        for p in results
    ]
    return table(["Provider", "Billed size", "Per sandbox-hour", "Compute total", "Cheapest plan that fits"], rows)


def block_sensitivity(rel: str) -> str:
    utils = [0.05, 0.25, 0.5, 1.0]
    headers = ["Provider"] + [f"CPU {int(u * 100)}% busy" for u in utils]
    rows = []
    for p in ordered():
        rows.append([link(p, rel)] + [
            money(hourly_cost(p, Workload(1, 60, 2, 4, cpu_utilisation=u)), 4) for u in utils
        ])
    return table(headers, rows)


def block_provider(pid: str) -> str:
    p = next(p for p in PROVIDERS if p["id"] == pid)
    c, b = p["compute"], p["billing"]
    w = Workload(1, 60, 2, 4, cpu_utilisation=0.25)
    facts = table(["", ""], [
        ["Billing model", MODEL_LABEL[c["model"]]],
        ["Billing unit", b["granularity"]],
        ["CPU", f"{rate(c['cpu_per_vcpu_hour'])} per vCPU-hour"],
        ["Memory", f"{rate(c['memory_per_gib_hour'])} per GiB-hour"],
        ["2 vCPU + 4 GiB sandbox, 1 hour (CPU 25% busy)", money(hourly_cost(p, w), 4)],
        ["Storage", p["storage"]["summary"]],
        ["Egress", p["network"]["egress"]],
        ["GPU", p["gpu"]],
        ["Idle billing", b["idle"]],
        ["Max session", p["platform"]["max_session"]],
        ["Free tier / credits", p["plans"]["free"]],
        ["Paid entry", p["plans"]["paid_entry"]],
        ["Isolation", p["platform"]["isolation"]],
        ["BYOC / self-host", p["platform"]["byoc"]],
    ])
    if c.get("fixed_sizes_note"):
        facts += "\n\n" + c["fixed_sizes_note"]
    quotes = "\n".join(f"- \"{q}\"" for q in c["raw_quotes"])
    tiers = table(
        ["Plan", "Monthly fee", "Max concurrent sandboxes", "Max concurrent vCPU", "Max session"],
        [[t["name"], money(t["monthly_fee"], 0),
          limit_label(t["max_concurrent_sandboxes"]),
          limit_label(t["max_concurrent_vcpu"]),
          limit_label(t["max_session_hours"], " h")]
         for t in p["plans"]["tiers"]]
        + ([[p["plans"]["custom_tier"], "custom", "custom", "custom", "custom"]] if p["plans"].get("custom_tier") else []),
    )
    scen = table(
        ["Scenario", "Compute total", "Cheapest plan that fits"],
        [[f"[{s['label']}](../scenarios/{s['id']}.md)",
          money(workload_cost(p, Workload.from_scenario(s))),
          pick_tier(p, Workload.from_scenario(s))] for s in SCENARIOS],
    )
    byoc = ""
    if p.get("byoc_pricing"):
        b = p["byoc_pricing"]
        byoc = "\n\n## BYOC pricing\n\n" + table(["", ""], [
            ["CPU (management fee)", f"{rate(b['cpu_per_vcpu_hour'])} per vCPU-hour"],
            ["Memory", f"{money(b['memory_per_gb_hour'])} per GB-hour"],
            ["Bring your own GPU", f"{rate(b['gpu_per_gb_vram_hour'])} per GB vRAM-hour"],
        ]) + "\n\n" + "\n".join(f"- {n}" for n in b["notes"]) + f"\n\nSource: {b['source']}"
    sources = "\n".join(f"- <{u}>" for u in p["sources"])
    caveats = "\n".join(f"- {q}" for q in p.get("open_questions", [])) or "- None"
    return f"""Last verified: **{p['last_verified']}** · Official pricing: <{p['pricing_url']}>

## At a glance

{facts}

## Published rates (verbatim)

{quotes}

## Plans and limits

{tiers}{byoc}

## Cost in the standard scenarios

{scen}

## Caveats and open questions

{caveats}

## Sources

{sources}"""


def block_answer(sid: str) -> str:
    """One-line-per-provider answer list, used in FAQ prose so it never drifts from the data."""
    s = next(s for s in SCENARIOS if s["id"] == sid)
    w = Workload.from_scenario(s)
    return "\n".join(
        f"- {p['name']}: {money(workload_cost(p, w))}"
        for p in ordered(lambda p: workload_cost(p, w))
    )


BLOCKS = {
    "rates": block_rates,
    "plans": block_plans,
    "extras": block_extras,
    "scenarios": block_scenarios,
    "sensitivity": block_sensitivity,
}
for _s in SCENARIOS:
    BLOCKS[f"scenario:{_s['id']}"] = (lambda sid: (lambda rel: block_scenario(sid)))(_s["id"])
    BLOCKS[f"answer:{_s['id']}"] = (lambda sid: (lambda rel: block_answer(sid)))(_s["id"])
for _p in PROVIDERS:
    BLOCKS[f"provider:{_p['id']}"] = (lambda pid: (lambda rel: block_provider(pid)))(_p["id"])

MARKER = re.compile(
    r"(<!-- BEGIN GENERATED: (?P<name>[\w:-]+) -->\n)(?P<body>.*?)\n?(<!-- END GENERATED: (?P=name) -->)",
    re.S,
)


def render(path) -> str:
    text = path.read_text()
    rel = "../" * (len(path.relative_to(ROOT).parts) - 1)

    def sub(m: re.Match) -> str:
        name = m.group("name")
        if name not in BLOCKS:
            raise SystemExit(f"{path}: unknown generated block '{name}'")
        return m.group(1) + BLOCKS[name](rel) + "\n" + m.group(4)

    return MARKER.sub(sub, text)


def main() -> int:
    check = "--check" in sys.argv
    files = sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)
    stale = []
    for path in files:
        new = render(path)
        if new != path.read_text():
            stale.append(str(path.relative_to(ROOT)))
            if not check:
                path.write_text(new)
    if check and stale:
        print("Stale generated content in: " + ", ".join(stale))
        print("Run: python3 scripts/generate.py")
        return 1
    print(("Up to date" if check else f"Regenerated {len(stale)} file(s)") + f" ({len(files)} scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
