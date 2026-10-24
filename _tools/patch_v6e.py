from pathlib import Path
T = Path(r"_tools\magazine_v6_template.html")
s = T.read_text(encoding="utf-8")
def rep(old, new, n=1):
    global s
    assert s.count(old) >= n, "MISS: " + old[:90]
    s = s.replace(old, new, n)

# wipe: reveal new page from the TOP (so the first thing seen is its masthead, not its blank bottom)
rep("if(i>0) clip='inset('+((1-reveal)*100).toFixed(3)+'% 0 0 0)';",
    "if(i>0) clip='inset(0 0 '+((1-reveal)*100).toFixed(3)+'% 0)';")

# sticker sheet: faster props so the page never reads as blank after the wipe
rep("sheet.style.opacity=String(eo(R(p,.08,.32)));", "sheet.style.opacity=String(eo(R(p,.02,.16)));")
rep("cards.forEach((c,i)=>{ const q=eo(R(p,.05+i*.02,.22+i*.02));", "cards.forEach((c,i)=>{ const q=eo(R(p,.05+i*.015,.18+i*.015));")
rep("const t=eo(R(p,.03,.3)); title.style.opacity=String(t);", "const t=eo(R(p,.01,.18)); title.style.opacity=String(t);")

T.write_text(s, encoding="utf-8")
print("patched v6e")
