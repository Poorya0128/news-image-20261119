"""Draws v13 entry.png: the world's news of Thursday 19 November 2026.

v13 keeps the v12 page (masthead, 4 leads, 12 picture cards, briefs,
map + DATE CHECK + footer) but:
  * the dedicated MARKETS and SPORTS panels are removed as sections;
    their items move into the bottom briefs list (numbered story briefs
    first, then MARKETS and SPORTS lines), so all 46 stories stay;
  * type is as large as the boxes allow and gaps are tightened.
Rev 2: the footer is thinned to a 1px rule + one 8px line (rule at
1002), and all reclaimed space goes to the bottom band (720-998).
Rev 5: the "HOW THIS PAGE WAS CHECKED" box is deleted and the
masthead spans the full width (~79px). Card headlines are fuller
summaries at ONE uniform size (2 lines max — candidate list, first
fit wins, never shrunk). Bottom band: tinted background, column
hairlines, and geometric icons (globe, list, chart, trophy, calendar)
drawn with Pillow shapes. Markets drops the ANT/Nasdaq tiles (they
duplicate card 5) for GTA VI launch items from the story data.
Rev 6 (user corrections to rev 5 — read carefully, each one fixes a
misread order):
  * FONT SPLIT: the page is Merriweather serif again (masthead,
    leads, cards, headers, region bar, UTC strip). ONLY the small
    texts are Archivo (sans): briefs, Date Check body, markets/sports
    lines, footer. Rev 5 wrongly switched the whole page to Archivo.
  * NO whole-band tint. Instead the briefs get ZEBRA striping
    (alternating rows, faint tint) in columns B and C; column D keeps
    clean row separation with hairline dividers.
  * SPORTS: the trophy icon is gone. Each team gets its REAL logo
    (assets/logos/*.png) in a uniform white chip next to its name —
    both logos in every row. Same chip system for the MARKETS logos.
  * DATE CHECK: redone tidy like rank-1 (red border, red header,
    tidy rows, red bold section labels, hairlines between sections).
    NO rainbow colours, NO section tints, NO coloured bars.
  * BRIEFS BIGGER: uniform 15px (was 13px), Archivo wdth 75; texts
    trimmed to fit, never shrunk. Column D rows at the same 15px.
  * MARKETS: the six major instruments only (S&P 500, Dow, VIX,
    Brent, WTI, Gold) — the GTA tiles are gone (they duplicated card
    16) and the caption drops the GTA reference. Real logos in chips.
  * Card headlines: fuller summaries at ONE uniform size, Merriweather
    15px (the full wordings only fit at 15px — Merriweather's width
    axis stops at 87, so 17-18px cannot hold them in 2 lines; the
    user allowed slightly smaller type for the full meaning).
  * Bottom tables follow rank-1's colour model: colour used
    purposefully and sparingly — dark section headers, coloured
    number badges (region colours), icons, real logos, one red accent
    (Date Check) — never full background tints.
Rev 7 (user orders):
  * SOURCE BADGES: every source label (leads + cards) sits in its
    own filled box in SRC_BADGE dark teal (12,96,100) — a colour
    used nowhere else on the page. Leads 10px, cards 9px (the card
    label row is narrower; 9px keeps every rev 6 topic).
  * STATUS BOXES: ONE colour for all 12 — STATUS_COLOR deep
    magenta (176,22,130), also used nowhere else. CLAIMED vs
    CONFIRMED is told by the word, not the colour.
  * SMALL-TEXT FONT: Archivo is replaced by Inter (Inter-VF.ttf,
    axes [optical size, weight]; optical size always 14). Inter is
    much wider than condensed Archivo (worst brief 229px at 13px
    Inter vs 197.7px at 15px Archivo-75 in the same 208px column),
    so the uniform brief size is re-derived at 12px Inter — the
    largest size fitting all 30 briefs + all market/sport rows
    without gutting the wording. The number chip shrinks 20->18px
    (text at +22) so the two widest briefs still fit at 12px.
  * MARKETS header moves UP to the shared bottom-band header
    baseline (same level as ALSO ON); the gained row becomes a
    dedicated GOLD row (LBMA logo — rev 8 corrected the World
    Gold Council logo; "$3,625" from the data, rev 10 — Kitco
    source right-aligned, no invented figure).
  * SPORTS header gets a small soccer-ball icon (Pillow shapes),
    same 13px size/style as the MARKETS chart icon. No trophy.
  * Sports rows: [home logo] Home Score Away [away logo] — the
    away logo moves to the RIGHT of the away name.
  * Section headers (MARKETS at head_y, SPORTS in the panel) are
    Merriweather 15px bold like the other bottom headers — headers
    are page type, not small text.
Rev 8 (user orders):
  * FOOTER: rewritten rank-1 style — one precise sentence (date
    rule + attribution + the real sources), 2 lines at 10px Inter
    BOLD (split A, measured: 895px + 549px in 980px). The old
    right-aligned sources line is merged into the sentence.
  * STATUS BOXES: the rev 7 magenta is GONE. CONFIRMED = pale
    green fill + dark green text; CLAIMED = pale orange fill +
    dark orange text. The fills are light and the texts dark, and
    neither fill collides with a saturated region colour (AFRICA
    green / MIDDLE EAST orange). The word still distinguishes them.
  * DATE CHECK: restructured as a tidy rank-1-style list of small
    OUTLINE-BOX chips (order 9): each item gets its own outline
    box in its story's region colour (text stays dark on paper),
    items are ordered so no two adjacent items share a colour
    (verified: NONE), and the whole box fits — nothing hidden.
    Content is condensed from the 7 old entries (Times section
    dropped — its facts are on the UTC strip / card 16's dek;
    Brasileirão, Fatah-3, Yunus, Sanon and the Markets note cut).
    Rule is one short header line. A date is shown only when it
    is NOT 19 Nov; a bare time means 19 Nov.
  * LEADS GET STATUS BOXES TOO: all 4 leads are CONFIRMED (none
    of their deks starts with "Claim:") — a status box sits below
    each lead's dek, same green scheme as the cards. Lead art
    64->56 and card art 52->48 pay for the +20px the boxes cost.
  * UTC STRIP: each entry's TITLE now takes the SAME colour as its
    time chip (was ink); title weight 600->700 so the colours
    (esp. LATIN AMERICA gold) stay readable on the paper.
  * VIX: +16.5% was wrong — the tile now says +15.8% (user's
    figure; data/markets.json updated).
  * GOLD LOGO: the World Gold Council logo is replaced by the
    LBMA logo (assets/logos/mkt_gold_lbma.png); DOW LOGO: the
    "D" (news publisher) is replaced by S&P Dow Jones Indices
    (assets/logos/mkt_dow_spdji.png). Both verified visually by
    the logo agent before use.
Rev 10 (user orders + Second Check + user corrections):
  * DATE CHECK: back to the rev 7 SECTION format (chips gone) —
    red-bordered box, red header, six labelled sections as
    flowing text, but TIDIED: red bold labels inline, Times as
    one item per line with the time right-aligned, 5px gaps
    between sections, 8px Inter at 12px pitch (16 lines total
    after the Second Check cuts; at 9px it needs 21). Content is
    st.DC_DISPLAY, the tidied presentation of the verbatim
    st.DATE_CHECK source data (condensations listed in stories.py).
  * The "30" count at the right end of the ALSO ON header is
    deleted (no replacement).
  * Second Check: Lead 2 ICJ hed/dek reworded; UTC strip entries
    00:04/13:05 replaced by 00:30 Australia jobless / 13:30 US
    jobless claims; cards 7/12/14 reworded; briefs 23/26/27/28/
    32/34/36/37/40/42/44 reworded (brief 28 exact user wording
    "Mars: Perseverance, Odyssey pause science" at 9.5px —
    BRIEF_SIZE_OVERRIDE; brief 32 "DC:" prefix, "bid" dropped);
    brief 30 Cincinnati/Fiona DELETED, replaced by Congo Ebola
    (AFRICA 6->7, NORTH AMERICA 9->8); Date Check drops Raoni
    ordinance (Not yet), Ebola/China drone controls/PAHO measles
    (Left out); Gold $3,625; S&P 500 logo = S&P Dow Jones
    Indices (reused mkt_dow_spdji.png); WTI label "WTI (Dec)";
    sports caption gains "· Thu 19 Nov local time".
  * Uniform brief size 12 -> 11px; card headlines 15 -> 12.5px;
    UTC strip titles 11 -> 10px (time chips stay 11px).

Run:  python build.py   (Pillow only, no network)
Writes entry.png (1024x1024, <= 1 MiB) next to this file.
The page is drawn at 2x and reduced for clean edges. Deterministic:
no random, no timestamps, so two runs are byte-identical.
"""
import io
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

