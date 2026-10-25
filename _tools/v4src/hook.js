/* =====================================================================
   hook.js — the cold open: OCULUS

   D + C + A, fused:

     D  the witness ....... an engraved eye, enormous, cropped by the frame
     A  the first beat .... a crimson pulse drawn across the plate
     C  the tear .......... the sheet is a cover sheet. Its lower edge
                            tears open, and from 1.02 it is pulled away
                            upward, uncovering plate I — which has been
                            running underneath the whole time.

   Because the sheet is clipped, nothing has to cross-dissolve: the film
   below is simply the real film. Every value is a pure function of film
   time, so capture frames are reproducible.

     0.00  ink dark; the frame hairlines draw
     0.06  the pulse starts drawing across the middle band
     0.16  the cream sheet rises into the frame (it was a sheet all along)
     0.26  kick + rule
     0.36  beat 1 — jolt, flash
     0.44  beat 2
     0.48  DO NOT        (chromatic split + 3D push)
     0.56  SCROLL AWAY   (display italic, wider split)
     0.62  the lower edge tears open — plate I shows through
     0.68  别 划 走
     0.74  the claim: THIS IS NOT TAROT, printed on the film itself
     0.86  beat 3
     0.92  the iris settles into one slow breath
     1.02  the sheet is pulled away upward
     1.30  plate I owns the frame
   ===================================================================== */

