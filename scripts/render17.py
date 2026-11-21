#!/usr/bin/env python3
"""Scene engine (render17): same split-screen structure as render16,
but each topic gets its OWN animated scene instead of the calendar
grid — the figures actually DO the activity.
  faucet  : dripping tap fills a jar (savings)
  reading : seated reader + a growing stack of finished books
  archery : archer shooting at a target, arrows accumulate
  pushup  : push-ups, loser quits and lies flat (discipline)
14s, 1080x1920, 30fps. Usage: python3 render17.py <config>
"""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H, FPS = 1080, 1920, 30
FRAMES = 420
NAME = sys.argv[1]
OUT = f"/tmp/scene-{NAME}-frames"
os.makedirs(OUT, exist_ok=True)

BG = (8, 8, 12)
WHITE = (245, 245, 245)
GOLD = (255, 196, 64)
RED = (255, 110, 90)
GREY = (200, 205, 215)
DIMGREY = (105, 108, 118)
CORE = (5, 5, 9)
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
TC = 3

def font(s): return ImageFont.truetype(BOLD, s, index=TC)

TEXTS = []
def text_c(cx, y, s, fnt, fill):
    TEXTS.append((cx, y, s, fnt, fill))

def fade(t, a, b):
    return 0.0 if t <= a else 1.0 if t >= b else (t - a) / (b - a)
def blend(c1, c2, k):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * k) for i in range(3))
def lerp(a, b, k): return a + (b - a) * k

def spotlight(d, cx, top, ground, tint, spread=1.0):
    d.polygon([(cx - 60, top), (cx + 60, top), (cx + 330 * spread, ground), (cx - 330 * spread, ground)], fill=tint)
    d.polygon([(cx - 30, top), (cx + 30, top), (cx + 180 * spread, ground), (cx - 180 * spread, ground)],
              fill=tuple(min(255, c + 14) for c in tint))

def limb2(d, md, pts, w_rim, w_mask, col):
    d.line(pts, fill=col, width=w_rim, joint="curve")
    md.line(pts, fill=255, width=w_mask, joint="curve")

def figure(d, md, x, ground, rim, P):
    hip = (x + P.get("sway", 0), ground - P["hip_h"])
    neck = (hip[0] + P.get("lean", 0), hip[1] - P["torso"])
    head = (neck[0] + P.get("head_dx", 0), neck[1] - 44 + P.get("head_drop", 0))
    sh = (neck[0], neck[1] + 14)
    for sgn in (-1, 1):
        foot = (x + sgn * P.get("stance", 26), ground)
        knee = ((hip[0] + foot[0]) / 2 + sgn * P.get("knee", 6), (hip[1] + ground) / 2)
        limb2(d, md, [hip, knee, foot], 13, 8, rim)
    limb2(d, md, [hip, neck], 15, 10, rim)
    for key in ("armL", "armR"):
        el, ha = P[key]
        elbow = (sh[0] + el[0], sh[1] + el[1])
        hand = (elbow[0] + ha[0], elbow[1] + ha[1])
        limb2(d, md, [sh, elbow, hand], 12, 7, rim)
    d.ellipse([head[0] - 33, head[1] - 33, head[0] + 33, head[1] + 33], outline=rim, width=6)
    md.ellipse([head[0] - 30, head[1] - 30, head[0] + 30, head[1] + 30], fill=255)

def pose_watch(f, phase=0.0):
    bob = 2.2 * math.sin(f * 0.11 + phase) + 1.2 * math.sin(f * 0.043 + phase)
    return dict(hip_h=150 + bob, torso=118, lean=2 * math.sin(f * 0.02 + phase),
                sway=3 * math.sin(f * 0.017 + phase), stance=26, knee=6,
                head_drop=0, head_dx=0,
                armL=((-16, 52), (-22, 44)), armR=((16, 52), (22, 44)))

def pose_mix(p1, p2, k):
    out = {}
    for key in p1:
        v1, v2 = p1[key], p2[key]
        if isinstance(v1, tuple):
            out[key] = tuple(tuple(lerp(a, b, k) for a, b in zip(s1, s2)) for s1, s2 in zip(v1, v2))
        else:
            out[key] = lerp(v1, v2, k)
    return out

def sized(s, base):
    if len(s) > 22: return font(int(base * 0.62))
    if len(s) > 14: return font(int(base * 0.78))
    return font(base)

