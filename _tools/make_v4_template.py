"""Build the v4 template: new gallery layout, typography, scene refinements.

Reads:  _tools/cinematic_v3_template.html   (working scene JS)
Writes: _tools/cinematic_v4_template.html   (markup placeholders for assets/fonts)
"""
import re
from pathlib import Path

ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
SRC = ROOT / "_tools" / "cinematic_v3_template.html"
DST = ROOT / "_tools" / "cinematic_v4_template.html"

s = SRC.read_text(encoding="utf-8")


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f"pattern x{n} (expected {count}): {old[:90]!r}"
    s = s.replace(old, new)


def replace_between(start, end, new):
    """Replace text from start marker (inclusive) up to end marker (exclusive)."""
    global s
    i = s.index(start)
    j = s.index(end, i)
    s = s[:i] + new + s[j:]

# ---------------------------------------------------------------- CSS ----
CSS = r"""
:root{
  --ink:#14100F; --berry:#8F2C3B; --cream:#FAF2EC; --gold:#7B5521;
  --bone:#F7F2E6; --plum:#241F22; --env:#0B0908; --rose:#F6B7CC;
  --serif:'Cormorant Garamond',Georgia,'Times New Roman',serif;
  --sans:'Jost','Segoe UI',Arial,sans-serif;
}
/*__FONTS__*/
*{ box-sizing:border-box; }
html,body{ margin:0; height:100%; background:#171214; overflow:hidden; -webkit-font-smoothing:antialiased; }
#fit{ position:fixed; inset:0; display:flex; align-items:center; justify-content:center;
      background:radial-gradient(120% 92% at 50% 38%, #2b2225 0%, #1a1518 58%, #100d0f 100%); }
#fit:after{ content:''; position:fixed; inset:0; pointer-events:none; opacity:.42;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/></filter><rect width='180' height='180' filter='url(%23n)' opacity='0.06'/></svg>"); }
#shell{ display:flex; flex-direction:column; align-items:center; transition:width .25s ease; }
#stageWrap{ position:relative; overflow:hidden; box-shadow:0 36px 90px rgba(0,0,0,.6), 0 1px 0 rgba(247,242,230,.10); }
#stage{ position:relative; width:1920px; height:1080px; overflow:hidden;
       transform-origin:top left; background:var(--cream); }
#stageBg{ position:absolute; inset:0; background:var(--cream); }
#paper{ position:absolute; inset:0; background-image:url(TEX_PAPER); background-size:1500px auto;
        mix-blend-mode:multiply; opacity:.55; pointer-events:none; }
#tooth{ position:absolute; inset:0; pointer-events:none; opacity:.5; mix-blend-mode:multiply;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='t'><feTurbulence type='fractalNoise' baseFrequency='0.62' numOctaves='3'/></filter><rect width='300' height='300' filter='url(%23t)' opacity='0.10'/></svg>"); }
#scenes{ position:absolute; inset:0; }
.scene{ position:absolute; inset:0; opacity:0; display:none; }
#grain{ position:absolute; inset:0; pointer-events:none; opacity:.5; z-index:24;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/></filter><rect width='160' height='160' filter='url(%23n)' opacity='0.055'/></svg>"); }
#vignette{ position:absolute; inset:0; pointer-events:none; z-index:23;
  background:radial-gradient(120% 95% at 50% 45%, rgba(0,0,0,0) 52%, rgba(60,35,28,.14) 100%); }
body.dark #vignette{ background:radial-gradient(115% 92% at 50% 46%, rgba(0,0,0,0) 38%, rgba(0,0,0,.55) 100%); }
#plate{ position:absolute; inset:32px; border:1px solid rgba(20,16,15,.22); pointer-events:none; z-index:25; }
body.dark #plate{ border-color:rgba(247,242,230,.18); }
#plate i{ position:absolute; width:13px; height:13px; border:0 solid rgba(20,16,15,.40); }
body.dark #plate i{ border-color:rgba(247,242,230,.34); }
#plate .c1{ left:-1px; top:-1px; border-left-width:1px; border-top-width:1px; }
#plate .c2{ right:-1px; top:-1px; border-right-width:1px; border-top-width:1px; }
#plate .c3{ left:-1px; bottom:-1px; border-left-width:1px; border-bottom-width:1px; }
#plate .c4{ right:-1px; bottom:-1px; border-right-width:1px; border-bottom-width:1px; }

/* ---------------- hud ---------------- */
#hud{ width:100%; display:flex; align-items:center; gap:26px; padding:18px 2px 0;
      color:rgba(247,242,230,.68); font:400 12px/1 var(--sans); letter-spacing:.26em; }
#hud .hLeft{ min-width:170px; }
#act{ color:rgba(247,242,230,.92); letter-spacing:.3em; }
#hud .hMid{ flex:1; }
#bar{ height:1px; background:rgba(247,242,230,.16); position:relative; }
#barFill{ position:absolute; left:0; top:-1px; height:3px; width:0; background:var(--berry); }
#hud .hRight{ display:flex; align-items:center; gap:18px; }
#tc{ min-width:96px; letter-spacing:.18em; color:rgba(247,242,230,.72); }
#hud button{ all:unset; cursor:pointer; font:400 11px/1 var(--sans); letter-spacing:.26em;
             color:rgba(247,242,230,.55); padding:2px 0; border-bottom:1px solid transparent; transition:all .2s; }
#hud button:hover{ color:var(--bone); border-bottom-color:rgba(247,242,230,.5); }
#chapters{ display:flex; gap:30px; padding:15px 2px 0; width:100%; }
.chap{ font:400 10px/1 var(--sans); letter-spacing:.24em; text-transform:uppercase;
       color:rgba(247,242,230,.34); cursor:pointer; position:relative; padding-bottom:7px; transition:color .25s; white-space:nowrap; }
.chap:hover{ color:rgba(247,242,230,.72); }
.chap.on{ color:var(--bone); }
.chap.on:after{ content:''; position:absolute; left:0; right:0; bottom:0; height:1px; background:var(--berry); }

/* ---------------- poster ---------------- */
#poster{ position:absolute; inset:0; background:var(--cream); z-index:40; cursor:pointer;
         display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }
#poster .pTop{ font:600 128px/1 var(--serif); letter-spacing:.2em; padding-left:.2em; color:var(--ink); }
#poster .pRule{ width:560px; height:1px; background:rgba(20,16,15,.45); margin:46px 0 42px; position:relative; }
#poster .pRule:before,#poster .pRule:after{ content:''; position:absolute; top:-3px; width:7px; height:7px;
   background:var(--berry); transform:rotate(45deg); }
#poster .pRule:before{ left:-4px; } #poster .pRule:after{ right:-4px; }
#poster .pTag{ font:400 33px/2.05 'Songti SC','SimSun',serif; letter-spacing:.2em; color:var(--ink); opacity:.88; }
#poster .pMeta{ font:400 12px/1 var(--sans); letter-spacing:.46em; color:var(--berry); margin-top:52px; }
#poster .pBtn{ font:400 11px/1 var(--sans); letter-spacing:.36em; border:1px solid rgba(20,16,15,.38);
   padding:15px 28px; margin-top:58px; color:rgba(20,16,15,.78); animation:pulse 2.8s ease-in-out infinite; }
@keyframes pulse{ 0%,100%{ opacity:.42 } 50%{ opacity:.95 } }

/* ---------------- draw card ---------------- */
#draw{ position:absolute; inset:0; background:rgba(11,9,8,.94); z-index:45; display:none;
       align-items:center; justify-content:center; flex-direction:column; gap:34px; color:var(--bone); }
#draw.show{ display:flex; }
#draw .dh{ font:400 11px/1 var(--sans); letter-spacing:.46em; opacity:.6; }
#draw .dcard{ width:470px; height:700px; border:1px solid rgba(247,242,230,.45); border-radius:4px;
              display:flex; flex-direction:column; align-items:center; justify-content:center; gap:26px;
              background:#1a1518; position:relative; }
#draw .dcard:before{ content:''; position:absolute; inset:13px; border:1px solid rgba(247,242,230,.18); border-radius:2px; }
#draw .dcard img{ width:300px; height:300px; object-fit:contain; }
#draw .dn{ font:600 27px/1 var(--serif); letter-spacing:.3em; }
#draw .dm{ font:400 17px/1.85 'Songti SC','SimSun',serif; letter-spacing:.12em; max-width:340px; text-align:center; opacity:.82; }
#draw button{ all:unset; cursor:pointer; border:1px solid rgba(247,242,230,.42); padding:11px 20px;
              font:400 11px/1 var(--sans); letter-spacing:.3em; color:var(--bone); }
#draw button:hover{ background:rgba(247,242,230,.08); }

/* ---------------- vertical page ---------------- */
#vertTop,#vertBot{ display:none; }
body.vertical #fit{ background:var(--cream); }
body.vertical #fit:after{ display:none; }
body.vertical #shell{ height:1920px; justify-content:space-between; }
body.vertical #stageWrap{ box-shadow:none; }
body.vertical #hud,body.vertical #chapters{ display:none; }
body.vertical #vertTop,body.vertical #vertBot{ display:flex; flex-direction:column; align-items:center;
   justify-content:center; width:1080px; flex:1 1 0; color:var(--ink); }
body.vertical .vt1{ font:600 27px/1 var(--serif); letter-spacing:.52em; padding-left:.52em; }
body.vertical .vt2{ font:400 10px/1 var(--sans); letter-spacing:.42em; margin-top:22px; color:var(--berry); }
body.vertical .vt3{ font:400 10px/1 var(--sans); letter-spacing:.5em; margin-top:52px; opacity:.42; }
body.vertical .vb1{ font:400 14px/1 var(--sans); letter-spacing:.36em; }
body.vertical .vb2{ font:400 9px/1 var(--sans); letter-spacing:.32em; margin-top:18px; opacity:.5; }

/* ---------------- capture ---------------- */
body.capture #hud,body.capture #chapters,body.capture #poster,
body.capture #vertTop,body.capture #vertBot{ display:none !important; }
body.capture #fit{ background:var(--cream); display:block; }
body.capture #fit:after{ display:none; }
body.capture #shell{ width:1920px; height:1080px; }
body.capture #stageWrap{ box-shadow:none; }
body.vertical.capture #shell{ width:1080px; height:1920px; }
"""

