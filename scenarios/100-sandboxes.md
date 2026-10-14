# How Much Does It Cost to Run 100 AI Agent Sandboxes?

A typical **coding-agent** workload: 100 agents each get their own sandbox for an hour, editing files and running commands between LLM calls.

## Assumptions

| | |
| --- | --- |
| Sandboxes | 100 |
| Runtime per sandbox | 60 minutes |
| Size | 2 vCPU, 4 GiB RAM, 10 GB disk |
| CPU busy | 25% of runtime |
| Running at once | 100 |

## Estimated cost by provider

Compute only, at list price. Excludes free credits, plan fees (see last column), egress and persistent storage.

<!-- BEGIN GENERATED: scenario:100-sandboxes -->
| Provider | Billed size | Per sandbox-hour | Compute total | Cheapest plan that fits |
| --- | --- | --- | --- | --- |
| [Northflank](../providers/northflank.md) | 2 vCPU / 4 GiB | $0.0667 | $6.67 | Pay-as-you-go (no plan fee) |
| [Cloudflare Sandbox](../providers/cloudflare.md) | **2 vCPU / 6 GiB** | $0.0925 | $9.25 | Workers Paid ($5/mo) |
| [Sprites (Fly.io)](../providers/sprites.md) | 2 vCPU / 4 GiB (used) | $0.1136 | $11.36 | Pay-as-you-go (no plan fee) ⚠ limits not published |
| [Vercel Sandbox](../providers/vercel.md) | 2 vCPU / 4 GiB | $0.1488 | $14.88 | Pro ($20/mo) |
| [E2B](../providers/e2b.md) | 2 vCPU / 4 GiB | $0.1656 | $16.56 | Pro ($150/mo) |
| [Daytona](../providers/daytona.md) | 2 vCPU / 4 GiB | $0.1661 | $16.61 | Tier 3 ($500 top-up) (no plan fee) |
| [Modal](../providers/modal.md) | 2 vCPU / 4 GiB | $0.2380 | $23.80 | Starter (no plan fee) |
| [Runloop](../providers/runloop.md) | 2 vCPU / 4 GiB | $0.3202 | $32.02 | Basic (no plan fee) ⚠ limits not published |
<!-- END GENERATED: scenario:100-sandboxes -->

⚠ = a plan limit isn't published, or the workload exceeds the plan's session limit.

## Notes

- 100 concurrent sandboxes exceeds the free tiers on E2B (20), Vercel (10) and Daytona Tier 1 (10 vCPU). Modal Starter's limit is exactly 100 containers.
- Utilisation is assumed at 25%. If your agents mostly wait on LLM calls (5–10% busy), Vercel and Cloudflare get noticeably cheaper. See the [sensitivity table](../comparisons/pricing-comparison.md#how-cpu-utilisation-changes-the-price).

Reproduce or change the assumptions:

```bash
python3 scripts/estimate.py --sandboxes 100 --minutes 60 --vcpu 2 --memory 4 --disk 10 --cpu-busy 0.25 --concurrency 100
```

[← All scenarios](README.md) · [Methodology](../methodology.md)
