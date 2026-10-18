# United Kingdom — levels, sources and the local sweep

A worked example. Other countries' notes can follow the same shape (add `references/countries/<country>.md`). Check every URL still works and every structural fact is current before relying on it; government structures change.

## Levels of government and the geography register

Load every unit into `geo_units.csv`, from the official current lists, with `parent_id` so the sweep can be finished region by region:

| Level (`level`) | Units | Notes |
|---|---|---|
| national | UK Parliament (Commons, Lords) | |
| devolved | Scottish Parliament, Senedd Cymru (Wales), Northern Ireland Assembly | Each has its own record of debates, motions and votes |
| region | The 9 English regions, plus Scotland, Wales and Northern Ireland as parents | Used to group the sweep |
| combined_authority | Combined authorities and mayoral strategic authorities; the Greater London Authority (Mayor and London Assembly) | Metro mayors and assemblies pass motions |
| county | County councils (two-tier areas) | Parent of their district councils |
| council | Every principal council: unitary, metropolitan borough, London borough, district; Scotland's 32 councils; Wales' 22 principal councils; Northern Ireland's 11 district councils | The core of the sweep |
| sub_council | Town and parish councils (England), community councils (Scotland, Wales) | Thousands; sweep only if the profile puts them in scope |

Official lists: the ONS Open Geography Portal (Local Authority Districts and Counties for the current year), GOV.UK's list of local councils, the Scottish, Welsh and Northern Ireland government lists. Cross-check against a second list (e.g. Wikipedia's lists of councils by type) and note recent reorganisations (local government reorganisation in England is ongoing: councils are being merged into new unitaries, so check the current year).

**Sweep order suggestion:** London boroughs → metropolitan boroughs (Greater Manchester, West Yorkshire, Merseyside, South Yorkshire, West Midlands, Tyne and Wear) → large unitaries and cities → Scotland → Wales → Northern Ireland → county and district councils. Finish one region before starting the next.

**Wording to look for locally:** councils cannot levy a wealth tax, so local support usually takes the form of a motion asking the council to "write to the Chancellor / Prime Minister calling for a wealth tax" or "tax on extreme wealth". The proposer and seconder are supporters even if the motion failed; the council is a `government_body` supporter only if it passed.

## Sources

**UK Parliament**
- Debates: Hansard (hansard.parliament.uk) and TheyWorkForYou (theyworkforyou.com), searchable by phrase and member
- Early day motions and signatories: edm.parliament.uk (bulk list source)
- Votes: votes.parliament.uk (Commons and Lords divisions)
- Bills: bills.parliament.uk
- Written questions: questions-statements.parliament.uk
- Committees and written evidence: committees.parliament.uk

**Devolved and London**
- Scottish Parliament: official report, motions (with supporters), votes — parliament.scot
- Senedd: Record of Proceedings, motions — senedd.wales (search in English and Welsh)
- Northern Ireland Assembly: Official Report, motions — niassembly.gov.uk
- London Assembly motions and Mayor's statements — london.gov.uk

**Councils**
- Council websites (meeting minutes and motions; many use the ModernGov platform, whose sites can be searched by keyword)
- Local Democracy Reporting Service stories in local papers
- Local party groups' websites and social pages (Green, Labour, Lib Dem, SNP, Plaid, independent and socialist groups)
- Trades union councils

**Parties:** manifestos for the 2010, 2015, 2017, 2019 and 2024 general elections, and the devolved and local elections; party and youth-wing conference motions.

**Unions:** TUC Congress motions and composites; Scottish TUC; Wales TUC; Irish Congress of Trade Unions (Northern Ireland); individual unions' policy pages.

**Registers:** Electoral Commission donations; Companies House; Charity Commission (England and Wales), OSCR (Scotland), Charity Commission for Northern Ireland; 360Giving GrantNav (grants to wealth-tax work); Register of Members' Financial Interests.

**Research, campaigns and media — candidates to check (not assumed supporters):**
- Research: the Wealth Tax Commission (2020) and its evidence papers and authors; CenTax; LSE International Inequalities Institute; university inequality and tax researchers
- Think tanks: IPPR, New Economics Foundation, Common Wealth, Compass, Fabian Society, Fairness Foundation, Resolution Foundation (check their actual positions)
- Campaigns: Tax Justice UK, Patriotic Millionaires UK, Oxfam GB, the Equality Trust, Tax Justice Network, Friends of the Earth, Greenpeace UK, 38 Degrees, People's Assembly, Positive Money, faith-based anti-poverty groups
- Media opinion: national comment sections (Guardian, Observer, i, Mirror, New Statesman, Tribune, Novara, Byline Times and others), regional papers' comment pages, podcasts and video commentators

## Notes from the first UK attempt
- Green councillors frequently propose a template motion (1% on assets over £10m, 2% over £1bn) — searching for that wording finds many councils at once.
- Some councils debated motions that failed; the proposers still count.
- "Tax wealth like work" in UK usage often means capital gains reform — grade carefully.
