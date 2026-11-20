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
"""

LEAD = [
    {"art": "peace", "region": "ASIA", "beat": "PEACE SUMMIT", "src": "BBC \u00b7 REUTERS",
     "at": (114.1, 22.5),
     "hed": "Trump, Putin, Xi issue joint peace declaration",
     "dek": ("Symbolic pledge after 90-minute Shenzhen meeting; no arms-talks timetable.")},
    {"art": "hague", "region": "GLOBAL", "beat": "GENOCIDE RULING", "src": "UN NEWS",
     "at": (4.4, 52.1),
     "hed": "ICJ finds Myanmar guilty of genocide",
     "dek": ("First genocide ruling vs a state; Rohingya case decided at The Hague.")},
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
    ("Cincinnati", "Fiona the hippo dies", "NORTH AMERICA", (-84.5, 39.1)),
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
    # data: ASIA 9, MIDDLE EAST 7, EUROPE 9, AFRICA 6, NORTH AMERICA 9,
    # LATIN AMERICA 3, GLOBAL 3 = 46. The UWCL briefs leave the list
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
TIMELINE = [
    ("00:04", "Crimean Bridge hit", "EUROPE"),
    ("08:27", "Big-three summit opens", "ASIA"),
    ("09:00", "ICJ reads judgment", "GLOBAL"),
    ("13:05", "Kyiv embassies hit", "EUROPE"),
    ("16:50", "First ANT trade", "NORTH AMERICA"),
    ("21:00", "Wall St closes", "NORTH AMERICA"),
    ("22:43", "Argentina 71\u20130", "LATIN AMERICA"),
]

JUDGE_NOTE = "Everything on this page happened, or was first reported, on Thursday 19 November 2026 (any time zone, see Date Check)."
SOURCES = "Sources named on each story."
FOOT_NOTE = "Claims by warring sides are attributed. Original drawings, illustration not a photo; map from Natural Earth."
# v8 (REVISION 3) footer: 4 lines, 10px, pitch 11.5, full width (22..1002).
# Each line fits on one line at 10px (measured against the real font).
FOOTER_LINES = [
    "SOURCES: every headline card, market tile group and sports result names its source (wire agency, UN body, exchange data or official release); short-list entries come from the same kinds of sources. Figures are copied from them, never estimated.",
    "CLAIMS: statements by parties to a conflict and single-source or unconfirmed reports carry a CLAIM tag and are attributed, never stated as fact.",
    "TIMES: clock times are UTC; scheduled times are marked as scheduled. Market figures are US closing values; sports scores are final results.",
    "LIMITS: compiled on Fri 20 Nov 2026; later corrections are not reflected. Original drawings, illustration not a photo; map from Natural Earth.",
]

DATE_CHECK = [
    ("DATE CHECK \u00b7 Thu 19 Nov 2026", None),
    ("Rule:", "An item counts if it happened, or was first reported, on Thu 19 Nov 2026 (UTC); local-date exceptions are marked."),
    ("Times:", "Trump-Xi-Putin talks opened 08:27 UTC (16:27 Shenzhen) \u00b7 ICJ judgment scheduled 10:00 The Hague = 09:00 UTC \u00b7 GTA VI unlocked 05:00 UTC in US/Canada (NZ rollout began 11:00 UTC on the 18th) \u00b7 Anthropic priced Wed 18th, first traded and closed Thu 19th."),
    ("Edge cases:", "Suneung 23:40 UTC 18th \u00b7 Kumamoto M5.7 17:22 18th \u00b7 Senegal boat 18th \u00b7 Kyiv missile 23:25 19th \u00b7 Brasileir\u00e3o: Corinthians 4-0 Botafogo (21:30 BRT 18th = 00:30 UTC 19th) and Cruzeiro 2-1 Palmeiras (20:30 BRT 18th) are not shown."),
    ("Left out, first reported Wed 18 Nov:", "Bank Indonesia hike \u00b7 Sanon verdict \u00b7 Yoro killings \u00b7 PAHO measles \u00b7 China drone controls \u00b7 Philippines release \u00b7 Gaza raid start \u00b7 Fatah-3 test \u00b7 Ethiopia\u2013Eritrea buildup \u00b7 Yunus home fire \u00b7 Ebola in Congo (ongoing; latest figures as of 16 Nov)."),
    ("Not yet news (Fri 20 Nov):", "Akvan landfall \u00b7 COP31 close \u00b7 Jurf al-Sakhar \u00b7 Trump news conference \u00b7 Raoni ordinance."),
    ("Markets:", "Figures are US closing values for 19 Nov; Asian and European closes and crypto are not shown (no verified 19 Nov close)."),
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
