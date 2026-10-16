# Sprites (Fly.io) Pricing

Sprites are persistent Fly.io microVMs (fixed 8 vCPU / 100 GB) that pause automatically when idle. CPU and memory are billed on actual consumption, not allocation, so costs depend heavily on how busy the sandbox is.

<!-- BEGIN GENERATED: provider:sprites -->
Last verified: **2026-10-16** · Official pricing: <https://fly.io/sprites>

## At a glance

|  |  |
| --- | --- |
| Billing model | usage |
| Billing unit | usage-metered (page says hourly; docs say per-second) |
| CPU | $0.0385 per vCPU-hour |
| Memory | $0.02187 per GiB-hour |
| 2 vCPU + 4 GiB sandbox, 1 hour (CPU 25% busy) | $0.1067 |
| Storage | Persistent: hot ~$0.50/GB-mo while awake, cold ~$0.02/GB-mo |
| Egress | Not metered today |
| GPU | Not offered |
| Idle billing | Only billed while running; pauses after ~30 s idle (warm/cold not billed) |
| Max session | No limit (persistent) |
| Free tier / credits | $30 trial credit |
| Paid entry | Pay-as-you-go; prepaid tiers (e.g. Hero $100/mo) |
| Isolation | microVM |
| BYOC / self-host | No |

## Published rates (verbatim)

- "CPU Time: Cumulative CPU usage measured by cpu.stat $0.0385 /CPU-hour"
- "Memory Time: Actual memory usage $0.021875 /GB-hour"
- "Storage HOT $0.000683 /GB-hour, COLD $0.000027 /GB-hour"
- "All resources are billed hourly, based on actual usage"

## Plans and limits

| Plan | Monthly fee | Max concurrent sandboxes | Max concurrent vCPU | Max session |
| --- | --- | --- | --- | --- |
| Pay-as-you-go | $0 | not published | not published | not published |
| Higher tiers (Champion and above) | custom | custom | custom | custom |

## Cost in the standard scenarios

| Scenario | Compute total | Cheapest plan that fits |
| --- | --- | --- |
| [1,000 × 5 min](../scenarios/short-lived-agents.md) | $5.53 | Pay-as-you-go (no plan fee) ⚠ limits not published |
| [100 × 1 h](../scenarios/100-sandboxes.md) | $11.36 | Pay-as-you-go (no plan fee) ⚠ limits not published |
| [1,000 × 2 h](../scenarios/large-batch.md) | $265.66 | Pay-as-you-go (no plan fee) ⚠ limits not published |
| [10 × 24/7 (month)](../scenarios/long-running-agents.md) | $794.68 | Pay-as-you-go (no plan fee) ⚠ limits not published |

## Caveats and open questions

- Fixed 8 vCPU / 100 GB per Sprite; memory is platform-managed. CPU and memory are billed on actual use, not allocation; this comparison assumes the stated memory is fully used.
- The pricing page says 'billed hourly'; the docs comparison table says 'Per-second'.
- Pay-as-you-go concurrency limits not published (Hero tier, $100/mo: 100 running).

## Sources

- <https://fly.io/sprites>
- <https://docs.fly.io/sprites>
- <https://docs.fly.io/sprites/concepts/lifecycle>
<!-- END GENERATED: provider:sprites -->

[← Back to the comparison](../README.md)
