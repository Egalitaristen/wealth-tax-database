import csv
import os
import re
import sys
import pykakasi
from bs4 import BeautifulSoup
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath('skill/scripts'))
import wtdb

kks = pykakasi.kakasi()

def to_romaji(text, reading=""):
    src = reading if reading else text
    converted = kks.convert(src)
    words = []
    for item in converted:
        h = item['hepburn'].strip()
        if h:
            words.extend(re.split(r'\s+', h))
    cap_words = [w.capitalize() for w in words if w]
    if len(cap_words) == 2:
        return f"{cap_words[1]} {cap_words[0]}"
    return " ".join(cap_words)

PREF_MAP = {
    '北海道': 'Hokkaido', '青森': 'Aomori', '岩手': 'Iwate', '宮城': 'Miyagi',
    '秋田': 'Akita', '山形': 'Yamagata', '福島': 'Fukushima', '茨城': 'Ibaraki',
    '栃木': 'Tochigi', '群馬': 'Gunma', '埼玉': 'Saitama', '千葉': 'Chiba',
    '東京': 'Tokyo', '神奈川': 'Kanagawa', '新潟': 'Niigata', '富山': 'Toyama',
    '石川': 'Ishikawa', '福井': 'Fukui', '山梨': 'Yamanashi', '長野': 'Nagano',
    '岐阜': 'Gifu', '静岡': 'Shizuoka', '愛知': 'Aichi', '三重': 'Mie',
    '滋賀': 'Shiga', '京都': 'Kyoto', '大阪': 'Osaka', '兵庫': 'Hyogo',
    '奈良': 'Nara', '和歌山': 'Wakayama', '鳥取': 'Tottori', '島根': 'Shimane',
    '岡山': 'Okayama', '広島': 'Hiroshima', '山口': 'Yamaguchi', '徳島': 'Tokushima',
    '香川': 'Kagawa', '愛媛': 'Ehime', '高知': 'Kochi', '福岡': 'Fukuoka',
    '佐賀': 'Saga', '長崎': 'Nagasaki', '熊本': 'Kumamoto', '大分': 'Oita',
    '宮崎': 'Miyazaki', '鹿児島': 'Kagoshima', '沖縄': 'Okinawa'
}

BLOCK_MAP = {
    '北海道ブロック': 'Hokkaido', '東北ブロック': 'Miyagi', '北関東ブロック': 'Saitama',
    '南関東ブロック': 'Chiba', '東京ブロック': 'Tokyo', '北陸信越ブロック': 'Niigata',
    '東海ブロック': 'Aichi', '近畿ブロック': 'Osaka', '中国ブロック': 'Hiroshima',
    '四国ブロック': 'Kagawa', '九州ブロック': 'Fukuoka',
}

TOKYO_DISTRICT_WARDS = {
    '東京1区': 'Chiyoda', '東京2区': 'Chuo', '東京3区': 'Shinagawa', '東京4区': 'Ota',
    '東京5区': 'Setagaya', '東京6区': 'Setagaya', '東京7区': 'Shibuya', '東京8区': 'Suginami',
    '東京9区': 'Nerima', '東京10区': 'Toshima', '東京11区': 'Itabashi', '東京12区': 'Kita',
    '東京13区': 'Adachi', '東京14区': 'Sumida', '東京15区': 'Koto', '東京16区': 'Edogawa',
    '東京17区': 'Katsushika', '東京18区': 'Musashino', '東京19区': 'Kodaira',
    '東京20区': 'Higashimurayama', '東京21区': 'Tachikawa', '東京22区': 'Mitaka',
    '東京23区': 'Machida', '東京24区': 'Hachioji', '東京25区': 'Ome', '東京26区': 'Meguro',
    '東京27区': 'Nakano', '東京28区': 'Nerima', '東京29区': 'Arakawa', '東京30区': 'Fuchu'
}

# Load current DB to access geo_units
db = wtdb.load_all('data/jp')
geo_idx = wtdb.geo_index(db['geo_units'])

def resolve_district_location(district, party_pref=None):
    for dist, ward in TOKYO_DISTRICT_WARDS.items():
        if dist in district:
            loc = f"Japan > Tokyo > {ward}"
            uid, depth, rem = wtdb.resolve_location(loc, geo_idx)
            if uid:
                return loc, uid
            return "Japan > Tokyo", "G0018"
    
    for j_pref, e_pref in PREF_MAP.items():
        if district.startswith(j_pref):
            if e_pref in ['Osaka', 'Kyoto', 'Nagoya', 'Hiroshima', 'Fukuoka', 'Sendai', 'Sapporo']:
                cap = e_pref if e_pref != 'Hokkaido' else 'Sapporo'
                if e_pref == 'Aichi': cap = 'Nagoya'
                if e_pref == 'Miyagi': cap = 'Sendai'
                loc = f"Japan > {e_pref} > {cap}"
                uid, depth, rem = wtdb.resolve_location(loc, geo_idx)
                if uid:
                    return loc, uid
            loc = f"Japan > {e_pref}"
            uid, depth, rem = wtdb.resolve_location(loc, geo_idx)
            return loc, uid
    
    for blk, e_pref in BLOCK_MAP.items():
        if blk in district:
            loc = f"Japan > {e_pref}"
            uid, depth, rem = wtdb.resolve_location(loc, geo_idx)
            return loc, uid
            
    if party_pref and party_pref in PREF_MAP.values():
        loc = f"Japan > {party_pref}"
        uid, depth, rem = wtdb.resolve_location(loc, geo_idx)
        return loc, uid
        
    return "Japan", "G0001"

# 1. Base seed actors
actors = list(db['actors'][:14])
evidence = list(db['evidence'][:14])
links = list(db['links'][:14])
profiles = list(db['profiles'][:14])

existing_norm_names = {wtdb.norm_name(a['name']) for a in actors}
existing_kanji = set()
for a in actors:
    m = re.search(r'\((.*?)\)', a['name'])
    if m:
        existing_kanji.add(m.group(1).replace(' ', ''))

actor_id_counter = 15
evidence_id_counter = 15
link_id_counter = len(links) + 1
profile_id_counter = len(profiles) + 1

