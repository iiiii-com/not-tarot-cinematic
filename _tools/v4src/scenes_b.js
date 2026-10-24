/* =====================================================================
   scenes_b.js — plates IV–VII · the deck, the draw, the totem, the seal, the name
   ===================================================================== */

const CARDS = [
  { sym: 'tiger', name: 'FEARLESS', latin: 'TIGRIS', fig: 'FIG. 6 — SORS',
    en: 'Fear is not the enemy. It is proof you are still alive.',
    zh: '恐惧不是敌人，是你还活着的证据。' },
  { sym: 'arch', name: 'LET GO', latin: 'ARCUS', fig: 'FIG. 7 — SORS',
    en: 'Letting go is a doorway, not a loss.',
    zh: '松开不是失去，是走过去。' },
  { sym: 'butterfly', name: 'BECOME', latin: 'PAPILIO', fig: 'FIG. 8 — SORS',
    en: 'You are becoming something that has not learned its name yet.',
    zh: '你正在成为的，还没学会名字。' },
  { sym: 'eye_tears', name: 'SEE CLEARLY', latin: 'OCULUS', fig: 'FIG. 9 — SORS',
    en: 'Seeing clearly is not seeing more. It is refusing to pretend.',
    zh: '看清不是看见，是不再假装。' },
  { sym: 'candle', name: 'CREATE', latin: 'CANDELA', fig: 'FIG. 10 — SORS',
    en: 'To make is to strike one small light and refuse the dark.',
    zh: '创造是划亮一根小火，拒绝黑暗。' },
  { sym: 'unicorn', name: 'GET SHIT DONE', latin: 'UNICORNIS', fig: 'FIG. 11 — SORS',
    en: 'Even unicorns know that a horn is not a plan. Move.',
    zh: '独角兽也知道，光有角不够，还得往前走。' },
];
const SIX_START = 24.5, CARD_LEN = 1.5;

