---
name: wealth-tax-database
description: Systematically build or extend a sourced database of people, organisations and institutions in a country, region or supranational area that support (or appear to support) actual wealth taxation since 2010, down to local-government level. Use when asked to map, find, update or export wealth tax supporters for any area.
---

# Wealth Tax Database

Build a comprehensive, verifiable overview of everyone in an area who supports — or appears to support — **actual wealth taxation**: politicians who voted for or sponsored it, academics who argued for it, journalists who advocate it, organisations campaigning for it, councils that passed motions for it, and so on.

This is a database, not a ranking. Every entry rests on dated, sourced, quoted evidence. The work is done in repeatable **runs**; each run reads the current state from disk, works the biggest gaps, writes results as it goes, and logs what it did, so any assistant in any session can pick up where the last one stopped.

Files in this skill (use them if present; the rules in this file are sufficient on their own):
- `references/source-playbook.md` — layers, bulk-list sources, query templates, search terms in many languages
- `references/area-profile-template.md` — what to establish about an area before searching
- `references/countries/gb.md` — UK levels of government, sources, and the local sweep list (worked example for other countries)
- `references/countries/us.md` — a federal system (states, ballot measures, coalition letters), and what worked there
- `scripts/wtdb.py` — Python helper (stdlib; `openpyxl` only for xlsx export): `init`, `add`, `set`, `validate`, `dedupe`, `merge`, `checkquotes`, `status`, `export`
- `scripts/profiles_wikidata.py` — fills `profiles.csv` (websites, socials, Wikipedia) from Wikidata IDs
- `scripts/topo_to_boundaries.py` — turns a TopoJSON of areas into `boundaries.json`, so the country gets a local map on the site
- `scripts/ocn_scan.py` — UK-only council meeting scanner (an example of a per-country source adapter)

---

## 1. Ground rules

1. **Apply the definition (section 2) to every piece of evidence.** Support for a mansion tax, capital gains reform or inheritance tax is not support for wealth taxation.
2. **No source, no row.** Every claim is an evidence row with a URL you actually opened and a **verbatim** quote found on that page. Never add an actor or evidence from memory or from a search-result snippet alone.
   - Fetch tools that return a summary can paraphrase. Quote from the raw page text (download it, or use a browser) and run `wtdb.py checkquotes` on the rows you add.
   - Never compose a sentence of your own and put it in `quote_original`. For list or roster pages where the only text is a name, use the text the page itself prints for that entry: a claim sentence in the page's structured data (JSON-LD), an official bill-status field such as `Rep. Lee, Barbara [D-CA-13]`, or the name and role as listed. Keep quotes short (about 25 words or fewer).
