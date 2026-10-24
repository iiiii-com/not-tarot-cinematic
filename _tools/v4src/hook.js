/* =====================================================================
   hook.js — the cold open (0 – 2.56 s)

   A short-video hook that keeps the plate language:
   black plate → 「别划走」 → 「这不是塔罗」 (塔罗 struck through) →
   white flash → the plate splits open and the paper world begins.

   Everything is a pure function of film time t, so ?capture=1 stills
   are deterministic at any t.
   ===================================================================== */
const HookFX = (() => {
  const END = 2.56;
  let root = null, veil = null, top = null, bot = null, seam = null,
      kick = null, l1 = null, l2 = null, sub = null, blot = null,
      strike = null, chip = null, flash = null,
      rules = [], corners = [];

  function beat(t, beats) {
    let v = 0;
    for (let i = 0; i < beats.length; i++) {
      const k = t - beats[i];
      if (k >= 0 && k < 0.36) {
        v = Math.max(v, k < 0.06 ? E.out(k / 0.06) : 1 - (k - 0.06) / 0.30);
      }
    }
    return v;
  }

  function build() {
    const stage = document.getElementById('stage');
    if (!stage) return false;
    root = document.createElement('div');
    root.id = 'hook';
    root.setAttribute('aria-hidden', 'true');
    root.innerHTML =
      '<div class="hk-veil">' +
        '<div class="hk-top"></div><div class="hk-bot"></div><div class="hk-seam"></div>' +
      '</div>' +
      '<i class="hk-rule r1"></i><i class="hk-rule r2"></i>' +
      '<i class="hk-corner tl"></i><i class="hk-corner tr"></i>' +
      '<i class="hk-corner bl"></i><i class="hk-corner br"></i>' +
      '<div class="hk-center">' +
        '<div class="hk-blot"></div>' +
        '<div class="hk-kick">NOT TAROT · 一颗心的四十五秒</div>' +
        '<div class="hk-l1" data-tx="别 划 走">别 划 走</div>' +
        '<div class="hk-l2" data-tx="这不是塔罗">' +
          '<span class="hk-a">这不是</span><span class="hk-b">塔罗<i class="hk-strike"></i></span>' +
        '</div>' +
        '<div class="hk-sub">一颗心<i class="hk-dia">◆</i>七张图版<i class="hk-dia">◆</i>最后一张牌，由你决定</div>' +
      '</div>' +
      '<div class="hk-chip">看到最后 <span class="hk-arrow">→</span> 抽一张属于你的牌</div>' +
      '<div class="hk-flash"></div>';
    stage.appendChild(root);

    veil = root.querySelector('.hk-veil');
    top = root.querySelector('.hk-top');
    bot = root.querySelector('.hk-bot');
    seam = root.querySelector('.hk-seam');
    kick = root.querySelector('.hk-kick');
    l1 = root.querySelector('.hk-l1');
    l2 = root.querySelector('.hk-l2');
    sub = root.querySelector('.hk-sub');
    blot = root.querySelector('.hk-blot');
    strike = root.querySelector('.hk-strike');
    chip = root.querySelector('.hk-chip');
    flash = root.querySelector('.hk-flash');
    /* torn-ink edge from the generated ink mask (deterministic, no images) */
    var ink = (window.TX && (window.TX.ink_0 || window.TX.ink_1)) || null;
    if (ink) root.style.setProperty('--inkmask', 'url("' + ink + '")');
    rules = [root.querySelector('.hk-rule.r1'), root.querySelector('.hk-rule.r2')];
    corners = [
      root.querySelector('.hk-corner.tl'), root.querySelector('.hk-corner.tr'),
      root.querySelector('.hk-corner.bl'), root.querySelector('.hk-corner.br'),
    ];
    return true;
  }

  function tick(t) {
    if (!root && !build()) return;
    if (t >= END) {
      if (!root.classList.contains('off')) root.classList.add('off');
      return;
    }
    root.classList.remove('off');

    const STx = (window.NT && window.NT.ST) || { ptr: { nx: 0, ny: 0 } };
    const ptr = STx.ptr || { nx: 0, ny: 0 };

    /* ---- plate split (the reveal) ---- */
    const K = E.inC(wt(t, 1.00, 1.36));
    top.style.transform = 'translateY(' + (-104 * K).toFixed(2) + '%)';
    bot.style.transform = 'translateY(' + (104 * K).toFixed(2) + '%)';
    if (K >= 0.999) {
      if (veil.style.display !== 'none') veil.style.display = 'none';
    } else {
      if (veil.style.display === 'none') veil.style.display = '';
      veil.style.opacity = '1';
    }
    seam.style.opacity = t > 0.97
      ? String(Math.max(0, 1 - K * 1.7) * (0.72 + 0.28 * Math.sin(t * 47)))
      : '0';
    seam.style.transform = 'scaleX(' + (1 - K * 0.55).toFixed(3) + ')';

    /* ---- calibration rules + corner marks ---- */
    const r1 = E.outC(wt(t, 0.03, 0.40));
    const r2 = E.outC(wt(t, 0.16, 0.52));
    const ruleOut = 1 - E.inC(wt(t, 1.00, 1.22));
    if (rules[0]) { rules[0].style.transform = 'scaleX(' + r1.toFixed(3) + ')'; rules[0].style.opacity = String(0.9 * ruleOut); }
    if (rules[1]) { rules[1].style.transform = 'scaleX(' + r2.toFixed(3) + ')'; rules[1].style.opacity = String(0.9 * ruleOut); }
    const ck = E.outC(wt(t, 0.10, 0.50)) * (1 - E.inC(wt(t, 1.00, 1.20)));
    for (let i = 0; i < corners.length; i++) corners[i].style.opacity = String(ck * 0.8);

    /* ---- kicker ---- */
    const kickIn = E.outC(wt(t, 0.02, 0.16));
    kick.style.opacity = String(kickIn * (1 - E.inC(wt(t, 0.42, 0.50))));
    kick.style.transform = 'translateY(' + ((1 - kickIn) * 10).toFixed(1) + 'px)';

    /* ---- line 1 · 别划走 ---- */
    const a1 = E.outC(wt(t, 0.05, 0.20));
    const o1 = E.inC(wt(t, 0.47, 0.55));
    l1.style.opacity = String(Math.max(0, a1 * (1 - o1)));
    l1.style.transform = 'translateY(' + ((1 - a1) * 30 - o1 * 22).toFixed(1) + 'px) scale(' +
      lerp(1.09, 1, a1).toFixed(3) + ')';

    /* ---- line 2 · 这不是塔罗 (slam + jolt) ---- */
    const a2 = E.outC(wt(t, 0.53, 0.63));
    const o2 = E.inC(wt(t, 0.94, 1.04));
    const jk = t - 0.53;
    const jolt = jk > 0 ? Math.exp(-jk * 8.6) * 30 : 0;
    const jx = Math.sin(t * 96) * jolt;
    const jy = Math.cos(t * 73) * jolt * 0.45;
    l2.style.opacity = String(Math.max(0, a2 * (1 - o2)));
    l2.style.transform = 'translate(calc(-50% + ' + jx.toFixed(1) + 'px), calc(-50% + ' + jy.toFixed(1) + 'px)) scale(' +
      (1 + (1 - a2) * 0.26 - o2 * 0.02).toFixed(3) + ')';

    /* ---- crimson blot behind the line ---- */
    const bg = E.outC(wt(t, 0.52, 0.94));
    const bo = 1 - E.inC(wt(t, 1.02, 1.20));
    const bt = beat(t, [0.56, 0.80, 0.99, 1.14]);
    blot.style.opacity = String(0.9 * bg * bo);
    blot.style.transform = 'scale(' + (0.18 + bg * 0.94 + bt * 0.05).toFixed(3) + ') rotate(' + (t * 9).toFixed(1) + 'deg)';

    /* ---- the strike through 塔罗 ---- */
    const sk = E.outC(wt(t, 0.68, 0.92));
    strike.style.transform = 'rotate(-2.2deg) scaleX(' + sk.toFixed(3) + ')';
    strike.style.opacity = String(0.92 * sk * (1 - o2));

    /* ---- sub line ---- */
    const sIn = E.outC(wt(t, 0.78, 0.92));
    const sOut = E.inC(wt(t, 1.02, 1.12));
    sub.style.opacity = String(sIn * (1 - sOut));
    sub.style.transform = 'translateY(' + ((1 - sIn) * 14).toFixed(1) + 'px)';

    /* ---- flashes (impact + reveal) ---- */
    const f1 = Math.max(0, 1 - Math.abs(t - 1.00) / 0.075);
    const f2 = Math.max(0, 1 - Math.abs(t - 1.36) / 0.055);
    flash.style.opacity = String(Math.min(1, f1 * 0.9 + f2 * 0.38));

    /* ---- chromatic offsets for the ghost layers ---- */
    let hx = (7.5 + 3.6 * Math.sin(t * 5.1)) * (1 + jolt * 0.09) + ptr.nx * 7;
    let hy = (5.4 + 3.0 * Math.cos(t * 6.3)) * (1 + jolt * 0.07) + ptr.ny * 5;
    if (t > 1.00) {
      const fade = Math.max(0.2, 1 - (t - 1.00) * 3);
      hx *= fade; hy *= fade;
    }
    root.style.setProperty('--hx', hx.toFixed(2));
    root.style.setProperty('--hy', hy.toFixed(2));

    /* ---- retention chip on the revealed paper ---- */
    const cIn = E.outC(wt(t, 1.46, 1.60));
    const cOut = E.inOut(wt(t, 2.40, 2.56));
    chip.style.opacity = String(cIn * (1 - cOut));
    chip.style.transform = 'translate(-50%, ' +
      (Math.sin(t * 0.9) * 1.6 + (1 - cIn) * 10).toFixed(1) + 'px)';
  }

  return { tick: tick, build: build };
})();

if (window.NT) window.NT.Hook = HookFX;
