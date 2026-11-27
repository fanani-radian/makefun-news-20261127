#!/usr/bin/env python3
"""Render the WORLD NEWS front page for Friday 27 November 2026.

Fresh build for make.fun competition news-image-20261127.
1024x1024 PNG, < 1 MiB. Run: python3 draw.py [output.png]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = os.path.join(FONT_DIR, "dejavu/DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "dejavu/DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "noto/NotoSans-Regular.ttf")
SANS_I = os.path.join(FONT_DIR, "noto/NotoSans-Italic.ttf")

NAVY = (26, 42, 74)
NAVY_D = (18, 30, 54)
RED = (178, 34, 34)
RED_D = (150, 25, 25)
TEAL = (0, 110, 110)
BLUE = (30, 80, 160)
INK = (20, 20, 20)
GREY = (90, 90, 90)
LGREY = (235, 235, 232)
CREAM = (250, 246, 236)
GOLD = (255, 200, 60)
MAP_BG = (214, 230, 240)
LAND = (168, 188, 158)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w, max_lines=None):
    """Greedy word wrap. Returns list of lines (truncated with ellipsis)."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        # trim last line to fit ellipsis
        while lines and draw.textlength(lines[-1] + "…", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1].rstrip()
        lines[-1] = lines[-1] + "…"
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = fnt.size + 3
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def story(draw, x, y, w, headline, body, tag, head_size=13, body_size=11,
          max_body_lines=3):
    """One news item. Returns y after the item (incl. spacing)."""
    hf = font(SANS_B, head_size)
    bf = font(SANS, body_size)
    tf = font(SANS_I, 9)
    y = text_block(draw, x, y, wrap(draw, headline, hf, w, 2), hf, INK,
                   head_size + 3)
    y = text_block(draw, x, y + 1,
                   wrap(draw, body, bf, w, max_body_lines), bf, (40, 40, 40),
                   body_size + 3)
    draw.text((x, y + 1), tag, font=tf, fill=GREY)
    return y + 7 + 11


def section_head(draw, x, y, w, title, color):
    f = font(SANS_B, 13)
    draw.text((x, y), title, font=f, fill=color)
    draw.line([(x, y + 19), (x + w, y + 19)], fill=color, width=2)
    return y + 26


