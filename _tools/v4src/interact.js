/* =====================================================================
   interact.js — everything the visitor can touch
   ===================================================================== */
let toastTimer = 0, hoverSfxAt = 0;
function showToast(msg, ms) {
  toastEl.textContent = msg;
  toastEl.classList.add('on');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toastEl.classList.remove('on'), ms || 2200);
}
function sfx(name) {
  const now = performance.now();
  if (name === 'hover') { if (now - hoverSfxAt < 90) return; hoverSfxAt = now; }
  try { Audio.sfx(name); } catch (e) {}
}

/* ------------------------------------------------------------ custom cursor */
function moveCursor(x, y) {
  cursorEl.style.transform = 'translate(' + x + 'px,' + y + 'px)';
}
stage.addEventListener('pointermove', e => {
  const r = stage.getBoundingClientRect();
  const s = r.width / 1920;
  const x = (e.clientX - r.left) / s, y = (e.clientY - r.top) / s;
  ST.ptr.x = x; ST.ptr.y = y;
  ST.ptr.nx = clamp((x / 1920) * 2 - 1, -1, 1);
  ST.ptr.ny = clamp((y / 1080) * 2 - 1, -1, 1);
  moveCursor(x, y);
  wake();
});
stage.addEventListener('pointerenter', () => document.body.classList.add('cur-on'));
stage.addEventListener('pointerleave', () => {
  document.body.classList.remove('cur-on');
  ST.ptr.nx *= 0.2; ST.ptr.ny *= 0.2;
});
stage.addEventListener('pointerover', e => {
  const hot = e.target.closest('button,.chap,.cwrap,.s5-cell,.p-drop,.hb,.dw-art,.p-plate');
  document.body.classList.toggle('cur-hot', !!hot);
});

/* --------------------------------------------------------------- idle HUD */
let wakeTimer = 0;
function wake() {
  if (CAPTURE) return;
  if (ST.started && !ST.drawOpen && !ST.helpOpen) {
    hudEl.classList.add('on'); hudEl.classList.add('live');
    chaptersEl.classList.add('on');
  }
  clearTimeout(wakeTimer);
  wakeTimer = setTimeout(() => {
    if (ST.playing) { hudEl.classList.remove('on'); chaptersEl.classList.remove('on'); }
  }, 3200);
}

/* ------------------------------------------------------------------ HUD */
const bPlay = $('#bPlay'), playIco = $('#playIco'), bRestart = $('#bRestart'),
      bSound = $('#bSound'), bFull = $('#bFull'), bHelp = $('#bHelp'),
      hudBar = $('#hudBar');

bPlay.addEventListener('click', () => {
  Audio.ensure(); sfx('click');
  if (ST.ended) { restart(); play(); }
  else play();
  syncPlayIcon();
});
bRestart.addEventListener('click', () => { sfx('click'); restart(); syncPlayIcon(); wake(); });
bSound.addEventListener('click', () => {
  const m = Audio.toggleMute();
  ST.muted = m;
  bSound.textContent = m ? 'SOUND OFF' : 'SOUND ON';
  bSound.classList.toggle('off', m);
  if (!m) { sfx('click'); Audio.start(); }
});
bFull.addEventListener('click', toggleFull);
bHelp.addEventListener('click', () => { sfx('click'); toggleHelp(); });

function syncPlayIcon() {
  playIco.textContent = ST.playing ? '❚❚' : '▶';
}
function toggleFull() {
  try {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen();
    else document.exitFullscreen();
  } catch (e) { showToast('FULLSCREEN UNAVAILABLE'); }
}

