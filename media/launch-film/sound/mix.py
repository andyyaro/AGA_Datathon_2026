"""The AuditsMadeSimple soundtrack: Kokoro af_heart, "Hip Hop 02" (Lily J) as a quiet bed, and 67 soft effects.

    python3 -I sound/mix.py

Inputs: assets/audio/music.wav (sound/music.py), narration/chosen/<id>.wav + narration/words.json (narration/pick.py),
sound/sfx-src/mixkit-<id>.mp3 (Mixkit sound effects, Mixkit Sound Effects Free License; 1113 and 2531 copied from the
EV-SIENT film's assets/audio/sfx), assets/edit.json + assets/rec/glossary.json (the takes' pointer paths and key schedule).
Outputs:
- assets/audio/mix.wav: the soundtrack, -16 LUFS integrated, true peak under -1.5 dBTP.
- assets/audio/vo.wav: the voice alone, at its level in the mix (before the limiter).
- assets/vo.js: window.VO, each line's start/end and word times in film seconds.
- assets/timing.js and sound/timing.json: window.TM, the drop, the end card and the scene windows. Every scene reads
  its start from it, and build.py writes the same numbers into index.html.

Levels (Andy: "the sound should not be too loud, just present, the voice should be clear"):
- The voice is the loudest thing: speech at -16 LUFS (gated integrated loudness of the voice alone, so the silences
  between lines do not count). The bed sits 9 dB under it between lines and is ducked 4.5 dB more while she speaks
  (40 ms attack, 450 ms release), so about 13.5 dB under the speech.
- Each effect's loudest 50 ms sits 3-6 dB over the bed's RMS in the second around it, and its moment lands one frame
  after its picture. sound/sfx_events.json is the measured list (dB over the bed, dB against the voice's speech level).
"""
import json, subprocess, sys, tempfile
from pathlib import Path
import numpy as np, soundfile as sf, librosa

ROOT = Path(__file__).resolve().parent.parent
SR = 48000
G = json.loads((ROOT / "sound/grid.json").read_text())
DROP, END_CARD, DUR, BAR = G["drop"], G["end_card"], G["duration"], G["bar"]
fb = lambda k: round(k * BAR, 3)     # film bar k (the music is cut so film bar lines are k * 2.4742 s)

# each line's start in film seconds (see sound/music.py for the cut):
# - the hook (v01-v03) on the breakdown, a breath of 0.5-0.6 s between lines, then the last bar (12.37-14.85) left to
#   the riser while the dots stream onto the mark;
# - v04 starts 0.43 s before the drop: the vowel of "Audits" (0.43 s into the clip, after the glottal stop; Whisper
#   puts the word at 0.36) lands on the groove's first kick at 14.845;
# - every later line starts about 0.5 s after its scene's window opens (after the window's settle or screen swap),
#   so each beat's picture is in place before the voice names it.
SLOTS = {"v01": 1.18, "v02": 4.95, "v03": 7.75, "v04": round(DROP - 0.43, 3), "v05": 16.55,
         "v06": 21.55, "v07": 26.05, "v08": 30.45, "v09": 37.6, "v10": 43.05,
         "v11": 47.35, "v12": 54.95, "v13": 62.75}
# scene windows (film seconds), all on the track's bar lines (half bars at s2/s3)
SCENES = {"s1": [0, DROP],                 # bars 0-6: the dot story over the breakdown
          "s2": [DROP, fb(8.5)],           # bars 6-8.5: the lockup on the drop, the tagline
          "s3": [fb(8.5), fb(12)],         # 3.5 bars: explore (landing page, Part 1, push-in on the ten bars)
          "s4": [fb(12), fb(15)],          # 3 bars: glossary (search, type, flip, push-in, hold to read)
          "s5": [fb(15), fb(19)],          # 4 bars: Audit Health Score (slider 10 -> 30 -> 75)
          "s6": [fb(19), fb(22)],          # 3 bars: proof ($1.09 trillion counter, the tier bar)
          "s7": [fb(22), END_CARD],        # 3 bars: the team, 1st place
          "s8": [END_CARD, DUR]}           # the end card on the track's own outro, faded over the last 2.5 s


