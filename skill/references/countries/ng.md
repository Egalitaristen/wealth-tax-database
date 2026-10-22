# Nigeria: no federal wealth or inheritance tax since 1996; support led by tax-justice coalitions, unions, economists and Lagos tax conferences

Worked notes from the Nigeria seed pass (`R001`, 2026-10-22). Check every URL still works before relying on it.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | House of Representatives, Senate, Federal Government of Nigeria | The 1999 Constitution places company income, stamp duties and capital gains under federal legislation while personal income tax and state land charges are collected by state internal revenue services |
| region | 36 states and the Federal Capital Territory (FCT) | Official OSGOF / OCHA COD-AB P-codes (`NG001`–`NG037`) in `code`. Abuja (FCT), Lagos and Oyo hold the bulk of civil society, union and academic headquarters |
| council | 774 Local Government Areas (LGAs) | The map tier, with official OSGOF / OCHA COD-AB P-codes (`NG001001`–`NG037006`) in `code`. Under the Fourth Schedule of the 1999 Constitution, LGAs levy tenement rates and market fees and cannot enact a net wealth or inheritance tax |

**Map:** `data/ng/boundaries.json` uses the official administrative boundaries of Nigeria (Admin 1 states + FCT and Admin 2 Local Government Areas) from the Office of the Surveyor General of the Federation (OSGOF), eHealth Africa and the UN Cartographic Section (UNCS), distributed via the OCHA Common Operational Datasets on HDX (`https://data.humdata.org/dataset/cod-ab-nga`, package metadata at `https://data.humdata.org/api/3/action/package_show?id=cod-ab-nga`). Licence: `CC-BY-IGO-3.0` (`https://creativecommons.org/licenses/by/3.0/igo/legalcode`). Both `units` (774 LGAs) and `regions` (36 states + FCT) come from the same shapefile bundle (`nga_admbnda_adm2_osgof_20190417.shp` and `nga_admbnda_adm1_osgof_20190417.shp`), so region outlines fall cleanly on LGA borders. Built with:

```bash
python skill/scripts/topo_to_boundaries.py nga_adm2.geojson --code-prop ADM2_PCODE --name-prop ADM2_EN \
  --project lonlat --scale 80 --simplify 1.2 --licence CC-BY-IGO-3.0 \
  --licence-url https://creativecommons.org/licenses/by/3.0/igo/legalcode --code-scheme OSGOF-PCODE --out units.json
python skill/scripts/topo_to_boundaries.py nga_adm1.geojson --code-prop ADM1_PCODE --name-prop ADM1_EN \
  --project lonlat --scale 80 --simplify 1.2 --licence CC-BY-IGO-3.0 \
  --licence-url https://creativecommons.org/licenses/by/3.0/igo/legalcode --code-scheme OSGOF-PCODE --out regions.json
```

## What worked and what to watch

- **The October 2024 Oxfam / CISLAC / TJNA / CARE reports (`H0001`, `H0002`, `H0006`) are the richest bulk lists.**
  1. *Income and Wealth Inequality in Nigeria: Trends and Drivers* (15 October 2024, policy brief PDF on `oi-files-cng-v2-prod.s3.eu-west-2.amazonaws.com`) names two lead authors (Henry Ushie at Oxfam in Nigeria and Chinedu Bassey at CISLAC / Tax Justice and Governance Platform), eight contributing authors, and foreword co-signers John Makina (Oxfam in Nigeria) and Dr Hussaini Abdu (CARE International in Nigeria). It proposes a 1% annual net wealth tax above $1 million (raising ~$7.5bn/year) or tiered rates of 2% above $5m, 3%–5% above $50m and 5%–10% above $1bn, plus a 0.02% stock levy and a Comprehensive Wealth Registry.
  2. *Taxing the Rich: Nigerian Fair Tax Monitor Thematic Report* (15 October 2024, PDF on `oi-files-cng-v2-prod.s3.eu-west-2.amazonaws.com`) by Mtwalo Msoni and Ishmael Zulu (Tax Justice Network Africa), edited with Martin Brehm Christensen (Oxfam Novib) and Henry Ushie, and co-published with CISLAC (led by Auwal Musa Rafsanjani) and Make Tax Fair, proposes a tiered annual Net Wealth Tax (1% on $1m–$5m, 2% on $5m–$50m, 5% above $50m; or the IPS / Oxfam / Fight Inequality Alliance / Patriotic Millionaires model of 2% >$5m, 5% >$50m, 10% >$1bn raising over $6bn / ₦4.59trn annually) and reintroducing inheritance taxation above ₦50 million.
- **Lagos professional conference (`H0004`):** Chartered Accountant Chief Blakey Okwudili Ijezie (`Okwudili Ijezie & Co.`, Kosofe LGA, Lagos) organised a February 2024 conference on *Wealth Taxation in Nigeria: A Veritable Tool for Sustainable Development*, covered in detail by *Vanguard* columnist Sunny Ikhioya (`vanguardngr.com/2024/03/blakeys-wealth-tax-conference/`). It yielded six actors across accounting, faith, economics and journalism.
- **Unions and socialist groups on the 2024–2026 tax reforms:** The Nigeria Labour Congress (NLC, led by Joe Ajaero), Non-Academic Staff Union of Educational and Associated Institutions (NASU, led by Dr Makolo Hassan), Socialist Party of Nigeria (SPN, led by Abiodun Bamigboye) and Campaign for Democratic and Workers' Rights (CDWR, led by Rufus Olusesan and Chinedu Bosah) all published statements demanding taxation of wealth, luxury assets (such as private jets) and billionaire lifestyles instead of regressive taxes on workers.
- **Deceased check caught a major union economist:** Former NLC Chief Economist and General Secretary Dr Peter Ozo-Eson (who spoke in January 2015 calling for heavy taxation on private jets and luxury goods of the rich) died on 13 December 2025. He is logged in `exclusions.csv` (`X0001`, `reason=deceased`), while the institutional position is recorded under the Nigeria Labour Congress (`A0041`).
- **False positive to avoid — fake "National Solidarity Wealth Tax" op-ed:** An opinion piece in *Independent Nigeria* (19 January 2026) claimed that Nigeria's 2026 tax reforms introduced a "National Solidarity Wealth Tax" of 1.5%–3% on net worth above ₦1 billion. The enacted Nigeria Tax Act 2025 contains no such tax.
- **False positive to avoid — Presidential Committee & ICTD HNWI Personal Income Tax compliance (`X0002`, `X0003`, `X0005`):** Taiwo Oyedele's Presidential Fiscal Policy and Tax Reforms Committee and the ICTD Borno State HNWI study (`ictd.ac`) focus on Personal Income Tax (PIT) compliance and raising the top marginal PIT rate to 25% while explicitly avoiding a tax on capital stock.
