import { billedSize, hourlyCost, pickTier, workloadCost } from "./model.js";

const MODEL_LABELS = {
  allocated: "Allocated",
  request_or_usage: "max(request, usage)",
  active_cpu: "Active CPU",
  usage: "Usage",
};
const FIELDS = ["count", "concurrency", "duration", "unit", "vcpu", "memory_gib", "disk_gb", "cpu_utilisation"];
const DEFAULTS = { count: 100, concurrency: "", duration: 60, unit: 1, vcpu: 2, memory_gib: 4, disk_gb: 10, cpu_utilisation: 25 };

const $ = (sel) => document.querySelector(sel);
const form = $("#form");

const usd = (x, digits = 2) =>
  x == null ? "n/a" : x.toLocaleString("en-US", { style: "currency", currency: "USD", minimumFractionDigits: digits, maximumFractionDigits: digits });
const num = (x) => Number(x.toPrecision(6)).toLocaleString("en-US");
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

async function loadPricing() {
  // Served at ./data/pricing.json in the container; ../data/pricing.json when serving the repo root locally.
  for (const url of ["data/pricing.json", "../data/pricing.json"]) {
    const res = await fetch(url).catch(() => null);
    if (res && res.ok) return res.json();
  }
  throw new Error("Could not load pricing.json");
}

/** Pick the largest unit that expresses the minutes as a round-ish number. */
function splitMinutes(minutes) {
  for (const unit of [43800, 1440, 60]) {
    if (minutes >= unit && Number.isInteger((minutes / unit) * 4)) return { duration: minutes / unit, unit };
  }
  return { duration: minutes, unit: 1 };
}

function scenarioToState(s) {
  return {
    count: s.count,
    concurrency: s.concurrency ?? "",
    ...splitMinutes(s.minutes),
    vcpu: s.vcpu,
    memory_gib: s.memory_gib,
    disk_gb: s.disk_gb ?? 0,
    cpu_utilisation: Math.round((s.cpu_utilisation ?? 1) * 100),
  };
}

function readState() {
  const fd = new FormData(form);
  return Object.fromEntries(FIELDS.map((k) => [k, fd.get(k)]));
}

function writeState(state) {
  for (const k of FIELDS) form.elements[k].value = state[k];
}

function toWorkload(s) {
  const pos = (v, fallback) => (Number.isFinite(+v) && +v > 0 ? +v : fallback);
  const count = Math.round(pos(s.count, 1));
  const conc = s.concurrency === "" || s.concurrency == null ? null : Math.round(pos(s.concurrency, count));
  return {
    count,
    minutes: pos(s.duration, 1) * pos(s.unit, 1),
    vcpu: pos(s.vcpu, 1),
    memory_gib: pos(s.memory_gib, 1),
    disk_gb: Math.max(0, +s.disk_gb || 0),
    cpu_utilisation: Math.min(100, Math.max(0, +s.cpu_utilisation || 0)) / 100,
    concurrency: conc,
  };
}

function describe(w) {
  const h = w.minutes / 60;
  const runtime =
    w.minutes < 60 ? `${num(w.minutes)} min`
    : h < 48 ? `${num(h)} h`
    : h % 730 === 0 ? `${num(h / 730)} mo (730 h)`
    : `${num(h / 24)} days`;
  return `${w.count.toLocaleString("en-US")} × ${runtime} · ${num(w.vcpu)} vCPU / ${num(w.memory_gib)} GiB · CPU ${Math.round(w.cpu_utilisation * 100)}% busy · ${(w.concurrency || w.count).toLocaleString("en-US")} at once`;
}

function compute(providers, w) {
  return providers
    .map((p) => {
      const size = billedSize(p, w);
      return {
        p,
        hourly: hourlyCost(p, w),
        total: workloadCost(p, w),
        size,
        oversized: size && (size[0] > w.vcpu + 1e-9 || size[1] > w.memory_gib + 1e-9),
        tier: pickTier(p, w),
      };
    })
    .sort((a, b) => (a.total ?? Infinity) - (b.total ?? Infinity));
}

const displayName = (p) => (p.status_notice ? `${p.name} (${p.status_notice.label})` : p.name);

function renderSummary(rows) {
  const priced = rows.filter((r) => r.total != null);
  const el = $("#summary");
  if (!priced.length) {
    el.innerHTML = `<p class="muted">No provider publishes a size this large.</p>`;
    return;
  }
  const [low, high] = [priced[0], priced[priced.length - 1]];
  const mid = priced.length / 2;
  const median = priced.length % 2 ? priced[Math.floor(mid)].total : (priced[mid - 1].total + priced[mid].total) / 2;
  const spread = low.total > 0 ? high.total / low.total : 1;
  const unpriced = rows.length - priced.length;

  el.innerHTML = `
    <div class="stat">
      <span class="stat-label">Lowest compute total</span>
      <span class="stat-value">${usd(low.total)}</span>
      <span class="stat-sub">${esc(low.p.name)} · ${usd(low.hourly, 4)} per sandbox-hour</span>
    </div>
    <div class="stat">
      <span class="stat-label">Median of ${priced.length} providers</span>
      <span class="stat-value muted-value">${usd(median)}</span>
      <span class="stat-sub">Range ${usd(low.total)} – ${usd(high.total)}</span>
    </div>
    <p class="summary-line">The most and least expensive providers differ by <strong>${spread.toFixed(1)}×</strong> for this workload.${
      unpriced ? ` ${unpriced} provider${unpriced > 1 ? "s have" : " has"} no size that fits.` : ""
    } Plan fees, egress and storage can change the order; see the plan column below.</p>`;
}

