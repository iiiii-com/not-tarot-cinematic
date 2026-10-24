# -*- coding: utf-8 -*-
"""Patch magazine_v5_template.html into magazine_v6_template.html (magazine v6)."""
from pathlib import Path
ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
SRC = ROOT / "_tools" / "magazine_v5_template.html"
DST = ROOT / "_tools" / "magazine_v6_template.html"
s = SRC.read_text(encoding="utf-8")

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c >= n, "MISS: " + old[:90]
    s = s.replace(old, new, n)

# --- global css / helper tuning ---
rep("mix-blend-mode:multiply;opacity:.42;", "mix-blend-mode:multiply;opacity:.34;")
rep("font-size:11px;letter-spacing:.16em;color:#cbbfb8}", "font-size:12px;letter-spacing:.16em;color:#cbbfb8}")
rep("const css={font:sans(11,500),letterSpacing:'0.36em'", "const css={font:sans(12,500),letterSpacing:'0.36em'")

# --- sticker: softer shadow, larger label ---
rep("st.style.padding=Math.max(6,Math.round(size*0.032))+'px';",
    "st.style.padding=Math.max(7,Math.round(size*0.035))+'px';")
rep("st.style.boxShadow='0 '+Math.round(size*0.10)+'px '+Math.round(size*0.18)+'px rgba(36,31,34,.20), 0 2px 5px rgba(36,31,34,.10)';",
    "st.style.boxShadow='0 '+Math.round(size*0.05)+'px '+Math.round(size*0.14)+'px rgba(36,31,34,.16), 0 1px 2px rgba(36,31,34,.10)';")
rep("marginTop:Math.round(size*0.05)+'px',font:sans(Math.max(9,Math.round(size*0.048)),500)",
    "marginTop:Math.round(size*0.042)+'px',font:sans(Math.max(12,Math.round(size*0.058)),500)")

# --- s01 cold open ---
old_s01 = """  u.push(p=>{
    const a=eo(R(p,0,.16)); k.style.opacity=String(a);
    const b=eo(R(p,.04,.34)); mast.style.opacity=String(b); mast.style.transform='translateY('+((1-b)*26)+'px)';
    const c=eo(R(p,.16,.5)); rule.style.opacity=String(c*.9); rule.style.transform='scaleX('+c+')';
    lines.forEach((t,i)=>{ const q=eo(R(p,.24+i*.07,.5+i*.07)); t.style.opacity=String(q); t.style.transform='translateY('+((1-q)*18)+'px)'; });
    st.forEach((s,i)=>{ const q=eb(R(p,.30+i*.08,.62+i*.08)); s.el.style.opacity=String(cl(R(p,.3+i*.08,.42+i*.08))); s.el.style.transform=s.base+' scale('+(0.84+0.16*q)+')'; if(s.label) s.label.style.opacity=String(cl(R(p,.4+i*.08,.6+i*.08))*.9); });
    foot.style.opacity=String(eo(R(p,.55,.78))); bar.style.opacity=String(eo(R(p,.58,.8))); price.style.opacity=String(eo(R(p,.6,.82))*.75);
    folio.style.opacity=String(eo(R(p,.02,.2)));
  });"""
new_s01 = """  u.push(p=>{
    k.style.opacity='1'; mast.style.opacity='1';
    rule.style.opacity='0.9'; rule.style.transform='scaleX(1)';
    lines.forEach(t=>{ t.style.opacity='1'; t.style.transform='none'; });
    st.forEach((s,i)=>{ const q=eb(R(p,i*.05,.24+i*.05)); s.el.style.opacity=String(cl(R(p,i*.05,.12+i*.05))); s.el.style.transform=s.base+' scale('+(0.94+0.06*q)+')'; if(s.label) s.label.style.opacity=String(cl(R(p,.05,.2))*.95); });
    foot.style.opacity=String(eo(R(p,.10,.26))); bar.style.opacity=String(eo(R(p,.12,.28))); price.style.opacity=String(eo(R(p,.14,.3))*.78);
    folio.style.opacity='1';
  });"""
rep(old_s01, new_s01)

# --- s02 contents ---
rep("const n=TX(r,it[0],{font:sans(12,500),letterSpacing:'0.2em',color:COL.berry,width:'40px'});",
    "const n=TX(r,it[0],{font:sans(13,500),letterSpacing:'0.2em',color:COL.berry,width:'44px'});")
