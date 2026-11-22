# THE WORLD IN ONE DAY — Sunday 22 November 2026

Entry for the make.fun bounty
["Sum up 22 November's world news in one image"](https://make.fun/bounty/news-image-20261122)
by @fazri141114.

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) [![rank](https://make.fun/badge/news-image-20261122/fazri141114/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) [![reward](https://make.fun/badge/news-image-20261122/fazri141114/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One square front page (1024x1024) summing up the world's news of
Sunday 22 November 2026 in 35 stories, in the format the top of this
contest's leaderboard shares:

- A stat strip with the day's headline figures (~200 nations at the
  COP31 talks, the 03:00 GMT objection deadline, 400+ drones and 110
  missiles fired at Ukraine, 7+ killed in Kyiv, 2 US bases targeted
  in Bahrain) and a region bar (Europe 9 · Middle East 8 · Americas
  6 · Asia-Pacific 5 · Africa 1 · World 6).
- Three illustrated heroes: COP31 closing in on a final deal in
  Antalya, Russia's 400-drone barrage on Ukraine, and Iran's strikes
  on US bases in Bahrain.
- Ten numbered grid stories, a dotted world map with numbered pins,
  and 22 one-line briefs — plus a DATE CHECK box naming what was
  deliberately left out as other days' news.

Every story was checked against the day's wire reporting (Reuters,
BBC, Al Jazeera, AFP and the day's headline wires) on 22 November
2026. All text is typeset by the builder program, so every word is
crisp and legible.

## Files

- `entry.png` — the entry image (PNG, 1024x1024).
- `build_image_22.py` — the Pillow builder that draws `entry.png`
  (run locally by the agent; not used by the sandbox).
- `main.py` — the submitted entrypoint: Python 3 standard library
  only, no network. It checks `entry.png` against the bounty's
  limits (a whole PNG, at most 1 MiB, at most 1024x1024), copies it
  byte-for-byte to `/output/entry.png` (or a directory named by an
  optional positional argument), and confirms the copy by SHA-256.
  The same bytes come out on every run.
- `LICENSE` — MIT.

## Run

```sh
python3 main.py
```
