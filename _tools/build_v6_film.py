"""Assemble the v6 MAGAZINE single-file film: raster detail icons + vector eye + fonts + paper."""
import base64, json, math
from pathlib import Path

ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
TPL = ROOT / "_tools" / "magazine_v6_template.html"
SPR = ROOT / "03_assets" / "symbols" / "sprites6"
FONTS = ROOT / "03_assets" / "fonts"
PAPER = ROOT / "03_assets" / "textures" / "paper_cream_hi.jpg"
OUT = ROOT / "07_final" / "NOT_TAROT_45s_v6.html"

BERRY, GOLD, BONE, PLUM = "#8F2C3B", "#5E3E17", "#F7F2E6", "#241F22"
PREFIX = [("", "berry"), ("g_", "gold"), ("b_", "bone"), ("p_", "plum")]

SPRITE_KEYS = {
    "ic_heart": "heart", "ic_heart_alt": "heart_alt", "ic_butterfly": "butterfly",
    "ic_tiger": "tiger", "ic_unicorn": "unicorn", "ic_crown": "crown", "ic_mirror": "mirror",
    "ic_compass": "compass", "ic_scales": "scales", "ic_wand": "wand", "ic_skull": "skull",
    "ic_moon": "moon", "ic_cloud_eye": "cloud_eye", "ic_book": "book", "ic_key": "key",
    "ic_snake": "snake", "ic_hourglass": "hourglass", "ic_arch": "arch", "ic_candle": "candle",
    "ic_star": "star",
}


def svg_uri(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode()


def eye_svg(color):
    ticks = []
    for k in range(16):
        a = k * math.pi * 2 / 16
        r1, r2 = 104, 142
        ticks.append('<path d="M%.1f %.1f L%.1f %.1f"/>' % (
            600 + math.cos(a) * r1, 380 + math.sin(a) * r1,
            600 + math.cos(a) * r2, 380 + math.sin(a) * r2))
    lashes = []
    for k in range(9):
        t = math.pi + 0.30 + (math.pi - 0.60) * k / 8.0
        x, y = 600 + math.cos(t) * 520, 380 + math.sin(t) * 244
        dx, dy = x - 600, y - 380
        n = math.hypot(dx, dy) or 1
        lashes.append('<path d="M%.1f %.1f L%.1f %.1f"/>' % (x, y, x + dx / n * 30, y + dy / n * 30))
    tears = ('<path d="M452 556 C446 574 436 586 436 600 C436 620 452 634 472 634 C492 634 508 620 508 600 C508 584 490 566 472 544 Z" stroke-width="2.6"/>'
             '<path d="M600 604 C594 620 586 630 586 642 C586 660 600 672 618 672 C636 672 650 660 650 642 C650 628 640 616 628 600 Z" stroke-width="2.6"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 760">
<g fill="none" stroke="{color}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">
<path d="M64 380 C 310 116 890 116 1136 380 C 890 644 310 644 64 380 Z"/>
<path d="M252 212 C 430 96 770 96 948 212" stroke-width="2.8" opacity=".9"/>
<circle cx="600" cy="380" r="150"/>
<circle cx="600" cy="380" r="96" stroke-width="2.4"/>
<circle cx="600" cy="380" r="44" fill="{color}" stroke="none"/>
{chr(10).join(ticks)}
{chr(10).join(lashes)}
{tears}
</g></svg>"""


def scissors(color):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 160">
<g fill="none" stroke="{color}" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round">
<circle cx="38" cy="128" r="16"/><circle cx="82" cy="128" r="16"/>
<path d="M44 114 L86 20"/><path d="M76 114 L34 20"/>
<circle cx="60" cy="86" r="2.6" fill="{color}" stroke="none"/></g></svg>'''


def flower(color):
    parts = []
    for k in range(6):
        parts.append(f'<path transform="rotate({k*60} 60 80)" d="M60 80 C44 62 44 30 60 18 C76 30 76 62 60 80 Z"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 160">'
            f'<g fill="none" stroke="{color}" stroke-width="3.6">{"".join(parts)}'
            f'<circle cx="60" cy="80" r="14"/><circle cx="60" cy="80" r="4" fill="{color}" stroke="none"/>'
            f'<path d="M60 96 L60 150"/><path d="M60 128 C46 120 40 118 34 106"/></g></svg>')


def b64_uri(p):
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()


def asset_table():
    A = {}
    for key, spr in SPRITE_KEYS.items():
        for pre, cname in PREFIX:
            A[pre + key] = b64_uri(SPR / f"{spr}__{cname}.png")
    for pre, col in (("", BERRY), ("g_", GOLD), ("b_", BONE), ("p_", PLUM)):
        A[pre + "ic_eye"] = svg_uri(eye_svg(col))
        A[pre + "ic_eye_tears"] = svg_uri(eye_svg(col))
        A[pre + "scissors_sym"] = svg_uri(scissors(col))
        A[pre + "flower_sym"] = svg_uri(flower(col))
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
        if p.exists():
            faces.append("@font-face{font-family:'" + fam + "';font-style:normal;font-weight:" + str(weight) +
                         ";font-display:block;src:url(data:font/woff2;base64," + base64.b64encode(p.read_bytes()).decode() + ") format('woff2');}")
    return "\n".join(faces)


def main():
    s = TPL.read_text(encoding="utf-8")
    A = asset_table()
    s = s.replace("const A = /*__ASSETS__*/{};",
                  "const A = /*__ASSETS__*/" + json.dumps(A, ensure_ascii=False, separators=(",", ":")) + ";")
    s = s.replace("/*__FONTS__*/", fonts_css())
    s = s.replace("__PAPER__", "data:image/jpeg;base64," + base64.b64encode(PAPER.read_bytes()).decode())
    OUT.write_text(s, encoding="utf-8")
    print("built", OUT, f"{OUT.stat().st_size/1e6:.2f} MB", "assets", len(A))


if __name__ == "__main__":
    main()