import stories as st

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
S = 2
W = H = 1024
M = 22
R = W - M

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 234)
PAPER2 = (238, 232, 219)
INK = (26, 27, 36)
INK2 = (72, 72, 82)
GREY = (120, 118, 112)
RULE = (190, 184, 170)
NAVY = (30, 44, 86)
BRICK = (170, 58, 44)
OCHRE = (222, 160, 52)
TEAL = (30, 122, 126)
CREAM = (248, 240, 222)
OUT = (36, 38, 56)
GREEN_D = (16, 90, 55)      # market gainers
RED_D = (150, 25, 25)       # market losers
FIN_HEAD = (18, 84, 48)     # markets section colour
SPO_HEAD = (22, 48, 96)     # sports section colour
# Rev 7: the source badges use SRC_BADGE dark teal (12,96,100) — a
# colour appearing NOWHERE else on the page (verified by exact-match
# scan of the rev 6 entry.png and of every logo file, 0 occurrences).
SRC_BADGE = (12, 96, 100)   # dark teal — source badges (leads+cards)
# Rev 8 (user order, REPLACES the rev 7 magenta): status boxes are
# pale fill + dark text, one scheme per status. CONFIRMED = pale
# green fill + dark green text; CLAIMED = pale orange fill + dark
# orange text. The fills are LIGHT (clearly distinct from the
# saturated region colours AFRICA green (28,126,70) and MIDDLE EAST
# orange (198,96,20) — verified by exact-match scan: neither fill
# appears anywhere in the rev 7 entry.png or any logo file) and the
# texts are DARK (readable on the pale fills). The word still
# distinguishes CLAIMED from CONFIRMED.
CONFIRMED_FILL = (212, 240, 218)   # pale green
CONFIRMED_TEXT = (11, 77, 44)      # dark green
CLAIMED_FILL = (252, 230, 206)     # pale orange
CLAIMED_TEXT = (150, 74, 8)        # dark orange
# (Region colours are purples/blues/reds/greens/golds; Date Check
# red is (170,58,44); market green/red are (16,90,55)/(150,25,25);
# TEAL (30,122,126) is defined but never drawn; the source-badge
# teal (12,96,100) is used only for the source badges.)

REG = {
    "ASIA": (122, 62, 168), "MIDDLE EAST": (198, 96, 20), "EUROPE": (36, 84, 166),
    "AFRICA": (28, 126, 70), "NORTH AMERICA": (188, 40, 40), "LATIN AMERICA": (196, 140, 20),
    "GLOBAL": (80, 88, 100),
}

# Rev 7 (uniform type, font split): ONE size for every brief line
# (columns B, C and D — markets and sports lines included) and ONE
# size for all 12 card headlines. No per-line ladders. A line that
# does not fit at the uniform size is trimmed in BRIEF_TRIMS (words
# cut, facts kept), never shrunk.
#   * Briefs: 11px Inter, optical size 14. Rev 10: the uniform
#     size drops 12 -> 11 to fit the longer Second Check wordings
#     (briefs 26/32/40/42/44; see BRIEF_TRIMS). MEASURED: at
#     11px the worst trimmed brief is 209.7px in the 212px
#     available (chip 18px, text at +22). Brief 28 is the one
#     exception (BRIEF_SIZE_OVERRIDE) — its exact user wording
#     only fits at <=9.8px. Inter's open letterforms and large
#     x-height read clearer than condensed Archivo at 15px
#     despite the smaller nominal size (verified by eye at 2x
#     and at 512px).
#   * Card headlines: 12.5px Merriweather, wdth 87 — rev 10
#     drops 15 -> 12.5 so the longer C2/C3 wordings (card 7,
#     card 12) fit 2 lines in 158px. MEASURED: cards 7 and 12
#     are 3 lines at 15/14/13px and fit 2 lines at 12.5px;
#     all 12 headlines fit 2 lines at 12.5px, wght 900.
BRIEF_SIZE = 11

# Rev 10: ONE exception to the uniform brief size. Brief 28 MUST
# read exactly "Mars: Perseverance, Odyssey pause science" (user
# correction — "Mars: pause science" is ambiguous). That line is
# 237.6px at 11px against 212.5px available, and even 10px is
# 216.0px — it only fits at <=9.8px. Dropping the uniform size
# to 9.8px for all 30 briefs + the Markets/Sports lines would
# gut legibility everywhere (the user has complained about small
# text twice), so this one line renders at 9.5px (205.2px, 7.3px
# slack) and everything else stays at 11px. The difference is
# one line among 30; the wording is exact.
# Rev 10 fix round: briefs 26, 32, 42, 44 also carry exact user
# wording that only fits below the 11px uniform size, so they get
# per-line overrides too (measured with the build's own tlen/AF:
# 26 = 208.3px at 9.5; 32 = 208.2px at 10; 44 = 208.4px at 10;
# 42 = 217.1px at 9.5 and only fits at 9.0px, 205.7px — the single
# line below 9.5, kept because the exact wording is the point of
# the fix and no word may be trimmed).
BRIEF_SIZE_OVERRIDE = {28: 9.5, 26: 9.5, 32: 10, 42: 9.0, 44: 10}
BRIEF_WDTH = 75  # kept for call-site compatibility; Inter has no
# width axis, so AF() ignores it (see afont).
CARD_HED_SIZE = 12.5
CARD_HED_WGHT = 900
CARD_HED_WDTH = 87
BRIEF_TRIMS = {
    17: ("Crimea", "Bridge hit; Ukraine confirms"),
    18: ("Shenzhen", "Putin vows 'painful' reply"),
    21: ("Yemen", "Houthis: 15 killed (CLAIM)"),
    22: ("Argentina", "Disability law 71-0"),
    # Rev 10: brief 23 reads exactly "Brazil: Raoni's birthplace"
    # (user correction — the 362,243 ha figure is dropped).
    23: ("Brazil", "Raoni's birthplace"),
    24: ("Indonesia", "forfeiture law passed"),
    25: ("Seoul", "Kim Keon-hee term finalised"),
    # Rev 10 (B5): the checker wording "Storm floods roads,
    # burn-scar alerts lifted" — exact, rendered at 9.5px
    # (BRIEF_SIZE_OVERRIDE, 208.3px); no word dropped.
    26: ("LA", "Storm floods roads, burn-scar alerts lifted"),
    # Rev 10 (B6): "Florida: Floods; Guard deployed".
    27: ("Florida", "Floods; Guard deployed"),
    # Rev 10 (user correction): exact wording "Mars: Perseverance,
    # Odyssey pause science" — rendered at 9.5px, see
    # BRIEF_SIZE_OVERRIDE (237.6px at 11px, cannot fit at 11px).
    28: ("Mars", "Perseverance, Odyssey pause science"),
    29: ("Senate", "Iran bid fails 48–51"),
    # Rev 10 (C6): the exact wording "Washington: DOJ withdraws
    # Venezuela TPS stay bid" is 263.6px at 11px and 229.1px even
    # with the "DC:" prefix — so the prefix is shortened to "DC:"
    # and the line renders at 10px (BRIEF_SIZE_OVERRIDE, 208.2px).
    # "bid" is kept: it is a bid for a stay, not the stay itself.
    32: ("DC", "DOJ withdraws Venezuela TPS stay bid"),
    # Rev 10 (C7): "Kenya: picks US group for Mrima Hill".
    34: ("Kenya", "picks US group for Mrima Hill"),
    # Rev 10 (B1): "Nigeria: signs Yutong CNG bus deal" (no plant
    # opened; a bus deal was signed).
    36: ("Nigeria", "signs Yutong CNG bus deal"),
    # Rev 10 (C8): "Nigeria: reviews row with S. Africa" (the row
    # started 17 Nov; rewording as given, not deleted).
    37: ("Nigeria", "reviews row with S. Africa"),
    38: ("Pakistan", "22 killed (CLAIM)"),
    # Rev 10 (C9): "Pakistan: extends ban on Indian aircraft".
    40: ("Pakistan", "extends ban on Indian aircraft"),
    41: ("Copenhagen", "MPs back Greenland"),
    # Rev 10 (B7): the checker wording "France: Greens' chief
    # opens door to Mélenchon" — exact, rendered at 9.0px
    # (BRIEF_SIZE_OVERRIDE, 205.7px); no rewording.
    42: ("France", "Greens' chief opens door to Mélenchon"),
    # Rev 10 (B8): the checker wording "Japan: Takaichi, Putin
    # agree to keep talking" — exact, rendered at 10px
    # (BRIEF_SIZE_OVERRIDE, 208.4px); "keep" kept.
    44: ("Japan", "Takaichi, Putin agree to keep talking"),
}

