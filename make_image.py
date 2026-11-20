#!/usr/bin/env python3
"""Render the news-image-20261120 front page: Friday 20 November 2026,
six stories plus a briefs strip. Writes entry.png (1024x1024, < 1 MiB).

Stories, each confirmed in news reports dated 20 November 2026:
  1. Trump pushes the Iran war decision to 2027: "no rush", he'll "see
     what happens" after Jan 1 (Reuters + 4 outlets, 20 Nov 03:06).
  2. The ICJ rules Myanmar committed genocide against the Rohingya:
     9-6, the first time the UN's highest court has held a state
     liable for genocide; ~10,000 killed, 700,000+ fled in 2017
     (BBC, UN, Reuters; ruling delivered 19 Nov, headline of 20 Nov).
  3. Cyclone Akvan makes landfall on India's Odisha coast: 300,000
     evacuated, 423 rescue teams deployed (The Hindu, 20 Nov).
  4. GTA VI earns an estimated $1.84bn on day one, passing The
     Odyssey's $1.805bn lifetime box office; 19.1m copies
     (Sensor Tower via Reuters, 19-20 Nov).
  5. COP31's revised draft in Antalya strips out all fossil-fuel
     phase-out language; backlash ahead of the final plenary on 20 Nov
     (The Guardian, Anadolu).
  6. Engine trouble forces Japan's Hayabusa2 probe to scrap its
     asteroid landing plan and change course (Space + 4 outlets, 20 Nov).
Briefs: Europe ready for talks with Russia to end the Ukraine war (BBC);
Anthropic's valuation reportedly reaches $1.5 trillion; the US and
Venezuela sign a deal to restore military cooperation.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
PAGE_BG = (247, 243, 232)
TEXT = (20, 20, 20)
ACCENT = (176, 58, 46)
CARD = (255, 253, 246)
MUTED = (96, 90, 78)
OCEAN = (31, 78, 121)
JADE = (18, 110, 105)
TANGERINE = (232, 126, 32)
BRASS = (214, 164, 32)
MIDNIGHT = (24, 42, 84)
PLUM = (94, 60, 140)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(pen, text, font, max_width):
    """Split text into lines no wider than max_width (pixels)."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = (current + " " + word).strip()
        if pen.textlength(candidate, font=font) <= max_width:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = word
    if current:
        lines.append(current)
    return lines


# ---------------- pictograms: each draws inside a (w x h) band ----------------
def draw_iran(pen, x0, y0, w, h):
    """Calendar page marked 2027 with a clock beside it."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 232, 214))
    # calendar page
    cx0, cy0, cw, ch = x0 + 30, y0 + 8, 200, h - 16
    pen.rectangle([cx0, cy0, cx0 + cw, cy0 + ch], fill=(255, 253, 246),
                  outline=(120, 110, 90))
    pen.rectangle([cx0, cy0, cx0 + cw, cy0 + 26], fill=ACCENT)
    pen.text((cx0 + cw // 2, cy0 + 4), "JANUARY", font=load_font(FONT_BOLD, 15),
             fill=(255, 255, 255), anchor="ma")
    pen.text((cx0 + cw // 2, cy0 + 30), "2027", font=load_font(FONT_BOLD, 34),
             fill=TEXT, anchor="ma")
    # clock
    ccx, ccy, r = x0 + w - 110, y0 + h // 2, 34
    pen.ellipse([ccx - r, ccy - r, ccx + r, ccy + r], fill=(255, 253, 246),
                outline=TEXT, width=3)
    pen.line([ccx, ccy, ccx, ccy - 22], fill=TEXT, width=4)
    pen.line([ccx, ccy, ccx + 16, ccy + 8], fill=TEXT, width=4)
    pen.ellipse([ccx - 4, ccy - 4, ccx + 4, ccy + 4], fill=ACCENT)


def draw_icj(pen, x0, y0, w, h):
    """Scales of justice on a dark blue field."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=MIDNIGHT)
    cx = x0 + w // 2
    pen.rectangle([cx - 4, y0 + 14, cx + 4, y0 + h - 16], fill=BRASS)
    pen.rectangle([cx - 150, y0 + 18, cx + 150, y0 + 24], fill=BRASS)
    pen.rectangle([cx - 60, y0 + h - 14, cx + 60, y0 + h - 6], fill=BRASS)
    for side in (-1, 1):
        px = cx + side * 130
        pen.line([px, y0 + 24, px, y0 + 52], fill=BRASS, width=3)
        pen.line([px - 34, y0 + 52, px, y0 + 24], fill=BRASS, width=2)
        pen.line([px + 34, y0 + 52, px, y0 + 24], fill=BRASS, width=2)
        pen.pieslice([px - 38, y0 + 52, px + 38, y0 + 76], 0, 180, fill=BRASS)
    pen.ellipse([cx - 8, y0 + 8, cx + 8, y0 + 20], fill=BRASS)


