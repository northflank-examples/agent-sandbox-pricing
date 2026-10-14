# Hidden Costs of AI Agent Sandboxes

The per-hour compute rate is usually the biggest part of a sandbox bill, but not the only part. These are the line items and constraints that most often surprise teams, with what each provider publishes. Items marked **not published** are not shown on the vendor's pricing page or docs; they may be free, quoted on request, or charged.

## 1. Idle compute

On allocated-resource providers, a sandbox that is running but waiting costs the same as one that is busy.

| Provider | What happens when the sandbox is idle |
| --- | --- |
| Northflank | Billed until paused; paused = no compute charge, volumes billed |
| E2B | Billed until paused or killed; auto-pause on timeout available |
| Daytona | Auto-stops after 15 min idle by default; stopped = disk only |
| Modal | Billed until terminated; optional `idle_timeout`; hard 24 h maximum lifetime |
| Runloop | Billed until shut down or suspended; by default nothing happens on idle; suspend/resume is a Pro plan feature |
| Vercel | Memory billed until timeout (default 5 min); CPU not billed while idle |
| Cloudflare | Memory/disk billed until sleep (default 10 min); CPU not billed while idle |
| Sprites | Auto-pauses after ~30 s; paused = storage only |

## 2. Plan fees and concurrency caps

| Provider | Concurrency limit → fee |
| --- | --- |
| Northflank | No concurrency limit, no plan fee |
| E2B | 20 (Hobby, free) → 100 (Pro, $150/mo) → 600 ($650/mo) → 1,100 ($1,150/mo) → Enterprise ($3,000/mo min) |
| Modal | 100 containers (Starter, free) → 5,000 (Team, $250/mo) |
| Vercel | 10 (Hobby) → 10,000 (Pro, $20/mo credited to usage) |
| Daytona | 10 → 100 → 250 → 500 vCPU, unlocked by $25 / $500 / $2,000 top-ups (prepaid credit, not a fee) |
| Cloudflare | 1,500 concurrent vCPU per account on Workers Paid ($5/mo) |
| Runloop | Not published for paid plans; Pro is $250/mo |
| Sprites | Not published for pay-as-you-go; Hero tier ($100/mo) allows 100 running |

## 3. Session length limits

Always-on agents hit these limits first. You can work around them with pause/resume or snapshot-and-restore, but that adds engineering effort and storage costs.

- **Northflank:** no session limit; sandboxes run until you pause or delete them.
- **E2B:** 1 h (Hobby) or 24 h (Pro) of *continuous* runtime. Pausing resets the clock, and Enterprise offers multi-day sessions.
- **Vercel:** 45 min (Hobby) or 24 h (Pro and Enterprise) per session. Stopping and resuming starts a new session.
- **Modal:** 24 h maximum sandbox lifetime. Modal recommends filesystem snapshots for longer work.
- **No published limit:** Daytona, Cloudflare, Sprites. Runloop's lifetime is configurable.

## 4. Forced resource shapes

- **Cloudflare:** at least 3 GiB of memory per vCPU on custom sizes, so a 2 vCPU sandbox is billed for at least 6 GiB.
- **Vercel:** each vCPU includes 2 GB of memory, so you can't buy less.
- **Sprites:** fixed 8 vCPU / 100 GB, billed on usage.
- **Northflank:** fixed plans on Northflank cloud, so 1 vCPU / 2 GiB is billed as the 1 vCPU / 4 GB plan. Custom sizes are available on BYOC.
- **Modal:** CPU is quoted per physical core (2 vCPU), with a 0.125-core minimum.

## 5. Storage and snapshots

| Provider | Persistent storage | Snapshots |
| --- | --- | --- |
| Northflank | Volumes $0.15/GB-mo | Not published |
| E2B | Included (10–20 GiB) | Not published |
| Daytona | First 5 GiB free, then ~$0.08/GiB-mo | Not published |
| Modal | Volumes $0.09/GiB-mo, 1 TiB/mo free | Not published |
| Runloop | ~$0.25/GB-mo devbox disk | ~$0.05/GB-mo |
| Vercel | Drives (beta) $0.05/GB-mo | $0.08/GB-mo, expire after 30 days unused |
| Cloudflare | Disk billed per GB-second while running | Not published |
| Sprites | ~$0.50/GB-mo hot (awake), ~$0.02/GB-mo cold | Count against storage |

## 6. Network egress

| Provider | Egress |
| --- | --- |
| Northflank | $0.06/GB |
| Modal | $0.04/GiB (1 TiB/mo included on Starter) |
| Cloudflare | $0.025/GB NA/EU (1 TB included) |
| Vercel | Included in Pro CDN allowance; $0.15/GB Enterprise |
| Sprites | Not metered today |
| E2B, Daytona, Runloop | Not published |

## 7. Charges outside the sandbox

- **Cloudflare:** Durable Objects (one per sandbox), Workers requests and Workers Logs are billed on top of Containers pricing.
- **Vercel:** $0.60 per million sandbox creations.
- **Runloop:** blueprint (image) builds at $0.252/hour.
- **Regional pricing:** Vercel rates vary by region, and Modal charges 1.15–1.75× for region selection.

## 8. Free credits expire, and some don't cover everything

- **E2B:** one-time $100 credit.
- **Daytona:** $200 credit.
- **Runloop:** $50 trial credit.
- **Sprites:** $30 trial credit.
- **Modal:** $30/mo credit on Starter, or $100/mo on Team.
- **Cloudflare and Vercel:** included usage depends on the plan (see the [provider pages](../providers/)).

Small prototypes may cost nothing for months. Plan your production costs without the credits.