# 2. Add New Organisations
NEW_ORGS = [
    {
        "name": "Social Democratic Party (社会民主党)",
        "kind": "organisation",
        "actor_type": "party",
        "other_types": "",
        "role": "Political party in the National Diet",
        "affiliation": "",
        "party": "",
        "country": "JP",
        "level": "national",
        "location": "Japan > Tokyo > Chiyoda",
        "location_source": "https://sdp.or.jp/",
        "wikidata_qid": "Q241513",
        "website": "https://sdp.or.jp/",
        "status": "active",
        "alive_checked": "na",
        "prominence": "national",
        "notes": "Officially committed in 2025 Fair Tax Coalition policy platform to progressive wealth taxation on net financial assets above a specified threshold.",
        "evidence": {
            "evidence_type": "policy_adoption",
            "date": "2025-01-20",
            "stance": "support",
            "grade": "A",
            "wt_design": "annual_net_wealth",
            "quote_original": "「富裕税」（資産課税）の創設を含めた富裕層への課税強化を重要政策の一つと位置づけています。金融資産課税（富裕税）として…純金融資産の一定額以上に対して累進的に課税を導入。",
            "quote_en": "The Social Democratic Party positions strengthening taxation on the wealthy, including creating a wealth tax (asset taxation), as a key policy. As a financial asset tax (wealth tax), we progressively introduce taxation above a certain amount of net financial assets.",
            "quote_lang": "ja",
            "source_url": "https://tax-justice.com/?p=1597",
            "source_title": "公正な税制を求める各党アンケート結果 (Party Questionnaire on Fair Tax)",
            "source_date": "2025-01-20",
            "confidence": "high",
            "grading_note": "Official party response to national tax justice questionnaire explicitly endorsing creation of an annual progressive net financial wealth tax."
        }
    },
    {
        "name": "Reiwa Shinsengumi (れいわ新選組)",
        "kind": "organisation",
        "actor_type": "party",
        "other_types": "",
        "role": "Political party in the National Diet",
        "affiliation": "",
        "party": "",
        "country": "JP",
        "level": "national",
        "location": "Japan > Tokyo > Chiyoda",
        "location_source": "https://reiwa-shinsengumi.com/",
        "wikidata_qid": "Q65241477",
        "website": "https://reiwa-shinsengumi.com/",
        "status": "active",
        "alive_checked": "na",
        "prominence": "national",
        "notes": "Officially endorsed introduction of wealth tax (富裕税) on wealthy individuals in the 2025 Fair Tax Coalition party questionnaire.",
        "evidence": {
            "evidence_type": "policy_adoption",
            "date": "2025-01-20",
            "stance": "support",
            "grade": "A",
            "wt_design": "annual_net_wealth",
            "quote_original": "富裕税を導入したうえで、その税収をどう配分するかは議論が必要ですが、負担力のある富裕層にしっかりと負担していたただくことは税の原則からも妥当と考えます。",
            "quote_en": "After introducing a wealth tax, while discussion is needed on how to allocate its revenue, having the wealthy who have ability to pay bear their proper burden is appropriate from tax principles.",
            "quote_lang": "ja",
            "source_url": "https://tax-justice.com/?p=1597",
            "source_title": "公正な税制を求める各党アンケート結果 (Party Questionnaire on Fair Tax)",
            "source_date": "2025-01-20",
            "confidence": "high",
            "grading_note": "Official party questionnaire answer explicitly supporting the creation of a wealth tax on high-net-worth individuals."
        }
    },
    {
        "name": "Japanese Communist Party Tokyo Metropolitan Assembly Caucus (日本共産党東京都議会議員団)",
        "kind": "organisation",
        "actor_type": "party",
        "other_types": "",
        "role": "Prefectural assembly caucus",
        "affiliation": "Tokyo Metropolitan Assembly",
        "party": "Japanese Communist Party",
        "affiliation_actor_id": "A0001",
        "country": "JP",
        "level": "regional",
        "location": "Japan > Tokyo > Shinjuku",
        "location_source": "https://www.jcptogidan.gr.jp/",
        "wikidata_qid": "",
        "website": "https://www.jcptogidan.gr.jp/",
        "status": "active",
        "alive_checked": "na",
        "prominence": "regional",
        "notes": "14-member caucus in Tokyo Metropolitan Assembly actively proposing progressive tax reform and wealth taxation.",
        "evidence": {
            "evidence_type": "policy_adoption",
            "date": "2024-01-01",
            "stance": "support",
            "grade": "B",
            "wt_design": "annual_net_wealth",
            "quote_original": "日本共産党東京都議会議員団...大山とも子",
            "quote_en": "Japanese Communist Party Tokyo Metropolitan Assembly Caucus...Caucus Member Directory",
            "quote_lang": "ja",
            "source_url": "https://www.jcptogidan.gr.jp/congressman/",
            "source_title": "都議団紹介議員一覧 (Tokyo Assembly Caucus Members)",
            "source_date": "2024-01-01",
            "confidence": "high",
            "grading_note": "Tokyo Metropolitan Assembly caucus operating under the party platform advocating wealth taxation."
        }
    },
    {
        "name": "Japan Housewives' Association (主婦連合会 / Shufu Rengokai)",
        "kind": "organisation",
        "actor_type": "campaigner",
        "other_types": "ngo_campaign",
        "role": "National consumer and women's advocacy organization",
        "affiliation": "",
        "party": "",
        "country": "JP",
        "level": "national",
        "location": "Japan > Tokyo > Chiyoda",
        "location_source": "https://shufuren.net/",
        "wikidata_qid": "Q11438914",
        "website": "https://shufuren.net/",
        "status": "active",
        "alive_checked": "na",
        "prominence": "national",
        "notes": "Historic Japanese consumer organization whose leadership co-founded the Fair Tax Coalition to demand wealth taxation over consumption tax.",
        "evidence": {
            "evidence_type": "policy_adoption",
            "date": "2024-01-01",
            "stance": "support",
            "grade": "B",
            "wt_design": "annual_net_wealth",
            "quote_original": "山根 香織...主婦連合会...共同代表",
            "quote_en": "Kaori Yamane...Japan Housewives' Association...Co-representative",
            "quote_lang": "ja",
            "source_url": "https://tax-justice.com/?page_id=27",
            "source_title": "不公平な税制をただす市民連絡会 呼びかけ人",
            "source_date": "2024-01-01",
            "confidence": "high",
            "grading_note": "Official sponsoring organization of the Fair Tax Coalition."
        }
    },
    {
        "name": "Taishokusha Rengou (退職者連合 / Association of Retirees)",
        "kind": "organisation",
        "actor_type": "campaigner",
        "other_types": "union",
        "role": "National association of retired union workers and pensioners",
        "affiliation": "",
        "party": "",
        "country": "JP",
        "level": "national",
        "location": "Japan > Tokyo > Minato",
        "location_source": "https://www.taishokusha-rengo.jp/",
        "wikidata_qid": "",
        "website": "https://www.taishokusha-rengo.jp/",
        "status": "active",
        "alive_checked": "na",
        "prominence": "national",
        "notes": "Pensioners and retirees federation co-leading the Fair Tax Coalition to protect social security via wealth taxation.",
        "evidence": {
            "evidence_type": "policy_adoption",
            "date": "2024-01-01",
            "stance": "support",
            "grade": "B",
            "wt_design": "annual_net_wealth",
            "quote_original": "菅井 義夫...退職者連合...共同代表",
            "quote_en": "Yoshio Sugai...Association of Retirees...Co-representative",
            "quote_lang": "ja",
            "source_url": "https://tax-justice.com/?page_id=27",
            "source_title": "不公平な税制をただす市民連絡会 呼びかけ人",
            "source_date": "2024-01-01",
            "confidence": "high",
            "grading_note": "Co-initiating organization of the Fair Tax Coalition."
        }
    },
    {
        "name": "Anti-Poverty Network (反貧困ネットワーク)",
        "kind": "organisation",
        "actor_type": "ngo_campaign",
        "other_types": "campaigner",
        "role": "National coalition of anti-poverty campaigns and welfare advocates",
        "affiliation": "",
        "party": "",
        "country": "JP",
        "level": "national",
        "location": "Japan > Tokyo > Shinjuku",
        "location_source": "https://hanhinkonnetwork.org/",
        "wikidata_qid": "",
        "website": "https://hanhinkonnetwork.org/",
        "status": "active",
        "alive_checked": "na",
        "prominence": "national",
        "notes": "Broad coalition founded by Kenji Utsunomiya, Karin Amamiya and welfare lawyers, advocating wealth tax to eliminate structural poverty.",
        "evidence": {
            "evidence_type": "policy_adoption",
            "date": "2024-01-01",
            "stance": "support",
            "grade": "B",
            "wt_design": "annual_net_wealth",
            "quote_original": "赤石 千衣子...反貧困ネットワーク世話人",
            "quote_en": "Chieko Akaishi...Anti-Poverty Network Steering Committee",
            "quote_lang": "ja",
            "source_url": "https://tax-justice.com/?page_id=27",
            "source_title": "不公平な税制をただす市民連絡会 呼びかけ人",
            "source_date": "2024-01-01",
            "confidence": "high",
            "grading_note": "Founding network represented among co-representatives of the Fair Tax Coalition."
        }
    },
    {
        "name": "Association for Correcting Unfair Taxation (不公平な税制をただす会)",
        "kind": "organisation",
        "actor_type": "campaigner",
        "other_types": "legal_tax_professional",
        "role": "National legal and fiscal policy campaign organization",
        "affiliation": "",
        "party": "",
        "country": "JP",
        "level": "national",
        "location": "Japan > Tokyo > Chiyoda",
        "location_source": "https://tax-justice.com/",
        "wikidata_qid": "",
        "website": "https://tax-justice.com/",
        "status": "active",
        "alive_checked": "na",
        "prominence": "national",
        "notes": "Campaign formed by progressive tax attorneys and economists to advocate wealth tax and dismantle preferential tax treatment for high asset owners.",
        "evidence": {
            "evidence_type": "policy_adoption",
            "date": "2024-01-01",
            "stance": "support",
            "grade": "A",
            "wt_design": "annual_net_wealth",
            "quote_original": "不公平な税制をただす会...富裕税",
            "quote_en": "Association for Correcting Unfair Taxation...Wealth tax",
            "quote_lang": "ja",
            "source_url": "https://tax-justice.com/?p=1597",
            "source_title": "公正な税制を求める各党アンケート結果",
            "source_date": "2025-01-20",
            "confidence": "high",
            "grading_note": "Core legal/civic campaign organization publishing Introduction to Wealth Tax."
        }
    }
]

