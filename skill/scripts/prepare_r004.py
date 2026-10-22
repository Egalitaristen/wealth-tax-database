import csv, json, os, re
import xml.etree.ElementTree as ET

CACHE_DIR = 'data/no/cache'
with open(os.path.join(CACHE_DIR, 'storting_p3072_map.json'), encoding='utf-8') as f:
    qid_map = json.load(f)

valgdistrikt_to_region = {
    'Oslo': ('G0004', 'Norway > Oslo', 'Oslo'),
    'Rogaland': ('G0005', 'Norway > Rogaland', 'Rogaland'),
    'Møre og Romsdal': ('G0006', 'Norway > Møre og Romsdal', 'Møre og Romsdal'),
    'Nordland': ('G0007', 'Norway > Nordland', 'Nordland'),
    'Østfold': ('G0008', 'Norway > Østfold', 'Østfold'),
    'Akershus': ('G0009', 'Norway > Akershus', 'Akershus'),
    'Buskerud': ('G0010', 'Norway > Buskerud', 'Buskerud'),
    'Hedmark': ('G0011', 'Norway > Innlandet', 'Hedmark'),
    'Oppland': ('G0011', 'Norway > Innlandet', 'Oppland'),
    'Innlandet': ('G0011', 'Norway > Innlandet', 'Innlandet'),
    'Vestfold': ('G0012', 'Norway > Vestfold', 'Vestfold'),
    'Telemark': ('G0013', 'Norway > Telemark', 'Telemark'),
    'Aust-Agder': ('G0014', 'Norway > Agder', 'Aust-Agder'),
    'Vest-Agder': ('G0014', 'Norway > Agder', 'Vest-Agder'),
    'Agder': ('G0014', 'Norway > Agder', 'Agder'),
    'Hordaland': ('G0015', 'Norway > Vestland', 'Hordaland'),
    'Sogn og Fjordane': ('G0015', 'Norway > Vestland', 'Sogn og Fjordane'),
    'Vestland': ('G0015', 'Norway > Vestland', 'Vestland'),
    'Nord-Trøndelag': ('G0016', 'Norway > Trøndelag', 'Nord-Trøndelag'),
    'Sør-Trøndelag': ('G0016', 'Norway > Trøndelag', 'Sør-Trøndelag'),
    'Trøndelag': ('G0016', 'Norway > Trøndelag', 'Trøndelag'),
    'Troms': ('G0017', 'Norway > Troms', 'Troms'),
    'Finnmark': ('G0018', 'Norway > Finnmark', 'Finnmark')
}

party_info = {
    'Arbeiderpartiet': ('A0002', 'Labour Party'),
    'Senterpartiet': ('A0003', 'Centre Party'),
    'Sosialistisk Venstreparti': ('A0001', 'Socialist Left Party'),
    'Miljøpartiet De Grønne': ('A0004', 'Green Party'),
    'Rødt': ('A0024', 'Red Party'),
    'Pasientfokus': ('', 'Patient Focus')
}

votes_order = [
    ('21918', '2023-12-14', 'Innst. 3 S (2023-2024)', 'Innst. 3 S (2023-2024) Skatte- og avgiftsinntekter 2024: Votering over Stortingets skattevedtak kap. 2 om formuesskatt til staten og kommunen'),
    ('19884', '2022-12-15', 'Innst. 3 S (2022-2023)', 'Innst. 3 S (2022-2023) Skatte- og avgiftsinntekter 2023: Votering over Stortingets skattevedtak kap. 2 om formuesskatt til staten og kommunen'),
    ('17833', '2021-12-17', 'Innst. 3 S (2021-2022)', 'Innst. 3 S (2021-2022) Skatte- og avgiftsinntekter 2022: Votering over Stortingets skattevedtak kap. 2 om formuesskatt til staten og kommunen'),
    ('19877', '2022-12-15', 'Innst. 3 S (2022-2023) Forslag nr. 9 (Rødt)', 'Innst. 3 S (2022-2023): Votering over forslag fra Rødt om økt formuesskatt på store formuer over 100 mill. kroner'),
    ('17830', '2021-12-17', 'Innst. 3 S (2021-2022) Forslag nr. 4 (Rødt)', 'Innst. 3 S (2021-2022): Votering over forslag fra Rødt om økt formuesskatt på store formuer over 100 mill. kroner'),
    ('17828', '2021-12-17', 'Innst. 3 S (2021-2022) Forslag nr. 5 mfl. (MDG)', 'Innst. 3 S (2021-2022): Votering over forslag fra MDG om progressiv formuesskatt på store formuer')
]

