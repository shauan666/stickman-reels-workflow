# Stickman Reels Workflow — Make Viral Stick-Figure Reels with AI

**A free, working AI workflow for faceless short-form video.** One still image → AI video generation → code-rendered text and counters → publish → daily data diagnosis. This is the exact system behind a live stick-figure channel posting A/B comparison Reels ("discipline vs laziness", "saver vs spender") to **Instagram Reels, Facebook Reels and YouTube Shorts** — built to grow traffic and move toward monetization without filming anything or showing a face.

![IG grid — Flow knife-skills reel at 1,313 views and climbing](assets/ig-grid-knife-1313.jpg)

## Use it in 3 steps (no coding, no filming, no face)

1. **Copy `SKILL.md` into your AI assistant** — Claude, ChatGPT, Gemini, or any AI that can read files and run code. That file is the whole operating procedure.
2. **Give it a topic** — e.g. *"make one about waking up early vs hitting snooze for a year."* The AI follows the format rules below and produces a finished 9:16 video.
3. **Publish it.** The free route (code-drawn scenes, `scripts/`) costs nothing. The optional AI-video route (Google Flow / Veo image-to-video) costs ~20 credits per clip and looks more alive.

That's it. You pick topics and read results; the AI runs the pipeline.

## FAQ

**How do I make a stick figure reel that actually gets views?**
Use the A/B duel format in this repo: frame 1 shows the whole game (question + both side labels + counters at zero), time jumps non-linearly from Day 1 to Day 365, the loser freezes early, the winner accelerates to an extreme number, and the ending *shows* the payoff (summit flag, overflowing jar, applause) instead of stating it. Full rules below.

**Does it cost money?**
No. The code-only route is 100% free (Python + Pillow + ffmpeg). AI-generated footage is an optional upgrade, not a requirement.

**Do I need to show my face or film anything?**
No. Everything is generated or drawn. That is the point of the faceless format.

**Which platforms does this work for?**
Instagram Reels, Facebook Reels, YouTube Shorts and TikTok — any 9:16 short-form platform. Publish a *different version* per platform, staggered in time; bursting the identical file everywhere gets suppressed (we measured it: four copies, zero views).

**How long does one video take?**
About 5–10 minutes end to end once the setup exists: keyframe → image-to-video → code overlay → light-music bed → publish.

**Why do some reels get zero views?**
The usual causes we have verified on our own accounts: silent videos (platforms explicitly flag audio as a performance factor), identical files burst-posted across surfaces, aphorism text-card endings nobody watches, and posting a format the account isn't classified for. Our rule: every near-zero post gets a written diagnosis (account status / first-batch distribution / retention / cross-surface comparison), not just a view count.

**Can this make money?**
Traffic first, honestly. The monetization paths this system is built for: platform creator programs (e.g. Facebook Content Monetization — invite-based, no honest timeline exists), affiliate product links attached to posts, and funnelling attention to your own products or services. Anyone promising you a date is guessing.

**What language does it work in?**
Any. Every text element is a config value. This repo ships Traditional Chinese and English configs; swap the strings.

## 中文說明 — 火柴人 Reels 工作流（免費、免露臉、不用拍攝）

**這是什麼？**
一套免費的 AI 短影音工作流：一張靜圖 → AI 生成影片（或純程式畫場景）→ 程式疊字與計數器 → 發布 → 每天看數據診斷。這是我們實際每天在用的系統，經營火柴人 A/B 對決 Reels（自律 vs 耍廢、存錢派 vs 月光派），同步發 Instagram Reels、Facebook Reels、YouTube Shorts——不用拍攝、不用露臉、不用出鏡。

**要花錢嗎？**
不用。純程式路線（Python + Pillow + ffmpeg）完全免費；AI 生成影片（Google Flow / Veo 圖生影片）是可選升級，一支約 20 點額度，不是必要條件。

**怎麼做一支？**
把本 repo 的 `SKILL.md` 交給你的 AI 助理（Claude、ChatGPT、Gemini，或任何能讀檔和跑程式的 AI），再給它一個主題，例如「早起 vs 賴床一整年」，它會照下面的格式規則產出 9:16 成品。你負責選題和看數據，AI 負責整條產線。

**為什麼有些 Reels 會零觀看？**
我們在自己帳號上驗證過的原因：沒有聲音的影片（平台明確把音訊列為表現因素）、同一支檔案同一時間在多個平台齊發（實測四份複本全部零觀看）、結尾用金句字卡收尾、格式跟帳號的分類不合。我們的規矩是：每一支近零觀看的貼文都要寫出診斷（帳號狀態／第一波分發／留存／跨平台對照），不只報數字。

**能靠這個賺錢嗎？**
先衝流量，老實講。變現路徑是這套系統本來就設計好的：平台創作者計畫（例如 Facebook Content Monetization，是邀請制，沒有人能誠實保證開通時間）、貼文掛聯盟行銷商品連結、把流量導到自己的產品或服務。跟你保證日期的人都是在猜。

