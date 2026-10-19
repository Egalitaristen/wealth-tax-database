#!/usr/bin/env python3
"""Turn a TopoJSON file of areas (states, regions, councils) into a boundaries.json for a country folder.

The site draws data/<iso2>/boundaries.json as the local map. Standard library only.

Examples
  # US states, already projected to a flat 975 x 610 canvas (npm package us-atlas, file states-albers-10m.json)
  python skill/scripts/topo_to_boundaries.py states-albers-10m.json --object states --name-prop name \\
      --code-prop id --source "US Census cartographic boundaries via us-atlas" --out data/us/boundaries.json

  # Longitude/latitude shapes (for example world-atlas or an ONS/GADM export converted to TopoJSON)
  python skill/scripts/topo_to_boundaries.py regions.json --object regions --project lonlat --out data/xx/boundaries.json

Unit names must match the `name` column of geo_units.csv. A unit also matches when its geo_units name starts with
the boundary name followed by " (" (so "Alabama" matches "Alabama (state legislature and state government)").
"""
import argparse, json, math, sys
from pathlib import Path


def decode(topo):
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
    return arcs


def ring_points(arcs, idx):
    pts = []
    for i in idx:
        a = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(a if not pts else a[1:])
    return pts


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("topojson", help="path to a .json TopoJSON file")
    ap.add_argument("--object", required=True, help="name of the object inside the TopoJSON (for example states)")
    ap.add_argument("--name-prop", default="name", help="property holding the area name (default: name)")
    ap.add_argument("--code-prop", default="", help="property (or 'id') holding a code to store with each unit")
    ap.add_argument("--project", choices=["planar", "lonlat"], default="planar",
                    help="planar: coordinates are already flat; lonlat: degrees, drawn with a mid-latitude correction")
    ap.add_argument("--scale", type=float, default=10, help="multiply coordinates before rounding to integers")
    ap.add_argument("--source", default="", help="where the shapes come from, stored in the file")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    topo = json.load(open(a.topojson, encoding="utf-8"))
    arcs = decode(topo)
    geoms = topo["objects"][a.object]["geometries"]
    lats = [p[1] for arc in arcs for p in arc]
    k = math.cos(math.radians((min(lats) + max(lats)) / 2)) if a.project == "lonlat" else 1.0

    def xy(p):
        x = p[0] * k * a.scale
        y = (-p[1] if a.project == "lonlat" else p[1]) * a.scale
        return round(x), round(y)

    units, xs, ys = [], [], []
    for g in geoms:
        props = g.get("properties", {})
        name = props.get(a.name_prop)
        if not name:
            continue
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        d = ""
        for poly in polys:
            for r in poly:
                pts = [xy(p) for p in ring_points(arcs, r)]
                d += "M" + "L".join(f"{x} {y}" for x, y in pts) + "Z"
                xs += [p[0] for p in pts]; ys += [p[1] for p in pts]
        code = g.get("id") if a.code_prop == "id" else props.get(a.code_prop, "") if a.code_prop else ""
        units.append({"name": name, "code": str(code or ""), "path": d})
    out = {"viewBox": [min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)], "source": a.source,
           "match": "name", "units": units}
    Path(a.out).write_text(json.dumps(out, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {a.out}: {len(units)} units, {Path(a.out).stat().st_size // 1024} KB")


if __name__ == "__main__":
    sys.exit(main())