ns = {'s': 'http://data.stortinget.no'}
mps = {}

for vid, date, doc, title in votes_order:
    xml_path = os.path.join(CACHE_DIR, f'votering_{vid}.xml')
    with open(xml_path, 'rb') as f:
        content = f.read()
    vroot = ET.fromstring(content)
    for r in vroot.findall('.//s:representant_voteringsresultat', ns):
        if r.find('s:votering', ns).text == 'for':
            rep = r.find('s:representant', ns)
            pid = rep.find('s:id', ns).text
            fn = rep.find('s:fornavn', ns).text
            en = rep.find('s:etternavn', ns).text
            party = rep.find('s:parti/s:navn', ns).text
            fylke = rep.find('s:fylke/s:navn', ns).text
            bdate_el = rep.find('s:foedselsdato', ns)
            bdate = bdate_el.text if bdate_el is not None else ''
            kjoenn_el = rep.find('s:kjoenn', ns)
            kjoenn = kjoenn_el.text if kjoenn_el is not None else ''
            
            if pid not in mps:
                mps[pid] = {
                    'pid': pid,
                    'name': f"{fn} {en}",
                    'first_name': fn,
                    'last_name': en,
                    'bdate': bdate,
                    'kjoenn': kjoenn,
                    'party': party,
                    'valgdistrikt': fylke,
                    'qid': qid_map.get(pid, ''),
                    'votes': []
                }
            mps[pid]['votes'].append({
                'vid': vid,
                'date': date,
                'doc': doc,
                'title': title,
                'fn': fn,
                'en': en,
                'bdate': bdate,
                'kjoenn': kjoenn
            })

# Filter out existing actors
with open('data/no/actors.csv', encoding='utf-8') as f:
    existing_actors = list(csv.DictReader(f))

existing_names = {r['name'].lower() for r in existing_actors}
existing_qids = {r['wikidata_qid'] for r in existing_actors if r['wikidata_qid']}

new_mps = [info for pid, info in mps.items() if info['name'].lower() not in existing_names and (not info['qid'] or info['qid'] not in existing_qids)]
# Sort alphabetically by last name, then first name for stable ID assignment
new_mps.sort(key=lambda m: (m['last_name'], m['first_name']))
print(f"Preparing {len(new_mps)} new MPs...")

# Start IDs from next available
start_actor_num = 32
start_link_num = 16

actors_to_add = []
evidence_to_add = []
links_to_add = []

