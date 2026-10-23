#!/usr/bin/env python3
"""Build Belgium geography register and boundaries from Eurostat GISCO 2024 data.

Data sources:
- Eurostat GISCO LAU 2024 (Local Administrative Units - 581 Belgian municipalities)
- Eurostat GISCO NUTS 2024 (NUTS 1 Regions and NUTS 2 Provinces)
- Licence: CC BY 4.0 / European Commission Decision 2011/833/EU (Attribution: (c) European Union, 1995-today)
- Official code scheme: Statbel NIS/INS codes (REFNIS)
"""
import csv, json, os, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache" / "be"
CACHE.mkdir(parents=True, exist_ok=True)

GISCO_LAU_URL = "https://gisco-services.ec.europa.eu/distribution/v2/lau/topojson/LAU_RG_01M_2024_4326.json"
GISCO_NUTS2_URL = "https://gisco-services.ec.europa.eu/distribution/v2/nuts/topojson/NUTS_RG_01M_2024_4326_LEVL_2.json"
GISCO_NUTS1_URL = "https://gisco-services.ec.europa.eu/distribution/v2/nuts/topojson/NUTS_RG_01M_2024_4326_LEVL_1.json"

def fetch_json(url, local_path):
    if local_path.exists() and local_path.stat().st_size > 1000:
        print(f"Using cached {local_path.name}")
        return json.load(open(local_path, encoding="utf-8"))
    print(f"Downloading {url} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req).read()
    data = json.loads(raw.decode("utf-8"))
    with open(local_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"Saved {local_path.name} ({len(raw) // 1024} KB)")
    return data

def extract_belgium_topo(src_topo, out_path, id_prefix="BE"):
    obj_key = list(src_topo["objects"].keys())[0]
    geoms = src_topo["objects"][obj_key]["geometries"]
    be_geoms = [g for g in geoms if g.get("id", "").startswith(id_prefix) or g.get("properties", {}).get("CNTR_CODE") == "BE"]
    
    # We only keep referenced arcs to minimize file size
    used_arcs = set()
    for g in be_geoms:
        arcs = g.get("arcs", [])
        if g["type"] == "MultiPolygon":
            for poly in arcs:
                for ring in poly:
                    for a in ring:
                        used_arcs.add(a if a >= 0 else ~a)
        elif g["type"] == "Polygon":
            for ring in arcs:
                for a in ring:
                    used_arcs.add(a if a >= 0 else ~a)

    sub_topo = {
        "type": "Topology",
        "transform": src_topo.get("transform"),
        "arcs": src_topo["arcs"],  # keep original arc array so indices match
        "objects": {
            obj_key: {
                "type": "GeometryCollection",
                "geometries": be_geoms
            }
        }
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(sub_topo, f)
    print(f"Wrote {out_path.name} with {len(be_geoms)} geometries")
    return obj_key

def get_province_info(nis_code):
    c = str(nis_code).strip()
    if c.startswith("1"):
        return "G0008", "Antwerpen", "BE21"
    if c.startswith("21"):
        return "G0007", "Brussels-Capital Region", "BE10"
    if c.startswith("23") or c.startswith("24"):
        return "G0011", "Vlaams-Brabant", "BE24"
    if c.startswith("25"):
        return "G0013", "Brabant wallon", "BE31"
    if c.startswith("3"):
        return "G0012", "West-Vlaanderen", "BE25"
    if c.startswith("4"):
        return "G0010", "Oost-Vlaanderen", "BE23"
    if c.startswith("5"):
        return "G0014", "Hainaut", "BE32"
    if c.startswith("6"):
        return "G0015", "Liège", "BE33"
    if c.startswith("7"):
        return "G0009", "Limburg", "BE22"
    if c.startswith("8"):
        return "G0016", "Luxembourg", "BE34"
    if c.startswith("9"):
        return "G0017", "Namur", "BE35"
    raise ValueError(f"Unknown NIS code {nis_code}")

def build_geo_units(be_lau_topo, obj_name):
    # Header: geo_unit_id,name,level,unit_type,parent_id,website,sweep_status,swept_run,swept_date,queries_run,hits,notes,code
    rows = []
    # Root
    rows.append({
        "geo_unit_id": "G0001",
        "name": "Belgium",
        "level": "national",
        "unit_type": "country",
        "parent_id": "",
        "website": "https://www.belgium.be",
        "sweep_status": "pending",
        "swept_run": "",
        "swept_date": "",
        "queries_run": "",
        "hits": "",
        "notes": "",
        "code": "BE"
    })
    # Federal Institutions
    rows.append({
        "geo_unit_id": "G0002",
        "name": "Chamber of Representatives",
        "level": "national",
        "unit_type": "legislature",
        "parent_id": "G0001",
        "website": "https://www.dekamer.be",
        "sweep_status": "pending",
        "swept_run": "",
        "swept_date": "",
        "queries_run": "",
        "hits": "",
        "notes": "Federal parliament lower house (Kamer van volksvertegenwoordigers / Chambre des représentants)",
        "code": ""
    })
    rows.append({
        "geo_unit_id": "G0003",
        "name": "Senate",
        "level": "national",
        "unit_type": "legislature",
        "parent_id": "G0001",
        "website": "https://www.senate.be",
        "sweep_status": "pending",
        "swept_run": "",
        "swept_date": "",
        "queries_run": "",
        "hits": "",
        "notes": "Federal parliament upper house (Senaat / Sénat)",
        "code": ""
    })
    rows.append({
        "geo_unit_id": "G0004",
        "name": "Federal Government",
        "level": "national",
        "unit_type": "executive",
        "parent_id": "G0001",
        "website": "https://www.belgium.be",
        "sweep_status": "pending",
        "swept_run": "",
        "swept_date": "",
        "queries_run": "",
        "hits": "",
        "notes": "Federal Council of Ministers",
        "code": ""
    })
    # 3 Regions
    rows.append({
        "geo_unit_id": "G0005",
        "name": "Flemish Region",
        "level": "region",
        "unit_type": "region",
        "parent_id": "G0001",
        "website": "https://www.vlaanderen.be",
        "sweep_status": "pending",
        "swept_run": "",
        "swept_date": "",
        "queries_run": "",
        "hits": "",
        "notes": "Vlaams Gewest / Flanders",
        "code": "BE2"
    })
    rows.append({
        "geo_unit_id": "G0006",
        "name": "Walloon Region",
        "level": "region",
        "unit_type": "region",
        "parent_id": "G0001",
        "website": "https://www.wallonie.be",
        "sweep_status": "pending",
        "swept_run": "",
        "swept_date": "",
        "queries_run": "",
        "hits": "",
        "notes": "Région wallonne / Wallonia",
        "code": "BE3"
    })
    rows.append({
        "geo_unit_id": "G0007",
        "name": "Brussels-Capital Region",
        "level": "region",
        "unit_type": "region",
        "parent_id": "G0001",
        "website": "https://be.brussels",
        "sweep_status": "pending",
        "swept_run": "",
        "swept_date": "",
        "queries_run": "",
        "hits": "",
        "notes": "Région de Bruxelles-Capitale / Brussels Hoofdstedelijk Gewest",
        "code": "BE1"
    })

    # Provinces (5 in Flanders, 5 in Wallonia)
    provinces = [
        ("G0008", "Antwerpen", "G0005", "BE21"),
        ("G0009", "Limburg", "G0005", "BE22"),
        ("G0010", "Oost-Vlaanderen", "G0005", "BE23"),
        ("G0011", "Vlaams-Brabant", "G0005", "BE24"),
        ("G0012", "West-Vlaanderen", "G0005", "BE25"),
        ("G0013", "Brabant wallon", "G0006", "BE31"),
        ("G0014", "Hainaut", "G0006", "BE32"),
        ("G0015", "Liège", "G0006", "BE33"),
        ("G0016", "Luxembourg", "G0006", "BE34"),
        ("G0017", "Namur", "G0006", "BE35"),
    ]
    for gid, pname, parent, pcode in provinces:
        rows.append({
            "geo_unit_id": gid,
            "name": pname,
            "level": "county",
            "unit_type": "province",
            "parent_id": parent,
            "website": "",
            "sweep_status": "pending",
            "swept_run": "",
            "swept_date": "",
            "queries_run": "",
            "hits": "",
            "notes": "",
            "code": pcode
        })

    # 581 Municipalities
    geoms = be_lau_topo["objects"][obj_name]["geometries"]
    # Sort by NIS code
    sorted_geoms = sorted(geoms, key=lambda g: g["properties"]["GISCO_ID"])
    
    gid_num = 18
    for g in sorted_geoms:
        p = g["properties"]
        gisco_id = p["GISCO_ID"]
        nis_code = gisco_id.replace("BE_", "")
        name = p["LAU_NAME"]
        parent_id, prov_name, prov_code = get_province_info(nis_code)
        
        rows.append({
            "geo_unit_id": f"G{gid_num:04d}",
            "name": name,
            "level": "council",
            "unit_type": "municipality",
            "parent_id": parent_id,
            "website": "",
            "sweep_status": "pending",
            "swept_run": "",
            "swept_date": "",
            "queries_run": "",
            "hits": "",
            "notes": f"NIS {nis_code}; Pop {p.get('POP_2024', '')}",
            "code": nis_code
        })
        gid_num += 1

    out_file = ROOT / "data" / "be" / "geo_units.csv"
    with open(out_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "geo_unit_id", "name", "level", "unit_type", "parent_id", "website",
            "sweep_status", "swept_run", "swept_date", "queries_run", "hits", "notes", "code"
        ])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {out_file} with {len(rows)} units ({gid_num - 18} municipalities)")

def main():
    print("Step 1: Downloading Eurostat TopoJSON files...")
    lau_topo = fetch_json(GISCO_LAU_URL, CACHE / "lau_2024.json")
    nuts2_topo = fetch_json(GISCO_NUTS2_URL, CACHE / "nuts2_2024.json")
    nuts1_topo = fetch_json(GISCO_NUTS1_URL, CACHE / "nuts1_2024.json")

    print("\nStep 2: Extracting Belgian subsets...")
    lau_obj = extract_belgium_topo(lau_topo, CACHE / "be_lau.json", id_prefix="BE_")
    nuts2_obj = extract_belgium_topo(nuts2_topo, CACHE / "be_nuts2.json", id_prefix="BE")
    nuts1_obj = extract_belgium_topo(nuts1_topo, CACHE / "be_nuts1.json", id_prefix="BE")

    print("\nStep 3: Building geo_units.csv...")
    be_lau = json.load(open(CACHE / "be_lau.json", encoding="utf-8"))
    build_geo_units(be_lau, lau_obj)

    print("\nStep 4: Running topo_to_boundaries for units, provinces, and regions...")
    # Units
    cmd_units = [
        sys.executable, str(ROOT / "skill" / "scripts" / "topo_to_boundaries.py"),
        str(CACHE / "be_lau.json"),
        "--object", lau_obj,
        "--name-prop", "LAU_NAME",
        "--code-prop", "id",
        "--strip-prefix", "BE_",
        "--project", "lonlat",
        "--scale", "100",
        "--simplify", "0.4",
        "--source", "Eurostat GISCO LAU 2024 / © European Union, 1995-today",
        "--licence", "CC-BY-4.0",
        "--licence-url", "https://ec.europa.eu/eurostat/about-us/policies/copyright",
        "--code-scheme", "Statbel NIS/INS codes (REFNIS)",
        "--out", str(CACHE / "units.json")
    ]
    subprocess.run(cmd_units, check=True)

    # Provinces
    cmd_prov = [
        sys.executable, str(ROOT / "skill" / "scripts" / "topo_to_boundaries.py"),
        str(CACHE / "be_nuts2.json"),
        "--object", nuts2_obj,
        "--name-prop", "NAME_LATN",
        "--code-prop", "id",
        "--project", "lonlat",
        "--scale", "100",
        "--simplify", "0.4",
        "--licence", "CC-BY-4.0",
        "--licence-url", "https://ec.europa.eu/eurostat/about-us/policies/copyright",
        "--out", str(CACHE / "provinces.json")
    ]
    subprocess.run(cmd_prov, check=True)

    # Regions
    cmd_reg = [
        sys.executable, str(ROOT / "skill" / "scripts" / "topo_to_boundaries.py"),
        str(CACHE / "be_nuts1.json"),
        "--object", nuts1_obj,
        "--name-prop", "NAME_LATN",
        "--code-prop", "id",
        "--project", "lonlat",
        "--scale", "100",
        "--simplify", "0.4",
        "--licence", "CC-BY-4.0",
        "--licence-url", "https://ec.europa.eu/eurostat/about-us/policies/copyright",
        "--out", str(CACHE / "regions.json")
    ]
    subprocess.run(cmd_reg, check=True)

    print("\nStep 5: Merging boundaries into data/be/boundaries.json...")
    cmd_merge = [
        sys.executable, str(ROOT / "skill" / "scripts" / "merge_boundaries.py"),
        str(CACHE / "units.json"),
        "--regions", str(CACHE / "provinces.json"),
        "--upper", str(CACHE / "regions.json"),
        "--out", str(ROOT / "data" / "be" / "boundaries.json")
    ]
    subprocess.run(cmd_merge, check=True)

    print("\nStep 6: Updating meta.json...")
    meta_path = ROOT / "data" / "be" / "meta.json"
    meta = json.load(open(meta_path, encoding="utf-8"))
    meta["boundaries"] = "boundaries.json"
    meta["lead"] = "Egalitaristen"
    meta["notes"] = "Scope: national (federal parliament, parties, unions, economists, NGOs), 3 regions (Flanders, Wallonia, Brussels), 10 provinces, and 581 municipalities (REFNIS codes). Seed pass R001."
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print("Updated meta.json")

if __name__ == "__main__":
    main()
