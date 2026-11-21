#!/usr/bin/env python3
"""Split-screen A/B engine, config-driven (render16).
Same format as render15: both sides in one frame from frame 1, loser
fills 6 of 30 days early then freezes, winner fills all 30. 14s,
1080x1920, 30fps. Configs: save / read / steps / discipline-en.
Usage: python3 render16.py <config> [start] [end]
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H, FPS = 1080, 1920, 30
FRAMES = 420
NAME = sys.argv[1]
OUT = f"/tmp/split-{NAME}-frames"
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

def figure(d, md, x, ground, rim, P):
    hip = (x + P.get("sway", 0), ground - P["hip_h"])
    neck = (hip[0] + P.get("lean", 0), hip[1] - P["torso"])
    head = (neck[0] + P.get("head_dx", 0), neck[1] - 44 + P.get("head_drop", 0))
    sh = (neck[0], neck[1] + 14)
    def limb(draw, pts, wdt, col):
        draw.line(pts, fill=col, width=wdt, joint="curve")
    for sgn in (-1, 1):
        foot = (x + sgn * P.get("stance", 26), ground)
        knee = ((hip[0] + foot[0]) / 2 + sgn * P.get("knee", 6), (hip[1] + ground) / 2)
        limb(d, [hip, knee, foot], 13, rim); limb(md, [hip, knee, foot], 8, 255)
    limb(d, [hip, neck], 15, rim); limb(md, [hip, neck], 10, 255)
    for key in ("armL", "armR"):
        el, ha = P[key]
        elbow = (sh[0] + el[0], sh[1] + el[1])
        hand = (elbow[0] + ha[0], elbow[1] + ha[1])
        limb(d, [sh, elbow, hand], 12, rim); limb(md, [sh, elbow, hand], 7, 255)
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

# CONFIG FIELD REFERENCE (reverse-engineered + documented after usability testing):
#   hook      : (line1, line2) question hook shown at top from frame 1
#   day       : format string with one {} for the day number, e.g. "Day {}"
#   a_label   : loser (left) label;  b_label: winner (right) label
#   cnt_label : counter caption under each grid
#   per       : counter units per filled cell (winner total = 30 * per)
#   cnt_fmt   : "money" ($x,xxx) | "unit" (needs unit=) | "days" | "plain"
#   unit      : unit string, REQUIRED when cnt_fmt="unit" (KeyError mid-render if missing)
#   ans       : (line1, line2) answer lines in the ending panel
#   cta       : closing question line;  follow: follow prompt line
#   Naming a config with the suffix "-en" switches the CTA to the smaller EN font.
# KNOWN LIMITS: the arc is hardwired to 30 days / 30 cells; the loser always
# fills exactly 6 cells (LEFT_PAT), so the loser ends at 20% of the winner.
# Output is silent — mux a bed from make_bed25.py if you need audio.
CONFIGS = {
    "save": dict(
        hook=("薪水一進來就花光的人", "30 天後輸在哪？"), day="第 {} 天",
        a_label="先花再說", b_label="先存再花", cnt_label="累積存款",
        per=100, cnt_fmt="money",
        ans=("錢不是月底剩的", "是月初先留的"),
        cta="你是哪一派？留言告訴我。", follow="追蹤起來，下一篇不迷路"),
    "read": dict(
        hook=("買書不讀的人", "30 天後輸在哪？"), day="第 {} 天",
        a_label="買了再說", b_label="每天讀 10 頁", cnt_label="已讀頁數",
        per=10, cnt_fmt="unit", unit="頁",
        ans=("書不是買來放的", "讀完才算你的"),
        cta="你是哪一派？留言告訴我。", follow="追蹤起來，下一篇不迷路"),
    "steps": dict(
        hook=("等準備好才開始的人", "30 天後輸在哪？"), day="第 {} 天",
        a_label="等準備好", b_label="先走一小步", cnt_label="累積練習",
        per=20, cnt_fmt="unit", unit="分鐘",
        ans=("贏的不是準備", "是先開始的人"),
        cta="你是哪一派？留言告訴我。", follow="追蹤起來，下一篇不迷路"),
    "discipline-en": dict(
        hook=("Waiting to feel motivated?", "Here's your 30 days"), day="Day {}",
        a_label="Motivation", b_label="Discipline", cnt_label="Days shown up",
        per=1, cnt_fmt="plain",
        ans=("Talent doesn't win", "showing up does"),
        cta="Which one are you? Comment below.", follow="Follow for the next one."),
}
CFG = CONFIGS[NAME]
EN = NAME.endswith("-en")

def sized(s, base):
    """Shrink font for long/English lines so nothing clips the frame."""
    if len(s) > 22: return font(int(base * 0.62))
    if len(s) > 14: return font(int(base * 0.78))
    return font(base)

def cnt_text(filled):
    v = filled * CFG["per"]
    if isinstance(v, float):
        v = round(v, 1)
        if v == int(v):
            v = int(v)
    fmt = CFG["cnt_fmt"]
    if fmt == "money": return f"${v:,}"
    if fmt == "unit": return f"{v} {CFG['unit']}"
    if fmt == "days": return f"{v} 天"
    return f"{v}"

LX, RX = 272, 808
GY = 1560
GRID_Y = 640
CELL, GAP = 54, 10
GRID_W = 6 * CELL + 5 * GAP
LEFT_PAT = {0, 1, 3, 6, 8, 10}
RIGHT_PAT = set(range(30))
DAY_START, DAY_END = 15, 320
ANS_START = 330

F_DAY = font(66)
F_LAB = font(62)
F_CNTLAB = font(42)
F_CTA = font(54) if not EN else font(46)
F_SM = font(44)

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

    spotlight(d, LX, 110, GY, (22, 21, 25), 0.78)
    spotlight(d, RX, 110, GY, (34, 30, 16), 0.78)
    d.line([540, 430, 540, GY], fill=(52, 52, 60), width=3)
    d.line([50, GY, 1030, GY], fill=(150, 150, 160), width=3)

    text_c(540, 150, CFG["hook"][0], sized(CFG["hook"][0], 74), WHITE)
    text_c(540, 245, CFG["hook"][1], sized(CFG["hook"][1], 88), GOLD)
    text_c(540, 385, CFG["day"].format(max(1, day_i)), F_DAY, WHITE)

    for cx, pat, lab, rim, is_b in (
        (LX, LEFT_PAT, CFG["a_label"], GREY, False),
        (RX, RIGHT_PAT, CFG["b_label"], GOLD, True),
    ):
        lab_col = rim if is_b else blend(WHITE, DIMGREY, freeze_k * 0.6)
        text_c(cx, 480, lab, sized(lab, 62), lab_col)
        gx0 = cx - GRID_W // 2
        filled = 0
        for i in range(30):
            r, c = divmod(i, 6)
            x = gx0 + c * (CELL + GAP); y = GRID_Y + r * (CELL + GAP)
            if i in pat and i < day_f:
                filled += 1
                if is_b:
                    d.rectangle([x, y, x + CELL, y + CELL], fill=(70, 52, 14), outline=GOLD, width=3)
                else:
                    d.rectangle([x, y, x + CELL, y + CELL], fill=(76, 76, 88), outline=blend(GREY, DIMGREY, freeze_k), width=3)
            else:
                d.rectangle([x, y, x + CELL, y + CELL], outline=(90, 92, 102), width=2)
        text_c(cx, 1015, CFG["cnt_label"], F_CNTLAB, GREY)
        num_col = GOLD if is_b else blend(RED, (150, 80, 74), freeze_k)
        ntxt = cnt_text(filled)
        text_c(cx, 1075, ntxt, sized(ntxt, 88), num_col)

        watch = pose_watch(f, 0 if not is_b else 2.0)
        if is_b:
            figure(d, md, cx, GY, GOLD, watch)
        else:
            slump = dict(watch); slump["head_drop"] = 30; slump["lean"] = 13
            slump["armL"] = ((-12, 56), (-14, 50)); slump["armR"] = ((12, 56), (14, 50))
            k = fade(f, 118, 160)
            pose = pose_mix(watch, slump, k)
            figure(d, md, cx, GY, blend(GREY, DIMGREY, freeze_k), pose)

    if f >= ANS_START:
        local = f - ANS_START
        d.rounded_rectangle([70, 1170, 1010, 1520], radius=26, fill=(10, 10, 15))
        k1 = fade(local, 5, 25)
        text_c(540, 1235, CFG["ans"][0], sized(CFG["ans"][0], 80), blend((10, 10, 15), WHITE, k1))
        k2 = fade(local, 30, 52)
        text_c(540, 1345, CFG["ans"][1], sized(CFG["ans"][1], 80), blend((10, 10, 15), GOLD, k2))
        k3 = fade(local, 60, 82)
        text_c(540, 1690, CFG["cta"], F_CTA, blend((0, 0, 0), WHITE, k3))
        text_c(540, 1795, CFG["follow"], F_SM, blend((0, 0, 0), GOLD, k3))

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

print("frames done: split-" + NAME, FRAMES)

# Auto-encode the finished mp4 on a full run (added after usability testing:
# the original script stopped at PNG frames and left encoding to the user).
if start == 0 and end == FRAMES:
    import subprocess
    out_mp4 = os.path.abspath(f"split-{NAME}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", f"{OUT}/frame_%04d.png", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", out_mp4], check=True)
    print("video written:", out_mp4)
