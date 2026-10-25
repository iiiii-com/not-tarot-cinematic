/* =====================================================================
   scenes_a.js — plates I–III · the drop, the heart, the signs, the eye, the world
   ===================================================================== */
const NS = 'http://www.w3.org/2000/svg';
function svgEl(tag, attrs, parent) {
  const n = document.createElementNS(NS, tag);
  if (attrs) for (const k in attrs) n.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(n);
  return n;
}
function pulse(local, beats, rise, fall) {
  rise = rise || 0.085; fall = fall || 0.52;
  let v = 0;
  for (const b of beats) {
    const k = local - b;
    if (k >= 0 && k < rise + fall) {
      v = Math.max(v, k < rise ? E.out(k / rise) : 1 - E.out((k - rise) / fall));
    }
  }
  return v;
}

/* =========================================================== I — THE DROP */
const S1 = scene(0, 2.6, (node) => {
  const staffA = mk('div', 's1-staff', node);
  mk('div', 's1-staff b', node);
  const vert = mk('div', 's1-vert', node, 'ONE DROP IS ENOUGH<i class="hz hzb">一滴，就够了</i>');
  mk('div', 's1-num', node, 'I');

  const target = mk('div', 's1-target', node);
  target.style.left = '620px'; target.style.top = '540px';
  const ring = mk('div', 's1-ring', target);
  for (let i = 0; i < 12; i++) {
    const tk = mk('i', null, ring);
    tk.style.cssText = 'position:absolute;left:50%;top:50%;width:1px;height:11px;background:rgba(36,31,34,.42);' +
      'transform-origin:50% 0;transform:rotate(' + (i * 30) + 'deg) translateY(-112px)';
  }
  const splash = mk('div', 's1-splash', node);
  splash.style.left = '620px'; splash.style.top = '540px';
  const rings = [0, 1, 2].map(() => mk('i', null, splash));
  const blot = mk('div', null, node);
  blot.style.cssText = 'position:absolute;left:620px;top:540px;width:0;height:0;border-radius:46% 54% 51% 49%/52% 47% 53% 48%;' +
    'background:var(--berry);' +
    'transform:translate(-50%,-50%);opacity:0;';
  const drop = mk('div', 's1-drop', node);
  const copy = mk('div', 's1-copy', node);
  mk('div', 'kick', copy, 'FRONTISPIECE<i class="hz">序 图</i>');
  const big = mk('h1', 's1-big', copy, '<span>ONE DROP</span><span>OF INK</span><i class="hz hzb">一滴 · 成墨</i>');
  const rule = mk('div', 's1-rule', copy);
  mk('i', 'dia', rule);
  mk('p', 's1-lede', copy, 'Everything begins as a single mark.<br>This one has a pulse.<i class="hz hzw">一切都从一道痕开始。<br>这一道，有脉搏。</i>');
  const lines = [big.children[0], big.children[1], rule, copy.querySelector('.s1-lede')];

  /* a few specimen ticks around the plate */
  const vertTicks = mk('div', null, node);
  vertTicks.style.cssText = 'position:absolute;right:150px;top:300px;bottom:340px;width:20px;';
  for (let i = 0; i < 9; i++) {
    const t = mk('i', null, vertTicks);
    t.style.cssText = 'position:absolute;right:0;top:' + (i * 12.5) + '%;width:' + (i % 3 === 0 ? 18 : 9) + 'px;height:1px;background:rgba(36,31,34,.28);';
    const lab = mk('span', 'lab', vertTicks, String(i + 1).padStart(2, '0'));
    lab.style.cssText = 'position:absolute;right:' + (i % 3 === 0 ? 24 : 15) + 'px;top:' + (i * 12.5) + '%;font-size:8px;opacity:.3;transform:translateY(-50%);';
  }

  S1.upd = (local, dur) => {
    // drop: anticipation, fall, land
    const fall = E.inC(wt(local, 0.28, 1.02));
    const y = lerp(-330, 331, fall);
    const ant = E.soft(wt(local, 0, 0.28));
    drop.style.transform = 'translateY(' + (y + ant * -18).toFixed(1) + 'px) scale(' + (1 + ant * 0.06).toFixed(3) + ')';
    drop.style.opacity = local > 1.16 ? String(Math.max(0, 1 - wt(local, 1.16, 1.30))) : String(wt(local, 0.02, 0.18));
    // target ring draws in
    ring.style.opacity = String(E.outC(wt(local, 0.1, 0.75)) * 0.9);
    ring.style.transform = 'scale(' + lerp(0.86, 1, E.outBack(wt(local, 0.1, 0.8))).toFixed(3) + ') rotate(' + (wt(local, 0, 2.6) * 22).toFixed(2) + 'deg)';

    // impact ripples
    const hit = 1.14;
    rings.forEach((r, i) => {
      const k = wt(local, hit + i * 0.12, hit + i * 0.12 + 0.9);
      r.style.opacity = String(k > 0 && k < 1 ? (1 - k) * 0.75 : 0);
      const sc = 0.16 + E.outQ(k) * (1.1 + i * 0.55);
      r.style.transform = 'translate(-50%,-50%) scale(' + sc.toFixed(3) + ')';
    });
    // blot grows, breathes, then condenses into a pulse seed
    const grow = E.outC(wt(local, 1.14, 1.62));
    const shrink = E.inOut(wt(local, 2.18, 2.52));
    const pulseK = pulse(local, [1.62, 1.94, 2.26], 0.05, 0.22);
    const sz = lerp(0, 150, grow) * (1 - shrink * 0.62) * (1 + pulseK * 0.10);
    blot.style.width = blot.style.height = sz.toFixed(1) + 'px';
    blot.style.opacity = String(grow * (1 - shrink * 0.28) * 0.92);
    blot.style.borderRadius = (46 + Math.sin(local * 3.1) * 2.5).toFixed(1) + '% ' + (54 - Math.sin(local * 2.4) * 2).toFixed(1) +
      '% ' + (51 + Math.cos(local * 2.9) * 2.4).toFixed(1) + '% ' + (49 - Math.cos(local * 3.3) * 2.2).toFixed(1) +
      '%/' + (52 + Math.sin(local * 2.2) * 2).toFixed(1) + '% ' + (47 - Math.sin(local * 2.7) * 2.3).toFixed(1) +
      '% ' + (53 + Math.cos(local * 2.5) * 2).toFixed(1) + '% ' + (48 - Math.cos(local * 3) * 2).toFixed(1) + '%';

    // type
    const ks = [0.5, 0.66, 1.0, 1.34];
    lines.forEach((ln, i) => {
      const k = E.outC(wt(local, ks[i], ks[i] + 0.72));
      ln.style.opacity = String(k);
      ln.style.transform = 'translateY(' + ((1 - k) * 26).toFixed(1) + 'px)';
    });
    vert.style.opacity = String(E.outC(wt(local, 1.4, 2.1)) * 0.4);
    S1.cam = { s: 1 + E.outC(wt(local, 0, 2.6)) * 0.02, x: 900, y: 520 };
  };
});

