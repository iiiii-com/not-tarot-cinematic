# -*- coding: utf-8 -*-
"""
Build symbol sprites for the 45s director-cut animatic.

1. Extract line-art sprites from the seven reference-derived card crops.
   (alpha = ink darkness; color = berry/crimson line art)
2. Draw the symbols that do not exist as reference art with the same
   single-weight line language (key, flower, star, snake, hourglass, arch,
   candle, scissors).
3. Save transparent RGBA PNGs + a contact sheet for QA.

Output: 03_assets/symbols/sprites/*.png
        ../../03_assets/symbols/sprites/sprites_contact_sheet.png  (same dir)
"""
import os
from PIL import Image, ImageDraw, ImageFilter

ROOT = r"E:\deepseek\PROJECT_MYSTIC_PROMO"
CARDS = os.path.join(ROOT, "03_assets", "cards")
OUT = os.path.join(ROOT, "03_assets", "symbols", "sprites")
os.makedirs(OUT, exist_ok=True)

BERRY = (143, 44, 59)
CRIMSON = (176, 31, 56)

# name -> (card file, y-bottom fraction of the art area, ink colour)
CARD_SOURCES = {
    "heart":           ("m1_02_band_aid_whisperer.png", 0.78, BERRY, 132),
    "eye":             ("m1b_12_dont_give_a_fuck.png", 0.78, BERRY, 132),
    "eye_tears":       ("m1b_06_tears_are_power.png", 0.78, BERRY, 140),
    "butterfly":       ("m1_10_bruised_not_broken.png", 0.78, BERRY, 132),
    "tiger":           ("m1_08_fearless.png", 0.78, BERRY, 140),
    "unicorn":         ("m1_07_get_shit_done.png", 0.78, BERRY, 140),
    "crown":           ("m1_03_ceo_babe.png", 0.78, BERRY, 140),
    "mirror":          ("m1_01_imagination_guru.png", 0.78, BERRY, 140),
    "compass":         ("m1_05_no_gps_lost_forever.png", 0.78, BERRY, 150),
    "hands":           ("m1_06_namaste_bitches.png", 0.78, BERRY, 150),
    "wand":            ("m1_04_wish_fulfilling_wizard.png", 0.78, BERRY, 140),
    "skull":           ("m1b_02_waiting_for_gold.png", 0.76, BERRY, 180),
    "moon":            ("m1b_04_retrograde_realness.png", 0.78, BERRY, 185),
    "cloud_eye":       ("m1b_03_end_of_drama.png", 0.78, BERRY, 175),
    "scales":          ("m1b_09_karma_is_a_bitch.png", 0.78, BERRY, 175),
    "question":        ("m1b_10_curiosity_unleashed.png", 0.78, BERRY, 175),
    "book":            ("m1_12_heavenly_insights.png", 0.78, BERRY, 140),
}


def extract(path, y_frac, ink, pad=6, thresh=132):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    im = im.crop((int(w * 0.05), int(h * 0.02), int(w * 0.95), int(h * y_frac)))
    px = im.load()
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    mp = mask.load()
    minx, miny, maxx, maxy = w, h, 0, 0
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            lum = (r * 299 + g * 587 + b * 114) // 1000
            sat = max(r, g, b) - min(r, g, b)
            if lum < thresh and sat > 30:
                a = 255 if lum < 80 else int(255 * (thresh - lum) / (thresh - 80))
                mp[x, y] = a
                if a > 40:
                    if x < minx: minx = x
                    if y < miny: miny = y
                    if x > maxx: maxx = x
                    if y > maxy: maxy = y
    if maxx <= minx or maxy <= miny:
        raise SystemExit("empty mask for " + path)
    minx = max(0, minx - pad); miny = max(0, miny - pad)
    maxx = min(w - 1, maxx + pad); maxy = min(h - 1, maxy + pad)
    mask = mask.crop((minx, miny, maxx + 1, maxy + 1))
    # strip straight frame lines (card panel borders) captured near the edges
    import numpy as np
    arr = np.array(mask).astype(np.float32)
    def longest_run(v):
        best = cur = 0
        for x in v:
            cur = cur + 1 if x > 30 else 0
            if cur > best: best = cur
        return best
    hh, ww = arr.shape
    for y in range(hh):
        if longest_run(arr[y]) > 0.55 * ww:
            arr[y] = 0
    for x in range(ww):
        if longest_run(arr[:, x]) > 0.55 * hh:
            arr[:, x] = 0
    def strip(edge):
        nonlocal arr
        guard = 0
        while guard < 60:
            if edge == 'top' and arr.shape[0] > 16 and arr[0].mean() > 150: arr = arr[1:]; guard += 1; continue
            if edge == 'bottom' and arr.shape[0] > 16 and arr[-1].mean() > 150: arr = arr[:-1]; guard += 1; continue
            if edge == 'left' and arr.shape[1] > 16 and arr[:,0].mean() > 150: arr = arr[:,1:]; guard += 1; continue
            if edge == 'right' and arr.shape[1] > 16 and arr[:,-1].mean() > 150: arr = arr[:,:-1]; guard += 1; continue
            break
    for edge in ('top','bottom','left','right'):
        strip(edge)
    mask = Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
    # colourise
    out = Image.new("RGBA", mask.size, ink + (255,))
    out.putalpha(mask)
    return out