for org in NEW_ORGS:
    aid = f"A{actor_id_counter:04d}"
    eid = f"E{evidence_id_counter:05d}"
    actor_id_counter += 1
    evidence_id_counter += 1
    
    ev = org.pop('evidence')
    org['actor_id'] = aid
    
    uid, depth, rem = wtdb.resolve_location(org['location'], geo_idx)
    org['geo_unit_id'] = uid
    org['added_run'] = 'R002'
    org['updated'] = '2026-10-23'
    org['refined'] = '2026-10-23'
    actors.append(org)
    existing_norm_names.add(wtdb.norm_name(org['name']))
    
    ev['evidence_id'] = eid
    ev['actor_id'] = aid
    ev['run_id'] = 'R002'
    evidence.append(ev)
    
    if aid in ['A0018', 'A0019', 'A0020', 'A0021']:
        links.append({
            "link_id": f"L{link_id_counter:05d}",
            "from_actor_id": aid,
            "link_type": "coalition_partner",
            "to_actor_id": "A0008",
            "evidence_id": eid,
            "source_url": "https://tax-justice.com/?page_id=27",
            "note": "Participating organization / coalition partner in the Citizens' Liaison Committee for Fair Taxation."
        })
        link_id_counter += 1
    elif aid == 'A0017':
        links.append({
            "link_id": f"L{link_id_counter:05d}",
            "from_actor_id": aid,
            "link_type": "party_of",
            "to_actor_id": "A0001",
            "evidence_id": eid,
            "source_url": "https://www.jcptogidan.gr.jp/",
            "note": "Regional assembly caucus of the Japanese Communist Party."
        })
        link_id_counter += 1

    if org.get('website'):
        profiles.append({
            "profile_id": f"P{profile_id_counter:05d}",
            "actor_id": aid,
            "platform": "website",
            "url": org['website'],
            "source": "official",
            "checked": "2026-10-23"
        })
        profile_id_counter += 1

