/* =====================================================================
   boot.js — fit the plate to the window, load the types, start the clock
   ===================================================================== */

function fit() {
  const vw = window.innerWidth, vh = window.innerHeight;
  let s = Math.min(vw / 1920, vh / 1080);
  if (VERTICAL) s = Math.min(vw / 1920, vh / 1920);
  document.documentElement.style.setProperty('--s', s.toFixed(5));
  document.documentElement.style.setProperty('--vh', (1080 * s).toFixed(2) + 'px');
}

const FONT_SPECS = [
  '400 20px "Cormorant Garamond"', '500 20px "Cormorant Garamond"', '600 20px "Cormorant Garamond"',
  'italic 400 20px "Cormorant Garamond"',
  '400 20px "EB Garamond"', 'italic 400 20px "EB Garamond"',
  '300 20px Jost', '400 20px Jost',
  '400 20px "IM Fell English SC"',
  '500 20px "Playfair Display"', '600 20px "Playfair Display"'
];
function loadFonts() {
  const jobs = FONT_SPECS.map(f => {
    try { return document.fonts.load(f, 'NOTTAROT 0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ'); } catch (e) { return Promise.resolve(); }
  });
  return Promise.race([
    Promise.all(jobs),
    new Promise(res => setTimeout(res, 2600))
  ]).then(() => { try { return document.fonts.ready; } catch (e) { return null; } });
}

function boot() {
  document.documentElement.addEventListener('resize', fit);
  if (VERTICAL) document.body.classList.add('vertical');
  if (CAPTURE) { document.body.classList.add('capture'); document.body.classList.remove('poster'); }
  fit();
  // scenes are declared before their references exist; build them once now
  SCENES.forEach((c, i) => {
    try { if (c.build) c.build(c.node, c); }
    catch (e) { console.error('scene build failed @' + c.t0, e); }
  });
  try { buildPoster(); } catch (e) { console.warn(e); }
  try { if (window.NT.TextFX) window.NT.TextFX.init(); } catch (e) { console.warn(e); }
  try { if (window.NT.MotionFX) window.NT.MotionFX.init(); } catch (e) { console.warn(e); }

  const firstT = FIXED_T != null ? FIXED_T : 0;
  render(firstT);
  if (FIXED_T != null) {
    posterEl.classList.add('gone');
    document.body.classList.remove('poster');
    ST.started = true;
  }
  if (!CAPTURE) {
    syncPlayIcon();
    if (ST.started) wake();
    else { hudEl.classList.remove('on'); chaptersEl.classList.remove('on'); }
  } else {
    hudEl.classList.remove('on');
    chaptersEl.classList.remove('on');
    if (window.NT.Audio) window.NT.Audio.stopAll();
  }

  loadFonts().then(() => {
    render(ST.t);
    requestAnimationFrame(() => {
      render(ST.t);
      window.__rendered = true;
    });
  });

  // expose a couple of helpers to the capture pipeline
  window.__vertical = !!VERTICAL;
}

window.__rendered = false;
try { boot(); } catch (err) { console.error(err); window.__rendered = true; }

/* close the shared IIFE opened in core.js */
})();
