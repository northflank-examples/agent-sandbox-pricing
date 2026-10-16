# Cloudflare Sandbox Pricing

The Cloudflare Sandbox SDK runs on Cloudflare Containers (Firecracker microVMs). CPU is billed on active usage, memory and disk on provisioned size, in 10 ms increments. Requires the Workers Paid plan; Durable Objects and Workers charges apply on top.

<!-- BEGIN GENERATED: provider:cloudflare -->
Last verified: **2026-10-16** · Official pricing: <https://developers.cloudflare.com/containers/pricing/>

## At a glance

|  |  |
| --- | --- |
| Billing model | active CPU |
| Billing unit | per 10 ms |
| CPU | $0.072 per vCPU-hour |
| Memory | $0.009 per GiB-hour |
| 2 vCPU + 4 GiB sandbox, 1 hour (CPU 25% busy) | $0.0900 |
| Storage | Disk $0.00000007/GB-s while running; no persistent volume pricing |
| Egress | $0.025/GB NA/EU (1 TB included) |
| GPU | Not offered |
| Idle billing | Memory/disk billed while awake; CPU only when busy; sleeps after 10 min (default) |
| Max session | No published max; keepAlive keeps billing |
| Free tier / credits | Included in Workers Paid: 375 vCPU-min, 25 GiB-hr memory/mo |
| Paid entry | Workers Paid $5/mo + usage |
| Isolation | Firecracker microVM |
| BYOC / self-host | No |

## Published rates (verbatim)

- "+$0.000020 per additional vCPU-second"
- "+$0.0000025 per additional GiB-second"
- "+$0.00000007 per additional GB-second"
- "Memory and disk usage are based on the provisioned resources for the instance type you select, while CPU usage is based on active usage only"

## Plans and limits

| Plan | Monthly fee | Max concurrent sandboxes | Max concurrent vCPU | Max session |
| --- | --- | --- | --- | --- |
| Workers Paid | $5 | not published | 1,500 | not published |
| Enterprise (custom limits) | custom | custom | custom | custom |

## Cost in the standard scenarios

| Scenario | Compute total | Cheapest plan that fits |
| --- | --- | --- |
| [1,000 × 5 min](../scenarios/short-lived-agents.md) | $5.35 | Workers Paid ($5/mo) |
| [100 × 1 h](../scenarios/100-sandboxes.md) | $9.25 | Workers Paid ($5/mo) |
| [1,000 × 2 h](../scenarios/large-batch.md) | $257.04 | Enterprise (custom limits) |
| [10 × 24/7 (month)](../scenarios/long-running-agents.md) | $536.11 | Workers Paid ($5/mo) |

## Caveats and open questions

- Durable Objects and Workers request charges apply on top and are not modelled.
- Custom instance types need at least 3 GiB memory per vCPU (1-4 vCPU), so 2 vCPU is billed with at least 6 GiB.
- Account limits are defaults and can be increased.

## Sources

- <https://developers.cloudflare.com/containers/pricing/>
- <https://developers.cloudflare.com/sandbox/platform/pricing/>
- <https://developers.cloudflare.com/containers/platform-details/limits/>
<!-- END GENERATED: provider:cloudflare -->

[← Back to the comparison](../README.md)