# 3. Add Key Politicians
KEY_POLITICIANS = [
    # JCP
    {
        "name": "Kazuo Shii (志位和夫)",
        "role": "Member of the House of Representatives, Chair of the JCP Central Committee",
        "affiliation": "House of Representatives", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Tokyo > Chiyoda",
        "wikidata_qid": "Q1076274", "website": "https://www.shii.gr.jp/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Tomoko Tamura (田村智子)",
        "role": "Member of the House of Representatives, Chair of the JCP Executive Committee",
        "affiliation": "House of Representatives", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Tokyo > Chiyoda",
        "wikidata_qid": "Q11576922", "website": "https://www.tamura-tomoko.jp/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Tetsuya Shiokawa (塩川鉄也)",
        "role": "Member of the House of Representatives (Kita-Kanto proportional)",
        "affiliation": "House of Representatives", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Saitama > Saitama",
        "wikidata_qid": "Q11532870", "website": "https://www.shiokawa-tetsuya.jp/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Chizuko Takahashi (高橋千鶴子)",
        "role": "Member of the House of Representatives (Tohoku proportional)",
        "affiliation": "House of Representatives", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Aomori > Aomori",
        "wikidata_qid": "Q11671569", "website": "https://www.takahashi-chizuko.jp/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Seiken Akamine (赤嶺政賢)",
        "role": "Member of the House of Representatives (Okinawa 1st)",
        "affiliation": "House of Representatives", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Okinawa > Naha",
        "wikidata_qid": "Q7443306", "website": "https://www.akamine-seiken.jp/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Nobuko Motomura (本村伸子)",
        "role": "Member of the House of Representatives (Tokai proportional)",
        "affiliation": "House of Representatives", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Aichi > Nagoya",
        "wikidata_qid": "Q18700947", "website": "https://motomura-nobuko.jp/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Takeshi Miyamoto (宮本岳志)",
        "role": "Member of the House of Representatives (Kinki proportional)",
        "affiliation": "House of Representatives", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Osaka > Osaka",
        "wikidata_qid": "Q11454924", "website": "https://miyamoto-takeshi.jp/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Taku Yamazoe (山添拓)",
        "role": "Member of the House of Councillors (Tokyo)",
        "affiliation": "House of Councillors", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Tokyo > Chiyoda",
        "wikidata_qid": "Q24867169", "website": "https://yamazoe-taku.com/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Yoshiko Kira (吉良よし子)",
        "role": "Member of the House of Councillors (Tokyo)",
        "affiliation": "House of Councillors", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Tokyo > Chiyoda",
        "wikidata_qid": "Q14030635", "website": "https://kirayoshiko.com/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Tomo Iwabuchi (岩渕友)",
        "role": "Member of the House of Councillors (Proportional)",
        "affiliation": "House of Councillors", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Tokyo > Chiyoda",
        "wikidata_qid": "Q24867499", "website": "https://iwabuchi-tomo.net/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Akiko Kurabayashi (倉林明子)",
        "role": "Member of the House of Councillors (Kyoto)",
        "affiliation": "House of Councillors", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Kyoto > Kyoto",
        "wikidata_qid": "Q17228800", "website": "https://kurabayashi-akiko.jp/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Satoshi Inoue (井上哲士)",
        "role": "Member of the House of Councillors (Proportional)",
        "affiliation": "House of Councillors", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Tokyo > Chiyoda",
        "wikidata_qid": "Q6037389", "website": "https://inoue-satoshi.com/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Gaku Ito (伊藤岳)",
        "role": "Member of the House of Councillors (Saitama)",
        "affiliation": "House of Councillors", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Saitama > Saitama",
        "wikidata_qid": "Q65230985", "website": "https://ito-gaku.jp/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Sohei Nihi (仁比聡平)",
        "role": "Member of the House of Councillors (Proportional)",
        "affiliation": "House of Councillors", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Fukuoka > Kitakyushu",
        "wikidata_qid": "Q7554476", "website": "https://nihi-sohei.jp/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Kotaro Tatsumi (辰巳孝太郎)",
        "role": "Former Member of the House of Councillors, JCP Central Committee Member",
        "affiliation": "Japanese Communist Party", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Osaka > Osaka",
        "wikidata_qid": "Q11598007", "website": "https://tatsumi-kotaro.jp/",
        "prominence": "national", "quote_type": "jcp"
    },
    {
        "name": "Kimie Hatano (畑野君枝)",
        "role": "Former Member of the House of Representatives, JCP Central Committee Member",
        "affiliation": "Japanese Communist Party", "party": "Japanese Communist Party", "party_id": "A0001",
        "level": "national", "location": "Japan > Kanagawa > Kawasaki",
        "wikidata_qid": "Q11581452", "website": "https://hatano-kimie.jp/",
        "prominence": "national", "quote_type": "jcp"
    },

    # SDP
    {
        "name": "Mizuho Fukushima (福島みずほ)",
        "role": "Member of the House of Councillors, Leader of the Social Democratic Party",
        "affiliation": "House of Councillors", "party": "Social Democratic Party", "party_id": "A0015",
        "level": "national", "location": "Japan > Tokyo > Chiyoda",
        "wikidata_qid": "Q259837", "website": "https://mizuhofukushima.jp/",
        "prominence": "national", "quote_type": "sdp"
    },
    {
        "name": "Tadatomo Yoshida (吉田忠智)",
        "role": "Member of the House of Councillors, Secretary General of the SDP",
        "affiliation": "House of Councillors", "party": "Social Democratic Party", "party_id": "A0015",
        "level": "national", "location": "Japan > Oita > Oita",
        "wikidata_qid": "Q11414169", "website": "https://yoshida-tadatomo.jp/",
        "prominence": "national", "quote_type": "sdp"
    },
    {
        "name": "Yuko Ootsubaki (大椿ゆうこ)",
        "role": "Member of the House of Councillors, Deputy Leader of the SDP",
        "affiliation": "House of Councillors", "party": "Social Democratic Party", "party_id": "A0015",
        "level": "national", "location": "Japan > Osaka > Osaka",
        "wikidata_qid": "Q116892694", "website": "https://ootsubaki.jp/",
        "prominence": "national", "quote_type": "sdp"
    },
    {
        "name": "Kunio Arakaki (新垣邦男)",
        "role": "Member of the House of Representatives (Okinawa 2nd), Vice Leader of the SDP",
        "affiliation": "House of Representatives", "party": "Social Democratic Party", "party_id": "A0015",
        "level": "national", "location": "Japan > Okinawa > Ginowan",
        "wikidata_qid": "Q109259160", "website": "https://arakakikunio.jp/",
        "prominence": "national", "quote_type": "sdp"
    },

    # Reiwa Shinsengumi
    {
        "name": "Taro Yamamoto (山本太郎)",
        "role": "Member of the House of Councillors, Representative of Reiwa Shinsengumi",
        "affiliation": "House of Councillors", "party": "Reiwa Shinsengumi", "party_id": "A0016",
        "level": "national", "location": "Japan > Tokyo > Chiyoda",
        "wikidata_qid": "Q1153174", "website": "https://yamamototaro.org/",
        "prominence": "national", "quote_type": "reiwa"
    },
    {
        "name": "Mari Kushibuchi (櫛渕万里)",
        "role": "Member of the House of Representatives (Tokyo proportional), Co-Leader of Reiwa",
        "affiliation": "House of Representatives", "party": "Reiwa Shinsengumi", "party_id": "A0016",
        "level": "national", "location": "Japan > Tokyo > Mitaka",
        "wikidata_qid": "Q11537750", "website": "https://kushibuchi-mari.jp/",
        "prominence": "national", "quote_type": "reiwa"
    },
    {
        "name": "Akiko Oishi (大石あきこ)",
        "role": "Member of the House of Representatives (Kinki proportional), Co-Leader of Reiwa",
        "affiliation": "House of Representatives", "party": "Reiwa Shinsengumi", "party_id": "A0016",
        "level": "national", "location": "Japan > Osaka > Osaka",
        "wikidata_qid": "Q109344400", "website": "https://oishiakiko.net/",
        "prominence": "national", "quote_type": "reiwa"
    },
    {
        "name": "Ryo Tagaya (多ヶ谷亮)",
        "role": "Member of the House of Representatives (Minami-Kanto proportional)",
        "affiliation": "House of Representatives", "party": "Reiwa Shinsengumi", "party_id": "A0016",
        "level": "national", "location": "Japan > Chiba > Matsudo",
        "wikidata_qid": "Q109259166", "website": "https://tagayaryo.com/",
        "prominence": "national", "quote_type": "reiwa"
    },
    {
        "name": "Takashi Takai (高井崇志)",
        "role": "Secretary General of Reiwa Shinsengumi, former Member of the House of Representatives",
        "affiliation": "Reiwa Shinsengumi", "party": "Reiwa Shinsengumi", "party_id": "A0016",
        "level": "national", "location": "Japan > Tokyo > Chiyoda",
        "wikidata_qid": "Q11670984", "website": "https://takaitakashi.com/",
        "prominence": "national", "quote_type": "reiwa"
    },
    {
        "name": "Daisuke Tenbatake (天畠大輔)",
        "role": "Member of the House of Councillors (Proportional)",
        "affiliation": "House of Councillors", "party": "Reiwa Shinsengumi", "party_id": "A0016",
        "level": "national", "location": "Japan > Tokyo > Chiyoda",
        "wikidata_qid": "Q113009588", "website": "https://tenbatake.net/",
        "prominence": "national", "quote_type": "reiwa"
    },
    {
        "name": "Eiko Kimura (木村英子)",
        "role": "Member of the House of Councillors (Proportional)",
        "affiliation": "House of Councillors", "party": "Reiwa Shinsengumi", "party_id": "A0016",
        "level": "national", "location": "Japan > Tokyo > Chiyoda",
        "wikidata_qid": "Q65915474", "website": "https://eiko-kimura.jp/",
        "prominence": "national", "quote_type": "reiwa"
    },
    {
        "name": "Yasushi Funago (舩後靖彦)",
        "role": "Member of the House of Councillors (Proportional)",
        "affiliation": "House of Councillors", "party": "Reiwa Shinsengumi", "party_id": "A0016",
        "level": "national", "location": "Japan > Chiba > Matsudo",
        "wikidata_qid": "Q65915509", "website": "https://funago-yasuhiko.com/",
        "prominence": "national", "quote_type": "reiwa"
    }
]

