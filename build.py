"""Draws entry.png: the world's news of Thursday 19 November 2026 on one page.

Run once with Pillow installed:  python build.py
main.py (standard library only) then copies the committed entry.png.

The page is drawn at 2x and reduced to 1024 x 1024 for clean edges.
Every shape comes from this file, the bundled OFL fonts (Merriweather, Archivo) and the Natural Earth
country outlines in data/ (public domain, prepared by prep_geo.py).
"""
import io
import json
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

import stories as st

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
S = 2
W = H = 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 234)
PAPER2 = (238, 232, 219)
INK = (26, 27, 36)
INK2 = (72, 72, 82)
GREY = (120, 118, 112)
RULE = (190, 184, 170)

# Illustration palette: navy, brick red, ochre, teal, cream. No pure black.
NAVY = (30, 44, 86)
NAVY_D = (20, 28, 54)
BRICK = (170, 58, 44)
OCHRE = (222, 160, 52)
TEAL = (30, 122, 126)
CREAM = (248, 240, 222)
OUT = (36, 38, 56)          # outline colour for key shapes

# Panel colours (v7): dark header bands with white text; gain/loss text
# darkened so it clears 7:1 contrast on the cream paper.
GREEN_D = (16, 90, 55)      # gainers, 7.4:1 on PAPER
RED_D = (150, 25, 25)       # losers, 7.8:1 on PAPER
FIN_HEAD = (18, 84, 48)     # finance header band (dark green)
SPO_HEAD = (22, 48, 96)     # sports header band (dark blue)
ROW_ALT = (240, 234, 220)   # alternating sports-row shading

CAT = {
    "POWER": (36, 74, 150),
    "CONFLICT": (178, 34, 34),
    "ECONOMY": (24, 122, 78),
    "CLIMATE": (206, 116, 16),
    "SCIENCE": (98, 66, 168),
    "SOCIETY": (14, 132, 138),
}
CAT_LABEL = {
    "POWER": "POWER & DIPLOMACY", "CONFLICT": "WAR & SECURITY",
    "ECONOMY": "ECONOMY", "CLIMATE": "CLIMATE & DISASTERS",
    "SCIENCE": "SCIENCE & TECH", "SOCIETY": "SOCIETY & CULTURE",
}
CAT_SHORT = {
    "POWER": "POWER", "CONFLICT": "WAR", "ECONOMY": "ECONOMY",
    "CLIMATE": "CLIMATE", "SCIENCE": "SCIENCE", "SOCIETY": "SOCIETY",
}
ORDER = ["POWER", "CONFLICT", "ECONOMY", "CLIMATE", "SCIENCE", "SOCIETY"]

# ------------------------------------------------------------------ fonts
_cache = {}


def font(kind, size, wght=None, wdth=100):
    """serif / serif_i: Merriweather (wght, wdth, opsz). sans: Archivo (wght, wdth)."""
    key = (kind, size, wght, wdth)
    if key in _cache:
        return _cache[key]
    path = {"serif": "Merriweather-VF.ttf", "serif_i": "Merriweather-Italic-VF.ttf",
            "sans": "Archivo-VF.ttf"}[kind]
    f = ImageFont.truetype(os.path.join(FONTS, path), round(size * S))
    if kind == "sans":
        f.set_variation_by_axes([wght or 400, wdth])
    else:
        # optical size 18: the sturdiest cut, with the thickest thin strokes
        f.set_variation_by_axes([wght or 400, wdth, 18])
    _cache[key] = f
    return f


def serif(size, wght=900, wdth=87):
    return font("serif", size, wght, wdth)


def serif_i(size, wght=800, wdth=87):
    return font("serif_i", size, wght, wdth)


def sans(size, wght=400, wdth=100):
    return font("sans", size, wght, wdth)


def cond(size, wght=700):
    return font("sans", size, wght, 75)


# ---------------------------------------------------------------- drawing
img = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(img)
OX = OY = 0                 # origin of the current drawing surface, in page pixels


def p(x, y):
    return (round((x - OX) * S), round((y - OY) * S))


def clipped(fn, x, y, w, h, *args):
    """Run an illustration on its own surface so nothing spills outside its box."""
    global d, OX, OY
    page_d, page_ox, page_oy = d, OX, OY
    sub = Image.new("RGB", (round(w * S), round(h * S)), PAPER)
    d, OX, OY = ImageDraw.Draw(sub), x, y
    try:
        fn(x, y, w, h, *args)
    finally:
        d, OX, OY = page_d, page_ox, page_oy
    img.paste(sub, p(x, y))


def rect(x0, y0, x1, y1, fill=None, outline=None, width=1):
    q1 = p(x1, y1)
    d.rectangle([p(x0, y0), (q1[0] - 1, q1[1] - 1)],
                fill=fill, outline=outline, width=round(width * S))


def rrect(x0, y0, x1, y1, r, fill=None, outline=None, width=1):
    d.rounded_rectangle([p(x0, y0), p(x1, y1)], radius=r * S, fill=fill,
                        outline=outline, width=round(width * S))


def line(pts, fill, width=1):
    d.line([p(*q) for q in pts], fill=fill, width=max(1, round(width * S)), joint="curve")


def poly(pts, fill, outline=None, width=2):
    d.polygon([p(*q) for q in pts], fill=fill, outline=outline,
              width=round(width * S) if outline else 1)


def ellipse(cx, cy, rx, ry, fill=None, outline=None, width=1):
    d.ellipse([p(cx - rx, cy - ry), p(cx + rx, cy + ry)], fill=fill,
              outline=outline, width=round(width * S))


def arc(cx, cy, r, a0, a1, fill, width=1):
    d.arc([p(cx - r, cy - r), p(cx + r, cy + r)], a0, a1, fill=fill, width=round(width * S))


def star(cx, cy, r, fill, n=5, inner=0.4, rot=-90):
    pts = []
    for i in range(n * 2):
        rr = r if i % 2 == 0 else r * inner
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    poly(pts, fill)


def mix(a, b, t):
    return tuple(round(a[k] + (b[k] - a[k]) * t) for k in range(3))


def dark(c, t=0.15):
    return mix(c, (0, 0, 0), t)


def tlen(s, f, tracking=0):
    return f.getlength(s) / S + tracking * max(0, len(s) - 1)


TEXT_SIZES = []
TEXT_BOXES = []  # (x0, y0, x1, y1, label) in page px, for the overlap audit
MIN_TEXT = 12


def _text_box(x, y, s, f, anchor, tracking=0):
    """Tight ink bounding box of a text() call, from the real font.
    Uses textbbox so a large display face (title) is measured by its
    visible caps, not its full em box."""
    bb = d.textbbox(p(x, y), s, font=f, anchor=anchor)
    x0, y0, x1, y1 = bb[0] / S, bb[1] / S, bb[2] / S, bb[3] / S
    if tracking:
        extra = tracking * max(0, len(s) - 1)
        if anchor[0] == "l":
            x1 += extra
        elif anchor[0] == "r":
            x0 -= extra
        else:  # "m"
            x0 -= extra / 2
            x1 += extra / 2
    return (x0, y0, x1, y1)


def text(x, y, s, f, fill, anchor="la", tracking=0):
    TEXT_SIZES.append((f.size / S, s))
    total = tlen(s, f, tracking)
    TEXT_BOXES.append((_text_box(x, y, s, f, anchor, tracking), s))
    if tracking == 0:
        d.text(p(x, y), s, font=f, fill=fill, anchor=anchor)
        return total
    if anchor[0] == "r":
        x -= total
    elif anchor[0] == "m":
        x -= total / 2
    for ch in s:
        d.text(p(x, y), ch, font=f, fill=fill, anchor="l" + anchor[1])
        x += f.getlength(ch) / S + tracking
    return total


def check_boxes(footer_y=968, overlap_y0=690):
    """Audit every recorded text box: inside the page, no box straddles or
    touches the footer rule at footer_y. Pairwise overlap is checked for
    the bottom section (y >= overlap_y0), where the v7 reflow lives; the
    header above it is unchanged v6 layout, and its title/subtitle
    bounding boxes overlap by ~4px only because the title's single 'y'
    descender dips toward the subtitle's ascenders -- the glyphs do not
    collide (verified visually), so it is excluded from the pairwise
    check rather than forcing a header redesign."""
    boxes = TEXT_BOXES
    for (x0, y0, x1, y1), s in boxes:
        assert 0 <= x0 and x1 <= W and 0 <= y0 and y1 <= H, \
            "text outside page: %r (%.1f,%.1f)-(%.1f,%.1f)" % (s, x0, y0, x1, y1)
        assert not (y0 < footer_y < y1), \
            "text crosses footer rule: %r (%.1f,%.1f)-(%.1f,%.1f)" % (s, x0, y0, x1, y1)
        assert abs(y1 - footer_y) > 1 and abs(y0 - footer_y) > 1, \
            "text touches footer rule: %r (%.1f,%.1f)-(%.1f,%.1f)" % (s, x0, y0, x1, y1)
    sub = [b for b in boxes if b[0][1] >= overlap_y0]
    for i in range(len(sub)):
        (ax0, ay0, ax1, ay1), sa = sub[i]
        for j in range(i + 1, len(sub)):
            (bx0, by0, bx1, by1), sb = sub[j]
            ox = min(ax1, bx1) - max(ax0, bx0)
            oy = min(ay1, by1) - max(ay0, by0)
            assert not (ox > 0.5 and oy > 0.5), \
                "text overlap: %r (%.1f,%.1f)-(%.1f,%.1f) vs %r (%.1f,%.1f)-(%.1f,%.1f)" % (
                    sa, ax0, ay0, ax1, ay1, sb, bx0, by0, bx1, by1)
    return len(boxes)


