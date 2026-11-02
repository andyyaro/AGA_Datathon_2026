/* A virtual clock for recording a live page frame by frame (loaded with addInitScript, before the page's own code).

   Until __vt.start() the page runs in real time, so setup (loading, clicking into a state) behaves normally.
   After it, time only moves when the recorder calls __vt.advance(ms):
   - Web Workers whose script starts with vclock-worker.js (capture/serve.py adds it) are stepped first, and awaited,
     so physics and paced computations in workers keep the page's time;
   - setTimeout / setInterval fire in order as virtual time passes their due time (a timer set inside a timer waits at
     least 4 ms, as browsers clamp nested timers, so self-rescheduling loops still let time pass);
   - requestAnimationFrame callbacks wait for the next advance, and get the virtual time;
   - performance.now, Date and Date.now read the virtual time. While code runs (from its first clock read to the next
     microtask checkpoint) the clock moves with real time, so a "work until 12 ms have passed" loop ends. Each stretch
     starts again from the frame's time, so the page's frames stay exactly one step apart;
   - CSS animations and transitions (the Web Animations API) are paused and set to the virtual time;
   - <video> elements that are "playing" are paused and seeked by the same step, then awaited.
   So every recorded frame is exactly 1/fps apart, however long a screenshot takes.

   AuditsMadeSimple film: copied from the Outbreak Detective share film (its capture/vclock.js).
   The one change: it installs itself in the top frame only. The live site embeds the team's Tableau dashboards as
   cross-origin iframes from public.tableau.com; they keep the real clock (they are painted and still before the
   virtual clock starts, and nothing in them moves while a take records). The site has no Web Workers, so the
   share film's vclock-worker.js and its local server are not needed. */