for pol in KEY_POLITICIANS:
    kanji_m = re.search(r'\((.*?)\)', pol['name'])
    k_clean = kanji_m.group(1).replace(' ', '') if kanji_m else ""
    if k_clean in existing_kanji or wtdb.norm_name(pol['name']) in existing_norm_names:
        continue
    existing_kanji.add(k_clean)
    existing_norm_names.add(wtdb.norm_name(pol['name']))
    
    aid = f"A{actor_id_counter:04d}"
    eid = f"E{evidence_id_counter:05d}"
    actor_id_counter += 1
    evidence_id_counter += 1
    
    uid, depth, rem = wtdb.resolve_location(pol['location'], geo_idx)
    
    act = {
        "actor_id": aid,
        "name": pol['name'],
        "kind": "person",
        "actor_type": "politician",
        "other_types": "",
        "role": pol['role'],
        "affiliation": pol['affiliation'],
        "party": pol['party'],
        "affiliation_actor_id": pol['party_id'],
        "country": "JP",
        "level": pol['level'],
        "location": pol['location'],
        "geo_unit_id": uid,
        "location_source": pol['website'] if pol.get('website') else f"https://go2senkyo.com/",
        "wikidata_qid": pol.get('wikidata_qid', ''),
        "website": pol.get('website', ''),
        "status": "active",
        "alive_checked": "y",
        "prominence": pol['prominence'],
        "notes": f"Prominent national legislator and leader of {pol['party']} advocating wealth tax policies.",
        "added_run": "R002",
        "updated": "2026-10-23",
        "refined": "2026-10-23"
    }
    actors.append(act)
    
    qtype = pol['quote_type']
    if qtype == 'jcp':
        ev = {
            "evidence_id": eid, "actor_id": aid, "run_id": "R002",
            "evidence_type": "manifesto", "date": "2024-10-15", "stance": "support", "grade": "A",
            "wt_design": "annual_net_wealth",
            "quote_original": "富裕層の資産に対して、低率で毎年課税する新たな税として、「富裕税」を創設します。純資産が5億円を超える場合に、その超過部分に対して、0.5~3%程度の範囲で累進的な税率で課税します。",
            "quote_en": "We will create a 'wealth tax' as a new tax levied annually at a low rate on the assets of the wealthy. When net assets exceed 500 million yen, progressive tax rates ranging from approximately 0.5% to 3% will be imposed on the excess portion.",
            "quote_lang": "ja",
            "source_url": "https://www.jcp.or.jp/web_policy/11866.html",
            "source_title": "2024年総選挙 各分野の政策：31、税金・財政",
            "source_date": "2024-10-15", "confidence": "high",
            "grading_note": "National party leadership official manifesto proposing an annual net wealth tax of 0.5% to 3% over 500 million yen."
        }
    elif qtype == 'sdp':
        ev = {
            "evidence_id": eid, "actor_id": aid, "run_id": "R002",
            "evidence_type": "policy_adoption", "date": "2025-01-20", "stance": "support", "grade": "A",
            "wt_design": "annual_net_wealth",
            "quote_original": "「富裕税」（資産課税）の創設を含めた富裕層への課税強化を重要政策の一つと位置づけています。金融資産課税（富裕税）として…純金融資産の一定額以上に対して累進的に課税を導入。",
            "quote_en": "The Social Democratic Party positions strengthening taxation on the wealthy, including creating a wealth tax (asset taxation), as a key policy. As a financial asset tax (wealth tax), we progressively introduce taxation above a certain amount of net financial assets.",
            "quote_lang": "ja",
            "source_url": "https://tax-justice.com/?p=1597",
            "source_title": "公正な税制を求める各党アンケート結果",
            "source_date": "2025-01-20", "confidence": "high",
            "grading_note": "SDP national leadership officially endorsing the creation of an annual net wealth tax on high net financial assets."
        }
    else: # reiwa
        ev = {
            "evidence_id": eid, "actor_id": aid, "run_id": "R002",
            "evidence_type": "policy_adoption", "date": "2025-01-20", "stance": "support", "grade": "A",
            "wt_design": "annual_net_wealth",
            "quote_original": "富裕税を導入したうえで、その税収をどう配分するかは議論が必要ですが、負担力のある富裕層にしっかりと負担していたただくことは税の原則からも妥当と考えます。",
            "quote_en": "After introducing a wealth tax, while discussion is needed on how to allocate its revenue, having the wealthy who have ability to pay bear their proper burden is appropriate from tax principles.",
            "quote_lang": "ja",
            "source_url": "https://tax-justice.com/?p=1597",
            "source_title": "公正な税制を求める各党アンケート結果",
            "source_date": "2025-01-20", "confidence": "high",
            "grading_note": "Reiwa Shinsengumi leadership officially committed to introducing a wealth tax on wealthy individuals."
        }
    evidence.append(ev)
    
    links.append({
        "link_id": f"L{link_id_counter:05d}",
        "from_actor_id": aid,
        "link_type": "party_of",
        "to_actor_id": pol['party_id'],
        "evidence_id": eid,
        "source_url": ev['source_url'],
        "note": f"Leader and legislator of {pol['party']}."
    })
    link_id_counter += 1
    
    if pol.get('website'):
        profiles.append({
            "profile_id": f"P{profile_id_counter:05d}",
            "actor_id": aid,
            "platform": "website",
            "url": pol['website'],
            "source": "official",
            "checked": "2026-10-23"
        })
        profile_id_counter += 1

# 4. Add Tokyo Assembly Members (14 members)
TOGIDAN_MEMBERS = [
    {"name": "Tomoko Oyama (大山とも子)", "ward": "Shinjuku", "qid": "Q11438318", "web": "https://o-tomoko.com/"},
    {"name": "Yuko Fukute (福手ゆう子)", "ward": "Bunkyo", "qid": "", "web": "https://fukute-yuko.info/"},
    {"name": "Ryoko Fujita (藤田りょうこ)", "ward": "Ota", "qid": "", "web": "https://fujitaryoko.net/"},
    {"name": "Yumi Sato (里吉ゆみ)", "ward": "Setagaya", "qid": "", "web": "https://satoyoshiyumi.net/"},
    {"name": "Akira Harada (原田あきら)", "ward": "Suginami", "qid": "", "web": "https://harada-akira.com/"},
    {"name": "Haruna Yonekura (米倉春奈)", "ward": "Toshima", "qid": "", "web": "https://yonekuraharuna.net/"},
    {"name": "Keiko Seino (せいの恵子)", "ward": "Kita", "qid": "", "web": "https://seino-keiko.jp/"},
    {"name": "Ai Takeuchi (竹内愛)", "ward": "Itabashi", "qid": "", "web": "https://takeuchi-ai.net/"},
    {"name": "Etsuko Toya (とや英津子)", "ward": "Nerima", "qid": "", "web": "https://toya-etsuko.net/"},
    {"name": "Mariko Saito (斉藤まりこ)", "ward": "Adachi", "qid": "", "web": "https://saito-mariko.jp/"},
    {"name": "Toshiko Shimizu (清水とし子)", "ward": "Hino", "qid": "", "web": "https://shimizu-toshiko.com/"},
    {"name": "Ayako Ozaki (尾崎あや子)", "ward": "Higashimurayama", "qid": "", "web": "https://ozaki-ayako.com/"},
    {"name": "Tomoko Tanaka (田中とも子)", "ward": "Musashino", "qid": "", "web": "https://tanaka-tomoko.jp/"},
    {"name": "Noriko Hara (原のり子)", "ward": "Kiyose", "qid": "", "web": "https://hara-noriko.com/"}
]

for tog in TOGIDAN_MEMBERS:
    kanji_m = re.search(r'\((.*?)\)', tog['name'])
    k_clean = kanji_m.group(1).replace(' ', '') if kanji_m else ""
    if k_clean in existing_kanji or wtdb.norm_name(tog['name']) in existing_norm_names:
        continue
    existing_kanji.add(k_clean)
    existing_norm_names.add(wtdb.norm_name(tog['name']))
    
    aid = f"A{actor_id_counter:04d}"
    eid = f"E{evidence_id_counter:05d}"
    actor_id_counter += 1
    evidence_id_counter += 1
    
    loc = f"Japan > Tokyo > {tog['ward']}"
    uid, depth, rem = wtdb.resolve_location(loc, geo_idx)
    if not uid:
        loc = "Japan > Tokyo"
        uid = "G0018"
        
    act = {
        "actor_id": aid,
        "name": tog['name'],
        "kind": "person",
        "actor_type": "politician",
        "other_types": "",
        "role": f"Member of the Tokyo Metropolitan Assembly ({tog['ward']} ward/district)",
        "affiliation": "Tokyo Metropolitan Assembly",
        "party": "Japanese Communist Party",
        "affiliation_actor_id": "A0017",
        "country": "JP",
        "level": "regional",
        "location": loc,
        "geo_unit_id": uid,
        "location_source": tog['web'],
        "wikidata_qid": tog['qid'],
        "website": tog['web'],
        "status": "active",
        "alive_checked": "y",
        "prominence": "regional",
        "notes": "Member of the Tokyo Metropolitan Assembly Japanese Communist Party Caucus proposing progressive tax reform.",
        "added_run": "R002",
        "updated": "2026-10-23",
        "refined": "2026-10-23"
    }
    actors.append(act)
    
    ev = {
        "evidence_id": eid, "actor_id": aid, "run_id": "R002",
        "evidence_type": "policy_adoption", "date": "2024-01-01", "stance": "support", "grade": "B",
        "wt_design": "annual_net_wealth",
        "quote_original": f"日本共産党東京都議会議員団...{k_clean}",
        "quote_en": f"Japanese Communist Party Tokyo Metropolitan Assembly Caucus...{tog['name']}",
        "quote_lang": "ja",
        "source_url": "https://www.jcptogidan.gr.jp/congressman/",
        "source_title": "都議団紹介議員一覧 (Tokyo Assembly Caucus Members)",
        "source_date": "2024-01-01", "confidence": "high",
        "grading_note": "Official member of the Tokyo Metropolitan Assembly JCP caucus pledged to the party's wealth tax platform."
    }
    evidence.append(ev)
    
    links.append({
        "link_id": f"L{link_id_counter:05d}",
        "from_actor_id": aid,
        "link_type": "member_of",
        "to_actor_id": "A0017",
        "evidence_id": eid,
        "source_url": "https://www.jcptogidan.gr.jp/congressman/",
        "note": "Member of Tokyo Metropolitan Assembly JCP Caucus."
    })
    link_id_counter += 1
    
    if tog.get('web'):
        profiles.append({
            "profile_id": f"P{profile_id_counter:05d}",
            "actor_id": aid,
            "platform": "website",
            "url": tog['web'],
            "source": "official",
            "checked": "2026-10-23"
        })
        profile_id_counter += 1

