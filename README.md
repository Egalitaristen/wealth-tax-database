# Wealth Tax Database

An open, sourced database of who publicly backs an actual wealth tax, built country by country. Each country is a folder of CSV files; a GitHub Action turns them into a [world map and browsable site](https://egalitaristen.github.io/wealth-tax-database/).

> **The data is AI-generated and may be wrong.** Every entry links to a source, and many rows have not yet been checked by a person. If you spot a mistake or want an entry removed, use the **Report** link on the site, or [open an issue](../../issues/new?template=data-report.yml).

## What is here

| Path | What it holds |
|---|---|
| `data/<iso2>/` | One database per country or region, for example `data/gb/`. Plain CSV files plus a `meta.json`. |
| `skill/` | The research workflow (`SKILL.md`), source playbook, templates and the `wtdb.py` helper. Works for people and for AI assistants. |
| `site/` | The static front end (world map, country views). |
| `scripts/build_site.py` | Turns `data/` into the site data. No framework, standard library only. |

The United Kingdom (`data/gb/`) is the first country, built over 20 runs with Claude. It is a work in progress: many rows are marked `verified=n`.

## What counts

- **Supporters only.** Opponents and sceptics are not recorded as actors.
- **An actual wealth tax:** a recurring tax on net wealth, a one-off levy, or a minimum tax on billionaires. Income, property and capital gains reforms alone do not count.
- **Dated, linked source** and a short quote for every entry. Grades: **A** explicit (a formal act or a stated design), **B** named, **C** implied.
- **Public figures and organisations only.** Petition signers and other private individuals are never recorded.
- People are assumed alive unless a death record is found; anyone found dead is removed.

## Add your country

1. Fork this repository.
2. Read [CONTRIBUTING.md](CONTRIBUTING.md) and `skill/SKILL.md`.
3. Create `data/<iso2>/`:
   ```bash
   python skill/scripts/wtdb.py init data/de --area "Germany"
   ```
4. Do the research, by hand or with an AI assistant, and fill the tables.
5. Check your work:
   ```bash
   python skill/scripts/wtdb.py validate data/de
   ```
6. Open a pull request. New rows start unverified; a second person confirms them.

## Build the site locally

```bash
pip install pycountry
python scripts/build_site.py          # writes _site/
python -m http.server --directory _site
```

## Licences

- Code: [MIT](LICENSE).
- Data in `data/`: [CC BY 4.0](DATA_LICENSE.md). Quotes are short extracts from cited sources and stay under their owners' copyright.

## Corrections and removals

Use the Report links on the site, or open a [data report](../../issues/new?template=data-report.yml). Reports are public issues, so do not paste private information into them.