# ------------------------------------------------------------------ fonts
# Rev 7 font split (user order): the page is Merriweather serif —
# masthead, leads, cards, headers, region bar, UTC strip. ONLY the
# small texts are Inter (sans, clearer at small sizes): briefs,
# Date Check body, markets/sports lines, footer. Rev 6 used Archivo
# for the small texts; the user found it unclear, so Inter replaces
# it. Inter variable axes: [optical size, weight] — NO italic file
# and NO width axis. Optical size is always 14 (its small-size
# optimum); `italic` and `wdth` are accepted for call-site
# compatibility and ignored.
_cache = {}


def font(italic, size, wght=900, wdth=87):
    """Merriweather (serif) — the page font."""
    key = ("M", italic, size, wght, wdth)
    if key in _cache:
        return _cache[key]
    path = "Merriweather-Italic-VF.ttf" if italic else "Merriweather-VF.ttf"
    f = ImageFont.truetype(os.path.join(FONTS, path), round(size * S))
    f.set_variation_by_axes([wght, wdth, 18])
    _cache[key] = f
    return f


def afont(italic, size, wght=900, wdth=87):
    """Inter (sans) — small texts only. Optical size 14, weight as
    requested; italic/width arguments are ignored (no such axes)."""
    key = ("I", size, wght)
    if key in _cache:
        return _cache[key]
    f = ImageFont.truetype(os.path.join(FONTS, "Inter-VF.ttf"), round(size * S))
    f.set_variation_by_axes([14, wght])
    _cache[key] = f
    return f


def F(size, wght=900, wdth=87):
    return font(False, size, wght, wdth)


def FI(size, wght=600, wdth=87):
    return font(True, size, wght, wdth)


def AF(size, wght=900, wdth=87):
    return afont(False, size, wght, wdth)


def AFI(size, wght=600, wdth=87):
    return afont(True, size, wght, wdth)


# ---------------------------------------------------------------- drawing
img = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(img)
OX = OY = 0


def p(x, y):
    return (round((x - OX) * S), round((y - OY) * S))


def clipped(fn, x, y, w, h, *args):
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


def line(pts, fill, width=1):
    d.line([p(*q) for q in pts], fill=fill, width=max(1, round(width * S)), joint="curve")


def poly(pts, fill, outline=None, width=2):
    d.polygon([p(*q) for q in pts], fill=fill, outline=outline,
              width=round(width * S) if outline else 1)


def ellipse(cx, cy, rx, ry, fill=None, outline=None, width=1):
    d.ellipse([p(cx - rx, cy - ry), p(cx + rx, cy + ry)], fill=fill,
              outline=outline, width=round(width * S))


def mix(a, b, t):
    return tuple(round(a[k] + (b[k] - a[k]) * t) for k in range(3))


def tlen(s, f, tracking=0):
    return f.getlength(s) / S + tracking * max(0, len(s) - 1)


TEXT_SIZES = []
TEXT_BOXES = []
# Photo rectangles in final (1024) coordinates, recorded by
# paste_photo; the final image's photo regions are quantized to 256
# colours after the downscale (see build()).
PHOTO_RECTS = []


def _text_box(x, y, s, f, anchor, tracking=0):
    bb = d.textbbox(p(x, y), s, font=f, anchor=anchor)
    x0, y0, x1, y1 = bb[0] / S, bb[1] / S, bb[2] / S, bb[3] / S
    if tracking:
        extra = tracking * max(0, len(s) - 1)
        if anchor[0] == "l":
            x1 += extra
        elif anchor[0] == "r":
            x0 -= extra
        else:
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


def check_boxes(footer_y=1002):
    # Full-page audit: every text box inside the page, none crossing
    # or touching the footer rule, and NO pairwise overlap anywhere
    # on the page (not just below y=690 — rev 3 only checked the
    # bottom band and missed the masthead/lead overlaps).
    boxes = TEXT_BOXES
    for (x0, y0, x1, y1), s in boxes:
        assert 0 <= x0 and x1 <= W and 0 <= y0 and y1 <= H, \
            "text outside page: %r (%.1f,%.1f)-(%.1f,%.1f)" % (s, x0, y0, x1, y1)
        assert not (y0 < footer_y < y1), \
            "text crosses footer rule: %r (%.1f,%.1f)-(%.1f,%.1f)" % (s, x0, y0, x1, y1)
        assert abs(y1 - footer_y) > 1 and abs(y0 - footer_y) > 1, \
            "text touches footer rule: %r (%.1f,%.1f)-(%.1f,%.1f)" % (s, x0, y0, x1, y1)
    for i in range(len(boxes)):
        (ax0, ay0, ax1, ay1), sa = boxes[i]
        for j in range(i + 1, len(boxes)):
            (bx0, by0, bx1, by1), sb = boxes[j]
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


def fit_size(s, sizes, maxw, wght=900, wdth=87, italic=False):
    """Largest size in `sizes` whose text fits maxw on one line (or None)."""
    for sz in sizes:
        if tlen(s, font(italic, sz, wght, wdth)) <= maxw:
            return sz
    return None


def fit_lines(s, sizes, maxw, maxlines, wght=900, wdth=87, italic=False):
    """Largest size in `sizes` whose text wraps to <= maxlines lines."""
    for sz in sizes:
        if len(wrap(s, font(italic, sz, wght, wdth), maxw)) <= maxlines:
            return sz
    return None


# --------------------------------------------------------------- geo data
WORLD = json.load(open(os.path.join(HERE, "data", "world.json")))


# ------------------------------------------------------------ illustrations
PHOTO = {"peace": "01", "hague": "02", "pif": "03", "kyiv": "04",
         "ant": "05", "cop31": "06", "dhaka_fire": "07", "akvan": "08",
         "tanker": "09", "gaza_return": "10", "talks": "11", "cost48": "12",
         "shield": "13", "strike": "14", "marathon": "15", "gta": "16"}
_photo_cache = {}


def paste_photo(x, y, w, h, num):
    """Centre-crop assets/cards/NN.png to fill the (w, h) art slot."""
    if num not in _photo_cache:
        _photo_cache[num] = Image.open(
            os.path.join(HERE, "assets", "cards", num + ".png")).convert("RGB")
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
    # The source is downscaled ~5x to the slot, so quantizing the
    # resized crop is visually near-lossless at this size — but it
    # cuts ~25 KB from the PNG, which is what keeps the file under
    # the 1 MiB limit. The source file is never modified.
    # 56 colours (not 256): the bigger type in rev 3
    # pushes the file over 1 MiB at 256; 64 keeps it under while the
    # illustrations still read clean at display size (verified by eye
    # against 256 — banding is negligible at 158-237px wide).
    # Dither NONE: Floyd-Steinberg dithering adds high-frequency noise
    # that compresses poorly; at this downscale it is invisible.
    im = im.quantize(colors=128, method=Image.Quantize.MEDIANCUT,
                     dither=Image.Dither.NONE).convert("RGB")
    img.paste(im, (round(x * S), round(y * S)))
    PHOTO_RECTS.append((x, y, w, h))


def pin(cx, cy, num, col, r=7.5):
    ellipse(cx, cy, r + 1.3, r + 1.3, fill=(255, 255, 255))
    ellipse(cx, cy, r, r, fill=col)
    s = str(num)
    fs = r * (1.5 if len(s) == 1 else 1.45)
    text(cx, cy + 0.4, s, F(fs, 900), (255, 255, 255), anchor="mm")


# ------------------------------------------------------------------- logos
# Real logos (assets/logos/*.png, RGBA with transparency) pasted in a
# UNIFORM chip system so they read as one matching set:
#   * every logo is shown at the SAME display height (LOGO_H),
#     centred inside its chip, scaled to fit (contain — never
#     stretched, aspect ratio preserved);
#   * every chip has the SAME style: white fill, thin light border,
#     3px corner radius, same height (LOGO_H + 2*LOGO_PAD) and the
#     same padding. Chip WIDTH follows the logo's aspect — a wide
#     wordmark (WTI, S&P 500) needs a wider chip than a shield;
#     forcing every chip square would shrink the wide wordmarks to
#     an unreadable sliver, so width follows aspect while height,
#     padding, border and radius stay identical for sports and
#     markets alike.
# Logos are drawn on the 2x canvas (LANCZOS, pasted with their own
# alpha as mask) and are NOT touched by the photo quantization at
# the end, so their brand colours stay exact.
LOGO_H = 14
LOGO_PAD = 2
LOGO_BORDER = (205, 195, 180)
_logo_cache = {}


def load_logo(name):
    if name not in _logo_cache:
        _logo_cache[name] = Image.open(
            os.path.join(HERE, "assets", "logos", name + ".png")).convert("RGBA")
    return _logo_cache[name]


