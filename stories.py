"""The stories of Thursday 19 November 2026.

Layout: 4 lead cards, 12 picture cards, and a numbered "Also on" list.
Every story has a number; the same number marks it on the map.
Each card names its region, its beat and its source.

Dates: every item happened, or was first reported, on 19 November 2026 in
some time zone. The Suneung exam began 23:40 UTC on the 18th, but the
flight halt (04:05 UTC) and the exam day itself are 19 November; the
Kyiv missile attack at 01:25 local on the 20th is 23:25 UTC on the 19th.

Count note: the brief lists 29 briefs (4+12+29=45), one short of the
46 the region counts sum to. The UWCL brief ("Arsenal 0-2 Lyon,
Barça 6-0") holds two distinct match results, so it is split into two
briefs here, giving 30 briefs and 46 stories. Region counts on the
page are the actual counts of the stories as assigned: ASIA 9,
MIDDLE EAST 6, EUROPE 6, AFRICA 6, NORTH AMERICA 11, LATIN AMERICA 3,
GLOBAL 5 = 46. (Card 16 was the Suneung exam, ASIA; v4 replaces it
with the GTA VI launch, NORTH AMERICA. Suneung is still referenced in
the UTC strip and the Date Check edge case.)

v8 (REVISION 3): the two UWCL briefs (London Arsenal 0-2 Lyon and
Barcelona 6-0, both filed GLOBAL) move out of the "Also on" list and
into the Sports panel. That leaves 28 briefs and 44 stories.
Recomputed from the data: ASIA 9, MIDDLE EAST 6, EUROPE 6, AFRICA 6,
NORTH AMERICA 11, LATIN AMERICA 3, GLOBAL 3 = 44. (The two removed
briefs are filed GLOBAL in this file, not EUROPE; the header and
region bar are computed from the data, so they show GLOBAL 3.)

v9: the two UWCL briefs are RESTORED to the "Also on" list (the user
ordered the v7 list back), so they now appear BOTH in the list AND in
the Sports panel (data/sports.json). 30 briefs, 46 stories: ASIA 9,
MIDDLE EAST 6, EUROPE 6, AFRICA 6, NORTH AMERICA 11, LATIN AMERICA 3,
GLOBAL 5 = 46. The Date Check (Rule/Times/Edge cases) and the
data-driven Markets/Sports panels are kept from v8; everything else
(timeline strip, art heights, divider, headers, footer) reverts to v7.

v12: ten briefs replaced (25-29, 41-45) per the user's edit prompt.
Recomputed from the data: ASIA 9, MIDDLE EAST 7, EUROPE 9, AFRICA 6,
NORTH AMERICA 9, LATIN AMERICA 3, GLOBAL 3 = 46.

v13 rev 10 (Second Check + user corrections): brief 30 "Cincinnati:
Fiona the hippo dies" is DELETED and replaced by "Congo: Ebola tops
11,600 cases" (AFRICA) — the user ordered the swap to make space for
the 19 Nov Ebola figures. Region counts recomputed: ASIA 9, MIDDLE
EAST 7, EUROPE 9, AFRICA 7, NORTH AMERICA 8, LATIN AMERICA 3,
GLOBAL 3 = 46. Brief 28 reads "Mars: Perseverance, Odyssey pause
science" (user correction — "Mars: pause science" is ambiguous);
brief 23 reads "Brazil: Raoni's birthplace" (figure dropped).
"""

LEAD = [
    {"art": "peace", "region": "ASIA", "beat": "PEACE SUMMIT", "src": "BBC \u00b7 REUTERS",
     "at": (114.1, 22.5),
     "hed": "Trump, Putin, Xi issue joint peace declaration",
     "dek": ("Symbolic pledge after 90-minute Shenzhen meeting; no arms-talks timetable.")},
    {"art": "hague", "region": "GLOBAL", "beat": "GENOCIDE RULING", "src": "UN NEWS",
     "at": (4.4, 52.1),
     "hed": "ICJ rules Myanmar committed genocide",
     "dek": ("9\u20136 ruling; first time a state found to have committed genocide.")},
    {"art": "pif", "region": "MIDDLE EAST", "beat": "ATTACK", "src": "SPA \u00b7 AFP",
     "at": (46.7, 24.7),
     "hed": "Houthi attack damages Riyadh's PIF Tower",
     "dek": "Tallest tower in Riyadh hit; no injuries reported."},
    {"art": "kyiv", "region": "EUROPE", "beat": "KYIV ATTACK", "src": "AFP \u00b7 KI",
     "at": (30.5, 50.4),
     "hed": "Russian drones hit Kyiv; 2 embassies damaged",
     "dek": "One dead as drones strike the capital; two embassies hit."},
]

