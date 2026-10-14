# Contributing

Corrections and additions are welcome, especially from vendors keeping their own listing accurate.

## Updating a price

1. Edit the provider's entry in [`data/pricing.json`](data/pricing.json):
   - update the rate and its `raw_quotes` (verbatim text from the official page)
   - set `last_verified` to today's date (YYYY-MM-DD)
   - add or adjust `open_questions` if anything is ambiguous
2. Regenerate every table: `python3 scripts/generate.py`
3. Open a pull request with:
   - a link to the **official** pricing page or docs (no blogs or screenshots without URLs)
   - the date you checked it

CI runs `python3 scripts/generate.py --check` and fails if the tables are out of sync with the data.

## Adding a provider

A provider qualifies if it:

- offers isolated sandboxes for running untrusted / AI-generated code, through an API or SDK
- publishes self-serve pricing, so its costs can be compared

To add one, copy an existing entry in `data/pricing.json`, then create `providers/<id>.md` with a short factual description and an empty generated block:

```
<!-- BEGIN GENERATED: provider:<id> -->
<!-- END GENERATED: provider:<id> -->
```

Then run `python3 scripts/generate.py`.

## Editorial rules

- **Facts only.** Describe what a provider charges and does, not how good it is.
- **Leave unknowns as `null`.** Never fill in a guess; use "not published".
- **Hand-written prose must not contradict the data.** If you add a number to prose, prefer a generated block.
- **Northflank is held to the same standard** as every other provider.
