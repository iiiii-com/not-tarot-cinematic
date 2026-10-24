/* =====================================================================
   decor.js — ornaments, marginalia, calibration marks, plate stamps.

   Loaded right after effects.js, before the scenes. Nothing here touches
   the scene sources: on the first frame (all scenes are already built by
   boot) the decor layer dresses each plate from the outside, then updates
   itself from t alone. That keeps ?capture=1 frames deterministic.
   ===================================================================== */
const ORN_SVG = {
  fleuron:
    '<svg viewBox="0 0 120 26" aria-hidden="true">' +
      '<g fill="none" stroke="currentColor" stroke-width=".9" stroke-linecap="round">' +
        '<path d="M7 13 Q 18 13 22 8 Q 26 3 32 5 Q 37 7 35 12"/>' +
        '<path d="M113 13 Q 102 13 98 8 Q 94 3 88 5 Q 83 7 85 12"/>' +
        '<path d="M43 13 H 54"/><path d="M66 13 H 77"/>' +
      '</g>' +
      '<path d="M60 7.6 L65.4 13 L60 18.4 L54.6 13 Z" fill="currentColor"/>' +
      '<circle cx="60" cy="3.6" r="1.15" fill="currentColor"/>' +
      '<circle cx="60" cy="22.4" r="1.15" fill="currentColor"/>' +
    '</svg>',
  corner:
    '<svg viewBox="0 0 96 96" aria-hidden="true">' +
      '<g fill="none" stroke="currentColor" stroke-width=".9" stroke-linecap="round">' +
        '<path d="M2 95 V 20 Q 2 2 20 2 H 95"/>' +
        '<path d="M10 95 V 24 Q 10 10 24 10 H 95" opacity=".5"/>' +
        '<path d="M24 22 q 10 0 10 10 q 0 8 -8 8 q -6 0 -6 -6 q 0 -4 4 -4" opacity=".8"/>' +
        '<path d="M95 28 q -7 2 -7 9" opacity=".55"/>' +
        '<path d="M28 95 q 2 -7 9 -7" opacity=".55"/>' +
      '</g>' +
      '<circle cx="20" cy="20" r="1.7" fill="currentColor"/>' +
      '<circle cx="40" cy="2" r="1.1" fill="currentColor"/>' +
      '<circle cx="2" cy="40" r="1.1" fill="currentColor"/>' +
    '</svg>',
  cross:
    '<svg viewBox="0 0 16 16" aria-hidden="true">' +
      '<path d="M8 .8v14.4M.8 8h14.4" stroke="currentColor" stroke-width=".9"/>' +
      '<circle cx="8" cy="8" r="1.25" fill="currentColor"/>' +
    '</svg>'
};