/* =========================================================== II — THE HEART */
const S2 = scene(2.6, 8.0, (node) => {
  // ECG
  const svg = svgEl('svg', { viewBox: '0 0 1920 1080', class: 's2-ecg' }, node);
  const PX0 = 140, PX1 = 1800, BASE = 742, PER = 328, AMP = 168;
  const xs = [];
  let d = '';
  for (let x = PX0; x <= PX1; x += 2) {
    const ph = ((x - PX0) % PER) / PER;
    const g = (c, w, a) => { const z = (ph - c) / w; return a * Math.exp(-(z * z) * 4); };
    let v = g(0.16, 0.045, 0.075) + g(0.30, 0.013, -0.115) + g(0.315, 0.0085, 1.0) +
            g(0.331, 0.012, -0.30) + g(0.455, 0.05, 0.135);
    const y = BASE - v * AMP;
    d += (x === PX0 ? 'M' : 'L') + x + ' ' + y.toFixed(2);
    xs.push(y);
  }
  const ghost = svgEl('path', { d, stroke: '#D8A5B8', 'stroke-width': 3.4, opacity: .45 }, svg);
  const main = svgEl('path', { d, stroke: '#8F2C3B', 'stroke-width': 2.4 }, svg);
  ghost.style.transform = 'translate(3px,4px)';
  const LEN = Math.ceil(main.getTotalLength());
  main.style.strokeDasharray = LEN; main.style.strokeDashoffset = LEN;
  ghost.style.strokeDasharray = LEN; ghost.style.strokeDashoffset = LEN;

  const heart = mk('div', 's2-heart', node);
  bg(heart, 'heart', 'berry');
  const heartGhost = mk('div', 's2-heart', node);
  bg(heartGhost, 'heart', 'mauve');
  heartGhost.style.opacity = '0';
  heartGhost.style.transform = 'translate(5px,7px)';

  const ruler = mk('div', 's2-ruler', node);
  const bpm = mk('div', 's2-bpm', node, '<i></i><span>72 BPM · NORMAL SINUS</span>');
  const bpmDot = bpm.querySelector('i');

  const copy = mk('div', 's2-copy', node);
  mk('div', 'kick', copy, 'THE FIRST SIGNAL<i class="hz">第一次信号</i>');
  const lines = ['EVERYTHING', 'MEANS', 'SOMETHING.'].map(t => {
    const w = mk('div', 's2-line', copy); const b = mk('b', null, w, t); return b;
  });
  const sub = mk('div', 's2-sub', copy, '<i class="hl"></i><em>A muscle keeping its own time</em><i class="hz">按自己的节拍跳动</i>');
  /* (the headline is English already — no duplicate sub-line) */

  const crosses = [[380, 250], [980, 830], [1560, 300], [720, 240]].map(([x, y]) => {
    const c = mk('div', 's2-cross', node); c.style.left = x + 'px'; c.style.top = y + 'px'; return c;
  });
  const note = mk('div', 's2-note', node,
    '<p>the line is not a wave —<br>it is a hand, testing the dark.</p><span class="lab">FIG. 2 · COR</span>');

  const beats = [1.30, 2.18, 3.06, 3.94, 4.82, 5.70, 6.58, 7.20];

  S2.upd = (local, dur) => {
    // line draws
    const draw = E.inOut(wt(local, 0.12, 2.25));
    main.style.strokeDashoffset = String(LEN * (1 - draw));
    ghost.style.strokeDashoffset = String(LEN * (1 - Math.max(0, draw * 1.008 - 0.008)));
    // heart appears at the drawn head
    const app = E.outC(wt(local, 0.9, 1.8));
    const bp = pulse(local, beats);
    const push = E.soft(wt(local, 3.4, 5.0)) * 0.012;
    heart.style.opacity = String(app);
    heart.style.transform = 'scale(' + (lerp(0.92, 1, app) * (1 + bp * 0.055)).toFixed(4) + ') rotate(' + (Math.sin(local * 0.6) * 0.6).toFixed(2) + 'deg)';
    heartGhost.style.opacity = String(app * 0.55);
    heartGhost.style.transform = heart.style.transform.replace(/scale\(/g, 'scale(').replace(')', '') + ')';
    // type
    const ks = [1.15, 1.42, 1.68];
    lines.forEach((b, i) => {
      b.style.transform = 'translateY(' + ((1 - E.outC(wt(local, ks[i], ks[i] + 0.8))) * 120).toFixed(2) + '%)';
    });
    sub.style.opacity = String(E.outC(wt(local, 2.2, 2.9)));
    // ruler + labels
    ruler.style.transform = 'scaleX(' + E.outC(wt(local, 0.75, 2.0)).toFixed(3) + ')';
    ruler.style.transformOrigin = '0 50%';
    crosses.forEach((c, i) => { c.style.opacity = String(E.outC(wt(local, 0.8 + i * 0.16, 1.4 + i * 0.16)) * 0.4); });
    note.style.opacity = String(E.outC(wt(local, 2.7, 3.5)) * 0.85);
    bpm.style.opacity = String(E.outC(wt(local, 0.6, 1.3)) * 0.8);
    bpmDot.style.transform = 'scale(' + (1 + bp * 1.5).toFixed(2) + ')';
    bpmDot.style.opacity = String(0.5 + bp * 0.5);
    // camera: heartbeat push
    S2.cam = { s: 1 + push + bp * 0.006, x: 620, y: 470 };
  };
});

/* =========================================================== III — THE SIGNS */
const S3 = scene(8.0, 14.0, (node) => {
  const cx = 960, cy = 500;
  const R3 = [170, 238, 320];
  const svg = svgEl('svg', { viewBox: '0 0 1920 1080', class: 's3-ring' }, node);
  const rings = R3.map(r => svgEl('circle', { cx, cy, r }, svg));
  for (let i = 0; i < 72; i++) {
    const a = (i / 72) * Math.PI * 2 - Math.PI / 2;
    const major = i % 6 === 0;
    const r0 = 184, r1 = major ? 230 : 208;
    svgEl('line', {
      x1: (cx + Math.cos(a) * r0).toFixed(2), y1: (cy + Math.sin(a) * r0).toFixed(2),
      x2: (cx + Math.cos(a) * r1).toFixed(2), y2: (cy + Math.sin(a) * r1).toFixed(2),
      class: major ? 'deg' : '', 'stroke-width': major ? 1.3 : 1
    }, svg);
  }
  const h1 = mk('div', 's3-h1', node), h2 = mk('div', 's3-h2', node);
  bg(h1, 'heart', 'berry'); bg(h2, 'heart', 'berry');

  const ghost = mk('div', 's3-ghost', node, 'XVIII');

  const SYMS = ['heart', 'eye', 'butterfly', 'tiger', 'unicorn', 'crown', 'mirror', 'compass',
                'hands', 'wand', 'skull', 'moon', 'key', 'flower', 'star', 'snake', 'hourglass', 'scales'];
  const nums = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII',
                'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII'];
  const items = SYMS.map((name, i) => {
    const ang = -Math.PI / 2 + (i / SYMS.length) * Math.PI * 2;
    const sx = cx + Math.cos(ang) * 320, sy = cy + Math.sin(ang) * 320;
    const el = mk('div', 's3-sym', node);
    bg(el, name, i % 5 === 0 ? 'crimson' : 'berry');
    return { el, sx, sy, ang };
  });

  const core = mk('div', 's3-core', node);
  mk('i', 'c1', core); mk('i', 'c2', core); mk('i', 'c3', core);
  mk('span', 'rn', core, 'XVIII');

  const title = mk('div', 's3-title', node, 'SYMBOLS <em>RELEASED</em>.<i class="hz hzb">符号释出。</i>');
  const subtitle = mk('div', 's3-sub', node, 'Eighteen signs walked out of one heart<i class="hz hzb">十八个符号，从一颗心里走出来</i>');
  const vertL = mk('div', 's3-vert', node, 'SIGNA · XVIII');
  const vertR = mk('div', 's3-vert b', node, 'PLATE II');

  S3.upd = (local, dur) => {
    // ring draws
    rings.forEach((r, i) => {
      const len = 2 * Math.PI * R3[i];
      const k = E.outC(wt(local, 0.15 + i * 0.14, 1.5 + i * 0.14));
      r.style.strokeDasharray = len; r.style.strokeDashoffset = len * (1 - k);
      r.style.opacity = String(0.25 + k * 0.75);
    });
    svg.style.transform = 'rotate(' + (E.inOut(wt(local, 0, 6)) * 6).toFixed(2) + 'deg)';
    svg.style.transformOrigin = cx + 'px ' + cy + 'px';
    svg.style.opacity = String(E.outC(wt(local, 0, 0.5)));

    // heart splits and lets go
    const split = E.inOut(wt(local, 0.35, 1.6));
    const fade = 1 - E.soft(wt(local, 1.9, 2.7));
    const hScale = lerp(1, 0.86, split);
    h1.style.opacity = String(fade);
    h2.style.opacity = String(fade);
    h1.style.transform = 'translate(' + lerp(-300, -54, split).toFixed(1) + 'px,' + lerp(16, -6, split).toFixed(1) + 'px) scale(' + hScale.toFixed(3) + ') rotate(' + (-split * 7).toFixed(2) + 'deg)';
    h2.style.transform = 'translate(' + lerp(-300, 54, split).toFixed(1) + 'px,' + lerp(16, -6, split).toFixed(1) + 'px) scale(' + hScale.toFixed(3) + ') rotate(' + (split * 7).toFixed(2) + 'deg)';

    // watermark numeral + central axis appear after the heart is gone
    const ck = E.outC(wt(local, 2.25, 3.15));
    ghost.style.opacity = String(ck * 0.05);
    core.style.opacity = String(ck * 0.9);
    core.style.transform = 'scale(' + lerp(0.82, 1, ck).toFixed(3) + ') rotate(' + (local * 2.6).toFixed(1) + 'deg)';

    // symbols fly out to the ring
    items.forEach((it, i) => {
      const start = 0.75 + i * 0.085;
      const k = E.outBack(wt(local, start, start + 1.05));
      const settle = E.inOut(wt(local, 4.6, 6.0));
      const shrink = 1 - settle * 0.06;
      const sx = cx + (it.sx - cx) * shrink, sy = cy + (it.sy - cy) * shrink;
      const px = lerp(cx, sx, k), py = lerp(cy, sy, k);
      const sc = lerp(0.12, 1, k) * (1 + Math.sin(local * 0.9 + i) * 0.008);
      it.el.style.transform = 'translate(' + px.toFixed(1) + 'px,' + py.toFixed(1) + 'px) translate(-50%,-50%) scale(' + sc.toFixed(3) + ') rotate(' + ((1 - k) * 34 + (i % 2 ? 1.5 : -1.5)).toFixed(2) + 'deg)';
      it.el.style.left = '0px'; it.el.style.top = '0px';
      it.el.style.margin = '0';
      it.el.style.opacity = String(k > 0.02 ? Math.min(1, k * 2.4) : 0);
      it.el.style.transformBox = 'view-box';
    });

    title.style.opacity = String(E.outC(wt(local, 2.55, 3.3)));
    title.style.transform = 'translateY(' + ((1 - E.outC(wt(local, 2.55, 3.3))) * 22).toFixed(1) + 'px)';
    subtitle.style.opacity = String(E.outC(wt(local, 3.3, 3.95)) * 0.7);
    vertL.style.opacity = String(E.outC(wt(local, 1.1, 2)) * 0.4);
    vertR.style.opacity = String(E.outC(wt(local, 1.3, 2.2)) * 0.4);
    S3.cam = { s: lerp(1.045, 1.0, E.inOut(wt(local, 0, 6))), x: cx, y: cy };
  };
});

