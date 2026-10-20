#!/usr/bin/env python3
"""Build the static site from data/<country>/ into _site/.

Usage: python scripts/build_site.py [--out _site]

Reads every folder in data/ that has a meta.json, writes one JSON file per country plus
world.json (country summary and projected world map paths), and copies the site files.
Needs only the standard library, plus pycountry for ISO codes (pip install pycountry).
"""
import argparse, csv, hashlib, json, math, re, shutil, sys, collections, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SITE = ROOT / "site"
RANK = {"A": 0, "B": 1, "C": 2}

try:
    import pycountry
except ImportError:  # the build still works; countries then match on name only
    pycountry = None


def rd(path):
    p = Path(path)
    if not p.exists():
        return []
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


# ---------- world map: decode world-atlas TopoJSON and project with Equal Earth ----------
def equal_earth(lon, lat):
    A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
    lam, phi = math.radians(lon), math.radians(lat)
    th = math.asin(math.sqrt(3) / 2 * math.sin(phi))
    t2, t6 = th * th, th ** 6
    x = 2 * math.sqrt(3) * lam * math.cos(th) / (3 * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)))
    y = th * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))
    return x, y


def world_paths():
    topo = json.load(open(SITE / "vendor" / "countries-110m.json", encoding="utf-8"))
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx; y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def ring(idx):
        pts = []
        for i in idx:
            a = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts.extend(a if not pts else a[1:])
        return pts

    def clip(pts, keep, edge):
        """Sutherland-Hodgman against one vertical edge. keep(lon) says which side stays; edge is +-180."""
        out = []
        for i, p in enumerate(pts):
            q = pts[i - 1]
            pin, qin = keep(p[0]), keep(q[0])
            if pin != qin:
                t = (edge - q[0]) / (p[0] - q[0])
                out.append((edge, q[1] + t * (p[1] - q[1])))
            if pin:
                out.append(p)
        return out

    def split_antimeridian(pts):
        """Rings that cross +-180 are unwrapped, then cut into an eastern and a western piece."""
        un, off = [pts[0]], 0.0
        for a, b in zip(pts, pts[1:]):
            if b[0] - a[0] > 180: off -= 360
            elif b[0] - a[0] < -180: off += 360
            un.append((b[0] + off, b[1]))
        if max(p[0] for p in un) <= 180 and min(p[0] for p in un) >= -180:
            return [pts]
        east = clip(un, lambda lon: lon <= 180, 180.0)
        west = clip([(lon - 360, lat) for lon, lat in un], lambda lon: lon >= -180, -180.0)
        return [r for r in (east, west) if len(r) > 2]

    out = {}
    for g in topo["objects"]["countries"]["geometries"]:
        cid = str(g.get("id", ""))
        if not cid or cid == "010":  # skip Antarctica and unidentified shapes
            continue
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        d = ""
        for poly in polys:
            for r in poly:
                for part in split_antimeridian(ring(r)):
                    pts = [equal_earth(*p) for p in part]
                    d += "M" + "L".join(f"{x * 100:.1f} {-y * 100:.1f}" for x, y in pts) + "Z"
        out[cid] = {"name": g["properties"]["name"], "path": d}
    return out


def numeric_for(iso2):
    if pycountry:
        c = pycountry.countries.get(alpha_2=iso2.upper())
        if c:
            return str(int(c.numeric))
    return ""


# ---------- locations: "Country > Region > Place" paths resolved against geo_units.csv ----------
def _bare(n):
    return re.sub(r"\s*\(.*$", "", n or "").strip().lower()


def geo_index(geo):
    by_id = {g["geo_unit_id"]: g for g in geo}
    kids, roots = collections.defaultdict(dict), {}
    for g in geo:
        if g.get("parent_id") and g["parent_id"] in by_id:
            kids[g["parent_id"]].setdefault(_bare(g["name"]), g["geo_unit_id"])
        elif g.get("unit_type") == "country":
            roots[_bare(g["name"])] = g["geo_unit_id"]
    return by_id, kids, roots


def resolve_location(location, idx):
    by_id, kids, roots = idx
    parts = [p.strip() for p in (location or "").split(">") if p.strip()]
    uid = roots.get(_bare(parts[0])) if parts else None
    if not uid:
        return "", 0, parts
    depth = 1
    for seg in parts[1:]:
        nxt = kids.get(uid, {}).get(_bare(seg))
        if not nxt:
            break
        uid, depth = nxt, depth + 1
    return uid, depth, parts[depth:]


def unit_path(uid, by_id):
    names, seen = [], set()
    while uid and uid in by_id and uid not in seen:
        seen.add(uid); names.append(re.sub(r"\s*\(.*$", "", by_id[uid]["name"]).strip()); uid = by_id[uid]["parent_id"]
    return " > ".join(reversed(names))


