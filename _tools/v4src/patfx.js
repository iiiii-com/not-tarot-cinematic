/* =====================================================================
   patfx.js — type × pattern interaction layer
   The engraved signs are printed *into* the big English letters, and the
   sign you hover on the plate swaps both the texture and the brush
   annotation that rides beside the word.

   deterministic: every animated value is a pure function of t.
   ===================================================================== */

const PatFX = (() => {
  'use strict';

  /* selector, default sprite, tint — one entry per headline */
  const TARGETS = [
    ['.s1-big',        'heart',     'berry'],
    ['.s2-line b',     'heart',     'berry'],
    ['.s3-title',      'star',      'crimson'],
    ['.s4-big',        'eye',       'berry'],
    ['.s5-h',          'compass',   'berry'],
    ['.s6-big',        'eye_tears', 'bone'],
    ['.c-name',        'butterfly', 'berry'],
    ['.s8-big',        'crown',     'gold'],
    ['.s9-word',       'butterfly', 'berry'],
    ['.s10-word',      'heart',     'plum'],
    ['.s11-word',      'crown',     'berry'],
    ['.p-title',       'heart',     'berry']
  ];

  const SIGN_SEL = '.s3-sym,.s8-sym,.s9-sym,.s5-cell';
  const MORPHS = ['butterfly', 'flower', 'heart', 'crown', 'eye'];

  const entries = [];
  let built = false;
  let curSign = null, curEntry = null, curEl = null, curAnno = '';

  function pos(el) { return { x: parseFloat(el.style.left || 0), y: parseFloat(el.style.top || 0) }; }

  function build() {
    built = true;
    if (!window.NT) return;
    TARGETS.forEach(([sel, sym, ink]) => {
      let list;
      try { list = document.querySelectorAll(sel); } catch (e) { return; }
      list.forEach(el => {
        if (el.dataset.pat === '1') return;
        el.dataset.pat = '1';
        el.classList.add('pat-host');
        const layer = document.createElement('span');
        layer.className = 'pat-layer';
        layer.setAttribute('aria-hidden', 'true');
        layer.innerHTML = el.innerHTML;
        el.appendChild(layer);
        entries.push({ el, layer, sym, ink });
      });
    });
    bind();
    if (entries.length) console.log('[patfx] types × patterns:', entries.length);
  }

  function activeIndex(t) {
    for (let i = T.length - 1; i >= 0; i--) if (t >= T[i][0]) return i;
    return 0;
  }

  function sceneOf(el) {
    const node = el.closest ? el.closest('.scene') : null;
    return node || null;
  }

  function activeSceneNode() {
    const i = activeIndex(ST.t);
    return SCENES[i] && SCENES[i].node ? SCENES[i].node : null;
  }

  /* -------- the sign under the pointer swaps annotation + texture ---- */
  function setSign(sym) {
    clearSign();
    if (!sym) return;
    const node = activeSceneNode();
    if (!node) return;
    const hit = entries.find(e => sceneOf(e.el) === node);
    if (!hit) return;
    curSign = sym; curEntry = hit;
    hit.el.classList.add('pat-hot');
    hit.layer.style.backgroundImage = 'url("' + url(sym, 'crimson') + '")';
  }

  function clearSign() {
    if (curEntry) {
      curEntry.el.classList.remove('pat-hot');
      curEntry.layer.style.backgroundImage = 'url("' + url(curEntry.sym, curEntry.ink) + '")';
    }
    curSign = null; curEntry = null;
  }

  function bind() {
    const stage = document.getElementById('stage') || document.body;
    stage.addEventListener('pointerover', e => {
      const s = e.target && e.target.closest ? e.target.closest(SIGN_SEL) : null;
      if (s) {
        const sym = s.dataset.sym || s.dataset.name;
        if (sym && sym !== curSign) setSign(sym);
      }
    });
    stage.addEventListener('pointerout', e => {
      const s = e.target && e.target.closest ? e.target.closest(SIGN_SEL) : null;
      if (s && curSign) clearSign();
    });
    stage.addEventListener('pointerdown', () => {
      if (curEntry) { try { window.NT.Audio && window.NT.Audio.sfx && window.NT.Audio.sfx('hover'); } catch (e2) { } }
    }, true);
  }

  /* ------------------------------- tick ------------------------------ */
  function backgroundFor(entry, t) {
    let sym = entry.sym, ink = entry.ink;
    if (entry.el.classList.contains('c-name') && window.NT.S7) {
      const c = window.NT.S7.cards && window.NT.S7.cards[Math.max(0, window.NT.S7.card || 0)];
      if (c && c.sym) sym = c.sym;
      ink = 'berry';
    } else if (entry.el.classList.contains('s9-word')) {
      const i = Math.floor((t - 36) / 0.55);
      sym = MORPHS[((i % MORPHS.length) + MORPHS.length) % MORPHS.length];
      ink = 'berry';
    } else if (entry.el.classList.contains('s11-word')) {
      const i = Math.floor((t - 42) / 1.6);
      sym = ['crown', 'heart', 'eye'][((i % 3) + 3) % 3];
      ink = 'berry';
    }
    return { sym, ink };
  }

  function tick(t) {
    if (!built) build();
    if (!entries.length) return;
    const node = activeSceneNode();
    for (let k = 0; k < entries.length; k++) {
      const e = entries[k];
      const inScene = node && sceneOf(e.el) === node;
      if (!inScene) { if (e.layer.style.opacity !== '0') e.layer.style.opacity = '0'; continue; }
      const bg = backgroundFor(e, t);
      const urlStr = 'url("' + url(bg.sym, bg.ink) + '")';
      if (e.layer.dataset.bg !== urlStr) {
        e.layer.dataset.bg = urlStr;
        e.layer.style.backgroundImage = urlStr;
      }
      const breathe = 0.13 + 0.055 * Math.sin(t * 1.65 + k * 1.3);
      e.layer.style.opacity = (e === curEntry ? 0.34 : breathe).toFixed(3);
      if (!e.layer.dataset.move) { e.layer.dataset.move = '1'; }
      e.layer.style.backgroundPosition =
        Math.round((t * 9 + k * 37) % 132) + 'px ' + Math.round((t * 6 + k * 23) % 132) + 'px';
    }
  }

  return { tick, build };
})();

if (window.NT) window.NT.PatFX = PatFX;
