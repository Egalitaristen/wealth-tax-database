# Area profile — United States

First drafted 2026-10-19 (run R001). Lines marked **[verify]** come from a search-result summary only and must be opened and confirmed before they are relied on.

## 1. Scope
- Area: United States; type: country (federal, with states)
- Levels in scope: national (Congress, federal executive), regional (50 states and DC: legislatures, governors, ballot measures). Local (county, city, school board): **not in scope for now**.
- Languages: English; Spanish for state and local media where relevant.
- Date of first run: 2026-10-19

## 2. Wealth tax history and live proposals (2010 onwards)
- **Ultra-Millionaire Tax Act** (Warren; House: Jayapal, Boyle), introduced 2021-03-01: 2% annual tax on net worth of $50m to $1bn plus 1% surtax above $1bn; cosponsored in the Senate by Sanders, Whitehouse, Merkley, Gillibrand, Schatz, Markey, Hirono. Source: [Warren press release](https://www.warren.senate.gov/newsroom/press-releases/warren-jayapal-boyle-introduce-ultra-millionaire-tax-on-fortunes-over-50-million). Reintroductions in later Congresses: **[verify]** on Congress.gov.
- **Billionaires Income Tax** (Wyden, 2023): annual tax on unrealised gains of billionaires; 15 Democratic cosponsors **[verify]** ([NAIOP summary](https://naiop.org/advocacy/news/2023/senate-democrats-introduce-tax-on-unrealized-capital-gains)).
- **California 2026 Billionaire Tax Act (Prop 40):** one-time 5% tax on net worth above $1bn, on the November 2026 ballot; proponent SEIU-UHW; endorsed by the California Democratic Party in early August 2026 against Gov. Newsom's opposition. Source: [ABC7, 2026-08-04](https://abc7news.com/post/despite-gov-gavin-newsoms-opposition-california-democrats-endorse-prop-40-billionaire-tax-measure/19621890/). Other named backers (Sanders, Khanna, Chu, California Federation of Labor, California Nurses Association) are **[verify]**.
- **State bills:** Washington S.B. 5486 / H.B. 1473 (2023), 1% over $250m **[verify]** ([Deloitte](https://www.deloitte.com/content/dam/Deloitte/us/Documents/Tax/us-tax-multistate-tax-alert-wealth-tax-bills-proposed-in-several-states.pdf)); several other states introduced bills in 2023 **[verify]**.
- **Excluded, do not count:** Massachusetts millionaires surtax (2022; an income surtax) and Maryland income-tax changes.

## 3. Legislatures and records
- Congress: bills and cosponsors at congress.gov; roll calls at senate.gov and clerk.house.gov.
- States: each legislature's bill and committee pages (listed in `geo_units.csv`).

## 4. Parties
- Democratic Party, Republican Party, Green Party, Working Families Party, independents. Check platforms and state party resolutions (California Democratic Party endorsed Prop 40).

## 5. Government below national level
- 50 states and DC loaded as G0003–G0053. State constitutions differ on taxing wealth (uniformity clauses), which is why many state proposals are ballot measures or constitutional amendments.

## 6. Search terms
- wealth tax · billionaire tax · ultra-millionaire tax · "tax on unrealized gains" · "billionaires minimum income tax" · "mark-to-market" · "tax the billionaires"
- Watch: "millionaires tax" and "surtax" are usually income taxes (excluded); "tax the rich" alone is not enough.

## 7. Media
- To be listed. Opinion sections of national papers, plus state outlets (CalMatters, Seattle Times) for state measures.

## 8. Registers
- Candid (foundation grants), OpenSecrets and state ethics commissions (ballot committees), California Secretary of State campaign finance.

## 9. Known networks (candidates to check, not assumed supporters)
- Patriotic Millionaires, Americans for Tax Fairness, Institute on Taxation and Economic Policy, Institute for Policy Studies, Oxfam America, Tax Justice Network, EU Tax Observatory/Zucman (only where acting in the US), SEIU, California Federation of Labor.

## 10. Notes for future runs
- Order: H0004 (Prop 40 endorsers, time-sensitive before November), H0002/H0003 (Congress.gov), H0005 (Patriotic Millionaires), H0006 (economists' letters), H0007 (state bills).
- Quotes are checked by fetching the raw page; the WebFetch tool summarises and can paraphrase.

## State-by-state sweep (R005, 2026-10-19)
One search per state (50 states plus DC) for wealth tax, billionaire tax or net worth tax proposals. This replaces the earlier note that no other state had a measure: the Oregon initiative below was missed by the first searches. Results come from search summaries, so each item is a lead and is queued in `harvest.csv` (H0014 to H0025) to be opened and sourced.

**Net-wealth or unrealised-gains designs (qualify):**
- **Oregon:** IP 70, the Very Rich Pay Their Fair Share Act (Jonathan Tasini): 2% a year on assets of residents worth $30m or more. Stalled in 2026 and not on the ballot ([Northwest Labor Press](https://nwlaborpress.org/2026/08/oregon-wealth-tax-initiative-campaign-stalls/)); initiative text at [Tax the Very Wealthy](https://taxtheverywealthy.com/the-initiative/). A coalition of progressive groups and unions plans a 2028 measure ([States Newsroom](https://washingtonstatestandard.com/?p=17425)); its design is unconfirmed.
- **Hawaii:** SB 925 (2023), SB 313 (2025) and HB 1235 (2026): 1% a year on net worth over $20m; Sen. Karl Rhoads.
- **Minnesota:** HF 4616 (Rep. Aisha Gomez): 1% on wealth over $10m, heard in committee, not in the final tax bill.
- **Rhode Island:** S2361 (2026): 1% of worldwide wealth, $25m exempt; Sen. Tiara Mack and Rep. Brandon Potter. Referred to committee.
- **New York:** S1570 / A3252 Billionaire Mark-to-Market Tax Act (2023-24).
- **Illinois:** SB 3376 (Sen. Karina Villa) applies income tax to the growth in billionaires' assets; backed by the Illinois Revenue Alliance (labor and community groups).
- **Maryland:** HB 1238 (2026), titled Ultra-High-Net-Worth Individual Surtax and Wealth Tax.
- **Vermont:** 2024 bill (Rep. Emilie Kornheiser) on unrealised gains above $10m net worth.
- **Washington:** done for 2025-26 (H0010); 2023-24 bills queued.
- **A coordinated push** by lawmakers in CA, CT, IL, HI, MD, NY and WA filed bills together (Common Dreams); the Connecticut bill is not yet identified.

**Processed in R006 (state bills, harvests H0014 to H0022):** sponsors recorded for Hawaii SB 313 and SB 925, Illinois SB 3376, Maryland HB 1238, Minnesota HF 4616, New York S1570 and A03252, Rhode Island S 2361, Vermont H.827, and the Oregon initiatives (IP 70 in 2026; the "Financial Assets Tax on Multimillionaires" coalition initiative planned for 2028, 1 to 1.2% a year on financial assets of taxpayers with net worth of $30m or more, per [OPB](https://www.opb.org/article/2026/10/08/oregon-wealth-tax-2028-ballot/)). Gaps: Hawaii's and Illinois's official sites could not be read (Cloudflare block; certificate error), the New York 2025-26 versions were not checked, and parties are only filled where a roster was read (Illinois, Maryland, Minnesota).

**Income-tax measures (do not qualify, listed so they are not re-checked):** Maine 2% surcharge over $1m (law, 2026); Rhode Island millionaire's income tax (law, 2026); Washington 9.9% millionaire's tax; Massachusetts surtax; Michigan "fair share" surcharge (shelved initiative and July 2026 resolution); Colorado Initiative 195 graduated income tax; Virginia HB 188 and HB 979; North Carolina HB 1073; Connecticut, New Jersey, Louisiana, Utah, Nebraska, Kentucky, Montana, Idaho and Arizona income-tax proposals; DC councilmember Nadeau's 3% surtax on investment income (tax on income from assets, not on net wealth).

**Think-tank only (ITEP "wealth proceeds tax" reports, no bill found):** Arkansas, Virginia, West Virginia. A wealth proceeds tax is a tax on investment income, so it would not qualify even if introduced.

**No wealth-tax proposal found:** Alabama, Alaska, Delaware, Florida, Georgia, Indiana, Kansas, Mississippi, Missouri, Nevada, New Hampshire, New Mexico, North Carolina, North Dakota, Ohio, Oklahoma, South Carolina, South Dakota, Tennessee, Texas, Utah, West Virginia, Wisconsin, Wyoming. Texas voters adopted a constitutional ban on net worth taxes in 2023. A thin search does not prove absence; legislature bill trackers have not been searched.

**Federal-candidate and campaign statements to harvest:** Iowa state senator and US Senate candidate Zach Wahls (May 2026); Pennsylvania legislators (April 2026).

## Findings on other states' ballot measures and bills (R004)
- **Ballot measures:** the Tax Foundation's 2026 list ([source](https://taxfoundation.org/research/state-tax/2026-state-tax-ballot-measures/)) describes California Prop 40 as the first US wealth tax to reach a ballot. No other wealth-tax ballot measure was found. Other states' union-backed measures are income taxes, which do not qualify: Washington's 9.9% "millionaire's tax" (referred to voters in 2026), Massachusetts's income surtax (2022) and its 2026 Question 5, and California's Prop 3 (extends high income tax rates).
- **DSA:** Ballotpedia ([source](https://news.ballotpedia.org/2026/10/13/democratic-socialists-of-america-dsa-takes-positions-on-22-state-and-local-ballot-measures-ahead-of-the-nov-2026-election/)) reports DSA took positions on 26 measures; the only wealth-tax measure among those it names is Prop 40 (supported), and it opposes Props 41 and 42, which would undo Prop 40. Its California chapters (state, East Bay, Long Beach) campaign for Prop 40.
- **State bills (these are legislation, not ballot measures):** Washington HB 1319 (Street; 1% a year on financial intangible assets over $100 million) and SB 5797 (Frame; $10 per $1,000 above $50 million), both 2025-26 session, with 18 Democratic sponsors, recorded in H0010. Source: [HB 1319](https://lawfilesext.leg.wa.gov/biennium/2025-26/Htm/Bills/House%20Bills/1319.htm), [SB 5797](https://lawfilesext.leg.wa.gov/biennium/2025-26/Htm/Bills/Senate%20Bills/5797.htm).
- **Still open:** the project lead recalls union and DSA measures elsewhere; if a specific state or year comes to mind, search it directly. Earlier measures such as Massachusetts 2022 were income taxes.

## Sweeps of R009 (2026-10-19)
- **Federal bills and endorsers:** the Ultra-Millionaire Tax Act (2026) is endorsed by nearly 40 unions and groups named in the sponsors' release, with ten leaders quoted; the Make Billionaires Pay Their Fair Share Act (S. 3956 / H.R. 7767, 5% a year above $1bn) is endorsed by NNU and the IAM Union.
- **Economists and academics:** six Nobel-winning economists on Prop 40 (Stiglitz, Diamond, Acemoglu, Banerjee, Duflo, Krugman); the four drafters (Saez, Gamage, Galle, Shanske); Saez and Zucman's signed analysis of the Sanders tax.
- **Think tanks and editorials:** IPS (with Chuck Collins), ITEP, the McClatchy California editorial board (Prop 40). Not recorded: the Roosevelt Institute's "fair share tax" (a redesign of tax on gains and inheritances) and the 2022 and later Davos "tax the rich" letters (no tax on wealth named).
- **Connecticut:** the 2023 coordinated package had no wealth-tax bill in Connecticut (income and capital-gains surcharges only). New York's S165 / A3632 (2025-26) are recorded.
- **Not found:** no wealth-tax bill was introduced in the 116th Congress that the searches could find.

## Sweeps of R020 (2026-10-19)
- **Economists and academics:** the July 2025 Le Monde op-ed of seven Nobel laureates (adds George Akerlof and Simon Johnson; Acemoglu, Banerjee, Duflo, Krugman and Stiglitz also signed). Robert Reich added from the Common Dreams launch report (Oct 2025) and his own Substack (Jan 2026). Not recorded: Madoff, Boushey, Batchelder, Galbraith, Darity, Baker (no wealth-tax statement found in searches); Thomas Piketty (listed on Wikipedia and a State Affairs digest, not added).
- **Candidates:** Graham Platner (Maine, own tax plan), Angie Nixon (Florida, own priorities page), Tony Thurmond (CA), Newsom (supports a national minimum tax on net worth over $100 million while opposing Prop 40). Brad Lander (NY-10) is described as backing a wealth tax by Branch and ABC but his campaign pages did not say so in text; not added.
- **Prop 40 supporters beyond the campaign roster:** the Wikipedia support list was used as a finder and each entry re-read at its cited source: ACLU of Southern California, APEN, Consumer Watchdog, Environmental Health Coalition, TransForm, California CPUSA, DSA San Diego, Los Angeles County Democratic Party, 50501 LA, Monterey County Weekly and Press Democrat editorial boards, Hiltzik, Ward, Rodriguez, Wahab, O'Farrell, Mistah F.A.B. Sources that returned 403 were skipped (Courage California, Democrats Abroad, SF League of Pissed Off Voters, SF Tenants Union, Santa Clara County).
- **Coalition letters:** Americans for Tax Fairness letters for the Billionaires Income Tax (Wyden): Nov 29, 2023 (about 106 signers) and Sept 17, 2025 (about 100 signers, including state groups in AZ, NV, NC, OK, IA, MO, NE, GA, WI, FL, PA, VA, ME, MI). These supply the first records in states that had none.
- **Still thin:** state fiscal-policy groups' own pages (searches found no wealth-tax statements from Policy Matters Ohio, GBPI, NC BTC, Oklahoma Policy Institute), state Democratic party platforms (none found outside California), journalists and columnists (only Meyerson, Case, Hiltzik).

## Sweeps of R021 (2026-10-19)
- **Added:** Abdul El-Sayed (MI Senate candidate, own tax agenda), Hamilton Nolan (own newsletter), Bob Lord (IPS paper).
- **Searched, nothing qualifying:** Michigan, Ohio, Texas, North Carolina, Minnesota Senate candidates other than El-Sayed (no wealth-tax statement found for McMorrow, Stevens, Flanagan, Cooper, Brown); columnists Aleem (critic of Newsom's plan, no own wealth-tax call found), Levitz, Klein, Yglesias; state fiscal-policy groups (Policy Matters Ohio, GBPI, NC BTC, Oklahoma Policy Institute, Wisconsin Budget Project); Indivisible chapters beyond the Sept 2025 letter and the Prop 40 roster; county Democratic parties.
- **Excluded by scope:** the January 2026 Davos "Time to Win" letter (about 400 millionaires; asks generically to "tax the super rich", not a wealth tax); Booker and Van Hollen tax bills (income tax).
- **Blocked (403), not retried:** Axios, Bloomberg Opinion, The Hill, dsausa.org.