/* -------------------------------------------------------------- scrubber */
let scrubbing = false;
function barRect() { return hudBar.getBoundingClientRect(); }
function seekFromEvent(e) {
  const r = barRect();
  const k = clamp01((e.clientX - r.left) / r.width);
  seek(k * DUR);
  if (ST.held !== undefined) {}
  if (ST.ended) {}
  syncPlayIcon();
  return k;
}
hudBar.addEventListener('pointerdown', e => {
  scrubbing = true; hudBar.setPointerCapture(e.pointerId);
  seekFromEvent(e); Audio.ensure();
});
hudBar.addEventListener('pointermove', e => {
  const r = barRect();
  const k = clamp01((e.clientX - r.left) / r.width);
  const t = k * DUR;
  let plate = PLATES[0];
  for (const p of PLATES) if (t >= p.t) plate = p;
  hudTip.textContent = fmtTime(t) + ' · ' + plate.roman + ' · ' + plate.title;
  hudTip.style.left = (k * 100).toFixed(2) + '%';
  if (scrubbing) seekFromEvent(e);
});
hudBar.addEventListener('pointerup', e => { scrubbing = false; try { hudBar.releasePointerCapture(e.pointerId); } catch (err) {} });
hudBar.addEventListener('pointercancel', () => { scrubbing = false; });

/* ---------------------------------------------------------------- chapters */
PLATES.forEach((p, i) => {
  const c = mk('button', 'chap', chaptersEl);
  c.setAttribute('aria-label', 'Chapter ' + p.roman + ' — ' + p.title);
  mk('span', 'cn', c, p.roman + ' · ' + p.title);
  c.addEventListener('click', e => {
    e.stopPropagation();
    sfx('click');
    if (!ST.started) startFilm(false);
    seek(Math.max(0.02, p.t));
    wake();
  });
  c.addEventListener('pointerenter', () => sfx('hover'));
});

/* ------------------------------------------------------------------ hold */
let holdTimer = 0, holdRaf = 0, holdStart = 0;
const holdCircle = holdRing.querySelector('circle');
function beginHoldCandidate(e) {
  if (!ST.playing) return;
  if (e.target.closest('button,.cwrap,.chap,hudBar,#hud,.p-drop')) return;
  clearTimeout(holdTimer);
  holdTimer = setTimeout(() => {
    ST.hold = true; holdStart = performance.now();
    holdRing.classList.add('on');
    document.body.classList.add('cur-drag');
    sfx('slow');
    const tick = () => {
      if (!ST.hold) return;
      const k = clamp01((performance.now() - holdStart) / 1400);
      holdCircle.style.strokeDashoffset = String(289 * (1 - k));
      holdRaf = requestAnimationFrame(tick);
    };
    tick();
  }, 220);
}
function endHold() {
  clearTimeout(holdTimer);
  if (ST.hold) {
    ST.hold = false;
    holdRing.classList.remove('on');
    document.body.classList.remove('cur-drag');
    cancelAnimationFrame(holdRaf);
    holdCircle.style.strokeDashoffset = '289';
  }
}
stage.addEventListener('pointerdown', beginHoldCandidate);
window.addEventListener('pointerup', endHold);
window.addEventListener('blur', endHold);

/* every touch of the paper leaves a wet ink mark */
stage.addEventListener('pointerdown', e => {
  if (!ST.started) return;
  if (e.target.closest('button,.chap,.hb,#hud,hudBar,#drawer,#help,#poster,.cwrap,.dw-close,.hp')) return;
  if (ST.ptr.x != null) inkPing(ST.ptr.x, ST.ptr.y);
}, true);