/* ============================================================ IV — THE DECK */
const S6 = scene(22.0, 24.5, (node) => {
  // ink flood (two irregular masks, growing)
  const ink1 = mk('div', 's6-ink', node);
  const ink2 = mk('div', 's6-ink b', node);
  ink1.style.webkitMaskImage = ink2.style.webkitMaskImage = '';
  ink1.style.maskImage = 'url("' + TX.ink_0 + '")';
  ink1.style.webkitMaskImage = 'url("' + TX.ink_0 + '")';
  ink2.style.maskImage = 'url("' + TX.ink_1 + '")';
  ink2.style.webkitMaskImage = 'url("' + TX.ink_1 + '")';
  ink2.style.opacity = '0.85';

  // tear line
  const svg = svgEl('svg', { viewBox: '0 0 1920 1080', class: 's6-tear' }, node);
  const path = svgEl('path', {}, svg);
  const rnd = mulberry(77);
  let d = 'M930 -10';
  for (let y = 0, x = 930; y <= 1100; y += 42) {
    x += (rnd() - 0.5) * 26;
    d += ' L' + (x + (rnd() - 0.5) * 8).toFixed(1) + ' ' + y;
  }
  path.setAttribute('d', d);
  const TL = Math.ceil(path.getTotalLength());
  path.style.strokeDasharray = TL; path.style.strokeDashoffset = TL;

  // dust suspended in the ink
  const dust = makeDust(node, 56, 21, null, 'bone');

  // ghost numeral + the rest of the deck, face down
  const num = mk('div', 's6-num', node, 'LII');
  const pile = [mk('div', 's6-pile p1', node), mk('div', 's6-pile p2', node)];

  // the deck card (blank, blind-embossed)
  const card = mk('div', 's6-card', node);
  const hw = mk('div', 's6-hw', card); bg(hw, 'heart', 'bone');
  mk('div', 's6-ln', card);
  mk('div', 's6-cap', card, 'NON EST TAROT');

  const copy = mk('div', 's6-copy', node);
  mk('div', 'kick', copy, 'THE DRAWING');
  mk('h1', 's6-big', copy, 'THE<span>DECK.</span>');
  const rule = mk('div', 's6-rule', copy, '<i class="hl"></i><i class="dia"></i>');
  mk('p', 's6-lede', copy, 'Fifty-two ways to say what you already knew.<br>None of them decided for you.');
  const pull = mk('div', 's6-pull', node, '<span>PULL</span><i></i>');
  mk('div', 's6-vert', node, 'A CARD IS A QUESTION YOU CAN HOLD');
  mk('div', 's6-corner tl', node); mk('div', 's6-corner br', node);

  S6.upd = (local, dur) => {
    const flood = E.outC(wt(local, 0.05, 0.85));
    const sz = lerp(260, 5200, flood);
    [ink1, ink2].forEach((el, i) => {
      const m = 'url("' + TX['ink_' + (i === 0 ? 0 : 1)] + '")';
      el.style.maskImage = m; el.style.webkitMaskImage = m;
      el.style.maskSize = (sz * (i === 0 ? 1 : 0.86)).toFixed(0) + 'px ' + (sz * (i === 0 ? 1 : 0.86)).toFixed(0) + 'px';
      el.style.maskPosition = '50% 48%';
      el.style.webkitMaskSize = el.style.maskSize;
      el.style.webkitMaskPosition = el.style.maskPosition;
      el.style.opacity = i === 0 ? '1'
        : String(E.outC(wt(local, 0.15, 1.0)) * 0.8 * (1 - E.inOut(wt(local, 1.05, 1.75))));
    });
    // tear
    path.style.strokeDashoffset = String(TL * (1 - E.inOut(wt(local, 0.55, 1.35))));
    // card enters, the rest of the deck settles behind it
    const ck = E.outBack(wt(local, 0.9, 1.55));
    card.style.opacity = String(E.outC(wt(local, 0.9, 1.25)));
    card.style.transform = 'translateY(' + ((1 - ck) * 52).toFixed(1) + 'px) rotate(' + ((1 - ck) * -1.4).toFixed(2) + 'deg)';
    pile.forEach((el, i) => {
      const pk = E.outBack(wt(local, 1.0 + i * 0.09, 1.62 + i * 0.09));
      el.style.opacity = String(pk * (0.9 - i * 0.25));
      el.style.transform = 'translate(' + ((1 - pk) * (30 + i * 16)).toFixed(1) + 'px,' + ((1 - pk) * (44 + i * 22)).toFixed(1) + 'px)';
    });
    num.style.opacity = String(E.outC(wt(local, 0.55, 1.4)) * 0.075);
    num.style.transform = 'translateX(' + ((1 - E.outC(wt(local, 0.55, 1.4))) * 40).toFixed(1) + 'px)';
    hw.style.opacity = String(0.12 + E.outC(wt(local, 1.2, 1.9)) * 0.17);
    // type
    copy.style.opacity = String(E.outC(wt(local, 1.1, 1.8)));
    copy.style.transform = 'translateX(' + ((1 - E.outC(wt(local, 1.1, 1.9))) * 26).toFixed(1) + 'px)';
    rule.style.transform = 'scaleX(' + E.outC(wt(local, 1.3, 2.0)).toFixed(3) + ')';
    rule.style.transformOrigin = '0 50%';
    pull.style.opacity = String(E.outC(wt(local, 1.6, 2.1)) * 0.9);
    driftDust(dust, local, 8);
    S6.cam = { s: 1 + E.outC(wt(local, 0, 2.5)) * 0.03, x: 960, y: 520 };
  };
});

