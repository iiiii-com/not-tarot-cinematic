"""Vector icon cleanup: crop the card-frame lines out by insetting the SVG viewBox.

Icons were traced from card crops that still carried the card's inner hairline
frame at the sprite border; insetting the viewBox by ~6% clips those frame lines
without touching the icon artwork.
"""
import re
from pathlib import Path

VEC = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO\03_assets\concept_v3\vec")
OUT = VEC.parent / "vec2"
OUT.mkdir(exist_ok=True)

INSET = 0.062

for p in sorted(VEC.glob("ic_*.svg")):
    t = p.read_text(encoding="utf-8")
    m = re.search(r'width="(\d+)" height="(\d+)"', t)
    if not m:
        # fall back: viewBox
        vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', t)
        w, h = float(vb.group(1)), float(vb.group(2))
        t = t.replace(vb.group(0), f'viewBox="{w*INSET:.1f} {h*INSET:.1f} {w*(1-2*INSET):.1f} {h*(1-2*INSET):.1f}"')
    else:
        w, h = int(m.group(1)), int(m.group(2))
        t = t.replace(m.group(0), f'width="{w}" height="{h}" viewBox="{w*INSET:.1f} {h*INSET:.1f} {w*(1-2*INSET):.1f} {h*(1-2*INSET):.1f}"')
    (OUT / p.name).write_text(t, encoding="utf-8")
    print(p.name, w, h, "->", (OUT / p.name).stat().st_size)
print("done", len(list(OUT.glob("ic_*.svg"))))
