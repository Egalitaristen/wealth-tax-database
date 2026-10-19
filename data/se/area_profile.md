# Area profile — Sweden

First written 2026-10-19 (run R001). Lines marked *(to source)* were not yet checked against a page and must be sourced or removed in R002.

## 1. Scope
- Area: Sweden; type: country.
- Levels of government in scope: national (Riksdag, government), European Parliament (Swedish MEPs), regional (21 län / regions, regionfullmäktige) and local (290 kommuner, kommunfullmäktige). Below municipal level (kommundelsnämnder, church parishes) is out of scope.
- Languages to search in: Swedish (main), English. Minority languages (Sami, Finnish, Meänkieli, Romani, Yiddish) only for the Sami parliament and a few northern municipalities, and only if a hit suggests it.
- Date of first run: 2026-10-19.

## 2. Wealth tax history and live proposals (2010 onwards)
- The national wealth tax (*förmögenhetsskatt*) was abolished with effect from 1 January 2007, and the wealth declaration went with it. Sources: Riksdag motion [2017/18:2962](https://data.riksdagen.se/dokument/H5022962.html) ("avskaffad i Sverige sedan den 1 januari 2007"); motion [2021/22:2597](https://data.riksdagen.se/dokument/H9022597.html) (the declaration disappeared). Inheritance and gift tax went in 2004–05 and the state property tax in 2008 *(to source)*.
- Since 2010 the question has been raised in the Riksdag mainly through motions, not bills. A search of the Riksdag open data for motions from 2010-01-01 containing *förmögenhetsskatt* or *miljardärsskatt* gives 82 motions (query and list in `harvest.csv` H0001). Most are by opponents or only mention the abolished tax.
- Supporters in the Riksdag since 2010: Vänsterpartiet (annual calls for a study from 2011, a costed design from 2019), Miljöpartiet (motions 2013, 2016, 2017, and in 2026 a "miljardärsskatt"), the independent MP Amineh Kakabaveh (2020, 2021). The Social Democrats have been cautious: a 2020 motion by one MP asks for a review of "en ny förmögenhetsskatt"; the party leader rejected a billionaire tax in 2026 *(to source; not recorded: opponents are out of scope)*.
- Live proposals 2026: V wants an inquiry into a "särskild miljardärsskatt"; MP wants a billionaire tax on a Zucman model (2% on wealth over 100 million euro) ([TV4, 2026-05-18](https://www.tv4.se/artikel/45KWAtSv8KaMNZnITwLqXf/mp-och-v-kraever-miljardaerskatt-men-sagas-av-expert)). Oxfam Sverige proposes a wealth tax of 2%, 3% and 5% in three brackets ([Oxfam Sverige, Feb 2026](https://oxfam.se/wp-content/uploads/2026/02/Vart-Ojamlika-Sverige-Utsatthet-och-Extrem-Formogenhet.pdf)).
- Government and election: the Tidö government (M, KD, L with SD support) opposed new wealth taxes: M and SD motions praise the abolition and Moderate MPs attack the "miljardärsskatt" in the chamber (e.g. Lotta Björklund, 2026-10-15, [protocol 2026/27:8](https://data.riksdagen.se/dokument/HE098.html)). The general election was held on 13 September 2026. According to [Swedish Wikipedia's article on the election](https://sv.wikipedia.org/wiki/Riksdagsvalet_i_Sverige_2026) (secondary source, read 2026-10-19), the red-green side won: S 28.0% (99 seats), V 8.4% (30), C 7.0% (25), MP 6.1% (22) against M 19.9% (70), SD 17.5% (62), KD 6.2% (22), L 5.3% (19). Kristersson resigned on 17 September; as of 13 October 2026 the government formation had stalled (S, V and MP all demand to be in government; C refuses V). The outcome decides whether the V and MP billionaire-tax inquiry demands reach negotiations. R003 should re-check.
- S position: the Social Democrats have rejected a wealth tax in the chamber throughout (see `exclusions.csv` X0008). The line is "skatten på kapital behöver öka" without a wealth tax. One S MP, Joakim Järrebring, asked in a 2020 motion for a review of "en ny förmögenhetsskatt" (grade C). In 2010 the S-MP-V election motion proposed only a study of taxing the wealthy more.
- MP position: MP's economic spokesperson said on 2011-04-13 that the party would not pursue a wealth tax (X0007). MP MPs Lillemets and Mutt nevertheless moved to reintroduce it in 2013, 2016 and 2017, and the party's spring 2026 motion (section 6.5) asks for "en ny skatt för miljardärer" on a Zucman model.
- V position: V has asked for a wealth tax in every year of the window, first as a study (2011-2013), then with a costed design in budget motions 2019-2021 (SEK 6m threshold, 1-5%), and in 2026 as an inquiry into a billionaire tax. V's chamber speeches 2016-2017 also say "Vi vill återinföra förmögenhetsskatten".
- Reports and commissions: Katalys no. 75 "Beskatta kapitalet!" (Per Sundgren, 2019) *(to open and source)*. Konjunkturinstitutet's comparison of Swedish taxes for SNS (2019) is cited by V motions; it does not argue for a tax.
- Main moments: the 2010 election (S/MP/V joint "study a tax on the wealthy" line), the 2012–13 V budget motions, the Januari agreement 2019, the 2026 election campaign and Zucman's visit to Stockholm University (Realtid, 2026-04-01).

## 3. Legislatures and where their records are
- **Riksdag.** Motions, bills, votes and debates are in the open data API: `https://data.riksdagen.se/dokumentlista/?sok=<term>&doktyp=mot&from=2010-01-01&utformat=json`. Full text: `https://data.riksdagen.se/dokument/<dok_id>.text` (XML with the text inside; unescape it). Signatories: `https://data.riksdagen.se/dokumentstatus/<dok_id>.json`, `dokintressent`. Votes: `https://data.riksdagen.se/voteringlista/`. Search works well; the API returns every motion containing the term.
- **European Parliament.** Swedish MEPs' motions and votes via the European Parliament's open data portal *(to source)*.
- **Regionfullmäktige and kommunfullmäktige.** Minutes (protokoll) and motions are published on each municipality's or region's own site, often on the platforms Platsen, Ciceron/Open ePlatform, Meetings+ or "Insyn" *(to source and map in R003)*.

## 4. Parties
- Riksdag parties 2022–2026: V, S, MP, C, L, KD, M, SD. Party names to use in the `party` column (English common name): `Left Party`, `Social Democrats`, `Green Party`, `Centre Party`, `Liberals`, `Christian Democrats`, `Moderates`, `Sweden Democrats`, `Independent`.
- Manifestos since 2010 (V, MP, S, C) *(to collect in R002)*.

## 5. Government below national level
- 21 län, each with a regionfullmäktige (health care and regional development) and a state county administrative board (länsstyrelse); 290 kommuner, each with a kommunfullmäktige. Official list: SCB's region code list, loaded in `geo_units.csv` (21 + 290 units + 3 national/supranational). Source for the list: SCB table BE0101A (variable *Region*, retrieved 2026-10-19 via `api.scb.se`).
- Taxation: municipalities and regions levy only a proportional income tax and cannot introduce a wealth tax *(to source)*. Local actors therefore call on the Riksdag or government, and many local motions will be statements to the state, not decisions.
- Boundaries for the municipality map: [okfse/sweden-geojson](https://github.com/okfse/sweden-geojson) (municipalities, derived by that project from Valmyndigheten's boundaries via Opendatasoft), simplified further here.
- Municipal minutes: see section 3.

## 6. Search terms
| Term | Note |
|---|---|
| förmögenhetsskatt | The wealth tax; also used for the abolished 1947–2006 tax |
| miljardärsskatt, miljardärskatt, skatt på miljardärer | Billionaire taxes; both spellings occur |
| förmögenhetsbeskattning, skatt på förmögenhet, skatt på stora förmögenheter | |
| superrika, extrem förmögenhet, "betala på sin förmögenhet" | Context only; check the person's own words |
| exitskatt, utflyttningsskatt | Exit tax |
| förmögenhetsregister, förmögenhetsdeklaration | A register or declaration is **not** a tax on its own; record as `out_of_definition` unless a tax is also proposed |
| arvsskatt, gåvoskatt, fastighetsskatt, kapitalskatter | **Excluded** taxes, check that a wealth tax is also named |
| Zucmanskatt, Zucman | Billionaire minimum tax (2% above 100 million euro) |
- Ambiguous: *kapitalskatt*, *skatt på kapital* (income from capital); *fastighetsavgift* (municipal property fee); *värnskatt* (income tax surtax, abolished 2020).

## 7. Media
- National: Dagens Nyheter, Svenska Dagbladet, Aftonbladet, Expressen, Dagens Industri, Dagens Arbete, Dagens ETC, Arbetet, Flamman, Syre, Realtid, Affärsvärlden, Dagens PS, Ordfront, Tidningen Kontakt; SVT, Sveriges Radio, TV4. Regional press: local editions of NTM, Mittmedia/Bonnier, Gota Media *(to map in R003)*.
- Opinion-column writers and economists known to write on tax: to be collected in R002.

## 8. Registers
- Lobbying: none in Sweden *(to source)*. Charities: Bolagsverket and Svensk Insamlingskontroll *(to source)*. Party funding: Kammarkollegiet's party-support register *(to source)*.

## 9. Known networks
- Oxfam Sverige (recorded), Arena Idé (recorded, with Elinor Odeberg), SSU and S-studenter (recorded as youth wings, against the party line), LO (press report only), Tankesmedjan Katalys (neutral in its 2019 report; excluded for now), Tankesmedjan Tiden (opposes a new wealth tax in its 2020 report), Fair Finance, Attac Sverige, Diakonia, Forum Syd/Concord Sverige, Kristna Fredsrörelsen, trade unions (LO and its unions, TCO, Saco), Tax Justice Network and Patriotic Millionaires contacts, "Skattejusterarna". All to be checked in R002/R003.

## 10. Notes for future runs
- Pre-2010 motions (e.g. 2009/10:Sk342 by Ameer Sachet) are before the time window; the API's `from=2010-01-01` filter excludes 2009/10 motions submitted in autumn 2009.
- The Riksdag free-text search matches whole words only; also search stems and compounds (*förmögenhetsbeskattning*, *förmögenhetsskatten*, *miljardärer*, *superrika*).
- Wikidata's API rate-limits this environment's address hard; `Special:EntityData/<QID>.json` still worked, and the QID can be read from an article page's `wgWikibaseItemId`. The Riksdag person register (`data.riksdagen.se/personlista/`) flags deceased members as `Avliden`, which serves as the death check for MPs.
- Motions are quoted from `data.riksdagen.se/dokument/<id>.html`. The page splits some words with a soft hyphen, so choose quote spans that avoid a hyphenated word.

## 11. Run plan

Status after R001 (2026-10-19): 35 actors, 58 evidence rows, all `verified=n`. National Riksdag motions read; all 314 geography units pending except the Riksdag (in progress). Order follows the skill's priorities: bulk lists, then geography, then thin layers, then upgrades.

| Run | Focus | Targets and method | Done when |
|---|---|---|---|
| **R002** (done 2026-10-19, part 1) | National politics | Built `skill/scripts/riksdag_scan.py`. Reran the motion search, read interpellations, questions, committee reports and 196 plenary protocols; added the 2026 MP motion, 11 chamber speeches and 19 actors. Still open: H0002 roll calls (reservations in SkU reports), the 2026/27 motions, EP, and party documents (vansterpartiet.se blocks curl; use a browser) | Riksdag unit `done`; party rows backed by their own documents |
| **R003** (done 2026-10-19, part 1) | Civil society and unions | Added Arena Idé, SSU, S-studenter, LO (press report), Elfva Barrio, a second Oxfam source, and Odeberg's own words; Tankesmedjan Tiden, Katalys and an old LO report went to exclusions. Web search returned nothing for Attac, Diakonia, Fair Finance, ForumCiv, Kristna fredsrörelsen, Greenpeace, Ung Vänster, Grön Ungdom, TCO, Saco or any union congress: those need their own sites read with a browser | Every network in section 9 checked on its own site |
| **R003b** (done 2026-10-19) | Organisation and party sites | Read mp.se (MP billionaire-tax page, Helldén's Almedalen speech), ungvanster.se, gronungdom.se, feministerna.se, socialisterna.org. Added Ung Vänster, Grön Ungdom, Feministiskt initiativ and upgraded MP to grade A. **Blocked**: vansterpartiet.se (403 for all clients) and attac.se, fairfinance.se, kristnafredsrorelsen.se, rattvisepartiet.se (no connection); no results for the union and NGO sites searched | V manifesto 2026 and K26 motion answer obtained by a person with a browser |
| **R004** (done 2026-10-19, thin) | Economists, academics, journalists, public figures | Added Kolsrud, Landais and a second Zucman source from the 2026-10-01 DN Debatt article (read via EFN). Johansson-Stenman, Östros and the opposing economists and business leaders went to exclusions. No journalist, wealthy individual or faith voice could be sourced from what the search engine indexes; DN, SvD, Aftonbladet and Dagens Arena opinion pages need a browser or the originals supplied | Coverage grid has no empty row for a type that has evidence |
| **R005** | Local sweep: Stockholm region | Stockholms län (region plus 26 municipalities), Uppsala (8), Södermanland (9), Gotland (1) = 44 units + 4 regions. For each unit: search the council's minutes and motions page, local news, and V/MP/S local groups; register hits or `hits=0`; start with the largest municipalities | All 44 units `done` |
| **R006** | Local sweep: Västra Götaland | Region plus 49 municipalities (Göteborg, Borås, Trollhättan, Skövde first) | 49 `done` |
| **R007** | Local sweep: South | Skåne (33), Blekinge (5), Halland (6), Kronoberg (8) = 52 | all `done` |
| **R008** | Local sweep: Southeast and Bergslagen | Östergötland (13), Jönköping (13), Kalmar (12), Örebro (12), Västmanland (10) = 60 | all `done` |
| **R009** | Local sweep: Mid | Dalarna (15), Värmland (16), Gävleborg (10), Västernorrland (7) = 48 | all `done` |
| **R010** | Local sweep: North | Jämtland (8), Västerbotten (15), Norrbotten (14) = 37 | all `done` |
| **R011** | QA and upgrades | Run `validate`, `dedupe`, `checkquotes` on all rows; a second person (or a separate agent that did not write the rows) opens sources and sets `verified`; upgrade C and B actors; check retractions; resolve the municipality-map licence; add MP constituencies to `location` once a constituency layer exists; update `meta.json` status | No `verified=n` rows left in A-grade evidence; saturation reported |

Tooling: the Riksdag adapter `skill/scripts/riksdag_scan.py` exists (motions, other document types, plenary protocols, votes, member register). For the local sweep, most municipalities publish minutes on a few platforms; check which, then write one adapter per platform instead of searching by hand.

Update sweeps after completion: re-run H0001 each autumn (budget motions, October) and each spring (spring bill motions, April-May).
