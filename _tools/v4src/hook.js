/* =====================================================================
   hook.js — the cold open: OCULUS

   Four gestures, each given its own rest. At any instant one thing moves
   and the next thing waits.

     A  the first beat .... a single crimson trace draws itself across a
                            black plate, two beats apart, then lands.
     D  the witness ....... the cream sheet climbs in from below and the
                            engraved eye develops on it as it arrives — the
                            eye is printed on the paper, so it rises with
                            the paper instead of landing on top of it.
     C  the tear .......... the sheet is torn away: a ragged edge sweeps up
                            through the frame, uncovering plate I, whose ink
                            drop is already in the air beneath it.

   Timing (all in film seconds):

     0.00  black. nothing moves. the film holds its breath
     0.34  the frame hairlines draw themselves in, slowly
     0.52  the trace starts walking, left to right
     1.00  beat 1                    1.34  beat 2
     1.90  the trace lands and rests, alone on the dark
     2.16  the paper begins to climb
     2.34  the eye develops on the climbing paper
     2.88  one line of type settles: THIS IS NOT TAROT
     3.02  beat 3, on the paper this time
     3.12  a held breath: paper, eye, one line. nothing moves
     3.46  the sheet is torn away upward, ragged edge first
     3.78  plate I owns the frame, its ink blot blooming

   Every value is a pure function of t, so capture frames reproduce exactly.
   ===================================================================== */

