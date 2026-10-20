# Wealth Tax Supporters

An open, sourced database of who publicly backs an actual wealth tax, built country by country. Each country is a folder of CSV files; Cloudflare Pages turns them into the site at [wealthtaxsupporters.com](https://wealthtaxsupporters.com).

> **The data is AI-generated and may be wrong.** Every entry links to a source, and many rows have not yet been checked by a person. If you spot a mistake or want an entry removed, use the **Report** link on the site, or [open an issue](../../issues/new?template=data-report.yml).

## Why this exists

The aim is to make it easy for people who share the view that wealth should be taxed to find each other, wherever they are. The place to start is the public record: the politicians, parties, organisations, economists and commentators who have said so, each with a source. A community layer for ordinary supporters is planned, but not built. See [docs/community.md](docs/community.md).

## What is here

| Path | What it holds |
|---|---|
| `data/<iso2>/` | One database per country or region, for example `data/gb/`. Plain CSV files plus a `meta.json`. |
| `skill/` | The research workflow (`SKILL.md`), source playbook, country examples and helper scripts (`wtdb.py`, `profiles_wikidata.py`, `topo_to_boundaries.py`). Works for people and for AI assistants. |
| `site/` | The static front end: one page and one script, no framework. Home with search and a dot world map, country pages (area map, directory, timeline, method), a page per supporter, method and contribute pages. |
| `scripts/build_site.py` | Turns `data/` into the site data, a search index and CSV downloads. Standard library plus `pycountry`. |
| `scripts/serve.py` | Serves the built site locally the way Cloudflare Pages does (unknown paths fall back to `index.html`). |
| `docs/`, `infra/` | The community plan, and the Cloudflare setup and draft database schema. Nothing deployed yet. |

Three countries so far, all built with Claude and all work in progress: the United Kingdom (`data/gb/`, with a council-level map), the United States (`data/us/`, federal and state level, with a state map) and Sweden (`data/se/`, national first pass done; regional and local sweep planned, with a municipality map). Most rows are still marked `verified=n`.

## What counts

- **Supporters only.** Opponents and sceptics are not recorded as actors.
- **An actual wealth tax:** a recurring tax on net wealth, a one-off levy, or a minimum tax on billionaires. Income, property and capital gains reforms alone do not count.
- **Dated, linked source** and a short quote for every entry. Grades: **A** explicit (a formal act or a stated design), **B** named, **C** implied.
- **Public figures and organisations only.** Petition signers and other private individuals are never recorded.
- People are assumed alive unless a death record is found; anyone found dead is removed.

## How the research works

The goal is a trustworthy list of who publicly backs an actual wealth tax, with the evidence behind every name, found by going after the most prominent supporters first. A first pass touches every layer once (legislature, parties, coalitions and unions, economists, commentators, wealthy and business, regional) and ends with a plan for later runs ordered by expected yield. Local sweeps are sampled first and expanded only where they pay. Coverage is reported honestly, so a blank means "not searched". The details are in [`skill/SKILL.md`](skill/SKILL.md); read its section 0 first.

## Add your country

1. Fork this repository.
2. Read [CONTRIBUTING.md](CONTRIBUTING.md) and `skill/SKILL.md`.
3. Create `data/<iso2>/`:
   ```bash
   python skill/scripts/wtdb.py init data/de --area "Germany"
   ```
4. Do the research, by hand or with an AI assistant. Tell the assistant the country, the scope (national, plus regional, plus local) and the depth (a first-pass seed is the default). It should start with the biggest supporters, not with tooling. Work on a branch, never on `main`.
5. Check your work:
   ```bash
   python skill/scripts/wtdb.py validate data/de
   python skill/scripts/wtdb.py checkquotes data/de --run R001     # quotes really are on the pages
   python skill/scripts/profiles_wikidata.py data/de               # websites and socials from Wikidata
   ```
6. For a local map, build a boundary file (see `skill/scripts/topo_to_boundaries.py`) and name it in `meta.json`.
7. Open a pull request. New rows start unverified; a second person confirms them.

## Build the site locally

```bash
pip install pycountry
python scripts/build_site.py          # writes _site/
python scripts/serve.py               # http://localhost:8000
```

The site uses clean URLs (`/gb`, `/gb/A0001`, `/about`), so it needs a host that falls back to `index.html` for unknown paths. Cloudflare Pages does this when the build has no `404.html`, and `scripts/serve.py` does the same locally. Filtered views are shareable: `/gb?place=United Kingdom > Wales&type=economist`.

## Licences

- Code: [MIT](LICENSE).
- Data in `data/`: [CC BY 4.0](DATA_LICENSE.md). Quotes are short extracts from cited sources and stay under their owners' copyright.

## Corrections and removals

Use the Report links on the site, or open a [data report](../../issues/new?template=data-report.yml). Reports are public issues, so do not paste private information into them.
