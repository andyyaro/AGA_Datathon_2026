"""Record the live site frame by frame on the virtual clock (capture/vclock.js), scripted in FILM time.

Adapted from the Outbreak Detective share film's recorder (its capture/rec.py). Changes for this film:
- it records the live site (https://gmufiscalpatriots.bytechisel.com/) directly: the pages are static (S3 +
  CloudFront) and have no Web Workers, so no local server is needed. Read and navigate only: no form is submitted.
  googletagmanager.com / google-analytics.com are blocked (analytics only, never in the picture), and
  localStorage fiscal_guide_dismissed=true keeps the landing page's "New here?" guide card closed;
- a take knows the film time of its first frame (t0), so its actions are written at film times taken from the
  narration's word times (assets/vo.js): s.at(T) records up to film time T. Played at 1x from t0, the take is in
  sync with the voice, so the conform (capture/conform.py) only has to trim it;
- the pointer path keeps a 4th value, 1 while the composition should draw the cursor (it fades in on `cursor_in`);
- moves can curve through a control point (quadratic Bezier), so the real pointer can go round things it should not
  hover (the Tableau iframes, the other chips, the other glossary card);
- typing is spread over a span of frames, one real key per step (the glossary filters on keyup);
- frames are written to the scratch dir, encoded to assets/rec/<take>.mp4 (H.264 CRF 17, yuv420p limited range,
  BT.709, tagged; a keyframe every 10 frames, 3200 x 1800 = the 1600 x 900 CSS viewport at dpr 2), and deleted. assets/rec/<take>.json holds the
  pointer path (CSS px of the viewport, one entry per frame), the marks (frame numbers) and element boxes (CSS px).
"""
import json, math, os, shutil, subprocess, time
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REC = ROOT / 'assets' / 'rec'
WORK = Path(os.environ.get('AMS_WORK', ROOT / 'capture-work'))   # raw frames, deleted after each take
BASE = 'https://gmufiscalpatriots.bytechisel.com/'
VCLOCK = (HERE / 'vclock.js').read_text()
# the screenshots are full-range sRGB JPEGs: convert to limited-range BT.709 and say so, so Chrome (and the HyperFrames
# render) decodes the colours as recorded; untagged full-range yuv would crush the blacks and shift the tier colours
TAGS = ['-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709']

# a soft in-out for a hand moving a mouse or turning a wheel
SINE = lambda p: 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, p)))
# a gentler start, a long settle: for scrolls (cubic in-out, its end stretched)
SCROLL = lambda p: (lambda q: 4 * q ** 3 if q < 0.5 else 1 - (-2 * q + 2) ** 3 / 2)(min(1, max(0, p)))


