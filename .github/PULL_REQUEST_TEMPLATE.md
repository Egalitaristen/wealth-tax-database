## What this changes

<!-- Country folder(s) touched, number of actors and evidence rows added or changed. -->

## Checklist

- [ ] `python skill/scripts/wtdb.py validate data/<iso2>` passes
- [ ] Every new row has a dated, working source URL and a short quote I checked on the page
- [ ] Supporters only: no opponents, no petition signers, no private individuals
- [ ] I checked for death records; anyone found dead is in `exclusions.csv`
- [ ] New rows are `verified=n` (only a second person sets `y`)
- [ ] `meta.json` is filled in (`name`, `iso2`, `lead`, `status`)

## AI assistance

- [ ] An AI assistant did some or all of the research, and I checked a sample of its rows against the sources
- [ ] No AI assistance