def draw_cyclone(pen, x0, y0, w, h):
    """Spiral storm over a coastline, with rain."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=(198, 222, 235))
    pen.rectangle([x0, y0 + 66, x0 + w, y0 + h], fill=(52, 110, 150))
    # coastline
    pen.polygon([(x0, y0 + h), (x0 + 120, y0 + 66), (x0 + 260, y0 + 78),
                 (x0 + w, y0 + 66), (x0 + w, y0 + h)], fill=(214, 196, 150))
    # spiral
    scx, scy = x0 + w // 2, y0 + 34
    for r, start, end in ((34, 0, 300), (26, 40, 340), (18, 80, 360),
                          (10, 120, 360)):
        pen.arc([scx - r, scy - r, scx + r, scy + r], start, end,
                fill=(255, 255, 255), width=5)
    pen.ellipse([scx - 5, scy - 5, scx + 5, scy + 5], fill=ACCENT)
    # rain
    for i in range(8):
        rx = x0 + 30 + i * 52
        pen.line([rx, y0 + 74, rx - 8, y0 + 88], fill=(220, 235, 245), width=3)


def draw_gta(pen, x0, y0, w, h):
    """Two bars: game revenue $1.84bn vs film $1.805bn."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=(24, 24, 30))
    bf = load_font(FONT_BOLD, 17)
    sf = load_font(FONT_REG, 14)
    pen.text((x0 + 16, y0 + 8), "GTA VI  $1.84bn", font=bf, fill=BRASS)
    pen.rectangle([x0 + 16, y0 + 32, x0 + 16 + 400, y0 + 48], fill=BRASS)
    pen.text((x0 + 16, y0 + 54), "THE ODYSSEY  $1.805bn", font=bf,
             fill=(220, 220, 230))
    pen.rectangle([x0 + 16, y0 + 76, x0 + 16 + 388, y0 + 90], fill=OCEAN)
    pen.text((x0 + w - 16, y0 + 8), "DAY ONE", font=sf, fill=(200, 200, 210),
             anchor="ra")


def draw_cop31(pen, x0, y0, w, h):
    """Globe with factory smoke and a crossed-out oil drop."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 226, 210))
    # globe
    gx, gy, gr = x0 + 90, y0 + h // 2, 38
    pen.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=OCEAN)
    pen.ellipse([gx - 22, gy - 26, gx + 4, gy - 2], fill=JADE)
    pen.ellipse([gx - 6, gy + 6, gx + 24, gy + 28], fill=JADE)
    # factory
    fx = x0 + 200
    pen.rectangle([fx, y0 + 46, fx + 120, y0 + h - 8], fill=(90, 90, 96))
    pen.rectangle([fx + 14, y0 + 22, fx + 30, y0 + 46], fill=(70, 70, 76))
    pen.rectangle([fx + 48, y0 + 30, fx + 62, y0 + 46], fill=(70, 70, 76))
    for i, (sx, sy, sr) in enumerate(((fx + 22, y0 + 12, 9),
                                      (fx + 30, y0 + 4, 7),
                                      (fx + 55, y0 + 18, 8))):
        pen.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(160, 160, 165))
    # crossed-out oil drop
    dx, dy = x0 + w - 70, y0 + h // 2
    pen.ellipse([dx - 18, dy - 6, dx + 18, dy + 26], fill=TEXT)
    pen.polygon([(dx, dy - 30), (dx - 16, dy - 2), (dx + 16, dy - 2)], fill=TEXT)
    pen.ellipse([dx - 30, dy - 34, dx + 30, dy + 30], outline=ACCENT, width=5)
    pen.line([dx - 21, dy - 24, dx + 21, dy + 21], fill=ACCENT, width=5)


def draw_hayabusa(pen, x0, y0, w, h):
    """Spacecraft diverted away from an asteroid marked with a red X."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=(12, 16, 34))
    for i in range(40):
        random.seed(300 + i)
        pen.point((x0 + random.randint(4, w - 4), y0 + random.randint(4, h - 4)),
                  fill=(220, 220, 240))
    # asteroid with red X
    ax, ay = x0 + w - 100, y0 + 44
    pen.ellipse([ax - 30, ay - 24, ax + 30, ay + 24], fill=(140, 135, 125))
    pen.ellipse([ax - 12, ay - 14, ax + 2, ay - 2], fill=(110, 105, 95))
    pen.ellipse([ax + 8, ay + 6, ax + 22, ay + 18], fill=(110, 105, 95))
    pen.line([ax - 22, ay - 16, ax + 22, ay + 16], fill=ACCENT, width=5)
    pen.line([ax - 22, ay + 16, ax + 22, ay - 16], fill=ACCENT, width=5)
    # spacecraft
    pen.rectangle([x0 + 40, y0 + 40, x0 + 120, y0 + 62], fill=(200, 205, 210))
    pen.pieslice([x0 + 110, y0 + 28, x0 + 160, y0 + 70], 270, 90,
                 fill=(230, 232, 235))
    pen.line([x0 + 40, y0 + 51, x0 + 16, y0 + 51], fill=(160, 165, 170), width=4)
    # diverted dashed path
    for i in range(10):
        t = i / 9.0
        px = int(x0 + 150 + (ax - 60 - x0 - 150) * t)
        py = int(y0 + 30 + 26 * math.sin(math.pi * t))
        pen.ellipse([px - 3, py - 3, px + 3, py + 3], fill=BRASS)


