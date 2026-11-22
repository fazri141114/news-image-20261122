#!/usr/bin/env python3
"""Builder for the make.fun entry "Sum up 22 November's world news in
one image" (news-image-20261122), by @fazri141114.

Draws a one-page illustrated broadsheet, THE WORLD IN ONE DAY, in the
format the top of this contest's leaderboard shares: a dated serif
masthead, a stat strip, three illustrated heroes, ten numbered grid
stories, a dotted world map and a numbered brief list — 35 stories,
every one first reported on Sunday 22 November 2026 in at least one
time zone. All text is rendered by this program (Pillow), so every
word is crisp; the panels are flat original drawings made here.

Run locally:  python3 build_image_22.py   ->  writes entry.png
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 40)
MUTE = (96, 90, 78)
RED = (178, 44, 38)
NAVY = (18, 38, 63)
TEAL = (36, 110, 100)
GOLD = (176, 124, 32)
WHITE = (255, 255, 255)

FD = "/usr/share/fonts/truetype/noto/"
SERIF_B = FD + "NotoSerif-Bold.ttf"
SERIF_R = FD + "NotoSerif-Regular.ttf"
SERIF_I = FD + "NotoSerif-Italic.ttf"
SANS_B = FD + "NotoSans-Bold.ttf"
SANS_R = FD + "NotoSans-Regular.ttf"
SANS_I = FD + "NotoSans-Italic.ttf"

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


img = Image.new("RGB", (W, H), PAPER)
dr = ImageDraw.Draw(img)


def tw(text, font):
    return dr.textlength(text, font=font)


def wrap(text, font, width):
    """Greedy word wrap to a pixel width; returns the list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if tw(trial, font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(text, font_path, size, width, min_size=9):
    """Shrink a font until the text fits one line; returns (font, text)."""
    while size > min_size and tw(text, F(font_path, size)) > width:
        size -= 1
    return F(font_path, size), text


def text(x, y, s, font, fill=INK, anchor="la"):
    dr.text((x, y), s, font=font, fill=fill, anchor=anchor)


def block(x, y, s, font, width, leading, fill=INK, max_lines=None):
    """Wrapped paragraph; returns the y just below it."""
    lines = wrap(s, font, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        dr.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def chip(x, y, n, r=9):
    """Numbered story badge: a filled circle with a white number."""
    dr.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    f = F(SANS_B, 11 if r >= 9 else 9)
    dr.text((x, y), str(n), font=f, fill=WHITE, anchor="mm")


def banner(x, y, w, label, fill, size=13):
    """Coloured headline banner across the top of a picture panel."""
    f, label = fit(label, SANS_B, size, w - 14)
    dr.rectangle([x, y, x + w, y + size + 11], fill=fill)
    dr.text((x + 7, y + 5), label, font=f, fill=WHITE)


def tag_row(x, y, n, tag, status):
    chip(x + 9, y + 8, n)
    text(x + 24, y, tag, F(SANS_B, 10.5), RED)
    f = F(SANS_B, 9.5)
    label = "✓ " + status
    dr.rectangle([x + 24, y + 14, x + 28 + tw(label, f), y + 28], outline=TEAL, width=1)
    text(x + 26, y + 16, label, f, TEAL)


# ---------------------------------------------------------------- stories
# (banner, tag, status, headline, deck) — heroes first, then the grid.
HEROES = [
    ("COP31: DEAL CLOSE", "ANTALYA, TÜRKIYE · CLIMATE", "CONFIRMED",
     "COP31 climate talks close in on a final deal",
     "A new package lands after a fight over fossil fuels; delegations "
     "have until 03:00 GMT to object before a final plenary. (Reuters, BBC)"),
    ("UKRAINE: BARRAGE", "KYIV, UKRAINE · WAR", "OFFICIALS' COUNT",
     "Russia fires 400 drones and 110 missiles",
     "One of the war's largest overnight attacks; at least seven people "
     "are killed in Kyiv. (Al Jazeera)"),
    ("BAHRAIN: STRUCK", "MANAMA, BAHRAIN · IRAN WAR", "CONFIRMED",
     "Iran strikes US bases in Bahrain",
     "An industrial site burns and no one is hurt; the IRGC says it hit "
     "two Patriot radars. Two tankers are hit in Hormuz. (Reuters, Al Jazeera)"),
]

GRID = [
    ("SHIP ABLAZE", "GULF OF FINLAND · WAR", "CONFIRMED",
     "Russian cargo ship burns after drone strike",
     "Finland says Ukraine was likely behind it. (BBC)"),
    ("HOME CITY HIT", "KRYVYI RIH · UKRAINE", "OFFICIALS'",
     "Strike hits Zelensky's home city",
     "Russian strike on the central city; 2 dead, dozens hurt. (Al Jazeera)"),
    ("BOAT CAPSIZES", "BAYELSA, NIGERIA · DISASTER", "REPORTED",
     "Boat carrying mourners capsizes",
     "Passengers were going to a funeral; 24 dead. (DW, Sky News)"),
    ("COALITION TALKS", "JERUSALEM · POLITICS", "OFFICIAL",
     "Eisenkot invites Likud to talks",
     "He seeks the broadest possible government. (Straits Times)"),
    ("AID VEHICLE HIT", "GAZA · CEASEFIRE", "CONFIRMED",
     "Strike hits food aid vehicle",
     "Three Palestinians die in an air attack. (Al Jazeera, Reuters)"),
    ("CAPTURED", "SINALOA, MEXICO · CRIME", "CONFIRMED",
     "'El Chapo Isidro' caught; violence follows",
     "FBI top-ten fugitive held after a shoot-out. (Sky News, BBC)"),
    ("POWER CUTS", "TEHRAN, IRAN · ENERGY", "REPORTED",
     "Iran to ration electricity",
     "War damage hits the energy network. (Straits Times)"),
    ("SEC PROBE", "WASHINGTON · TECH", "REPORTED",
     "Nvidia faces US accounting probe",
     "The SEC inquiry is at an early stage. (Straits Times)"),
    ("BOLSONARO: ICU", "BRASILIA, BRAZIL · HEALTH", "CONFIRMED",
     "Bolsonaro in intensive care",
     "Ex-president stable, breathing on his own. (Al Jazeera, Reuters)"),
    ("AUKUS ROW", "CANBERRA · DEFENCE", "OFFICIAL",
     "Marles rejects US report on AUKUS subs",
     "He says the budget office is wrong. (ABC, Reuters)"),
]

BRIEFS = [
    ("FBI", "probes apparent hack of its crime database (BBC)"),
    ("US", "Teen gamer and mother help FBI rescue a girl (BBC)"),
    ("Saudi Arabia", "Air defences down a missile (Investing.com)"),
    ("Lebanon", "Aoun demands Israeli withdrawal (Al Jazeera)"),
    ("Iran", "President warns of a 'silent economic war' (AJ)"),
    ("Moldova", "Reports a Russian airspace breach (Kyiv Ind.)"),
    ("Belgium", "Air traffic halts in 23 Nov strike (ST)"),
    ("Germany", "IG Metall widens car, shipyard strikes (Reuters)"),
    ("Portugal", "Lisbon marches over living costs (Reuters)"),
    ("Denmark", "Expels Russian attaché over rapper plot (Guardian)"),
    ("Bangladesh", "30 Awami League homes set on fire (TOI)"),
    ("Australia", "Fred Nile, ex-NSW MP, dies aged 92 (ABC)"),
    ("Melbourne", "70 years since the 1956 Olympics opened (ABC)"),
    ("Trade", "EU and Indonesia sign deal after 10 years (DW)"),
    ("Rugby", "England beat New Zealand 37–12 (Reuters)"),
    ("Football", "Arsenal 2–2 Newcastle; Leeds 4–1 Chelsea (BBC)"),
    ("Tennis", "Zverev v Alcaraz in ATP Finals final (TOI)"),
    ("Football", "Liverpool host Manchester United today (AJ)"),
    ("Somalia", "Expels UAE ambassador, recalls its envoy"),
    ("Ethiopia", "~700,000 displaced by fighting in the south"),
    ("DR Congo", "At least 40 civilians killed in Cantine"),
    ("Canada", "Hegseth tightens US security cooperation"),
]


# ---------------------------------------------------------------- panels
def star(cx, cy, r, fill=(255, 176, 66)):
    pts = []
    for i in range(10):
        ang = -1.5708 + i * 0.6283
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * __import__("math").cos(ang),
                    cy + rad * __import__("math").sin(ang)))
    dr.polygon(pts, fill=fill)