const HookFX = (() => {
  'use strict';

  const END = 1.30;
  const REVEAL = 1.06;

  let root = null, sheet = null, paper = null, eye = null,
      under = null, uedge = null, ecgA = null, ecgB = null, beats = null,
      big1 = null, big2 = null, kick = null, rule = null, hzline = null,
      claim = null, tear = null, tearB = null, crossH = null, crossV = null,
      iris = null, pupil = null, flash = null,
      hdr = null, ftr = null, mks = [], frame = null,
      built = false;

  /* the torn edge: 13 deterministic samples across the plate */
  const EDGE = [0, .10, .03, .14, .06, .16, .08, .15, .05, .12, .02, .09, 0];
  const TEAR_X = [];
  for (let i = 0; i < EDGE.length; i++) TEAR_X.push(Math.round(i * 1920 / (EDGE.length - 1)));

  const BASE_Y = 690;   /* where the tear sits once fully open */

  function setBg(el, key) {
    if (!el) return;
    const tx = window.TX || {};
    if (tx[key]) el.style.backgroundImage = 'url("' + tx[key] + '")';
  }

  function mk(tag, cls, parent, html) {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    if (parent) parent.appendChild(n);
    return n;
  }

  function edgeY(i, open) {
    const jag = EDGE[i] * 92;
    const closed = 1080 + 40 * (1 - Math.abs(i - 6) / 6);
    const opened = BASE_Y + jag;
    return closed + (opened - closed) * open;
  }

  /* the cover sheet is everything ABOVE the tear line: top-left, across the
     top edge, down the right side, then walk the torn edge right-to-left back
     to the start. Closed, the tear sits below the frame (full cover); open, it
     sits at BASE_Y and the underside shows below. */
  function clipFor(open) {
    const pts = ['0px 0px', '1920px 0px'];
    for (let i = TEAR_X.length - 1; i >= 0; i--) {
      pts.push(TEAR_X[i] + 'px ' + edgeY(i, open).toFixed(1) + 'px');
    }
    return 'polygon(' + pts.join(',') + ')';
  }

  /* the underside is the exact complement of that polygon */
  function underClipFor(open) {
    const pts = [];
    for (let i = 0; i < TEAR_X.length; i++) {
      pts.push(TEAR_X[i] + 'px ' + edgeY(i, open).toFixed(1) + 'px');
    }
    return 'polygon(' + pts.join(',') + ',1920px 1080px,0px 1080px)';
  }

  function pointsFor(open) {
    let s = '';
    for (let i = 0; i < TEAR_X.length; i++) s += (i ? ' ' : '') + TEAR_X[i] + ',' + edgeY(i, open).toFixed(1);
    return s;
  }

  function build() {
    const host = document.getElementById('stage');
    if (!host) return false;

    root = document.createElement('div');
    root.id = 'hook';
    host.appendChild(root);

    /* ---- C · the underside, printed on the back of the sheet ---- */
    under = mk('div', 'hk-under', root);
    const ue = mk('div', 'hk-ueye', under);
    setBg(ue, 'motif_eng_eye_wide_bone');
    mk('div', 'hk-ugrid', under);
    claim = mk('div', 'hk-claim', under,
      '<div class="row"><span class="hk-t" data-t="THIS IS NOT TAROT">THIS IS NOT TAROT</span>' +
      '<span class="hz">这 不是塔罗</span></div>' +
      '<div class="sub">keep going — the last card is yours</div>');

    /* the sheet: everything that belongs to the cold open and gets torn away */
    sheet = mk('div', 'hk-sheet', root);

    mk('div', 'hk-dark', sheet);
    paper = mk('div', 'hk-paper', sheet);
    setBg(paper, 'paper_cream');
    mk('div', 'hk-tone', sheet);
    const vg = mk('div', 'hk-vig', sheet);
    setBg(vg, 'vignette');
    const gr = mk('div', 'hk-grain', sheet);
    setBg(gr, 'grain_0');

    /* ---- A · the pulse ---- */
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'hk-pulse');
    svg.setAttribute('viewBox', '0 0 1920 1080');
    svg.setAttribute('preserveAspectRatio', 'none');
    sheet.appendChild(svg);
    const d =
      'M-40 560 H352 l26 -10 l18 26 l14 -14 l16 -150 l20 300 l18 -150 l16 76 l14 -88 l18 10 ' +
      'H968 l26 -10 l18 26 l14 -14 l16 -170 l20 320 l18 -160 l16 86 l14 -100 l18 10 ' +
      'H1512 l26 -10 l18 26 l14 -14 l16 -140 l20 290 l18 -150 l16 76 l14 -88 l18 10 H1960';
    ecgB = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    ecgB.setAttribute('class', 'hk-ecg b');
    ecgB.setAttribute('d', d);
    ecgB.setAttribute('pathLength', '1');
    svg.appendChild(ecgB);
    ecgA = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    ecgA.setAttribute('class', 'hk-ecg');
    ecgA.setAttribute('d', d);
    ecgA.setAttribute('pathLength', '1');
    svg.appendChild(ecgA);

    beats = mk('div', 'hk-beats', sheet,
      '<i style="left:600px;top:540px"></i><i style="left:1250px;top:520px"></i><i style="left:1706px;top:556px"></i>');

    /* ---- D · the eye ---- */
    eye = mk('div', 'hk-eye', sheet);
    setBg(eye, 'motif_eng_eye_wide_ink');
    iris = mk('div', 'hk-iris', sheet, '<i class="a"></i><i class="b"></i><i class="c"></i>');
    pupil = mk('i', 'd', iris);

    /* ---- A · the words ---- */
    kick = mk('div', 'hk-kick', sheet,
      'A FILM IN SEVEN PLATES<i class="dia"></i>ONE QUESTION<span class="hz">七 图 版</span>');
    rule = mk('i', 'hk-rule', sheet);
    big1 = mk('div', 'hk-line hk-big1', sheet, '<span class="hk-t" data-t="DO NOT">DO NOT</span>');
    big2 = mk('div', 'hk-line hk-big2', sheet, '<span class="hk-t" data-t="SCROLL AWAY">SCROLL AWAY</span>');
    hzline = mk('div', 'hk-hzline', sheet, '<i class="bar"></i><span class="hz">别 划 走</span>');

    const cross = mk('div', 'hk-cross', sheet);
    crossH = mk('i', 'h', cross);
    crossV = mk('i', 'v', cross);

    /* ---- chrome ---- */
    const fsvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    fsvg.setAttribute('class', 'hk-frame');
    fsvg.setAttribute('viewBox', '0 0 1920 1080');
    fsvg.innerHTML =
      '<rect x="64" y="64" width="1792" height="952" fill="none" stroke="currentColor" stroke-width="1.4" opacity=".55"/>' +
      '<rect x="72" y="72" width="1776" height="936" fill="none" stroke="currentColor" stroke-width=".8" opacity=".32"/>' +
      '<path d="M64 940 H288" stroke="currentColor" stroke-width="1" opacity=".45"/>' +
      '<path d="M1632 940 H1856" stroke="currentColor" stroke-width="1" opacity=".45"/>' +
      '<g stroke="currentColor" stroke-width="1" opacity=".5">' +
      '<path d="M960 64 v10 M960 1006 v10"/></g>';
    sheet.appendChild(fsvg);
    frame = fsvg;

    hdr = mk('div', 'hk-hdr', sheet, '<span>NOT TAROT — OCULUS</span><span>TAKE 01 · COLD OPEN</span>');
    ftr = mk('div', 'hk-ftr', sheet, '<span>FIG. 0 — GUTTA</span><span>MMXXVI</span>');
    ['tl', 'tr', 'bl', 'br'].forEach((c) => mks.push(mk('i', 'hk-mk ' + c, sheet)));

    flash = mk('div', 'hk-flash', sheet);

    /* ---- C · the exposed film + its torn edge (not clipped) ---- */
    uedge = mk('div', 'hk-uedge', root);

    const usv = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    usv.setAttribute('class', 'hk-uline');
    usv.setAttribute('viewBox', '0 0 1920 1080');
    usv.setAttribute('preserveAspectRatio', 'none');
    root.appendChild(usv);
    tear = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
    tear.setAttribute('class', 'a');
    tear.setAttribute('pathLength', '1');
    tearB = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
    tearB.setAttribute('class', 'b');
    tearB.setAttribute('pathLength', '1');
    usv.appendChild(tear);
    usv.appendChild(tearB);

    built = true;
    return true;
  }

  function tick(t) {
    if (!built && !build()) return;

    if (t >= END) {
      if (root.style.display !== 'none') root.style.display = 'none';
      return;
    }
    root.style.display = 'block';

    /* ---------- envelopes ---------- */
    const k1 = E.outC(wt(t, 0.02, 0.22));
    const rise = E.outC(wt(t, 0.16, 0.46));
    const eyeIn = E.outC(wt(t, 0.34, 0.74));
    const draw = E.outC(wt(t, 0.05, 0.36));
    const ecgOut = 1 - E.inOut(wt(t, 0.74, 0.90));
    const open = E.outC(wt(t, 0.62, 0.96));
    const lift = E.inC(wt(t, 1.02, 1.30));

    const b1 = t >= 0.36 ? Math.exp(-(t - 0.36) * 18) : 0;
    const b2 = t >= 0.44 ? Math.exp(-(t - 0.44) * 19) : 0;
    const b3 = t >= 0.86 ? Math.exp(-(t - 0.86) * 16) : 0;
    const jolt = b1 * 4.8 + b2 * 3.0 + b3 * 2.6;

    /* ---------- the sheet ---------- */
    sheet.style.clipPath = clipFor(open);
    sheet.style.opacity = (1 - lift * lift * 0.55).toFixed(3);
    sheet.style.transform =
      'translate3d(' + (lift * -26).toFixed(1) + 'px,' + (jolt - lift * 1240).toFixed(1) + 'px,0) ' +
      'rotateX(' + (2.0 - rise * 2.0 + lift * 5.5).toFixed(2) + 'deg) ' +
      'rotateY(' + (-3.8 + eyeIn * 1.6 + lift * 2.4).toFixed(2) + 'deg) ' +
      'scale(' + (1.045 - eyeIn * 0.045).toFixed(4) + ')';

    const ab = 1.2 + jolt * 1.7 + lift * 3.4;
    root.style.setProperty('--hk-abx', (-ab).toFixed(2) + 'px');
    root.style.setProperty('--hk-aby', (ab * 0.36).toFixed(2) + 'px');

    /* ---------- ground ---------- */
    paper.style.transform = 'translate3d(0,' + ((1 - rise) * 106).toFixed(2) + '%,0)';

    /* ---------- the eye ---------- */
    eye.style.opacity = (eyeIn * 0.95).toFixed(3);
    eye.style.transform =
      'translate3d(' + (-12 + eyeIn * 12).toFixed(1) + 'px,' + (24 - eyeIn * 24).toFixed(1) + 'px,0) ' +
      'scale(' + (1.15 - eyeIn * 0.15).toFixed(4) + ') rotate(' + (-2.6 + eyeIn * 2.6).toFixed(2) + 'deg)';

    const iIn = E.outC(wt(t, 0.70, 0.92));
    const br = 1 + (t > 0.92 ? Math.sin((t - 0.92) * 6.2) * 0.016 : 0);
    iris.style.opacity = (iIn * 0.92).toFixed(3);
    iris.style.transform = 'scale(' + br.toFixed(4) + ')';
    const pup = E.outC(wt(t, 0.78, 0.96));
    pupil.style.opacity = (pup * 0.86).toFixed(3);
    pupil.style.transform = 'scale(' + (0.62 + pup * 0.38 + b3 * 0.22).toFixed(3) + ')';

    /* ---------- the pulse ---------- */
    ecgA.style.opacity = (0.95 * ecgOut).toFixed(3);
    ecgA.style.strokeDashoffset = (1 - draw).toFixed(4);
    ecgB.style.opacity = (0.40 * ecgOut).toFixed(3);
    ecgB.style.strokeDashoffset = (1 - Math.min(1, draw * 1.08)).toFixed(4);

    const bt = [0.36, 0.44, 0.86];
    const nds = beats.children;
    for (let i = 0; i < 3; i++) {
      const dt = t - bt[i];
      const on = dt >= 0 ? Math.exp(-dt * 4.8) : 0;
      nds[i].style.opacity = (on * 0.95 * ecgOut).toFixed(3);
      nds[i].style.transform = 'scale(' + (0.6 + on * 1.6).toFixed(3) + ')';
    }

    /* ---------- the tear edge ---------- */
    const pts = pointsFor(open);
    tear.setAttribute('points', pts);
    tearB.setAttribute('points', pts);
    const edgeIn = E.outC(wt(t, 0.64, 0.80));
    const edgeOut = 1 - lift;
    tear.style.opacity = (edgeIn * 0.86 * edgeOut).toFixed(3);
    tearB.style.opacity = (edgeIn * 0.92 * edgeOut).toFixed(3);
    tear.style.strokeDashoffset = (1 - E.outC(wt(t, 0.62, 1.04))).toFixed(3);
    tearB.style.strokeDashoffset = (1 - E.outC(wt(t, 0.62, 1.04))).toFixed(3);

    /* the underside: exactly the band the sheet no longer covers */
    under.style.clipPath = underClipFor(open);
    under.style.opacity = (1 - lift * lift).toFixed(3);
    under.style.transform = 'translate3d(0,' + (-lift * 40).toFixed(1) + 'px,0)';

    const ey = edgeY(6, open);
    uedge.style.top = (ey - 74).toFixed(1) + 'px';
    uedge.style.opacity = (open * 0.9 * (1 - lift)).toFixed(3);

    /* ---------- the claim ---------- */
    const cIn = E.outC(wt(t, 0.76, 0.98));
    claim.style.opacity = (cIn * (1 - lift * 0.7)).toFixed(3);
    claim.style.transform =
      'translate3d(' + ((1 - cIn) * -28).toFixed(1) + 'px,' + ((1 - cIn) * 14 - lift * 30).toFixed(1) + 'px,0)';

    kick.style.opacity = (E.outC(wt(t, 0.26, 0.44)) * 0.96).toFixed(3);
    rule.style.transform = 'scaleX(' + E.outC(wt(t, 0.28, 0.52)).toFixed(3) + ')';

    const l1 = E.outC(wt(t, 0.48, 0.68));
    const l2 = E.outC(wt(t, 0.56, 0.78));
    big1.style.opacity = l1.toFixed(3);
    big1.style.transform = 'translate3d(0,' + ((1 - l1) * 30).toFixed(1) + 'px,0) scale(' + (1.07 - l1 * 0.07).toFixed(3) + ')';
    big1.style.filter = 'blur(' + ((1 - l1) * 8).toFixed(2) + 'px)';
    big2.style.opacity = l2.toFixed(3);
    big2.style.transform = 'translate3d(0,' + ((1 - l2) * 34).toFixed(1) + 'px,0) scale(' + (1.06 - l2 * 0.06).toFixed(3) + ')';
    big2.style.filter = 'blur(' + ((1 - l2) * 9).toFixed(2) + 'px)';

    const hz = E.outC(wt(t, 0.68, 0.86));
    hzline.style.opacity = hz.toFixed(3);
    hzline.style.transform = 'translate3d(' + ((1 - hz) * -20).toFixed(1) + 'px,0,0)';

    /* ---------- chrome ---------- */
    const ch = 1 - E.inOut(wt(t, 0.74, 0.90));
    hdr.style.opacity = (E.outC(wt(t, 0.10, 0.30)) * 0.95 * ch).toFixed(3);
    ftr.style.opacity = (E.outC(wt(t, 0.42, 0.62)) * 0.92 * ch).toFixed(3);
    frame.style.opacity = (0.46 * (1 - E.inOut(wt(t, 0.80, 0.96)))).toFixed(3);
    for (let i = 0; i < mks.length; i++) {
      mks[i].style.opacity = (0.55 * E.outC(wt(t, 0.05 + i * 0.03, 0.24 + i * 0.03)) * ch).toFixed(3);
    }
    crossH.style.transform = 'scaleX(' + k1.toFixed(3) + ')';
    crossV.style.transform = 'scaleY(' + k1.toFixed(3) + ')';

    /* ---------- flash ---------- */
    const fl = Math.max(
      b1 * 0.34,
      b2 * 0.18,
      E.outC(wt(t, 0.16, 0.24)) * (1 - E.outC(wt(t, 0.24, 0.42))) * 0.42
    );
    flash.style.opacity = fl.toFixed(3);
  }

  return { build, tick, END };
})();

if (window.NT) window.NT.Hook = HookFX;