CARDS = [
    {"art": "ant", "region": "NORTH AMERICA", "beat": "MARKETS", "topic": "NORTH AMERICA \u00b7 IPO", "src": "REUTERS",
     "at": (-74.0, 40.7),
     "hed": "Anthropic debuts; Wall St slides",
     "dek": "ANT up 17% on debut; Nasdaq falls 2.3%."},
    {"art": "cop31", "region": "GLOBAL", "beat": "CLIMATE", "topic": "GLOBAL \u00b7 CLIMATE", "src": "REUTERS",
     "at": (30.7, 36.9),
     "hed": "COP31 draft drops fossil fuel text",
     "dek": "80 paras, down from 144; talks continue."},
    {"art": "dhaka_fire", "region": "ASIA", "beat": "UNREST", "topic": "ASIA \u00b7 UNREST", "src": "REUTERS",
     "at": (90.4, 23.8),
     "hed": "Violence in Awami League lockdown",
     "dek": "Two ruling-party members killed, police say."},
    {"art": "akvan", "region": "ASIA", "beat": "WEATHER", "topic": "ASIA \u00b7 STORM", "src": "PTI",
     "at": (86.0, 20.0),
     "hed": "Odisha evacuates ahead of Akvan",
     "dek": "About 299,000 evacuated before landfall."},
    {"art": "tanker", "region": "MIDDLE EAST", "beat": "HORMUZ", "topic": "MIDDLE EAST \u00b7 OIL", "src": "AP",
     "at": (56.0, 26.5),
     "hed": "Iran: 2 supertankers hit mines",
     "dek": "Claim: 4m+ barrels aboard in Hormuz."},
    {"art": "gaza_return", "region": "MIDDLE EAST", "beat": "GAZA", "topic": "MIDDLE EAST \u00b7 GAZA", "src": "AFP",
     "at": (34.4, 31.4),
     "hed": "Israel says Gaza tank raid has ended",
     "dek": "Families return to camp as raid ends."},
    {"art": "talks", "region": "EUROPE", "beat": "DIPLOMACY", "topic": "EUROPE \u00b7 DIPLOMACY", "src": "AP",
     "at": (13.4, 52.5),
     "hed": "Kushner: Russia 'comfortable'",
     "dek": "Claim: NATO-like guarantees on the table."},
    {"art": "cost48", "region": "NORTH AMERICA", "beat": "WAR COST", "topic": "NORTH AMERICA \u00b7 COST", "src": "AP",
     "at": (-77.0, 38.9),
     "hed": "Iran war cost: $48.3bn",
     "dek": "US estimate, as of 13 November."},
    {"art": "shield", "region": "EUROPE", "beat": "CYBER", "topic": "EUROPE \u00b7 CYBER", "src": "DW \u00b7 AP",
     "at": (4.4, 50.8),
     "hed": "EU: AI-assisted cyberattack",
     "dek": "First such disclosure from Brussels."},
    {"art": "strike", "region": "LATIN AMERICA", "beat": "STRIKE", "topic": "LATIN AMERICA \u00b7 STRIKE", "src": "EFE",
     "at": (-74.1, 4.7),
     "hed": "Nationwide strike vs tax bill",
     "dek": "About 55,000 nationwide (govt); 285 marches."},
    {"art": "marathon", "region": "AFRICA", "beat": "DOPING", "topic": "AFRICA \u00b7 SPORT", "src": "AIU \u00b7 BBC",
     "at": (36.8, -1.3),
     "hed": "Jepchirchir banned 3 years (EPO)",
     "dek": "World marathon champion tests positive."},
    {"art": "gta", "region": "NORTH AMERICA", "beat": "LAUNCH", "topic": "NORTH AMERICA \u00b7 LAUNCH", "src": "ROCKSTAR",
     "at": (-80.2, 25.8),
     "hed": "GTA VI launches",
     "dek": "US midnight ET = 05:00 UTC; NZ opened 11:00 UTC 18th."},
]