/* ============================================================ V — THE DRAW */
const S7 = scene(SIX_START, 33.5, (node) => {
  const halo = mk('div', 's7-halo', node);
  const cwraps = CARDS.map((c, i) => {
    const wrap = mk('div', 'cwrap', node);
    const face = mk('div', 'cface', wrap);
    const front = mk('div', 'cf', face);
    paperBg(front, 'cream');
    mk('div', 'cf-top', front, '<span>CARD ' + String(i + 1).padStart(2, '0') + '</span><span>NOT TAROT</span>');
    const art = mk('div', 'cf-art', front); bg(art, c.sym, 'berry');
    ['a', 'b', 'c', 'd'].forEach(k => mk('div', 'cf-orn ' + k, front));
    const bot = mk('div', 'cf-bot', front);
    mk('div', 'cf-name', bot, c.name);
    mk('div', 'cf-latin', bot, c.latin);
    const back = mk('div', 'cb', face);
    mk('div', 'cb-top', back, 'NOT TAROT · SORS');
    const bin = mk('div', 'cb-in', back,
      '<div class="cb-en">“' + c.en + '”</div><div class="cb-dia"></div><div class="cb-zh">' + c.zh + '</div>');
    mk('div', 'cb-bot', back, c.latin + ' · ' + String(i + 1).padStart(2, '0'));
    wrap.style.visibility = 'hidden';
    wrap.dataset.card = i;
    return { wrap, face, front, art, back };
  });

  const copy = mk('div', 'c-copy', node);
  const prog = mk('div', 'c-progress', copy, '<span class="lab">CARD 01 / 06</span><i class="hl"></i>');
  const name = mk('h1', 'c-name', copy, 'FEARLESS');
  const latin = mk('div', 'c-latin', copy, 'TIGRIS');
  const sep = mk('div', 'c-sep', copy, '<i class="hl"></i><i class="dia"></i>');
  const mean = mk('p', 'c-mean', copy, '“Fear is not the enemy.”');
  const zh = mk('p', 'c-zh', copy, CARDS[0].zh);
  const hint = mk('div', 'c-hint', copy, 'CLICK THE CARD TO TURN IT · WHEEL TO PASS');
  const fig = mk('div', 'c-fig', node, CARDS[0].fig);
  const count = mk('div', 's7-count', node, 'SIX CARDS<br>ONE HAND');

  S7.card = -1;
  function setCard(i) {
    if (S7.card === i) return;
    S7.card = i;
    const c = CARDS[i];
    name.textContent = c.name;
    latin.textContent = c.latin;
    mean.textContent = '“' + c.en + '”';
    zh.textContent = c.zh;
    fig.textContent = c.fig;
    prog.children[0].textContent = 'CARD ' + String(i + 1).padStart(2, '0') + ' / 06';
    halo.style.backgroundImage = 'url("' + url(c.sym, 'mauve') + '")';
    // reset any flipped cards
    cwraps.forEach(w => { w.face.style.transform = 'rotateY(0deg)'; });
  }

  S7.upd = (local, dur) => {
    const idx = clamp(Math.floor(local / CARD_LEN), 0, 5);
    const u = local - idx * CARD_LEN;
    setCard(idx);
    for (let i = 0; i < 6; i++) {
      const w = cwraps[i];
      if (i > idx) { w.wrap.style.visibility = 'hidden'; continue; }
      w.wrap.style.visibility = 'visible';
      if (i === idx) {
        const k = E.outC(wt(u, 0, 0.5));
        w.wrap.style.opacity = String(Math.min(1, u / 0.16));
        w.wrap.style.zIndex = String(30 + i);
        w.wrap.style.transform = 'translate(' + ((1 - k) * 30).toFixed(1) + 'px,' + ((1 - k) * 44).toFixed(1) +
          'px) rotate(' + ((1 - k) * -3.2).toFixed(2) + 'deg) scale(' + lerp(0.965, 1, k).toFixed(3) + ')';
      } else {
        // retired → fan, bottom right
        const slotX = 1512 + i * 24, slotY = 820 - i * 14;
        const fanRot = -6 + i * 2.4;
        const rk = E.inOut(wt(local, (i + 1) * CARD_LEN, (i + 1) * CARD_LEN + 0.62));
        const tx = (slotX - 720) * rk, ty = (slotY - 520) * rk;
        w.wrap.style.opacity = String(1 - rk * 0.06);
        w.wrap.style.zIndex = String(10 + i);
        w.wrap.style.transform = 'translate(' + tx.toFixed(1) + 'px,' + ty.toFixed(1) + 'px) rotate(' +
          (fanRot * rk).toFixed(2) + 'deg) scale(' + lerp(1, 0.38, rk).toFixed(3) + ')';
      }
    }
    // copy reveal
    const fadeEnd = 1 - E.inOut(wt(local, 8.7, 9.0));
    copy.style.opacity = String(fadeEnd);
    const k1 = E.outC(wt(u, 0.06, 0.48));
    const k2 = E.outC(wt(u, 0.18, 0.58));
    const k3 = E.outC(wt(u, 0.3, 0.72));
    name.style.opacity = String(k1); name.style.transform = 'translateY(' + ((1 - k1) * 26).toFixed(1) + 'px)';
    latin.style.opacity = String(k2);
    sep.style.transform = 'scaleX(' + k2.toFixed(3) + ')'; sep.style.transformOrigin = '0 50%';
    mean.style.opacity = String(k3); mean.style.transform = 'translateY(' + ((1 - k3) * 14).toFixed(1) + 'px)';
    zh.style.opacity = String(k3 * 0.9);
    hint.style.opacity = String(E.outC(wt(u, 0.9, 1.3)) * 0.42 * fadeEnd);
    halo.style.opacity = String(0.055 * fadeEnd);
    fig.style.opacity = String(E.outC(wt(u, 0.2, 0.6)) * 0.45 * fadeEnd);
    count.style.opacity = String(0.4 * fadeEnd);
    S7.cam = { s: 1 + E.inOut(wt(local, 0, 9)) * 0.025, x: 860, y: 540 };
  };
  window.NT.S7 = {
    cards: CARDS, starts: CARDS.map((_, i) => SIX_START + i * CARD_LEN), cwraps,
    activeAt(t) { return clamp(Math.floor((t - SIX_START) / CARD_LEN), 0, 5); },
    startOf(i) { return SIX_START + i * CARD_LEN; },
    setCard
  };
});

