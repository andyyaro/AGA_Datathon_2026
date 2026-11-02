"""The film's three recorded takes, from the live site (SPEC.md SHOTS s3 to s5). One function per take.

    <pw-venv>/bin/python -I capture/takes.py explore glossary score      # or: all

Each take is scripted in film time: its actions sit on the narration's word times (assets/vo.js, the same words the
scenes find with W()), and it records from about half a second before its scene to most of a second after, so it
plays at 1x. Before the clock starts, each page is loaded and set up in real time (the Tableau views are awaited).

  explore   s3 21.031-29.691  landing page: the hero, then on "money" an eased scroll to Part 1 "Funding by State";
                              the pointer comes in and rests on the active chip "Top 10 States (50.9%)" (no click:
                              a chip click reloads the Tableau view). The ten gold bars stay in frame for the push-in
                              on "Ten states".
  glossary  s4 29.691-37.113  glossary.html: the pointer clicks the search field and types "material weakness" (two
                              cards remain), moves out left of the category chips, the page scrolls the results up,
                              and the pointer enters the Material Weakness card, which flips on "plain words".
  score     s5 37.113-47.010  audit_health_score_casestudy.html at the simulator: the pointer grabs the knob and drags
                              risk 10 -> 30 (90 Low -> 70 Medium) before "one number", lets go; on "Red" it drags on
                              to 75 (25 High) and lets go.
"""
import json, re, subprocess, sys, time
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))   # run with python -I: our own capture/ folder only
from rec import Shot, ROOT, SINE

VO = json.loads(re.search(r'\{.*\}', (ROOT / 'assets' / 'vo.js').read_text(), re.S).group(0))
TM = json.loads((ROOT / 'sound' / 'timing.json').read_text())
norm = lambda w: re.sub(r"[^a-z0-9$.']", '', w.lower()).strip('.')


def W(line, word, nth=0, end=False):
    """Film time of a word in a narration line (its start, or its end)."""
    hits = [x for x in VO[line]['words'] if norm(x['w']) == norm(word)]
    return hits[nth]['t1' if end else 't0']


TAKES = {}
take = lambda f: TAKES.setdefault(f.__name__, f)