i = s.index("<style>")
j = s.index("</style>") + len("</style>")
s = s[:i] + "<style>" + CSS + "</style>" + s[j:]

# ---------------------------------------------------------------- body ----
BODY = r"""
<body>
<div id="fit"><div id="shell">
  <div id="vertTop">
    <div class="vt1">NOT TAROT</div>
    <div class="vt2">AN ENTIRELY ORIGINAL DECK OF SIX PERSONALITY CARDS</div>
    <div class="vt3">I &nbsp;·&nbsp; II &nbsp;·&nbsp; III &nbsp;·&nbsp; IV &nbsp;·&nbsp; V &nbsp;·&nbsp; VI &nbsp;·&nbsp; VII</div>
  </div>
  <div id="stageWrap"><div id="stage">
    <div id="stageBg"></div>
    <div id="paper"></div>
    <div id="tooth"></div>
    <div id="scenes"></div>
    <div id="vignette"></div>
    <div id="plate"><i class="c1"></i><i class="c2"></i><i class="c3"></i><i class="c4"></i></div>
    <div id="grain"></div>
    <div id="poster">
      <div class="pTop">NOT TAROT</div>
      <div class="pRule"></div>
      <div class="pTag">你抽到的，不只是一张牌<br>而是一个关于自己的答案</div>
      <div class="pMeta">A FILM IN SEVEN PLATES &nbsp;·&nbsp; 45 SEC</div>
      <div class="pBtn">CLICK TO BEGIN &nbsp;·&nbsp; 点击开始</div>
    </div>
    <div id="draw">
      <div class="dh">YOUR CARD &nbsp;·&nbsp; 你的卡</div>
      <div class="dcard"><img id="dimg" alt=""><div class="dn" id="dname"></div><div class="dm" id="dmean"></div></div>
      <button id="dBtn">DRAW AGAIN &nbsp;·&nbsp; 再抽一张</button>
    </div>
  </div></div>
  <div id="hud">
    <div class="hLeft"><span id="act">I · HEART</span></div>
    <div class="hMid"><div id="bar"><div id="barFill"></div></div></div>
    <div class="hRight">
      <span id="tc">00:00:00</span>
      <button id="bPlay">PAUSE</button>
      <button id="bMute">SOUND ON</button>
      <button id="bRestart">REPLAY</button>
    </div>
  </div>
  <div id="chapters"></div>
  <div id="vertBot">
    <div class="vb1">MAKE YOUR OWN MEANING.</div>
    <div class="vb2">SIX CARDS &nbsp;·&nbsp; ONE ANSWER THAT IS YOURS &nbsp;·&nbsp; MMXXVI</div>
  </div>
</div></div>
<script>
"""
i = s.index("<body>")
j = s.index("<script>")
s = s[:i] + BODY + s[j + len("<script>"):]
s = s.replace("<script>\n<script>", "<script>")

# ------------------------------------------------------------- JS edits --
# fonts
s = s.replace("Georgia,serif", "Cormorant Garamond, Georgia, serif")

# palette constant
rep("const INK='#14100F', BERRY='#8F2C3B', CREAM='#FAF2EC', GOLD='#7B5521', BONE='#F7F2E6', PLUM='#241F22', ENV='#0B0908';",
    "const INK='#14100F', BERRY='#8F2C3B', CREAM='#FAF2EC', GOLD='#7B5521', BONE='#F7F2E6', PLUM='#241F22', ENV='#0B0908', ROSE='#F6B7CC';")

# ---------- S01 tag
rep("const cap=T('ONE DROP.',d,{left:'0',width:W+'px',top:(H*0.80)+'px',textAlign:'center',font:'600 30px Cormorant Garamond, Georgia, serif',letterSpacing:'22px',color:INK,opacity:'0'});",
    "const cap=T('ONE DROP.',d,{left:'0',width:W+'px',top:(H*0.81)+'px',textAlign:'center',font:'600 34px Cormorant Garamond, Georgia, serif',letterSpacing:'26px',color:INK,opacity:'0'});\n"
    "  const tag=T('I · THE DROP',d,{left:'92px',top:'82px',font:'12px Cormorant Garamond, Georgia, serif',letterSpacing:'9px',color:BERRY,opacity:'0.55'});")