def logo_chip(x, y, name):
    """Paste logo `name` in its uniform chip at (x, y). Returns the
    chip width (height is always LOGO_H + 2*LOGO_PAD)."""
    im = load_logo(name)
    iw, ih = im.size
    lw = LOGO_H * iw / ih
    cw = lw + 2 * LOGO_PAD
    ch = LOGO_H + 2 * LOGO_PAD
    x0, y0 = p(x, y)
    x1, y1 = p(x + cw, y + ch)
    d.rounded_rectangle([(x0, y0), (x1 - 1, y1 - 1)], radius=round(3 * S),
                        fill=(255, 255, 255), outline=LOGO_BORDER,
                        width=max(1, round(1 * S)))
    li = im.resize((round(lw * S), round(LOGO_H * S)), Image.LANCZOS)
    img.paste(li, (round((x + LOGO_PAD) * S), round((y + LOGO_PAD) * S)), li)
    return cw


# Sports: full name in sports.json -> (short name shown, logo file).
TEAM = {
    "Vasco da Gama": ("Vasco", "vasco"),
    "Internacional": ("Inter", "internacional"),
    "Vitória": ("Vitória", "vitoria"),
    "Bragantino": ("Bragantino", "bragantino"),
    "São Paulo": ("São Paulo", "saopaulo"),
    "Fluminense": ("Fluminense", "fluminense"),
    "Orlando City": ("Orlando", "orlando"),
    "Cincinnati": ("Cincinnati", "cincinnati"),
    "Seattle": ("Seattle", "seattle"),
    "Real Salt Lake": ("RSL", "rsl"),
}

# Markets: tile label -> logo file.
# Rev 8: Gold uses the LBMA logo (mkt_gold_lbma.png — the World Gold
# Council logo was wrong, WGC does not set prices) and Dow uses the
# S&P Dow Jones Indices logo (mkt_dow_spdji.png — the old "D" was the
# Dow Jones news publisher, not the index administrator). Both files
# were downloaded from Wikipedia/Wikimedia Commons and verified
# visually on a contact sheet by the logo agent before use.
# Rev 10 (D2): the S&P 500 tile ALSO uses the S&P Dow Jones Indices
# logo (mkt_dow_spdji.png — S&P DJI administers the S&P 500, not
# S&P Global); the file is reused, nothing new downloaded.
# Rev 10 (D3): the WTI tile label is "WTI (Dec)" (December contract)
# — the key must match data/markets.json exactly.
MKT_LOGO = {
    "S&P 500": "mkt_dow_spdji",
    "Dow": "mkt_dow_spdji",
    "VIX": "mkt_vix",
    "Brent": "mkt_brent",
    "WTI (Dec)": "mkt_wti",
    "Gold": "mkt_gold_lbma",
}


def src_badge(x_right, y_center, src, size, height, pad):
    """Draw a source label in its own filled box (SRC_BADGE dark
    teal), right-anchored at x_right, vertically centred on
    y_center. Text is Merriweather bold, white, centred in the box.
    Returns the badge's left edge. The box colour is independent —
    it appears nowhere else on the page (verified by scan)."""
    bf = F(size, 700)
    tw = tlen(src, bf, 0.5)
    bw = tw + pad
    bx0 = x_right - bw
    top = y_center - height / 2
    rect(bx0, top, x_right, top + height, fill=SRC_BADGE)
    asc, desc = (v / S for v in bf.getmetrics())
    th = asc + desc
    text((bx0 + x_right) / 2, top + (height - th) / 2, src, bf,
         (255, 255, 255), anchor="ma", tracking=0.5)
    return bx0


# ------------------------------------------------------------------ page
def header():
    # top bar 0-6, kicker y=14, masthead, subtitle, region bar.
    # Rev 5: the "HOW THIS PAGE WAS CHECKED" box is DELETED, so the
    # masthead spans the full width. Rev 6: back to Merriweather —
    # largest size fitting M..R at wdth 87 (the axis minimum), ~78px.
    # Baseline/subtitle/region bar are placed from the real font
    # metrics so the masthead's descenders ('y') clear the subtitle
    # and the masthead top clears the kicker.
    rect(0, 0, W, 6, fill=INK)
    kf = F(12, 800)
    text(M, 14, "THE DAY IN WORLD NEWS", kf, REG["MIDDLE EAST"], tracking=1.2)
    text(R, 14, "%d STORIES \u00b7 7 REGIONS \u00b7 ONE DAY" % st.count(), kf, INK2,
         anchor="ra", tracking=1.2)
    title = "Thursday 19 November 2026"
    best = None
    for sz in range(95, 50, -1):
        tf = F(sz, 900, 87)
        w = tlen(title, tf, -0.01 * sz)
        if w <= R - M:
            best = (sz, tf, w)
            break
    sz, tf, w = best
    asc, desc = (v / S for v in tf.getmetrics())
    baseline = round(14 + 12 + 2 + asc)  # kicker bottom + 2px + ascent
    ty = round(baseline - asc)
    text(M, ty, title, tf, INK, tracking=-0.01 * sz)
    sub_y = round(baseline + desc + 4)
    text(M, sub_y, st.JUDGE_NOTE, FI(17, 600), INK2)
    # region bar: 20px, equal segments, 2px gaps, 12px bold
    y = sub_y + 24
    counts = {}
    for _, s in st.all_stories():
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    regs = [r for r in st.REGIONS if counts.get(r)]
    bw = (R - M) / len(regs)
    bf = F(12, 900)
    x = M
    for r in regs:
        rect(x, y, x + bw - 2, y + 20, fill=REG[r])
        text(x + bw / 2 - 1, y + 3.5, "%s %d" % (r, counts[r]), bf, (255, 255, 255),
             anchor="ma", tracking=0.8)
        x += bw
    print("masthead size: %d (width %.1f); baseline %d; subtitle y %d; region bar %d" % (
        sz, w, baseline, sub_y, y))
    return y + 20


def chip_strip(y0):
    # clock icon + "UTC", then 7 chips spread evenly M..R. 20px tall.
    # Rev 8 (user order): each entry's TITLE takes the SAME colour
    # as its time chip (was ink) — the colour covers both the time
    # and the title. Title weight 600->700 so the colours (esp.
    # LATIN AMERICA gold) stay readable on the paper.
    f_time = F(11, 900)
    # Rev 10 (C1): the new strip titles ("Australia jobless 4.9%",
    # "US jobless claims 203k") total 933.8px at 11px — gap -0.6px.
    # Titles drop to 10px (time chips stay 11px): total 875.3px,
    # gap 9.1px. MEASURED.
    # Rev 11: strip rebuilt as real events only — the 7 chips in
    # st.TIMELINE with full labels total 891.1px at 10px, gap 6.3px.
    # MEASURED. No shortening needed.
    f_lab = F(10, 700)
    cy = y0 + 10
    ellipse(M + 7, cy, 7, 7, outline=INK, width=1.6)
    line([(M + 7, cy), (M + 7, cy - 4)], INK, 1.6)
    line([(M + 7, cy), (M + 11, cy)], INK, 1.6)
    text(M + 17, y0 + 2.5, "UTC", F(11, 900), INK)
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
        text(x + tw + 4, y0 + 3.5, what, f_lab, col)
        x += w + gap
    return y0 + 20


# Cards 5-16: deks deleted; the headline is a fuller summary of the
# main news that carries the COMPLETE meaning (hed + dek facts), at
# ONE uniform size (CARD_HED_SIZE, 2 lines max). Status comes from
# the story's own dek: "Claim: ..." -> CLAIMED, everything else ->
# CONFIRMED. Every card's status goes in a filled box (pale fill +
# dark text, rev 8 — never plain text, never the region colour).
# Rev 6: Merriweather 15px — the only size holding all 12 full
# wordings in 2 lines (measured: 17px holds 5/12, 18px 2/12).
# Rev 10: CARD_HED_SIZE drops to 12.5px — the longer C2/C3
# wordings (card 7, card 12) are 3 lines at 15/14/13px and fit
# 2 lines at 12.5px; all 12 fit at 12.5px, wght 900. MEASURED.
# Card 7 keeps the full meaning: "Two ruling-party members killed
# on eve of shutdown" (2 killed + ruling-party members + eve of
# shutdown, not during the lockdown).
NEW_HED_CANDS = {
    5: ["Anthropic +17% on debut; Nasdaq -2.3%"],
    6: ["COP31 drops fossil text; 80 of 144"],
    7: ["Two ruling-party members killed on eve of shutdown"],
    8: ["Odisha evacuates 299,000 before landfall"],
    9: ["Iran: 2 tankers hit mines; 4m+ barrels"],
    10: ["Gaza raid ends; families return to camp"],
    11: ["Kushner: Russia OK with NATO-like deal"],
    12: ["Iran war cost $48.3bn, Pentagon estimate, 13 Nov"],
    13: ["EU: first AI-assisted cyberattack"],
    14: ["Tax-bill strike: 55,000 out, 285 protest actions"],
    15: ["Champion Jepchirchir banned 3 yrs, EPO"],
    16: ["GTA VI out at midnight ET; NZ opened 11:00"],
}


