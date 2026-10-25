/* =====================================================================
   trans.js — plate-to-plate handoff, made continuous

   The film is cut into eleven scenes by hard time marks. Those cuts used
   to be pure crossfades in the scene layer. This module overlays a short
   gesture centred on every plate mark so the change reads as one held
   breath rather than a flicker:

     0–1.5 s before the mark ... the outgoing plate settles
     the mark itself .......... a hairline crosses, motes lift
     0–1.5 s after the mark ... the incoming plate resolves

   The gesture vocabulary is drawn per cut from the plate it opens:
     I   paper shutter (ink dropping onto fresh paper)
     II  bloom (crimson)
     III rule (registration hairline)
     IV  ink wash
     V   motes only
     VI  paper shutter (the ink flood)
     VII bloom (crimson, the draw)
     VIII rule + motes
     IX  bloom (gold)
     X   ink wash (the closing)
     XI  paper shutter (brand)

   Deterministic: every value is a pure function of film time t.
   ===================================================================== */

const TransFX = (() => {
  'use strict';

  /* plate marks, in film order — mirrors core.js T[i][0] */
  const MARKS = [0, 8.0, 14.0, 17.5, 22.0, 24.5, 33.5, 36.0, 40.0, 42.0];
  const HALF = 0.9;                 /* gesture half-width, seconds */
  const LEAD = 1.55;                 /* how far ahead the plate shadow starts breathing */

  /* per-mark gesture recipe: [kind, weighted intensity, isGold] */
  const RECIPES = [
    ['shut',   0.90, 0],   /* I    */
    ['bloom',  0.95, 0],   /* II   */
    ['rule',   1.00, 0],   /* III  */
    ['ink',    0.72, 0],   /* IV   */
    ['dip',    1.00, 0],   /* V    */
    ['shut',   1.00, 0],   /* VI   */
    ['bloom',  1.00, 0],   /* VII  */
    ['rule',   0.85, 0],   /* VIII */
    ['bloom',  0.85, 1],   /* IX   */
    ['ink',    0.85, 0],   /* X    */
    ['shut',   1.00, 0],   /* XI   */
  ];

  let root = null, vig = null, dip = null, ink = null, bloom = null, bloomB = null,
      shutT = null, shutB = null, ruleA = null, ruleB = null, cut = null,
      motes = null, built = false;

  const MOTE_N = 16;
  const mote = [];

  function setBg(el, key) {
    if (!el || !window.TX || !window.TX[key]) return;
    el.style.backgroundImage = 'url("' + window.TX[key] + '")';
  }

  function build() {
    const fx = document.getElementById('fx');
    if (!fx) return false;
    root = document.createElement('div');
    root.className = 'tr-root';
    root.setAttribute('aria-hidden', 'true');

    /* motes are built once, deterministically */
    const rnd = mulberry(7719);
    let moteHtml = '';
    for (let i = 0; i < MOTE_N; i++) {
      const x = 90 + rnd() * 1740;
      const y = 90 + rnd() * 900;
      const s = 2 + rnd() * 2.6;
      const bone = rnd() > 0.62 ? ' b' : '';
      mote.push({ x, y, s, dx: (rnd() - 0.5) * 34, dy: -18 - rnd() * 46, d: rnd() });
      moteHtml += '<i class="' + bone.trim() + '" style="left:' + x.toFixed(1) + 'px;top:' +
        y.toFixed(1) + 'px;width:' + s.toFixed(1) + 'px;height:' + s.toFixed(1) + 'px"></i>';
    }

    root.innerHTML =
      '<div class="tr-vig"></div>' +
      '<div class="tr-dip"></div>' +
      '<div class="tr-ink"></div>' +
      '<div class="tr-bloom"></div>' +
      '<div class="tr-bloom gold"></div>' +
      '<div class="tr-shut t"></div>' +
      '<div class="tr-shut b"></div>' +
      '<div class="tr-rule"></div>' +
      '<div class="tr-rule b"></div>' +
      '<div class="tr-cut"></div>' +
      '<div class="tr-motes">' + moteHtml + '</div>';

    fx.appendChild(root);

    vig = root.querySelector('.tr-vig');
    dip = root.querySelector('.tr-dip');
    ink = root.querySelector('.tr-ink');
    bloom = root.querySelector('.tr-bloom:not(.gold)');
    bloomB = root.querySelector('.tr-bloom.gold');
    shutT = root.querySelector('.tr-shut.t');
    shutB = root.querySelector('.tr-shut.b');
    ruleA = root.querySelector('.tr-rule');
    ruleB = root.querySelector('.tr-rule.b');
    cut = root.querySelector('.tr-cut');
    motes = root.querySelectorAll('.tr-motes i');

    setBg(ink, 'ink_0');
    const mask = (window.TX && (window.TX.ink_flood || window.TX.ink_0)) || null;
    if (mask) root.style.setProperty('--trmask', 'url("' + mask + '")');
    if (mask && ink) {
      ink.style.webkitMaskImage = 'url("' + mask + '")';
      ink.style.maskImage = 'url("' + mask + '")';
    }
    if (vig) setBg(vig, 'vignette');

    built = true;
    return true;
  }

  /* find the nearest plate mark, and the gesture distance (|d| in s) */
  function probe(t) {
    let best = -1, bestD = 1e9;
    for (let i = 0; i < MARKS.length; i++) {
      const d = t - MARKS[i];
      if (Math.abs(d) < Math.abs(bestD)) { bestD = d; best = i; }
    }
    return { i: best, d: bestD };
  }

  function tick(t) {
    if (!built && !build()) return;
    const p = probe(t);
    if (p.i < 0 || Math.abs(p.d) > LEAD + HALF) {
      root.style.display = 'none';
      return;
    }
    root.style.display = 'block';

    const recipe = RECIPES[p.i] || RECIPES[4];
    const [kind, amt, gold] = recipe;
    const a = Math.abs(p.d);

    /* ---- the plate shadow: breathes across the whole handoff ---- */
    /* peak right at the mark, soft shoulders of LEAD seconds              */
    let vg = 0;
    if (a < LEAD) vg = Math.pow(1 - a / LEAD, 1.6) * 0.86;
    /* the outgoing plate darkens a touch harder (the page turns away)    */
    if (p.d < 0) vg *= 1.06;
    vig.style.opacity = vg.toFixed(3);

    /* ---- a single motion envelope for the cut gesture ------------------ */
    /* u = 1 at the mark, falls to 0 at HALF seconds either side          */
    const u = a < HALF ? Math.pow(1 - a / HALF, 1.35) : 0;

    /* baseline reset (cheap, only ~11 marks over 45 s) */
    bloom.style.opacity = '0';
    bloomB.style.opacity = '0';
    shutT.style.opacity = '0';
    shutB.style.opacity = '0';
    ruleA.style.opacity = '0';
    ruleB.style.opacity = '0';
    ink.style.opacity = '0';
    dip.style.opacity = '0';
    cut.style.opacity = '0';
    for (let i = 0; i < motes.length; i++) motes[i].style.opacity = '0';

    if (u <= 0.001) return;

    /* the hairline that runs exactly at the mark ------------------------ */
    cut.style.opacity = (u * u * amt).toFixed(3);
    cut.style.transform = 'translate3d(0,' + ((p.d < 0 ? -1 : 1) * (1 - u) * 26).toFixed(1) + 'px,0) scaleX(' +
      (0.5 + u * 0.5).toFixed(3) + ')';

    if (kind === 'dip') {
      /* asymmetric: ramps in over the last 0.55 s, releases over the first
         0.30 s after the mark, so the scene swap happens inside the dark */
      const ramp = p.d < 0
        ? E.inOut(clamp01(1 - a / 0.55))
        : E.inOut(clamp01(1 - a / 0.30));
      dip.style.opacity = (ramp * amt).toFixed(3);
    } else if (kind === 'shut') {
      /* two sheets slide apart — the cut itself is the seam ------------- */
      const open = E.outC(Math.min(1, (1 - u) * 2.4));
      const sh = (u * amt);
      shutT.style.opacity = sh.toFixed(3);
      shutB.style.opacity = sh.toFixed(3);
      shutT.style.transform = 'translate3d(0,' + (-(1 - sh) * 102).toFixed(2) + '%,0)';
      shutB.style.transform = 'translate3d(0,' + ((1 - sh) * 102).toFixed(2) + '%,0)';
    } else if (kind === 'bloom') {
      const target = gold ? bloomB : bloom;
      const other = gold ? bloom : bloomB;
      other.style.opacity = '0';
      target.style.opacity = (u * amt * 0.95).toFixed(3);
      target.style.transform = 'scale(' + (0.72 + (1 - u) * 0.55).toFixed(3) + ')';
    } else if (kind === 'ink') {
      /* a wash, not a blackout: the mask blob is pushed below the frame so
         the ink rises from the bottom edge; the ceiling stays low enough
         that the plate never goes blank (see diffseq notes in patch doc) */
      ink.style.opacity = (u * u * amt * 0.40).toFixed(3);
      ink.style.transform = 'translate3d(0,' + ((1 - u) * 30).toFixed(1) +
        '%,0) scale(' + (1.10 - u * 0.10).toFixed(3) + ')';
    } else if (kind === 'rule') {
      ruleA.style.opacity = (u * amt).toFixed(3);
      ruleB.style.opacity = (u * amt * 0.7).toFixed(3);
      ruleA.style.left = ((0.5 - u * 0.32) * 100).toFixed(2) + '%';
      ruleB.style.left = ((0.5 - u * 0.11) * 100).toFixed(2) + '%';
    }

    /* motes ride every kind of cut, a little softer for 'motes' -------- */
    const mAmt = (kind === 'motes' ? 1 : 0.55) * amt;
    for (let i = 0; i < motes.length; i++) {
      const m = mote[i];
      /* a drifting ribbon: each mote lifts as the cut passes it */
      const k = u * (0.55 + m.d * 0.7);
      motes[i].style.opacity = (k * mAmt).toFixed(3);
      motes[i].style.transform = 'translate3d(' + (m.dx * u).toFixed(1) + 'px,' +
        (m.dy * u).toFixed(1) + 'px,0) scale(' + (1 + u * 0.4).toFixed(2) + ')';
    }
  }

  return { tick, build, MARKS };
})();

if (window.NT) window.NT.Trans = TransFX;