# ---------- S02 tag + heart size
rep("const tag=T('01 · THE HEART',d,{left:'90px',top:'80px',font:'11px Cormorant Garamond, Georgia, serif',letterSpacing:'8px',color:BERRY,opacity:'.7'});",
    "const tag=T('I · THE HEART',d,{left:'92px',top:'82px',font:'12px Cormorant Garamond, Georgia, serif',letterSpacing:'9px',color:BERRY,opacity:'0.55'});")
rep("const bh=760*e;", "const bh=880*e;")

# ---------- S03 tag + larger symbols
rep("const d=S03;\n  const halfL=", "const d=S03;\n  const tag=T('II · RELEASE',d,{left:'92px',top:'82px',font:'12px Cormorant Garamond, Georgia, serif',letterSpacing:'9px',color:BERRY,opacity:'0.55'});\n  const halfL=")
rep("{left:'0',top:'0',height:'120px',opacity:'0'}", "{left:'0',top:'0',height:'150px',opacity:'0'}")
rep("s.im.style.height=(160*(0.4+0.6*qe))+'px';", "s.im.style.height=(198*(0.4+0.6*qe))+'px';")
rep("s.im.style.left=(x-80)+'px'; s.im.style.top=(y-80)+'px';", "s.im.style.left=(x-99)+'px'; s.im.style.top=(y-99)+'px';")
rep("const r=lerp(60,450,qe), ang=s.ang+p*0.25;", "const r=lerp(60,500,qe), ang=s.ang+p*0.25;")
rep("font:'600 30px Cormorant Garamond, Georgia, serif',letterSpacing:'12px',color:INK,opacity:'0'});\n  UPD.push(p=>{\n    const crack=",
    "font:'600 34px Cormorant Garamond, Georgia, serif',letterSpacing:'18px',color:INK,opacity:'0'});\n  UPD.push(p=>{\n    const crack=")

# ---------- S04 tag + bigger eye
rep("const eye=IMG(A.eng_eye,wrap,{left:(W/2-620)+'px',top:'-160px',height:'1320px'});",
    "const tag=T('III · THE WORLD',d,{left:'92px',top:'82px',font:'12px Cormorant Garamond, Georgia, serif',letterSpacing:'9px',color:BERRY,opacity:'0.55'});\n  const eye=IMG(A.eng_eye,wrap,{left:(W/2-720)+'px',top:'-240px',height:'1560px'});")
rep("font:'600 26px Cormorant Garamond, Georgia, serif',letterSpacing:'16px',color:INK,opacity:'0'}",
    "font:'600 30px Cormorant Garamond, Georgia, serif',letterSpacing:'22px',color:INK,opacity:'0'}")

# ---------- S05: full rewrite
replace_between(
    "/* ---------- S05 cloud world ---------- */",
    "/* ---------- S06 ink bleed to black + card skeleton ---------- */",
    r"""/* ---------- S05 symbol world ---------- */
(function(){
  const d=S05;
  const tag=T('III · THE WORLD',d,{left:'92px',top:'82px',font:'12px Cormorant Garamond, Georgia, serif',letterSpacing:'9px',color:BERRY,opacity:'0.55'});
  const orb1=E('div',d,{position:'absolute',left:(W/2-600)+'px',top:(H/2-600)+'px',width:'1200px',height:'1200px',border:'1px solid rgba(143,44,59,.20)',borderRadius:'50%'});
  const orb2=E('div',d,{position:'absolute',left:(W/2-760)+'px',top:(H/2-760)+'px',width:'1520px',height:'1520px',border:'1px dashed rgba(143,44,59,.16)',borderRadius:'50%'});
  const eye=IMG(A.eng_eye,d,{left:(W/2-520)+'px',top:(H*0.50-520)+'px',height:'1040px',opacity:'0.14'});
  const ouro=IMG(A.eng_ouroboros,d,{left:'-240px',top:'-260px',height:'1000px',opacity:'0.5'});
  const wide=IMG(A.eng_eye_wide,d,{left:(W-540)+'px',top:'-250px',height:'940px',opacity:'0.32'});
  const humans=[['ic_hands',0.10],['ic_unicorn',0.26],['ic_crown',0.42],['ic_book',0.58],['ic_moon',0.74],['ic_dragon',0.90]];
  const hs=humans.map(([n,x])=>{ const im=IMG(A[n],d,{left:(W*x)+'px',top:(H*0.66)+'px',height:'300px',opacity:'0'}); return im; });
  const horizon=E('div',d,{position:'absolute',left:'0',top:(H*0.66)+'px',width:W+'px',height:'1px',background:'rgba(143,44,59,.24)'});
  UPD.push(p=>{
    ouro.style.transform='translate('+(-70*p)+'px,'+(26*p)+'px) rotate('+(-3*p)+'deg)';
    wide.style.transform='translate('+(48*(1-p))+'px,'+(-24*p)+'px)';
    orb1.style.transform='rotate('+(p*5)+'deg)';
    orb2.style.transform='rotate('+(-p*3.4)+'deg)';
    eye.style.opacity=String(0.10+0.12*p);
    hs.forEach((im,i)=>{ const q=clamp01((p-i*0.055)/0.40); im.style.opacity=String(q*0.9);
      im.style.height=(300+44*q)+'px'; im.style.top=(H*0.66-58*q)+'px'; });
  });
})();

""")

