# Audits Made Simple launch film: storyboard and build

67.4 s, 1920 × 1080, 30 fps. H.264 with AAC at 256 kb/s; measured on the MP4: -16.1 LUFS
integrated, true peak -2.1 dBTP, loudness range 4.2 LU. Every claim in it and its source is in
[FACTS.md](FACTS.md); the full brief, with every time, is [SPEC.md](SPEC.md).

## What is real and what is rebuilt

- **Real:** every screen of the product. Three takes of the live site
  (https://gmufiscalpatriots.bytechisel.com/), recorded frame by frame on a virtual clock at
  1600 × 900 and twice the pixel density, with real pointer moves, clicks and keys. Each take was
  scripted on the narration's word times, so it plays at 1x and none needs a speed label. The capture
  only read and navigated: no form was sent and nobody logged in. The Tableau views were left to
  paint before the clock started.
- **Rebuilt:** the browser window around the recordings (HyperFrames' window stage: settle, screen
  swap, step aside) and the pointer, drawn on its recorded path. The dots, the lockup, the counter,
  the tier bar, the team and the end card are drawn by the composition, with numbers from FACTS.md
  only.
- **Left as recorded:** the site's frosted top bar shows a faint blur of the page under it. The live
  glossary has 54 terms; the copy in this repository's `webapp/` has 52. The film shows the live site
  and says 54.

## The film

| Time (s) | Scene | Narration | What you see |
|---|---|---|---|
| 0–14.8 | Hook | "$8.58 trillion in federal assistance. Where did it go? And what did the audits find? It's all public, but split across three federal databases, in auditors' language." | 858 dots, one per $10 billion, bloom into a field. "$8.58 trillion." / "Where did it go?" / "It's all public." and three rows: USAspending.gov · who got the money, FAC.gov · what audits found, SAM.gov · who is excluded. On the last bar the dots stream onto the mark. |
| 14.8–21.0 | Lockup | "This is Audits Made Simple. Federal spending and audit data, made understandable." | On the music's drop the dots become the mark and the wordmark wipes in beside it; the tagline. |
| 21.0–29.7 | Explore | "Start with the money: interactive Tableau dashboards show where it goes. Ten states received just over half of it." | The window settles on the landing page. "See where the money goes." / "Interactive Tableau dashboards, built by the team." The page scrolls to Funding by State, the pointer rests on "Top 10 States (50.9%)" and the camera pushes in on the ten bars. |
| 29.7–37.1 | Glossary | "Stuck on a term like material weakness? The glossary explains it in plain words." | "Look up the jargon." / "54 terms in plain words, each with why it matters." The pointer clicks the search field and types "material weakness"; two cards are left; the Material Weakness card flips to its definition and why it matters, and the camera pushes in. |
| 37.1–47.0 | Score | "The Audit Health Score turns audit results into one number, from 0 to 100. Red means look closer: a signal, not proof of wrongdoing." | "One number from 0 to 100." / "Green, yellow or red: a screening signal, not proof of wrongdoing." The pointer drags the simulator from 90 (Low, green) to 70 (Medium, yellow), the camera pushes in on the score, then on to 25 (High, red). |
| 47.0–54.4 | Proof | "Joined with spending records, the scores show $1.09 trillion went to recipients in the red." | The window steps aside. "Joined with spending records." hands over to a counter that counts to "$1.09 trillion", "went to 9,976 recipients in the red tier." A bar splits by funding: Green $372.0 billion, Yellow $598.6 billion, Red $1.09 trillion, the red part growing with the counter. A footnote says how the data was joined and that it is a signal, not proof of wrongdoing. |
| 54.4–61.9 | Team | "Five students at George Mason built it, and won first place nationally at the AGA Datathon." | "Fiscal Patriots · George Mason University", the five names with the roles the site's About page gives them, "1st place nationally.", "AGA Datathon 2026 · Washington, D.C." |
| 61.9–67.4 | End card | "Audits Made Simple. Explore it yourself." | The mark draws (the A, then the check), the wordmark beside it, the tagline and the address gmufiscalpatriots.bytechisel.com; it fades. |

## Look

- **Frame grammar** from the Outbreak Detective share film: the real site inside a browser window on
  a bare ground, a small coloured kicker over a bold sentence-case headline and one grey sub-line at
  the top left, a dot story for the hook, the lockup on the drop and an end card of mark, line and
  address. From the EV-SIENT film: a push-in on the element the voice names (at most 1.35x), a
  counter that counts, and the window stepping aside for a short note.
- **Tokens** from the HIG Native design system: a #F2F2F7 ground, white surfaces, hairline
  separators, capsule pills, the window at radius 16 with no shadow. The tiers are the system green,
  yellow and red, and each is always shown with a word as well as its colour.
- **Brand:** this repository's own (`docs/assets/brand/`). Blue #1F3FE0 is the film's one accent
  (kickers, the dots, the pointer's press ring); navy #10183A is the headline ink; coral #FF5A3C is the
  check in the mark only, so it never stands for the red tier; the cream #FFF3C9 never fills a frame.
- **Type:** Inter Display SemiBold for headlines and the counter, Inter for everything else, the
  address pill included. No monospace and no em dashes on screen.

## Sound

- **Voice:** Kokoro-82M, voice af_heart, 13 lines, every chosen take matching the script word for
  word. All lines are at speed 1.0 except the twelfth, at 1.06, because Whisper heard "won" in the
  1.0 take as "one". `narration/lines-tts.json` spells the figures, "Audits Made Simple" and "A.G.A."
  as they are said.
- **Music:** "Hip Hop 02" by Lily J (Mixkit 738), relaxed R&B at 97 BPM, a bar every 2.474 s, cut on
  its bar lines by `sound/music.py` with 12 ms crossfades that keep its four-bar chord cycle:

  | Film (s) | Track (s) | What plays |
  |---|---|---|
  | 0–14.845 | 84.17–99.01 | The breakdown (keys and a soft bass, no drums) under the hook, starting on the second chord so its last bar leads into the drop |
  | 14.845–61.856 | 0.04–47.05 | The groove from the track's first bar: its first kick lands on "Audits" in "This is Audits Made Simple" |
  | 61.856–67.4 | 106.43 to the end | The track's own outro under the end card, faded over the last 2.5 s |

- **Effects:** 67 soft Mixkit sounds: a pop for a part arriving, a tick for a step or a counter, an
  air whoosh for the window and the camera, a wind whoosh for the dots' stream and a riser into the
  drop. The pointer's real presses and releases get a mouse click, and the 17 letters of "material
  weakness" get single keys, each on the frame where it happens. The list is in
  [assets/audio/SOURCE.md](assets/audio/SOURCE.md); the measured times and levels are in
  `sound/sfx_events.json`.
- **Levels:** speech -15.6 LUFS; the music 9 dB under it, ducked 4.5 dB more while she speaks; each
  effect 3 to 5 dB over the music and at least 3.6 dB under the voice. Master -16.0 LUFS, true peak
  -2.0 dBTP, with the limiter at four times the sample rate; the MP4 measures -16.1 LUFS and -2.1 dBTP.

## Build

Get the inputs first: `tools/fetch_vendor.sh` for GSAP and the fonts, then the music and effects
listed in [assets/audio/SOURCE.md](assets/audio/SOURCE.md). The Python steps need numpy, soundfile,
librosa and mlx-whisper (`<voice-venv>`), or Playwright 1.64 with Chromium and numpy
(`<playwright-venv>`), and ffmpeg. The recordings are not kept, so a rebuild records the live site
again; it was recorded on 2026-11-01, and the site may have changed since.

```sh
tools/fetch_vendor.sh
# Voice each line of narration/lines-tts.json with Kokoro-82M (af_heart) at speeds 1.0 and 1.06,
# as narration/takes/<id>.<k>.wav
<voice-venv>/bin/python narration/pick.py takes                  # best take per line, words.json
<voice-venv>/bin/python -I sound/music.py                         # assets/audio/music.wav, sound/grid.json
<voice-venv>/bin/python -I sound/mix.py                           # mix.wav, assets/vo.js, assets/timing.js, sfx_events.json
<playwright-venv>/bin/python -I capture/takes.py all              # assets/rec/<take>.mp4 and .json, from the live site
<playwright-venv>/bin/python -I capture/conform.py                # assets/shots/<shot>.mp4, assets/edit.js and .json
python3 -I build.py                                               # scene and take windows into index.html
npx --yes hyperframes@0.8.173 lint && npx --yes hyperframes@0.8.173 check
npx --yes hyperframes@0.8.173 render -o renders/raw.mp4 --fps 30
ffmpeg -y -i renders/raw.mp4 -i assets/audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k \
  -shortest -movflags +faststart renders/audits-made-simple-v1.mp4
python3 -I narration/vtt.py                                       # renders/audits-made-simple-v1.en.vtt
```

The ffmpeg step puts the exact mix back on the picture, because the renderer's own audio comes out
quieter. The scenes find their cue words in `window.VO`, so a re-voiced line re-times the picture,
and the effects follow the same word times and the recorded pointer paths.

## The README preview

`docs/assets/readme/audits-made-simple-in-action.webp` is 29.8–45.8 s of the film: the glossary
search, the card flip and the Audit Health Score dragged from green to red, at 1200 px and 15 fps,
1.6 MB. The film is light and flat, so quality 90 shows no blocking even in the push-ins.

```sh
mkdir -p preview
ffmpeg -ss 29.8 -t 16 -i renders/audits-made-simple-v1.mp4 \
  -vf "fps=15,scale=1200:676:flags=lanczos" preview/f%03d.png
img2webp -loop 0 -lossy -q 90 -m 6 -d 67 preview/f*.png \
  -o ../../docs/assets/readme/audits-made-simple-in-action.webp
```