def flame(cx, base, s, colors=((178, 44, 38), (232, 116, 40), (246, 190, 84))):
    for col, k in zip(colors, (1.0, 0.68, 0.4)):
        dr.polygon([(cx - 9 * s * k, base), (cx + 9 * s * k, base),
                    (cx + 2 * s * k, base - 30 * s * k),
                    (cx - 4 * s * k, base - 20 * s * k)], fill=col)


def paint_cop31(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(178, 219, 211))
    dr.ellipse([x + 12, y + 26, x + 66, y + 80], fill=(58, 110, 178))
    dr.polygon([(x + 24, y + 34), (x + 40, y + 30), (x + 36, y + 46),
                (x + 26, y + 44)], fill=(74, 148, 92))
    dr.polygon([(x + 42, y + 52), (x + 56, y + 50), (x + 52, y + 64),
                (x + 42, y + 60)], fill=(74, 148, 92))
    # the long table and its row of delegates
    dr.rectangle([x + 16, y + h - 34, x + w - 16, y + h - 18], fill=(122, 82, 48))
    cols = [(178, 44, 38), (18, 38, 63), (36, 110, 100), (176, 124, 32),
            (96, 90, 78), (58, 110, 178), (122, 82, 48), (70, 70, 110)]
    n = 8
    for i in range(n):
        cx = x + 34 + i * (w - 68) // (n - 1)
        dr.ellipse([cx - 6, y + h - 58, cx + 6, y + h - 46], fill=(232, 196, 158))
        dr.rectangle([cx - 8, y + h - 46, cx + 8, y + h - 34], fill=cols[i])
    # a big clock: the deadline hangs over the talks
    cx, cy, r = x + w - 40, y + 48, 24
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=INK, width=2)
    dr.line([cx, cy, cx, cy - 15], fill=INK, width=3)
    dr.line([cx, cy, cx + 11, cy + 6], fill=INK, width=3)
    dr.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)