/* =========================================================== IV — THE WITNESS */
const S4 = scene(14.0, 17.5, (node) => {
  const cx = 1266, cy = 502, RX = 372, UY = 176, LY = 136;
  const RI = 152, RP = 54, ICY = cy - 12;

  // ---- the witness: an engraved eye, drawn stroke by stroke -----------------
  const svg = svgEl('svg', { viewBox: '0 0 1920 1080', class: 's4-eye-svg' }, node);
  const defs = svgEl('defs', {}, svg);
  const lidGroup = svgEl('g', {}, svg);
  const openClip = svgEl('clipPath', { id: 's4eyeOpen' }, defs);
  const clipped = svgEl('g', { 'clip-path': 'url(#s4eyeOpen)' }, lidGroup);

  const N = 132;
  function curve(up, sy, t0, t1, n) {
    const out = [];
    for (let i = 0; i <= n; i++) {
      const t = lerp(t0, t1, i / n);
      const s = Math.pow(Math.sin(Math.PI * t), up ? 0.86 : 0.94);
      out.push([cx + (t * 2 - 1) * RX, cy - (up ? UY * sy * s : -LY * sy * s)]);
    }
    return out;
  }
  const pt = p => p[0].toFixed(1) + ' ' + p[1].toFixed(1);
  const pathOf = pts => 'M' + pt(pts[0]) + ' L' + pts.slice(1).map(pt).join(' L');
  const tailOf = pts => ' L' + pts.map(pt).join(' L');
  function tangent(pts, i) {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
    const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1;
    return [dx / L, dy / L];
  }

  const upper = curve(true, 1, 0, 1, N);
  const lower = curve(false, 1, 0, 1, N);
  const openD = pathOf(upper) + tailOf(lower.slice().reverse()) + ' Z';
  svgEl('path', { d: openD }, openClip);

  // the opening itself, double ruled
  svgEl('path', { d: pathOf(upper), 'stroke-width': 2.7 }, lidGroup);
  svgEl('path', { d: pathOf(lower), 'stroke-width': 2.5 }, lidGroup);
  svgEl('path', { d: pathOf(curve(true, 1.20, 0.10, 0.92, 84)), 'stroke-width': 1, class: 'eye-fine' }, lidGroup);
  svgEl('path', { d: pathOf(curve(false, 1.16, 0.12, 0.90, 84)), 'stroke-width': .9, class: 'eye-fine' }, lidGroup);

  // an eyebrow, engraved with a comb of hachures
  const brow = [];
  for (let i = 0; i <= 90; i++) {
    const t = lerp(0.04, 0.96, i / 90);
    brow.push([cx + (t * 2 - 1) * RX * 1.02, cy - UY - 62 - 32 * Math.pow(Math.sin(Math.PI * t), 0.8)]);
  }
  svgEl('path', { d: pathOf(brow), 'stroke-width': 1.5, class: 'eye-fine' }, lidGroup);
  for (let k = 1; k < 18; k++) {
    const i = Math.round((k / 18) * (brow.length - 1));
    const p = brow[i], [tx, ty] = tangent(brow, i);
    const len = 6 + 5 * Math.sin((k / 18) * Math.PI);
    svgEl('line', { x1: p[0], y1: p[1], x2: p[0] - ty * len * 1.2, y2: p[1] + tx * len * 1.2,
      'stroke-width': .7, class: 'eye-fine', opacity: .38 }, lidGroup);
  }

  // upper lashes, swept along the lid normal
  for (let k = 1; k < 27; k++) {
    const t = k / 27;
    if (t < 0.05 || t > 0.955) continue;
    const i = Math.round(t * (upper.length - 1)), p = upper[i], [tx, ty] = tangent(upper, i);
    let nx = ty, ny = -tx;
    const len = 22 + 30 * Math.pow(Math.sin(Math.PI * t), 0.7);
    const sw = 0.20;
    const dx = nx * Math.cos(sw) - ny * Math.sin(sw), dy = nx * Math.sin(sw) + ny * Math.cos(sw);
    const ex = p[0] + dx * len, ey = p[1] + dy * len;
    const mx = p[0] + dx * len * 0.55 + tx * len * 0.14, my = p[1] + dy * len * 0.55 + ty * len * 0.14;
    svgEl('path', { d: 'M' + pt(p) + ' Q' + pt([mx, my]) + ' ' + pt([ex, ey]),
      'stroke-width': k % 4 === 0 ? 1.5 : 1.05, class: 'eye-fine' }, lidGroup);
  }
  // lower lashes, shorter and denser near the corners
  for (let k = 1; k < 15; k++) {
    const t = k / 15;
    if (t < 0.10 || t > 0.90) continue;
    const i = Math.round(t * (lower.length - 1)), p = lower[i], [tx, ty] = tangent(lower, i);
    let nx = -ty, ny = tx;
    const len = 8 + 9 * Math.sin(Math.PI * t);
    const ex = p[0] + nx * len + tx * len * 0.3, ey = p[1] + ny * len + ty * len * 0.3;
    svgEl('path', { d: 'M' + pt(p) + ' Q' + pt([p[0] + nx * len * .6 + tx * 2, p[1] + ny * len * .6 + ty * 2]) + ' ' + pt([ex, ey]),
      'stroke-width': .9, class: 'eye-fine' }, lidGroup);
  }

  // corner flourishes, anchored to the corners
  svgEl('path', { d: 'M' + pt([cx - RX + 6, cy]) + ' c -20 -3 -34 -14 -34 -30 c 0 -11 9 -18 19 -15 c 9 3 10 13 3 17 c -5 3 -11 0 -10 -5',
    'stroke-width': 1.1, class: 'eye-fine' }, lidGroup);
  svgEl('path', { d: 'M' + pt([cx + RX - 4, cy]) + ' c 20 -4 34 -16 33 -33 c -1 -12 -12 -19 -21 -14 c -7 4 -7 13 -1 16 c 6 3 12 -1 11 -7',
    'stroke-width': 1.1, class: 'eye-fine' }, lidGroup);

  // iris, clipped by the opening so the lids cross it
  const irisRot = svgEl('g', {}, clipped);
  svgEl('circle', { cx, cy: ICY, r: RI, 'stroke-width': 2.4 }, irisRot);
  for (let i = 0; i < 120; i++) {
    const a = (i / 120) * Math.PI * 2;
    const r0 = RI - 14, r1 = RI - 2 + (i % 2 ? 1.5 : 0);
    svgEl('line', { x1: cx + Math.cos(a) * r0, y1: ICY + Math.sin(a) * r0,
      x2: cx + Math.cos(a) * r1, y2: ICY + Math.sin(a) * r1,
      'stroke-width': .9, class: 'eye-mid' }, irisRot);
  }
  svgEl('circle', { cx, cy: ICY, r: RI * 0.80, 'stroke-width': .9, opacity: .5 }, irisRot);
  svgEl('circle', { cx, cy: ICY, r: RI * 0.55, 'stroke-width': .9, 'stroke-dasharray': '2 4', opacity: .45 }, irisRot);
  for (let i = 0; i < 80; i++) {
    const a = (i / 80) * Math.PI * 2;
    const r0 = RP + 10, r1 = RI * (0.86 + (i % 3 === 0 ? 0.06 : 0));
    svgEl('line', { x1: cx + Math.cos(a) * r0, y1: ICY + Math.sin(a) * r0,
      x2: cx + Math.cos(a) * r1, y2: ICY + Math.sin(a) * r1,
      'stroke-width': i % 5 === 0 ? 1.45 : 0.85, class: i % 2 ? 'eye-fine' : 'eye-mid' }, irisRot);
  }
  // corona, engraved outside the iris
  for (let i = 0; i < 84; i++) {
    const a = (i / 84) * Math.PI * 2;
    const r0 = RI + 12, r1 = RI + 12 + (i % 3 === 0 ? 24 : 12);
    svgEl('line', { x1: cx + Math.cos(a) * r0, y1: ICY + Math.sin(a) * r0,
      x2: cx + Math.cos(a) * r1, y2: ICY + Math.sin(a) * r1,
      'stroke-width': .8, class: 'eye-fine' }, clipped);
  }

  // the pupil follows the pointer
  const pupilGroup = svgEl('g', {}, clipped);
  svgEl('circle', { cx, cy: ICY, r: RP, 'stroke-width': 2.6 }, pupilGroup);
  svgEl('circle', { cx, cy: ICY, r: 22, class: 'eye-pp' }, pupilGroup);
  svgEl('circle', { cx, cy: ICY, r: RP * 0.76, 'stroke-width': .9, 'stroke-dasharray': '1 4', opacity: .55 }, pupilGroup);
  svgEl('path', { d: 'M' + pt([cx - 13, ICY - 6]) + ' A 13 13 0 0 1 ' + pt([cx - 2, ICY + 12]),
    'stroke-width': 2, class: 'eye-paper', opacity: .95 }, pupilGroup);
  svgEl('circle', { cx: cx + 15, cy: ICY - 17, r: 3, class: 'eye-paper', 'stroke-width': 0 }, pupilGroup);

  // the line that shows while the eye is shut
  const blinkLine = svgEl('line', { x1: cx - RX, y1: cy, x2: cx + RX, y2: cy, 'stroke-width': 2.2, opacity: 0 }, lidGroup);

  const copy = mk('div', 's4-copy', node);
  mk('div', 'kick', copy, 'THE WITNESS<i class="hz">见 证 者</i>');
  const big = mk('h1', 's4-big', copy, 'IT SEES<span>YOU FIRST.</span><i class="hz hzb">它先看见你。</i>');
  const rule = mk('div', 's4-rule', copy, '<i class="hl"></i><i class="dia"></i>');
  mk('p', 's4-lede', copy, 'Before you named a thing, it had already looked at you.<br>Meaning is a gaze you step into.<i class="hz hzw">在你为一样东西命名之前，它已经看过你了。<br>意义，是你走进的一道目光。</i>');
  const look = mk('div', 's4-look', node, 'MOVE THE CURSOR — IT FOLLOWS<i class="hz">移动鼠标 · 它会跟随</i>');
  mk('div', 's4-fig lab berry', node, 'FIG. 4 \u2014 OCULUS');

  const scale = mk('div', 's4-scale', node);
  for (let i = 0; i < 24; i++) {
    const t = mk('i', (i % 6 === 0 ? 'b' : ''), scale);
    t.style.top = (6 + i * 4) + '%';
  }
  [['0', 6], ['30', 26], ['60', 46], ['90', 66], ['120', 86]].forEach(([txt, top]) => {
    const sp = mk('span', null, scale, txt); sp.style.top = top + '%';
  });

  svg.style.transformOrigin = cx + 'px ' + cy + 'px';

  S4.upd = (local, dur) => {
    const reveal = E.outC(wt(local, 0.30, 1.15));
    let closed = 1 - E.inOut(wt(local, 0.34, 1.18));
    const u = Math.abs(local - 2.36) / 0.10;
    const b = Math.max(0, 1 - u * u);
    closed = Math.max(closed, b * b * (3 - 2 * b));
    const sy = 1 - closed * 0.965;
    lidGroup.setAttribute('transform', 'translate(' + cx + ' ' + cy + ') scale(1 ' + sy.toFixed(4) + ') translate(' + (-cx) + ' ' + (-cy) + ')');
    blinkLine.setAttribute('opacity', (closed * 0.9).toFixed(3));
    svg.style.opacity = String(reveal * 0.74);
    svg.style.transform = 'scale(' + lerp(1.04, 1, E.inOut(wt(local, 0, 3.5))).toFixed(4) + ') rotate(-1.6deg)';

    irisRot.setAttribute('transform', 'translate(' + cx + ' ' + ICY + ') rotate(' + (local * 2.4 + 11).toFixed(2) + ') translate(' + (-cx) + ' ' + (-ICY) + ')');
    const nx = ST.ptr.nx, ny = ST.ptr.ny;
    const ix = nx * 32 + Math.sin(local * 0.7) * 2.0;
    const iy = ny * 20 + Math.cos(local * 0.9) * 1.6;
    pupilGroup.setAttribute('transform', 'translate(' + ix.toFixed(2) + ' ' + iy.toFixed(2) + ')');

    big.style.opacity = String(E.outC(wt(local, 0.75, 1.6)));
    big.style.transform = 'translateY(' + ((1 - E.outC(wt(local, 0.75, 1.6))) * 18).toFixed(1) + 'px)';
    rule.style.opacity = String(E.outC(wt(local, 1.05, 1.8)));
    copy.querySelector('.s4-lede').style.opacity = String(E.outC(wt(local, 1.3, 2.0)) * 0.74);
    look.style.opacity = String(E.outC(wt(local, 1.5, 2.2)) * 0.7);
    S4.cam = { s: 1 + E.inOut(wt(local, 0, 3.5)) * 0.045, x: cx, y: cy };
  };
});

