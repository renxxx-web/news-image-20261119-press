# Research — news-image-20261119 (Thursday 19 November 2026)

Method (Bos's standing rule): pull the actual top-3 entries of the two previous
editions, extract each one's strengths per aspect, combine them, then improve
on the combination. Images were fetched from the make.fun API
(`GET /api/submissions/<id>` → `judge.artifact.url`) and read visually.
Copies live in `research/` (never committed to the entry repo).

## Competition facts (news-image-20261119, from the kit + requirements API)

- Open now; **entries close 2026-11-21T00:00:00Z**; prize $250 over the 50 best
  win rates ($50 / $30 / $15 / $5×7 / $3×40).
- Image: whole PNG or JPEG, **≤ 1 MiB, ≤ 1024×1024**, written by the program to
  `/output/entry.png`; no network; two runs must write identical bytes.
- Flow: **bundle** (repo_url + commit_sha + transcript bundle), program/v1.
- Judge (AI vision, pairwise, criteria in order): (1) names the day + specific
  recognisable events of that day; (2) selection & breadth across regions and
  fields; (3) reads clearly from the image alone, nothing false or
  self-contradictory; (4) faithful, claims attributed, no hype; (5) craft —
  one clear composition, legible at ~300 px, no garbled text.

## Top 3 — news-image-20261118 (13,375 entries, dev-heat rates)

### #1 warungbiru — "woodcut block" (rate .992, 967 KB)
- Masthead: giant red date block "18 NOV WED 2026", huge serif
  "Wednesday 18 November 2026", strap "Everything on this page happened, or
  was first reported, on…", top-right tally box "40 STORIES · 7 REGIONS · ONE PAGE".
- Coloured region tally bar (Europe 8, Americas 9, Asia 6, Africa 6, ME 4,
  Oceania 3, World 4).
- "THE DAY IN NUMBERS": six big figures with one-line captions (141 / 126 /
  25.9bn km / 55 / 251–11 / 11,300+).
- 13 large story cards, each with a rich woodcut-style illustration, number,
  region·beat tag, status tag (CONFIRMED / CLAIM) + wire credit, bold serif
  headline, 2–3 line factual summary.
- "ALSO ON WEDNESDAY — 27 MORE STORIES": numbered one-liners 14–40, bold
  datelines, flanking a dotted world map ("WHERE IT HAPPENED") whose numbered
  pins match the card numbers; an off-map arrow "3 · TO VOYAGER".
- DATE CHECK box: stories deliberately excluded as other days' news — a
  visible faithfulness device. Footer: source list + "all 40 stories happened,
  or were first reported, on…".

### #2 eager-badger-82 — flat-design twin of #1 (rate .992, 351 KB)
- Same skeleton and same 40 stories; flat vector icons instead of woodcut art,
  navy masthead, airier spacing. Proves the *structure and coverage* carry the
  score; art style is secondary. Cheaper file (351 KB vs 967 KB).

### #3 alim3596 — "Deft Gauge" (rate .991, 224 KB)
- Same lineage again: single-line numbers strip, 13 cards with small flat art,
  map bottom-left, briefs 14–40 in three columns, DATE CHECK box, sources
  footer. Slightly denser/smaller type — still podium.

**Takeaway: the entire 20261118 podium is one design family.** Structure,
breadth (40 stories / 7 regions), attribution tags and the date-check device
are what the judge rewards.

## Top 3 — news-image-01 (Friday 13 November 2026, 4,148 entries)

### #1 gentle-meteor-30 (rate .859, 335 KB)
- Navy masthead, huge serif date, "35 STORIES · 6 CONTINENTS · ONE DAY".
- 11 big illustrated cards (bolder art, larger headlines than 20261118's),
  dotted map bottom-left with numbered pins + region-colour legend,
  "ALSO ON FRIDAY 13 NOVEMBER" briefs 12–35 in two columns, footer:
  "Every story was reported on Friday 13 November 2026; disputed claims are
  attributed."

### #2 aksara-lintas — "blue edition" (rate .857, 593 KB)
- Cream paper, black display serif, red kicker. 15 medium cards with
  left-rail thumbnails (denser card grid), map with "numbers = stories 1–15,
  dots = briefs" legend, briefs 16–34. Shows a thumbnail-rail card variant
  also podiums.

### #3 superskie (rate .855, 431 KB)
- Near-twin of #2 (same stories/layout, flatter art, 33 stories). Confirms
  the family resemblance across the whole podium.

## Combined strengths (what we take)

1. Masthead that *names the day* three ways: giant date, weekday + full date
   in display serif, and the "everything on this page happened on…" strap.
2. A story/region tally the judge can count (40 stories · 7 regions).
3. A "Day in Numbers" strip of ~6 attributed figures.
4. 11–13 illustrated story cards: number, region·beat tag, CONFIRMED/CLAIM
   status + wire credit, serif headline, 2–3 line summary.
5. Dotted world map with pins numbered to match the cards.
6. Numbered one-line briefs bringing the total to 33–40 stories across
   ≥6 regions / ≥5 continents, each with a bold dateline.
7. Faithfulness devices: attribution inside summaries ("X says"), a
   DATE CHECK box excluding other days' stories, a sources footer.

## Where the winners are weak — our improvements

- **(a) Numbers are text-only.** No winner draws a single chart. → Our
  "Day in Numbers" panel adds three *drawn* mini-charts beside the figures:
  Wall Street's day as bars (Dow −0.97%, S&P −0.41%, Nasdaq +0.01%, Reuters),
  biggest-IPOs-ever bars (Anthropic $81.3bn vs SpaceX $75bn), and oil bars
  (Brent $92.54 +0.6%, WTI $84.30 +1.3%).
- **(b) Maps carry pins only.** → Our map adds the day's defining geometry:
  dashed **summit arcs from Washington and Moscow converging on a starred
  Shenzhen**, captioned as the route of the day's biggest story, on top of
  the numbered pins.
- **(c) Breadth matched and organised:** 40 stories, 7 regions (Europe 10,
  Asia 7, Africa 7, Americas 5, Middle East 4, Oceania 4, World 3), fields
  spanning diplomacy, war, courts, climate, markets, tech, culture, sport,
  weather and health.
- **(d) Date discipline kept:** DATE CHECK box lists real 18-November stories
  we deliberately leave out (Alcaraz–Medvedev, the Kemerovo An-12 crash,
  Ebola doubling, UK inflation 3.6%, Voyager 1's light-day) and what has not
  happened yet (COP31's closing text, Anthropic's first close).

## The day itself (19 Nov 2026) — lead stories used

- **Shenzhen:** Trump, Xi and Putin hold the first-ever US–China–Russia
  trilateral on the APEC sidelines (~90 min); four-point "Peace Declaration"
  (UN reform, nuclear-risk dialogue, more refined-oil supply, ICC condemned);
  no breakthrough on Ukraine/Iran; Trump calls Putin "my friend". (AP/Reuters)
- **Anthropic IPO:** priced $83, ~$81.3bn raised, ~$1.5tn value — largest IPO
  on record; Nasdaq debut as ANT; Dow −0.97% to 49,710, Brent $92.54. (Reuters)
- **Iran war:** Iran fires on Kuwait after the US self-defence strike on
  Qeshm; Trump "dirty bomb" warning, Iran denies; Hormuz shipping hit. (Reuters)
- **Ukraine:** Crimean Bridge struck for the third time in a week; Zelensky's
  "unprecedented seven-stage strike". (Reuters)
- **Gaza:** Israeli tanks into central Gaza (Nuseirat); Nasser Hospital strike
  kills six incl. a surgeon; aid groups score the truce plan 4/26. (Reuters)
- **COP31 Antalya:** final-stage deadlock on fossil-fuel language; draft drops
  the $120bn adaptation target. (Reuters/PANA/TheCable)
- **The Hague:** ICJ rules Myanmar committed genocide (Rohingya case). (PANA)
- **Washington:** emergency Supreme Court filing over Venezuelan TPS. (AP)
- **GTA VI:** midnight global rollout from New Zealand; Metacritic 99;
  ~17m copies / $1.65bn pre-sales (Sensor Tower); Take-Two +6%. (Reuters)
- **Yongbyon:** IAEA says North Korea is expanding uranium enrichment.
- **Copenhagen:** parliament votes 109–0 for the Greenland security pact.
- **Khartoum:** Sudan court gives RSF leader Hemedti a second death sentence.
- **Suva:** Fiji declares a national disaster over El Niño drought.
- Plus 27 briefs: Manila $2bn+ US loan package, Takaichi–Putin talks,
  Indonesia's asset-forfeiture law, Yunus home torched in Dhaka, UNHCR
  Malaysia halt, Houthi hit on Riyadh's PIF Tower, Gas Husky sinking,
  Pavlohrad child death, Rome cancer-care verdict, BAE job cuts, gold's
  14-month low, IEA datacentre emissions, Kirkuk–Ceyhan restart, Gambia mpox,
  DR Congo Ebola aid plea, Afreximbank $30m, South Sudan protection plea,
  Burkina Faso exile critics, CAR mission chief, Cyclone Xavier alerts,
  Rio Tinto's $250m Bougainville fund, and sport: Shelton–Jodar (Turin),
  Chelsea–PSG, England's ODI series win (Hobart), Wales stun the All Blacks,
  Hamilton–Ferrari (Las Vegas), Walmart's outlook.