def paint_ukraine(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(13, 24, 44))
    for sx, sy in [(30, 20), (90, 12), (150, 26), (210, 14), (262, 30), (60, 40), (180, 42)]:
        dr.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(210, 218, 235))
    dr.ellipse([x + w - 52, y + 14, x + w - 26, y + 40], fill=(226, 222, 196))
    dr.ellipse([x + w - 60, y + 10, x + w - 36, y + 36], fill=(13, 24, 44))
    # drone and missile trails over a dark skyline
    for i, (dx, dy) in enumerate([(36, 30), (96, 22), (168, 36), (238, 24)]):
        for k in range(5):
            dr.ellipse([x + dx + k * 9, y + dy + k * 5, x + dx + k * 9 + 3,
                        y + dy + k * 5 + 3], fill=(240, 120, 90))
        dr.polygon([(x + dx + 48, y + dy + 26), (x + dx + 58, y + dy + 22),
                    (x + dx + 54, y + dy + 32)], fill=(240, 120, 90))
    base = y + h
    for bx, bh, bw in [(0, 34, 40), (44, 48, 34), (82, 28, 46), (132, 42, 30),
                       (166, 30, 40), (210, 50, 36), (250, 32, 42), (296, 40, 30)]:
        dr.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(6, 12, 24))
        for wy in range(base - bh + 6, base - 6, 11):
            for wx in range(x + bx + 5, x + bx + bw - 6, 10):
                if (wx + wy) % 3 == 0:
                    dr.rectangle([wx, wy, wx + 4, wy + 5], fill=(246, 190, 84))
    star(x + 120, base - 62, 13)
    star(x + 236, base - 74, 10)