**實績證據（可查核）**
一支 13 秒的衝突版火柴人 Reel，2026-11-22 發布於 Facebook，2026-11-24 查核時累計 120884 次瀏覽；同一套 A/B 對決格式在 Instagram 單支最高 3943 次觀看。本 repo 從頭到尾就是做這件事的完整方法，持續更新中。

## The format rules (from viral teardowns + our own published data)

The skeleton is not invented — it is reverse-engineered frame by frame from breakout stick-figure channels of Oct–Nov 2026 (e.g. MindFrame Animation: two Shorts at 22M views within two weeks of launch; Visual Mindset: up to 10M per Short), then corrected against our own numbers:

1. **Frame 1 is the whole game**: question hook + both labels + counters at 0, in one frame.
2. **Non-linear time jumps**: Day 1 → Day 365. The loser freezes at the first jump (single digits); the winner accelerates to an extreme total (8 vs 12,480 reps; $0 vs $36,500).
3. **One event at 50–70%**: a quitting moment, a summit, an overflowing jar — not a straight race.
4. **The ending is shown, never written**: payoff event on screen, no aphorism card. 8 of 10 breakout videos end this way.
5. **One closing question only**: "WHICH ONE ARE YOU?" — an identity question, not a lecture.
6. **≤15 seconds, light-music bed, all text rendered in code** — video models garble on-screen text, so text is never generated, always overlaid.

## The workflow

```
1. Pick a topic with demand evidence (a big account's recent breakout,
   the same topic moving on several accounts, or a proven classic concept)
2. Compose ONE keyframe still: the A/B contrast must read in 1 second
3. Image-to-video (Google Flow / Veo 3.1 Fast, 8s, 720x1280)
   — or a code-drawn scene on the free route; watermark-check every frame
4. Code overlay: hook / day jumps / both counters / ending freeze + question
   + synthesized light-music bed (no copyright risk)
5. Publish a DIFFERENT version per surface, staggered — never burst
6. Next-day diagnosis: views → retention (skip rate, avg watch) → follows
   → inquiries → revenue. Near-zero posts get a cause, not just a number
```

## Real results (measured 2026-11-21 to 2026-11-23)

**Update 2026-11-23:** a video on our Facebook profile passed **82000 views** within a day of posting and is still climbing toward 100000, with viewers actively debating both sides in the comments. Produced end-to-end with the workflow in this repo.

| Video | Views | Notes |
|---|---|---|
| Latte factor (one coffee a day → $1.45M) | 3,504 | Highest engagement rate on the account |
| Split-screen Discipline vs Motivation | 3,332 | Avg watch 9.5s of 14s, 824 replays |
| Why dividend investors don't sell at −20% | 1,418 | |
| Flow knife-skills duel (AI-video route) | 1,313 ↑ | Was 26 views at 25 minutes; kept climbing |
| Flow weeding duel | — | 13.2% skip rate, the account's lowest |

![IG grid overview](assets/ig-grid-overview.jpg)

## What failed (kept honest)

- **Code-drawn stick figures look like slideshows** — motion must be performed by the video model; code only does the text layer.
- **Aphorism endings** — nobody watches a conclusion they have to read. Show it.
- **Burst-posting the identical file to four surfaces** — all four scored zero on Facebook. Different version per surface, staggered.
- **Silent videos** — Facebook's own dashboard says Reels with audio perform better. Every video now ships with a synthesized light-music bed.
- **Wrong format for the account's classification** — our Facebook profile was classified as a story account; explainer reels died there while the same videos were pushed to strangers on Instagram. Surface roles: IG = reach + follows; FB = stories + monetization.

## Files in this repo

- `SKILL.md` — **the AI entry point.** Hand this file to your AI; it contains the full operating procedure, format rules, free vs paid routes and QA gates.
- `AGENTS.md` — pointer file for AI agents (read SKILL.md first).
- `AI_START_HERE.md` — human-readable overview of the same workflow.
- `scripts/render25.py` — overlay engine: config-driven compositor (hook / day-jump curve / loser freeze-or-drain / winner acceleration counters / ending freeze + question) for AI-generated footage.
- `scripts/render16.py` — split-screen comparison engine (free route). `scripts/render17.py` — scene engine (free route). `scripts/render23.py` — warm story engine (free route).
- `scripts/make_bed25.py` — light-music synthesizer: music-box arpeggio + soft pad, pure code, zero copyright risk.
- `assets/` — backend and profile screenshots (the evidence).

## Follow the live operation

All public, all running now — follow along:

