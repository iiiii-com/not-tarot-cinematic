/* =====================================================================
   textfx.js — ink misregistration, colour conflict & 3-D press for type
   Reads every headline once, stamps two extra "impressions" of the same
   words in crimson / gold behind it, then drives them from the pointer
   and from the film clock so the colour story is deterministic in
   captures and alive in the browser.
   ===================================================================== */

const TextFX = (() => {
  const INK = {
    plum: '#241F22', berry: '#8F2C3B', crimson: '#B01F38',
    gold: '#7B5521', bone: '#F7F2E6', mauve: '#D8A5B8',
    page: '#FEFAF9'
  };
  const PAIRS = [
    [INK.crimson, INK.gold], [INK.gold, INK.crimson], [INK.crimson, INK.mauve],
    [INK.berry, INK.gold], [INK.gold, INK.mauve], [INK.mauve, INK.crimson]
  ];
  const CARD_INKS = [INK.berry, INK.crimson, INK.gold, INK.plum, INK.berry, INK.crimson];
  const PAL_CYCLES = [[INK.crimson, INK.gold], [INK.gold, INK.crimson],
                      [INK.crimson, INK.mauve], [INK.gold, INK.mauve],
                      [INK.mauve, INK.crimson], [INK.gold, INK.crimson]];

  /* selector, main ink per index, depth, ghost opacity */
  const TARGETS = [
    ['.s1-big span',        [INK.plum, INK.berry],                 1.25, .50, .34],
    ['.s2-line b',          [INK.plum, INK.plum, INK.berry],       1.35, .52, .34],
    ['.s2-sub em',          [INK.gold],                           0.90, .40, .26],
    ['.s3-title em',        [INK.crimson],                         1.10, .55, .34],
    ['.s4-big span',        [INK.plum, INK.berry],                 1.30, .50, .32],
    ['.s5-h span',          [INK.plum, INK.berry],                 1.30, .50, .32],
    ['.s6-big span',        [INK.bone, INK.gold],                  1.50, .55, .30],
    ['.s8-big span',        [INK.berry, INK.gold],                 1.30, .52, .32],
    ['.s9-word',            [INK.berry],                           1.55, .50, .32],
    ['.s10-word',           [INK.plum],                           1.20, .38, .24],
    ['.s11-word',           [INK.plum],                            2.00, .50, .34],
    ['.s11-sub',            [INK.berry],                           1.10, .46, .30],
    ['.s11-kick',           [INK.crimson],                         0.80, .42, .26],
    ['.cf-name',            CARD_INKS,                             1.05, .48, .30],
    ['.cf-latin',           [INK.gold],                            0.80, .36, .22],
    ['.p-title span',       [INK.plum, INK.berry],                 1.60, .52, .34],
    ['.p-kicker',           [INK.crimson],                         0.70, .40, .24],
    ['.p-lede b',           [INK.berry],                           0.80, .42, .26],
    ['.dw-name',            [INK.berry],                           1.20, .48, .30],
    ['.dw-latin2',          [INK.gold],                            0.80, .36, .22]
  ];

  const STAGE3D = ['.s1-copy', '.s2-copy', '.s4-copy', '.s5-left',
                   '.s6-copy', '.s8-copy', '.c-copy', '.s11-wrap'];

  let booted = false, happy = false;
  let capT = null, hudAct = null, cName = null, s11word = null, s9word = null;
  let stageEl = null, lastHover = 0;
  let cycleEls = [];
  let mx = 0, my = 0, raf = 0, reg = 1;

  function isPlain(el) {
    if (el.children && el.children.length) return false;
    return !!(el.textContent && el.textContent.trim());
  }

  /* a red face gets gold + mauve impressions so the words never sink into
     a single red blur; dark faces get the loud crimson + gold pair */
  function ghostPair(main, pair) {
    if (main === INK.berry || main === INK.crimson) return [INK.gold, INK.mauve];
    if (main === INK.gold) return [INK.crimson, INK.mauve];
    if (main === INK.bone) return [INK.crimson, INK.gold];
    return pair;
  }

  function stamp(el, main, pair, d, o1, o2) {
    pair = ghostPair(main, pair);
    if (main === INK.berry || main === INK.crimson) { o1 *= 0.62; o2 *= 0.55; }
    const txt = el.textContent.trim();
    if (!txt) return;
    el.setAttribute('data-tx', txt);
    if (main) el.style.color = main;
    el.style.setProperty('--c1', pair[0]);
    el.style.setProperty('--c2', pair[1]);
    el.style.setProperty('--d', d);
    el.style.setProperty('--o1', Math.min(1, o1 * 1.75).toFixed(2));
    el.style.setProperty('--o2', Math.min(1, o2 * 2.15).toFixed(2));
    try {
      if (getComputedStyle(el).position === 'static') el.classList.add('tx-rel');
    } catch (e) { el.classList.add('tx-rel'); }
  }

  function build() {
    TARGETS.forEach((spec, ti) => {
      const sel = spec[0], mains = spec[1], d = spec[2], o1 = spec[3], o2 = spec[4];
      let nodes = [];
      try { nodes = [...document.querySelectorAll(sel)]; } catch (e) { nodes = []; }
      nodes.forEach((el, i) => {
        if (!isPlain(el)) return;
        if (el.getAttribute('data-tx')) return;
        const main = mains[Math.min(i, mains.length - 1)];
        stamp(el, main, PAIRS[(i + ti) % PAIRS.length], d, o1, o2);
      });
    });
    STAGE3D.forEach(sel => {
      document.querySelectorAll(sel).forEach(el => el.classList.add('c3d'));
    });
  }

  function bind() {
    stageEl = document.getElementById('stage') || document.body;
    window.addEventListener('pointermove', e => {
      try {
        const r = stageEl.getBoundingClientRect();
        if (!r.width || !r.height) return;
        mx = ((e.clientX - r.left) / r.width) * 2 - 1;
        my = ((e.clientY - r.top) / r.height) * 2 - 1;
        mx = Math.max(-1, Math.min(1, mx));
        my = Math.max(-1, Math.min(1, my));
        if (!raf) {
          raf = requestAnimationFrame(() => {
            raf = 0;
            const rs = document.documentElement.style;
            rs.setProperty('--mx', mx.toFixed(3));
            rs.setProperty('--my', my.toFixed(3));
          });
        }
      } catch (err) { /* ignore */ }
    }, { passive: true });

    window.addEventListener('pointerleave', () => {
      mx = 0; my = 0;
      const rs = document.documentElement.style;
      rs.setProperty('--mx', '0');
      rs.setProperty('--my', '0');
    });

    document.addEventListener('pointerdown', e => {
      const tx = e.target && e.target.closest ? e.target.closest('[data-tx]') : null;
      if (!tx) return;
      tx.classList.remove('tx-hit');
      void tx.offsetWidth;
      tx.classList.add('tx-hit');
      setTimeout(() => tx.classList.remove('tx-hit'), 560);
      try { window.NT.Audio.sfx('click'); } catch (err) { }
    }, true);

    document.addEventListener('dblclick', e => {
      const tx = e.target && e.target.closest ? e.target.closest('[data-tx]') : null;
      if (!tx) return;
      tx.classList.remove('tx-hit');
      void tx.offsetWidth;
      tx.classList.add('tx-hit');
      setTimeout(() => tx.classList.remove('tx-hit'), 600);
      try { window.NT.showToast('REPRINT<i class="hz">重印</i>', 1000); } catch (err) { }
    }, true);

    window.addEventListener('keydown', e => {
      if (e.key !== '[' && e.key !== ']') return;
      reg = Math.max(0.35, Math.min(2.4, reg + (e.key === ']' ? 0.15 : -0.15)));
      document.documentElement.style.setProperty('--reg', reg.toFixed(2));
      try { window.NT.showToast('MISPRINT · ' + reg.toFixed(2) + '×', 1200); } catch (err) { }
    }, { passive: true });

    document.addEventListener('pointerover', e => {
      const tx = e.target && e.target.closest ? e.target.closest('[data-tx]') : null;
      if (!tx) return;
      const now = performance.now();
      if (now - lastHover < 130) return;
      lastHover = now;
      try { window.NT.Audio.sfx('hover'); } catch (err) { }
    }, { passive: true });
  }

  function toggle() {
    const on = !document.body.classList.contains('tx-mono');
    document.body.classList.toggle('tx-mono', on);
    try {
      if (window.NT.showToast) window.NT.showToast(on ? 'MISPRINT OFF · ONE INK<i class="hz">只留一种墨</i>' : 'MISPRINT ON · THREE INKS<i class="hz">三种墨再次错位</i>', 1600);
    } catch (e) { }
    try { window.NT.Audio.sfx('flip'); } catch (e) { }
  }

  /* per-frame, deterministic: all cycling is a pure function of film time */
  function tick(t) {
    if (!booted) return;
    if (!happy) {
      happy = true;
      capT = document.getElementById('capT');
      hudAct = document.getElementById('hudAct');
      cName = document.querySelector('.c-name');
      s11word = document.querySelector('.s11-word');
      s9word = document.querySelector('.s9-word');
    }

    /* the caption changes ink every 2.4 s — a slow colour conversation */
    if (capT) {
      const pal = [INK.plum, INK.berry, INK.crimson, INK.gold];
      const ci = Math.floor(t / 2.4) % pal.length;
      capT.style.color = pal[ci];
    }

    /* the plate label in the HUD shifts with each plate */
    if (hudAct) {
      const pl = [
        [0, INK.berry], [8, INK.crimson], [14, INK.gold], [22, INK.bone],
        [24.5, INK.berry], [33.5, INK.gold], [40, INK.plum]
      ];
      let col = INK.berry;
      for (let i = 0; i < pl.length; i++) if (t >= pl[i][0]) col = pl[i][1];
      hudAct.style.color = col;
    }

    /* the right-hand card name is printed in the ink of the card on show */
    if (cName) {
      const ci = Math.max(0, Math.min(5, Math.floor((t - 24.5) / 1.5)));
      const dark = t >= 22 && t < 24.5;
      cName.style.color = dark ? INK.bone : CARD_INKS[ci];
    }

    /* the brand wordmark breathes off-register and trades inks */
    if (s11word) {
      const inks = [[INK.crimson, INK.gold], [INK.gold, INK.crimson],
                    [INK.crimson, INK.mauve], [INK.gold, INK.mauve]];
      const pal = inks[Math.floor(t / 3.4) % inks.length];
      s11word.style.setProperty('--c1', pal[0]);
      s11word.style.setProperty('--c2', pal[1]);
      const b = Math.sin(t * 0.85) * 1.35;
      s11word.style.setProperty('--bx2', (3.6 + b).toFixed(2) + 'px');
      s11word.style.setProperty('--by2', (2.4 - b * 0.7).toFixed(2) + 'px');
      s11word.style.setProperty('--bx1', (-2.6 - b * 0.6).toFixed(2) + 'px');
      s11word.style.setProperty('--by1', (-1.8 + b * 0.4).toFixed(2) + 'px');
    }

    /* BECOME. drifts its ghost like a slow heartbeat */
    if (s9word) {
      const k = Math.sin(t * 0.6);
      s9word.style.setProperty('--bx1', (-1.6 + k * 1.5).toFixed(2) + 'px');
      s9word.style.setProperty('--by1', (-1.2 - k * 1.1).toFixed(2) + 'px');
    }

    /* colour-shift: the extra impressions trade inks every few seconds */
    if (!cycleEls.length) {
      try {
        cycleEls = [...document.querySelectorAll(
          '.s2-line b, .s3-title em, .s4-big span, .s5-h span, .s8-big span, .s9-word')];
      } catch (e) { cycleEls = []; }
    }
    if (cycleEls.length) {
      const step = Math.floor(t / 2.7);
      for (let i = 0; i < cycleEls.length; i++) {
        const pal = PAL_CYCLES[(step + i) % PAL_CYCLES.length];
        cycleEls[i].style.setProperty('--c1', pal[0]);
        cycleEls[i].style.setProperty('--c2', pal[1]);
      }
    }
  }

  function init() {
    if (booted) return;
    booted = true;
    try { document.documentElement.style.setProperty('--mx', '0'); } catch (e) { }
    build();
    bind();
    window.NT.TextFX = { init, tick, toggle, build };
  }

  return { init, tick, toggle };
})();

/* hand the little press to the rest of the film before boot() runs */
if (window.NT) window.NT.TextFX = TextFX;