def pick_hed(num):
    hf = F(CARD_HED_SIZE, CARD_HED_WGHT, CARD_HED_WDTH)
    for cand in NEW_HED_CANDS[num]:
        if len(wrap(cand, hf, 158)) <= 2:
            return cand
    raise AssertionError("card %d: no headline fits 2 lines: %r" % (
        num, NEW_HED_CANDS[num]))


def card(x, y, w, art_h, s, num, hsize, dsize, lead):
    col = REG[s["region"]]
    rect(x, y, x + w, y + 3, fill=col)
    paste_photo(x, y + 3, w, art_h, PHOTO[s["art"]])
    agap = 5 if lead else 4
    yy = y + 3 + art_h + agap
    if lead:
        pin(x + 8, yy + 7, num, col, r=8)
        kf = F(11, 800)
        text(x + 21, yy, s["region"] + " \u00b7 " + s["beat"], kf, col, tracking=0.6)
        # Rev 7: the source sits in its own dark-teal box (10px
        # text, 14px box, centred on the pin). Measured: worst lead
        # (GLOBAL · GENOCIDE RULING + UN NEWS) clears by 5.1px.
        src_badge(x + w, yy + 7, s["src"], 10, 14, 8)
    else:
        pin(x + 7, yy + 7, num, col, r=7)
        tf = F(10, 800)
        lab = s["topic"]
        # Rev 7: the source is a 9px dark-teal badge (6px padding),
        # so the clearance math uses the BADGE width, not the plain
        # text width. Fit order (keeps every rev 6 topic): full
        # label at tracking 0.38, then at tracking 0, then the
        # region-only label (split at " · ") at 0.38, then at 0;
        # characters are trimmed only as a last resort (never
        # reached in practice). The label starts at x+19 (pin gap
        # 5px) so card 16 ("NORTH AMERICA" + ROCKSTAR badge) fits:
        # 19+81.4+56.2 = 156.6 against the 157 limit.
        bw = tlen(s["src"], F(9, 700), 0.5) + 6
        lab = s["topic"]
        trk = 0.38
        lw = tlen(lab, tf, trk)
        if 19 + lw + bw > w - 1:
            trk = 0.0
            lw = tlen(lab, tf, trk)
        if 19 + lw + bw > w - 1:
            lab = lab.split(" \u00b7 ")[0]
            trk = 0.38
            lw = tlen(lab, tf, trk)
            if 19 + lw + bw > w - 1:
                trk = 0.0
                lw = tlen(lab, tf, trk)
        while lab and 19 + lw + bw > w - 1:
            lab = lab[:-1]
            lw = tlen(lab, tf, trk)
        text(x + 19, yy, lab, tf, col, tracking=trk)
        src_badge(x + w, yy + 7, s["src"], 9, 12, 6)
    yy += 17 if lead else 15
    if lead:
        hed = s["hed"]
        # Leads use the condensed cut (wdth 87): at 21.5px the
        # headlines and at 12.5px the deks each wrap to exactly 2
        # lines in 237px (measured).
        hf = F(hsize, 900, 87)
        hlines = wrap(hed, hf, w)
        assert len(hlines) <= 2, "lead %d headline needs %d lines: %r" % (num, len(hlines), hed)
        hlead = round(hsize * 1.36)
        for ln in hlines:
            text(x, yy, ln, hf, INK)
            yy += hlead
        yy += 3
        df = F(dsize, 500, 87)
        dlines = wrap(s["dek"], df, w)
        assert len(dlines) <= 2, "lead %d dek needs %d lines: %r" % (num, len(dlines), s["dek"])
        dlead = round(dsize * 1.38)
        for ln in dlines:
            text(x, yy, ln, df, INK2)
            yy += dlead
        # Rev 8 (user order): the 4 leads carry a status box too,
        # below the dek, in the same scheme as the cards (pale green
        # fill + dark green text for CONFIRMED, pale orange + dark
        # orange for CLAIMED). Same rule as the cards (dek starts
        # with "Claim:" -> CLAIMED, else CONFIRMED); all 4 lead deks
        # fail the Claim test, so all 4 leads are CONFIRMED.
        yy += 4
        status = "CLAIMED" if s["dek"].startswith("Claim:") else "CONFIRMED"
        fill, tcol = status_colors(status)
        sf = F(10, 900)
        box_w = tlen(status, sf) + 12
        rect(x, yy, x + box_w, yy + 16, fill=fill)
        text(x + box_w / 2, yy + 2.5, status, sf, tcol, anchor="ma")
        yy += 16
        return yy
    # picture cards: fuller headline at ONE uniform size (15px
    # Merriweather, 2 lines max — first fitting candidate wins),
    # then a filled status box. Rev 8: pale fill + dark text —
    # CONFIRMED is pale green + dark green, CLAIMED is pale orange
    # + dark orange (the rev 7 magenta is gone). The word tells
    # CLAIMED from CONFIRMED; the fill is light so it never reads
    # as a region colour.
    hed = pick_hed(num)
    hf = F(CARD_HED_SIZE, CARD_HED_WGHT, CARD_HED_WDTH)
    hlines = wrap(hed, hf, w)
    assert len(hlines) <= 2, "card %d headline needs %d lines at %spx: %r" % (
        num, len(hlines), CARD_HED_SIZE, hed)
    hlead = round(CARD_HED_SIZE * 1.28)
    for ln in hlines:
        text(x, yy, ln, hf, INK)
        yy += hlead
    yy += 4
    status = "CLAIMED" if s["dek"].startswith("Claim:") else "CONFIRMED"
    fill, tcol = status_colors(status)
    sf = F(10, 900)
    box_w = tlen(status, sf) + 12
    rect(x, yy, x + box_w, yy + 16, fill=fill)
    text(x + box_w / 2, yy + 2.5, status, sf, tcol, anchor="ma")
    yy += 16
    return yy


def status_colors(status):
    """(fill, text) for a status box (rev 8): pale fill + dark text."""
    if status == "CLAIMED":
        return CLAIMED_FILL, CLAIMED_TEXT
    return CONFIRMED_FILL, CONFIRMED_TEXT

def map_block(x0, y0, w):
    # map image only (header drawn by build); height ~68, 1px warm-grey frame
    # Rev 8: lat range 57/-40 (was 60/-45) — 6px shorter, so the
    # Date Check below gets 6px more. Copenhagen (55.68) and Kyiv
    # (50.4) pins sit at the top edge and are clamped with leader
    # lines, as the code already handles.
    # Rev 11: lat range 55/-38 — 3px shorter still, so the Date
    # Check (now 9px) gets 3px more. Only Copenhagen (55.68) newly
    # clamps at the top edge, and it already used a leader line;
    # pins still relax to >= 19.0px apart (measured).
    my = y0
    lat0, lat1 = 55.0, -38.0
    h = round(w * (lat0 - lat1) / 360)
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
    # Spread pins so no two touch: pin outer radius is r+1.3 = 7.8,
    # so centres need >= 19px apart (7.8*2 + ~3.4px gap). The old
    # 15px target was SMALLER than the 17px pin diameter, which is
    # why the Europe/ME cluster overlapped. Iterate to convergence
    # (early exit once nothing moves).
    PIN_R = 6.5
    PIN_MIN = 19.0
    for _ in range(2000):
        moved = False
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                dx, dy = pos[j][0] - pos[i][0], pos[j][1] - pos[i][1]
                dist = math.hypot(dx, dy) or 0.01
                if dist < PIN_MIN:
                    push = (PIN_MIN - dist) / 2
                    ux, uy = dx / dist, dy / dist
                    pos[i][0] -= ux * push; pos[i][1] -= uy * push
                    pos[j][0] += ux * push; pos[j][1] += uy * push
                    moved = True
        for q in pos:
            q[0] = min(x0 + w - 8, max(x0 + 8, q[0]))
            q[1] = min(my + h - 8, max(my + 8, q[1]))
        if not moved:
            break
    min_pin_dist = min(
        math.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1])
        for i in range(len(pos)) for j in range(i + 1, len(pos)))
    assert min_pin_dist >= PIN_MIN - 0.5, \
        "pins still too close: min centre distance %.1fpx" % min_pin_dist
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
        pin(cx, cy, n, REG[s["region"]], r=PIN_R)
    return my + h, min_pin_dist