3. **Time window and the living.** Only evidence dated 2010-01-01 or later counts. Individuals are assumed alive unless a death record is found. Check before adding (Wikidata's date of death, or an obituary search when in doubt); anyone found dead goes in `exclusions.csv` (`deceased`), not in `actors.csv`. Record the check by setting `alive_checked=y`; do not narrate it in `notes`. Dissolved organisations may stay, marked `dissolved`.
4. **Supporters only.** Opponents are not recorded as actors. If an existing supporter later retracts or votes against, add evidence with `stance=retracted`; they then show as a former supporter.
5. **Public role, public record.** Only people acting in a public capacity (elected officials, officials, published authors, journalists, organisation leaders, people who publicly declared themselves, e.g. signed a published letter). Never record private individuals (ordinary petition signers, private social-media users), and never record home addresses, personal phone numbers or personal emails. Organisation websites and official pages are fine.
6. **The CSV files are the database.** Write each actor and its evidence to disk as soon as it is verified — never hold a batch in memory to write at the end. The xlsx is a generated export, never edited by hand.
7. **Controlled vocabularies only** (section 5). If nothing fits, use the closest value and say so in `notes`; propose a vocabulary change in the run log rather than inventing a value.
8. **Report counts from the files**, not from memory (`wtdb.py status`, or count the CSV rows).
9. **Search in every official language of the area** (local-language terms are in the source playbook). English-only searching misses most of the local layer.

---

## 2. What counts as wealth taxation

A tax on the **stock of wealth** (net assets) of the wealthy, rather than on income, transactions or a single type of property.

**Included** — the `wt_design` values:

| wt_design | Meaning | Examples |
|---|---|---|
| `annual_net_wealth` | Recurring annual tax on net wealth above a threshold | 2% on assets over £10m; Spain's patrimonio; Norway's formuesskatt |
| `one_off_levy` | One-time levy on net wealth | California's one-time 5% billionaire tax ballot measure; post-crisis wealth levies |
| `billionaire_minimum` | Minimum tax set as a % of wealth for the ultra-rich | Zucman's 2% minimum tax on billionaires; the G20 2024 billionaire-tax discussion; France's "taxe Zucman" |
| `unrealised_gains` | Annual taxation of unrealised gains for the very wealthy (mark-to-market) | US billionaire minimum income tax on unrealised gains |
| `exit_tax` | Tax on wealth or unrealised gains when the wealthy emigrate | Exit-tax proposals tied to a wealth tax |
| `partial_wealth` | Recurring tax on net holdings of a broad asset class (e.g. financial assets), not a single property | — |
| `defend_existing` | Opposing abolition, or supporting keeping or raising an existing wealth tax | Defending a national wealth tax against repeal |
| `wealth_tax_unspecified` | Calls for "a wealth tax" without saying which design | "We need a wealth tax" |

**Excluded** (never qualifies on its own): mansion or high-value property taxes; council tax or property tax reform; land value tax; capital gains tax changes on realisation; inheritance, estate or gift taxes; income or dividend tax rises; windfall taxes; corporate taxes; financial transaction taxes; closing loopholes or tax-avoidance measures; generic "tax the rich" or "fair share" with no reference to the stock of wealth.

**Ambiguous phrases.** "Tax wealth like work" or "tax wealth not work" often means aligning capital gains with income tax (common UK usage). Treat it as grade C at most, and only when nothing in the speaker's own platform shows they mean capital gains. If it clearly means capital gains or dividends, it does not qualify. Watch local terms that also cover excluded taxes (e.g. Italian *patrimoniale* can mean property taxes; Dutch *vermogensbelasting* often refers to the savings box) and read the context.

**Not enough on their own:** "tax the wealthy", "tax billionaires more", "make the rich pay their fair share", and support for bills that change income or capital-gains tax (a millionaires' surtax, a minimum income tax on realised income). Count them only when the person's own words or the named bill refer to wealth, net worth or unrealised gains, as in the table above. Record the near-misses in `exclusions.csv` (`out_of_definition` or `insufficient_evidence`) so nobody re-checks them.

Someone who supports both an included design and an excluded one qualifies on the included evidence; record only that evidence.

---

## 3. Evidence grades

| Grade | Label | Rule |
|---|---|---|
| **A** | Explicit | Endorses an included design **with specifics** (rate, threshold, named bill or proposal), **or** a formal act: voted for, sponsored or co-sponsored, signed a motion or letter that calls for an included design, organisational policy adoption, authored a publication recommending one, gave supportive testimony. |
| **B** | Named | Supports "a wealth tax", "wealth levy", "billionaire tax" or an equivalent local term by name, without specifics. |
| **C** | Implied | Language that probably means wealth taxation but is ambiguous ("make the super-rich pay on their wealth"). Included and flagged as *appears to support*; a target for upgrade. |

**Roster and endorsement lists.** When a campaign's own page lists someone as an endorser, that is a claim by the campaign, not a statement by the endorser. Grade it **B** and say so in `grading_note`; upgrade to A when you find the endorser's own statement, vote or signature. Sponsors and cosponsors in official bill data are a formal act (A).

An actor's grade is the best grade among its support evidence. Grade each piece of evidence on its own, and write one line in `grading_note` explaining why.

---

## 4. Who counts — actor types and inclusion rules

`kind` is `person`, `organisation` or `institution` (a public body: a council, parliament, government or commission).

| actor_type | kind | Include when… |
|---|---|---|
| `politician` | person | Elected official or candidate at any level (supranational to local), or a minister, with qualifying evidence: vote, sponsorship, signed motion, speech or statement. Record level and geography. |
| `party` | organisation | Party, party branch, council group or youth wing; evidence from a manifesto, policy document or conference motion. |
| `government_body` | institution | A council, parliament, government or commission that **passed** a motion or adopted a position, or a commission that recommended it. A failed motion goes on the proposer, not the body. |
| `academic` | person | Scholar outside economics (law, politics, public health, sociology and so on) who wrote in favour (paper, book, report, op-ed, testimony). Merely researching wealth taxes does not count. |
| `economist` | person | Any economist, whether at a university, central bank, international organisation, bank, think tank or consultancy, arguing in favour. Use this for economists in academia too, so that one filter finds them all. |
| `think_tank` | organisation | Published a recommendation, or campaigns for it. |
| `ngo_campaign` | organisation | NGO, charity, campaign group or coalition campaigning for or endorsing it. |
| `union` | organisation | Union, union confederation or trades council with a policy, motion or campaign. |
| `union_official` | person | Union leader or official speaking for it. |
| `journalist` | person | Writes **opinion** pieces (columns, op-eds, essays, podcasts, video commentary) arguing for it. Reporters writing straight news do not count. |
| `media_outlet` | organisation | An editorial (the outlet's own stated view) argues for it. |
| `legal_tax_professional` | person / organisation | Tax lawyer, accountant, valuer, former tax-authority official or professional body that publishes in favour or gives supportive evidence. |
| `wealthy_individual` | person | A wealthy person who has **publicly** declared support (signed letter, member of a public group such as Patriotic Millionaires, statement). |
| `business_leader` | person / organisation | A business figure or business association publicly in favour. |
| `faith` | person / organisation | Faith leader or faith organisation. |
| `cultural_figure` | person | Artist, writer, athlete or celebrity with a public statement. |
| `campaigner` | person | Individual activist or NGO leader with a public profile (spokesperson, founder, author, charity chief executive). |
| `international_body` | institution / organisation | International or supranational body, or intergovernmental group (UN, IMF, OECD, G20 track, EU institutions, EU Tax Observatory). |
| `funder` | organisation | Foundation that **funds wealth-tax advocacy or research specifically**; evidence is a grant record or a programme page. |

International actors (Zucman, Oxfam International) are included in a country database only when they acted **in or towards that area** (testimony to its parliament, a campaign there). Give them their Wikidata ID so databases can be merged later.

---

## 5. Data files

In this repository, `<area-slug>` is the lowercase ISO 3166-1 alpha-2 code (`gb`, `de`) or `<iso2>-<region>` (`us-ca`). Each folder also needs a `meta.json` (`name`, `iso2`, `lead`, `status`, `boundaries`, `notes`; `init` creates it). Put the scope you chose (levels covered, anything left out) in `notes` and in section 1 of `area_profile.md`. Everything lives in `data/<area-slug>/` (e.g. `data/gb/`, `data/us-california/`, `data/eu/`). Create it with `python skill/scripts/wtdb.py init data/<slug> --area "<Area name>"`, or by hand with exactly these headers. IDs are prefix + zero-padded number (A0001, E00001, G0001, L0001, H0001, X0001, R001).

**actors.csv** — one row per actor
`actor_id, name, kind, actor_type, other_types, role, affiliation, party, affiliation_actor_id, country, level, location, wikidata_qid, website, status, alive_checked, prominence, notes, added_run, updated`
- `other_types`: extra `actor_type` values separated by `;`, for people who fit more than one (for example `journalist` primary with `economist` here). `actor_type` is the main role; the site and the coverage grid count a person under every type they hold.
- `party`: for politicians, the party's common name in English (for example `Labour`, `Green Party`, `Democratic Party`; `Independent` if none). Use one name per party so the site can filter on it; a regional or state branch uses the national party's name (the Minnesota DFL is `Democratic Party`). Blank for non-politicians, and for local officials in non-partisan offices when the party is not known. `validate` warns about a missing party above local level.
- `level`: supranational · national · regional · local (the level of government or society they act at)
- `location`: where they are based or whom they represent, written as a path from the country down, separated by ` > `: `United States > California > Camarillo`, `United Kingdom > London > Hackney`, `United Kingdom > Yorkshire and The Humber > Leeds East`. The first part is the country root unit in `geo_units.csv`. Each next part that matches a register unit under the previous one is resolved to that unit; anything after that is plain place text (a city, district or constituency the register does not list yet). Give the finest place you can prove. If you only know the state, stop at the state; if you only know the country (a national union, a nationwide campaign), write just the country. Never guess a finer place. A national-level actor sits at the country; a legislator sits at the place they represent (the district, constituency, state or region), not at the institution (that goes in `role`). The site counts an actor for every unit on the path, so a city actor counts for their state and the country.
- `status`: active · former_role · dissolved
- `alive_checked`: y · na (organisations and institutions). `y` means you looked for a death record and found none.
- `notes`: only what a reader needs: an identity caveat (a common name, a role taken from a list), where the party or role came from, or context the evidence rows do not show. **Never** write that the person is alive, that Wikidata has no match, or that no death record was found; `alive_checked` already says it, and the site shows the notes to readers. Leave `notes` empty when there is nothing to add.
- `prominence`: international · national · regional · local (how widely they are known on this issue)

**evidence.csv** — one row per piece of evidence (an actor can have many)
`evidence_id, actor_id, date, stance, grade, evidence_type, wt_design, design_detail, quote_original, quote_lang, quote_en, source_url, source_title, publisher, archive_url, accessed, harvest_id, grading_note, verified, run_id`
- `date`: YYYY-MM-DD (or YYYY-MM / YYYY if that is all that is known); the date of the act or statement, not of a later article about it
- `stance`: support · retracted
- `grade`: A · B · C
- `evidence_type`: vote · bill_sponsorship · motion · motion_signature · open_letter · publication · report · op_ed · editorial · speech · statement · interview · social_post · manifesto · policy_adoption · campaign · coalition_membership · testimony · funding · other
- `wt_design`: values in section 2
- `design_detail`: rate, threshold, bill name or number (e.g. "2% over £10m")
- `quote_original`: verbatim from the source page; `quote_lang`: ISO code; `quote_en`: translation if not English
- `verified`: n · y · failed (y means re-opened in QA and the quote was found)

**geo_units.csv** — the geography checklist for the local sweep
`geo_unit_id, name, level, unit_type, parent_id, website, sweep_status, swept_run, swept_date, queries_run, hits, notes`
- The register is a **tree**. The top row is the **country root** (`unit_type=country`, `level=national`, no parent), named as the first part of every `location`. Regions, states and nations are its children (`parent_id`), and councils, counties or cities sit below those. Institutions such as the legislature or the executive are also children of the root, but actors are not placed on them (see `location`).
- Unit names must be unique among siblings. Write the plain name (`California`), not `California (state legislature)`; put descriptions in `unit_type` and `notes`.
- `level`: supranational · national · devolved · region · county · combined_authority · council · sub_council. In a federal country, states are `region`. Load only the depth you are sweeping; a unit with children is a parent, and `status` counts the lowest units.
- `sweep_status`: pending · in_progress · done · skipped

**boundaries.json** (optional, in the country folder, named in `meta.json`) draws the local map on the site: `{"viewBox": [x, y, w, h], "units": [{"name", "code", "path"}]}`. A unit's `name` must equal a `geo_units.csv` name, or be that name up to the opening bracket (`Alabama` matches `Alabama (state legislature and state government)`). Make it from a TopoJSON with `scripts/topo_to_boundaries.py`. Check the licence of the shapes and say where they came from in the file's `source`.

**links.csv** — relationships, used for snowballing
`link_id, from_actor_id, to_actor_id, link_type, evidence_id, source_url, note`
- `link_type`: member_of · works_for · leads · co_author · co_signatory · funds · founded · coalition_partner · party_of

**profiles.csv** — official or professional links for an actor, one row per link
`profile_id, actor_id, platform, url, source, checked`
- `platform`: website · official_page · x · bluesky · mastodon · instagram · facebook · youtube · tiktok · linkedin · substack · wikipedia
- Only pages the person or their organisation publishes (their own site, party or parliament page, professional social accounts), or that Wikidata or a parliament lists for them. No personal accounts, email addresses or phone numbers, and nothing guessed from a name search. `url` must be https. `source` says where the link came from and `checked` is the date you read that source. Skip private individuals and people who are only known as wealthy signers.

**harvest.csv** — bulk lists to process (see 6.3)
`harvest_id, title, list_type, url, date, est_size, status, actors_added, notes`
- `list_type`: roll_call · cosponsors · motion_signatories · open_letter · coalition_members · report_authors · commission_evidence · conference_motion · other
- `status`: queued · in_progress · done · failed

**exclusions.csv** — candidates checked and rejected, so they are not checked again
`exclusion_id, name, reason, detail, source_url, run_id`
- `reason`: out_of_definition · pre_2010_only · deceased · private_individual · opposes · insufficient_evidence · duplicate

**runs.csv** — one row per run
`run_id, date, assistant, focus, targets, queries_run, sources_opened, candidates_seen, new_actors, new_evidence, grade_upgrades, verified_ok, verified_failed, saturation, notes_next`

**area_profile.md** — the area profile (section 6.1).

Helper commands (when Python is available):
```
python skill/scripts/wtdb.py add data/gb actors '{"name":"…","kind":"person",…}'   # assigns ID; prints it
python skill/scripts/wtdb.py add data/gb evidence @new_evidence.jsonl               # one JSON object per line
python skill/scripts/wtdb.py set data/gb geo_units G0042 sweep_status=done hits=2 queries_run=6
python skill/scripts/wtdb.py validate data/gb     # errors must be fixed before a run ends
python skill/scripts/wtdb.py dedupe data/gb       # likely duplicate actors
python skill/scripts/wtdb.py merge data/gb A0012 A0345   # merge a duplicate (second) into the first: moves evidence, links, profiles
python skill/scripts/wtdb.py checkquotes data/gb --run R004   # fetch sources and check the quotes are on the pages
python skill/scripts/profiles_wikidata.py data/gb  # websites, socials and Wikipedia from Wikidata IDs
python skill/scripts/topo_to_boundaries.py states.json --object states --out data/us/boundaries.json
python skill/scripts/wtdb.py status data/gb       # counts, coverage grid, sweep progress, suggested next targets
python skill/scripts/wtdb.py export data/gb       # writes data/gb/<slug>_wealth_tax_supporters.xlsx
```
Writing CSVs directly is fine too, but quote fields properly (quotes often contain commas), and run `validate` afterwards.

---

## 6. Workflow

### 6.0 Start or resume
- **In this repository, never push to `main`.** Work on a branch, open one pull request per run (or per country), and let the checks run (`validate` on every country, the site build). A person merges.
- If `data/<slug>/` exists: read `area_profile.md`, the last 3 rows of `runs.csv` (especially `notes_next`), and the `status` output. Continue from there; do not redo finished work.
- If not: confirm the area and its scope (which levels of government; whether to go below council level), then `init`. Start the run log entry in your head now and write it at the end.

### 6.1 Area profile (first run only, then update as needed)
Fill in `area_profile.md` from `references/area-profile-template.md`: wealth-tax history and live proposals since 2010; legislatures and where their votes, motions and speeches are published; parties; the structure of government below national level and what each level can tax; official languages and the search terms for each; main national and regional media; registers (company, charity, grant, lobbying, donations); known coalitions and campaigns. Every factual line gets a source.

### 6.2 Geography register (first run)

**How to divide a country.** Use the administrative hierarchy where political and tax power sits, one tree per country: a federal country goes country → state → county or city; a unitary country goes country → nation or region → council. Choose a depth you will actually sweep, load only that depth, and write the choice in `meta.json` `notes` and the area profile. Finer places that you meet before you load them are not lost: put them in `location` as place text (`United States > California > Camarillo`) and they resolve later when you add that layer. Seats are places, not institutions: an MP belongs to the constituency, a US representative to the district. If the register has no layer for constituencies or districts, keep them as place text under the region or state. A second boundary file for such a layer (constituencies, districts) is a separate piece of work.
Fetch the **official current list** of every sub-national unit down to the lowest level in scope (for the UK: nations → regions/counties → combined authorities → every principal council; see `references/countries/gb.md`). Load all of them into `geo_units.csv` with `sweep_status=pending`, with `parent_id` set so progress can be reported region by region. Do not work from memory; councils merge and change.

For a country with a local map, also build `boundaries.json` from an official or open boundary source (see `scripts/topo_to_boundaries.py`) and set `boundaries` in `meta.json`. Do it in the first run; it costs little and makes coverage visible on the site.

### 6.3 Bulk harvest (highest yield; always first priority)
Lists produce many actors at once with uniform, strong evidence. Find them and queue them in `harvest.csv`, then process each list entry by entry:
- roll-call votes on wealth-tax bills or amendments, and bill co-sponsors
- signatories of parliamentary or council motions
- open letters with published signatory lists (economists, millionaires, faith leaders, organisations)
- coalition and campaign member lists
- authors of wealth-tax reports and commissions; witnesses and written evidence to commissions and committees
- union and party conference motions (mover, seconder, supporting bodies)

Rosters can be large (a ballot campaign's endorsement page listed about 250 names). Parse the page's structured data instead of retyping names, check each name against the database (name variants such as "Coalition for Human Needs" and "Coalition on Human Needs" are the same body: `merge`), and keep the list's own entry text as the quote. Wikipedia and other secondary lists are good for finding names, never as the source; re-read each name at its own cited page.

For each person or organisation on a list: check for duplicates, check the definition applies to what the list actually calls for, check they are not dead (or, for an organisation, that it still exists), then add the actor and an evidence row whose `harvest_id` points to the list. Mark the list `done` with `actors_added`.

### 6.4 Layer passes
Work through the layers in the source playbook (legislatures, parties, executive, academia, think tanks, civil society, unions, media, legal and tax, wealthy and business, faith and culture, funders, international). For each, run the query pack in every relevant language, open the promising results, and add what qualifies. Choose layers using the `status` coverage grid (actor_type × level): go where the cells are thin.

### 6.5 Local sweep — every unit, no exceptions
Supporters at council level rarely appear in national searches, so every geography unit is visited and marked, **including units with zero results**: a `done` with `hits=0` is what proves coverage.

For each unit (work one parent region at a time, so the region is finished before moving on):
1. Run the local query pack from the source playbook, in local language(s), using the unit's name (and the main town names for counties).
2. Search the council's own site for meeting minutes and motions (many councils' sites can be searched directly; a site-restricted web search works otherwise).
3. Check local news (in the UK, the Local Democracy Reporting Service carries council motions) and local party groups, trades councils and campaign branches.
4. Add every qualifying actor (councillor, council group, local branch, the council itself if a motion **passed**), with `location` set to that council's path.
5. `set` the unit: `sweep_status=done`, `swept_run`, `swept_date`, `queries_run`, `hits`; in `notes`, record motions found even if they failed.

Order within a region: larger cities and units with known signals first, but every unit is completed. Units below council level (town and parish councils) are swept only when the profile puts them in scope.

### 6.6 Snowball and upgrade
- **Snowball:** for actors added this run, follow `links` outwards: co-authors, co-signatories, members of the same coalition, their organisation, their party's council group. Add new candidates, and record links.
- **Upgrade:** for C- and B-graded actors, search for explicit evidence (a vote, a signed letter, a specified design) and add it. Leave the old evidence in place.
- **Retractions:** for prominent supporters, check whether they have since retracted.

### 6.7 QA, export and report (end of every run)
1. `validate` → fix every error. Warnings: fix or justify in `notes`.
2. `dedupe` → merge true duplicates: keep the older ID, move evidence across, and record the other in `exclusions.csv` with `reason=duplicate`.
3. **Quote check:** run `checkquotes --run <this run>`. Fix or remove every row it reports as not found. Rows it skips (PDFs, blocked pages) need a manual look: open the page, find the quote.
   Then spot-check at least 10% of the run's rows (minimum 5) by hand for grade and meaning, not just wording.
   **`verified=y` is set only by someone other than the row's author**: a person, or a separate agent that has not seen the work. Authors leave rows at `n`. A row whose quote cannot be found is set to `failed` and then fixed or removed.
4. Append the run row to `runs.csv`, including `saturation` (see 6.8) and `notes_next` (concrete next targets).
5. Open or update the pull request (6.0). `export` if the user wants a spreadsheet, and report to the user: new actors and evidence by type and level, geography units completed versus remaining, grade upgrades, verification results, notable findings, and next targets. Use numbers from `status`, not from memory.

### 6.8 Choosing what to do in a run, and when to stop
Priority order for each run:
1. queued harvest lists
2. pending geography units (finish the current region)
3. thin cells in the coverage grid
4. upgrades of C-graded actors
5. snowballing

**Saturation:** for a layer or region, `saturation = candidates already in the database (or excluded) ÷ candidates seen`. When it is ≥ 0.9 for two consecutive passes, mark that layer saturated in the run notes and move on. The database is "complete for now" when the harvest queue is empty, every geography unit is `done`, and every layer is saturated; from then on, runs are update sweeps (new evidence since the last run date).

A good run size is one harvest list or one region of the local sweep plus a layer pass. Write to disk continuously, so an interrupted run loses nothing.

### 6.9 Parallel work (if the assistant can run subagents)
Split by region (local sweep) or by layer, never so that two workers write the same file. Each worker writes `staging_<worker>.jsonl` files (actors and evidence with temporary IDs) and returns them; the coordinator deduplicates against the database, adds with `wtdb.py add`, runs `validate`, and has a separate worker do the spot-check.

### 6.10 Without code
Follow the same steps by hand: keep the CSVs in exactly the format above, check the `validate` rules yourself (required fields, allowed values, dates from 2010, a URL and a quote on every evidence row, no actor without evidence, no duplicates), and deliver the CSVs or a spreadsheet built from them.

---

## 7. Export

The xlsx export contains: **Overview** (counts, grade mix, coverage and sweep progress, definitions); **Supporters** (one row per actor: grade, *explicit / named / appears to support*, designs, evidence count, first and latest evidence date, strongest source); **Evidence**; **Local coverage** (each geography unit with sweep status and supporter count); **Links**; **Profiles** (websites and socials); **Harvest lists**; **Run log**; **Former supporters** (latest stance retracted, shown only when there are some). There is no points score. Users filter by grade, type, level, prominence and date.

---

## 8. Things that went wrong before (avoid them)

- Actions typed outside the vocabulary, so the methodology no longer described the data → always use the controlled values; `validate` enforces them.
- Mansion-tax and council-tax supporters counted as wealth-tax supporters → apply section 2 to every piece of evidence.
- Opponents mixed into the supporter list → supporters only.
- Related tables existed only in the assistant's memory and never reached the file; earlier turns "compressed" in the log → write to disk continuously; log every run.
- Theme-by-theme, name-by-name searching gave few new actors per turn → bulk lists first, then the geography sweep, then snowballing.
- Reporters counted as supporters because they quoted one → journalists need opinion pieces.
- Notes full of "alive on the basis of..." and "no Wikidata match" on hundreds of rows, shown to readers on the site → `alive_checked=y` records the check; `validate` now warns when notes narrate it.
- Paraphrased "quotes": a roster import wrote its own sentence ("Campaign lists X as an endorser…") into 252 rows, because the fetch tool summarises pages → quote the page's own text, and run `checkquotes`.
- One bucket hid a group: all university economists were typed `academic`, so the Economist filter showed four people → type by discipline (`economist` for any economist) and use `other_types` for people who fit two.
- Near-duplicate organisations from different letters and rosters ("Coalition for Human Needs" and "Coalition on Human Needs") → `dedupe` after every large import, then `merge`.
- Party names written several ways ("Labour Party", "Labour", "Welsh Labour"; "Democratic-Farmer-Labor") → one common name per party, branches use the national name.
- Pages that said "tax the wealthy" but not wealth tax were nearly counted → apply section 2 to the speaker's own words.
- Progress reports that ignored higher-level units ("no geography units loaded") → `status` counts the lowest units of whatever depth you loaded.
- Pushing straight to `main`, or setting `verified=y` on one's own rows → branch, pull request, and a different checker for `verified=y`.
