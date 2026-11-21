#!/usr/bin/env python3
"""Warm story test 2 (render23): "The Windowsill Water" — built on the
researched story formula (2026-11-21): object-anomaly hook held long,
twist at ~62%, warm reveal, unanswered-question ending.
14s, 1080x1920, 30fps. Warm palette + faced figure (render18 system).
Usage: python3 render23.py [start] [end]
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FRAMES = 420
OUT = "/tmp/warm-water-frames"
os.makedirs(OUT, exist_ok=True)

CREAM = (243, 234, 216)
FLOOR = (231, 216, 184)
BROWN = (74, 56, 40)
INK = (26, 24, 22)
WOOD = (186, 150, 105)
FRAMEC = (150, 120, 90)
PINK = (244, 168, 168)
WATER = (140, 190, 224)
CAT = (133, 110, 86)
LEAF = (120, 170, 105)
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
TC = 3

def font(s): return ImageFont.truetype(BOLD, s, index=TC)
F_HOOK = font(72)
F_MID = font(56)
F_PAY = font(66)
F_SM = font(42)
F_TICK = font(46)

def fade(t, a, b):
    return 0.0 if t <= a else 1.0 if t >= b else (t - a) / (b - a)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def limb(d, pts, wdt=20, col=INK):
    d.line(pts, fill=col, width=wdt, joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0] - wdt // 2, p[1] - wdt // 2, p[0] + wdt // 2, p[1] + wdt // 2], fill=col)

def face(d, cx, cy, r, mood):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 253, 248), outline=INK, width=8)
    ey = cy - 12
    if mood == "sleepy":
        for sgn in (-1, 1):
            ex = cx + sgn * 34
            d.arc([ex - 17, ey - 8, ex + 17, ey + 12], start=200, end=340, fill=INK, width=6)
        d.line([cx - 14, cy + 40, cx + 14, cy + 40], fill=INK, width=6)
    elif mood == "awake":
        for sgn in (-1, 1):
            ex = cx + sgn * 34
            d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=INK)
        d.arc([cx - 16, cy + 22, cx + 16, cy + 48], start=20, end=160, fill=INK, width=6)
    elif mood == "wow":
        for sgn in (-1, 1):
            ex = cx + sgn * 34
            d.ellipse([ex - 13, ey - 13, ex + 13, ey + 13], fill=INK)
            d.ellipse([ex - 4, ey - 6, ex + 4, ey + 2], fill=(255, 255, 255))
        d.ellipse([cx - 11, cy + 34, cx + 11, cy + 58], outline=INK, width=6)
    else:  # touched
        for sgn in (-1, 1):
            ex = cx + sgn * 34
            d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=INK)
            chx = cx + sgn * 58
            d.ellipse([chx - 15, cy + 22, chx + 15, cy + 40], fill=PINK)
        d.arc([cx - 22, cy + 18, cx + 22, cy + 56], start=15, end=165, fill=INK, width=7)

def water_level(f):
    """Glass fill fraction over time: drains, two refills, cat drinks, final refill."""
    if f < 110:
        return 0.92
    if f < 155:
        return 0.92 - 0.67 * (f - 110) / 45.0          # drain to .25
    if f < 170:
        return 0.25 + 0.75 * fade(f, 155, 170)          # refill 1
    if f < 215:
        return 1.0 - 0.80 * (f - 170) / 45.0            # drain to .20
    if f < 230:
        return 0.20 + 0.80 * fade(f, 215, 230)          # refill 2
    if f < 262:
        return 1.0 - 0.90 * (f - 230) / 32.0            # drain to .10
    if f < 345:
        return max(0.03, 0.10 - 0.07 * fade(f, 285, 345))  # cat drinks
    if f < 368:
        return 0.03 + 0.97 * fade(f, 345, 368)          # final refill, extra full
    return 1.0

def pouring(f):
    return (155 <= f < 170) or (215 <= f < 230) or (345 <= f < 368)

def sky_color(f):
    if f < 110:
        return (196, 222, 235)
    if f < 262:
        p = ((f - 110) % 52) / 52.0
        return lerp((250, 214, 160), (196, 222, 235), math.sin(p * math.pi))
    return (240, 192, 142)  # dusk for twist + climax

def draw_cat(d, f):
    # cat enters f262-288 from the right, lands on sill, drinks with head bobs
    if f < 262:
        return
    t = fade(f, 262, 288)
    cx = 1120 - 330 * t
    hop = -70 * math.sin(t * math.pi) if t < 1 else 0
    cy = 1006 + hop
    drink = f >= 292
    bob = 10 * math.sin(f * 0.35) if drink else 0
    # tail
    sway = 12 * math.sin(f * 0.08)
    d.line([(cx + 62, cy - 6), (cx + 108, cy - 34 + sway), (cx + 118, cy - 78 + sway)], fill=CAT, width=17, joint="curve")
    # body + head
    d.ellipse([cx - 72, cy - 44, cx + 72, cy + 44], fill=CAT)
    hx, hy = cx - 66, cy - 52 + (bob if drink else 0)
    d.ellipse([hx - 42, hy - 42, hx + 42, hy + 42], fill=CAT)
    d.polygon([(hx - 34, hy - 28), (hx - 30, hy - 62), (hx - 6, hy - 38)], fill=CAT)
    d.polygon([(hx + 34, hy - 28), (hx + 30, hy - 62), (hx + 6, hy - 38)], fill=CAT)
    if not drink:
        d.ellipse([hx - 18, hy - 6, hx - 8, hy + 4], fill=INK)
    # front leg
    d.line([(cx - 40, cy + 30), (cx - 40, cy + 46)], fill=CAT, width=14)

def draw_figure(d, f):
    ground = 1290
    # presence windows: refill beats + twist peek + climax
    if 140 <= f < 240:
        fx = 415
        mood = "sleepy" if f < 185 else "awake"
    elif 262 <= f < 345:
        fx = 150
        mood = "wow"
    elif f >= 345:
        fx = int(415 - 115 * fade(f, 368, 392))
        mood = "touched"
    else:
        return
    hip = (fx, ground - 300)
    neck = (fx + 16, hip[1] - 215)
    head = (neck[0] + 14, neck[1] - 96)
    sh = (neck[0], neck[1] + 20)
    limb(d, [hip, (fx - 34, ground - 150), (fx - 52, ground)])
    limb(d, [hip, (fx + 40, ground - 150), (fx + 62, ground)])
    limb(d, [hip, neck], 22)
    if pouring(f):
        # right arm up holding a jug tilted toward the glass
        hand = (sh[0] + 128, sh[1] + 30)
        limb(d, [sh, (sh[0] + 84, sh[1] + 52), hand])
        limb(d, [sh, (sh[0] - 44, sh[1] + 110), (sh[0] - 30, sh[1] + 205)])
        jx, jy = hand[0] + 26, hand[1] - 8
        d.polygon([(jx - 30, jy - 44), (jx + 34, jy - 30), (jx + 22, jy + 34), (jx - 18, jy + 30)], fill=(168, 196, 214), outline=INK)
        d.line([(jx + 30, jy + 16), (652, 906)], fill=WATER, width=7)
    elif 262 <= f < 345:
        # peeking: both arms down, still
        limb(d, [sh, (sh[0] - 40, sh[1] + 108), (sh[0] - 26, sh[1] + 200)])
        limb(d, [sh, (sh[0] + 48, sh[1] + 104), (sh[0] + 60, sh[1] + 196)])
    else:
        limb(d, [sh, (sh[0] - 44, sh[1] + 110), (sh[0] - 30, sh[1] + 205)])
        limb(d, [sh, (sh[0] + 52, sh[1] + 104), (sh[0] + 66, sh[1] + 198)])
    face(d, head[0], head[1], 88, mood)
    if 185 <= f < 240:
        d.text((head[0] + 118, head[1] - 128), "？", font=F_MID, fill=BROWN, anchor="ma")

WX0, WY0, WX1, WY1 = 300, 380, 900, 1050   # window
SILL_Y = 1050

start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
end = int(sys.argv[2]) if len(sys.argv) > 2 else FRAMES
for f in range(start, end):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1300, W, H], fill=FLOOR)
    d.ellipse([180, 1252, 700, 1310], fill=(222, 205, 168))

    # window + sky + sun + clouds
    d.rounded_rectangle([WX0 - 18, WY0 - 18, WX1 + 18, WY1 + 18], radius=26, fill=FRAMEC)
    d.rounded_rectangle([WX0, WY0, WX1, WY1], radius=18, fill=sky_color(f))
    if f < 262:
        if f < 110:
            sx, sy = 720, 520
        else:
            p = ((f - 110) % 52) / 52.0
            sx = 380 + 440 * p
            sy = 560 - 130 * math.sin(p * math.pi)
        d.ellipse([sx - 42, sy - 42, sx + 42, sy + 42], fill=(255, 213, 92))
    else:
        d.ellipse([738, 830, 822, 914], fill=(255, 183, 102))
    clx = 420 + (f % 200) * 0.5
    d.ellipse([clx, 470, clx + 150, 520], fill=(255, 255, 255))
    d.ellipse([clx + 60, 450, clx + 190, 505], fill=(255, 255, 255))
    d.rectangle([592, WY0, 608, WY1], fill=FRAMEC)
    d.rectangle([WX0, 706, WX1, 722], fill=FRAMEC)

    # sill
    d.rectangle([258, SILL_Y, 942, SILL_Y + 58], fill=WOOD)
    d.ellipse([596, SILL_Y - 8, 706, SILL_Y + 10], fill=(222, 205, 168))

    # plant pot (left on sill)
    d.polygon([(352, 968), (428, 968), (416, 1046), (364, 1046)], fill=(196, 120, 84))
    for ang in (-0.7, -0.25, 0.25, 0.7):
        ex = 390 + 62 * math.sin(ang)
        ey = 968 - 58 * math.cos(ang)
        d.line([(390, 972), (ex, ey)], fill=LEAF, width=10)
        d.ellipse([ex - 14, ey - 14, ex + 14, ey + 14], fill=LEAF)

    # glass of water
    lvl = water_level(f)
    wtop = 1040 - int(lvl * 138)
    d.rectangle([620, wtop, 684, 1038], fill=WATER)
    d.rounded_rectangle([614, 884, 690, 1044], radius=10, outline=INK, width=5)

    draw_cat(d, f)
    draw_figure(d, f)

    # texts
    if f < 110:
        d.text((540, 128), "窗台這杯水", font=F_HOOK, fill=BROWN, anchor="ma")
        d.text((540, 216), "每天都會自己消失", font=F_HOOK, fill=BROWN, anchor="ma")
    elif f < 262:
        day = 1 + (f - 110) // 30
        d.rounded_rectangle([806, 116, 986, 196], radius=20, fill=(255, 253, 246), outline=FRAMEC, width=3)
        d.text((896, 156), f"第 {day} 天", font=F_TICK, fill=BROWN, anchor="mm")
        if f >= 176:
            d.text((430, 150), "他每天補滿，從來不問", font=F_MID, fill=BROWN, anchor="ma")
    elif f < 345:
        if f >= 292:
            d.text((540, 150), "原來，是樓下的貓", font=F_MID, fill=BROWN, anchor="ma")
    if f >= 345:
        d.rounded_rectangle([90, 1420, 990, 1690], radius=28, fill=(255, 253, 246))
        d.text((540, 1478), "有些善良", font=F_PAY, fill=BROWN, anchor="ma")
        d.text((540, 1570), "不用被發現", font=F_PAY, fill=BROWN, anchor="ma")
        d.text((540, 1752), "你有沒有也在偷偷照顧誰？留言告訴我", font=font(44), fill=BROWN, anchor="ma")
        d.text((540, 1832), "追蹤起來，下一篇不迷路", font=F_SM, fill=(150, 124, 88), anchor="ma")

    img.save(f"{OUT}/frame_{f:04d}.png")

print("frames done: warm-water", FRAMES)