# ---------- per-country data ----------
def build_country(folder):
    meta = json.load(open(folder / "meta.json", encoding="utf-8"))
    slug = folder.name
    actors, ev, geo = rd(folder / "actors.csv"), rd(folder / "evidence.csv"), rd(folder / "geo_units.csv")
    prof = collections.defaultdict(list)
    for p in rd(folder / "profiles.csv"):
        if p["url"].startswith("https://"):
            prof[p["actor_id"]].append([p["platform"], p["url"]])
    links, runs, excl = rd(folder / "links.csv"), rd(folder / "runs.csv"), rd(folder / "exclusions.csv")
    gidx = geo_index(geo)
    by_id = gidx[0]
    by = collections.defaultdict(list)
    for e in ev:
        by[e["actor_id"]].append(e)

    E = [[e["actor_id"], e["date"], e["grade"], e["evidence_type"], e["wt_design"], e["design_detail"],
          e["quote_original"][:420], e["source_url"], e["source_title"], e["publisher"], e["verified"],
          e["evidence_id"]] for e in ev]
    P = []
    for a in actors:
        es = by.get(a["actor_id"], [])
        if not es:
            continue
        best = min(RANK.get(x["grade"], 3) for x in es)
        dates = sorted(x["date"] for x in es if x["date"])
        designs = sorted({x["wt_design"] for x in es if x["wt_design"]})
        P.append([a["actor_id"], a["name"], a["kind"], a["actor_type"], a["role"], a["affiliation"], a["level"],
                  a.get("location", ""), "ABC"[best], len(es), dates[0] if dates else "",
                  dates[-1] if dates else "", designs, a["notes"], a["website"], a.get("party", ""),
                  [x.strip() for x in a.get("other_types", "").split(";") if x.strip()], prof.get(a["actor_id"], [])])

    bounds = None
    bfile = meta.get("boundaries")
    if bfile and (folder / bfile).exists():
        bounds = json.load(open(folder / bfile, encoding="utf-8"))
    units = {_bare(g["name"]): g for g in geo}
    here, inside = collections.defaultdict(list), collections.defaultdict(list)
    for a in actors:
        if a["actor_id"] not in by:
            continue
        uid = resolve_location(a.get("location", ""), gidx)[0]
        if uid:
            here[uid].append(a["actor_id"])
        seen = set()
        while uid and uid in by_id and uid not in seen:  # an actor counts for its unit and every unit above it
            seen.add(uid); inside[uid].append(a["actor_id"]); uid = by_id[uid]["parent_id"]
    roots = set(gidx[2].values())
    C, vb, mapped = [], None, set()
    if bounds:
        vb = bounds["viewBox"]
        for u in bounds["units"]:
            g = units.get(_bare(u["name"]))
            if not g:
                continue
            mapped.add(g["geo_unit_id"])
            ids = inside.get(g["geo_unit_id"], [])
            state = "support" if ids else ("clear" if g["sweep_status"] == "done" else "open")
            C.append([u["name"], u.get("code", ""), state, g["sweep_status"], g["hits"], g["notes"][:600], ids, u["path"],
                      unit_path(g["geo_unit_id"], by_id)])
    O = []
    for g in geo:
        uid = g["geo_unit_id"]
        if uid in mapped or not here.get(uid):
            continue
        name = g["name"] + (" (country level)" if uid in roots else "")
        O.append([name, g["level"], g["sweep_status"], g["notes"][:500], here[uid], unit_path(uid, by_id)])
    L = [[l["from_actor_id"], l["to_actor_id"], l["link_type"], l["note"]] for l in links]
    verified = sum(1 for e in ev if e["verified"] == "y")
    last = max([r.get("date", "") for r in runs] or [""])
    done = sum(1 for g in geo if g["sweep_status"] == "done")
    with_sup = sum(1 for u, ids in inside.items() if ids and u not in roots)
    grades = collections.Counter(p[8] for p in P)
    summary = dict(slug=slug, iso2=meta.get("iso2", slug.split("-")[0].upper()), name=meta["name"],
                   status=meta.get("status", ""), lead=meta.get("lead", ""), notes=meta.get("notes", ""),
                   supporters=len(P), evidence=len(E), verified=verified, A=grades["A"], B=grades["B"], C=grades["C"],
                   units=len(geo) - len(roots), units_done=done, units_with_supporters=with_sup, updated=last, excluded=len(excl),
                   polls=[p for p in meta.get("polls", []) if str(p.get("url", "")).startswith("https://")])
    country = dict(meta=summary, P=P, E=E, C=C, vb=vb, O=O, L=L)

    # Search index rows: [slug, id, name, type, role, place, grade, statements]
    index = [[slug, p[0], p[1], p[3], p[4][:80], [x.strip() for x in p[7].split(">")][-1] if p[7] else "", p[8], p[9]]
             for p in P]
    # Place rows: [slug, unit path, supporters inside]
    places = [[slug, unit_path(u, by_id), len(ids)] for u, ids in inside.items() if ids and u not in roots]
    summary["featured"] = featured(P, ev)
    summary["types"] = dict(collections.Counter(p[3] for p in P).most_common())
    summary["designs"] = dict(collections.Counter(d for p in P for d in p[12]).most_common())
    return summary, country, index, places


