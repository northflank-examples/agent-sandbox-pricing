# Cost of Short-Lived Agent Sandboxes (1,000 × 5 minutes)

Typical of **tool-call code execution**: an agent runs a snippet, reads the output, and the sandbox is thrown away. Runtime is short, so per-second billing, minimum charges and per-creation fees matter more than they do for long jobs.

## Assumptions

| | |
| --- | --- |
| Sandboxes | 1,000 |
| Runtime per sandbox | 5 minutes |
| Size | 1 vCPU, 2 GiB RAM, 5 GB disk |
| CPU busy | 50% of runtime |
| Running at once | 50 |

## Estimated cost by provider

Compute plus disk while running, at list price. Excludes free credits, plan fees (see last column), egress and persistent storage.

<!-- BEGIN GENERATED: scenario:short-lived-agents -->
| Provider | Billed size | Per sandbox-hour | Compute total | Cheapest plan that fits |
| --- | --- | --- | --- | --- |
| [Northflank](../providers/northflank.md) | **1 vCPU / 4 GiB** | $0.0500 | $4.17 | Pay-as-you-go (no plan fee) |
| [Cloudflare Sandbox](../providers/cloudflare.md) | **1 vCPU / 3 GiB** | $0.0643 | $5.35 | Workers Paid ($5/mo) |
| [Sprites (Fly.io)](../providers/sprites.md) | 1 vCPU / 2 GiB (used) | $0.0664 | $5.53 | Pay-as-you-go (no plan fee) ⚠ limits not published |
| [E2B](../providers/e2b.md) | 1 vCPU / 2 GiB | $0.0828 | $6.90 | Pro ($150/mo) |
| [Daytona](../providers/daytona.md) | 1 vCPU / 2 GiB | $0.0828 | $6.90 | Tier 2 ($25 top-up) (no plan fee) |
| [Vercel Sandbox](../providers/vercel.md) | 1 vCPU / 2 GiB | $0.1064 | $8.87 | Pro ($20/mo) |
| [Modal](../providers/modal.md) | 1 vCPU / 2 GiB | $0.1190 | $9.92 | Starter (no plan fee) |
| [Runloop](../providers/runloop.md) | 1 vCPU / 2 GiB | $0.1601 | $13.34 | Basic (no plan fee) ⚠ limits not published |
<!-- END GENERATED: scenario:short-lived-agents -->

⚠ = a plan limit isn't published, or the workload exceeds the plan's session limit.

## Notes

- One run costs about $4–$13 depending on provider. Run daily, that's roughly $125–$400 a month, so E2B's $100 or Daytona's $200 free credit covers the first few weeks.
- Vercel bills memory in 1-minute increments and charges a creation fee. Neither matters at 5 minutes, but both would for sub-minute sandboxes.
- Northflank cloud has no 1 vCPU / 2 GB plan, so it is billed as its 1 vCPU / 4 GB plan ($0.05/hr). Cloudflare bills 1 vCPU with at least 3 GiB.
- If your sandboxes live for seconds, cold-start time and snapshot/restore support usually matter more than the rate.

Reproduce or change the assumptions in the [web estimator](https://p01--sandbox-pricing-estimator--wdgpv6bn4jz8.code.run?count=1000&duration=5&vcpu=1&memory_gib=2&disk_gb=5&cpu_utilisation=50&concurrency=50), or locally:

```bash
python3 scripts/estimate.py --sandboxes 1000 --minutes 5 --vcpu 1 --memory 2 --disk 5 --cpu-busy 0.5 --concurrency 50
```

[← All scenarios](README.md) · [Methodology](../methodology.md)