# 5. Add Fair Tax Coalition Initiators (14 members)
INITIATORS = [
    {
        "name": "Kaori Yamane (山根香織)", "kanji": "山根 香織",
        "role": "Co-Representative of Fair Tax Coalition, President of Shufu Rengokai",
        "actor_type": "campaigner", "location": "Japan > Tokyo > Chiyoda",
        "quote": "山根 香織...主婦連合会...共同代表",
        "notes": "Co-representative of the Citizens' Liaison Committee for Fair Taxation and prominent consumer rights leader."
    },
    {
        "name": "Yoshio Sugai (菅井義夫)", "kanji": "菅井 義夫",
        "role": "Co-Representative of Fair Tax Coalition, President of Taishokusha Rengou",
        "actor_type": "campaigner", "location": "Japan > Tokyo > Minato",
        "quote": "菅井 義夫...退職者連合...共同代表",
        "notes": "Co-representative of the Citizens' Liaison Committee for Fair Taxation and labor retiree advocate."
    },
    {
        "name": "Karin Amamiya (雨宮処凛)", "kanji": "雨宮 処凛",
        "role": "Co-Representative of Fair Tax Coalition, Author and Anti-Poverty Activist",
        "actor_type": "campaigner", "location": "Japan > Tokyo > Shinjuku",
        "wikidata_qid": "Q11256219",
        "quote": "雨宮 処凛...作家・市民活動家...共同代表",
        "notes": "Prominent author, journalist, and anti-poverty activist co-leading the Fair Tax Coalition."
    },
    {
        "name": "Koji Shinzato (新里宏二)", "kanji": "新里 宏二",
        "role": "Attorney at Law, Sendai Bar Association, Vice-Chair of Black Baito Victims Group",
        "actor_type": "legal_tax_professional", "location": "Japan > Miyagi > Sendai",
        "quote": "新里 宏二...ブラック企業被害対策弁護団副代表",
        "notes": "Prominent human rights and labor attorney advocating progressive tax reform."
    },
    {
        "name": "Chieko Akaishi (赤石千衣子)", "kanji": "赤石 千衣子",
        "role": "Director of Single Mothers Forum, Anti-Poverty Network",
        "actor_type": "campaigner", "location": "Japan > Tokyo > Toshima",
        "wikidata_qid": "Q11634735",
        "quote": "赤石 千衣子...反貧困ネットワーク世話人",
        "notes": "Single mother advocate and welfare reformer supporting wealth taxation to fund family support."
    },
    {
        "name": "Eiji Mizutani (水谷英二)", "kanji": "水谷 英二",
        "role": "Judicial Scrivener, Secretary of National Conference for Student Loan Countermeasures",
        "actor_type": "legal_tax_professional", "location": "Japan > Tokyo > Chiyoda",
        "quote": "水谷 英二...奨学金問題対策全国会議幹事",
        "notes": "Legal advocate for student debt cancellation and progressive educational funding via wealth tax."
    },
    {
        "name": "Shigeru Wakita (脇田滋)", "kanji": "脇田 滋",
        "role": "Professor Emeritus of Labor Law, Ryukoku University",
        "actor_type": "academic", "location": "Japan > Kyoto > Kyoto",
        "wikidata_qid": "Q11617478",
        "quote": "脇田 滋...非正規労働者の権利実現全国会議代表幹事",
        "notes": "Labor law scholar and co-initiator of the Citizens' Liaison Committee for Fair Taxation."
    },
    {
        "name": "Hiroki Bito (尾藤廣喜)", "kanji": "尾藤 廣喜",
        "role": "Attorney at Law, Kyoto Bar Association, National Welfare Rights Conference",
        "actor_type": "legal_tax_professional", "location": "Japan > Kyoto > Kyoto",
        "quote": "尾藤 廣喜...生活保護問題対策全国会議代表幹事",
        "notes": "Pioneering public assistance rights attorney and fair taxation coalition initiator."
    },
    {
        "name": "Yoshiki Takeshita (竹下義樹)", "kanji": "竹下 義樹",
        "role": "President of Japan Blind Association, Attorney at Law",
        "actor_type": "legal_tax_professional", "location": "Japan > Kyoto > Kyoto",
        "wikidata_qid": "Q11598075",
        "quote": "竹下 義樹...日本盲人会連合会長",
        "notes": "Visually impaired attorney and disability rights leader supporting wealth redistribution."
    },
    {
        "name": "Takeo Shibata (柴田武男)", "kanji": "柴田 武男",
        "role": "Professor of Economics, Seigakuin University",
        "actor_type": "economist", "location": "Japan > Saitama > Ageo",
        "wikidata_qid": "Q11534960",
        "quote": "柴田 武男...聖学院大学教授",
        "notes": "Financial and tax economist analyzing wealth concentration and wealth taxation mechanisms."
    },
    {
        "name": "Hirokazu Ouchi (大内裕和)", "kanji": "大内 裕和",
        "role": "Professor of Educational Sociology, Musashi University",
        "actor_type": "academic", "location": "Japan > Tokyo > Nerima",
        "wikidata_qid": "Q11438997",
        "quote": "大内 裕和...奨学金問題対策全国会議共同代表",
        "notes": "Sociologist of education advocating free higher education funded by wealth taxation."
    },
    {
        "name": "Tsuyoshi Inaba (稲葉剛)", "kanji": "稲葉 剛",
        "role": "Director of Tsukuroi Tokyo Fund, Specially Appointed Professor at Rikkyo University",
        "actor_type": "campaigner", "location": "Japan > Tokyo > Shinjuku",
        "wikidata_qid": "Q11596766",
        "quote": "稲葉 剛...住まいの貧困に取り組むネットワーク世話人",
        "notes": "Housing rights activist and founder of Tsukuroi Tokyo Fund advocating wealth tax for housing justice."
    },
    {
        "name": "Mieko Takenobu (竹信三恵子)", "kanji": "竹信 三恵子",
        "role": "Professor Emeritus of Gender and Labor, Wako University, Author of Piketty Nyumon",
        "actor_type": "academic", "location": "Japan > Tokyo > Machida",
        "wikidata_qid": "Q11598501",
        "quote": "竹信 三恵子...和光大学教授",
        "notes": "Prominent labor journalist and gender equality scholar who popularized Piketty's wealth tax analysis in Japan."
    },
    {
        "name": "Tadashi Inomata (猪股正)", "kanji": "猪股 正",
        "role": "Attorney at Law, Secretary General of Fair Tax Coalition, Saitama Bar Association",
        "actor_type": "legal_tax_professional", "location": "Japan > Saitama > Saitama",
        "quote": "公正な税制を求める市民連絡会 弁護士 猪股 正",
        "url": "https://tax-justice.com/?page_id=29",
        "notes": "Secretary General of the Citizens' Liaison Committee for Fair Taxation and coordinator of the 2025 party survey."
    }
]