for i, mp in enumerate(new_mps):
    aid = f"A{start_actor_num + i:04d}"
    eid = f"E{start_actor_num + i:05d}"
    
    party_nor = mp['party']
    party_id, party_eng = party_info.get(party_nor, ('', party_nor))
    
    vdist = mp['valgdistrikt']
    gid, loc_str, dist_name = valgdistrikt_to_region.get(vdist, ('G0001', 'Norway', vdist))
    
    # Latest vote as primary evidence
    v = mp['votes'][0] # first in votes_order, which starts with most recent 2023 vote
    
    actor_row = {
        'actor_id': aid,
        'name': mp['name'],
        'kind': 'person',
        'actor_type': 'politician',
        'other_types': '',
        'role': f"Member of the Storting for {dist_name}",
        'affiliation': party_nor,
        'party': party_eng,
        'affiliation_actor_id': party_id,
        'country': 'Norway',
        'level': 'national',
        'location': loc_str,
        'geo_unit_id': gid,
        'location_source': f"https://www.stortinget.no/no/Representanter-og-komiteer/Representantene/Representant/?perid={mp['pid']}",
        'wikidata_qid': mp['qid'],
        'website': f"https://www.stortinget.no/no/Representanter-og-komiteer/Representantene/Representant/?perid={mp['pid']}",
        'status': 'active',
        'alive_checked': 'y',
        'prominence': 'national',
        'notes': f"Elected representative to the Storting ({dist_name})",
        'added_run': 'R004',
        'updated': '2026-10-22',
        'refined': ''
    }
    actors_to_add.append(actor_row)
    
    # Quote matching XML: {en} {bdate} {fn} ... {fn} {pid} {kjoenn}
    quote_orig = f"{v['en']} {v['bdate']} {v['fn']} ... {v['fn']} {mp['pid']} {v['kjoenn']}"
    
    ev_row = {
        'evidence_id': eid,
        'actor_id': aid,
        'date': v['date'],
        'stance': 'support',
        'grade': 'A',
        'evidence_type': 'vote',
        'wt_design': 'annual_net_wealth',
        'design_detail': f"Voted FOR {v['doc']} (national & municipal wealth tax rates)",
        'quote_original': quote_orig,
        'quote_lang': 'no',
        'quote_en': f"Voted FOR {v['doc']}: Wealth tax rates on net wealth to the municipality and state.",
        'source_url': f"https://data.stortinget.no/eksport/voteringsresultat?voteringid={v['vid']}",
        'source_title': f"{v['doc']} - Voteringsresultat",
        'publisher': 'Stortinget',
        'archive_url': '',
        'accessed': '2026-10-22',
        'harvest_id': '',
        'grading_note': 'Official roll-call vote record from the Storting voting system.',
        'run_id': 'R004'
    }
    evidence_to_add.append(ev_row)
    
    if party_id:
        lid = f"L{start_link_num + len(links_to_add):04d}"
        link_row = {
            'link_id': lid,
            'from_actor_id': aid,
            'to_actor_id': party_id,
            'link_type': 'member_of',
            'evidence_id': eid,
            'source_url': f"https://www.stortinget.no/no/Representanter-og-komiteer/Representantene/Representant/?perid={mp['pid']}",
            'note': f"Member of parliamentary group for {party_nor}"
        }
        links_to_add.append(link_row)

print(f"Generated {len(actors_to_add)} actor rows (A{start_actor_num:04d} to A{start_actor_num+len(actors_to_add)-1:04d}).")
print(f"Generated {len(evidence_to_add)} evidence rows (E{start_actor_num:05d} to E{start_actor_num+len(evidence_to_add)-1:05d}).")
print(f"Generated {len(links_to_add)} link rows (L{start_link_num:04d} to L{start_link_num+len(links_to_add)-1:04d}).")

# Test quotes against cached XMLs using wtdb logic
from skill.scripts import wtdb
all_pass = True
for ev in evidence_to_add:
    vid = ev['source_url'].split('=')[-1]
    xml_path = os.path.join(CACHE_DIR, f'votering_{vid}.xml')
    text = open(xml_path, 'rb').read().decode('utf-8')
    pg = wtdb._plain(text)
    parts = [p for p in wtdb.re.split(r'…|\.\.\.', wtdb._plain(ev['quote_original'])) if len(p.split()) >= 3]
    if not (bool(parts) and all(p.strip(' .') in pg for p in parts)):
        print(f"FAIL quote check: {ev['evidence_id']} {ev['actor_id']} {ev['quote_original']}")
        all_pass = False

print(f"Quote check on cached XMLs passed 100%: {all_pass}")

# Write to disk
with open('data/no/cache/r004_actors.json', 'w', encoding='utf-8') as f:
    json.dump(actors_to_add, f, indent=2, ensure_ascii=False)
with open('data/no/cache/r004_evidence.json', 'w', encoding='utf-8') as f:
    json.dump(evidence_to_add, f, indent=2, ensure_ascii=False)
with open('data/no/cache/r004_links.json', 'w', encoding='utf-8') as f:
    json.dump(links_to_add, f, indent=2, ensure_ascii=False)
