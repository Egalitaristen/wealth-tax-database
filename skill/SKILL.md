---
name: wealth-tax-supporter-map
description: Systematically build or extend a sourced database of people, organisations and institutions in a country, region or supranational area that support (or appear to support) actual wealth taxation since 2010, down to local-government level. Use when asked to map, find, update or export wealth tax supporters for any area.
---

# Wealth Tax Supporter Map

Build a comprehensive, verifiable overview of everyone in an area who supports — or appears to support — **actual wealth taxation**: politicians who voted for or sponsored it, academics who argued for it, journalists who advocate it, organisations campaigning for it, councils that passed motions for it, and so on.

This is a map, not a ranking. Every entry rests on dated, sourced, quoted evidence. The work is done in repeatable **runs**; each run reads the current state from disk, works the biggest gaps, writes results as it goes, and logs what it did, so any assistant in any session can pick up where the last one stopped.

Files in this skill (use them if present; the rules in this file are sufficient on their own):
- `references/source-playbook.md` — layers, bulk-list sources, query templates, search terms in many languages
- `references/area-profile-template.md` — what to establish about an area before searching
- `references/countries/gb.md` — UK levels of government, sources, and the local sweep list (worked example for other countries)
- `scripts/wtdb.py` — Python helper (stdlib; `openpyxl` only for xlsx export): `init`, `add`, `set`, `validate`, `dedupe`, `status`, `export`

---

## 1. Ground rules

1. **Apply the definition (section 2) to every piece of evidence.** Support for a mansion tax, capital gains reform or inheritance tax is not support for wealth taxation.
2. **No source, no row.** Every claim is an evidence row with a URL you actually opened and a verbatim quote found on that page. Never add an actor or evidence from memory or from a search-result snippet alone.
3. **Time window and the living.** Only evidence dated 2010-01-01 or later counts. Individuals must be alive; check before adding (Wikidata or an obituary search when in doubt). Dissolved organisations may stay, marked `dissolved`.
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

Someone who supports both an included design and an excluded one qualifies on the included evidence; record only that evidence.

---

## 3. Evidence grades

| Grade | Label | Rule |
|---|---|---|
| **A** | Explicit | Endorses an included design **with specifics** (rate, threshold, named bill or proposal), **or** a formal act: voted for, sponsored or co-sponsored, signed a motion or letter that calls for an included design, organisational policy adoption, authored a publication recommending one, gave supportive testimony. |
| **B** | Named | Supports "a wealth tax", "wealth levy", "billionaire tax" or an equivalent local term by name, without specifics. |
| **C** | Implied | Language that probably means wealth taxation but is ambiguous ("make the super-rich pay on their wealth"). Included and flagged as *appears to support*; a target for upgrade. |

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
| `campaigner` | person | Individual activist with a public profile (spokesperson, founder, author). |
| `international_body` | institution / organisation | International or supranational body, or intergovernmental group (UN, IMF, OECD, G20 track, EU institutions, EU Tax Observatory). |
| `funder` | organisation | Foundation that **funds wealth-tax advocacy or research specifically**; evidence is a grant record or a programme page. |

International actors (Zucman, Oxfam International) are included in a country database only when they acted **in or towards that area** (testimony to its parliament, a campaign there). Give them their Wikidata ID so databases can be merged later.

---

## 5. Data files

In this repository, `<area-slug>` is the lowercase ISO 3166-1 alpha-2 code (`gb`, `de`) or `<iso2>-<region>` (`us-ca`). Each folder also needs a `meta.json` (`name`, `iso2`, `lead`, `status`, optional `boundaries`); `init` creates it. Everything lives in `data/<area-slug>/` (e.g. `data/gb/`, `data/us-california/`, `data/eu/`). Create it with `python skill/scripts/wtdb.py init data/<slug> --area "<Area name>"`, or by hand with exactly these headers. IDs are prefix + zero-padded number (A0001, E00001, G0001, L0001, H0001, X0001, R001).

**actors.csv** — one row per actor
`actor_id, name, kind, actor_type, role, affiliation, affiliation_actor_id, country, level, geo_unit_id, wikidata_qid, website, status, alive_checked, prominence, notes, added_run, updated`
- `level`: supranational · national · regional · local
- `status`: active · former_role · dissolved
- `alive_checked`: y · na (organisations and institutions)
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
- `level`: supranational · national · devolved · region · county · combined_authority · council · sub_council
- `sweep_status`: pending · in_progress · done · skipped