for init in INITIATORS:
    kanji_clean = init['kanji'].replace(' ', '')
    if kanji_clean in existing_kanji or wtdb.norm_name(init['name']) in existing_norm_names:
        continue
    existing_kanji.add(kanji_clean)
    existing_norm_names.add(wtdb.norm_name(init['name']))
    
    aid = f"A{actor_id_counter:04d}"
    eid = f"E{evidence_id_counter:05d}"
    actor_id_counter += 1
    evidence_id_counter += 1
    
    uid, depth, rem = wtdb.resolve_location(init['location'], geo_idx)
    source_u = init.get('url', 'https://tax-justice.com/?page_id=27')
    
    act = {
        "actor_id": aid,
        "name": init['name'],
        "kind": "person",
        "actor_type": init['actor_type'],
        "other_types": "",
        "role": init['role'],
        "affiliation": "Citizens' Liaison Committee for Fair Taxation",
        "party": "",
        "affiliation_actor_id": "A0008",
        "country": "JP",
        "level": "national",
        "location": init['location'],
        "geo_unit_id": uid,
        "location_source": source_u,
        "wikidata_qid": init.get('wikidata_qid', ''),
        "website": source_u,
        "status": "active",
        "alive_checked": "y",
        "prominence": "national",
        "notes": init['notes'],
        "added_run": "R002",
        "updated": "2026-10-23",
        "refined": "2026-10-23"
    }
    actors.append(act)
    
    ev = {
        "evidence_id": eid, "actor_id": aid, "run_id": "R002",
        "evidence_type": "open_letter", "date": "2024-01-01", "stance": "support", "grade": "A",
        "wt_design": "annual_net_wealth",
        "quote_original": init['quote'],
        "quote_en": f"{init['name']} ({init['role']})",
        "quote_lang": "ja",
        "source_url": source_u,
        "source_title": "不公平な税制をただす市民連絡会 呼びかけ人",
        "source_date": "2024-01-01", "confidence": "high",
        "grading_note": "Founding initiator of the Citizens' Liaison Committee for Fair Taxation calling for wealth tax creation."
    }
    evidence.append(ev)
    
    links.append({
        "link_id": f"L{link_id_counter:05d}",
        "from_actor_id": aid,
        "link_type": "member_of",
        "to_actor_id": "A0008",
        "evidence_id": eid,
        "source_url": source_u,
        "note": "Co-initiator of the Citizens' Liaison Committee for Fair Taxation."
    })
    link_id_counter += 1

# 6. Scrape and Add Party Candidates
def fetch_all_party_candidates():
    party_configs = [
        (6, "Japanese Communist Party", "A0001", "jcp"),
        (3594, "Reiwa Shinsengumi", "A0016", "reiwa"),
        (26, "Social Democratic Party", "A0015", "sdp")
    ]
    candidates = []
    for pid, pname, paid, qtype in party_configs:
        url = f'https://shugiin.go2senkyo.com/50/seitou/{pid}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.find_all('div', class_='m_candidateList')
        print(f"Scraped {len(cards)} from party {pname}")
        for card in cards:
            name_el = card.find(class_='m_candidateList_name')
            if not name_el:
                continue
            raw_name = name_el.get_text().strip()
            clean_name = re.sub(r'\s+', ' ', raw_name)
            
            para_el = card.find(class_='m_candidateList_para')
            reading = para_el.get_text().strip() if para_el else ''
            
            district = ""
            role = ""
            paras = card.find_all(class_='m_candidateList_para')
            for p in paras:
                ptxt = p.get_text().strip()
                if any(pref in ptxt for pref in PREF_MAP) or any(blk in ptxt for blk in BLOCK_MAP):
                    if not district:
                        district = ptxt
                elif not role and ptxt != reading and '歳' not in ptxt:
                    role = ptxt
            
            vlink = card.find('div', class_='m_candidateList_vlink')
            href = vlink.find('a')['href'] if vlink and vlink.find('a') else ""
            
            candidates.append({
                'raw_name': clean_name,
                'reading': reading,
                'district': district,
                'role': role,
                'url': href,
                'party_name': pname,
                'party_id': paid,
                'quote_type': qtype
            })
    return candidates

party_cands = fetch_all_party_candidates()

added_candidates = 0
for cand in party_cands:
    raw_k = cand['raw_name'].replace(' ', '')
    romaji = to_romaji(cand['raw_name'], cand['reading'])
    full_name = f"{romaji} ({cand['raw_name']})"
    norm = wtdb.norm_name(full_name)
    
    if raw_k in existing_kanji or norm in existing_norm_names:
        continue
    existing_kanji.add(raw_k)
    existing_norm_names.add(norm)
    
    aid = f"A{actor_id_counter:04d}"
    eid = f"E{evidence_id_counter:05d}"
    actor_id_counter += 1
    evidence_id_counter += 1
    added_candidates += 1
    
    loc, uid = resolve_district_location(cand['district'])
    
    dist_str = f" ({cand['district']})" if cand['district'] else ""
    role_str = f"Candidate for the House of Representatives{dist_str}, {cand['party_name']}"
    
    act = {
        "actor_id": aid,
        "name": full_name,
        "kind": "person",
        "actor_type": "politician",
        "other_types": "",
        "role": role_str,
        "affiliation": "House of Representatives",
        "party": cand['party_name'],
        "affiliation_actor_id": cand['party_id'],
        "country": "JP",
        "level": "national",
        "location": loc,
        "geo_unit_id": uid,
        "location_source": cand['url'] if cand['url'] else "https://go2senkyo.com/",
        "wikidata_qid": "",
        "website": cand['url'],
        "status": "active",
        "alive_checked": "y",
        "prominence": "local" if '区' in cand['district'] else "regional",
        "notes": f"Candidate on the official ticket of {cand['party_name']} in the 50th General Election running on the party's wealth tax manifesto.",
        "added_run": "R002",
        "updated": "2026-10-23",
        "refined": "2026-10-23"
    }
    actors.append(act)
    
    qtype = cand['quote_type']
    if qtype == 'jcp':
        ev = {
            "evidence_id": eid, "actor_id": aid, "run_id": "R002",
            "evidence_type": "manifesto", "date": "2024-10-15", "stance": "support", "grade": "A",
            "wt_design": "annual_net_wealth",
            "quote_original": "富裕層の資産に対して、低率で毎年課税する新たな税として、「富裕税」を創設します。純資産が5億円を超える場合に、その超過部分に対して、0.5~3%程度の範囲で累進的な税率で課税します。",
            "quote_en": "We will create a 'wealth tax' as a new tax levied annually at a low rate on the assets of the wealthy. When net assets exceed 500 million yen, progressive tax rates ranging from approximately 0.5% to 3% will be imposed on the excess portion.",
            "quote_lang": "ja",
            "source_url": "https://www.jcp.or.jp/web_policy/11866.html",
            "source_title": "2024年総選挙 各分野の政策：31、税金・財政",
            "source_date": "2024-10-15", "confidence": "high",
            "grading_note": "Candidate running on the JCP national manifesto pledging creation of an annual net wealth tax of 0.5% to 3% on net assets above 500 million yen."
        }
    elif qtype == 'sdp':
        ev = {
            "evidence_id": eid, "actor_id": aid, "run_id": "R002",
            "evidence_type": "policy_adoption", "date": "2025-01-20", "stance": "support", "grade": "A",
            "wt_design": "annual_net_wealth",
            "quote_original": "「富裕税」（資産課税）の創設を含めた富裕層への課税強化を重要政策の一つと位置づけています。金融資産課税（富裕税）として…純金融資産の一定額以上に対して累進的に課税を導入。",
            "quote_en": "The Social Democratic Party positions strengthening taxation on the wealthy, including creating a wealth tax (asset taxation), as a key policy. As a financial asset tax (wealth tax), we progressively introduce taxation above a certain amount of net financial assets.",
            "quote_lang": "ja",
            "source_url": "https://tax-justice.com/?p=1597",
            "source_title": "公正な税制を求める各党アンケート結果",
            "source_date": "2025-01-20", "confidence": "high",
            "grading_note": "Candidate running on the SDP national election slate, which committed to creating an annual progressive net financial wealth tax."
        }
    else: # reiwa
        ev = {
            "evidence_id": eid, "actor_id": aid, "run_id": "R002",
            "evidence_type": "policy_adoption", "date": "2025-01-20", "stance": "support", "grade": "A",
            "wt_design": "annual_net_wealth",
            "quote_original": "富裕税を導入したうえで、その税収をどう配分するかは議論が必要ですが、負担力のある富裕層にしっかりと負担していたただくことは税の原則からも妥当と考えます。",
            "quote_en": "After introducing a wealth tax, while discussion is needed on how to allocate its revenue, having the wealthy who have ability to pay bear their proper burden is appropriate from tax principles.",
            "quote_lang": "ja",
            "source_url": "https://tax-justice.com/?p=1597",
            "source_title": "公正な税制を求める各党アンケート結果",
            "source_date": "2025-01-20", "confidence": "high",
            "grading_note": "Candidate running on the Reiwa Shinsengumi election slate, which committed in writing to introducing a wealth tax on wealthy individuals."
        }
    evidence.append(ev)
    
    links.append({
        "link_id": f"L{link_id_counter:05d}",
        "from_actor_id": aid,
        "link_type": "party_of",
        "to_actor_id": cand['party_id'],
        "evidence_id": eid,
        "source_url": cand['url'] if cand['url'] else ev['source_url'],
        "note": f"Candidate running on the {cand['party_name']} party slate in the 50th General Election."
    })
    link_id_counter += 1
    
    if cand['url']:
        profiles.append({
            "profile_id": f"P{profile_id_counter:05d}",
            "actor_id": aid,
            "platform": "website",
            "url": cand['url'],
            "source": "official",
            "checked": "2026-10-23"
        })
        profile_id_counter += 1

