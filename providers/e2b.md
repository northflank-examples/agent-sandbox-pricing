# E2B Sandbox Pricing

E2B provides Firecracker microVM sandboxes for AI agents with an open-source runtime. Compute is billed per second on allocated vCPU and memory; a monthly plan fee sets session length and concurrency limits.

<!-- BEGIN GENERATED: provider:e2b -->
Last verified: **2026-10-16** · Official pricing: <https://e2b.dev/pricing>

## At a glance

|  |  |
| --- | --- |
| Billing model | allocated |
| Billing unit | per second |
| CPU | $0.0504 per vCPU-hour |
| Memory | $0.0162 per GiB-hour |
| 2 vCPU + 4 GiB sandbox, 1 hour (CPU 25% busy) | $0.1656 |
| Storage | Included (10 GiB Hobby / 20 GiB Pro) |
| Egress | Not published |
| GPU | Not listed |
| Idle billing | Billed while running; paused, killed or timed out = billing stops |
| Max session | Continuous runtime 1 h (Hobby) / 24 h (Pro); pausing resets it |
| Free tier / credits | Hobby: one-time $100 credit, 1 h sessions, 20 concurrent |
| Paid entry | Pro $150/mo + usage |
| Isolation | Firecracker microVM |
| BYOC / self-host | Enterprise (AWS, GCP, Azure); Apache-2.0 runtime can be self-hosted |

## Published rates (verbatim)

- "vCPUs 1 Hobby / Pro $0.000014/s"
- "Memory (GiB) 1 Hobby / Pro $0.0000045/s"
- "You pay per second for compute resources while your sandbox is running"

## Plans and limits

| Plan | Monthly fee | Max concurrent sandboxes | Max concurrent vCPU | Max session |
| --- | --- | --- | --- | --- |
| Hobby | $0 | 20 | not published | 1 h |
| Pro | $150 | 100 | not published | 24 h |
| Pro + 500 concurrency | $650 | 600 | not published | 24 h |
| Pro + 1,000 concurrency | $1,150 | 1,100 | not published | 24 h |
| Enterprise ($3,000/mo minimum; multi-day sessions, BYOC) | custom | custom | custom | custom |

## Cost in the standard scenarios

| Scenario | Compute total | Cheapest plan that fits |
| --- | --- | --- |
| [1,000 × 5 min](../scenarios/short-lived-agents.md) | $6.90 | Pro ($150/mo) |
| [100 × 1 h](../scenarios/100-sandboxes.md) | $16.56 | Pro ($150/mo) |
| [1,000 × 2 h](../scenarios/large-batch.md) | $331.20 | Pro + 1,000 concurrency ($1,150/mo) |
| [10 × 24/7 (month)](../scenarios/long-running-agents.md) | $1,208.88 | Pro ($150/mo) ⚠ max session 24 h; restart or Enterprise ($3,000/mo minimum; multi-day sessions, BYOC) |

## Caveats and open questions

- Default RAM: the pricing page marks 4 GiB as default; the billing docs say '2 vCPU, 512 MiB RAM'.
- Hobby uses the default sandbox size; custom CPU/RAM requires Pro.
- Egress pricing and paused-sandbox storage pricing are not published.

## Sources

- <https://e2b.dev/pricing>
- <https://e2b.dev/docs/billing>
- <https://e2b.dev/docs/sandbox/persistence>
- <https://e2b.dev/docs/byoc>
- <https://github.com/e2b-dev/infra>
<!-- END GENERATED: provider:e2b -->

[← Back to the comparison](../README.md)