rep("const t=TX(r,it[1],{font:sero(VERT?30:38),color:COL.ink,whiteSpace:'nowrap'});",
    "const t=TX(r,it[1],{font:sero(VERT?33:41),color:COL.ink,whiteSpace:'nowrap'});")
rep("const pn=TX(r,it[2],{font:sans(11,500),letterSpacing:'0.16em',color:COL.ink,opacity:'0.7',marginLeft:'auto'});",
    "const pn=TX(r,it[2],{font:sans(12.5,500),letterSpacing:'0.16em',color:COL.ink,opacity:'0.75',marginLeft:'auto'});")
rep("const st=sticker(d,A.ic_heart,{x:VERT?'72%':'77%',y:VERT?'74%':'62%',size:VERT?150:232,rot:-7,face:COL.blush,label:'PEEL & KEEP'});",
    "const st=sticker(d,A.ic_heart,{x:VERT?'50%':'27%',y:VERT?'82%':'76%',size:VERT?168:238,rot:-7,face:COL.blush,label:'PEEL & KEEP'});")
rep("const cap=TX(d,'SEVEN PLATES · ONE QUESTION · 78 SYMBOLS',{left:mx,top:VERT?'86%':'88%',font:sans(10,500)",
    "const cap=TX(d,'SEVEN PLATES · ONE QUESTION · 78 SYMBOLS',{left:mx,top:VERT?'90.5%':'88.5%',font:sans(11.5,500)")

# --- s03 feature ---
rep("p.setAttribute('stroke-width','2.4')", "p.setAttribute('stroke-width','2.2')")
rep("p.setAttribute('d','M0 78 L150 78 L172 70 L192 84 L212 18 L238 112 L262 78 L330 78 L352 71 L372 83 L390 42 L410 96 L428 78 L900 78');",
    "p.setAttribute('d','M0 80 L180 80 L202 72 L220 86 L240 20 L264 112 L286 80 L384 80 L402 73 L420 85 L438 40 L456 98 L474 80 L900 80');")
rep("const st=sticker(d,A.ic_heart,{x:VERT?'50%':'77%',y:VERT?'33%':'43%',size:VERT?248:398,rot:-4,face:COL.blush});",
    "const st=sticker(d,A.ic_heart_alt,{x:VERT?'50%':'78%',y:VERT?'32%':'42%',size:VERT?300:430,rot:-4,face:COL.blush});")
rep("{left:mx,top:VERT?'70%':'74%',width:VERT?'84%':'43%',font:sans(VERT?15:16,400),lineHeight:'1.8'",
    "{left:mx,top:VERT?'70%':'74%',width:VERT?'84%':'43%',font:sans(VERT?16:17,400),lineHeight:'1.82'")
rep("const cap=TX(d,'FIG. 01 — THE ANATOMICAL HEART, AFTER THE MINOR ARCANA',{left:VERT?'8.5%':'62%',top:VERT?'84%':'83%',font:sans(10,500)",
    "const cap=TX(d,'FIG. 01 — THE ANATOMICAL HEART, AFTER THE MINOR ARCANA',{left:VERT?'8.5%':'62%',top:VERT?'84%':'83%',font:sans(11.5,500)")

