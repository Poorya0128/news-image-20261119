"""Turns Natural Earth country shapes (public domain) into two small files.

  data/raw/ne_110m_countries.geojson -> data/world.json  (whole world, 0.1 deg)
  data/raw/ne_50m_countries.geojson  -> data/gulf.json   (Gulf region, 0.02 deg)

Source: https://github.com/nvkelso/natural-earth-vector (geojson/).
Run once: python prep_geo.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "data", "raw")


def rings(geom):
    if geom["type"] == "Polygon":
        polys = [geom["coordinates"]]
    else:
        polys = geom["coordinates"]
    for poly in polys:
        yield poly[0]                     # outer ring only


def simplify(ring, step):
    out = []
    for lon, lat in ring:
        q = [round(lon / step) * step, round(lat / step) * step]
        q = [round(q[0], 3), round(q[1], 3)]
        if not out or out[-1] != q:
            out.append(q)
    return out


def world():
    g = json.load(open(os.path.join(RAW, "ne_110m_countries.geojson")))
    shapes = []
    for f in g["features"]:
        if f["properties"]["NAME"] == "Antarctica":
            continue
        for r in rings(f["geometry"]):
            s = simplify(r, 0.1)
            if len(s) >= 3:
                shapes.append(s)
    return shapes


def gulf(box=(38.0, 18.0, 64.0, 36.0)):
    g = json.load(open(os.path.join(RAW, "ne_50m_countries.geojson")))
    out = []
    for f in g["features"]:
        name = f["properties"]["NAME"]
        for r in rings(f["geometry"]):
            if any(box[0] <= lo <= box[2] and box[1] <= la <= box[3] for lo, la in r):
                s = simplify(r, 0.02)
                if len(s) >= 3:
                    out.append({"name": name, "ring": s})
    return out


if __name__ == "__main__":
    w = world()
    json.dump(w, open(os.path.join(HERE, "data", "world.json"), "w"), separators=(",", ":"))
    gl = gulf()
    json.dump(gl, open(os.path.join(HERE, "data", "gulf.json"), "w"), separators=(",", ":"))
    print(len(w), "world rings;", len(gl), "gulf rings")
