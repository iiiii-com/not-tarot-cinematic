# -*- coding: utf-8 -*-
"""Assemble the v4 single-file film.

    python _tools/build_cinematic_v4.py [--out PATH]

Reads _tools/v4src/{shell.html, base.css, ui.css, acts.css, fx.css,
core.js, effects.js, scenes_a.js, scenes_b.js, interact.js, boot.js},
inlines the brand fonts, the engraving sprite set (25 motifs x 6 ink tints)
and the procedurally generated paper / grain / vignette / plate / ink-mask
textures, then writes one standalone HTML.

Textures are painted as NORMAL-composited layered images (RGB paper, RGBA
grain / vignette / plate, LA ink masks).  We deliberately avoid
mix-blend-mode for the permanent film treatment: blend groups and stacking
contexts are too easy to silence across browsers / GPU paths.
"""
import argparse
import base64
import io
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
SRC = ROOT / "_tools" / "v4src"
SPR = ROOT / "03_assets" / "symbols" / "sprites"
OUT_DEFAULT = ROOT / "07_final" / "NOT_TAROT_45s_cinematic.html"

FONT_DIRS = [
    Path(os.environ.get("NT_FONT_CACHE", "") or "_none_"),
    ROOT / "03_assets" / "fonts",
    Path(r"E:\deepseek\review_out\fonts"),
]

CSS_ORDER = ["base.css", "ui.css", "acts.css", "fx.css"]
JS_ORDER = ["core.js", "effects.js", "scenes_a.js", "scenes_b.js",
            "interact.js", "boot.js"]

SPRITES = ["heart", "eye", "eye_tears", "butterfly", "tiger", "unicorn",
           "crown", "mirror", "compass", "hands", "wand", "skull", "moon",
           "cloud_eye", "scales", "question", "book", "key", "flower",
           "star", "snake", "hourglass", "arch", "candle", "scissors"]

TINTS = {
    "berry": (143, 44, 59),
    "crimson": (176, 31, 56),
    "gold": (123, 85, 33),
    "plum": (36, 31, 34),
    "bone": (247, 242, 230),
    "mauve": (216, 165, 184),
}

FONTS = [
    # family, weight, style, cached filename, legacy project filename
    ("Cormorant Garamond", 400, "normal", "cormorant_normal_400.woff2",
     "CormorantGaramond-400-normal.woff2"),
    ("Cormorant Garamond", 500, "normal", "cormorant_normal_500.woff2",
     "CormorantGaramond-500-normal.woff2"),
    ("Cormorant Garamond", 600, "normal", "cormorant_normal_600.woff2",
     "CormorantGaramond-600-normal.woff2"),
    ("Cormorant Garamond", 400, "italic", "cormorant_italic_400.woff2", ""),
    ("Playfair Display", 500, "normal", "playfair_normal_500.woff2", ""),
    ("Playfair Display", 600, "normal", "playfair_normal_600.woff2", ""),
    ("Playfair Display", 700, "normal", "playfair_normal_700.woff2", ""),
    ("EB Garamond", 400, "normal", "ebgaramond_normal_400.woff2", ""),
    ("EB Garamond", 400, "italic", "ebgaramond_italic_400.woff2", ""),
    ("Jost", 300, "normal", "jost_normal_300.woff2", "Jost-300-normal.woff2"),
    ("Jost", 400, "normal", "jost_normal_400.woff2", "Jost-400-normal.woff2"),
    ("Jost", 500, "normal", "jost_normal_500.woff2", "Jost-500-normal.woff2"),
    ("IM Fell English SC", 400, "normal", "fell_normal_400.woff2", ""),
    ("Pinyon Script", 400, "normal", "pinyon_normal_400.woff2", ""),
]


# --------------------------------------------------------------------- utils
def b64(data):
    return base64.b64encode(data).decode("ascii")


