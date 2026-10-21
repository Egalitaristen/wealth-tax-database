# Spain: a ceded wealth tax and a national top-up

A seventh worked example. Spain still levies the Impuesto sobre el Patrimonio, but the autonomous communities run it and Madrid and Andalusia rebate it to zero; the national Impuesto Temporal de Solidaridad de las Grandes Fortunas (Ley 38/2022) tops it up on net wealth above EUR 3m. Supporters cluster on the left of the PSOE (Podemos, Sumar, IU, ERC, EH Bildu, BNG), in the big unions and the tax-justice platforms. Check every URL still works before relying on it.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Cortes Generales (Congreso, Senado), Gobierno | Roll calls are open data on congreso.es; the server blocks heavy scanning (HTTP 403 after about 10,000 requests), so fetch only the votes you need |
| region | 17 autonomous communities and Ceuta and Melilla | ISO 3166-2:ES codes (`ES-CT`), because INE numbers communities and provinces from 01 alike. Names in English (Catalonia, Community of Madrid) |
| county | 52 provinces, Ceuta and Melilla | The map tier, with the two-digit INE code. Deputies and senators are elected by province, so they go there. The 8,100 municipios are place text after the province (`Spain > Galicia > Pontevedra > Vigo`) |

**Map:** `data/es/boundaries.json` uses the IGN's reference boundaries (CC BY 4.0, credit "© Instituto Geográfico Nacional"), as packaged in TopoJSON by the npm package es-atlas (`es/provinces.json` and `es/autonomous_regions.json`, ids are INE codes). Gibraltar (54 and 20) is dropped and the Canary Islands are moved into an inset.

```bash
npm pack es-atlas@0.6.0 && tar xzf es-atlas-0.6.0.tgz
python skill/scripts/topo_to_boundaries.py package/es/provinces.json --object provinces --code-prop id --where "id!=54" \
  --shift 35,38:17,6.8 --project lonlat --scale 100 --simplify 0.4 --licence CC-BY-4.0 \
  --licence-url https://creativecommons.org/licenses/by/4.0/ --code-scheme "INE province codes" \
  --source "© Instituto Geográfico Nacional (IGN), CNIG reference data via es-atlas, CC BY 4.0" --out prov.json
python skill/scripts/topo_to_boundaries.py package/es/autonomous_regions.json --object autonomous_regions --code-prop id \
  --where "id!=20" --shift 05:17,6.8 --project lonlat --scale 100 --simplify 0.6 --licence CC-BY-4.0 \
  --licence-url https://creativecommons.org/licenses/by/4.0/ --code-scheme "INE autonomous community codes" --out ccaa.json
# then copy ccaa.json's units into prov.json as "regions" (codes rewritten to ISO 3166-2:ES) and save as data/es/boundaries.json
```

## Where supporters were found (seed pass, October 2026)
- The Congreso roll call of 7 June 2022 on the Unidas Podemos bill for a tax on fortunes over EUR 10m (58 yes).
- Bills and their signatories (BOCG series B), the parties that voted for Ley 38/2022, Sumar's programmes.
- The Plataforma por la Justicia Fiscal and its members, Oxfam Intermón, Gestha, CCOO, UGT, Attac, backers of the European citizens' initiative "Tax the Rich".
- Regional bodies: the Catalan Parlament and Generalitat, Navarre, the Basque foral bodies.
- Not found: any Spanish millionaire or business owner on record for a wealth tax.
