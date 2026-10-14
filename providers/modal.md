# Modal Sandbox Pricing

Modal Sandboxes run arbitrary code in gVisor-isolated containers on Modal's serverless platform. Sandboxes are billed per second on max(request, actual usage), at a separate, higher rate than Modal Functions; Modal quotes CPU per physical core (= 2 vCPU), normalised to per-vCPU here.

<!-- BEGIN GENERATED: provider:modal -->
Last verified: **2026-10-14** · Official pricing: <https://modal.com/pricing>

## At a glance

|  |  |
| --- | --- |
| Billing model | max(request, usage) |
| Billing unit | per second |
| CPU | $0.07096 per vCPU-hour |
| Memory | $0.02401 per GiB-hour |
| 2 vCPU + 4 GiB sandbox, 1 hour (CPU 25% busy) | $0.2380 |
| Storage | Volumes $0.09/GiB-mo (1 TiB/mo free) |
| Egress | $0.04/GiB (1 TiB/mo included on Starter) |
| GPU | Standard GPU rates + CPU/RAM: L4 ~$0.80/hr, A100 80GB ~$2.50/hr, H100 ~$3.95/hr |
| Idle billing | Billed while running; optional idle_timeout terminates |
| Max session | 5 min default, up to 24 h |
| Free tier / credits | Starter: $30/mo free credits |
| Paid entry | Team $250/mo + usage |
| Isolation | gVisor (default) or VM runtime |
| BYOC / self-host | No |

## Published rates (verbatim)

- "Modal Sandbox + Notebooks pricing: CPU Physical core (2 vCPU equivalent) $0.00003942 / core / sec"
- "Memory $0.00000667 / GiB / sec"
- "You pay for max(request, actual)"

## Plans and limits

| Plan | Monthly fee | Max concurrent sandboxes | Max concurrent vCPU | Max session |
| --- | --- | --- | --- | --- |
| Starter | $0 | 100 | not published | 24 h |
| Team | $250 | 5,000 | not published | 24 h |
| Enterprise (custom) | custom | custom | custom | custom |

## Cost in the standard scenarios

| Scenario | Compute total | Cheapest plan that fits |
| --- | --- | --- |
| [1,000 × 5 min](../scenarios/short-lived-agents.md) | $9.92 | Starter (no plan fee) |
| [100 × 1 h](../scenarios/100-sandboxes.md) | $23.80 | Starter (no plan fee) |
| [1,000 × 2 h](../scenarios/large-batch.md) | $475.92 | Team ($250/mo) |
| [10 × 24/7 (month)](../scenarios/long-running-agents.md) | $1,737.11 | Starter (no plan fee) ⚠ max session 24 h; restart or Enterprise (custom) |

## Caveats and open questions

- Billed on max(request, actual usage). Modal recommends requesting ~p50-75 of CPU and bursting, which can cost less than the fixed-size figures here.
- Sandbox CPU/RAM rates are ~3x Modal Function rates; the pricing page does not state why.
- Snapshot pricing not published.

## Sources

- <https://modal.com/pricing>
- <https://modal.com/docs/guide/sandbox>
- <https://modal.com/docs/guide/sandbox-resources>
<!-- END GENERATED: provider:modal -->

[← Back to the comparison](../README.md)