def img_uri(im, fmt="PNG", quality=90):
    buf = io.BytesIO()
    if fmt == "JPEG":
        im.convert("RGB").save(buf, "JPEG", quality=quality, optimize=True,
                               progressive=True)
        return "data:image/jpeg;base64," + b64(buf.getvalue())
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + b64(buf.getvalue())


def alpha_boost(im):
    """extracted line art is thin + low alpha; lift it so 1px lines survive."""
    lut = [min(255, int(255 * ((i / 255.0) ** 0.38) * 1.9)) for i in range(256)]
    im = im.copy()
    im.putalpha(im.split()[3].point(lut))
    return im


def tinted(im, rgb):
    out = Image.new("RGBA", im.size, rgb + (255,))
    out.putalpha(im.split()[3])
    return out


# ---------------------------------------------------------------- textures
def _noise(w, h, sigma, seed):
    """smooth 0..1 noise field."""
    rng = np.random.default_rng(seed)
    a = (rng.random((h, w)) * 255).astype(np.uint8)
    im = Image.fromarray(a, "L").filter(ImageFilter.GaussianBlur(sigma))
    return np.asarray(im, dtype=np.float32) / 255.0


def _noise_tile(w, h, sigma, seed):
    """quadrant-averaged noise -> horizontally + vertically continuous."""
    rng = np.random.default_rng(seed)
    a = (rng.random((h * 2, w * 2)) * 255).astype(np.uint8)
    im = Image.fromarray(a, "L").filter(ImageFilter.GaussianBlur(sigma))
    arr = np.asarray(im, dtype=np.float32) / 255.0
    return (arr[:h, :w] + arr[h:, :w] + arr[:h, w:] + arr[h:, w:]) / 4.0


def make_paper(base, seed, w=1024, h=576, mottle=2.8, flecks=520,
               fibres=150, light=False, edge=5.0):
    """opaque paper stock: tone mottling + fibres + flecks + press edge."""
    arr = np.empty((h, w, 3), np.float32)
    arr[:] = base
    low = _noise(w, h, 46, seed)
    mid = _noise(w, h, 7, seed + 11)
    fine = _noise(w, h, 1.4, seed + 23)
    arr += ((low - 0.5) * 2.0 * mottle)[..., None]
    arr += ((mid - 0.5) * 2.0 * mottle * 0.6)[..., None]
    arr += ((fine - 0.5) * 2.0 * 1.1)[..., None]
    grad = np.linspace(-1.0, 1.0, h, dtype=np.float32)[:, None, None] * edge
    arr += grad
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    d = ImageDraw.Draw(im, "RGBA")
    rng = np.random.default_rng(seed + 5)
    fibre_col = (232, 222, 204) if light else (38, 29, 22)
    for _ in range(fibres):
        x = float(rng.integers(0, w))
        y = float(rng.integers(0, h))
        ln = float(rng.integers(5, 44))
        ang = float(rng.normal(0.0, 0.55))
        col = fibre_col + (int(rng.integers(3, 10)),)
        d.line([(x, y), (x + ln * math.cos(ang), y + ln * math.sin(ang))],
               fill=col, width=1)
    for _ in range(flecks):
        x = int(rng.integers(0, w))
        y = int(rng.integers(0, h))
        r = int(rng.integers(0, 2))
        if light:
            col = (208, 196, 176, int(rng.integers(3, 12)))
        else:
            col = (58, 44, 33, int(rng.integers(4, 16)))
        d.ellipse([x, y, x + r + 1, y + r + 1], fill=col)
    return im


