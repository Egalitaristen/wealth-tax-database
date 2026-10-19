# Area profile — United Kingdom

First drafted 2026-10-18 (run 1). Lines marked **[verify]** come from a search-result summary only and must be opened and confirmed before they are relied on. Sources are given per line.

## 1. Scope
- Area: United Kingdom; type: country (with devolved nations)
- Levels of government in scope: supranational (UK MEPs 2010–2020 only), national, devolved (Scotland, Wales, Northern Ireland), combined authorities and the Greater London Authority, county councils, and every principal council (unitary, metropolitan, London borough, district, Scottish, Welsh and Northern Ireland councils). Sub-council level (town, parish, community councils): **not in scope for now**; revisit once the principal-council sweep is done.
- Languages to search in: English; Welsh (Senedd, Welsh councils); Scottish Gaelic and Scots are not expected to matter. Irish only for Northern Ireland Assembly material if it appears.
- Date of first run: 2026-10-18

## 2. Wealth tax history and live proposals (2010 onwards)
Everything here needs opening and sourcing in a later run; the entries are leads, not evidence.
- **Wealth Tax Commission (2020):** independent commission; December 2020 report recommended a one-off charge rather than an annual tax; reported model 1% on net wealth above £500,000 paid over five years. Source: [LSE news](https://www.lse.ac.uk/news/latest-news-from-lse/l-december/wealth-commission-report), [RSM summary](https://www.rsmuk.com/insights/tax-voice/wealth-tax-options-for-taxing-wealth-and-raising-revenue) **[verify figures against the report]**
- **Green Party proposal:** annual 1% on wealth above £10m, 2% above £1bn. Used as template wording in council motions (see section 5). Source: [Hackney Citizen, 4 Dec 2024](https://www.hackneycitizen.co.uk/2024/12/04/opposition-town-hall-immediate-wealth-tax/), [Leeds Green councillors](https://leeds.greenparty.org.uk/?p=6757). The 2024 general election manifesto wording itself is **[verify]**.
- **Autumn 2025 Budget lobbying:** Green and other local parties campaigning "cut bills, tax billionaires" ahead of the Chancellor's second budget. Source: [Irish News](https://uk.irishnews.com/news/uk/chancellor-faces-calls-for-wealth-tax-a-week-before-second-budget-MT3VQDEXSZJPZMHCQO7V7TFVSU), [Mid Sussex & Crawley Greens](https://midsussex.greenparty.org.uk/2025/11/21/mid-sussex-crawley-green-party-says-our-message-to-rachel-reeves-is-simple-cut-bills-tax-billionaires/)
- **Millionaires' letter** (more than 100 millionaires urging a 2% annual tax above £10m) and **statements by senior Labour figures on ruling a wealth tax in or out:** reported in a secondary summary only. **[verify date, signatories and wording]**
- Existing UK wealth tax: none. Past UK levies to rule out of scope: Bank levy, windfall taxes, mansion tax proposals (all excluded by the definition).
- Still to research: Labour, Lib Dem, SNP, Plaid and Green manifestos 2010–2024; Scottish, Welsh and NI motions; TUC congress motions; European Parliament votes (UK MEPs 2010–2020); House of Lords debates; the Fairness Foundation, CenTax, IPPR, NEF, Tax Justice UK, Patriotic Millionaires UK and Oxfam GB positions.

## 3. Legislatures and where their records are
Candidates, from `references/countries/uk.md`; check each URL is live and searchable before use.
- UK Parliament: Hansard hansard.parliament.uk; TheyWorkForYou; divisions votes.parliament.uk; early day motions edm.parliament.uk (bulk list source); bills bills.parliament.uk; written questions; committees.parliament.uk
- Scottish Parliament: parliament.scot (official report, motions with supporters, votes)
- Senedd: senedd.wales (Record of Proceedings; search English and Welsh)
- Northern Ireland Assembly: niassembly.gov.uk
- London Assembly and Mayor: london.gov.uk
- European Parliament (UK MEPs 2010–2020): HowTheyVote.eu and the Parliament's roll-call records

## 4. Parties
To fill: manifestos for 2010, 2015, 2017, 2019 and 2024 general elections, devolved elections and mayoral elections; party and youth-wing conference motions (Green, Labour, Lib Dem, SNP, Plaid Cymru, Sinn Féin, SDLP, independent and socialist groups).

## 5. Government below national level
- **Structure loaded into `geo_units.csv` (416 units):** 6 national/devolved/executive/supranational legislature units; 9 English regions plus Scotland, Wales and Northern Ireland as grouping parents; the Greater London Authority and 15 combined authorities / strategic authorities; 21 county councils; 361 councils.
- **361 councils by ONS type:** 63 unitary (E06), 164 non-metropolitan district (E07), 36 metropolitan borough (E08), 33 London borough or City of London (E09), 32 Scottish council area (S12), 22 Welsh principal area (W06), 11 Northern Ireland district (N09).
- **Source of the list:** ONS Open Geography Portal service "Local Authority Districts (May 2026) Boundaries UK BFC" (fetched 2026-10-18). Region, county and combined-authority parents were assigned automatically by matching each council's centroid to the ONS December 2025 region, county/unitary and combined-authority boundary layers. **Spot-check the parents** during the sweep, especially for combined authorities where non-constituent or associate members may be missing, and for the Greater London Authority, whose boundary is the 32 boroughs plus the City.
- **Local government reorganisation:** ongoing in England. A secondary summary says the government announced decisions on 16 July 2026 for 14 areas, replacing 134 councils with 38 unitaries, with shadow elections in May 2027 and go-live from 1 April 2028. **[verify against the written ministerial statement]** The register reflects councils that exist now; re-load the affected areas after each reorganisation takes effect and keep old councils' records, because evidence dated before the merger belongs to the old body.
- **What councils can tax:** councils cannot levy a wealth tax, so local support takes the form of motions asking the council to write to the Chancellor or Prime Minister, plus statements by councillors and local groups. The proposer and seconder are supporters even if the motion failed; the council counts as a `government_body` only if it passed.
- **Where minutes are published:** council websites, often on the ModernGov platform; Local Democracy Reporting Service stories; local party group pages.

## 6. Search terms
- English terms: "wealth tax", "tax on extreme wealth", "billionaire tax", "wealth levy", "one-off wealth levy", "annual wealth tax", "tax on wealth", "2% on assets over £10m", "Zucman" (for billionaire minimum), "tax the super-rich" (grade C only if it refers to wealth).
- Welsh terms: to be added from the Senedd record (check "treth cyfoeth" and related phrases in the first Welsh pass).
- Ambiguous terms: "tax wealth like work" often means aligning capital gains tax with income tax (excluded unless the speaker's own platform shows otherwise); "mansion tax", "council tax reform", "land value tax" and "windfall tax" are excluded.

## 7. Media
To fill: Guardian, Observer, i, Mirror, New Statesman, Tribune, Novara, Byline Times and others with opinion sections; regional papers; Local Democracy Reporting Service; podcasts and video commentators.

## 8. Registers
Electoral Commission donations; Companies House; Charity Commission (England and Wales), OSCR (Scotland), Charity Commission for Northern Ireland; 360Giving GrantNav; Register of Members' Financial Interests. URLs to be confirmed in a later run.

## 9. Known networks
Candidates only, not assumed supporters: Tax Justice UK, Patriotic Millionaires UK, Oxfam GB, Equality Trust, Tax Justice Network, Friends of the Earth, Greenpeace UK, 38 Degrees, People's Assembly, Positive Money; IPPR, New Economics Foundation, Common Wealth, Compass, Fabian Society, Fairness Foundation, Resolution Foundation; CenTax, LSE International Inequalities Institute; TUC and the unions.

## 10. Notes for future runs
- Geography register and profile are done. `geo_units.csv` has 416 rows, all `pending`, and there are no actors yet.
- Next priority per the workflow is bulk harvest: early day motions with signatories, Commons divisions and amendments on wealth-tax proposals, Wealth Tax Commission authors and evidence, open letters (economists and millionaires), Tax Justice UK and Patriotic Millionaires UK coalition lists, TUC congress motions.
- Then the local sweep, starting with London boroughs (Hackney's December 2024 motion is a known lead), then metropolitan boroughs, with Leeds as a known lead.
- Searching for the Green template wording ("1% on assets over £10 million, 2% over £1 billion") can find many councils at once.
- Optional: install `openpyxl` (`pip install openpyxl`) before the first export; it is not installed on this machine.

## 11. Findings from run 4 (2026-10-18)
- **Parties with a wealth tax in a manifesto or stated policy (leads, sources in evidence.csv):** Green Party of England and Wales (2024: 1% over £10m, 2% over £1bn; 2017: wealth tax on the top 1%; 2015 reported as £3m threshold, not yet sourced); Scottish Greens (2024 plan with 1%-10% bands; 2026 Holyrood manifesto commits to exploring a Scottish wealth tax); Welsh Liberal Democrats (leader Jane Dodds, 2% over £10m, Senedd 19 Nov 2025).
- **Parties checked with no wealth tax found:** Labour, Liberal Democrats (UK), SNP and Plaid Cymru 2024 manifestos (per secondary summaries only; open the manifestos to confirm). Scottish Liberal Democrats 2026 propose land value and private jet taxes. SNP 2026 proposes private jet tax and mansion tax (excluded designs). SNP MSPs did vote for a wealth tax amendment on 26 Nov 2025 (see H0010).
- **Senedd:** open debate on a 2% wealth tax on 19 Nov 2025 led by Julie Morgan; no division recorded in the sources read. Check the Senedd Record for a vote.
- **Organisations:** Tax Justice UK, Oxfam GB and Patriotic Millionaires UK all campaign for 2% over £10m (est. £24bn a year). IPPR (statement found concerns income from wealth, not a net wealth tax), the Fairness Foundation (pages unreadable) and NEF (guest essays only) are in exclusions.csv for now.
- **Letters:** July 2025 letter of 36 economists (H0012) and July 2026 Proud to Pay letter (H0006).
- **Sources that block automated fetches:** edm.parliament.uk, congress.tuc.org.uk, thecritic.co.uk (HTTP 403 bot checks). Use mirrors (Beyond the Vote, Wayback) or secondary reports and flag them.

## 12. Local sweep notes (run 5, 2026-10-18)
- **Template motion:** the Green group wording ("write to the Prime Minister and the Chancellor urging an immediate introduction of a national wealth tax", 1% above £10m and 2% above £1bn, plus better HMRC/ONS data on high-wealth individuals) was used at Hackney (29 Jan 2025, not carried) and Lambeth (15 Oct 2025, not carried). Search for this wording elsewhere.
- **Readable council records:** hackney.moderngov.co.uk and many other ModernGov sites return HTTP 403 to automated fetches. Open Council Network (opencouncil.network/councils/<name>/committees/council, then /meetings/<id>) shows meeting summaries and decision records and could be fetched; its text is AI-generated from the council record, so cite it as such and re-check the minutes when reachable.
- **Elections:** London borough elections took place in May 2026 and Lambeth now has Green cabinet members; earlier motions may have been repeated, and some may have passed. Sweep 2026 meetings for every borough.
- **A failed motion** does not make the council a supporter; the proposer, seconder and speakers are recorded as individuals (Zoë Garbett, Penny Wrout, Scott Ainslie, Martin Abrams) and the Green groups as organisations.

## 13. Local sweep notes (run 7, 2026-10-18)
- **Passed motions so far:** Calderdale Council, 9 Apr 2025 (Green motion, amended; national wealth tax on the richest 1%); Islington Council, 4 Dec 2025 (motion advocating wealth taxes, text unread). Failed: Hackney (29 Jan 2025), Lambeth (15 Oct 2025). Unknown: Newham (10 Nov 2025 Green motion), Leeds (Green amendment 12 Nov 2025).
- **Scanner limits:** Open Council Network covers most London boroughs from 2009 but most northern English councils only from about Feb 2024. Summaries are AI-generated and a motion listed only as a document title may not trigger the keyword scan. Use `opencouncil.network/decisions/ID` pages for decision text. Rate limit: one request per 0.9 s (a 429 appears if you go faster).
- **Blocked sites:** *.moderngov.co.uk, democracy.islington.gov.uk and some others return 403 or a bot check to automated fetches; I did not try to bypass them.
- **Leads:** Fermanagh and Omagh District Council wealth tax motion (Oct 2021, to be sent to the Executive, PM and Chancellor); Scottish Parliament 4 Jun 2026 motion S7M-00249 and amendments; Senedd debate 19 Nov 2025.

## 14. Local sweep notes (run 8, 2026-10-18)
- **English councils:** 206 scanned on Open Council Network from 2022, no new wealth tax motion found beyond Hackney, Lambeth, Islington, Newham, Calderdale and Leeds. Detection is weak where the site has no meeting summaries (180 of 264 councils): only attendee lists and document titles are searchable. Those units are in_progress, not done.
- **Councils not on Open Council Network (about 37 English ones):** a handful were checked with one web search each (Norwich, Warrington, Colchester, Chelmsford, Luton, Warwick, Derby, Hartlepool, Stockton-on-Tees and five counties) with nothing found; the rest have not been searched.
- **Scanner:** `skill/scripts/adapters/gb_ocn_scan.py` (was `scripts/ocn_scan.py`) now filters to meetings from 2022 (set OCN_MIN_YEAR) and lists councils' full-council committees by name pattern; councils with unusual committee names need `slug:committee` arguments.

## 15. Layer pass notes (run 9, 2026-10-18)
- **Civil society:** the Bond letter of 27 Feb 2025 (146 INGO leaders) is the largest single source of civil-society supporters; its wealth tax paragraph is a side argument in a letter about aid cuts. Tax Justice UK, Oxfam GB, Christian Aid, Save the Children and others signed through their leaders.
- **Unions:** Unite (1% over £4m, Sept 2024), the RMT, and the TUC (2024 and 2025 Congress motions). Unresolved: Unison, GMB, NEU, CWU, TSSA, Usdaw, PCS, FBU (FBU, Unite, CWU and TSSA backed a Labour conference 2025 motion; source blocked).
- **Academics and economists:** July 2025 letter (36), Wealth Tax Commission authors, Patrick Diamond and Colm Murphy (QMUL), Tippet and Zucman (2026 report). Lead: CenTax (Advani and Summers) has published a framework for a tax on £10m (per Patriotic Millionaires UK) — read the CenTax page.
- **Politicians outside the EDMs:** Lord Kinnock (2% above £10m, July 2025); Andy Burnham has not ruled it out (not recorded as support).
- **Journalists:** none recorded. The search tool returns news, not columns. Try columnist author pages directly (Guardian, New Statesman, Tribune, Mirror, Novara, Byline Times) with opinion-piece quotes.
- **Business and faith:** only the Proud to Pay signers and Church Action for Tax Justice so far.

## 16. Scotland, Wales and Northern Ireland notes (run 10, 2026-10-18)
- **Parties:** SNP conference (Oct 2025) backed a local wealth tax motion; Plaid Cymru (Jul 2025) backs a 2% tax over £10m; Scottish Greens (2024, 2026); Welsh Liberal Democrats (Nov 2025). Labour in Wales (Drakeford) opposed a Wales-only wealth tax and favours land value tax.
- **Unions:** STUC Congress 2024 motion to initiate plans for a wealth tax in the local tax system.
- **Councils:** Fermanagh and Omagh (5 Oct 2021) is the only council motion found in these nations; Open Council Network covers only 29 of 65 councils and many have thin coverage.
- **Scottish Parliament 4 June 2026:** the agreed motion and amendments were about private jet and mansion taxes, council tax and business rates, not a tax on net wealth.

## 17. Layer notes (run 11, 2026-10-18)
- **Greens:** the 19 Nov 2025 letter to the Chancellor (greenparty.org.uk PDF) is the best primary source for the party's wealth tax policy (1% over £10m, 2% over £1bn, £14.8bn). It was co-signed by 15 council leaders and deputies, listing the Green-led councils to check: Bristol, Lancaster, Stroud, Hastings, Warwick, Mid Suffolk, Lewes, Maidstone, Forest of Dean, Folkestone and Hythe, East Hertfordshire, East Suffolk, Runnymede; Babergh (deputy).
- **Civil society coalition (19 Nov 2025):** Tax Justice UK, 38 Degrees, Oxfam GB, Greenpeace UK, Patriotic Millionaires UK, Green New Deal Rising, 350, Global Justice Now, the FBU. 575,271 petition signatures delivered to the Treasury.
- **Unions with wealth tax wording found:** Unite, RMT, TUC (2024, 2025), STUC, FBU (graded B). Unison, GMB, NEU, CWU, PCS: nothing found with wealth tax wording.
- **Journalists:** none; the search tool cannot reach the Guardian or find columns.

## 18. Remaining gaps by actor type (run 13, 2026-10-18)
Counts from `wtdb.py status`: journalist 1, media_outlet 0, think_tank 1, funder 0, economist 2, faith 1, legal/tax professional 1, business 4. Most blocked sources need a real browser (Guardian author pages, Church Times, Equality Trust, BMJ, Express and Star, Morning Star archive). The `claude-in-chrome` tools exist in this session and could be used for those pages if the user wants.

## 19. Chrome pass (run 14, 2026-10-18)
- **Faith:** Church Action for Tax Justice's open letter of 18 Oct 2022 (signers include Rowan Williams and Archbishop of Wales Andrew John); Williams backed a wealth tax in Feb 2022. Both read in the Church Times via Chrome.
- **Media:** The Guardian editorials (26 Jul 2020 "necessary but not sufficient"; 23 May 2025 recommending 2% over £10m). Columns: Toynbee, Jones, Shaheen (Tax Justice UK), Knowles, Tippet. Aditya Chakrabortty opposes (exclusions). Morning Star has not been checked for editorials, only news and an article by Richard Burgon.
- **Labour conference 2025:** delegates backed a wealth tax motion submitted by FBU, CWU, TSSA and Unite (Morning Star).
- **Councils read in Chrome:** Bristol (16/18), Lewes, Runnymede, Forest of Dean, Maidstone, 2025-26, nothing found. Moderngov.co.uk sites remain behind a Cloudflare block even in Chrome.

## 20. Petitions (run 16, 2026-10-18)
- **Not recorded as supporters:** petition signers are private individuals (rule 5). Only organisers, sponsors and delivering MPs are candidates.
- **UK Parliament e-petitions on a wealth tax** (petition.parliament.uk, read in Chrome): "Introduce a 2% wealth tax on assets over £10 million & tax reform" (1,780 signatures, closed), "Implement a 2% wealth tax on individuals with net assets exceeding £10 million" (1,449, closed), "Commission a Treasury Review on the practicalities of levying a wealth tax" (651, closed) and several smaller open ones. All small; none reached the 10,000 response threshold.
- **Campaign petitions** (read in Chrome, run 17; organisers, wording and totals only, no signers): Tax Justice UK via Campaigns By You (2% over £10m, £24bn; 101,318 of 200,000), 38 Degrees act petition (same design; 104,662 of 200,000), Oxfam GB letter-petition (2% over £10m; counter dynamic), Greenpeace UK (one-off National Renewal Tax over £10m; 92,178), 350.org (national and global wealth taxes; no count), Richard Burgon's 80,000 petition (Morning Star). Tax Justice UK's release of 19 Nov 2025 gives 575,271 signatures delivered across partners (its petition page update says over 724,000 in total). Two further 38 Degrees petitions were not opened.
- **EDM 1725** was re-read on the official edm.parliament.uk page in Chrome: 53 signatures, 0 withdrawn, all matching the Beyond the Vote mirror. The mirror's unnamed "Member 1506" is Andrew Gwynne (13 Nov 2025); fixed.

## 21. Think-tank gap fill (run 18, 2026-10-18)
- **Added:** Compass (2026 paper, yearly 2% over £10m), Economic Change Unit and NEF (May 2023 joint 2% analysis with Tax Justice UK), plus NEF economist Lukasz Krebel and Robert Palmer (Tax Justice UK, 2023). Rows are verified=n: read through a summarising fetch, not the originals.
- **Not recorded (no wealth tax position found):** IPPR (taxes income from wealth like work), Fairness Foundation (progressive tax principles only), Demos (property, CGT, exit tax), Positive Money, Class, Common Wealth. The Law360 May 2026 item on a think tank saying the UK already leads the OECD is an opponent-side lead, name unconfirmed.

## 22. Thin-cell gap fill (run 19, 2026-10-18)
- **Added:** John Muellbauer (0.5% annual property wealth tax replacing top council tax bands; partial_wealth), Gary Stevenson and Julia Davies (evidence upgrades), Green New Deal Rising (grade A campaign page). Julia Davies reclassified as business_leader.
- **Excluded:** Charlie Mullins (WeFix founder) opposes the Patriotic Millionaires approach (X0028).
- **No hits:** funders (Rowntree, Barrow Cadbury, Oak, Esmee Fairbairn; Patriotic Millionaires UK's funding not public in results), media editorials (Mirror, Tribune, Byline Times, New Statesman, Independent), Guardian columnists beyond those already recorded.
- **Correction:** Richard Murphy was first logged as grade B, then removed and excluded (X0029) on the user's correction: he generally opposes a separate wealth tax and prefers closing loopholes.

## 23. Influencers (run 20, 2026-10-18)
- **Gary Stevenson** (Gary's Economics, about one million followers on YouTube per the New Statesman) now typed journalist (video commentary) with three more rows: New Statesman op-ed describing his advocacy, a New Statesman podcast on his lobbying of the new government, and his own Millionaires for Humanity statement.
- **Jeremy Corbyn:** 2023 statement for a 1-2% wealth tax on assets over £10m added.
- **Leads not added:** Aaron Bastani, Grace Blakeley, Paul Mason, Mehdi Hasan, Ash Sarkar, Jolyon Maugham, Will Hutton, Mariana Mazzucato (questioned the Green plan in Jan 2026).
