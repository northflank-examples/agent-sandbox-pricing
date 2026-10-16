# Runloop Devbox Pricing

Runloop provides microVM "Devboxes" aimed at AI coding agents and benchmarks. Compute, memory and disk are all metered per second on allocated resources.

<!-- BEGIN GENERATED: provider:runloop -->
> **⚠ Shutting down:** "Runloop is winding down its services. Support for existing customers continues through November 13, 2026 at 11:59 PM PT." ([source](https://docs.runloop.ai/docs/devboxes/configuration/sizes))

Last verified: **2026-10-16** · Official pricing: <https://runloop.ai/pricing>

## At a glance

|  |  |
| --- | --- |
| Billing model | allocated |
| Billing unit | per second |
| CPU | $0.108 per vCPU-hour |
| Memory | $0.0252 per GiB-hour |
| 2 vCPU + 4 GiB sandbox, 1 hour (CPU 25% busy) | $0.3168 |
| Storage | Devbox disk $0.00034236/GB-hr (~$0.25/GB-mo); snapshots ~$0.05/GB-mo |
| Egress | Not published |
| GPU | Not listed |
| Idle billing | Billed while running (by default nothing happens on idle); suspend (Pro plan) = storage only |
| Max session | 1 h default lifetime, configurable |
| Free tier / credits | $50 trial credit (3 running devboxes) |
| Paid entry | Basic: usage only; Pro $250/mo + usage (adds suspend/resume) |
| Isolation | microVM |
| BYOC / self-host | Enterprise (VPC deployment) |

## Published rates (verbatim)

- "Devbox CPU $0.108 / CPU-hr"
- "Devbox Memory $0.0252 / GB-hr"
- "Devbox Storage $0.00034236 / GB-hr"
- "MEDIUM 2 CPU / 4 GB / 8 GB disk $0.3195"

## Plans and limits

| Plan | Monthly fee | Max concurrent sandboxes | Max concurrent vCPU | Max session |
| --- | --- | --- | --- | --- |
| Basic | $0 | not published | not published | not published |
| Enterprise (VPC deployment) | custom | custom | custom | custom |

## Cost in the standard scenarios

| Scenario | Compute total | Cheapest plan that fits |
| --- | --- | --- |
| [1,000 × 5 min](../scenarios/short-lived-agents.md) | $13.34 | Basic (no plan fee) ⚠ limits not published |
| [100 × 1 h](../scenarios/100-sandboxes.md) | $32.02 | Basic (no plan fee) ⚠ limits not published |
| [1,000 × 2 h](../scenarios/large-batch.md) | $640.45 | Basic (no plan fee) ⚠ limits not published |
| [10 × 24/7 (month)](../scenarios/long-running-agents.md) | $2,362.62 | Basic (no plan fee) ⚠ limits not published |

## Caveats and open questions

- Egress pricing not published.
- Paid-plan concurrency limits not published.
- Pricing FAQ example ('2-CPU / 4 GB … 8 hours … approximately $2.73/day') does not match the listed unit rates, which give $2.53; the unit rates and size table agree with each other and are used here.
- Suspend/resume is listed as a Pro plan feature.

## Sources

- <https://runloop.ai/pricing>
- <https://docs.runloop.ai/docs/devboxes/configuration/sizes>
- <https://docs.runloop.ai/docs/devboxes/lifecycle>
<!-- END GENERATED: provider:runloop -->

[← Back to the comparison](../README.md)