/* ------------------------------------------------------------------ cards */
stage.addEventListener('click', e => {
  const w = e.target.closest('.cwrap');
  if (w) {
    const i = +w.dataset.card;
    const face = w.querySelector('.cface');
    const flipped = face.dataset.flipped === '1';
    face.dataset.flipped = flipped ? '0' : '1';
    face.style.transform = flipped ? 'rotateY(0deg)' : 'rotateY(180deg)';
    ST.flipped = !flipped;
    inkPing(ST.ptr.x != null ? ST.ptr.x : 720, ST.ptr.y != null ? ST.ptr.y : 520, true);
    sfx('flip');
    return;
  }
});
stage.addEventListener('pointermove', e => {
  const w = e.target.closest('.cwrap');
  if (!w) return;
  const face = w.querySelector('.cface');
  if (!face || face.dataset.flipped === '1') return;
  const r = w.getBoundingClientRect();
  if (!r.width) return;
  const nx = clamp(((e.clientX - r.left) / r.width) * 2 - 1, -1, 1);
  const ny = clamp(((e.clientY - r.top) / r.height) * 2 - 1, -1, 1);
  face.style.transform = 'rotateX(' + (-ny * 5.5).toFixed(2) + 'deg) rotateY(' + (nx * 6.5).toFixed(2) + 'deg)';
});
stage.addEventListener('pointerout', e => {
  const w = e.target.closest('.cwrap');
  if (!w) return;
  const face = w.querySelector('.cface');
  if (face && face.dataset.flipped !== '1') face.style.transform = 'rotateY(0deg)';
});
stage.addEventListener('wheel', e => {
  if (ST.t >= 22.0 && ST.t < SIX_START - 0.4) {
    e.preventDefault();
    sfx('draw');
    if (!ST.playing) { play(); syncPlayIcon(); }
    seek(SIX_START + 0.35);
    return;
  }
  if (ST.t < SIX_START - 0.4 || ST.t > 33.6) return;
  e.preventDefault();
  const cur = NT.S7.activeAt(ST.t);
  const next = clamp(cur + (e.deltaY > 0 ? 1 : -1), 0, 5);
  if (next !== cur) { sfx('draw'); seek(NT.S7.startOf(next) + 0.35); }
}, { passive: false });

/* --------------------------------------------------------------- eye region */
/* pupil follows through ST.ptr (read in S4.upd) — no extra wiring needed */

/* ----------------------------------------------------------------- poster */
let posterBuilt = false;
function buildPoster() {
  if (posterBuilt) return;
  posterBuilt = true;
  paperBg(posterEl, 'cream');
  const wrap = mk('div', 'p-wrap', posterEl);
  mk('div', 'p-top', wrap,
    '<span>NOT TAROT · EDITION 01</span><span>AN INK STUDY IN SEVEN PLATES</span><span>MMXXVI</span>');
  const main = mk('div', 'p-main', wrap);
  const left = mk('div', 'p-left', main);
  mk('div', 'p-kicker', left, 'A FILM ABOUT SIGNS · 45 SECONDS');
  mk('h1', 'p-title', left, '<span>NOT</span><span>TAROT</span>');
  mk('div', 'p-rule', left, '<i></i>');
  mk('p', 'p-lede', left,
    'A single ink becomes a heart, a heart becomes a language, and the language learns to hold you. ' +
    '<b>Nothing here predicts anything.</b> Everything here means something — because you say so.');
  const drop = mk('div', 'p-drop', left);
  const dr = mk('div', 'p-drop-ring', drop, '<div class="p-drop-dot"></div>');
  mk('div', 'p-drop-hint', drop, '<b>Drag the drop — or click anywhere</b><span>SOUND ON · HEADPHONES RECOMMENDED</span>');
  const right = mk('div', 'p-right', main);
  const plate = mk('figure', 'p-plate', right);
  mk('div', 'p-plate-art', plate);
  const art = plate.querySelector('.p-plate-art');
  bg(art, 'heart', 'berry');
  mk('div', 'p-corner c1', plate); mk('div', 'p-corner c2', plate);
  mk('div', 'p-corner c3', plate); mk('div', 'p-corner c4', plate);
  const cap = mk('figcaption', null, plate, '<span>FIG. I - COR</span>');
  mk('div', 'p-side', right, 'NOT TAROT — AN INK STUDY IN SEVEN PLATES');
  mk('div', 'p-stamp', right, 'NOT<br>TAROT');
  mk('div', 'p-bot', wrap,
    '<span>EDITION 01 · 07 PLATES</span><span class="p-sep">◆</span>' +
    '<span>DRAG THE DROP TO BEGIN</span><span class="p-sep">◆</span><span>45S · 1 INK</span>');

  /* drag the drop */
  const dot = dr.querySelector('.p-drop-dot');
  let drag = null;
  dr.addEventListener('pointerdown', e => {
    e.preventDefault();
    Audio.ensure();
    drop.classList.add('dragging');
    const r = stage.getBoundingClientRect();
    const s = r.width / 1920;
    drag = { x: e.clientX, y: e.clientY, r, s };
    dr.setPointerCapture(e.pointerId);
  });
  dr.addEventListener('pointermove', e => {
    if (!drag) return;
    dot.style.transform = 'translate(' + ((e.clientX - drag.x) / drag.s).toFixed(1) + 'px,' +
      ((e.clientY - drag.y) / drag.s).toFixed(1) + 'px) scale(' + (1 + Math.min(0.6, Math.hypot(e.clientX - drag.x, e.clientY - drag.y) / 400)) + ')';
  });
  dr.addEventListener('pointerup', e => {
    if (!drag) return;
    const moved = Math.hypot(e.clientX - drag.x, e.clientY - drag.y);
    drag = null;
    drop.classList.remove('dragging');
    dot.style.transform = '';
    sfx('drop');
    startFilm(true, moved > 60);
  });
  posterEl.addEventListener('click', e => {
    if (e.target.closest('.p-drop')) return;
    sfx('click');
    startFilm(true, false);
  });
  posterEl.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); startFilm(true, false); }
  });
}

