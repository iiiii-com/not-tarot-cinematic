/* =====================================================================
   effects.js — sound engine + reusable film-effect builders
   ===================================================================== */

/* ------------------------------------------------------------------ AUDIO */
const Audio = (() => {
  let ctx = null, master = null, comp = null, muted = false, running = false;
  let noise = null, lastT = 0, started = false;

  function ensure() {
    if (ctx) return ctx;
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    ctx = new AC();
    master = ctx.createGain(); master.gain.value = 0.0;
    comp = ctx.createDynamicsCompressor();
    comp.threshold.value = -20; comp.knee.value = 18; comp.ratio.value = 3.4;
    comp.attack.value = 0.004; comp.release.value = 0.22;
    master.connect(comp); comp.connect(ctx.destination);
    // noise buffer
    const len = ctx.sampleRate * 1.2;
    noise = ctx.createBuffer(1, len, ctx.sampleRate);
    const d = noise.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
    return ctx;
  }
  function on() {
    if (!ctx) return;
    const t = ctx.currentTime;
    master.gain.cancelScheduledValues(t);
    master.gain.setTargetAtTime(muted ? 0 : 0.55, t, 0.25);
  }
  function now() { return ctx ? ctx.currentTime : 0; }
  function env(g, t0, a, d, peak) {
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(Math.max(0.0002, peak), t0 + a);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + a + d);
  }
  /* kick / heartbeat */
  function thump(vel = 0.8, freq = 58, dur = 0.55, when) {
    if (!ctx || muted) return;
    const t0 = when != null ? when : now() + 0.01;
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.type = 'sine';
    o.frequency.setValueAtTime(freq * 2.6, t0);
    o.frequency.exponentialRampToValueAtTime(freq, t0 + 0.09);
    o.frequency.exponentialRampToValueAtTime(freq * 0.72, t0 + dur);
    env(g, t0, 0.008, dur, 0.55 * vel);
    o.connect(g); g.connect(master); o.start(t0); o.stop(t0 + dur + 0.1);
  }
  function tick(hi = 1, vel = 0.12, when) {
    if (!ctx || muted) return;
    const t0 = when != null ? when : now() + 0.005;
    const src = ctx.createBufferSource(); src.buffer = noise;
    const f = ctx.createBiquadFilter(); f.type = 'bandpass';
    f.frequency.value = 1800 * hi; f.Q.value = 7;
    const g = ctx.createGain(); env(g, t0, 0.003, 0.05, vel);
    src.connect(f); f.connect(g); g.connect(master);
    src.start(t0); src.stop(t0 + 0.12);
  }
  function whoosh(dur = 0.75, up = 1, vel = 0.16, when) {
    if (!ctx || muted) return;
    const t0 = when != null ? when : now() + 0.01;
    const src = ctx.createBufferSource(); src.buffer = noise;
    const f = ctx.createBiquadFilter(); f.type = 'bandpass'; f.Q.value = 1.2;
    f.frequency.setValueAtTime(up ? 260 : 2400, t0);
    f.frequency.exponentialRampToValueAtTime(up ? 2300 : 240, t0 + dur);
    const g = ctx.createGain(); env(g, t0, dur * 0.42, dur * 0.6, vel);
    src.connect(f); f.connect(g); g.connect(master);
    src.start(t0); src.stop(t0 + dur + 0.1);
  }
  function press(vel = 0.5, when) {
    if (!ctx || muted) return;
    const t0 = when != null ? when : now() + 0.005;
    const src = ctx.createBufferSource(); src.buffer = noise;
    const f = ctx.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = 700; f.Q.value = 1.4;
    const g = ctx.createGain(); env(g, t0, 0.006, 0.16, vel);
    src.connect(f); f.connect(g); g.connect(master);
    src.start(t0); src.stop(t0 + 0.26);
    thump(vel * 0.55, 74, 0.28, t0);
  }
  function chime(root = 523.25, vel = 0.14, when) {
    if (!ctx || muted) return;
    const t0 = when != null ? when : now() + 0.01;
    [1, 1.5, 2.01, 3.02].forEach((m, i) => {
      const o = ctx.createOscillator(), g = ctx.createGain();
      o.type = 'sine'; o.frequency.value = root * m;
      env(g, t0 + i * 0.008, 0.02, 1.5 - i * 0.2, vel / (i + 1.4));
      o.connect(g); g.connect(master); o.start(t0); o.stop(t0 + 2.0);
    });
  }
  /* cue points across the film */
  const CUES = [];
  function cue(t, fn) { CUES.push({ t, fn, hit: false }); }
  /* cold open — proof sheet: press, ink flood, stamp, drain */
  cue(0.03, () => { thump(0.42, 30, 1.7); });
  cue(0.30, () => { whoosh(0.52, 1, 0.10); });
  cue(0.62, () => { tick(1.1, 0.08); });
  cue(0.80, () => { press(0.5); setTimeout(() => tick(2.6, 0.12), 60); });
  cue(1.02, () => { whoosh(0.62, 0, 0.14); });
  cue(1.36, () => { chime(392, 0.045); });
  cue(1.12, () => { thump(1, 52, 0.85); setTimeout(() => tick(0.5, 0.18), 30); });
  [3.35, 4.22, 5.09, 5.96, 6.83, 7.70].forEach(t => cue(t, () => thump(0.85, 56, 0.5)));
  cue(8.0, () => { whoosh(0.9, 0, 0.2); thump(0.6, 44, 1.0); });
  cue(9.0, () => chime(392, 0.08));
  cue(11.2, () => whoosh(0.6, 1, 0.1));
  cue(14.0, () => { thump(0.3, 40, 1.4); });
  cue(17.5, () => whoosh(0.7, 1, 0.12));
  cue(22.0, () => { whoosh(1.5, 0, 0.26); thump(0.9, 36, 2.0); });
  cue(24.5, () => { whoosh(0.6, 1, 0.14); tick(1.4, 0.14); });
  const cardTimes = [25.15, 26.65, 28.15, 29.65, 31.15, 32.65];
  cardTimes.forEach((t, i) => cue(t, () => press(0.42), ) );
  cardTimes.forEach((t, i) => { cue(t, () => tick(1.9 - i * 0.06, 0.1)); });
  cue(33.6, () => chime(523.25, 0.1));
  cue(36.0, () => { whoosh(0.8, 0, 0.16); chime(659.25, 0.07); });
  cue(38.2, () => press(0.3));
  cue(40.0, () => { whoosh(1.1, 0, 0.2); thump(0.7, 40, 1.2); });
  cue(42.0, () => { chime(783.99, 0.16); press(0.35); });
  cue(43.2, () => chime(1046.5, 0.05));

  function start() {
    if (!ensure()) return;
    if (ctx.state === 'suspended') ctx.resume();
    on();
    started = true; running = true;
    lastT = ST.t;
    CUES.forEach(c => { if (c.t < ST.t - 0.02) c.hit = true; });
  }
  function stopAll() { running = false; }
  function pause() { running = false; if (ctx) on(); }
  function update(t) {
    if (!ctx || !running) return;
    if (t < lastT - 0.08) { // seek backwards — re-arm upcoming cues
      CUES.forEach(c => { c.hit = c.t < t - 0.02; });
    }
    lastT = t;
    for (const c of CUES) {
      if (!c.hit && c.t <= t && c.t > t - 0.35) { c.hit = true; try { c.fn(); } catch (e) {} }
      else if (!c.hit && c.t < t) c.hit = true;
    }
  }
  function sfx(name) {
    if (!ctx || muted) return;
    if (name === 'hover') tick(2.4, 0.045);
    else if (name === 'click') tick(1.4, 0.09);
    else if (name === 'flip') { tick(2.0, 0.1); whoosh(0.28, 1, 0.05); }
    else if (name === 'draw') { press(0.4); chime(659.25, 0.06); }
    else if (name === 'drop') thump(0.8, 50, 0.7);
    else if (name === 'slow') { tick(0.8, 0.08); }
  }
  function toggleMute() { muted = !muted; on(); return muted; }
  return { start, pause, stopAll, update, sfx, toggleMute, get muted() { return muted; }, ensure };
})();
window.NT.Audio = Audio;

