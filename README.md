[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/hrd04-ai/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/hrd04-ai/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World in One Day — 20 November 2026

One image that tells Friday 20 November 2026 at a glance. A newspaper
front page: masthead with the date, six illustrated stories, and a strip
of three more briefs at the foot.

## The six stories

- **Iran call delayed** — Trump pushes the Iran war decision to 2027:
  "no rush", he'll "see what happens" after Jan 1 (Reuters).
- **Genocide ruling** — the ICJ rules Myanmar committed genocide
  against the Rohingya, 9–6, the first time the UN's highest court
  has held a state liable for genocide (The Hague).
- **Cyclone Akvan** — 300,000 evacuated as the severe cyclone makes
  landfall on India's Odisha coast; 423 rescue teams deployed.
- **GTA VI beats Hollywood** — $1.84bn on day one tops The Odyssey's
  $1.805bn lifetime box office; 19.1m copies (Sensor Tower).
- **COP31 backlash** — the revised climate draft in Antalya strips out
  all fossil-fuel phase-out language, ahead of the final plenary.
- **Hayabusa2 grounded** — engine trouble forces Japan's probe to
  scrap its asteroid landing plan and change course.

Every panel carries a hand-drawn pictogram, a headline and one factual
sublabel, so a reader who missed the day can follow it from the picture
alone. The briefs strip adds Europe's readiness to talk with Russia
about ending the Ukraine war, Anthropic's reported $1.5 trillion
valuation, and the US–Venezuela deal to restore military cooperation.

## How it was made

`make_image.py` draws the page with Pillow and saves `entry.png`
(1024×1024, under 1 MiB). `main.py` only copies that finished image to
the output path — standard library only, no network, no randomness — so
repeated runs produce byte-identical output.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
