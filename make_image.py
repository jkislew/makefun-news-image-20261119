"""Paint entry.png: one newspaper page holding a whole day of news.

Build-time generator for the make.fun news-image-20261119 entry,
rewritten with a data-driven layout: a palette table, small text
helpers, and one routine per story. The judge sees only the image,
so each story carries its own headline with the names, places and
numbers that make it identifiable on its own:

  lead    renewed US-Iran fire in the Gulf (Qeshm Island, Kuwait,
          Bahrain, Bab el-Mandeb back in Houthi hands)
  second  Trump, Xi and Putin in one room at APEC in Shenzhen
  money   Anthropic prices its IPO at $83, about $81.3bn raised,
          the largest on record; Nvidia slips 3% after Huang
  europe  Brussels proposes lending Ukraine 45 billion euros,
          repayable only out of Russian reparations
  space   Voyager 1, launched 49 years ago, one light-day away
  play    Grand Theft Auto VI goes on sale at midnight, Vice City
  ticker  hawkish Fed minutes and a 19-month dollar high, the
          Bangladesh lockdown, Gaza, and the Crimea Bridge

The script uses no clock, no randomness and no network, and it
writes the same PNG bytes on every run. The grader never runs it:
main.py ships the rendered entry.png unchanged.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont


def rgb(text):
    return tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    "paper": rgb("F7F2E7"), "ink": rgb("14202E"), "red": rgb("B22228"),
    "teal": rgb("176B7A"), "sand": rgb("D8BC8A"), "gold": rgb("E8B03C"),
    "blue": rgb("264A96"), "night": rgb("0A0E22"), "sea": rgb("A8CDCD"),
    "shore": rgb("C4A064"), "burst": rgb("E65A28"), "hull": rgb("3C3C42"),
    "deck": rgb("5A5A62"), "cn": rgb("DE2910"), "ru": rgb("CC0000"),
    "ua1": rgb("005BBB"), "ua2": rgb("FFD500"), "dish": rgb("DCDCE4"),
    "earth": rgb("5A96DC"), "gta": rgb("B2225A"), "palm": rgb("103C28"),
    "trunk": rgb("10281E"), "sun": rgb("FFE282"), "white": rgb("FFFFFF"),
}

FONT_FILES = {
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "plain": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}
HERE = os.path.dirname(os.path.abspath(__file__))
SIZE = 1024


def font(kind, points):
    return ImageFont.truetype(FONT_FILES[kind], points)


def label(d, xy, s, kind, points, colour, anchor=None):
    d.text(xy, s, font=font(kind, points), fill=PAL[colour], anchor=anchor)


def para(d, x, y, s, points, colour, width, kind="plain"):
    fnt = font(kind, points)
    words, line = s.split(), ""
    for word in words:
        trial = word if not line else line + " " + word
        if d.textlength(trial, font=fnt) <= width:
            line = trial
            continue
        d.text((x, y), line, font=fnt, fill=PAL[colour])
        y += int(points * 1.12)
        line = word
    if line:
        d.text((x, y), line, font=fnt, fill=PAL[colour])
    return y


def frame(d, box):
    d.rectangle(box, outline=PAL["ink"], width=3)


def star(d, cx, cy, r, colour="gold"):
    ring = []
    for k in range(10):
        ang = k * math.pi / 5 - math.pi / 2
        rad = r if k % 2 == 0 else r * 0.45
        ring.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(ring, fill=PAL[colour])


def masthead(d):
    label(d, (512, 16), "THE WORLD IN ONE DAY", "serif", 63, "ink", "ma")
    d.rectangle([24, 98, 1000, 104], fill=PAL["red"])
    label(d, (512, 110), "Thursday 19 November 2026  \u00b7  the whole day, in one image",
          "bold", 26, "ink", "ma")
    d.rectangle([24, 146, 1000, 149], fill=PAL["ink"])


def gulf_lead(d):
    frame(d, [24, 168, 1000, 452])
    d.rectangle([34, 178, 470, 442], fill=PAL["sea"])
    d.polygon([(34, 178), (300, 178), (250, 260), (34, 330)], fill=PAL["sand"])
    arabia = [(34, 442), (200, 442), (330, 350), (470, 430), (470, 442)]
    d.polygon(arabia, fill=PAL["sand"])
    d.ellipse([225, 268, 315, 308], fill=PAL["shore"], outline=PAL["ink"], width=2)
    label(d, (270, 312), "QESHM IS.", "bold", 17, "ink", "ma")
    label(d, (120, 190), "IRAN", "bold", 20, "ink")
    label(d, (352, 415), "ARABIA", "bold", 20, "ink")
    label(d, (150, 352), "STRAIT OF", "bold", 16, "teal")
    label(d, (150, 372), "HORMUZ", "bold", 16, "teal")
    hull = [(120, 300), (215, 300), (200, 318), (135, 318)]
    d.polygon(hull, fill=PAL["hull"])
    d.rectangle([150, 284, 175, 300], fill=PAL["deck"])
    d.rectangle([178, 292, 205, 300], fill=PAL["red"])
    shots = [(285, 275, 380, 210), (260, 290, 150, 235)]
    for sx, sy, ex, ey in shots:
        arc_box = [min(sx, ex), min(sy, ey) - 26, max(sx, ex), max(sy, ey) + 26]
        d.arc(arc_box, start=200, end=340, fill=PAL["red"], width=4)
        star(d, ex, ey, 17, "burst")
    star(d, 268, 282, 22, "burst")
    label(d, (492, 182), "GULF WAR", "serif", 56, "red")
    label(d, (492, 246), "FLARES AGAIN", "serif", 56, "ink")
    story = " ".join([
        "US jets hit an Iranian missile site on Qeshm Island. Iran",
        "answers on US bases in Kuwait; Bahrain downs a third attack",
        "in a week. Houthis retake Bab el-Mandeb.",
    ])
    para(d, 492, 320, story, 24, "ink", 490)


def shenzhen(d):
    frame(d, [24, 464, 1000, 640])
    d.rectangle([46, 486, 164, 552], outline=PAL["ink"], width=2)
    for stripe in range(5):
        top = 486 + stripe * 13
        d.rectangle([46, top, 164, top + 7], fill=PAL["red"])
    d.rectangle([46, 486, 94, 521], fill=PAL["blue"])
    d.rectangle([178, 486, 296, 552], fill=PAL["cn"], outline=PAL["ink"], width=2)
    for cx, cy, r in [(204, 506, 13), (228, 498, 7), (234, 514, 7)]:
        star(d, cx, cy, r)
    d.rectangle([310, 486, 428, 552], outline=PAL["ink"], width=2)
    d.rectangle([310, 508, 428, 530], fill=PAL["blue"])
    d.rectangle([310, 530, 428, 552], fill=PAL["ru"])
    label(d, (46, 568), "SHENZHEN \u00b7 APEC SUMMIT", "bold", 21, "teal")
    label(d, (46, 596), "ONE TABLE, THREE FLAGS", "bold", 21, "ink")
    label(d, (492, 476), "TRUMP, XI, PUTIN:", "serif", 35, "ink")
    label(d, (492, 518), "ONE HOUR TOGETHER", "serif", 35, "ink")
    story = " ".join([
        "A first trilateral on the summit sidelines:",
        "three nuclear powers, the world watching.",
    ])
    para(d, 492, 572, story, 23, "ink", 490)


def anthropic(d):
    frame(d, [24, 652, 506, 806])
    label(d, (40, 662), "ANTHROPIC'S IPO:", "serif", 32, "ink")
    label(d, (40, 699), "BIGGEST IN HISTORY", "serif", 32, "red")
    label(d, (40, 742), "$83 a share \u2014 $81.3bn raised.", "bold", 21, "ink")
    for i, hgt in enumerate([10, 16, 22, 28]):
        left = 46 + i * 40
        colour = "teal" if i < 3 else "gold"
        d.rectangle([left, 796 - hgt, left + 26, 796], fill=PAL[colour],
                    outline=PAL["ink"], width=2)
    label(d, (222, 774), "Nvidia -3% post-Huang", "plain", 19, "ink")


def europe(d):
    frame(d, [518, 652, 1000, 806])
    d.ellipse([536, 666, 624, 754], fill=PAL["blue"], outline=PAL["ink"], width=2)
    for k in range(8):
        ang = k * math.pi / 4
        star(d, 580 + 30 * math.cos(ang), 710 + 30 * math.sin(ang), 7)
    label(d, (640, 666), "EU LENDS UKRAINE", "serif", 30, "ink")
    label(d, (640, 702), "\u20ac45 BILLION", "serif", 36, "blue")
    d.rectangle([534, 760, 634, 776], fill=PAL["ua1"])
    d.rectangle([534, 776, 634, 792], fill=PAL["ua2"])
    story = " ".join([
        "Brussels borrows to keep Kyiv funded \u2014 repaid",
        "only when Russia pays reparations.",
    ])
    para(d, 648, 754, story, 18, "ink", 336)


def voyager(d):
    frame(d, [24, 818, 506, 958])
    d.rectangle([32, 826, 210, 950], fill=PAL["night"])
    d.ellipse([52, 852, 118, 906], fill=PAL["dish"], outline=PAL["gold"], width=2)
    d.line([118, 878, 178, 858], fill=PAL["gold"], width=3)
    d.line([85, 900, 70, 930], fill=PAL["gold"], width=3)
    star(d, 168, 918, 6, "white")
    star(d, 40, 926, 5, "white")
    d.ellipse([176, 910, 198, 932], fill=PAL["earth"])
    label(d, (226, 828), "VOYAGER 1 AT", "serif", 28, "ink")
    label(d, (226, 861), "ONE LIGHT-DAY", "serif", 28, "teal")
    para(d, 226, 902, "49 years out; its signal takes a full day to come home.",
         18, "ink", 266)


def vice_city(d):
    frame(d, [518, 818, 1000, 958])
    bands = [rgb("582C78"), rgb("96346E"), rgb("D6545C"), rgb("F68C50"),
             rgb("FACD78")]
    for i, colour in enumerate(bands):
        d.rectangle([526, 826 + i * 25, 712, 826 + (i + 1) * 25], fill=colour)
    d.ellipse([588, 856, 648, 916], fill=PAL["sun"])
    for px in (554, 666):
        d.line([px, 950, px + 8, 870], fill=PAL["trunk"], width=5)
        for dx in (-26, -10, 12, 28):
            box = [px + 8 + dx - 22, 848, px + 8 + dx + 22, 888]
            d.arc(box, start=180, end=330, fill=PAL["palm"], width=4)
    label(d, (578, 916), "VICE CITY", "bold", 20, "white")
    label(d, (728, 828), "GTA VI DAY", "serif", 31, "gta")
    story = " ".join([
        "The wait ends at midnight: the biggest",
        "game on Earth launches on PS5 and Xbox.",
    ])
    para(d, 728, 870, story, 19, "ink", 258)


def ticker(d):
    d.rectangle([24, 966, 1000, 1016], fill=PAL["ink"])
    top = "FED MINUTES POINT TO MORE HIKES \u00b7 DOLLAR AT A 19-MONTH HIGH"
    bottom = ("BANGLADESH LOCKS DOWN OVER HASINA'S RETURN \u2014 ISRAEL INTO "
              "CENTRAL GAZA \u00b7 CRIMEA BRIDGE HIT")
    label(d, (512, 978), top, "bold", 17, "paper", "ma")
    label(d, (512, 1000), bottom, "bold", 15, "gold", "ma")


def render():
    page = Image.new("RGB", (SIZE, SIZE), PAL["paper"])
    d = ImageDraw.Draw(page)
    for routine in (masthead, gulf_lead, shenzhen, anthropic, europe,
                    voyager, vice_city, ticker):
        routine(d)
    target = os.path.join(HERE, "entry.png")
    page.save(target, format="PNG", optimize=True)
    print("wrote", target)


if __name__ == "__main__":
    render()