LX, RX = 272, 808
SG = 990                      # scene ground line
DAY_START, DAY_END = 15, 320
ANS_START = 330
LEFT_PAT = {0, 1, 3, 6, 8, 10}

def pat_count(day_f):
    return len([p for p in LEFT_PAT if p < day_f])

# ---------- scenes (each returns the counter value for that side) ----------

def scene_faucet(d, md, cx, rim, is_b, day_f, day_i, f, freeze_k):
    jar_x0, jar_x1, jar_t, jar_b = cx - 105, cx + 85, 705, SG
    val = day_i * 100 if is_b else pat_count(day_f) * 100
    level = (val / 3000.0) * (jar_b - jar_t - 26)
    surf = jar_b - level
    if level > 2:
        d.rectangle([jar_x0 + 7, surf, jar_x1 - 7, jar_b - 7], fill=(23, 52, 84))
        d.line([jar_x0 + 7, surf, jar_x1 - 7, surf], fill=(110, 180, 235), width=4)
    d.rectangle([jar_x0, jar_t, jar_x1, jar_b], outline=rim, width=5)
    # faucet: pipe + spout + handle, spout above jar left part
    sx = cx - 55
    d.line([cx - 185, 648, sx, 648], fill=rim, width=13)
    d.line([sx, 648, sx, 692], fill=rim, width=13)
    d.line([cx - 140, 622, cx - 140, 648], fill=rim, width=9)
    d.line([cx - 162, 622, cx - 118, 622], fill=rim, width=9)
    active = (day_f < 30) if is_b else (day_f <= 11)
    if active and f >= DAY_START:
        for k in range(2):
            span = max(30.0, surf - 700)
            dy = 700 + ((f * 13 + k * 47) % span)
            d.ellipse([sx - 6, dy, sx + 6, dy + 15], fill=(110, 180, 235))
    watch = pose_watch(f, 0 if not is_b else 2.0)
    if is_b:
        figure(d, md, cx + 168, SG, GOLD, watch)
    else:
        slump = dict(watch); slump["head_drop"] = 30; slump["lean"] = 13
        slump["armL"] = ((-12, 56), (-14, 50)); slump["armR"] = ((12, 56), (14, 50))
        figure(d, md, cx + 168, SG, blend(GREY, DIMGREY, freeze_k), pose_mix(watch, slump, fade(f, 118, 160)))
    return val

