#!/usr/bin/env python3
# render25.py — breakout-replication overlay: extreme counters, day jumps,
# ending = frozen final tableau + identity question (NO aphorism card).
# usage: python3 render25.py <pullup|jar|mountain|piano>
# footage: ~/workspace/your_files/flow-<name>-i2v.mp4 (720x1280, ~7.93s)
# output : ~/workspace/your_files/flow-<name>-full.mp4 (720x1280, 30fps, ~10.4s, light-music bed)
import os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
TC = 3
def font(s): return ImageFont.truetype(BOLD, s, index=TC)

CFG = {
    "pullup": dict(
        hook=["同一根單槓", "一年後差多少？"],
        l_label="動機派", r_label="自律派", metric="單槓", unit=" 下",
        prefix="", l_final=8, r_final=12480, loser="freeze", l_val_y=438, l_val_alpha=255,
        dayfmt="第 {} 天", question="你是哪一派？", qsub="留言告訴我",
        follow="追蹤起來，下一篇不迷路"),
    "jar": dict(
        hook=["同一個存錢罐", "一年後差多少？"],
        l_label="先花派", r_label="先存派", metric="存下", unit="",
        prefix="$", l_final=0, r_final=36500, loser="drain", loser_peak=300,
        dayfmt="第 {} 天", question="你是哪一派？", qsub="留言告訴我",
        follow="追蹤起來，下一篇不迷路"),
    "mountain": dict(
        hook=["Same mountain.", "One year later?"],
        l_label="The Quitter", r_label="The Climber", metric="Altitude", unit=" m",
        prefix="", l_final=300, r_final=4800, loser="freeze",
        dayfmt="DAY {}", question="WHICH ONE ARE YOU?", qsub="Comment below",
        follow="Follow for more"),
    "piano": dict(
        hook=["同一台鋼琴", "一年後差多少？"],
        l_label="三天派", r_label="天天練", metric="練琴", unit=" 小時",
        prefix="", l_final=2, r_final=1095, loser="freeze",
        dayfmt="第 {} 天", question="你是哪一派？", qsub="留言告訴我",
        follow="追蹤起來，下一篇不迷路"),
}
name = sys.argv[1]
cfg = CFG[name]

W, H, FPS = 720, 1280, 30
SRC = os.path.expanduser(f"~/workspace/your_files/flow-{name}-i2v.mp4")
OUT = os.path.expanduser(f"~/workspace/your_files/flow-{name}-full.mp4")
TMP = f"/tmp/flowov25-{name}"
shutil.rmtree(TMP, ignore_errors=True)
os.makedirs(TMP + "/raw"); os.makedirs(TMP + "/out")

subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SRC, "-vf", "fps=30",
                TMP + "/raw/f_%04d.png"], check=True)
raw = sorted(f for f in os.listdir(TMP + "/raw") if f.endswith(".png"))
NF = len(raw)
print(name, "footage frames:", NF)

GOLD = (255, 201, 84); GREY = (205, 208, 220); WHITE = (245, 245, 245)
DIM = (150, 152, 165)

def text_c(d, cx, y, s, fnt, fill, alpha=255):
    w = d.textlength(s, font=fnt)
    d.text((cx - w / 2, y), s, font=fnt, fill=fill + (alpha,))

def glow_text(base, cx, y, s, fnt, fill, alpha=255):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w = d.textlength(s, font=fnt)
    d.text((cx - w / 2, y), s, font=fnt, fill=fill + (alpha,))
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(6)))
    d2 = ImageDraw.Draw(base)
    d2.text((cx - w / 2, y), s, font=fnt, fill=fill + (alpha,))

def fmt(v):
    return f"{cfg['prefix']}{v:,}{cfg['unit']}"

def loser_val(u):
    if cfg["loser"] == "freeze":
        return cfg["l_final"] if u >= 0.25 else int(cfg["l_final"] * (u / 0.25))
    # drain: rises to peak by 0.25, holds to 0.40, drains to 0 by 0.55
    peak = cfg["loser_peak"]
    if u < 0.25: return int(peak * (u / 0.25))
    if u < 0.40: return peak
    if u < 0.55: return int(peak * (1 - (u - 0.40) / 0.15))
    return 0

