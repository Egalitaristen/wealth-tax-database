import csv
import io
import json
import math
import os
import re
import tarfile
import urllib.request

tar_url = "https://registry.npmjs.org/jpn-atlas/-/jpn-atlas-1.0.2.tgz"
req = urllib.request.Request(tar_url, headers={"User-Agent": "Mozilla/5.0"})
tar = tarfile.open(fileobj=io.BytesIO(urllib.request.urlopen(req).read()), mode="r:gz")

# DBF
dbf_bytes = tar.extractfile("package/build/polbnda_jpn.dbf").read()
header_len = int.from_bytes(dbf_bytes[8:10], "little")
record_len = int.from_bytes(dbf_bytes[10:12], "little")
num_records = int.from_bytes(dbf_bytes[4:8], "little")

muni_db = {}
pos = header_len
for r in range(num_records):
    rec = dbf_bytes[pos:pos+record_len]
    pos += record_len
    adm = rec[80:90].decode("ascii", errors="replace").strip()
    nam = rec[9:34].decode("utf-8", errors="replace").strip()
    laa = rec[34:67].decode("utf-8", errors="replace").strip()
    if not adm or adm.startswith("UN"):
        continue
    if adm not in muni_db and laa:
        muni_db[adm] = (laa, nam, adm[:2])

PREFS = [
    ("01", "Hokkaido", "JP-01"),
    ("02", "Aomori", "JP-02"),
    ("03", "Iwate", "JP-03"),
    ("04", "Miyagi", "JP-04"),
    ("05", "Akita", "JP-05"),
    ("06", "Yamagata", "JP-06"),
    ("07", "Fukushima", "JP-07"),
    ("08", "Ibaraki", "JP-08"),
    ("09", "Tochigi", "JP-09"),
    ("10", "Gunma", "JP-10"),
    ("11", "Saitama", "JP-11"),
    ("12", "Chiba", "JP-12"),
    ("13", "Tokyo", "JP-13"),
    ("14", "Kanagawa", "JP-14"),
    ("15", "Niigata", "JP-15"),
    ("16", "Toyama", "JP-16"),
    ("17", "Ishikawa", "JP-17"),
    ("18", "Fukui", "JP-18"),
    ("19", "Yamanashi", "JP-19"),
    ("20", "Nagano", "JP-20"),
    ("21", "Gifu", "JP-21"),
    ("22", "Shizuoka", "JP-22"),
    ("23", "Aichi", "JP-23"),
    ("24", "Mie", "JP-24"),
    ("25", "Shiga", "JP-25"),
    ("26", "Kyoto", "JP-26"),
    ("27", "Osaka", "JP-27"),
    ("28", "Hyogo", "JP-28"),
    ("29", "Nara", "JP-29"),
    ("30", "Wakayama", "JP-30"),
    ("31", "Tottori", "JP-31"),
    ("32", "Shimane", "JP-32"),
    ("33", "Okayama", "JP-33"),
    ("34", "Hiroshima", "JP-34"),
    ("35", "Yamaguchi", "JP-35"),
    ("36", "Tokushima", "JP-36"),
    ("37", "Kagawa", "JP-37"),
    ("38", "Ehime", "JP-38"),
    ("39", "Kochi", "JP-39"),
    ("40", "Fukuoka", "JP-40"),
    ("41", "Saga", "JP-41"),
    ("42", "Nagasaki", "JP-42"),
    ("43", "Kumamoto", "JP-43"),
    ("44", "Oita", "JP-44"),
    ("45", "Miyazaki", "JP-45"),
    ("46", "Kagoshima", "JP-46"),
    ("47", "Okinawa", "JP-47"),
]

def get_clean_name(laa):
    return re.sub(r"\s+(Shi|Ku|Machi|Cho|Mura|Son)$", "", laa).strip()

by_pref = {}
for adm, (laa, nam, pcode) in muni_db.items():
    cname = get_clean_name(laa)
    by_pref.setdefault(pcode, []).append((cname, adm, laa))

collisions_by_pref = set()
for pcode, items in by_pref.items():
    counts = {}
    for cname, adm, laa in items:
        counts[cname] = counts.get(cname, 0) + 1
    for cname, cnt in counts.items():
        if cnt > 1:
            collisions_by_pref.add((pcode, cname))

muni_names = {}
for adm, (laa, nam, pcode) in muni_db.items():
    cname = get_clean_name(laa)
    if (pcode, cname) in collisions_by_pref:
        suffix_match = re.search(r"\s+(Shi|Ku|Machi|Cho|Mura|Son)$", laa)
        sfx = suffix_match.group(1).lower() if suffix_match else ""
        sfx_map = {"shi": "city", "ku": "ward", "machi": "town", "cho": "town", "mura": "village", "son": "village"}
        muni_names[adm] = f"{cname} ({sfx_map.get(sfx, sfx)})"
    else:
        muni_names[adm] = cname

# Read TopoJSON
topo = json.load(tar.extractfile("package/japan/japan.json"))

tr = topo.get("transform")
arcs = []
for arc in topo["arcs"]:
    pts, x, y = [], 0, 0
    for p in arc:
        if tr:
            x += p[0]; y += p[1]
            pts.append((x * tr["scale"][0] + tr["translate"][0], y * tr["scale"][1] + tr["translate"][1]))
        else:
            pts.append((p[0], p[1]))
    arcs.append(pts)

def ring_points(idx):
    pts = []
    for i in idx:
        a = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(a if not pts else a[1:])
    return pts