/* -------------------------------------------------------------- start film */
let startedOnce = false;
function startFilm(drop, dragged) {
  if (ST.started) return;
  Audio.ensure();
  posterEl.classList.add('gone');
  document.body.classList.remove('poster');
  ST.started = true;
  if (!startedOnce) {
    startedOnce = true;
    seek(0);
    setTimeout(() => play(), 90);
  } else if (drop) { seek(0); play(); }
  syncPlayIcon();
  wake();
  if (dragged) showToast('THE DROP IS IN THE INK NOW');
  else showToast('EVERYTHING MEANS SOMETHING');
}

/* ----------------------------------------------------------------- drawer */
let drawerBuilt = false;
const drawer = $('#drawer');
let lastDraw = -1;
function buildDrawer() {
  if (drawerBuilt) return;
  drawerBuilt = true;
  const dw = mk('div', 'dw', drawer);
  paperBg(dw, 'cream');
  const art = mk('div', 'dw-art', dw);
  mk('div', 'sym', art);
  mk('div', 'dw-no', art);
  mk('div', 'dw-latin', art);
  const txt = mk('div', 'dw-txt', dw);
  mk('div', 'dw-kick', txt, 'YOUR CARD · DRAWN FROM THE DECK');
  mk('h2', 'dw-name', txt);
  mk('div', 'dw-latin2', txt);
  mk('div', 'dw-sep', txt);
  mk('p', 'dw-mean', txt);
  mk('p', 'dw-zh', txt);
  const btns = mk('div', 'dw-btns', txt,
    '<button class="hb primary" data-act="again">DRAW AGAIN</button>' +
    '<button class="hb" data-act="save">SAVE THE CARD</button>' +
    '<button class="hb" data-act="close">CLOSE</button>');
  mk('div', 'dw-close', dw, '✕');
  btns.addEventListener('click', e => {
    const act = e.target.closest('[data-act]');
    if (!act) return;
    sfx('click');
    if (act.dataset.act === 'again') drawCard();
    else if (act.dataset.act === 'save') saveCard();
    else closeDrawer();
  });
  dw.querySelector('.dw-close').addEventListener('click', closeDrawer);
  drawer.addEventListener('click', e => { if (e.target === drawer) closeDrawer(); });
}
function drawCard(force) {
  buildDrawer();
  const i = force != null ? force : Math.floor(Math.random() * CARDS.length);
  lastDraw = i;
  const c = CARDS[i];
  const art = drawer.querySelector('.dw-art .sym');
  art.style.backgroundImage = 'url("' + url(c.sym, 'berry') + '")';
  drawer.querySelector('.dw-no').textContent = 'No. ' + String(i + 1).padStart(2, '0') + ' / 06';
  drawer.querySelector('.dw-latin').textContent = c.latin;
  drawer.querySelector('.dw-name').textContent = c.name;
  drawer.querySelector('.dw-latin2').textContent = c.latin + ' · ' + c.fig.replace('FIG. ', 'FIG. ');
  drawer.querySelector('.dw-mean').textContent = '“' + c.en + '”';
  drawer.querySelector('.dw-zh').textContent = c.zh;
  drawer.classList.add('on');
  drawer.setAttribute('aria-hidden', 'false');
  ST.drawOpen = true;
  try { Audio.sfx('draw'); } catch (e) {}
}
function closeDrawer() {
  drawer.classList.remove('on');
  drawer.setAttribute('aria-hidden', 'true');
  ST.drawOpen = false;
}
function saveCard() {
  const c = CARDS[lastDraw >= 0 ? lastDraw : 0];
  try {
    const cv = document.createElement('canvas');
    cv.width = 900; cv.height = 1280;
    const g = cv.getContext('2d');
    g.fillStyle = '#FAF2EC'; g.fillRect(0, 0, 900, 1280);
    g.strokeStyle = '#8F2C3B'; g.lineWidth = 3; g.strokeRect(44, 44, 812, 1192);
    g.lineWidth = 1; g.strokeStyle = 'rgba(36,31,34,.35)'; g.strokeRect(62, 62, 776, 1156);
    const img = new Image();
    img.onload = () => {
      g.drawImage(img, 230, 250, 440, 440);
      g.textAlign = 'center';
      g.fillStyle = '#241F22';
      g.font = '600 54px "Cormorant Garamond", Georgia, serif';
      g.fillText(c.name, 450, 790);
      g.fillStyle = '#8F2C3B';
      g.font = 'italic 26px "EB Garamond", Georgia, serif';
      g.fillText(c.latin, 450, 840);
      g.fillStyle = 'rgba(36,31,34,.9)';
      wrap(g, c.en, 450, 920, 640, 30, 'italic 25px "EB Garamond", Georgia, serif');
      g.fillStyle = '#8F2C3B';
      g.font = '22px "Cormorant Garamond", Georgia, serif';
      wrap(g, c.zh, 450, 1040, 640, 34, '22px "Cormorant Garamond", Georgia, serif');
      g.fillStyle = 'rgba(36,31,34,.55)';
      g.font = '13px Jost, sans-serif';
      g.fillText('NOT TAROT · MAKE YOUR OWN MEANING.', 450, 1150);
      const a = document.createElement('a');
      a.download = 'not-tarot-' + c.name.toLowerCase().replace(/\s+/g, '-') + '.png';
      a.href = cv.toDataURL('image/png');
      a.click();
      showToast('CARD SAVED');
    };
    img.onerror = () => showToast('SAVE UNAVAILABLE');
    img.src = url(c.sym, 'berry');
  } catch (e) { showToast('SAVE UNAVAILABLE'); }
}
function wrap(g, text, x, y, maxW, lh, font) {
  g.font = font;
  const words = text.split(' ');
  let line = '', yy = y;
  for (const w of words) {
    const test = line ? line + ' ' + w : w;
    if (g.measureText(test).width > maxW && line) { g.fillText(line, x, yy); line = w; yy += lh; }
    else line = test;
  }
  if (line) g.fillText(line, x, yy);
}

