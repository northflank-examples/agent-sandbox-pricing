# AI Agent Sandbox Pricing Comparison (2026): Northflank, E2B, Daytona, Modal, Vercel, Cloudflare, Runloop & Sprites

An open, source-linked comparison of what it costs to run **AI agent sandboxes** (isolated environments where agents execute code), covering per-vCPU and per-GiB rates, billing models, idle charges, plan fees, and **total cost for realistic agent workloads**.

- **Prices last verified:** 2026-10-14 (each provider page shows its own verification date)
- **Providers:** [Northflank](providers/northflank.md) · [E2B](providers/e2b.md) · [Daytona](providers/daytona.md) · [Modal](providers/modal.md) · [Vercel Sandbox](providers/vercel.md) · [Cloudflare Sandbox](providers/cloudflare.md) · [Runloop](providers/runloop.md) · [Sprites (Fly.io)](providers/sprites.md)
- **Note:** Runloop is winding down; it supports existing customers until November 13, 2026 ([source](https://docs.runloop.ai/docs/devboxes/configuration/sizes)). It stays in the tables until then.
- **Data:** every number comes from [`data/pricing.json`](data/pricing.json), and every table below is generated from it. Price your own workload in the [web estimator](https://p01--sandbox-pricing-estimator--wdgpv6bn4jz8.code.run) or the [CLI](#estimate-your-own-workload).

> **Disclosure:** this repository is maintained by [Northflank](https://northflank.com/product/sandboxes), one of the providers compared. To keep it fair, every provider uses the same [methodology](methodology.md), every rate links to the vendor's own pricing page, and corrections from any vendor or user are welcome via [pull request](CONTRIBUTING.md).

## Contents

- [Quick comparison: price per sandbox-hour](#quick-comparison-price-per-sandbox-hour)
- [Cost by workload](#cost-by-workload)
- [How much do AI agent sandboxes cost?](#how-much-do-ai-agent-sandboxes-cost)
- [Why the cheapest rate isn't always the cheapest bill](#why-the-cheapest-rate-isnt-always-the-cheapest-bill)
- [Plans, free tiers and idle billing](#plans-free-tiers-and-idle-billing)
- [Estimate your own workload](#estimate-your-own-workload)
- [FAQ](#faq)
- [Methodology and sources](#methodology-and-sources)

## Quick comparison: price per sandbox-hour

List prices for one sandbox with **2 vCPU and 4 GiB RAM**, sorted by the price for a typical agent sandbox (CPU 25% busy). Two price columns are shown because three providers (Vercel, Cloudflare, Sprites) bill CPU only while it's busy. For the others, CPU utilisation doesn't change the price. The *billed size* column shows what you actually pay for when a provider can't sell exactly 2 vCPU / 4 GiB.

<!-- BEGIN GENERATED: rates -->
| Provider | CPU / vCPU-hr | RAM / GiB-hr | Billed size for 2 vCPU + 4 GiB | Per hour (CPU 100% busy) | Per hour (CPU 25% busy) | Billing model | Billing unit | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Northflank](providers/northflank.md) | $0.01667 | $0.00833 | 2 vCPU / 4 GiB | $0.0667 | $0.0667 | allocated | per second | [pricing](https://northflank.com/pricing) |
| [Cloudflare Sandbox](providers/cloudflare.md) | $0.072 | $0.009 | **2 vCPU / 6 GiB** | $0.1980 | $0.0900 | active CPU | per 10 ms | [pricing](https://developers.cloudflare.com/containers/pricing/) |
| [Sprites (Fly.io)](providers/sprites.md) | $0.0385 | $0.02187 | 2 vCPU / 4 GiB (used) | $0.1645 | $0.1067 | usage | usage-metered (page says hourly; docs say per-second) | [pricing](https://fly.io/sprites) |
| [Vercel Sandbox](providers/vercel.md) | $0.128 | $0.0212 | 2 vCPU / 4 GiB | $0.3408 | $0.1488 | active CPU | CPU: active time; memory: 1-min increments | [pricing](https://vercel.com/docs/vercel-sandbox/pricing) |
| [E2B](providers/e2b.md) | $0.0504 | $0.0162 | 2 vCPU / 4 GiB | $0.1656 | $0.1656 | allocated | per second | [pricing](https://e2b.dev/pricing) |
| [Daytona](providers/daytona.md) | $0.0504 | $0.0162 | 2 vCPU / 4 GiB | $0.1656 | $0.1656 | allocated | per second | [pricing](https://www.daytona.io/pricing) |
| [Modal](providers/modal.md) | $0.07096 | $0.02401 | 2 vCPU / 4 GiB | $0.2380 | $0.2380 | max(request, usage) | per second | [pricing](https://modal.com/pricing) |
| [Runloop](providers/runloop.md) (shutting down) | $0.108 | $0.0252 | 2 vCPU / 4 GiB | $0.3168 | $0.3168 | allocated | per second | [pricing](https://runloop.ai/pricing) |
<!-- END GENERATED: rates -->

*Billing model:* **allocated** = you pay for the vCPU and RAM reserved for the sandbox, every second it runs, busy or not · **max(request, usage)** = the same, except you pay for actual usage instead if it exceeds the reservation (Modal) · **active CPU** = RAM billed while running, CPU billed only while it is executing · **usage** = only the CPU time and RAM actually consumed. **Bold** billed sizes mean the provider bills more than you asked for, because of fixed plans or a minimum RAM-per-vCPU ratio. See [billing models explained](comparisons/billing-models.md).

*Validation:* the formula reproduces 31 of 31 prices and worked examples published by the vendors themselves, including all of Northflank's and Runloop's listed sizes, E2B's calculator, and Vercel's and Sprites' cost examples. CI re-runs these checks ([`scripts/validate.py`](scripts/validate.py)).

## Cost by workload

Hourly rates don't answer "what will my bill be?", so here are four standard agent workloads, priced on every provider. Totals are **compute plus disk while running, at list price** (disk is $0 where the provider includes it): no free credits, plan fees, egress or persistent storage. Each scenario page also shows which plan you'd need to reach that concurrency.

<!-- BEGIN GENERATED: scenarios -->
| Provider | [1,000 × 5 min](scenarios/short-lived-agents.md) | [100 × 1 h](scenarios/100-sandboxes.md) | [1,000 × 2 h](scenarios/large-batch.md) | [10 × 24/7 (month)](scenarios/long-running-agents.md) |
| --- | --- | --- | --- | --- |
| [Northflank](providers/northflank.md) | $4.17 | $6.67 | $133.32 | $486.62 |
| [Cloudflare Sandbox](providers/cloudflare.md) | $5.35 | $9.25 | $257.04 | $536.11 |
| [Sprites (Fly.io)](providers/sprites.md) | $5.53 | $11.36 | $265.66 | $794.68 |
| [Vercel Sandbox](providers/vercel.md) | $8.87 | $14.88 | $425.60 | $805.92 |
| [E2B](providers/e2b.md) | $6.90 | $16.56 | $331.20 | $1,208.88 |
| [Daytona](providers/daytona.md) | $6.90 | $16.61 | $332.28 | $1,220.71 |
| [Modal](providers/modal.md) | $9.92 | $23.80 | $475.92 | $1,737.11 |
| [Runloop](providers/runloop.md) (shutting down) | $13.34 | $32.02 | $640.45 | $2,362.62 |

- **1,000 × 5 min**: 1,000 short code-execution sandboxes (1 vCPU, 2 GiB, 5 GB disk), 5 minutes each, 50 running at once, CPU 50% busy.
- **100 × 1 h**: 100 coding-agent sandboxes (2 vCPU, 4 GiB, 10 GB disk), 1 hour each, all running at once, CPU 25% busy.
- **1,000 × 2 h**: 1,000 sandboxes for an eval / RL batch (2 vCPU, 4 GiB, 10 GB disk), 2 hours each, all running at once, CPU 50% busy.
- **10 × 24/7 (month)**: 10 always-on agent environments (2 vCPU, 4 GiB, 20 GB disk) running 24/7 for a 730-hour month, CPU 10% busy.
<!-- END GENERATED: scenarios -->

**Key takeaways (for these assumptions):**

- **Northflank has the lowest allocated-resource rates** in this comparison ($0.01667/vCPU-hr, $0.00833/GB-hr), so it is the cheapest option in all four standard scenarios.
- **Mostly-idle sandboxes change the order.** Cloudflare bills CPU only while it's busy and has a low memory rate, so it is cheaper than Northflank when the CPU is busy less than about 9% of the time. That comparison excludes Cloudflare's Workers and Durable Objects charges. See the [utilisation sensitivity table](comparisons/pricing-comparison.md#how-cpu-utilisation-changes-the-price).
- **E2B and Daytona publish identical CPU and RAM rates** ($0.0504/vCPU-hr, $0.0162/GiB-hr). The difference is in plan structure: E2B charges $150–$1,150/mo for concurrency, and Daytona raises limits as you top up credit.
- **Modal sandboxes cost about 3× Modal Functions** on CPU and RAM. Compare sandbox rates, not the headline Functions rates.
- **Fixed sizes and ratios add cost.** Northflank cloud sells fixed plans, so a 1 vCPU / 2 GiB sandbox is billed as 1 vCPU / 4 GB ($0.05/hr). Cloudflare needs at least 3 GiB per vCPU, so 2 vCPU / 4 GiB is billed as 6 GiB.
- **Plan limits can cost more than compute.** Northflank has no plan fee or concurrency limit, while running 1,000 sandboxes at once needs E2B's $1,150/mo concurrency add-on, Modal's $250/mo Team plan, or an enterprise contract on Daytona and Cloudflare.

## How much do AI agent sandboxes cost?

At list prices, a 2 vCPU / 4 GiB sandbox costs roughly **$0.07–$0.32 per hour** depending on provider (CPU 25% busy). The basic formula is:

```
cost = sandboxes × hours × (vCPU × CPU rate × CPU-billing factor  +  GiB × memory rate  +  disk)
       + per-sandbox fees + plan fee
```

For example, 100 agents × 1 hour × 2 vCPU / 4 GiB on Northflank is 100 × 1 × (2 × $0.01667 + 4 × $0.00833) = **$6.67**. The same workload is **$16.56 on E2B** and **$23.80 on Modal**.

The main cost drivers, roughly in order of impact:

1. **Runtime.** You pay for wall-clock time the sandbox exists, not the time your agent is "working", unless the provider bills active CPU or auto-pauses.
2. **Size.** Billed vCPU and memory. Some providers force a ratio: Cloudflare needs at least 3 GiB per vCPU, and Vercel fixes 2 GB per vCPU.
3. **Concurrency.** It decides which plan you need: E2B Pro caps at 100 concurrent sandboxes, Modal Starter at 100, Vercel Hobby at 10.
4. **Idle time.** It is the biggest hidden cost for long-lived agents (see below).
5. **Storage, snapshots and egress.** These are usually small for short tasks and significant for persistent environments. See [hidden costs](comparisons/hidden-costs.md).

## Why the cheapest rate isn't always the cheapest bill

- **Idle billing.** A coding agent that waits on LLM responses 80% of the time still pays full price on allocated-resource providers, unless you pause it. Active-CPU providers (Vercel, Cloudflare) charge only memory during that wait, and Sprites pauses automatically after about 30 s idle.
- **Forced resource ratios.** On Cloudflare you can't buy 2 vCPU with 4 GiB. The minimum is 6 GiB, and you pay for it.
- **Plan fees and concurrency caps.** E2B's per-second rate is the same as Daytona's, but 1,000 concurrent sandboxes on E2B adds $1,150/mo.
- **Session limits.** Modal sandboxes have a hard 24 h maximum lifetime. E2B Pro and Vercel Pro limit a single continuous session to 24 h, but pausing and resuming resets the clock. Always-on agents must build snapshot/restore or pause/resume logic, or move to an enterprise plan.
- **Line items beyond CPU and memory.** Metered disk (Runloop, Sprites hot storage, Cloudflare, Daytona above 5 GiB) and Vercel's per-creation fee are in the scenario totals. Cloudflare's Durable Objects and Workers requests and egress are not, and several vendors don't publish egress prices at all.

Full breakdown: [comparisons/hidden-costs.md](comparisons/hidden-costs.md).

## Plans, free tiers and idle billing

<!-- BEGIN GENERATED: plans -->
| Provider | Free tier / credits | Paid entry | Max session | Idle billing |
| --- | --- | --- | --- | --- |
| [Northflank](providers/northflank.md) | Free tier: 2 services, 1 database, 2 cron jobs | Pay-as-you-go, no plan fee | No limit | Billed while running; paused = no compute charge (volumes still billed) |
| [E2B](providers/e2b.md) | Hobby: one-time $100 credit, 1 h sessions, 20 concurrent | Pro $150/mo + usage | Continuous runtime 1 h (Hobby) / 24 h (Pro); pausing resets it | Billed while running; paused, killed or timed out = billing stops |
| [Daytona](providers/daytona.md) | $200 free compute credit | No plan fee; limits rise with top-ups | No limit (auto-stop default 15 min; 0 = never) | Auto-stops after 15 min idle (default); stopped = disk only |
| [Modal](providers/modal.md) | Starter: $30/mo free credits | Team $250/mo + usage | 5 min default, up to 24 h | Billed while running; optional idle_timeout terminates |
| [Runloop](providers/runloop.md) (shutting down) | $50 trial credit (3 running devboxes) | Basic: usage only; Pro $250/mo + usage (adds suspend/resume) | 1 h default lifetime, configurable | Billed while running (by default nothing happens on idle); suspend (Pro plan) = storage only |
| [Vercel Sandbox](providers/vercel.md) | Hobby: 5 h active CPU, 420 GB-hr memory/mo; 45 min sessions; 10 concurrent | Pro $20/mo (credited against usage) | 45 min (Hobby), 24 h (Pro); resets on stop/resume | Memory billed while running; CPU only when busy; stopped = snapshot storage |
| [Cloudflare Sandbox](providers/cloudflare.md) | Included in Workers Paid: 375 vCPU-min, 25 GiB-hr memory/mo | Workers Paid $5/mo + usage | No published max; keepAlive keeps billing | Memory/disk billed while awake; CPU only when busy; sleeps after 10 min (default) |
| [Sprites (Fly.io)](providers/sprites.md) | $30 trial credit | Pay-as-you-go; prepaid tiers (e.g. Hero $100/mo) | No limit (persistent) | Only billed while running; pauses after ~30 s idle (warm/cold not billed) |
<!-- END GENERATED: plans -->

Storage, egress, GPU, isolation technology and BYOC options are in [comparisons/pricing-comparison.md](comparisons/pricing-comparison.md).

## Estimate your own workload

**Web:** [p01--sandbox-pricing-estimator--wdgpv6bn4jz8.code.run](https://p01--sandbox-pricing-estimator--wdgpv6bn4jz8.code.run). Enter your sandbox count, runtime, size and CPU utilisation and it prices the workload on every provider, using the same data and model as the tables above. Estimates have shareable links.

**CLI:** no dependencies beyond Python 3.9+:

```bash
git clone https://github.com/northflank-examples/agent-sandbox-pricing.git
cd agent-sandbox-pricing
python3 scripts/estimate.py --sandboxes 500 --minutes 30 --vcpu 2 --memory 4 --cpu-busy 0.3 --concurrency 200
```

It prints the per-sandbox-hour price, the compute total and the cheapest published plan that fits your concurrency for every provider.

### Web estimator

The [hosted estimator](https://p01--sandbox-pricing-estimator--wdgpv6bn4jz8.code.run) is the static page in [`web/`](web/) (no build step). To run it locally:

```bash
python3 -m http.server 8000   # from the repo root, then open http://localhost:8000/web/
```

To deploy it, build the root [`Dockerfile`](Dockerfile) (nginx serving `web/` and `data/pricing.json` on port 8080), for example as a Northflank combined service. CI checks that [`web/model.js`](web/model.js) gives the same results as [`scripts/model.py`](scripts/model.py) (`python3 scripts/check_web_model.py`, needs Node.js 18+).

## FAQ

### What is the cheapest AI agent sandbox provider?

It depends on how busy your sandboxes are. For sandboxes that do real work (CPU more than about 10% busy), **Northflank** has the lowest list price in this comparison: $0.0667/hr for 2 vCPU / 4 GiB. For mostly-idle sandboxes, **Cloudflare Sandbox** can be cheaper on compute because it bills CPU only while active. It also requires the $5/mo Workers Paid plan and adds Durable Objects charges. Check your own numbers with the [estimator](https://p01--sandbox-pricing-estimator--wdgpv6bn4jz8.code.run).

### How much does it cost to run 100 AI agents?

Take 100 sandboxes running for one hour at 2 vCPU / 4 GiB with the CPU 25% busy. Compute alone costs:

<!-- BEGIN GENERATED: answer:100-sandboxes -->
- Northflank: $6.67
- Cloudflare Sandbox: $9.25
- Sprites (Fly.io): $11.36
- Vercel Sandbox: $14.88
- E2B: $16.56
- Daytona: $16.61
- Modal: $23.80
- Runloop: $32.02
<!-- END GENERATED: answer:100-sandboxes -->

On top of that, E2B requires its $150/mo Pro plan for 100 concurrent sandboxes. Details: [scenarios/100-sandboxes.md](scenarios/100-sandboxes.md).

### Do sandbox providers charge for idle time?

Most do, if the sandbox is still running. Northflank, E2B, Daytona, Modal and Runloop bill allocated CPU and RAM for every second a sandbox runs, idle or not. Vercel and Cloudflare bill memory while running but CPU only when busy. Sprites bills only actual usage and auto-pauses after about 30 s.

Paused or stopped sandboxes are generally free of compute charges on all providers but may still incur storage. Daytona auto-stops after 15 idle minutes by default. Cloudflare sleeps after 10 minutes. Runloop does nothing on idle unless you configure it.

### Which providers charge for egress?

Published egress prices are:

- Northflank: $0.06/GB.
- Modal: $0.04/GiB, with 1 TiB/mo included on Starter.
- Cloudflare: $0.025/GB in NA/EU, with 1 TB included.
- Vercel: included in Pro's CDN allowance, or $0.15/GB on Enterprise.
- Sprites: not metered today.

E2B, Daytona and Runloop don't publish egress pricing.

### What's the maximum sandbox session length?

- Northflank: no session limit.
- E2B: 1 h of continuous runtime on Hobby, 24 h on Pro. Pausing resets it, and paused sandboxes are kept indefinitely.
- Vercel: 45 min per session on Hobby, 24 h on Pro. Stopping and resuming starts a new session.
- Modal: 24 h maximum lifetime. Modal recommends filesystem snapshots for longer work.
- Daytona, Cloudflare and Sprites: no published maximum.
- Runloop: defaults to 1 h, and you can configure it.

### Is self-hosting or BYOC cheaper than a managed sandbox?

At scale it can be, because you pay your cloud provider's rates (and can use committed-use discounts or spot capacity) plus any platform fee. BYOC is offered by:

- Northflank: AWS, GCP, Azure, Oracle, CoreWeave, Civo, or your own Kubernetes cluster. You pay your cloud provider directly, plus a management fee of $0.02083/vCPU-hour ($0 for memory, $0.00139/GB vRAM-hour for your own GPUs).
- E2B: Enterprise only (AWS, GCP and Azure). The Apache-2.0 runtime can also be self-hosted.
- Daytona and Runloop: Enterprise only.

Self-hosting also means you operate the isolation layer (Firecracker, Kata, gVisor) yourself.

### Do any sandbox providers offer GPUs?

Yes: Northflank (L4, A100, H100 and RTX PRO 6000, with CPU and RAM included), Modal (standard GPU rates plus CPU/RAM) and Daytona (preemptible or on-demand H100, H200, B200 and others). E2B, Vercel, Cloudflare, Runloop and Sprites list no GPU sandboxes. See the [GPU column](comparisons/pricing-comparison.md#storage-network-gpu-and-isolation).

### What isn't included in these numbers?

Free credits, plan fees (shown separately), persistent storage, snapshots, egress, regional price multipliers, enterprise discounts, and platform charges outside the sandbox itself, such as Cloudflare Workers and Durable Objects. See [methodology.md](methodology.md).

## Methodology and sources

- Rates come only from official vendor pricing pages and docs, linked from each [provider page](providers/). Anything that isn't published is marked **not published**, never assumed to be free.
- Rates are normalised to **per vCPU-hour** and **per GiB-hour**. Modal's "physical core" is counted as 2 vCPU, as Modal itself states.
- Fixed sizes are respected: you are billed for the cheapest size the provider actually sells that fits the request.
- Scenario costs assume the sandbox runs for its full duration with the stated CPU utilisation. Active-CPU and usage-billed providers are charged CPU × utilisation. Allocated-resource providers are charged full CPU.
- Full details, including rounding and known limitations, are in [methodology.md](methodology.md).

## Repository layout

```
README.md                     ← you are here
methodology.md                how numbers are collected and calculated
providers/                    one page per provider (rates, plans, limits, sources)
comparisons/
  pricing-comparison.md       full rate, plan, storage/network/GPU tables
  billing-models.md           allocated vs active-CPU vs usage billing
  hidden-costs.md             what the per-hour rate doesn't tell you
scenarios/                    four standard workloads, priced per provider
data/pricing.json             single source of truth
scripts/estimate.py           price your own workload (CLI)
web/                          the same estimator as a web page
scripts/validate.py           checks the model against vendor-published prices
scripts/generate.py           regenerates every table from the data
```

## Contributing

Found a price change or an error? See [CONTRIBUTING.md](CONTRIBUTING.md). Edit `data/pricing.json`, run `python3 scripts/generate.py`, and open a PR with a link to the official source. Vendors are welcome to submit corrections for their own listings.

## License

Content is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): reuse it freely with attribution. Scripts are MIT. Prices are the respective vendors' and may change at any time, so always confirm on the official pricing page before buying.
