"""Assemble the v5 MAGAZINE single-file film: vector icons, fonts, paper."""
import base64, json
from pathlib import Path

ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
TPL = ROOT / "_tools" / "magazine_v5_template.html"
VEC = ROOT / "03_assets" / "concept_v3" / "vec2"
FONTS = ROOT / "03_assets" / "fonts"
PAPER = ROOT / "03_assets" / "textures" / "paper_cream_hi.jpg"
OUT = ROOT / "07_final" / "NOT_TAROT_45s_v5.html"

BERRY, GOLD, BONE, PLUM = "#8F2C3B", "#5E3E17", "#F7F2E6", "#241F22"


def svg_uri(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode()


def tint(svg: str, color: str) -> str:
    return svg.replace(BERRY, color).replace("rgb(143,44,59)", color)


def scissors(color: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 160">
<g fill="none" stroke="{color}" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round">
<circle cx="38" cy="128" r="16"/><circle cx="82" cy="128" r="16"/>
<path d="M44 114 L86 20"/><path d="M76 114 L34 20"/>
<circle cx="60" cy="86" r="2.6" fill="{color}" stroke="none"/></g></svg>'''


def flower(color: str) -> str:
    parts = []
    for k in range(6):
        ang = k * 60
        parts.append(f'<path transform="rotate({ang} 60 80)" d="M60 80 C44 62 44 30 60 18 C76 30 76 62 60 80 Z"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 160">'
            f'<g fill="none" stroke="{color}" stroke-width="3.6">{"".join(parts)}'
            f'<circle cx="60" cy="80" r="14"/><circle cx="60" cy="80" r="4" fill="{color}" stroke="none"/>'
            f'<path d="M60 96 L60 150"/><path d="M60 128 C46 120 40 118 34 106"/></g></svg>')


def asset_table():
    A = {}
    for p in sorted(VEC.glob("ic_*.svg")):
        name = p.stem
        svg = p.read_text(encoding="utf-8")
        A[name] = svg_uri(svg)
        A["g_" + name] = svg_uri(tint(svg, GOLD))
        A["b_" + name] = svg_uri(tint(svg, BONE))
        A["p_" + name] = svg_uri(tint(svg, PLUM))
    for nm, fn in (("scissors_sym", scissors), ("flower_sym", flower)):
        for pre, col in (("", BERRY), ("g_", GOLD), ("b_", BONE), ("p_", PLUM)):
            A[pre + nm] = svg_uri(fn(col))
    return A


def fonts_css():
    faces = []
    for fname, fam, weight in (
        ("CormorantGaramond-400-normal.woff2", "Cormorant Garamond", 400),
        ("CormorantGaramond-600-normal.woff2", "Cormorant Garamond", 600),
        ("Jost-400-normal.woff2", "Jost", 400),
        ("Jost-500-normal.woff2", "Jost", 500),
    ):
        p = FONTS / fname
        if not p.exists():
            continue
        b64 = base64.b64encode(p.read_bytes()).decode()
        faces.append("@font-face{font-family:'" + fam + "';font-style:normal;font-weight:" + str(weight) +
                     ";font-display:block;src:url(data:font/woff2;base64," + b64 + ") format('woff2');}")
    return "\n".join(faces)


def main():
    s = TPL.read_text(encoding="utf-8")
    A = asset_table()
    s = s.replace("const A = /*__ASSETS__*/{};",
                  "const A = /*__ASSETS__*/" + json.dumps(A, ensure_ascii=False, separators=(",", ":")) + ";")
    s = s.replace("/*__FONTS__*/", fonts_css())
    paper_b64 = base64.b64encode(PAPER.read_bytes()).decode()
    s = s.replace("__PAPER__", "data:image/jpeg;base64," + paper_b64)
    OUT.write_text(s, encoding="utf-8")
    print("built", OUT, f"{OUT.stat().st_size/1e6:.2f} MB", "assets", len(A))


if __name__ == "__main__":
    main()
