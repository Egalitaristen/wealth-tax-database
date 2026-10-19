# Sweden: a unitary state with strong municipalities

A third worked example. It shows a country whose national records are open data, whose wealth tax was abolished before the time window, and where all local power sits in 21 regions (län) and 290 municipalities (kommuner). Check every URL still works before relying on it.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Riksdag; the government (Regeringen) | Motions, votes and speeches are open data |
| supranational | Swedish members of the European Parliament | Listed as a unit; MEPs are located at the country |
| region | 21 län (each with a regionfullmäktige) | Named by SCB's official names, for example `Stockholms län`. Regions run health care and regional development |
| council | 290 kommuner (each with a kommunfullmäktige) | Named plainly (`Stockholm`, `Gotland`); the county of the same place has `län` in its name, so names stay unique |

The official list is SCB's region code table (`api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101A/BefolkningNy`, variable `Region`): a two-digit code is a county, a four-digit code a municipality whose first two digits are its county.

**Map:** `data/se/boundaries.json` is a municipality map built from the okfse/sweden-geojson file (290 shapes), simplified with a Douglas-Peucker pass and drawn from longitude/latitude with a mid-latitude correction. The shape licence still has to be confirmed.

## Where the national record is

Use `skill/scripts/riksdag_scan.py` (stdlib only): `search` for documents and context, `speeches` for plenary debates, `votes`, `signers`, `member`. The raw API calls it wraps:

The Riksdag open data API is the best bulk source in any of the three countries so far:

```bash
# all motions since 2010 containing a term
curl 'https://data.riksdagen.se/dokumentlista/?sok=f%C3%B6rm%C3%B6genhetsskatt&doktyp=mot&from=2010-01-01&utformat=json&sz=200&p=1'
# full text (XML with the text inside, unescape it) and signatories
curl 'https://data.riksdagen.se/dokument/<dok_id>.text'
curl 'https://data.riksdagen.se/dokumentstatus/<dok_id>.json'    # dokintressent = signatories
# the member register, with deceased members marked "Avliden"
curl 'https://data.riksdagen.se/personlista/?utformat=json&rdlstatus=samtliga&sz=2000'
```

Other `doktyp` values worth the same search: `ip` (interpellation), `fr` (written question), `bet` (committee report), and speeches via `anforandelista`. Votes are in `voteringlista`.

## What worked and what to watch

- Read each hit in context. Of 82 motions that contain the word, only 11 call for a wealth tax. Most are opposition-bloc motions describing the abolished tax, or governing-party motions praising its abolition.
- Budget motions of the Left Party are the strongest source: they contain a costed design (threshold, rates, revenue, start date). The signatories listed in `dokintressent` are co-signatories of that proposal; record each with a `motion_signature` row quoting the proposal sentence.
- *Förmögenhetsregister* (a register of wealth) and *förmögenhetsdeklaration* are about information, not a tax. Record the motion in `exclusions.csv` as `out_of_definition`.
- The Wikidata API rate-limits shared addresses; `Special:EntityData/<QID>.json` still works.
- The speech-list API (`anforandelista`) ignores `sok` and `p`; plenary debates are found by searching `doktyp=prot` (full text) and attributing each hit to the nearest preceding `Anf. N Name (Party)`, which is what `riksdag_scan.py speeches` does.
- The member register also gives each member's constituency (`valkrets`) and flags deceased members (`Avliden`).
- Chamber speeches are the best source for individual V and MP members; quote one sentence of the speech and cite the protocol page with the speech number.
- Party websites (vansterpartiet.se) return 403 to plain HTTP clients; use a browser for party documents.
