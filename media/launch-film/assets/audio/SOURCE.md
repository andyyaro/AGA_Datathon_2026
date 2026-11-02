# Third-party sounds, pictures and type in the film

These are in the film but not in this repository. The music and sound-effect licences cover using them
inside a film, not handing the files on by themselves, so they are listed here instead. Download each one
again to the path shown to rebuild.

## Music

| Used as | Track | Licence | Put it at |
|---|---|---|---|
| The bed under the whole film, cut on its bar lines by `sound/music.py`: the breakdown under the hook, the groove from the drop on "Audits", the track's own outro under the end card | "Hip Hop 02" by Lily J, Mixkit 738 | [Mixkit Stock Music Free License](https://mixkit.co/license/): free in any project, no credit required, not for use in a music-only track | `sound/track.mp3` |

## Sound effects

All from Mixkit, under the [Mixkit Sound Effects Free License](https://mixkit.co/license/). The names
are the ones `sound/mix.py` uses (`SFX`); each file goes in `sound/sfx-src/` as `mixkit-<id>.mp3`. The
film has 67 effects; `sound/sfx_events.json` lists each one with its time and level.

| Name in `mix.py` | Mixkit id | Times used | What it marks |
|---|---|---|---|
| `tick` | 1120 | 27 | A step or a counter: the three databases, the bar's parts, each tenth of a trillion, the five names, the score passing each ten |
| `key` | 2531 | 17 | Each letter of "material weakness" as it appears in the glossary's search field (single keys cut from a laptop typing take) |
| `pop` | 2357 | 8 | A part arriving: the dot field, the mark, the card flip, a tier change, the counter landing, "1st place", the end card's mark |
| `whoosh_air` | 1492 | 7 | The window and the camera: the settle, the two screen swaps, the three push-ins, the step aside |
| `click_down`, `click_up` | 1113 | 3 each | The pointer's real presses and releases, from the recordings (one mouse click, split in two) |
| `whoosh_wind` | 1465 | 1 | The dots streaming onto the mark |
| `riser` | 2408 | 1 | The swell into the drop |

`mix.py` also names `sweep` (3115), `pop_hard` (3005) and `typing` (2538). The film does not play them,
so they are not needed to rebuild it.

## Voice

Kokoro-82M ([Apache-2.0](https://huggingface.co/hexgrad/Kokoro-82M)), voice af_heart, run locally. The
lines are `narration/lines-tts.json`; the audio is generated, so it is not kept.

## Type

Inter and Inter Display 4.1 (Regular, Medium and SemiBold; Display SemiBold), by the Inter Project Authors, under
the [SIL Open Font License 1.1](https://openfontlicense.org/). `tools/fetch_vendor.sh` puts them in
`assets/fonts/` with their licence and checks each file. The wordmark is Bricolage Grotesque ExtraBold
(SIL OFL 1.1), already turned into outlines in `assets/brand/film/wordmark.svg`, so no font file is needed.

## Pictures

Every screen in the film is the live site, https://gmufiscalpatriots.bytechisel.com/, recorded frame by
frame by `capture/takes.py`: the landing page with the team's Tableau dashboards (Tableau Public embeds),
the glossary and the Audit Health Score simulator. The recordings are not kept here; their pointer paths,
marks and element boxes are, in `assets/rec/*.json`, and `capture/conform.py` turns a new recording into
the clips the composition plays.
