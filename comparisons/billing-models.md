# Sandbox Billing Models Explained

AI sandbox providers use four different billing models. Comparing headline "per vCPU-hour" rates across them is misleading unless you know which model applies.

## 1. Allocated resources

**Providers:** Northflank, E2B, Daytona, Runloop

You pay for the vCPU and memory **reserved** for the sandbox, every second it runs, whether or not the CPU is doing anything. Think of it like renting a machine by the second: the meter runs on its size, not on how hard it works.

```
cost per hour = vCPU × CPU rate + GiB × memory rate (+ disk, where metered)
```

- **Predictable:** the cost depends only on size and runtime.
- **Pays for idle:** an agent waiting 30 seconds for an LLM response pays for 30 seconds of full CPU and RAM. To avoid that, pause or stop the sandbox:
  - Daytona auto-stops after 15 idle minutes by default.
  - E2B can auto-pause on timeout.
  - Runloop has an opt-in idle suspend.
  - Northflank supports pausing through its API, which stops compute charges.
  - Runloop's suspend/resume is a Pro plan feature.
- **Fixed sizes on some providers.** Northflank cloud sells fixed plans (e.g. 1 vCPU / 4 GB, 2 vCPU / 4 GB), so you pay for the smallest plan that fits. Runloop offers presets plus custom sizes.
- **Low rates offset idle time.** Northflank's rates are low enough that a fully allocated sandbox still costs less than most active-CPU options unless utilisation is very low (see the [sensitivity table](pricing-comparison.md#how-cpu-utilisation-changes-the-price)).

## 2. max(request, usage)

**Provider:** Modal

You set a CPU and memory **request** (a guaranteed minimum), and the sandbox can burst above it when the host has spare capacity. Modal bills "whichever is higher: your resource request or your actual usage".

```
cost per hour = max(requested cores, used cores) × CPU rate + max(requested GiB, used GiB) × memory rate
```

- If you request what you need, this behaves exactly like **allocated** billing, and this comparison prices it that way.
- Modal recommends requesting around p50–75 of observed CPU use and letting bursts cover the peaks. That can lower costs compared with the figures here, at the risk of being throttled when the host is busy.
- CPU is quoted per *physical core*, which Modal defines as 2 vCPU.

## 3. Active CPU + provisioned memory

**Providers:** Vercel Sandbox, Cloudflare Sandbox

**Memory** (and on Cloudflare, disk) is billed for the whole runtime. **CPU** is billed only while it is actually executing. Vercel says it outright: "Time spent waiting for I/O (such as network requests, database queries, or AI model calls) does not count toward Active CPU."

```
cost per hour = vCPU × CPU rate × utilisation + GiB × memory rate
```

- **Suits agent loops** that spend most of their time waiting on model responses.
- **Higher CPU rates** (Vercel $0.128, Cloudflare $0.072 per vCPU-hour) mean busy workloads such as builds, tests and data processing cost more than on allocated-resource providers.
- **Fixed memory ratios** apply: Vercel includes 2 GB per vCPU, and Cloudflare needs at least 3 GiB per vCPU.

## 4. Actual usage

**Provider:** Sprites (Fly.io)

CPU is billed on cumulative CPU time measured by the kernel (`cpu.stat`), and memory on **actual memory used**, not the allocation. Sprites have a fixed 8 vCPU / 100 GB shape, but you only pay for what's consumed while the Sprite is running. Sprites pause after about 30 seconds idle (per the lifecycle docs) and then cost only storage.

- **Suits** bursty, persistent environments that sit idle most of the day.
- **Hard to predict in advance:** this comparison assumes the full stated memory is used, which is conservative.

## Which model is cheapest?

| Your workload | Usually cheapest model |
| --- | --- |
| Short, CPU-heavy tasks (builds, tests, evals) | Allocated, at low rates |
| Agent loops mostly waiting on LLM calls | Active CPU, or allocated at low rates |
| Long-lived environments idle most of the day | Usage-billed, or anything with automatic pause |
| Thousands of concurrent sandboxes | Whatever has no plan fee for concurrency |

Run your own numbers in the [web estimator](https://p01--sandbox-pricing-estimator--wdgpv6bn4jz8.code.run) or with `python3 scripts/estimate.py --help`.