(() => {
  if (window.top !== window) return;   // the top frame only: the Tableau iframes keep real time
  const W = window;
  { let a = 0x5eed1978; Math.random = () => { a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }   // seeded (mulberry32)
  const rPerf = performance.now.bind(performance), rDateNow = Date.now, RDate = Date;
  const rRAF = W.requestAnimationFrame.bind(W), rCAF = W.cancelAnimationFrame.bind(W);
  const rST = W.setTimeout.bind(W), rCT = W.clearTimeout.bind(W), rSI = W.setInterval.bind(W), rCI = W.clearInterval.bind(W);
  const mPlay = HTMLMediaElement.prototype.play, mPause = HTMLMediaElement.prototype.pause;
  const pausedGet = Object.getOwnPropertyDescriptor(HTMLMediaElement.prototype, 'paused').get;
  let on = false, vnow = 0, dateAt = 0, id = 1e9, seq = 0, seg = 0, inTimer = 0;
  let raf = new Map();
  const timers = new Map();
  const anims = new WeakMap();                       // Animation -> [its time when first seen, virtual time then]
  const playing = new Set();
  const RWorker = W.Worker, clocked = new Set(), acks = new Map(), stats = { hello: 0, posted: 0, acked: 0, late: 0 };

  W.Worker = class extends RWorker {
    constructor(...a) {
      super(...a);
      // registered before the page sets onmessage, so the clock's own messages never reach the page
      this.addEventListener('message', (ev) => {
        const m = ev.data;
        if (!m || !m.__vt) return;
        ev.stopImmediatePropagation();
        if (m.__vt === 'hello') { stats.hello++; clocked.add(this); if (on) this.postMessage({ __vt: 'start', n: 0 }); }
        if (m.__vt === 'ack') { stats.acked++; const r = acks.get(m.n); if (r) { acks.delete(m.n); r(); } else stats.late++; }
      });
    }
  };
  const tellWorkers = (msg) => Promise.all([...clocked].map((w) => new Promise((res) => {
    const n = ++seq; acks.set(n, res); w.postMessage({ ...msg, n }); stats.posted++;
    rST(() => { if (acks.delete(n)) { console.warn('vclock: a worker did not answer'); res(); } }, 20000);
  })));

  // share-film: as in vclock-worker.js, each clock read while code runs costs EPS ms, counted rather than measured
  const EPS = 0.028;
  let reads = 0;
  const close = () => { seg = 0; reads = 0; };
  const vt = () => { if (!seg) { seg = 1; queueMicrotask(close); } reads++; return vnow + reads * EPS; };
  const delay = (ms) => Math.max(inTimer ? 4 : 0, +ms || 0);
  const call = (timer, fn, ...a) => { close(); inTimer = timer; try { fn(...a); } catch (e) { console.error(e); } finally { inTimer = 0; close(); } };
  performance.now = () => (on ? vt() : rPerf());
  const now = () => (on ? Math.floor(dateAt + vt()) : rDateNow());
  class VDate extends RDate { constructor(...a) { if (a.length) super(...a); else super(now()); } static now() { return now(); } }
  W.Date = VDate;
  W.requestAnimationFrame = (cb) => { if (!on) return rRAF(cb); raf.set(++id, cb); return id; };
  W.cancelAnimationFrame = (k) => { if (!raf.delete(k)) rCAF(k); };
  W.setTimeout = (fn, ms = 0, ...a) => { if (!on || typeof fn !== 'function') return rST(fn, ms, ...a); timers.set(++id, { at: vt() + delay(ms), fn, a }); return id; };
  W.setInterval = (fn, ms = 0, ...a) => { if (!on || typeof fn !== 'function') return rSI(fn, ms, ...a); const e = Math.max(4, +ms || 0); timers.set(++id, { at: vt() + e, fn, a, e }); return id; };
  W.clearTimeout = (k) => { if (!timers.delete(k)) rCT(k); };
  W.clearInterval = (k) => { if (!timers.delete(k)) rCI(k); };

  HTMLMediaElement.prototype.play = function () {
    if (!on) return mPlay.call(this);
    playing.add(this); this.dispatchEvent(new Event('play')); this.dispatchEvent(new Event('playing'));
    return Promise.resolve();
  };
  HTMLMediaElement.prototype.pause = function () {
    if (playing.delete(this)) this.dispatchEvent(new Event('pause'));
    return mPause.call(this);
  };
  Object.defineProperty(HTMLMediaElement.prototype, 'paused', { configurable: true, get() { return playing.has(this) ? false : pausedGet.call(this); } });

  const syncAnimations = (prev) => {
    for (const a of document.getAnimations()) {
      let s = anims.get(a);
      if (!s) { s = [a.playState === 'running' ? 0 : a.currentTime ?? 0, prev]; anims.set(a, s); }   // new since the last frame: it began then
      if (a.playState === 'running') a.pause();
      a.currentTime = s[0] + (vnow - s[1]) * (a.playbackRate || 1);
    }
  };
  const seeked = (v) => new Promise((res) => { if (!v.seeking) return res(); const t = rST(res, 3000); v.addEventListener('seeked', () => { rCT(t); res(); }, { once: true }); });

  W.__vt = {
    async start() {
      if (on) return;
      vnow = rPerf(); dateAt = rDateNow() - vnow; on = true;
      for (const a of document.getAnimations()) { anims.set(a, [a.currentTime ?? 0, vnow]); if (a.playState === 'running') a.pause(); }
      for (const v of document.querySelectorAll('video')) if (!pausedGet.call(v)) { mPause.call(v); playing.add(v); }
      await tellWorkers({ __vt: 'start' });
    },
    async advance(ms) {
      await tellWorkers({ __vt: 'advance', ms });
      close();
      const prev = vnow, to = vnow + ms;
      for (;;) {
        let k = null, t = null;
        for (const [i, x] of timers) if (x.at <= to && (!t || x.at < t.at)) { k = i; t = x; }
        if (!t) break;
        vnow = Math.max(vnow, t.at);
        if (t.e) t.at += t.e; else timers.delete(k);
        call(1, t.fn, ...t.a);
      }
      vnow = to;
      const q = raf; raf = new Map();
      for (const cb of q.values()) call(0, cb, vnow);
      await Promise.resolve();
      syncAnimations(prev);
      const waits = [];
      for (const v of playing) {
        if (!v.isConnected) { playing.delete(v); continue; }
        const t = Math.min(v.duration || Infinity, v.currentTime + ms / 1000);
        v.currentTime = t; v.dispatchEvent(new Event('timeupdate'));
        if (v.duration && t >= v.duration - 1e-3) { playing.delete(v); v.dispatchEvent(new Event('ended')); }
        waits.push(seeked(v));
      }
      await Promise.all(waits);
      await new Promise((r) => rRAF(() => rRAF(r)));   // let the browser lay out and paint this frame
      return vnow;
    },
    get now() { return vnow; },
    get on() { return on; },
    get workers() { return clocked.size; },
    stats,
  };
})();