# ---------- S06: full rewrite
replace_between(
    "/* ---------- S06 ink bleed to black + card skeleton ---------- */",
    "/* ---------- six cards ---------- */",
    r"""/* ---------- S06 ink bleed to black + card skeleton ---------- */
(function(){
  const d=S06;
  const ink=E('div',d,{position:'absolute',left:(W/2)+'px',top:(H/2)+'px',width:'10px',height:'10px',background:'#0B0908',borderRadius:'50%',transform:'translate(-50%,-50%)'});
  const ring=E('div',d,{position:'absolute',left:(W/2)+'px',top:(H/2)+'px',width:'46px',height:'46px',border:'1px solid rgba(247,242,230,.55)',borderRadius:'50%',transform:'translate(-50%,-50%)',opacity:'0'});
  const tag=T('IV · THE BLACK',d,{left:'92px',top:'82px',font:'12px Cormorant Garamond, Georgia, serif',letterSpacing:'9px',color:BONE,opacity:'0'});
  const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');
  svg.setAttribute('width',W); svg.setAttribute('height',H); svg.style.cssText='position:absolute;left:0;top:0';
  const mk=(dd,op)=>{ const p=document.createElementNS('http://www.w3.org/2000/svg','path');
    p.setAttribute('d',dd); p.setAttribute('fill','none'); p.setAttribute('stroke',BONE);
    p.setAttribute('stroke-width','3'); p.setAttribute('opacity','0'); svg.appendChild(p); return p; };
  const crk1=mk('M740 140 L806 328 L774 402 L860 520 L820 636 L908 758 L864 936');
  const crk2=mk('M1180 190 L1116 356 L1158 430 L1088 548 L1132 664 L1064 806');
  const crk3=mk('M620 940 L700 840 L742 868 L806 772 L852 806');
  d.appendChild(svg);
  const card=E('div',d,{position:'absolute',left:(W/2-280)+'px',top:(H/2-380)+'px',width:'560px',height:'760px',border:'2px solid '+BONE,borderRadius:'16px',opacity:'0'});
  const cardIn=E('div',card,{position:'absolute',inset:'15px',border:'1px solid rgba(247,242,230,.55)',borderRadius:'8px'});
  const cLab=T('NOT TAROT · THE DECK',d,{left:'0',width:W+'px',top:(H*0.86)+'px',textAlign:'center',font:'13px Cormorant Garamond, Georgia, serif',letterSpacing:'16px',color:'rgba(247,242,230,.7)',opacity:'0'});
  UPD.push(p=>{
    const grow=clamp01(p/0.55), e=ease(grow);
    const size=lerp(10,3100,e);
    ink.style.width=size+'px'; ink.style.height=size+'px';
    const q=clamp01((p-0.42)/0.35);
    ring.style.opacity=String(clamp01((p-0.18)/0.2)*(1-clamp01((p-0.62)/0.3)));
    const rs=1+1.6*clamp01((p-0.18)/0.5); ring.style.transform='translate(-50%,-50%) scale('+rs+')';
    crk1.setAttribute('opacity',String(Math.min(1,q*1.8))); crk2.setAttribute('opacity',String(Math.min(0.9,q*1.5)));
    crk3.setAttribute('opacity',String(Math.min(0.8,q*1.4)));
    card.style.opacity=String(clamp01((p-0.5)/0.25)*0.95);
    card.style.transform='scale('+lerp(0.94,1,ease(clamp01((p-0.5)/0.4)))+')';
    tag.style.opacity=String(clamp01((p-0.25)/0.3)*0.8);
    cLab.style.opacity=String(clamp01((p-0.62)/0.25)*0.9);
  });
})();

""")

# ---------- buildCard: full rewrite
replace_between(
    "function buildCard(d,icon,label,meaning,idx){",
    "buildCard(S07,...CARDS[0],0);",
    r"""function buildCard(d,icon,label,meaning,idx){
  const card=E('div',d,{position:'absolute',left:(W/2-280)+'px',top:(H/2-380)+'px',width:'560px',height:'760px',transformStyle:'preserve-3d'});
  const front=E('div',card,{position:'absolute',inset:'0',background:CREAM,border:'2px solid '+BERRY,borderRadius:'20px',overflow:'hidden',boxShadow:'0 30px 70px rgba(20,16,15,.20)'});
  E('div',front,{position:'absolute',inset:'15px',border:'1px solid rgba(143,44,59,.55)',borderRadius:'12px'});
  const back=E('div',card,{position:'absolute',inset:'0',background:BERRY,borderRadius:'20px',transform:'rotateY(180deg)',backfaceVisibility:'hidden',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',gap:'30px',padding:'60px',boxShadow:'0 30px 70px rgba(20,16,15,.20)'});
  E('div',back,{position:'absolute',inset:'15px',border:'1px solid rgba(247,242,230,.5)',borderRadius:'12px'});
  front.style.backfaceVisibility='hidden';
  const bno=T('No. 0'+(idx+1),back,{position:'static',color:BONE,font:'12px Cormorant Garamond, Georgia, serif',letterSpacing:'8px',opacity:'0.8'});
  const bt=T(meaning,back,{position:'static',color:CREAM,font:'23px/1.95 \"Songti SC\",\"SimSun\",serif',letterSpacing:'3px',textAlign:'center'});
  const bmar=T('NOT TAROT',back,{position:'static',color:BONE,font:'11px Cormorant Garamond, Georgia, serif',letterSpacing:'12px',opacity:'0.75'});
  const sym=IMG(A[icon],d,{left:(W/2)+'px',top:(H/2-505)+'px',height:'860px',transformOrigin:'center center'});
  const labelEl=T(label,d,{left:'0',width:W+'px',top:(H-142)+'px',textAlign:'center',font:'600 46px Cormorant Garamond, Georgia, serif',letterSpacing:'22px',color:INK});
  const no=T('0'+(idx+1)+' / 06',d,{left:'0',width:W+'px',top:(H-88)+'px',textAlign:'center',font:'11px Cormorant Garamond, Georgia, serif',letterSpacing:'9px',color:BERRY,opacity:'0.75'});
  const st={flip:false};
  card.style.cursor='pointer';
  card.addEventListener('click',()=>{ st.flip=!st.flip; });
  UPD.push(p=>{
    const e=easeBack(clamp01(p/0.5));
    card.style.transform='translateY('+((1-e)*300)+'px) rotateY('+(st.flip?180:0)+'deg)';
    card.style.opacity=String(clamp01(p/0.14));
    sym.style.opacity=String(clamp01((p-0.10)/0.32)*(st.flip?0:1));
    sym.style.transform='rotate('+(icon==='ic_tiger'?180:0)+'deg) translateY('+((1-e)*90)+'px) scale('+(0.86+0.14*e)+')';
    labelEl.style.opacity=String(clamp01((p-0.26)/0.28));
    no.style.opacity=labelEl.style.opacity;
  });
}

""")

# ---------- S13 rewrite
replace_between(
    "/* ---------- S13 ring assembly ---------- */",
    "/* ---------- S14 mandala morph ---------- */",
    r"""/* ---------- S13 ring assembly ---------- */
const RING12=['g_ic_tiger','g_scissors_sym','g_ic_butterfly','g_ic_eye_tears','g_flower_sym','g_ic_unicorn','g_ic_crown','g_icon_heart','g_ic_skull','g_ic_moon','g_ic_hands','g_ic_book'];
const buildRing=(d)=>{ const syms=RING12.map((n,i)=>IMG(A[n],d,{left:'0',top:'0',height:'196px',opacity:'0'})); return syms; };
(function(){
  const d=S13;
  const tag=T('VI · THE SEAL',d,{left:'92px',top:'82px',font:'12px Cormorant Garamond, Georgia, serif',letterSpacing:'9px',color:GOLD,opacity:'0.6'});
  const ringA=E('div',d,{position:'absolute',left:(W/2-470)+'px',top:(H/2-470)+'px',width:'940px',height:'940px',border:'2px solid '+GOLD,borderRadius:'50%',opacity:'0'});
  const ringB=E('div',d,{position:'absolute',left:(W/2-360)+'px',top:(H/2-360)+'px',width:'720px',height:'720px',border:'1px solid '+GOLD,borderRadius:'50%',opacity:'0'});
  const ringC=E('div',d,{position:'absolute',left:(W/2-405)+'px',top:(H/2-405)+'px',width:'810px',height:'810px',border:'1px dashed rgba(123,85,33,.45)',borderRadius:'50%',opacity:'0'});
  const syms=buildRing(d);
  UPD.push(p=>{
    ringA.style.opacity=String(clamp01((p-0.12)/0.25)*0.9);
    ringB.style.opacity=String(clamp01((p-0.26)/0.3)*0.8);
    ringC.style.opacity=String(clamp01((p-0.2)/0.3)*0.9);
    ringC.style.transform='rotate('+(p*14)+'deg)';
    syms.forEach((im,i)=>{
      const q=clamp01((p-i*0.045)/0.45), qe=ease(q);
      const ang=i/12*Math.PI*2 - Math.PI/2;
      const from={x:W/2+Math.cos(ang+1.2)*130,y:H/2+Math.sin(ang+1.2)*130};
      const to={x:W/2+Math.cos(ang)*470,y:H/2+Math.sin(ang)*470};
      const x=lerp(from.x,to.x,qe), y=lerp(from.y,to.y,qe);
      im.style.left=(x-98)+'px'; im.style.top=(y-62)+'px'; im.style.opacity=String(q*0.96);
    });
  });
})();

""")