def paint_bahrain(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(16, 32, 54))
    dr.rectangle([x, y + h - 30, x + w, y + h], fill=(29, 78, 95))
    for i in range(6):
        dr.line([x + 14 + i * 52, y + h - 14, x + 40 + i * 52, y + h - 14],
                fill=(120, 180, 200), width=2)
    # industrial plant on the left, burning
    for bx, bh in [(10, 52), (34, 68), (58, 44)]:
        dr.rectangle([x + bx, y + h - 30 - bh, x + bx + 18, y + h - 30], fill=(8, 16, 30))
    dr.rectangle([x + 40, y + h - 100, x + 46, y + h - 88], fill=(8, 16, 30))
    flame(x + 42, y + h - 88, 0.9)
    star(x + 88, y + 34, 12)
    # a tanker on the right, struck
    sx, sy = x + w - 128, y + h - 44
    dr.polygon([(sx, sy), (sx + 108, sy), (sx + 96, sy + 14), (sx + 12, sy + 14)],
               fill=(10, 10, 14))
    dr.rectangle([sx + 16, sy - 10, sx + 62, sy], fill=(10, 10, 14))
    dr.rectangle([sx + 70, sy - 16, sx + 80, sy], fill=(10, 10, 14))
    flame(sx + 84, sy - 2, 0.8)


GRID_KINDS = ["ship", "burst", "boat", "talks", "aid",
              "caught", "power", "probe", "icu", "sub"]


