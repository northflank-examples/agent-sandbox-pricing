// Reads {providers, workloads} JSON on stdin and prints the JS model's results as JSON.
// Driven by scripts/check_web_model.py; not shipped to the browser.
import { hourlyCost, workloadCost, pickTierText } from "./model.js";

let input = "";
for await (const chunk of process.stdin) input += chunk;
const { providers, workloads } = JSON.parse(input);
const out = workloads.map((w) =>
  providers.map((p) => ({ hourly: hourlyCost(p, w), total: workloadCost(p, w), tier: pickTierText(p, w) })),
);
process.stdout.write(JSON.stringify(out));