def simplify(pts, tol=0.8):
    if tol <= 0 or len(pts) < 5:
        return pts
    def dp(a, b):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1e-9
        best, at = 0.0, None
        for i in range(a + 1, b):
            d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / n
            if d > best:
                best, at = d, i
        if best > tol and at is not None:
            return dp(a, at)[:-1] + dp(at, b)
        return [pts[a], pts[b]]
    mid = len(pts) // 2
    out = dp(0, mid)[:-1] + dp(mid, len(pts) - 1)
    return out if len(out) >= 4 else pts

scale = 4
def xy(p):
    return round(p[0] * scale), round(p[1] * scale)

# Extract municipality rings grouped by code
muni_rings_by_code = {}
for g in topo["objects"]["municipalities"]["geometries"]:
    code = g.get("id")
    polys = g.get("arcs") or []
    polys = polys if g["type"] == "MultiPolygon" else [polys]
    rings = [ring_points(r) for poly in polys for r in poly]
    muni_rings_by_code.setdefault(code, []).extend(rings)

# Extract prefecture rings grouped by code
pref_rings_by_code = {}
for g in topo["objects"]["prefectures"]["geometries"]:
    code = g.get("id")
    polys = g.get("arcs") or []
    polys = polys if g["type"] == "MultiPolygon" else [polys]
    rings = [ring_points(r) for poly in polys for r in poly]
    pref_rings_by_code.setdefault(code, []).extend(rings)

# Build units for boundaries.json
units = []
xs, ys = [], []
for code in sorted(muni_rings_by_code.keys()):
    rings = muni_rings_by_code[code]
    d = ""
    for r in rings:
        pts = []
        for p in simplify([xy(p) for p in r], 0.8):
            if not pts or p != pts[-1]:
                pts.append(p)
        if len(pts) < 3:
            continue
        d += f"M{pts[0][0]} {pts[0][1]}l" + " ".join(f"{x - px} {y - py}" for (px, py), (x, y) in zip(pts, pts[1:])) + "z"
        xs += [p[0] for p in pts]; ys += [p[1] for p in pts]
    if d:
        name = muni_names.get(code, f"Municipality {code}")
        units.append({"name": name, "code": code, "path": d})

pref_dict = {p[0]: (p[1], p[2]) for p in PREFS}
regions = []
for code in sorted(pref_rings_by_code.keys()):
    rings = pref_rings_by_code[code]
    d = ""
    for r in rings:
        pts = []
        for p in simplify([xy(p) for p in r], 0.8):
            if not pts or p != pts[-1]:
                pts.append(p)
        if len(pts) < 3:
            continue
        d += f"M{pts[0][0]} {pts[0][1]}l" + " ".join(f"{x - px} {y - py}" for (px, py), (x, y) in zip(pts, pts[1:])) + "z"
    if d:
        pname, pcode = pref_dict.get(code, (f"Prefecture {code}", f"JP-{code}"))
        regions.append({"name": pname, "code": pcode, "path": d})

boundaries = {
    "viewBox": [min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)],
    "source": "Geospatial Information Authority of Japan (GSI) Global Map Japan (2016) via jpn-atlas, BSD-3-Clause",
    "licence": "BSD-3-Clause",
    "licence_url": "https://raw.githubusercontent.com/biskwikman/jpn-atlas/master/LICENSE",
    "code_scheme": "JIS X 0402",
    "match": "code",
    "units": units,
    "regions": regions
}

os.makedirs("data/jp", exist_ok=True)
with open("data/jp/boundaries.json", "w", encoding="utf-8") as f:
    json.dump(boundaries, f, separators=(",", ":"), ensure_ascii=False)
b_size = os.path.getsize("data/jp/boundaries.json") // 1024
print(f"Wrote data/jp/boundaries.json: {len(units)} units, {len(regions)} regions, {b_size} KB")

# Now build geo_units.csv
geo_rows = [
    ["geo_unit_id", "name", "level", "unit_type", "parent_id", "website", "sweep_status", "swept_run", "swept_date", "queries_run", "hits", "notes", "code"],
    ["G0001", "Japan", "national", "country", "", "", "pending", "", "", "", "", "", ""],
    ["G0002", "National Diet (Kokkai)", "national", "legislature", "G0001", "https://www.sangiin.go.jp", "pending", "", "", "", "", "Bicameral parliament of Japan (Shugiin and Sangiin)", ""],
    ["G0003", "House of Representatives (Shugiin)", "national", "legislature", "G0001", "https://www.shugiin.go.jp", "pending", "", "", "", "", "Lower house of the National Diet", ""],
    ["G0004", "House of Councillors (Sangiin)", "national", "legislature", "G0001", "https://www.sangiin.go.jp", "pending", "", "", "", "", "Upper house of the National Diet", ""],
    ["G0005", "Cabinet of Japan (Naikaku)", "national", "executive", "G0001", "https://www.kantei.go.jp", "pending", "", "", "", "", "Executive branch of the Government of Japan", ""]
]

gid = 6
pref_gid_map = {}
for pnum, pname, pcode in PREFS:
    p_gid = f"G{gid:04d}"
    pref_gid_map[pnum] = p_gid
    geo_rows.append([p_gid, pname, "region", "prefecture", "G0001", "", "pending", "", "", "", "", "", pcode])
    gid += 1

# Units
for u in units:
    code = u["code"]
    name = u["name"]
    pnum = code[:2]
    parent_gid = pref_gid_map.get(pnum, "G0001")
    u_gid = f"G{gid:04d}"
    geo_rows.append([u_gid, name, "council", "municipality", parent_gid, "", "pending", "", "", "", "", "", code])
    gid += 1

with open("data/jp/geo_units.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(geo_rows)

print(f"Wrote data/jp/geo_units.csv: {len(geo_rows) - 1} units.")
