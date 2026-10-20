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

**Map:** `data/se/boundaries.json` uses Statistics Sweden's (SCB) digital boundaries for thematic maps (CC0, "Källa: SCB"): the 290 kommuner as units and the 21 län as region outlines, both in SWEREF 99 TM. The kommunkod and länskod are in `geo_units.csv` `code`. The files are on SCB's page "Digitala gränser" (the shapefile zip); their text is Latin-1:

```bash
python skill/scripts/topo_to_boundaries.py Kommun_Sweref99TM.shp --name-prop KnNamn --code-prop KnKod --encoding latin-1 \
  --scale 0.002 --flip-y --simplify 0.8 --source "SCB, CC0" --out kommuner.json
python skill/scripts/topo_to_boundaries.py Lan_Sweref99TM_region.shp --name-prop LnNamn --code-prop LnKod --encoding latin-1 \
  --scale 0.002 --flip-y --simplify 1.2 --out lan.json   # then put lan.json's units into "regions"
```

## Where the national record is

Use `skill/scripts/adapters/se_riksdag_scan.py` (stdlib only): `search` for documents and context, `speeches` for plenary debates, `votes`, `signers`, `member`. The raw API calls it wraps:

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
- Web search: use `allowed_domains` per outlet group instead of one broad query. DN, SvD, Aftonbladet and Expressen are rejected by the search tool (crawler-blocked), but Dagens Arena, Arbetet, Flamman, mp.se, arenaide.se and most think-tank sites work. `blocked_domains` removes the same recycled EFN/Realtid/Dagens PS pages.

## Municipal and regional portals (local sweep)

- **MeetingPlus** (Formpipe): `<base>/search?text=<word>*&psize=100&pindex=1`, server-rendered, searches agenda items and attached documents, whole-word so use the trailing `*`. Used by Stockholm (meetingspublic.stockholm.se), Huddinge (sammantraden.huddinge.se), Danderyd (meetingsplus.danderyd.se) and Region Gotland (sammantraden.gotland.se). Adapter: `skill/scripts/adapters/se_meetingplus_scan.py`.
- **Nacka** has its own protocol search: `https://www.nacka.se/sok?q=<word>*`, documents under `handlingar.nacka.se`.
- Most others publish protocols as PDF links on Sitevision pages (Botkyrka, Solna, Täby, Vallentuna, Katrineholm, Oxelösund ...). Their site search often covers pages only (Solna, Järfälla, Tyresö, Haninge, Södertälje, Uppsala return nothing for the word) so it does not prove absence. Search-engine queries limited to a municipality's domain return unrelated protocols.
- A hit in an attachment (SOU, PM, report) is a mention. The useful hits are reservations, motions, interpellations and debate protocols by named councillors.
- Local actors are placed at the municipality: `location = Sweden > Stockholms län > Stockholm`.

## Tooling that changed what was reachable

- `vansterpartiet.se` and its PDFs return 403 to curl, WebFetch and Playwright's request API, but `skill/scripts/fetch_page.py` (headless Chromium, file fetched with `fetch()` from inside the site's own page) reads them: the election manifesto 2026, the congress motion book and the board's answers.
- DN Debatt articles can be read in full the same way (no login needed for the ones tried); DN, SvD, Aftonbladet and Expressen are still rejected by the web-search tool, so the search itself must be run on the site: `fetch_page.py "<site search URL>" --consent --wait 5000`. Mind the spelling of search words (an encoded typo returns "0 hits" that looks like a result).
- `wtdb.py checkquotes` now reads PDFs (pdftotext, with line-end hyphens joined) and retries in the browser when a page differs for plain clients.
- Network limits remain: attac.se, fairfinance.se, kristnafredsrorelsen.se and rattvisepartiet.se are unreachable from this environment even with a browser.
