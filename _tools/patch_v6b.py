# -*- coding: utf-8 -*-
"""Second pass patch on magazine_v6_template.html (layout/typography/scene fixes)."""
from pathlib import Path
ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
T = ROOT / "_tools" / "magazine_v6_template.html"
s = T.read_text(encoding="utf-8")

def rep(old, new, n=1):
    global s
    assert s.count(old) >= n, "MISS: " + old[:100]
    s = s.replace(old, new, n)

# 1) barcode bars must be flex children, not absolutely positioned
rep("for(let i=0;i<26;i++){ const w=(i%4===0)?3:(i%3===0?2:1); const h=34*(i%5===0?1:(0.55+((i*37)%40)/70)); B(wrap,{width:w+'px',height:h+'px',background:COL.ink}); }",
    "for(let i=0;i<26;i++){ const w=(i%4===0)?3:(i%3===0?2:1); const h=34*(i%5===0?1:(0.55+((i*37)%40)/70)); const bb=document.createElement('div'); bb.style.width=w+'px'; bb.style.height=h+'px'; bb.style.background=COL.ink; wrap.appendChild(bb); }")

# 2) contents rows: roman numerals + editorial descriptions + reposition sticker
old_rows = """  const items=[['03','THE HEART','03'],['07','THE INDEX','07'],['11','THE STICKER SHEET','11'],['15','THE SEAL','15'],['18','COLOPHON','18']];
  const rows=items.map((it,i)=>{
    const r=E('div',rowsEl,{display:'flex',alignItems:'baseline',gap:'16px',opacity:'0',paddingBottom:'10px',borderBottom:'1px dotted rgba(20,16,15,.30)'});
    const n=TX(r,it[0],{font:sans(13,500),letterSpacing:'0.2em',color:COL.berry,width:'44px'});
    const t=TX(r,it[1],{font:sero(VERT?33:41),color:COL.ink,whiteSpace:'nowrap'});
    
    const pn=TX(r,it[2],{font:sans(12.5,500),letterSpacing:'0.16em',color:COL.ink,opacity:'0.75',marginLeft:'auto'});
    return r;
  });"""
new_rows = """  const items=[['I','THE HEART','A mirror with a pulse.','03'],['II','THE INDEX','Sixteen keys, seventy-eight symbols.','07'],['III','THE STICKER SHEET','Six to peel, keep, and carry.','11'],['IV','THE SEAL','Where the symbols become one.','15'],['V','COLOPHON','Paper, type, and thanks.','18']];
  const rows=items.map((it,i)=>{
    const r=E('div',rowsEl,{display:'flex',flexDirection:'column',gap:'5px',opacity:'0',paddingBottom:'13px',borderBottom:'1px dotted rgba(20,16,15,.30)'});
    const top=E('div',r,{display:'flex',alignItems:'baseline',gap:'16px'});
    TX(top,it[0],{font:sans(12,500),letterSpacing:'0.2em',color:COL.berry,width:'34px'});
    TX(top,it[1],{font:sero(VERT?31:40),color:COL.ink,whiteSpace:'nowrap'});
    TX(top,it[3],{font:sans(12,500),letterSpacing:'0.16em',color:COL.ink,opacity:'0.72',marginLeft:'auto'});
    TX(r,it[2],{marginLeft:'50px',font:sans(VERT?13:14,400),letterSpacing:'0.03em',color:COL.ink,opacity:'0.62'});
    return r;
  });"""
rep(old_rows, new_rows)
rep("const st=sticker(d,A.ic_heart,{x:VERT?'50%':'27%',y:VERT?'82%':'76%',size:VERT?168:238,rot:-7,face:COL.blush,label:'PEEL & KEEP'});",
    "const st=sticker(d,A.ic_heart,{x:VERT?'50%':'27%',y:VERT?'82%':'67%',size:VERT?168:236,rot:-7,face:COL.blush,label:'PEEL & KEEP'});")

# 3) feature: heart_alt sticker larger
rep("const st=sticker(d,A.ic_heart_alt,{x:VERT?'50%':'78%',y:VERT?'32%':'42%',size:VERT?300:430,rot:-4,face:COL.blush});",
    "const st=sticker(d,A.ic_heart_alt,{x:VERT?'50%':'78%',y:VERT?'32%':'42%',size:VERT?316:468,rot:-4,face:COL.blush,iconH:0.76});")