# ---------- S14 rewrite
replace_between(
    "/* ---------- S14 mandala morph ---------- */",
    "/* ---------- S15 collapse to line ---------- */",
    r"""/* ---------- S14 mandala morph ---------- */
(function(){
  const d=S14;
  const syms=buildRing(d);
  const rays=E('div',d,{position:'absolute',left:(W/2-490)+'px',top:(H/2-490)+'px',width:'980px',height:'980px',borderRadius:'50%',border:'1px dashed rgba(123,85,33,.55)',opacity:'0',transformOrigin:'center center'});
  const morphNames=['ic_butterfly','flower_sym','icon_heart','ic_crown','ic_eye_tears'];
  const morph=morphNames.map(n=>IMG(A[n],d,{left:(W/2-300)+'px',top:(H/2-300)+'px',height:'600px',opacity:'0'}));
  const cap=T('BECOME.',d,{left:'0',width:W+'px',top:(H*0.855)+'px',textAlign:'center',font:'600 34px Cormorant Garamond, Georgia, serif',letterSpacing:'26px',color:INK,opacity:'0'});
  UPD.push((p,loc)=>{
    rays.style.opacity=String(clamp01(p/0.2)*0.8);
    rays.style.transform='rotate('+loc*9+'deg)';
    syms.forEach((im,i)=>{ const ang=i/12*Math.PI*2-Math.PI/2;
      im.style.left=(W/2+Math.cos(ang)*470-98)+'px'; im.style.top=(H/2+Math.sin(ang)*470-62)+'px'; im.style.opacity='0.96'; });
    const step=Math.min(4,Math.floor(loc/0.8)), f=clamp01((loc-step*0.8)/0.25);
    morph.forEach((m,i)=>{ m.style.opacity=String(i===step?clamp01(f)*0.98:(i===step-1?(1-f)*0.98:0)); });
    cap.style.opacity=String(clamp01((p-0.60)/0.2)*0.9);
  });
})();

""")

# ---------- S15 rewrite
replace_between(
    "/* ---------- S15 collapse to line ---------- */",
    "/* ---------- S16 brand reveal ---------- */",
    r"""/* ---------- S15 collapse to line ---------- */
(function(){
  const d=S15;
  const syms=buildRing(d);
  syms.forEach((im,i)=>{ const ang=i/12*Math.PI*2-Math.PI/2;
    im.style.left=(W/2+Math.cos(ang)*470-98)+'px'; im.style.top=(H/2+Math.sin(ang)*470-62)+'px'; im.style.opacity='0.96'; });
  const ringA=E('div',d,{position:'absolute',left:(W/2-470)+'px',top:(H/2-470)+'px',width:'940px',height:'940px',border:'2px solid '+GOLD,borderRadius:'50%'});
  const line=E('div',d,{position:'absolute',left:(W/2)+'px',top:(H/2)+'px',width:'0px',height:'2px',background:PLUM,transform:'translateY(-50%)'});
  const word=T('NOT TAROT',d,{left:'0',width:W+'px',top:(H/2-170)+'px',textAlign:'center',font:'600 176px Cormorant Garamond, Georgia, serif',letterSpacing:'34px',color:PLUM,opacity:'0'});
  UPD.push(p=>{
    const col=ease(clamp01(p/0.45));
    syms.forEach(im=>{ im.style.transform='scale('+lerp(1,0.22,col)+')'; im.style.opacity=String(lerp(0.96,0.18,col)); });
    ringA.style.transform='scale('+lerp(1,0.18,col)+')'; ringA.style.opacity=String(lerp(0.9,0,col));
    const lw=lerp(0,1560,ease(clamp01((p-0.28)/0.35)))*(1-ease(clamp01((p-0.70)/0.30))*0.94);
    line.style.width=lw+'px'; line.style.left=(W/2-lw/2)+'px';
    line.style.opacity=String(clamp01((p-0.22)/0.2));
    word.style.opacity=String(clamp01((p-0.60)/0.32)*0.92);
  });
})();

""")

# ---------- S16 rewrite
replace_between(
    "/* ---------- S16 brand reveal ---------- */",
    "/* ---------- S17 static hold ---------- */",
    r"""/* ---------- S16 brand reveal ---------- */
(function(){
  const d=S16;
  const top=T('A FILM IN SEVEN PLATES',d,{left:'0',width:W+'px',top:(H*0.24)+'px',textAlign:'center',font:'11px Cormorant Garamond, Georgia, serif',letterSpacing:'14px',color:PLUM,opacity:'0'});
  const word=T('NOT TAROT',d,{left:'0',width:W+'px',top:(H/2-190)+'px',textAlign:'center',font:'600 176px Cormorant Garamond, Georgia, serif',letterSpacing:'34px',color:PLUM,opacity:'0'});
  const l1=E('div',d,{position:'absolute',left:(W/2-600)+'px',top:(H/2-212)+'px',width:'0px',height:'1px',background:PLUM});
  const l2=E('div',d,{position:'absolute',left:(W/2-600)+'px',top:(H/2+172)+'px',width:'0px',height:'1px',background:PLUM});
  const sub=T('MAKE YOUR OWN MEANING.',d,{left:'0',width:W+'px',top:(H/2+70)+'px',textAlign:'center',font:'24px Cormorant Garamond, Georgia, serif',letterSpacing:'20px',color:PLUM,opacity:'0'});
  const cln=T('SIX CARDS  ·  ONE ANSWER THAT IS YOURS  ·  MMXXVI',d,{left:'0',width:W+'px',top:(H*0.80)+'px',textAlign:'center',font:'11px Cormorant Garamond, Georgia, serif',letterSpacing:'9px',color:GOLD,opacity:'0'});
  UPD.push(p=>{
    const e=ease(clamp01(p/0.45));
    word.style.opacity=String(e);
    l1.style.width=(1200*e)+'px'; l2.style.width=(1200*e)+'px';
    sub.style.opacity=String(clamp01((p-0.34)/0.35)*0.92);
    top.style.opacity=String(clamp01((p-0.2)/0.35)*0.6);
    cln.style.opacity=String(clamp01((p-0.5)/0.3)*0.7);
  });
})();

""")

