# Source playbook

Layers, the sources that work for each, and query templates. Replace `{TERM}` with each search term for the area's languages (table at the end), `{AREA}` with the area name, `{UNIT}` with a geography unit name, and `{DOMAIN}` with a site's domain. Use quotation marks around exact phrases. Always open the page itself; a search snippet is not evidence.

Named organisations below are **candidates to check**, not assumed supporters: each must meet the definition with its own evidence.

---

## Bulk lists first (harvest)

These produce many actors at once. Queue every one you find in `harvest.csv`.

| List | Where to find it | Query ideas |
|---|---|---|
| Roll-call votes on wealth-tax bills or amendments | Parliament vote records; vote trackers (e.g. HowTheyVote.eu for the European Parliament) | `{TERM} amendment vote {AREA}`, `{TERM} bill division` |
| Bill sponsors and co-sponsors | Parliament bill pages | `{TERM} bill cosponsors`, `"{TERM}" private member's bill` |
| Signatories of parliamentary or council motions | Motion registers (e.g. UK early day motions) | `"{TERM}" motion signatures` |
| Open letters | Campaign sites, newspapers that published them | `open letter "{TERM}" signatories`, `economists letter "{TERM}"`, `millionaires letter "tax us"` |
| Coalition and campaign members | "Our members" or "supporters" pages of coalitions | `"{TERM}" coalition members`, `campaign "{TERM}" "supported by"` |
| Report and commission authors | Report title pages, commission websites | `"{TERM}" commission report authors {AREA}` |
| Evidence to commissions and committees | Committee written-evidence pages | `"{TERM}" written evidence committee` |
| Conference motions | Union and party conference agendas and reports | `congress motion "{TERM}"`, `conference composite "{TERM}"` |

International lists worth checking for every area (for actors from that area): the Patriotic Millionaires and Millionaires for Humanity letters to world leaders; the "Proud to Pay More" letters; economists' letters supporting the G20 billionaire minimum tax; the European Citizens' Initiative "Tax the Rich" (organisers and partner organisations); Tax Justice Network and Global Alliance for Tax Justice member lists; Oxfam national affiliates.

---

## Layers

### L1 Legislatures (national, devolved, regional, supranational)
- Debate records (Hansard-type): search for each term; record speakers who argued for it.
- Written and oral questions calling for it.
- Votes, bills, motions: see bulk lists.
- Committee reports and witnesses.
- Queries: `site:{PARLIAMENT_DOMAIN} "{TERM}"`, `"{TERM}" MP speech {AREA}`, `"{TERM}" senator OR deputy {AREA}`

### L2 Parties
- Manifestos since 2010 (national and regional elections); the Manifesto Project corpus helps for older ones.
- Conference motions, policy documents, youth-wing and council-group positions.
- Queries: `"{TERM}" manifesto {YEAR}`, `party conference "{TERM}" motion passed`, `"young" party "{TERM}"`

### L3 Executive and government bodies
- Government programmes and coalition agreements; ministers' statements; tax commissions and their recommendations.
- Queries: `coalition agreement "{TERM}"`, `minister "{TERM}" {AREA}`, `tax commission recommends "{TERM}"`

### L4 Sub-national and local (see the local sweep pack below)

### L5 Academia and economists
- Scholarly search (OpenAlex, Google Scholar, SSRN, RePEc) for papers recommending a wealth tax for the area; then check the author's own conclusion.
- Authors of books and policy reports; university research centres on inequality or tax.
- Economists' open letters (bulk).
- Queries: `"{TERM}" {AREA} working paper recommend`, `"case for a wealth tax" {AREA}`, `economist op-ed "{TERM}"`

### L6 Think tanks
- Publications pages; "our proposals" pages; responses to budgets.
- Queries: `think tank "{TERM}" {AREA} report`, `site:{DOMAIN} "{TERM}"`

### L7 Civil society: NGOs, campaigns, coalitions, charities
- National branches of tax-justice, anti-poverty, climate and development NGOs; campaign coalitions; charities speaking on inequality.
- Queries: `campaign "{TERM}" {AREA}`, `"tax the super-rich" campaign {AREA}`, `climate "{TERM}" campaign {AREA}`

### L8 Unions
- Confederation congress motions; each major union's policy pages and leaders' speeches; trades councils (local).
- Queries: `union "{TERM}" {AREA}`, `general secretary "{TERM}"`, `trades council "{TERM}"`

