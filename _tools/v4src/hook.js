/* =====================================================================
   hook.js — cold open, v2 · 「校样 · PROOF」  (0 – 2.56 s)

   The plate is already there on frame one: paper, frame, registration.
   「别划走」 is set in ink on that paper. A torn ink flood sweeps in,
   「这不是塔罗」 is printed bone-on-ink and sealed with a crimson 非,
   then the ink drains and dissolves into plate I (which is running
   underneath). Finally one retention line — 看到最后 · 抽一张属于你的牌.

   Pure function of film time t → deterministic stills at any t.
   ===================================================================== */
const HookFX = (() => {
  const END = 2.56;
  const REVEAL = 1.24;

  let root = null, stage = null, act1 = null, act2 = null,
      paper = null, grain = null, vig = null,
      kick = null, l1 = null, ink = null, l2 = null, cap = null,
      seal = null, chip = null, hdr = null, ftr = null, frame = null,
      flash = null, rules = [], mks = [];

  function setBg(el, key) {
    if (!el || !window.TX || !window.TX[key]) return;
    el.style.backgroundImage = 'url("' + window.TX[key] + '")';
  }

  function build() {
    const stageEl = document.getElementById('stage');
    if (!stageEl) return false;

    root = document.createElement('div');
    root.id = 'hook';
    root.setAttribute('aria-hidden', 'true');
    root.innerHTML =
      '<div class="hk-stage">' +
        '<div class="hk-paper"></div><div class="hk-tone"></div>' +
        '<div class="hk-vig"></div><div class="hk-grain"></div>' +
        '<svg class="hk-frame" viewBox="0 0 1920 1080" preserveAspectRatio="none"></svg>' +
        '<div class="hk-hdr"><span>NOT TAROT — 校样</span><span>第 Ⅰ 图版 / Ⅶ</span></div>' +
        '<div class="hk-ftr"><span>FIG. 0 — GUTTA</span><span>MMXXVI</span></div>' +
        '<i class="hk-mk a"></i><i class="hk-mk b"></i>' +
        '<i class="hk-mk c"></i><i class="hk-mk d"></i>' +
        '<div class="hk-act1">' +
          '<div class="hk-kick">四 十 五 秒<i class="dia"></i>七 张 图 版<i class="dia"></i>一 个 问 题</div>' +
          '<i class="hk-rule r1"></i>' +
          '<div class="hk-l1">别 <em>划</em> 走</div>' +
          '<i class="hk-rule r2"></i>' +
        '</div>' +
        '<div class="hk-ink"><i></i><b></b></div>' +
        '<div class="hk-act2">' +
          '<div class="hk-l2">这不是<span class="b">塔罗</span></div>' +
          '<div class="hk-cap">一颗心<i class="dia"></i>七张图版<i class="dia"></i>最后一张，由你决定</div>' +
        '</div>' +
        '<div class="hk-seal"><i></i><b>非</b></div>' +
        '<div class="hk-flash"></div>' +
      '</div>' +
      '<div class="hk-chip">看到最后<i class="dia"></i>抽一张属于你的牌</div>';
    stageEl.appendChild(root);

    stage = root.querySelector('.hk-stage');
    paper = root.querySelector('.hk-paper');
    grain = root.querySelector('.hk-grain');
    vig = root.querySelector('.hk-vig');
    frame = root.querySelector('.hk-frame');
    hdr = root.querySelector('.hk-hdr');
    ftr = root.querySelector('.hk-ftr');
    act1 = root.querySelector('.hk-act1');
    act2 = root.querySelector('.hk-act2');
    kick = root.querySelector('.hk-kick');
    l1 = root.querySelector('.hk-l1');
    ink = root.querySelector('.hk-ink');
    l2 = root.querySelector('.hk-l2');
    cap = root.querySelector('.hk-cap');
    seal = root.querySelector('.hk-seal');
    chip = root.querySelector('.hk-chip');
    flash = root.querySelector('.hk-flash');
    rules = [root.querySelector('.hk-rule.r1'), root.querySelector('.hk-rule.r2')];
    mks = [
      root.querySelector('.hk-mk.a'), root.querySelector('.hk-mk.b'),
      root.querySelector('.hk-mk.c'), root.querySelector('.hk-mk.d'),
    ];

    /* paper stock + film treatment, re-used from the film's own textures */
    setBg(paper, 'paper_cream');
    setBg(grain, 'grain_0');
    setBg(vig, 'vignette');
    if (flash) setBg(flash, 'paper_cream');
    setBg(root.querySelector('.hk-ink > i'), 'grain_0');
    setBg(root.querySelector('.hk-ink > b'), 'grain_1');
    setBg(root.querySelector('.hk-seal > i'), 'grain_0');
    const mask = (window.TX && (window.TX.ink_flood || window.TX.ink_0 || window.TX.ink_1)) || null;
    if (mask) root.style.setProperty('--inkmask', 'url("' + mask + '")');

    /* plate frame: double hairline + centre ticks, matching the film chrome */
    frame.innerHTML =
      '<g fill="none" stroke="currentColor" stroke-width="1">' +
        '<rect x="64.5" y="64.5" width="1791" height="951" opacity="1"></rect>' +
        '<rect x="78.5" y="78.5" width="1763" height="923" opacity=".5"></rect>' +
        '<path d="M960 64v14M960 1002v14M64 540h14M1842 540h14" opacity=".72"></path>' +
      '</g>';

    return true;
  }

  function tick(t) {
    if (!root && !build()) return;
    if (t >= END) {
      root.classList.add('off');
      return;
    }
    root.classList.remove('off');

    /* stage dissolves into plate I once the ink has drained */
    const stageFade = 1 - E.inOut(wt(t, 1.19, 1.24));
    if (t >= REVEAL) {
      stage.style.display = 'none';
    } else {
      stage.style.display = '';
      stage.style.opacity = String(stageFade);
    }

    /* ---- act 1: paper, registration, the first sentence ---- */
    /* frame one already carries the hook: it doubles as the platform cover */
    const kin = 0.92;
    kick.style.opacity = String(kin);
    rules[0].style.transform = 'scaleX(' + E.outC(wt(t, 0.00, 0.26)) + ')';
    rules[1].style.transform = 'scaleX(' + E.outC(wt(t, 0.05, 0.32)) + ')';
    for (let i = 0; i < mks.length; i++) {
      mks[i].style.opacity = String(0.5 * E.outC(wt(t, 0.06 + i * 0.04, 0.36 + i * 0.04)));
    }

    const l1in = 1;
    const l1out = t >= 0.56 ? 1 : 0;
    const l1s = lerp(1.055, 1, E.outC(wt(t, 0.00, 0.80)));
    l1.style.opacity = String(l1in * (1 - l1out));
    l1.style.transform = 'translate3d(0,0,0) scale(' + l1s + ')';

    /* ---- the torn ink flood: in 0.30–0.64, out 1.00–1.28 ---- */
    const fin = E.outC(wt(t, 0.26, 0.58));
    const fout = E.inC(wt(t, 1.02, 1.20));
    const iout = E.inOut(wt(t, 1.150, 1.180));
    const iop = E.outC(wt(t, 0.26, 0.32)) * (1 - iout);
    ink.style.opacity = String(iop);
    /* warm bloom that swallows the dissolve — reads as a page catching light */
    const fl = Math.max(0, Math.min(
      E.outC(wt(t, 1.138, 1.162)),
      1 - E.inOut(wt(t, 1.162, 1.216))
    ));
    if (flash) flash.style.opacity = String(fl * 0.95);
    const impact = t >= 0.56 ? Math.exp(-(t - 0.56) * 13) * 3 : 0;
    stage.style.transform = 'translate3d(0,' + impact + 'px,0)';
    if (fout > 0) {
      const fy = lerp(0, -2.4, fout);
      const fr = lerp(-1.5, -0.6, fout);
      const fs = lerp(1, 1.02, fout);
      ink.style.transform = 'translate3d(0,' + fy + '%,0) rotate(' + fr + 'deg) scale(' + fs + ')';
    } else {
      const ix = lerp(30, 0, fin);
      const isx = lerp(0.64, 1, fin);
      const isy = lerp(0.92, 1, fin);
      ink.style.transform = 'translate3d(' + ix + '%,0,0) rotate(-1.5deg) scale(' + isx + ',' + isy + ')';
    }

    /* ---- act 2: second sentence on the ink + the 非 stamp ---- */
    const a2in = E.outC(wt(t, 0.56, 0.74));
    const a2out = E.inOut(wt(t, 1.00, 1.12));
    const a2s = lerp(1.05, 1, E.outC(wt(t, 0.56, 0.92)));
    l2.style.opacity = String(a2in * (1 - a2out));
    l2.style.transform = 'translate3d(0,' + ((1 - a2in) * 22) + 'px,0) scale(' + a2s + ')';
    const cin = E.outC(wt(t, 0.64, 0.84));
    cap.style.opacity = String(cin * (1 - E.inOut(wt(t, 1.03, 1.15))));

    const sIn = E.outC(wt(t, 0.72, 0.78));
    const sPunch = E.outC(wt(t, 0.74, 0.92));
    const sOut = E.inOut(wt(t, 1.04, 1.16));
    const jk = t - 0.76;
    const jolt = jk > 0 ? Math.exp(-jk * 9) * 6 : 0;
    seal.style.opacity = String(sIn * (1 - sOut));
    seal.style.transform =
      'translate3d(' + (jolt * 0.7) + 'px,' + jolt + 'px,0) ' +
      'rotate(' + lerp(-15, -9, sPunch) + 'deg) ' +
      'scale(' + lerp(1.46, 1, sPunch) + ')';

    /* ---- chrome fades with the stage ---- */
    const chf = 1 - E.inOut(wt(t, 1.04, 1.18));
    const hdrOp = 0.56 * chf;
    hdr.style.opacity = String(hdrOp);
    ftr.style.opacity = String(hdrOp * 0.82);
    frame.style.opacity = String(0.46 * chf);
    if (act1) act1.style.opacity = String(chf);

    /* ---- retention line on the revealed plate ---- */
    const chipIn = E.outC(wt(t, 1.26, 1.48));
    const chipOut = 1 - E.inOut(wt(t, 2.30, 2.52));
    chip.style.opacity = String(chipIn * chipOut);
    chip.style.transform = 'translateX(-50%) translateY(' + ((1 - chipIn) * 14) + 'px)';
  }

  return { build: build, tick: tick, END: END };
})();

if (window.NT) window.NT.Hook = HookFX;
