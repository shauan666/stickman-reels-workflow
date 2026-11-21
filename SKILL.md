---
name: stickman-reels-workflow
description: Produce A/B-contrast stick-figure motivational Reels (still → video → code overlay → publish → daily diagnosis). Includes a free code-only route (no generation AI, no credits) and an optional AI-video route. Use when asked to make stickman/stick-figure short videos, motivational reels, or A/B discipline-vs-motivation videos.
---

# Stickman Reels Workflow

You are producing stick-figure short videos for the project owner, following this skill.
Read `README.md` in this repo for the format rationale and real results. This file is the operating procedure.

## The format (non-negotiable)

1. Frame 1 = the whole game: a question hook + both sides' labels + counters at zero, in one frame.
2. Nonlinear time jumps (Day 1 → Day 365). The loser FREEZES at the first jump; the winner accelerates to an absurd magnitude (8 vs 12,480; $0 vs $36,500).
3. One event at 50–70% (quitting, summit, overflow, applause) — not a straight race.
4. The ending SHOWS the conclusion as a visual event. No aphorism cards.
5. Final line is an identity question only: 「你是哪一派？ / WHICH ONE ARE YOU?」
6. ≤15 seconds. Always with music (silent videos underperform; platforms flag it).
7. Every topic needs demand evidence: a big account's recent outlier > the same topic travelling across accounts > trend surfaces > evergreen concept bank. No random picks.
8. A genuinely different version per surface. Never burst-post the identical file to multiple surfaces (measured: identical file posted to 4 surfaces in 65 seconds → all zero views).

## Route A — FREE, code only (no generation AI, no credits)

Needs only Python 3 + Pillow + ffmpeg.

| Engine | What it makes | Script |
|---|---|---|
| Split-screen duel | Side-by-side game state, grid/count progress, 14s | `scripts/render16.py` (config-driven) |
| Scene engine | Figures actually performing: faucet saving, reading/book stacks, archery, push-ups | `scripts/render17.py` |
| Warm story | Beige, round-headed faced figures, single-protagonist micro-story with a warm twist | `scripts/render23.py` |
| Overlay + music | Text/counters over any footage; synthesized light-music bed, zero copyright risk | `scripts/render25.py`, `scripts/make_bed25.py` |

Steps: pick a config (or add one: two-line hook, loser label + pattern, winner label + extreme final number, closing question) → run the script → QA (below) → deliver mp4 (1080×1920 or 720×1280).

## Route B — AI video (livelier motion, costs credits)

Still image keyframe (composed as a legible A/B comparison) → image-to-video (e.g. Google Flow / Veo, 8s, ~20 credits/clip) → `render25.py` overlay + light music.

- Video models garble text: ALL text is composited in code afterwards. Never ask the video model to render words.
- Watermark-check every generated clip frame by frame; reject watermarked clips.
- Check the credit balance before generating; log cost + remaining balance per account after each clip.

## QA gates (a video that fails is not delivered)

1. Both figures are ACTING, not standing in poses.
2. The 30-day / one-year progress is countable by eye.
3. The scene is genuinely different from the previous video (new text alone is not a new video).
4. Sample mid + ending frames: text crisp, nothing occluded, no garbled characters, no watermark.

## Captions & reporting

Caption: hook + search keyword first → content → side-picking question → 3–5 hashtags at the end (never a long tag row).
Report effect, not activity: views → retention (skip rate, avg watch seconds) → follows → inquiries → revenue.
Any near-zero video gets a diagnosis, not just a number: account status / first-batch distribution / retention / same format on another surface.

## Never

- Never burst-post identical files across surfaces.
- Never let a video model render on-screen text.
- Never put private accounts, emails, or credit ledgers into a public repo — publish method and results only.
- Never promise a platform monetization date (invitation-based; the platform decides).