def warn_icon(x, y, s):
    poly([(x + s / 2, y), (x + s, y + s * 0.9), (x, y + s * 0.9)], (232, 176, 32),
         outline=INK, width=1.2)
    rect(x + s / 2 - 1, y + s * 0.28, x + s / 2 + 1, y + s * 0.62, fill=INK)
    ellipse(x + s / 2, y + s * 0.72, 1.4, 1.4, fill=INK)


# ------------------------------------------------------------------- icons
# Geometric icons drawn with Pillow shapes only (no emoji, no assets).
# Each takes the top-left corner, a size s, and a colour.
def icon_globe(x, y, s, col):
    # circle + vertical meridian + equator line
    ellipse(x + s / 2, y + s / 2, s / 2, s / 2, outline=col, width=1.5)
    ellipse(x + s / 2, y + s / 2, s * 0.2, s / 2, outline=col, width=1.0)
    line([(x + 1, y + s / 2), (x + s - 1, y + s / 2)], col, 1.0)


def icon_list(x, y, s, col):
    # 3 rows: small square + rule
    for k in range(3):
        yy = y + k * (s / 3) + 0.5
        rect(x, yy, x + 3, yy + 3, fill=col)
        line([(x + 5, yy + 1.5), (x + s, yy + 1.5)], col, 1.6)


def icon_chart(x, y, s, col):
    # 3 ascending bars + baseline
    bw = (s - 3) / 3
    for k, h in enumerate((0.45, 0.7, 1.0)):
        bx = x + k * (bw + 1.5)
        rect(bx, y + s - h * s, bx + bw, y + s, fill=col)
    line([(x, y + s + 1), (x + s, y + s + 1)], col, 1.2)


def icon_calendar(x, y, s, col):
    # outline + top strip + two ring ticks + check
    rect(x + 1, y + 2, x + s - 1, y + s, outline=col, width=1.4)
    rect(x + 1, y + 2, x + s - 1, y + 2 + s * 0.28, fill=col)
    line([(x + s * 0.3, y), (x + s * 0.3, y + 3)], col, 1.4)
    line([(x + s * 0.7, y), (x + s * 0.7, y + 3)], col, 1.4)
    line([(x + s * 0.28, y + s * 0.62), (x + s * 0.45, y + s * 0.78),
          (x + s * 0.75, y + s * 0.45)], col, 1.4)


def icon_ball(x, y, s, col):
    # Simple soccer ball, same 13px size and clean style as the
    # MARKETS chart icon (rev 7): circle outline, small filled
    # centre pentagon, five short seams radiating to the edge. No
    # trophy, no big emblem — just a neat ball mark for the SPORTS
    # header.
    cx, cy, r = x + s / 2, y + s / 2, s / 2
    ellipse(cx, cy, r, r, outline=col, width=1.4)
    pr = s * 0.20
    pts = []
    for k in range(5):
        a = math.radians(-90 + k * 72)
        pts.append((cx + pr * math.cos(a), cy + pr * math.sin(a)))
    poly(pts, fill=col)
    for k in range(5):
        a = math.radians(-90 + k * 72)
        line([(cx + pr * math.cos(a), cy + pr * math.sin(a)),
              (cx + (r - 1) * math.cos(a), cy + (r - 1) * math.sin(a))],
             col, 1.2)


# Date Check, rev 10: back to the rev 7 SECTION format at the user's
# order — red-bordered box, red Merriweather header, then labelled
# sections (Rule / Times / Edge cases / Left out / Not yet /
# Markets) as flowing text — but TIDIED so a reader can scan it at
# a glance: red bold section labels inline, Times as one item per
# line with the time right-aligned, 5px gaps between sections, 9px
# Inter at 13px pitch. Rev 11 (user order): the body font grows
# 8px -> 9px. 10px does not fit without gutting the content (19
# lines at 10px need ~300px in a ~242px box; the map can only
# give ~15px), so 9px is the largest size that fits with every
# fact intact — 16 lines after the rev 11 condensations (Times
# items shortened, Edge/Markets tightened), measured. The rev 7
# flaw (only 13 of 32 lines shown) is fixed by construction: the
# renderer asserts the whole block ends inside the box. Content
# comes from st.DC_DISPLAY (the tidied presentation of the
# verbatim st.DATE_CHECK source data).
# The box stretches from below the map to y=995 (aligned with the
# brief columns); pitch 13 + gaps 2 fill it with 4px slack.
DC_RED = (170, 58, 44)
DC_FONT = 9      # Inter, small texts
DC_PITCH = 13    # 9px Inter is 11.5 tall; 1.5px leading
DC_GAP = 2       # gap between sections


def datecheck_block(x0, y0, w, h=164):
    rect(x0, y0, x0 + w, y0 + h, outline=DC_RED, width=1.5)
    px = x0 + 8
    pw = w - 16
    # header: red calendar icon + red Merriweather caps header.
    icon_calendar(px, y0 + 4, 12, DC_RED)
    ht = "DATE CHECK \u00b7 Thu 19 Nov 2026"
    hf = None
    for sz in (13, 12, 11):
        f = F(sz, 900)
        if tlen(ht, f, 0.8) <= pw - 15:
            hf = f
            break
    assert hf is not None, "date check header too wide: %r" % ht
    text(px + 15, y0 + 4, ht, hf, DC_RED, tracking=0.8)
    y = y0 + 20
    bf = AF(DC_FONT, 500)   # body
    lf = AF(DC_FONT, 800)   # section labels, red bold
    tf = AF(DC_FONT, 700)   # right-aligned times, bold ink
    nlines = [0]

    def wrap_first(body, first_w):
        # Greedy word wrap; first line max first_w, rest max pw.
        words = body.split()
        lines = []
        cur = ""
        avail = first_w
        for w_ in words:
            t = (cur + " " + w_).strip()
            if tlen(t, bf) <= avail or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w_
                avail = pw
        if cur:
            lines.append(cur)
        return lines

    def para(label, body):
        # Red bold label inline + flowing wrapped body.
        nonlocal y
        lw = tlen(label, lf)
        lines = wrap_first(body, pw - lw - 4)
        for i, ln in enumerate(lines):
            assert tlen(ln, bf) <= pw + 0.5, \
                "date check line too wide: %r" % ln
            if i == 0:
                text(px, y, label, lf, DC_RED)
                text(px + lw + 4, y, ln, bf, INK)
            else:
                text(px, y, ln, bf, INK)
            y += DC_PITCH
            nlines[0] += 1

    def timed(label, items):
        # One item per line; the time right-aligned, bold ink.
        # The label sits on the first item's line.
        nonlocal y
        lw = tlen(label, lf)
        for k, (item, right) in enumerate(items):
            x = px
            if k == 0:
                text(px, y, label, lf, DC_RED)
                x = px + lw + 4
            if right is None:
                w_ = text(x, y, item, bf, INK)
                assert x + w_ <= px + pw + 0.5, \
                    "date check timed item too wide: %r" % item
            else:
                rw = tlen(right, tf)
                w_ = text(x, y, item, bf, INK)
                assert x + w_ + 8 + rw <= px + pw + 0.5, \
                    "date check timed item too wide: %r" % item
                text(px + pw, y, right, tf, INK, anchor="ra")
            y += DC_PITCH
            nlines[0] += 1

    for i, (label, kind, payload) in enumerate(st.DC_DISPLAY):
        if i:
            y += DC_GAP
        if kind == "para":
            para(label, payload)
        else:
            timed(label, payload)
    # end of the last line's text: last line top + font height.
    asc, desc = (v / S for v in bf.getmetrics())
    end_y = y - DC_PITCH + asc + desc
    assert end_y <= y0 + h + 0.5, \
        "date check overflows box by %.1fpx (%d lines)" % (
            end_y - (y0 + h), nlines[0])
    return end_y, nlines[0]


ZEBRA = (240, 234, 222)  # faint warm tint for alternating brief rows