# "Also on Thursday 19 November": (place, text, region, (lon, lat))
# The UWCL item holds two results, split into two briefs (London, Barcelona).
BRIEFS = [
    ("Crimea", "Bridge hit again; Ukraine confirms", "EUROPE", (33.6, 45.3)),
    ("Shenzhen", "Putin vows 'more painful' reply", "EUROPE", (114.1, 22.5)),
    ("Iraq", "Kataib Hezbollah compromise", "MIDDLE EAST", (44.4, 33.3)),
    ("Lebanon", "Israel strikes Janta", "MIDDLE EAST", (36.0, 33.9)),
    ("Yemen", "Houthis say 15 killed (CLAIM)", "MIDDLE EAST", (44.2, 15.4)),
    ("Argentina", "Disability law passes 71-0", "LATIN AMERICA", (-58.4, -34.6)),
    ("Brazil", "Lula signs Raoni's land (362,243 ha)", "LATIN AMERICA", (-53.0, -10.0)),
    ("Indonesia", "asset forfeiture law passed", "ASIA", (106.8, -6.2)),
    ("Seoul", "Kim Keon-hee jail term finalised", "ASIA", (126.98, 37.57)),
    ("Los Angeles", "Burn-scar evacuation alerts", "NORTH AMERICA", (-118.24, 34.05)),
    ("Florida", "Flood emergency widened", "NORTH AMERICA", (-81.7, 28.5)),
    ("Mars", "Perseverance, Odyssey hit glitches", "GLOBAL", (-118.17, 34.15)),
    ("Senate", "Iran war-powers bid fails 48–51", "NORTH AMERICA", (-77.0, 38.9)),
    ("Congo", "Ebola tops 11,600 cases", "AFRICA", (22.0, -2.0)),
    ("Florida", "record 20th execution", "NORTH AMERICA", (-81.7, 28.5)),
    ("Washington", "DOJ drops TPS bid", "NORTH AMERICA", (-77.0, 38.9)),
    ("Senegal", "4 bodies found", "AFRICA", (-17.4, 14.7)),
    ("Kenya", "rare earths deal", "AFRICA", (36.8, -1.3)),
    ("Sudan", "strikes hit Nyala (CLAIM)", "AFRICA", (24.9, 12.0)),
    ("Nigeria", "Yutong CNG plant opens", "AFRICA", (3.4, 6.5)),
    ("South Africa", "row with Nigeria", "AFRICA", (28.2, -25.7)),
    ("Pakistan", "22 militants killed (CLAIM)", "ASIA", (70.0, 33.0)),
    ("Pakistan", "Qatar MoU signed", "ASIA", (73.1, 33.7)),
    ("Pakistan", "airspace ban", "ASIA", (73.1, 33.7)),
    # v12: ten briefs replaced (25-29, 41-45). #41 "Lawmakers back
    # Greenland deal" is 206px at 11.5px -- 30px wider than the 176px
    # column, so it is shortened to "MPs back Greenland deal" (176.0px,
    # exactly the column width); the other nine use the briefed texts
    # verbatim. Mars (a space story) is plotted at JPL, Pasadena, since
    # every brief needs a map dot. Region counts recomputed from the
    # data: ASIA 9, MIDDLE EAST 7, EUROPE 9, AFRICA 7, NORTH AMERICA 8,
    # LATIN AMERICA 3, GLOBAL 3 = 46 (rev 10: brief 30 Cincinnati ->
    # Congo Ebola moves one count NORTH AMERICA -> AFRICA). The UWCL briefs leave the list
    # (and the Sports panel), so the list/Sports duplication is gone.
    ("Copenhagen", "MPs back Greenland deal", "EUROPE", (12.57, 55.68)),
    ("France", "Green leader to back Mélenchon", "EUROPE", (2.35, 48.86)),
    ("Tbilisi", "Gas blast kills six", "EUROPE", (44.79, 41.72)),
    ("Japan", "Takaichi, Putin agree to keep talks", "ASIA", (139.69, 35.68)),
    ("Israel", "Mosque arson probe in Dahi", "MIDDLE EAST", (34.78, 32.09)),
    ("Kyiv", "missile attack 23:25 UTC", "EUROPE", (30.5, 50.4)),
]