# ---------- S17 rewrite
replace_between(
    "/* ---------- S17 static hold ---------- */",
    "const TIMES=",
    r"""/* ---------- S17 static hold ---------- */
(function(){
  const d=S17;
  const top=T('A FILM IN SEVEN PLATES',d,{left:'0',width:W+'px',top:(H*0.24)+'px',textAlign:'center',font:'11px Cormorant Garamond, Georgia, serif',letterSpacing:'14px',color:PLUM,opacity:'0.6'});
  const word=T('NOT TAROT',d,{left:'0',width:W+'px',top:(H/2-190)+'px',textAlign:'center',font:'600 176px Cormorant Garamond, Georgia, serif',letterSpacing:'34px',color:PLUM});
  const l1=E('div',d,{position:'absolute',left:(W/2-600)+'px',top:(H/2-212)+'px',width:'1200px',height:'1px',background:PLUM});
  const l2=E('div',d,{position:'absolute',left:(W/2-600)+'px',top:(H/2+172)+'px',width:'1200px',height:'1px',background:PLUM});
  const sub=T('MAKE YOUR OWN MEANING.',d,{left:'0',width:W+'px',top:(H/2+70)+'px',textAlign:'center',font:'24px Cormorant Garamond, Georgia, serif',letterSpacing:'20px',color:PLUM,opacity:'0.92'});
  const cln=T('SIX CARDS  ·  ONE ANSWER THAT IS YOURS  ·  MMXXVI',d,{left:'0',width:W+'px',top:(H*0.80)+'px',textAlign:'center',font:'11px Cormorant Garamond, Georgia, serif',letterSpacing:'9px',color:GOLD,opacity:'0.7'});
  UPD.push(()=>{});
})();

""")

# ---------- acts + chapters
rep("const ACTS=[[0,'01 · HEART'],[8,'02 · RELEASE'],[14,'03 · THE WORLD'],[22,'04 · THE BLACK'],[24.5,'05 · THE DRAW'],[33.5,'06 · THE SEAL'],[40,'07 · THE NAME']];",
    "const ACTS=[[0,'I · HEART'],[8,'II · RELEASE'],[14,'III · THE WORLD'],[22,'IV · THE BLACK'],[24.5,'V · THE DRAW'],[33.5,'VI · THE SEAL'],[40,'VII · THE NAME']];")

rep("""(function(){
  const ch=document.getElementById('chapters');
  ACTS.forEach((a,i)=>{ const c=E('div',ch,{}); c.className='chap'; c.title=a[1]; c.addEventListener('click',()=>{ seek(a[0]); }); });
})();""",
    """(function(){
  const ch=document.getElementById('chapters');
  ACTS.forEach((a,i)=>{ const c=E('div',ch,{}); c.className='chap'; c.textContent=a[1];
    c.addEventListener('click',()=>{ seek(a[0]+0.02); if(!PLAYING){ T0=performance.now()/1000-a[0]-0.02; PLAYING=true; document.getElementById('poster').style.display='none'; } }); });
})();""")

# ---------- layout + stage background + dark mode
rep("const S13=scene(), S14=scene(), S15=scene(), S16=scene(), S17=scene();",
    """const S13=scene(), S14=scene(), S15=scene(), S16=scene(), S17=scene();
const stageEl=document.getElementById('stage'), wrapEl=document.getElementById('stageWrap'),
      shellEl=document.getElementById('shell'), stageBg=document.getElementById('stageBg'),
      hudEl=document.getElementById('hud'), chapEl=document.getElementById('chapters');
function fitLayout(){
  let scale;
  if(VERTICAL){ scale=1080/1920; }
  else if(CAPTURE){ scale=1; }
  else { scale=Math.min((window.innerWidth-120)/1920,(window.innerHeight-178)/1080); }
  scale=Math.max(0.2,scale);
  stageEl.style.transform='scale('+scale+')';
  wrapEl.style.width=(1920*scale)+'px';
  wrapEl.style.height=(1080*scale)+'px';
  if(!VERTICAL && !CAPTURE){ hudEl.style.width=(1920*scale)+'px'; chapEl.style.width=(1920*scale)+'px'; }
}
window.addEventListener('resize',fitLayout);""")

rep("""  t=Math.max(0,Math.min(DUR-0.001,t)); CURT=t;
  let idx=TIMES.findIndex(([a,b])=>t>=a&&t<b); if(idx<0) idx=TIMES.length-1;""",
    """  t=Math.max(0,Math.min(DUR-0.001,t)); CURT=t;
  const dark=(t>=21.96&&t<24.50);
  document.body.classList.toggle('dark',dark);
  stageBg.style.background=(t>=22.0&&t<24.5)?ENV:((t>=33.5&&t<40.0)?ROSE:CREAM);
  let idx=TIMES.findIndex(([a,b])=>t>=a&&t<b); if(idx<0) idx=TIMES.length-1;""")

rep("/* capture API */\nrender(0);", "/* capture API */\nfitLayout();\nrender(0);")

# ---------- draw card: bone variants
rep("""  const names=Object.keys(A).filter(k=>k.startsWith('ic_')||k==='scissors_sym'||k==='flower_sym'||k==='icon_heart');
  const k=names[Math.floor(Math.random()*names.length)];
  document.getElementById('dimg').src=A[k];
  document.getElementById('dname').textContent=k.replace(/^ic_/,'').replace(/_/g,' ').toUpperCase();""",
    """  const names=['ic_heart','ic_skull','ic_moon','ic_cloud_eye','ic_hands','ic_crown','ic_butterfly','ic_tiger','ic_unicorn','ic_eye_tears','ic_book','ic_mirror','ic_compass','ic_wand','ic_dragon','scissors_sym','flower_sym'];
  const k=names[Math.floor(Math.random()*names.length)];
  document.getElementById('dimg').src=A['b_'+k]||A[k];
  document.getElementById('dname').textContent=k.replace(/^ic_/,'').replace(/_/g,' ').toUpperCase();""")

# paper init line stays valid; remove old vertical refs if any
s = s.replace("document.getElementById('verticalFrame')", "document.getElementById('vertTop')")

# ================= pass 2: art-direction fixes after first v4 review =====
rep("<title>NOT TAROT · 45s · v3 ONE INK</title>",
    "<title>NOT TAROT · 45s · v4 ANTIQUE PLATE</title>")

# ---------- S01 hook: bigger target, bigger drop, earlier caption
rep("const tgt=E('div',d,{position:'absolute',left:(W/2-70)+'px',top:(H*0.62-70)+'px',width:'140px',height:'140px',border:'1px solid '+BERRY,borderRadius:'50%',opacity:'0.35'});",
    "const tgt=E('div',d,{position:'absolute',left:(W/2-170)+'px',top:(H*0.62-170)+'px',width:'340px',height:'340px',border:'1px solid '+BERRY,borderRadius:'50%',opacity:'0.45'});\n"
    "  const tgt2=E('div',d,{position:'absolute',left:(W/2-215)+'px',top:(H*0.62-215)+'px',width:'430px',height:'430px',border:'1px dashed rgba(143,44,59,.28)',borderRadius:'50%',opacity:'0.8'});")
