# -*- coding: utf-8 -*-
"""Concept v3 stills: direction A (6 frames) + direction B (1 plate) + transition sheet + contact sheet.

Uses cleaned extractions (icons floor 90, engraving floor 105) and paper textures.
Everything PIL, 1920x1080.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = r"E:/deepseek/PROJECT_MYSTIC_PROMO"
C3 = os.path.join(ROOT, "03_assets", "concept_v3")
M2 = os.path.join(C3, "motifs2")
TEX = os.path.join(ROOT, "03_assets", "textures")
os.makedirs(C3, exist_ok=True)

W, H = 1920, 1080
CREAM = (250, 242, 236)
INK = (20, 16, 15)
BERRY = (143, 44, 59)
GOLD = (123, 85, 33)
BONE = (247, 242, 230)
ROSE = (246, 183, 204)
PLUM = (36, 31, 34)
ENVBLACK = (11, 9, 8)

FD = "C:/Windows/Fonts/"
_fcache = {}

def font(name, size):
    key = (name, size)
    if key in _fcache:
        return _fcache[key]
    try:
        f = ImageFont.truetype(FD + name, size)
    except Exception:
        f = ImageFont.truetype(FD + "georgia.ttf", size)
    _fcache[key] = f
    return f

def serif(s): return font("georgia.ttf", s)
def serif_b(s): return font("georgiab.ttf", s)
def serif_i(s): return font("georgiai.ttf", s)
def sans(s): return font("arial.ttf", s)

def tracked_text(d, xy, s, f, fill, tracking=0.14, anchor="la", alpha=255):
    """Draw letter-spaced text. anchor: l/m/r + a/m/s/b (horizontal, vertical)."""
    if alpha < 255:
        fill = tuple(fill) + (int(alpha),)
    total = 0
    widths = []
    for ch in s:
        w = d.textlength(ch, font=f)
        widths.append(w)
    if len(s) > 1:
        total = sum(widths) + tracking * f.size * (len(s) - 1)
    else:
        total = sum(widths)
    x, y = xy
    if anchor[0] == "m": x -= total / 2
    elif anchor[0] == "r": x -= total
    asc, desc = f.getmetrics()
    hh = asc + desc
    if anchor[1] == "m": y -= hh / 2
    elif anchor[1] == "s": y -= hh
    for ch, w in zip(s, widths):
        d.text((x, y), ch, font=f, fill=fill)
        x += w + tracking * f.size
    return total

def paper(name, w, h, opacity=1.0, tint=None):
    p = os.path.join(TEX, "paper_%s.jpg" % name)
    im = Image.open(p).convert("RGB")
    im = ImageOps.fit(im, (w, h), method=Image.LANCZOS)
    if tint:
        t = Image.new("RGB", (w, h), tint)
        im = Image.blend(im, t, opacity)
    return im

def canvas(name, tint=None, opacity=1.0):
    return paper(name, W, H, opacity, tint).convert("RGBA")

def spr(name):
    raw = None
    for d in (M2, os.path.join(ROOT, "03_assets", "symbols", "sprites")):
        p = os.path.join(d, name + ".png")
        if os.path.exists(p):
            raw = Image.open(p).convert("RGBA")
            break
    if raw is None:
        raise FileNotFoundError(name)
    r, g, b, a = raw.split()
    arr = np.array(a, dtype=np.float32)
    if name.endswith("_bone"):
        arr = np.clip((arr - 35.0) * (255.0 / 215.0), 0, 255)
        return Image.merge("RGBA", (r, g, b, Image.fromarray(arr.astype(np.uint8), "L")))
    if name.startswith("eng_"):
        arr = np.clip((arr - 30.0) * (255.0 / 210.0), 0, 255)
        a2 = Image.fromarray(arr.astype(np.uint8), "L")
        ink = Image.new("RGBA", raw.size, INK + (255,))
        ink.putalpha(a2)
        return ink
    # icons: boost, kill card border by long-run removal, crop edges
    arr = np.clip((arr - 42.0) * 2.35, 0, 255)
    a2 = Image.fromarray(arr.astype(np.uint8), "L")
    aa = np.array(a2)
    for _ in range(2):
        for y in range(aa.shape[0]):
            row = aa[y] > 90
            if row.mean() > 0.72:
                aa[y] = 0
        for x in range(aa.shape[1]):
            col = aa[:, x] > 90
            if col.mean() > 0.72:
                aa[:, x] = 0
    a2 = Image.fromarray(aa, "L")
    bb = a2.point(lambda v: 255 if v > 8 else 0).getbbox()
    if bb:
        a2 = a2.crop(bb)
    w, h = a2.size
    cutx, cuty = int(w * 0.035), int(h * 0.03)
    a2 = a2.crop((cutx, cuty, w - cutx, h - cuty))
    bb = a2.point(lambda v: 255 if v > 8 else 0).getbbox()
    if bb:
        a2 = a2.crop(bb)
    ink = Image.new("RGBA", a2.size, INK + (255,))
    ink.putalpha(a2)
    return ink

def paste(base, im, cx, cy, h=None, w=None, rot=0.0, alpha=255, tint=None):
    if im is None: return
    im = im.copy()
    if tint:
        r, g, b, a = im.split()
        t = Image.new("RGBA", im.size, tint + (255,))
        t.putalpha(a)
        im = t
    if h:
        h = int(h)
        k = h / im.height
        im = im.resize((max(1, int(im.width * k)), h), Image.LANCZOS)
    elif w:
        w = int(w)
        k = w / im.width
        im = im.resize((w, max(1, int(im.height * k))), Image.LANCZOS)
    if rot:
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    if alpha < 255:
        a = im.split()[3].point(lambda v: int(v * alpha / 255))
        im.putalpha(a)
    base.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)

def hairline(d, x1, y1, x2, y2, fill, width=2, alpha=255):
    if alpha < 255: fill = fill + (alpha,)
    d.line([(x1, y1), (x2, y2)], fill=fill, width=width)

def ring(d, cx, cy, r, fill, width=2):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fill, width=width)

def ticks(d, x, y, n, step, vertical=False, fill=(140, 120, 105), length=(6, 14)):
    for i in range(n):
        L = length[1] if i % 5 == 0 else length[0]
        if vertical:
            d.line([(x, y + i * step), (x + L, y + i * step)], fill=fill, width=1)
        else:
            d.line([(x + i * step, y), (x + i * step, y + L)], fill=fill, width=1)

def micro(base, text, xy, color, size=17, tracking=0.18, anchor="la", alpha=255):
    d = ImageDraw.Draw(base)
    tracked_text(d, xy, text, sans(size), color, tracking, anchor, alpha)

def drop_shape(d, cx, cy, r, fill):
    pts = []
    for i in range(48):
        t = 2 * math.pi * i / 48
        # teardrop: pointed top
        x = r * math.sin(t) * (1 - 0.18 * max(0, -math.cos(t)))
        y = -r * 1.45 * math.cos(t) * (1 - 0.35 * max(0, -math.cos(t))) + r * 0.35
        pts.append((cx + x, cy + y))
    d.polygon(pts, fill=fill)

def vector_icon(im, kind, cx, cy, h):
    """Hand-drawn single-weight line icons for motifs not in the reference decks."""
    d = ImageDraw.Draw(im)
    col = INK
    w = 3
    if kind == "scissors":
        # handles
        d.ellipse([cx - 70, cy + h*0.30, cx - 10, cy + h*0.30 + 60], outline=col, width=w)
        d.ellipse([cx + 10, cy + h*0.30, cx + 70, cy + h*0.30 + 60], outline=col, width=w)
        # blades crossing up
        d.line([(cx - 46, cy + h*0.31), (cx + 40, cy - h*0.46)], fill=col, width=w)
        d.line([(cx + 46, cy + h*0.31), (cx - 40, cy - h*0.46)], fill=col, width=w)
        d.line([(cx - 40, cy - h*0.46), (cx - 30, cy - h*0.40)], fill=col, width=w)
        d.line([(cx + 40, cy - h*0.46), (cx + 30, cy - h*0.40)], fill=col, width=w)
        d.ellipse([cx - 6, cy + h*0.10, cx + 6, cy + h*0.10 + 12], fill=col)
    elif kind == "flower":
        # stem
        d.line([(cx, cy + h*0.46), (cx, cy + h*0.06)], fill=col, width=w)
        # leaves
        d.arc([cx - 60, cy + h*0.22, cx - 6, cy + h*0.34], 170, 350, fill=col, width=2)
        d.arc([cx + 6, cy + h*0.12, cx + 60, cy + h*0.24], 190, 10, fill=col, width=2)
        # 6 petals
        for i in range(6):
            a = i * math.pi / 3
            px = cx + 44 * math.cos(a)
            py = cy - h*0.20 + 44 * math.sin(a)
            d.ellipse([px - 26, py - 34, px + 26, py + 34], outline=col, width=2)
        d.ellipse([cx - 12, cy - h*0.20 - 12, cx + 12, cy - h*0.20 + 12], outline=col, width=2)

def thread(base, pts, color, width=2, alpha=255):
    d = ImageDraw.Draw(base)
    if alpha < 255: color = color + (alpha,)
    d.line(pts, fill=color, width=width, joint="curve")

def bezier(p0, p1, p2, p3, n=60):
    out = []
    for i in range(n + 1):
        t = i / n
        x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
        y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
        out.append((x, y))
    return out

def grain(base, amount=6):
    a = np.array(base.convert("RGB")).astype(np.int16)
    noise = np.random.default_rng(3).normal(0, amount, a.shape[:2])[:, :, None]
    a = np.clip(a + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(a).convert("RGBA")

def save(base, name):
    out = os.path.join(C3, name)
    base.convert("RGB").save(out, quality=94)
    print("saved", name)
    return out

# ------------------------------------------------------------------ A1 DROP
def a1():
    im = canvas("cream")
    d = ImageDraw.Draw(im)
    # left ruler
    ticks(d, 130, 140, 56, 15, vertical=True, fill=(180, 160, 145), length=(7, 18))
    hairline(d, 130, 140, 130, 980, (180, 160, 145), 1)
    # falling thread: vertical hairline down to the drop
    hairline(d, 960, 80, 960, 420, BERRY, 1, 120)
    # concentric target
    for r in (150, 260, 370):
        ring(d, 960, 500, r, BERRY, 1)
    ring(d, 960, 500, 92, BERRY, 1)
    # the drop
    drop_shape(d, 960, 460, 64, BERRY)
    d.ellipse([960 - 11, 460 - 11, 960 + 11, 460 + 11], fill=CREAM)
    # axis
    hairline(d, 300, 500, 1620, 500, BERRY, 1, 90)
    # dimension line above type
    hairline(d, 700, 660, 1220, 660, (180, 160, 145), 1)
    for x in (700, 1220):
        hairline(d, x, 650, x, 670, (180, 160, 145), 1)
    micro(im, "LATENT LINE / Ø 1.2 PX", (960, 676), (150, 130, 115), 15, 0.2, "ma")
    micro(im, "CONCEPT A-01 / DROP", (130, 70), (150, 130, 115))
    micro(im, "0.0 – 2.6 SEC", (130, 96), (170, 150, 135), 14, 0.18)
    micro(im, "ONE DROP. ONE LINE.", (1790, 70), BERRY, 20, 0.34, "ra")
    # big type bottom
    tracked_text(d, (150, 780), "ONE", serif_b(104), INK, 0.04, "la")
    tracked_text(d, (150, 892), "DROP.", serif_i(104), BERRY, 0.04, "la")
    micro(im, "EVERYTHING BEGINS WITH A SINGLE MARK.", (150, 758), (150, 130, 115), 16, 0.2)
    return grain(im, 4)

# ------------------------------------------------------------------ A2 EYE
def a2():
    im = canvas("cream")
    eye = spr("eng_eye_wide_ink")
    paste(im, eye, int(W*0.40), int(H*0.50), h=int(H*0.98), alpha=255)
    d = ImageDraw.Draw(im)
    # berry thread crossing
    pts = bezier((140, 780), (620, 850), (1240, 320), (1830, 360))
    thread(im, pts, BERRY, 2)
    # pupil accent
    d.ellipse([int(W*0.40)-13, int(H*0.51)-13, int(W*0.40)+13, int(H*0.51)+13], fill=BERRY)
    # left column labels
    micro(im, "A-02 / THE EYE OPENS", (60, 60), (150, 130, 115))
    micro(im, "S-01 / THE WITNESS", (60, 104), BERRY, 16, 0.2)
    hairline(d, 60, 150, 60, 420, BERRY, 1, 120)
    micro(im, "THE WORLD", (78, 400), (150, 130, 115), 15, 0.2)
    micro(im, "LOOKS BACK.", (78, 424), (150, 130, 115), 15, 0.2)
    # crop marks
    for (cx, cy, sx, sy) in [(40, 40, 1, 1), (W-40, 40, -1, 1), (40, H-40, 1, -1), (W-40, H-40, -1, -1)]:
        d.line([(cx, cy), (cx + 40*sx, cy)], fill=(120, 100, 90), width=1)
        d.line([(cx, cy), (cx, cy + 40*sy)], fill=(120, 100, 90), width=1)
    tracked_text(d, (1840, 960), "IT SEES YOU FIRST.", serif(34), INK, 0.12, "ra")
    tracked_text(d, (1840, 1002), "6.0 – 10.0 SEC", sans(14), (150, 130, 115), 0.2, "ra")
    return grain(im, 4)

# ------------------------------------------------------------------ A3 HEART
def a3():
    im = canvas("cream")
    d = ImageDraw.Draw(im)
    hx, hy, hh = int(W*0.26), int(H*0.45), int(H*0.64)
    # vines drawn behind the heart
    vine_specs = [
        ((hx - 30, H + 40), (hx - 270, int(H*0.74)), (hx - 310, int(H*0.42)), (hx - 225, int(H*0.28))),
        ((hx + 30, H + 40), (hx + 320, int(H*0.76)), (hx + 330, int(H*0.40)), (hx + 245, int(H*0.24))),
    ]
    for p0, p1, p2, p3 in vine_specs:
        pts = bezier(p0, p1, p2, p3)
        thread(im, pts, (150, 60, 70), 2, 200)
        for k in range(5, 56, 8):
            idx = min(len(pts) - 2, int(k / 60.0 * len(pts)))
            px, py = pts[idx]
            nx, ny = pts[idx + 2]
            ang = math.atan2(ny - py, nx - px)
            side = 1 if k % 2 == 0 else -1
            lx = px + 26 * math.cos(ang + side * math.pi / 2)
            ly = py + 26 * math.sin(ang + side * math.pi / 2)
            d.ellipse([lx-13, ly-6, lx+13, ly+6], outline=(150, 60, 70), width=2)
    heart = spr("ic_heart")
    paste(im, heart, hx, hy, h=hh)
    d = ImageDraw.Draw(im)
    # ruler strip
    ticks(d, 120, 200, 40, 20, vertical=True, fill=(180, 160, 145), length=(8, 18))
    hairline(d, 120, 200, 120, 980, (180, 160, 145), 1)
    # annotation lines
    ann = [
        (hx + int(hh*0.26), int(H*0.28), 1120, 240, "AORTA / S-02"),
        (hx + int(hh*0.30), int(H*0.45), 1180, 470, "VENTRICLE / S-03"),
        (hx + int(hh*0.24), int(H*0.64), 1120, 690, "THE WOUND / S-04"),
    ]
    for (x1, y1, x2, y2, lab) in ann:
        hairline(d, x1, y1, x2, y2, (120, 100, 90), 1)
        d.ellipse([x1-4, y1-4, x1+4, y1+4], fill=INK)
        d.ellipse([x2-4, y2-4, x2+4, y2+4], outline=INK, width=2)
        micro(im, lab, (x2 + 14, y2 - 9), (120, 100, 90), 15)
    micro(im, "A-03 / ANATOMY OF FEELING", (60, 60), (150, 130, 115))
    micro(im, "12.0 – 18.0 SEC", (60, 86), (170, 150, 135), 14)
    tracked_text(d, (150, 850), "SOME THINGS ARE BETTER", serif(48), INK, 0.05, "la")
    tracked_text(d, (150, 920), "SEEN IN CROSS-SECTION.", serif_i(48), BERRY, 0.05, "la")
    return grain(im, 4)

# ------------------------------------------------------------------ A4 BLACK INVERSION
def a4():
    im = canvas("env_black", tint=ENVBLACK, opacity=0.45)
    eye = spr("eng_eye_bone")
    paste(im, eye, int(W*0.74), int(H*0.50), h=int(H*0.52), alpha=235)
    d = ImageDraw.Draw(im)
    # grid lines bone
    for i in range(1, 9):
        hairline(d, 0, i*H/9, W, i*H/9, BONE, 1, 26)
    for i in range(1, 13):
        hairline(d, i*W/12, 0, i*W/12, H, BONE, 1, 26)
    micro(im, "A-04 / INVERSION", (60, 60), (200, 190, 178))
    micro(im, "THE ONLY BLACK IN THE FILM", (60, 100), BONE, 20, 0.26)
    tracked_text(d, (120, 430), "TURN", serif_b(150), BONE, 0.02, "la")
    tracked_text(d, (120, 590), "THE INK", serif_b(150), BONE, 0.02, "la")
    tracked_text(d, (120, 750), "BLACK.", serif_b(150), BERRY, 0.02, "la")
    # crosshair on eye pupil area (approx)
    cx, cy = int(W*0.74), int(H*0.48)
    d.line([(cx-60, cy), (cx+60, cy)], fill=BONE, width=1)
    d.line([(cx, cy-60), (cx, cy+60)], fill=BONE, width=1)
    micro(im, "S-05 / THE TURN", (W-60, 60), (200, 190, 178), 15, 0.2, "ra")
    return grain(im, 5)

# ------------------------------------------------------------------ A5 CARDS
def a5():
    im = canvas("cream")
    d = ImageDraw.Draw(im)
    items = [
        ("ic_tiger", "FEARLESS"),
        ("scissors", "LET GO"),
        ("ic_butterfly", "BECOME"),
        ("ic_eye_tears", "SEE CLEARLY"),
        ("flower", "CREATE"),
        ("ic_unicorn", "GET SHIT DONE"),
    ]
    cw, ch, gap = 236, 372, 28
    total = 6 * cw + 5 * gap
    x0 = (W - total) // 2
    base_y = 470
    rots = [-7, 5, -3, 7, -5, 3]
    for i, (sym, label) in enumerate(items):
        cx = x0 + i * (cw + gap) + cw // 2
        cy = base_y + ([-8, 6, -14, 8, -6, 2][i])
        card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        if i == 2:
            cd.rounded_rectangle([0, 0, cw, ch], radius=7, fill=BERRY + (255,))
        else:
            cd.rounded_rectangle([0, 0, cw, ch], radius=7, fill=(255, 251, 247, 255), outline=BERRY + (255,), width=3)
            cd.rounded_rectangle([10, 10, cw-10, ch-10], radius=5, outline=(198, 152, 154, 255), width=1)
        card = card.rotate(rots[i], expand=True, resample=Image.BICUBIC)
        im.paste(card, (int(cx - card.width/2), int(cy - ch/2)), card)
        if sym in ("scissors", "flower"):
            vector_icon(im, sym, cx, cy - 6, int(ch*0.86))
        else:
            icon = spr(sym)
            if i == 2:
                r, g, b, a = icon.split()
                t = Image.new("RGBA", icon.size, CREAM + (255,))
                t.putalpha(a)
                icon = t
            paste(im, icon, cx, cy - 16, h=int(ch*0.86), rot=rots[i])
        tracked_text(d, (cx, base_y + ch/2 + 34), label, serif(21), INK, 0.12, "ma")
    # baseline rule above cards
    hairline(d, x0 - 30, base_y - ch/2 - 34, x0 + total + 30, base_y - ch/2 - 34, BERRY, 1, 80)
    micro(im, "A-05 / SIX HUMAN CARDS", (60, 60), (150, 130, 115))
    micro(im, "THE CARD IS ONLY A CONTAINER", (60, 104), BERRY, 18, 0.22)
    micro(im, "21.0 – 30.0 SEC / 6 × 1.5 SEC", (60, 140), (170, 150, 135), 14, 0.18)
    tracked_text(d, (W-70, 1000), "SIX CARDS. SIX ANSWERS.", serif_i(40), BERRY, 0.08, "ra")
    return grain(im, 4)

# ------------------------------------------------------------------ A6 TOTEM / BRAND
def a6():
    im = canvas("rose", tint=CREAM, opacity=0.30)
    d = ImageDraw.Draw(im)
    cx, cy = W//2, H//2
    GOLDD = (110, 72, 22)
    # outer measurement ticks
    for i in range(72):
        a = i * 2 * math.pi / 72
        r1 = 452
        r2 = 452 + (18 if i % 6 == 0 else 9)
        d.line([(cx + r1*math.cos(a), cy + r1*math.sin(a)),
                (cx + r2*math.cos(a), cy + r2*math.sin(a))], fill=GOLDD, width=1)
    ring(d, cx, cy, 392, GOLDD, 3)
    ring(d, cx, cy, 374, GOLDD, 1)
    ring(d, cx, cy, 176, GOLDD, 2)
    ring(d, cx, cy, 160, GOLDD, 1)
    # center crosshair
    hairline(d, cx - 158, cy, cx + 158, cy, GOLDD, 1, 90)
    hairline(d, cx, cy - 158, cx, cy + 158, GOLDD, 1, 90)
    syms = ["ic_eye_tears", "ic_heart", "ic_crown", "ic_butterfly", "ic_moon", "ic_skull",
            "eng_ouroboros_ink", "ic_hands", "ic_compass", "eng_spider_ink", "ic_book", "ic_unicorn"]
    for i, s in enumerate(syms):
        a = -math.pi/2 + i * 2*math.pi / len(syms)
        x = cx + 382 * math.cos(a); y = cy + 382 * math.sin(a)
        try:
            sym = spr(s)
        except Exception:
            continue
        hh = 132 if sym.width <= sym.height * 1.5 else 104
        paste(im, sym, x, y, h=hh, tint=GOLDD)
        d.line([(cx + 176*math.cos(a), cy + 176*math.sin(a)),
                (cx + 300*math.cos(a), cy + 300*math.sin(a))], fill=GOLDD, width=1)
        d.ellipse([x-4, y-4, x+4, y+4], fill=GOLDD)
    tracked_text(d, (cx, cy - 58), "NOT TAROT", serif_b(56), GOLDD, 0.30, "ma")
    hairline(d, cx - 205, cy + 16, cx + 205, cy + 16, GOLDD, 1, 210)
    tracked_text(d, (cx, cy + 54), "MAKE YOUR OWN MEANING.", serif(23), INK, 0.22, "ma")
    micro(im, "A-06 / THE SEAL", (60, 60), (110, 80, 40))
    micro(im, "S-12 → S-18 / ALL SYMBOLS RETURN", (60, 86), (110, 80, 40), 15, 0.2)
    micro(im, "36.0 – 45.0 SEC / BRAND REVEAL", (W-60, 60), (110, 80, 40), 15, 0.2, "ra")
    return grain(im, 4)

# ------------------------------------------------------------------ B1 COLLAGE PLATE
def b1():
    im = canvas("env_black", tint=ENVBLACK, opacity=0.5)
    d = ImageDraw.Draw(im)
    # plate frame
    d.rectangle([70, 70, W-70, H-70], outline=BONE, width=2)
    d.rectangle([92, 92, W-92, H-92], outline=BONE, width=1)
    # title band
    tracked_text(d, (W//2, 132), "EXQUISITE CORPSE", serif(46), BONE, 0.24, "ma")
    tracked_text(d, (W//2, 196), "A DISSECTION IN FOUR PLATES / STUDY 03 / NOT TAROT", sans(15), (185, 175, 165), 0.28, "ma")
    hairline(d, 130, 236, W-130, 236, BONE, 1, 90)
    # quadrant separators
    hairline(d, W//2, 256, W//2, 900, BONE, 1, 70)
    hairline(d, 130, 578, W-130, 578, BONE, 1, 70)
    # quadrants content
    q = [
        ("P L A T E   I", "THE WITNESS", "eng_eye_bone", 0.26, 0.40, 0.36),
        ("P L A T E   I I", "THE CYCLE", "eng_ouroboros_bone", 0.74, 0.40, 0.30),
        ("P L A T E   I I I", "THE PATIENT", "eng_spider_bone", 0.26, 0.71, 0.24),
        ("P L A T E   I V", "THE TRANSFORMER", "eng_moth_bone", 0.74, 0.71, 0.24),
    ]
    for label, sub, sym, fx, fy, fh in q:
        try:
            s = spr(sym)
            paste(im, s, int(W*fx), int(H*fy), h=int(H*fh))
        except Exception as e:
            print("plate fail", sym, e)
        qx = 130 if fx < 0.5 else W//2 + 30
        qy = 250 if fy < 0.5 else 590
        micro(im, label, (qx, qy), (200, 190, 180), 14, 0.26)
        micro(im, sub, (qx, qy + 22), BONE, 17, 0.2)
    # bottom band
    hairline(d, 130, 930, W-130, 930, BONE, 1, 90)
    micro(im, "DISSECTION OF A FEELING — EVERY ELEMENT SEPARATED, THEN RE-ASSEMBLED", (130, 960), (190, 180, 170), 15, 0.2)
    micro(im, "B-01 / ALTERNATE DIRECTION", (W-130, 960), BONE, 15, 0.2, "ra")
    hairline(d, 130, 1000, 620, 1000, BERRY, 3)
    return grain(im, 5)

# ------------------------------------------------------------------ TRANSITIONS
def transition_sheet():
    cw, ch = 440, 264
    pad, hdr = 14, 40
    rows = 4
    SW = 3 * cw + 4 * pad
    SH = rows * (ch + hdr + pad) + pad
    sheet = Image.new("RGB", (SW, SH), (26, 22, 20))
    sd = ImageDraw.Draw(sheet)
    cjk = font("msyh.ttc", 19)
    cjk_s = font("msyh.ttc", 15)
    labels = [
        ("T1  线接续 / LINE CONTINUITY", "上镜最后一根线 = 下镜第一根线；线本身变形，画面不淡入淡出。0.35s"),
        ("T2  墨渗 / INK BLEED", "一滴墨在 2 帧内吃满全屏；下一场从墨的负形里长出来。0.45s"),
        ("T3  撕纸 / TORN PAPER", "整场像一张纸被撕开，纤维可见；撕口就是下一场的舞台。0.30s"),
        ("T4  盖印 / STAMP", "符号先被“压”进画面：重环 + 位移残影 + 短放射线。0.25s"),
    ]
    for r in range(rows):
        y0 = pad + r * (ch + hdr + pad)
        sd.text((pad, y0), labels[r][0], font=cjk, fill=(238, 230, 220))
        sd.text((pad + 460, y0 + 2), labels[r][1], font=cjk_s, fill=(160, 150, 140))
        for c in range(3):
            x0 = pad + c * (cw + pad)
            cell = Image.new("RGBA", (cw, ch), CREAM + (255,))
            cd = ImageDraw.Draw(cell)
            t = c / 2.0
            if r == 0:
                # heart -> eye morph through one continuous line
                try:
                    heart = spr("ic_heart"); eye = spr("ic_eye_tears")
                    if c == 0:
                        paste(cell, heart, cw*0.55, ch*0.52, h=ch*0.62)
                        cd.line([(cw*0.80, ch*0.50), (cw*0.98, ch*0.50)], fill=BERRY, width=2)
                    elif c == 1:
                        paste(cell, heart, cw*0.40, ch*0.55, h=ch*0.42, alpha=110)
                        paste(cell, eye, cw*0.64, ch*0.48, h=ch*0.40, alpha=150)
                        pts = bezier((cw*0.10, ch*0.30), (cw*0.35, ch*0.75), (cw*0.65, ch*0.20), (cw*0.95, ch*0.55))
                        thread(cell, pts, BERRY, 2)
                    else:
                        paste(cell, eye, cw*0.46, ch*0.50, h=ch*0.60)
                        cd.line([(cw*0.02, ch*0.52), (cw*0.18, ch*0.52)], fill=BERRY, width=2)
                except Exception as e:
                    print("t1", e)
            elif r == 1:
                if c == 0:
                    rad = ch * 0.10
                    cd.ellipse([cw*0.5-rad, ch*0.5-rad, cw*0.5+rad, ch*0.5+rad], fill=(11, 9, 8))
                    cd.ellipse([cw*0.5-rad, ch*0.5-rad, cw*0.5+rad, ch*0.5+rad], outline=BERRY, width=2)
                elif c == 1:
                    rad = ch * 1.25
                    cd.ellipse([cw*0.5-rad, ch*0.5-rad, cw*0.5+rad, ch*0.5+rad], fill=(11, 9, 8))
                else:
                    cd.rectangle([0, 0, cw, ch], fill=(11, 9, 8))
                    try:
                        eye = spr("eng_eye_bone"); paste(cell, eye, cw*0.55, ch*0.50, h=ch*0.55, alpha=150)
                    except Exception:
                        pass
                    micro(cell, "NEXT: THE EYE", (16, ch-30), BONE, 13, 0.2)
            elif r == 2:
                # torn cream paper revealing bone engraving scene
                reveal = 0.25 + 0.35 * t
                pts = [(cw, 0)]
                for yy in range(0, ch + 24, 22):
                    off = 22 * math.sin(yy * 0.22 + t * 7)
                    pts.append((cw * (1 - reveal) + off, yy))
                pts += [(cw, ch), (0, ch), (0, 0)]
                cd.polygon(pts, fill=(12, 10, 9))
                # fibers
                for k in range(16):
                    yy = 10 + k * (ch - 20) / 16
                    fx = cw * (1 - reveal) + 20 * math.sin(yy * 0.22 + t * 7)
                    cd.line([(fx, yy), (fx + 10 + 8 * math.sin(k), yy + 3)], fill=(205, 190, 172), width=1)
                try:
                    eye = spr("eng_eye_bone")
                    paste(cell, eye, cw*0.36, ch*0.50, h=ch*0.46, alpha=120)
                except Exception:
                    pass
            else:
                # stamp: crown pressed into paper
                try:
                    crown = spr("ic_crown")
                except Exception:
                    crown = None
                if c == 0:
                    if crown: paste(cell, crown, cw*0.5, ch*0.48, h=ch*0.34)
                elif c == 1:
                    rad = ch * 0.30
                    cd.ellipse([cw*0.5-rad, ch*0.5-rad, cw*0.5+rad, ch*0.5+rad], outline=BERRY, width=6)
                    if crown: paste(cell, crown, cw*0.5+8, ch*0.5+6, h=ch*0.34, alpha=110)
                else:
                    rad = ch * 0.30
                    cd.ellipse([cw*0.5-rad, ch*0.5-rad, cw*0.5+rad, ch*0.5+rad], outline=BERRY, width=3)
                    cd.ellipse([cw*0.5-rad*0.78, ch*0.5-rad*0.78, cw*0.5+rad*0.78, ch*0.5+rad*0.78], outline=INK, width=2)
                    for k in range(16):
                        a = k * 2 * math.pi / 16
                        r1 = rad * 1.12; r2 = rad * (1.22 + 0.05 * math.sin(k))
                        cd.line([(cw*0.5+r1*math.cos(a), ch*0.5+r1*math.sin(a)),
                                 (cw*0.5+r2*math.cos(a), ch*0.5+r2*math.sin(a))], fill=INK, width=2)
                    if crown: paste(cell, crown, cw*0.5, ch*0.5, h=ch*0.32)
            sheet.paste(cell.convert("RGB"), (x0, y0 + hdr))
    out = os.path.join(C3, "transitions_v3.jpg")
    sheet.save(out, quality=92)
    print("saved transitions_v3.jpg")

# ------------------------------------------------------------------ CONTACT SHEET
def contact_sheet(paths):
    cols = 2
    tw, th = 860, 484
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (cols*(tw+26) + 26, rows*(th+46) + 26), (245, 240, 234))
    d = ImageDraw.Draw(sheet)
    cjk = font("msyh.ttc", 20)
    for i, (label, p) in enumerate(paths):
        cx, cy = i % cols, i // cols
        x = 26 + cx*(tw+26); y = 26 + cy*(th+46)
        im = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (x, y))
        d.text((x, y + th + 12), label, font=cjk, fill=(70, 60, 55))
    out = os.path.join(C3, "concept_sheet_A.jpg")
    sheet.save(out, quality=92)
    print("saved", out)

if __name__ == "__main__":
    paths = []
    for fn, label in [(a1, "A-01  DROP · 一滴墨"), (a2, "A-02  THE EYE · 巨眼"),
                      (a3, "A-03  HEART · 解剖心"), (a4, "A-04  INVERSION · 黑场"),
                      (a5, "A-05  SIX CARDS · 六卡"), (a6, "A-06  THE SEAL · 图腾/品牌")]:
        name = fn.__name__.upper().replace("A", "A-") + ".jpg"
        name = "A" + fn.__name__[1] + "_v3.jpg"
        save(fn(), name)
        paths.append((label, os.path.join(C3, name)))
    save(b1(), "B1_v3.jpg")
    paths.append(("B-01  COLLAGE · 拆解剧场", os.path.join(C3, "B1_v3.jpg")))
    contact_sheet(paths)
    transition_sheet()