/* ------------------------------------------------------------------- help */
const help = $('#help');
let helpBuilt = false;
function buildHelp() {
  if (helpBuilt) return;
  helpBuilt = true;
  const hp = mk('div', 'hp', help);
  paperBg(hp, 'cream');
  mk('h3', null, hp, 'HOW TO READ THE PLATES');
  mk('div', 'hp-sub', hp, 'A silent film you can touch.');
  const grid = mk('div', 'hp-grid', hp);
  const rows = [
    ['Play / pause', 'SPACE'], ['Seek ± 2 s', '← →'],
    ['Restart the film', 'HOME'], ['Mute the room', 'M'],
    ['Fullscreen', 'F'], ['Hold to breathe (0.34×)', 'HOLD'],
    ['Turn a card over', 'CLICK CARD'], ['Pass through the deck', 'WHEEL'],
    ['Draw your own card', 'CLICK AT THE END'], ['Silence the cursor', 'ESC'],
    ['Jump to a plate', '1 \u2013 7'], ['Name a sign', 'HOVER'],
  ];
  rows.forEach(([a, b]) => {
    const r = mk('div', 'hp-row', grid, '<span>' + a + '</span><kbd>' + b + '</kbd>');
  });
  mk('div', 'hp-note', hp, 'Drag the drop on the title plate to begin. The film runs 45 seconds; ' +
    'after the wordmark, click anywhere to draw a card of your own.');
  mk('div', 'dw-close', hp, '✕').addEventListener('click', () => toggleHelp(false));
  help.addEventListener('click', e => { if (e.target === help) toggleHelp(false); });
}
function toggleHelp(force) {
  buildHelp();
  const open = force != null ? force : !ST.helpOpen;
  ST.helpOpen = open;
  help.classList.toggle('on', open);
  help.setAttribute('aria-hidden', open ? 'false' : 'true');
  if (open) pause();
}