/* ============================================================ VI — THE TOTEM */
const S8 = scene(33.5, 36.0, (node) => {
  const cx = 1218, cy = 548;
  const svg = svgEl('svg', { viewBox: '0 0 1920 1080', class: 's8-ring' }, node);
  [152, 234, 312].forEach(r => svgEl('circle', { cx, cy, r }, svg));
  svgEl('circle', { cx, cy, r: 338, 'stroke-dasharray': '1 7', 'stroke-width': 1 }, svg);
  for (let i = 0; i < 48; i++) {
    const a = (i / 48) * Math.PI * 2 - Math.PI / 2;
    const r0 = 292, r1 = i % 4 === 0 ? 312 : 302;
    svgEl('line', {
      x1: (cx + Math.cos(a) * r0).toFixed(1), y1: (cy + Math.sin(a) * r0).toFixed(1),
      x2: (cx + Math.cos(a) * r1).toFixed(1), y2: (cy + Math.sin(a) * r1).toFixed(1),
      class: i % 4 === 0 ? 'b' : ''
    }, svg);
  }
  const SYMS = ['heart', 'eye', 'butterfly', 'tiger', 'unicorn', 'crown', 'mirror', 'compass', 'book', 'candle', 'star', 'key'];
  const items = SYMS.map((s, i) => {
    const a = Math.PI / 12 - Math.PI / 2 + (i / 12) * Math.PI * 2;
    const el = mk('div', 's8-sym', node); bg(el, s, 'gold');
    return { el, x: cx + Math.cos(a) * 312, y: cy + Math.sin(a) * 312 };
  });
  const dust = makeDust(node, 48, 34, { x: 900, y: 240, w: 680, h: 620 }, 'gold');
  const core = mk('div', 's8-core', node); bg(core, 'crown', 'berry');

  const copy = mk('div', 's8-copy', node);
  mk('div', 'kick', copy, 'SIX SIGNS, ONE MARK');
  const big = mk('h1', 's8-big', copy, '<span>THE</span><span>TOTEM.</span>');
  const rule = mk('div', 's8-rule', copy, '<i class="hl"></i><i class="dia"></i>');
  mk('p', 's8-lede', copy, 'What you keep becomes you.<br>Six signs, gathered into a single mark.');
  const list = mk('div', 's8-list', copy);
  ['FEARLESS', 'LET GO', 'BECOME', 'SEE CLEARLY', 'CREATE', 'GET SHIT DONE'].forEach((n, i) => {
    mk('div', 's8-row', list, '<b>' + String(i + 1).padStart(2, '0') + '</b><span>' + n + '</span>');
  });

  S8.upd = (local, dur) => {
    const build = E.inOut(wt(local, 0.1, 1.2));
    svg.style.transform = 'rotate(' + (build * 6).toFixed(2) + 'deg)';
    svg.style.transformOrigin = cx + 'px ' + cy + 'px';
    svg.style.opacity = String(build * 0.95);
    items.forEach((it, i) => {
      const k = E.outBack(wt(local, 0.15 + i * 0.05, 0.15 + i * 0.05 + 0.75));
      const px = lerp(cx, it.x, k), py = lerp(cy, it.y, k);
      it.el.style.transform = 'translate(' + px.toFixed(1) + 'px,' + py.toFixed(1) + 'px) translate(-50%,-50%) scale(' + lerp(0.2, 1, k).toFixed(3) + ') rotate(' + ((1 - k) * -24).toFixed(1) + 'deg)';
      it.el.style.opacity = String(Math.min(1, k * 3));
      it.el.style.left = '0px'; it.el.style.top = '0px';
    });
    const ck = E.outC(wt(local, 0.75, 1.6));
    core.style.transform = 'scale(' + lerp(0.35, 1, ck).toFixed(3) + ') rotate(' + (ck * -8).toFixed(2) + 'deg)';
    core.style.opacity = String(ck);
    driftDust(dust, local, 9);

    big.style.opacity = String(E.outC(wt(local, 0.35, 1.25)));
    big.style.transform = 'translateY(' + ((1 - E.outC(wt(local, 0.35, 1.25))) * 22).toFixed(1) + 'px)';
    rule.style.opacity = String(E.outC(wt(local, 0.6, 1.4)));
    copy.querySelector('.s8-lede').style.opacity = String(E.outC(wt(local, 0.8, 1.6)) * 0.74);
    Array.from(list.children).forEach((row, i) => {
      const k = E.outC(wt(local, 1.0 + i * 0.07, 1.45 + i * 0.07));
      row.style.opacity = String(k * 0.95);
      row.style.transform = 'translateX(' + ((1 - k) * -14).toFixed(1) + 'px)';
    });
    S8.cam = { s: 1 + E.inOut(wt(local, 0, 2.5)) * 0.035, x: cx, y: cy };
  };
});