def also_block(x0, y0, x1, y_end, items):
    # One numbered-brief column: colour number chip + bold place + hed.
    # ONE uniform size (BRIEF_SIZE, Inter) for every line: lines
    # that do not fit are trimmed in BRIEF_TRIMS (words cut, facts
    # kept), never shrunk — with exceptions in BRIEF_SIZE_OVERRIDE
    # for lines whose exact user wording only fits smaller (briefs
    # 26, 28, 32, 42, 44).
    # Pitch stretches to fill y0..y_end.
    # ZEBRA striping (rev 6, rank-1 colour model): alternating rows
    # get a faint background tint so the rows read apart — no full
    # band tint, just one-in-two rows. The number chip (region
    # colour) is the coloured badge; the zebra is the row separator.
    # Rev 7: the chip is 18px wide (was 20) and the text starts at
    # +22 (was +26) — the 4px this frees is what lets the two
    # widest briefs fit at 12px Inter (211.5px in 212px available).
    cw = x1 - x0
    pitch = (y_end - y0) / len(items)
    sizes_used = []
    for i, (n, s) in enumerate(items):
        cy = y0 + i * pitch
        assert cy + pitch <= y_end + 0.5, "list row %d runs past y_end" % n
        if i % 2 == 0:
            rect(x0, cy, x1, cy + pitch, fill=ZEBRA)
        col = REG[s["region"]]
        rect(x0, cy + 1, x0 + 18, cy + 15, fill=col)
        text(x0 + 9, cy + 2, str(n), AF(9.5, 900), (255, 255, 255), anchor="ma")
        place, hed = BRIEF_TRIMS.get(n, (s["place"], s["hed"]))
        pre = place + ": "
        sz = BRIEF_SIZE_OVERRIDE.get(n, BRIEF_SIZE)
        pf = AF(sz, 800, BRIEF_WDTH)
        rf = AF(sz, 500, BRIEF_WDTH)
        assert tlen(pre, pf) + tlen(hed, rf) <= cw - 22 + 0.5, \
            "brief %d too wide at %spx: %s" % (n, sz, pre + hed)
        sizes_used.append(sz)
        text(x0 + 22, cy + 1, pre, pf, INK)
        text(x0 + 22 + tlen(pre, pf), cy + 1, hed, rf, INK2)
    return y0 + len(items) * pitch, sizes_used


def panel_lines(x0, y0, x1, y_end):
    # Column D: the former MARKETS and SPORTS panels, now plain brief
    # lines (no panel frame, no header band). ALL rows at ONE uniform
    # size (BRIEF_SIZE, Inter) — market lines, sport lines and
    # captions alike; no per-line fallback.
    # Rev 6: every market tile and every team gets its REAL logo in
    # the uniform white chip (logo_chip), one chip before each label
    # and before each team name — both logos in every sports row.
    # The trophy icon is gone. Rows are separated by hairline
    # dividers (no tint).
    # Rev 7: (a) the MARKETS header no longer consumes a row here —
    # it sits at the shared bottom-band header baseline in build(),
    # at the same level as ALSO ON. The row it frees becomes a
    # dedicated GOLD row: Gold leaves the tiles and gets its own
    # fuller standalone row (World Gold Council logo, value from
    # the data, Kitco source right-aligned — no invented figure).
    # (b) The SPORTS header is Merriweather 15px bold like the other
    # bottom headers, with a small soccer-ball icon (no trophy).
    # Rev 10 (B9): the sports caption carries "· Thu 19 Nov local
    # time" (all 5 games played Thursday local time, ended 20 Nov
    # UTC); it wraps to 2 lines and the pitch absorbs the extra row.
    # (c) Sports rows read [home logo] Home Score Away [away logo]:
    # the away logo sits to the RIGHT of the away name.
    mk = json.load(open(os.path.join(HERE, "data", "markets.json")))
    sp = json.load(open(os.path.join(HERE, "data", "sports.json")))
    gold_tile = next(t for t in mk["tiles"] if t["label"] == "Gold")
    rows = []  # (kind, payload); captions pre-wrapped to display lines
    for t in mk["tiles"]:
        if t["label"] == "Gold":
            continue  # gold gets its own dedicated row, below
        rows.append(("mkt", t))
    rows.append(("gold", gold_tile))
    capf = AF(BRIEF_SIZE, 500, BRIEF_WDTH)
    for ln in wrap(mk["caption"], capf, x1 - x0):
        rows.append(("cap", ln))
    rows.append(("head", ("SPORTS", SPO_HEAD)))
    for h, sc, a in sp["rows"]:
        rows.append(("spo", (h, sc, a)))
    for ln in wrap(sp["caption"], capf, x1 - x0):
        rows.append(("cap", ln))
    pitch = (y_end - y0) / len(rows)
    cw = x1 - x0
    for i, (kind, payload) in enumerate(rows):
        cy = y0 + i * pitch
        assert cy + pitch <= y_end + 0.5, "panel row %d runs past y_end" % i
        if kind == "head":
            label, col = payload
            icon_ball(x0, cy + 1, 13, col)
            text(x0 + 17, cy + 1, label, F(15, 900), col, tracking=1.0)
        elif kind == "cap":
            f = AF(BRIEF_SIZE, 500, BRIEF_WDTH)
            assert tlen(payload, f) <= cw + 0.5, "caption too wide: %r" % payload
            text(x0, cy + 1, payload, f, INK2)
        elif kind == "mkt":
            t = payload
            col = {"up": GREEN_D, "down": RED_D, "flat": GREY}.get(t["dir"], GREY)
            lf = AF(BRIEF_SIZE, 800, BRIEF_WDTH)
            vf = AF(BRIEF_SIZE, 900, BRIEF_WDTH)
            xx = x0 + logo_chip(x0, cy + 1, MKT_LOGO[t["label"]]) + 4
            text(xx, cy + 1, t["label"], lf, INK)
            xx += tlen(t["label"] + " ", lf)
            if t["value"]:
                text(xx, cy + 1, t["value"], vf, INK)
                xx += tlen(t["value"] + " ", vf)
            if t["change"]:
                text(xx, cy + 1, t["change"], vf, col)
            assert xx <= x1 + 0.5, "market line too wide: %r" % t["label"]
        elif kind == "gold":
            # Dedicated GOLD row: logo chip + label + value from the
            # data ("$3,625", rev 10) + the Kitco source right-aligned.
            # The value is the data's own — nothing invented.
            t = payload
            lf = AF(BRIEF_SIZE, 800, BRIEF_WDTH)
            vf = AF(BRIEF_SIZE, 900, BRIEF_WDTH)
            xx = x0 + logo_chip(x0, cy + 1, MKT_LOGO["Gold"]) + 4
            text(xx, cy + 1, "Gold", lf, INK)
            xx += tlen("Gold ", lf)
            text(xx, cy + 1, t["value"], vf, INK)
            text(x1, cy + 1, "Kitco", AF(BRIEF_SIZE, 600, BRIEF_WDTH), GREY,
                 anchor="ra")
            assert xx + tlen(t["value"], vf) <= x1 - tlen("Kitco", AF(BRIEF_SIZE, 600, BRIEF_WDTH)) - 4, \
                "gold row too wide: %r" % t["value"]
        elif kind == "spo":
            h, sc, a = payload
            lf = AF(BRIEF_SIZE, 800, BRIEF_WDTH)
            sf = AF(BRIEF_SIZE, 900, BRIEF_WDTH)
            h_short, h_logo = TEAM[h]
            a_short, a_logo = TEAM[a]
            xx = x0 + logo_chip(x0, cy + 1, h_logo) + 4
            text(xx, cy + 1, h_short, lf, INK)
            xx += tlen(h_short + " ", lf)
            text(xx, cy + 1, sc, sf, INK)
            xx += tlen(sc + " ", sf)
            text(xx, cy + 1, a_short, lf, INK)
            xx += tlen(a_short, lf) + 4
            xx += logo_chip(xx, cy + 1, a_logo)
            assert xx <= x1 + 0.5, "sport line too wide: %r" % (h + " " + sc + " " + a)
        # hairline divider under every row except the last: clean row
        # separation for column D (no tint).
        if i < len(rows) - 1:
            line([(x0, cy + pitch - 1), (x1, cy + pitch - 1)], RULE, 0.7)
    return y0 + len(rows) * pitch, len(rows)


def footer():
    # Rev 8 (rank-1 style): one precise sentence in TWO lines at
    # 10px Inter BOLD (split A, measured: 895px + 549px in 980px).
    # Rule at 997, lines at 1000 and 1011 (pitch 11); the band ends
    # at 995. The old right-aligned sources line is merged into the
    # sentence (its markets tail is line 2's ending).
    line([(M, 997), (R, 997)], INK, 1)
    f = AF(10, 800)
    for i, ln in enumerate(st.FOOTER_LINES):
        assert tlen(ln, f) <= R - M + 0.5, "footer line %d too wide: %r" % (i, ln)
        text(M, 1000 + i * 11, ln, f, INK2)


