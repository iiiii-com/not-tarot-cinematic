/* ============================================================================
   motion.js — DYNAMIC PASS 2026-10
   Gives the print its own life:
     · ornaments breathe / drift / spin on the individual transform properties
     · the plate chrome is a physical sheet: pointer 3D parallax + gate drift
     · the frame and the big rings suffer chromatic misregistration (色彩错插)
     · each plate change fires a short "misregistration pulse"
     · specimen cells become small glass plates under the pointer

   Every value is a pure function of film time t (and the pointer), so a still
   captured at t is deterministic. In capture mode the organic CSS animations
   are paused and their phase is seeked to t.
   ========================================================================= */
const MotionFX = (() => {
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => Array.from(document.querySelectorAll(s));

  const PLATE_MARKS = [0, 8.0, 14.0, 17.5, 22.0, 24.5, 33.5, 36.0, 40.0, 42.0];

  /* selector → animation flavour */
  const ANIM = [
    ['.corner-orn', 'm-breathe'],
    ['.plate-stamp', 'm-spin'],
    ['.marg', 'm-breathe'],
    ['.dim-lab', 'm-breathe'],
    ['.mk', 'm-tremor'],

    ['.s1-orb', 'm-drift'],
    ['.s1-fleck', 'm-float'],
    ['.s8-deco', 'm-spin'],
    ['.s9-deco', 'm-spinr'],
    ['.s2-pulser', 'm-pulse'],
    ['.s3-deco', 'm-sway'],
    ['.s3-num', 'm-breathe'],
    ['.s4-orb', 'm-float'],
    ['.s4-axis', 'm-sway'],
    ['.s5-frame', 'm-pulse'],
    ['.s5-lat', 'm-breathe'],
    ['.s5-tick', 'm-breathe'],
    ['.s6-fleck', 'm-float'],
    ['.s6-cmark', 'm-breathe'],
    ['.s7-orb', 'm-drift'],
    ['.s8-num', 'm-breathe'],
    ['.s9-num', 'm-breathe'],
    ['.s9-counter', 'm-spinr'],
    ['.s10-conv', 'm-breathe'],
    ['.s10-conv line', 'm-dash'],
    ['.s10-seed', 'm-pulse'],
    ['.s11-cart', 'm-sway'],
    ['.s11-colophon', 'm-breathe'],

    ['.s3-sym', 'm-float'],
    ['.s8-sym', 'm-float'],
    ['.s9-sym', 'm-float'],
    ['.s5-sym', 'm-float']
  ];

  /* elements that print with a chromatic split */
  const ABER = ['#rules', '.s3-ring', '.s8-ring', '.s9-ring', '.s5-frame', '.s11-cart'];
  const ABER_SOFT = ['.plate-stamp'];

  let ready = false;
  let built = false;
  let chromeEl = null;
  let shadowEl = null;
  let stampEl = null;
  let animEls = [];

  /* ------------------------------------------------------------------ build */
  function build() {
    if (built) return;
    built = true;
    chromeEl = $('#chrome');
    shadowEl = $('#plateShadow');
    stampEl = $('.plate-stamp');

    ANIM.forEach(([sel, cls], si) => {
      $$(sel).forEach((el, i) => {
        if (el.classList.contains('m-anim')) return;
        el.classList.add('m-anim', cls);
        const off = (i * 0.63 + si * 1.31) % 7.2;
        el._mOff = off;
        el.style.animationDelay = (-off).toFixed(2) + 's';
        el.style.animationDuration = (4.8 + (i % 6) * 0.7).toFixed(2) + 's';
        animEls.push(el);
      });
    });

    ABER.forEach((sel) => $$(sel).forEach((el) => el.classList.add('aber')));
    ABER_SOFT.forEach((sel) => $$(sel).forEach((el) => el.classList.add('aber-soft')));

    if (window.NT && window.NT.REDUCED) document.body.classList.add('motion-off');
  }

  function clamp(v, a, b) { return v < a ? a : (v > b ? b : v); }

  /* ------------------------------------------------------------ plate pulse */
  function platePulse(t) {
    let v = 0;
    for (let i = 0; i < PLATE_MARKS.length; i++) {
      const d = t - PLATE_MARKS[i];
      if (d >= 0 && d < 1.15) {
        const k = 1 - d / 1.15;
        v = Math.max(v, k * k);
      }
    }
    return v;
  }

  /* ------------------------------------------------------------------- tick */
  function tick(t) {
    if (!ready) return;
    if (!built) build();
    const st = (window.NT && window.NT.ST) || {};
    const ptr = st.ptr || {};
    const px = ptr.nx || 0;
    const py = ptr.ny || 0;
    const pulse = platePulse(t);
    const dr = Math.sin(t * 0.37);
    const dr2 = Math.cos(t * 0.29);
    const off = document.body.classList.contains('motion-off');

    if (chromeEl) {
      if (off) {
        chromeEl.style.transform = '';
      } else {
        const rx = clamp(-py * 1.45 - dr * 0.42 - pulse * 0.55, -2.2, 2.2).toFixed(3);
        const ry = clamp(px * 1.75 + dr2 * 0.48 + pulse * 0.70, -2.6, 2.6).toFixed(3);
        const tx = clamp(-px * 10.0 + Math.sin(t * 0.23) * 2.2 - pulse * 3.0, -12, 12).toFixed(2);
        const ty = clamp(-py * 7.0 + Math.cos(t * 0.19) * 2.0, -9, 9).toFixed(2);
        chromeEl.style.transform =
          'perspective(3000px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg) translate3d(' + tx + 'px,' + ty + 'px,0)';
      }
    }
    if (shadowEl && !off) {
      shadowEl.style.transform = 'translate3d(' + (px * 5.2).toFixed(2) + 'px,' + (py * 3.8).toFixed(2) + 'px,0)';
    }
    if (stampEl && !off) {
      stampEl.style.transform =
        'perspective(760px) rotateX(' + (Math.sin(t * 0.5) * 4.5).toFixed(2) + 'deg) rotateY(' +
        (Math.cos(t * 0.43) * 5.5).toFixed(2) + 'deg)';
    } else if (stampEl) {
      stampEl.style.transform = '';
    }

    /* chromatic misregistration: pointer + slow swell + plate pulse spike */
    const abx = 2.2 + px * 4.6 + dr * 1.9 + pulse * 7.0;
    const aby = 1.6 + py * 3.6 + dr2 * 1.5 + pulse * 5.0;
    const root = document.documentElement.style;
    root.setProperty('--abx', abx.toFixed(2) + 'px');
    root.setProperty('--aby', aby.toFixed(2) + 'px');
    root.setProperty('--mx', px.toFixed(3));
    root.setProperty('--my', py.toFixed(3));

    /* capture: seek every organic animation to film time */
    if (window.NT && window.NT.CAPTURE) {
      const els = animEls;
      for (let i = 0; i < els.length; i++) {
        const el = els[i];
        el.style.animationDelay = (-(t + (el._mOff || 0))).toFixed(2) + 's';
      }
    }
  }

  /* ----------------------------------------------------------------- toggle */
  function toggle() {
    const on = document.body.classList.toggle('motion-off');
    if (window.NT && window.NT.showToast) {
      window.NT.showToast(on ? 'MOTION OFF · STILL PLATE<i class="hz">动态已关闭</i>' : 'MOTION ON · LIVING PLATE<i class="hz">动态已开启</i>');
    }
    if (window.NT && window.NT.Audio && window.NT.Audio.sfx) window.NT.Audio.sfx('hover');
    return on;
  }

  function init() {
    ready = true;
  }

  return { init, tick, toggle, build, phase: () => animEls.length };
})();
if (window.NT) window.NT.MotionFX = MotionFX;
