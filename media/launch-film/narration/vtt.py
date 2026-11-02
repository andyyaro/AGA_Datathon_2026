"""Captions for the film: renders/audits-made-simple-v1.en.vtt from the narration as it sits in the mix.

    python3 -I narration/vtt.py

The text is the written script (narration/lines.json: "$8.58 trillion", "AuditsMadeSimple", "AGA"), not the spoken
spelling in lines-tts.json; the times are each line's place in the film (assets/vo.js, written by sound/mix.py).
A line longer than 64 characters becomes two cues, split after its first comma or full stop past a quarter of the line,
the second cue starting on its first word's time. Rows wrap at about 42 characters, two rows at most, preferring a break after punctuation.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINES = json.loads((ROOT / "narration/lines.json").read_text())
VO = json.loads((ROOT / "assets/vo.js").read_text().split("=", 1)[1].strip().rstrip(";"))
OUT = ROOT / "renders/audits-made-simple-v1.en.vtt"
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def ts(t):
    h, r = divmod(max(0.0, t), 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def wrap(text, width=42):
    if len(text) <= width: return text
    words = text.split(); best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        score = max(len(a), len(b)) - (7 if a[-1] in ",.?:" else 0)
        if best is None or score < best[0]: best = (score, a, b)
    return best[1] + "\n" + best[2]


cues = []
for key, text in LINES.items():
    v = VO[key]
    if len(text) > 64:
        m = next((m for m in re.finditer(r"[,.?:] ", text) if m.start() > len(text) / 4), None)
        if m:
            first, second = text[: m.start() + 1], text[m.end():]
            w0 = norm(second.split()[0])
            n_before = len(first.split())
            # the spoken words are Whisper's tokens; find the second part's first word at or after its position
            t1 = next((w["t0"] for w in v["words"][max(0, n_before - 2):] if norm(w["w"]) == w0), None)
            if t1 is not None:
                cues += [(v["start"], t1 - 0.04, first), (t1, v["end"], second)]
                continue
    cues.append((v["start"], v["end"], text))

out = ["WEBVTT", ""]
for i, (a, b, text) in enumerate(cues, 1):
    out += [str(i), f"{ts(a)} --> {ts(b)}", wrap(text), ""]
OUT.parent.mkdir(exist_ok=True)
OUT.write_text("\n".join(out))
print(f"{OUT.relative_to(ROOT)}: {len(cues)} cues, {cues[0][0]:.2f}-{cues[-1][1]:.2f} s")