def lufs(path):
    out = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    summ = out[out.rfind("Summary:"):]
    i = float(summ.split("I:")[1].split("LUFS")[0])
    tp = float(summ.split("Peak:")[1].split("dBFS")[0]) if "Peak:" in summ else 0.0
    return i, tp


def to_stereo(y):
    return np.vstack([y, y]) if y.ndim == 1 else y


def load(path, sr=SR):
    y, s = sf.read(path, always_2d=True)
    y = y.T.astype(np.float64)
    if s != sr:
        y = np.vstack([librosa.resample(ch, orig_sr=s, target_sr=sr) for ch in y])
    return y


def main():
    words = json.loads((ROOT / "narration/words.json").read_text())
    music = load(ROOT / "assets/audio/music.wav")
    n = music.shape[1]

    # ---------------------------------------------------------------- the voice
    vo = np.zeros(n)
    meta, prev_end = {}, 0.0
    for key, t0 in SLOTS.items():
        y = load(ROOT / f"narration/chosen/{key}.wav").mean(0)
        if t0 < prev_end + 0.25:
            print(f"warning: {key} starts {prev_end + 0.25 - t0:.2f} s too early", file=sys.stderr)
        a = int(round(t0 * SR)); b = min(n, a + len(y))
        vo[a:b] += y[: b - a]
        end = t0 + len(y) / SR
        meta[key] = {"start": round(t0, 3), "end": round(end, 3), "text": words[key]["text"],
                     "words": [{"w": w["w"], "t0": round(t0 + w["t0"], 3), "t1": round(t0 + w["t1"], 3)} for w in words[key]["words"]]}
        prev_end = end
    tmp = Path(tempfile.mkdtemp())
    sf.write(tmp / "vo_raw.wav", vo.astype(np.float32), SR)
    # Kokoro is clean and bright already: a high-pass, a touch of presence, light de-essing and compression
    chain = ("highpass=f=80,equalizer=f=3000:t=q:w=1.2:g=1.5,equalizer=f=250:t=q:w=1.0:g=-1,"
             "deesser=i=0.2:f=0.5,acompressor=threshold=0.1:ratio=2.5:attack=10:release=150:makeup=1.3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp / "vo_raw.wav"), "-af", chain, "-ar", str(SR),
                    str(ROOT / "assets/audio/vo.wav")], check=True)
    vo = load(ROOT / "assets/audio/vo.wav").mean(0)[:n]
    vo = np.pad(vo, (0, n - len(vo)))

    # ---------------------------------------------------------------- the bed: quieter, less boom, ducked by the voice
    sf.write(tmp / "m.wav", music.T.astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp / "m.wav"), "-af",
                    "bass=g=-4:f=110:w=0.7,equalizer=f=2500:t=q:w=1.5:g=-2", str(tmp / "m2.wav")], check=True)
    bed = load(tmp / "m2.wav")
    # measured as it sits in the mix: the same signal in both channels (a mono file would read 3 dB quieter)
    sf.write(tmp / "v.wav", np.vstack([vo, vo]).T.astype(np.float32), SR)
    vi, _ = lufs(tmp / "v.wav")
    bi, _ = lufs(tmp / "m2.wav")
    # speech at -16 LUFS: EBU R128 gating already drops the silent blocks between lines, so the voice track's
    # integrated loudness is the loudness of the speech itself
    vo *= 10 ** ((-16 - vi) / 20)
    # Kokoro's plosives peak up to 5 dB over the rest of her speech: catch them on the voice alone (-3 dBFS ceiling,
    # 1 ms look-ahead, delay compensated) so the master limiter never has to squash a word or pump the bed
    sf.write(tmp / "v.wav", np.vstack([vo, vo]).T.astype(np.float32), SR, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp / "v.wav"), "-af",
                    "alimiter=limit=0.708:attack=1:release=40:level=disabled:latency=1", "-c:a", "pcm_f32le",
                    str(tmp / "v_lim.wav")], check=True)
    vo = load(tmp / "v_lim.wav").mean(0)[:n]; vo = np.pad(vo, (0, n - len(vo)))
    vi2, _ = lufs(tmp / "v_lim.wav")
    vo *= 10 ** ((-16 - vi2) / 20)
    bed *= 10 ** ((-25 - bi) / 20)            # the bed 9 dB under the speech before ducking
    # duck: -4.5 dB under the voice, 40 ms attack, 450 ms release (followed at 1 kHz, then interpolated)
    hop = SR // 1000
    env = np.sqrt(np.convolve(vo ** 2, np.ones(int(0.05 * SR)) / int(0.05 * SR), "same"))[::hop]
    on = (env > 10 ** (-45 / 20)).astype(float)
    g = np.empty(len(on)); state = 0.0
    att, rel = 1 - np.exp(-1 / (0.04 * 1000)), 1 - np.exp(-1 / (0.45 * 1000))
    for i, target in enumerate(on):
        state += (att if target > state else rel) * (target - state)
        g[i] = state
    g = np.interp(np.arange(n), np.arange(len(g)) * hop, g)
    duck = 10 ** (-4.5 * g / 20)
    bed *= duck

    # ---------------------------------------------------------------- effects
    sfx = np.zeros((2, n))
    TMd = {"drop": DROP, **SCENES}
    W = word_finder(meta)
    events = sfx_events(W, TMd, meta)
    placed = [place(sfx, name, t, gain_db, pitch, bed) for t, name, gain_db, pitch in events]

    # ---------------------------------------------------------------- sum, level, limit
    mix = bed + sfx + np.vstack([vo, vo])
    sf.write(tmp / "mix.wav", mix.T.astype(np.float32), SR)
    mi, _ = lufs(tmp / "mix.wav")
    mix *= 10 ** ((-16 - mi) / 20)
    sf.write(tmp / "mix2.wav", mix.T.astype(np.float32), SR)
    # the master limiter runs at 4x the sample rate, so it catches the peaks between samples too (a mouse click's sharp
    # transient overshot the sample-peak ceiling by 0.6 dB between samples)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp / "mix2.wav"), "-af",
                    "aresample=192000,alimiter=limit=0.79:attack=3:release=60:level=disabled:latency=1,aresample=48000",
                    "-ar", str(SR), str(ROOT / "assets/audio/mix.wav")], check=True)
    fi, tp = lufs(ROOT / "assets/audio/mix.wav")
    # the voice alone at its level in the mix (for checks and stems), and a measured report of the balance
    gain = 10 ** ((-16 - mi) / 20)
    sf.write(ROOT / "assets/audio/vo.wav", (np.vstack([vo, vo]) * gain).T.astype(np.float32), SR, subtype="FLOAT")
    sf.write(tmp / "bed_pre.wav", (bed / duck * gain).T.astype(np.float32), SR)
    vli, _ = lufs(ROOT / "assets/audio/vo.wav"); bli, _ = lufs(tmp / "bed_pre.wav")
    speaking = g > 0.5
    rms = lambda x: 10 * np.log10(np.mean(x ** 2) + 1e-12)
    duck_db = float(np.median(20 * np.log10(duck[speaking])))
    print(f"levels: speech {vli:.1f} LUFS, bed (before ducking) {bli:.1f} LUFS = {vli - bli:.1f} dB under the voice; "
          f"ducked {duck_db:.1f} dB more while she speaks (median), so {vli - bli - duck_db:.1f} dB under the speech")

    (ROOT / "assets/vo.js").write_text("window.VO = " + json.dumps(meta) + ";\n")
    tm = {"drop": DROP, "end_card": END_CARD, "track_ending": G["track_ending"], "duration": DUR, **SCENES}
    (ROOT / "assets/timing.js").write_text("window.TM = " + json.dumps(tm) + ";\n")
    (ROOT / "sound/timing.json").write_text(json.dumps(tm, indent=1))
    print(f"mix.wav {DUR} s, {fi:.1f} LUFS, true peak {tp:.1f} dBTP; voice, bed and {len(events)} effects")
    sfx_report(placed, vo, events)
    print("lines: " + ", ".join(f"{k} {m['start']:.2f}-{m['end']:.2f}" for k, m in meta.items()))