/* ============================================================ VII — THE SEAL */
const S9 = scene(36.0, 40.0, (node) => {
  const cx = 960, cy = 468;
  const svg = svgEl('svg', { viewBox: '0 0 1920 1080', class: 's9-ring' }, node);
  [188, 258, 330].forEach(r => svgEl('circle', { cx, cy, r }, svg));
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2 - Math.PI / 2;
    svgEl('line', {
      x1: (cx + Math.cos(a) * 188).toFixed(1), y1: (cy + Math.sin(a) * 188).toFixed(1),
      x2: (cx + Math.cos(a) * 330).toFixed(1), y2: (cy + Math.sin(a) * 330).toFixed(1),
      'stroke-width': 0.8
    }, svg);
  }
  for (let i = 0; i < 72; i++) {
    const a = (i / 72) * Math.PI * 2 - Math.PI / 2;
    const r0 = 330, r1 = i % 6 === 0 ? 342 : 336;
    svgEl('line', {
      x1: (cx + Math.cos(a) * r0).toFixed(1), y1: (cy + Math.sin(a) * r0).toFixed(1),
      x2: (cx + Math.cos(a) * r1).toFixed(1), y2: (cy + Math.sin(a) * r1).toFixed(1),
      'stroke-width': i % 6 === 0 ? 1.2 : 0.8
    }, svg);
  }
  const SYMS = ['heart', 'eye', 'butterfly', 'tiger', 'unicorn', 'crown', 'mirror', 'compass', 'wand', 'flower', 'star', 'key'];
  const items = SYMS.map((s, i) => {
    const el = mk('div', 's9-sym', node); bg(el, s, i % 2 ? 'crimson' : 'berry');
    const a = -Math.PI / 2 + (i / 12) * Math.PI * 2;
    return { el, x: cx + Math.cos(a) * 258, y: cy + Math.sin(a) * 258 };
  });
  const dmarks = [];
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2 - Math.PI / 2;
    const el = mk('div', 's9-dia', node);
    el.style.left = (cx + Math.cos(a) * 286).toFixed(1) + 'px';
    el.style.top = (cy + Math.sin(a) * 286).toFixed(1) + 'px';
    dmarks.push(el);
  }
  const MORPHS = ['butterfly', 'flower', 'heart', 'crown', 'eye'];
  const dust = makeDust(node, 40, 57, { x: 520, y: 120, w: 880, h: 660 }, 'berry');
  const core = mk('div', 's9-core', node);
  const coreSyms = MORPHS.map(s => { const d = mkSym(core, s, 'berry'); d.style.inset = '0'; return d; });
  const word = mk('div', 's9-word', node, 'BECOME.');
  mk('div', 's9-sub', node, 'a sign that refuses one meaning');
  mk('div', 's9-lr l', node); mk('div', 's9-lr r', node);

  S9.upd = (local, dur) => {
    const grow = E.inOut(wt(local, 0.05, 1.4));
    svg.style.transform = 'scale(' + lerp(0.82, 1, grow).toFixed(3) + ') rotate(' + (local * 1.6).toFixed(2) + 'deg)';
    svg.style.transformOrigin = cx + 'px ' + cy + 'px';
    svg.style.opacity = String(grow);
    items.forEach((it, i) => {
      const k = E.outC(wt(local, 0.2 + i * 0.045, 0.9 + i * 0.045));
      it.el.style.opacity = String(k);
      it.el.style.transform = 'translate(' + it.x.toFixed(1) + 'px,' + it.y.toFixed(1) + 'px) translate(-50%,-50%) scale(' + lerp(0.5, 1, k).toFixed(3) + ')';
      it.el.style.left = '0px'; it.el.style.top = '0px';
    });
    // emblem morph cycle
    const start = 0.75, step = 0.55;
    coreSyms.forEach((s, i) => {
      const a = start + i * step;
      const b = a + step;
      let op = 0, sc = 0.7;
      if (local >= a) {
        if (i === coreSyms.length - 1) {
          op = E.outC(wt(local, a, a + 0.3));
          sc = lerp(0.7, 1, E.outC(wt(local, a, a + 0.35)));
        } else {
          op = E.outC(wt(local, a, a + 0.18)) * (1 - E.soft(wt(local, b - 0.12, b + 0.06)));
          const q = wt(local, a, b);
          sc = lerp(0.7, 1.12, E.outC(q));
        }
      }
      s.style.opacity = String(op);
      s.style.transform = 'scale(' + sc.toFixed(3) + ') rotate(' + ((i % 2 ? 1 : -1) * (1 - op) * 8).toFixed(1) + 'deg)';
    });
    const wk = E.outC(wt(local, 2.3, 3.2));
    word.style.opacity = String(wk);
    word.style.transform = 'translateY(' + ((1 - wk) * 24).toFixed(1) + 'px)';
    document.querySelector('.s9-sub').style.opacity = String(E.outC(wt(local, 2.8, 3.5)) * 0.55);
    document.querySelectorAll('.s9-lr').forEach(lr => { lr.style.opacity = String(wk * 0.55); });
    dmarks.forEach((d, i) => {
      d.style.opacity = String(E.outC(wt(local, 0.5 + i * 0.05, 1.0 + i * 0.05)) * 0.85);
    });
    driftDust(dust, local, 7);
    S9.cam = { s: 1 + E.inOut(wt(local, 0, 4)) * 0.03, x: cx, y: cy };
  };
});