# --- s04 full rewrite ---
start = s.index("/* ---------- 04 THE INDEX ---------- */")
end = s.index("/* ---------- 05 PULL QUOTE ---------- */")
new_s04 = """/* ---------- 04 THE INDEX ---------- */
function s04(d,u){
  B(d,{inset:'0',background:COL.page});
  const mx=VERT?'8.5%':'5.2%';
  const k=kick(d,'04 — THE INDEX',{left:mx,top:VERT?'5.2%':'7.4%'});
  const title=TX(d,'Sixteen of seventy-eight.',{left:mx,top:VERT?'9%':'11.5%',font:sero(VERT?50:76,true),color:COL.ink,opacity:'0'});
  const defs=[
    [A.ic_heart,'HEART'],[A.ic_butterfly,'BECOME'],[A.ic_tiger,'FEARLESS'],[A.ic_unicorn,'UNICORN'],
    [A.ic_crown,'CROWN'],[A.ic_mirror,'MIRROR'],[A.ic_compass,'COMPASS'],[A.ic_cloud_eye,'CLOUD'],
    [A.ic_wand,'WAND'],[A.ic_skull,'SKULL'],[A.ic_moon,'MOON'],[A.ic_book,'BOOK'],
    [A.scissors_sym,'LET GO'],[A.flower_sym,'CREATE'],[A.ic_star,'ORACLE'],[A.ic_eye,'TEARS']
  ];
  const cols=4, rowsn=4;
  const gx=VERT?.085:.055, gw=1-gx*2;
  const gy=VERT?.285:.315, gh=VERT?.545:.525;
  const cells=[];
  for(let i=0;i<16;i++){
    const c=i%cols, r=Math.floor(i/cols);
    const cxPct=((gx+gw*(c+0.5)/cols)*100).toFixed(2)+'%';
    const cyPct=((gy+gh*(r+0.5)/rowsn)*100).toFixed(2)+'%';
    const num=TX(d,String(i+1).padStart(3,'0'),{left:cxPct,top:cyPct,transform:'translate(-50%,-86px)',font:sans(12,500),letterSpacing:'0.18em',color:COL.berry,opacity:'0'});
    const ih=(i===15)?(VERT?96:88):(VERT?118:112);
    const im=IMG(d,defs[i][0],{left:cxPct,top:cyPct,height:ih+'px',width:'auto',transform:'translate(-50%,-50%)',opacity:'0'});
    const nm=TX(d,defs[i][1],{left:cxPct,top:cyPct,transform:'translate(-50%,62px)',font:sans(VERT?11:12,500),letterSpacing:'0.22em',color:COL.ink,opacity:'0'});
    cells.push({num,im,nm});
  }
  for(let c=1;c<cols;c++){ const x=(gx+gw*c/cols)*100; B(d,{left:x.toFixed(2)+'%',top:(gy*100)+'%',height:(gh*100)+'%',width:'1px',background:'rgba(20,16,15,.10)'}); }
  for(let r=1;r<rowsn;r++){ const y=(gy+gh*r/rowsn)*100; B(d,{left:(gx*100)+'%',right:(gx*100)+'%',top:y.toFixed(2)+'%',height:'1px',background:'rgba(20,16,15,.10)'}); }
  const folio=TX(d,'04',{right:mx,top:VERT?'5.6%':'7.6%',font:sans(12,500),letterSpacing:'0.2em',color:COL.berry});
  const cap=TX(d,'PLATE I — A KEY TO THE ICONS · 16 OF 78',{left:mx,top:VERT?'86.5%':'90.5%',font:sans(11.5,500),letterSpacing:'0.26em',color:COL.berry,opacity:'0'});
  u.push(p=>{
    k.style.opacity=String(eo(R(p,0,.16)));
    const t=eo(R(p,.03,.32)); title.style.opacity=String(t); title.style.transform='translateY('+((1-t)*20)+'px)';
    cells.forEach((c,i)=>{
      const d0=.10+(i%cols)*.02+Math.floor(i/cols)*.06;
      const q=eo(R(p,d0,d0+.22));
      c.im.style.opacity=String(q); c.num.style.opacity=String(q*.8); c.nm.style.opacity=String(q*.62);
    });
    cap.style.opacity=String(eo(R(p,.58,.8))); folio.style.opacity=String(eo(R(p,.02,.14)));
  });
}

"""
s = s[:start] + new_s04 + s[end:]

# --- s05 pull quote ---
rep("const bg=IMG(d,A.ic_eye_tears,{left:'50%',top:'52%',height:VERT?'980px':'880px',width:'auto',transform:'translate(-50%,-50%)',opacity:'0.055'});",
    "const bg=IMG(d,A['p_ic_eye_tears'],{left:'50%',top:'52%',height:VERT?'1180px':'980px',width:'auto',transform:'translate(-50%,-50%)',opacity:'0.06'});")
rep("const st=sticker(d,A.ic_butterfly,{x:VERT?'80%':'84%',y:VERT?'64%':'66%',size:VERT?130:180,rot:8,face:COL.rose});",
    "const st=sticker(d,A.ic_butterfly,{x:VERT?'80%':'86%',y:VERT?'66%':'72%',size:VERT?140:190,rot:8,face:COL.rose});")
rep("u.push(p=>{\n    const b=eo(R(p,0,.3)); bg.style.opacity=String(0.055*b);",
    "u.push(p=>{\n    const b=eo(R(p,0,.3)); bg.style.opacity=String(0.06*b);")

