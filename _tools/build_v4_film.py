"""Assemble the v4 single-file film: inline SVG icons, fonts, paper texture."""
import base64, re
from pathlib import Path

ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
TPL = ROOT / "_tools" / "cinematic_v4_template.html"
VEC = ROOT / "03_assets" / "concept_v3" / "vec2"
FONTS = ROOT / "03_assets" / "fonts"
PAPER = ROOT / "03_assets" / "textures" / "paper_cream_hi.jpg"
OUT = ROOT / "07_final" / "NOT_TAROT_45s_v4.html"

BERRY, GOLD, BONE, PLUM = "#8F2C3B", "#5E3E17", "#F7F2E6", "#241F22"


def svg_uri(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode()


def tint(svg: str, color: str) -> str:
    svg = svg.replace(BERRY, color).replace("rgb(143,44,59)", color)
    return svg


def scissors(color: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 160">
<g fill="none" stroke="{color}" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round">
<circle cx="38" cy="128" r="16"/><circle cx="82" cy="128" r="16"/>
<path d="M44 114 L86 20"/><path d="M76 114 L34 20"/>
<circle cx="60" cy="86" r="2.6" fill="{color}" stroke="none"/>
</g></svg>'''


def flower(color: str) -> str:
    petals = "".join(
        f'<path d="M60 78 C{60 + 30 * __import__("math").cos((k * 60) * 3.14159 / 180):.1f} {78 + 30 * __import__("math").sin((k * 60) * 3.14159 / 180):.1f} '
        f'{60 + 34 * __import__("math").cos((k * 60 + 18) * 3.14159 / 180):.1f} {78 + 34 * __import__("math").sin((k * 60 + 18) * 3.14159 / 180):.1f} '
        f'60 {78 + 62 * __import__("math").sin((k * 60 - 90 + 6) * 3.14159 / 180) + 62 * 0:.1f}"/>' for k in range(6))
    # simpler: 6 ellipse-ish petals drawn explicitly
    parts = []
    for k in range(6):
        ang = k * 60
        parts.append(
            f'<path transform="rotate({ang} 60 80)" d="M60 80 C44 62 44 30 60 18 C76 30 76 62 60 80 Z"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 160">'
            f'<g fill="none" stroke="{color}" stroke-width="3.6">{ "".join(parts) }'
            f'<circle cx="60" cy="80" r="14"/><circle cx="60" cy="80" r="4" fill="{color}" stroke="none"/>'
            f'<path d="M60 96 L60 150"/><path d="M60 128 C46 120 40 118 34 106"/></g></svg>')


def eye_open(color: str) -> str:
    import math
    lashes = []
    for k in range(9):
        a = math.radians(-158 + k * 17)
        x1, y1 = 800 + 690 * math.cos(a), 450 + 320 * math.sin(a)
        x2, y2 = 800 + 790 * math.cos(a), 450 + 400 * math.sin(a)
        lashes.append(f'<path d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}"/>')
    ticks = []
    for k in range(28):
        a = math.radians(k * (360 / 28))
        ticks.append(f'<path d="M{800 + 168 * math.cos(a):.0f} {450 + 168 * math.sin(a):.0f} '
                     f'L{800 + 214 * math.cos(a):.0f} {450 + 214 * math.sin(a):.0f}"/>')
    tear = '<path d="M905 690 C 930 730 936 754 922 776 C 900 790 878 772 878 748 C 878 728 892 706 905 690 Z"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900">'
            f'<g fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M40 450 C 450 110 1150 110 1560 450 C 1150 790 450 790 40 450 Z"/>'
            f'<path d="M40 450 C 450 110 1150 110 1560 450"/>'
            f'<circle cx="800" cy="450" r="238"/><circle cx="800" cy="450" r="150"/>'
            f'<circle cx="800" cy="450" r="56"/><path d="M800 392 L800 508"/>'
            f'{"".join(ticks)}{"".join(lashes)}{tear}</g>'
            f'<circle cx="800" cy="450" r="36" fill="{color}"/></svg>')


def asset_table():
    A = {}
    for p in sorted(VEC.glob("ic_*.svg")):
        name = p.stem
        svg = p.read_text(encoding="utf-8")
        A[name] = svg_uri(svg)
        A["g_" + name] = svg_uri(tint(svg, GOLD))
        A["b_" + name] = svg_uri(tint(svg, BONE))
    A["icon_heart"] = A["ic_heart"]
    A["g_icon_heart"] = A["g_ic_heart"]
    A["b_icon_heart"] = A["b_ic_heart"]
    A["eye_open"] = svg_uri(eye_open(BERRY))
    A["b_eye_open"] = svg_uri(eye_open(BONE))
    for nm, fn in (("scissors_sym", scissors), ("flower_sym", flower)):
        A[nm] = svg_uri(fn(BERRY))
        A["g_" + nm] = svg_uri(fn(GOLD))
        A["b_" + nm] = svg_uri(fn(BONE))
    return A


def fonts_css():
    faces = []
    for fname, fam, weight in (
        ("CormorantGaramond-400-normal.woff2", "Cormorant Garamond", 400),
        ("CormorantGaramond-600-normal.woff2", "Cormorant Garamond", 600),
        ("Jost-400-normal.woff2", "Jost", 400),
    ):
        p = FONTS / fname
        if not p.exists():
            continue
        b64 = base64.b64encode(p.read_bytes()).decode()
        faces.append(
            "@font-face{font-family:'" + fam + "';font-style:normal;font-weight:" + str(weight) +
            ";font-display:block;src:url(data:font/woff2;base64," + b64 + ") format('woff2');}")
    return "\n".join(faces)


def main():
    s = TPL.read_text(encoding="utf-8")
    A = asset_table()
    import json
    assets_js = json.dumps(A, ensure_ascii=False, separators=(",", ":"))
    tex_js = "{}"

    s = s.replace("const A = /*__ASSETS__*/{};", "const A = /*__ASSETS__*/" + assets_js + ";")
    s = s.replace("const TX = /*__TEXTURES__*/{};", "const TX = /*__TEXTURES__*/" + tex_js + ";")
    s = s.replace("/*__FONTS__*/", fonts_css())
    paper_b64 = base64.b64encode(PAPER.read_bytes()).decode()
    s = s.replace("TEX_PAPER", "data:image/jpeg;base64," + paper_b64)
    s = s.replace("let PLAYING=!CAPTURE, T0=performance.now()/1000, PAUSED=false, MUTED=false, CURT=0;",
                  "let PLAYING=false, T0=null, PAUSED=false, MUTED=false, CURT=0;")
    s = s.replace("ACTS.forEach((a,i)=>{ const c=E('div',ch,{}); c.className=\'chap\'; c.textContent=a[1];",
                  "ACTS.forEach((a,i)=>{ const c=E('div',ch,{}); c.className=\'chap\'; c.textContent=a[1].split(\' \')[0]; c.title=a[1];")
    OUT.write_text(s, encoding="utf-8")
    print("built", OUT, f"{OUT.stat().st_size/1e6:.2f} MB", "assets", len(A))


if __name__ == "__main__":
    main()
