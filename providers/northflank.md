# Northflank Sandbox Pricing

Northflank runs sandboxes in microVMs (Kata Containers) for CPU workloads and under gVisor for GPU workloads, on its managed cloud or inside your own cloud account (BYOC). On Northflank cloud, sandboxes use fixed compute plans (for example `nf-compute-200`: 2 vCPU / 4 GB at $0.0667/hr), billed per second of runtime.

> Disclosure: this repository is maintained by Northflank. Northflank's data follows the same methodology as every other provider here.

<!-- BEGIN GENERATED: provider:northflank -->
Last verified: **2026-10-14** · Official pricing: <https://northflank.com/pricing>

## At a glance

|  |  |
| --- | --- |
| Billing model | allocated |
| Billing unit | per second |
| CPU | $0.01667 per vCPU-hour |
| Memory | $0.00833 per GiB-hour |
| 2 vCPU + 4 GiB sandbox, 1 hour (CPU 25% busy) | $0.0667 |
| Storage | Ephemeral disk included; SSD volumes $0.15/GB-mo |
| Egress | $0.06/GB |
| GPU | L4 $0.80/hr, A100 80GB $1.76/hr, H100 $2.74/hr, RTX PRO 6000 $3.00/hr (GPU plans include CPU and RAM) |
| Idle billing | Billed while running; paused = no compute charge (volumes still billed) |
| Max session | No limit |
| Free tier / credits | Free tier: 2 services, 1 database, 2 cron jobs |
| Paid entry | Pay-as-you-go, no plan fee |
| Isolation | microVM (Kata Containers) for CPU sandboxes; gVisor for GPU sandboxes |
| BYOC / self-host | Yes: AWS, GCP, Azure, Oracle, CoreWeave, Civo, or your own Kubernetes cluster ($0.02083/vCPU-hr management fee, $0 memory; cloud costs separate) |

Northflank cloud sells fixed plans (nf-compute-*); custom sizes are available on BYOC. The cheapest plan that fits is billed.

## Published rates (verbatim)

- "CPU $ 0.01667 / vCPU / hour"
- "Memory $ 0.00833 / GB / hour"
- "nf-compute-200 vCPU 2 dedicated Memory 4096 MB Price $ 48.00 /month ($ 0.0667 /hr)"
- "Northflank cloud bills compute per second of runtime"
- "Ephemeral storage is included in the compute charge"

## Plans and limits

| Plan | Monthly fee | Max concurrent sandboxes | Max concurrent vCPU | Max session |
| --- | --- | --- | --- | --- |
| Pay-as-you-go | $0 | no limit | no limit | no limit |
| Enterprise (custom pricing for high-scale or custom deployments) | custom | custom | custom | custom |

## BYOC pricing

|  |  |
| --- | --- |
| CPU (management fee) | $0.02083 per vCPU-hour |
| Memory | $0.00 per GB-hour |
| Bring your own GPU | $0.00139 per GB vRAM-hour |

- Cloud provider costs are separate (paid directly to your cloud).
- Enterprise pricing may apply for high-scale or custom deployments.

Source: https://northflank.com/pricing (Bring your own cloud tab)

## Cost in the standard scenarios

| Scenario | Compute total | Cheapest plan that fits |
| --- | --- | --- |
| [1,000 × 5 min](../scenarios/short-lived-agents.md) | $4.17 | Pay-as-you-go (no plan fee) |
| [100 × 1 h](../scenarios/100-sandboxes.md) | $6.67 | Pay-as-you-go (no plan fee) |
| [1,000 × 2 h](../scenarios/large-batch.md) | $133.32 | Pay-as-you-go (no plan fee) |
| [10 × 24/7 (month)](../scenarios/long-running-agents.md) | $486.62 | Pay-as-you-go (no plan fee) |

## Caveats and open questions

- Northflank cloud uses fixed compute plans; custom sizes are available on BYOC.
- BYOC is billed as a management fee on top of your own cloud bill: $0.02083/vCPU-hour, $0.00/GB-hour memory, $0.00139/GB vRAM-hour for GPUs. Enterprise pricing may apply for high-scale or custom deployments.

## Sources

- <https://northflank.com/pricing>
- <https://northflank.com/product/sandboxes>
- <https://northflank.com/docs/v1/application/sandboxes/sandboxes-on-northflank-cloud>
<!-- END GENERATED: provider:northflank -->

[← Back to the comparison](../README.md)
