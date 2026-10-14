# Sandbox Cost Scenarios

Four standard workloads, priced on every provider using the same assumptions. Totals are compute-only list prices: free credits, plan fees, egress and persistent storage are excluded. Each scenario page shows the cheapest plan that fits.

<!-- BEGIN GENERATED: scenarios -->
| Provider | [1,000 × 5 min](../scenarios/short-lived-agents.md) | [100 × 1 h](../scenarios/100-sandboxes.md) | [1,000 × 2 h](../scenarios/large-batch.md) | [10 × 24/7 (month)](../scenarios/long-running-agents.md) |
| --- | --- | --- | --- | --- |
| [Northflank](../providers/northflank.md) | $4.17 | $6.67 | $133.32 | $486.62 |
| [Cloudflare Sandbox](../providers/cloudflare.md) | $5.35 | $9.25 | $257.04 | $536.11 |
| [Sprites (Fly.io)](../providers/sprites.md) | $5.53 | $11.36 | $265.66 | $794.68 |
| [Vercel Sandbox](../providers/vercel.md) | $8.87 | $14.88 | $425.60 | $805.92 |
| [E2B](../providers/e2b.md) | $6.90 | $16.56 | $331.20 | $1,208.88 |
| [Daytona](../providers/daytona.md) | $6.90 | $16.61 | $332.28 | $1,220.71 |
| [Modal](../providers/modal.md) | $9.92 | $23.80 | $475.92 | $1,737.11 |
| [Runloop](../providers/runloop.md) | $13.34 | $32.02 | $640.45 | $2,362.62 |

- **1,000 × 5 min**: 1,000 short code-execution sandboxes (1 vCPU, 2 GiB, 5 GB disk), 5 minutes each, 50 running at once, CPU 50% busy.
- **100 × 1 h**: 100 coding-agent sandboxes (2 vCPU, 4 GiB, 10 GB disk), 1 hour each, all running at once, CPU 25% busy.
- **1,000 × 2 h**: 1,000 sandboxes for an eval / RL batch (2 vCPU, 4 GiB, 10 GB disk), 2 hours each, all running at once, CPU 50% busy.
- **10 × 24/7 (month)**: 10 always-on agent environments (2 vCPU, 4 GiB, 20 GB disk) running 24/7 for a 730-hour month, CPU 10% busy.
<!-- END GENERATED: scenarios -->

To price your own workload, run `python3 scripts/estimate.py --help`.
