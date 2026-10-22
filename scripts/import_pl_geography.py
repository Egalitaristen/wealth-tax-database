"""Import official GUS TERYT/TERC ZIP: python scripts/import_pl_geography.py TERC.zip.

Download TERC / urzedowy from the Statistics Poland full-files page.
Only general-purpose gminas (RODZ 1/2/3) are included, not their components
or city subdivisions. Codes are the original official TERYT codes.
"""
import argparse
import csv
import datetime
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://eteryt.stat.gov.pl/eTeryt/rejestr_teryt/udostepnianie_danych/baza_teryt/uzytkownicy_indywidualni/pobieranie/pliki_pelne.aspx'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    with zipfile.ZipFile(args.source) as archive:
        names = [n for n in archive.namelist() if n.lower().endswith('.xml')]
        if len(names) != 1:
            raise ValueError('Expected exactly one TERC XML in the archive')
        document = ET.fromstring(archive.read(names[0]))
    records = []
    for element in document.findall('.//row'):
        r = {child.tag: child.text or '' for child in element}
        if r['RODZ'] and r['RODZ'] not in {'1', '2', '3'}:
            continue
        r['code'] = r['WOJ'] + r['POW'] + r['GMI'] + r['RODZ']
        records.append(r)
    records.sort(key=lambda r: (len(r['code']), r['code']))
    ids = {r['code']: f'G{i:04d}' for i, r in enumerate(records, 2)}
    assert len(ids) == len(records), 'Duplicate TERYT code'
    path = ROOT / 'data/pl/geo_units.csv'
    with path.open(encoding='utf-8', newline='') as stream:
        fields = next(csv.reader(stream))
    today = datetime.date.today().isoformat()
    rows = [dict(geo_unit_id='G0001', name='Poland', level='national',
                 unit_type='country', website='https://stat.gov.pl/', code='PL',
                 sweep_status='in_progress', swept_run='R001', swept_date=today,
                 notes='National seed; no comprehensive parliamentary or local sweep.')]
    for r in records:
        tier = len(r['code'])
        parent = 'G0001' if tier == 2 else ids[r['WOJ'] if tier == 4 else r['WOJ'] + r['POW']]
        name = r['NAZWA'].capitalize() if tier == 2 else r['NAZWA']
        if tier == 4:
            name = f"{r['NAZWA_DOD']} {name}"
        if tier == 7:
            name += ' (' + {'1': 'urban gmina', '2': 'rural gmina', '3': 'urban-rural gmina'}[r['RODZ']] + ')'
        rows.append(dict(geo_unit_id=ids[r['code']], name=name,
                         level={2: 'region', 4: 'county', 7: 'council'}[tier],
                         unit_type={2: 'voivodeship', 4: 'powiat', 7: 'gmina'}[tier],
                         parent_id=parent, code=r['code'], website=SOURCE,
                         sweep_status='pending',
                         notes=f"Official GUS TERYT/TERC; state at {r['STAN_NA']}; downloaded {today}. Advocacy not searched."))
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    for tier, label in [(2, 'voivodeships'), (4, 'powiats/cities with powiat rights'), (7, 'gminas')]:
        print(f"Imported {sum(len(r['code']) == tier for r in records)} {label}.")


if __name__ == '__main__':
    main()
