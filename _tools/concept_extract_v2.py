# -*- coding: utf-8 -*-
"""Concept v3 extraction v2: clean icons (kill card haze) + engraving motifs (tight crops)."""
import os, numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont

ROOT = r"E:/deepseek/PROJECT_MYSTIC_PROMO"
C3 = os.path.join(ROOT, "03_assets", "concept_v3")
MOT = os.path.join(C3, "motifs2")
os.makedirs(MOT, exist_ok=True)

CREAM = (250, 242, 236)
INK = (20, 16, 15)
BONE = (247, 242, 230)

def darkness_alpha(im, lo=18, hi=236, gamma=1.05, floor=45, ceil_boost=1.0):
    g = np.array(im.convert("L")).astype(np.float32)
    a = np.clip((hi - g) / max(1e-3, hi - lo) * 255.0, 0, 255)
    a = (a / 255.0) ** gamma * 255.0
    # kill faint paper haze / card bevel
    a = np.clip((a - floor) * (255.0 / max(1e-3, 255.0 - floor)) * ceil_boost, 0, 255)
    return Image.fromarray(a.astype(np.uint8), "L")

def trim(a, thr=24):
    bb = a.point(lambda v: 255 if v > thr else 0).getbbox()
    return a.crop(bb) if bb else a

def tint(a, color):
    rgba = Image.new("RGBA", a.size, color + (0,))
    rgba.putalpha(a)
    return rgba

def save(rgba, name):
    p = os.path.join(MOT, name + ".png")
    rgba.save(p)
    return p

# ---------- icons ----------
ICON_SRC = {
    "heart": ("cards/m1_02_band_aid_whisperer.png", (0.06, 0.04, 0.94, 0.80)),
    "skull": ("cards/m1b_02_waiting_for_gold.png", (0.06, 0.04, 0.94, 0.80)),
    "moon": ("cards/m1b_04_retrograde_realness.png", (0.05, 0.03, 0.95, 0.82)),
    "cloud_eye": ("cards/m1b_03_end_of_drama.png", (0.05, 0.03, 0.95, 0.82)),
    "hands": ("cards/m1_06_namaste_bitches.png", (0.05, 0.05, 0.95, 0.80)),
    "crown": ("cards/m1_03_ceo_babe.png", (0.06, 0.03, 0.94, 0.80)),
    "butterfly": ("cards/m1_10_bruised_not_broken.png", (0.05, 0.03, 0.95, 0.82)),
    "tiger": ("cards/m1_08_fearless.png", (0.05, 0.03, 0.95, 0.82)),
    "unicorn": ("cards/m1_07_get_shit_done.png", (0.05, 0.03, 0.95, 0.82)),
    "eye_tears": ("cards/m1b_12_dont_give_a_fuck.png", (0.03, 0.03, 0.97, 0.84)),
    "book": ("cards/m1_12_heavenly_insights.png", (0.04, 0.03, 0.96, 0.82)),
    "mirror": ("cards/m1_01_imagination_guru.png", (0.06, 0.03, 0.94, 0.80)),
    "compass": ("cards/m1_05_no_gps_lost_forever.png", (0.05, 0.04, 0.95, 0.82)),
    "wand": ("cards/m1_04_wish_fulfilling_wizard.png", (0.04, 0.04, 0.96, 0.84)),
    "dragon": ("cards/m2_major_05.png", (0.05, 0.04, 0.95, 0.86)),
}

def extract_icon(src, inset, upscale=3, floor=52):
    im = Image.open(os.path.join(ROOT, "03_assets", src)).convert("RGB")
    w, h = im.size
    box = (int(w * inset[0]), int(h * inset[1]), int(w * inset[2]), int(h * inset[3]))
    im = im.crop(box)
    im = im.resize((im.width * upscale, im.height * upscale), Image.LANCZOS)
    im = im.filter(ImageFilter.MedianFilter(3))
    a = darkness_alpha(im, floor=floor)
    a = trim(a, 20)
    return tint(a, INK)

# ---------- engraving motifs ----------
REF6 = Image.open(os.path.join(ROOT, "00_reference", "reference_06_engraving_deck.jpg")).convert("RGB")

def engrave(name, box, rot=0.0, inset=0.045, floor=58):
    im = REF6.crop(box)
    if rot:
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    a = darkness_alpha(im, floor=floor, gamma=1.0)
    m = Image.new("L", a.size, 0)
    d = ImageDraw.Draw(m)
    ix, iy = int(a.width * inset), int(a.height * inset)
    d.rounded_rectangle([ix, iy, a.width - ix, a.height - iy], radius=int(min(a.size) * 0.05), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(int(min(a.size) * 0.02)))
    a = Image.composite(a, Image.new("L", a.size, 0), m)
    a = trim(a, 22)
    ink = tint(a, INK); bone = tint(a, BONE)
    save(ink, "eng_" + name + "_ink"); save(bone, "eng_" + name + "_bone")
    return ink, bone

def sheet(items, name, cell=330):
    cols = 5
    rows = (len(items) + cols - 1) // cols
    W = cols * (cell + 10) + 10
    H = rows * (cell + 34) + 10
    out = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(out)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    for i, (nm, rgba) in enumerate(items):
        cx, cy = i % cols, i // cols
        x = 10 + cx * (cell + 10); y = 10 + cy * (cell + 34)
        d.text((x, y), nm, font=f, fill=(80, 80, 80))
        im = rgba.copy()
        k = min(cell / im.width, cell / im.height)
        im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
        out.paste(im, (x + (cell - im.width) // 2, y + 18 + (cell - im.height) // 2), im)
    out.save(os.path.join(C3, name), quality=90)
    print("saved", name)

if __name__ == "__main__":
    icons = []
    for nm, (src, inset) in ICON_SRC.items():
        try:
            rgba = extract_icon(src, inset)
            save(rgba, "ic_" + nm)
            icons.append((nm, rgba))
        except Exception as e:
            print("icon fail", nm, e)
    sheet(icons, "_icons_v2.jpg")

    eng = []
    for nm, box, rot, inset in [
        ("eye", (500, 380, 1010, 890), -5.0, 0.06),
        ("eye_wide", (450, 330, 1080, 1010), -5.0, 0.08),
        ("ouroboros", (1190, 255, 1610, 705), -5.0, 0.05),
        ("spider", (650, 1275, 1080, 1715), -6.0, 0.05),
        ("moth", (1320, 1300, 1700, 1760), -4.0, 0.05),
        ("cloud", (60, 120, 430, 540), 0.0, 0.04),
    ]:
        ink, bone = engrave(nm, box, rot, inset)
        eng.append((nm, ink)); eng.append((nm, bone))
    sheet(eng, "_engrave_v2_all.jpg")