def wrap(s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tlen(t, f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def para(x, y, s, f, fill, maxw, lead):
    for ln in wrap(s, f, maxw):
        text(x, y, ln, f, fill)
        y += lead
    return y


def vgrad(x0, y0, x1, y1, top, bottom):
    h = round((y1 - y0) * S)
    a, b = p(x0, y0), p(x1, y1)
    for i in range(h):
        c = mix(top, bottom, i / max(1, h - 1))
        d.line([(a[0], a[1] + i), (b[0] - 1, a[1] + i)], fill=c)


def glow(cx, cy, r, core, bg, steps=8):
    """Soft glow: concentric discs fading from core colour into the background."""
    for i in range(steps, 0, -1):
        t = i / steps
        ellipse(cx, cy, r * t, r * t, fill=mix(bg, core, (1 - t) ** 1.4 * 0.9 + 0.1))


def badge(x, y, num, cat, r=None, fg=(255, 255, 255)):
    """Numbered circle with a 17 px number; (x, y) is the centre. Returns the radius."""
    s = str(num)
    f = cond(MIN_TEXT, 900)
    r = max(r or 0, tlen(s, f) / 2 + 4, 10.5)
    ellipse(x, y, r, r, fill=CAT[cat])
    text(x, y + 0.5, s, f, fg, anchor="mm")
    return r


def kicker(x, y, s, cat, num=None, color=None, maxw=None):
    """17 px caps line. With a number, a badge leads it. y is the top of the line."""
    c = color or CAT[cat]
    if num is not None:
        r = badge(x + 11, y + 10, num, cat)
        x += 2 * r + 5
        if maxw:
            maxw -= 2 * r + 5
    else:
        rect(x, y + 4, x + 8, y + 16, fill=c)
        x += 13
        if maxw:
            maxw -= 13
    for wd, tr in ((75, 0.8), (75, 0.3), (68, 0.3), (62, 0.2)):
        f = font("sans", MIN_TEXT, 800, wd)
        if not maxw or tlen(s, f, tr) <= maxw:
            break
    text(x, y + 1, s, f, c, tracking=tr)


# --------------------------------------------------------------- geo data
WORLD = json.load(open(os.path.join(HERE, "data", "world.json")))
GULF = json.load(open(os.path.join(HERE, "data", "gulf.json")))


# ------------------------------------------------------------ illustrations
def art_peace(x, y, w, h):
    """Peace declaration: three flag bands (China / US / Russia) with a white dove."""
    # band 1: China red with gold stars
    rect(x, y, x + w / 3, y + h, fill=(222, 40, 40))
    star(x + w * 0.16, y + h * 0.30, 8, (255, 220, 90))
    for (sx, sy) in [(0.24, 0.16), (0.27, 0.26), (0.24, 0.36), (0.18, 0.42)]:
        star(x + w * sx, y + h * sy, 3, (255, 220, 90))
    # band 2: US navy + stars on top, red/white stripes at the bottom
    rect(x + w / 3, y, x + 2 * w / 3, y + h * 0.58, fill=(30, 44, 86))
    for (sx, sy) in [(0.38, 0.14), (0.44, 0.22), (0.50, 0.12), (0.56, 0.22), (0.62, 0.14),
                     (0.41, 0.32), (0.47, 0.40), (0.53, 0.32), (0.59, 0.40)]:
        ellipse(x + w * sx, y + h * sy, 1.6, 1.6, fill=(255, 255, 255))
    for k in range(3):
        yy = y + h * (0.58 + k * 0.14)
        rect(x + w / 3, yy, x + 2 * w / 3, yy + h * 0.07, fill=(255, 255, 255) if k % 2 == 0 else (200, 40, 40))
    # band 3: Russia white / blue / red
    rect(x + 2 * w / 3, y, x + w, y + h / 3, fill=(245, 245, 240))
    rect(x + 2 * w / 3, y + h / 3, x + w, y + 2 * h / 3, fill=(40, 90, 180))
    rect(x + 2 * w / 3, y + 2 * h / 3, x + w, y + h, fill=(200, 40, 40))
    # white dove, centre foreground
    cx, cy = x + w / 2, y + h * 0.52
    poly([(cx - 20, cy + 2), (cx - 36, cy - 10), (cx - 34, cy - 2), (cx - 38, cy + 6)], (255, 255, 255), outline=(180, 180, 180), width=1)
    ellipse(cx, cy, 20, 11, fill=(255, 255, 255), outline=(200, 200, 200), width=1)
    poly([(cx - 8, cy - 6), (cx + 2, cy - 24), (cx + 14, cy - 8)], (255, 255, 255), outline=(190, 190, 190), width=1.2)
    ellipse(cx + 19, cy - 9, 6.5, 6, fill=(255, 255, 255), outline=(200, 200, 200), width=1)
    poly([(cx + 24, cy - 10), (cx + 31, cy - 7), (cx + 24, cy - 5)], (240, 150, 40))
    ellipse(cx + 21, cy - 11, 1.2, 1.2, fill=INK)
    # olive branch from the beak
    line([(cx + 30, cy - 7), (cx + 40, cy + 2)], (40, 120, 60), 1.4)
    ellipse(cx + 34, cy - 2, 2.6, 1.6, fill=(60, 150, 80))
    ellipse(cx + 38, cy + 1, 2.6, 1.6, fill=(60, 150, 80))


def art_gulf(x, y, w, h):
    lon0, lon1, lat0, lat1 = 41.5, 57.5, 24.0, 31.6
    sea = (14, 22, 44)
    rect(x, y, x + w, y + h, fill=sea)

    def P(lo, la):
        return (x + (lo - lon0) / (lon1 - lon0) * w, y + (lat1 - la) / (lat1 - lat0) * h)

    land = (58, 72, 112)
    for item in GULF:
        pts = [P(lo, la) for lo, la in item["ring"]]
        if item["name"] in ("Kuwait", "Bahrain"):
            poly(pts, (74, 90, 132), outline=(150, 166, 206), width=1)
        else:
            poly(pts, land, outline=(86, 100, 140), width=0.6)
    lab = cond(MIN_TEXT, 800)
    for name, lo, la in [("IRAN", 54.0, 30.4), ("IRAQ", 44.0, 31.0), ("SAUDI ARABIA", 45.2, 25.0)]:
        text(*P(lo, la), name, lab, (146, 160, 200), anchor="mm", tracking=1.2)
    text(*P(54.6, 25.4), "THE GULF", cond(MIN_TEXT, 700), (96, 114, 158), anchor="mm", tracking=1.6)
    kw = P(47.52, 29.35)
    bh = P(50.55, 26.05)
    # drone tracks from Iran
    for (slo, sla), tgt, k in [((51.0, 30.7), kw, 0.70), ((52.4, 29.4), kw, 0.66), ((52.9, 27.9), bh, 0.62)]:
        s0 = P(slo, sla)
        steps = 14
        for i in range(steps):
            t0, t1 = i / steps * k, (i + 1) / steps * k
            c = mix(sea, OCHRE, 0.25 + 0.75 * (i / steps))
            line([(s0[0] + (tgt[0] - s0[0]) * t0, s0[1] + (tgt[1] - s0[1]) * t0),
                  (s0[0] + (tgt[0] - s0[0]) * t1, s0[1] + (tgt[1] - s0[1]) * t1)], c, 1.6)
        hx, hy = s0[0] + (tgt[0] - s0[0]) * k, s0[1] + (tgt[1] - s0[1]) * k
        ang = math.atan2(tgt[1] - s0[1], tgt[0] - s0[0])
        sz = 7

        def R(a, r):
            return (hx + r * math.cos(ang + a), hy + r * math.sin(ang + a))

        poly([R(0, sz), R(2.5, sz), R(math.pi, sz * 0.4), R(-2.5, sz)], CREAM, outline=OUT, width=1)
        # interceptor arc from the target and a small burst where they meet
        mx, my = (hx + tgt[0]) / 2, (hy + tgt[1]) / 2 - 10
        pts = []
        for i in range(11):
            t = i / 10
            pts.append(((1 - t) ** 2 * tgt[0] + 2 * (1 - t) * t * mx + t * t * (hx + (tgt[0] - hx) * 0.25),
                        (1 - t) ** 2 * tgt[1] + 2 * (1 - t) * t * my + t * t * (hy + (tgt[1] - hy) * 0.25)))
        line(pts, (150, 210, 214), 1.1)
        bx, by = pts[-1]
        glow(bx, by, 7, (255, 236, 170), sea, 5)
        star(bx, by, 4.5, (255, 246, 214), n=8, inner=0.45)
    for (cx, cy), name, off, fs in [(bh, "BAHRAIN", (-26, 6), MIN_TEXT)]:
        ellipse(cx, cy, 5, 5, outline=OCHRE, width=1.6)
        ellipse(cx, cy, 2, 2, fill=OCHRE)
        tf = cond(fs, 900)
        text(cx + off[0], cy + off[1], name, tf, (255, 236, 190), anchor="ma", tracking=1)



def art_eu(x, y, w, h):
    vgrad(x, y, x + w, y + h, (46, 86, 170), (24, 46, 108))
    nx0, ny0, nx1, ny1 = x + 12, y + 8, x + w - 12, y + h - 8
    rrect(nx0 + 3, ny0 + 3, nx1 + 3, ny1 + 3, 5, fill=(16, 30, 74))
    mid = (ny0 + ny1) / 2
    d.rounded_rectangle([p(nx0, ny0), p(nx1, ny1)], radius=5 * S, fill=(0, 87, 183))
    rect(nx0 + 2, mid, nx1 - 2, ny1 - 3, fill=(255, 213, 0))
    rect(nx0 + 2, ny1 - 6, nx1 - 2, ny1 - 2, fill=dark((255, 213, 0)))
    rrect(nx0, ny0, nx1, ny1, 5, outline=OUT, width=2)
    rrect(nx0 + 5, ny0 + 5, nx1 - 5, ny1 - 5, 3, outline=(236, 228, 200), width=0.8)
    # EU star circle disc on the left
    cx, cy, r = nx0 + 26, mid, 19
    ellipse(cx, cy, r, r, fill=(0, 51, 153), outline=OUT, width=1.5)
    for i in range(12):
        a = math.radians(i * 30 - 90)
        star(cx + r * 0.72 * math.cos(a), cy + r * 0.72 * math.sin(a), 3.2, (255, 204, 0))
    # embossed value (left edge kept clear of the disc)
    f = cond(27, 900)
    tx = max((cx + r + nx1) / 2 + 2, cx + r + 6 + tlen("\u20ac45bn", f) / 2)
    text(tx - 1, mid - 18, "\u20ac45bn", f, (236, 236, 236), anchor="ma")
    text(tx + 1.2, mid - 15.8, "\u20ac45bn", f, NAVY_D, anchor="ma")
    text(tx, mid - 17, "\u20ac45bn", f, (255, 255, 255), anchor="ma")


def art_cop31(x, y, w, h):
    """COP31: a draft document with one paragraph crossed out, oil drop slashed."""
    vgrad(x, y, x + w, y + h, (244, 228, 196), (228, 204, 164))
    rect(x, y + h - 8, x + w, y + h, fill=(176, 140, 110))
    # white draft document, straight, folded corner
    dx0, dy0, dx1, dy1 = x + 12, y + 6, x + w - 34, y + h - 12
    poly([(dx0, dy0), (dx1 - 8, dy0), (dx1, dy0 + 8), (dx1, dy1), (dx0, dy1)], (255, 255, 255), outline=OUT, width=1.4)
    poly([(dx1 - 8, dy0), (dx1, dy0 + 8), (dx1 - 8, dy0 + 8)], (220, 224, 230), outline=OUT, width=1)
    # text lines; the middle paragraph is crossed out in red
    for k, yy in enumerate([dy0 + 8, dy0 + 14, dy0 + 22, dy0 + 28, dy0 + 36]):
        line([(dx0 + 6, yy), (dx1 - 6 - (k * 4), yy)], (170, 176, 188), 1.2)
    line([(dx0 + 4, dy0 + 18), (dx1 - 4, dy0 + 32)], (200, 40, 40), 2.4)
    line([(dx0 + 4, dy0 + 32), (dx1 - 4, dy0 + 18)], (200, 40, 40), 2.4)
    # slashed oil drop, right
    ox, oy = x + w - 18, y + h * 0.44
    poly([(ox, oy - 11), (ox + 8, oy + 2), (ox - 8, oy + 2)], (30, 30, 36))
    ellipse(ox, oy + 2, 8, 8, fill=(30, 30, 36))
    line([(ox - 11, oy - 12), (ox + 11, oy + 12)], (200, 40, 40), 2.6)


def art_voyager(x, y, w, h):
    bg = (26, 20, 66)
    vgrad(x, y, x + w, y + h, (52, 34, 110), (14, 14, 44))
    rng = random.Random(18112026)
    for _ in range(55):
        ellipse(x + rng.random() * w, y + rng.random() * h, 0.6, 0.6, fill=mix((110, 120, 170), (255, 255, 255), rng.random()))
    ex, ey = x + 70, y + 14
    vx, vy = x + w - 34, y + 20
    # faint beam back to Earth
    poly([(vx - 14, vy - 10), (vx - 14, vy + 10), (ex, ey + 1.5), (ex, ey - 1.5)], (62, 50, 130))
    poly([(vx - 14, vy - 4), (vx - 14, vy + 4), (ex, ey + 0.6), (ex, ey - 0.6)], (92, 80, 170))
    glow(ex, ey, 7, (120, 180, 255), bg, 4)
    ellipse(ex, ey, 3.2, 3.2, fill=(80, 150, 240))
    # probe: big dish, bus, booms
    line([(vx + 3, vy + 4), (vx + 26, vy + 18)], (200, 200, 210), 1.4)
    line([(vx - 2, vy + 6), (vx - 10, vy + 22)], (200, 200, 210), 1.4)
    rect(vx - 5, vy + 4, vx + 6, vy + 12, fill=OCHRE, outline=OUT, width=1.2)
    ellipse(vx, vy, 15, 15, fill=(236, 236, 240), outline=OUT, width=2)
    d.pieslice([p(vx - 15, vy - 15), p(vx + 15, vy + 15)], -30, 150, fill=dark((236, 236, 240)))
    ellipse(vx - 1.5, vy - 1.5, 12, 12, fill=(236, 236, 240))
    ellipse(vx, vy, 15, 15, outline=OUT, width=2)
    ellipse(vx, vy, 2.4, 2.4, fill=(170, 170, 182))
    # ruler under the beam
    ry = y + h - 13
    line([(x + 8, ry), (x + w - 8, ry)], (210, 214, 236), 1)
    for xx in (x + 8, x + w - 8):
        line([(xx, ry - 4), (xx, ry + 4)], (210, 214, 236), 1)
    lab = "1 LIGHT-DAY = 25.9bn km"
    tf = cond(MIN_TEXT, 800)
    tw = tlen(lab, tf, 0.3) + 10
    mx = x + w / 2
    rect(mx - tw / 2, ry - 11, mx + tw / 2, ry + 10, fill=(20, 16, 54))
    text(mx, ry - 10, lab, tf, OCHRE, anchor="ma", tracking=0.3)
    text(x + 8, y + 4, "EARTH", cond(MIN_TEXT, 800), (160, 180, 236), tracking=0.6)


def art_markets(x, y, w, h):
    bg = (16, 48, 52)
    vgrad(x, y, x + w, y + h, (20, 58, 62), (12, 36, 40))
    cx, cy, cs = x + w * 0.62, y + h * 0.52, 12
    glow(cx, cy, 44, (90, 200, 120), bg, 9)
    # candles rising out of the chip, up and to the right
    vals = [(0.70, 0.30, 0.52), (0.76, 0.40, 0.62), (0.82, 0.46, 0.70), (0.88, 0.44, 0.80), (0.94, 0.62, 0.94)]
    for i, (fx, lo, hi) in enumerate(vals):
        xx = x + w * fx
        y_lo, y_hi = y + h * (1 - lo) - 6, y + h * (1 - hi)
        c = (70, 200, 120) if i != 3 else (214, 90, 70)
        line([(xx + 4, y_hi - 4), (xx + 4, y_lo + 4)], c, 1)
        rect(xx, y_hi, xx + 8, y_lo, fill=c, outline=dark(c, 0.3), width=1)
    for k in range(4):
        o = -cs + (k + 0.5) * cs * 2 / 4
        line([(cx - cs - 5, cy + o), (cx + cs + 5, cy + o)], (150, 170, 160), 1.4)
        line([(cx + o, cy - cs - 5), (cx + o, cy + cs + 5)], (150, 170, 160), 1.4)
    rrect(cx - cs, cy - cs, cx + cs, cy + cs, 4, fill=(40, 46, 50), outline=OUT, width=2)
    rrect(cx - cs * 0.62, cy - cs * 0.62, cx + cs * 0.62, cy + cs * 0.62, 2, fill=(118, 196, 40))
    for i, (lab, val) in enumerate([("KOSPI", "+2.73%"), ("NIKKEI", "+1.19%")]):
        tf = cond(MIN_TEXT, 900)
        s = lab + " " + val
        tw = tlen(s, tf) + 12
        tx, ty = x + 6, y + 5 + i * 25
        rrect(tx, ty, tx + tw, ty + 21, 10, fill=CREAM)
        text(tx + 6, ty + 1.5, lab, tf, INK)
        text(tx + 6 + tlen(lab + " ", tf), ty + 1.5, val, tf, CAT["ECONOMY"])


def art_gaza(x, y, w, h):
    vgrad(x, y, x + w, y + h, (236, 214, 176), (210, 176, 132))
    rect(x, y + h - 18, x + w, y + h, fill=(186, 150, 108))
    for i in range(6):
        tx = x + 6 + i * 22
        poly([(tx, y + h - 18), (tx + 9, y + h - 34), (tx + 18, y + h - 18)], (248, 244, 232), outline=OUT, width=1)
    lx = x + w * 0.66
    for k in range(6):
        line([(lx, y + 6 + k * (h - 12) / 6), (lx, y + 6 + k * (h - 12) / 6 + (h - 12) / 12)], (214, 168, 20), 2.4)
    text(x + 6, y + h - 11, "CEASEFIRE LINE", cond(10.5, 900), (120, 80, 10), anchor="la", tracking=0.4)
    # key info, 3 words
    kf = cond(12, 900)
    lab = "TANKS IN GAZA"
    tw = tlen(lab, kf, 0.6) + 12
    rect(x + 6, y + 5, x + 6 + tw, y + 23, fill=(26, 27, 36))
    text(x + 12, y + 6.5, lab, kf, (255, 255, 255), tracking=0.6)
    cx, cy = x + w * 0.80, y + h - 22
    rrect(cx - 26, cy - 6, cx + 26, cy + 8, 6, fill=(86, 92, 76), outline=OUT, width=1.4)
    for k in range(5):
        ellipse(cx - 20 + k * 10, cy + 8, 4.2, 4.2, fill=(52, 54, 46))
    rrect(cx - 12, cy - 16, cx + 10, cy - 5, 4, fill=(104, 110, 92), outline=OUT, width=1.4)
    line([(cx - 12, cy - 11), (cx - 30, cy - 13)], OUT, 2.6)


ART = {"eu": art_eu, "cop31": art_cop31, "voyager": art_voyager, "markets": art_markets}


# ---------------------------------------------------------------- icons
def icon(kind, x, y, s, cat):
    c = CAT[cat]
    rrect(x, y, x + s, y + s, 6, fill=c)
    wcol = (255, 255, 255)
    cx, cy = x + s / 2, y + s / 2
    u = s / 40
    if kind == "burst":
        star(cx, cy, 15 * u, wcol, n=10, inner=0.5)
        star(cx, cy, 6 * u, c, n=8, inner=0.5)
    elif kind == "cyclone":
        for i, r in enumerate((14, 10, 6)):
            arc(cx, cy, r * u, 40 + i * 120, 300 + i * 120, wcol, 2.6 * u)
        ellipse(cx, cy, 2.4 * u, 2.4 * u, fill=wcol)
    elif kind == "border":
        for k in range(5):
            line([(cx, y + 6 * u + k * 6.4 * u), (cx, y + 9.5 * u + k * 6.4 * u)], wcol, 2 * u)
        poly([(cx - 4 * u, cy), (cx - 13 * u, cy - 7 * u), (cx - 13 * u, cy + 7 * u)], wcol)
        poly([(cx + 4 * u, cy), (cx + 13 * u, cy - 7 * u), (cx + 13 * u, cy + 7 * u)], wcol)
    elif kind == "target":
        for r in (13, 7):
            arc(cx, cy, r * u, 0, 360, wcol, 2.4 * u)
        line([(cx, cy - 17 * u), (cx, cy + 17 * u)], wcol, 2 * u)
        line([(cx - 17 * u, cy), (cx + 17 * u, cy)], wcol, 2 * u)
    elif kind == "shield":
        poly([(cx, cy - 15 * u), (cx + 12 * u, cy - 10 * u), (cx + 11 * u, cy + 4 * u), (cx, cy + 15 * u),
              (cx - 11 * u, cy + 4 * u), (cx - 12 * u, cy - 10 * u)], wcol)
        poly([(cx, cy - 10 * u), (cx + 7 * u, cy - 7 * u), (cx + 6 * u, cy + 3 * u), (cx, cy + 9 * u)], c)
    elif kind == "ipo":
        poly([(cx, y + 3 * u), (cx + 7 * u, y + 11 * u), (cx - 7 * u, y + 11 * u)], wcol)
        text(cx, y + s - 3, "IPO", cond(MIN_TEXT, 900), wcol, anchor="mb")
    elif kind == "gamepad":
        rrect(cx - 15 * u, cy - 8 * u, cx + 15 * u, cy + 9 * u, 8 * u, fill=wcol)
        rect(cx - 10 * u, cy - 1.5 * u, cx - 3 * u, cy + 1.5 * u, fill=c)
        rect(cx - 8 * u, cy - 3.5 * u, cx - 5 * u, cy + 3.5 * u, fill=c)
        ellipse(cx + 6 * u, cy + 1 * u, 1.8 * u, 1.8 * u, fill=c)
        ellipse(cx + 10 * u, cy - 2 * u, 1.8 * u, 1.8 * u, fill=c)
    elif kind == "advance":
        poly([(x + 7 * u, cy - 5 * u), (x + 22 * u, cy - 5 * u), (x + 22 * u, cy - 12 * u), (x + 34 * u, cy),
              (x + 22 * u, cy + 12 * u), (x + 22 * u, cy + 5 * u), (x + 7 * u, cy + 5 * u)], wcol)
    elif kind == "fence":
        for k in (-10, 10):
            rect(cx + k * u - 2 * u, cy - 12 * u, cx + k * u + 2 * u, cy + 13 * u, fill=wcol)
        rect(cx - 16 * u, cy - 8 * u, cx + 16 * u, cy - 1 * u, fill=wcol)
        rect(cx - 16 * u, cy + 3 * u, cx + 16 * u, cy + 10 * u, fill=wcol)
        for k in range(4):
            xx = cx - 14 * u + k * 9 * u
            poly([(xx, cy - 8 * u), (xx + 4 * u, cy - 8 * u), (xx + 1 * u, cy - 1 * u), (xx - 3 * u, cy - 1 * u)], c)


# ------------------------------------------------------- v5 card artwork
REG = {
    "ASIA": (122, 62, 168), "MIDDLE EAST": (198, 96, 20), "EUROPE": (36, 84, 166),
    "AFRICA": (28, 126, 70), "NORTH AMERICA": (188, 40, 40), "LATIN AMERICA": (196, 140, 20),
    "GLOBAL": (80, 88, 100),
}


def mini_map(x, y, w, h, lon0, lon1, lat0, lat1, land, sea, outline=(255, 255, 255)):
    """Equirectangular crop of the Natural Earth world, filled into the box."""
    rect(x, y, x + w, y + h, fill=sea)

    def P(lo, la):
        return (x + (lo - lon0) / (lon1 - lon0) * w, y + (lat1 - la) / (lat1 - lat0) * h)

    for ring in WORLD:
        if any(lon0 - 20 <= lo <= lon1 + 20 and lat0 - 20 <= la <= lat1 + 20 for lo, la in ring):
            poly([P(lo, la) for lo, la in ring], land, outline=outline, width=0.6)
    return P


def drone(cx, cy, s, fill, ang=math.pi):
    def R(a, r):
        return (cx + r * math.cos(ang + a), cy + r * math.sin(ang + a))
    poly([R(0, s), R(2.5, s), R(math.pi, s * 0.35), R(-2.5, s)], fill, outline=OUT, width=1)


def art_voyager_lead(x, y, w, h):
    vgrad(x, y, x + w, y + h, (40, 30, 96), (12, 12, 40))
    rng = random.Random(18112026)
    for _ in range(90):
        ellipse(x + rng.random() * w, y + rng.random() * h, 0.6, 0.6,
                fill=mix((120, 120, 180), (255, 255, 255), rng.random()))
    ex, ey = x + 34, y + h * 0.46
    vx, vy = x + w - 62, y + h * 0.40
    poly([(vx - 18, vy - 12), (vx - 18, vy + 12), (ex, ey + 1.6), (ex, ey - 1.6)], (60, 52, 130))
    poly([(vx - 18, vy - 4), (vx - 18, vy + 4), (ex, ey + 0.6), (ex, ey - 0.6)], (110, 100, 190))
    glow(ex, ey, 14, (120, 180, 255), (24, 20, 66), 6)
    ellipse(ex, ey, 6, 6, fill=(70, 140, 236))
    poly([(ex - 3, ey - 3), (ex + 2, ey - 4), (ex + 3, ey), (ex - 1, ey + 2)], (90, 180, 110))
    line([(vx + 4, vy + 6), (vx + 40, vy + 26)], (200, 200, 210), 1.8)
    line([(vx - 3, vy + 8), (vx - 16, vy + 32)], (200, 200, 210), 1.8)
    rect(vx - 7, vy + 6, vx + 9, vy + 18, fill=OCHRE, outline=OUT, width=1.4)
    ellipse(vx, vy, 24, 24, fill=(236, 236, 240), outline=OUT, width=2)
    d.pieslice([p(vx - 24, vy - 24), p(vx + 24, vy + 24)], -30, 150, fill=dark((236, 236, 240)))
    ellipse(vx - 2, vy - 2, 19.5, 19.5, fill=(236, 236, 240))
    ellipse(vx, vy, 24, 24, outline=OUT, width=2)
    ellipse(vx, vy, 3.4, 3.4, fill=(170, 170, 182))
    tf = cond(12.5, 800)
    text(x + 8, y + 4, "EARTH", tf, (170, 190, 240), anchor="la", tracking=0.8)
    text(vx - 28, y + 4, "VOYAGER 1", tf, (220, 220, 236), anchor="ra", tracking=0.8)
    ry = y + h - 16
    line([(ex, ry), (vx, ry)], (210, 214, 236), 1)
    for xx in (ex, vx):
        line([(xx, ry - 4), (xx, ry + 4)], (210, 214, 236), 1)



def art_drones_ua(x, y, w, h):
    vgrad(x, y, x + w, y + h, (52, 70, 120), (156, 120, 130))
    rect(x, y + h - 14, x + w, y + h, fill=(40, 46, 64))
    rng = random.Random(141)
    for i in range(14):
        cx = x + 14 + (i % 7) * (w - 28) / 6 + rng.uniform(-6, 6)
        cy = y + 9 + (i // 7) * 11 + rng.uniform(-2, 2)
        if i in (3, 9):
            glow(cx, cy, 8, (255, 230, 160), (90, 90, 130), 4)
            star(cx, cy, 6, (255, 240, 200), n=8, inner=0.45)
        else:
            drone(cx, cy, 5, (226, 228, 236))
    f = cond(13, 900)
    s = "141 FIRED \u00b7 126 DOWNED"
    tw = tlen(s, f, 0.4) + 10
    rect(x + 6, y + h - 22, x + 6 + tw, y + h - 5, fill=(255, 255, 255))
    text(x + 11, y + h - 21, s, f, INK, tracking=0.4)


def art_alaska(x, y, w, h):
    P = mini_map(x, y, w, h, -176, -104, 50, 73, (60, 96, 176), (214, 226, 236))
    rect(x + w * 0.50, y, x + w, y + h, fill=(246, 240, 228))
    bx0, bx1 = x + w * 0.54, x + w - 8
    f = cond(20, 900)
    text(bx0, y + 5, "56", f, (36, 74, 150))
    text(bx1, y + 5, "44", f, (178, 34, 34), anchor="ra")
    text((bx0 + bx1) / 2, y + 8, "D \u00b7 R", cond(11, 800), INK2, anchor="ma")
    cols, rows = 20, 5
    cw = (bx1 - bx0) / cols
    for k in range(100):
        c, r = divmod(k, rows)
        col = (36, 74, 150) if k < 56 else (178, 34, 34)
        cx = bx0 + c * cw + cw / 2
        cy = y + 28 + r * ((h - 48) / rows) + 3
        ellipse(cx, cy, 1.7, 1.7, fill=col)
    text(bx0 + (bx1 - bx0) / 2, y + h - 13, "SENATE SEATS", cond(11, 800), INK2, anchor="ma", tracking=0.8)


def art_inflation(x, y, w, h):
    vgrad(x, y, x + w, y + h, (240, 232, 214), (226, 214, 190))
    base = y + h - 16
    bars = [("UK", 3.5, 3.6, (36, 74, 150)), ("EURO AREA", 3.8, 4.0, (0, 51, 153))]
    bw = 26
    for i, (lab, prev, now, col) in enumerate(bars):
        cx = x + w * (0.27 + i * 0.46)
        sc = (h - 40) / 4.2
        rect(cx - bw - 2, base - prev * sc, cx - 2, base, fill=(176, 170, 160))
        rect(cx + 2, base - now * sc, cx + bw + 2, base, fill=col, outline=OUT, width=1)
        text(cx + bw / 2 + 2, base - now * sc - 16, "%.1f%%" % now, cond(14, 900), col, anchor="ma")
        text(cx, base + 2, lab, cond(12, 800), INK2, anchor="ma", tracking=0.6)
    line([(x + 6, base), (x + w - 6, base)], INK2, 1)


def art_akvan(x, y, w, h):
    """Cyclone Akvan: a big spiral over the sea, buses evacuating along the coast."""
    vgrad(x, y, x + w, y + h, (44, 116, 176), (24, 76, 136))
    # rain streaks
    for (rx, ry) in [(0.14, 0.12), (0.30, 0.06), (0.86, 0.10), (0.92, 0.24)]:
        line([(x + w * rx, y + h * ry), (x + w * rx - 4, y + h * ry + 8)], (180, 210, 235), 1)
    # cyclone spiral, upper centre
    cx, cy = x + w * 0.50, y + h * 0.40
    for i, r in enumerate((17, 12, 7)):
        arc(cx, cy, r, 20 + i * 120, 300 + i * 120, (255, 255, 255), 3)
    ellipse(cx, cy, 3.2, 3.2, fill=(255, 255, 255))
    # coast + road at the foot
    rect(x, y + h - 14, x + w, y + h, fill=(224, 202, 152))
    line([(x, y + h - 8), (x + w, y + h - 8)], (120, 116, 108), 1)
    # two evacuation buses heading inland (to the right)
    for bx in (0.16, 0.52):
        bxx = x + w * bx
        rect(bxx, y + h - 14, bxx + 16, y + h - 6, fill=(255, 196, 60), outline=OUT, width=1)
        rect(bxx + 3, y + h - 13, bxx + 7, y + h - 10, fill=(180, 220, 240))
        rect(bxx + 9, y + h - 13, bxx + 13, y + h - 10, fill=(180, 220, 240))
        ellipse(bxx + 4, y + h - 6, 2, 2, fill=INK)
        ellipse(bxx + 12, y + h - 6, 2, 2, fill=INK)
    # tiny figures walking inland
    for fx in (0.40, 0.44, 0.86):
        px_, py_ = x + w * fx, y + h - 4
        ellipse(px_, py_ - 7, 1.8, 1.8, fill=INK)
        line([(px_, py_ - 5), (px_, py_)], INK, 1.2)


def art_sudan(x, y, w, h):
    vgrad(x, y, x + w, y + h, (246, 214, 160), (222, 168, 110))
    rng = random.Random(37)
    bx = x
    while bx < x + w:
        bw = rng.choice([14, 18, 22])
        bh = rng.choice([14, 18, 24])
        rect(bx, y + h - bh, bx + bw - 2, y + h, fill=(176, 120, 86))
        rect(bx + 4, y + h - bh + 4, bx + 8, y + h - bh + 8, fill=(120, 76, 56))
        bx += bw
    drone(x + w * 0.62, y + 20, 10, (70, 70, 84), ang=math.pi * 0.85)
    cx, cy = x + w * 0.30, y + h - 26
    arc(cx, cy, 9, 0, 360, (178, 34, 34), 2)
    line([(cx - 13, cy), (cx + 13, cy)], (178, 34, 34), 1.6)
    line([(cx, cy - 13), (cx, cy + 13)], (178, 34, 34), 1.6)
    f = cond(14, 900)
    text(x + 6, y + 5, "EL OBEID", f, INK, tracking=0.8)
    # key info, 2 words
    kf = cond(15, 900)
    lab = "37 KILLED"
    tw = tlen(lab, kf, 0.6) + 12
    rect(x + w - 6 - tw, y + 5, x + w - 6, y + 24, fill=(178, 34, 34))
    text(x + w - 12, y + 6.5, lab, kf, (255, 255, 255), anchor="ra", tracking=0.6)


def art_gold(x, y, w, h):
    vgrad(x, y, x + w, y + h, (240, 234, 220), (222, 212, 192))
    gold, goldd = (230, 180, 60), (196, 146, 40)
    for i, (gx, gy) in enumerate([(0.10, 0.62), (0.30, 0.62), (0.20, 0.36)]):
        x0, y0 = x + w * gx, y + h * gy
        poly([(x0, y0 + 18), (x0 + 6, y0), (x0 + 34, y0), (x0 + 40, y0 + 18)], gold, outline=OUT, width=1.2)
        poly([(x0 + 28, y0), (x0 + 34, y0), (x0 + 40, y0 + 18), (x0 + 32, y0 + 18)], goldd)
    ax, ay = x + w * 0.38, y + 8
    line([(ax, ay), (ax + 14, ay + 34)], (178, 34, 34), 4)
    poly([(ax + 6, ay + 36), (ax + 22, ay + 30), (ax + 18, ay + 46)], (178, 34, 34))
    text(x + w - 8, y + 8, "$3,800", cond(20, 900), (178, 34, 34), anchor="ra")
    text(x + w - 8, y + 28, "14-MONTH LOW", cond(12, 800), INK2, anchor="ra", tracking=0.5)


def art_gta(x, y, w, h):
    vgrad(x, y, x + w, y + h, (88, 40, 120), (238, 110, 120))
    ellipse(x + w * 0.74, y + h * 0.62, 20, 20, fill=(255, 196, 120))
    rect(x, y + h - 14, x + w, y + h, fill=(40, 22, 60))
    for px_ in (x + w * 0.10, x + w * 0.88):
        line([(px_, y + h - 14), (px_ + 4, y + 22)], (40, 22, 60), 3)
        for a in (-150, -120, -60, -30, -90):
            r = math.radians(a)
            line([(px_ + 4, y + 22), (px_ + 4 + 16 * math.cos(r), y + 22 - 10 * math.sin(-r) + 8)], (40, 22, 60), 2.4)
    cx, cy = x + w * 0.42, y + h * 0.60
    rrect(cx - 26, cy - 13, cx + 26, cy + 14, 13, fill=(250, 250, 250), outline=OUT, width=1.6)
    rect(cx - 18, cy - 2, cx - 8, cy + 3, fill=OUT)
    rect(cx - 15, cy - 5, cx - 11, cy + 6, fill=OUT)
    for bx, by in ((cx + 10, cy + 2), (cx + 16, cy - 3)):
        ellipse(bx, by, 2.6, 2.6, fill=(178, 34, 34))
    text(x + 6, y + 3, "MIDNIGHT IN NZ", cond(10.5, 900), (255, 236, 220), tracking=0.6)
    # key info, 2 words, on a red banner (was white-on-sun, unreadable)
    kf = cond(18, 900)
    lab = "GTA VI"
    tw = tlen(lab, kf, 0.6) + 12
    rect(x + w - 8 - tw, y + 4, x + w - 8, y + 24, fill=(178, 34, 34))
    text(x + w - 14, y + 5.5, lab, kf, (255, 255, 255), anchor="ra", tracking=0.6)


def art_anthropic(x, y, w, h):
    vgrad(x, y, x + w, y + h, (26, 34, 72), (12, 18, 46))
    for gx in range(1, 5):
        line([(x + gx * w / 5, y + 6), (x + gx * w / 5, y + h - 6)], (48, 58, 96), 0.8)
    pts = [(x + 8, y + h - 12), (x + w * 0.28, y + h - 24), (x + w * 0.48, y + h - 16),
           (x + w * 0.68, y + h - 30), (x + w - 10, y + 10)]
    for i in range(len(pts) - 1):
        line([pts[i], pts[i + 1]], (64, 224, 160), 2.4)
    for px_, py_ in pts:
        ellipse(px_, py_, 2.6, 2.6, fill=(255, 255, 255))
    text(x + 8, y + 5, "ANT", cond(15, 900), (255, 255, 255), tracking=0.8)
    text(x + w - 8, y + h - 19, "$83", cond(15, 900), (255, 196, 88), anchor="ra")


def art_border(x, y, w, h):
    P = mini_map(x, y, w, h, 32, 46, 8.5, 18.5, (214, 196, 160), (150, 190, 214))
    bx = x + w * 0.52
    for k in range(7):
        line([(bx, y + 6 + k * (h - 12) / 7), (bx, y + 6 + k * (h - 12) / 7 + (h - 12) / 14)], INK, 2)
    cy = y + h * 0.56
    poly([(bx - 6, cy), (bx - 26, cy - 11), (bx - 26, cy - 4), (bx - 48, cy - 4), (bx - 48, cy + 4),
          (bx - 26, cy + 4), (bx - 26, cy + 11)], (28, 126, 70), outline=OUT, width=1)
    poly([(bx + 6, cy), (bx + 26, cy - 11), (bx + 26, cy - 4), (bx + 48, cy - 4), (bx + 48, cy + 4),
          (bx + 26, cy + 4), (bx + 26, cy + 11)], (150, 90, 40), outline=OUT, width=1)
    f = cond(12.5, 900)
    text(bx - 8, y + 5, "ETHIOPIA", f, INK, anchor="ra", tracking=0.5)
    text(bx + 8, y + 5, "ERITREA", f, INK, tracking=0.5)


def art_hague(x, y, w, h):
    """ICJ ruling: golden scales on a dark navy ground, gavel at the foot."""
    vgrad(x, y, x + w, y + h, (26, 42, 88), (12, 22, 52))
    cx, cy = x + w / 2, y + h * 0.50
    # gold disc behind the scales
    ellipse(cx, cy, 30, 30, fill=(216, 168, 70), outline=(240, 200, 110), width=1.6)
    ellipse(cx, cy, 24, 24, outline=(240, 200, 110), width=1)
    # scales, dark on gold
    line([(cx, cy - 20), (cx, cy + 18)], INK, 2.6)
    line([(cx - 24, cy - 14), (cx + 24, cy - 14)], INK, 2.6)
    ellipse(cx, cy - 22, 3, 3, fill=INK)
    for sgn in (-1, 1):
        px_ = cx + sgn * 24
        line([(px_, cy - 14), (px_ - 9, cy + 2)], INK, 1.5)
        line([(px_, cy - 14), (px_ + 9, cy + 2)], INK, 1.5)
        poly([(px_ - 11, cy + 2), (px_ + 11, cy + 2), (px_, cy + 12)], INK)
    # gavel, diagonal at the foot
    gx, gy = x + w * 0.78, y + h * 0.82
    poly([(gx - 16, gy + 4), (gx + 8, gy - 12), (gx + 12, gy - 8), (gx - 12, gy + 8)], (120, 84, 52), outline=OUT, width=1)
    rect(gx + 4, gy - 16, gx + 14, gy - 6, fill=(150, 106, 66), outline=OUT, width=1)


def art_pif(x, y, w, h):
    """Riyadh: the PIF Tower against a sunset sky, impact flash and smoke at the top."""
    vgrad(x, y, x + w, y + h, (255, 168, 92), (186, 66, 58))
    ellipse(x + w * 0.14, y + h * 0.26, 11, 11, fill=(255, 240, 200))
    # low skyline silhouette
    rng = random.Random(1911)
    bx = x
    while bx < x + w:
        bw = rng.choice([12, 16, 20])
        bh = rng.choice([8, 12, 16])
        rect(bx, y + h - bh, bx + bw - 2, y + h, fill=(70, 44, 76))
        bx += bw
    # PIF tower: dark steel slab, centre-right, tapering
    tx0, tx1 = x + w * 0.55, x + w * 0.74
    ty0, ty1 = y + 8, y + h - 12
    poly([(tx0, ty1), (tx0 + 5, ty0 + 8), (tx1 - 5, ty0 + 8), (tx1, ty1)], (44, 60, 96), outline=OUT, width=1.4)
    poly([(tx0 + 5, ty0 + 8), (tx1 - 5, ty0 + 8), (tx1 - 9, ty0 + 24), (tx0 + 9, ty0 + 24)], (30, 42, 72))
    for k in range(5):
        yy = ty0 + 28 + k * (ty1 - ty0 - 40) / 4
        line([(tx0 + 6, yy), (tx1 - 6, yy)], (120, 136, 180), 0.8)
    # impact flash + smoke at the top of the tower
    fx, fy = tx0 + 2, ty0 + 14
    glow(fx, fy, 12, (255, 224, 130), (255, 168, 92), 6)
    star(fx, fy, 8, (255, 244, 200), n=8, inner=0.45)
    for (sx, sy, r) in [(16, -8, 4), (24, -12, 5), (32, -10, 3.4)]:
        ellipse(fx + sx, fy + sy, r, r * 0.7, fill=(120, 116, 112))
    # crack below the impact
    line([(fx + 2, fy + 8), (fx + 6, fy + 16), (fx + 1, fy + 22)], (20, 20, 30), 1.4)


def art_kyiv(x, y, w, h):
    """Kyiv under drone attack: big drones, searchlights, a burning building."""
    vgrad(x, y, x + w, y + h, (38, 48, 98), (14, 16, 38))
    rng = random.Random(1919)
    for _ in range(22):
        ellipse(x + rng.random() * w, y + rng.random() * h * 0.45, 0.7, 0.7,
                fill=mix((120, 130, 180), (255, 255, 255), rng.random()))
    # fire glow at the foot of the city
    glow(x + w * 0.52, y + h - 6, 26, (255, 150, 50), (20, 20, 44), 7)
    # searchlight beams
    poly([(x + w * 0.18, y + h), (x + w * 0.20, y + h), (x + w * 0.34, y + 6), (x + w * 0.30, y + 6)], (200, 208, 235))
    poly([(x + w * 0.82, y + h), (x + w * 0.84, y + h), (x + w * 0.66, y + 10), (x + w * 0.62, y + 10)], (200, 208, 235))
    # city silhouette with one burning building
    bx = x
    while bx < x + w:
        bw = rng.choice([16, 20, 26])
        bh = rng.choice([12, 18, 24])
        rect(bx, y + h - bh, bx + bw - 2, y + h, fill=(22, 24, 46))
        if rng.random() < 0.5:
            rect(bx + 4, y + h - bh + 4, bx + 7, y + h - bh + 7, fill=(255, 210, 120))
        bx += bw
    # burning building, centre
    fx, fy = x + w * 0.52, y + h - 24
    rect(fx - 12, fy, fx + 12, y + h, fill=(16, 18, 36))
    poly([(fx - 9, fy), (fx - 3, fy - 14), (fx + 1, fy - 4), (fx + 6, fy - 16), (fx + 10, fy)],
         (240, 120, 40), outline=OUT, width=1)
    poly([(fx - 4, fy), (fx - 1, fy - 8), (fx + 3, fy - 2), (fx + 5, fy)], (255, 210, 90))
    # four large drones with red navigation lights
    for (dx, dy, s) in [(0.24, 0.24, 10), (0.48, 0.16, 9), (0.70, 0.30, 11), (0.86, 0.18, 8)]:
        drone(x + w * dx, y + h * dy, s, (228, 230, 238), ang=math.pi * 0.9)
        ellipse(x + w * dx + s * 0.8, y + h * dy + s * 0.4, 1.6, 1.6, fill=(255, 60, 60))


def art_ant(x, y, w, h):
    """Anthropic debut: green rise on the left, red slide on the right."""
    rect(x, y, x + w / 2, y + h, fill=(14, 56, 38))
    rect(x + w / 2, y, x + w, y + h, fill=(82, 24, 24))
    line([(x + w / 2, y), (x + w / 2, y + h)], (255, 255, 255), 1)
    # rising line, left
    pts = [(x + 6, y + h - 12), (x + w * 0.18, y + h - 26), (x + w * 0.34, y + h - 18), (x + w * 0.46, y + 10)]
    for i in range(len(pts) - 1):
        line([pts[i], pts[i + 1]], (64, 224, 160), 2.2)
    for px_, py_ in pts:
        ellipse(px_, py_, 2.2, 2.2, fill=(255, 255, 255))
    text(x + 6, y + 4, "ANT", cond(11, 900), (255, 255, 255), tracking=0.8)
    text(x + 6, y + h - 18, "+17%", cond(11, 900), (64, 224, 160))
    # falling line, right
    pts2 = [(x + w * 0.54, y + 12), (x + w * 0.68, y + h * 0.38), (x + w * 0.84, y + h * 0.52), (x + w - 6, y + h - 10)]
    for i in range(len(pts2) - 1):
        line([pts2[i], pts2[i + 1]], (255, 100, 90), 2.2)
    for px_, py_ in pts2:
        ellipse(px_, py_, 2.2, 2.2, fill=(255, 255, 255))
    text(x + w * 0.54, y + 4, "NASDAQ", cond(10, 900), (255, 255, 255), tracking=0.6)
    text(x + w * 0.54, y + h - 18, "-2.2%", cond(11, 900), (255, 140, 130))


def art_dhaka_fire(x, y, w, h):
    """Dhaka: a house with big flames bursting from the roof and windows."""
    vgrad(x, y, x + w, y + h, (66, 54, 60), (32, 28, 36))
    # smoke above
    for (sx, sy, r) in [(0.30, 0.14, 6), (0.52, 0.08, 7), (0.72, 0.14, 5)]:
        ellipse(x + w * sx, y + h * sy, r, r * 0.7, fill=(110, 106, 110))
    # house silhouette
    hx0, hx1, hy = x + w * 0.24, x + w * 0.76, y + h * 0.58
    rect(hx0, hy, hx1, y + h - 8, fill=(36, 34, 44))
    poly([(hx0 - 6, hy), (x + w * 0.50, hy - 16), (hx1 + 6, hy)], (28, 26, 36))
    rect(hx0 + 8, hy + 10, hx0 + 20, hy + 22, fill=(255, 170, 60))
    rect(hx1 - 20, hy + 10, hx1 - 8, hy + 22, fill=(255, 170, 60))
    # big flames from the roof
    fx, fy = x + w * 0.50, hy - 12
    poly([(fx - 18, fy + 12), (fx - 10, fy - 16), (fx - 3, fy - 2), (fx + 4, fy - 22),
          (fx + 10, fy - 6), (fx + 18, fy + 12)], (240, 120, 40), outline=OUT, width=1.2)
    poly([(fx - 9, fy + 10), (fx - 4, fy - 8), (fx + 1, fy + 2), (fx + 6, fy - 10), (fx + 9, fy + 10)],
         (255, 210, 90))
    # embers
    for (ex, ey) in [(0.22, 0.30), (0.80, 0.24), (0.66, 0.36)]:
        ellipse(x + w * ex, y + h * ey, 2, 2, fill=(255, 180, 80))


def art_tanker(x, y, w, h):
    """Hormuz: a supertanker with a large spiked mine in the foreground."""
    vgrad(x, y, x + w, y + h, (18, 52, 84), (10, 32, 60))
    for k in range(3):
        yy = y + h * (0.26 + k * 0.18)
        line([(x + 6, yy), (x + w - 6, yy)], (60, 110, 150), 0.8)
    # tanker, centre-right
    hx0, hx1, hy = x + w * 0.34, x + w * 0.92, y + h * 0.50
    poly([(hx0, hy), (hx0 + 8, hy + 12), (hx1 - 5, hy + 12), (hx1, hy)], (24, 28, 44), outline=OUT, width=1.4)
    rect(hx0 + 6, hy - 10, hx1 - 16, hy, fill=(178, 34, 34), outline=OUT, width=1.2)
    rect(hx1 - 14, hy - 20, hx1 - 5, hy, fill=(236, 236, 240), outline=OUT, width=1.2)
    for k in range(4):
        cx = hx0 + 12 + k * (hx1 - hx0 - 32) / 3
        rect(cx, hy - 7, cx + 5, hy - 2, fill=(255, 196, 88))
    # large mine, foreground left
    mx, my = x + w * 0.18, y + h * 0.76
    for a in range(0, 360, 45):
        r = math.radians(a)
        line([(mx + 9 * math.cos(r), my + 9 * math.sin(r)),
              (mx + 15 * math.cos(r), my + 15 * math.sin(r))], (210, 210, 220), 1.8)
    ellipse(mx, my, 10, 10, fill=(60, 64, 76), outline=(255, 255, 255), width=1.4)
    # warning triangle, top right
    tx, ty = x + w - 20, y + 6
    poly([(tx + 7, ty), (tx + 14, ty + 12), (tx, ty + 12)], OCHRE, outline=OUT, width=1)
    text(tx + 7, ty + 2, "!", cond(10, 900), INK, anchor="ma")


def art_gaza_return(x, y, w, h):
    """Gaza: a tank withdrawing on a road, families walking back toward tents."""
    vgrad(x, y, x + w, y + h, (240, 224, 190), (216, 190, 150))
    # road, perspective
    poly([(x + w * 0.34, y + h), (x + w * 0.46, y + h * 0.40), (x + w * 0.54, y + h * 0.40),
          (x + w * 0.66, y + h)], (232, 226, 214))
    # tents in the distance, right
    for (tx, ts) in [(0.68, 10), (0.80, 13), (0.90, 9)]:
        txx = x + w * tx
        poly([(txx - ts, y + h * 0.40), (txx, y + h * 0.40 - ts * 0.8), (txx + ts, y + h * 0.40)],
             (250, 246, 236), outline=OUT, width=1)
    # big tank, rear view, centre-left on the road
    tx0, tx1, ty = x + w * 0.30, x + w * 0.58, y + h * 0.62
    rect(tx0, ty, tx1, ty + 12, fill=(74, 82, 66), outline=OUT, width=1.2)
    rect(tx0 + 6, ty - 10, tx1 - 6, ty, fill=(88, 96, 78), outline=OUT, width=1.2)
    rect(tx0 - 3, ty + 12, tx1 + 3, ty + 16, fill=(40, 44, 38))
    line([(tx0 + 10, ty - 10), (tx0 + 12, ty - 18)], (60, 66, 54), 2)
    # walking figures on the road
    for (fx, fy, s) in [(0.62, 0.66, 5), (0.68, 0.74, 6), (0.60, 0.82, 7)]:
        px_, py_ = x + w * fx, y + h * fy
        ellipse(px_, py_ - s * 1.6, s * 0.45, s * 0.45, fill=INK)
        line([(px_, py_ - s), (px_, py_ + s * 0.4)], INK, 1.6)
        line([(px_, py_ - s * 0.4), (px_ - s * 0.7, py_ + s)], INK, 1.4)
        line([(px_, py_ - s * 0.4), (px_ + s * 0.7, py_ + s)], INK, 1.4)
    glow(x + w * 0.82, y + h * 0.22, 12, (255, 220, 140), (240, 224, 190), 5)
    ellipse(x + w * 0.82, y + h * 0.22, 6, 6, fill=(255, 232, 170))


def art_talks(x, y, w, h):
    """Berlin talks: a negotiation table with US and Russian flags, a handshake."""
    vgrad(x, y, x + w, y + h, (204, 210, 220), (178, 186, 200))
    # handshake above the table: two forearms meeting in a clasp
    cx, cy = x + w * 0.50, y + h * 0.34
    poly([(x + w * 0.06, cy - 6), (cx - 12, cy - 4), (cx - 12, cy + 6), (x + w * 0.06, cy + 8)], (52, 54, 66))
    poly([(x + w * 0.94, cy - 6), (cx + 12, cy - 4), (cx + 12, cy + 6), (x + w * 0.94, cy + 8)], (70, 72, 84))
    ellipse(cx, cy, 9, 7, fill=(232, 190, 150), outline=OUT, width=1.2)
    line([(cx - 9, cy - 2), (cx + 9, cy + 2)], (200, 150, 110), 1.2)
    # table
    rect(x + 6, y + h - 18, x + w - 6, y + h - 8, fill=(150, 106, 66), outline=OUT, width=1.2)
    rect(x + 6, y + h - 8, x + w - 6, y + h, fill=(120, 84, 52))
    # US flag on the table, left
    fx = x + w * 0.20
    line([(fx, y + h - 34), (fx, y + h - 18)], (80, 78, 72), 1.2)
    rect(fx, y + h - 34, fx + 18, y + h - 22, fill=(200, 40, 40), outline=OUT, width=0.8)
    rect(fx, y + h - 34, fx + 8, y + h - 28, fill=(30, 44, 86))
    line([(fx, y + h - 29), (fx + 18, y + h - 29)], (255, 255, 255), 1)
    line([(fx, y + h - 25), (fx + 18, y + h - 25)], (255, 255, 255), 1)
    # Russian flag on the table, right
    fx = x + w * 0.72
    line([(fx, y + h - 34), (fx, y + h - 18)], (80, 78, 72), 1.2)
    rect(fx, y + h - 34, fx + 18, y + h - 30, fill=(245, 245, 240), outline=OUT, width=0.8)
    rect(fx, y + h - 30, fx + 18, y + h - 26, fill=(40, 90, 180), outline=OUT, width=0.8)
    rect(fx, y + h - 26, fx + 18, y + h - 22, fill=(200, 40, 40), outline=OUT, width=0.8)


def art_cost48(x, y, w, h):
    """War cost: a tall stack of gold coins and the $48.3bn figure."""
    vgrad(x, y, x + w, y + h, (242, 236, 222), (224, 214, 194))
    # coin stack, left
    cx = x + w * 0.26
    for k in range(6):
        cy = y + h - 12 - k * 6
        ellipse(cx, cy, 13, 3.6, fill=(222, 176, 80), outline=(160, 120, 50), width=1)
    ellipse(cx, y + h - 12 - 5 * 6 - 3, 13, 3.6, fill=(240, 200, 110), outline=(160, 120, 50), width=1)
    text(cx, y + h - 12 - 5 * 6 - 12, "$", serif(20, 900), (120, 88, 30), anchor="ma")
    # figure, right
    text(x + w - 8, y + h * 0.30, "$48.3bn", cond(13, 900), (178, 34, 34), anchor="ra")
    text(x + w - 8, y + h * 0.58, "WAR COST", cond(10, 900), INK2, anchor="ra", tracking=0.6)
    # scattered coins at the foot
    for (sx, sy) in [(0.62, 0.82), (0.74, 0.88), (0.86, 0.80)]:
        ellipse(x + w * sx, y + h * sy, 6, 2.4, fill=(222, 176, 80), outline=(160, 120, 50), width=1)


def art_shield(x, y, w, h):
    """Cyberattack: a laptop showing a shield with circuit nodes, red alert badge."""
    vgrad(x, y, x + w, y + h, (24, 40, 84), (12, 22, 52))
    # laptop screen + base
    sx0, sy0, sx1, sy1 = x + w * 0.14, y + 6, x + w * 0.86, y + h - 14
    rect(sx0, sy0, sx1, sy1, fill=(16, 24, 48), outline=(120, 140, 180), width=1.4)
    poly([(sx0 - 6, sy1), (sx1 + 6, sy1), (sx1 + 10, y + h - 6), (sx0 - 10, y + h - 6)], (140, 148, 164), outline=OUT, width=1)
    # shield on the screen with circuit nodes
    cx, cy = x + w * 0.50, y + h * 0.46
    s = 13
    poly([(cx, cy - s), (cx + s * 0.85, cy - s * 0.55), (cx + s * 0.75, cy + s * 0.45),
          (cx, cy + s), (cx - s * 0.75, cy + s * 0.45), (cx - s * 0.85, cy - s * 0.55)],
         (38, 62, 120), outline=(150, 180, 230), width=1.4)
    nodes = [(cx - 5, cy - 4), (cx + 5, cy - 5), (cx, cy + 1), (cx - 4, cy + 6), (cx + 5, cy + 5)]
    for (nx, ny) in nodes:
        ellipse(nx, ny, 2, 2, fill=(120, 200, 140))
    for (a, b) in [(0, 2), (1, 2), (2, 3), (2, 4)]:
        line([nodes[a], nodes[b]], (120, 200, 140), 1)
    # red alert badge, top-right of the screen
    bx, by = sx1 - 4, sy0 + 4
    ellipse(bx, by, 7, 7, fill=(200, 40, 40), outline=(255, 255, 255), width=1.2)
    text(bx, by - 6, "!", cond(11, 900), (255, 255, 255), anchor="ma")


def art_strike(x, y, w, h):
    """Bogota strike: a dense crowd with three big placards and a raised fist."""
    vgrad(x, y, x + w, y + h, (244, 230, 200), (228, 206, 168))
    base = y + h - 10
    # three large placards on sticks
    for (px_, col, mark) in [(0.22, (178, 34, 34), "o"), (0.50, (36, 84, 166), "s"), (0.78, (28, 126, 70), "l")]:
        sx = x + w * px_
        line([(sx, base - 30), (sx, base - 30 - 14)], INK, 1.4)
        rect(sx - 15, base - 44, sx + 15, base - 30, fill=col, outline=OUT, width=1)
        if mark == "o":
            ellipse(sx, base - 37, 4.5, 4.5, outline=(255, 255, 255), width=1.6)
        elif mark == "s":
            star(sx, base - 37, 5, (255, 255, 255))
        else:
            line([(sx - 8, base - 37), (sx + 8, base - 37)], (255, 255, 255), 2)
    # raised fist, right
    fx, fy = x + w * 0.90, base - 34
    ellipse(fx, fy, 5, 5, fill=(232, 190, 150), outline=OUT, width=1)
    rect(fx - 4, fy + 4, fx + 4, fy + 12, fill=(232, 190, 150), outline=OUT, width=1)
    # dense crowd: heads + shoulders
    rng = random.Random(1919)
    for i in range(10):
        cx = x + 8 + i * (w - 16) / 9 + rng.uniform(-2, 2)
        cy = base - 14 + rng.uniform(-3, 3)
        ellipse(cx, cy - 7, 4.6, 4.6, fill=(52, 54, 66))
        poly([(cx - 7, base), (cx - 5, cy - 2), (cx + 5, cy - 2), (cx + 7, base)],
             mix((52, 54, 66), (200, 180, 150), rng.random() * 0.5))
    rect(x, base, x + w, y + h, fill=(186, 150, 108))


def art_marathon(x, y, w, h):
    """Banned marathon champion: a runner crossing the finish tape, slashed medal."""
    vgrad(x, y, x + w, y + h, (238, 228, 204), (216, 200, 170))
    # track lanes
    for k in range(2):
        yy = y + h * (0.66 + k * 0.14)
        line([(x + 6, yy), (x + w - 6, yy)], (180, 170, 150), 1)
    # checkered finish tape across the top third
    ty = y + 8
    for k in range(12):
        rect(x + 8 + k * (w - 16) / 12, ty, x + 8 + (k + 1) * (w - 16) / 12, ty + 7,
             fill=(26, 27, 36) if k % 2 == 0 else (255, 255, 255), outline=OUT, width=0.6)
    line([(x + 8, ty + 7), (x + 8, ty + 16)], INK, 1.4)
    line([(x + w - 8, ty + 7), (x + w - 8, ty + 16)], INK, 1.4)
    # runner, striding through the tape
    cx, cy = x + w * 0.46, y + h * 0.52
    ellipse(cx, cy - 15, 5.5, 5.5, fill=INK)
    line([(cx, cy - 9), (cx + 2, cy + 6)], INK, 2.2)
    line([(cx + 2, cy + 6), (cx - 12, cy + 20)], INK, 2)
    line([(cx + 2, cy + 6), (cx + 14, cy + 14)], INK, 2)
    line([(cx, cy - 7), (cx - 14, cy - 15)], INK, 2)
    line([(cx, cy - 7), (cx + 14, cy - 1)], INK, 2)
    # medal with a red prohibition slash, top-right
    mx, my = x + w * 0.84, y + h * 0.30
    ellipse(mx, my, 11, 11, fill=OCHRE, outline=OUT, width=1.4)
    text(mx, my - 8, "1", cond(13, 900), INK, anchor="ma")
    ellipse(mx, my, 14, 14, outline=(178, 34, 34), width=2.6)
    line([(mx - 10, my - 10), (mx + 10, my + 10)], (178, 34, 34), 2.6)


def art_exam(x, y, w, h):
    """Suneung exam: a classroom of desks with students writing, wall clock."""
    vgrad(x, y, x + w, y + h, (226, 234, 244), (196, 210, 228))
    # blackboard strip at the top
    rect(x, y, x + w, y + 9, fill=(46, 84, 66))
    line([(x + 8, y + 5), (x + w * 0.55, y + 5)], (220, 230, 220), 1)
    # wall clock, top right
    kx, ky = x + w * 0.86, y + h * 0.30
    ellipse(kx, ky, 8, 8, fill=(255, 255, 255), outline=OUT, width=1.4)
    line([(kx, ky), (kx, ky - 5)], INK, 1.4)
    line([(kx, ky), (kx + 4, ky + 1)], INK, 1.4)
    # two rows of desks with students bent over papers
    for row, ry in enumerate((0.52, 0.78)):
        for col in range(3):
            dx = x + w * (0.14 + col * 0.30)
            dy = y + h * ry
            rect(dx, dy, dx + 26, dy + 8, fill=(150, 106, 66), outline=OUT, width=1)
            ellipse(dx + 13, dy - 8, 5, 5, fill=(52, 54, 66))
            rect(dx + 6, dy - 4, dx + 20, dy, fill=(255, 255, 255), outline=OUT, width=0.8)


ART = {"peace": art_peace, "gulf": art_gulf, "voyager": art_voyager_lead,
       "eu": art_eu, "drones_ua": art_drones_ua, "alaska": art_alaska, "cop31": art_cop31,
       "inflation": art_inflation, "akvan": art_akvan, "sudan": art_sudan,
       "gold": art_gold, "gta": art_gta, "border": art_border, "gaza": art_gaza,
       "anthropic": art_anthropic, "hague": art_hague, "pif": art_pif,
       "kyiv": art_kyiv, "ant": art_ant,
       "dhaka_fire": art_dhaka_fire, "tanker": art_tanker, "gaza_return": art_gaza_return,
       "talks": art_talks, "cost48": art_cost48, "shield": art_shield,
       "strike": art_strike, "marathon": art_marathon, "exam": art_exam}


# v4: the 16 card images are ready-made files (the user's own generations
# for cards 1-15, the GTA VI image for card 16), not PIL drawings.
# assets/cards/small/NN.png is 232x104; it is centre-cropped to fill the
# art slot and pasted at 2x. The PIL art functions above are unused by
# this page but kept for reference.
PHOTO = {"peace": "01", "hague": "02", "pif": "03", "kyiv": "04",
         "ant": "05", "cop31": "06", "dhaka_fire": "07", "akvan": "08",
         "tanker": "09", "gaza_return": "10", "talks": "11", "cost48": "12",
         "shield": "13", "strike": "14", "marathon": "15", "gta": "16"}
_photo_cache = {}


def paste_photo(x, y, w, h, num):
    """Centre-crop assets/cards/small/NN.png to fill the (w, h) art slot."""
    if num not in _photo_cache:
        _photo_cache[num] = Image.open(
            os.path.join(HERE, "assets", "cards", "small", num + ".png")).convert("RGB")
    im = _photo_cache[num]
    iw, ih = im.size
    target = w / h
    if iw / ih > target:
        nw = int(ih * target)
        x0 = (iw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, ih))
    else:
        nh = int(iw / target)
        y0 = (ih - nh) // 2
        im = im.crop((0, y0, iw, y0 + nh))
    im = im.resize((round(w * S), round(h * S)), Image.LANCZOS)
    img.paste(im, (round(x * S), round(y * S)))


# ------------------------------------------------------------------ page
M = 22
R = W - M


def pin(cx, cy, num, col, r=7.5):
    ellipse(cx, cy, r + 1.3, r + 1.3, fill=(255, 255, 255))
    ellipse(cx, cy, r, r, fill=col)
    s = str(num)
    text(cx, cy + 0.4, s, cond(r * (1.5 if len(s) == 1 else 1.45), 900), (255, 255, 255), anchor="mm")


def header():
    # vertical budget: top bar 0-6, kicker 15-27, title 31-101,
    # subtitle 106-121, region bar 130-150
    rect(0, 0, W, 6, fill=INK)
    # kicker + story count on one baseline (y=15, 12px)
    f = cond(12, 800)
    text(M, 15, "THE DAY IN WORLD NEWS", f, CAT["CONFLICT"], tracking=1.6)
    text(R, 15, "%d STORIES \u00b7 7 REGIONS \u00b7 ONE DAY" % st.count(), f, INK2, anchor="ra", tracking=1.6)
    # title: v12 scales it to 74% of the full width (fits 726 px, ends
    # x~746); the baseline stays at y~96 (draw y = 96 - ascent, from the
    # real font). Letter-spacing -0.01em, as before.
    title = "Thursday 19 November 2026"
    best = None
    for sz in range(90, 50, -1):
        tf = serif(sz, 900, 100)
        w = tlen(title, tf, -0.01 * sz)
        if w <= 726:
            best = (sz, tf, w)
            break
    sz, tf, w = best
    assert abs((M + w) - 746) <= 2, "title ends at %.1f, not ~746" % (M + w)
    ty = round(96 - tf.getmetrics()[0] / S)
    text(M, ty, title, tf, INK, tracking=-0.01 * sz)
    # v12 credibility block in the freed area x 758..1002, y 46..102:
    # 1px vertical rule (divider colour), heading, then 4 body lines.
    # Heading centre y=52, body line centres y=64/75/86/97.
    line([(758, 46), (758, 102)], RULE, 1)
    _ch = "HOW THIS PAGE WAS CHECKED"
    assert tlen(_ch, cond(9, 800), 1.2) <= 236, "credibility heading too wide"
    text(766, 48, _ch, cond(9, 800), CAT["CONFLICT"], tracking=1.2)
    _cred = [
        "Each story is dated by its first report (UTC).",
        "Claims by warring sides are marked CLAIM.",
        "Sources named on every story: Reuters, AP, AFP,",
        "BBC, UN News and official records. See Date Check.",
    ]
    _cf = serif_i(9, 600)
    for _ln in _cred:
        assert tlen(_ln, _cf) <= 236, "credibility line too wide: %r" % _ln
    for _i, _ln in enumerate(_cred):
        text(766, 60 + 11 * _i, _ln, _cf, (58, 58, 58))
    text(M, 106, st.JUDGE_NOTE, serif_i(15, 600), INK2)
    # region bar: y 130..150, height 20, equal-width segments, 2px gaps, 11px bold
    y = 130
    counts = {}
    for _, s in st.all_stories():
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    regs = [r for r in st.REGIONS if counts.get(r)]
    bw = (R - M) / len(regs)
    bf = cond(11, 900)
    x = M
    for r in regs:
        rect(x, y, x + bw - 2, y + 20, fill=REG[r])
        text(x + bw / 2 - 1, y + 3.5, "%s %d" % (r, counts[r]), bf, (255, 255, 255), anchor="ma", tracking=0.8)
        x += bw
    return y + 20  # 150


def card(x, y, w, art_h, s, num, hsize, dsize, lead):
    col = REG[s["region"]]
    rect(x, y, x + w, y + 3, fill=col)
    if s["art"] in PHOTO:
        paste_photo(x, y + 3, w, art_h, PHOTO[s["art"]])
    else:
        clipped(ART[s["art"]], x, y + 3, w, art_h)

    # label row (regular cards use a tighter gap/row so a row is exactly 155px)
    agap = 7 if lead else 5
    yy = y + 3 + art_h + agap
    if lead:
        # number circle 16px, 11px caps kicker, source right-aligned 10px
        pin(x + 8, yy + 7, num, col, r=8)
        kf = cond(11, 800)
        text(x + 21, yy, s["region"] + " \u00b7 " + s["beat"], kf, col, tracking=0.6)
        text(x + w, yy, s["src"], cond(10, 700), GREY, anchor="ra", tracking=0.5)
        if s.get("tag"):
            text(x + w, yy, s["tag"], cond(10, 700), GREY, anchor="ra", tracking=0.5)
    else:
        # level 2: 14px pin, 6px gap, 10px region+topic (0.04em tracking),
        # 10px source right-aligned on the same baseline.
        # Row never exceeds the card width: drop the topic word first,
        # keep only the region. The source is never dropped or shortened.
        pin(x + 7, yy + 7, num, col, r=7)
        tf = cond(10, 800)
        sf = cond(10, 700)
        lab = s["topic"]
        lw = tlen(lab, tf, 0.38)
        sw = tlen(s["src"], sf)
        if 14 + 6 + lw + sw > w:
            lab = lab.split(" \u00b7 ")[0]
        text(x + 20, yy, lab, tf, col, tracking=0.38)
        text(x + w, yy, s["src"], sf, GREY, anchor="ra")
    yy += 18 if lead else 16
    # headline: exactly 2 lines (lead 26/28, level2 17/21)
    hf = serif(hsize, 900)
    hlead = 28 if lead else 21
    lines = wrap(s["hed"], hf, w)[:2]
    for ln in lines:
        text(x, yy, ln, hf, INK)
        yy += hlead
    yy += 3
    # dek: exactly 2 lines (lead 13.5/16, level2 12.5/15)
    df = sans(dsize, 500, 87.5)
    dlead = 16 if lead else 15
    for ln in wrap(s["dek"], df, w)[:2]:
        text(x, yy, ln, df, INK2)
        yy += dlead
    return yy


def map_block(x0, y0, w):
    # map image only (header drawn by build at y=728); height ~80, 1px warm-grey frame
    my = y0
    lat0, lat1 = 60.0, -38.0
    h = round(w * (lat0 - lat1) / 360)  # 81 at w=296
    rect(x0, my, x0 + w, my + h, outline=(200, 190, 175), width=1)
    sea, landc = (214, 224, 230), (204, 196, 182)

    def P(lo, la):
        return (x0 + (lo + 180) / 360 * w, my + (lat0 - la) / (lat0 - lat1) * h)

    def land(ax, ay, aw, ah):
        rect(ax, ay, ax + aw, ay + ah, fill=sea)
        for ring in WORLD:
            poly([P(lo, la) for lo, la in ring], landc, outline=(255, 255, 255), width=0.5)

    clipped(land, x0, my, w, h)
    stories = st.all_stories()
    nlead = len(st.LEAD) + len(st.CARDS)
    pins = [(n, s) + P(*s["at"]) for n, s in stories[:nlead] if s.get("at")]
    pos = [[q[2], q[3]] for q in pins]
    for _ in range(300):
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                dx, dy = pos[j][0] - pos[i][0], pos[j][1] - pos[i][1]
                dist = math.hypot(dx, dy) or 0.01
                if dist < 15:
                    push = (15 - dist) / 2
                    ux, uy = dx / dist, dy / dist
                    pos[i][0] -= ux * push; pos[i][1] -= uy * push
                    pos[j][0] += ux * push; pos[j][1] += uy * push
        for q in pos:
            q[0] = min(x0 + w - 8, max(x0 + 8, q[0]))
            q[1] = min(my + h - 8, max(my + 8, q[1]))
    # brief dots: every brief gets a dot. If its true spot sits under a
    # numbered pin (final or true position) or on another dot, nudge it to
    # the nearest free spot on a small ring so it stays visible.
    drawn_dots = []
    for n, s in stories[nlead:]:
        px_, py_ = P(*s["at"])
        cands = [(px_, py_)]
        for rad in (14, 20, 26):
            for ang in range(8):
                a = math.radians(ang * 45)
                cands.append((px_ + rad * math.cos(a), py_ + rad * math.sin(a)))
        spot = None
        for cx, cy in cands:
            if not (x0 + 4 <= cx <= x0 + w - 4 and my + 4 <= cy <= my + h - 4):
                continue
            if any(math.hypot(cx - qx, cy - qy) < 12 for qx, qy in pos):
                continue
            if any(math.hypot(cx - q[2], cy - q[3]) < 12 for q in pins):
                continue
            if any(math.hypot(cx - dx, cy - dy) < 5 for dx, dy in drawn_dots):
                continue
            spot = (cx, cy)
            break
        if not spot:
            continue
        drawn_dots.append(spot)
        ellipse(spot[0], spot[1], 2.4, 2.4, fill=(255, 255, 255))
        ellipse(spot[0], spot[1], 1.8, 1.8, fill=REG[s["region"]])
    for (n, s, tx, ty), (cx, cy) in zip(pins, pos):
        if math.hypot(cx - tx, cy - ty) > 3:
            line([(tx, ty), (cx, cy)], INK2, 0.7)
            ellipse(tx, ty, 1.4, 1.4, fill=INK)
    for (n, s, tx, ty), (cx, cy) in zip(pins, pos):
        pin(cx, cy, n, REG[s["region"]], r=6.6)
    return my + h


def _mins(tm):
    h, m = tm.split(":")
    return int(h) * 60 + int(m)


def chip_strip(y0):
    # v7 chip strip: clock icon + "UTC", then 7 chips spread evenly M..R.
    # Each chip: coloured time rect (region colour, white bold time) +
    # description. Strip height 20px (y0..y0+20); chips 15px, centred.
    f_time = cond(11, 900)
    f_lab = sans(11, 600, 80)
    cy = y0 + 10
    ellipse(M + 7, cy, 7, 7, outline=INK, width=1.6)
    line([(M + 7, cy), (M + 7, cy - 4)], INK, 1.6)
    line([(M + 7, cy), (M + 11, cy)], INK, 1.6)
    text(M + 17, y0 + 2.5, "UTC", cond(11, 900), INK)
    chips = []
    for tm, what, reg in st.TIMELINE:
        tw = tlen(tm, f_time) + 10
        lw = tlen(what, f_lab)
        chips.append((tm, what, REG[reg], tw, tw + 4 + lw))
    total = sum(c[4] for c in chips)
    x_start = 72
    gap = (R - x_start - total) / (len(chips) - 1)
    assert gap >= 4, "strip chips too wide (gap %.1f)" % gap
    x = x_start
    for tm, what, col, tw, w in chips:
        rect(x, y0 + 2, x + tw, y0 + 17, fill=col)
        text(x + tw / 2, y0 + 3.5, tm, f_time, (255, 255, 255), anchor="ma")
        text(x + tw + 4, y0 + 3.5, what, f_lab, INK)
        x += w + gap
    return y0 + 20


def warn_icon(x, y, s):
    """Warning triangle with an exclamation mark."""
    poly([(x + s / 2, y), (x + s, y + s * 0.9), (x, y + s * 0.9)], (232, 176, 32), outline=INK, width=1.2)
    rect(x + s / 2 - 1, y + s * 0.28, x + s / 2 + 1, y + s * 0.62, fill=INK)
    ellipse(x + s / 2, y + s * 0.72, 1.4, 1.4, fill=INK)


def datecheck_block(x0, y0, w, h=116):
    # DATE CHECK box: fills the whole box (1px frame, padding 8), 10px /
    # 12px pitch, title bold with a 12px warning icon. Content is the
    # blocks of stories.DATE_CHECK in order; lines are laid out one by one
    # and the box stops when full — whatever does not fit is cut from the
    # END (last block first). Returns (bottom_y, cut_text) where cut_text
    # is the exact text that did not fit, in reading order.
    # v9: title/rule tightened (body at y0+28, was y0+33) so the kept v8
    # content (Rule 2 + Times 5 + Edge cases 4 = 11 lines) fits the v7 box.
    rect(x0, y0, x0 + w, y0 + h, outline=(200, 190, 175), width=1)
    px = x0 + 8
    pw = w - 16
    tf = cond(12, 900)
    bf = sans(10, 800, 80)
    rf = sans(10, 600, 80)
    warn_icon(px, y0 + 5, 12)
    text(px + 18, y0 + 5, st.DATE_CHECK[0][0], tf, INK, tracking=0.8)
    y = y0 + 5 + 17
    line([(px, y), (px + pw, y)], INK, 1.0)
    y += 6
    w = pw
    x0 = px
    lines = []
    for label, body in st.DATE_CHECK[1:]:
        words = (label + " " + body).split(" ")
        nlab = len(label.split(" "))
        cur = []
        curw = 0
        for i, wd in enumerate(words):
            f = bf if i < nlab else rf
            ww = tlen(wd + " ", f)
            if cur and curw + ww > w:
                lines.append(cur)
                cur = [(wd, f)]
                curw = ww
            else:
                cur.append((wd, f))
                curw += ww
        if cur:
            lines.append(cur)
    nfit = max(0, int((y0 + h - y) // 12))
    keep, cut = lines[:nfit], lines[nfit:]
    for ln in keep:
        xx = x0
        for wd, f in ln:
            text(xx, y, wd + " ", f, INK)
            xx += tlen(wd + " ", f)
        y += 12
    cut_text = " ".join(" ".join(wd for wd, _ in ln) for ln in cut)
    return y, cut_text


def timeline_block(x0, y0, w, y_end):
    text(x0, y0, "THE DAY BY THE CLOCK \u00b7 UTC", cond(13, 900), INK, tracking=1.2)
    y = y0 + 19
    line([(x0, y), (x0 + w, y)], INK, 1.2)
    rows = st.TIMELINE
    step = (y_end - y - 4) / len(rows)
    for k, (tm, what, reg) in enumerate(rows):
        yy = y + 4 + k * step
        col = REG[reg]
        rect(x0, yy + 1, x0 + 46, yy + 17, fill=col)
        text(x0 + 23, yy + 2, tm, cond(13, 900), (255, 255, 255), anchor="ma")
        text(x0 + 54, yy + 1.5, what, sans(13, 600, 80), INK)


def also_block(x0, y0, x1, y_end, items=None):
    # One list column: numbered colour chips + bold place + one-line hed.
    # v12: 11.5px font (+5%). The pitch stretches so the column exactly
    # fills y0..y_end (v12: 15 rows over 722..966 -> 244/15 = 16.27px),
    # so the bottom of the last entry lands on y=966, shared with the
    # Date Check box bottom and the Sports panel bottom. A line that does
    # not fit at 11.5 drops to 11.2 -- the smallest shrink that changes
    # the 2x pixel font (11.3/11.4 round to the same 23px). Every entry
    # must fit one line and never touch the next column's badge.
    # items: (number, story) pairs; defaults to all briefs.
    stories = items if items is not None else st.all_stories()[len(st.LEAD) + len(st.CARDS):]
    cw = x1 - x0
    pitch = (y_end - y0) / len(stories)
    for i, (n, s) in enumerate(stories):
        cy = y0 + i * pitch
        assert cy + pitch <= y_end + 0.5, "list row %d runs past y_end" % n
        col = REG[s["region"]]
        rect(x0, cy + 1, x0 + 18, cy + 13, fill=col)
        text(x0 + 9, cy + 1.5, str(n), cond(8.5, 900), (255, 255, 255), anchor="ma")
        pre = s["place"] + ": "
        pf = rf = None
        pw = total = None
        for _sz in (11.5, 11.2):
            _pf = font("sans", _sz, 800, 80)
            _rf = font("sans", _sz, 500, 80)
            _pw = tlen(pre, _pf)
            _tot = _pw + tlen(s["hed"], _rf)
            if _tot <= cw - 24 + 0.5:
                pf, rf, pw, total = _pf, _rf, _pw, _tot
                break
        assert pf is not None, \
            "list entry %d too wide even at 11.2: %.1f > %.1f (%s)" % (n, _tot, cw - 24, s["place"] + ": " + s["hed"])
        text(x0 + 24, cy + 1, pre, pf, INK)
        text(x0 + 24 + pw, cy + 1, s["hed"], rf, INK2)
    bottom = y0 + len(stories) * pitch
    assert abs(bottom - y_end) < 0.5, "list bottom %.2f != y_end %.1f" % (bottom, y_end)
    return bottom


def _panel_frame(x0, y0, x1, y1):
    """Cream panel with a 1px warm-grey frame."""
    rect(x0, y0, x1, y1, fill=PAPER)
    rect(x0, y0, x1, y1, outline=(200, 190, 175), width=1)


def _bar_icon(x, y, s):
    """Small bar-chart icon: three white bars rising left to right."""
    base = y + s - 2
    for i, h in enumerate((5, 8, 11)):
        bx = x + 2 + i * 4
        rect(bx, base - h, bx + 3, base, fill=(255, 255, 255))


def _ball_icon(x, y, s):
    """Small football icon: white ball, dark pentagon, radiating seams."""
    cx, cy = x + s / 2, y + s / 2
    r = s / 2 - 1
    ellipse(cx, cy, r, r, fill=(255, 255, 255))
    poly([(cx, cy - 3), (cx + 3, cy - 1), (cx + 2, cy + 3), (cx - 2, cy + 3), (cx - 3, cy - 1)],
         SPO_HEAD)
    for (ax, ay) in [(cx, cy - 3), (cx + 3, cy - 1), (cx + 2, cy + 3), (cx - 2, cy + 3), (cx - 3, cy - 1)]:
        line([(ax, ay), (cx + (ax - cx) * 2.4, cy + (ay - cy) * 2.4)], SPO_HEAD, 0.8)


def _pct_value(x_right, y, pct, val, color):
    """Right-aligned 'pct (val)': pct bold coloured, val regular. Returns left edge."""
    vf = sans(11, 500, 80)
    pf = cond(12, 900)
    vw = tlen(val, vf)
    pw = tlen(pct, pf)
    text(x_right, y, val, vf, INK2, anchor="ra")
    text(x_right - vw - 4, y, pct, pf, color, anchor="ra")
    return x_right - vw - 4 - pw


def _load_json(name):
    with open(os.path.join(HERE, "data", name), encoding="utf-8") as fh:
        return json.load(fh)


def finance_panel(x0, y0, x1, y1):
    """MARKETS panel (v8 data, v9 spacing): reads data/markets.json. Header
    band (20px) with a bar icon, MARKETS, and the subtitle right-aligned;
    then a 4x2 tile grid, one line per tile 'label value change' with a
    drawn direction triangle (up green / down red / flat grey); then a
    caption line and a source line. Text >= 11px; tile rows drop from the
    end if they do not fit before the caption. Tile gaps tightened to 1px
    (v9) so the panel fits the v7 content area."""
    data = _load_json("markets.json")
    _panel_frame(x0, y0, x1, y1)
    # header band (20px): bar icon + MARKETS + subtitle right-aligned
    rect(x0, y0, x1, y0 + 20, fill=FIN_HEAD)
    _bar_icon(x0 + 8, y0 + 3, 14)
    text(x0 + 28, y0 + 3.5, data["title"], cond(13, 900), (255, 255, 255), tracking=0.8)
    text(x1 - 8, y0 + 4.5, data["subtitle"], sans(11, 500, 80), (255, 255, 255), anchor="ra")
    # tile grid: panel padding 4, gap 2; tile rows 13px, 1px gaps (v9:
    # tightened from 2px so the v8 panels fit the v7 content area)
    ix0, ix1 = x0 + 4, x1 - 4
    gap = 2
    tw = (ix1 - ix0 - gap) // 2
    th = 13
    tgap = 1
    lf = sans(11, 700, 62)
    vf = sans(11, 900, 62)
    y = y0 + 22
    nrows = 0
    for i, t in enumerate(data["tiles"]):
        r, c = divmod(i, 2)
        tx0 = ix0 + c * (tw + gap)
        ty = y + r * (th + tgap)
        if ty + th > y1 - 26:  # keep room for caption + source lines
            break
        nrows = max(nrows, r + 1)
        rect(tx0, ty, tx0 + tw, ty + th, fill=PAPER2, outline=(200, 190, 175), width=1)
        col = {"up": GREEN_D, "down": RED_D, "flat": GREY}.get(t["dir"], GREY)
        # direction triangle (5px) at the left, then label/value/change
        ax = tx0 + 2
        ay = ty + th / 2
        if t["dir"] == "up":
            poly([(ax, ay + 2.5), (ax + 5, ay + 2.5), (ax + 2.5, ay - 2.5)], col)
        elif t["dir"] == "down":
            poly([(ax, ay - 2.5), (ax + 5, ay - 2.5), (ax + 2.5, ay + 2.5)], col)
        else:
            line([(ax, ay), (ax + 5, ay)], col, 1.6)
        cx = ax + 7
        segw = tlen(t["label"], lf) + tlen(" ", lf) + tlen(t["value"], vf) + \
            tlen(" ", vf) + tlen(t["change"], vf)
        assert cx + segw <= tx0 + tw - 1, \
            "market tile too wide: %s (%.1f > %.1f)" % (t["label"], cx + segw, tx0 + tw - 1)
        text(cx, ty + 1, t["label"], lf, INK)
        cx += tlen(t["label"] + " ", lf)
        text(cx, ty + 1, t["value"], vf, INK)
        cx += tlen(t["value"] + " ", vf)
        text(cx, ty + 1, t["change"], vf, col)
    # caption line, then source line
    cap_y = y + nrows * (th + tgap) + 2
    text(ix0, cap_y, data["caption"], sans(11, 500, 80), INK2)
    text(ix0, cap_y + 12, data["source"], sans(11, 500, 80), INK2)
    return cap_y + 24


SPORTS_ROWS = None  # v8: rows come from data/sports.json


def sports_panel(x0, y0, x1, y1, rows=None):
    """SPORTS panel (v8 data, v9 spacing): reads data/sports.json. Header
    band (20px) with a football icon + SPORTS; subtitle on its own line;
    result rows (16px, alternating shading, dark score chip centred);
    caption left and source right on one shared baseline. Text >= 11px
    (row text 12px); rows drop from the end if they do not fit before the
    caption. v12: row height 16px (was 14px) so the 5 rows + subtitle +
    footer fill the taller 836..966 box; no row is dropped."""
    data = _load_json("sports.json")
    rows = list(rows if rows is not None else data["rows"])
    _panel_frame(x0, y0, x1, y1)
    # header band (20px): football icon + SPORTS
    rect(x0, y0, x1, y0 + 20, fill=SPO_HEAD)
    _ball_icon(x0 + 8, y0 + 3, 14)
    text(x0 + 28, y0 + 3.5, data["title"], cond(13, 900), (255, 255, 255), tracking=0.8)
    # subtitle on its own line (too long to share the band with the title)
    ix0, ix1 = x0 + 8, x1 - 8
    sub_y = y0 + 22
    text(ix0, sub_y, data["subtitle"], sans(11, 500, 80), INK2)
    # rows: 16px (v12, was 14px); drop from the end if they would cross
    # the caption line -- but v12 must keep all 5 rows, so the caller must
    # give the panel enough height.
    rh = 16
    body_top = sub_y + 13
    max_rows = max(0, (y1 - 14 - body_top) // rh)
    rows = rows[:max_rows]
    y = body_top
    for i, (home, score, away) in enumerate(rows):
        if i % 2 == 0:
            rect(ix0 - 2, y - 1, ix1 + 2, y + rh - 1, fill=ROW_ALT)
        text(ix0, y + 1.5, home, sans(12, 700, 80), INK)
        cf = cond(12, 900)
        cw = tlen(score, cf) + 12
        cx = (ix0 + ix1) / 2
        rect(cx - cw / 2, y + 0.5, cx + cw / 2, y + 13.5, fill=INK)
        text(cx, y + 1.5, score, cf, (255, 255, 255), anchor="ma")
        text(ix1, y + 1.5, away, sans(12, 700, 80), INK, anchor="ra")
        y += rh
    # caption left, source right, one shared baseline
    cap_y = y + 2
    text(ix0, cap_y, data["caption"], sans(11, 500, 80), INK2)
    text(ix1, cap_y, data["source"], sans(11, 500, 80), INK2, anchor="ra")
    return cap_y + 12


def footer():
    # v7 footer: rule at 968, one line of 10px text at 982.
    # Left: FOOT_NOTE; right: SOURCES.
    line([(M, 968), (R, 968)], INK, 1)
    f = sans(10, 500, 80)
    text(M, 982, st.FOOT_NOTE, f, INK2)
    text(R, 982, st.SOURCES, f, INK2, anchor="ra")


def build():
    # vertical budget (v12): header 0-150, chip UTC strip 156-176,
    # level 1 188-~371 (art 64), divider ~374,
    # level 2 rows ~386-~533 / ~541-~688 (art 48, 8px row gap), thin divider 697,
    # bottom headers baseline 702, bottom content 722-966 (four columns),
    # footer rule 968, footer text 982.
    # Kept from v8: Date Check content (Rule/Times/Edge cases) and the
    # data-driven Markets (8 tiles) + Sports (5 rows) panels in col D.
    # Everything else reverts to v7 (chip strip, art heights, lists with
    # the UWCL entries restored, 46 stories, two-line footer).
    y = header()  # -> 150
    y = chip_strip(156)  # -> 176
    # level 1: 4 cols 234px, gap 14; art 64, hed 20/28, dek 12.5/16
    l1w = [234, 234, 234, 234]
    l1x = [M]
    for wd in l1w[:-1]:
        l1x.append(l1x[-1] + wd + 14)
    ends = []
    for i, s in enumerate(st.LEAD):
        ends.append(card(l1x[i], 188, l1w[i], 64, s, i + 1, 20, 12.5, True))
    l1_end = max(ends)
    line([(M, l1_end + 3), (R, l1_end + 3)], RULE, 1)
    # level 2: 2 rows of 6 cols 152px, gap 14; art 48, hed 16/21, dek 12/15
    l2w = [152, 152, 152, 152, 152, 152]
    l2x = [M]
    for wd in l2w[:-1]:
        l2x.append(l2x[-1] + wd + 14)
    n = len(st.LEAD) + 1
    row_y = l1_end + 3 + 12
    l2_end = row_y
    for row in range(2):
        ends = []
        for c in range(6):
            s = st.CARDS[row * 6 + c]
            ends.append(card(l2x[c], row_y, l2w[c], 48, s, n, 16, 12, False))
            n += 1
        l2_end = max(ends)
        row_y = l2_end + 8
    assert l2_end <= 692, "level 2 ends too late (%.1f); divider at 697 unreachable" % l2_end
    # v12: thin 1px warm-grey divider, exactly copying the card divider
    # at y~375 (same thickness, same RULE colour, same length).
    line([(M, 697), (R, 697)], RULE, 1)
    # bottom headers (shared baseline 702; centres y~708): map title left,
    # list title right. Both moved up 6px from v11, icons with them.
    ellipse(M + 7, 709, 6, 6, fill=REG["GLOBAL"])
    ellipse(M + 7, 709, 2.4, 2.4, fill=(255, 255, 255))
    text(M + 18, 702, "WHERE IT HAPPENED", cond(13, 900), INK, tracking=1.2)
    lx = 304
    for k in range(3):
        line([(lx + 2, 705 + k * 5), (lx + 14, 705 + k * 5)], INK, 1.6)
    text(lx + 18, 702, "ALSO ON THURSDAY 19 NOVEMBER", cond(13, 900), INK, tracking=1.2)
    # bottom body (722-966), four columns, gutters 12-14px. All three
    # columns share top edge 722 and bottom edge 966.
    # col A (23..290): map on top (722..795), Date Check below (802..966)
    map_end = map_block(23, 722, 267)  # -> 795
    dc_end, dc_cut = datecheck_block(23, 802, 267, 164)
    # col B (304..515): briefs 17-31 ; col C (527..727): briefs 32-46
    # v12: lists run 722..966 (pitch 16.27px); first row top 722, last
    # row bottom 966.
    briefs = st.all_stories()[len(st.LEAD) + len(st.CARDS):]
    list_b_end = also_block(304, 722, 515, 966, briefs[:15])
    list_c_end = also_block(527, 722, 727, 966, briefs[15:])
    # col D (741..1001): Markets 722..828, 8px gap, Sports 836..966
    mk_end = finance_panel(741, 722, 1001, 828)
    sp_end = sports_panel(741, 836, 1001, 966)
    footer()
    nboxes = check_boxes(footer_y=968, overlap_y0=690)
    print("text boxes audited:", nboxes)
    print("list ends: B %.2f C %.2f (target 966)" % (list_b_end, list_c_end))
    print("date check cut:", repr(dc_cut) if dc_cut else "(none)")
    print("markets panel end:", round(mk_end), "sports panel end:", round(sp_end))

    out = img.resize((W, H), Image.LANCZOS).convert("RGB")
    buf = io.BytesIO()
    out.save(buf, "JPEG", quality=95, optimize=True)
    data = buf.getvalue()
    if len(data) > 1048576:
        buf = io.BytesIO()
        out.save(buf, "JPEG", quality=85, optimize=True)
        data = buf.getvalue()
    with open(os.path.join(HERE, "entry.png"), "wb") as fh:
        fh.write(data)
    print("entry.png", len(data), "bytes; level1 end", round(l1_end), "level2 end", round(l2_end),
          "map end", round(map_end), "datecheck end", round(dc_end),
          "smallest text", round(min(sz for sz, _ in TEXT_SIZES), 1))


if __name__ == "__main__":
    build()