def word_finder(meta):
    norm = lambda s: "".join(c for c in s.lower() if c.isalnum())
    def W(k, w, nth=0):
        alts = w.split("|")
        ws = meta[k]["words"]
        for exact in (True, False):
            c = 0
            for x in ws:
                t = norm(x["w"])
                if any((t == a) if exact else t.startswith(a) for a in alts):
                    if c == nth: return x["t0"]
                    c += 1
        print(f"warning: no word {w!r} in {k}", file=sys.stderr)
        return meta[k]["start"]
    return W


SFX = {  # Mixkit sound effects (sound/sfx-src/mixkit-<id>.mp3); the vocabulary is secure-data-hub's, plus the pointer
    "whoosh_wind": "mixkit-1465.mp3", "whoosh_air": "mixkit-1492.mp3", "sweep": "mixkit-3115.mp3",
    "tick": "mixkit-1120.mp3", "pop": "mixkit-2357.mp3", "pop_hard": "mixkit-3005.mp3",
    "typing": "mixkit-2538.mp3", "riser": "mixkit-2408.mp3",
    # the pointer, as in the EV-SIENT film (its sound/design.py): a real mouse click (press at 0.011 s, release at
    # 0.140 s in the file, split so each half lands on its own recorded frame) and single keys cut from a laptop take
    "click_down": "mixkit-1113.mp3", "click_up": "mixkit-1113.mp3", "key": "mixkit-2531.mp3",
}
WIN = int(0.05 * SR)          # an effect's level is the RMS of its loudest 50 ms
BED_WIN = int(1.0 * SR)       # the bed's level is its RMS over the second around the effect's peak (a shorter window follows single drum hits)
_cache = {}


