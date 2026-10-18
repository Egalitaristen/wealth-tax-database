#!/usr/bin/env python3
"""Build the static site from data/<country>/ into _site/.

Usage: python scripts/build_site.py [--out _site]

Reads every folder in data/ that has a meta.json, writes one JSON file per country plus
world.json (country summary and projected world map paths), and copies the site files.
Needs only the standard library, plus pycountry for ISO codes (pip install pycountry).
"""
import argparse, csv, hashlib, json, math, shutil, sys, collections, datetime
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


# ---------- per-country data ----------
def build_country(folder):
    meta = json.load(open(folder / "meta.json", encoding="utf-8"))
    slug = folder.name
    actors, ev, geo = rd(folder / "actors.csv"), rd(folder / "evidence.csv"), rd(folder / "geo_units.csv")
    links, runs, excl = rd(folder / "links.csv"), rd(folder / "runs.csv"), rd(folder / "exclusions.csv")
    gname = {g["geo_unit_id"]: g["name"] for g in geo}
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
                  gname.get(a["geo_unit_id"], ""), "ABC"[best], len(es), dates[0] if dates else "",
                  dates[-1] if dates else "", designs, a["notes"], a["website"], a.get("party", "")])

    bounds = None
    bfile = meta.get("boundaries")
    if bfile and (folder / bfile).exists():
        bounds = json.load(open(folder / bfile, encoding="utf-8"))
    units = {g["name"]: g for g in geo}
    sup_by_geo = collections.defaultdict(list)
    for a in actors:
        if a["geo_unit_id"] in gname:
            sup_by_geo[gname[a["geo_unit_id"]]].append(a["actor_id"])
    C, vb, mapped = [], None, set()
    if bounds:
        vb = bounds["viewBox"]
        for u in bounds["units"]:
            g = units.get(u["name"])
            if not g:
                continue
            mapped.add(u["name"])
            state = "support" if sup_by_geo.get(u["name"]) else ("clear" if g["sweep_status"] == "done" else "open")
            C.append([u["name"], u.get("code", ""), state, g["sweep_status"], g["hits"], g["notes"][:600],
                      sup_by_geo.get(u["name"], []), u["path"]])
    O = [[g["name"], g["level"], g["sweep_status"], g["notes"][:500], sup_by_geo[g["name"]]]
         for g in geo if g["name"] not in mapped and sup_by_geo.get(g["name"])]
    L = [[l["from_actor_id"], l["to_actor_id"], l["link_type"], l["note"]] for l in links]
    verified = sum(1 for e in ev if e["verified"] == "y")
    last = max([r.get("date", "") for r in runs] or [""])
    done = sum(1 for g in geo if g["sweep_status"] == "done")
    grades = collections.Counter(p[8] for p in P)
    summary = dict(slug=slug, iso2=meta.get("iso2", slug.split("-")[0].upper()), name=meta["name"],
                   status=meta.get("status", ""), lead=meta.get("lead", ""), notes=meta.get("notes", ""),
                   supporters=len(P), evidence=len(E), verified=verified, A=grades["A"], B=grades["B"], C=grades["C"],
                   units=len(geo), units_done=done, updated=last, excluded=len(excl))
    country = dict(meta=summary, P=P, E=E, C=C, vb=vb, O=O, L=L)
    return summary, country


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "_site"))
    out = Path(ap.parse_args().out)
    if out.exists():
        shutil.rmtree(out)
    (out / "data").mkdir(parents=True)
    for f in ("app.js", "style.css"):
        shutil.copy(SITE / f, out / f)
    # Pages caches files for 10 minutes; a content hash in the URL makes updates show at once.
    html = (SITE / "index.html").read_text(encoding="utf-8")
    for f in ("app.js", "style.css"):
        h = hashlib.md5((SITE / f).read_bytes()).hexdigest()[:8]
        html = html.replace(f'"{f}"', f'"{f}?v={h}"')
    (out / "index.html").write_text(html, encoding="utf-8")
    countries = []
    for folder in sorted(DATA.iterdir()):
        if folder.is_dir() and (folder / "meta.json").exists():
            summary, country = build_country(folder)
            summary["numeric"] = numeric_for(summary["iso2"].split("-")[0])
            countries.append(summary)
            json.dump(country, open(out / "data" / f"{folder.name}.json", "w", encoding="utf-8"),
                      separators=(",", ":"), ensure_ascii=False)
            print(f"  {folder.name}: {summary['supporters']} supporters, {summary['evidence']} evidence rows")
    world = dict(paths=world_paths(), countries=countries, built=datetime.date.today().isoformat())
    json.dump(world, open(out / "data" / "world.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
    (out / ".nojekyll").write_text("")
    print(f"Built {len(countries)} countr{'y' if len(countries) == 1 else 'ies'} into {out}")


if __name__ == "__main__":
    sys.exit(main())