PANELS = [
    {"kicker": "IRAN CALL DELAYED", "pic": draw_iran, "colour": MIDNIGHT,
     "head": "Trump pushes Iran war decision to 2027",
     "sub": "\u2018No rush\u2026 see what happens after Jan 1\u2019 \u00b7 Reuters"},
    {"kicker": "GENOCIDE RULING", "pic": draw_icj, "colour": PLUM,
     "head": "UN court: Myanmar committed genocide",
     "sub": "ICJ 9\u20136 \u00b7 first state ever held liable \u00b7 The Hague"},
    {"kicker": "CYCLONE AKVAN", "pic": draw_cyclone, "colour": OCEAN,
     "head": "300,000 evacuated as cyclone hits Odisha",
     "sub": "Severe storm makes landfall \u00b7 423 rescue teams"},
    {"kicker": "GTA VI BEATS HOLLYWOOD", "pic": draw_gta, "colour": BRASS,
     "head": "GTA VI\u2019s $1.84bn tops The Odyssey\u2019s run",
     "sub": "19.1m copies day one \u00b7 Sensor Tower estimate"},
    {"kicker": "COP31 BACKLASH", "pic": draw_cop31, "colour": JADE,
     "head": "Climate draft drops fossil-fuel phase-out",
     "sub": "Antalya \u00b7 final plenary today \u00b7 delegates push back"},
    {"kicker": "HAYABUSA2 GROUNDED", "pic": draw_hayabusa, "colour": MIDNIGHT,
     "head": "Engine trouble ends asteroid landing plan",
     "sub": "JAXA probe changes course \u00b7 Space"},
]

BRIEFS = [
    "Europe ready for talks with Russia to end Ukraine war",
    "Anthropic\u2019s valuation reportedly reaches $1.5 trillion",
    "US and Venezuela sign deal to restore military cooperation",
]


def render():
    page = Image.new("RGB", (CANVAS_W, CANVAS_H), PAGE_BG)
    pen = ImageDraw.Draw(page)

    # ---- masthead ----
    pen.rectangle([0, 0, CANVAS_W, 118], fill=TEXT)
    pen.text((512, 14), "THE WORLD IN ONE DAY", font=load_font(FONT_SERIF, 54),
             fill=PAGE_BG, anchor="ma")
    pen.text((512, 76), "FRIDAY 20 NOVEMBER 2026",
             font=load_font(FONT_BOLD, 26), fill=BRASS, anchor="ma")
    pen.line([16, 126, CANVAS_W - 16, 126], fill=ACCENT, width=4)

    # ---- story grid: 2 columns x 3 rows ----
    margin, top = 16, 140
    cell_w, cell_h = 488, 246
    gap_x, gap_y = 16, 12
    head_font = load_font(FONT_BOLD, 25)
    sub_font = load_font(FONT_REG, 17)
    kick_font = load_font(FONT_BOLD, 15)
    for idx, panel in enumerate(PANELS):
        col, row = idx % 2, idx // 2
        x = margin + col * (cell_w + gap_x)
        y = top + row * (cell_h + gap_y)
        pen.rectangle([x, y, x + cell_w, y + cell_h], fill=CARD,
                      outline=(200, 192, 172))
        pen.rectangle([x, y, x + cell_w, y + 26], fill=panel["colour"])
        pen.text((x + 10, y + 4), panel["kicker"], font=kick_font,
                 fill=(255, 255, 255))
        panel["pic"](pen, x + 8, y + 34, cell_w - 16, 92)
        hy = y + 136
        for line in wrap_text(pen, panel["head"], head_font, cell_w - 24)[:2]:
            pen.text((x + 12, hy), line, font=head_font, fill=TEXT)
            hy += 30
        for line in wrap_text(pen, panel["sub"], sub_font, cell_w - 24)[:2]:
            pen.text((x + 12, hy + 2), line, font=sub_font, fill=MUTED)
            hy += 22

    # ---- briefs strip ----
    fy = top + 3 * cell_h + 2 * gap_y + 4
    pen.rectangle([margin, fy, CANVAS_W - margin, fy + 78], fill=(238, 232, 214),
                  outline=(200, 192, 172))
    pen.text((margin + 10, fy + 8), "ALSO IN BRIEF", font=load_font(FONT_BOLD, 16),
             fill=ACCENT)
    brief_font = load_font(FONT_REG, 16)
    by = fy + 30
    for item in BRIEFS:
        pen.text((margin + 10, by), "\u2022  " + item, font=brief_font, fill=TEXT)
        by += 20
    pen.text((512, CANVAS_H - 22),
             "Six stories, one day \u2014 drawn from the news of 20 November 2026",
             font=load_font(FONT_REG, 14), fill=MUTED, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    page.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
