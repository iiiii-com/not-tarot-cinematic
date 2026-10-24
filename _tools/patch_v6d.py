from pathlib import Path
T = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO\_tools\magazine_v6_template.html")
s = T.read_text(encoding="utf-8")
def rep(old, new, n=1):
    global s
    assert s.count(old) >= n, "MISS: " + old[:100]
    s = s.replace(old, new, n)

rep("const ringNames=[A.ic_tiger,A.ic_butterfly,A.ic_scales,A.scissors_sym,A.flower_sym,A.ic_unicorn,A.ic_crown,A.ic_skull,A.ic_moon,A.ic_wand,A.ic_book,A.ic_compass];",
    "const ringNames=[A.p_ic_tiger,A.p_ic_butterfly,A.p_ic_scales,A.p_scissors_sym,A.p_flower_sym,A.p_ic_unicorn,A.p_ic_crown,A.p_ic_skull,A.p_ic_moon,A.p_ic_wand,A.p_ic_book,A.p_ic_compass];")
rep("height:(VERT?90:118)+'px'", "height:(VERT?96:124)+'px'")
rep("const head=TX(d,'Become.',{left:VERT?'50%':mx,top:VERT?'80%':'81%',transform:VERT?'translate(-50%,0)':'none',font:sero(VERT?84:128,true)",
    "const head=TX(d,'Become.',{left:VERT?'50%':mx,top:VERT?'78%':'78.5%',transform:VERT?'translate(-50%,0)':'none',font:sero(VERT?84:120,true)")
rep("top:VERT?'86.5%':'89.5%',transform:VERT?'translate(-50%,0)':'none',font:sans(11.5,500)",
    "top:VERT?'86.5%':'90.5%',transform:VERT?'translate(-50%,0)':'none',font:sans(11.5,500)")
T.write_text(s, encoding="utf-8")
print("patched v6d")