def paint_grid(kind, x, y, w, h):
    if kind == "ship":
        dr.rectangle([x, y, x + w, y + h], fill=(24, 44, 74))
        dr.rectangle([x, y + h - 12, x + w, y + h], fill=(29, 78, 95))
        sx, sy = x + w // 2 - 44, y + h - 26
        dr.polygon([(sx, sy), (sx + 88, sy), (sx + 78, sy + 10), (sx + 10, sy + 10)],
                   fill=(12, 12, 16))
        dr.rectangle([sx + 14, sy - 8, sx + 52, sy], fill=(12, 12, 16))
        flame(sx + 66, sy, 0.62)
    elif kind == "burst":
        dr.rectangle([x, y, x + w, y + h], fill=(52, 58, 78))
        for bx, bh in [(8, 18), (40, 26), (76, 16), (112, 24), (148, 18)]:
            dr.rectangle([x + bx, y + h - bh, x + bx + 24, y + h], fill=(16, 18, 28))
        star(x + w // 2, y + 20, 14)
    elif kind == "boat":
        dr.rectangle([x, y, x + w, y + h], fill=(44, 92, 140))
        for i in range(5):
            dr.arc([x + 8 + i * 36, y + h - 16, x + 40 + i * 36, y + h + 2],
                   0, 180, fill=(170, 205, 235), width=2)
        bx, by = x + w // 2 - 40, y + h - 30
        dr.polygon([(bx, by), (bx + 80, by), (bx + 66, by + 12), (bx + 14, by + 12)],
                   fill=(90, 52, 30))
        dr.rectangle([bx + 26, by - 10, bx + 56, by], fill=(240, 236, 224))
    elif kind == "talks":
        dr.rectangle([x, y, x + w, y + h], fill=(110, 116, 74))
        dr.rounded_rectangle([x + 22, y + 10, x + 84, y + 34], 8, fill=WHITE)
        dr.polygon([(x + 36, y + 34), (x + 36, y + 44), (x + 48, y + 34)], fill=WHITE)
        dr.rounded_rectangle([x + w - 84, y + 22, x + w - 22, y + 46], 8, fill=(26, 26, 40))
        dr.polygon([(x + w - 48, y + 46), (x + w - 48, y + 56), (x + w - 60, y + 46)],
                   fill=(26, 26, 40))
    elif kind == "aid":
        dr.rectangle([x, y, x + w, y + h], fill=(196, 164, 108))
        tx, ty = x + w // 2 - 42, y + 6
        dr.rectangle([tx, ty, tx + 62, ty + 26], fill=WHITE)
        dr.polygon([(tx + 62, ty + 6), (tx + 80, ty + 14), (tx + 80, ty + 38),
                    (tx + 62, ty + 38)], fill=WHITE)
        dr.rectangle([tx + 24, ty + 5, tx + 32, ty + 21], fill=RED)
        dr.rectangle([tx + 20, ty + 9, tx + 36, ty + 17], fill=RED)
        for wx in (tx + 12, tx + 62):
            dr.ellipse([wx, ty + 32, wx + 12, ty + 44], fill=(26, 26, 40))
    elif kind == "caught":
        dr.rectangle([x, y, x + w, y + h], fill=(96, 30, 30))
        star(x + w // 2, y + h // 2, 20, fill=(246, 190, 84))
        dr.ellipse([x + w // 2 - 6, y + h // 2 - 6, x + w // 2 + 6, y + h // 2 + 6],
                   fill=(96, 30, 30))
    elif kind == "power":
        dr.rectangle([x, y, x + w, y + h], fill=(70, 84, 104))
        px, py = x + w // 2, y + 8
        dr.line([px, py, px - 16, y + h - 6], fill=(20, 22, 30), width=3)
        dr.line([px, py, px + 16, y + h - 6], fill=(20, 22, 30), width=3)
        dr.line([px - 12, py + 12, px + 12, py + 12], fill=(20, 22, 30), width=3)
        dr.line([x + 8, py + 18, px - 4, py + 12], fill=(20, 22, 30), width=2)
        dr.line([x + w - 8, py + 18, px + 4, py + 12], fill=(20, 22, 30), width=2)
        dr.polygon([(px + 2, py + 16), (px - 6, py + 30), (px + 1, py + 30),
                    (px - 3, py + 42), (px + 7, py + 27), (px + 2, py + 27)],
                   fill=(246, 190, 84))
    elif kind == "probe":
        dr.rectangle([x, y, x + w, y + h], fill=(30, 34, 48))
        cx, cy = x + w // 2 - 8, y + h // 2 - 4
        dr.rectangle([cx - 16, cy - 12, cx + 16, cy + 12], outline=(120, 200, 160), width=3)
        dr.line([cx - 16, cy - 12, cx + 16, cy + 12], fill=(120, 200, 160), width=2)
        dr.ellipse([cx + 12, cy + 6, cx + 30, cy + 24], outline=(246, 190, 84), width=4)
        dr.line([cx + 26, cy + 20, cx + 38, cy + 32], fill=(246, 190, 84), width=4)
    elif kind == "icu":
        dr.rectangle([x, y, x + w, y + h], fill=(16, 54, 58))
        pts = [(x + 10, y + h // 2), (x + 44, y + h // 2), (x + 56, y + 14),
               (x + 68, y + h - 14), (x + 80, y + h // 2), (x + 108, y + h // 2),
               (x + 118, y + 22), (x + 128, y + h // 2), (x + w - 10, y + h // 2)]
        dr.line(pts, fill=(96, 230, 170), width=3)
    elif kind == "sub":
        dr.rectangle([x, y, x + w, y + h], fill=(18, 48, 84))
        sx, sy = x + 26, y + h // 2 - 8
        dr.rounded_rectangle([sx, sy, sx + 120, sy + 16], 8, fill=(12, 20, 34))
        dr.rectangle([sx + 48, sy - 10, sx + 62, sy], fill=(12, 20, 34))
        dr.line([sx + 55, sy - 10, sx + 55, sy - 18], fill=(12, 20, 34), width=3)
        for i in range(4):
            dr.ellipse([sx + 16 + i * 24, sy + 5, sx + 22 + i * 24, sy + 11],
                       fill=(246, 190, 84))


# ---------------------------------------------------------------- the map
MAP_ROWS = [
    "                                                                                                    ",
    "        #########          #####  #########                                                         ",
    "     ##############      #########################     #########                                    ",
    "   #################    ###########################  ############    #########                      ",
    "  ##################    ##########################    ##########  #############################     ",
    "   ################      ########################      ######## ###############################     ",
    "    #############         ######################        ########################################    ",
    "     ##########            ##################          ######################################     ",
    "      ########              ################            ####################################       ",
    "      ########               ##############              ##################################         ",
    "       ######                 ############                ##########  ##################          ",
    "       ######                  ##########                  ########   #################  ##       ",
    "        #####                   ########                    ######     ################   ####    ",
    "        ####         ##          ######                      ####       ##############              ",
    "        ###         ####          #####          ##           ##         ############               ",
    "         ##          ###           ####         ######       ###          ##########                ",
    "         ##           ##            ###         ########      ##           ########     ##          ",
    "          #            #             ##        ##########                      ######    ####         ",
    "                      ##             #        ############                      ####      ##         ",
    "                     ###                        ##########                       ##                 ",
    "                     ####                        ########                        ##    ##           ",
    "                     #####                        ######                                      ##    ",
    "                      #####                        ####                         #            ###    ",
    "                      ######                       ###                         ##     #    #####    ",
    "                       #####                       ##              #          ###    ##     ###     ",
    "                       ####                                        ##          ##    #              ",
    "                        ###                                        #           ########           ",
    "                        ##                                                    ##########     #      ",
    "                        ##                                                     ########       ##    ",
    "                         #                                                      ######              ",
    "                         #                                                       ####        #      ",
    "                                                                                 ##         ##    ",
    "                                                                                            ##    ",
    "                                                                                            #     ",
]

# story number -> (column, row) on the mask grid above
PINS = {1: (59, 13), 2: (58, 10), 3: (64, 16), 4: (57, 7), 5: (60, 11),
        6: (52, 21), 7: (61, 14), 8: (58, 15), 9: (20, 16), 10: (64, 13),
        11: (29, 13), 12: (37, 26), 13: (91, 31)}


def paint_map(x, y, w, h):
    rows = len(MAP_ROWS)
    cols = max(len(r) for r in MAP_ROWS)
    cw, ch = w / cols, h / rows
    dot = max(1.6, cw * 0.34)
    for ri, row in enumerate(MAP_ROWS):
        for ci, c in enumerate(row):
            if c == "#":
                cx, cy = x + ci * cw + cw / 2, y + ri * ch + ch / 2
                dr.ellipse([cx - dot, cy - dot, cx + dot, cy + dot], fill=(196, 178, 138))
    for n, (ci, ri) in PINS.items():
        cx, cy = x + ci * cw + cw / 2, y + ri * ch + ch / 2
        r = 7.5
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=WHITE, width=1)
        dr.text((cx, cy), str(n), font=F(SANS_B, 8.5), fill=WHITE, anchor="mm")


# ---------------------------------------------------------------- layout
MX = 26
CW = W - 2 * MX  # 972


def panel_paint(fn, x, y, w, h):
    """Paint a panel on its own tile so nothing spills outside it."""
    global dr
    sub = Image.new("RGB", (w, h), PAPER)
    keep = dr
    dr = ImageDraw.Draw(sub)
    fn(0, 0, w, h)
    dr = keep
    img.paste(sub, (x, y))


def rule(y, fill=INK, width=2):
    dr.line([MX, y, W - MX, y], fill=fill, width=width)


# top strip
text(MX, 10, "THE WORLD IN ONE DAY", F(SANS_B, 13), RED)
right = "35 STORIES · 6 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
text(W - MX, 12, right, F(SANS_B, 11), INK, anchor="ra")
rule(30)

# masthead
f, masthead = fit("Sunday 22 November 2026", SERIF_B, 92, CW)
text(W // 2, 38, masthead, f, INK, anchor="ma")
sub = "Climate deal in sight at COP31 · Iran hits US bases in Bahrain · Russia's 400-drone barrage on Ukraine"
f, sub = fit(sub, SERIF_I, 18, CW)
text(W // 2, 128, sub, f, (70, 60, 48), anchor="ma")
rule(154)

# stat strip
STATS = [("~200", "nations at the COP31 talks"),
         ("03:00", "GMT deadline for objections"),
         ("400+", "drones fired at Ukraine"),
         ("110", "missiles in the same night"),
         ("7+", "people killed in Kyiv"),
         ("2", "US bases targeted in Bahrain")]
sw = CW / 6
for i, (num, label) in enumerate(STATS):
    cx = MX + sw * i + sw / 2
    text(cx, 160, num, F(SERIF_B, 30), RED, anchor="ma")
    for j, ln in enumerate(wrap(label, F(SANS_R, 10.5), sw - 10)):
        text(cx, 196 + j * 12, ln, F(SANS_R, 10.5), MUTE, anchor="ma")

# region bar
REGIONS = [("EUROPE 9", NAVY), ("MIDDLE EAST 8", RED), ("AMERICAS 6", TEAL),
           ("ASIA-PACIFIC 5", GOLD), ("AFRICA 1", (110, 116, 74)),
           ("WORLD 6", (96, 90, 78))]
for i, (label, col) in enumerate(REGIONS):
    x0 = MX + sw * i
    dr.rectangle([x0, 224, x0 + sw - 2, 242], fill=col)
    text(x0 + (sw - 2) / 2, 228, label, F(SANS_B, 11), WHITE, anchor="ma")

# heroes
HY = 254
HW = (CW - 24) // 3  # 316
PAINTERS = [paint_cop31, paint_ukraine, paint_bahrain]
BANNERS = [RED, NAVY, (52, 58, 78)]
for i, (bnr, tag, status, head, deck) in enumerate(HEROES):
    x = MX + i * (HW + 12)
    panel_paint(PAINTERS[i], x, HY, HW, 92)
    banner(x, HY, HW, bnr, BANNERS[i], 13)
    tag_row(x, HY + 100, i + 1, tag, status)
    yy = block(x, HY + 128, head, F(SERIF_B, 23), HW, 26, INK, 2)
    block(x, yy + 2, deck, F(SANS_R, 12), HW, 15, (52, 48, 40), 3)

# the grid: two rows of five
GY = 486
GW = (CW - 40) // 5  # 186
for idx, (bnr, tag, status, head, deck) in enumerate(GRID):
    x = MX + (idx % 5) * (GW + 10)
    y = GY + (idx // 5) * 134
    panel_paint(lambda a, b, w, h, k=GRID_KINDS[idx]: paint_grid(k, a, b, w, h),
                x, y, GW, 52)
    banner(x, y, GW, bnr, NAVY if idx % 2 == 0 else RED, 11)
    chip(x + 8, y + 62, idx + 4, 7.5)
    ftag, tag = fit(tag, SANS_B, 9.5, GW - 66)
    text(x + 20, y + 57, tag, ftag, RED)
    text(x + GW, y + 57, status, F(SANS_B, 7.5), TEAL, anchor="ra")
    yy = block(x, y + 74, head, F(SANS_B, 14.5), GW, 17, INK, 2)
    block(x, yy + 1, deck, F(SANS_R, 10.5), GW, 13, (52, 48, 40), 2)

# bottom: map + briefs
BY = 764
text(MX, BY, "WHERE IT HAPPENED", F(SANS_B, 12), RED)
paint_map(MX, BY + 20, 288, 128)
text(MX, BY + 152, "Red pins carry the numbers of stories 1–13.",
     F(SANS_I, 9.5), MUTE)
BX = MX + 312
text(BX, BY, "ALSO ON SUNDAY 22 NOVEMBER — 22 MORE STORIES", F(SANS_B, 12.5), RED)
BCW = (W - MX - BX - 12) // 2  # 318
for j, (lead, rest) in enumerate(BRIEFS):
    col = j // 11
    x = BX + col * (BCW + 12)
    y = BY + 22 + (j % 11) * 13.8
    n = 14 + j
    text(x, y, f"{n}", F(SANS_B, 11), RED)
    lead_w = tw(lead + " ", F(SANS_B, 11.5))
    text(x + 20, y, lead, F(SANS_B, 11.5), INK)
    frest, rest = fit(rest, SANS_R, 11.5, BCW - 20 - lead_w, 9.5)
    text(x + 20 + lead_w, y, rest, frest, (52, 48, 40))

# date check
DY = 938
dr.rectangle([MX, DY, W - MX, DY + 46], outline=RED, width=1)
text(MX + 8, DY + 4, "DATE CHECK", F(SANS_B, 10.5), RED)
dc = ("Wires read up to 05:50 UTC, Sunday 22 November 2026; every story here was reported or still "
      "developing on 22 November in at least one time zone. Left out as other days' news: the Peru "
      "earthquake (20 Nov local), the Shenzhen summit and the Rohingya ruling (19–20 Nov).")
block(MX + 8, DY + 18, dc, F(SANS_R, 9.8), CW - 16, 12, (52, 48, 40), 2)

# footer
text(MX, 988, "Every story here happened, or was first reported, on Sunday 22 November 2026. "
              "Officials' counts are attributed; pictures and map are original drawings.",
     F(SANS_R, 9.5), MUTE)
dr.rectangle([0, 1004, W, 1024], fill=INK)
text(MX, 1009, "THE WORLD IN ONE DAY", F(SANS_B, 11), WHITE)
text(W - MX, 1009, "SUNDAY 22 NOVEMBER 2026 · ONE PAGE", F(SANS_B, 11), WHITE, anchor="ra")

img.save("/home/hatch/workspace/makefun-news-image-22/entry.png", optimize=True)
print("entry.png written")