/* ============================================================ — COLLAPSE */
const S10 = scene(40.0, 42.0, (node) => {
  const cx = 960, cy = 470;
  const ghost = mk('div', null, node);
  ghost.style.cssText = 'position:absolute;left:0;top:0;width:1920px;height:1080px;';
  const svg = svgEl('svg', { viewBox: '0 0 1920 1080', class: 's9-ring' }, ghost);
  [190, 262, 330].forEach(r => svgEl('circle', { cx, cy, r }, svg));
  const SYMS = ['heart', 'eye', 'butterfly', 'tiger', 'unicorn', 'crown'];
  const items = SYMS.map((s, i) => {
    const el = mk('div', 's9-sym', ghost); bg(el, s, 'berry');
    const a = -Math.PI / 2 + (i / 6) * Math.PI * 2;
    return { el, x: cx + Math.cos(a) * 272, y: cy + Math.sin(a) * 272 };
  });
  const word = mk('div', 's10-word', node, 'BECOME.');
  const num = mk('div', 's10-num', node, 'VII');
  const line = mk('div', 's10-line', node);
  const sub = mk('div', 's10-sub', node, 'The cards stop here. The meaning does not.');

  S10.upd = (local, dur) => {
    const k = E.inOut(wt(local, 0.1, 1.5));
    const sc = lerp(1, 0.02, k);
    ghost.style.transform = 'translate(' + cx + 'px,' + cy + 'px) scale(' + sc.toFixed(4) + ') rotate(' + (k * -22).toFixed(2) + 'deg)';
    ghost.style.transformOrigin = '0 0';
    ghost.style.opacity = String(1 - k * 0.85);
    items.forEach((it, i) => {
      it.el.style.opacity = String((1 - k) * 0.9);
      it.el.style.transform = 'translate(' + it.x.toFixed(1) + 'px,' + it.y.toFixed(1) + 'px) translate(-50%,-50%)';
      it.el.style.left = '0px'; it.el.style.top = '0px';
    });
    const wk = E.outC(wt(local, 0.35, 1.3));
    word.style.opacity = String(wk * (1 - E.inOut(wt(local, 1.42, 1.94))));
    num.style.opacity = String(0.05 * wk);
    const sk = E.outC(wt(local, 0.9, 1.7));
    sub.style.opacity = String(sk * (1 - E.inOut(wt(local, 1.5, 1.95))) * 0.86);
    sub.style.transform = 'translateY(' + ((1 - sk) * 14).toFixed(1) + 'px)';
    const lk = E.inOut(wt(local, 0.95, 1.55));
    line.style.width = (lk * 720).toFixed(0) + 'px';
    line.style.left = (960 - lk * 360).toFixed(0) + 'px';
    line.style.opacity = String(lk * 0.75);
    S10.cam = { s: 1 + E.inOut(wt(local, 0, 2)) * 0.02, x: cx, y: cy };
  };
});

