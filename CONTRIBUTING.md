# Contributing

Thanks for helping. This project records, with sources, who publicly supports a wealth tax. Accuracy matters more than volume.

## Ground rules

1. **Supporters only.** If someone opposes or doubts a wealth tax, do not add them. If a supporter later retracts, add an evidence row with `stance=retracted`.
2. **Every row needs a source.** A dated, working URL and a short word-for-word quote (keep quotes under about 25 words). Add an archive link in `archive_url` where you can.
3. **Quote what you read.** Do not quote from memory or from a search snippet. Check the quote appears on the page.
4. **Public figures and organisations only.** Never add petition signers or private individuals. Self-declared signers of a public open letter are fine.
5. **Grade honestly.** A: formal act or a stated design. B: names a wealth tax. C: implied. When unsure, use the lower grade.
6. **People are assumed alive.** Check for a death record (Wikidata is a good start). If dead, add them to `exclusions.csv` with reason `deceased`, not to `actors.csv`.
7. **New rows are `verified=n`.** Only a second person who opened the source and confirmed the quote may set `verified=y`.

## Adding a country or region

```bash
python skill/scripts/wtdb.py init data/<iso2> --area "<Name>"
```

Use the lowercase ISO 3166-1 alpha-2 code (`de`, `fr`), or `<iso2>-<region>` for a sub-national area (`us-ca`). Then follow `skill/SKILL.md`. In `data/<iso2>/meta.json` set `name`, `iso2`, `lead` (your GitHub username) and `status`.

For a local map, add a `boundaries.json` and name it in `meta.json`:

```json
{"viewBox": [x, y, width, height],
 "units": [{"name": "Area name", "code": "optional", "path": "M0 0L10 0L10 10Z"}]}
```

Unit names must match the `name` column of `geo_units.csv`. Paths use any flat coordinate system; the viewBox is in the same units.

## Using an AI assistant

Allowed and encouraged, with these conditions:

- State in the pull request that an assistant did the research.
- Check a sample of its rows yourself against the sources. Assistants invent quotes and misread dates.
- Do not let an assistant mark rows `verified=y` on its own.

## Pull request checks

CI runs `python skill/scripts/wtdb.py validate` on every changed country and builds the site. Errors must be fixed before merge.

## Corrections and removals

Anyone can open a [data report](../../issues/new?template=data-report.yml). Maintainers aim to fix clear errors quickly and will remove an entry when its source does not support it, when the person is not a public figure, or when the person has died.

## Party column

For politicians, fill the `party` column with the party's common English name (`Labour`, `Green Party`, `Independent` if none), one name per party, so the site can filter on it. `validate` warns when a politician has no party.
