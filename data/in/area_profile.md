# Area profile — India

Run R001, 2026-10-20. Seed pass. Facts marked [verify] come from a search summary only.

## 1. Scope
- Area: India (country). Depth: **seed**.
- Levels in the register: the Union, 36 states and union territories, and 734 districts (the map tier, with Local Government Directory codes). Actors are placed at the Union level so far; no state or district body was searched.
- Languages to search in: English first; Hindi (संपत्ति कर, धन कर, विरासत कर) and Malayalam, Bengali and Tamil for the Left parties' state organs. Only English was used in R001.
- R002 added: the Tax the Top campaign sites (taxthetop.org via the headless browser; taxtherichin.wordpress.com and its nine-part 2023 op-ed series), the petition press statement, the 2024 joint memorandum of ten central trade unions, the Left parties' joint Budget statement (Feb 2025), the CPI(M) and CPI(ML) manifestos and Central Committee texts, the Rozgar Adhikar Abhiyan conference report in Hindi, and Hindi, Bengali, Malayalam and Tamil searches. Generic Hindi and Bengali searches mostly returned Bangladeshi, explainer or tax-collection pages: the useful Hindi and Bengali pages (Nyay Tak, cpimwestbengal.org) were found by following named people and organisations from English sources, so that is the method to repeat.
- Left out: Hindi-language media and party documents, state assemblies (Kerala, West Bengal, Tamil Nadu above all), Lok Sabha and Rajya Sabha debates, union congress resolutions, Parliament standing committees.

## 2. Wealth tax history and live proposals (2010 onwards)
- India had a Wealth-Tax Act, 1957. It was abolished in the Union Budget of February 2015 and ceased to apply from assessment year 2016–17; the criticism that followed is the earliest dated support in the file (Prakash Karat, 1 March 2015) [verify the abolition date against the Finance Act, 2015].
- Government position: Finance Minister Sitharaman has argued against an inheritance tax, and Chief Economic Adviser Nageswaran warned of capital outflows (Business Today, 15 Dec 2024).
- May 2024: the World Inequality Lab issue brief by Bharti, Chancel, Piketty and Somanchi proposes a 2% annual tax on net wealth above Rs 10 crore and a 33% inheritance tax (baseline), raising about 2.7% of GDP [source: the brief].
- April 2024 election: CPI(M) and CPI manifestos named wealth and inheritance taxes. Congress did not (Jairam Ramesh and a fact-check say so), but its leaders called for a 2% tax on billionaires in July and September 2024 ahead of the G20.
- March–April 2026: Wealth Tracker India 2026, from the Centre for Financial Accountability and the Tax the Top campaign, urges a 2%–6% levy on 1,688 people with more than Rs 1,000 crore.
- April 2020: a group of about 50 Indian Revenue Service officers floated a temporary wealth tax as an option; the board disowned the paper.
- Polls: the only India figure found is a 2021 Fight Inequality Alliance India survey (3,231 people, 24 states) that more than 80% support taxing the rich and pandemic profiteers. That is a tax on "the rich", not a wealth tax, so it is not in `meta.json` `polls`.

## 3. Legislatures and where their records are
- Lok Sabha and Rajya Sabha: swept in R002 for every sitting day since 2010 (see `skill/references/countries/in.md` for the APIs). Result: no motion or bill with named sponsors since 2015, but 24 speeches by 22 MPs from the CPI(M), CPI, Congress, TMC, BJD, NCP(SP) and DMK (grades A to C), mostly in Budget and Finance Bill debates. Written questions were not read. Hindi-language speeches are not searchable.
- No wealth-tax private member's bill was found in a first search; the Parliament private-members' lists were not read.

## 4. Parties
- CPI(M): 2024 manifesto names a general wealth tax and an inheritance tax (cpim.org). CPI: same, via PTI coverage. CPI(ML) Liberation, RSP, Forward Bloc, DMK, TMC, AAP, SP, RJD and the Congress state branches not read.

## 5. Government below national level
- States run most services but the Constitution places taxes on capital value (outside agricultural land) with the Union (Entry 86 of the Union List) [verify], so states can only lobby; Kerala and Tamil Nadu are the likeliest states to speak.
- Districts are administrative units, not elected bodies in most of India; municipal and panchayat bodies sit below them and were not loaded. The register therefore stops at districts: **local decision: skip**, until the state pass shows motions exist.

## 6. Search terms
- English: wealth tax, inheritance tax, estate duty, billionaire tax, super-rich tax, "tax the rich", "Tax the Top".
- Hindi: संपत्ति कर / धन कर (wealth tax), विरासत कर (inheritance tax). Watch "wealth tax" used for the old Wealth-Tax Act in historical pieces, and "super-rich surcharge", which is an income-tax surcharge and is out of the definition.

## 7. Media
- The Wire, Scroll, The Hindu, Frontline, Janata Weekly, People's Democracy (CPI(M)), Newsclick, Down To Earth. Opinion pieces by economists in these outlets are the likeliest source of further `economist` and `journalist` rows.

## 8. Registers
- Not checked: Lobbying is not registered in India; donations via the Electoral Bonds scheme are not relevant.

## 9. Known networks
- Tax the Top campaign and its partners; Fight Inequality Alliance India; Oxfam India; the Left parties and their unions (CITU, AITUC, AIKS) and the Centre for Financial Accountability. The campaign's website (taxthetop) was not reachable from the sandbox, so its partner list is the top harvest target.

## 10. Plan for the next runs (ordered by expected yield)
R002 did items 1 and 2 in part; the order after R002 is in `notes_next` of the R002 row. Why India has fewer rows than Germany's first pass: Germany's count came from named sponsors on Bundestag motions (a bulk list that exists in the record). India has no wealth-tax motion or bill with named sponsors since 2015, so supporters are found through campaigns, party documents and signed statements; the largest remaining bulk list, the Tax the Top petition (about 100 signers), is not published in full.
1. **Tax the Top petition**: the press statement says about 100 signed but names 13; find the full signature list (not on taxthetop.org's front page; ask the campaign, or look for the petition on a petition site) and the 'more than 20 organisations' that took part. Expected 80+ people.
2. **Unions and mass organisations**: AIKS, SFI, AIDWA and union congress resolutions; the ten central unions' memoranda for other years (2025, 2026); CPI(M) and CPI MPs' speeches in `rsdebate.nic.in` and `sansad.in` (full-text search needed). Expected 10–30 rows.
3. **Economists and commentators**: Jayati Ghosh, C. P. Chandrasekhar, Arun Kumar, Himanshu, Sudipto Mundle, R. Nagaraj and others in The Wire, Scroll, Frontline; each needs a page where they argue for the tax.
4. **Congress**: Jairam Ramesh's September 2024 G20 statement, Rahul Gandhi's survey speeches, any Congress MP speeches. Upgrade Ramesh from B.
5. **Hindi and regional-language sources**, state assemblies, municipal bodies: only if 1–4 show support lives there.
6. QIDs and `profiles.csv`: fill Wikidata IDs for the people added (the API rate-limited the sandbox).
7. Map: district codes in `boundaries.json` are assigned in this project (state code plus running number) because no official-code source with open shapes was found; swap in Local Government Directory (LGD) codes. The shapes are the Census 2011 districts with later changes; newer districts are missing.