const HookFX = (() => {
  'use strict';

  const END = 3.78;
  const REVEAL = 3.46;

  let root = null, sheet = null, paper = null, eye = null,
      ecgA = null, ecgB = null, beats = null,
      kick = null, rule = null, big1 = null,
      crossH = null, crossV = null,
      iris = null, pupil = null, flash = null,
      hdr = null, ftr = null, mks = [], frame = null,
      tear = null, tearB = null, tearS = null,
      built = false;

  /* motifs live in window.A, textures in window.TX */
  function setBg(el, key) {
    if (!el) return;
    const a = window.A || {}, tx = window.TX || {};
    const src = tx[key] || a[key];
    if (src) el.style.backgroundImage = 'url("' + src + '")';
  }

  function mk(tag, cls, parent, html) {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    if (parent) parent.appendChild(n);
    return n;
  }

  /* one ECG line: flat baseline, a small P bump, a tall QRS, a T hump */
  function ecgPath(off) {
    const y0 = 646, pts = [];
    const push = (x, y) => pts.push(x.toFixed(1) + ' ' + y.toFixed(1));
    push(-60, y0);
    [452, 1004, 1556, 1960].forEach((sx, i) => {
      const base = y0 + off * (i % 2 ? 5 : -3);
      push(sx - 132, base);
      push(sx - 108, base - 13);
      push(sx - 86, base + 6);
      push(sx - 62, base);
      push(sx - 34, base);
      push(sx - 12, base + 15);
      push(sx, base - 158);
      push(sx + 12, base + 42);
      push(sx + 28, base - 3);
      push(sx + 62, base);
    });
    return 'M' + pts.join(' L');
  }

  /* ---- the torn edge ------------------------------------------------ */
  /* 13 points across the frame; amplitudes stay small so the tear reads as
     paper, not as a saw. */
  const EDGE = [0, .10, .03, .14, .06, .16, .08, .15, .05, .12, .02, .09, 0];
  const TEAR_X = EDGE.map((_, i) => i * 1920 / 12);
  const BASE_Y = 690;

  function edgeY(i, open) {
    /* closed: the ragged edge sits below the frame on the sheet's own bottom
       edge; open: it travels up past the top, taking the sheet with it. */
    const closed = 1120 + 26 * (1 - Math.abs(i - 6) / 6);
    const opened = BASE_Y + EDGE[i] * 92 - 880;
    return closed + (opened - closed) * open;
  }
  function clipFor(open) {
    const pts = ['0px 0px', '1920px 0px'];
    for (let i = TEAR_X.length - 1; i >= 0; i--) {
      pts.push(TEAR_X[i].toFixed(1) + 'px ' + edgeY(i, open).toFixed(1) + 'px');
    }
    return 'polygon(' + pts.join(',') + ')';
  }
  function pointsFor(open) {
    return TEAR_X.map((x, i) => x.toFixed(1) + ',' + edgeY(i, open).toFixed(1)).join(' ');
  }

  function build() {
    const host = document.getElementById('stage');
    if (!host) return false;

    root = document.createElement('div');
    root.id = 'hook';
    root.setAttribute('aria-hidden', 'true');
    host.appendChild(root);

    /* ------------------------------------------------------------ sheet */
    sheet = mk('div', 'hk-sheet', root);

    mk('div', 'hk-dark', sheet);
    paper = mk('div', 'hk-paper', sheet);
    setBg(paper, 'paper_cream');
    mk('div', 'hk-tone', sheet);
    mk('div', 'hk-vig', sheet);
    setBg(mk('div', 'hk-grain', sheet), 'grain_0');

    /* ------------------------------------------------------- the trace */
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'hk-pulse');
    svg.setAttribute('viewBox', '0 0 1920 1080');
    svg.setAttribute('preserveAspectRatio', 'none');
    sheet.appendChild(svg);

    function path(cls, d) {
      const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      p.setAttribute('class', cls);
      p.setAttribute('d', d);
      p.setAttribute('pathLength', '1');
      svg.appendChild(p);
      return p;
    }
    ecgB = path('hk-ecg b', ecgPath(6));
    ecgA = path('hk-ecg', ecgPath(0));

    beats = mk('div', 'hk-beats', sheet);
    [[452, 646], [1004, 646], [1556, 646]].forEach(([x, y]) => {
      const d = mk('i', null, beats);
      d.style.left = x + 'px';
      d.style.top = y + 'px';
    });

    /* --------------------------------------------------------- the eye */
    eye = mk('div', 'hk-eye', sheet);
    setBg(eye, 'motif_eng_eye_wide_ink');

    iris = mk('div', 'hk-iris', sheet);
    ['a', 'b', 'c'].forEach(k => mk('i', k, iris));
    pupil = mk('i', 'd', iris);

    /* -------------------------------------------------------- the type */
    kick = mk('div', 'hk-kick', sheet, 'A FILM IN SEVEN PLATES<i class="dia"></i>ONE QUESTION');
    rule = mk('i', 'hk-rule', sheet);
    big1 = mk('div', 'hk-line hk-big1', sheet,
      '<span class="hk-t" data-t="THIS IS NOT TAROT">THIS IS NOT TAROT</span>');

    /* ------------------------------------------------------------ chrome */
    const cross = mk('div', 'hk-cross', sheet);
    crossH = mk('i', 'h', cross);
    crossV = mk('i', 'v', cross);

    const fr = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    fr.setAttribute('class', 'hk-frame');
    fr.setAttribute('viewBox', '0 0 1920 1080');
    fr.setAttribute('preserveAspectRatio', 'none');
    fr.innerHTML =
      '<rect x="64" y="64" width="1792" height="952" fill="none" stroke="currentColor" ' +
      'stroke-width="1.4" opacity=".55"/>' +
      '<rect x="72" y="72" width="1776" height="936" fill="none" stroke="currentColor" ' +
      'stroke-width=".8" opacity=".32"/>' +
      '<path d="M64 940 H288" stroke="currentColor" stroke-width="1" opacity=".45"/>' +
      '<path d="M1632 940 H1856" stroke="currentColor" stroke-width="1" opacity=".45"/>' +
      '<path d="M960 64 V92" stroke="currentColor" stroke-width=".9" opacity=".38"/>' +
      '<path d="M960 988 V1016" stroke="currentColor" stroke-width=".9" opacity=".38"/>';
    sheet.appendChild(fr);
    frame = fr;

    hdr = mk('div', 'hk-hdr', sheet,
      '<span>NOT TAROT — OCULUS</span><span>TAKE 01 · COLD OPEN</span>');
    ftr = mk('div', 'hk-ftr', sheet,
      '<span>FIG. 0 — GUTTA</span><span>MMXXVI</span>');

    ['tl', 'tr', 'bl', 'br'].forEach(k => mks.push(mk('i', 'hk-mk ' + k, sheet)));

    flash = mk('div', 'hk-flash', sheet);

    /* ---- the torn edge, drawn above the sheet --------------------- */
    const ul = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    ul.setAttribute('class', 'hk-uline');
    ul.setAttribute('viewBox', '0 0 1920 1080');
    ul.setAttribute('preserveAspectRatio', 'none');
    root.appendChild(ul);
    function poly(cls) {
      const p = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
      p.setAttribute('class', cls);
      p.setAttribute('pathLength', '1');
      ul.appendChild(p);
      return p;
    }
    tearS = poly('c');
    tear = poly('a');
    tearB = poly('b');

    built = true;
    return true;
  }

  function tick(t) {
    if (!built) { if (!build()) return; }
    if (t >= END) {
      if (root.style.display !== 'none') root.style.display = 'none';
      return;
    }
    if (root.style.display === 'none') root.style.display = '';

    /* -------------------------------------------------- phase envelopes */
    const draw = E.outC(wt(t, 0.52, 1.90));        /* the trace walks       */
    const ecgOut = 1 - E.inOut(wt(t, 1.90, 2.18)); /* the trace lets go     */
    const rise = E.inOut(wt(t, 2.16, 2.86));       /* the sheet climbs      */
    const eyeIn = E.outC(wt(t, 2.34, 3.02));       /* the eye develops      */
    const typeIn = E.outC(wt(t, 2.88, 3.12));      /* one line settles      */
    const open = E.inOut(wt(t, REVEAL, END));      /* the sheet is torn     */

    const b1 = t >= 1.00 ? Math.exp(-(t - 1.00) * 4.6) : 0;
    const b2 = t >= 1.34 ? Math.exp(-(t - 1.34) * 5.0) : 0;
    const b3 = t >= 3.02 ? Math.exp(-(t - 3.02) * 4.4) : 0;
    const jolt = b1 * 3.4 + b2 * 2.4 + b3 * 1.6;

    /* --------------------------------------------------------- the sheet */
    const breath = t > 3.12 ? Math.sin((t - 3.12) * 1.9) * 0.0016 : 0;
    sheet.style.clipPath = clipFor(open);
    sheet.style.opacity = String(1 - open * 0.18);
    sheet.style.transform =
      'translate3d(' + (open * -12).toFixed(2) + 'px,' + (jolt - open * 52).toFixed(2) + 'px,0)' +
      ' rotateX(' + (1.0 - rise * 1.0 + open * 3.0).toFixed(3) + 'deg)' +
      ' rotateY(' + (-1.4 + eyeIn * 0.5 + open * 1.2).toFixed(3) + 'deg)' +
      ' scale(' + (1.020 - eyeIn * 0.020 + breath).toFixed(4) + ')';

    /* chromatic split: tiny, so the type reads as printed, not as a blur */
    const ab = -(0.7 + jolt * 0.40 + open * 1.0);
    root.style.setProperty('--hk-abx', ab.toFixed(2) + 'px');
    root.style.setProperty('--hk-aby', (ab * 0.34).toFixed(2) + 'px');

    paper.style.transform = 'translate3d(0,' + ((1 - rise) * 104).toFixed(2) + '%,0)';

    /* ----------------------------------------------------------- the eye */
    eye.style.opacity = String(eyeIn * 0.96);
    eye.style.transform =
      'translate3d(' + (-6 + eyeIn * 6).toFixed(1) + 'px,' + (12 - eyeIn * 12).toFixed(1) + 'px,0)' +
      ' scale(' + (1.08 - eyeIn * 0.08).toFixed(4) + ')' +
      ' rotate(' + (-1.5 + eyeIn * 1.5).toFixed(2) + 'deg)';

    const iIn = E.outC(wt(t, 2.52, 2.94));
    const ibr = 1 + (t > 2.94 ? Math.sin((t - 2.94) * 2.3) * 0.010 : 0);
    iris.style.opacity = String(iIn * 0.88);
    iris.style.transform = 'scale(' + ibr.toFixed(4) + ')';

    const pup = E.outC(wt(t, 2.64, 2.98));
    pupil.style.opacity = String(pup * 0.82);
    pupil.style.transform = 'scale(' + (0.72 + pup * 0.28 + b3 * 0.10).toFixed(3) + ')';

    /* --------------------------------------------------------- the trace */
    ecgA.style.opacity = String(0.94 * ecgOut);
    ecgA.style.strokeDashoffset = String(1 - draw);
    ecgB.style.opacity = String(0.30 * ecgOut);
    ecgB.style.strokeDashoffset = String(1 - Math.min(1, draw * 1.04));

    const bt = [1.00, 1.34, 3.02];
    for (let i = 0; i < beats.children.length; i++) {
      const dt = t - bt[i];
      const on = dt >= 0 ? Math.exp(-dt * 2.6) : 0;
      const n = beats.children[i];
      n.style.opacity = String(on * 0.92 * ecgOut);
      n.style.transform = 'scale(' + (0.45 + on * 1.45).toFixed(3) + ')';
    }

    /* ---------------------------------------------------------- the type */
    kick.style.opacity = String(E.outC(wt(t, 2.86, 3.08)) * 0.9 * (1 - open));
    rule.style.transform = 'scaleX(' + E.outC(wt(t, 2.90, 3.16)).toFixed(3) + ')';

    big1.style.opacity = String(typeIn * (1 - open * 0.9));
    big1.style.transform =
      'translate3d(0,' + ((1 - typeIn) * 14 - open * 18).toFixed(1) + 'px,0)' +
      ' scale(' + (1.028 - typeIn * 0.028).toFixed(4) + ')';
    big1.style.filter = typeIn < 0.995 ? 'blur(' + ((1 - typeIn) * 4).toFixed(2) + 'px)' : 'none';

    /* ------------------------------------------------------------ chrome */
    const ch = 1 - E.inOut(wt(t, 3.44, 3.66));
    hdr.style.opacity = String(E.outC(wt(t, 0.34, 0.68)) * 0.86 * ch);
    ftr.style.opacity = String(E.outC(wt(t, 2.72, 3.00)) * 0.8 * ch);
    frame.style.opacity = String(0.44 * E.outC(wt(t, 0.36, 0.72)) * ch * (1 - open));
    for (let i = 0; i < mks.length; i++) {
      mks[i].style.opacity = String(0.46 * E.outC(wt(t, 0.38 + i * 0.05, 0.66 + i * 0.05)) * ch);
    }
    crossH.style.transform = 'scaleX(' + E.outC(wt(t, 0.32, 0.66)).toFixed(3) + ')';
    crossV.style.transform = 'scaleY(' + E.outC(wt(t, 0.34, 0.68)).toFixed(3) + ')';

    /* ---- the ragged edge itself ------------------------------------ */
    const pts = pointsFor(open);
    tear.setAttribute('points', pts);
    tearB.setAttribute('points', pts);
    tearS.setAttribute('points', pts);
    const edgeIn = E.outC(wt(t, REVEAL - 0.06, REVEAL + 0.04));
    const edgeOut = 1 - E.outC(wt(t, END - 0.14, END));
    tearS.style.opacity = String(edgeIn * 0.62 * edgeOut);
    tear.style.opacity = String(edgeIn * 0.70 * edgeOut);
    tearB.style.opacity = String(edgeIn * 0.50 * edgeOut);

    flash.style.opacity = String(Math.max(b1 * 0.10, b2 * 0.07, b3 * 0.05) * ecgOut);
  }

  return { build, tick, END };
})();

if (window.NT) window.NT.Hook = HookFX;