/* click the blind deck → throw the deck forward */
stage.addEventListener('click', e => {
  if (!ST.started || ST.drawOpen || ST.helpOpen) return;
  if (ST.t >= 22.0 && ST.t < SIX_START - 0.4) {
    if (e.target.closest('button,.chap,.hb,hudBar,#hud,#drawer,#help,#poster')) return;
    if (!ST.playing) { play(); syncPlayIcon(); }
    inkPing(ST.ptr.x != null ? ST.ptr.x : 720, ST.ptr.y != null ? ST.ptr.y : 520, true);
    sfx('draw');
    seek(SIX_START + 0.35);
    return;
  }
});

/* click anywhere at the end → draw a card */
stage.addEventListener('click', e => {
  if (!ST.started || ST.drawOpen || ST.helpOpen) return;
  if (ST.t >= 42.0 && !e.target.closest('button,.chap,.hb,hudBar,#hud,.cwrap')) {
    drawCard();
  }
});
hudEl.addEventListener('click', e => { if (e.target.closest('#hud')) e.stopPropagation(); });

/* ------------------------------------------------------------------ keys */
window.addEventListener('keydown', e => {
  const k = e.key;
  if (k === 'Escape') {
    if (ST.drawOpen) { closeDrawer(); return; }
    if (ST.helpOpen) { toggleHelp(false); return; }
    document.body.classList.remove('cur-on');
    return;
  }
  if (!ST.started && (k === ' ' || k === 'Enter')) { e.preventDefault(); startFilm(true, false); return; }
  if (k === ' ') { e.preventDefault(); if (ST.helpOpen) toggleHelp(false); else { play(); syncPlayIcon(); } }
  else if (k === 'ArrowRight') { e.preventDefault(); seek(ST.t + 2); syncPlayIcon(); wake(); }
  else if (k === 'ArrowLeft') { e.preventDefault(); seek(ST.t - 2); syncPlayIcon(); wake(); }
  else if (k === 'Home') { e.preventDefault(); restart(); syncPlayIcon(); }
  else if (k === 'm' || k === 'M') { bSound.click(); }
  else if (k === 'f' || k === 'F') { toggleFull(); }
  else if (k === '?' || k === '/') { toggleHelp(); }
  else if (k === 'd' || k === 'D') { if (ST.started) drawCard(); }
});

/* ------------------------------------------------------------- field hovers */
document.addEventListener('pointerover', e => {
  const cell = e.target.closest('.s5-cell');
  if (cell && cell.dataset.sym) {
    ST.hoverSym = cell.dataset.sym;
    if (NT.S5) NT.S5.setHover(cell.dataset.sym);
    sfx('hover');
    return;
  }
  if (ST.hoverSym && !e.target.closest('.s5-grid')) {
    ST.hoverSym = null;
    if (NT.S5) NT.S5.setHover('heart');
  }
  const cw = e.target.closest('.cwrap');
  if (cw) sfx('hover');
});
/* keyboard accessibility for the title plate */
document.addEventListener('pointerdown', () => { document.body.classList.remove('poster'); }, { once: false });

/* leave the film at the poster state on first load */
document.body.classList.add('poster');
