#!/usr/bin/env python3
"""Build-time renderer for the news-image-20261121 round 2 board.

Draws entry.png (1024x1024) with Pillow at BUILD time only. The runtime
entrypoint (main.py) is stdlib-only and merely copies this PNG.
All 36 stories were verified against live 21 Nov 2026 reporting
(BBC/AP/Reuters/AFP/UPI/Euronews/France 24/Al Jazeera/Straits Times
via the OneTurn day page and wire searches) on 2026-11-22.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
RED = (178, 34, 28)
NAVY = (31, 58, 95)
TEAL = (15, 118, 110)
GOLD = (176, 132, 16)
GREY = (90, 88, 82)
LIGHT = (255, 255, 255)
CARD = (255, 253, 247)
RULE = (26, 26, 26)

FDIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def card(draw, x, y, w, h, outline=(200, 192, 175)):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=outline, width=1)


def tag(draw, x, y, label, bg, fg=LIGHT):
    f = SANS_B(10)
    tw = draw.textlength(label, font=f)
    draw.rectangle([x, y, x + tw + 12, y + 16], fill=bg)
    draw.text((x + 6, y + 2), label, font=f, fill=fg)
    return tw + 12


# ---------------------------------------------------------------- stories
# (number, region, headline, detail, source)
HERO = [
    (1, "MIDDLE EAST", "Iran strikes US bases in Bahrain",
     "Tehran says it hit two US positions; Bahrain reports a fire at a "
     "civilian site. Iran also says it downed a US drone near Qeshm.",
     "AL JAZEERA"),
    (2, "UKRAINE", "Missile hits Zelenskyy's hometown",
     "A Russian ballistic missile struck central Kryvyi Rih, killing two "
     "people, incl. a 7-year-old boy, and wounding about 60.",
     "AP"),
    (3, "CLIMATE", "COP31 runs past its deadline",
     "The UN climate summit in Antalya goes into overtime with no deal: "
     "the draft omits fossil fuels and talks may slip to next year.",
     "BBC"),
]
MEDIUM = [
    (4, "SAUDI ARABIA", "Three missiles downed over Riyadh",
     "Three Houthi missiles downed over Riyadh; a drone is downed in the south.", "REUTERS"),
    (5, "MARKETS", "AI sell-off drags Wall St into correction",
     "S&P 500 -3.7%; Nasdaq wipes out 2026 gains; Anthropic IPO stumbles day two.", "AP"),
    (6, "MEXICO", "FBI most-wanted cartel boss captured",
     "Forces seize Chapo Isidro in Sinaloa; follow-on violence kills at least 11.", "BBC"),
    (7, "JUSTICE", "Myanmar guilty of Rohingya genocide",
     "World court finds Myanmar responsible for the 2017 Rohingya genocide.", "THE GUARDIAN"),
]
BEPI = (8, "SPACE", "BepiColombo reaches Mercury",
        "After 8 years and 10bn km, the ESA-JAXA craft enters Mercury orbit.",
        "UPI")

# briefs grouped by column: (number, headline, detail)
COLUMNS = [
    ("EUROPE", [
        (9, "UK and EU sign three deals",
         "Food, emissions, youth travel deals."),
        (10, "Trump, Xi and Putin meet",
         "First three-way summit; little agreed."),
        (11, "Denmark expels Russian envoy",
         "Envoy expelled over alleged murder plot."),
        (12, "Russian ship hit by drones",
         "Sparta II burns, drifts to Finland."),
        (13, "UN AI-weapons talks continue",
         "100 states back rules by 2028."),
        (14, "Estonia shuts Russia border",
         "All three crossings shut from 1 Dec."),
        (15, "Rutte plans Warsaw visit",
         "After missiles land in Poland."),
    ]),
    ("MIDDLE EAST & GULF", [
        (16, "Strike kills 3 in Gaza",
         "Food truck hit in Gaza City; 3 dead."),
        (17, "Hormuz tanker attacks go on",
         "Tankers hit near Khasab; Brent near $90."),
        (18, "Saudi-Japan oil stockpile",
         "Crude stored in Japan to triple."),
        (19, "Basra power fire kills four",
         "Four dead, 35 hurt in Basra."),
        (20, "Turkey seizes Sozcu TV",
         "Last big independent channel falls."),
        (21, "Iraq, militia set joint post",
         "Joint centre set up in Jurf al-Sakhar."),
        (22, "Gulf economies hit by Iran war",
         "Recession as Hormuz disruption bites."),
    ]),
    ("THE AMERICAS", [
        (23, "FBI crime database hacked",
         "FBI probes apparent NCIC breach."),
        (24, "Record floods hit Florida",
         "Hundreds rescued; St Johns still rising."),
        (25, "Mamdani: shut Rikers by 2032",
         "NY mayor sets 2032 closure date."),
        (26, "M6.7 quake shakes Peru",
         "Lima rattled; no deaths reported."),
        (27, "Bolsonaro in intensive care",
         "Ex-president stable; surgery weighed."),
        (28, "Palisades fire arson verdict",
         "Rinderknecht guilty over 2025 LA fire."),
        (29, "Measles death in Virginia",
         "Virginia's first measles death of 2026."),
    ]),
    ("ASIA-PACIFIC & BEYOND", [
        (30, "Davao jet: all 146 safe",
         "Engine warning; all leave by slides."),
        (31, "M6.8 quake off Timor-Leste",
         "Sea quake north-east of Dili."),
        (32, "EU-Indonesia trade deal",
         "98.5% of tariffs on EU goods go."),
        (33, "Nvidia chief Huang ousted",
         "Trump discussed exit with Xi."),
        (34, "GTA VI earns $3.8bn on day one",
         "Biggest entertainment launch ever."),
        (35, "Riemann proof claim via AI",
         "Mathematician says Claude helped."),
        (36, "England beat All Blacks 37-12",
         "Record margin at Twickenham."),
    ]),
]

NUMBERS = [
    ("S&P 500", "-3.7%"),
    ("BRENT CRUDE", "$89.95"),
    ("GTA VI, DAY ONE", "$3.8bn"),
    ("DISPLACED, ETHIOPIA", "700,000"),
    ("PERU / TIMOR QUAKES", "M6.7 / M6.8"),
    ("SAFE IN DAVAO", "146"),
]

# map pins: (story number, lon, lat)
PINS = [(1, 50.5, 26.2), (2, 33.4, 47.9), (3, 30.7, 36.9), (4, 46.7, 24.6),
        (5, -74.0, 40.7), (6, -108.5, 25.6), (7, 4.3, 52.1),
        (26, -75.9, -11.2), (30, 125.6, 7.1)]
PIN_NAMES = "1 Bahrain   2 Kryvyi Rih   3 Antalya   4 Riyadh   5 New York"
PIN_NAMES2 = "6 Sinaloa   7 The Hague   26 Peru   30 Davao"

# ---------------------------------------------------------------- pictograms
def pic_bahrain(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 58))
    for i, yy in enumerate((18, 34, 50)):
        d.arc([x + 20 + i * 8, y + yy - 26, x + 150 + i * 8, y + yy + 26],
              start=200, end=340, fill=(255, 170, 60), width=3)
        d.ellipse([x + 148 + i * 8 - 4, y + yy - 4, x + 148 + i * 8 + 4,
                   y + yy + 4], fill=(255, 220, 120))
    for bx, bw, bh in ((8, 34, 26), (48, 22, 40), (76, 30, 20), (112, 40, 34)):
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(12, 18, 38))
    d.polygon([(x + 130, y + h - 40), (x + 142, y + h - 62), (x + 154, y + h - 40)],
              fill=(255, 120, 40))
    d.polygon([(x + 136, y + h - 40), (x + 142, y + h - 52), (x + 148, y + h - 40)],
              fill=(255, 220, 90))


def pic_kryvyi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 38, 66))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(30, 20, 36))
    for bx, bw, bh in ((6, 30, 44), (42, 20, 62), (68, 34, 38), (108, 24, 54),
                       (138, 30, 46), (174, 26, 58)):
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(18, 12, 22))
    cx, cy = x + w - 62, y + 34
    for r, col in ((34, (255, 170, 40)), (22, (255, 210, 90)), (12, (255, 240, 180))):
        pts = []
        for k in range(12):
            ang = math.pi * k / 6
            rr = r if k % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=col)
    for sx, sy, sr in ((x + 40, y + 22, 12), (x + 70, y + 14, 9), (x + 100, y + 26, 10)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 100, 120))


def pic_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(13, 84, 76))
    cx, cy, r = x + 52, y + h // 2 + 4, 38
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(140, 200, 220))
    d.ellipse([cx - 22, cy - 26, cx - 2, cy - 8], fill=(90, 170, 90))
    d.ellipse([cx + 2, cy + 6, cx + 24, cy + 26], fill=(90, 170, 90))
    d.ellipse([cx + 8, cy - 30, cx + 26, cy - 14], fill=(90, 170, 90))
    d.arc([cx - r, cy - r, cx + r, cy + r], start=0, end=360,
          fill=(255, 255, 255), width=2)
    kx, ky, kr = x + w - 46, y + 30, 24
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 253, 247),
              outline=(26, 26, 26), width=2)
    d.line([kx, ky, kx, ky - 14], fill=(26, 26, 26), width=3)
    d.line([kx, ky, kx + 11, ky + 6], fill=(26, 26, 26), width=3)
    d.text((x + w - 118, y + h - 20), "DAY 16: NO DEAL", font=SANS_B(10),
           fill=(255, 220, 90))


def pic_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 42, 74))
    for bx, bw, frac in ((6, 26, 0.55), (38, 18, 0.8), (60, 22, 0.48),
                         (88, 14, 1.0), (108, 26, 0.62), (140, 20, 0.85)):
        bh = int(h * frac)
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(8, 22, 44))
    d.rectangle([x + 88, y + 1, x + 102, y + 5], fill=(8, 22, 44))
    for sx, sy in ((30, 14), (90, 8), (150, 16)):
        d.arc([x + sx - 20, y + sy - 4, x + sx + 20, y + sy + 22],
              start=300, end=60, fill=(255, 255, 255), width=3)
        d.ellipse([x + sx - 3, y + sy - 3, x + sx + 3, y + sy + 3],
                  fill=(255, 200, 80))
    d.polygon([(x + w - 30, y + 6), (x + w - 12, y + 6), (x + w - 21, y + 22)],
              fill=(255, 200, 80))


def pic_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 253, 247))
    for bx, frac in ((10, 0.30), (30, 0.50), (50, 0.40), (70, 0.68),
                     (90, 0.55), (110, 0.85), (130, 0.72), (150, 0.95)):
        bh = int(h * frac)
        d.rectangle([x + bx, y + h - 6 - bh, x + bx + 14, y + h - 6],
                    fill=(190, 190, 185))
    pts = [(x + 12, y + h * 0.28), (x + 45, y + h * 0.45), (x + 78, y + h * 0.38),
           (x + 110, y + h * 0.66), (x + 142, y + h * 0.62),
           (x + 172, y + h * 0.92)]
    d.line(pts, fill=(178, 34, 28), width=4, joint="curve")
    d.polygon([(x + 172, y + h * 0.92), (x + 158, y + h * 0.86),
               (x + 162, y + h * 0.98)], fill=(178, 34, 28))


def pic_chapo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 38, 44))
    cx, cy = x + w // 2, y + h // 2 - 2
    R = int(h * 0.34)
    pts = []
    for k in range(10):
        ang = math.pi * k / 5 - math.pi / 2
        rr = R if k % 2 == 0 else R * 0.43
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(212, 175, 55))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(38, 38, 44))
    d.ellipse([x + w - 30, y + 6, x + w - 14, y + 22], outline=(200, 200, 200), width=3)
    d.ellipse([x + w - 48, y + 6, x + w - 32, y + 22], outline=(200, 200, 200), width=3)
    d.line([x + w - 40, y + 14, x + w - 24, y + 14], fill=(200, 200, 200), width=2)


def pic_icj(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 44, 84))
    cx, cy = x + w // 2, y + h // 2
    d.line([cx, cy - 26, cx, cy + 26], fill=(255, 220, 120), width=3)
    d.line([cx - 34, cy - 20, cx + 34, cy - 20], fill=(255, 220, 120), width=3)
    d.line([cx - 34, cy - 20, cx - 34, cy - 6], fill=(255, 220, 120), width=2)
    d.line([cx + 34, cy - 20, cx + 34, cy - 6], fill=(255, 220, 120), width=2)
    d.polygon([(cx - 46, cy - 6), (cx - 22, cy - 6), (cx - 34, cy + 10)],
              fill=(255, 220, 120))
    d.polygon([(cx + 22, cy - 6), (cx + 46, cy - 6), (cx + 34, cy + 10)],
              fill=(255, 220, 120))
    d.ellipse([cx - 3, cy - h * 0.30, cx + 3, cy - h * 0.30 + 6],
              fill=(255, 220, 120))
    d.rectangle([cx - 18, cy + h * 0.30, cx + 18, y + h - 4],
                fill=(255, 220, 120))


def pic_bepi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 16, 34))
    for sx, sy in ((14, 14), (40, 8), (70, 20), (96, 10), (30, 84), (120, 78)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    cx, cy, r = x + 62, y + h // 2 + 6, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 140, 130))
    for ox, oy, orad in ((cx - 14, cy - 10, 6), (cx + 10, cy + 12, 8),
                         (cx + 14, cy - 16, 4), (cx - 4, cy + 16, 5)):
        d.ellipse([ox - orad, oy - orad, ox + orad, oy + orad], fill=(120, 110, 100))
    d.ellipse([cx - r - 14, cy - r - 10, cx + r + 14, cy + r + 10],
              outline=(255, 200, 80), width=2)
    d.rectangle([x + w - 34, y + 12, x + w - 22, y + 24], fill=(220, 220, 220))
    d.rectangle([x + w - 46, y + 15, x + w - 34, y + 21], fill=(90, 140, 220))
    d.rectangle([x + w - 22, y + 15, x + w - 10, y + 21], fill=(90, 140, 220))


# ---------------------------------------------------------------- world map
NA = [(-168, 66), (-155, 71), (-140, 70), (-125, 71), (-118, 70), (-110, 68),
      (-100, 69), (-90, 69), (-85, 66), (-80, 62), (-77, 62), (-70, 58),
      (-65, 60), (-60, 55), (-55, 52), (-60, 47), (-65, 44), (-70, 42),
      (-75, 36), (-80, 32), (-81, 26), (-84, 30), (-90, 21), (-97, 26),
      (-105, 22), (-110, 29), (-117, 33), (-125, 40), (-125, 49), (-130, 56),
      (-135, 60), (-145, 60), (-155, 58), (-162, 58), (-168, 66)]
GL = [(-55, 60), (-45, 60), (-40, 65), (-30, 68), (-22, 70), (-25, 76),
      (-35, 80), (-50, 80), (-58, 76), (-60, 70), (-55, 60)]
SA = [(-80, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
      (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -52), (-66, -55),
      (-65, -45), (-58, -38), (-48, -28), (-41, -23), (-35, -8), (-40, -3),
      (-50, 0), (-55, 5), (-62, 9), (-70, 11), (-77, 8), (-80, 9)]
EU = [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (3, 53), (8, 57),
      (10, 59), (5, 60), (12, 61), (18, 62), (18, 69), (25, 71), (30, 70),
      (28, 65), (23, 60), (21, 56), (18, 55), (12, 55), (8, 57), (8, 54),
      (3, 52), (0, 49), (-2, 44), (-2, 37), (0, 39), (3, 42), (7, 44),
      (10, 44), (14, 45), (19, 42), (23, 40), (26, 38), (30, 36), (28, 41),
      (23, 40), (19, 45), (15, 44), (12, 44), (8, 44), (3, 43), (-1, 38),
      (-6, 36), (-10, 36)]
AF = [(-17, 15), (-16, 20), (-15, 27), (-10, 31), (-5, 35), (0, 36),
      (10, 37), (11, 34), (20, 32), (25, 32), (32, 31), (35, 28),
      (34, 27), (37, 22), (39, 18), (43, 12), (48, 11), (51, 12),
      (46, 5), (41, 0), (40, -5), (39, -12), (36, -18), (33, -26),
      (28, -33), (20, -35), (17, -32), (15, -27), (13, -18), (12, -6),
      (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12), (-17, 15)]
AS = [(30, 36), (36, 36), (36, 33), (40, 36), (44, 39), (48, 39), (50, 37),
      (54, 37), (57, 27), (58, 25), (61, 25), (66, 25), (70, 24), (72, 20),
      (76, 10), (80, 8), (80, 13), (85, 19), (89, 22), (91, 22), (94, 17),
      (97, 16), (100, 8), (103, 2), (104, 9), (106, 11), (109, 13),
      (108, 18), (105, 20), (108, 21), (110, 20), (113, 22), (117, 23),
      (120, 25), (122, 28), (121, 32), (120, 35), (122, 37), (124, 40),
      (127, 40), (130, 42), (132, 43), (135, 44), (138, 46), (140, 47),
      (142, 50), (142, 53), (140, 56), (138, 59), (136, 60), (142, 60),
      (150, 60), (156, 59), (158, 55), (162, 56), (163, 60), (170, 66),
      (178, 65), (170, 70), (160, 70), (150, 72), (140, 73), (130, 72),
      (120, 73), (110, 74), (105, 77), (100, 76), (95, 76), (90, 75),
      (85, 74), (80, 73), (75, 72), (70, 72), (68, 70), (65, 69),
      (60, 69), (55, 68), (50, 68), (45, 68), (40, 67), (35, 66),
      (32, 70), (30, 70), (28, 68), (32, 66), (36, 64), (40, 62),
      (42, 58), (40, 52), (38, 48), (35, 45), (32, 42), (30, 36)]
AU = [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33), (129, -32),
      (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (147, -39),
      (150, -37), (153, -32), (153, -27), (150, -23), (146, -19), (142, -15),
      (142, -11), (140, -17), (136, -15), (135, -12), (132, -11), (130, -13),
      (126, -14), (122, -17), (118, -20), (113, -22)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 57), (1, 53), (-1, 51)]
JP = [(130, 31), (133, 34), (136, 35), (139, 37), (141, 40), (142, 43),
      (144, 44), (141, 42), (139, 38), (136, 36), (133, 34)]
NZ = [(167, -45), (170, -43), (174, -41), (176, -38), (174, -36), (172, -40),
      (168, -44), (167, -45)]
ID = [(95, 5), (98, 3), (100, 0), (104, -3), (108, -6), (112, -7),
      (116, -8), (120, -9), (124, -9), (128, -6), (132, -4), (136, -2),
      (140, -3), (138, -6), (132, -7), (126, -8), (120, -9), (114, -8),
      (110, -7), (106, -6), (102, -4), (98, 0), (95, 5)]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 232, 239),
                outline=(200, 192, 175), width=1)
    lon0, lon1, lat0, lat1 = -170.0, 190.0, -58.0, 84.0

    def px(lon, lat):
        return (x + (lon - lon0) / (lon1 - lon0) * w,
                y + (lat1 - lat) / (lat1 - lat0) * h)

    for lon in range(-150, 181, 30):
        gx, _ = px(lon, 0)
        d.line([gx, y, gx, y + h], fill=(205, 220, 230), width=1)
    for lat in (-30, 0, 30, 60):
        _, gy = px(0, lat)
        d.line([x, gy, x + w, gy], fill=(205, 220, 230), width=1)
    for poly in (NA, GL, SA, EU, AF, AS, AU, UK, JP, NZ, ID):
        d.polygon([px(lo, la) for lo, la in poly], fill=(216, 210, 196),
                  outline=(160, 152, 132))
    for num, lon, lat in PINS:
        cx, cy = px(lon, lat)
        r = 11
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                  outline=(255, 255, 255), width=2)
        f = SANS_B(11)
        tw = d.textlength(str(num), font=f)
        d.text((cx - tw / 2, cy - 8), str(num), font=f, fill=(255, 255, 255))
    d.text((x + 8, y + 6), "WHERE IT HAPPENED", font=SANS_B(11), fill=NAVY)
    d.text((x + 8, y + h - 30), PIN_NAMES, font=SANS(10), fill=INK)
    d.text((x + 8, y + h - 17), PIN_NAMES2, font=SANS(10), fill=INK)

# ---------------------------------------------------------------- layout
PICS = {1: pic_bahrain, 2: pic_kryvyi, 3: pic_cop31, 4: pic_riyadh,
        5: pic_markets, 6: pic_chapo, 7: pic_icj}


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 16  # margin

    # ---- masthead
    d.rectangle([M, 10, W - M, 12], fill=RULE)
    title = "THE WORLD IN ONE DAY"
    f_title = SERIF_B(46)
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 18), title, font=f_title, fill=INK)
    date = "SATURDAY  21  NOVEMBER  2026"
    f_date = SANS_B(25)
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 72), date, font=f_date, fill=RED)
    sub = "36 stories  ·  7 regions  ·  all first reported on this day"
    f_sub = SANS(13)
    tw = d.textlength(sub, font=f_sub)
    d.text(((W - tw) / 2, 104), sub, font=f_sub, fill=GREY)
    d.rectangle([M, 124, W - M, 126], fill=RULE)
    d.rectangle([M, 129, W - M, 130], fill=RULE)

    # ---- hero row: 3 big cards
    hy, hh = 138, 212
    hw = [336, 324, 324]
    hx = [M, M + 336 + 8, M + 336 + 8 + 324 + 8]
    for (num, region, head, detail, src), x, w in zip(HERO, hx, hw):
        card(d, x, hy, w, hh)
        PICS[num](d, x + 1, hy + 1, w - 2, 84)
        tag(d, x + 8, hy + 92, region, RED)
        d.text((x + 8, hy + 114), str(num), font=SERIF_B(22), fill=RED)
        lines = wrap(d, head, SANS_B(19), w - 44)
        text_block(d, (x + 34, hy + 114), lines[:2], SANS_B(19), INK, leading=22)
        y = hy + 114 + 22 * len(lines[:2]) + 2
        lines = wrap(d, detail, SANS(12), w - 16)
        text_block(d, (x + 8, y), lines[:3], SANS(12), (60, 58, 52), leading=15)

    # ---- medium row: 4 cards
    my, mh = 358, 142
    mw = 244
    for i, (num, region, head, detail, src) in enumerate(MEDIUM):
        x = M + i * (mw + 8)
        card(d, x, my, mw, mh)
        PICS[num](d, x + 1, my + 1, mw - 2, 48)
        tag(d, x + 8, my + 54, region, NAVY)
        lines = wrap(d, head, SANS_B(14), mw - 16)
        y = text_block(d, (x + 8, my + 76), lines[:2], SANS_B(14), INK, leading=17)
        lines = wrap(d, detail, SANS(11), mw - 16)
        text_block(d, (x + 8, y + 1), lines[:2], SANS(11), (60, 58, 52), leading=13)

    # ---- map strip + BepiColombo card
    sy = 508
    draw_map(d, M, sy, 648, 110)
    bx = M + 648 + 8
    bw = W - M - bx
    card(d, bx, sy, bw, 110)
    pic_bepi(d, bx + 1, sy + 1, 130, 108)
    tx = bx + 138
    tag(d, tx, sy + 8, BEPI[1], TEAL)
    lines = wrap(d, BEPI[2], SANS_B(15), bw - 146)
    y = text_block(d, (tx, sy + 30), lines[:2], SANS_B(15), INK, leading=18)
    lines = wrap(d, BEPI[3], SANS(11), bw - 146)
    text_block(d, (tx, y + 2), lines[:3], SANS(11), (60, 58, 52), leading=14)

    # ---- briefs: 4 columns x 7
    by = 626
    d.text((M, by), "THE REST OF THE DAY -- 28 MORE STORIES",
           font=SANS_B(13), fill=INK)
    d.rectangle([M, by + 18, W - M, by + 19], fill=RULE)
    col_w, gap = 244, 8
    row_h = 39
    for ci, (region, items) in enumerate(COLUMNS):
        x = M + ci * (col_w + gap)
        y = by + 26
        d.text((x, y), region, font=SANS_B(11), fill=RED)
        d.rectangle([x, y + 15, x + col_w, y + 16], fill=(200, 192, 175))
        yy = y + 22
        for num, head, detail in items:
            d.text((x, yy), str(num), font=SANS_B(12), fill=RED)
            lines = wrap(d, head, SANS_B(12), col_w - 26)
            y2 = text_block(d, (x + 26, yy), lines[:1], SANS_B(12), INK, leading=14)
            lines = wrap(d, detail, SANS(10), col_w - 26)
            text_block(d, (x + 26, y2), lines[:1], SANS(10), (80, 78, 72),
                       leading=12)
            yy += row_h
    # ---- numbers strip
    ny = 954
    d.rectangle([M, ny, W - M, ny + 36], fill=NAVY)
    seg = (W - 2 * M) // 6
    for i, (label, val) in enumerate(NUMBERS):
        cx = M + i * seg + seg // 2
        f1, f2 = SANS_B(9), SANS_B(15)
        tw = d.textlength(label, font=f1)
        d.text((cx - tw / 2, ny + 4), label, font=f1, fill=(180, 200, 230))
        tw = d.textlength(val, font=f2)
        d.text((cx - tw / 2, ny + 17), val, font=f2, fill=(255, 255, 255))
        if i:
            d.line([M + i * seg, ny + 5, M + i * seg, ny + 31],
                   fill=(90, 110, 150), width=1)

    # ---- footer
    fy = 994
    foot = ("Sources: BBC, AP, Reuters, AFP, UPI, Euronews, France 24, "
            "Al Jazeera, The Guardian, Straits Times. Every story was first "
            "reported on Saturday 21 November 2026.")
    lines = wrap(d, foot, SANS(11), W - 2 * M)
    text_block(d, (M, fy), lines, SANS(11), GREY, leading=14)
    d.text((M, 1010), "make.fun  news-image-20261121  --  Round 2",
           font=SANS_B(10), fill=GREY)
    return img


def main():
    img = build()
    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