# The day by the clock, in UTC: only times stated by the sources.
# The strip shows 7 of these; the full 12 are the brief's timeline.
# v5: 04:05 Korea flights halt and 23:19 Florida execution leave the
# strip (both stories stay on the page: Florida is a brief, Suneung in
# the Date Check). New: 08:27 Big-three summit opens (16:27 local,
# Shenzhen, UTC+8) and 09:00 ICJ reads judgment (10:00 The Hague, UTC+1).
# v9: back to the v7 chip strip (7 events, full labels); the 05:00 GTA VI
# tick and the proportional axis are removed.
# Rev 11 (user order): the strip is rebuilt as real events at the
# moment they happened — no data releases, no statistics, no
# publication times. 00:30 Australia jobless, 13:30 US jobless
# claims and 21:00 Wall St closes are removed. Time corrections:
# First ANT trade 16:50 -> 16:48, Argentina 22:43 -> 22:40.
# Full labels fit at 10px Merriweather (total 891.1px, gap 6.3px
# measured) — no shortening needed. Two consecutive chips may
# share a colour (07:00 + 08:27 ASIA; 16:48 + 19:01 N. AMERICA).
TIMELINE = [
    ("07:00", "Kim Keon-hee term upheld", "ASIA"),
    ("08:27", "Big-three summit opens", "ASIA"),
    ("09:00", "ICJ reads judgment", "GLOBAL"),
    ("16:48", "First ANT trade", "NORTH AMERICA"),
    ("19:01", "Senate Iran vote", "NORTH AMERICA"),
    ("22:40", "Argentina 71\u20130", "LATIN AMERICA"),
    ("23:25", "Kyiv missile attack", "EUROPE"),
]

JUDGE_NOTE = "Everything on this page happened, or was first reported, on Thursday 19 November 2026 (any time zone, see Date Check)."
# Rev 8 footer (rank-1 style): one precise sentence — date rule +
# attribution + the real sources — in TWO lines at 10px Inter bold
# (split A, measured: line 1 is 895px, line 2 is 549px, limit 980).
# Sources are the real ones from the data (leads + cards): Reuters,
# AP, AFP, BBC, UN News, SPA, PTI, DW, EFE, AIU — plus "and others"
# for KI and Rockstar, which are named on their own cards.
FOOTER_LINES = [
    "Every story here happened, or was first reported, on Thursday 19 November 2026; claims are attributed. Sources: Reuters, AP, AFP, BBC, UN News, SPA, PTI, DW, EFE, AIU and others.",
    "Original drawings, illustration not a photo; map from Natural Earth. Markets: AP \u00b7 MarketWatch \u00b7 Kitco \u00b7 Reuters.",
]

# DATE CHECK — source data (rev 10 restores the rev 7 7-entry
# paragraphs; the rev 8/9 chip format is gone at the user's order).
# The renderer does NOT print these paragraphs verbatim: it prints
# DC_DISPLAY below, the same facts tidied for the 227px box (the
# rev 7 flaw was truncation — only 13 of 32 lines shown). Every
# condensation is listed in the DC_DISPLAY comment; nothing is
# invented, and every item in every section is still present.
DATE_CHECK = [
    ('DATE CHECK · Thu 19 Nov 2026', None),
    ('Rule:', 'An item counts if it happened, or was first reported, on Thu 19 Nov 2026 (UTC); local-date exceptions are marked.'),
    ('Times:', 'Trump-Xi-Putin talks opened 08:27 UTC (16:27 Shenzhen) · ICJ judgment scheduled 10:00 The Hague = 09:00 UTC · GTA VI unlocked 05:00 UTC in US/Canada (NZ rollout began 11:00 UTC on the 18th) · Anthropic priced late 18 Nov ET, first traded and closed Thu 19th.'),
    ('Edge cases:', 'Suneung 23:40 UTC 18th · Kumamoto M5.7 17:22 18th · Senegal boat 18th · Kyiv missile 23:25 19th · Brasileirão: Corinthians 4-0 Botafogo (21:30 BRT 18th = 00:30 UTC 19th) and Cruzeiro 2-1 Palmeiras (20:30 BRT 18th) are not shown.'),
    ('Left out, first reported Wed 18 Nov:', 'Bank Indonesia hike · Sanon verdict · Yoro killings · Philippines release · Gaza raid start · Fatah-3 test · Ethiopia–Eritrea buildup · Yunus home fire.'),
    ('Not yet news (Fri 20 Nov):', 'Akvan landfall · COP31 close · Jurf al-Sakhar · Trump news conference.'),
    ('Markets:', 'Figures are US closing values for 19 Nov; Asian and European closes and crypto are not shown (no verified 19 Nov close).'),
]