def win_rms_db(y, w=WIN):
    e = np.convolve((y ** 2).mean(0), np.ones(w) / w, "same")
    k = int(np.argmax(e))
    return 10 * np.log10(e[k] + 1e-12), k


def key_slices():
    """Single keystrokes cut from the laptop typing take (EV-SIENT's slices(): onsets 20 dB under the loudest hit,
    at least 40 ms apart, 85 ms each from just before the onset, 10 ms fade out)."""
    y = load(ROOT / "sound/sfx-src" / SFX["key"])
    m = y.mean(0); hop = SR // 1000
    e = np.sqrt(np.convolve(m ** 2, np.ones(hop) / hop, "same"))[::hop]
    th = e.max() * 10 ** (-20 / 20)
    out, last = [], -10_000
    for i in range(1, len(e)):
        if e[i] > th >= e[i - 1] and i - last > 40:
            last = i
            a = max(0, (i - 4) * hop); s = y[:, a: a + int(0.085 * SR)].copy()
            if s.shape[1] < int(0.085 * SR): continue
            f = int(0.01 * SR); s[:, -f:] *= np.linspace(1, 0, f)
            out.append(s)
    return out


def clip(name, variant=0):
    if (name, variant) not in _cache:
        if name == "key":
            ks = _cache.setdefault("_keys", key_slices())
            y = ks[(variant * 7) % len(ks)]
        else:
            y = load(ROOT / "sound/sfx-src" / SFX[name])
        if name == "typing":   # a short burst of keys from the middle of the take
            y = y[:, int(1.0 * SR): int(1.75 * SR)]
            f = int(0.03 * SR); y[:, :f] *= np.linspace(0, 1, f); y[:, -f:] *= np.linspace(1, 0, f)
        if name == "riser":    # let it swell in from nothing
            f = int(1.2 * SR); y = y.copy(); y[:, :f] *= np.linspace(0, 1, f) ** 2
        if name == "click_down":   # the press: 0 to 0.10 s
            y = y[:, : int(0.10 * SR)].copy(); f = int(0.01 * SR); y[:, -f:] *= np.linspace(1, 0, f)
        if name == "click_up":     # the release: 0.125 to 0.30 s
            y = y[:, int(0.125 * SR): int(0.30 * SR)].copy(); f = int(0.02 * SR); y[:, -f:] *= np.linspace(1, 0, f)
        # the moment: a transient's onset for the pointer, the loudest 5 ms for everything else
        env = np.convolve(np.abs(y).mean(0), np.ones(240) / 240, "same")
        if name in ("click_down", "click_up", "key"):
            peak = int(np.argmax(env > 0.3 * env.max())) / SR
        else:
            peak = np.argmax(env) / SR
        _cache[(name, variant)] = (y, peak)
    return _cache[(name, variant)]


