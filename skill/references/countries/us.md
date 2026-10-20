# United States: a federal system, with ballot measures

A second worked example, next to the UK, at **Standard** depth: national and state level in full, local levels recorded when met but not swept. It is closer to what most countries need. It shows what changes in a federal country with many small, uneven layers. Check every URL still works before relying on it.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | US Congress; the federal executive and agencies | Bills, cosponsors and roll calls |
| region | The 50 states and DC | Name each unit like `Alabama (state legislature and state government)` so the boundary file can match on `Alabama` |
| local | 3,143 counties and equivalents (parishes, boroughs, census areas, independent cities) | The map tier. Named as the Census names them (`Ventura County`) with the 5-digit FIPS code in `code`. Cities stay as place text below their county: `United States > California > Ventura County > Camarillo` |

The register is loaded down to the counties (SKILL.md 6.7), but local sweeping stays proportionate: the first runs searched national and state level, and the counties stay `pending` until a sample shows they pay.

**Counties and places:** the county list with codes is the Census gazetteer (`2020_Gaz_counties_national`). To place a mayor or councillor, look the city up in the Census place-to-county table (`national_place_by_county2020.txt`) and use the county when the city lies in one county only; prefer the incorporated city when an unincorporated place shares its name. Congressional districts cross county lines, so a representative stays at state level with the district (`CA-47`) as place text.

**Map:** `data/us/boundaries.json` comes from the `us-atlas` package (Census cartographic boundaries, already projected, with Alaska and Hawaii as insets): counties as units and states as region outlines.

```bash
python skill/scripts/topo_to_boundaries.py counties-albers-10m.json --object counties --code-prop id \
  --scale 4 --simplify 0.8 --source "US Census cartographic boundaries via us-atlas" --out counties.json
python skill/scripts/topo_to_boundaries.py states-albers-10m.json --object states --code-prop id \
  --scale 4 --simplify 1.5 --out states.json
# then put the units of states.json into counties.json as "regions"
```

us-atlas predates Alaska's 2019 split of Valdez-Cordova, so the register keeps Valdez-Cordova Census Area (02261) as one unit to match the map.

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
