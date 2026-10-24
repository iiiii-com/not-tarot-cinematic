# -*- coding: utf-8 -*-
"""
NOT TAROT — 45s concept film ANIMATIC (director's cut)

Renders the 18 shots of 02_storyboard/storyboard_45s_director_cut.md with
reference-derived line-art sprites.

Usage:
  python _tools/make_director_film.py kf          # 18 keyframe stills 1920x1080
  python _tools/make_director_film.py frames 16x9 # 1080 jpg frames -> 07_final/_render_dir/frames_16x9
  python _tools/make_director_film.py frames 9x16
"""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = r"E:/deepseek/PROJECT_MYSTIC_PROMO"
SPR = os.path.join(ROOT, "03_assets", "symbols", "sprites")
TEX = os.path.join(ROOT, "03_assets", "textures")
RENDER = os.path.join(ROOT, "07_final", "_render_dir")
KF = os.path.join(ROOT, "03_assets", "keyframes")
FPS = 24
TOTAL = 1080

PAL = {
    "page_white": (254, 250, 249),
    "cream": (250, 242, 236),
    "blush": (247, 199, 199),
    "rose": (246, 183, 204),
    "mauve": (216, 165, 184),
    "pale_rose": (252, 233, 239),
    "berry": (143, 44, 59),
    "crimson": (176, 31, 56),
    "gold": (123, 85, 33),
    "ink": (20, 16, 15),
    "env_black": (11, 9, 8),
    "bone": (247, 242, 230),
    "white": (255, 248, 238),
    "plum": (94, 59, 76),
    "brand_plum": (36, 31, 34),
}

# ---------------------------------------------------------------- fonts
_fc = {}