### L9 Media (opinion only)
- Opinion and comment sections of national and regional outlets; columnists' archives; editorials ("Our view", "The Guardian view on…" style); podcasts and video commentators with a public profile.
- Queries: `site:{OUTLET_DOMAIN}/commentisfree "{TERM}"`, `opinion "{TERM}" {AREA}`, `editorial "{TERM}"`, `column "why we need a wealth tax"`

### L10 Legal and tax professionals
- Professional tax journals and blogs; submissions to commissions; law-firm and chambers commentary; former tax-authority officials writing in favour; professional bodies' consultation responses.
- Queries: `tax barrister OR "tax lawyer" "{TERM}" in favour`, `former tax official "{TERM}"`, `accountant "{TERM}" design {AREA}`

### L11 Wealthy individuals and business
- Members and signatories of Patriotic Millionaires, Millionaires for Humanity, taxmenow (German-speaking countries), Proud to Pay More; business leaders' statements; business associations.
- Queries: `millionaire "tax me" {AREA}`, `billionaire supports "{TERM}"`, `CEO "{TERM}" {AREA}`

### L12 Faith, culture and other public figures
- Statements by church and faith bodies; artists', athletes' and writers' letters and statements.
- Queries: `bishop OR church "{TERM}"`, `actor OR musician "{TERM}" {AREA}`

### L13 Funders
- Grant databases (360Giving in the UK; Candid in the US; foundation annual reports elsewhere) for grants to wealth-tax work; funders listed on reports.
- Queries: `grant "wealth tax" foundation`, `"funded by" "{TERM}" report`

### L14 International and supranational
- UN tax convention process; IMF, OECD, World Bank and G20 documents; European Parliament and Commission; EU Tax Observatory; ICRICT.
- Include in an area's database only when the actor acted in or towards that area.

### L15 Polling and petitions
- Use only to find **organisations or public figures** who commissioned a poll or launched a petition. Never record private signatories.

---

## Local sweep pack (run for every geography unit)

1. `"{TERM}" "{UNIT}" council motion`
2. `"{TERM}" "{UNIT}" councillor`
3. `site:{COUNCIL_DOMAIN} "{TERM}"` (and the council's own minutes search, if it has one)
4. `"{UNIT}" council "tax the super-rich" OR "tax the rich" motion` (finds C-grade and leads to minutes)
5. `"{UNIT}" trades council OR "union branch" "{TERM}"`
6. `"{UNIT}" Green OR Labour OR Socialist (or the area's relevant parties) group "{TERM}"`
7. Local newspaper sites for the unit: `site:{LOCAL_NEWS_DOMAIN} "{TERM}"`

Record the number of queries run and hits on the unit. Failed motions still identify the proposer and seconder as supporters.

---

## Search terms by language

Use all applicable terms, plus the area's own name for any specific proposal (bill names, initiative numbers, "taxe Zucman").

| Language | Terms |
|---|---|
| English | wealth tax · net wealth tax · wealth levy · billionaire tax · billionaire minimum tax · tax on extreme wealth · tax the super-rich · "1% wealth tax" / "2% wealth tax" |
| Swedish | förmögenhetsskatt · skatt på förmögenhet · miljardärsskatt |
| Norwegian | formuesskatt · formueskatt |
| Danish | formueskat · milliardærskat |
| Finnish | varallisuusvero |
| German | Vermögensteuer · Vermögenssteuer · Vermögensabgabe · Milliardärssteuer · Reichensteuer (check: often means income tax) |
| French | impôt sur la fortune · ISF · taxe Zucman · impôt plancher · taxe sur les milliardaires · impôt sur les grandes fortunes |
| Spanish | impuesto sobre el patrimonio · impuesto a las grandes fortunas · impuesto de solidaridad · impuesto a los milmillonarios |
| Catalan | impost sobre el patrimoni |
| Italian | patrimoniale · imposta patrimoniale · tassa sui miliardari (check: *patrimoniale* can mean property taxes) |
| Portuguese | imposto sobre grandes fortunas · IGF · taxação dos super-ricos · imposto sobre a riqueza |
| Dutch | vermogensbelasting · miljonairsbelasting · miljardairsbelasting (check: may refer to the savings box) |
| Polish | podatek majątkowy · podatek od bogactwa |
| Welsh | treth cyfoeth |
| Irish | cáin rachmais |

If the area uses a language not listed, build the term list in the area profile first, from the area's own news coverage of wealth taxes.
