"""Rebuild Canada's official 2025 CSD register and simplified map (network required).

Statistics Canada, Open Government Licence - Canada. Census subdivisions include
municipal equivalents, reserves and unorganized areas; not all elect councils.
Province outlines are the agency's 2021 digital boundaries, in the same EPSG:3347
projection. The province-outline vintage is recorded separately from the CSDs.
"""
import csv
import importlib.util
import json
from pathlib import Path
import time
from urllib.parse import urlencode
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/ca'
BASE = 'https://geo.statcan.gc.ca/geo_wa/rest/services/'
CSD = BASE + '2025/lcsd000a25s_e/MapServer/0'
PR = BASE + '2021/Digital_boundary_files/MapServer/0'
LICENCE = 'https://open.canada.ca/en/open-government-licence-canada'


def fetch(url):
    for attempt in range(3):
        try:
            with urlopen(url, timeout=60) as response:
                data = json.load(response)
            if 'error' in data:
                raise RuntimeError(data['error'])
            return data
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2)


def features(service):
    result = []
    while True:
        params = dict(f='json' if service == CSD else 'pjson', where='OBJECTID>0', outFields='*',
                      returnGeometry='true', outSR=3347,
                      maxAllowableOffset=800, geometryPrecision=0,
                      orderByFields='OBJECTID', resultOffset=len(result),
                      resultRecordCount=500)
        page_cache = ROOT / '.cache' / f"ca-{'csd' if service == CSD else 'pr'}-{len(result)}.json"
        if page_cache.exists():
            page = json.loads(page_cache.read_text(encoding='utf-8'))
        else:
            page = fetch(service + '/query?' + urlencode(params))
            page_cache.write_text(json.dumps(page), encoding='utf-8')
        batch = page.get('features', [])
        if not batch:
            raise RuntimeError('Empty page before completing register')
        result.extend(batch)
        print(f'{service}: {len(result)} features', flush=True)
        if not page.get('exceededTransferLimit'):
            return result


def main():
    cache = ROOT / '.cache'
    cache.mkdir(exist_ok=True)
    csd_cache = cache / 'ca-csds.json'
    if csd_cache.exists():
        csds = json.loads(csd_cache.read_text(encoding='utf-8'))
    else:
        csds = features(CSD)
        csd_cache.write_text(json.dumps(csds), encoding='utf-8')
    provinces = features(PR)
    assert len(csds) == 5054 and len(provinces) == 13
    assert len({f['attributes']['CSDUID'] for f in csds}) == 5054
    spec = importlib.util.spec_from_file_location('boundaries', ROOT / 'skill/scripts/topo_to_boundaries.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    def shapes(items, name, code):
        output = []
        for feature in items:
            props = feature['attributes']
            path = ''
            for ring in feature['geometry']['rings']:
                points = module.simplify([(round(p[0] / 2000, 2), round(-p[1] / 2000, 2)) for p in ring], .25)
                if len(set(points)) < 3:
                    # Preserve tiny municipal equivalents as an actual polygon.
                    points = [(round(p[0] / 2000, 4), round(-p[1] / 2000, 4)) for p in ring]
                if len(set(points)) >= 3:
                    path += 'M' + 'L'.join(f'{x} {y}' for x, y in points) + 'Z'
            if not path:
                raise RuntimeError(f'Missing shape: {props[code]}')
            output.append(dict(name=props[name].split(' / ')[0], code=props[code], path=path))
        return output

    units = shapes(csds, 'CSDNAME', 'CSDUID')
    regions = shapes(provinces, 'PRNAME', 'PRUID')
    extent = fetch(CSD + '?f=json')['extent']
    boundaries = dict(viewBox=[extent['xmin']/2000, -extent['ymax']/2000,
                               (extent['xmax']-extent['xmin'])/2000,
                               (extent['ymax']-extent['ymin'])/2000],
                      source='Statistics Canada: 2025 Census Subdivision Boundary File; 2021 digital province/territory outlines. Open Government Licence - Canada.',
                      licence='Open Government Licence - Canada', licence_url=LICENCE,
                      code_scheme='Statistics Canada CSDUID (7 digits); PRUID (2 digits)',
                      match='code', units=units, regions=regions)
    OUT.mkdir(exist_ok=True)
    (OUT / 'boundaries.json').write_text(json.dumps(boundaries, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    fields = next(csv.reader((OUT / 'geo_units.csv').open(encoding='utf-8-sig')))
    with (OUT / 'geo_units.csv').open(encoding='utf-8-sig', newline='') as stream:
        existing = {row['code']: row for row in csv.DictReader(stream) if row.get('code')}
    province_names = {f['attributes']['PRUID']: f['attributes']['PRNAME'].split(' / ')[0] for f in csds}
    province_ids = {code: f'G{i:04d}' for i, code in enumerate(sorted(province_names), 2)}
    rows = [dict(geo_unit_id='G0001', name='Canada', level='national', unit_type='country',
                 code='CA', website='https://www.canada.ca/', sweep_status='in_progress')]
    for code, name in sorted(province_names.items()):
        rows.append(dict(geo_unit_id=province_ids[code], name=name, level='region',
                         unit_type='province or territory', parent_id='G0001', code=code,
                         sweep_status='pending', website=CSD,
                         notes='Statistics Canada PRUID; 2025 CSD register.'))
    for i, feature in enumerate(sorted(csds, key=lambda f: f['attributes']['CSDUID']), 15):
        props = feature['attributes']
        rows.append(dict(geo_unit_id=f'G{i:04d}', name=props['CSDNAME'], level='council',
                         unit_type=props['CSDTYPE'], parent_id=province_ids[props['PRUID']],
                         code=props['CSDUID'], sweep_status='pending', website=CSD,
                         notes='2025 census subdivision; municipal equivalents include reserves and unorganized areas.'))
    # Rebuilding shapes must not erase research coverage or its notes.
    for row in rows:
        old = existing.get(row['code'])
        if old:
            for column in ('sweep_status', 'swept_run', 'swept_date', 'queries_run', 'hits', 'notes'):
                if old.get(column):
                    row[column] = old[column]
    with (OUT / 'geo_units.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f'Wrote {len(rows)} register units and {len(units)} map shapes.')


if __name__ == '__main__':
    main()