# ---------------------------------------------------------------- procedural
def _canvas(h, ss=4):
    return Image.new("RGBA", (h * ss, h * ss), (0, 0, 0, 0)), ss


def _finish(im, ss):
    w, h = im.size
    return im.resize((max(2, w // ss), max(2, h // ss)), Image.LANCZOS)


def make_key(ink=BERRY, h=400):
    ss = 4
    im = Image.new("RGBA", (int(h * 0.42) * ss, h * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    W, H = im.size
    lw = max(2, int(W * 0.016))
    # bow (ring)
    r = W * 0.20
    cx, cy = W * 0.5, r * 1.35
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ink + (255,), width=lw)
    d.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45], outline=ink + (255,), width=lw)
    # shaft
    d.line([(cx, cy + r), (cx, H * 0.92)], fill=ink + (255,), width=lw)
    # teeth
    d.line([(cx, H * 0.78), (cx + W * 0.22, H * 0.78)], fill=ink + (255,), width=lw)
    d.line([(cx, H * 0.88), (cx + W * 0.16, H * 0.88)], fill=ink + (255,), width=lw)
    d.line([(cx + W * 0.22, H * 0.78), (cx + W * 0.22, H * 0.83)], fill=ink + (255,), width=lw)
    return _finish(im, ss)


def make_flower(ink=BERRY, h=400):
    ss = 4
    im = Image.new("RGBA", (h * ss, h * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    W, H = im.size
    lw = max(2, int(W * 0.012))
    cx, cy = W * 0.5, H * 0.36
    R = W * 0.22
    # rose spiral
    pts = []
    for i in range(0, 260):
        t = i / 260.0
        a = t * 5.2 * 3.14159
        rr = R * (0.16 + 0.84 * t)
        pts.append((cx + rr * 1.06 * __import__("math").cos(a),
                    cy + rr * 0.92 * __import__("math").sin(a)))
    d.line(pts, fill=ink + (255,), width=lw, joint="curve")
    # outer petals
    for k in range(6):
        a = k * 3.14159 / 3 + 0.3
        px, py = cx + R * 1.28 * __import__("math").cos(a), cy + R * 1.2 * __import__("math").sin(a)
        d.arc([px - R * 0.55, py - R * 0.55, px + R * 0.55, py + R * 0.55],
              int(a * 57.3) - 60, int(a * 57.3) + 120, fill=ink + (255,), width=lw)
    # stem + leaves
    d.line([(cx, cy + R * 1.25), (cx + W * 0.02, H * 0.94)], fill=ink + (255,), width=lw)
    for side, yy in ((-1, 0.62), (1, 0.78)):
        d.arc([cx + side * W * 0.02 - W * 0.13, H * yy - H * 0.05,
               cx + side * W * 0.02 + W * 0.13, H * yy + H * 0.05],
              200, 340, fill=ink + (255,), width=lw)
    return _finish(im, ss)


def make_star(ink=BERRY, h=400):
    ss = 4
    im = Image.new("RGBA", (h * ss, h * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    W, H = im.size
    cx, cy, R, r = W * 0.5, H * 0.5, W * 0.40, W * 0.10
    lw = max(2, int(W * 0.012))
    pts = []
    for i in range(8):
        a = -3.14159 / 2 + i * 3.14159 / 4
        rr = R if i % 2 == 0 else r
        pts.append((cx + rr * __import__("math").cos(a), cy + rr * __import__("math").sin(a)))
    d.line(pts + [pts[0]], fill=ink + (255,), width=lw, joint="curve")
    return _finish(im, ss)


def make_snake(ink=BERRY, h=400):
    ss = 4
    im = Image.new("RGBA", (int(h * 0.62 * ss), h * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    W, H = im.size
    lw = max(2, int(W * 0.030))
    import math
    pts = []
    for i in range(90):
        t = i / 89.0
        x = W * 0.18 + W * 0.14 * math.sin(t * 5.4 * 3.14159)
        y = H * (0.90 - 0.78 * t)
        pts.append((x, y))
    d.line(pts, fill=ink + (255,), width=lw, joint="curve")
    # head
    hx, hy = pts[-1]
    d.ellipse([hx - lw * 1.5, hy - lw * 1.6, hx + lw * 1.7, hy + lw * 1.4], outline=ink + (255,), width=lw)
    d.ellipse([hx + lw * 0.2, hy - lw * 0.8, hx + lw * 0.7, hy - lw * 0.3], fill=ink + (255,))
    d.line([(hx + lw * 1.6, hy + lw * 0.1), (hx + lw * 2.4, hy - lw * 0.1)], fill=ink + (255,), width=lw)
    return _finish(im, ss)


def make_hourglass(ink=BERRY, h=400):
    ss = 4
    im = Image.new("RGBA", (int(h * 0.62 * ss), h * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    W, H = im.size
    lw = max(2, int(W * 0.022))
    top = [(W * 0.12, H * 0.10), (W * 0.88, H * 0.10), (W * 0.52, H * 0.50), (W * 0.12, H * 0.10)]
    d.line(top, fill=ink + (255,), width=lw, joint="curve")
    d.line([(W * 0.12, H * 0.90), (W * 0.88, H * 0.90)], fill=ink + (255,), width=lw)
    d.line([(W * 0.12, H * 0.10), (W * 0.12, H * 0.90)], fill=ink + (255,), width=lw)
    d.line([(W * 0.88, H * 0.10), (W * 0.88, H * 0.90)], fill=ink + (255,), width=lw)
    # sand cone (hatched)
    for k in range(1, 6):
        yy = H * (0.50 + 0.075 * k)
        half = (W * 0.40) * (k / 6.0)
        d.line([(W * 0.5 - half, yy), (W * 0.5 + half, yy)], fill=ink + (180,), width=max(2, lw - 1))
    # falling grain
    d.line([(W * 0.5, H * 0.50), (W * 0.5, H * 0.60)], fill=ink + (255,), width=lw)
    return _finish(im, ss)


def make_arch(ink=BERRY, h=400):
    ss = 4
    im = Image.new("RGBA", (int(h * 0.68 * ss), h * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    W, H = im.size
    lw = max(2, int(W * 0.024))
    d.arc([W * 0.10, H * 0.08, W * 0.90, H * 0.62], 180, 360, fill=ink + (255,), width=lw)
    d.line([(W * 0.10, H * 0.35), (W * 0.10, H * 0.94)], fill=ink + (255,), width=lw)
    d.line([(W * 0.90, H * 0.35), (W * 0.90, H * 0.94)], fill=ink + (255,), width=lw)
    d.arc([W * 0.20, H * 0.16, W * 0.80, H * 0.56], 180, 360, fill=ink + (255,), width=lw)
    # keystone
    d.line([(W * 0.5, H * 0.08), (W * 0.5, H * 0.17)], fill=ink + (255,), width=lw)
    # threshold shadow lines
    for k in range(3):
        inset = W * (0.16 + 0.03 * k)
        d.line([(inset, H * 0.94 - k * H * 0.02), (W - inset, H * 0.94 - k * H * 0.02)],
               fill=ink + (120,), width=max(2, lw - 1))
    return _finish(im, ss)


def make_candle(ink=BERRY, h=400):
    ss = 4
    im = Image.new("RGBA", (int(h * 0.46 * ss), h * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    W, H = im.size
    lw = max(2, int(W * 0.030))
    # body
    d.line([(W * 0.32, H * 0.40), (W * 0.32, H * 0.86), (W * 0.68, H * 0.86), (W * 0.68, H * 0.40),
            (W * 0.32, H * 0.40)], fill=ink + (255,), width=lw, joint="curve")
    # drips
    for x, y2 in ((W * 0.36, H * 0.52), (W * 0.63, H * 0.47)):
        d.line([(x, H * 0.40), (x, y2)], fill=ink + (255,), width=max(2, lw - 1))
        d.ellipse([x - lw, y2 - lw, x + lw, y2 + lw], outline=ink + (255,), width=max(2, lw - 2))
    # wick + flame
    d.line([(W * 0.5, H * 0.40), (W * 0.5, H * 0.30)], fill=ink + (255,), width=lw)
    d.arc([W * 0.34, H * 0.10, W * 0.66, H * 0.34], 20, 250, fill=ink + (255,), width=lw)
    # holder
    d.line([(W * 0.22, H * 0.86), (W * 0.78, H * 0.86)], fill=ink + (255,), width=lw)
    d.ellipse([W * 0.18, H * 0.86, W * 0.82, H * 0.94], outline=ink + (255,), width=lw)
    return _finish(im, ss)


def make_scissors(ink=BERRY, h=400):
    ss = 4
    im = Image.new("RGBA", (int(h * 0.62 * ss), h * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    W, H = im.size
    lw = max(2, int(W * 0.024))
    # blades: two long thin shapes from pivot
    px, py = W * 0.5, H * 0.62
    for s in (-1, 1):
        d.line([(px, py), (W * 0.5 + s * W * 0.34, H * 0.08 + (0.04 if s > 0 else 0) * H)],
               fill=ink + (255,), width=lw)
        d.line([(px, py), (W * 0.5 + s * W * 0.10, H * 0.08)], fill=ink + (255,), width=lw)
    # finger rings
    d.ellipse([W * 0.30, H * 0.68, W * 0.44, H * 0.86], outline=ink + (255,), width=lw)
    d.ellipse([W * 0.56, H * 0.68, W * 0.70, H * 0.86], outline=ink + (255,), width=lw)
    # pivot
    d.ellipse([px - lw * 1.6, py - lw * 1.6, px + lw * 1.6, py + lw * 1.6], fill=ink + (255,))
    # sliver hatching on blades
    for k in range(4):
        yy = H * (0.18 + 0.09 * k)
        d.line([(W * 0.5 - W * 0.10, yy), (W * 0.5 - W * 0.03, yy + H * 0.02)],
               fill=ink + (110,), width=max(2, lw - 2))
    return _finish(im, ss)


PROC = {
    "key": make_key,
    "flower": make_flower,
    "star": make_star,
    "snake": make_snake,
    "hourglass": make_hourglass,
    "arch": make_arch,
    "candle": make_candle,
    "scissors": make_scissors,
}


def main():
    made = {}
    for name, (fn, y_frac, ink, thresh) in CARD_SOURCES.items():
        try:
            sp = extract(os.path.join(CARDS, fn), y_frac, ink, thresh=thresh)
            sp.save(os.path.join(OUT, name + ".png"))
            made[name] = sp
            print("extracted", name, sp.size)
        except Exception as e:  # noqa
            print("FAILED", name, e)
    for name, fn in PROC.items():
        sp = fn()
        sp.save(os.path.join(OUT, name + ".png"))
        made[name] = sp
        print("drawn   ", name, sp.size)

    # contact sheet: sprites tinted berry on cream
    cols, cell = 7, 300
    rows = (len(made) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * cell), (250, 242, 236))
    d = ImageDraw.Draw(sheet)
    for i, (name, sp) in enumerate(made.items()):
        s = sp.copy()
        hh = int(cell * 0.72)
        ww = max(1, int(s.width * hh / s.height))
        s = s.resize((ww, hh), Image.LANCZOS)
        x = (i % cols) * cell + (cell - ww) // 2
        y = (i // cols) * cell + int(cell * 0.08)
        sheet.paste(s, (x, y), s)
        d.text(((i % cols) * cell + 10, (i // cols) * cell + cell - 26), name,
               fill=(143, 44, 59))
    sheet.save(os.path.join(OUT, "sprites_contact_sheet.png"))
    print("sheet:", os.path.join(OUT, "sprites_contact_sheet.png"), sheet.size)


if __name__ == "__main__":
    main()