# --- s06 sticker sheet ---
rep("const sheet=B(d,{left:VERT?'5.5%':'8%',top:VERT?'17%':'20%',width:VERT?'89%':'84%',height:VERT?'66%':'70%',background:COL.bone,borderRadius:'18px',boxShadow:'0 30px 70px rgba(36,31,34,.16)',opacity:'0'});",
    "const sheet=B(d,{left:VERT?'5.5%':'8%',top:VERT?'17%':'20%',width:VERT?'89%':'84%',height:VERT?'66%':'70%',background:'rgba(247,242,230,.62)',border:'1px solid rgba(20,16,15,.16)',borderRadius:'18px',boxShadow:'0 24px 60px rgba(36,31,34,.12)',opacity:'0'});")
rep("const cut=TX(sheet,'KISS-CUT · 6 OF 78',{position:'absolute',left:'18px',top:'12px',font:sans(9,500)",
    "const cut=TX(sheet,'KISS-CUT · 6 OF 78',{position:'absolute',left:'18px',top:'14px',font:sans(11,500)")
rep("el.style.boxShadow='0 16px 34px rgba(36,31,34,.18), 0 1px 3px rgba(36,31,34,.12)';",
    "el.style.boxShadow='0 10px 26px rgba(36,31,34,.14), 0 1px 2px rgba(36,31,34,.08)';")
rep("const im=IMG(face,defs[i][1],{position:'relative',height:(ch2*0.42)+'px',width:'auto',maxWidth:'76%'});",
    "const im=IMG(face,defs[i][1],{position:'relative',height:(ch2*0.46)+'px',width:'auto',maxWidth:'78%'});")
rep("const lb=TX(face,defs[i][0],{font:sans(Math.max(9,cw2*0.056),500),letterSpacing:'0.18em',color:COL.ink,whiteSpace:'nowrap'});",
    "const lb=TX(face,defs[i][0],{font:sans(Math.max(11,cw2*0.062),500),letterSpacing:'0.1em',color:COL.ink,whiteSpace:'nowrap'});")
rep("const no=TX(el,String(i+1).padStart(2,'0'),{position:'absolute',right:'9px',bottom:'6px',font:sans(8,500)",
    "const no=TX(el,String(i+1).padStart(2,'0'),{position:'absolute',right:'9px',bottom:'6px',font:sans(9.5,500)")
rep("const peel=TX(d,'PEEL HERE ↘',{left:'50%',top:VERT?'86%':'93%',transform:'translate(-50%,0)',font:sans(10,500)",
    "const peel=TX(d,'PEEL HERE ↘',{left:'50%',top:VERT?'86%':'93%',transform:'translate(-50%,0)',font:sans(11.5,500)")
rep("cards.forEach((c,i)=>{ const q=eo(R(p,.14+i*.07,.34+i*.07));",
    "cards.forEach((c,i)=>{ const q=eo(R(p,.05+i*.02,.22+i*.02));")
rep("c.el.style.transform='translate(-50%,-50%) rotate('+c.rot+'deg) translateY('+((1-q)*30)+'px)';",
    "c.el.style.transform='translate(-50%,-50%) rotate('+c.rot+'deg) translateY('+((1-q)*22)+'px)';")

# --- s07 black interlude ---
rep("function s07(d,u){\n  B(d,{inset:'0',background:COL.ink});",
    "function s07(d,u){\n  B(d,{inset:'0',background:COL.ink});\n  const geye=IMG(d,A['b_ic_eye_tears'],{left:'50%',top:'50%',height:VERT?'900px':'720px',width:'auto',transform:'translate(-50%,-50%)',opacity:'0.05'});")
rep("const dot=B(d,{left:'50%',top:'58%',width:'7px',height:'7px',transform:'translate(-50%,-50%) rotate(45deg)',background:COL.berry,opacity:'0'});",
    "const dot=B(d,{left:'50%',top:'57%',width:'5px',height:'5px',transform:'translate(-50%,-50%) rotate(45deg)',background:COL.berry,opacity:'0'});")
rep("const line=B(d,{left:'30%',right:'30%',top:'64.5%',height:'1px',background:'rgba(247,242,230,.22)',opacity:'0'});",
    "const line=B(d,{left:'30%',right:'30%',top:'63%',height:'1px',background:'rgba(247,242,230,.22)',opacity:'0'});")