function renderBars(rows) {
  const max = Math.max(...rows.map((r) => r.total ?? 0)) || 1;
  $("#bars").innerHTML = rows
    .map((r, i) => {
      const pct = r.total == null ? 0 : Math.max(0.6, (r.total / max) * 100);
      const tip = r.total == null ? `${r.p.name}: no size fits` : `${r.p.name}: ${usd(r.total)} total, ${usd(r.hourly, 4)} per sandbox-hour`;
      return `<li class="bar-row${i === 0 && r.total != null ? " is-best" : ""}" title="${esc(tip)}">
        <span class="bar-name">${esc(displayName(r.p))}</span>
        <span class="bar-track"><span class="bar" style="width:${pct}%"></span></span>
        <span class="bar-value">${r.total == null ? "n/a" : usd(r.total)}</span>
      </li>`;
    })
    .join("");
}

function renderTable(rows) {
  $("#table tbody").innerHTML = rows
    .map((r) => {
      const size = r.size ? `${num(r.size[0])} vCPU / ${num(r.size[1])} GiB` : "No size fits";
      const tier = r.tier.warning ? `${esc(r.tier.label)} <span class="warn" title="${esc(r.tier.warning)}">⚠ ${esc(r.tier.warning)}</span>` : esc(r.tier.label);
      return `<tr>
        <th scope="row"><a href="${esc(r.p.pricing_url)}" target="_blank" rel="noopener">${esc(r.p.name)}</a>${r.p.status_notice ? ` <span class="warn" title="${esc(r.p.status_notice.text)}">⚠ ${esc(r.p.status_notice.label)}</span>` : ""}</th>
        <td class="num mono">${r.hourly == null ? "n/a" : usd(r.hourly, 4)}</td>
        <td class="num mono strong">${usd(r.total)}</td>
        <td class="size">${r.oversized ? `<strong>${size}</strong>` : size}</td>
        <td>${MODEL_LABELS[r.p.compute.model] ?? esc(r.p.compute.model)}</td>
        <td class="tier">${tier}</td>
      </tr>`;
    })
    .join("");
}

function syncUrl(state) {
  const params = new URLSearchParams();
  for (const k of FIELDS) if (String(state[k]) !== String(DEFAULTS[k])) params.set(k, state[k]);
  const qs = params.toString();
  history.replaceState(null, "", qs ? `?${qs}` : location.pathname);
}

function stateFromUrl() {
  const params = new URLSearchParams(location.search);
  const s = { ...DEFAULTS };
  for (const k of FIELDS) if (params.has(k)) s[k] = params.get(k);
  return s;
}

function markPreset(scenarios, w) {
  for (const btn of document.querySelectorAll("#presets button")) {
    const s = scenarios.find((x) => x.id === btn.dataset.id);
    const same =
      s &&
      s.count === w.count &&
      Math.abs(s.minutes - w.minutes) < 1e-9 &&
      s.vcpu === w.vcpu &&
      s.memory_gib === w.memory_gib &&
      (s.disk_gb ?? 0) === w.disk_gb &&
      Math.abs((s.cpu_utilisation ?? 1) - w.cpu_utilisation) < 1e-9 &&
      (s.concurrency ?? null) === w.concurrency;
    btn.setAttribute("aria-pressed", same ? "true" : "false");
  }
}

async function main() {
  const data = await loadPricing();
  const { providers, scenarios = [] } = data;

  $("#presets").innerHTML = scenarios
    .map((s) => `<button type="button" class="chip" data-id="${esc(s.id)}" title="${esc(s.description)}">${esc(s.label)}</button>`)
    .join("");
  $("#updated").textContent = `Prices last updated ${data.last_updated}. List prices in ${data.currency}; verify against each provider's pricing page.`;

  const update = () => {
    const state = readState();
    const w = toWorkload(state);
    $("#busy-out").textContent = `${Math.round(w.cpu_utilisation * 100)}%`;
    $("#workload-desc").textContent = describe(w);
    const rows = compute(providers, w);
    renderSummary(rows);
    renderBars(rows);
    renderTable(rows);
    markPreset(scenarios, w);
    syncUrl(state);
  };

  $("#presets").addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-id]");
    if (!btn) return;
    writeState(scenarioToState(scenarios.find((s) => s.id === btn.dataset.id)));
    update();
  });
  form.addEventListener("input", update);
  form.addEventListener("submit", (e) => e.preventDefault());

  $("#copy-link").addEventListener("click", async (e) => {
    const btn = e.currentTarget;
    try {
      await navigator.clipboard.writeText(location.href);
      btn.textContent = "Link copied";
    } catch {
      btn.textContent = "Copy failed";
    }
    setTimeout(() => (btn.textContent = "Copy link to this estimate"), 1600);
  });

  writeState(stateFromUrl());
  update();
}

main().catch((err) => {
  $("#summary").innerHTML = `<p class="warn">Couldn't load pricing data: ${esc(err.message)}</p>`;
});
