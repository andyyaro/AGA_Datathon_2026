"""Contact sheets of the conformed shots, with the recorded pointer drawn in, for looking at (snaps/capture-<shot>.jpg).

    <pw-venv>/bin/python -I capture/sheet.py [shot ...]

20 film frames per shot, evenly spaced from its start to its end, 5 x 4, left to right; the times are printed. The
pointer is a dark dot with a white rim where the composition will draw the cursor (a blue ring while the button is
down); it is left out while the take says the cursor is hidden.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
EDIT = json.loads((ROOT / 'assets' / 'edit.json').read_text())
W, H, COLS, ROWS, PAD = 480, 270, 5, 4, 6


def dot(img, x, y, down):
    yy, xx = np.ogrid[:H, :W]
    d = np.hypot(xx - x, yy - y)
    if down: img[(d >= 8) & (d < 10.5)] = (31, 63, 224)
    img[d < 6.5] = (255, 255, 255)
    img[d < 4.5] = (16, 24, 58)


def sheet(name):
    s = EDIT['shots'][name]
    n = len(s['cursor'])
    picks = [round(i * (n - 1) / (COLS * ROWS - 1)) for i in range(COLS * ROWS)]
    sel = '+'.join(f'eq(n\\,{k})' for k in picks)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(ROOT / s['src']), '-vf', f"select='{sel}',scale={W}:{H}:flags=area",
                          '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    assert len(frames) == len(picks), (len(frames), len(picks))
    k = W / EDIT['viewport'][0]
    out = np.full((ROWS * (H + PAD) + PAD, COLS * (W + PAD) + PAD, 3), 200, np.uint8)
    for i, (f, p) in enumerate(zip(frames, picks)):
        img = f.copy()
        x, y, down, vis = s['cursor'][p]
        if vis: dot(img, x * k, y * k, down)
        r, c = divmod(i, COLS)
        out[PAD + r * (H + PAD):PAD + r * (H + PAD) + H, PAD + c * (W + PAD):PAD + c * (W + PAD) + W] = img
    dst = ROOT / 'snaps' / f'capture-{name}.jpg'
    dst.parent.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{out.shape[1]}x{out.shape[0]}', '-i', '-',
                    '-frames:v', '1', '-q:v', '3', str(dst)], input=out.tobytes(), check=True)
    print(f"{dst.relative_to(ROOT)}: film " + ' '.join(f"{s['start'] + p / EDIT['fps']:.2f}" for p in picks))


if __name__ == '__main__':
    for name in sys.argv[1:] or EDIT['shots']:
        sheet(name)
