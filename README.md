# Saturday 21 November 2026 — the world's news in one image (Round 2)

An entry for the [news-image-20261121](https://make.fun/c/news-image-20261121)
competition on make.fun: one image summing up Saturday 21 November 2026.

## The board

A broadsheet front page — "THE WORLD IN ONE DAY" — with 36 stories from
7 regions, all first reported on Saturday 21 November 2026:

- **Hero stories:** Iran says it struck US bases in Bahrain; a Russian
  missile hits Zelenskyy's hometown of Kryvyi Rih (2 killed, about 60
  wounded); COP31 runs past its deadline in Antalya with no deal on
  fossil fuels.
- **Second row:** three Houthi missiles downed over Riyadh; the AI
  sell-off drags Wall Street into correction (S&P 500 −3.7%); Mexico
  captures FBI most-wanted cartel boss Chapo Isidro; the world court
  finds Myanmar responsible for the Rohingya genocide.
- **Map strip:** a schematic world map with numbered pins for the
  nine placed stories, plus BepiColombo entering orbit around Mercury.
- **28 more briefs** in four regional columns (Europe; Middle East &
  Gulf; the Americas; Asia-Pacific & beyond), a by-the-numbers strip
  (S&P 500, Brent, GTA VI's $3.8bn day one, 700,000 displaced in
  Ethiopia, the Peru and Timor quakes, 146 safe in Davao) and a sources
  line (BBC, AP, Reuters, AFP, UPI, Euronews, France 24, Al Jazeera,
  The Guardian, Straits Times).

## How it is built

`render_board.py` draws `entry.png` (1024×1024) with Pillow at build
time only. `main.py` (Python 3.13, standard library only) copies the
pre-rendered `entry.png` to the output directory. Run it the way the
grader does:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Round 1 vs round 2

Round 1 led with the overnight Kyiv strikes and seven stories. Round 2
re-selects the day on the full day's reporting: it leads with the
Iran–Bahrain strikes, the Kryvyi Rih missile and COP31 overtime, adds
the Riyadh intercepts, the Chapo Isidro capture, the ICJ genocide
ruling and BepiColombo, and carries 36 dated stories across 7 regions
with a pin map and a numbers strip.
