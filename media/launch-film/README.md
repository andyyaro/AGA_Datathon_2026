# Audits Made Simple launch film

The 67-second film at the top of the [repository README](../../README.md), published at
https://andyyaro.github.io/AGA_Datathon_2026/film.html. It starts with $8.58 trillion of federal
assistance as 858 dots, then shows the live site at work: the team's Tableau dashboards, the glossary
explaining "material weakness" and the Audit Health Score simulator dragged from green to red. It ends
on one number the scores surfaced ($1.09 trillion to 9,976 recipients in the red tier) and the five
students at George Mason who built it and took 1st place nationally at the AGA Datathon 2026.

Every screen in it is the live site (https://gmufiscalpatriots.bytechisel.com/), recorded frame by
frame and played at its real speed; the capture only read and navigated, with no form sent and no
log-in. The dots, the counter, the tier bar and the team's names are drawn by the composition,
with every number taken from [FACTS.md](FACTS.md).

[STORYBOARD.md](STORYBOARD.md) has the scenes, the look, the sound and every build step.
[FACTS.md](FACTS.md) has every claim in the film and where it comes from. [SPEC.md](SPEC.md) is the
full brief the film was built to: the music cut, every shot and every time.

## What is here

| Path | What it is |
|---|---|
| `index.html`, `compositions/` | The composition (HyperFrames 0.8.173, GSAP): the browser-window stage that plays the three recordings, and one file per scene |
| `build.py` | Writes the scene windows and the recordings' windows into `index.html` |
| `assets/film.js` | The 858 dots: the field they bloom into and each dot's place on the mark's two strokes |
| `assets/vo.js`, `assets/timing.js` | Each narration line's start and word times, and the scene windows (written by `sound/mix.py`) |
| `assets/edit.js`, `assets/edit.json`, `assets/rec/*.json` | The edit: each recording's window in the film, its marks, the push-in boxes, and the pointer's path frame by frame |
| `capture/` | The recorder: a virtual clock for the page (`vclock.js`), the frame-by-frame recorder (`rec.py`), the three takes scripted on the word times (`takes.py`), the trim to the film (`conform.py`) and contact sheets (`sheet.py`) |
| `narration/` | The script (`lines.json`), the script as voiced (`lines-tts.json`), `pick.py`, which chooses the best take of each line and times its words (`words.json`), and `vtt.py`, which writes the captions |
| `sound/` | The music edit (`music.py`, `grid.json`), the mix (`mix.py`, `timing.json`) and the measured list of the 67 effects (`sfx_events.json`) |
| `SPEC.md`, `FACTS.md` | The brief, and every claim with its source |
| `tools/fetch_vendor.sh` | Fetches GSAP and the Inter fonts at the pinned versions and checks each file's SHA-256 |
| `deploy/film.html`, `deploy/index.html` | The watch page, and a redirect to it from the site's root |
| `assets/brand/film/` | The wordmark cut from the logo for the film; the rest of the brand is in [`docs/assets/brand/`](../../docs/assets/brand/) |
| `assets/audio/SOURCE.md` | Every third-party sound and font in the film, with its licence and where it goes |

## What is not here, and why

The working folder for the film is about 130 MB. This folder keeps the source and leaves out
everything that is generated or that its licence does not let us hand on by itself:

- **Generated:** the narration takes and chosen lines, the music edit, the mix, the clips trimmed to
  the film (`assets/shots/`), the contact sheets and the renders. The build steps make them again.
- **The screen recordings** of the live site (`assets/rec/*.mp4`, three takes at 3200 × 1800). Their
  pointer paths, marks and element boxes are kept in `assets/rec/*.json`; `capture/takes.py` records
  them again from the live site.
- **Third-party media:** the music ("Hip Hop 02" by Lily J, Mixkit) and seven Mixkit sound effects.
  [assets/audio/SOURCE.md](assets/audio/SOURCE.md) lists each one with its licence and the path it
  goes to.
- **Libraries and fonts:** GSAP 3.14.2 and Inter 4.1 (SIL OFL 1.1) are fetched by
  `tools/fetch_vendor.sh`.
- **Working notes:** the progress log and the review notes made while building the film.

## Publishing

The MP4, its captions and its poster are assets of the
[`film-v1` release](https://github.com/andyyaro/AGA_Datathon_2026/releases/tag/film-v1), so the
15.0 MB film is not in the repository's history. The
[film page workflow](../../.github/workflows/film.yml) puts them on GitHub Pages with
`deploy/film.html`, `deploy/index.html` and the logo. It runs when anything in `deploy/` changes
on `main`. After replacing a release asset, run it by hand:

```sh
gh release upload film-v1 audits-made-simple-launch.mp4 --clobber
gh workflow run film.yml
```

## Credits

Audits Made Simple is the work of the Fiscal Patriots, five students at George Mason University:
Khaled Alkurd (team lead), Pranavi Doodala (project manager), Mariam Debas (visualization lead), Nikita
Chandrasing (product manager) and Andy Yaro (product developer). The Tableau dashboards on screen are
the team's.

Narration: Kokoro-82M (Apache-2.0), voice af_heart. Music: "Hip Hop 02" by Lily J (Mixkit). Sound
effects: Mixkit. Type: Inter and Inter Display (SIL OFL 1.1); the wordmark is Bricolage Grotesque
ExtraBold (SIL OFL 1.1).
