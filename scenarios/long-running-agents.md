# Cost of Long-Running / Always-On Agent Sandboxes

**Persistent agent environments**, e.g. a background coding agent per developer, kept running 24/7 for a month (730 hours) with low CPU utilisation.

## Assumptions

| | |
| --- | --- |
| Sandboxes | 10 |
| Runtime per sandbox | 43,800 minutes |
| Size | 2 vCPU, 4 GiB RAM, 20 GB disk |
| CPU busy | 10% of runtime |
| Running at once | 10 |

## Estimated cost by provider

Compute plus disk while running, at list price. Excludes free credits, plan fees (see last column), egress and persistent storage.

<!-- BEGIN GENERATED: scenario:long-running-agents -->
| Provider | Billed size | Per sandbox-hour | Compute total | Cheapest plan that fits |
| --- | --- | --- | --- | --- |
| [Northflank](../providers/northflank.md) | 2 vCPU / 4 GiB | $0.0667 | $486.62 | Pay-as-you-go (no plan fee) |
| [Cloudflare Sandbox](../providers/cloudflare.md) | **2 vCPU / 6 GiB** | $0.0734 | $536.11 | Workers Paid ($5/mo) |
| [Sprites (Fly.io)](../providers/sprites.md) | 2 vCPU / 4 GiB (used) | $0.1089 | $794.68 | Pay-as-you-go (no plan fee) ⚠ limits not published |
| [Vercel Sandbox](../providers/vercel.md) | 2 vCPU / 4 GiB | $0.1104 | $805.92 | Pro ($20/mo) ⚠ max session 24 h; restart or Enterprise (custom) |
| [E2B](../providers/e2b.md) | 2 vCPU / 4 GiB | $0.1656 | $1,208.88 | Pro ($150/mo) ⚠ max session 24 h; restart or Enterprise ($3,000/mo minimum; multi-day sessions, BYOC) |
| [Daytona](../providers/daytona.md) | 2 vCPU / 4 GiB | $0.1672 | $1,220.71 | Tier 2 ($25 top-up) (no plan fee) ⚠ above the default max per sandbox (4 vCPU / 8 GiB / 10 GB disk); ask to raise it |
| [Modal](../providers/modal.md) | 2 vCPU / 4 GiB | $0.2380 | $1,737.11 | Starter (no plan fee) ⚠ max session 24 h; restart or Enterprise (custom) |
| [Runloop](../providers/runloop.md) (shutting down) | 2 vCPU / 4 GiB | $0.3236 | $2,362.62 | Basic (no plan fee) ⚠ limits not published |
<!-- END GENERATED: scenario:long-running-agents -->

⚠ = a plan limit isn't published, or the workload exceeds the plan's session limit.

## Notes

- This is where **idle billing** dominates. If the environments could be paused when unused (Sprites auto-pauses, E2B can pause on timeout, Daytona auto-stops), real costs could be far lower than shown here on any provider.
- Modal sandboxes have a hard 24 h lifetime. E2B Pro and Vercel limit continuous sessions to 24 h, but pause/resume resets the clock. Either way, always-on use needs pause/resume or snapshot/restore logic, or an enterprise plan.
- Disk is already in the totals for Daytona, Runloop, Cloudflare and Sprites. Elsewhere, a 20 GB persistent volume adds up to about $3/mo per sandbox. See [hidden costs](../comparisons/hidden-costs.md#5-storage-and-snapshots).

Reproduce or change the assumptions in the [web estimator](https://p01--sandbox-pricing-estimator--wdgpv6bn4jz8.code.run?count=10&duration=1&unit=43800&disk_gb=20&cpu_utilisation=10&concurrency=10), or locally:

```bash
python3 scripts/estimate.py --sandboxes 10 --minutes 43800 --vcpu 2 --memory 4 --disk 20 --cpu-busy 0.1 --concurrency 10
```

[← All scenarios](README.md) · [Methodology](../methodology.md)
