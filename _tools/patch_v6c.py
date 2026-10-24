# -*- coding: utf-8 -*-
"""Third pass: index/seal/contents refinements."""
from pathlib import Path
T = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO\_tools\magazine_v6_template.html")
s = T.read_text(encoding="utf-8")
def rep(old, new, n=1):
    global s
    assert s.count(old) >= n, "MISS: " + old[:100]
    s = s.replace(old, new, n)

# cover: mirror sticker slightly inward
rep("sticker(d,A.ic_mirror,{x:VERT?'71%':'87%',y:VERT?'54%':'70%',size:VERT?196:238,rot:-8,face:COL.rose})",
    "sticker(d,A.ic_mirror,{x:VERT?'71%':'85.5%',y:VERT?'54%':'70%',size:VERT?196:238,rot:-8,face:COL.rose})")

# contents: faster row entrance
rep("rows.forEach((r,i)=>{ const q=eo(R(p,.18+i*.07,.42+i*.07));",
    "rows.forEach((r,i)=>{ const q=eo(R(p,.10+i*.05,.28+i*.05));")

# index: swap cloud for balance icon, nudge labels
rep("[A.ic_compass,'COMPASS'],[A.ic_cloud_eye,'CLOUD'],", "[A.ic_compass,'COMPASS'],[A.ic_scales,'BALANCE'],")
rep("transform:'translate(-50%,70px)',font:sans(VERT?12:12.5,500)", "transform:'translate(-50%,76px)',font:sans(VERT?12:12.5,500)")

# seal: berry ring icons (contrast), swap cloud for scales, headline/sub lower
rep("const ringNames=[A['g_ic_tiger'],A['g_ic_butterfly'],A['g_ic_cloud_eye'],A['g_scissors_sym'],A['g_flower_sym'],A['g_ic_unicorn'],A['g_ic_crown'],A['g_ic_skull'],A['g_ic_moon'],A['g_ic_wand'],A['g_ic_book'],A['g_ic_compass']];",
    "const ringNames=[A.ic_tiger,A.ic_butterfly,A.ic_scales,A.scissors_sym,A.flower_sym,A.ic_unicorn,A.ic_crown,A.ic_skull,A.ic_moon,A.ic_wand,A.ic_book,A.ic_compass];")
rep("ring.style.opacity=String(eo(R(p,.06,.34))*0.95);", "ring.style.opacity=String(eo(R(p,.06,.34))*0.85);")
rep("const head=TX(d,'Become.',{left:VERT?'50%':mx,top:VERT?'80%':'82.5%'", "const head=TX(d,'Become.',{left:VERT?'50%':mx,top:VERT?'80%':'81%'")
rep("const sub=TX(d,VERT?'SIX CARDS. ONE ANSWER.':'SIX CARDS. ONE ANSWER. THE REST IS YOURS.',{left:VERT?'50%':mx,top:VERT?'86.5%':'91.5%'",
    "const sub=TX(d,VERT?'SIX CARDS. ONE ANSWER.':'SIX CARDS. ONE ANSWER. THE REST IS YOURS.',{left:VERT?'50%':mx,top:VERT?'86.5%':'89.5%'")

T.write_text(s, encoding="utf-8")
print("patched v6c")
