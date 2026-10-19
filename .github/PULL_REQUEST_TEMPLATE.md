## What this changes

<!-- Country folder(s) touched, number of actors and evidence rows added or changed. -->

## Checklist

- [ ] `python skill/scripts/wtdb.py validate data/<iso2>` passes
- [ ] Every new row has a dated, working source URL and a short quote from the page itself (not a paraphrase)
- [ ] I ran `wtdb.py checkquotes` on the new rows and looked at anything it could not fetch
- [ ] I ran `wtdb.py dedupe` and merged true duplicates
- [ ] Supporters only: no opponents, no petition signers, no private individuals
- [ ] I checked for death records; anyone found dead is in `exclusions.csv`
- [ ] New rows are `verified=n` (only a second person sets `y`)
- [ ] `meta.json` is filled in (`name`, `iso2`, `lead`, `status`)

## AI assistance

- [ ] An AI assistant did some or all of the research, and I checked a sample of its rows against the sources
- [ ] No AI assistance
