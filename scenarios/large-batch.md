# Cost of Running 1,000 Concurrent Sandboxes (Evals / RL)

An **evaluation or reinforcement-learning batch**: 1,000 sandboxes run in parallel for 2 hours, e.g. one per SWE-bench-style task.

## Assumptions

| | |
| --- | --- |
| Sandboxes | 1,000 |
| Runtime per sandbox | 120 minutes |
| Size | 2 vCPU, 4 GiB RAM, 10 GB disk |
| CPU busy | 50% of runtime |
| Running at once | 1,000 |

## Estimated cost by provider

Compute plus disk while running, at list price. Excludes free credits, plan fees (see last column), egress and persistent storage.

<!-- BEGIN GENERATED: scenario:large-batch -->
| Provider | Billed size | Per sandbox-hour | Compute total | Cheapest plan that fits |
| --- | --- | --- | --- | --- |
| [Northflank](../providers/northflank.md) | 2 vCPU / 4 GiB | $0.0667 | $133.32 | Pay-as-you-go (no plan fee) |
| [Cloudflare Sandbox](../providers/cloudflare.md) | **2 vCPU / 6 GiB** | $0.1285 | $257.04 | Enterprise (custom limits) |
| [Sprites (Fly.io)](../providers/sprites.md) | 2 vCPU / 4 GiB (used) | $0.1328 | $265.66 | Pay-as-you-go (no plan fee) ⚠ limits not published |
| [E2B](../providers/e2b.md) | 2 vCPU / 4 GiB | $0.1656 | $331.20 | Pro + 1,000 concurrency ($1,150/mo) |
| [Daytona](../providers/daytona.md) | 2 vCPU / 4 GiB | $0.1661 | $332.28 | Enterprise (custom; BYOC) |
| [Vercel Sandbox](../providers/vercel.md) | 2 vCPU / 4 GiB | $0.2128 | $425.60 | Pro ($20/mo) |
| [Modal](../providers/modal.md) | 2 vCPU / 4 GiB | $0.2380 | $475.92 | Team ($250/mo) |
| [Runloop](../providers/runloop.md) | 2 vCPU / 4 GiB | $0.3202 | $640.45 | Basic (no plan fee) ⚠ limits not published |
<!-- END GENERATED: scenario:large-batch -->

⚠ = a plan limit isn't published, or the workload exceeds the plan's session limit.

## Notes

- At this concurrency, **plan limits dominate**. E2B needs its $1,150/mo concurrency add-on. Daytona's top tier allows 500 vCPU (this needs 2,000), and so does Cloudflare's account limit (1,500 vCPU), so both require enterprise arrangements.
- Utilisation is assumed at 50% because eval workloads run tests and builds.

Reproduce or change the assumptions in the [web estimator](https://p01--sandbox-pricing-estimator--wdgpv6bn4jz8.code.run?count=1000&duration=2&unit=60&cpu_utilisation=50&concurrency=1000), or locally:

```bash
python3 scripts/estimate.py --sandboxes 1000 --minutes 120 --vcpu 2 --memory 4 --disk 10 --cpu-busy 0.5 --concurrency 1000
```

[← All scenarios](README.md) · [Methodology](../methodology.md)