const Extras = (() => {
  'use strict';

  let ready = false;
  const REV = [], UPD = [];
  let stampEl, stampNum, stampSub;
  let tipEl, tipK, tipName, tipDesc;
  let s1orb, s1orbB, s1flecks, s2pulsers, s4orbs, s4dust,
      s6flecks, s7orbs, railRows, s9counter, s10conv, s10seed;

  /* ------------------------------------------------------------ tiny helpers */
  function sv(tag, attrs, parent) {
    const n = document.createElementNS('http://www.w3.org/2000/svg', tag);
    if (attrs) for (const k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function pos(el, x, y) { el.style.left = x + 'px'; el.style.top = y + 'px'; return el; }
  function rv(el, ai, a, d, mx) {
    el.dataset.rv = a + ',' + d + ',' + (mx == null ? 1 : mx);
    (REV[ai] = REV[ai] || []).push(el);
    return el;
  }
  /* an ornament svg, centred on x/y when given */
  function glyph(parent, key, cls, x, y, w, h, rot) {
    const d = mk('div', 'orn ' + (cls || ''), parent);
    d.innerHTML = ORN_SVG[key];
    if (w) d.style.width = w + 'px';
    if (h) d.style.height = h + 'px';
    if (x != null) {
      d.style.left = x + 'px'; d.style.top = y + 'px';
      d.style.margin = (-(h || w) / 2) + 'px 0 0 ' + (-(w || h) / 2) + 'px';
    }
    if (rot) d.style.transform = 'rotate(' + rot + 'deg)';
    return d;
  }
  function marg(parent, html, x, y, rot, cls) {
    const n = mk('div', 'marg ' + (cls || ''), parent, html);
    n.style.left = x + 'px'; n.style.top = y + 'px';
    n.style.transform = 'translate(-50%,-50%) rotate(' + (rot || 0) + 'deg)';
    return n;
  }
  /* dimension line with diamond caps and a small caps label */
  function dim(parent, ai, x1, y1, x2, y2, label, a, d, mx, o) {
    o = o || {};
    const len = Math.hypot(x2 - x1, y2 - y1);
    const ang = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
    const l = mk('div', 'dim', parent);
    l.style.left = x1 + 'px'; l.style.top = y1 + 'px'; l.style.width = len + 'px';
    l.style.transform = 'rotate(' + ang.toFixed(2) + 'deg)';
    mk('i', 'dim-cap a', l); mk('i', 'dim-cap b', l);
    rv(l, ai, a, d, o.lop == null ? .75 : o.lop);
    if (label) {
      const lb = mk('span', 'dim-lab', parent, label);
      lb.style.left = ((x1 + x2) / 2 + (o.dx || 0)) + 'px';
      lb.style.top = ((y1 + y2) / 2 + (o.dy == null ? -17 : o.dy)) + 'px';
      lb.style.transform = 'translate(-50%,-50%)' + (o.rot ? ' rotate(' + o.rot + 'deg)' : '');
      rv(lb, ai, a + .1, d, o.lop == null ? .8 : o.lop);
    }
    return l;
  }

  /* ============================================================ plate I — S1 */
  function buildS1(node, ai) {
    s1orb = pos(mk('div', 's1-orb', node), 620, 540);
    s1orbB = pos(mk('div', 's1-orb b', node), 620, 540);
    rv(s1orb, ai, .45, 1.1, .85); rv(s1orbB, ai, .7, 1.3, .7);

    s1flecks = [];
    const rnd = mulberry(19);
    for (let i = 0; i < 11; i++) {
      const el = mk('div', 's1-fleck', node);
      s1flecks.push({ el: el, a: (i / 11) * Math.PI * 2 + (rnd() - .5) * .34, d: 34 + rnd() * 96, ph: rnd() * 6.28 });
      el.style.width = el.style.height = (2.4 + rnd() * 2.6).toFixed(1) + 'px';
    }
    /* four sighting marks on the ring's axes */
    [[620, 250], [620, 830], [330, 540], [910, 540]].forEach(([x, y], i) => {
      rv(glyph(node, 'cross', 'soft', x, y, 13, 13), ai, 1.05 + i * .06, .6, .62);
    });
    rv(marg(node, '墨滴很有耐心，<br>它早就到了', 892, 692, -2.5), ai, 1.6, .9, .6);
    rv(glyph(node, 'fleuron', '', 1236, 806, 150, 32), ai, 1.95, .9, .6);
    dim(node, ai, 512, 188, 512, 534, '下落', 1.2, .8, .6, { lop: .5, dx: -44, dy: 0, rot: -90 });

    UPD[0] = local => {
      s1orb.style.transform = 'rotate(' + (local * 4).toFixed(2) + 'deg)';
      s1orbB.style.transform = 'rotate(' + (-local * 2.4).toFixed(2) + 'deg)';
      const k = E.outC(wt(local, 1.14, 1.78));
      const fade = 1 - E.inOut(wt(local, 1.8, 2.4));
      for (const f of s1flecks) {
        const r = f.d * k;
        f.el.style.left = (620 + Math.cos(f.a) * r).toFixed(1) + 'px';
        f.el.style.top = (540 + Math.sin(f.a) * r - k * k * 12).toFixed(1) + 'px';
        f.el.style.opacity = String(k * fade * .62);
      }
    };
  }

  /* =========================================================== plate I — S2 */
  function buildS2(node, ai) {
    /* engraved calibration grid, tucked behind the trace */
    const g = sv('svg', { viewBox: '0 0 1920 1080', class: 's2-grid' }, null);
    node.insertBefore(g, node.firstChild);
    const defs = sv('defs', {}, g);
    const p1 = sv('pattern', { id: 'ntg1', width: '32', height: '32', patternUnits: 'userSpaceOnUse' }, defs);
    sv('path', { d: 'M 32 0 H 0 V 32', fill: 'none', 'stroke-width': .7, class: 's2-grid-fine' }, p1);
    const p2 = sv('pattern', { id: 'ntg2', width: '160', height: '160', patternUnits: 'userSpaceOnUse' }, defs);
    sv('rect', { x: 0, y: 0, width: '160', height: '160', fill: 'url(#ntg1)' }, p2);
    sv('path', { d: 'M 160 0 H 0 V 160', fill: 'none', 'stroke-width': 1, class: 's2-grid-bold' }, p2);
    sv('rect', { x: 104, y: 472, width: 1712, height: 438, fill: 'url(#ntg2)', class: 's2-grid-area' }, g);
    sv('path', { d: 'M 104 472 V 910 M 104 910 H 1816', fill: 'none', 'stroke-width': 1, class: 's2-grid-bold' }, g);

    s2pulsers = [0, 1, 2].map(() => pos(mk('div', 's2-pulser', node), 600, 540));
    const BEATS = [1.30, 2.18, 3.06, 3.94, 4.82, 5.70, 6.58, 7.20];
    UPD[1] = local => {
      const bp = pulse(local, BEATS);
      for (let i = 0; i < 3; i++) {
        s2pulsers[i].style.opacity = String(bp * (.24 - i * .06));
        s2pulsers[i].style.transform = 'scale(' + (1 + bp * (.85 + i * .5)).toFixed(3) + ')';
      }
    };
    dim(node, ai, 140, 948, 468, 948, '1 秒 \u00b7 72 次', 1.3, .8, .8, { lop: .55, dy: 15 });
    rv(marg(node, '在腕上量到，<br>在喉咙里相信', 330, 892, -2), ai, 2.1, .9, .55);
  }

  /* ========================================================== plate II — S3 */
  function buildS3(node, ai) {
    const cx = 960, cy = 500;
    const deco = sv('svg', { viewBox: '0 0 1920 1080', class: 's3-deco' }, null);
    node.insertBefore(deco, node.firstChild);
    sv('circle', { cx: cx, cy: cy, r: 360, 'stroke-dasharray': '1 9', 'stroke-width': 1, class: 's3-guide d' }, deco);
    for (let i = 0; i < 72; i++) {
      const a = (i / 72) * Math.PI * 2 - Math.PI / 2;
      const r0 = 344, r1 = i % 6 === 0 ? 354 : 349;
      sv('line', {
        x1: (cx + Math.cos(a) * r0).toFixed(1), y1: (cy + Math.sin(a) * r0).toFixed(1),
        x2: (cx + Math.cos(a) * r1).toFixed(1), y2: (cy + Math.sin(a) * r1).toFixed(1),
        class: 's3-guide'
      }, deco);
    }
    sv('line', { x1: cx - 372, y1: cy, x2: cx + 372, y2: cy, class: 's3-guide', 'stroke-dasharray': '2 7' }, deco);
    sv('line', { x1: cx, y1: cy - 372, x2: cx, y2: cy + 372, class: 's3-guide', 'stroke-dasharray': '2 7' }, deco);

    const SYMS = ['heart', 'eye', 'butterfly', 'tiger', 'unicorn', 'crown', 'mirror', 'compass',
                  'hands', 'wand', 'skull', 'moon', 'key', 'flower', 'star', 'snake', 'hourglass', 'scales'];
    const NUMS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII',
                  'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII'];
    const syms = node.querySelectorAll('.s3-sym');
    const glyphs = [];
    for (let i = 0; i < 18; i++) {
      const a = -Math.PI / 2 + (i / 18) * Math.PI * 2;
      const n = pos(mk('div', 's3-num', node, NUMS[i]),
        (cx + Math.cos(a) * 398).toFixed(1), (cy + Math.sin(a) * 398).toFixed(1));
      /* keep the top and bottom-centre labels clear of chrome + title lines */
      if (i !== 0 && i !== 9) rv(n, ai, 2.2 + i * .025, .6, .5);
      glyphs.push(n);
      if (syms[i]) { syms[i].dataset.name = SYMS[i]; syms[i].dataset.num = NUMS[i]; }
    }
    dim(node, ai, 1520, 862, 1690, 862, '比例 1 : 1', 2.45, .7, .8, { lop: .5, dy: 15 });
    rv(marg(node, '十八种说法，<br>说同一件不可能的事', 330, 246, -2), ai, 2.7, .9, .55);
  }

  /* ========================================================= plate III — S4 */
  function buildS4(node, ai) {
    const cx = 1266, cy = 502;
    s4orbs = [pos(mk('div', 's4-orb', node), cx, cy), pos(mk('div', 's4-orb b', node), cx, cy)];
    rv(s4orbs[0], ai, .5, 1.2, .6); rv(s4orbs[1], ai, .7, 1.3, .5);

    const ax1 = mk('div', 's4-axis', node);
    ax1.style.left = '760px'; ax1.style.top = cy + 'px'; ax1.style.width = '1000px'; ax1.style.height = '1px';
    rv(ax1, ai, .6, 1, .5);
    const ax2 = mk('div', 's4-axis', node);
    ax2.style.left = cx + 'px'; ax2.style.top = '96px'; ax2.style.width = '1px'; ax2.style.height = '812px';
    rv(ax2, ai, .65, 1, .5);

    dim(node, ai, 894, 214, 1638, 214, 'A \u00b7 744', 1.1, .9, .8, { lop: .55, dy: -16 });
    dim(node, ai, 1706, 326, 1706, 638, 'B \u00b7 312', 1.2, .9, .8, { lop: .55, dx: 34, dy: 0, rot: 90 });

    s4dust = makeDust(node, 26, 45, { x: 860, y: 160, w: 820, h: 680 }, 'plum');
    rv(marg(node, '眼睛是一只手，<br>从不停止触摸', 596, 866, 0), ai, 1.75, .9, .56);

    UPD[3] = local => {
      driftDust(s4dust, local, 5);
      s4orbs[0].style.transform = 'rotate(' + (local * 1.1).toFixed(2) + 'deg)';
      s4orbs[1].style.transform = 'rotate(' + (-local * .8).toFixed(2) + 'deg)';
    };
  }

  /* ========================================================== plate III — S5 */
  function buildS5(node, ai) {
    const frame = mk('div', 's5-frame', node);
    frame.style.left = '799px'; frame.style.top = '149px';
    frame.style.width = '946px'; frame.style.height = '782px';
    rv(frame, ai, .25, .9, .85);

    [[800, 150], [1744, 150], [800, 930], [1744, 930]].forEach(([x, y], i) => {
      rv(glyph(node, 'cross', 'soft', x, y, 13, 13), ai, .4 + i * .06, .6, .6);
    });
    for (let i = 0; i < 13; i++) {
      const t = mk('div', 's5-tick', node);
      t.style.left = '786px'; t.style.top = (150 + i * 65) + 'px';
      t.style.width = (i % 3 === 0 ? 13 : 8) + 'px';
      rv(t, ai, .8 + i * .03, .5, .6);
    }
    const NAMES = window.NT.SYM_NAMES || {};
    const cells = node.querySelectorAll('.s5-cell');
    for (let i = 0; i < cells.length; i++) {
      const info = NAMES[cells[i].dataset.sym];
      if (!info) continue;
      const lat = mk('div', 's5-lat', cells[i], info[0]);
      rv(lat, ai, 1.5 + i * .028, .6, .55);
    }
    rv(marg(node, '每个符号，都是一扇小门', 1792, 540, 90, 'tight'), ai, 2.0, .9, .55);
  }

  /* =========================================================== plate IV — S6 */
  function buildS6(node, ai) {
    rv(glyph(node, 'corner', 'inv', 168, 168, 84, 84), ai, .5, .8, .55);
    rv(glyph(node, 'corner', 'inv', 1752, 912, 84, 84, 180), ai, .6, .8, .55);
    const ctr = glyph(node, 'corner', 'inv', 1752, 168, 84, 84);
    ctr.style.transform = 'scaleX(-1)';
    rv(ctr, ai, .55, .8, .55);
    const cbl = glyph(node, 'corner', 'inv', 168, 912, 84, 84);
    cbl.style.transform = 'scaleY(-1)';
    rv(cbl, ai, .65, .8, .55);

    s6flecks = [];
    const rnd = mulberry(91);
    for (let i = 0; i < 16; i++) {
      const a = rnd() * Math.PI * 2, r = 150 + rnd() * 340;
      const el = mk('div', 's6-fleck', node);
      el.style.width = el.style.height = (1.8 + rnd() * 2.4).toFixed(1) + 'px';
      s6flecks.push({ el: el, x: 930 + Math.cos(a) * r, y: 540 + Math.sin(a) * r * .82, ph: rnd() * 6.28 });
    }
    const card = node.querySelector('.s6-card');
    if (card) ['c1', 'c2', 'c3', 'c4'].forEach((c, i) => {
      const d = mk('div', 's6-cmark ' + c, card);
      d.innerHTML = ORN_SVG.cross;
      rv(d, ai, 1.12 + i * .05, .6, .85);
    });
    rv(glyph(node, 'fleuron', 'inv', 1380, 700, 150, 32), ai, 1.7, .8, .55);
    rv(marg(node, '五十二张脸，<br>一个背面', 330, 306, -90, 'inv tight'), ai, 1.3, .9, .5);

    UPD[5] = local => {
      const k = E.outC(wt(local, .85, 1.6));
      for (const f of s6flecks) {
        f.el.style.left = (f.x + Math.sin(local * .8 + f.ph) * 6).toFixed(1) + 'px';
        f.el.style.top = (f.y + Math.cos(local * .6 + f.ph) * 5).toFixed(1) + 'px';
        f.el.style.opacity = String(k * .55);
      }
    };
  }

  /* ============================================================ plate V — S7 */
  function buildS7(node, ai) {
    s7orbs = [pos(mk('div', 's7-orb', node), 720, 520), pos(mk('div', 's7-orb b', node), 720, 520)];
    rv(s7orbs[0], ai, .2, 1.2, .8); rv(s7orbs[1], ai, .35, 1.2, .6);

    [[476, 166], [964, 166], [476, 874], [964, 874]].forEach(([x, y], i) => {
      rv(glyph(node, 'cross', 'soft', x, y, 13, 13), ai, .5 + i * .07, .6, .6);
    });

    const S7 = window.NT.S7;
    const cards = (S7 && S7.cards) || [];
    const rail = mk('div', 'c-rail', node);
    rail.style.left = '96px'; rail.style.top = '262px';
    mk('div', 'cr-cap', rail, '索引 \u00b7 六张牌');
    const ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI'];
    railRows = cards.map((c, i) => {
      const row = mk('div', 'c-rail-row', rail, '<b>' + ROMAN[i] + '</b><span>' + c.name + '</span>');
      row.dataset.i = i;
      row.addEventListener('pointerenter', () => { try { sfx('hover'); } catch (e) {} });
      row.addEventListener('click', e => {
        e.stopPropagation();
        try { sfx('click'); } catch (err) {}
        if (!ST.started) return;
        seek(S7.startOf(i) + .35);
        if (!ST.playing) { try { play(); syncPlayIcon(); } catch (err) {} }
        try { wake(); } catch (err) {}
      });
      return row;
    });
    rv(rail, ai, .3, 1.0, .95);

    UPD[6] = local => {
      const idx = clamp(Math.floor(local / 1.5), 0, 5);
      for (let i = 0; i < railRows.length; i++) railRows[i].classList.toggle('on', i === idx);
      s7orbs[0].style.transform = 'rotate(' + (local * 1.4).toFixed(2) + 'deg)';
      s7orbs[1].style.transform = 'rotate(' + (-local * 1.8).toFixed(2) + 'deg)';
    };
  }

  /* =========================================================== plate VI — S8 */
  function buildS8(node, ai) {
    const cx = 1218, cy = 548;
    const deco = sv('svg', { viewBox: '0 0 1920 1080', class: 's8-deco' }, null);
    node.insertBefore(deco, node.firstChild);
    for (let i = 0; i < 12; i++) {
      const a = -Math.PI / 2 + (i / 12) * Math.PI * 2;
      sv('line', {
        x1: (cx + Math.cos(a) * 158).toFixed(1), y1: (cy + Math.sin(a) * 158).toFixed(1),
        x2: (cx + Math.cos(a) * 312).toFixed(1), y2: (cy + Math.sin(a) * 312).toFixed(1),
        'stroke-width': .7, 'stroke-opacity': .5
      }, deco);
    }
    sv('circle', { cx: cx, cy: cy, r: 378, 'stroke-dasharray': '1 8', 'stroke-width': 1, 'stroke-opacity': .55 }, deco);

    const SYMS = ['heart', 'eye', 'butterfly', 'tiger', 'unicorn', 'crown', 'mirror', 'compass', 'book', 'candle', 'star', 'key'];
    const NUMS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'];
    const syms = node.querySelectorAll('.s8-sym');
    for (let i = 0; i < 12; i++) {
      if (syms[i]) { syms[i].dataset.name = SYMS[i]; syms[i].dataset.num = NUMS[i]; }
      const a = -Math.PI / 2 + (i / 12) * Math.PI * 2;
      const n = pos(mk('div', 's8-num', node, NUMS[i]),
        (cx + Math.cos(a) * 386).toFixed(1), (cy + Math.sin(a) * 386).toFixed(1));
      if (i !== 6) rv(n, ai, .55 + i * .045, .6, .6);
    }
    rv(marg(node, '你留下的，<br>成为你', 330, 878, -2), ai, 1.5, .9, .55);
  }

  /* ========================================================== plate VI — S9 */
  function buildS9(node, ai) {
    const cx = 960, cy = 468;
    const deco = sv('svg', { viewBox: '0 0 1920 1080', class: 's9-deco' }, null);
    node.insertBefore(deco, node.firstChild);
    for (let i = 0; i < 24; i++) {
      const a = -Math.PI / 2 + (i / 24) * Math.PI * 2;
      const px = cx + Math.cos(a) * 360, py = cy + Math.sin(a) * 360;
      sv('ellipse', {
        cx: px.toFixed(1), cy: py.toFixed(1), rx: 6.5, ry: 17,
        transform: 'rotate(' + (a * 180 / Math.PI + 90).toFixed(1) + ' ' + px.toFixed(1) + ' ' + py.toFixed(1) + ')',
        fill: 'none', 'stroke-width': .85, 'stroke-opacity': .62
      }, deco);
    }
    const NUMS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'];
    const syms = node.querySelectorAll('.s9-sym');
    for (let i = 0; i < 12; i++) {
      if (syms[i]) { syms[i].dataset.name = syms[i].dataset.name || ''; }
      const a = -Math.PI / 2 + (i / 12) * Math.PI * 2;
      const n = pos(mk('div', 's9-num', node, NUMS[i]),
        (cx + Math.cos(a) * 392).toFixed(1), (cy + Math.sin(a) * 392).toFixed(1));
      if (i !== 6) rv(n, ai, 1.0 + i * .05, .6, .58);
    }
    const SYMS = ['heart', 'eye', 'butterfly', 'tiger', 'unicorn', 'crown', 'mirror', 'compass', 'wand', 'flower', 'star', 'key'];
    for (let i = 0; i < syms.length; i++) {
      if (SYMS[i]) { syms[i].dataset.name = SYMS[i]; syms[i].dataset.num = NUMS[i]; }
    }
    s9counter = pos(mk('div', 's9-counter', node), cx, cy);
    rv(s9counter, ai, .45, 1.2, .6);
    rv(marg(node, '一个符号，所有含义', 300, 898, -2), ai, 2.3, .9, .55);

    UPD[8] = local => {
      s9counter.style.transform = 'rotate(' + (-local * 3.2).toFixed(2) + 'deg)';
    };
  }

  /* ========================================================= plate VII — S10 */
  function buildS10(node, ai) {
    s10conv = [];
    for (let i = 0; i < 8; i++) {
      const el = mk('div', 's10-conv', node);
      s10conv.push({ el: el, a: i * 45 + 22 });
    }
    s10seed = pos(mk('div', 's10-seed', node), 960, 470);

    UPD[9] = local => {
      const k = E.inOut(wt(local, .1, 1.4));
      for (const c of s10conv) {
        const r = lerp(470, 30, k);
        c.el.style.left = '960px'; c.el.style.top = '470px';
        c.el.style.width = (120 * (1 - k * .78)).toFixed(1) + 'px';
        c.el.style.transform = 'rotate(' + c.a + 'deg) translateX(' + r.toFixed(1) + 'px)';
        c.el.style.opacity = String((1 - k * .55) * .5);
      }
      const sk = E.outC(wt(local, .08, .5)) * (1 - E.inOut(wt(local, 1.15, 1.8)));
      s10seed.style.opacity = String(sk * .85);
      s10seed.style.transform = 'scale(' + (.5 + sk * 1.7).toFixed(3) + ')';
    };
  }

  /* ========================================================= plate VII — S11 */
  function buildS11(node, ai) {
    const cart = mk('div', 's11-cart', node);
    ['tl', 'tr', 'bl', 'br'].forEach(c => {
      const d = mk('div', 'cc ' + c, cart);
      d.innerHTML = ORN_SVG.corner;
    });
    rv(cart, ai, .3, 1.0, .62);

    const col = mk('div', 's11-colophon', node,
      '<b>COLOPHON</b>FILM \u00b7 ONE INK, ONE HAND<br>PLATES \u00b7 SEVEN<br>SPRITES \u00b7 XXV ENGRAVINGS<br>TYPE \u00b7 CORMORANT, PLAYFAIR, JOST, FELL');
    rv(col, ai, .95, .8, .55);

    const ed = mk('div', 's11-colophon', node,
      '<b>EDITION 01</b>MMXXVI \u00b7 45 SECONDS<br>1920 \u00d7 1080 \u00b7 24 FPS<br>ONE COLOUR \u00b7 NOT TAROT');
    ed.style.left = 'auto'; ed.style.right = '132px';
    ed.style.top = '186px'; ed.style.bottom = 'auto'; ed.style.textAlign = 'right';
    rv(ed, ai, 1.05, .8, .5);
  }

  /* ===================================================== chrome + stamp + tip */
  function buildChromeOrn() {
    ['tl', 'tr', 'bl', 'br'].forEach(c => {
      const d = mk('div', 'corner-orn ' + c, chrome);
      d.innerHTML = ORN_SVG.corner;
    });
  }

  const STAMPS = [[8.0, 'II', '符号'], [14.0, 'III', '世界'], [22.0, 'IV', '牌'],
                  [24.5, 'V', '抽牌'], [33.5, 'VI', '印记'], [40.0, 'VII', '名']];
  function buildStamp() {
    stampEl = mk('div', 'plate-stamp', fxEl);
    mk('span', 'ps-cap', stampEl, '图版');
    stampNum = mk('span', 'ps-num', stampEl, 'I');
    stampSub = mk('span', 'ps-sub', stampEl, '心');
  }
  function paintStamp(t) {
    let hit = null;
    for (const s of STAMPS) if (t >= s[0] && t < s[0] + 1.55) hit = s;
    if (!hit) { stampEl.style.opacity = '0'; return; }
    const u = (t - hit[0]) / 1.55;
    const op = E.outC(clamp01(u / .16)) * (1 - E.inOut(clamp01((u - .52) / .48))) * .9;
    stampEl.classList.toggle('inv', document.body.classList.contains('dark'));
    stampEl.style.opacity = op.toFixed(3);
    const rot = -13 + 9 * E.outC(clamp01(u / .4));
    const sc = 1.14 - .14 * E.outC(clamp01(u / .34));
    stampEl.style.transform = 'rotate(' + rot.toFixed(2) + 'deg) scale(' + sc.toFixed(3) + ')';
    if (stampNum.textContent !== hit[1]) {
      stampNum.textContent = hit[1];
      stampSub.textContent = hit[2];
    }
  }

  function buildTip() {
    tipEl = mk('div', null, stage);
    tipEl.id = 'symTip';
    tipK = mk('span', 'tt-k', tipEl, '符号');
    tipName = mk('b', null, tipEl, '\u2014');
    tipDesc = mk('em', null, tipEl, '');
  }
  function showTip(name, num) {
    const NAMES = window.NT.SYM_NAMES || {};
    const info = NAMES[name];
    tipK.textContent = num ? '符号 \u00b7 ' + num : '符号';
    tipName.textContent = info ? info[0] : String(name || '');
    tipDesc.textContent = info ? info[1] + ' \u00b7 ' + info[2] : '一个未读的符号';
    tipEl.classList.add('on');
  }
  function hideTip() { if (tipEl) tipEl.classList.remove('on'); }

  function bindInteractions() {
    stage.addEventListener('pointerover', e => {
      const t = e.target;
      const s = t && t.closest ? t.closest('.s3-sym,.s8-sym,.s9-sym') : null;
      if (s && s.dataset.name) { showTip(s.dataset.name, s.dataset.num); return; }
      hideTip();
    });
    stage.addEventListener('pointermove', () => {
      if (tipEl && tipEl.classList.contains('on')) {
        tipEl.style.left = ST.ptr.x + 'px';
        tipEl.style.top = (ST.ptr.y - 16) + 'px';
      }
    });
    stage.addEventListener('pointerleave', hideTip);
    window.addEventListener('keydown', e => {
      const k = e.key;
      if (k >= '1' && k <= '7' && ST.started && !e.metaKey && !e.ctrlKey && !e.altKey) {
        const p = PLATES[+k - 1];
        if (!p) return;
        e.preventDefault();
        seek(Math.max(.02, p.t));
        try { sfx('click'); syncPlayIcon(); wake(); } catch (err) {}
      }
    });
  }

  /* --------------------------------------------------------------- builders */
  const BUILDERS = [buildS1, buildS2, buildS3, buildS4, buildS5, buildS6,
                    buildS7, buildS8, buildS9, buildS10, buildS11];

  function paint(t) {
    if (!ready) {
      ready = true;
      for (let i = 0; i < SCENES.length; i++) {
        if (BUILDERS[i]) BUILDERS[i](SCENES[i].node, i);
      }
      buildChromeOrn(); buildStamp(); buildTip(); bindInteractions();
    }
    let ai = 0;
    for (let i = 0; i < T.length; i++) if (t >= T[i][0]) ai = i;
    const local = t - T[ai][0];
    const list = REV[ai];
    if (list) {
      for (let i = 0; i < list.length; i++) {
        const el = list[i];
        const p = el.dataset.rv.split(',');
        el.style.opacity = (E.outC(wt(local, +p[0], +p[0] + +p[1])) * +p[2]).toFixed(3);
      }
    }
    if (UPD[ai]) UPD[ai](local, t);
    paintStamp(t);
    if (tipEl && tipEl.classList.contains('on')) {
      tipEl.style.left = ST.ptr.x + 'px';
      tipEl.style.top = (ST.ptr.y - 16) + 'px';
    }
  }

  return { paint: paint, hideTip: hideTip };
})();

window.NT.Extras = Extras;
