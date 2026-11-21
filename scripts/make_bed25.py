#!/usr/bin/env python3
"""Light-music bed, duration-parameterised (from make_lightmusic.py).
User's direction: ASMR-feel LIGHT MUSIC — soft music-box arpeggio + warm pad.
Usage: python3 make_bed25.py <duration_seconds> <out_wav>"""
import math, random, struct, sys, wave

SR = 44100
DUR = float(sys.argv[1])
OUT = sys.argv[2]
N = int(SR * DUR)
random.seed(3)
S = DUR / 12.433  # time scale vs the original 12.433s layout

buf = [0.0] * N

def add_fn(i0, i1, fn, gain):
    for i in range(max(0, i0), min(N, i1)):
        buf[i] += fn((i - i0) / SR) * gain

def note(freq, dur=2.2):
    def fn(t):
        if t > dur:
            return 0.0
        v = math.sin(2 * math.pi * freq * t) * math.exp(-t * 2.0)
        v += 0.45 * math.sin(2 * math.pi * freq * 2.0 * t) * math.exp(-t * 4.5)
        v += 0.22 * math.sin(2 * math.pi * freq * 3.98 * t) * math.exp(-t * 7.0)
        return v * min(1.0, t / 0.004)
    return fn

def place(t0, freq, gain):
    i0 = int(t0 * SR)
    add_fn(i0, i0 + int(2.2 * SR), note(freq), gain)

A3, C4, E4, F3, F4, C5, G3, B3, D4 = 220.0, 261.63, 329.63, 174.61, 349.23, 523.25, 196.0, 246.94, 293.66
G4, A4, B4, D5, E5 = 392.0, 440.0, 493.88, 587.33, 659.25

bars = [(0.0, A3, E4), (3.1, F3, C4), (6.2, C4, G4), (9.3, G3, D4)]
for t0, root, fifth in bars:
    for f in (root / 2, root, fifth):
        def pad_fn(t, f=f):
            return math.sin(2 * math.pi * f * t) * (0.8 + 0.2 * math.sin(2 * math.pi * 0.07 * t))
        i0 = int(t0 * S * SR)
        add_fn(i0, i0 + int(3.2 * S * SR), pad_fn, 0.012)

arp = [
    (0.0, A3), (0.775, C4), (1.55, E4), (2.325, A4),
    (3.1, F3 * 2), (3.875, A3), (4.65, C4), (5.425, F4),
    (6.2, C4), (6.975, E4), (7.75, G4), (8.525, C5),
    (9.3, G3 * 2), (10.075, B3), (10.85, D4), (11.625, G4),
]
for t0, f in arp:
    place(t0 * S, f, 0.055)

mel = [
    (0.35, E5), (1.10, C5), (1.85, A4), (2.60, E5),
    (3.45, F4 * 2), (4.20, A4), (4.95, C5), (5.70, A4),
    (6.55, G4), (7.30, E5), (8.05, C5),
    (8.80, D5), (9.55, B4), (10.30, G4), (11.05, A4), (11.80, E5),
]
for t0, f in mel:
    place(t0 * S, f, 0.085)

noise = 0.0
for i in range(N):
    noise = noise * 0.98 + (random.random() * 2 - 1) * 0.02
    buf[i] += noise * 0.006

for i in range(N):
    t = i / SR
    fade = min(1.0, t / 0.8, (DUR - t) / 1.2)
    buf[i] = max(-0.9, min(0.9, buf[i] * max(0.0, fade)))

with wave.open(OUT, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b"".join(struct.pack("<h", int(v * 32767)) for v in buf))
print("bed written", DUR, "s ->", OUT)