/* ------------------------------------------------------- effect constructors */
function fxRipple(parent, x, y, size, stroke) {
  const n = mk('div', 'fx-ripple', parent);
  n.style.left = x + 'px'; n.style.top = y + 'px';
  n.style.width = n.style.height = size + 'px';
  if (stroke) n.style.borderColor = stroke;
  return n;
}
function fxStamp(parent, x, y, size, cls) {
  const n = mk('div', 'fx-stamp ' + (cls || ''), parent);
  n.style.left = x + 'px'; n.style.top = y + 'px';
  n.style.width = n.style.height = size + 'px';
  return n;
}
function fxBloom(parent, x, y, size) {
  const n = mk('div', 'fx-bloom', parent);
  n.style.left = x + 'px'; n.style.top = y + 'px';
  n.style.width = n.style.height = size + 'px';
  return n;
}
/* a plate-coloured shutter used for blinks / wipes */
function makeShutter(parent, where) {
  const n = mk('div', 'fx-shutter ' + where, parent);
  paperBg(n, 'cream');
  return n;
}
/* tiny engraved dust motes, deterministic */
const DUST_COLOURS = { berry: '#8F2C3B', bone: '#F7F2E6', gold: '#7B5521', plum: '#241F22' };
function makeDust(parent, count, seed, area, colour) {
  const rnd = mulberry(seed);
  const nodes = [];
  const frag = document.createDocumentFragment();
  const col = DUST_COLOURS[colour || 'berry'] || DUST_COLOURS.berry;
  for (let i = 0; i < count; i++) {
    const n = mk('i', null, null);
    const x = (area ? area.x : 0) + rnd() * (area ? area.w : 1920);
    const y = (area ? area.y : 0) + rnd() * (area ? area.h : 1080);
    const s = 1 + rnd() * 2.4;
    n.style.cssText = 'position:absolute;left:' + x + 'px;top:' + y + 'px;width:' + s + 'px;height:' + s +
      'px;border-radius:50%;background:' + col + ';opacity:' + (0.10 + rnd() * 0.22).toFixed(3) + ';display:block;';
    frag.appendChild(n); nodes.push({ n, x, y, s, p: rnd() * 6.28, sp: 0.2 + rnd() * 0.6 });
  }
  parent.appendChild(frag);
  return nodes;
}
function driftDust(dust, t, amp) {
  for (const d of dust) {
    d.n.style.transform = 'translate(' + (Math.sin(t * d.sp + d.p) * amp).toFixed(2) + 'px,' +
      (Math.cos(t * d.sp * 0.8 + d.p) * amp * 0.7).toFixed(2) + 'px)';
  }
}
/* engraved ruler ticks as a node */
function makeTicks(parent, n, length, gap, thick) {
  const wrap = mk('div', null, parent);
  wrap.style.cssText = 'position:absolute;left:0;top:0;right:0;bottom:0;pointer-events:none;';
  const frag = document.createDocumentFragment();
  for (let i = 0; i < n; i++) {
    const t = mk('i', null, null);
    const len = (i % 5 === 0) ? length : length * 0.55;
    t.style.cssText = 'position:absolute;display:block;width:' + (thick || 1) + 'px;height:' + len +
      'px;background:rgba(36,31,34,.34);left:' + (i * gap) + 'px;top:0;';
    frag.appendChild(t);
  }
  wrap.appendChild(frag);
  return wrap;
}
/* a hairline svg circle-ring with degree ticks */
/* a click leaves one wet ink mark: a soft dot and an irregular halo */
function inkPing(x, y, big) {
  const fx = document.getElementById('fx');
  if (!fx) return;
  const n = mk('div', 'ink-ping', fx);
  n.style.left = x + 'px'; n.style.top = y + 'px';
  if (big) n.classList.add('big');
  n.innerHTML = '<i></i><b></b>';
  setTimeout(() => n.remove(), 1000);
}
/* a paper-coloured wash that lifts the frame for one frame (transition beat) */
function paperFlash(strength) {
  const fx = document.getElementById('fx');
  if (!fx) return;
  const n = mk('div', 'paper-flash', fx);
  n.style.opacity = String(strength == null ? 0.5 : strength);
  setTimeout(() => n.remove(), 420);
}
function ringSvg(parent, cx, cy, radii, ticks, cls) {
  const NS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('class', cls || 's3-ring');
  svg.setAttribute('viewBox', '0 0 1920 1080');
  (radii || []).forEach(r => {
    const c = document.createElementNS(NS, 'circle');
    c.setAttribute('cx', cx); c.setAttribute('cy', cy); c.setAttribute('r', r);
    svg.appendChild(c);
  });
  if (ticks) {
    const total = ticks.n || 72;
    for (let i = 0; i < total; i++) {
      const a = (i / total) * Math.PI * 2 - Math.PI / 2;
      const major = i % (ticks.major || 6) === 0;
      const r0 = ticks.r0, r1 = major ? ticks.r1 : ticks.r1 - (ticks.len || 10);
      const l = document.createElementNS(NS, 'line');
      l.setAttribute('x1', (cx + Math.cos(a) * r0).toFixed(2));
      l.setAttribute('y1', (cy + Math.sin(a) * r0).toFixed(2));
      l.setAttribute('x2', (cx + Math.cos(a) * r1).toFixed(2));
      l.setAttribute('y2', (cy + Math.sin(a) * r1).toFixed(2));
      if (major) l.setAttribute('class', 'deg');
      svg.appendChild(l);
    }
  }
  parent.appendChild(svg);
  return svg;
}
