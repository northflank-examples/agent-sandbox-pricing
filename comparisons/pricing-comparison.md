# AI Agent Sandbox Pricing Comparison: Full Tables

All tables are generated from [`data/pricing.json`](../data/pricing.json) and verified against official vendor pricing pages (dates in each [provider page](../providers/)). Rates are list prices for the default US region.

## Compute rates

<!-- BEGIN GENERATED: rates -->
| Provider | CPU / vCPU-hr | RAM / GiB-hr | Billed size for 2 vCPU + 4 GiB | Per hour (CPU 100% busy) | Per hour (CPU 25% busy) | Billing model | Billing unit | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Northflank](../providers/northflank.md) | $0.01667 | $0.00833 | 2 vCPU / 4 GiB | $0.0667 | $0.0667 | allocated | per second | [pricing](https://northflank.com/pricing) |
| [Cloudflare Sandbox](../providers/cloudflare.md) | $0.072 | $0.009 | **2 vCPU / 6 GiB** | $0.1980 | $0.0900 | active CPU | per 10 ms | [pricing](https://developers.cloudflare.com/containers/pricing/) |
| [Sprites (Fly.io)](../providers/sprites.md) | $0.0385 | $0.02187 | 2 vCPU / 4 GiB (used) | $0.1645 | $0.1067 | usage | usage-metered (page says hourly; docs say per-second) | [pricing](https://fly.io/sprites) |
| [Vercel Sandbox](../providers/vercel.md) | $0.128 | $0.0212 | 2 vCPU / 4 GiB | $0.3408 | $0.1488 | active CPU | CPU: active time; memory: 1-min increments | [pricing](https://vercel.com/docs/vercel-sandbox/pricing) |
| [E2B](../providers/e2b.md) | $0.0504 | $0.0162 | 2 vCPU / 4 GiB | $0.1656 | $0.1656 | allocated | per second | [pricing](https://e2b.dev/pricing) |
| [Daytona](../providers/daytona.md) | $0.0504 | $0.0162 | 2 vCPU / 4 GiB | $0.1656 | $0.1656 | allocated | per second | [pricing](https://www.daytona.io/pricing) |
| [Modal](../providers/modal.md) | $0.07096 | $0.02401 | 2 vCPU / 4 GiB | $0.2380 | $0.2380 | max(request, usage) | per second | [pricing](https://modal.com/pricing) |
| [Runloop](../providers/runloop.md) | $0.108 | $0.0252 | 2 vCPU / 4 GiB | $0.3168 | $0.3168 | allocated | per second | [pricing](https://runloop.ai/pricing) |
<!-- END GENERATED: rates -->

## How CPU utilisation changes the price

Price per hour for one **2 vCPU / 4 GiB** sandbox at different levels of CPU activity.

- **Allocated-resource providers** (Northflank, E2B, Daytona, Modal, Runloop) charge the same at every utilisation.
- **Active-CPU and usage-billed providers** (Vercel, Cloudflare, Sprites) get cheaper as the sandbox spends more time waiting on I/O or LLM calls.
- **Cloudflare** is billed at 6 GiB here because of its 3 GiB per vCPU minimum.

<!-- BEGIN GENERATED: sensitivity -->
| Provider | CPU 5% busy | CPU 25% busy | CPU 50% busy | CPU 100% busy |
| --- | --- | --- | --- | --- |
| [Northflank](../providers/northflank.md) | $0.0667 | $0.0667 | $0.0667 | $0.0667 |
| [E2B](../providers/e2b.md) | $0.1656 | $0.1656 | $0.1656 | $0.1656 |
| [Daytona](../providers/daytona.md) | $0.1656 | $0.1656 | $0.1656 | $0.1656 |
| [Modal](../providers/modal.md) | $0.2380 | $0.2380 | $0.2380 | $0.2380 |
| [Runloop](../providers/runloop.md) | $0.3168 | $0.3168 | $0.3168 | $0.3168 |
| [Vercel Sandbox](../providers/vercel.md) | $0.0976 | $0.1488 | $0.2128 | $0.3408 |
| [Cloudflare Sandbox](../providers/cloudflare.md) | $0.0612 | $0.0900 | $0.1260 | $0.1980 |
| [Sprites (Fly.io)](../providers/sprites.md) | $0.0914 | $0.1067 | $0.1260 | $0.1645 |
<!-- END GENERATED: sensitivity -->

## Plans, free tiers and idle billing

<!-- BEGIN GENERATED: plans -->
| Provider | Free tier / credits | Paid entry | Max session | Idle billing |
| --- | --- | --- | --- | --- |
| [Northflank](../providers/northflank.md) | Free tier: 2 services, 1 database, 2 cron jobs | Pay-as-you-go, no plan fee | No limit | Billed while running; paused = no compute charge (volumes still billed) |
| [E2B](../providers/e2b.md) | Hobby: one-time $100 credit, 1 h sessions, 20 concurrent | Pro $150/mo + usage | Continuous runtime 1 h (Hobby) / 24 h (Pro); pausing resets it | Billed while running; paused, killed or timed out = billing stops |
| [Daytona](../providers/daytona.md) | $200 free compute credit | No plan fee; limits rise with top-ups | No limit (auto-stop default 15 min; 0 = never) | Auto-stops after 15 min idle (default); stopped = disk only |
| [Modal](../providers/modal.md) | Starter: $30/mo free credits | Team $250/mo + usage | 5 min default, up to 24 h | Billed while running; optional idle_timeout terminates |
| [Runloop](../providers/runloop.md) | $50 trial credit (3 running devboxes) | Basic: usage only; Pro $250/mo + usage (adds suspend/resume) | 1 h default lifetime, configurable | Billed while running (by default nothing happens on idle); suspend (Pro plan) = storage only |
| [Vercel Sandbox](../providers/vercel.md) | Hobby: 5 h active CPU, 420 GB-hr memory/mo; 45 min sessions; 10 concurrent | Pro $20/mo (credited against usage) | 45 min (Hobby), 24 h (Pro); resets on stop/resume | Memory billed while running; CPU only when busy; stopped = snapshot storage |
| [Cloudflare Sandbox](../providers/cloudflare.md) | Included in Workers Paid: 375 vCPU-min, 25 GiB-hr memory/mo | Workers Paid $5/mo + usage | No published max; keepAlive keeps billing | Memory/disk billed while awake; CPU only when busy; sleeps after 10 min (default) |
| [Sprites (Fly.io)](../providers/sprites.md) | $30 trial credit | Pay-as-you-go; prepaid tiers (e.g. Hero $100/mo) | No limit (persistent) | Only billed while running; pauses after ~30 s idle (warm/cold not billed) |
<!-- END GENERATED: plans -->

## Storage, network, GPU and isolation

<!-- BEGIN GENERATED: extras -->
| Provider | Storage | Egress | GPU | Isolation | BYOC / self-host |
| --- | --- | --- | --- | --- | --- |
| [Northflank](../providers/northflank.md) | Ephemeral disk included; SSD volumes $0.15/GB-mo | $0.06/GB | L4 $0.80/hr, A100 80GB $1.76/hr, H100 $2.74/hr, RTX PRO 6000 $3.00/hr (GPU plans include CPU and RAM) | microVM (Kata Containers) for CPU sandboxes; gVisor for GPU sandboxes | Yes: AWS, GCP, Azure, Oracle, CoreWeave, Civo, or your own Kubernetes cluster ($0.02083/vCPU-hr management fee, $0 memory; cloud costs separate) |
| [E2B](../providers/e2b.md) | Included (10 GiB Hobby / 20 GiB Pro) | Not published | Not listed | Firecracker microVM | Enterprise (AWS, GCP, Azure); Apache-2.0 runtime can be self-hosted |
| [Daytona](../providers/daytona.md) | First 5 GiB free, then $0.000108/GiB-hr (~$0.08/GiB-mo) | Not published (restricted on Tier 1-2) | Preemptible: H100 $2.27/hr, H200 $2.61/hr, B200 $3.59/hr; on-demand: H100 $3.95/hr | Containers by default; optional VM sandboxes with their own kernel | Enterprise (bring your own compute) |
| [Modal](../providers/modal.md) | Volumes $0.09/GiB-mo (1 TiB/mo free) | $0.04/GiB (1 TiB/mo included on Starter) | Standard GPU rates + CPU/RAM: L4 ~$0.80/hr, A100 80GB ~$2.50/hr, H100 ~$3.95/hr | gVisor (default) or VM runtime | No |
| [Runloop](../providers/runloop.md) | Devbox disk $0.00034236/GB-hr (~$0.25/GB-mo); snapshots ~$0.05/GB-mo | Not published | Not listed | microVM | Enterprise (VPC deployment) |
| [Vercel Sandbox](../providers/vercel.md) | 64 GB ephemeral NVMe included; snapshots $0.08/GB-mo | Included in CDN (Pro); $0.15/GB (Enterprise) | Not offered | Firecracker microVM | No |
| [Cloudflare Sandbox](../providers/cloudflare.md) | Disk $0.00000007/GB-s while running; no persistent volume pricing | $0.025/GB NA/EU (1 TB included) | Not offered | Firecracker microVM | No |
| [Sprites (Fly.io)](../providers/sprites.md) | Persistent: hot ~$0.50/GB-mo while awake, cold ~$0.02/GB-mo | Not metered today | Not offered | microVM | No |
<!-- END GENERATED: extras -->

## Related

- [Billing models explained](billing-models.md)
- [Hidden costs](hidden-costs.md)
- [Workload scenarios](../scenarios/README.md)
- [Methodology](../methodology.md)
