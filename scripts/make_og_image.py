"""Draws the 1200x630 share image with the logo mark and wordmark.

Usage: python scripts/make_og_image.py <folder with InstrumentSerif-Regular.ttf, InstrumentSerif-Italic.ttf, Geist.ttf> site/og.png
Needs Pillow. The fonts are on Google Fonts (OFL).
"""
import re, sys
from PIL import Image, ImageDraw, ImageFont

FONTS = sys.argv[1]
OUT = sys.argv[2]
S = 3  # supersample, then downscale for smooth edges
W, H = 1200 * S, 630 * S
PAPER, INK, SIGNAL, MUTED = (243, 239, 230), (23, 21, 15), (217, 67, 30), (124, 118, 106)

BODY = "M4 58 L4 57 C30 57 42 56.5 47 53 C52 49.5 54 42 54 30 C54.27 27.3 54.61 24.6 55.03 21.94 L60 21.94 L60 58 Z"
TIP = "M55.03 17.94 C56.15 10.75 57.81 3.84 60 -2 L60 17.94 Z"
DEP = "M4 54.5 L43.92 54.5 C37.66 56.65 25.71 57 4 57 Z"
TRAIL = ((55, 1), (38, 1), (22, 18), (18, 50))


def bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(1, n + 1):
        t = i / n; m = 1 - t
        out.append((m**3 * p0[0] + 3 * m * m * t * p1[0] + 3 * m * t * t * p2[0] + t**3 * p3[0],
                    m**3 * p0[1] + 3 * m * m * t * p1[1] + 3 * m * t * t * p2[1] + t**3 * p3[1]))
    return out


def poly(d):
    toks = re.findall(r"[MLCZ]|-?\d+(?:\.\d+)?", d)
    pts, i, cur = [], 0, None
    while i < len(toks):
        c = toks[i]; i += 1
        if c in "ML":
            cur = (float(toks[i]), float(toks[i + 1])); i += 2; pts.append(cur)
        elif c == "C":
            a = [(float(toks[i + k]), float(toks[i + k + 1])) for k in (0, 2, 4)]; i += 6
            pts += bez(cur, *a); cur = a[2]
    return pts


img = Image.new("RGB", (W, H), PAPER)
dr = ImageDraw.Draw(img)
# The mark, 64-unit grid scaled up and placed on the left.
k, ox, oy = 7.2 * S, 90 * S, 105 * S
tr = lambda pts: [(ox + x * k, oy + (y + 4) * k) for x, y in pts]
dr.polygon(tr(poly(BODY)), fill=INK)
dr.polygon(tr(poly(TIP)), fill=SIGNAL)
dr.polygon(tr(poly(DEP)), fill=SIGNAL)
# Dotted trail: dots spaced evenly along the curve.
path = [TRAIL[0]] + bez(*TRAIL, n=400)
dots, acc, step, last = [], 0.0, 5.2, path[0]
dots.append(last)
for p in path[1:]:
    acc += ((p[0] - last[0]) ** 2 + (p[1] - last[1]) ** 2) ** .5; last = p
    if acc >= step:
        dots.append(p); acc = 0
r = 1.25 * k
for x, y in tr(dots):
    dr.ellipse((x - r, y - r, x + r, y + r), fill=SIGNAL)

serif = ImageFont.truetype(f"{FONTS}/InstrumentSerif-Regular.ttf", 112 * S)
italic = ImageFont.truetype(f"{FONTS}/InstrumentSerif-Italic.ttf", 112 * S)
sans = ImageFont.truetype(f"{FONTS}/Geist.ttf", 34 * S)
tx, ty = 600 * S, 190 * S
dr.text((tx, ty), "Wealth Tax", font=serif, fill=INK)
dr.text((tx, ty + 112 * S), "Supporters", font=italic, fill=SIGNAL)
dr.text((tx + 4 * S, ty + 262 * S), "Who backs a wealth tax near you?", font=sans, fill=MUTED)
dr.text((tx + 4 * S, ty + 312 * S), "wealthtaxsupporters.com", font=sans, fill=INK)
img.resize((1200, 630), Image.LANCZOS).save(OUT, optimize=True)
print("saved", OUT)