rep("for(let k=0;k<8;k++){ const a=k/8*Math.PI*2; const tick=E('div',d,{position:'absolute',left:(W/2+Math.cos(a)*96-14)+'px',top:(H*0.62+Math.sin(a)*96)+'px',width:'28px',height:'1px',background:BERRY,opacity:'0.5',transform:'rotate('+(a*180/Math.PI)+'deg)'}); }",
    "for(let k=0;k<16;k++){ const a=k/16*Math.PI*2; const ln=(k%4===0)?46:24; const tick=E('div',d,{position:'absolute',left:(W/2+Math.cos(a)*258-ln/2)+'px',top:(H*0.62+Math.sin(a)*258)+'px',width:ln+'px',height:'1px',background:BERRY,opacity:'0.45',transform:'rotate('+(a*180/Math.PI)+'deg)'}); }")
rep("const drop=E('div',d,{position:'absolute',left:(W/2-10)+'px',top:'-70px',width:'20px',height:'28px',background:INK,borderRadius:'50% 50% 50% 50% / 62% 62% 38% 38%'});",
    "const drop=E('div',d,{position:'absolute',left:(W/2-13)+'px',top:'-96px',width:'26px',height:'38px',background:INK,borderRadius:'50% 50% 50% 50% / 62% 62% 38% 38%'});")
rep("drop.style.top=(-70+e*(H*0.62-40))+'px';", "drop.style.top=(-96+e*(H*0.62-56))+'px';")
rep("const s=1+q*10;", "const s=1+q*15;")
rep("cap.style.opacity=clamp01((p-0.56)/0.2)*0.8;", "cap.style.opacity=clamp01((p-0.40)/0.2)*0.9;")

# ---------- S03: bigger ring symbols
rep("{left:'0',top:'0',height:'150px',opacity:'0'}", "{left:'0',top:'0',height:'232px',opacity:'0'}")
rep("s.im.style.height=(198*(0.4+0.6*qe))+'px';", "s.im.style.height=(232*(0.45+0.55*qe))+'px';")
rep("s.im.style.left=(x-99)+'px'; s.im.style.top=(y-99)+'px';", "s.im.style.left=(x-116)+'px'; s.im.style.top=(y-116)+'px';")
rep("const r=lerp(60,500,qe), ang=s.ang+p*0.25;", "const r=lerp(80,520,qe), ang=s.ang+p*0.25;")

# ---------- S04: line-art giant eye instead of engraving blob
rep("const tag=T('III · THE WORLD',d,{left:'92px',top:'82px',font:'12px Cormorant Garamond, Georgia, serif',letterSpacing:'9px',color:BERRY,opacity:'0.55'});\n  const eye=IMG(A.eng_eye,wrap,{left:(W/2-720)+'px',top:'-240px',height:'1560px'});",
    "const tag=T('III · THE EYE',d,{left:'92px',top:'82px',font:'12px Cormorant Garamond, Georgia, serif',letterSpacing:'9px',color:BERRY,opacity:'0.55'});\n  const eye=IMG(A.eye_open,wrap,{left:(W/2)+'px',top:'-112px',height:'1304px',transform:'translateX(-50%)'});")

# ---------- S05: full line-art world (no engraving bitmaps)
replace_between(
    "/* ---------- S05 symbol world ---------- */",
    "/* ---------- S06 ink bleed to black + card skeleton ---------- */",
    r"""/* ---------- S05 symbol world ---------- */
(function(){
  const d=S05;
  const tag=T('III · THE WORLD',d,{left:'92px',top:'82px',font:'12px Cormorant Garamond, Georgia, serif',letterSpacing:'9px',color:BERRY,opacity:'0.55'});
  const orb1=E('div',d,{position:'absolute',left:(W/2-540)+'px',top:(H*0.44-540)+'px',width:'1080px',height:'1080px',border:'1px solid rgba(143,44,59,.18)',borderRadius:'50%',opacity:'0'});
  const orb2=E('div',d,{position:'absolute',left:(W/2-760)+'px',top:(H*0.44-760)+'px',width:'1520px',height:'1520px',border:'1px dashed rgba(143,44,59,.13)',borderRadius:'50%',opacity:'0'});
  const horizon=E('div',d,{position:'absolute',left:'0',top:(H*0.70)+'px',width:'0px',height:'1px',background:'rgba(143,44,59,.34)',opacity:'0'});
  const items=[
    {n:'ic_eye_tears', x:.62, y:-.06, h:980, op:.085, par:.05},
    {n:'ic_cloud_eye', x:.80, y:.16, h:520, op:.55,  par:.12},
    {n:'ic_moon',      x:.15, y:.17, h:470, op:.55,  par:.15},
    {n:'ic_skull',     x:.21, y:.63, h:400, op:.62,  par:.20},
    {n:'ic_hands',     x:.79, y:.62, h:380, op:.55,  par:.17},
    {n:'ic_compass',   x:.50, y:.34, h:250, op:.42,  par:.09},
    {n:'ic_wand',      x:.35, y:.73, h:230, op:.42,  par:.13},
    {n:'ic_mirror',    x:.55, y:.80, h:190, op:.34,  par:.11}
  ].map(o=>{ const im=IMG(A[o.n],d,{left:(W*o.x)+'px',top:(H*o.y)+'px',height:o.h+'px',opacity:'0',transform:'translateX(-50%)'}); return Object.assign({im},o); });
  const tks=[];
  for(let k=0;k<18;k++){ const ang=k/18*Math.PI*2; const tk=E('div',d,{position:'absolute',left:(W/2+Math.cos(ang)*700-15)+'px',top:(H*0.44+Math.sin(ang)*420-1)+'px',width:'30px',height:'1px',background:'rgba(143,44,59,.32)',transform:'rotate('+(ang*180/Math.PI)+'deg)',opacity:'0'}); tks.push(tk); }
  UPD.push((p,loc)=>{
    const e=ease(clamp01(p/0.42));
    orb1.style.opacity=String(e*0.85); orb2.style.opacity=String(e*0.7);
    orb1.style.transform='rotate('+(loc*2.2)+'deg)'; orb2.style.transform='rotate('+(-loc*1.5)+'deg)';
    horizon.style.opacity=String(clamp01((p-0.04)/0.22));
    horizon.style.width=(W*ease(clamp01((p-0.04)/0.30)))+'px';
    items.forEach((o,i)=>{ const q=ease(clamp01((p-i*0.055)/0.42));
      o.im.style.opacity=String(o.op*(0.1+0.9*q));
      o.im.style.transform='translateX(-50%) translate('+((loc*o.par*9)*((i%2)?1:-1))+'px,'+((1-q)*44)+'px)'; });
    tks.forEach((tk,i)=>{ tk.style.opacity=String(clamp01((p-i*0.02)/0.25)*0.8); });
  });
})();

""")

# ---------- S06: strengthen the skeleton card
rep("const cardIn=E('div',card,{position:'absolute',inset:'15px',border:'1px solid rgba(247,242,230,.55)',borderRadius:'8px'});",
    "const cardIn=E('div',card,{position:'absolute',inset:'14px',border:'1px solid rgba(247,242,230,.55)',borderRadius:'8px'});\n"
    "  const card2=E('div',d,{position:'absolute',left:(W/2-280+18)+'px',top:(H/2-380-16)+'px',width:'560px',height:'760px',border:'1px solid rgba(247,242,230,.30)',borderRadius:'16px',opacity:'0',transform:'rotate(1.8deg)'});")