class Shot:
    def __init__(self, name, t0, w=1600, h=900, dpr=2, fps=30, storage=None, quality=93):
        self.name, self.t0, self.w, self.h, self.dpr, self.fps = name, t0, w, h, dpr, fps
        self.storage = {'fiscal_guide_dismissed': 'true', **(storage or {})}
        self.quality = quality
        self.frames = WORK / name
        self.n = 0
        self.mouse = [w + 40, h * 0.5]
        self.down = False
        self.vis = 0
        self.track = []
        self.marks = {}
        self.meta = {}
        self.log = []

    def __enter__(self):
        shutil.rmtree(self.frames, ignore_errors=True); self.frames.mkdir(parents=True)
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(args=['--hide-scrollbars', '--ignore-gpu-blocklist', '--force-color-profile=srgb'])
        self.ctx = self.browser.new_context(viewport={'width': self.w, 'height': self.h}, device_scale_factor=self.dpr,
                                            color_scheme='light', service_workers='block', locale='en-US')
        self.ctx.route(lambda u: 'googletagmanager.com' in u or 'google-analytics.com' in u, lambda r: r.abort())
        init = ''.join(f'localStorage.setItem({json.dumps(k)}, {json.dumps(v)});' for k, v in self.storage.items())
        self.ctx.add_init_script(f'try {{ if (window.top === window) {{ {init} }} }} catch (e) {{}}')
        self.ctx.add_init_script(VCLOCK)
        self.page = self.ctx.new_page()
        self.page.on('console', lambda m: m.type == 'error' and self.log.append(f'{m.type}: {m.text[:160]}'))
        self.page.on('pageerror', lambda e: self.log.append(f'pageerror: {str(e)[:160]}'))
        return self

    def __exit__(self, *exc):
        self.browser.close(); self.pw.stop()

    # ---- setup, in real time ----
    def goto(self, path, wait='load'):
        self.page.goto(BASE + path, wait_until=wait, timeout=90000)

    def idle(self, seconds):
        """Wait in real time while Playwright keeps hearing the page (frames, console)."""
        self.page.wait_for_timeout(seconds * 1000)

    def park(self, x, y):
        """Put the real pointer somewhere harmless before the clock starts (nothing hovered by accident)."""
        self.mouse = [x, y]; self.page.mouse.move(x, y)

    def scroll_to(self, top):
        self.page.evaluate('(t) => window.scrollTo({ top: t, left: 0, behavior: "instant" })', top)

    def tableau_ready(self, timeout=120):
        """Wait until every public.tableau.com /views/ iframe has painted its viz (canvas or image tiles)."""
        t0 = time.time()
        while time.time() - t0 < timeout:
            frames = [f for f in self.page.frames if 'public.tableau.com' in f.url and '/views/' in f.url]
            ok = bool(frames)
            for f in frames:
                try:
                    c = f.evaluate("document.querySelectorAll('canvas').length + document.querySelectorAll('.tvimagesContainer img, .tab-tvView img').length")
                except Exception:
                    c = 0
                if c <= 0: ok = False
            if ok: return round(time.time() - t0, 1), len(frames)
            self.page.wait_for_timeout(500)            # (not time.sleep: Playwright only learns of new frames while it waits)
        raise RuntimeError('the Tableau views did not paint')

    def start(self):
        self.page.evaluate('__vt.start()')
        self.wall = time.time()

    # ---- recording, in film time ----
    def T(self, n=None):
        """The film time of frame n (default: the next frame to be recorded)."""
        return self.t0 + (self.n if n is None else n) / self.fps

    def F(self, t):
        """The frame number that plays at film time t."""
        return round((t - self.t0) * self.fps)

    def frame(self, n=1):
        for _ in range(n):
            self.page.evaluate(f'__vt.advance({1000 / self.fps})')
            self.page.screenshot(path=str(self.frames / f'{self.n:05d}.jpg'), type='jpeg', quality=self.quality)
            self.track.append([round(self.mouse[0], 2), round(self.mouse[1], 2), int(self.down), self.vis])
            self.n += 1

    def at(self, t):
        """Record until film time t (the next frame recorded is the one that plays at t)."""
        k = self.F(t) - self.n
        if k < 0: print(f'  {self.name}: {-k} frames late for {t:.3f}')
        self.frame(max(0, k))

    def mark(self, key):
        """Name the next frame (the composition reads these as film times, e.g. the frame a click lands on)."""
        self.marks[key] = self.n

    def show(self, on=True):
        self.vis = int(on)
        if on: self.mark('cursor_in')

    def move(self, x, y, t1, via=None, ease=SINE, steps=4):
        """Move the pointer to (x, y), arriving at film time t1, eased; through the control point `via` if given.
        The page gets several real mouse moves per frame."""
        (x0, y0), n = self.mouse, max(1, self.F(t1) - self.n)
        cx, cy = via or ((x0 + x) / 2, (y0 + y) / 2)
        P = lambda p: ((1 - p) ** 2 * x0 + 2 * p * (1 - p) * cx + p * p * x, (1 - p) ** 2 * y0 + 2 * p * (1 - p) * cy + p * p * y)
        for i in range(1, n + 1):
            for k in range(1, steps + 1):
                self.page.mouse.move(*P(ease((i - 1 + k / steps) / n)))
            self.mouse = list(P(ease(i / n)))
            self.frame()

    def press(self):
        self.page.mouse.move(*self.mouse); self.page.mouse.down(); self.down = True

    def release(self):
        self.page.mouse.up(); self.down = False

    def click(self, hold=3):
        self.mark('click'); self.press(); self.frame(hold); self.release()

    def type_text(self, text, t1):
        """Type `text` one real key at a time, the keys spread evenly up to film time t1."""
        n = max(len(text), self.F(t1) - self.n)
        due = [round((i + 1) * n / len(text)) for i in range(len(text))]
        done = 0
        for i in range(1, n + 1):
            while done < len(text) and due[done] <= i:
                self.page.keyboard.type(text[done]); done += 1
            self.frame()

    def scroll(self, top, t1, ease=SCROLL):
        """Scroll the window to `top`, eased, arriving at film time t1."""
        y0 = self.page.evaluate('scrollY')
        n = max(1, self.F(t1) - self.n)
        for i in range(1, n + 1):
            self.scroll_to(y0 + (top - y0) * ease(i / n))
            self.frame()

    def box(self, sel):
        b = self.page.locator(sel).first.bounding_box()
        return b['x'] + b['width'] / 2, b['y'] + b['height'] / 2, b

    def rect(self, key, sel):
        """Keep an element's box (CSS px of the viewport, now) in the take's metadata, e.g. for a push-in."""
        b = self.page.locator(sel).first.bounding_box()
        self.meta.setdefault('rects', {})[key] = [round(b[k], 1) for k in ('x', 'y', 'width', 'height')]
        return b

    def encode(self, crf=17, keep=False):
        REC.mkdir(parents=True, exist_ok=True)
        out = REC / f'{self.name}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(self.fps), '-i', str(self.frames / '%05d.jpg'),
                        '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', *TAGS,
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', str(crf), '-pix_fmt', 'yuv420p', '-g', '10', '-bf', '0',
                        '-movflags', '+faststart', str(out)], check=True)
        meta = {'name': self.name, 'fps': self.fps, 'frames': self.n, 't0': self.t0, 'viewport': [self.w, self.h], 'dpr': self.dpr,
                'url': BASE, 'recorded': time.strftime('%Y-%m-%d %H:%M'), 'marks': self.marks, **self.meta,
                'mouse_fields': ['x', 'y', 'down', 'visible'], 'mouse': self.track}
        (REC / f'{self.name}.json').write_text(json.dumps(meta, separators=(',', ':')) + '\n')
        took = time.time() - self.wall
        print(f'{self.name}: {self.n} frames ({self.n / self.fps:.2f} s, film {self.t0:.3f}-{self.T():.3f}) in {took:.0f} s -> {out.relative_to(ROOT)}'
              f' ({out.stat().st_size / 1e6:.1f} MB)')
        for l in self.log[:12]: print('  ', l)
        if not keep: shutil.rmtree(self.frames, ignore_errors=True)
        return out