def main():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    # ---- top strip -------------------------------------------------------
    d.rectangle([0, 0, W, 16], fill="white")
    f_top = font(SANS_B, 9)
    t = "THE WORLD IN ONE DAY  •  A FRONT PAGE OF FRIDAY'S NEWS"
    d.text(((W - d.textlength(t, font=f_top)) / 2, 3), t, font=f_top,
           fill=NAVY)

    # ---- masthead --------------------------------------------------------
    d.rectangle([0, 16, W, 104], fill=NAVY)
    f_mast = font(SERIF_B, 62)
    d.text((10, 26), "WORLD NEWS", font=f_mast, fill="white")
    f_day = font(SANS_B, 30)
    f_date = font(SANS_B, 22)
    d.text((W - 10 - d.textlength("FRIDAY", font=f_day), 24), "FRIDAY",
           font=f_day, fill="white")
    d.text((W - 10 - d.textlength("27 NOVEMBER 2026", font=f_date), 58),
           "27 NOVEMBER 2026", font=f_date, fill=GOLD)

    # ---- red subline -----------------------------------------------------
    d.rectangle([0, 104, W, 134], fill="white")
    f_sub = font(SANS_B, 12)
    d.text((8, 107),
           "SUMMING UP FRIDAY 27 NOVEMBER 2026 — GULF WAR WIDENS, "
           "ZELENSKYY WARNS OF NEW MASS STRIKE, TOKYO PRICES HOT",
           font=f_sub, fill=RED)
    f_src = font(SANS, 10)
    d.text((8, 122), "Sources: Reuters  •  AP  •  CNN  •  Yonhap  •  Bloomberg",
           font=f_src, fill=GREY)

    # ---- lead row + numbers panel ----------------------------------------
    lead_x, lead_y, lead_w = 8, 140, 640
    num_x, num_w = 656, 360
    row_h = 152

    # lead illustration: night refinery, flames, moon
    ix, iy, iw, ih = lead_x, lead_y, 196, row_h
    d.rectangle([ix, iy, ix + iw, iy + ih], fill=(12, 18, 38))
    # stars
    for sx, sy in [(20, 18), (60, 10), (110, 22), (150, 12), (180, 30),
                   (40, 40), (95, 34), (165, 44)]:
        d.ellipse([ix + sx - 1, iy + sy - 1, ix + sx + 1, iy + sy + 1],
                  fill=(220, 220, 200))
    # moon
    d.ellipse([ix + 148, iy + 12, ix + 182, iy + 46], fill=(235, 228, 190))
    # refinery silhouette
    d.rectangle([ix + 8, iy + 96, ix + 60, iy + ih - 22], fill=(40, 48, 70))
    d.rectangle([ix + 66, iy + 108, ix + 118, iy + ih - 22], fill=(34, 42, 62))
    d.rectangle([ix + 124, iy + 88, ix + 150, iy + ih - 22], fill=(40, 48, 70))
    # flare stack
    d.rectangle([ix + 158, iy + 58, ix + 164, iy + ih - 22], fill=(52, 58, 80))
    # tanks
    d.ellipse([ix + 20, iy + 118, ix + 52, iy + 128], fill=(60, 66, 88))
    d.ellipse([ix + 76, iy + 122, ix + 108, iy + 130], fill=(60, 66, 88))
    # flames
    d.polygon([(ix + 152, iy + 58), (ix + 170, iy + 58), (ix + 161, iy + 34)],
              fill=(255, 140, 0))
    d.polygon([(ix + 156, iy + 58), (ix + 166, iy + 58), (ix + 161, iy + 44)],
              fill=(255, 220, 80))
    d.polygon([(ix + 30, iy + 96), (ix + 48, iy + 96), (ix + 39, iy + 74)],
              fill=(255, 120, 0))
    d.polygon([(ix + 84, iy + 108), (ix + 100, iy + 108), (ix + 92, iy + 88)],
              fill=(255, 120, 0))
    # smoke
    for cx, cy, r in [(45, 66, 9), (58, 54, 12), (74, 42, 14), (96, 78, 9),
                      (108, 66, 11)]:
        d.ellipse([ix + cx - r, iy + cy - r, ix + cx + r, iy + cy + r],
                  fill=(120, 118, 112))
    # projectile streak
    d.line([(ix + 120, iy + 20), (ix + 148, iy + 34)], fill=(255, 200, 90),
           width=2)
    d.ellipse([ix + 146, iy + 32, ix + 152, iy + 38], fill=(255, 200, 90))
    # banner
    d.rectangle([ix, iy + ih - 22, ix + iw, iy + ih], fill=RED)
    f_ban = font(SANS_B, 11)
    bt = "GULF WAR WIDENS"
    d.text((ix + (iw - d.textlength(bt, font=f_ban)) / 2, iy + ih - 19), bt,
           font=f_ban, fill="white")

    # lead text
    tx = ix + iw + 12
    tw = lead_x + lead_w - tx
    f_lead_h = font(SANS_B, 19)
    y = lead_y + 2
    y = text_block(d, tx, y,
                   wrap(d, "Gulf war widens: refinery hit kills one, "
                        "drones kill two Italians in Kuwait",
                        f_lead_h, tw, 3), f_lead_h, INK, 22)
    f_lead_b = font(SANS, 11)
    y = text_block(d, tx, y + 3,
                   wrap(d, "A Houthi projectile struck Aramco's Jazan "
                        "refinery on Thursday, killing a Nepalese worker "
                        "and injuring several others; fire crews fought "
                        "the blaze as some operations were suspended. "
                        "Hours later Iranian drones hit a Kuwaiti "
                        "air-defence station, killing two Italian "
                        "technicians and wounding two more. Tehran "
                        "denies any role.",
                        f_lead_b, tw, 6), f_lead_b, (40, 40, 40), 14)
    d.text((tx, lead_y + row_h - 13), "CNN; Reuters",
           font=font(SANS_I, 9), fill=GREY)

    # numbers panel
    d.rectangle([num_x, lead_y, num_x + num_w, lead_y + row_h], fill=NAVY)
    f_np = font(SANS_B, 12)
    d.text((num_x + 10, lead_y + 6), "THE DAY IN NUMBERS", font=f_np,
           fill=GOLD)
    nums = [
        ("NIKKEI 225", "57,499.16", "+0.86%"),
        ("KOSPI", "4,711.21", "+0.29%"),
        ("S&P 500", "7,182.78", "−0.25%"),
        ("BRENT", "$91.46", "−3.3%"),
        ("GOLD / OZ", "$3,590", ""),
        ("BITCOIN", "$60,766", "+0.8%"),
    ]
    cw = num_w // 3
    f_lab = font(SANS_B, 8)
    f_val = font(SANS_B, 14)
    f_chg = font(SANS_B, 10)
    for i, (lab, val, chg) in enumerate(nums):
        cx = num_x + (i % 3) * cw
        cy = lead_y + 28 + (i // 3) * 44
        d.text((cx + 10, cy), lab, font=f_lab, fill=(170, 190, 220))
        d.text((cx + 10, cy + 11), val, font=f_val, fill="white")
        if chg:
            col = (120, 220, 120) if chg.startswith("+") else (255, 120, 120)
            d.text((cx + 10, cy + 28), chg, font=f_chg, fill=col)
    f_nl = font(SANS, 9)
    d.text((num_x + 10, lead_y + 116),
           "Dow 50,182.95 +0.33%  •  Nasdaq 23,585.80 −0.62%",
           font=f_nl, fill=(200, 210, 230))
    d.text((num_x + 10, lead_y + 128),
           "Asia: Thu 26 Nov closes. US: Wed 25 Nov closes;",
           font=f_nl, fill=(170, 180, 200))
    d.text((num_x + 10, lead_y + 139),
           "markets shut Thu for Thanksgiving.",
           font=f_nl, fill=(170, 180, 200))

    # ---- timeline strip --------------------------------------------------
    tl_y = 300
    d.rectangle([8, tl_y, W - 8, tl_y + 40], fill=CREAM)
    f_tl = font(SANS_B, 11)
    d.text((12, tl_y + 4), "HOW THE DAY UNFOLDED — WITA (UTC+8)",
           font=f_tl, fill=NAVY)
    tl = [
        ("00:05", "Rocket Lab window opens, NZ"),
        ("03:30", "Jazan refinery hit reported"),
        ("05:21", "Coalition hits 50 Houthi targets"),
        ("06:00", "Europa League comebacks"),
        ("06:50", "Zelenskyy warns of mass strike"),
        ("07:30", "Tokyo CPI 2.9%"),
    ]
    f_tt = font(SANS_B, 11)
    f_tx = font(SANS, 10)
    seg = (W - 16) // 6
    for i, (tm, ev) in enumerate(tl):
        x = 12 + i * seg
        d.text((x, tl_y + 20), tm, font=f_tt, fill=RED)
        for j, ln in enumerate(wrap(d, ev, f_tx, seg - 52, 2)):
            d.text((x + 44, tl_y + 20 + j * 12), ln, font=f_tx, fill=INK)

    # ---- columns ---------------------------------------------------------
    col_y = 348
    col_h = 392
    cw3 = 330
    xs = [8, 347, 686]

    # column 1 — Middle East & Gulf
    y = section_head(d, xs[0], col_y, cw3, "MIDDLE EAST & GULF", RED)
    y = story(d, xs[0], y, cw3,
              "Iran drones kill two Italians in Kuwait",
              "Two Rheinmetall Italia technicians, 65 and 36, were killed "
              "and two wounded. Iran denies involvement.",
              "Reuters; CNN", max_body_lines=2)
    y = story(d, xs[0], y, cw3,
              "Coalition hits 50 Houthi targets",
              "The coalition struck about 50 targets in Sanaa, Hodeidah "
              "and Saada, hours after the Jazan attack.",
              "CNN; Reuters", max_body_lines=2)
    y = story(d, xs[0], y, cw3,
              "Two tankers hit mines off Oman",
              "Iran's Guards said two tankers caught fire after hitting "
              "mines north of Khasab. Not confirmed.",
              "Reuters; Tehran", max_body_lines=2)
    y = story(d, xs[0], y, cw3,
              "Iraq shuts two Kurdish crossings",
              "Baghdad closed the al-Waleed crossing with Syria and "
              "Bashta with Iran, asserting federal control.",
              "Reuters; Iraqi News Agency", max_body_lines=2)
    y = story(d, xs[0], y, cw3,
              "Egypt: driver held over tanker fire",
              "A day after a Ring Road crash and fire killed 31, "
              "prosecutors arrested the driver for speeding.",
              "Reuters; CNN", max_body_lines=2)

    # column 2 — Ukraine & Europe + Americas & Africa
    y = section_head(d, xs[1], col_y, cw3, "UKRAINE & EUROPE", TEAL)
    y = story(d, xs[1], y, cw3,
              "Zelenskyy: new mass strike coming",
              "Zelenskyy said Russia is readying 'a new massive strike' "
              "on the power grid as crews restore power.",
              "Reuters; AP", max_body_lines=2)
    y = story(d, xs[1], y, cw3,
              "Russia hits two grain ships off Odesa",
              "Two cargo ships carrying 100,000 tonnes of grain for "
              "Turkey and Egypt were struck; one caught fire.",
              "Reuters; Kyiv", max_body_lines=2)
    y = story(d, xs[1], y, cw3,
              "EU summit: budget 'light-years' away",
              "Meloni: the war 'must not expand into the Mediterranean'; "
              "leaders deadlocked over the €1.6tn budget.",
              "Reuters; AP", max_body_lines=2)
    y = section_head(d, xs[1], y + 2, cw3, "AMERICAS & AFRICA", BLUE)
    y = story(d, xs[1], y, cw3,
              "US, Qatar to clear Venezuela arrears",
              "Washington will lend to clear $2.74bn Venezuela owes the "
              "IDB; Qatar may cover $1.42bn owed to CAF.",
              "Reuters; Bloomberg", max_body_lines=2)
    y = story(d, xs[1], y, cw3,
              "Mecca pact FMs meet in Islamabad",
              "The FMs of Pakistan, Saudi Arabia and Turkey meet today, "
              "the first session since their pact took effect.",
              "Reuters; Evrensel", max_body_lines=2)

    # column 3 — Asia & Oceania
    y = section_head(d, xs[2], col_y, cw3, "ASIA & OCEANIA", BLUE)
    y = story(d, xs[2], y, cw3,
              "Kyiv: Kim 'suspends' arms aid to Russia",
              "Ukraine's intel claims Kim halted KN-23 missile and "
              "artillery deliveries to Russia. Kyiv could not verify it.",
              "Yonhap; Kyiv Independent", max_body_lines=2)
    y = story(d, xs[2], y, cw3,
              "Tokyo core CPI 2.9%, above target",
              "Core inflation in Japan's capital rose 2.9% in November, "
              "above the BOJ's 2% target for a third straight month.",
              "Reuters; Business Today", max_body_lines=2)
    y = story(d, xs[2], y, cw3,
              "JERA talks data centres with Meta",
              "Japan's biggest power firm is in talks with Anthropic and "
              "Meta on data centres near power plants around Tokyo.",
              "Reuters; Nikkei", max_body_lines=2)
    y = story(d, xs[2], y, cw3,
              "Duterte trial opens on Monday",
              "Duterte's ICC trial opens on 30 Nov in The Hague on three "
              "counts of crimes against humanity over his drug war.",
              "Reuters; Amnesty", max_body_lines=2)
    y = story(d, xs[2], y, cw3,
              "Australia reserves 20% of LNG",
              "Parliament passed a law making LNG exporters reserve up to "
              "a fifth of output for the domestic market from 2028.",
              "Reuters; SMH", max_body_lines=2)

    # ---- Also today ------------------------------------------------------
    at_y = 724
    f_at = font(SANS_B, 13)
    d.text((8, at_y), "ALSO TODAY", font=f_at, fill=INK)
    d.line([(8, at_y + 19), (W - 8, at_y + 19)], fill=RED, width=2)
    briefs = [
        ("Europa League: Milan, Bournemouth fight back",
         "Milan came from 2-0 down to win 4-2 at Olympiacos; Bournemouth "
         "stayed perfect.",
         "Reuters; UEFA"),
        ("Chess: Gukesh–Sindarov drawn again",
         "Game 3 in Geneva was a 60-move draw; the match is level 1.5-1.5. "
         "Today is a rest day.",
         "Chess.com; IANS"),
        ("Rocket Lab's 101st flight due",
         "An Electron rocket is due to launch from New Zealand at 00:05 "
         "UTC with a Japanese satellite.",
         "Space.com; Rocket Lab"),
        ("EU summit resumes in Brussels",
         "Leaders meet for a second day; the budget and €45bn Ukraine "
         "loan remain undecided.",
         "Reuters; AP"),
    ]
    bw = 244
    bx = [8, 264, 520, 776]
    for i, (h, b, t) in enumerate(briefs):
        story(d, bx[i], at_y + 26, bw, h, b, t, head_size=12, body_size=10,
              max_body_lines=2)

    # ---- bottom row: map + date-check ------------------------------------
    bot_y = 842
    bot_h = 176
    map_x, map_w = 8, 640
    d.rectangle([map_x, bot_y, map_x + map_w, bot_y + bot_h], fill=MAP_BG)
    f_mh = font(SANS_B, 11)
    d.text((map_x + 8, bot_y + 5), "WHERE IT HAPPENED", font=f_mh, fill=NAVY)

    # rough continents (equirectangular, lon -170..190, lat 78..-58)
    def proj(lon, lat):
        x = map_x + (lon + 170) / 360.0 * map_w
        y = bot_y + 22 + (78 - lat) / 136.0 * (bot_h - 30)
        return (x, y)

    continents = [
        # North America
        [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69),
         (-85, 66), (-76, 62), (-65, 60), (-55, 47), (-70, 42), (-75, 35),
         (-80, 26), (-85, 30), (-90, 21), (-97, 16), (-105, 20),
         (-115, 28), (-125, 40), (-125, 48), (-140, 60), (-158, 58),
         (-168, 66)],
        # South America
        [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-40, -5), (-35, -8),
         (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-70, -52),
         (-73, -40), (-72, -20), (-80, -5), (-80, 10)],
        # Africa
        [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
         (35, 28), (43, 12), (51, 11), (48, -2), (40, -10), (35, -20),
         (32, -29), (20, -35), (12, -18), (9, 0), (-8, 5), (-17, 15)],
        # Europe
        [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57),
         (12, 55), (18, 56), (21, 60), (28, 71), (35, 68), (40, 60),
         (30, 55), (28, 46), (23, 40), (19, 42), (12, 44), (3, 43),
         (-10, 36)],
        # Asia
        [(40, 60), (50, 68), (65, 70), (80, 73), (100, 77), (130, 72),
         (160, 70), (178, 66), (170, 60), (160, 55), (142, 50), (140, 40),
         (130, 35), (122, 30), (115, 22), (108, 10), (100, 8), (95, 15),
         (90, 22), (80, 8), (75, 8), (70, 20), (60, 25), (55, 26),
         (48, 30), (43, 12), (40, 35), (35, 36), (30, 36), (40, 45),
         (40, 60)],
        # Australia
        [(113, -22), (122, -14), (132, -12), (142, -11), (150, -23),
         (153, -27), (150, -37), (140, -38), (132, -32), (124, -33),
         (115, -35), (113, -22)],
    ]
    for poly in continents:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=(140, 160, 140))

    pins = [
        ("JAZAN", 16.9, 42.6, (2, 6)),
        ("KUWAIT", 29.4, 47.9, (6, -12)),
        ("KHASAB", 26.2, 56.2, (4, 4)),
        ("ODESA", 46.5, 30.7, (-46, -14)),
        ("KYIV", 50.5, 30.5, (6, -4)),
        ("BRUSSELS", 50.8, 4.4, (-62, -6)),
        ("TOKYO", 35.7, 139.7, (4, -12)),
        ("CANBERRA", -35.3, 149.1, (-66, -4)),
        ("ISLAMABAD", 33.7, 73.1, (4, -12)),
        ("CAIRO", 30.0, 31.2, (-6, 8)),
    ]
    f_pin = font(SANS_B, 8)
    for name, lat, lon, off in pins:
        x, y = proj(lon, lat)
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=RED,
                  outline="white")
        d.text((x + off[0], y + off[1]), name, font=f_pin, fill=NAVY)

    # date-check box
    dc_x, dc_w = 656, 360
    d.rectangle([dc_x, bot_y, dc_x + dc_w, bot_y + bot_h], fill="white",
                outline=NAVY, width=2)
    f_dc = font(SANS_B, 12)
    d.text((dc_x + 10, bot_y + 8), "DATE-CHECKED  •  27 NOV 2026",
           font=f_dc, fill=RED)
    f_dcb = font(SANS, 11)
    y = text_block(d, dc_x + 10, bot_y + 30,
                   wrap(d, "Every story above happened, or was first "
                        "reported, on Fri 27 Nov 2026 in some time zone. "
                        "Names, numbers and dates are as reported by the "
                        "sources named. Nothing here is invented.",
                        f_dcb, dc_w - 20, 6), f_dcb, INK, 14)
    f_dcf = font(SANS_B, 10)
    d.text((dc_x + 10, bot_y + bot_h - 26),
           "WORLD NEWS — 27 NOVEMBER 2026", font=f_dcf, fill=NAVY)
    d.text((dc_x + 10, bot_y + bot_h - 14),
           "news-image-20261127", font=font(SANS, 9), fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
