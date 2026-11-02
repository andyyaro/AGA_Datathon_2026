"""Cut "Hip Hop 02" (Lily J, Mixkit 738, Mixkit Stock Music Free License) to the AuditsMadeSimple film.

    python3 -I sound/music.py     # -> assets/audio/music.wav, sound/grid.json

Andy, 2026-11-01: "calm but not too calm"; every film in the series has its own track.
Hip Hop 02 is relaxed, positive contemporary R&B at 97.0 BPM, 4/4 (measured 2026-11-01 with librosa: the beat
tracker says 97.5, but a fine scan of the kick onsets fits 97.00 exactly and 97.5 drifts off within a minute).
A bar is 2.4742 s. The downbeat kicks start at 0.045 s in the decoded file (onset within +-10 ms on every bar
checked), so a bar line here is 0.040 + 2.4742 n s: 5 ms before the kick, so a cut never clips its attack.
The chords run in a 4-bar cycle (chroma: bar vs bar+4 similarity 0.98): chord I on bars 4k, 4k+1, chord II on
4k+2, 4k+3. Structure (RMS per bar and band):
- Bars 0-31 (0.04-79.2): the full groove from the first sample (kick, snare on 2 and 4, hats, bass, keys).
  There is NO quiet intro. Bars 16-17 vary the kick pattern; the groove never stops.
- Bars 32-41 (79.2-104.0): the breakdown. Hats about 20 dB down, the kick gone, keys and a soft bass on 1 and 3.
- Bars 42-45 (104.0-113.9): the track's own outro. Bar 42 the last bass, bar 43 the keys alone, bar 44 the final
  chord with one low note, bar 45 its ring-out; silence from about 114.

So the drop is made by the edit (joins on bar lines, 12 ms crossfades, chord cycle kept: each join goes from a
bar 4k+3 to a bar 4k, or from 4k+2 to 4k+3):
  film  0.00-14.85  track  84.17-99.01  bars 34-39: the breakdown under the hook (keys, soft bass, no drums),
                                        starting on chord II so its last bar leads into chord I on the drop
  film 14.85-61.86  track   0.04-47.05  bars 0-18: THE DROP. The groove's first kick lands with the name, on
                                        "Audits" in "This is AuditsMadeSimple."
  film 61.86-67.40  track 106.43-...    bars 43-45: the drums fall away under the end card; the track's own
                                        outro (keys, the final chord), faded over the last 2.5 s
Film bar k starts at 2.4742 k s, and the drop is film bar 6.
"""
import json, subprocess
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
TRACK = ROOT / "sound/track.mp3"
SR, B0, BPM = 48000, 0.040, 97.0
BAR = 4 * 60 / BPM
tb = lambda n: B0 + n * BAR          # track bar n
fb = lambda k: k * BAR               # film bar k
DROP, END_CARD = fb(6), fb(25)
SEGMENTS = [(0.0, tb(34)), (DROP, tb(0)), (END_CARD, tb(43))]   # (film start, track start)
FILM_END = 67.4
FADE = 2.5
XF = 0.012


def main():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(TRACK), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    track = np.frombuffer(raw, np.float32).reshape(-1, 2).T.astype(np.float64)
    n = int(round(FILM_END * SR))
    out = np.zeros((2, n))
    x = int(XF * SR); ramp = np.linspace(0, 1, x)
    for k, (f0s, t0s) in enumerate(SEGMENTS):
        f0 = int(round(f0s * SR)); f1 = int(round(SEGMENTS[k + 1][0] * SR)) if k + 1 < len(SEGMENTS) else n
        t0 = int(round(t0s * SR))
        seg = track[:, t0: t0 + (f1 - f0)]
        seg = np.pad(seg, ((0, 0), (0, (f1 - f0) - seg.shape[1])))
        if k > 0:   # the outgoing bar fades out over the 12 ms before the line while the incoming one fades in
            pre = track[:, max(0, t0 - x): t0]
            pre = np.pad(pre, ((0, 0), (x - pre.shape[1], 0)))
            out[:, f0 - x: f0] = out[:, f0 - x: f0] * (1 - ramp) + pre * ramp
        out[:, f0:f1] = seg
    fi = int(0.3 * SR); out[:, :fi] *= np.linspace(0, 1, fi)
    fo = int(FADE * SR); out[:, -fo:] *= np.linspace(1, 0, fo) ** 1.5
    import soundfile as sf
    (ROOT / "assets/audio").mkdir(parents=True, exist_ok=True)
    sf.write(ROOT / "assets/audio/music.wav", out.T.astype(np.float32), SR, subtype="FLOAT")   # float: the mp3's overs are not clipped
    grid = {"track": "Hip Hop 02 (Lily J, Mixkit 738)", "bpm": BPM, "bar": round(BAR, 5), "track_bar0": B0,
            "drop": round(DROP, 3), "end_card": round(END_CARD, 3), "track_ending": round(END_CARD, 3),
            "fade_out": [round(FILM_END - FADE, 3), FILM_END], "duration": FILM_END,
            "segments": [[round(f, 3), round(t, 3)] for f, t in SEGMENTS],
            "segment_bars": [[0, 6, "track bars 34-39, breakdown"], [6, 25, "track bars 0-18, groove"],
                             [25, None, "track bars 43-45, outro"]],
            "film_bars": [round(fb(k), 3) for k in range(int(FILM_END / BAR) + 1)]}
    (ROOT / "sound/grid.json").write_text(json.dumps(grid, indent=1))
    print(f"music.wav {FILM_END} s; drop {DROP:.3f}, end card {END_CARD:.3f}, bar {BAR:.4f}")


if __name__ == "__main__":
    main()
