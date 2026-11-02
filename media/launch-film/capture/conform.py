"""The edit of the recorded takes: which recorded frame plays on each film frame, keyed to the narration.

    <pw-venv>/bin/python -I capture/conform.py        -> assets/shots/<shot>.mp4, assets/edit.js (window.EDIT), assets/edit.json

Adapted from the EV-SIENT launch film's tools/conform.py. Each shot is a list of (film time, recording frame) keys;
between keys the recording plays at whatever speed joins them (a hold is two keys on one frame). The keys sit on the
narration's word times (assets/vo.js) and on the takes' own marks (assets/rec/<take>.json), so if a line moves, its
shot follows. The takes were recorded in film time (capture/takes.py), so today every key pair runs at exactly 1x.
If a later retime makes a stretch of picture play faster than it was recorded, the shot's `label` says so (for the
composition's corner tag, e.g. "1.5× speed"); slower than recorded is never allowed (it would repeat frames).

Shot windows: each shot starts 0.1 s before its scene (the window settles, or the screen swaps in, on the scene's bar
line) and runs on past the next scene's start while the window swaps or steps aside (TAIL). Frames are picked, never
blended. The output is 2400 x 1350 (1.5x the 1600 x 900 CSS viewport), so a push-in to 1.35x in a window up to about
1780 px wide stays sharp. Pointer paths, marks and element boxes stay in CSS px of the viewport (multiply by
EDIT.scale for shot pixels).
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REC = ROOT / 'assets' / 'rec'
OUT = ROOT / 'assets' / 'shots'
FPS = 30
VIEW = (1600, 900)
SIZE = (2400, 1350)
TM = json.loads((ROOT / 'sound' / 'timing.json').read_text())
VO = json.loads(re.search(r'\{.*\}', (ROOT / 'assets' / 'vo.js').read_text(), re.S).group(0))
norm = lambda w: re.sub(r"[^a-z0-9$.']", '', w.lower()).strip('.')


def W(line, word, nth=0, end=False):
    hits = [x for x in VO[line]['words'] if norm(x['w']) == norm(word)]
    return hits[nth]['t1' if end else 't0']


def take(name):
    return json.loads((REC / f'{name}.json').read_text())


fr = lambda t: round(t * FPS)
HEAD, TAIL = 0.1, 0.65

# ---------------------------------------------------------------- the shots: (film s, recording frame) keys
def shots():
    ex, gl, sc = take('explore'), take('glossary'), take('score')
    M = lambda tk, k: tk['marks'][k]
    R = lambda tk, t: round((t - tk['t0']) * FPS)          # the frame a take recorded for film time t
    S3, S4, S5 = TM['s3'], TM['s4'], TM['s5']
    out = {}
    # s3: the hero holds through the settle; on "money" the scroll to Part 1; the pointer rests on the chip by "goes"
    a, b = S3[0] - HEAD, S3[1] + TAIL
    k0 = W('v06', 'money') + 0.01
    k1 = W('v06', 'goes') - 0.05
    out['explore'] = ('explore', a, b, 's3', [(a, M(ex, 'scroll0') - fr(k0 - a)), (k0, M(ex, 'scroll0')),
                                              (k1, M(ex, 'rest')), (b, M(ex, 'rest') + fr(b - k1))])
    # s4: the click on "on", the typing over "material weakness", the flip on "plain words"
    a, b = S4[0] - HEAD, S4[1] + TAIL
    k0 = W('v08', 'on') - 0.05
    k1 = W('v08', 'weakness', end=True) + 0.05
    k2 = W('v08', 'plain') - 0.35                    # the flip starts as the pointer crosses the card's top edge
    out['glossary'] = ('glossary', a, b, 's4', [(a, M(gl, 'click') - fr(k0 - a)), (k0, M(gl, 'click')),
                                                (k1, M(gl, 'type1')), (k2, M(gl, 'flip')), (b, M(gl, 'flip') + fr(b - k2))])
    # s5: the first drag between "score" and "one"; the second from just before "Red"
    a, b = S5[0] - HEAD, S5[1] + TAIL
    k0 = W('v09', 'score') + 0.33
    k1 = W('v10', 'red') - 0.3
    out['score'] = ('score', a, b, 's5', [(a, M(sc, 'grab1') - fr(k0 - a)), (k0, M(sc, 'grab1')),
                                          (k1, M(sc, 'grab2')), (b, M(sc, 'grab2') + fr(b - k1))])
    return out


def frame_at(keys, t):
    if t <= keys[0][0]: return keys[0][1]
    for (t0, f0), (t1, f1) in zip(keys, keys[1:]):
        if t <= t1: return round(f0 + (f1 - f0) * (t - t0) / (t1 - t0))
    return keys[-1][1]


def speeds(keys):
    """Playback speed of each key segment (recorded frames per film frame)."""
    return [((f1 - f0) / max(1e-9, (t1 - t0) * FPS)) for (t0, f0), (t1, f1) in zip(keys, keys[1:])]


def conform(name, tk_name, start, end, scene, keys):
    tk = take(tk_name)
    n = tk['frames']
    f0, f1 = fr(start), fr(end)
    src = [frame_at(keys, f / FPS) for f in range(f0, f1)]
    assert all(0 <= k < n for k in src), f'{name}: needs recorded frames {min(src)}..{max(src)}, the take has 0..{n - 1}'
    assert all(b >= a for a, b in zip(src, src[1:])), f'{name}: the recording would run backwards'
    sp = speeds(keys)
    assert min(sp) > 0.97, f'{name}: slower than recorded ({min(sp):.2f}x) would repeat frames'
    fast = max(sp)
    label = None if fast < 1.04 else f'{fast:.1f}× speed'.replace('.0×', '×')
    # stream the take's frames through, picking one per film frame (no temp files: decode -> pick -> encode)
    OUT.mkdir(parents=True, exist_ok=True)
    w, h = SIZE
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(REC / f'{tk_name}.mp4'), '-vf', f'scale={w}:{h}:flags=lanczos:out_color_matrix=bt709:out_range=tv',
                            '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    dst = OUT / f'{name}.mp4'
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-s', f'{w}x{h}', '-r', str(FPS),
                            '-i', '-', '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-g', '10', '-bf', '0',
                            '-movflags', '+faststart', str(dst)], stdin=subprocess.PIPE)
    size = w * h * 3 // 2
    cur, buf = -1, None
    for k in src:
        while cur < k:
            buf = dec.stdout.read(size); cur += 1
            assert len(buf) == size, f'{name}: the take ended at frame {cur}'
        enc.stdin.write(buf)
    enc.stdin.close(); enc.wait(); dec.stdout.close(); dec.kill(); dec.wait()
    assert enc.returncode == 0
    marks = {}
    for k, m in tk['marks'].items():
        if src[0] <= m <= src[-1]:                         # the film time the marked frame first plays
            marks[k] = next(round((f0 + i) / FPS, 3) for i, s in enumerate(src) if s >= m)
    return {'src': f'assets/shots/{name}.mp4', 'scene': scene, 'take': tk_name, 'start': round(f0 / FPS, 4), 'dur': round(len(src) / FPS, 4),
            'size': list(SIZE), 'frames': [src[0], src[-1]], 'speed': round(fast, 3), 'label': label,
            'marks': marks, 'rects': tk.get('rects', {}), 'scroll': tk.get('scroll'),
            'cursor_fields': tk['mouse_fields'], 'cursor': [tk['mouse'][k] for k in src],
            'keys': [[round(t, 3), f] for t, f in keys]}


if __name__ == '__main__':
    only = sys.argv[1:]
    old = ROOT / 'assets' / 'edit.json'
    edit = json.loads(old.read_text()) if only and old.exists() else {}
    edit.update({'fps': FPS, 'viewport': list(VIEW), 'scale': SIZE[0] / VIEW[0],
                 'note': 'capture/conform.py: shots cut from the live-site takes (assets/rec). cursor and rects in CSS px of the 1600 x 900 viewport; '
                         'cursor entries [x, y, down, visible], one per film frame from start; marks in film seconds.'})
    edit.setdefault('shots', {})
    for name, (tk, a, b, scene, keys) in shots().items():
        if only and name not in only: continue
        s = edit['shots'][name] = conform(name, tk, a, b, scene, keys)
        print(f"{name:9s} film {s['start']:6.2f}-{s['start'] + s['dur']:6.2f} ({s['dur']:.2f} s)  take frames {s['frames'][0]}..{s['frames'][1]}"
              f"  speed {s['speed']:.2f}x{'  label ' + s['label'] if s['label'] else ''}")
        print(f"          marks {s['marks']}")
    (ROOT / 'assets' / 'edit.json').write_text(json.dumps(edit, separators=(',', ':')) + '\n')
    (ROOT / 'assets' / 'edit.js').write_text('// Generated by capture/conform.py.\nwindow.EDIT = ' + json.dumps(edit, separators=(',', ':')) + ';\n')
