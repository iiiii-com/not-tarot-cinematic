/* =====================================================================
   core.js — one concatenated scope. Utilities, stage, render clock.
   ===================================================================== */
;(() => {
'use strict';

/* ------------------------------------------------------------------ query */
const Q = new URLSearchParams(location.search);
const CAPTURE = Q.get('capture') === '1';
const VERTICAL = Q.get('vertical') === '1';
const FIXED_T = Q.has('t') ? Math.max(0, Math.min(45, parseFloat(Q.get('t')) || 0)) : null;
const REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const DUR = 45.0;

const A = window.A || {};
const TX = window.TX || {};

/* -------------------------------------------------------------------- dom */
const $ = s => document.querySelector(s);
const $$ = s => Array.from(document.querySelectorAll(s));
const stage = $('#stage');
const artEl = $('#art');
const scenesEl = $('#scenes');
const fxEl = $('#fx');
const paperA = $('#paperA'), paperB = $('#paperB'), paperTone = $('#paperTone');
const chrome = $('#chrome');
const hdC = $('#hdC'), hdR = $('#hdR'), ftL = $('#ftL');
const capN = $('#capN'), capT = $('#capT');
const grainEls = $$('#grain i');
const plateEl = $('#plateShadow'), vignetteEl = $('#vignette');
if (TX.plate) plateEl.style.backgroundImage = 'url("' + TX.plate + '")';
if (TX.vignette) vignetteEl.style.backgroundImage = 'url("' + TX.vignette + '")';
const hudEl = $('#hud'), hudFill = $('#hudFill'), hudDot = $('#hudDot');
const hudTip = $('#hudTip'), hudClock = $('#hudClock'), hudAct = $('#hudAct');
const posterEl = $('#poster');
const chaptersEl = $('#chapters');
const holdRing = $('#holdRing');
const toastEl = $('#toast');
const cursorEl = $('#cursor');

/* ------------------------------------------------------------------- math */
const clamp = (v, a, b) => v < a ? a : v > b ? b : v;
const clamp01 = v => v < 0 ? 0 : v > 1 ? 1 : v;
const lerp = (a, b, k) => a + (b - a) * k;
const wt = (t, a, b) => clamp01(b <= a ? (t >= b ? 1 : 0) : (t - a) / (b - a));
const E = {
  in: k => k * k,
  out: k => 1 - (1 - k) * (1 - k),
  outC: k => 1 - Math.pow(1 - k, 3),
  outQ: k => 1 - Math.pow(1 - k, 4),
  inC: k => k * k * k,
  inOut: k => k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2,
  outExpo: k => k >= 1 ? 1 : 1 - Math.pow(2, -10 * k),
  outBack: k => { const c = 1.70158, c3 = c + 1; return 1 + c3 * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); },
  soft: k => k * k * (3 - 2 * k),
};
// progress of an event that starts at `at`, lasts `d`
const ev = (t, at, d, e) => (e || E.outC)(wt(t, at, at + d));

function mulberry(seed) {
  let s = seed >>> 0;
  return () => {
    s += 0x6D2B79F5; let z = s;
    z = Math.imul(z ^ (z >>> 15), z | 1);
    z ^= z + Math.imul(z ^ (z >>> 7), z | 61);
    return ((z ^ (z >>> 14)) >>> 0) / 4294967296;
  };
}

/* ------------------------------------------------------------------- dom helpers */
function mk(tag, cls, parent, html) {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (html != null) n.innerHTML = html;
  if (parent) parent.appendChild(n);
  return n;
}
function url(name, tint) { return A[name + '_' + (tint || 'berry')] || A[name + '_berry'] || ''; }
function bg(node, name, tint) { node.style.backgroundImage = 'url("' + url(name, tint) + '")'; return node; }
function mkSym(parent, name, tint, size, x, y, cls) {
  const n = mk('div', 'sym ' + (cls || ''), parent);
  bg(n, name, tint);
  if (size) { n.style.width = n.style.height = size + 'px'; }
  if (x != null) { n.style.left = x + 'px'; n.style.top = y + 'px'; n.style.transform = 'translate(-50%,-50%)'; }
  return n;
}
function paperBg(node, key) { node.style.backgroundImage = 'url("' + TX['paper_' + key] + '")'; }
function setX(node, x) { node.style.transform = 'translate(' + x + 'px,0)'; }

/* ------------------------------------------------------------ scene framework */
const T = [[0, 2.6], [2.6, 8.0], [8.0, 14.0], [14.0, 17.5], [17.5, 22.0], [22.0, 24.5],
           [24.5, 33.5], [33.5, 36.0], [36.0, 40.0], [40.0, 42.0], [42.0, 45.0]];
const SCENES = [];
function scene(t0, t1, build) {
  const node = mk('div', 'scene', scenesEl);
  const ctx = { node, t0, t1, kids: {}, upd: null, cam: null, build };
  SCENES.push(ctx);
  return ctx;
}

/* ------------------------------------------------------------- plate metadata */
const PLATES = [
  { t: 0.0,  roman: 'I',   title: '心',  cap: '一滴墨，在听自己的脉搏。', fig: 'FIG. 1 — GUTTA' },
  { t: 8.0,  roman: 'II',  title: '符号',  cap: '万物皆有意味。', fig: 'FIG. 2 — SIGNA' },
  { t: 14.0, roman: 'III', title: '世界',  cap: '一整套小小的记号，等你来读。', fig: 'FIG. 3 — MUNDUS' },
  { t: 22.0, roman: 'IV',  title: '牌',   cap: '牌，是一个可以握在手里的问题。', fig: 'FIG. 4 — CHORDA' },
  { t: 24.5, roman: 'V',   title: '抽牌',   cap: '六种活法，挑你此刻需要的那一种。', fig: 'FIG. 5 — SORTES' },
  { t: 33.5, roman: 'VI',  title: '印记',  cap: '你留下的，成为你。', fig: 'FIG. 6 — TOTEM' },
  { t: 40.0, roman: 'VII', title: '名',   cap: '是器物，不是神谕。', fig: 'FIG. 7 — NOMEN' },
];
const FIGS = [
  'FIG. 1 — GUTTA', 'FIG. 2 — COR', 'FIG. 3 — SIGNA', 'FIG. 4 — OCULUS', 'FIG. 5 — MUNDUS',
  'FIG. 6 — CHORDA', 'FIG. 7 — SORTES', 'FIG. 8 — TOTEM', 'FIG. 9 — SIGILLUM',
  'FIG. 10 — NOMEN', 'FIG. 11 — MARCA'
];

/* paper stock schedule: [time, key] ; crossfades over 0.42 s */
const PAPER_KEYS = { cream: 1, env: 1, pageWhite: 1 };
const PAPER_STOPS = [[0, 'cream'], [22.0, 'cream'], [22.42, 'env'], [24.30, 'env'],
                     [24.72, 'cream'], [40.0, 'cream'], [41.60, 'pageWhite']];

/* --------------------------------------------------------------- runtime state */
const ST = {
  t: 0, playing: false, started: false, ended: false, muted: false,
  hold: false, rate: 1, dark: false, active: -1,
  ptr: { x: 960, y: 540, nx: 0, ny: 0 },
  hoverSym: null, flipped: false, drawOpen: false, helpOpen: false,
  userDragged: false, slowAllowed: !REDUCED,
};
window.NT = { ST, A, TX, DUR, CAPTURE, VERTICAL, REDUCED };

/* ------------------------------------------------------------------ paperwork */
const paperState = { a: 'cream', b: 'cream', k: 0 };
function paperAt(t) {
  let a = PAPER_STOPS[0][1], b = PAPER_STOPS[0][1], k = 0;
  for (let i = 0; i < PAPER_STOPS.length; i++) {
    const s = PAPER_STOPS[i];
    if (t >= s[0]) { a = s[1]; if (i + 1 < PAPER_STOPS.length) { b = PAPER_STOPS[i + 1][1]; } else b = s[1]; }
  }
  for (let i = 0; i < PAPER_STOPS.length - 1; i++) {
    const s0 = PAPER_STOPS[i], s1 = PAPER_STOPS[i + 1];
    if (t >= s0[0] && t < s1[0] && s0[1] !== s1[1]) {
      k = E.soft(wt(t, s1[0] - 0.42, s1[0]));
      a = s0[1]; b = s1[1];
    }
  }
  return { a, b, k };
}
let lastPaperSig = '';
function paintPaper(t) {
  const p = paperAt(t);
  const sig = p.a + '|' + p.b + '|' + p.k.toFixed(3);
  if (sig === lastPaperSig) return;
  lastPaperSig = sig;
  if (p.a !== paperState.a || !paperA.style.backgroundImage) paperBg(paperA, p.a);
  paperBg(paperB, p.b);
  paperB.style.opacity = p.k.toFixed(3);
  paperState.a = p.a; paperState.b = p.b; paperState.k = p.k;
  document.body.classList.toggle('dark', p.a === 'env');
}

/* ------------------------------------------------------------- chrome + captions */
let lastChromeSig = '';
const CHROME_CREAM = [36, 31, 34], CHROME_DARK = [247, 242, 230];
function paintChrome(t) {
  let plate = PLATES[0];
  for (const p of PLATES) if (t >= p.t) plate = p;
  // which scene for the figure number
  let si = 0;
  for (let i = 0; i < T.length; i++) if (t >= T[i][0]) si = i;
  const fig = FIGS[si] || FIGS[0];
  const dark = (t >= 21.85 && t < 24.62);
  const sig = plate.roman + fig + dark;
  if (sig !== lastChromeSig) {
    lastChromeSig = sig;
    hdC.textContent = '第 ' + plate.roman + ' 图版 · ' + plate.title;
    hdR.textContent = '图版 ' + plate.roman + ' / VII';
    ftL.textContent = fig;
    capN.textContent = plate.roman;
    capT.textContent = plate.cap;
    document.body.classList.toggle('dark', dark);
  }
  // ink colour crossfade on the black plate
  const k = E.soft(wt(t, 21.7, 22.15)) - E.soft(wt(t, 24.30, 24.75));
  const c = CHROME_CREAM.map((v, i) => Math.round(lerp(v, CHROME_DARK[i], clamp01(k))));
  chrome.style.color = 'rgb(' + c[0] + ',' + c[1] + ',' + c[2] + ')';
  chrome.style.opacity = (t > 24.6 && t < 24.85) ? '1' : '';
  // gold wash on the totem plate
  const gold = E.soft(wt(t, 33.6, 34.2)) * (1 - E.soft(wt(t, 39.9, 40.8)));
  const goldA = gold * 0.15;
  if (goldA.toFixed(3) !== paperTone.style.opacity) {
    paperTone.style.opacity = goldA.toFixed(3);
    paperTone.style.background =
      'radial-gradient(115% 100% at 50% 46%, rgba(123,85,33,.95) 0%, rgba(123,85,33,.95) 52%, rgba(123,85,33,.42) 100%)';
  }
}

/* --------------------------------------------------------------- grain + weave */
function paintGrain(t) {
  const frame = Math.floor(t * 24);
  const k = ((frame % 4) + 4) % 4;
  const tile = 224;
  for (let i = 0; i < grainEls.length; i++) {
    const g = grainEls[i];
    g.style.backgroundImage = 'url("' + TX['grain_' + (i % 2)] + '")';
    g.style.opacity = i === k ? '0.72' : '0';
    if (i === k) {
      g.style.backgroundPosition = (((frame * 137.13) % tile).toFixed(1)) + 'px ' +
                                   (((frame * 91.71) % tile).toFixed(1)) + 'px';
    }
  }
}
function paintWeave(t) {
  const s = (ST.camScale || 1);
  const wx = Math.sin(t * 2.13) * 0.55 + Math.sin(t * 7.37) * 0.24 + ST.ptr.nx * 3.2;
  const wy = Math.cos(t * 1.71) * 0.5 + Math.sin(t * 5.93) * 0.22 + ST.ptr.ny * 2.1;
  const wr = Math.sin(t * 1.29) * 0.028 + Math.sin(t * 3.1) * 0.01;
  artEl.style.transform = 'translate(' + wx.toFixed(2) + 'px,' + wy.toFixed(2) + 'px) rotate(' +
    wr.toFixed(4) + 'deg) scale(' + s.toFixed(4) + ')';
  artEl.style.transformOrigin = (ST.camOx || 960) + 'px ' + (ST.camOy || 540) + 'px';
}

/* ------------------------------------------------------------------ HUD paint */
let lastHudSig = '';
function paintHud(t) {
  if (CAPTURE) return;
  const p = clamp01(t / DUR);
  hudFill.style.width = (p * 100).toFixed(2) + '%';
  hudDot.style.left = (p * 100).toFixed(2) + '%';
  const mm = Math.floor(t / 60), ss = Math.floor(t % 60);
  hudClock.textContent = (mm < 10 ? '0' : '') + mm + ':' + (ss < 10 ? '0' : '') + ss;
  let plate = PLATES[0];
  for (const pl of PLATES) if (t >= pl.t) plate = pl;
  if (hudAct.dataset.k !== plate.roman) {
    hudAct.dataset.k = plate.roman;
    hudAct.textContent = plate.roman + ' — ' + plate.title;
  }
  // chapter dots
  if (chaptersEl.children.length) {
    const idx = PLATES.indexOf(plate);
    for (let i = 0; i < chaptersEl.children.length; i++) {
      chaptersEl.children[i].classList.toggle('on', i === idx);
    }
  }
  document.body.classList.toggle('dark', ST.dark);
}

/* --------------------------------------------------------------------- render */
function render(t) {
  t = clamp(t, 0, DUR);
  ST.t = t;
  // active scene
  let ai = 0;
  for (let i = 0; i < T.length; i++) if (t >= T[i][0]) ai = i;
  if (ai !== ST.active) {
    for (let i = 0; i < SCENES.length; i++) SCENES[i].node.classList.toggle('on', i === ai);
    ST.active = ai;
    if (SCENES[ai]) { SCENES[ai].cam = null; }
  }
  const sc = SCENES[ai];
  if (sc) {
    const local = t - T[ai][0];
    try { if (sc.upd) sc.upd(local, T[ai][1] - T[ai][0], t); } catch (err) { /* keep the film alive */ }
    if (sc.cam) { ST.camScale = sc.cam.s || 1; ST.camOx = sc.cam.x || 960; ST.camOy = sc.cam.y || 540; }
    else { ST.camScale = 1; ST.camOx = 960; ST.camOy = 540; }
  }
  paintPaper(t);
  paintChrome(t);
  paintGrain(t);
  paintWeave(t);
  paintHud(t);
  if (window.NT.Extras) window.NT.Extras.paint(t);
  if (window.NT.TextFX) window.NT.TextFX.tick(t);
}

/* --------------------------------------------------------------------- player */
let rafId = 0, lastNow = 0;
function loop(now) {
  if (!ST.playing) return;
  if (!lastNow) lastNow = now;
  const dt = Math.min(0.06, (now - lastNow) / 1000);
  lastNow = now;
  let t = ST.t + dt * (ST.hold ? 0.34 : 1);
  if (t >= DUR) { t = DUR; render(t); if (window.NT.Audio) window.NT.Audio.update(t); pause(true); }
  else { render(t); if (window.NT.Audio) window.NT.Audio.update(t); }
  if (ST.playing) rafId = requestAnimationFrame(loop);
}
function play() {
  if (ST.playing) { pause(); return; }
  if (ST.t >= DUR - 0.02) ST.t = 0;
  ST.playing = true; lastNow = 0;
  ST.started = true; ST.ended = false;
  document.body.classList.add('playing');
  if (window.NT.Audio) window.NT.Audio.start();
  rafId = requestAnimationFrame(loop);
}
function pause(finished) {
  ST.playing = false;
  document.body.classList.remove('playing');
  cancelAnimationFrame(rafId);
  lastNow = 0;
  if (window.NT.Audio) window.NT.Audio.pause();
  if (finished) { ST.ended = true; }
}
function seek(t) {
  t = clamp(t, 0, DUR);
  const was = ST.playing;
  if (was) { ST.playing = false; cancelAnimationFrame(rafId); lastNow = 0; }
  ST.ended = t >= DUR - 0.001;
  render(t);
  if (was) { ST.playing = true; lastNow = 0; rafId = requestAnimationFrame(loop); }
}
function restart() { seek(0); ST.ended = false; }

/* expose for capture */
window.__renderAt = t => { pause(); render(clamp(t, 0, DUR)); };
window.__seek = seek;
window.__play = play;
window.__pause = pause;
window.__state = ST;

/* ------------------------------------------------------------- small utilities */
function fmtTime(t) {
  const ss = Math.floor(t % 60), mm = Math.floor(t / 60);
  return mm + ':' + (ss < 10 ? '0' : '') + ss;
}
