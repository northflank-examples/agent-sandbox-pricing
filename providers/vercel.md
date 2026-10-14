# Vercel Sandbox Pricing

Vercel Sandbox runs Firecracker microVMs on Vercel's infrastructure. CPU is billed only while active (I/O wait is free); provisioned memory is billed for the whole runtime. Each vCPU comes with 2 GB of memory.

<!-- BEGIN GENERATED: provider:vercel -->
Last verified: **2026-10-14** · Official pricing: <https://vercel.com/docs/vercel-sandbox/pricing>

## At a glance

|  |  |
| --- | --- |
| Billing model | active CPU |
| Billing unit | CPU: active time; memory: 1-min increments |
| CPU | $0.128 per vCPU-hour |
| Memory | $0.0212 per GiB-hour |
| 2 vCPU + 4 GiB sandbox, 1 hour (CPU 25% busy) | $0.1488 |
| Storage | 64 GB ephemeral NVMe included; snapshots $0.08/GB-mo |
| Egress | Included in CDN (Pro); $0.15/GB (Enterprise) |
| GPU | Not offered |
| Idle billing | Memory billed while running; CPU only when busy; stopped = snapshot storage |
| Max session | 45 min (Hobby), 24 h (Pro); resets on stop/resume |
| Free tier / credits | Hobby: 5 h active CPU, 420 GB-hr memory/mo; 45 min sessions; 10 concurrent |
| Paid entry | Pro $20/mo (credited against usage) |
| Isolation | Firecracker microVM |
| BYOC / self-host | No |

## Published rates (verbatim)

- "Sandbox Active CPU $0.128/hour"
- "Sandbox Provisioned Memory $0.0212/GB-hour"
- "Sandbox Creations $0.60/1M"
- "Provisioned memory is billed in 1 minute minimum increments"

## Plans and limits

| Plan | Monthly fee | Max concurrent sandboxes | Max concurrent vCPU | Max session |
| --- | --- | --- | --- | --- |
| Hobby | $0 | 10 | not published | 0.75 h |
| Pro | $20 | 10,000 | not published | 24 h |
| Enterprise (custom) | custom | custom | custom | custom |

## Cost in the standard scenarios

| Scenario | Compute total | Cheapest plan that fits |
| --- | --- | --- |
| [1,000 × 5 min](../scenarios/short-lived-agents.md) | $8.87 | Pro ($20/mo) |
| [100 × 1 h](../scenarios/100-sandboxes.md) | $14.88 | Pro ($20/mo) |
| [1,000 × 2 h](../scenarios/large-batch.md) | $425.60 | Pro ($20/mo) |
| [10 × 24/7 (month)](../scenarios/long-running-agents.md) | $805.92 | Pro ($20/mo) ⚠ max session 24 h; restart or Enterprise (custom) |

## Caveats and open questions

- Rates shown are iad1; other regions differ.
- Each vCPU includes 2 GB memory; sizes are 1 or an even number of vCPUs.

## Sources

- <https://vercel.com/docs/vercel-sandbox/pricing>
- <https://vercel.com/docs/vercel-sandbox/concepts>
<!-- END GENERATED: provider:vercel -->

[← Back to the comparison](../README.md)