def build():
    # vertical budget (v13 rev 8): header 0-~165 (masthead ~78px
    # Merriweather, full width), chip strip +4, leads ~192-~406 (hed
    # 21.5, dek 12.5, wdth 87, art 56, status box 16), card rows
    # ~417-~669 (uniform 15px Merriweather headlines, 2 lines +
    # status box, art 48), divider/body placed dynamically from
    # l2_end so the freed space flows to the bottom band (body
    # ~693-995), footer rule 997, footer text 1000 + 1011 (10px
    # Inter bold, 2 lines, ~1023).
    y = header()
    y = chip_strip(y + 4)
    # level 1: 4 cols 237px, gap 10; art 56 (rev 8: was 64 — the
    # 8px pays for the status box below each lead's dek), hed
    # 21.5/29, dek 12.5/17, status box 16.
    l1w = [237, 237, 237, 237]
    l1x = [M]
    for wd in l1w[:-1]:
        l1x.append(l1x[-1] + wd + 10)
    ends = []
    for i, s in enumerate(st.LEAD):
        ends.append(card(l1x[i], y + 4, l1w[i], 56, s, i + 1, 21.5, 12.5, True))
    l1_end = max(ends)
    line([(M, l1_end + 3), (R, l1_end + 3)], RULE, 1)
    # level 2: 2 rows of 6 cols 158px, gap 6; art 48 (rev 8: was
    # 52 — the 4px per row helps pay for the lead status boxes),
    # uniform 15px Merriweather headline (2 lines) + status box,
    # no dek. The hsize/dsize args are ignored for picture cards
    # (size is the uniform constant).
    l2w = [158, 158, 158, 158, 158, 158]
    l2x = [M]
    for wd in l2w[:-1]:
        l2x.append(l2x[-1] + wd + 6)
    n = len(st.LEAD) + 1
    row_y = l1_end + 3 + 8
    l2_end = row_y
    for row in range(2):
        ends = []
        for c in range(6):
            s = st.CARDS[row * 6 + c]
            ends.append(card(l2x[c], row_y, l2w[c], 48, s, n, 15, 12.5, False))
            n += 1
        l2_end = max(ends)
        row_y = l2_end + 4
    assert l2_end <= 692, "level 2 ends too late (%.1f)" % l2_end
    # bottom band placed dynamically from l2_end: divider +5, headers
    # +6, body +24 (rev 8: was +26 — the map's top pins and their
    # white outlines still clear the 15px section headers: pin tops
    # sit at body_y+0.2 against the header text bottom at
    # l2_end+21, i.e. ~1.2px clear).
    div_y = l2_end + 5
    head_y = l2_end + 6
    body_y = l2_end + 24
    line([(M, div_y), (R, div_y)], RULE, 1)
    # Rev 6: NO whole-band tint (rev 5's tint is gone — the user
    # called it out). The band reads as clean paper; the columns are
    # separated by hairlines, the briefs by zebra striping, and the
    # colour comes from headers, badges and logos only (rank-1 model).
    for hx in (293, 535, 775):
        line([(hx, body_y), (hx, 995)], RULE, 1)
    # bottom headers (shared baseline head_y), each with an icon.
    icon_globe(M, head_y + 1, 14, INK)
    text(M + 19, head_y, "WHERE IT HAPPENED", F(15, 900), INK, tracking=1.2)
    lx = 298
    icon_list(lx, head_y + 1, 14, INK)
    text(lx + 19, head_y, "ALSO ON THURSDAY 19 NOVEMBER", F(15, 900), INK, tracking=1.2)
    # Rev 7: MARKETS header at the shared bottom-band header
    # baseline — the SAME level as ALSO ON — with the chart icon
    # and the markets subtitle right-aligned. The row it used to
    # occupy inside the panel is freed for the dedicated GOLD row.
    mk_sub = json.load(open(os.path.join(HERE, "data", "markets.json")))["subtitle"]
    icon_chart(778, head_y + 1, 13, FIN_HEAD)
    text(778 + 17, head_y, "MARKETS", F(15, 900), FIN_HEAD, tracking=1.0)
    # Subtitle at 9px Inter: at 10px it is 132.5px wide and overlaps
    # the MARKETS header (which ends at 875.0); at 9px it starts at
    # ~881.7, clearing by ~6.7px.
    text(1001, head_y, mk_sub, AF(9, 600), GREY, anchor="ra")
    # bottom body body_y-995:
    # col A (23..288): map, then Date Check
    map_end, pin_min = map_block(23, body_y, 265)
    dc_end, dc_lines = datecheck_block(23, map_end + 4, 265, 995 - (map_end + 4))
    # cols B (298..532) + C (538..772): briefs 17-31 / 32-46
    briefs = st.all_stories()[len(st.LEAD) + len(st.CARDS):]
    list_b_end, sizes_b = also_block(298, body_y, 532, 995, briefs[:15])
    list_c_end, sizes_c = also_block(538, body_y, 772, 995, briefs[15:])
    # col D (778..1001): markets + sports as plain brief lines.
    # Ends at 993 so the last caption's descender clears the footer
    # rule at 997.
    panel_end, panel_rows = panel_lines(778, body_y, 1001, 993)
    footer()
    nboxes = check_boxes(footer_y=997)
    print("text boxes audited:", nboxes)
    print("body_y %.1f div_y %.1f head_y %.1f" % (body_y, div_y, head_y))
    print("small-text font: Inter (opsz 14); uniform brief size: %s (B %s, C %s, panel %s)" % (
        BRIEF_SIZE, sorted(set(sizes_b)), sorted(set(sizes_c)), BRIEF_SIZE))
    print("source badge colour: %s (dark teal); status: CONFIRMED fill %s text %s / CLAIMED fill %s text %s" % (
        SRC_BADGE, CONFIRMED_FILL, CONFIRMED_TEXT, CLAIMED_FILL, CLAIMED_TEXT))
    print("uniform card headline size: %s (wght %s, wdth %s)" % (
        CARD_HED_SIZE, CARD_HED_WGHT, CARD_HED_WDTH))
    print("card headlines:", {n: pick_hed(n) for n in range(5, 17)})
    print("card status:", {n: ("CLAIMED" if st.CARDS[n - 5]["dek"].startswith("Claim:") else "CONFIRMED") for n in range(5, 17)})
    print("lead status:", {n: ("CLAIMED" if st.LEAD[n - 1]["dek"].startswith("Claim:") else "CONFIRMED") for n in range(1, 5)})
    print("map pins: min centre distance %.1fpx (need >= 18.5)" % pin_min)
    print("list ends: B %.2f C %.2f panel %.2f (target 995)" % (list_b_end, list_c_end, panel_end))
    print("date check: %d lines, ends %.1f (box height %.1f) — nothing cut" % (
        dc_lines, dc_end, 995 - (map_end + 4)))
    print("panel rows:", panel_rows)
    print("map end", round(map_end), "datecheck end", round(dc_end))
    print("smallest text", round(min(sz for sz, _ in TEXT_SIZES), 1))

    out = img.resize((W, H), Image.LANCZOS).convert("RGB")
    # Quantize each photo region at final resolution. The 2x quantize
    # in paste_photo is mostly undone by the LANCZOS downscale (it
    # re-blends neighbouring colours), so the real saving comes from
    # re-quantizing here, at the exact display size. The rectangles
    # contain only the illustrations — badges, labels and headlines
    # sit below them — so no text is touched. Deterministic
    # (MEDIANCUT), so byte-identical runs are preserved.
    for (px, py, pw, ph) in PHOTO_RECTS:
        region = out.crop((round(px), round(py), round(px + pw), round(py + ph)))
        out.paste(region.quantize(colors=128,
                                  method=Image.Quantize.MEDIANCUT,
                                  dither=Image.Dither.NONE).convert("RGB"),
                  (round(px), round(py)))
    # The world map too (56 colours): its sea/land are flat, so the
    # palette keeps them exactly; only the antialiased coastline
    # edges lose a few shades. Start 4px below the map top so the
    # "WHERE IT HAPPENED" header text (whose baseline sits ~2px
    # below the map's top edge) is never touched.
    mx0, my0 = 23, round(body_y) + 4
    mx1, my1 = 288, round(map_end)
    region = out.crop((mx0, my0, mx1, my1))
    out.paste(region.quantize(colors=56,
                              method=Image.Quantize.MEDIANCUT,
                              dither=Image.Dither.NONE).convert("RGB"),
              (mx0, my0))
    buf = io.BytesIO()
    # compress_level=9 plus 56-colour photo/map quantization: the
    # bigger type in rev 3 pushes the file over 1 MiB at
    # the default level 6 / 256 colours; level 9 + 56 colours buys it back.
    out.save(buf, "PNG", optimize=True, compress_level=9)
    data = buf.getvalue()
    with open(os.path.join(HERE, "entry.png"), "wb") as fh:
        fh.write(data)
    print("entry.png", len(data), "bytes; level1 end", round(l1_end), "level2 end", round(l2_end))


if __name__ == "__main__":
    build()
