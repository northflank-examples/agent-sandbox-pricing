# Methodology

How the prices in this repository are collected, normalised and calculated, so you can check or reproduce any number.

## Sources

- Only **official vendor sources** are used: pricing pages, billing docs and limits docs. Each provider page lists the exact URLs. Blog posts, third-party comparisons and sales quotes are not used.
- Each provider has a `last_verified` date in [`data/pricing.json`](data/pricing.json). Prices are re-checked at least quarterly and whenever a vendor announces a change.
- Rates are **list prices** for the **default / US region**, in USD, on the standard self-serve plan. Enterprise discounts, committed-use pricing and regional multipliers are excluded.
- Each provider page quotes the published rates **verbatim**, so the normalisation can be checked.

## Missing and uncertain data

- `null` / **not published** means the vendor doesn't publish the value, or it couldn't be verified. It never means free.
- Where official sources contradict each other (e.g. a pricing page and a docs page), the conflict is listed under the provider's **Caveats and open questions** and the more specific, more recent source is used.

## Normalisation

| Issue | How it's handled |
| --- | --- |
| Time units (per second, per 10 ms, per hour) | Converted to per hour: per-second rate × 3,600 |
| CPU units | Per **vCPU** (one hyperthread). Modal quotes per physical core = 2 vCPU, so its rate is halved. |
| GB vs GiB memory | Treated as equal. For Northflank this is confirmed, because its plan prices only reproduce if 4096 MB = 4 GB. For other vendors that say "GB" it's unconfirmed; the difference is ~7%. |
| Fixed sizes (Northflank cloud plans) | The cheapest plan with at least the requested vCPU and memory is billed. |
| Bundled sizes (Runloop presets) | Unit rates are used; they reproduce the preset prices exactly. |
| Request vs usage (Modal) | Priced at the request, i.e. as if you reserve what you need. |
| Minimum memory ratios (Cloudflare ≥ 3 GiB/vCPU, Vercel 2 GB/vCPU) | Memory is billed at the higher of what you request and what the provider requires. |
| Minimum billing increments (Vercel memory: 1 min) | Runtime is rounded up to the minimum. |
| Per-sandbox fees (Vercel creations) | Added per sandbox. |
| Included disk (Daytona first 5 GiB) | Subtracted before disk is charged. |

## Cost formula

For each provider and workload:

```
billed_vcpu   = vcpu                          (allocated model)
              = vcpu × cpu_utilisation        (active_cpu and usage models)
(billed size = cheapest fixed size that fits, where the provider only sells fixed sizes)
billed_memory = max(memory_gib, vcpu × min_memory_per_vcpu)
billed_disk   = max(0, disk_gb − free_disk_gb)

hourly  = billed_vcpu × cpu_rate + billed_memory × memory_rate + billed_disk × disk_rate
total   = sandboxes × (max(hours, minimum_billing) × hourly + per_sandbox_fee)
```

The implementation is [`scripts/model.py`](scripts/model.py), about 100 lines with no dependencies.

## Validation against vendor figures

[`scripts/validate.py`](scripts/validate.py) checks the model against prices and worked examples that the vendors publish themselves, and runs in CI:

| Vendor figure | Cases | Result |
| --- | --- | --- |
| Northflank plan prices (nf-compute-10 to nf-compute-32-488) | 18 | Match within $0.002/hr (vendor rounds to 4 dp) |
| E2B pricing calculator (1,000 sandbox-hours at default size → $166) | 1 | $165.60 |
| Runloop size table (X_SMALL to XX_LARGE) | 6 | Exact |
| Vercel "Example calculations" (10% CPU) | 4 | Exact |
| Sprites pricing examples (CPU + RAM + hot storage) | 2 | Within line-item rounding |

Where a vendor's own figures disagree with its listed rates, the rates are used and the discrepancy is noted on the provider page. For example, Runloop's FAQ estimate of $2.73/day doesn't match its unit rates, which give $2.53/day.

### Plan selection

For each scenario, the "cheapest plan that fits" is the lowest-fee published plan whose **concurrent sandbox** and **concurrent vCPU** limits cover the workload. If the session length exceeds every published plan's limit, the plan with the longest session is shown with a ⚠. If no published plan fits, the enterprise / custom tier is shown.

## What's excluded from scenario totals

- Free credits and included allowances (e.g. Cloudflare's 375 vCPU-minutes/month)
- Plan fees, which are shown separately
- Persistent storage that outlives the sandbox, snapshots and egress (disk billed while the sandbox runs *is* included), which are listed in [hidden costs](comparisons/hidden-costs.md)
- Charges outside the sandbox (Cloudflare Workers / Durable Objects, build minutes)
- Taxes

## Known limitations

- **Utilisation is an assumption.** Active-CPU and usage-billed providers are very sensitive to it. Each scenario states its assumption, and the [sensitivity table](comparisons/pricing-comparison.md#how-cpu-utilisation-changes-the-price) shows the range.
- **Modal** bills max(request, usage). Requesting less than your peak and bursting can cost less than shown here.
- **Sprites memory** is billed on actual use. This comparison assumes the full stated memory is used, which overstates Sprites' cost for light workloads.
- **No performance normalisation.** A vCPU is not identical across providers (CPU generation, oversubscription, microVM overhead). This is a price comparison, not a benchmark.
- **Point-in-time.** Vendors change prices frequently, so always confirm on the official page before making a decision.

## Conflict of interest

This repository is maintained by Northflank, which is one of the providers compared. To keep that from biasing the comparison:

- Northflank is held to the same sourcing rules as every other provider.
- All calculations are open source and reproducible.
- Cases where competitors are cheaper are reported as prominently as cases where Northflank is.
- Any vendor can submit corrections (see [CONTRIBUTING.md](CONTRIBUTING.md)).
