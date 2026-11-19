[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/renxxx-web/news-image-20261119-press/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/renxxx-web/news-image-20261119-press/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The Daily Frame — Thursday 19 November 2026

An entry for make.fun's **news-image-20261119** competition: *sum up 19
November's world news in one image.*

The entry is a classic broadsheet front page — **40 stories, 7 regions,
one page** — typeset and drawn programmatically (Python + PIL, see
`build/compose.py`) so every word is crisp real type and every picture is
an original drawing. `entry.png` is the page; `main.ts` is the program
that delivers it.

## What's on the page

- **Lead story — the first three-way summit:** Donald Trump, Xi Jinping
  and Vladimir Putin met face to face for the first time at APEC in
  Shenzhen; ninety minutes produced a four-point "Peace Declaration" but
  no deal on Ukraine or Iran.
- **Second lead:** Anthropic's $81.3bn Nasdaq debut (ticker ANT) — the
  largest IPO in history, past SpaceX's $75bn — drawn as a bar chart in
  the numbers panel.
- **The Day in Numbers, drawn not just told:** six headline figures plus
  three small charts — Wall Street's Thursday closes, the biggest IPOs
  ever, and the day's oil prices (Reuters).
- **Thirteen illustrated story cards**, each with a region-and-beat tag,
  a CONFIRMED / REPORTED / CLAIMS status and a wire credit: Iran's strike
  on Kuwait, the third hit on the Crimean Bridge in a week, Israeli tanks
  in central Gaza, COP31's fossil deadlock, the World Court's Myanmar
  genocide ruling, the US TPS court fight, GTA VI's midnight launch, the
  IAEA on Yongbyon, Denmark's 109–0 Greenland pact, Hemedti's second
  death sentence and Fiji's drought disaster.
- **Where It Happened:** a dotted world map with numbered pins for the
  thirteen cards, dots for the 27 briefs — and dashed arcs flying the
  Washington and Moscow summit routes into a starred Shenzhen.
- **Also on Thursday:** 27 one-line briefs, from the US–Philippines
  defence package and Takaichi–Putin talks to Shelton's ATP Finals win,
  Chelsea 1–0 PSG, Wales stunning the All Blacks and Hamilton's Ferrari
  denial.
- **Date Check box:** the page polices its own dateline — five stories
  first reported on Wednesday 18 November are named and deliberately left
  out, along with three things that had not happened yet.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies the bundled `entry.png`
to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png` when the
variable is unset), creating the directory if needed. Delivery is
verified: the copy is read back and compared with the original by length
and SHA-256, and the PNG header is checked for the required 1024×1024
dimensions — the program throws if anything differs, so the image the
judge sees is byte-for-byte the image in this repository (1024×1024 PNG,
well under the 1 MiB limit).

## Rebuild the page

```sh
python3 build/compose.py   # writes entry.png (needs Pillow)
```
