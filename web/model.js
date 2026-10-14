// Port of scripts/model.py for the web estimator. Keep the two in sync:
// scripts/check_web_model.py fails CI if they disagree on any provider or workload.

function requestedSize(p, w) {
  const c = p.compute;
  if (c.fixed_sizes && c.fixed_sizes.length) {
    const fits = c.fixed_sizes.filter((s) => s.vcpu >= w.vcpu && s.memory_gib >= w.memory_gib);
    if (!fits.length) return null;
    const price = (s) => s.vcpu * c.cpu_per_vcpu_hour + s.memory_gib * c.memory_per_gib_hour;
    // Python's min() keeps the first of equal elements; reduce with strict < does the same.
    const best = fits.reduce((a, b) => (price(b) < price(a) ? b : a));
    return [best.vcpu, best.memory_gib];
  }
  // Some providers force a minimum memory:vCPU ratio, so you pay for more RAM than you need.
  return [w.vcpu, Math.max(w.memory_gib, w.vcpu * (c.min_memory_gib_per_vcpu || 0))];
}

const tooBig = (vcpu, mem, disk, maxVcpu, maxMem, maxDisk) =>
  (maxVcpu != null && vcpu > maxVcpu) || (maxMem != null && mem > maxMem) || (maxDisk != null && disk > maxDisk);

/** The provider's max_size if the billed size exceeds it, else null. */
function overMax(p, w, size) {
  const m = p.compute.max_size;
  return m && tooBig(size[0], size[1], w.disk_gb, m.vcpu, m.memory_gib, m.disk_gb) ? m : null;
}

export function maxSizeLabel(m) {
  const parts = [];
  if (m.vcpu != null) parts.push(`${fmtG(m.vcpu)} vCPU`);
  if (m.memory_gib != null) parts.push(`${fmtG(m.memory_gib)} GiB`);
  if (m.disk_gb != null) parts.push(`${fmtG(m.disk_gb)} GB disk`);
  return parts.join(" / ");
}

export function billedSize(p, w) {
  const size = requestedSize(p, w);
  if (!size) return null;
  const m = overMax(p, w, size);
  return m && m.hard ? null : size;
}

export function hourlyCost(p, w) {
  const c = p.compute;
  if (c.cpu_per_vcpu_hour == null || c.memory_per_gib_hour == null) return null;
  const size = billedSize(p, w);
  if (!size) return null;
  let [vcpu, mem] = size;
  if (c.model === "active_cpu" || c.model === "usage") vcpu *= w.cpu_utilisation;
  const disk = Math.max(0, w.disk_gb - (c.disk_free_gb || 0));
  return vcpu * c.cpu_per_vcpu_hour + mem * c.memory_per_gib_hour + disk * (c.disk_per_gb_hour || 0);
}

export function workloadCost(p, w) {
  const perHour = hourlyCost(p, w);
  if (perHour == null) return null;
  const minSeconds = p.billing.minimum_billed_seconds || 0;
  const hours = Math.max(w.minutes / 60, minSeconds / 3600);
  return w.count * (hours * perHour + (p.compute.per_sandbox_fee || 0));
}

const limit = (v) => (v == null || v === "unlimited" ? null : v);

// Same strings as Python's f"{x:g}" / f"{x:,}" for the values that appear in plan data.
const fmtG = (x) => String(Number(x.toPrecision(6)));
const fmtThousands = (x) => x.toLocaleString("en-US");

/** Cheapest published plan whose sandbox size, concurrency and session limits fit the workload. */
export function pickTier(p, w) {
  const concurrency = w.concurrency || w.count;
  const sessionHours = w.minutes / 60;
  // Array.prototype.sort is stable, like Python's sorted().
  const tiers = [...p.plans.tiers].sort((a, b) => a.monthly_fee - b.monthly_fee);

  const fitsConcurrency = (t) => {
    const maxSbx = limit(t.max_concurrent_sandboxes);
    const maxVcpu = limit(t.max_concurrent_vcpu);
    if (maxSbx != null && concurrency > maxSbx) return false;
    if (maxVcpu != null && concurrency * w.vcpu > maxVcpu) return false;
    return true;
  };
  const label = (t) =>
    `${t.name} (${t.monthly_fee === 0 ? "no plan fee" : `$${fmtThousands(t.monthly_fee)}/mo`})`;

  const size = billedSize(p, w);
  if (!size) return { label: "n/a", fee: null, warning: null };
  // Only a default (raisable) maximum can be exceeded here; above a hard one there is no size.
  const over = overMax(p, w, size);
  const sizeNote = over ? `above the default max per sandbox (${maxSizeLabel(over)}); ask to raise it` : null;
  const warn = (note) => [note, sizeNote].filter(Boolean).join("; ") || null;
  const fitsSize = (t) =>
    !tooBig(size[0], size[1], w.disk_gb, t.max_sandbox_vcpu, t.max_sandbox_memory_gib, t.max_sandbox_disk_gb);

  const candidates = tiers.filter((t) => fitsConcurrency(t) && fitsSize(t));
  if (!candidates.length) return { label: p.plans.custom_tier || "Contact sales", fee: null, warning: warn(null) };

  const fully = candidates.filter((t) => limit(t.max_session_hours) == null || sessionHours <= t.max_session_hours);
  if (fully.length) {
    const t = fully[0];
    const warning = warn(p.platform.limits_published === false ? "limits not published" : null);
    return { label: label(t), fee: t.monthly_fee, warning };
  }
  // Nothing fits the session length: take the longest-session plan (cheapest on ties).
  const t = candidates.reduce((a, b) => {
    const ka = [-(limit(a.max_session_hours) || 0), a.monthly_fee];
    const kb = [-(limit(b.max_session_hours) || 0), b.monthly_fee];
    return kb[0] < ka[0] || (kb[0] === ka[0] && kb[1] < ka[1]) ? b : a;
  });
  return {
    label: label(t),
    fee: t.monthly_fee,
    warning: warn(`max session ${fmtG(t.max_session_hours)} h; restart or ${p.plans.custom_tier ?? "contact sales"}`),
  };
}

/** The string scripts/estimate.py prints in its "plan that fits" column. */
export function pickTierText(p, w) {
  const t = pickTier(p, w);
  if (!t.warning) return t.label;
  return `${t.label} ⚠ ${t.warning}`;
}