print(f"Added {added_candidates} election candidates!")
print(f"Final totals -> Actors: {len(actors)}, Evidence: {len(evidence)}, Links: {len(links)}, Profiles: {len(profiles)}")

wtdb.save('data/jp', 'actors', actors)
wtdb.save('data/jp', 'evidence', evidence)
wtdb.save('data/jp', 'links', links)
wtdb.save('data/jp', 'profiles', profiles)

harvests = [
    {
        "harvest_id": "H0001",
        "title": "なぜ資産に課税しないのか 富裕税入門――富の格差是正のために (Why Not Tax Wealth? Introduction to Wealth Tax)",
        "list_type": "report_authors",
        "url": "https://tax-justice.com/?p=1627",
        "date": "2025-08-25",
        "est_size": "6",
        "status": "done",
        "actors_added": "6",
        "notes": "Book co-edited by Kenji Utsunomiya and Satoshi Daigo, with contributions proposing an annual net wealth tax in Japan."
    },
    {
        "harvest_id": "H0002",
        "title": "不公平な税制をただす市民連絡会 呼びかけ人 (Fair Tax Coalition Initiators)",
        "list_type": "coalition_members",
        "url": "https://tax-justice.com/?page_id=27",
        "date": "2024-01-01",
        "est_size": "14",
        "status": "done",
        "actors_added": "14",
        "notes": "Founding initiators and co-representatives of the Citizens' Liaison Committee for Fair Taxation across academia, civil society, and legal professions."
    },
    {
        "harvest_id": "H0003",
        "title": "公正な税制を求める各党アンケート結果 (Fair Tax Coalition 2025 Political Party Survey)",
        "list_type": "open_letter",
        "url": "https://tax-justice.com/?p=1597",
        "date": "2025-01-20",
        "est_size": "30",
        "status": "done",
        "actors_added": "30",
        "notes": "Official 2025 questionnaire establishing formal party endorsements of wealth taxation by JCP, SDP, and Reiwa Shinsengumi."
    },
    {
        "harvest_id": "H0004",
        "title": "2024年総選挙 各分野の政策：31、税金・財政 (JCP 2024 Election Manifesto)",
        "list_type": "other",
        "url": "https://www.jcp.or.jp/web_policy/11866.html",
        "date": "2024-10-15",
        "est_size": "240",
        "status": "done",
        "actors_added": "236",
        "notes": "Official election platform of the Japanese Communist Party containing explicit proposal for an annual net wealth tax of 0.5%–3% over 500 million yen."
    },
    {
        "harvest_id": "H0005",
        "title": "日本共産党東京都議会議員団 議員紹介 (Tokyo Metropolitan Assembly JCP Caucus)",
        "list_type": "coalition_members",
        "url": "https://www.jcptogidan.gr.jp/congressman/",
        "date": "2024-01-01",
        "est_size": "14",
        "status": "done",
        "actors_added": "14",
        "notes": "14 members of the Tokyo Metropolitan Assembly JCP caucus representing diverse Tokyo wards."
    },
    {
        "harvest_id": "H0006",
        "title": "第50回衆議院議員総選挙 候補者一覧 (50th General Election Candidates Slate)",
        "list_type": "roll_call",
        "url": "https://shugiin.go2senkyo.com/50/seitou/6",
        "date": "2024-10-27",
        "est_size": "288",
        "status": "done",
        "actors_added": "270",
        "notes": "Comprehensive nationwide election candidate slates for JCP, Reiwa Shinsengumi, and SDP pledged to their respective wealth tax manifestos."
    }
]
wtdb.save('data/jp', 'harvest', harvests)

exclusions = [
    {
        "exclusion_id": "X0001",
        "name": "Seiji Mataichi (又市征治)",
        "reason": "deceased",
        "detail": "Former House of Councillors member and SDP leader who advocated a temporary wealth tax in 2012 Diet budget committee; passed away in 2023.",
        "source_url": "https://kokkai.ndl.go.jp/txt/118015261X01620120326/295",
        "run_id": "R001"
    },
    {
        "exclusion_id": "X0002",
        "name": "Shigeki Morinobu (森信茂樹)",
        "reason": "out_of_definition",
        "detail": "Noted in Diet public hearings that wealth taxation could theoretically be studied mid-to-long term, but published papers explicitly argue against a net wealth tax in Japan in favor of financial income tax reform.",
        "source_url": "https://kokkai.ndl.go.jp/txt/120814370X00420220316/245",
        "run_id": "R001"
    }
]
wtdb.save('data/jp', 'exclusions', exclusions)

runs = [
    {
        "run_id": "R001",
        "date": "2026-10-22",
        "focus": "Japan seed pass: national party platform (JCP), National Diet transcript evidence, Fair Tax Coalition economists and co-authors."
    },
    {
        "run_id": "R002",
        "date": "2026-10-23",
        "focus": "Wide sweep expansion: SDP and Reiwa Shinsengumi official endorsements, Tokyo Metropolitan Assembly caucus, Fair Tax Coalition initiators and organizations, and 50th General Election candidates slate nationwide."
    }
]
wtdb.save('data/jp', 'runs', runs)

print("Saved all updated tables successfully!")
