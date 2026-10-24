# -*- coding: utf-8 -*-
"""
NOT TAROT — 45s animatic generator (comp / pitch version)
Renders 1080 JPEG frames for 16:9 and 9:16 from the storyboard, then the
caller encodes with ffmpeg (see RUN comments at the bottom).

This is intentionally a *comp*: layout, timing, palette, type placement are
faithful; motion is placeholder-quality (no AE stroke animation / no 3D).

Outputs:
  07_final/_render/frames_16x9/frame_00001.jpg ... frame_01080.jpg
  07_final/_render/frames_9x16/frame_00001.jpg ... frame_01080.jpg
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ROOT = r"E:/deepseek/PROJECT_MYSTIC_PROMO"
CARDS = os.path.join(ROOT, "03_assets", "cards")
TEX = os.path.join(ROOT, "03_assets", "textures")
RENDER = os.path.join(ROOT, "07_final", "_render")
FPS = 24
DUR = 45.0
TOTAL = int(FPS * DUR)  # 1080

PAL = {
    "page_white": "#FEFAF9",
    "cream": "#FAF2EC",
    "blush": "#F7C7C7",
    "rose": "#F6B7CC",
    "mauve": "#D8A5B8",
    "pale_rose": "#FCE9EF",
    "berry": "#8F2C3B",
    "crimson": "#B01F38",
    "gold": "#7B5521",
    "ink": "#14100F",
    "env_black": "#0B0908",
    "bone": "#F7F2E6",
    "lilac": "#CFC3D2",
    "mint": "#B7D8DC",
    "brand_plum": "#5E3B4C",
    "white": "#FFF8EE",
}

_font_cache = {}
def font(kind, size):
    key = (kind, size)
    if key in _font_cache:
        return _font_cache[key]
    cands = {
        "serif": [r"C:/Windows/Fonts/georgia.ttf", r"C:/Windows/Fonts/times.ttf"],
        "serif_b": [r"C:/Windows/Fonts/georgiab.ttf", r"C:/Windows/Fonts/timesbd.ttf"],
        "sans": [r"C:/Windows/Fonts/arial.ttf", r"C:/Windows/Fonts/segoeui.ttf"],
        "sans_b": [r"C:/Windows/Fonts/arialbd.ttf", r"C:/Windows/Fonts/segoeuib.ttf"],
        "script": [r"C:/Windows/Fonts/segoesc.ttf", r"C:/Windows/Fonts/georgiai.ttf"],
    }[kind]
    f = None
    for p in cands:
        if os.path.exists(p):
            try:
                f = ImageFont.truetype(p, size)
                break
            except Exception:
                pass
    if f is None:
        f = ImageFont.load_default()
    _font_cache[key] = f
    return f


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


_img_cache = {}
def card(name):
    """Load + cache card image (RGBA)."""
    if name in _img_cache:
        return _img_cache[name]
    p = os.path.join(CARDS, name)
    if os.path.exists(p):
        im = Image.open(p).convert("RGBA")
    else:
        im = Image.new("RGBA", (500, 850), PAL["cream"])
        d = ImageDraw.Draw(im)
        d.rectangle([8, 8, 492, 842], outline=PAL["berry"], width=3)
        d.text((40, 380), name[:22], fill=PAL["berry"], font=font("serif", 28))
    _img_cache[name] = im
    return im


def paper(name):
    p = os.path.join(TEX, name)
    if not os.path.exists(p):
        return None
    key = "paper:" + name
    if key not in _img_cache:
        _img_cache[key] = Image.open(p).convert("RGB")
    return _img_cache[key]


def bg(size, color, paper_name=None):
    im = Image.new("RGB", size, color)
    tex = paper(paper_name) if paper_name else None
    if tex is not None:
        t = tex.resize(size, Image.LANCZOS)
        im = Image.blend(im, t, 0.22)
    return im


def paste_card(base, im, cx, cy, target_h, alpha=1.0, rot=0.0, flipx=1.0):
    """Paste card centered at (cx, cy) with height target_h, optional rotation."""
    w = int(im.width * (target_h / im.height))
    h = int(target_h)
    if w < 2 or h < 2:
        return
    card_im = im.resize((max(2, w), max(2, h)), Image.LANCZOS)
    if flipx < 1.0:
        nw = max(2, int(card_im.width * flipx))
        card_im = card_im.resize((nw, card_im.height), Image.LANCZOS)
    if rot:
        card_im = card_im.rotate(rot, expand=True, resample=Image.BICUBIC)
    if alpha < 1.0:
        r, g, b, a = card_im.split()
        a = a.point(lambda v: int(v * alpha))
        card_im.putalpha(a)
    base.paste(card_im, (int(cx - card_im.width / 2), int(cy - card_im.height / 2)), card_im)


def draw_tracked(draw, xy, text, fnt, fill, tracking=0.12, anchor_center_x=None, progress=1.0):
    """Draw text with letter-spacing. Optionally reveal by progress (0-1)."""
    text = text.upper()
    n = len(text)
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    space = fnt.size * tracking
    total = sum(widths) + space * (n - 1)
    x = xy[0] if anchor_center_x is None else anchor_center_x - total / 2
    y = xy[1]
    shown = int(math.ceil(n * max(0.0, min(1.0, progress))))
    for i, ch in enumerate(text[:shown]):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += widths[i] + space


def tracked_width(draw, text, fnt, tracking=0.12):
    text = text.upper()
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    return sum(widths) + fnt.size * tracking * max(0, len(text) - 1)


def vignette(im, strength=0.16):
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-w * 0.35, -h * 0.35, w * 1.35, h * 1.35], fill=int(255 * (1 - strength)))
    black = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.composite(im, black, mask.filter(ImageFilter.GaussianBlur(60)))


from PIL import ImageFilter  # noqa: E402  (after helpers for readability)


# ---------------------------------------------------------------- shots
def shot_s01(t, W, H):
    im = Image.new("RGB", (W, H), PAL["env_black"])
    e = card("m4_engraving_eye_angled.png")
    p = ease_in_out(min(1.0, t / 1.6))
    alpha = 0.15 + 0.85 * p
    h = H * (1.18 + 0.02 * t)
    paste_card(im, e, W * 0.5, H * 0.52, h, alpha=alpha)
    return im


def shot_s02(t, W, H):
    im = Image.new("RGB", (W, H), PAL["env_black"])
    e = card("m4_engraving_eye_angled.png")
    h = H * (1.22 + 0.02 * t)
    paste_card(im, e, W * 0.5, H * 0.44, h, alpha=1.0)
    d = ImageDraw.Draw(im)
    # caption sits BELOW the etching (animatic subtitle, not part of the artwork)
    f = font("serif", int(H * 0.026))
    draw_tracked(d, (0, H * 0.885), "THE ALL-SEEING EYE", f, PAL["bone"],
                 tracking=0.16, anchor_center_x=W / 2, progress=min(1.0, t / 1.1))
    f2 = font("serif", int(H * 0.015))
    draw_tracked(d, (0, H * 0.935), "TRUE SIGHT GOES BEYOND VISION", f2, PAL["bone"],
                 tracking=0.10, anchor_center_x=W / 2, progress=min(1.0, max(0, t - 0.6) / 1.0))
    return im


def shot_s03(t, W, H):
    """paper-ink bleed: black -> blush"""
    im = bg((W, H), PAL["blush"], "paper_blush.jpg")
    black = Image.new("RGB", (W, H), PAL["env_black"])
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    # irregular black veil receding from lower-right
    p = ease_in_out(t)
    rnd = random.Random(7)
    for i in range(90):
        x = W * (0.15 + rnd.random() * 1.0) * (1 + p * 0.6) - p * W * 0.4
        y = H * (rnd.random() * 1.1) - p * H * 0.2
        rr = (W * 0.10 + rnd.random() * W * 0.22) * (1.0 - 0.8 * p)
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(6))
    return Image.composite(black, im, mask)


def m1_band(W, H, color, paper_name):
    return bg((W, H), color, paper_name)


def shot_s04(t, W, H):
    im = m1_band(W, H, PAL["blush"], "paper_blush.jpg")
    cards = ["m1_07_get_shit_done.png", "m1_02_band_aid_whisperer.png", "m1b_06_tears_are_power.png"]
    starts = [0.1, 1.45, 2.8]
    h = H * 0.78
    for i, (name, st) in enumerate(zip(cards, starts)):
        if t < st:
            continue
        lt = min(1.0, (t - st) / 0.32)
        e = ease_out(lt)
        alpha = min(1.0, lt * 1.8)
        dy = (1 - e) * H * 0.10
        pop = 1.0 + 0.03 * math.sin(math.pi * min(1.0, (t - st) / 0.5))
        rot = (-2.2, 0.0, 2.2)[i] if W > H else 0
        paste_card(im, card(name), W * 0.5, H * 0.50 + dy, h * pop, alpha=alpha, rot=rot)
    return im


def shot_s05(t, W, H):
    im = m1_band(W, H, PAL["blush"], "paper_blush.jpg")
    h = H * 0.80
    # main card center-left
    cx = W * (0.42 if W > H else 0.5)
    paste_card(im, card("m1b_06_tears_are_power.png"), cx, H * 0.51 + math.sin(t * 2.2) * 2, h)
    # two slides from right
    slides = [("m1_08_fearless.png", 1.2), ("m1_03_ceo_babe.png", 1.7)]
    for i, (name, st) in enumerate(slides):
        if t < st:
            continue
        e = ease_out(min(1.0, (t - st) / 0.55))
        x = W * (1.02 - 0.30 * e) if W > H else W * (0.78 + 0.02 * i)
        y = H * (0.44 - 0.06 * i) if W > H else H * (0.30 + 0.06 * i)
        paste_card(im, card(name), x, y, h * 0.62, rot=-5 + i * 3)
    return im


def shot_s06(t, W, H):
    im = bg((W, H), PAL["mauve"], "paper_mauve.jpg")
    h = H * 0.78
    if t < 2.2:
        # flip 0-0.6 then hold fool
        if t < 0.6:
            p = t / 0.6
            fx = abs(math.cos(math.pi * p))
            img = "m2_the_fool.png" if p < 0.5 else "m2_major_02.png"
        else:
            fx = 1.0
            img = "m2_the_fool.png"
        paste_card(im, card(img), W * 0.5, H * 0.5, h, flipx=max(0.02, fx))
    else:
        paste_card(im, card("m2_major_02.png"), W * 0.5, H * 0.5, h)
    return im


def shot_s07(t, W, H):
    im = Image.new("RGB", (W, H), PAL["env_black"])
    e = card("m4_engraving_eye_angled.png")
    paste_card(im, e, W * 0.5, H * 0.38, H * (0.95 + 0.03 * t), alpha=0.95)
    d = ImageDraw.Draw(im)
    f = font("serif", int(H * 0.085))
    draw_tracked(d, (0, H * 0.80), "XXVI", f, PAL["bone"], tracking=0.16,
                 anchor_center_x=W / 2, progress=min(1.0, t / 1.0))
    return im


def shot_s08(t, W, H):
    im = m1_band(W, H, PAL["blush"], "paper_blush.jpg")
    cards = ["m1b_09_karma_is_a_bitch.png", "m1_06_namaste_bitches.png", "m1b_08_nostalgia_overload.png"]
    idx = min(2, int(t / 1.3))
    lt = t - idx * 1.3
    pop = 1.0 + 0.02 * math.sin(math.pi * min(1.0, lt / 0.25))
    paste_card(im, card(cards[idx]), W * 0.5, H * 0.5, H * 0.82 * pop)
    return im


def shot_s09(t, W, H):
    im = bg((W, H), PAL["rose"], "paper_rose.jpg")
    h = H * 0.84
    src = card("m3_knowing_26.png")
    cw = h * (src.width / src.height)
    cx, cy = W * 0.5, H * 0.5
    paste_card(im, src, cx, cy, h, alpha=0.97)
    d = ImageDraw.Draw(im)
    # gold border self-draw along the card's own outer border (inset 2.5%)
    inset = 0.025
    x0, y0 = cx - cw * (0.5 - inset), cy - h * (0.5 - inset)
    x1, y1 = cx + cw * (0.5 - inset), cy + h * (0.5 - inset)
    p = ease_in_out(max(0.0, min(1.0, (t - 0.2) / 2.0)))
    if p > 0:
        col = PAL["gold"]
        wdt = max(2, int(h * 0.005))
        per = 2 * (x1 - x0) + 2 * (y1 - y0)
        ln = per * p
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
        for i in range(len(pts) - 1):
            ax, ay = pts[i]
            bx, by = pts[i + 1]
            seg = math.hypot(bx - ax, by - ay)
            if ln <= 0:
                break
            f = min(1.0, ln / seg) if seg else 1.0
            d.line([ax, ay, ax + (bx - ax) * f, ay + (by - ay) * f], fill=col, width=wdt)
            ln -= seg
    return im


def shot_s10(t, W, H):
    a = m1_band(W, H, PAL["blush"], "paper_blush.jpg")
    paste_card(a, card("m1b_06_tears_are_power.png"), W * 0.5, H * 0.5, H * 0.86)
    b = Image.new("RGB", (W, H), PAL["env_black"])
    paste_card(b, card("m4_engraving_eye_angled.png"), W * 0.5, H * 0.5, H * 0.86)
    if t < 1.2:
        p = 0.0
    elif t < 1.55:
        p = ease_in_out((t - 1.2) / 0.35)
    elif t < 2.8:
        p = 1.0
    elif t < 3.2:
        p = 1.0 - ease_in_out((t - 2.8) / 0.4)
    else:
        p = 0.0
    if p <= 0:
        return a
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    # vertical noisy edge moving right -> left
    edge = W * (1.02 - p * 1.06)
    rnd = random.Random(11)
    jitter = [rnd.randint(-8, 8) for _ in range(H)]
    for y in range(H):
        d.line([max(0, edge + jitter[y]), y, W, y], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(2.5))
    return Image.composite(b, a, mask)


_ref_cache = {}
def ref_img(name):
    p = os.path.join(ROOT, "00_reference", name)
    if name not in _ref_cache:
        _ref_cache[name] = Image.open(p).convert("RGBA")
    return _ref_cache[name]


def shot_s11(t, W, H):
    """Brand layer = the reference brand page itself (catalog spread) + 3 cards."""
    im = bg((W, H), PAL["page_white"], "paper_page_white.jpg")
    doc = ref_img("reference_07_brand_page.jpg")
    if W > H:
        # left: brand page document (kept whole, it IS the brand-layer reference)
        dh = H * 0.59
        paste_card(im, doc, W * 0.28, H * 0.50, dh)
        # right: three cards as a vertical column, labels visible
        for i, name in enumerate(["m1b_06_tears_are_power.png", "m1_07_get_shit_done.png", "m1_08_fearless.png"]):
            e = ease_out(min(1.0, max(0.0, (t - 0.5 - i * 0.12) / 0.5)))
            paste_card(im, card(name), W * 0.815, H * (0.245 + i * 0.25) + (1 - e) * H * 0.06,
                       H * 0.225, alpha=e, rot=(-3, 0, 3)[i])
        d = ImageDraw.Draw(im)
        f2 = font("sans", int(H * 0.019))
        draw_tracked(d, (0, H * 0.945), "NOT TAROT", f2, PAL["brand_plum"], tracking=0.34,
                     anchor_center_x=W * 0.28)
    else:
        dh = H * 0.42
        dw = dh * (doc.width / doc.height)
        paste_card(im, doc, W * 0.5, H * 0.235, dh)
        for i, name in enumerate(["m1b_06_tears_are_power.png", "m1_07_get_shit_done.png", "m1_08_fearless.png"]):
            e = ease_out(min(1.0, max(0.0, (t - 0.5 - i * 0.12) / 0.5)))
            paste_card(im, card(name), W * (0.22 + i * 0.28), H * 0.70 + (1 - e) * H * 0.05,
                       H * 0.25, alpha=e, rot=(-3, 0, 3)[i])
        d = ImageDraw.Draw(im)
        draw_tracked(d, (0, H * 0.905), "NOT TAROT", font("sans", int(H * 0.024)),
                     PAL["brand_plum"], tracking=0.32, anchor_center_x=W / 2)
    return im


def shot_s12(t, W, H):
    im = bg((W, H), PAL["page_white"], "paper_page_white.jpg")
    names = ["m1_v1_berry_tears_are_power.png", "m1_v2_black_tears_are_power.png",
             "m1_v3_lilac_tears_are_power.png"]
    floaty = math.sin(t * 2.4) * 2
    if W > H:
        for i, name in enumerate(names):
            paste_card(im, card(name), W * (0.26 + 0.24 * i), H * 0.50 + floaty, H * 0.70)
    else:
        for i, name in enumerate(names):
            paste_card(im, card(name), W * 0.5, H * (0.26 + 0.26 * i) + floaty, H * 0.22)
    d = ImageDraw.Draw(im)
    f = font("sans", int(H * 0.020))
    draw_tracked(d, (0, H * 0.93), "THREE MOODS, ONE DECK", f, PAL["brand_plum"],
                 tracking=0.16, anchor_center_x=W / 2)
    return im


def shot_s13(t, W, H):
    im = Image.new("RGB", (W, H), PAL["env_black"])
    d = ImageDraw.Draw(im)
    a = min(1.0, t / 0.8)
    f = font("serif_b", int(H * 0.075))
    tw = tracked_width(d, "NOT TAROT", f, 0.34)
    x = W / 2 - tw / 2
    y = H * 0.46
    for i, chh in enumerate("NOT TAROT"):
        ch = chh.upper()
        if ch.strip():
            col = tuple(int(c * a) for c in tuple(int(PAL["bone"][k:k + 2], 16) for k in (1, 3, 5)))
            d.text((x, y), ch, font=f, fill=col)
        x += d.textlength(ch, font=f) + f.size * 0.34
    if t > 0.9:
        f2 = font("serif", int(H * 0.022))
        a2 = min(1.0, (t - 0.9) / 0.6)
        col2 = tuple(int(c * a2) for c in tuple(int(PAL["bone"][k:k + 2], 16) for k in (1, 3, 5)))
        draw_tracked(d, (0, H * 0.60), "YOU ALREADY KNOW", f2, col2, tracking=0.18,
                     anchor_center_x=W / 2, progress=min(1.0, max(0.0, (t - 0.9) / 0.8)))
    return im


SHOTS = [
    (0.0, 3.0, shot_s01),
    (3.0, 6.0, shot_s02),
    (6.0, 7.0, shot_s03),
    (7.0, 11.0, shot_s04),
    (11.0, 15.0, shot_s05),
    (15.0, 19.0, shot_s06),
    (19.0, 22.0, shot_s07),
    (22.0, 26.0, shot_s08),
    (26.0, 30.0, shot_s09),
    (30.0, 34.0, shot_s10),
    (34.0, 38.0, shot_s11),
    (38.0, 42.0, shot_s12),
    (42.0, 45.0, shot_s13),
]


def render(vertical=False):
    W, H = (720, 1280) if vertical else (1280, 720)
    out = os.path.join(RENDER, "frames_9x16" if vertical else "frames_16x9")
    os.makedirs(out, exist_ok=True)
    for i in range(TOTAL):
        t = i / FPS
        for (a, b, fn) in SHOTS:
            if a <= t < b:
                im = fn(t - a, W, H)
                break
        else:
            im = Image.new("RGB", (W, H), PAL["env_black"])
        im = ImageEnhance.Brightness(im).enhance(0.99 + 0.01 * math.sin(i * 0.7))
        im.save(os.path.join(out, f"frame_{i + 1:05d}.jpg"), quality=90)
        if (i + 1) % 120 == 0:
            print(f"{'9x16' if vertical else '16x9'}: {i + 1}/{TOTAL}", flush=True)
    print("done:", out, flush=True)


if __name__ == "__main__":
    render(vertical=False)
    render(vertical=True)