def make_grain(seed, size=224):
    """tileable RGBA film grain: dark + light speckles, low alpha."""
    s = size
    rng = np.random.default_rng(seed)
    clump = _noise_tile(s, s, 1.7, seed)
    dark = np.clip((clump - 0.47) * 2.6, 0, 1) ** 1.25 * 44.0
    dark += (rng.random((s, s)) ** 6.0) * 26.0
    dark = np.clip(dark, 0, 54)
    light = (rng.random((s, s)) ** 8.0) * 30.0
    ad = dark / 255.0
    al = light / 255.0
    a_out = 1.0 - (1.0 - ad) * (1.0 - al)
    a_safe = np.maximum(a_out, 1e-5)
    dark_rgb = np.array([20, 18, 16], np.float32)
    light_rgb = np.array([255, 252, 246], np.float32)
    rgb = (dark_rgb * ad[..., None] +
           light_rgb * (al * (1.0 - ad))[..., None]) / a_safe[..., None]
    out = np.zeros((s, s, 4), np.uint8)
    out[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    out[..., 3] = np.clip(a_out * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def make_vignette(seed, w=1024, h=576):
    """RGBA black edge falloff, transparent centre."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nx = (xx / (w - 1) - 0.5) * 2.0
    ny = (yy / (h - 1) - 0.5) * 2.0
    r = np.sqrt((nx * 0.94) ** 2 + (ny * 1.0) ** 2) / math.sqrt(0.94 ** 2 + 1.0)
    edge = np.clip((r - 0.40) / 0.60, 0, 1) ** 1.5
    alpha = edge * 92.0
    alpha += np.clip((np.abs(ny) - 0.66) / 0.34, 0, 1) ** 2.2 * 20.0
    alpha += (_noise(w, h, 14, seed) - 0.5) * 9.0
    alpha = np.clip(alpha, 0, 124)
    out = np.zeros((h, w, 4), np.uint8)
    out[..., 0] = 9
    out[..., 1] = 7
    out[..., 2] = 6
    out[..., 3] = alpha.astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def make_plate(seed, w=1024, h=576):
    """RGBA letterpress plate pressure: barely-there mottling."""
    broad = _noise(w, h, 62, seed)
    medium = _noise(w, h, 9, seed + 3)
    alpha = np.clip(broad - 0.44, 0, 1) * 20.0
    alpha += (medium - 0.5) * 9.0
    alpha = np.clip(alpha, 0, 26)
    out = np.zeros((h, w, 4), np.uint8)
    out[..., 0] = 34
    out[..., 1] = 27
    out[..., 2] = 21
    out[..., 3] = alpha.astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def make_ink_mask(seed, size=512, grow=1.0):
    """LA mask: opaque ink blob, transparent outside, torn noisy edge."""
    s = size
    yy, xx = np.mgrid[0:s, 0:s].astype(np.float32)
    nx = (xx / (s - 1) - 0.5) * 2.0
    ny = (yy / (s - 1) - 0.52) * 2.0
    r = np.sqrt((nx * 0.96) ** 2 + ny ** 2)
    big = _noise_tile(s, s, 30, seed)
    small = _noise_tile(s, s, 6, seed + 7)
    edge = (0.66 + (big - 0.5) * 0.42 + (small - 0.5) * 0.14) * grow
    mask = np.clip((edge - r) / 0.022, 0, 1)
    alpha = (mask * 255.0).astype(np.uint8)
    lum = np.zeros((s, s), np.uint8)
    return Image.fromarray(np.stack([lum, alpha], axis=-1), "LA")


def build_textures(verbose=True):
    tx = {}
    tx["paper_cream"] = img_uri(make_paper((250, 242, 236), 101), "JPEG", 88)
    tx["paper_pageWhite"] = img_uri(make_paper((254, 250, 249), 103,
                                               mottle=1.7, flecks=300),
                                    "JPEG", 88)
    tx["paper_env"] = img_uri(make_paper((13, 11, 10), 107, mottle=2.4,
                                         flecks=900, fibres=220, light=True,
                                         edge=0.0), "JPEG", 88)
    for i in range(2):
        tx["grain_%d" % i] = img_uri(make_grain(400 + i), "PNG")
    tx["vignette"] = img_uri(make_vignette(501), "PNG")
    tx["plate"] = img_uri(make_plate(601), "PNG")
    for i in range(2):
        tx["ink_%d" % i] = img_uri(make_ink_mask(700 + i,
                                                 grow=1.0 if i == 0 else 0.9),
                                   "PNG")
    if verbose:
        print("  textures:", ", ".join("%s %.0fKB" % (k, len(v) / 1024)
                                       for k, v in tx.items()))
    return tx


# ------------------------------------------------------------------- fonts
def find_font(cached, legacy):
    for d in FONT_DIRS:
        if not d or not d.is_dir():
            continue
        for name in (cached, legacy):
            if not name:
                continue
            p = d / name
            if p.is_file():
                return p
    return None


def build_font_css(verbose=True):
    blocks = []
    total = 0
    missing = []
    for family, weight, style, cached, legacy in FONTS:
        p = find_font(cached, legacy)
        if p is None:
            missing.append(cached)
            continue
        data = p.read_bytes()
        total += len(data)
        blocks.append(
            "@font-face{font-family:'%s';font-style:%s;font-weight:%d;"
            "font-display:block;src:url(data:font/woff2;base64,%s) "
            "format('woff2');}"
            % (family, style, weight, b64(data)))
    if verbose:
        print("  fonts: %d faces, %.0fKB" % (len(blocks), total / 1024))
        if missing:
            print("  WARNING missing fonts:", ", ".join(missing))
    return "\n".join(blocks)


# ------------------------------------------------------------------ assets
def build_assets(verbose=True):
    assets = {}
    for name in SPRITES:
        p = SPR / (name + ".png")
        if not p.is_file():
            print("  WARNING missing sprite:", name)
            continue
        im = alpha_boost(Image.open(p).convert("RGBA"))
        for tint, rgb in TINTS.items():
            assets[name + "_" + tint] = img_uri(tinted(im, rgb), "PNG")
    if verbose:
        size = sum(len(v) for v in assets.values())
        print("  sprites: %d images, %.1fMB" % (len(assets), size / 1e6))
    return assets


# ------------------------------------------------------------------- build
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.environ.get("NT_OUT", str(OUT_DEFAULT)))
    ap.add_argument("--force-textures", action="store_true",
                    help="regenerate textures (they are cheap; kept for compat)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)
    out = Path(args.out)
    v = not args.quiet

    if v:
        print("building", out.name)
    font_css = build_font_css(v)
    assets = build_assets(v)
    textures = build_textures(v)

    css = []
    js = []
    for name in CSS_ORDER:
        p = SRC / name
        if not p.is_file():
            sys.exit("missing source: " + str(p))
        css.append("/* ===== %s ===== */\n" % name +
                   p.read_text(encoding="utf-8"))
    for name in JS_ORDER:
        p = SRC / name
        if not p.is_file():
            sys.exit("missing source: " + str(p))
        js.append("/* ===== %s ===== */\n" % name +
                  p.read_text(encoding="utf-8"))

    shell = (SRC / "shell.html").read_text(encoding="utf-8")
    html = shell
    html = html.replace("/*__FONT_CSS__*/", font_css)
    html = html.replace("/*__CSS__*/", "\n".join(css))
    html = html.replace("/*__ASSETS__*/{}",
                        json.dumps(assets, ensure_ascii=False,
                                   separators=(",", ":")))
    html = html.replace("/*__TEXTURES__*/{}",
                        json.dumps(textures, ensure_ascii=False,
                                   separators=(",", ":")))
    html = html.replace("/*__JS__*/", "\n".join(js))
    for token in ("__FONT_CSS__", "__CSS__", "__ASSETS__", "__TEXTURES__",
                  "__JS__"):
        if token in html:
            sys.exit("placeholder left unfilled: " + token)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    if v:
        print("built %s  %.2f MB" % (out, out.stat().st_size / 1e6))


if __name__ == "__main__":
    main()