- YouTube「OneLine Forward」: https://www.youtube.com/@OneLineForwardStudio
- Instagram: [@artbronai0102](https://www.instagram.com/artbronai0102/)
- Facebook profile (Professional mode)「Ma Pei Wen」: https://www.facebook.com/profile.php?id=61575916052418
- Facebook Page「火柴人劇場」: https://www.facebook.com/profile.php?id=769510329574719
- Facebook Page「Mono Stories」: https://www.facebook.com/profile.php?id=1496718363516277

## Privacy boundary

What is public here is the **method and the results**. Credentials, generation-credit ledgers and the operator's personal information are not in this repo and will not be published.

## License

MIT

---

# 中文說明

## 這是什麼

一個由 AI 實際營運中的火柴人短影音生產線：產圖 → 圖生影片 → 程式疊字 → 多版面發佈 → 每日數據診斷。每天生產 A/B 對照火柴人 Reels（同一個起點、兩種做法、一年後差多少），發佈到 Instagram、Facebook 粉專與 YouTube Shorts，由 AI 負責選題、生成、疊字、發佈與成效診斷，經營者只做方向決策。這不是概念驗證——是正在跑的帳號，數字是真的。

## 怎麼用（超簡單）

1. 下載／clone 整個專案。
2. 把 `SKILL.md` 交給你的 AI（Muse、ChatGPT、Gemini 都可以），跟它說一個題目，例如「做一支早起 vs 賴床一年的」。
3. AI 照格式規則產出可直接發佈的成品，你發佈即可。

**免費 vs 付費，先講清楚：**
- **完全免費（純程式，不用任何生成 AI）**：同框對照、場景片、暖色故事片、疊字、合成音樂——腳本都在 `scripts/`，有 Python + ffmpeg 就能產出可發佈的成品。
- **需要生成點數（畫面更生動）**：關鍵幀 → Flow／Veo 圖生影片（約 20 點／支）→ 程式疊字。點數是選配，不是門檻。

## 格式規則（從爆款對標拆解出來的骨架）

骨架不是自己發明的——拆解 2026 年 10–11 月新創頻道的爆款（MindFrame Animation 上線兩週兩支 2,200 萬觀看、Visual Mindset 最高 1,000 萬）逐幀歸納：

1. **第一幀就是完整賽局**：提問 + 左右兩方標籤 + 計數器歸零，同框出現。
2. **時間非線性跳躍**：第 1 天 → 第 365 天，輸家在第一次跳躍就凍結（停在個位數），贏家加速衝到誇張量級（8 下 vs 12,480 下；$0 vs $36,500）。
3. **中段要有事件**（約 50–70% 處）：不是直線比賽，是有人放棄、有人登頂、罐子滿出來。
4. **結論要用演的，不用寫的**：結尾是事件畫面（登頂插旗、存錢罐溢出、觀眾鼓掌），不是格言字卡。10 支爆款裡 8 支如此。
5. **最後只留一個提問**：「你是哪一派？／WHICH ONE ARE YOU?」——身分提問，不是道德教訓。
6. **15 秒內**、輕音樂墊底（無聲影片會被平台點名成效較差）、**所有文字用程式疊**（影片生成模型產字必亂碼）。

## 生產流程

```
① 對標選題（要有需求證據：大帳號近期爆款／同題多帳號流動／經典概念庫）
② 產一張關鍵幀靜圖（A/B 對照在構圖裡就要一秒看懂）
③ 圖生影片（Google Flow / Veo 3.1 Fast，8 秒，720×1280）——逐幀驗浮水印
④ 程式疊字（鉤子／天數跳躍／雙邊計數／結尾定格＋提問）＋合成輕音樂
⑤ 各版面發不同版本（不連發相同檔案），排程滴出
⑥ 每日診斷：觀看→留存（跳出率／平均觀看）→追蹤→詢問→收入；
   接近零的影片必須給出原因（帳號狀態／首批分發／留存／跨版面對照），不只報數字
```

## 真實成績（2026-11-21～23 實測）

**2026-11-23 更新：** 臉書個人檔案的一支影片，發佈不到一天突破 **82000 觀看**，還在往 100000 爬，留言區兩派觀眾吵成一團。從選題到發佈，用的就是這個 repo 的完整流程。

| 影片 | 觀看 | 備註 |
|---|---|---|
| 拿鐵因子（一杯咖啡偷走 145 萬） | 3,504 | 帳號最高互動率 |
| 同框版 自律 vs 動機 | 3,332 | 平均觀看 9.5s／14s、重播 824 次 |
| 配息為什麼跌 20% 也不賣 | 1,418 | |
| Flow 刀工對決（圖生影片路線） | 1,313 ↑ | 發佈 25 分鐘時只有 26，持續爬升中 |
| Flow 除草對決 | — | 跳出率 13.2%，全帳號最低 |

## 踩過的雷（誠實區）

- **純程式畫的火柴人動畫像投影片**——動作必須由生成模型演，程式只負責文字層。
- **格言字卡收尾沒人看**——結論要演成事件。
- **同一支影片短時間在多個版面連發相同檔案**——臉書四支全 0。已改為各版面不同版本、錯開時間。
- **無聲影片**——臉書後台直接標示「使用音訊的 Reel 成效更佳」；現在每支都墊合成輕音樂（零版權風險）。
- **臉書個人檔案被演算法歸類為故事型帳號**——解說片在 FB 推不動、同支在 IG 被推給陌生人。版面分工：IG 衝量與追蹤，FB 走故事片與盈利。

## 隱私邊界

公開的是**方法與成績**。帳號憑證、生成點數帳本、營運者個人資訊不在此 repo，也不會公開。
