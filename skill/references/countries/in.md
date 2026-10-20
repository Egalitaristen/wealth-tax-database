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
- **Not enough:** a trade-union call for an "additional 2 per cent tax on the super-rich" (Jan 2025) and Sam Pitroda's inheritance-tax remarks (April 2024) are not wealth taxes as defined.
- **Fetch notes:** `dailypioneer.com` returned 404 to scripted fetches and `oxfamindia.org` press pages moved; `wikidata.org` rate-limits shared addresses; `sansad.in` redirects. Search summaries paraphrase: open each page and take quotes from its text.
- **Terms:** wealth tax (संपत्ति कर / धन कर), inheritance tax (विरासत कर), estate duty. "Super-rich surcharge" is an income-tax surcharge and is out of the definition.
