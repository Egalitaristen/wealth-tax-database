# India: no wealth tax since 2015, support concentrated in a few places

A fifth worked example, from a seed pass made with English-language web search only. Check every URL still works before relying on it.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Lok Sabha, Rajya Sabha, Government of India | The Union taxes capital value; the Wealth-Tax Act, 1957 was abolished from the 2015 Budget |
| region | 36 states and union territories | Kerala, West Bengal and Tamil Nadu are the first to search |
| local | 726 districts | The map tier; administrative units, not councils. Municipal and panchayat bodies are not loaded |

**Map:** `data/in/boundaries.json` is built from the compilation `udit-001/india-maps-data` (`topojson/india.json`, via the jsDelivr CDN: `cdn.jsdelivr.net/gh/udit-001/india-maps-data@main/topojson/india.json`). It has the two objects `districts` and `states`. The compiler gives no licence and mixes boundary vintages, and its `dt_code` field repeats, so the district codes in the register are assigned here (state code plus a running number). Replace them with Local Government Directory codes and an official boundary source when one is found. GitHub's own API is blocked from the sandbox but the CDN works; `datameet/maps` raw paths changed and returned 404.

```bash
python skill/scripts/topo_to_boundaries.py india_coded.json --object districts --name-prop district --code-prop code \
  --project lonlat --scale 60 --simplify 0.5 --out units.json
python skill/scripts/topo_to_boundaries.py india_coded.json --object states --name-prop st_nm --code-prop code \
  --project lonlat --scale 60 --simplify 0.8 --out regions.json   # then copy its units into "regions"
```

## What worked and what to watch

- **A single paper carries the economists.** The World Inequality Lab brief (24 May 2024, PDF on `prod.wid.world`) names four authors and a rate and threshold, so it gave four people and the lab at grade A.
- **Party manifestos:** the CPI(M) press statement on its manifesto (`cpim.org/?p=11104`) is fetchable; the Congress 2024 manifesto does not propose a wealth tax, and Congress officials said so. Record individual Congress leaders, not the party.
- **A campaign hub:** the Centre for Financial Accountability (`cenfa.org`) republishes coverage of the Tax the Top campaign and quotes its spokesperson. The campaign's own site was not reachable from the sandbox.
- **Campaign site:** `taxthetop.org` is a JavaScript page: plain `curl` returns 69 bytes, but `skill/scripts/fetch_page.py --text --links` (after `pip install playwright trafilatura`) reads it and lists its PDFs (`press-statement-22-april-2026.pdf` names the petition's best-known signers; `campaign-note-english.pdf`). `taxthetop.in` and `www.taxthetop.org` are refused by the proxy; the Wayback Machine is not reachable.
- **Joint statements are the best bulk lists:** the Left parties' Budget statement of 3 Feb 2025 (`cpim.org/left-parties-call-on-alternative-proposals-for-budget/`, 4% wealth tax on 200 billionaires) gave five parties and five leaders; the ten central unions' memorandum of 24 June 2024 (copy on `publicservices.international`) gave ten unions.
- **Search method:** web search for Hindi or Bengali phrases (संपत्ति कर, वेल्थ टैक्स, সম্পদ কর) mostly returns Bangladeshi budget news, tax-collection notices or explainers. What worked was following leads from English sources: the campaigns' own sites (`taxtherichin.wordpress.com` has a nine-part op-ed series with named authors in its RSS feed), `nyaytak.com` (Hindi report of the Rozgar Adhikar Abhiyan conference, with its advisory committee), and the CPI(M) site, which publishes Central Committee texts in English and (via `cpimwestbengal.org`) Bengali.
- **Posters in the JavaScript bundle:** the campaign site's 'Voices in support' carousel is an array of images with name labels in the page's JavaScript bundle (`/assets/index-*.js`); the quotes are on the images, so read them with the image viewer and find the original dated page for the quote before recording anything.
- **Parliament record, as a bulk list.** Both houses have open APIs that make a full sweep cheap, and this is what found most of the MP-level supporters:
  - Rajya Sabha: `https://sansad.in/api_rs/debate/rs-session` lists session numbers; `https://rsdoc.nic.in/business/SessionDates?Sessionno=<n>` lists sitting dates; `https://rsdoc.nic.in/business/BusinessVerbatim?ses_no=<n>&ses_dt=dd/mm/yyyy` lists that day's PDFs (use the `Full Day` file). Hindi in these PDFs uses a broken font, so only English words are searchable.
  - Lok Sabha: `https://sansad.in/api_ls/business/AllLoksabhaAndSessionDates` lists dates; `https://sansad.in/api_ls/debate/text-of-debate?loksabha=<n>&sessionNo=<ROMAN>&debateDate=m/d/yyyy&locale=en` returns the day's PDF URL. `elibrary.sansad.in` (DSpace 7: `/server/api/discover/search/objects?query="wealth tax"&scope=b2770639-c57b-4ba3-a9f1-57761c60d195`) full-text searches older debates with a `TEXT` bundle per item, but only reached 2016 here.
  - Speaker names are the last speaker heading before a hit in `pdftotext -layout` output; skip chair headings, and allow mixed-case states in the heading (`SHRI P. WILSON (Tamil Nadu):`), or the speaker comes out wrong. Read each hit in context: most are the Minister quoting Budget figures, opponents welcoming the abolition, or estate-duty-only remarks.
  - The Rajya Sabha private members' bills list (`cms.rajyasabha.nic.in/UploadedFiles/ElectronicPublications/pm_legislation2013.pdf`, 1952-2023) contains no wealth-tax bill.
- **Quote checker:** `wtdb.py checkquotes` handles these PDFs but a full-day Lok Sabha PDF is large, so run it in the background.
- **Not enough:** a trade-union call for an "additional 2 per cent tax on the super-rich" (Jan 2025) and Sam Pitroda's inheritance-tax remarks (April 2024) are not wealth taxes as defined.
- **Fetch notes:** `dailypioneer.com` returned 404 to scripted fetches and `oxfamindia.org` press pages moved; `wikidata.org` rate-limits shared addresses; `sansad.in` redirects. Search summaries paraphrase: open each page and take quotes from its text.
- **Terms:** wealth tax (संपत्ति कर / धन कर), inheritance tax (विरासत कर), estate duty. "Super-rich surcharge" is an income-tax surcharge and is out of the definition.