def winner_val(u):
    return int(cfg["r_final"] * (u ** 1.7)) if u < 1 else cfg["r_final"]

def hud_text(img, cx, y, s, fnt, fill, a, back_alpha=205):
    d = ImageDraw.Draw(img)
    w = d.textlength(s, font=fnt)
    back = Image.new("RGBA", (int(w) + 28, fnt.size + 16), (0, 0, 0, back_alpha))
    img.alpha_composite(back, (int(cx - w / 2) - 14, y - 4))
    d = ImageDraw.Draw(img)
    text_c(d, cx, y, s, fnt, fill, a)

def draw_hud(img, u, a):
    d = ImageDraw.Draw(img)
    y = 56
    for line in cfg["hook"]:
        glow_text(img, W // 2, y, line, font(42), WHITE, a)
        y += 54
    day = 1 + int(364 * (u ** 2.0))
    dtxt = cfg["dayfmt"].format(day)
    tw = d.textlength(dtxt, font=font(38))
    cw = int(tw) + 48
    chip = Image.new("RGBA", (cw, 64), (0, 0, 0, 150))
    img.alpha_composite(chip, (W // 2 - cw // 2, y + 6))
    d = ImageDraw.Draw(img)
    text_c(d, W // 2, y + 16, dtxt, font(38), GOLD, a)
    lv, rv = loser_val(u), winner_val(u)
    hud_text(img, 178, 268, cfg["l_label"], font(33), GREY, a)
    hud_text(img, 178, cfg.get("l_val_y", 314), f"{cfg['metric']} {fmt(lv)}", font(36), DIM, a, cfg.get("l_val_alpha", 205))
    hud_text(img, 528, 268, cfg["r_label"], font(33), GOLD, a)
    hud_text(img, 528, 314, f"{cfg['metric']} {fmt(rv)}", font(36), GOLD, a)

idx = 0
last = None
for i, fn in enumerate(raw):
    u = i / max(NF - 1, 1)
    img = Image.open(TMP + "/raw/" + fn).convert("RGBA")
    a = min(255, int(255 * i / 20)) if i < 20 else 255
    draw_hud(img, u, a)
    img.convert("RGB").save(TMP + "/out/f_%04d.png" % idx); idx += 1
    last = img

# ending tableau: last frame held 2.5s, final numbers big, identity question
HOLD = 75
for j in range(HOLD):
    img = last.copy()
    dim = Image.new("RGBA", (W, H), (0, 0, 0, 110))
    img.alpha_composite(dim)
    d = ImageDraw.Draw(img)
    text_c(d, 178, 700, cfg["l_label"], font(34), GREY)
    text_c(d, 528, 700, cfg["r_label"], font(34), GOLD)
    text_c(d, 178, 748, fmt(cfg["l_final"]), font(58), DIM)
    text_c(d, 528, 748, fmt(cfg["r_final"]), font(58), GOLD)
    if j >= 10:
        aq = min(255, int(255 * (j - 10) / 15)) if j < 25 else 255
        glow_text(img, W // 2, 880, cfg["question"], font(52), WHITE, aq)
        text_c(d, W // 2, 962, cfg["qsub"], font(32), WHITE, aq)
    if j >= 35:
        af = min(255, int(255 * (j - 35) / 15)) if j < 50 else 255
        text_c(d, W // 2, 1150, cfg["follow"], font(28), DIM, af)
    img.convert("RGB").save(TMP + "/out/f_%04d.png" % idx); idx += 1

total = idx
dur = total / FPS
print(name, "total frames:", total, "duration:", round(dur, 2))

VID = TMP + "/video.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i",
                TMP + "/out/f_%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-crf", "20", VID], check=True)
# light-music bed at exact duration, then mux
subprocess.run(["python3", os.path.expanduser("~/workspace/projects/test-reel-001/make_bed25.py"),
                str(dur), TMP + "/bed.wav"], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", VID, "-i", TMP + "/bed.wav",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", OUT], check=True)
shutil.rmtree(TMP, ignore_errors=True)
print(name, "done ->", OUT)