def place(out, name, t, gain_db, pitch, bed):
    """Put effect `name` in `out` so its moment lands one frame after film time t, its loudest 50 ms `gain_db` over
    the bed's RMS around that moment. Returns (t, name, start sample, the placed signal) for the report."""
    variant = 0
    if name.startswith("key"):
        name, variant = "key", int(name[3:] or 0)
    y, peak = clip(name, variant)
    if pitch != 1.0:   # small pitch steps rotate repeated sounds (resampling also shortens or lengthens them)
        y = np.vstack([librosa.resample(ch, orig_sr=SR, target_sr=int(SR / pitch)) for ch in y]); peak /= pitch
    at = int(round((t + 1 / 30) * SR))
    lo, hi = max(0, at - BED_WIN // 2), min(bed.shape[1], at + BED_WIN // 2)
    bed_db = 10 * np.log10(np.mean(bed[:, lo:hi] ** 2) + 1e-12)
    lvl, _ = win_rms_db(y)
    y = y * 10 ** ((bed_db + gain_db - lvl) / 20)
    a = int(round((t + 1 / 30 - peak) * SR))   # its peak one frame after the picture
    s0 = max(0, -a); a = max(0, a)
    b = min(out.shape[1], a + y.shape[1] - s0)
    out[:, a:b] += y[:, s0: s0 + (b - a)]
    return t, name, a, y[:, s0: s0 + (b - a)], bed_db


def sfx_report(placed, vo, events):
    """Measured: each effect's loudest 50 ms over the bed under it, and under the voice (her median 50 ms level while
    she speaks, the same measure). Effects should sit 3-6 dB over the bed and always under the voice."""
    m = vo ** 2
    e = np.convolve(m, np.ones(WIN) / WIN, "same")
    speak = e > 10 ** (-45 / 10)
    v_db = 10 * np.log10(np.median(e[speak]))
    over, under = [], []
    for t, name, a, y, bed_db in placed:
        lvl, _ = win_rms_db(y)
        over.append(lvl - bed_db); under.append(lvl - v_db)
    over, under = np.array(over), np.array(under)
    print(f"effects: {len(placed)}; over the bed {over.min():.1f} to {over.max():.1f} dB; "
          f"under the voice's speech level by {-under.max():.1f} to {-under.min():.1f} dB")
    bad = [(round(p[0], 2), p[1]) for p, o, u in zip(placed, over, under) if not (2.9 <= o <= 6.1) or u > -3]
    if bad: print("warning: effects outside 3-6 dB over the bed or not 3 dB under the voice:", bad, file=sys.stderr)
    (ROOT / "sound/sfx_events.json").write_text(json.dumps(
        [{"t": round(p[0], 3), "sound": p[1], "db_over_bed": round(float(o), 1), "db_vs_voice": round(float(u), 1),
          "pitch": ev[3]} for p, o, u, ev in zip(placed, over, under, events)], indent=1))


def pointer_events(shot):
    """Presses and releases from a take's recorded pointer path (EDIT cursor [x, y, down, visible] per film frame)."""
    s = EDIT["shots"][shot]; out, down = [], 0
    for i, (x, y, d, v) in enumerate(s["cursor"]):
        t = s["start"] + i / 30
        if d and not down: out.append((t, "click_down"))
        if down and not d: out.append((t, "click_up"))
        down = d
    return out


def key_times():
    """The film time each typed key first shows in the glossary take: capture/rec.py type_text() types key k before
    recorded frame type0 + due[k] - 1; capture/conform.py maps recorded frames to film frames."""
    rec = json.loads((ROOT / "assets/rec/glossary.json").read_text())
    s = EDIT["shots"]["glossary"]
    text, t0f, t1f = "material weakness", rec["marks"]["type0"], rec["marks"]["type1"]
    n = max(len(text), t1f - t0f)
    due = [round((i + 1) * n / len(text)) for i in range(len(text))]
    keys = s["keys"]
    def frame_at(t):
        for (ta, fa), (tb, fb) in zip(keys, keys[1:]):
            if t <= tb: return round(fa + (fb - fa) * (t - ta) / (tb - ta))
        return keys[-1][1]
    films = [f / 30 for f in range(int(s["start"] * 30), int((s["start"] + s["dur"]) * 30) + 1)]
    out = []
    for k in range(len(text)):
        g = t0f + due[k] - 1
        out.append(next(t for t in films if frame_at(t) >= g))
    return out


EDIT = json.loads((ROOT / "assets/edit.json").read_text())


def sfx_events(W, TM, meta):
    """(film time of the picture, sound, dB over the bed, pitch). Every time below is a picture event of the built
    film (index.html, compositions/*.html, assets/edit.json; listed in SPEC.md BUILD). One vocabulary, as in
    secure-data-hub: a soft pop is a part arriving, a tick a step or a counter, a whoosh travel or a camera move, a
    riser and a soft hit on the drop; the pointer's real presses, releases and keys. Nothing here is a denial, so the
    low pop is never used. Levels 3-6 dB over the bed (measured: sound/sfx_events.json)."""
    e = []
    # s1, the hook (the breakdown: keys and soft bass). The field of 858 dots blooms on "$8.58"; the legend; the three
    # databases rise one by one on "three"; the dots stream onto the mark over the riser (fastest at about 13.7 s)
    e.append((W("v01", "8") + 0.05, "pop", 3, 1.0))
    e.append((W("v01", "trillion") + 0.56, "tick", 3, 1.0))
    for k in range(3):
        e.append((W("v03", "three") - 0.04 + 0.3 * k, "tick", 4, (1.0, 1.06, 1.12)[k]))
    e.append((13.7, "whoosh_wind", 3, 1.0))
    # the drop: the riser peaks on the first kick, and the mark resolves with a soft hit
    e.append((TM["drop"], "riser", 4, 1.0))
    e.append((TM["drop"], "pop", 5, 1.0))
    # s2: the tagline; out, the window settles (an ease-out arrival: fastest on its first frame)
    e.append((W("v05", "federal") - 0.04, "tick", 3, 1.0))
    e.append((TM["s3"][0], "whoosh_air", 4, 1.0))
    # s3: the push-in on the ten gold bars (power2.inOut 1.1 s: fastest at its middle)
    e.append((W("v07", "ten") - 0.12 + 0.55, "whoosh_air", 3, 1.1))
    # s4: the screen swap (through the bare stage, at the scene line); the pointer clicks the search field; the keys
    # of "material weakness" as each letter shows; the card flips (its back face is in by 34.2); the push-in
    e.append((TM["s4"][0], "whoosh_air", 4, 1.06))
    e += [(t, name, 5 if name == "click_down" else 4, 1.0) for t, name in pointer_events("glossary")]
    for k, t in enumerate(key_times()):
        e.append((t, f"key{k}", 3.5 + (0.5 if k % 3 == 0 else -0.3 if k % 3 == 1 else 0.2), 1.0))
    flip = EDIT["shots"]["glossary"]["marks"]["flip"]
    e.append((flip + 0.23, "pop", 4, 1.0))
    e.append((flip - 0.2 + 0.55, "whoosh_air", 3, 1.1))
    # s5: the swap; the pointer grabs the knob and lets go, twice; the score counts down (a tick every 10 points,
    # except where the tier word changes: there the new tier arrives with a pop); the push-in on the score
    e.append((TM["s5"][0], "whoosh_air", 4, 1.03))
    e += [(t, name, 5 if name == "click_down" else 4, 1.0) for t, name in pointer_events("score")]
    mk = EDIT["shots"]["score"]["marks"]
    e.append((mk["yellow"], "pop", 4, 1.0))
    e.append((mk["red"], "pop", 4, 0.94))
    sc = EDIT["shots"]["score"]; prev = None; k = 0
    for i, (x, y, d, v) in enumerate(sc["cursor"]):
        score = 100 - round((x - 463) / 4.52)          # the knob's value: x = 463 + 4.52 risk (capture/takes.py knob())
        t = sc["start"] + i / 30
        if d and prev is not None and any(score <= m < prev for m in range(10, 100, 10)):
            if min(abs(t - mk["yellow"]), abs(t - mk["red"])) > 0.15:
                e.append((t, "tick", 3, (1.0, 0.97, 0.94, 0.91)[min(k, 3)])); k += 1
        prev = score if d else prev
    e.append((W("v09", "one") - 0.25 + 0.55, "whoosh_air", 3, 1.1))
    # s6: the window steps aside and leaves (an ease-in exit: fastest at its end, 47.61); the green and yellow parts of
    # the bar fill; the counter ticks on every tenth of a trillion as it counts (fast, then slowing: cubic ease out)
    # and the figure lands with a pop
    e.append((TM["s6"][0] + 0.48, "whoosh_air", 4, 0.95))
    e.append((W("v11", "records") + 0.05, "tick", 3, 1.0))
    e.append((W("v11", "scores") + 0.05, "tick", 3, 1.06))
    s6 = TM["s6"][0]
    f0 = int(np.ceil((W("v11", "1") - s6) * 30 - 1e-9)); f1 = int(np.ceil((W("v11", "trillion") - 0.1 - s6) * 30 - 1e-9))
    shown = lambda f: round(1.09 * (1 - (1 - min(1, (f - f0) / (f1 - f0))) ** 3), 2)
    k = 0
    for f in range(f0 + 1, f1):
        if int(shown(f) * 10) > int(shown(f - 1) * 10):
            e.append((s6 + f / 30, "tick", 3.5 - 0.05 * k, 1.0 + 0.02 * k)); k += 1
    e.append((s6 + f1 / 30, "pop", 4, 1.0))
    # s7: the five names in a row (staggered 0.14 s), "1st place nationally." lands with a pop, the event line ticks
    for k in range(5):
        e.append((W("v12", "students") + 0.14 * k, "tick", 3, 1.0 + 0.04 * k))
    e.append((W("v12", "first") - 0.04, "pop", 5, 1.0))
    e.append((W("v12", "aga") - 0.04, "tick", 3, 1.0))
    # s8, the end card on the track's outro: the check lands in the mark (soft pop); the address pill on "Explore"
    e.append((TM["s8"][0] + 0.95, "pop", 5, 1.0))
    e.append((W("v13", "explore") - 0.04, "tick", 4, 1.0))
    return sorted(e)


if __name__ == "__main__":
    main()
