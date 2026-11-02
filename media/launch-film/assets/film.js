// Shared by s1-open and s2-lockup (loaded once by index.html, like vo.js and timing.js).
// The hook's 858 dots (one per $10 billion of the $8.58 trillion, FACTS #1-2) in a sunflower field, and where each one
// lands on the mark when they stream onto it over the riser. Deterministic (seeded), so s1's last frame and s2's
// first frame put every dot in the same place.
(function () {
  const rng = (seed) => () => {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };

  // the field (s1): right of the copy column
  const N = 858, FX = 1340, FY = 540, SP = 12.4, R = 6, PHI = Math.PI * (3 - Math.sqrt(5));

  // the lockup (s2), in the brand lockup's own proportions (lockup-color.svg: mark 168 at y 72, a 36 gap, the
  // wordmark 344 x 110.72 at y 100.906), centred, the mark 280 px
  const MS = 280, k = MS / 168;
  const WW = 344 * k, WH = 110.72 * k, GAP = 36 * k;
  const LX = Math.round((1920 - (MS + GAP + WW)) / 2), MY = 318;
  const lockup = { mark: [LX, MY, MS], word: [LX + MS + GAP, MY + (100.906 - 72) * k, WW, WH] };

  // the mark's two stroked paths (120 viewBox): the A (stroke 18) and the check (stroke 12)
  const A = [[20, 104], [60, 16], [100, 104]], C = [[34, 70], [51, 86], [94, 44]];
  const len = (P) => { let s = 0; for (let i = 1; i < P.length; i++) s += Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); return s; };
  const at = (P, p) => {                       // point and unit normal at fraction p of the polyline
    let d = p * len(P);
    for (let i = 1; i < P.length; i++) {
      const [x0, y0] = P[i - 1], [x1, y1] = P[i], l = Math.hypot(x1 - x0, y1 - y0);
      if (d <= l || i === P.length - 1) { const u = Math.min(1, d / l); return [x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, -(y1 - y0) / l, (x1 - x0) / l]; }
      d -= l;
    }
  };
  const LA = len(A), LC = len(C), NC = Math.round(N * LC / (LA + LC));
  const unit = MS / 120, rUnits = R / unit;

  // targets: evenly spread along each path (with a little seeded jitter), across the stroke's width
  const rand = rng(858), targets = [];
  for (let i = 0; i < N; i++) {
    const onC = i >= N - NC, P = onC ? C : A, n = onC ? NC : N - NC, j = onC ? i - (N - NC) : i;
    const p = Math.min(1, Math.max(0, (j + 0.5 + (rand() - 0.5) * 0.8) / n));
    const half = (onC ? 6 : 9) - rUnits;
    const off = (rand() * 2 - 1) * half;
    const [x, y, nx, ny] = at(P, p);
    targets.push({ x: LX + (x + nx * off) * unit, y: MY + (y + ny * off) * unit, c: onC ? 1 : 0, p });
  }

  // the field's dots: bloom order from the centre out (jittered), as in the Outbreak open
  const rb = rng(2024), dots = [];
  for (let n = 0; n < N; n++) {
    const rr = SP * Math.sqrt(n + 0.5), th = n * PHI;
    dots.push({ fx: FX + rr * Math.cos(th), fy: FY + rr * Math.sin(th), bloom: rr * (0.7 + 0.6 * rb()) });
  }
  const bl = dots.map((d, i) => i).sort((a, b) => dots[a].bloom - dots[b].bloom);
  bl.forEach((i, r) => (dots[i].bloom = r / (N - 1)));

  // pair dots with targets so the stream flows one way and never crosses itself: both sorted top to bottom, then in
  // bands of 26, each band left to right
  const byY = (arr, key) => arr.map((o, i) => i).sort((a, b) => arr[a][key] - arr[b][key]);
  const dY = byY(dots, "fy"), tY = byY(targets, "y"), B = 26;
  for (let s = 0; s < N; s += B) {
    const db = dY.slice(s, s + B).sort((a, b) => dots[a].fx - dots[b].fx);
    const tb = tY.slice(s, s + B).sort((a, b) => targets[a].x - targets[b].x);
    db.forEach((di, q) => { const t = targets[tb[q]]; Object.assign(dots[di], { tx: t.x, ty: t.y, c: t.c, p: t.p }); });
  }
  // departure: the dots nearest the mark (left-most) leave first
  const dx = dots.map((d, i) => i).sort((a, b) => dots[a].fx - dots[b].fx);
  dx.forEach((i, r) => (dots[i].dep = r / (N - 1)));

  window.FILM = { N, R, field: { x: FX, y: FY, r: SP * Math.sqrt(N) }, lockup, dots,
    blue: "#1F3FE0", coral: "#FF5A3C", navy: "#10183A" };
})();