def gold_bars(s, n):
    """The ten gold bars of the Tableau bar chart, found by colour in recorded frame n (CSS px of the viewport)."""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(s.frames / f'{n:05d}.jpg'), '-vf', f'scale={s.w}:{s.h}:flags=area',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(s.h, s.w, 3).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (abs(r - 179) < 22) & (abs(g - 164) < 22) & (abs(b - 126) < 26) & (r - b > 35)
    ys, xs = np.nonzero(m)
    if len(xs) < 500: return None
    return [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


@take
def explore():
    S3 = TM['s3']
    with Shot('explore', t0=round(S3[0] - 0.5, 3)) as s:
        s.goto('')
        print('  tableau', s.tableau_ready())
        s.idle(2.5)
        s.scroll_to(0); s.park(1410, 330)             # the gap right of the hero: nothing to hover there
        card = s.page.evaluate("document.querySelector('article.exploreSlide[data-slide=\"1\"]:not([data-clone])').getBoundingClientRect().top + scrollY")
        top = round(card - 110)                        # Part 1's card 110 px below the top (under the 77 px bar)
        s.meta['scroll'] = top
        s.start()
        s.at(W('v06', 'money') + 0.01)
        s.mark('scroll0'); s.scroll(top, W('v06', 'dashboards') + 0.03); s.mark('scroll1')
        s.rect('card', 'article.exploreSlide[data-slide="1"]:not([data-clone])')
        s.rect('chip', 'button.chip[data-viz="top10States"]')
        s.rect('chart', 'article.exploreSlide[data-slide="1"]:not([data-clone]) iframe')
        s.rect('tip', '#aTip')
        cx, cy, b = s.box('button.chip[data-viz="top10States"]')
        s.show()                                       # the pointer fades in as the page comes to rest
        s.at(s.T() + 0.07)
        # over the chips' row, never down into the chart (the Tableau view has its own hover tooltips)
        # the tip comes to rest under the chip's "(50.9%)", so the drawn arrow hangs below the label instead of over it
        s.move(cx + 75, cy + 11, W('v06', 'goes') - 0.05, via=(cx + 240, b['y'] - 52))
        s.mark('rest')
        s.at(W('v07', 'ten'))
        s.mark('ten')
        s.at(S3[1] + 0.8)
        s.meta.setdefault('rects', {})['bars'] = gold_bars(s, s.marks['ten'])
        s.encode()


@take
def glossary():
    S4 = TM['s4']
    with Shot('glossary', t0=round(S4[0] - 0.5, 3)) as s:
        s.goto('glossary.html')
        s.page.wait_for_function("document.querySelectorAll('.term-card').length >= 12", timeout=30000)
        s.idle(1.5)
        s.scroll_to(0); s.park(1310, 520)              # right of the chips, above the cards
        s.rect('search0', '#glossarySearch')
        fx, fy, fb = s.box('#glossarySearch')
        s.start()
        s.at(S4[0] + 0.15); s.show()
        s.at(S4[0] + 0.25)
        # above the category chips' first row (y 430-470, x 440-1160) all the way
        s.move(fb['x'] + fb['width'] * 0.66, fy + 1, W('v08', 'on') - 0.05, via=(1240, 395))
        s.click()                                      # focus: the field's border turns the site's accent
        s.at(W('v08', 'on') + 0.2); s.mark('type0')
        s.type_text('material weakness', W('v08', 'weakness', end=True) + 0.05); s.mark('type1')
        s.meta['cards_after_search'] = s.page.evaluate("[...document.querySelectorAll('.term-card')].filter(c => c.offsetParent).map(c => c.querySelector('.term-card-front').innerText.split('\\n')[0])")
        s.at(s.T() + 0.12)
        # out to the left of the category chips (none starts left of x 440), at the field's height
        s.move(fb['x'] - 6, fy + 16, s.T() + 0.55, via=(fb['x'] + 200, fy + 6))
        s.at(s.T() + 0.05)
        down = 116                                     # the results up into the middle of the frame
        s.mark('scroll0'); s.scroll(down, s.T() + 0.6); s.mark('scroll1')
        s.meta['scroll'] = down
        s.rect('card', '.term-card >> visible=true')
        s.rect('search', '#glossarySearch')
        s.meta['rects']['cards'] = [s.meta['rects']['card'][0], s.meta['rects']['card'][1],
                                    s.page.evaluate("(() => { const c = [...document.querySelectorAll('.term-card')].filter(c => c.offsetParent); const b = c[c.length - 1].getBoundingClientRect(); return b.right; })()") - s.meta['rects']['card'][0],
                                    s.meta['rects']['card'][3]]
        cx, cy, cb = s.box('.term-card >> visible=true')
        # into the Material Weakness card from above its right half; it flips as the pointer crosses its top edge, and
        # the pointer comes to rest below the card's last line, so the drawn arrow never covers the definition
        enter = W('v08', 'plain') - 0.32
        tx, ty = cb['x'] + 204, cb['y'] + cb['height'] - 26
        t_arrive = enter + 0.5
        s.at(t_arrive - 0.8)
        flip = None
        x0, y0 = s.mouse
        n = s.F(t_arrive) - s.n
        for i in range(1, n + 1):
            p = SINE(i / n)
            for k in range(1, 5):
                q = SINE((i - 1 + k / 4) / n)
                s.page.mouse.move(x0 + (tx - x0) * q, y0 + (ty - y0) * q)
            s.mouse = [x0 + (tx - x0) * p, y0 + (ty - y0) * p]
            if flip is None and s.mouse[1] >= cb['y']:
                flip = s.n; s.mark('flip')
            s.frame()
        s.mark('rest')
        s.at(S4[1] + 0.8)
        print(f"  flip starts at film {s.T(flip):.2f} (plain {W('v08', 'plain'):.2f}, words {W('v08', 'words'):.2f}); cards: {s.meta['cards_after_search']}")
        s.encode()


@take
def score():
    S5 = TM['s5']
    with Shot('score', t0=round(S5[0] - 0.5, 3)) as s:
        s.goto('audit_health_score_casestudy.html')
        s.page.wait_for_selector('#riskSlider'); s.idle(1.5)
        s.scroll_to(280); s.park(1300, 640)            # the simulator and the "screening signal" note in frame
        s.meta['scroll'] = 280
        for k, sel in [('sim', '.simulator-card'), ('slider', '#riskSlider'), ('circle', '#scoreCircle'), ('tier', '#tierOutput'),
                       ('display', '.sim-display'), ('note', 'article.content-container > p')]:
            s.rect(k, sel)
        mono = s.page.evaluate("document.querySelector('div[style*=\"monospace\"]').getBoundingClientRect().top")
        assert mono > s.h + 400, mono                  # the monospace "Core calculation" block is far below the frame
        sl = s.meta['rects']['slider']
        knob = lambda v: (sl[0] + 14 + (sl[2] - 28) * v / 150, sl[1] + sl[3] / 2)
        state = lambda: s.page.evaluate("[document.getElementById('riskValueDisplay').textContent, document.getElementById('scoreOutput').textContent, document.getElementById('tierOutput').textContent]")
        tier_marks = {'Medium': 'yellow', 'High': 'red'}

        def drag(v0, v1, t1):
            (x0, y), (x1, _) = knob(v0), knob(v1)
            n = s.F(t1) - s.n
            for i in range(1, n + 1):
                for k in range(1, 5):
                    s.page.mouse.move(x0 + (x1 - x0) * SINE((i - 1 + k / 4) / n), y)
                s.mouse = [x0 + (x1 - x0) * SINE(i / n), y]
                tier = state()[2]
                if tier in tier_marks and tier_marks[tier] not in s.marks: s.mark(tier_marks[tier])
                s.frame()
            s.page.evaluate("(v) => { const e = document.getElementById('riskSlider'); if (+e.value !== v) { e.value = v; e.dispatchEvent(new Event('input', { bubbles: true })); } }", v1)

        s.start()
        s.at(S5[0] + 0.3); s.show()
        s.at(S5[0] + 0.4)
        s.move(*knob(10), W('v09', 'score') + 0.3, via=(knob(10)[0] + 260, knob(10)[1] + 150))
        s.at(W('v09', 'score') + 0.33); s.mark('grab1'); s.press()
        s.at(W('v09', 'score') + 0.46)
        drag(10, 30, W('v09', 'one') - 0.18)
        s.meta['state_at_30'] = state()
        s.at(W('v09', 'one') - 0.1); s.mark('release1'); s.release()
        s.at(W('v10', 'red') - 0.3); s.mark('grab2'); s.press()
        s.at(W('v10', 'red') - 0.2)
        drag(30, 75, W('v10', 'red') + 0.85)
        s.meta['state_at_75'] = state()
        s.at(s.T() + 0.1); s.mark('release2'); s.release()
        s.at(S5[1] + 0.7)
        print(f"  yellow at film {s.T(s.marks.get('yellow', 0)):.2f}, red at film {s.T(s.marks.get('red', 0)):.2f} (Red {W('v10', 'red'):.2f});"
              f" states {s.meta['state_at_30']} {s.meta['state_at_75']}")
        s.encode()


if __name__ == '__main__':
    names = list(TAKES) if sys.argv[1:] == ['all'] else sys.argv[1:]
    for n in names:
        TAKES[n]()
