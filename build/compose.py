#!/usr/bin/env python3
"""The Daily Frame — Thursday 19 November 2026.

Typesets a one-page broadsheet summing up the world news of Thursday
19 November 2026 as a single 1024x1024 PNG. Pure PIL: every word is real
type, every picture an original drawing made of shapes.

Layout (winners' combined strengths, then improved):
  masthead naming the day -> region tally bar -> "Day in Numbers" panel
  with DRAWN charts -> 13 illustrated story cards -> dotted world map
  with numbered pins AND the day's summit arcs -> 27 numbered briefs
  -> date-check box -> sources footer.
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

W = H = 1024
PAPER = (247, 242, 231)
CARD_BG = (255, 253, 246)
INK = (22, 30, 50)
NAVY = (18, 38, 76)
RED = (178, 32, 44)
GOLD = (198, 146, 42)
TEAL = (16, 110, 110)
PURPLE = (96, 54, 140)
GREEN = (34, 120, 70)
OCHRE = (196, 120, 28)
GREY = (105, 105, 105)
LINE = (203, 195, 172)
FAINT = (120, 118, 105)

REG = {"EUROPE": NAVY, "ASIA": RED, "AFRICA": OCHRE, "AMERICAS": TEAL,
       "MIDDLE EAST": PURPLE, "OCEANIA": GREEN, "WORLD": GREY}

FD = "/usr/share/fonts/truetype/noto/"
_cache = {}
def F(name, size):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FD + name, size)
    return _cache[key]
def DISPLAY(size): return F("NotoSerifDisplay-Black.ttf", size)
def SERIF_B(size): return F("NotoSerif-Bold.ttf", size)
def SERIF(size): return F("NotoSerif-Regular.ttf", size)
def SERIF_I(size): return F("NotoSerif-Italic.ttf", size)
def SANS_B(size): return F("NotoSans-Bold.ttf", size)
def SANS(size): return F("NotoSans-Regular.ttf", size)

img = Image.new("RGB", (W, H), PAPER)
dr = ImageDraw.Draw(img, "RGBA")

def tw(text, font):
    return dr.textlength(text, font=font)

def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= width or not cur:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def text_block(x, y, text, font, fill, width, lh, max_lines=None, align="left"):
    lines = wrap(text, font, width)
    if max_lines: lines = lines[:max_lines]
    for i, ln in enumerate(lines):
        xx = x if align == "left" else x + (width - tw(ln, font)) / 2
        dr.text((xx, y + i * lh), ln, font=font, fill=fill)
    return y + len(lines) * lh

def spaced(x, y, text, font, fill, tracking=2):
    """Letter-spaced small caps line; returns end x."""
    for ch in text:
        dr.text((x, y), ch, font=font, fill=fill)
        x += tw(ch, font) + tracking
    return x

# ---------------------------------------------------------------- content
# (num, region, beat, status, source, headline, summary, art)
CARDS = [
 (1, "ASIA", "APEC SUMMIT", "CONFIRMED", "AP · REUTERS",
  "Trump, Xi and Putin hold first three-way summit",
  "Ninety minutes at APEC in Shenzhen yield a four-point Peace Declaration, "
  "but no deal on Ukraine or Iran. Trump calls Putin “my friend”.", "summit"),
 (2, "AMERICAS", "BUSINESS", "CONFIRMED", "REUTERS",
  "Anthropic’s $81bn IPO is the biggest ever",
  "The Claude maker prices at $83 a share, a $1.5 trillion value, and lists "
  "as ANT on Nasdaq — the first frontier-AI firm to go public, past "
  "SpaceX’s $75bn record.", "ipo"),
 (3, "MIDDLE EAST", "IRAN WAR", "CLAIMS", "REUTERS",
  "Iran fires on Kuwait after US strike on Qeshm",
  "Tehran answers the US strike on Qeshm Island. Trump warns Iran is "
  "“looking at” a dirty bomb and vows to “wipe them out”; Iran denies it.", "strait"),
 (4, "EUROPE", "UKRAINE WAR", "BOTH SIDES", "REUTERS",
  "Crimean Bridge hit a third time in a week",
  "Zelensky hails an “unprecedented” seven-stage strike; Moscow confirms "
  "the third attack on the span this week.", "bridge"),
 (5, "MIDDLE EAST", "GAZA", "", "REUTERS",
  "Israeli tanks push into central Gaza",
  "A rare incursion past the Yellow Line at Nuseirat. A strike on Nasser "
  "Hospital kills six, incl. a surgeon.", "gaza"),
 (6, "WORLD", "CLIMATE", "", "REUTERS · PANA",
  "COP31 endgame: fossil words fail again",
  "Final-stage talks split on “transition away” vs phaseout; the draft "
  "drops a $120bn adaptation target.", "cop"),
 (7, "WORLD", "THE HAGUE", "", "PANA",
  "World Court: Myanmar committed genocide",
  "The ICJ’s first ruling of its kind, in the Rohingya case brought by "
  "Gambia. Amnesty calls it historic.", "court"),
 (8, "AMERICAS", "US POLITICS", "", "AP",
  "US asks top court to lift TPS shield",
  "An emergency filing seeks to end restored protection for Venezuelan "
  "migrants while the case runs.", "tps"),
 (9, "WORLD", "CULTURE", "", "REUTERS",
  "GTA VI ends a 13-year wait at midnight",
  "Rollout starts in New Zealand; Metacritic 99 ties Ocarina of Time. "
  "Sensor Tower: 17m copies, $1.65bn early.", "gta"),
 (10, "ASIA", "NORTH KOREA", "", "IAEA",
  "IAEA: North Korea expands Yongbyon",
  "Grossi tells the board the enrichment plant is growing. Seoul’s Lee "
  "renews his call for dialogue.", "yongbyon"),
 (11, "EUROPE", "ARCTIC", "", "FOLKETING",
  "Denmark votes 109–0 on Greenland pact",
  "Parliament is unanimous for the Arctic security deal signed with "
  "Greenland and the United States.", "arctic"),
 (12, "AFRICA", "SUDAN", "", "AFRICANEWS",
  "Hemedti gets a second death sentence",
  "A Sudan court sentences the RSF leader again, over a $396m scandal, "
  "as his war grinds on.", "sudan"),
 (13, "OCEANIA", "WEATHER", "", "FIJI GOVT",
  "Fiji declares disaster over drought",
  "A nationwide El Niño declaration; emergency water goes to remote "
  "islands and farmers first.", "fiji"),
]

# (num, dateline, text, map dot col, row)
BRIEFS = [
 (14, "Manila", "US–Philippines $2bn+ defence loans", 90, 20),
 (15, "Tokyo", "Takaichi, Putin agree to keep talking", 96, 13),
 (16, "Jakarta", "asset-forfeiture law passes", 86, 26),
 (17, "Dhaka", "Yunus home torched amid shutdown", 81, 17),
 (18, "Kuala Lumpur", "UNHCR halts new asylum cases", 84, 23),
 (19, "Riyadh", "Houthi missile damages PIF Tower", 67, 16),
 (20, "Black Sea", "tanker Gas Husky sinks off Bulgaria", 62, 11),
 (21, "Pavlohrad", "boy, 11, dies after Russian strike", 66, 8),
 (22, "Rome", "parents jailed over son’s cancer care", 57, 11),
 (23, "London", "BAE cuts 1,070 jobs in defence boom", 52, 9),
 (24, "Washington", "gold at $3,720, a 14-month low", 27, 11),
 (25, "Paris", "datacentre emissions +70% by 2030 — IEA", 55, 10),
 (26, "Ceyhan", "Iraq restarts Kirkuk pipeline after 12y", 66, 12),
 (27, "Banjul", "Gambia declares mpox outbreak", 48, 20),
 (28, "Kinshasa", "NRC: Ebola response needs wider aid", 58, 25),
 (29, "Abuja", "$30m Afreximbank line for exporters", 55, 21),
 (30, "Mundri", "women plead for protection", 62, 22),
 (31, "Ouagadougou", "HRW: exile critics hunted", 53, 20),
 (32, "Bangui", "UN names CAR mission chief", 59, 23),
 (33, "Avarua", "Cyclone Xavier gale alerts", 4, 31),
 (34, "Buka", "Rio Tinto’s $250m mine-legacy fund", 101, 26),
 (35, "Turin", "Shelton edges Jodar 7-6(8) 7-5", 56, 9),
 (36, "London", "Chelsea 1-0 PSG: Buurman, 87’", 51, 8),
 (37, "Hobart", "Duckett ton seals England ODI series", 99, 37),
 (38, "Cardiff", "Wales stun the All Blacks", 51, 7),
 (39, "Las Vegas", "Hamilton denies Ferrari rift", 18, 13),
 (40, "Bentonville", "Walmart lifts outlook, sales +5.2%", 24, 13),
]

FIGURES = [
 ("3", "leaders at the first US–China–Russia summit table"),
 ("4", "points in Shenzhen’s Peace Declaration"),
 ("$81.3bn", "raised by Anthropic — the largest IPO ever"),
 ("589m", "children live in conflict zones, a record"),
 ("109–0", "Denmark’s vote for the Greenland pact"),
 ("99", "GTA VI’s Metacritic score, tying Ocarina of Time"),
]

# Dotted world map: row -> [(col_start, col_end)] land spans.
# Grid 111 cols x 42 rows; col ~ (lon+172)/3.24, row ~ (78-lat)/3.24.
LAND = {
 0: [(10,10),(14,14),(18,18),(22,22),(27,27),(40,45),(66,66),(72,72),(80,80),(90,90),(98,98)],
 1: [(2,8),(12,30),(39,47),(64,106)],
 2: [(1,9),(13,34),(40,46),(55,58),(60,107)],
 3: [(2,10),(12,36),(41,45),(54,60),(61,107)],
 4: [(3,10),(11,37),(48,48),(54,61),(62,107)],
 5: [(4,11),(10,38),(50,51),(53,107)],
 6: [(9,37),(50,52),(53,62),(63,106)],
 7: [(10,36),(50,52),(52,64),(65,105)],
 8: [(10,35),(51,63),(64,100)],
 9: [(11,34),(50,62),(63,98)],
 10: [(11,33),(49,61),(66,68),(70,95)],
 11: [(12,33),(49,60),(60,66),(68,93)],
 12: [(12,32),(49,52),(55,57),(58,59),(60,65),(67,92)],
 13: [(13,31),(50,58),(62,69),(68,73),(74,79),(80,92)],
 14: [(14,29),(49,66),(64,69),(70,76),(75,79),(81,90)],
 15: [(15,24),(48,65),(63,68),(75,78),(82,86),(90,90)],
 16: [(16,22),(47,64),(60,65),(75,78),(83,87),(89,91)],
 17: [(17,20),(47,63),(76,77),(83,87),(89,90)],
 18: [(19,22),(47,62),(83,86)],
 19: [(28,34),(48,61),(85,88)],
 20: [(28,36),(49,61),(78,78),(84,95)],
 21: [(29,37),(50,60),(84,97)],
 22: [(30,38),(51,60),(85,98),(99,101)],
 23: [(30,39),(52,60),(86,99),(100,102)],
 24: [(31,40),(53,61),(87,96)],
 25: [(31,41),(54,62),(88,94)],
 26: [(32,41),(55,63)],
 27: [(32,41),(55,64),(89,89),(91,91),(94,94),(97,97)],
 28: [(33,41),(56,64),(67,67),(88,100)],
 29: [(33,40),(56,64),(67,68),(88,101)],
 30: [(33,39),(57,64),(67,67),(89,101),(108,108)],
 31: [(33,38),(57,63),(90,100)],
 32: [(33,37),(57,62),(91,99)],
 33: [(33,37),(58,61),(92,98)],
 34: [(33,36),(58,60),(93,97),(104,105)],
 35: [(33,36),(94,96),(103,105)],
 36: [(33,35),(103,104)],
 37: [(33,35),(102,103)],
 38: [(33,34)],
 39: [(33,34)],
 40: [(33,33)],
 41: [(33,33)],
}
# Card pins: num -> (col, row) on the same grid (slightly displaced for legibility)
PINS = {1: (88, 17), 2: (15, 12), 3: (69, 15), 4: (64, 10), 5: (63, 14),
        6: (60, 13), 7: (54, 8), 8: (29, 12), 9: (28, 16), 10: (92, 12),
        11: (58, 6), 12: (63, 19), 13: (108, 30)}
PIN_REGION = {1: "ASIA", 2: "AMERICAS", 3: "MIDDLE EAST", 4: "EUROPE",
              5: "MIDDLE EAST", 6: "WORLD", 7: "EUROPE", 8: "AMERICAS",
              9: "WORLD", 10: "ASIA", 11: "EUROPE", 12: "AFRICA", 13: "OCEANIA"}

# ---------------------------------------------------------------- art
def star(cx, cy, r, fill, outline=None):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    dr.polygon(pts, fill=fill, outline=outline)

def flag_us(x, y, w, h):
    for i in range(7):
        if i % 2 == 0:
            dr.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7], fill=(178, 34, 52))
    dr.rectangle([x, y, x + w * 0.42, y + h * 4 / 7], fill=(30, 40, 110))
    for r in range(3):
        for c in range(4):
            dr.ellipse([x + 3 + c * w * 0.1, y + 2 + r * h * 0.16,
                        x + 5 + c * w * 0.1, y + 4 + r * h * 0.16], fill=(255, 255, 255))

def flag_cn(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(x + w * 0.2, y + h * 0.28, h * 0.2, (255, 222, 0))

def flag_ru(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h / 3], fill=(245, 245, 245))
    dr.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    dr.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 43, 30))

def flag_dk(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(200, 30, 45))
    dr.rectangle([x + w * 0.28, y, x + w * 0.4, y + h], fill=(255, 255, 255))
    dr.rectangle([x, y + h * 0.42, x + w, y + h * 0.58], fill=(255, 255, 255))

def art_summit(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(196, 214, 228))
    for bx, bw, bh in [(0.03, 0.1, 0.5), (0.16, 0.07, 0.34), (0.78, 0.09, 0.44), (0.9, 0.08, 0.6)]:
        dr.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h], fill=(90, 110, 140))
    dr.ellipse([x + w * 0.34, y + h * 0.68, x + w * 0.66, y + h * 1.05], fill=(150, 96, 40))
    fw, fh = w * 0.17, h * 0.42
    for i, fn in enumerate((flag_us, flag_cn, flag_ru)):
        fx = x + w * (0.22 + i * 0.24)
        dr.line([fx + fw / 2, y + h * 0.1, fx + fw / 2, y + h * 0.72], fill=(60, 60, 60), width=2)
        fn(fx, y + h * 0.1, fw, fh)

def art_ipo(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(16, 30, 58))
    base = y + h * 0.88
    for i, bh in enumerate((0.25, 0.42, 0.6, 0.85)):
        bx = x + w * (0.08 + i * 0.17)
        dr.rectangle([bx, base - h * bh, bx + w * 0.11, base], fill=(64, 145, 220))
    pts = [(x + w * (0.1 + i * 0.17), base - h * v) for i, v in enumerate((0.3, 0.47, 0.65, 0.92))]
    dr.line(pts, fill=GOLD, width=3)
    dr.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 9, pts[-1][1] + 2), (pts[-1][0] - 2, pts[-1][1] + 9)], fill=GOLD)
    dr.rounded_rectangle([x + w * 0.72, y + h * 0.1, x + w * 0.95, y + h * 0.36], 4, fill=GOLD)
    t = "ANT"; dr.text((x + w * 0.835 - tw(t, SANS_B(13)) / 2, y + h * 0.13), t, font=SANS_B(13), fill=(16, 30, 58))

def art_strait(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(214, 200, 160))
    dr.rectangle([x, y + h * 0.62, x + w, y + h], fill=(38, 110, 130))
    for i in range(3):
        yy = y + h * (0.7 + i * 0.1)
        for xx in range(int(x + 6), int(x + w - 16), 26):
            dr.arc([xx, yy, xx + 16, yy + 7], 180, 360, fill=(180, 220, 230), width=2)
    cx, cy = x + w * 0.5, y + h * 0.3
    dr.polygon([(cx - 16, cy), (cx + 16, cy), (cx + 8, cy + 7), (cx - 8, cy + 7)], fill=(40, 40, 46))
    for dx, dy in [(-20, -8), (20, -8), (-20, 10), (20, 10)]:
        dr.line([cx, cy + 3, cx + dx, cy + dy], fill=(40, 40, 46), width=2)
        dr.ellipse([cx + dx - 4, cy + dy - 2, cx + dx + 4, cy + dy + 2], outline=(40, 40, 46), width=2)
    for r in (12, 20, 28):
        dr.arc([x + w * 0.08 - r, y + h * 0.62 - r, x + w * 0.08 + r, y + h * 0.62 + r], 300, 360, fill=RED, width=2)

def art_bridge(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(188, 208, 224))
    dr.rectangle([x, y + h * 0.72, x + w, y + h], fill=(52, 104, 140))
    deck = y + h * 0.52
    dr.line([x, deck, x + w * 0.44, deck], fill=(50, 54, 60), width=4)
    dr.line([x + w * 0.6, deck + h * 0.1, x + w, deck + h * 0.1], fill=(50, 54, 60), width=4)
    dr.line([x + w * 0.44, deck, x + w * 0.6, deck + h * 0.16], fill=(50, 54, 60), width=3)
    for fx in (0.12, 0.3):
        dr.line([x + w * fx, deck - h * 0.26, x + w * fx, deck], fill=(50, 54, 60), width=3)
        dr.line([x + w * fx, deck - h * 0.26, x + w * (fx + 0.14), deck], fill=(50, 54, 60), width=1)
        dr.line([x + w * fx, deck - h * 0.26, x + w * (fx - 0.1), deck], fill=(50, 54, 60), width=1)
    star(x + w * 0.52, y + h * 0.3, h * 0.2, (240, 130, 30), (200, 60, 20))
    star(x + w * 0.52, y + h * 0.3, h * 0.1, (250, 200, 60))

def art_gaza(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(216, 198, 164))
    dr.rectangle([x, y + h * 0.8, x + w, y + h], fill=(168, 142, 104))
    bx, by = x + w * 0.62, y + h * 0.16
    dr.rectangle([bx, by, bx + w * 0.3, by + h * 0.6], fill=(226, 222, 212))
    dr.rectangle([bx + w * 0.11, by + h * 0.12, bx + w * 0.19, by + h * 0.44], fill=RED)
    dr.rectangle([bx + w * 0.065, by + h * 0.22, bx + w * 0.235, by + h * 0.34], fill=RED)
    tx, ty = x + w * 0.1, y + h * 0.58
    dr.rectangle([tx, ty, tx + w * 0.34, ty + h * 0.16], fill=(74, 78, 56))
    dr.rectangle([tx + w * 0.08, ty - h * 0.12, tx + w * 0.22, ty], fill=(74, 78, 56))
    dr.line([tx + w * 0.2, ty - h * 0.06, tx + w * 0.46, ty - h * 0.16], fill=(50, 52, 40), width=4)
    for i in range(4):
        dr.ellipse([tx + i * w * 0.085, ty + h * 0.15, tx + i * w * 0.085 + w * 0.07, ty + h * 0.3], fill=(50, 52, 40))

def art_cop(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(196, 226, 214))
    cx, cy, r = x + w * 0.34, y + h * 0.52, h * 0.34
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 200))
    dr.polygon([(cx - r * 0.6, cy - r * 0.3), (cx - r * 0.1, cy - r * 0.5), (cx - r * 0.2, cy + r * 0.1), (cx - r * 0.55, cy + r * 0.2)], fill=(80, 170, 90))
    dr.polygon([(cx + r * 0.2, cy + r * 0.3), (cx + r * 0.65, cy + r * 0.15), (cx + r * 0.6, cy + r * 0.6), (cx + r * 0.25, cy + r * 0.62)], fill=(80, 170, 90))
    tx = x + w * 0.74
    dr.rectangle([tx, y + h * 0.14, tx + w * 0.07, y + h * 0.74], fill=(240, 244, 246), outline=(90, 90, 90))
    dr.rectangle([tx + 1, y + h * 0.3, tx + w * 0.07 - 1, y + h * 0.74], fill=RED)
    dr.ellipse([tx - w * 0.035, y + h * 0.68, tx + w * 0.105, y + h * 0.94], fill=RED)
    dr.text((x + w * 0.83, y + h * 0.3), "1.5°", font=SANS_B(12), fill=RED)

def art_court(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(228, 222, 204))
    cx = x + w * 0.5
    dr.line([cx, y + h * 0.12, cx, y + h * 0.8], fill=(90, 74, 40), width=3)
    dr.line([x + w * 0.2, y + h * 0.2, x + w * 0.8, y + h * 0.2], fill=(90, 74, 40), width=3)
    for px in (x + w * 0.2, x + w * 0.8):
        dr.line([px, y + h * 0.2, px - w * 0.07, y + h * 0.52], fill=(90, 74, 40), width=1)
        dr.line([px, y + h * 0.2, px + w * 0.07, y + h * 0.52], fill=(90, 74, 40), width=1)
        dr.pieslice([px - w * 0.09, y + h * 0.44, px + w * 0.09, y + h * 0.62], 0, 180, fill=(150, 120, 60))
    dr.rectangle([cx - w * 0.1, y + h * 0.8, cx + w * 0.1, y + h * 0.88], fill=(90, 74, 40))
    star(cx, y + h * 0.1, 5, GOLD)

def art_tps(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(206, 216, 230))
    bx, bw = x + w * 0.14, w * 0.56
    dr.polygon([(bx, y + h * 0.3), (bx + bw / 2, y + h * 0.08), (bx + bw, y + h * 0.3)], fill=(240, 242, 246), outline=(90, 100, 120))
    for i in range(4):
        cx = bx + bw * (0.1 + i * 0.24)
        dr.rectangle([cx, y + h * 0.34, cx + bw * 0.1, y + h * 0.78], fill=(240, 242, 246), outline=(90, 100, 120))
    dr.rectangle([bx - w * 0.02, y + h * 0.78, bx + bw + w * 0.02, y + h * 0.86], fill=(240, 242, 246), outline=(90, 100, 120))
    sx, sy = x + w * 0.8, y + h * 0.34
    dr.polygon([(sx, sy), (sx + w * 0.11, sy + h * 0.08), (sx + w * 0.11, sy + h * 0.3),
                (sx + w * 0.055, sy + h * 0.44), (sx, sy + h * 0.3)], fill=RED)
    star(sx + w * 0.055, sy + h * 0.18, 5, (255, 255, 255))

def art_gta(x, y, w, h):
    for i, col in enumerate([(64, 32, 92), (140, 44, 96), (214, 92, 60), (246, 160, 70)]):
        dr.rectangle([x, y + h * i / 4, x + w, y + h * (i + 1) / 4], fill=col)
    dr.ellipse([x + w * 0.4, y + h * 0.34, x + w * 0.6, y + h * 0.62], fill=(252, 210, 110))
    dr.rectangle([x, y + h * 0.78, x + w, y + h], fill=(30, 20, 44))
    px = x + w * 0.14
    dr.line([px, y + h, px + w * 0.03, y + h * 0.4], fill=(24, 16, 34), width=4)
    for ang in (-0.7, -0.25, 0.2, 0.65):
        ex = px + w * 0.03 + math.cos(ang - 1.2) * w * 0.11
        ey = y + h * 0.4 + math.sin(ang - 1.2) * h * 0.2
        dr.line([px + w * 0.03, y + h * 0.4, ex, ey], fill=(24, 16, 34), width=3)
    gx, gy = x + w * 0.58, y + h * 0.6
    dr.rounded_rectangle([gx, gy, gx + w * 0.3, gy + h * 0.26], 9, fill=(24, 22, 34))
    dr.rectangle([gx + w * 0.05, gy + h * 0.1, gx + w * 0.11, gy + h * 0.16], fill=(220, 220, 230))
    dr.rectangle([gx + w * 0.07, gy + h * 0.08, gx + w * 0.09, gy + h * 0.18], fill=(220, 220, 230))
    for dx, dy, col in [(0.22, 0.09, RED), (0.25, 0.14, GOLD), (0.19, 0.14, TEAL)]:
        dr.ellipse([gx + w * dx, gy + h * dy, gx + w * dx + 5, gy + h * dy + 5], fill=col)

def art_yongbyon(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(210, 216, 208))
    tx, ty = x + w * 0.16, y + h * 0.2
    dr.polygon([(tx, ty + h * 0.66), (tx + w * 0.07, ty), (tx + w * 0.17, ty), (tx + w * 0.24, ty + h * 0.66)], fill=(150, 152, 148), outline=(100, 102, 98))
    dr.ellipse([tx + w * 0.05, ty - h * 0.05, tx + w * 0.19, ty + h * 0.06], fill=(190, 192, 188))
    cx, cy = x + w * 0.68, y + h * 0.5
    for deg in (0, 60, 120):
        phi = math.radians(deg)
        pts = []
        for i in range(41):
            t = 2 * math.pi * i / 40
            # ellipse semi-axes a (x) and b (y), rotated by phi
            ex, ey = w * 0.2 * math.cos(t), h * 0.12 * math.sin(t)
            pts.append((cx + ex * math.cos(phi) - ey * math.sin(phi),
                        cy + ex * math.sin(phi) + ey * math.cos(phi)))
        dr.line(pts, fill=(200, 60, 40), width=2)
    dr.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(200, 60, 40))

def art_arctic(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(186, 216, 236))
    dr.rectangle([x, y + h * 0.7, x + w, y + h], fill=(120, 178, 214))
    dr.polygon([(x + w * 0.06, y + h * 0.72), (x + w * 0.2, y + h * 0.42), (x + w * 0.34, y + h * 0.72)], fill=(248, 252, 255), outline=(140, 180, 210))
    dr.polygon([(x + w * 0.42, y + h * 0.74), (x + w * 0.55, y + h * 0.52), (x + w * 0.66, y + h * 0.74)], fill=(248, 252, 255), outline=(140, 180, 210))
    px, py = x + w * 0.8, y + h * 0.16
    dr.line([px, py, px, py + h * 0.52], fill=(70, 70, 70), width=2)
    flag_dk(px, py, w * 0.16, h * 0.3)

def art_sudan(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(232, 216, 188))
    gx, gy = x + w * 0.3, y + h * 0.3
    dr.polygon([(gx, gy), (gx + w * 0.2, gy + h * 0.1), (gx + w * 0.16, gy + h * 0.22), (gx - w * 0.04, gy + h * 0.12)], fill=(120, 84, 40))
    dr.line([gx + w * 0.14, gy + h * 0.16, gx + w * 0.42, gy + h * 0.5], fill=(120, 84, 40), width=5)
    dr.rectangle([x + w * 0.14, y + h * 0.74, x + w * 0.5, y + h * 0.82], fill=(120, 84, 40))
    dr.rectangle([x + w * 0.62, y + h * 0.2, x + w * 0.68, y + h * 0.7], fill=(90, 74, 40))
    dr.pieslice([x + w * 0.53, y + h * 0.6, x + w * 0.77, y + h * 0.84], 0, 180, fill=(150, 120, 60))

def art_fiji(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(170, 216, 232))
    dr.ellipse([x + w * 0.74, y + h * 0.08, x + w * 0.94, y + h * 0.36], fill=(250, 200, 80))
    dr.rectangle([x, y + h * 0.66, x + w, y + h], fill=(214, 188, 138))
    dr.polygon([(x + w * 0.1, y + h * 0.68), (x + w * 0.34, y + h * 0.5), (x + w * 0.58, y + h * 0.68)], fill=(226, 204, 152))
    for sx, ex in [(0.16, 0.3), (0.4, 0.52), (0.62, 0.78)]:
        dr.line([x + w * sx, y + h * 0.82, x + w * (sx + 0.05), y + h * 0.9, x + w * ex, y + h * 0.86], fill=(150, 116, 70), width=2)
    px = x + w * 0.82
    dr.line([px, y + h * 0.68, px + w * 0.02, y + h * 0.3], fill=(90, 70, 44), width=3)
    for ang in (-0.8, -0.35, 0.1, 0.55):
        ex = px + w * 0.02 + math.cos(ang - 1.2) * w * 0.13
        ey = y + h * 0.3 + math.sin(ang - 1.2) * h * 0.22
        dr.line([px + w * 0.02, y + h * 0.3, ex, ey], fill=(52, 130, 66), width=3)

ART = {"summit": art_summit, "ipo": art_ipo, "strait": art_strait, "bridge": art_bridge,
       "gaza": art_gaza, "cop": art_cop, "court": art_court, "tps": art_tps,
       "gta": art_gta, "yongbyon": art_yongbyon, "arctic": art_arctic,
       "sudan": art_sudan, "fiji": art_fiji}

# ---------------------------------------------------------------- charts
def chart_wall_st(x, y, w, h):
    dr.text((x, y), "WALL STREET · THU (REUTERS)", font=SANS_B(10), fill=INK)
    rows = [("Dow", -0.97, RED), ("S&P 500", -0.41, RED), ("Nasdaq", 0.01, GREEN)]
    zero = x + w * 0.52
    dr.line([zero, y + 12, zero, y + h - 1], fill=(150, 145, 130), width=1)
    for i, (lab, v, col) in enumerate(rows):
        yy = y + 13 + i * 10.5
        dr.text((x, yy), lab, font=SANS(9.5), fill=INK)
        bw = abs(v) / 1.0 * (w * 0.34)
        if v < 0:
            dr.rectangle([zero - bw, yy + 1, zero, yy + 8], fill=col)
            dr.text((zero - bw - 30, yy), f"{v:.2f}", font=SANS_B(9), fill=col)
        else:
            dr.rectangle([zero, yy + 1, zero + max(bw, 2), yy + 8], fill=col)
            dr.text((zero + 4, yy), "+0.01", font=SANS_B(9), fill=col)

def chart_ipos(x, y, w, h):
    dr.text((x, y), "BIGGEST IPOs EVER ($BN)", font=SANS_B(10), fill=INK)
    for i, (lab, v, col) in enumerate((("Anthropic ’26", 81.3, NAVY), ("SpaceX ’26", 75.0, (150, 148, 140)))):
        yy = y + 15 + i * 14
        dr.text((x, yy - 3), lab, font=SANS(9.5), fill=INK)
        bw = v / 85 * (w * 0.52)
        dr.rectangle([x + w * 0.34, yy, x + w * 0.34 + bw, yy + 9], fill=col)
        dr.text((x + w * 0.34 + bw + 5, yy - 3), f"{v:.1f}", font=SANS_B(9.5), fill=INK)

def chart_oil(x, y, w, h):
    dr.text((x, y), "OIL · THU (REUTERS)", font=SANS_B(10), fill=INK)
    for i, (lab, v, pct) in enumerate((("Brent", 92.54, "+0.6%"), ("WTI", 84.30, "+1.3%"))):
        yy = y + 15 + i * 14
        dr.text((x, yy - 3), lab, font=SANS(9.5), fill=INK)
        bw = v / 100 * (w * 0.44)
        dr.rectangle([x + w * 0.2, yy, x + w * 0.2 + bw, yy + 9], fill=GOLD)
        dr.text((x + w * 0.2 + bw + 5, yy - 3), f"${v:.2f} {pct}", font=SANS_B(9.5), fill=INK)

# ---------------------------------------------------------------- page
M = 18
CW = W - 2 * M  # 988

def masthead():
    dr.rectangle([M, 12, M + 100, 96], fill=RED)
    dr.text((M + 50 - tw("19", DISPLAY(46)) / 2, 16), "19", font=DISPLAY(46), fill=(255, 255, 255))
    dr.text((M + 50 - tw("NOV", SANS_B(15)) / 2, 64), "NOV", font=SANS_B(15), fill=(255, 255, 255))
    dr.text((M + 50 - tw("THU · 2026", SANS_B(10)) / 2, 81), "THU · 2026", font=SANS_B(10), fill=(255, 235, 220))
    x = 132
    spaced(x, 15, "THE DAILY FRAME · THE DAY IN WORLD NEWS", SANS_B(13), RED, 2)
    dr.text((x, 34), "Thursday 19 November 2026", font=DISPLAY(42), fill=INK)
    dr.text((x, 80), "Everything on this page happened, or was first reported, on Thursday 19 November 2026.",
            font=SERIF_I(13), fill=(70, 66, 58))
    bx = 812
    dr.rectangle([bx, 12, 1006, 96], fill=NAVY)
    for i, t in enumerate(("40 STORIES", "7 REGIONS", "ONE PAGE")):
        dr.text((bx + 97 - tw(t, SANS_B(16)) / 2, 20 + i * 26), t, font=SANS_B(16), fill=(255, 255, 255))
        if i < 2:
            dr.line([bx + 18, 41 + i * 26, 988, 41 + i * 26], fill=(90, 116, 160), width=1)
    dr.line([M, 102, 1006, 102], fill=INK, width=3)
    dr.line([M, 106, 1006, 106], fill=INK, width=1)

def tally():
    y0, y1 = 110, 130
    parts = [("EUROPE", 10), ("ASIA", 7), ("AFRICA", 7), ("AMERICAS", 5),
             ("MIDDLE EAST", 4), ("OCEANIA", 4), ("WORLD", 3)]
    x = M
    for name, n in parts:
        wseg = CW * n / 40
        dr.rectangle([x, y0, x + wseg - 2, y1], fill=REG[name])
        t = f"{name} {n}"
        dr.text((x + wseg / 2 - tw(t, SANS_B(12)) / 2, y0 + 4), t, font=SANS_B(12), fill=(255, 255, 255))
        x += wseg

def numbers_panel():
    y0, y1 = 136, 267
    dr.rectangle([M, y0, 1006, y1], fill=(255, 253, 246), outline=LINE)
    spaced(M + 12, y0 + 7, "THE DAY IN NUMBERS", SANS_B(13), RED, 2)
    note = "— drawn, not just told"
    dr.text((1006 - 12 - tw(note, SERIF_I(12)), y0 + 7), note, font=SERIF_I(12), fill=FAINT)
    colw = CW / 6
    for i, (num, cap) in enumerate(FIGURES):
        x = M + i * colw + 12
        dr.text((x, y0 + 23), num, font=DISPLAY(27), fill=NAVY if i % 2 == 0 else RED)
        text_block(x, y0 + 52, cap, SANS(9.5), (70, 66, 58), colw - 22, 11, max_lines=3)
    dr.line([M + 12, y0 + 79, 994, y0 + 79], fill=LINE, width=1)
    cw3 = (CW - 24) / 3
    chart_wall_st(M + 12, y0 + 83, cw3 - 14, 44)
    chart_ipos(M + 12 + cw3, y0 + 83, cw3 - 14, 44)
    chart_oil(M + 12 + 2 * cw3, y0 + 83, cw3 - 14, 44)

def card(x, y, w, h, data, big):
    num, region, beat, status, source, head, summ, art = data
    dr.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=LINE)
    art_h = 76 if big else 46
    ART[art](x + 1, y + 1, w - 2, art_h)
    ty = y + art_h + 7
    col = REG[region]
    dr.rectangle([x + 8, ty, x + 26, ty + 15], fill=col)
    dr.text((x + 17 - tw(str(num), SANS_B(10)) / 2, ty + 2), str(num), font=SANS_B(10), fill=(255, 255, 255))
    dr.text((x + 31, ty + 2), f"{region} · {beat}", font=SANS_B(9.5), fill=col)
    right = (status + " · " if status else "") + source
    dr.text((x + w - 8 - tw(right, SANS(8.5)), ty + 2), right, font=SANS(8.5), fill=FAINT)
    hy = ty + 19
    hy = text_block(x + 8, hy, head, SERIF_B(19 if big else 15), INK, w - 16, 22 if big else 17, max_lines=2)
    text_block(x + 8, hy + 1, summ, SERIF(11.5 if big else 10.3), (52, 50, 44), w - 16, 13.5 if big else 12,
               max_lines=3)

def cards():
    y = 273; gap = 10
    w3 = (CW - 2 * gap) / 3
    for i in range(3):
        card(M + i * (w3 + gap), y, w3, 194, CARDS[i], big=True)
    y2 = 473; gap2 = 8
    w5 = (CW - 4 * gap2) / 5
    for i in range(5):
        card(M + i * (w5 + gap2), y2, w5, 146, CARDS[3 + i], big=False)
    y3 = 625
    for i in range(5):
        card(M + i * (w5 + gap2), y3, w5, 146, CARDS[8 + i], big=False)

def bezier(p0, p1, p2, n=42):
    pts = []
    for i in range(n + 1):
        t = i / n
        xx = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        yy = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((xx, yy))
    return pts

def map_and_briefs():
    y0 = 777
    spaced(M, y0, "WHERE IT HAPPENED", SANS_B(13), INK, 1)
    note = "— the summit routes into Shenzhen (star), dashed"
    dr.text((M + 196, y0 + 1), note, font=SERIF_I(11), fill=FAINT)
    bx = 474
    dr.text((bx, y0), "ALSO ON THURSDAY 19 NOVEMBER", font=SANS_B(13), fill=RED)
    dr.text((bx + tw("ALSO ON THURSDAY 19 NOVEMBER", SANS_B(13)) + 8, y0 + 1), "— 27 more stories",
            font=SERIF_I(11), fill=FAINT)
    mx, my = M, y0 + 20
    px_, py_ = 4.0, 3.7
    def cell(c, r):
        return mx + c * px_, my + r * py_
    for r, spans in LAND.items():
        for a, b in spans:
            for c in range(a, b + 1):
                xx, yy = cell(c, r)
                dr.ellipse([xx - 1.3, yy - 1.3, xx + 1.3, yy + 1.3], fill=(148, 158, 178))
    shenzhen = cell(*PINS[1])
    for start, ctrl in [(cell(*PINS[8]), (mx + 58 * px_, my - 8 * py_)),
                        (cell(64, 6), (mx + 80 * px_, my - 1 * py_))]:
        pts = bezier(start, ctrl, shenzhen)
        for i in range(0, len(pts) - 1, 2):
            dr.line([pts[i], pts[i + 1]], fill=RED, width=2)
    for _, _, _, c, r in BRIEFS:
        xx, yy = cell(c, r)
        dr.ellipse([xx - 1.7, yy - 1.7, xx + 1.7, yy + 1.7], fill=(70, 84, 110))
    for num, (c, r) in PINS.items():
        xx, yy = cell(c, r)
        if num == 1:
            star(xx, yy, 9, GOLD, RED)
            dr.text((xx + 10, yy - 6), "1", font=SANS_B(10), fill=RED)
        else:
            col = REG[PIN_REGION[num]]
            dr.ellipse([xx - 6.5, yy - 6.5, xx + 6.5, yy + 6.5], fill=col, outline=(255, 255, 255), width=1)
            dr.text((xx - tw(str(num), SANS_B(8)) / 2, yy - 5), str(num), font=SANS_B(8), fill=(255, 255, 255))
    dr.text((mx, my + 42 * py_ + 3), "Numbered pins: stories 1–13 · dots: briefs 14–40 · positions approximate",
            font=SERIF_I(9.5), fill=FAINT)
    # briefs in two columns
    colw = 258
    for ci, group in enumerate((BRIEFS[:14], BRIEFS[14:])):
        x = bx + ci * (colw + 14)
        yy = y0 + 19
        for num, dateline, text, _, _ in group:
            dr.text((x, yy), f"{num}", font=SANS_B(10), fill=RED)
            line = f"{dateline}: {text}"
            yy = text_block(x + 22, yy, line, SERIF(10), INK, colw - 22, 12.4, max_lines=2)
            yy += 0.5

def date_check_and_footer():
    y0 = 980
    dr.rectangle([M, y0, 1006, y0 + 27], outline=RED, width=1)
    dr.text((M + 8, y0 + 4), "DATE CHECK", font=SANS_B(9.5), fill=RED)
    msg = ("Left out on purpose — each was first reported on Wednesday 18 November: Alcaraz’s win over Medvedev · "
           "the Kemerovo An-12 crash · Ebola cases doubling in DR Congo · UK inflation at 3.6% · Voyager 1 at one light-day. "
           "Not yet happened: COP31’s closing text (Fri) · Anthropic’s first close · GTA VI’s first-week sales.")
    text_block(M + 76, y0 + 4, msg, SERIF(9.5), (70, 66, 58), CW - 88, 11.5, max_lines=2)
    dr.text((M, 1012), "Sources: Reuters · AP · AFP · Xinhua · IAEA · PANA · Africanews · Sensor Tower",
            font=SANS(9), fill=FAINT)
    right = "All 40 stories happened, or were first reported, on Thursday 19 November 2026. Original drawings."
    dr.text((1006 - tw(right, SANS(9)), 1012), right, font=SANS(9), fill=FAINT)

def main():
    masthead(); tally(); numbers_panel(); cards(); map_and_briefs(); date_check_and_footer()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    main()