def font(kind, size):
    key = (kind, int(size))
    if key in _fc:
        return _fc[key]
    cands = {
        "serif": [r"C:/Windows/Fonts/georgia.ttf", r"C:/Windows/Fonts/times.ttf"],
        "serif_b": [r"C:/Windows/Fonts/georgiab.ttf", r"C:/Windows/Fonts/times.ttf"],
        "sans": [r"C:/Windows/Fonts/arial.ttf", r"C:/Windows/Fonts/segoeui.ttf"],
    }[kind]
    f = None
    for p in cands:
        if os.path.exists(p):
            try:
                f = ImageFont.truetype(p, int(size))
                break
            except Exception:
                pass
    if f is None:
        try:
            f = ImageFont.load_default(size=int(size))
        except TypeError:
            f = ImageFont.load_default()
    _fc[key] = f
    return f


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def eout(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def lerp(a, b, t):
    return a + (b - a) * t


def mix(c1, c2, t):
    return tuple(int(round(lerp(c1[i], c2[i], t))) for i in range(3))


# ---------------------------------------------------------------- assets
_sp = {}
_tex = {}


def sprite(name):
    if name not in _sp:
        p = os.path.join(SPR, name + ".png")
        im = Image.open(p).convert("RGBA")
        # lift the anti-aliased ink so 1-2 px lines survive scaling in the film
        lut = [min(255, int(255 * ((i / 255.0) ** 0.68) * 1.30)) for i in range(256)]
        a = im.split()[3].point(lut)
        im.putalpha(a)
        _sp[name] = im
    return _sp[name]


_tint_cache = {}


def tinted(name, color):
    key = (name, color)
    if key not in _tint_cache:
        s = sprite(name)
        out = Image.new("RGBA", s.size, tuple(color) + (255,))
        out.putalpha(s.split()[3])
        _tint_cache[key] = out
    return _tint_cache[key]


def paper(name):
    if name not in _tex:
        _tex[name] = Image.open(os.path.join(TEX, name)).convert("RGB")
    return _tex[name]


_bg_cache = {}


def bg(W, H, color, paper_name=None, grain=0.20):
    key = (W, H, tuple(color), paper_name, grain)
    if key in _bg_cache:
        return _bg_cache[key].copy()
    im = Image.new("RGB", (W, H), tuple(color))
    if paper_name:
        im = Image.blend(im, paper(paper_name).resize((W, H), Image.LANCZOS), grain)
    _bg_cache[key] = im
    return im.copy()


_res_cache = {}


def resized(im, h):
    """resize RGBA sprite to height h (cached)."""
    h = max(2, int(round(h)))
    key = (id(im), h)
    if key not in _res_cache:
        w = max(2, int(round(im.width * h / im.height)))
        _res_cache[key] = im.resize((w, h), Image.LANCZOS)
    return _res_cache[key]


def paste_sp(base, im, cx, cy, h, alpha=1.0, rot=0, tint=None):
    if tint is not None:
        im = tinted_im(im, tint)
    s = resized(im, h)
    if rot:
        s = s.rotate(rot, expand=True, resample=Image.BICUBIC)
    if alpha < 1.0:
        a = s.split()[3].point(lambda v: int(v * max(0.0, alpha)))
        s = s.copy()
        s.putalpha(a)
    base.paste(s, (int(cx - s.width / 2), int(cy - s.height / 2)), s)


_tintim = {}


def tinted_im(im, color):
    key = (id(im), tuple(color))
    if key not in _tintim:
        out = Image.new("RGBA", im.size, tuple(color) + (255,))
        out.putalpha(im.split()[3])
        _tintim[key] = out
    return _tintim[key]


def text_tracked(d, cx, y, s, f, fill, tracking=0.14, progress=1.0, alpha=1.0):
    s = s.upper()
    n = len(s)
    if n == 0:
        return
    widths = [d.textlength(ch, font=f) for ch in s]
    sp = f.size * tracking
    total = sum(widths) + sp * (n - 1)
    x = cx - total / 2
    shown = int(math.ceil(n * max(0.0, min(1.0, progress))))
    fill = tuple(int(round(c * alpha)) for c in fill[:3])
    for i, ch in enumerate(s[:shown]):
        d.text((x, y), ch, font=f, fill=fill)
        x += widths[i] + sp


def camera(im, zoom):
    """zoom >= 1: crop centre; zoom < 1: shrink on same-size canvas."""
    W, H = im.size
    if abs(zoom - 1.0) < 0.002:
        return im
    if zoom >= 1.0:
        cw, ch = int(W / zoom), int(H / zoom)
        x = (W - cw) // 2
        y = (H - ch) // 2
        return im.crop((x, y, x + cw, y + ch)).resize((W, H), Image.LANCZOS)
    nw, nh = int(W * zoom), int(H * zoom)
    out = Image.new("RGB", (W, H), PAL["cream"])
    sm = im.resize((nw, nh), Image.LANCZOS)
    out.paste(sm, ((W - nw) // 2, (H - nh) // 2))
    return out


# ---------------------------------------------------------------- ECG
ECG_PTS = [(0.00, 0.0), (0.18, 0.0), (0.22, -0.10), (0.26, 0.0), (0.30, 0.02),
           (0.335, -0.42), (0.365, 0.22), (0.40, 0.0), (0.46, 0.0), (0.50, -0.06),
           (0.54, 0.03), (0.58, 0.0), (0.62, -0.33), (0.65, 0.17), (0.69, 0.0), (1.0, 0.0)]


def ecg_points(x0, y0, w, h, progress, samples=260):
    pts = []
    n = len(ECG_PTS) - 1
    for i in range(samples):
        t = i / (samples - 1.0) * progress
        j = min(n - 1, int(t * n))
        f = t * n - j
        ax, ay = ECG_PTS[j]
        bx, by = ECG_PTS[j + 1]
        pts.append((x0 + (ax + (bx - ax) * f) * w, y0 - (ay + (by - ay) * f) * h))
    return pts


# ---------------------------------------------------------------- cards
_card_cache = {}


def m1_card(name, h, label, color="berry"):
    """cream card + blush panel + sprite + label."""
    key = (name, int(h), label, color)
    if key in _card_cache:
        return _card_cache[key]
    cw = int(h / 1.714)
    c = Image.new("RGBA", (cw, int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    ink = PAL[color]
    d.rounded_rectangle([0, 0, cw - 1, h - 1], radius=max(3, int(h * 0.018)),
                        fill=PAL["cream"], outline=ink, width=max(1, int(h * 0.0022)))
    m = int(cw * 0.055)
    d.rounded_rectangle([m, m, cw - m, h - m], radius=max(2, int(h * 0.011)),
                        fill=PAL["blush"], outline=ink, width=max(1, int(h * 0.0016)))
    sp = sprite(name)
    art_h = h * 0.55
    paste_sp(c, sp, cw * 0.5, h * 0.40, art_h, tint=None)
    f = font("serif", max(8, int(h * 0.052)))
    text_tracked(d, cw * 0.5, h * 0.80, label, f, ink, tracking=0.08)
    # thin baseline
    tw = 0
    for ch in label.upper():
        tw += d.textlength(ch, font=f) + f.size * 0.08
    d.line([(cw * 0.5 - tw * 0.5, h * 0.875), (cw * 0.5 + tw * 0.5, h * 0.875)],
           fill=ink, width=max(1, int(h * 0.0016)))
    _card_cache[key] = c
    return c


def blank_card(h):
    key = ("blank", int(h))
    if key in _card_cache:
        return _card_cache[key]
    cw = int(h / 1.714)
    c = Image.new("RGBA", (cw, int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    ink = PAL["berry"]
    d.rounded_rectangle([0, 0, cw - 1, h - 1], radius=max(3, int(h * 0.018)),
                        fill=PAL["cream"], outline=ink, width=max(1, int(h * 0.0022)))
    m = int(cw * 0.055)
    d.rounded_rectangle([m, m, cw - m, h - m], radius=max(2, int(h * 0.011)),
                        fill=PAL["blush"], outline=ink, width=max(1, int(h * 0.0016)))
    _card_cache[key] = c
    return c


# ---------------------------------------------------------------- shots
RING18 = ["butterfly", "eye", "moon", "key", "flower", "star", "snake", "tiger", "crown",
          "mirror", "compass", "scales", "hourglass", "arch", "candle", "hands", "skull", "cloud_eye"]

GRID20 = ["butterfly", "eye", "moon", "key", "flower", "star", "snake", "tiger", "crown", "mirror",
          "compass", "scales", "hourglass", "arch", "candle", "hands", "skull", "cloud_eye", "wand", "book"]

GRID25 = ["crown", "eye", "butterfly", "moon", "compass",
          "key", "flower", "star", "snake", "tiger",
          "mirror", "scales", "heart", "hourglass", "arch",
          "hands", "candle", "skull", "cloud_eye", "wand",
          "book", "eye_tears", "scissors", "unicorn", "question"]

CARDS6 = [("tiger", "FEARLESS"), ("scissors", "LET GO"), ("butterfly", "BECOME"),
          ("eye", "SEE CLEARLY"), ("flower", "CREATE"), ("unicorn", "GET SHIT DONE")]


def s01a(t, W, H, P):
    im = bg(W, H, PAL["cream"], "paper_cream.jpg")
    d = ImageDraw.Draw(im)
    ink = PAL["berry"]
    lw = max(3, int(H * 0.0040))
    p = ease(t / 0.85)
    x0, y0, w, h = W * 0.08, H * 0.545, W * 0.84, H * 0.22
    pts = ecg_points(x0, y0, w, h, p)
    if len(pts) > 2:
        d.line(pts, fill=ink, width=lw, joint="curve")
        tip = pts[-1]
        rr = lw * 1.6
        d.ellipse([tip[0] - rr, tip[1] - rr, tip[0] + rr, tip[1] + rr], fill=ink)
    return camera(im, 1.0 + 0.02 * ease(t))


def s01b(t, W, H, P):
    im = bg(W, H, PAL["cream"], "paper_cream.jpg")
    d = ImageDraw.Draw(im)
    ink = PAL["berry"]
    p = ease(t / 1.8)
    hh = H * (0.10 + 0.22 * p) * (1.0 + 0.035 * math.sin(t * 2 * math.pi / 0.8))
    paste_sp(im, sprite("heart"), W * 0.5, H * 0.46, hh)
    # ECG line under the heart, fading
    q = max(0.0, 1.0 - t / 1.2)
    if q > 0.02:
        pts = ecg_points(W * 0.10, H * 0.845, W * 0.80, H * 0.10, 1.0)
        d.line(pts, fill=tuple(int(c * q) for c in ink), width=max(3, int(H * 0.0032)), joint="curve")
    if t > 1.2:
        f = font("serif", int(H * 0.050))
        a = ease((t - 1.2) / 0.5)
        text_tracked(d, W * 0.5, H * 0.865, "EVERYTHING MEANS SOMETHING.", f,
                     PAL["brand_plum"], tracking=0.10, alpha=a)
    return camera(im, 1.02 - 0.04 * ease(t / 2.6))


def s02a(t, W, H, P):
    im = bg(W, H, PAL["cream"], "paper_cream.jpg")
    d = ImageDraw.Draw(im)
    pulse = 1.0 + 0.03 * math.sin(t * 2 * math.pi / 0.7)
    paste_sp(im, sprite("heart"), W * 0.5, H * 0.47, H * 0.30 * pulse)
    # crack: berry line + cream offset to suggest split
    p = ease(t / 0.35)
    cx, cy = W * 0.5, H * 0.47
    crack = [(cx - W * 0.03, cy + H * 0.02), (cx + W * 0.01, cy + H * 0.06),
             (cx - W * 0.02, cy + H * 0.10), (cx + W * 0.03, cy + H * 0.14)]
    upto = int(len(crack) * p)
    if upto > 1:
        d.line(crack[:upto], fill=PAL["berry"], width=max(3, int(H * 0.0050)), joint="curve")
    # symbols peeking
    peeks = [("butterfly", -0.05, 0.05, -15), ("key", 0.05, 0.02, 10),
             ("moon", -0.08, 0.10, 20), ("eye", 0.09, 0.08, -8)]
    for name, dx, dy, rot in peeks:
        e = eout(max(0.0, min(1.0, (t - 0.3) / 0.6)))
        paste_sp(im, sprite(name), cx + W * 0.5 * dx * e, cy + H * 0.5 * dy * e,
                 H * 0.085 * e, alpha=e, rot=rot)
    return camera(im, 1.0 + 0.03 * ease(t / 2.2))


def ring_positions(W, H, t, appear_from=9.0):
    cx, cy = W * 0.5, H * 0.50
    R = min(W, H) * 0.33
    out = []
    n = len(RING18)
    for i, name in enumerate(RING18):
        a = -math.pi / 2 + i * 2 * math.pi / n
        floatx = math.sin(t * 1.0 + i * 1.7) * W * 0.002
        floaty = math.cos(t * 1.3 + i * 2.1) * H * 0.003
        out.append((name, cx + R * math.cos(a) + floatx, cy + R * math.sin(a) * 0.92 + floaty))
    return out


def s02b(t, W, H, P):
    im = bg(W, H, PAL["cream"], "paper_cream.jpg")
    heart_h = H * (0.30 - 0.10 * ease(t / 3.8))
    paste_sp(im, sprite("heart"), W * 0.5, H * 0.50, heart_h, alpha=max(0.35, 1 - 0.4 * ease(t / 3.8)))
    n = len(RING18)
    for i, (name, x, y) in enumerate(ring_positions(W, H, t, 6.2)):
        lt = (t - 6.2) - i * 0.12
        if lt <= 0:
            continue
        e = eout(min(1.0, lt / 0.45))
        hh = H * 0.078
        # emerge from the heart
        hx, hy = W * 0.5, H * 0.50
        cx = hx + (x - hx) * e
        cy = hy + (y - hy) * e
        paste_sp(im, sprite(name), cx, cy, hh * (0.6 + 0.4 * e), alpha=e)
    return camera(im, 1.10 - 0.10 * ease(t / 3.8))


def s03(t, W, H, P):
    im = bg(W, H, PAL["cream"], "paper_cream.jpg")
    d = ImageDraw.Draw(im)
    cols, rows = 5, 5
    # a faint structural circle so the grid reads as a "world", not a contact sheet
    cx, cy = W * 0.5, H * 0.50
    d.ellipse([cx - H * 0.40, cy - H * 0.40, cx + H * 0.40, cy + H * 0.40],
              outline=PAL["blush"], width=max(2, int(H * 0.0016)))
    for i, name in enumerate(GRID25):
        r, c = divmod(i, cols)
        x = W * (0.145 + 0.71 * c / (cols - 1))
        y = H * (0.18 + 0.64 * r / (rows - 1))
        # one symbol micro-moves every 0.8s
        slot = int(t / 0.8)
        dx = dy = 0.0
        if (i * 7) % 25 == slot % 25:
            dx = math.sin(t * 6.0) * W * 0.004
            dy = math.cos(t * 5.0) * H * 0.004
        hh = H * (0.105 if name == "heart" else 0.092)
        paste_sp(im, sprite(name), x + dx, y + dy, hh)
    f = font("serif", int(H * 0.040))
    if 4.5 < t < 6.0:
        a = min(1.0, (t - 4.5) / 0.3) * min(1.0, (6.0 - t) / 0.3)
        text_tracked(d, W * 0.5, H * 0.925, "A WORLD OF SYMBOLS.", f, PAL["brand_plum"],
                     tracking=0.12, alpha=a)
    return camera(im, 1.08 - 0.06 * ease(t / 4.5) - 0.02 * ease(max(0, t - 4.5) / 1.5))


def s04a(t, W, H, P):
    im = bg(W, H, PAL["cream"], "paper_cream.jpg")
    d = ImageDraw.Draw(im)
    cx, cy = W * 0.5, H * 0.52
    cols, rows = 4, 5
    n = len(GRID20)
    for i, name in enumerate(GRID20):
        r, c = divmod(i, cols)
        x0 = W * (0.14 + 0.72 * c / (cols - 1))
        y0 = H * (0.20 + 0.60 * r / (rows - 1))
        order = (rows - r) + abs(c - (cols - 1) / 2.0) * 0.6
        st = order * 0.10
        lt = (t - st) / 0.45
        if lt >= 1.0:
            continue
        if lt <= 0:
            paste_sp(im, sprite(name), x0, y0, H * 0.085)
            continue
        e = ease(lt)
        x = lerp(x0, cx, e)
        y = lerp(y0, cy, e)
        hh = lerp(H * 0.085, H * 0.006, e)
        paste_sp(im, sprite(name), x, y, hh, alpha=1 - e * 0.7)
    # ink core
    p = ease(max(0.0, t - 1.4) / 0.8)
    if p > 0.01:
        rr = H * 0.012 * (0.3 + p) * (1 + 0.15 * math.sin(t * 20))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=PAL["berry"])
    return camera(im, 1.0 + 0.12 * ease(max(0, t - 1.0) / 1.2))


def s04b(t, W, H, P):
    im = bg(W, H, PAL["cream"], "paper_cream.jpg")
    d = ImageDraw.Draw(im)
    h = H * (0.55 + 0.05 * ease(t / 2.8))
    card = blank_card(h)
    # unfold 0.5s then flip
    if t < 0.5:
        e = eout(t / 0.5)
        s = card.resize((max(2, int(card.width * e)), card.height), Image.LANCZOS)
        im.paste(s, (int(W * 0.5 - s.width / 2), int(H * 0.52 - s.height / 2)), s)
    elif t < 1.2:
        e = ease((t - 0.5) / 0.7)
        sx = abs(math.cos(math.pi * e))
        s = card.resize((max(2, int(card.width * sx)), card.height), Image.LANCZOS)
        im.paste(s, (int(W * 0.5 - s.width / 2), int(H * 0.52 - s.height / 2)), s)
    else:
        paste_sp(im, card, W * 0.5, H * 0.52, h, rot=0)
    if t > 2.2:
        # 6 slot markers
        for k in range(6):
            x = W * (0.30 + 0.08 * k)
            d.ellipse([x - W * 0.006, H * 0.755, x + W * 0.006, H * 0.768],
                      outline=PAL["berry"], width=2)
    if t > 1.0:
        f = font("serif", int(H * 0.040))
        a = ease((t - 1.0) / 0.5) * (1.0 - ease(max(0, t - 2.4) / 0.4)) if t < 2.8 else 0
        if a > 0.02:
            text_tracked(d, W * 0.5, H * 0.885, "THE DECK", f, PAL["brand_plum"], tracking=0.14, alpha=a)
    return camera(im, 1.02 - 0.02 * ease(t / 2.8))


def s05(t, W, H, P, idx):
    """idx 0..5 card draw shot."""
    name, label = CARDS6[idx]
    im = bg(W, H, PAL["cream"], "paper_cream.jpg")
    d = ImageDraw.Draw(im)
    h = H * (0.52 if W > H else 0.46)
    card = m1_card(name, h, label)
    # entry motion per card
    e = eout(min(1.0, t / 0.45))
    if idx == 0:      # slide up from bottom
        y = H * (0.52 + 0.18 * (1 - e))
        x = W * 0.5
        rot = -2.0 * (1 - e)
    elif idx == 1:    # mask reveal: fade + slight scale
        y = H * 0.52
        x = W * 0.5
        rot = 0
    elif idx == 2:    # slide from right
        x = W * (0.5 + 0.35 * (1 - e))
        y = H * 0.52
        rot = 0
    elif idx == 3:    # pop
        y = H * 0.52
        x = W * 0.5
        rot = 0
    elif idx == 4:    # slide from left
        x = W * (0.5 - 0.35 * (1 - e))
        y = H * 0.52
        rot = 0
    else:             # settle from below
        y = H * (0.52 + 0.10 * (1 - e))
        x = W * 0.5
        rot = 1.5 * (1 - e)
    scale = 1.0 + 0.02 * math.sin(math.pi * min(1.0, t / 0.8))
    paste_sp(im, card, x, y, h * scale, rot=rot)
    # subtle paper grain flash at cut
    return camera(im, 1.01 + 0.01 * ease(t / 1.5))


def s06a(t, W, H, P):
    im = bg(W, H, PAL["env_black"], "paper_env_black.jpg", grain=0.12)
    names = ["eye", "heart", "butterfly", "tiger", "crown", "key"]
    for i, name in enumerate(names):
        a = max(0.0, min(1.0, (t - i * 0.12) / 0.35))
        hh = H * 0.05
        x = W * (0.30 + 0.08 * (i % 3))
        y = H * (0.42 + 0.12 * (i // 3))
        paste_sp(im, sprite(name), x, y, hh, alpha=a * 0.9, tint=PAL["bone"])
    # fade to white point at the end
    p = ease(max(0.0, t - 1.2) / 0.3)
    if p > 0.01:
        im = Image.blend(im, bg(W, H, PAL["cream"]), p * 0.35)
        d = ImageDraw.Draw(im)
        rr = H * 0.012 * (0.2 + p)
        d.ellipse([W * 0.5 - rr, H * 0.5 - rr, W * 0.5 + rr, H * 0.5 + rr], fill=PAL["cream"])
    return camera(im, 1.0 + 0.005 * ease(t / 1.5))


RING12 = ["eye", "heart", "butterfly", "flower", "tiger", "crown",
          "key", "mirror", "compass", "moon", "star", "hourglass"]


def gold_mandala(im, d, W, H, t, shrink=1.0, tint_col=None, ring_alpha=1.0):
    col = tint_col or PAL["gold"]
    cx, cy = W * 0.5, H * 0.48
    Rh = min(W, H) * 0.40 * shrink
    # double frame
    pad = H * 0.055 * shrink
    d.rectangle([pad, pad, W - pad, H - pad], outline=col, width=max(1, int(H * 0.0035)))
    pad2 = pad + H * 0.022 * shrink
    d.rectangle([pad2, pad2, W - pad2, H - pad2], outline=col, width=max(1, int(H * 0.0018)))
    # centre ring
    r0 = Rh * 0.42
    d.ellipse([cx - r0, cy - r0, cx + r0, cy + r0], outline=col, width=max(1, int(H * 0.0028)))
    # 12 symbols on the ring
    n = len(RING12)
    for i, name in enumerate(RING12):
        a = -math.pi / 2 + i * 2 * math.pi / n
        x = cx + Rh * math.cos(a)
        y = cy + Rh * math.sin(a)
        appear = eout(max(0.0, min(1.0, (t - 4.5 - i * 0.10) / 0.5)))
        if appear <= 0:
            continue
        hh = H * 0.052 * shrink * (0.7 + 0.3 * appear)
        paste_sp(im, sprite(name), lerp(cx, x, appear), lerp(cy, y, appear), hh,
                 alpha=ring_alpha * appear, tint=col)


def s06b(t, W, H, P):
    im = bg(W, H, PAL["rose"], "paper_rose.jpg")
    d = ImageDraw.Draw(im)
    gold_mandala(im, d, W, H, t, ring_alpha=1.0)
    return camera(im, 1.0 + 0.035 * ease(t / 4.5))


MORPH = [("butterfly", 0.00, 0.90), ("flower", 0.80, 1.70), ("heart", 1.60, 2.50),
         ("crown", 2.40, 3.20), ("eye", 3.10, 4.00)]


def s06c(t, W, H, P):
    im = bg(W, H, PAL["rose"], "paper_rose.jpg")
    d = ImageDraw.Draw(im)
    gold_mandala(im, d, W, H, 99, ring_alpha=1.0)
    cx, cy = W * 0.5, H * 0.48
    for name, a0, a1 in MORPH:
        if t < a0 - 0.25 or t > a1 + 0.25:
            continue
        if t < a0:
            alpha = 0.0
        elif t < a0 + 0.35:
            alpha = (t - a0) / 0.35
        elif t < a1 - 0.25:
            alpha = 1.0
        else:
            alpha = max(0.0, (a1 + 0.25 - t) / 0.5)
        if alpha <= 0.01:
            continue
        hh = H * (0.16 + 0.012 * math.sin(t * 3))
        paste_sp(im, sprite(name), cx, cy, hh, alpha=min(1.0, alpha), tint=PAL["gold"])
    # second inner ring at 3.5s
    if t > 3.5:
        a = ease((t - 3.5) / 0.5)
        r = min(W, H) * 0.40 * 0.30
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=PAL["gold"],
                  width=max(1, int(H * 0.0022 * a)))
    if t > 2.5:
        f = font("serif", int(H * 0.050))
        a = ease((t - 2.5) / 0.4)
        text_tracked(d, W * 0.5, H * 0.775, "BECOME.", f, PAL["white"], tracking=0.14, alpha=a)
    return camera(im, 1.0 + 0.03 * ease(t / 4.0))


def s07a(t, W, H, P):
    # cross-fade rose -> page white during the shot
    p = ease(clamp01((t - 0.9) / 0.7))
    base = bg(W, H, PAL["rose"], "paper_rose.jpg")
    if p > 0:
        white = bg(W, H, PAL["page_white"], "paper_page_white.jpg")
        base = Image.blend(base, white, p)
    d = ImageDraw.Draw(base)
    shrink = 1.0 - 0.72 * ease(min(1.0, t / 1.1))
    col = mix(PAL["gold"], PAL["brand_plum"], ease(clamp01((t - 0.5) / 0.8)))
    gold_mandala(base, d, W, H, 99, shrink=max(0.26, shrink), tint_col=col, ring_alpha=1.0)
    # emblem: heart at centre
    if shrink > 0.3:
        paste_sp(base, sprite("heart"), W * 0.5, H * 0.48, H * 0.13 * shrink * 1.4, tint=col)
    return camera(base, 1.0 - 0.06 * ease(t / 2.0))


def clamp01(x):
    return max(0.0, min(1.0, x))


def s07b(t, W, H, P):
    im = bg(W, H, PAL["page_white"], "paper_page_white.jpg", grain=0.16)
    d = ImageDraw.Draw(im)
    f = font("serif", int(H * 0.085))
    a1 = ease(max(0.0, (t - 0.3) / 0.35))
    if a1 > 0.01:
        # rules
        tw = 0
        for ch in "NOT TAROT":
            tw += d.textlength(ch, font=f) + f.size * 0.16
        y = H * 0.44
        text_tracked(d, W * 0.5, y, "NOT TAROT", f, PAL["brand_plum"], tracking=0.16, alpha=a1)
        d.line([(W * 0.5 - tw / 2, y - H * 0.020), (W * 0.5 + tw / 2, y - H * 0.020)],
               fill=tuple(int(c * a1) for c in PAL["brand_plum"]), width=max(1, int(H * 0.0030)))
        d.line([(W * 0.5 - tw / 2, y + f.size * 1.18), (W * 0.5 + tw / 2, y + f.size * 1.18)],
               fill=int_alpha(PAL["brand_plum"], a1), width=max(1, int(H * 0.0016)))
    a2 = ease(max(0.0, (t - 1.0) / 0.35))
    if a2 > 0.01:
        f2 = font("serif", int(H * 0.030))
        text_tracked(d, W * 0.5, H * 0.585, "MAKE YOUR OWN MEANING.", f2,
                     PAL["brand_plum"], tracking=0.12, alpha=a2)
    # micro grain breathing
    return im


def int_alpha(c, a):
    return tuple(int(round(v * a)) for v in c)


# ---------------------------------------------------------------- timeline
SHOTS = [
    ("S01a", 0.0, 1.4, s01a), ("S01b", 1.4, 4.0, s01b),
    ("S02a", 4.0, 6.2, s02a), ("S02b", 6.2, 10.0, s02b),
    ("S03", 10.0, 16.0, s03),
    ("S04a", 16.0, 18.2, s04a), ("S04b", 18.2, 21.0, s04b),
    ("S05a", 21.0, 22.5, lambda t, W, H, P: s05(t, W, H, P, 0)),
    ("S05b", 22.5, 24.0, lambda t, W, H, P: s05(t, W, H, P, 1)),
    ("S05c", 24.0, 25.5, lambda t, W, H, P: s05(t, W, H, P, 2)),
    ("S05d", 25.5, 27.0, lambda t, W, H, P: s05(t, W, H, P, 3)),
    ("S05e", 27.0, 28.5, lambda t, W, H, P: s05(t, W, H, P, 4)),
    ("S05f", 28.5, 30.0, lambda t, W, H, P: s05(t, W, H, P, 5)),
    ("S06a", 30.0, 31.5, s06a),
    ("S06b", 31.5, 36.0, s06b),
    ("S06c", 36.0, 40.0, s06c),
    ("S07a", 40.0, 42.0, s07a),
    ("S07b", 42.0, 45.0, s07b),
]


def shot_at(t):
    for sid, a, b, fn in SHOTS:
        if a <= t < b:
            return sid, fn, t - a, b - a
    sid, a, b, fn = SHOTS[-1]
    return sid, fn, b - a, b - a


def frame(t, W, H, fmt):
    sid, fn, lt, dur = shot_at(t)
    im = fn(lt, W, H, P=(t, dur))
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
    return im.convert("RGB")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "kf"
    if mode == "kf":
        os.makedirs(KF, exist_ok=True)
        reps = {"S01a": 0.9, "S01b": 2.4, "S02a": 1.4, "S02b": 2.6, "S03": 3.0,
                "S04a": 1.4, "S04b": 1.9, "S05a": 0.9, "S05b": 0.7, "S05c": 0.7,
                "S05d": 0.7, "S05e": 0.8, "S05f": 0.9, "S06a": 0.8, "S06b": 2.6,
                "S06c": 2.0, "S07a": 1.2, "S07b": 1.8}
        for sid, a, b, fn in SHOTS:
            lt = reps[sid]
            im = frame(a + lt, 1920, 1080, "16x9")
            p = os.path.join(KF, sid + "_keyframe.png")
            im.save(p)
            print("kf", p)
    elif mode == "frames":
        fmt = sys.argv[2] if len(sys.argv) > 2 else "16x9"
        W, H = (1280, 720) if fmt == "16x9" else (720, 1280)
        out = os.path.join(RENDER, "frames_" + fmt)
        os.makedirs(out, exist_ok=True)
        for i in range(TOTAL):
            t = i / float(FPS)
            frame(t, W, H, fmt).save(os.path.join(out, "frame_%05d.jpg" % (i + 1)), quality=90)
            if (i + 1) % 60 == 0:
                print(fmt, i + 1, "/", TOTAL, flush=True)
    else:
        print("unknown mode", mode)


if __name__ == "__main__":
    main()
