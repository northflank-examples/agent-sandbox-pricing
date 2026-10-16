# Daytona Sandbox Pricing

Daytona provides container (default) and VM sandboxes for AI agents. Compute is billed per second on reserved vCPU, memory and disk, with no plan fee; usage limits rise with account top-ups.

<!-- BEGIN GENERATED: provider:daytona -->
Last verified: **2026-10-16** · Official pricing: <https://www.daytona.io/pricing>

## At a glance

|  |  |
| --- | --- |
| Billing model | allocated |
| Billing unit | per second |
| CPU | $0.0504 per vCPU-hour |
| Memory | $0.0162 per GiB-hour |
| 2 vCPU + 4 GiB sandbox, 1 hour (CPU 25% busy) | $0.1656 |
| Storage | First 5 GiB free, then $0.000108/GiB-hr (~$0.08/GiB-mo) |
| Egress | Not published (restricted on Tier 1-2) |
| GPU | Preemptible: H100 $2.27/hr, H200 $2.61/hr, B200 $3.59/hr; on-demand: H100 $3.95/hr |
| Idle billing | Auto-stops after 15 min idle (default); stopped = disk only |
| Max session | No limit (auto-stop default 15 min; 0 = never) |
| Free tier / credits | $200 free compute credit |
| Paid entry | No plan fee; limits rise with top-ups |
| Isolation | Containers by default; optional VM sandboxes with their own kernel |
| BYOC / self-host | Enterprise (bring your own compute) |

## Published rates (verbatim)

- "Compute vCPU $0.0504/h"
- "Memory GiB $0.0162/h"
- "Storage GiB $0.000108/h * Price per GiB after first 5 free"
- "All billing is calculated per second"

## Plans and limits

| Plan | Monthly fee | Max concurrent sandboxes | Max concurrent vCPU | Max session |
| --- | --- | --- | --- | --- |
| Tier 1 | $0 | not published | 10 | not published |
| Tier 2 ($25 top-up) | $0 | not published | 100 | not published |
| Tier 3 ($500 top-up) | $0 | not published | 250 | not published |
| Tier 4 ($2,000 top-up every 30 days) | $0 | not published | 500 | not published |
| Enterprise (custom; BYOC) | custom | custom | custom | custom |

## Cost in the standard scenarios

| Scenario | Compute total | Cheapest plan that fits |
| --- | --- | --- |
| [1,000 × 5 min](../scenarios/short-lived-agents.md) | $6.90 | Tier 2 ($25 top-up) (no plan fee) |
| [100 × 1 h](../scenarios/100-sandboxes.md) | $16.61 | Tier 3 ($500 top-up) (no plan fee) |
| [1,000 × 2 h](../scenarios/large-batch.md) | $332.28 | Enterprise (custom; BYOC) |
| [10 × 24/7 (month)](../scenarios/long-running-agents.md) | $1,220.71 | Tier 2 ($25 top-up) (no plan fee) ⚠ above the default max per sandbox (4 vCPU / 8 GiB / 10 GB disk); ask to raise it |

## Caveats and open questions

- Egress pricing not published.
- Tier 1 memory pool is listed as both 10 GiB and 20 GiB on the limits page.
- Tier limits are a shared pool across all running sandboxes.

## Sources

- <https://www.daytona.io/pricing>
- <https://www.daytona.io/docs/en/billing>
- <https://www.daytona.io/docs/en/limits>
- <https://www.daytona.io/docs/en/sandboxes>
- <https://www.daytona.io/docs/en/isolation>
<!-- END GENERATED: provider:daytona -->

[← Back to the comparison](../README.md)