rep("card.style.opacity=String(clamp01((p-0.5)/0.25)*0.95);",
    "card.style.opacity=String(clamp01((p-0.5)/0.25)*0.92); card2.style.opacity=String(clamp01((p-0.52)/0.25)*0.55);")

# ---------- buildCard: center symbol on card, tune scale
rep("const sym=IMG(A[icon],d,{left:(W/2)+'px',top:(H/2-505)+'px',height:'860px',transformOrigin:'center center'});",
    "const sym=IMG(A[icon],d,{left:(W/2)+'px',top:(H/2-500)+'px',height:'820px',transformOrigin:'center center',transform:'translateX(-50%)'});")
rep("sym.style.transform='rotate('+(icon==='ic_tiger'?180:0)+'deg) translateY('+((1-e)*90)+'px) scale('+(0.86+0.14*e)+')';",
    "sym.style.transform='translateX(-50%) rotate('+(icon==='ic_tiger'?180:0)+'deg) translateY('+((1-e)*90)+'px) scale('+(0.86+0.14*e)+')';")
rep("const labelEl=T(label,d,{left:'0',width:W+'px',top:(H-142)+'px',textAlign:'center',font:'600 46px Cormorant Garamond, Georgia, serif',letterSpacing:'22px',color:INK});",
    "const labelEl=T(label,d,{left:'0',width:W+'px',top:(H-140)+'px',textAlign:'center',font:'600 44px Cormorant Garamond, Georgia, serif',letterSpacing:'20px',color:INK});")

# ---------- S13/S14: heavier gold rings
rep("const ringA=E('div',d,{position:'absolute',left:(W/2-470)+'px',top:(H/2-470)+'px',width:'940px',height:'940px',border:'2px solid '+GOLD,borderRadius:'50%',opacity:'0'});",
    "const ringA=E('div',d,{position:'absolute',left:(W/2-470)+'px',top:(H/2-470)+'px',width:'940px',height:'940px',border:'3px solid '+GOLD,borderRadius:'50%',opacity:'0'});")
rep("const ringB=E('div',d,{position:'absolute',left:(W/2-360)+'px',top:(H/2-360)+'px',width:'720px',height:'720px',border:'1px solid '+GOLD,borderRadius:'50%',opacity:'0'});",
    "const ringB=E('div',d,{position:'absolute',left:(W/2-360)+'px',top:(H/2-360)+'px',width:'720px',height:'720px',border:'2px solid '+GOLD,borderRadius:'50%',opacity:'0'});")
rep("const morphNames=['ic_butterfly','flower_sym','icon_heart','ic_crown','ic_eye_tears'];",
    "const morphNames=['ic_butterfly','flower_sym','icon_heart','ic_crown','ic_eye_tears'];\n  const ringD=E('div',d,{position:'absolute',left:(W/2-540)+'px',top:(H/2-540)+'px',width:'1080px',height:'1080px',border:'1px solid rgba(123,85,33,.4)',borderRadius:'50%',opacity:'0',transformOrigin:'center center'});")
rep("rays.style.opacity=String(clamp01(p/0.2)*0.8);", "rays.style.opacity=String(clamp01(p/0.2)*0.8); ringD.style.opacity=String(clamp01(p/0.25)*0.7); ringD.style.transform='rotate('+(-loc*7)+'deg)';")

# ---------- S15: keep mandala residue while the line collapses
rep("syms.forEach(im=>{ im.style.transform='scale('+lerp(1,0.22,col)+')'; im.style.opacity=String(lerp(0.96,0.18,col)); });",
    "syms.forEach(im=>{ im.style.transform='scale('+lerp(1,0.30,col)+')'; im.style.opacity=String(lerp(0.96,0.40,col)); });")
rep("ringA.style.transform='scale('+lerp(1,0.18,col)+')'; ringA.style.opacity=String(lerp(0.9,0,col));",
    "ringA.style.transform='scale('+lerp(1,0.24,col)+')'; ringA.style.opacity=String(lerp(0.9,0.30,col));")

# ---------- S06: stronger ink card skeleton
rep("width:'560px',height:'760px',border:'2px solid '+BONE,borderRadius:'16px',opacity:'0'});",
    "width:'560px',height:'760px',border:'3px solid '+BONE,borderRadius:'14px',opacity:'0'});")
rep("p.setAttribute('stroke-width','3');", "p.setAttribute('stroke-width','4');")
rep("card.style.opacity=String(clamp01((p-0.5)/0.25)*0.92); card2.style.opacity=String(clamp01((p-0.52)/0.25)*0.55);",
    "card.style.opacity=String(clamp01((p-0.5)/0.25)*0.95); card2.style.opacity=String(clamp01((p-0.52)/0.25)*0.6);")

# ---------- S13: seat the ring symbols on the circle + core sigil
rep("im.style.left=(x-98)+'px'; im.style.top=(y-62)+'px'; im.style.opacity=String(q*0.96);",
    "im.style.left=(x-78)+'px'; im.style.top=(y-98)+'px'; im.style.opacity=String(q*0.96);")
rep("const syms=buildRing(d);\n  UPD.push(p=>{\n    ringA.style.opacity=String(clamp01((p-0.12)/0.25)*0.9);",
    "const syms=buildRing(d);\n  const core=IMG(A.g_icon_heart,d,{left:(W/2)+'px',top:(H/2)+'px',height:'132px',opacity:'0',transform:'translate(-50%,-50%)'});\n  UPD.push(p=>{\n    ringA.style.opacity=String(clamp01((p-0.12)/0.25)*0.9);")
rep("ringC.style.transform='rotate('+(p*14)+'deg)';",
    "ringC.style.transform='rotate('+(p*14)+'deg)';\n    core.style.opacity=String(clamp01((p-0.30)/0.3)*0.95);\n    core.style.transform='translate(-50%,-50%) scale('+lerp(0.7,1,ease(clamp01((p-0.30)/0.45)))+')';")

# ---------- S14: ring symbol offsets
rep("im.style.left=(W/2+Math.cos(ang)*470-98)+'px'; im.style.top=(H/2+Math.sin(ang)*470-62)+'px'; im.style.opacity='0.96'; });",
    "im.style.left=(W/2+Math.cos(ang)*470-78)+'px'; im.style.top=(H/2+Math.sin(ang)*470-98)+'px'; im.style.opacity='0.96'; });", count=s.count("im.style.left=(W/2+Math.cos(ang)*470-98)+'px'; im.style.top=(H/2+Math.sin(ang)*470-62)+'px'; im.style.opacity='0.96'; });"))

DST.write_text(s, encoding="utf-8")
print("template written", DST, len(s), "chars")

# quick sanity: no unbalanced template leftovers
for bad in ["__ASSETS__", "__TEXTURES__"]:
    print(bad, "present" if bad in s else "gone", "->", "expected present in v3 style")