# 4) index grid: bigger icons, clear label gaps
rep("const gy=VERT?.285:.315, gh=VERT?.545:.525;", "const gy=VERT?.255:.255, gh=VERT?.575:.60;")
rep("const num=TX(d,String(i+1).padStart(3,'0'),{left:cxPct,top:cyPct,transform:'translate(-50%,-86px)',font:sans(12,500)",
    "const num=TX(d,String(i+1).padStart(3,'0'),{left:cxPct,top:cyPct,transform:'translate(-50%,-92px)',font:sans(12,500)")
rep("const ih=(i===15)?(VERT?96:88):(VERT?118:112);", "const ih=(i===15)?(VERT?104:98):(VERT?136:128);")
rep("const nm=TX(d,defs[i][1],{left:cxPct,top:cyPct,transform:'translate(-50%,62px)',font:sans(VERT?11:12,500)",
    "const nm=TX(d,defs[i][1],{left:cxPct,top:cyPct,transform:'translate(-50%,70px)',font:sans(VERT?12:12.5,500)")
rep("background:'rgba(20,16,15,.10)'}); }\n  for(let r=1;r<rowsn;r++)", "background:'rgba(20,16,15,.08)'}); }\n  for(let r=1;r<rowsn;r++)")
rep("top:y.toFixed(2)+'%',height:'1px',background:'rgba(20,16,15,.10)'}); }",
    "top:y.toFixed(2)+'%',height:'1px',background:'rgba(20,16,15,.08)'}); }")

# 5) seal: smaller ring, lower headline, bigger icons
rep("const R0=VERT?236:392, cy=H*(VERT?0.46:0.47);", "const R0=VERT?228:364, cy=H*(VERT?0.46:0.455);")
rep("height:(VERT?86:112)+'px'", "height:(VERT?90:118)+'px'")
rep("const head=TX(d,'Become.',{left:VERT?'50%':mx,top:VERT?'79%':'78%',transform:VERT?'translate(-50%,0)':'none',font:sero(VERT?84:132,true)",
    "const head=TX(d,'Become.',{left:VERT?'50%':mx,top:VERT?'80%':'82.5%',transform:VERT?'translate(-50%,0)':'none',font:sero(VERT?84:128,true)")
rep("const sub=TX(d,VERT?'SIX CARDS. ONE ANSWER.':'SIX CARDS. ONE ANSWER. THE REST IS YOURS.',{left:VERT?'50%':mx,top:VERT?'86%':'89.5%'",
    "const sub=TX(d,VERT?'SIX CARDS. ONE ANSWER.':'SIX CARDS. ONE ANSWER. THE REST IS YOURS.',{left:VERT?'50%':mx,top:VERT?'86.5%':'91.5%'")

# 6) colophon: add editorial note + spacing
rep("const bx=VERT?'8.5%':'5.2%', by=VERT?'36%':'38%';", "const bx=VERT?'8.5%':'5.2%', by=VERT?'36%':'37%';")
rep("const r=B(d,{left:bx,top:'calc('+by+' + '+(i*42)+'px)',display:'flex',gap:'28px',opacity:'0'});",
    "const r=B(d,{left:bx,top:'calc('+by+' + '+(i*44)+'px)',display:'flex',gap:'28px',opacity:'0'});")
rep("const folio=TX(d,'09',", "const note=TX(d,'Every symbol in this issue was drawn by hand, then pressed into uncoated paper. One ink, one paper, one question \\u2014 and seventy-eight ways to answer it.',{left:bx,top:VERT?'63%':'64%',width:VERT?'84%':'34%',font:sans(VERT?14:14.5,400),lineHeight:'1.85',color:COL.ink,opacity:'0'});\n  const folio=TX(d,'09',")
rep("    foot.style.opacity=String(eo(R(p,.6,.82))*.8); folio.style.opacity=String(eo(R(p,.02,.16)));",
    "    note.style.opacity=String(eo(R(p,.34,.6))*.72);\n    foot.style.opacity=String(eo(R(p,.6,.82))*.8); folio.style.opacity=String(eo(R(p,.02,.16)));")

T.write_text(s, encoding="utf-8")
print("patched v6b", len(s))