rep("k.style.opacity=String(eo(R(p,0,.3))*.55);\n    const f=0.86+0.14*Math.sin(p*46);\n    const a=eo(R(p,.08,.4)), b=eo(R(p,.22,.52));\n    l1.style.opacity=String(a*(0.82+0.18*f)); l1.style.transform='translate(-50%,0) translateY('+((1-a)*24)+'px)';\n    l2.style.opacity=String(b*(0.82+0.18*f)); l2.style.transform='translate(-50%,0) translateY('+((1-b)*24)+'px)';",
    "k.style.opacity=String(eo(R(p,0,.3))*.55); geye.style.opacity=String(0.05*eo(R(p,0,.4)));\n    const a=eo(R(p,.08,.4)), b=eo(R(p,.22,.52));\n    l1.style.opacity=String(a); l1.style.transform='translate(-50%,0) translateY('+((1-a)*24)+'px)';\n    l2.style.opacity=String(b); l2.style.transform='translate(-50%,0) translateY('+((1-b)*24)+'px)';")

# --- s08 seal ---
rep("border:'2px solid '+COL.goldd,borderRadius:'50%',opacity:'0'});", "border:'1.6px solid '+COL.goldd,borderRadius:'50%',opacity:'0'});")
rep("const core=IMG(d,A['g_ic_heart'],{left:'50%',top:(VERT?'46%':'47%'),height:VERT?'118px':'148px'",
    "const core=IMG(d,A['g_ic_heart'],{left:'50%',top:(VERT?'46%':'47%'),height:VERT?'124px':'158px'")
rep("const ringNames=[A['g_ic_tiger'],A['g_ic_butterfly'],A['g_ic_eye_tears'],A['g_scissors_sym'],A['g_flower_sym'],A['g_ic_unicorn'],A['g_ic_crown'],A['g_ic_skull'],A['g_ic_moon'],A['g_ic_hands'],A['g_ic_book'],A['g_ic_compass']];",
    "const ringNames=[A['g_ic_tiger'],A['g_ic_butterfly'],A['g_ic_cloud_eye'],A['g_scissors_sym'],A['g_flower_sym'],A['g_ic_unicorn'],A['g_ic_crown'],A['g_ic_skull'],A['g_ic_moon'],A['g_ic_wand'],A['g_ic_book'],A['g_ic_compass']];")
rep("const im=IMG(d,ringNames[i],{left:ix+'px',top:iy+'px',height:(VERT?74:96)+'px'",
    "const im=IMG(d,ringNames[i],{left:ix+'px',top:iy+'px',height:(VERT?86:112)+'px'")
rep("const sub=TX(d,VERT?'SIX CARDS. ONE ANSWER.':'SIX CARDS. ONE ANSWER. THE REST IS YOURS.',{left:VERT?'50%':mx,top:VERT?'86%':'89%',transform:VERT?'translate(-50%,0)':'none',font:sans(10,500)",
    "const sub=TX(d,VERT?'SIX CARDS. ONE ANSWER.':'SIX CARDS. ONE ANSWER. THE REST IS YOURS.',{left:VERT?'50%':mx,top:VERT?'86%':'89.5%',transform:VERT?'translate(-50%,0)':'none',font:sans(11.5,500)")

# --- s09 colophon ---
rep("TX(r,c[0],{font:sans(9,500),letterSpacing:'0.28em',color:COL.berry,width:VERT?'110px':'130px'});",
    "TX(r,c[0],{font:sans(11,500),letterSpacing:'0.28em',color:COL.berry,width:VERT?'122px':'140px'});")
rep("TX(r,c[1],{font:sans(13,400),letterSpacing:'0.16em',color:COL.ink});",
    "TX(r,c[1],{font:sans(15,400),letterSpacing:'0.16em',color:COL.ink});")
rep("height:(VERT?34:42)+'px',width:'auto',transform:'translate(-50%,-50%)',opacity:'0'});",
    "height:(VERT?38:46)+'px',width:'auto',transform:'translate(-50%,-50%)',opacity:'0'});")
rep("const foot=TX(d,'ISSUE 01 · MMXXVI · PRINTED IN THE STUDIO · NOT FOR SALE',{left:mx,top:VERT?'88%':'90%',font:sans(9,500)",
    "const foot=TX(d,'ISSUE 01 · MMXXVI · PRINTED IN THE STUDIO · NOT FOR SALE',{left:mx,top:VERT?'88%':'90%',font:sans(10.5,500)")

# --- s10 back cover ---
rep("const mast=TX(d,'NOT TAROT',{left:VERT?'50%':mx,top:VERT?'9%':'10%',transform:VERT?'translate(-50%,0)':'none',font:sero(VERT?64:92,false)",
    "const mast=TX(d,'NOT TAROT',{left:VERT?'50%':mx,top:VERT?'9%':'10%',transform:VERT?'translate(-50%,0)':'none',font:sero(VERT?68:98,false)")