def scene_reading(d, md, cx, rim, is_b, day_f, day_i, f, freeze_k):
    books = int(day_f // 5) if is_b else (1 if day_f >= 3 else 0)
    # stack of finished books, left of the stool
    for i in range(books):
        y1 = SG - 25 * i; y0 = y1 - 23
        jit = 5 if i % 2 else -4
        col = GOLD if (i % 3 != 2) else GREY
        if not is_b: col = GREY
        d.rectangle([cx - 205 + jit, y0, cx - 112 + jit, y1], outline=col, width=4)
    # stool
    d.line([cx - 105, 878, cx + 28, 878], fill=rim, width=8)
    d.line([cx - 92, 878, cx - 92, SG], fill=rim, width=7)
    d.line([cx + 15, 878, cx + 15, SG], fill=rim, width=7)
    # seated figure
    hip = (cx - 38, 868)
    droop = 0 if is_b else int(30 * freeze_k)
    neck = (hip[0] + 4 + droop // 3, hip[1] - 168)
    bob = 2.0 * math.sin(f * 0.09) if is_b else 0
    head = (neck[0] + 10, neck[1] - 52 + droop + bob)
    sh = (neck[0], neck[1] + 12)
    limb2(d, md, [hip, (cx + 38, 872), (cx + 38, SG - 4)], 13, 8, rim)   # front leg
    limb2(d, md, [hip, (cx - 2, 884), (cx - 8, SG - 4)], 13, 8, rim)     # back leg
    limb2(d, md, [hip, neck], 15, 10, rim)
    if is_b or freeze_k < 0.5:
        # open book in hands
        bc = (sh[0] + 58, sh[1] + 62)
        limb2(d, md, [sh, (bc[0] - 38, bc[1] - 6), (bc[0] - 8, bc[1] + 16)], 12, 7, rim)
        limb2(d, md, [sh, (bc[0] + 40, bc[1] - 4), (bc[0] + 10, bc[1] + 16)], 12, 7, rim)
        d.polygon([(bc[0] - 52, bc[1] - 16), (bc[0], bc[1] + 2), (bc[0], bc[1] + 44), (bc[0] - 52, bc[1] + 26)], outline=rim, width=5)
        d.polygon([(bc[0] + 52, bc[1] - 16), (bc[0], bc[1] + 2), (bc[0], bc[1] + 44), (bc[0] + 52, bc[1] + 26)], outline=rim, width=5)
    else:
        # book closed on lap, head down, Zzz
        limb2(d, md, [sh, (hip[0] + 26, hip[1] - 38), (hip[0] + 52, hip[1] - 22)], 12, 7, rim)
        limb2(d, md, [sh, (hip[0] - 6, hip[1] - 30), (hip[0] + 16, hip[1] - 16)], 12, 7, rim)
        d.rectangle([hip[0] + 22, hip[1] - 34, hip[0] + 86, hip[1] - 14], outline=rim, width=5)
        if f > 175:
            text_c(cx + 82, 606, "Z", font(48), DIMGREY)
            text_c(cx + 110, 570, "Z", font(36), DIMGREY)
    d.ellipse([head[0] - 33, head[1] - 33, head[0] + 33, head[1] + 33], outline=rim, width=6)
    md.ellipse([head[0] - 30, head[1] - 30, head[0] + 30, head[1] + 30], fill=255)
    return books

def _shots(seed, n, start0, start1, jitter, miss_p):
    rng = random.Random(seed)
    out = []
    for i in range(n):
        sf = start0 + (start1 - start0) * (i / max(1, n - 1)) + rng.randint(-4, 4)
        out.append((sf, rng.uniform(-jitter, jitter), rng.uniform(-jitter, jitter), rng.random() < miss_p))
    return out

SHOTS = {
    True: _shots(11, 26, 30, 312, 34, 0.0),     # winner: tight grouping
    False: _shots(23, 5, 26, 96, 95, 0.4),      # loser: few, wild, quits
}

def scene_archery(d, md, cx, rim, is_b, day_f, day_i, f, freeze_k):
    val = day_i * 10 if is_b else min(day_i, 2) * 10
    tc = (cx + 128, 756)  # target centre
    # target stand + rings
    d.line([tc[0] - 42, SG, tc[0], 830], fill=rim, width=7)
    d.line([tc[0] + 42, SG, tc[0], 830], fill=rim, width=7)
    for r, col, wdt in ((96, WHITE if is_b else GREY, 5), (64, rim, 5), (30, GOLD if is_b else GREY, 5)):
        d.ellipse([tc[0] - r, tc[1] - r, tc[0] + r, tc[1] + r], outline=col, width=wdt)
    d.ellipse([tc[0] - 9, tc[1] - 9, tc[0] + 9, tc[1] + 9], fill=GOLD if is_b else GREY)
    # archer, side-on facing the target
    ax = cx - 148
    hip = (ax, SG - 150); neck = (ax + 4, hip[1] - 118); head = (neck[0] + 4, neck[1] - 46)
    sh = (neck[0], neck[1] + 14)
    limb2(d, md, [hip, (ax - 26, SG - 74), (ax - 42, SG)], 13, 8, rim)
    limb2(d, md, [hip, (ax + 24, SG - 74), (ax + 40, SG)], 13, 8, rim)
    limb2(d, md, [hip, neck], 15, 10, rim)
    d.ellipse([head[0] - 33, head[1] - 33, head[0] + 33, head[1] + 33], outline=rim, width=6)
    md.ellipse([head[0] - 30, head[1] - 30, head[0] + 30, head[1] + 30], fill=255)
    shooting = is_b or f < 120
    if shooting:
        bow_t = (sh[0] + 66, sh[1] - 58); bow_b = (sh[0] + 66, sh[1] + 66)
        limb2(d, md, [sh, (sh[0] + 62, sh[1] - 4), (bow_t[0] - 4, bow_t[1] + 52)], 12, 7, rim)  # bow arm
        limb2(d, md, [sh, (sh[0] - 30, sh[1] + 10), (sh[0] + 6, sh[1] + 2)], 12, 7, rim)       # draw arm
        d.arc([bow_t[0] - 26, bow_t[1], bow_b[0] + 30, bow_b[1]], start=288, end=72, fill=rim, width=7)
        d.line([bow_t[0] + 8, bow_t[1] + 4, bow_b[0] + 8, bow_b[1] - 4], fill=rim, width=3)
        muzzle = (bow_t[0] + 16, sh[1] - 2)
    else:
        limb2(d, md, [sh, (sh[0] + 30, sh[1] + 52), (sh[0] + 44, sh[1] + 96)], 12, 7, rim)
        limb2(d, md, [sh, (sh[0] - 14, sh[1] + 54), (sh[0] - 8, sh[1] + 98)], 12, 7, rim)
        d.arc([sh[0] + 18, sh[1] + 58, sh[0] + 74, sh[1] + 168], start=288, end=72, fill=rim, width=7)
        muzzle = (sh[0] + 60, sh[1] + 60)
    # arrows: flown ones stick, one may be mid-flight
    for sf, jx, jy, miss in SHOTS[is_b]:
        if f < sf: continue
        hit = (tc[0] + 60 + jx * 0.4, SG - 6) if miss else (tc[0] + jx, tc[1] + jy)
        k = (f - sf) / 6.0
        if k < 1.0:
            px = lerp(muzzle[0], hit[0], k); py = lerp(muzzle[1], hit[1], k) - 26 * math.sin(k * math.pi)
            d.line([px - 40, py + 8, px, py], fill=WHITE, width=5)
            d.line([px - 40, py + 8, px - 28, py - 4], fill=rim, width=4)
        else:
            d.line([hit[0] - 52, hit[1] - 14, hit[0], hit[1]], fill=WHITE, width=5)
            d.line([hit[0] - 52, hit[1] - 14, hit[0] - 38, hit[1] - 26], fill=rim, width=4)
            d.line([hit[0] - 52, hit[1] - 14, hit[0] - 40, hit[1] - 2], fill=rim, width=4)
    return val

def scene_pushup(d, md, cx, rim, is_b, day_f, day_i, f, freeze_k):
    val = day_i * 30 if is_b else min(day_i, 6) * 30
    active = is_b or f < 118
    if active:
        body_y = 838 + 15 * math.sin(f * 0.55) if f >= DAY_START else 845
        head = (cx - 158, body_y - 4)
        neck = (cx - 118, body_y); hip = (cx + 6, body_y + 4)
        limb2(d, md, [hip, (cx + 88, 922), (cx + 158, SG - 2)], 13, 8, rim)
        limb2(d, md, [neck, hip], 15, 10, rim)
        elbow = (neck[0] - 16, (body_y + SG) / 2)
        limb2(d, md, [neck, elbow, (neck[0] + 2, SG - 2)], 12, 7, rim)
        limb2(d, md, [neck, (elbow[0] + 26, elbow[1]), (neck[0] + 28, SG - 2)], 12, 7, rim)
    else:
        # lying flat, done
        head = (cx - 168, SG - 26)
        neck = (cx - 128, SG - 16); hip = (cx + 6, SG - 14)
        limb2(d, md, [hip, (cx + 92, SG - 8), (cx + 162, SG - 2)], 13, 8, rim)
        limb2(d, md, [neck, hip], 15, 10, rim)
        limb2(d, md, [neck, (cx - 74, SG - 8), (cx - 30, SG - 4)], 12, 7, rim)
        if f > 175:
            text_c(cx - 146, 866, "Z", font(48), DIMGREY)
            text_c(cx - 118, 830, "Z", font(36), DIMGREY)
    d.ellipse([head[0] - 31, head[1] - 31, head[0] + 31, head[1] + 31], outline=rim, width=6)
    md.ellipse([head[0] - 28, head[1] - 28, head[0] + 28, head[1] + 28], fill=255)
    return val

CONFIGS = {
    "faucet": dict(scene=scene_faucet,
        hook=("薪水一進來就花光的人", "30 天後輸在哪？"), day="第 {} 天",
        a_label="先花再說", b_label="先存再花", cnt_label="累積存款", cnt_fmt="money",
        ans=("錢不是月底剩的", "是月初先留的")),
    "reading": dict(scene=scene_reading,
        hook=("買書不讀的人", "30 天後輸在哪？"), day="第 {} 天",
        a_label="買了再說", b_label="每天讀 10 頁", cnt_label="讀完本數", cnt_fmt="unit", unit="本",
        ans=("書不是買來放的", "讀完才算你的")),
    "archery": dict(scene=scene_archery,
        hook=("等手感來才練的人", "30 天後輸在哪？"), day="第 {} 天",
        a_label="等手感來", b_label="天天練 10 箭", cnt_label="練習箭數", cnt_fmt="unit", unit="箭",
        ans=("贏的不是手感", "是射出去的箭")),
    "pushup": dict(scene=scene_pushup,
        hook=("等有動力才開始的人", "30 天後輸在哪？"), day="第 {} 天",
        a_label="動機派", b_label="自律派", cnt_label="伏地挺身", cnt_fmt="unit", unit="下",
        ans=("贏的不是天分", "是出現的次數")),
}
CFG = CONFIGS[NAME]
CTA = "你是哪一派？留言告訴我。"
FOLLOW = "追蹤起來，下一篇不迷路"

F_DAY = font(66)
F_CNTLAB = font(42)
F_CTA = font(54)
F_SM = font(44)

def cnt_text(v):
    if CFG["cnt_fmt"] == "money": return f"${v:,}"
    return f"{v} {CFG['unit']}"

start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
end = int(sys.argv[3]) if len(sys.argv) > 3 else FRAMES
for f in range(start, end):
    art = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(art)
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    TEXTS.clear()

    day_f = min(30.0, max(0.0, (f - DAY_START) / (DAY_END - DAY_START) * 30))
    day_i = int(day_f)
    freeze_k = fade(f, 150, 210)

    spotlight(d, LX, 110, 1210, (22, 21, 25), 0.78)
    spotlight(d, RX, 110, 1210, (34, 30, 16), 0.78)
    d.line([540, 430, 540, 1210], fill=(52, 52, 60), width=3)
    for cx in (LX, RX):
        d.line([cx - 235, SG, cx + 235, SG], fill=(150, 150, 160), width=3)

    text_c(540, 150, CFG["hook"][0], sized(CFG["hook"][0], 74), WHITE)
    text_c(540, 245, CFG["hook"][1], sized(CFG["hook"][1], 88), GOLD)
    text_c(540, 385, CFG["day"].format(max(1, day_i)), F_DAY, WHITE)

    for cx, lab, rim, is_b in (
        (LX, CFG["a_label"], GREY, False),
        (RX, CFG["b_label"], GOLD, True),
    ):
        lab_col = rim if is_b else blend(WHITE, DIMGREY, freeze_k * 0.6)
        text_c(cx, 480, lab, sized(lab, 62), lab_col)
        side_rim = GOLD if is_b else blend(GREY, DIMGREY, freeze_k)
        val = CFG["scene"](d, md, cx, side_rim, is_b, day_f, day_i, f, freeze_k)
        text_c(cx, 1030, CFG["cnt_label"], F_CNTLAB, GREY)
        num_col = GOLD if is_b else blend(RED, (150, 80, 74), freeze_k)
        ntxt = cnt_text(val)
        text_c(cx, 1090, ntxt, sized(ntxt, 88), num_col)

    if f >= ANS_START:
        local = f - ANS_START
        d.rounded_rectangle([70, 1170, 1010, 1520], radius=26, fill=(10, 10, 15))
        k1 = fade(local, 5, 25)
        text_c(540, 1235, CFG["ans"][0], sized(CFG["ans"][0], 80), blend((10, 10, 15), WHITE, k1))
        k2 = fade(local, 30, 52)
        text_c(540, 1345, CFG["ans"][1], sized(CFG["ans"][1], 80), blend((10, 10, 15), GOLD, k2))
        k3 = fade(local, 60, 82)
        text_c(540, 1690, CTA, F_CTA, blend((0, 0, 0), WHITE, k3))
        text_c(540, 1795, FOLLOW, F_SM, blend((0, 0, 0), GOLD, k3))

    glow = art.filter(ImageFilter.GaussianBlur(13))
    comp = Image.new("RGB", (W, H), BG)
    comp = ImageChops.add(comp, glow)
    comp = ImageChops.add(comp, glow)
    comp = ImageChops.screen(comp, art)
    comp = Image.composite(Image.new("RGB", (W, H), CORE), comp, mask)
    tl = Image.new("RGB", (W, H), (0, 0, 0))
    tld = ImageDraw.Draw(tl)
    for cx, y, s, fnt, fill in TEXTS:
        tld.text((cx, y), s, font=fnt, fill=fill, anchor="ma")
    comp = ImageChops.screen(comp, tl.filter(ImageFilter.GaussianBlur(7)))
    comp = ImageChops.screen(comp, tl)
    comp.save(f"{OUT}/frame_{f:04d}.png")

print("frames done: scene-" + NAME, FRAMES)
