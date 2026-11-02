# AuditsMadeSimple launch film: SPEC

```text
GOAL:    someone with no accounting background understands, in one minute, what AuditsMadeSimple is and sees it
         work: the team's Tableau dashboards, the glossary, the Audit Health Score; then one real number it surfaced
         ($1.09 trillion to red-tier recipients) and who built it (the Fiscal Patriots, five students at George
         Mason, 1st place nationally at the AGA Datathon 2026).
OUTPUT:  HyperFrames 0.8.173, 1920 x 1080, 30 fps, 67.4 s (set by the sound stage; hard ceiling 70 s).
         renders/audits-made-simple-v1.mp4
SOUND:   (sound stage, 2026-11-01: sound/music.py, sound/mix.py, sound/grid.json, sound/timing.json)
         "Hip Hop 02" (Lily J, Mixkit 738, Mixkit Stock Music Free License), relaxed R&B at 97.0 BPM, 4/4, kick on 1,
         snare on 2 and 4. Measured with librosa: the beat tracker says 97.5, but a fine scan over the kick onsets
         fits 97.00 exactly (97.5 drifts off within a minute). A bar is 2.4742 s. The downbeat kicks start at 0.045 s
         in the decoded file (within +-10 ms on every bar checked; the research stage's 0.075 would clip the drop's
         kick), so a track bar line is 0.040 + 2.4742 n s (5 ms before the kick). The chords run in a 4-bar cycle
         (chroma, bar vs bar+4 similarity 0.98). Track map (per-bar band levels): bars 0-31 (0.04-79.2) the full
         groove from the first sample, NO quiet intro (bars 16-17 vary the kick); bars 32-41 (79.2-104.0) a
         breakdown, hats about 20 dB down, kick gone, keys and a soft bass on 1 and 3; bars 42-45 (104.0-113.9) the
         track's own outro (bar 42 the last bass, 43 keys alone, 44 the final chord, 45 its ring-out). The drop is
         made by the edit (joins on bar lines, 12 ms crossfades, each join keeps the chord cycle):
           film  0.000-14.845  track  84.17-99.01  (bars 34-39) breakdown under the hook: keys, soft bass, no drums;
                                                   it starts on chord II so its last bar leads into chord I on the drop
           film 14.845-61.856  track   0.04-47.05  (bars 0-18)  THE DROP: the groove's first kick lands at 14.855,
                                                   with the vowel of "Audits" in "This is AuditsMadeSimple" (14.845)
           film 61.856-67.400  track 106.43-...    (bars 43-45) the drums fall away under the end card: the track's own
                                                   outro, faded over the last 2.5 s (64.9-67.4)
         Film bar k starts at 2.4742 k (0, 2.474, 4.948, 7.423, 9.897, 12.371, 14.845, 17.320, 19.794, 22.268,
         24.742, 27.217, 29.691, 32.165, 34.639, 37.113, 39.588, 42.062, 44.536, 47.010, 49.485, 51.959, 54.433,
         56.907, 59.381, 61.856, 64.330, 66.804); the drop is film bar 6, the end card film bar 25.
         Voice Kokoro af_heart at speed 1.0 for every line except v12 (the 1.06 take: Whisper heard the 1.0 take's
         "won" as "one", a homophone, so the take with a clean transcript was kept). Every chosen line's transcript
         matches the script word for word (narration/words.json). Lines in film seconds (sound/mix.py SLOTS):
           v01 1.18-4.39   v02 4.95-7.23   v03 7.75-12.49   v04 14.415-15.85   v05 16.55-19.55   v06 21.55-25.48
           v07 26.05-28.22 v08 30.45-35.14 v09 37.60-42.34  v10 43.05-46.48    v11 47.35-53.59   v12 54.95-60.40
           v13 62.75-64.97
         Breaths inside a scene 0.5-0.7 s; 1-2.5 s across scene changes so each beat's picture lands first; the last
         bar before the drop (12.49-14.42) is left to the riser. Cue words (film s, from assets/vo.js; W() finds them):
           "trillion" 2.10, "audits" 6.35, "three" 9.55, "databases" 10.23, "Audits" 14.78 (vowel 14.845),
           "understandable" 18.69, "money" 22.09, "Tableau" 23.39, "Ten" 26.05, "half" 27.71, "material" 31.45,
           "weakness" 31.81, "glossary" 32.99, "plain" 34.31, "score" 38.24, "one" 40.06, "number" 40.32,
           "0" 41.10, "100" 41.72, "Red" 43.05, "signal" 44.77, "trillion" (v11) 51.11, "red" (v11) 53.23,
           "first" 57.57, "nationally" 58.23, "AGA" 59.25, "Audits" (v13) 62.75, "Explore" 63.91.
         W() gotchas: Whisper writes the figures as "$8" + ".58" and "$1" + ".09", and folds "dollars" into them, so
         the next word ("in" in v01, "went" in v11) starts early by the length of "dollars"; "0" and "100" are digits;
         "auditor's" keeps its apostrophe; "AGA" is one token.
         Levels (measured on the outputs): speech -15.6 LUFS (gated, the voice alone as it sits in the mix), the bed
         -24.6 LUFS = 9.0 dB under the voice and ducked 4.5 dB more while she speaks (40 ms attack, 450 ms release),
         so 13.5 dB under the speech; the voice's plosive peaks are caught on the voice alone (-3 dBFS ceiling) so the
         master limiter never squashes a word. Master -16.0 LUFS integrated, true peak -2.0 dBTP, LRA 4.2 LU (finish
         stage: the master limiter now runs at 192 kHz, because a mouse click's transient overshot the sample-peak
         ceiling by 0.6 dB between samples; the mp4 measures -16.1 LUFS, -2.1 dBTP).
         Effects (finish stage, 2026-11-02: sound/mix.py sfx_events, measured list sound/sfx_events.json): 67 soft
         Mixkit effects in secure-data-hub's vocabulary. Soft pop (2357) = a part arriving: the dot field on "$8.58",
         the mark on the drop, the card flip (back face in at 34.20), the yellow and red tiers (39.30, 43.20; red a touch
         lower, pitch 0.94), the counter landing (51.01), "1st place nationally." (57.53), the end card's check (62.81).
         Tick (1120) = a step or a counter: the legend, the three databases (9.51 + 0.3 k, climbing), the tagline, the
         bar's green and yellow parts, every tenth of a trillion as the counter counts (10 ticks, 49.88-50.51, slowing
         with its cubic ease), the score passing each ten while dragged (39.73, 43.50, 43.67; the ticks at 80 and 60 give
         way to the tier pops 0.07 and 0.03 s later), the five names (55.23 + 0.14 k), the event line, the address pill.
         Air whoosh (1492) = the window and the camera: settle 21.031, swaps 29.691 and 37.113, push-ins at their
         fastest (middle: 26.48, 34.32, 40.36), step aside at 47.49 (ease-in, fastest near its end). Wind whoosh (1465)
         = the dots' stream onto the mark (fastest about 13.7). Riser (2408) peaking on the drop. The pointer, as in
         EV-SIENT's sound/design.py: a real mouse click (Mixkit 1113, split into its press and its release) on each
         recorded press and release (30.70/30.80, 38.567/39.933, 42.733/44.033) and 17 single keys cut from a laptop
         take (Mixkit 2531) on the frames where each letter of "material weakness" first shows (31.00-32.30, from
         capture/rec.py's type_text schedule mapped through the conform). No low pops (nothing here is a denial).
         Placement: each effect's moment (a transient's onset for clicks and keys, the loudest 5 ms otherwise) lands one
         frame after its picture; its loudest 50 ms sits 3-5 dB over the bed's RMS in the second around it, and every
         effect is 3.6 dB or more under the voice's median speech level (same 50 ms measure).
LOOK:    One light look, Apple-clean, in three layers:
         1. FRAME GRAMMAR from the Outbreak Detective share film (outbreak-detective-share-v7):
            the real site recorded on a deterministic virtual clock (capture/vclock.js + rec.py) inside HyperFrames'
            browser-device-stage window rebuilt around media clips (settle 0.9 s: opacity over the first 66%, rise
            4.5% of frame height, scale 0.965 -> 1; screen swap 0.55 s through the bare stage, B rises 1.6%; "up"
            exit 0.5 s power2.in); the cursor drawn by the composition on the recorded mouse path; a small coloured
            kicker over a bold sentence-case headline and one grey sub-line at the top left, aligned to the window's
            left edge; a dot story for the hook; the lockup on the drop; an end card of mark, line and address. A take
            played faster than recorded says so in its corner ("1.5x speed" written with the real times sign).
            From the EV-SIENT film: a push-in on the element the voice names (scale <= 1.35, 1.1 s power2.inOut), a
            counter that counts, and the window stepping aside for a short note.
         2. TOKENS from HIG Native (the design system Andy says the
            CERFODES architecture film also used): ground grouped-background-primary #F2F2F7; surfaces
            grouped-background-secondary #FFFFFF; text label-primary #000000, label-secondary rgba(60,60,67,0.6),
            label-tertiary rgba(60,60,67,0.3) (decorative only); hairlines separator rgba(0,0,0,0.12); the window
            radius 16 (radius-mac-window), chips and pills capsules, concentric radii; status = dot + word, never
            colour alone; tiers in system colours: green #34C759, yellow #FFCC00 (dot only, never as text), red
            #FF383C. HIG's own --font-mono and its shadows are NOT used.
         3. BRAND from andyyaro/AGA_Datathon_2026 docs/assets/brand (@56f4133), copied to assets/brand/: the mark
            (a blue A, stroke 18, with a coral check, stroke 12, in a 120 viewBox: two stroked paths, so it can be
            drawn), the wordmark (Bricolage Grotesque ExtraBold, already outlined in the lockup SVGs: "Audits" navy,
            "Made" blue, "Simple" navy). Colours: blue #1F3FE0 = the film's one accent (kickers, the active chip
            ring, the dots, the cursor's halo); navy #10183A = headline ink; coral #FF5A3C = the check in the mark
            ONLY (it never means "red tier": that is HIG system red, so no colour means two things); cream #FFF3C9
            = only inside the rounded app-icon tile (icons/icon-rounded.svg), never a frame ground (cream editorial
            = the banned Huly look).
         Type: Inter Display SemiBold for headlines (72-88 px, -0.025em, navy) and the big counter; Inter Regular /
         Medium for sub-lines, labels, the address pill and every name or number (Inter = the OFL stand-in for SF
         Pro, the system face HIG Native names and the live site itself renders in; the Outbreak films use it too:
         copy Inter*.woff2 + OFL-Inter.txt from the Outbreak Detective share film's assets/fonts). Kickers are sentence case in
         Inter SemiBold blue; if a caps label is ever needed it is Montserrat SemiBold caps +0.13em. NO MONOSPACE
         anywhere, including the address pill.
MOTION:  calm: headlines rise 22 px with blur 5 -> 0 on their word times (window.VO via W()); dots and parts pop in
         (scale 0.86 -> 1, back.out(1.4)); exits blur out at about half the entrance; cuts and titles on beats (half
         bars at least). The window moves only by the stage's settle, swap and exit, plus push-ins. The cursor
         moves on eased recorded paths; clicks show a small press ring in the accent.
SHOTS:   (windows set by the sound stage on the track's bar lines: sound/timing.json = window.TM; build.py writes
         them into index.html; scenes find their cue words in window.VO with W())
         s1 open     0-14.845   the dot story on the bare ground, no window. v01 "$8.58 trillion": 858 dots (one
                                per $10 billion) bloom into a field; kicker "Federal assistance · fiscal years 2019
                                to 2024", legend "● $10 billion". v02: the headline becomes "Where did it go?" then
                                "What did the audits find?". v03: three dot + word labels rise under the field:
                                "USAspending.gov · who got the money", "FAC.gov · what audits found", "SAM.gov · who
                                is excluded". The last bar (12.37-14.845; v03 ends 12.49): the labels fade, the
                                dots stream onto the mark's two paths (blue onto the A, a few coral onto the
                                check) over the riser.
         s2 lockup   14.845-21.031  on the downbeat the dots resolve into the solid mark (strokes drawn), the
                                wordmark wipes in beside it: the lockup, centred. v04 "This is AuditsMadeSimple."
                                v05: the tagline "Federal spending and audit data, made understandable." Out: the
                                lockup lifts and blurs as the window settles.
         s3 explore  21.031-29.691  the window settles with the landing page (hero "Where does federal financial
                                assistance go?"). Kicker "Explore", headline "See where the money goes.", sub
                                "Interactive Tableau dashboards, built by the team." v06: the page scrolls to Part 1
                                "Funding by State", the cursor rests on the active chip "Top 10 States (50.9%)".
                                v07 "Ten states": push in on the bar chart's ten gold bars (California 12.34% down
                                to North Carolina 2.60%, as the dashboard itself shows them; the film adds no
                                per-state numbers of its own).
         s4 glossary 29.691-37.113  (3 bars) screen swap to glossary.html. Kicker "Glossary", headline "Look up the jargon.",
                                sub "54 terms in plain words, each with why it matters." v08: the cursor clicks the
                                search field and types "material weakness"; two cards remain; on "plain words" the
                                cursor rests on Material Weakness, the card flips: "A severe deficiency in internal
                                control ..." / "Why it matters: The most serious red flag in an audit."; push in on
                                the card.
         s5 score    37.113-47.010  screen swap to audit_health_score_casestudy.html, scrolled to the simulator.
                                Kicker "Audit Health Score", headline "One number from 0 to 100.", sub "Green, yellow
                                or red: a screening signal, not proof of wrongdoing." v09: the cursor drags the
                                slider from risk 10 (90 · Low, green) to 30 (70 · Medium, yellow), on "one number"
                                push in on the score circle; v10 "Red": on to 75 (25 · High, red); release.
         s6 proof    47.010-54.433  the window steps aside left and leaves; on the bare ground the voice's own clause
                                "Joined with spending records." holds the counter's place (on "with"), then hands over
                                to the counter, which counts to "$1.09 trillion" (Inter Display, navy); "went to 9,976
                                recipients in the red tier." A single horizontal bar splits by funding: ● Green $372.0
                                billion · ● Yellow $598.6 billion · ● Red $1.09 trillion (green on "records", yellow on
                                "scores", the red segment grows WITH the counter, same frames and ease, so the whole bar
                                holds 3 s; review 2026-11-01, it used to fill on "red" and finish 0.1 s before the
                                exit). Footnote:
                                "FAC audits joined to USAspending awards on UEI, fiscal years 2019 to 2024. A signal,
                                not proof of wrongdoing."
         s7 team     54.433-61.856  kicker "AGA Datathon 2026 · Washington, D.C.", headline "1st place nationally.",
                                sub "Fiscal Patriots · George Mason University". The five names with their roles as
                                the site's About page gives them, as plain text in one calm row (no cards):
                                Khaled Alkurd · Team lead, Pranavi Doodala · Project manager, Mariam Debas ·
                                Visualization lead, Nikita Chandrasing · Product manager, Andy Yaro · Product
                                developer. v12 over it.
         s8 end      61.856-67.4  the drums fall away. The mark draws (A, then the check), the wordmark beside it;
                                the line "Federal spending and audit data, made understandable."; the address pill
                                "gmufiscalpatriots.bytechisel.com" (Inter). v13. Hold, fade.
OBJECTS: the live site only (gmufiscalpatriots.bytechisel.com; same bytes as the repo's webapp/pages except the
         glossary, which is newer live: 54 terms vs 52): index (= landing_page.html) with the Part 1 carousel card
         and its Tableau embed, glossary.html, audit_health_score_casestudy.html (the simulator). Read and navigate
         only: no form submits, no logins. Capture at 1600 x 900 CSS px, dpr 2, on the virtual clock, from the live
         site; seed localStorage fiscal_guide_dismissed=true so the "New here?" card stays closed; block
         googletagmanager.com during capture (analytics only, not in the picture); wait for every
         public.tableau.com /views/ iframe to paint (first render ~2.4 s; a chip switch ~7 s, so no chip switch is
         recorded) before the clock starts. Never frame: the AHS page's "Core calculation" block and the ML page's
         code words (both monospace), the 👋 guide card. Numbers drawn by the film come from FACTS.md only.
CAPTURE: (capture stage, 2026-11-01: capture/vclock.js + rec.py + takes.py from the Outbreak share film, capture/conform.py
         from EV-SIENT's tools/conform.py, capture/sheet.py for contact sheets.) The live site, 1600 x 900 CSS px at dpr 2,
         recorded frame by frame on the virtual clock (top frame only; the Tableau iframes are painted and still before
         the clock starts), real pointer moves (4 per frame), real clicks and keys, eased window scrolls. Each take is
         scripted in FILM time from the word times in assets/vo.js and runs about 0.5 s before to 0.8 s after its scene,
         so it plays at 1x: no take needs a speed tag. Masters assets/rec/<take>.mp4 (3200 x 1800, H.264 CRF 17,
         yuv420p limited range, BT.709 tagged, keyframe every 10 frames; raw frames deleted) + <take>.json (pointer
         [x, y, down, visible] per frame in CSS px, marks as frame numbers, element boxes in CSS px).
         The edit: assets/shots/<shot>.mp4 (2400 x 1350 = 1.5x the viewport, CRF 16, same tags) and assets/edit.js
         (window.EDIT; edit.json for Python): per shot src, start, dur, speed, label (null), marks in film seconds,
         rects in CSS px (x EDIT.scale = 1.5 for shot px), scroll, cursor per film frame. The shot clip starts at
         `start` with data-media-start 0.
           explore  20.933-30.333 (9.40 s, s3)  landing hero holds through the settle; scroll to Part 1 22.10-23.90 (on
                    "money"); cursor fades in at 23.90 in the gap right of the card and arcs over the chip row (never
                    over the Tableau view, which has its own tooltips) to rest at 24.93 with its tip under the active
                    chip's "(50.9%)" (no click: a chip click reloads the Tableau view). Push-in boxes: bars [488, 591,
                    524, 195] (the ten gold bars, found by colour), chart [323, 520.9, 954, 715.5], chip [514.2, 386.9,
                    201.8, 37]; mark ten 26.067.
           glossary 29.600-37.767 (8.17 s, s4)  cursor in 29.83 above the chips, click on the search field 30.70 (the
                    border turns the site's accent), types "material weakness" 30.97-32.33 (the grid filters per key:
                    12 cards, then 4, then Material Weakness + Significant Deficiency), moves out left of the chips,
                    scroll 116 px 33.03-33.63, enters the Material Weakness card: flip 33.97-34.57 ("plain words"
                    34.31-34.57), rests 34.50 below the card's last line (the arrow never covers the definition).
                    Push-in box: card [136, 496.2, 314, 280]; cards [136, 496.2, 652, 280]; search [400, 234.8, 800, 55].
           score    37.000-47.667 (10.67 s, s5) AHS page at scroll 280 (simulator, then the site's own "Important:
                    Audit Health Score is a screening signal, not proof of wrongdoing" note in frame; the monospace
                    "Core calculation" block is 2,500 px below). Cursor in 37.40, grabs the knob 38.57, drags risk
                    10 -> 30 (yellow at 39.30), lets go 39.93 (score 70 Medium on "one number" 40.06); grabs again
                    42.73, drags 30 -> 75 (red at 43.20; "Red" 43.05), lets go 44.03 (25 High); holds to the end.
                    Push-in boxes: circle [578, 490.6, 120, 120], display [447, 469.6, 706, 141], slider [449, 385.2,
                    706, 4], note [406, 711.6, 788, 91.4].
         Glass bars: the site's sticky top bar is frosted (85% white + blur), so a faint blur of the page under it shows
         (landing: the 1/4 pill; AHS: the hero's sub-line). That is the real site, left as recorded. Re-run:
         <pw-venv>/bin/python -I capture/takes.py all; capture/conform.py; capture/sheet.py (snaps/capture-*.jpg).
         The EV-SIENT 3D laptop is not used (the SPEC's window stage carries the frame; it would add a fourth device).
BUILD:   (build stage, 2026-11-01: index.html, compositions/s1-open ... s8-end, assets/film.js, build.py.) HyperFrames 0.8.173,
         lint 0 errors 0 warnings, check --json ok (lint, runtime, layout, motion, contrast all 0 findings).
         Plumbing from secure-data-hub: one host per scene (data-composition-src), build.py writes each host's window from
         sound/timing.json and now also each take's clip window from assets/edit.json; every entrance is keyed to a word
         with W() over window.VO. The window lives in index.html, not in a scene: it spans s3 to s6 and holds the three
         <video class="clip"> takes at the top level of the root composition, as both references place theirs, so each
         take stays frame-accurate when seeked; the copy over it (kicker, headline, sub) is in the s3, s4 and s5 hosts.
         Window: 1202 x 727 incl. a 1 px separator hairline, radius 16, no shadow; a 50 px bar (three muted dots, the
         address pill in Inter Medium 22 on fill-quaternary); the screen 1200 x 675 at (360, 340), so 1 CSS px of the
         1600 x 900 capture = 0.75 px. Each take sits in a .cam (transform-origin 0 0) with its cursor (the Outbreak arrow,
         black with a white edge, scaled 0.86 while pressed) and a press ring in brand blue on each click or grab. Moves:
         settle at s3 (21.031), swaps at s4 (29.416 out, 29.691 in) and s5 (36.838 out, 37.113 in), push-ins (power2.inOut
         1.1 s): explore bars x1.35 from 25.93 ("Ten"); glossary x1.35 from 33.77 (flip 33.97, "plain" 34.31) framed by
         hand (camView, view top-left at CSS 75.5, 185) on the search box and the two cards, so the box is whole and
         nothing touches an edge; score x1.32 from 39.81 ("one" 40.06) framed by hand (view top-left at CSS 193.9, 142)
         on the whole simulator card with the site's "try the simulator!" scribble above and its "screening signal, not
         proof of wrongdoing" note below, the next heading out of frame (review 2026-11-01: the box-centred pushes cut the
         search box at two edges and sliced the scribble and the card top); s6 step aside 47.01-47.61
         (x -260, scale 0.94, fade, power2.in).
         s1/s2 hand-off: assets/film.js (window.FILM) seeds the 858 dots, the sunflower field (centre 1340, 540; spacing 12.4;
         r 6) and each dot's target inside the mark's strokes (30% on the check, coral), paired band by band so the stream
         flows one way without crossing; s1's last frame and s2's first frame put every dot in the same place. The lockup
         keeps the brand lockup's proportions (mark 280 px at x 503, y 318; wordmark 573 x 184.5; gap 60). The wordmark is
         assets/brand/film/wordmark.svg, cut unchanged from lockup-color.svg without the cream ground.
         Type as planned (Inter Display SemiBold heads, Inter body; local OFL files in assets/fonts with OFL-Inter.txt; no
         Montserrat needed: no caps labels). label-secondary is set solid #68686D for video legibility, as the CERFODES film
         did with the same HIG token. Built copy that refines the plan: s1 heads "$8.58 trillion." / "Where did it go?" +
         sub "And what did the audits find?" / "It’s all public." + sub "But split across three federal databases:" and
         the three dot rows; legend "$10 billion each"; s6 kicker "What the scores show"; s7 top to bottom as the voice says
         it: "Fiscal Patriots · George Mason University", the five names and roles, "1st place nationally.", "AGA Datathon
         2026 · Washington, D.C.".
         Picture events for the finish stage's effects (film s): s1 labels rise 9.51, 9.81, 10.11; stream 12.63-14.78; s2
         strokes draw 14.845-15.35, wordmark wipe 14.905; settle 21.031 (0.9 s); swaps 29.416-29.966 and 36.838-37.388;
         clicks/grabs (EDIT cursor down): 30.70 search, 38.567 and 42.733 slider (releases 39.933, 44.033); typing
         30.967-32.333; card flip 33.967; tier changes yellow 39.30, red 43.20; step aside 47.01; s6 headline 47.67, green fill 48.11,
         yellow 49.13, headline out 49.41-49.69, counter and red fill together 49.81-51.04 (one counter step per frame),
         red key 51.02, line 51.55 (review 2026-11-01: nothing new lands on "red" 53.23 any more); s7 names
         55.23 + 0.14 k (k 0-4), headline 57.53, sub 59.21; s8 A 61.97-62.59, check lands 62.85, wordmark 62.70, line
         63.25, pill 63.87, fade to ground 66.45-67.35.
BANNED:  monospace fonts (grep mono|Mono|monospace|Courier|Menlo|Consolas|ui-monospace before every snapshot);
         em dashes on screen and en dashes as separators (ranges are written "2019 to 2024"); the Huly look (cream
         editorial; the brand cream never fills a frame); the Linear look of Orkestra v2; Provalume's Biennale paper;
         Secure Data Hub's blueprint dot grid; drop shadows on content (the window gets a hairline, no shadow); a row
         of three feature cards of our own; the logo docked in a corner; screen shake; floods of messages or dots
         flying everywhere; any claim that red tier means fraud; any figure not in FACTS.md; implying Andy won alone.
QA:      1.8, 5.6, 10.4, 13.9, 15.6, 19.2, 23.0, 27.8, 31.8, 35.6, 38.6, 40.6, 45.5, 50.6, 53.9, 57.6, 60.9,
         63.2, 66.2.
```