**links.csv** — relationships, used for snowballing
`link_id, from_actor_id, to_actor_id, link_type, evidence_id, source_url, note`
- `link_type`: member_of · works_for · leads · co_author · co_signatory · funds · founded · coalition_partner · party_of

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
python skill/scripts/wtdb.py status data/gb       # counts, coverage grid, sweep progress, suggested next targets
python skill/scripts/wtdb.py export data/gb       # writes data/gb/<slug>_wealth_tax_supporters.xlsx
```
Writing CSVs directly is fine too, but quote fields properly (quotes often contain commas), and run `validate` afterwards.

---

## 6. Workflow

### 6.0 Start or resume
- If `data/<slug>/` exists: read `area_profile.md`, the last 3 rows of `runs.csv` (especially `notes_next`), and the `status` output. Continue from there; do not redo finished work.
- If not: confirm the area and its scope (which levels of government; whether to go below council level), then `init`. Start the run log entry in your head now and write it at the end.

### 6.1 Area profile (first run only, then update as needed)
Fill in `area_profile.md` from `references/area-profile-template.md`: wealth-tax history and live proposals since 2010; legislatures and where their votes, motions and speeches are published; parties; the structure of government below national level and what each level can tax; official languages and the search terms for each; main national and regional media; registers (company, charity, grant, lobbying, donations); known coalitions and campaigns. Every factual line gets a source.

### 6.2 Geography register (first run)
Fetch the **official current list** of every sub-national unit down to the lowest level in scope (for the UK: nations → regions/counties → combined authorities → every principal council; see `references/countries/gb.md`). Load all of them into `geo_units.csv` with `sweep_status=pending`, with `parent_id` set so progress can be reported region by region. Do not work from memory; councils merge and change.

### 6.3 Bulk harvest (highest yield; always first priority)
Lists produce many actors at once with uniform, strong evidence. Find them and queue them in `harvest.csv`, then process each list entry by entry:
- roll-call votes on wealth-tax bills or amendments, and bill co-sponsors
- signatories of parliamentary or council motions
- open letters with published signatory lists (economists, millionaires, faith leaders, organisations)
- coalition and campaign member lists
- authors of wealth-tax reports and commissions; witnesses and written evidence to commissions and committees
- union and party conference motions (mover, seconder, supporting bodies)

For each person or organisation on a list: check for duplicates, check the definition applies to what the list actually calls for, check they are alive or still exist, then add the actor and an evidence row whose `harvest_id` points to the list. Mark the list `done` with `actors_added`.

### 6.4 Layer passes
Work through the layers in the source playbook (legislatures, parties, executive, academia, think tanks, civil society, unions, media, legal and tax, wealthy and business, faith and culture, funders, international). For each, run the query pack in every relevant language, open the promising results, and add what qualifies. Choose layers using the `status` coverage grid (actor_type × level): go where the cells are thin.

### 6.5 Local sweep — every unit, no exceptions
Supporters at council level rarely appear in national searches, so every geography unit is visited and marked, **including units with zero results**: a `done` with `hits=0` is what proves coverage.

For each unit (work one parent region at a time, so the region is finished before moving on):
1. Run the local query pack from the source playbook, in local language(s), using the unit's name (and the main town names for counties).
2. Search the council's own site for meeting minutes and motions (many councils' sites can be searched directly; a site-restricted web search works otherwise).
3. Check local news (in the UK, the Local Democracy Reporting Service carries council motions) and local party groups, trades councils and campaign branches.
4. Add every qualifying actor (councillor, council group, local branch, the council itself if a motion **passed**), linked to `geo_unit_id`.
5. `set` the unit: `sweep_status=done`, `swept_run`, `swept_date`, `queries_run`, `hits`; in `notes`, record motions found even if they failed.

Order within a region: larger cities and units with known signals first, but every unit is completed. Units below council level (town and parish councils) are swept only when the profile puts them in scope.

### 6.6 Snowball and upgrade
- **Snowball:** for actors added this run, follow `links` outwards: co-authors, co-signatories, members of the same coalition, their organisation, their party's council group. Add new candidates, and record links.
- **Upgrade:** for C- and B-graded actors, search for explicit evidence (a vote, a signed letter, a specified design) and add it. Leave the old evidence in place.
- **Retractions:** for prominent supporters, check whether they have since retracted.

### 6.7 QA, export and report (end of every run)
1. `validate` → fix every error. Warnings: fix or justify in `notes`.
2. `dedupe` → merge true duplicates: keep the older ID, move evidence across, and record the other in `exclusions.csv` with `reason=duplicate`.
3. **Spot-check:** re-open the source for at least 10% of this run's evidence rows (minimum 5) and confirm the quote is there and the grade holds. Set `verified=y` or `failed`; fix or remove failed rows. If you can delegate to a separate agent that has not seen the work, have it do this.
4. Append the run row to `runs.csv`, including `saturation` (see 6.8) and `notes_next` (concrete next targets).
5. `export`, and report to the user: new actors and evidence by type and level, geography units completed versus remaining, grade upgrades, verification results, notable findings, and next targets. Use numbers from `status`, not from memory.

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

The xlsx export contains: **Overview** (counts, grade mix, coverage and sweep progress, definitions); **Supporters** (one row per actor: grade, *explicit / named / appears to support*, designs, evidence count, first and latest evidence date, strongest source); **Evidence**; **Local coverage** (each geography unit with sweep status and supporter count); **Links**; **Harvest lists**; **Run log**; **Former supporters** (latest stance retracted). There is no points score. Users filter by grade, type, level, prominence and date.

---

## 8. Things that went wrong before (avoid them)

- Actions typed outside the vocabulary, so the methodology no longer described the data → always use the controlled values; `validate` enforces them.
- Mansion-tax and council-tax supporters counted as wealth-tax supporters → apply section 2 to every piece of evidence.
- Opponents mixed into the supporter list → supporters only.
- Related tables existed only in the assistant's memory and never reached the file; earlier turns "compressed" in the log → write to disk continuously; log every run.
- Theme-by-theme, name-by-name searching gave few new actors per turn → bulk lists first, then the geography sweep, then snowballing.
- Reporters counted as supporters because they quoted one → journalists need opinion pieces.