FEATURE_TYPES = ["economist", "wealthy_individual", "campaigner", "journalist", "politician", "union_official",
                 "academic", "business_leader", "cultural_figure", "legal_tax_professional", "faith"]


def featured(P, ev):
    """A few short, explicit quotes from named people for the home page, spread across types."""
    people = {p[0]: p for p in P if p[2] == "person"}
    spoken = {"speech", "op_ed", "statement", "interview", "social_post", "testimony", "publication", "editorial", "campaign"}
    best = {}
    for e in ev:
        p = people.get(e["actor_id"])
        q = re.sub(r"\s+", " ", e["quote_original"]).strip()
        if not p or e["grade"] != "A" or not (70 <= len(q) <= 230) or not e["source_url"].startswith("http"):
            continue
        # Whole sentences in the person's own voice: starts with a capital, ends with punctuation,
        # and does not describe them in the third person.
        surname = p[1].split()[-1].lower()
        if (e["evidence_type"] not in spoken or not q[0].isupper() or q[-1] not in '.!?"”'
                or surname in q.lower() or re.match(r"(He|She|They|His|Her|Their)\s", q)):
            continue
        score = (len(p[17]) > 0, p[3] != "politician" or p[6] == "national", e["date"])
        if e["actor_id"] not in best or score > best[e["actor_id"]][0]:
            best[e["actor_id"]] = (score, [p[0], p[1], p[3], p[4][:90], q, e["source_url"], e["publisher"], e["date"]])
    by_type = collections.defaultdict(list)
    for score, row in sorted(best.values(), key=lambda x: x[0], reverse=True):
        by_type[row[2]].append(row)
    out = []
    while len(out) < 8 and any(by_type.values()):
        for t in FEATURE_TYPES + sorted(by_type):
            if by_type.get(t) and len(out) < 8:
                out.append(by_type[t].pop(0))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "_site"))
    out = Path(ap.parse_args().out)
    if out.exists():
        shutil.rmtree(out)
    (out / "data").mkdir(parents=True)
    # Every file in site/ except the page and the vendored map source is copied as is.
    assets = [f for f in SITE.iterdir() if f.is_file() and f.name != "index.html"]
    for f in assets:
        shutil.copy(f, out / f.name)
    # A content hash in each asset URL makes updates show at once despite caching.
    html = (SITE / "index.html").read_text(encoding="utf-8")
    for f in assets:
        if f.suffix in (".js", ".css", ".svg"):
            h = hashlib.md5(f.read_bytes()).hexdigest()[:8]
            html = html.replace(f'"/{f.name}"', f'"/{f.name}?v={h}"')
    (out / "index.html").write_text(html, encoding="utf-8")
    countries, index, places = [], [], []
    for folder in sorted(DATA.iterdir()):
        if folder.is_dir() and (folder / "meta.json").exists():
            summary, country, idx, pl = build_country(folder)
            summary["numeric"] = numeric_for(summary["iso2"].split("-")[0])
            countries.append(summary)
            index += idx
            places += pl
            json.dump(country, open(out / "data" / f"{folder.name}.json", "w", encoding="utf-8"),
                      separators=(",", ":"), ensure_ascii=False)
            dl = out / "download" / folder.name
            dl.mkdir(parents=True)
            for name in ("actors.csv", "evidence.csv", "profiles.csv", "geo_units.csv"):
                if (folder / name).exists():
                    shutil.copy(folder / name, dl / name)
            print(f"  {folder.name}: {summary['supporters']} supporters, {summary['evidence']} evidence rows")
    world = dict(paths=world_paths(), countries=countries, built=datetime.date.today().isoformat())
    json.dump(world, open(out / "data" / "world.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
    json.dump(dict(people=index, places=places), open(out / "data" / "index.json", "w", encoding="utf-8"),
              separators=(",", ":"), ensure_ascii=False)
    print(f"Built {len(countries)} countr{'y' if len(countries) == 1 else 'ies'} into {out}")


if __name__ == "__main__":
    sys.exit(main())
