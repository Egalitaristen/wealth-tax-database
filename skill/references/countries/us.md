# United States: a federal system, with ballot measures

A second worked example, next to the UK. It shows what changes in a federal country with many small, uneven layers. Check every URL still works before relying on it.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | US Congress; the federal executive and agencies | Bills, cosponsors and roll calls |
| region | The 50 states and DC | Name each unit like `Alabama (state legislature and state government)` so the boundary file can match on `Alabama` |
| local | Counties, cities, school boards | Out of scope in the first run. Actors found here (a mayor, a city council, a county party) are still recorded, with `level=local` and a `location` such as `United States > California > Camarillo`; the city stays as place text until that layer is loaded |

The first run chose **national plus state level** and said so in `meta.json` and the area profile. That is a good pattern: pick a depth, write it down, and load only that depth into `geo_units.csv`.

**Map:** `data/us/boundaries.json` comes from the `us-atlas` package (`states-albers-10m.json`), which is already projected and has Alaska and Hawaii as insets:

```bash
python skill/scripts/topo_to_boundaries.py states-albers-10m.json --object states --name-prop name \
  --code-prop id --source "US Census cartographic boundaries via us-atlas" --out data/us/boundaries.json
```

## What was in scope

- **Counts:** the Ultra-Millionaire Tax Act (2% over $50m, 1% over $1bn), state net-worth bills, California's one-time 5% billionaire tax ballot measure (Prop 40), and Senator Wyden's Billionaires Income Tax (`unrealised_gains`).
- **Does not count:** millionaires' surtaxes and other income-tax changes (Massachusetts, Maine, Rhode Island), "wealth proceeds" taxes on investment income, and "tax the wealthy" statements with no reference to wealth.

## Sources that worked

- **Congress:** official bill-status data (govinfo bulk `BILLSTATUS`) lists every sponsor and cosponsor with a standard name field, which makes a clean quote and a grade A (formal act). Congress.gov pages give the same.
- **State bills:** each legislature's own bill page (for example the Washington, New York, Illinois and Minnesota sites). Sponsors and cosponsors are grade A.
- **Ballot measure campaigns:** the campaign's endorsement page. Its structured data (JSON-LD) carries one claim sentence per endorser. Because the campaign made the claim, grade B; upgrade when the endorser's own statement is found.
- **Coalition letters:** sign-on letters from national groups (for example Americans for Tax Fairness) listing national, state and local organisations. They filled the states that had no other record. Treat each signing organisation as grade A for the design the letter names, and name the design.
- **Economists:** open letters (for example Nobel laureates' letters), then each signer's own page. A long list of academics returned few statements about wealth taxes specifically; the layer is thin in the US.
- **Candidates:** campaign pages and platforms for 2026 candidates, read directly.
- **Finding names:** Wikipedia's endorsement list is useful for discovering names. Re-read each name at its cited page and never use Wikipedia as the source.

## Checks that mattered

- Check the living: three cosponsors had died (recorded in `exclusions.csv`).
- Pages that fetch tools summarise can be paraphrased; the run fetched raw pages to check quotes. Run `wtdb.py checkquotes` to automate it.
- Parties: use `Democratic Party` for state branches such as Minnesota's DFL.
- Names that look alike are often different bodies (a national group and its chapter). Merge only true duplicates.