# DC_DISPLAY — the tidied presentation of DATE_CHECK, rendered by
# datecheck_block. Same facts, restructured so the whole box fits
# (16 lines at 9px Inter in the 242px box — nothing hidden):
#   * Rule: one line — "on 19 Nov 2026 (UTC), or first reported."
#     (the "An item counts if it happened" lead-in and the
#     "local-date exceptions are marked" clause are dropped; the
#     Edge section below IS the marked exceptions, each dated).
#   * Times: four item lines, time right-aligned, chronological
#     (05:00 GTA, 08:27 talks, 09:00 ICJ, then Anthropic).
#     Rev 11: the items are shortened so each fits one line at 9px
#     — GTA drops "(NZ 11:00 UTC 18th)" (card 16 carries the NZ
#     detail), talks drop "(16:27 Shenzhen)", ICJ drops
#     "scheduled". Anthropic keeps the full B10 wording ("priced
#     late 18 Nov ET; traded + closed Thu 19th", 247.0px in 249px
#     available — measured, 2px slack).
#   * Edge cases: flowing text, full UTC conversion kept
#     ("21:30 BRT 18th = 00:30 UTC 19th"). Rev 11: "UTC" dropped
#     after Suneung's time (the Rule already says UTC), "19th"
#     dropped after Kyiv 23:25 (unmarked = 19 Nov per the Rule),
#     Cruzeiro's "(20:30 BRT 18th)" dropped. Ebola is NOT here
#     (user correction: it is a 19 Nov story in its own right,
#     now brief 30, not an edge case).
#   * Left out / Not yet: verbatim items; labels shortened to
#     "Left out · Wed 18 Nov:" / "Not yet · Fri 20 Nov:".
#     Left out drops Ebola (now brief 30), China drone controls
#     (announced 19 Oct, not 18 Nov) and PAHO measles (17th, not
#     18th); Not yet drops Raoni ordinance (signed 19 Nov — the
#     Raoni story is brief 23).
#   * Markets: "Figures are" dropped, "(no verified 19 Nov
#     close)" -> "— no verified close"; the reason is kept.
# Kinds: "para" = red bold label inline + flowing wrapped body;
# "timed" = one item per line, (item, right-aligned time or None).
DC_DISPLAY = [
    ("Rule:", "para", "on 19 Nov 2026 (UTC), or first reported."),
    ("Times:", "timed", [
        ("GTA VI unlocked", "05:00 UTC"),
        ("Trump–Xi–Putin talks opened", "08:27 UTC"),
        ("ICJ judgment", "10:00 Hague = 09:00 UTC"),
        ("Anthropic priced late 18 Nov ET; traded + closed Thu 19th", None),
    ]),
    ("Edge cases:", "para", "Suneung 23:40 18th · Kumamoto M5.7 17:22 18th · Senegal boat 18th · Kyiv missile 23:25 · Brasileirão: Corinthians 4–0 Botafogo 21:30 BRT 18th (= 00:30 UTC 19th); Cruzeiro 2–1 Palmeiras — not shown."),
    ("Left out · Wed 18 Nov:", "para", "Bank Indonesia hike · Sanon verdict · Yoro killings · Philippines release · Gaza raid start · Fatah-3 test · Ethiopia–Eritrea buildup · Yunus home fire."),
    ("Not yet · Fri 20 Nov:", "para", "Akvan landfall · COP31 close · Jurf al-Sakhar · Trump news conference."),
    ("Markets:", "para", "US closes for 19 Nov only; Asian/European closes and crypto not shown — no verified close."),
]

REGIONS = ["ASIA", "MIDDLE EAST", "EUROPE", "AFRICA", "NORTH AMERICA", "LATIN AMERICA", "GLOBAL"]


def all_stories():
    """(number, story) in page order: leads, cards, then briefs."""
    out = []
    n = 1
    for s in LEAD + CARDS:
        out.append((n, s)); n += 1
    for b in BRIEFS:
        out.append((n, {"region": b[2], "at": b[3], "place": b[0], "hed": b[1]})); n += 1
    return out


def count():
    return len(LEAD) + len(CARDS) + len(BRIEFS)


def continents():
    return {"ASIA", "EUROPE", "AFRICA", "NORTH AMERICA", "LATIN AMERICA"}


if __name__ == "__main__":
    print(count(), "stories")