/* ============================================================ — THE NAME */
const S11 = scene(42.0, 45.0, (node) => {
  const wrap = mk('div', 's11-wrap', node);
  mk('div', 's11-kick', wrap, 'EDITION 01 · MMXXV');
  const ruleT = mk('div', 's11-rule', wrap);
  const wordWrap = mk('div', null, wrap);
  wordWrap.style.cssText = 'overflow:hidden;padding:.06em .1em .12em;';
  const word = mk('div', 's11-word', wordWrap, 'NOT TAROT');
  const sub = mk('div', 's11-sub', wrap, 'MAKE YOUR OWN MEANING.');
  const ruleB = mk('div', 's11-rule b', wrap);
  const col = mk('div', 's11-col', wrap, 'ONE INK · ONE COLOUR · ONE HAND');
  const hint = mk('div', 's11-hint', wrap, 'CLICK ANYWHERE TO DRAW YOUR CARD');

  const ghost = mk('div', 's11-ghost', node); bg(ghost, 'eye_tears', 'plum');
  const seal = mk('div', 's11-seal', node,
    '<i class="ring1"></i><i class="ring2"></i><span class="mono">NT</span><span class="yr">MMXXVI</span>');
  const meta = mk('div', 's11-meta', node,
    '<span>45 SECONDS</span><span>·</span><span>1920 × 1080</span><span>·</span><span>NOT TAROT</span>');

  S11.upd = (local, dur) => {
    const p = Math.min(local, 1.55);
    const k1 = E.outC(wt(p, 0.05, 0.5));
    const kw = E.outExpo(wt(p, 0.18, 1.05));
    const k2 = E.outC(wt(p, 0.55, 1.05));
    const k3 = E.outC(wt(p, 0.72, 1.2));
    const k4 = E.outC(wt(p, 0.9, 1.35));
    ruleT.style.transform = 'scaleX(' + (k1 * 0.62).toFixed(3) + ')';
    ruleT.style.transformOrigin = '50% 50%';
    word.style.transform = 'translateY(' + ((1 - kw) * 108).toFixed(2) + '%) translate(' +
      (ST.ptr.nx * 5).toFixed(2) + 'px,' + (ST.ptr.ny * 4).toFixed(2) + 'px)';
    sub.style.opacity = String(k2);
    sub.style.letterSpacing = (0.42 + k2 * 0.24).toFixed(3) + 'em';
    ruleB.style.transform = 'scaleX(' + (k2 * 0.5).toFixed(3) + ')';
    ruleB.style.transformOrigin = '50% 50%';
    col.style.opacity = String(k3 * 0.45);
    const sealK = E.outBack(wt(p, 0.85, 1.32));
    seal.style.opacity = String(Math.min(1, sealK * 1.2));
    seal.style.transform = 'rotate(-9deg) scale(' + lerp(0.78, 1, sealK).toFixed(3) + ')';
    const hk = E.outC(wt(p, 1.05, 1.5));
    hint.style.opacity = String(hk * (0.5 + Math.sin((local - 1.0) * 2.2) * 0.16));
    meta.style.opacity = String(k3 * 0.34);
    ghost.style.transform = 'rotate(' + (14 + local * 1.2).toFixed(2) + 'deg)';
    S11.cam = { s: lerp(1.015, 1, E.outC(wt(local, 0, 1.6))), x: 960, y: 540 };
  };
});

/* draw-your-card data shared with the overlay */
window.NT.CARDS = CARDS;