rep("const b1=TX(d,'MAKE YOUR',{left:VERT?'50%':mx,top:VERT?'30%':'30%',transform:VERT?'translate(-50%,0)':'none',font:sero(VERT?62:92,true)",
    "const b1=TX(d,'MAKE YOUR',{left:VERT?'50%':mx,top:VERT?'30%':'30%',transform:VERT?'translate(-50%,0)':'none',font:sero(VERT?66:98,true)")
rep("const b2=TX(d,'OWN MEANING.',{left:VERT?'50%':mx,top:VERT?'37%':'40%',transform:VERT?'translate(-50%,0)':'none',font:sero(VERT?62:92,true)",
    "const b2=TX(d,'OWN MEANING.',{left:VERT?'50%':mx,top:VERT?'37%':'40%',transform:VERT?'translate(-50%,0)':'none',font:sero(VERT?66:98,true)")
rep("sticker(d,A.ic_eye_tears,{x:VERT?'28%':'26%',y:VERT?'57%':'62%',size:VERT?150:200,rot:-6,face:COL.rose}),",
    "sticker(d,A.ic_mirror,{x:VERT?'28%':'26%',y:VERT?'57%':'64%',size:VERT?158:210,rot:-6,face:COL.rose}),")
rep("const info=TX(d,'78 CARDS · ONE ANSWER THAT IS YOURS',{left:VERT?'50%':mx,top:VERT?'91%':'88.5%',transform:VERT?'translate(-50%,0)':'none',font:sans(10,500)",
    "const info=TX(d,'78 CARDS · ONE ANSWER THAT IS YOURS',{left:VERT?'50%':mx,top:VERT?'91%':'88.5%',transform:VERT?'translate(-50%,0)':'none',font:sans(11.5,500)")

# --- s11 end ---
rep("const w2=TX(d,'SEE YOU IN THE CARDS.',{left:'50%',top:'50%',transform:'translate(-50%,0)',font:sero(30,true)",
    "const w2=TX(d,'SEE YOU IN THE CARDS.',{left:'50%',top:'50%',transform:'translate(-50%,0)',font:sero(33,true)")

# --- running footer ---
rep("TX(d,'NOT TAROT — ISSUE 01 — THE ANSWER ISSUE',{left:'8%',bottom:'3.2%',font:sans(8,500),letterSpacing:'0.24em',color:fc,opacity:'0.55'});",
    "TX(d,'NOT TAROT — ISSUE 01 — THE ANSWER ISSUE',{left:'8%',bottom:'3.2%',font:sans(10,500),letterSpacing:'0.24em',color:fc,opacity:'0.62'});")
rep("TX(d,'P. '+String(i+1).padStart(2,'0'),{right:'8%',bottom:'3.2%',font:sans(8,500),letterSpacing:'0.24em',color:fc,opacity:'0.55'});",
    "TX(d,'P. '+String(i+1).padStart(2,'0'),{right:'8%',bottom:'3.2%',font:sans(10,500),letterSpacing:'0.24em',color:fc,opacity:'0.62'});")

# --- render(): paper wipe ---
start = s.index("function render(t){")
end = s.index("/* ---------- player ---------- */")
new_render = """function render(t){
  let idx=0;
  for(let i=0;i<TIMES.length;i++){ if(t>=TIMES[i][0]) idx=i; }
  const a0=TIMES[idx][0];
  const reveal = (idx===0)?1:cl((t-a0)/0.30);
  for(let i=0;i<SCENES.length;i++){
    const el=SCENES[i];
    let show=false, clip='none';
    if(i<idx-1) show=false;
    else if(i===idx-1) show=(reveal<1);
    else if(i===idx){ show=true; if(i>0) clip='inset('+((1-reveal)*100).toFixed(3)+'% 0 0 0)'; }
    el.style.opacity=show?'1':'0';
    el.style.clipPath=clip;
    const p=cl((t-TIMES[i][0])/(TIMES[i][1]-TIMES[i][0]));
    const u=UPS[i]; for(let k=0;k<u.length;k++) u[k](p,t);
  }
}

"""
s = s[:start] + new_render + s[end:]

DST.write_text(s, encoding="utf-8")
print("wrote", DST, len(s), "chars")