const S5 = scene(17.5, 22.0, (node) => {
  const grid = mk('div', 's5-grid', node);
  const ALL = ['heart', 'eye', 'eye_tears', 'butterfly', 'tiger', 'unicorn', 'crown', 'mirror', 'compass',
               'hands', 'wand', 'skull', 'moon', 'cloud_eye', 'scales', 'question', 'book', 'key',
               'flower', 'star', 'snake', 'hourglass', 'arch', 'candle', 'scissors'];
  const NAMES = {
        heart: ['COR', 'a muscle that keeps time', '一块记时的肌肉'],
        eye: ['OCULUS', 'the first witness', '第一个见证者'],
        eye_tears: ['LACRIMAE', 'sight that spills', '会溢出的看见'],
        butterfly: ['PAPILIO', 'the self mid-change', '正在变形的自己'],
        tiger: ['TIGRIS', 'fear wearing stripes', '披着条纹的恐惧'],
        unicorn: ['UNICORNIS', 'the impossible errand', '不可能的任务'],
        crown: ['CORONA', 'what you agree to carry', '你同意承担的重量'],
        mirror: ['SPECULUM', 'the other you', '另一个你'],
        compass: ['CIRCINUS', 'a hand that insists on north', '执意指向北方的手'],
        hands: ['MANUS', 'what holds and lets go', '握紧，也放开'],
        wand: ['VIRGA', 'a line that makes', '一条能造物的线'],
        skull: ['CALVARIA', 'the argument for today', '为今天辩护的理由'],
        moon: ['LUNA', 'the borrowed light', '借来的光'],
        cloud_eye: ['NIMBUS', 'a weather that watches', '会注视的天气'],
        scales: ['LIBRA', 'the price of almost', '差一点点的价格'],
        question: ['QUAESTIO', 'the door with no handle', '没有把手的门'],
        book: ['LIBER', 'a room you can carry', '可以随身携带的房间'],
        key: ['CLAVIS', 'the permission you make', '你自己给的许可'],
        flower: ['FLOS', 'a wound somebody named', '有人命名的伤口'],
        star: ['STELLA', 'the far-off yes', '很远的那个「是」'],
        snake: ['ANGUIS', 'the change you resent', '你不情愿的改变'],
        hourglass: ['HORA', 'a leak you call a life', '你称之为生命的漏'],
        arch: ['ARCUS', 'the shape of passing through', '穿过去的形状'],
        candle: ['CANDELA', 'a small refusal of the dark', '对黑暗的小小拒绝'],
        scissors: ['FORFEX', 'the cut that lets go', '让你松手的那一剪']
  };
  window.NT.SYM_NAMES = NAMES;
  const cells = ALL.map((name, i) => {
    const c = mk('div', 's5-cell', grid);
    c.dataset.sym = name;
    const s = mk('div', 's5-sym', c);
    bg(s, name, 'berry');
    const no = mk('div', 's5-no', c, String(i + 1).padStart(2, '0'));
    return { c, s, name, i };
  });

  const left = mk('div', 's5-left', node);
  mk('div', 'kick', left, 'TWENTY-FIVE SPECIMENS<i class="hz">二十五个标本</i>');
  mk('h1', 's5-h', left, 'A WORLD OF<span>SYMBOLS.</span><i class="hz hzb">符号的世界。</i>');
  const rule = mk('div', 's5-rule', left, '<i class="hl"></i><i class="dia"></i><i class="hl"></i>');
  mk('p', 's5-para', left, 'They are never fixed: a heart is a pump, a promise, a warning —' +
        'the same mark, three fates. Which one looks back at you is yours to decide.' +
        'That is the whole trick of signs, and the whole trouble of being alive.<i class="hz hzw">它们从来不是固定的：心是泵，是承诺，也是警告——同一个记号，三种命运。哪一个在回望你，由你决定。</i>');
  const hover = mk('div', 's5-hover', node);
  const hNum = mk('span', 'num', hover, 'SPECIMEN 01');
  const hName = mk('span', 'nm', hover, 'COR');
  const hDesc = mk('span', 'ds', hover, 'COR · a muscle that keeps time<i class="hz">一块记时的肌肉</i>');
  const count = mk('div', 's5-count', node, '25 SIGNS · 18 RELEASED · 7 KEPT<i class="hz">释出十八 · 留存七</i>');
  mk('div', 's5-foot', node, '<span>SPECIMEN PLATE · THE WORLD<i class="hz">标本图版 · 世界</i></span><span>SCALE 1 : 1<i class="hz">比例</i></span><span>ONE INK · ONE COLOUR<i class="hz">一滴墨 · 一种颜色</i></span>');

  function setHover(name) {
    const c = cells.find(x => x.name === name);
    if (!c) return;
    hNum.textContent = 'SPECIMEN ' + String(c.i + 1).padStart(2, '0');
    hName.textContent = NAMES[name] ? NAMES[name][0] : name;
    hDesc.innerHTML = NAMES[name] ? NAMES[name][1] + '<i class="hz">' + NAMES[name][2] + '</i>' : 'an unread sign';
  }
  window.NT.S5 = { cells, setHover };
  // hover listeners are wired in interact.js

  S5.upd = (local, dur) => {
    const conv = E.inOut(wt(local, 4.30, 4.50));
    cells.forEach(({ s }, i) => {
      const start = 0.32 + i * 0.036;
      const k = E.outBack(wt(local, start, start + 0.62));
      const hov = ST.hoverSym === cells[i].name ? 1 : 0;
      s.style.transform = 'scale(' + (k * (1 + hov * 0.12) * (1 - conv * 0.45)).toFixed(3) + ')';
      s.style.opacity = String(k * (1 - conv * 0.4));
      cells[i].c.style.background = hov ? 'rgba(143,44,59,.045)' : '';
    });
    grid.style.opacity = String(1 - conv * 0.5);
    left.style.opacity = String(E.outC(wt(local, 0.5, 1.6)) * (1 - conv * 0.35));
    left.style.transform = 'translateX(' + ((1 - E.outC(wt(local, 0.5, 1.6))) * -18).toFixed(1) + 'px)';
    hover.style.opacity = String(E.outC(wt(local, 1.4, 2.2)) * (1 - conv));
    count.style.opacity = String(E.outC(wt(local, 1.0, 1.8)) * 0.45 * (1 - conv));
    S5.cam = { s: 1 + E.inOut(wt(local, 0, 4.5)) * 0.03, x: 1180, y: 520 };
  };
});
