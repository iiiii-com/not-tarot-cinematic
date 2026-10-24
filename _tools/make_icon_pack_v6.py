# -*- coding: utf-8 -*-
"""v6 icon pack: clean reference sprites, tint 4 ways, save PNGs."""
from PIL import Image, ImageDraw
import numpy as np, os, json
import scipy.ndimage as ndi
SP = r"03_assets\symbols\sprites"
OUT = r"03_assets\symbols\sprites6"
os.makedirs(OUT, exist_ok=True)
COLORS = {"berry": (143,44,59), "gold": (94,62,23), "bone": (247,242,230), "plum": (36,31,34)}
USE = {
 "heart":"heart", "heart_alt":"heart_bandaid", "eye":"eye", "butterfly":"butterfly",
 "tiger":"tiger", "unicorn":"unicorn", "crown":"crown", "mirror":"mirror",
 "compass":"compass", "scales":"scales", "wand":"wand", "skull":"skull",
 "moon":"moon", "cloud_eye":"cloud_eye", "book":"book", "key":"key",
 "snake":"snake", "hourglass":"hourglass", "arch":"arch", "candle":"candle", "star":"star",
}

def clean(name):
    im = Image.open(os.path.join(SP, USE[name] + ".png")).convert("RGBA")
    a = np.asarray(im)[:, :, 3].astype(np.float32) / 255.0
    a = np.clip((a ** 0.85) * 1.28, 0, 1)
    lab, n = ndi.label(a > 0.12)
    keep = np.zeros_like(a, dtype=bool)
    for sid in range(1, n + 1):
        ys, xs = np.where(lab == sid)
        if len(xs) < 3:
            continue
        keep[lab == sid] = True
    a = np.where(keep, a, 0)
    if name == "heart_alt":
        m = (a > 0.18)
        for y in range(a.shape[0]):
            if m[y].mean() > 0.58: a[y, :] = 0
        for x in range(a.shape[1]):
            if m[:, x].mean() > 0.58: a[:, x] = 0
    arr = (a * 255).astype(np.uint8)
    bb = Image.fromarray(arr).getbbox()
    if not bb:
        raise RuntimeError(name)
    return Image.fromarray(arr).crop((max(0, bb[0]-6), max(0, bb[1]-6), min(arr.shape[1], bb[2]+6), min(arr.shape[0], bb[3]+6)))

manifest = {}
for name in USE:
    al = clean(name)
    manifest[name] = list(al.size)
    for cname, rgb in COLORS.items():
        rgba = Image.new("RGBA", al.size, rgb + (255,))
        rgba.putalpha(al)
        rgba.save(os.path.join(OUT, f"{name}__{cname}.png"), optimize=True)

# contact sheet
cell = 210; cols = 7; rows = (len(USE) + cols - 1) // cols
sheet = Image.new("RGB", (cell * cols, cell * rows), (250, 242, 236)); d = ImageDraw.Draw(sheet)
for i, name in enumerate(USE):
    im = Image.open(os.path.join(OUT, f"{name}__berry.png")).convert("RGBA")
    hh = min(cell - 30, 170); ww = max(1, int(im.width * hh / im.height)); im = im.resize((ww, hh), Image.LANCZOS)
    x = (i % cols) * cell + (cell - ww) // 2; y = (i // cols) * cell + (cell - hh) // 2 + 6
    sheet.paste(im, (x, y), im); d.text(((i % cols) * cell + 5, (i // cols) * cell + 3), name, fill=(20, 16, 15))
sheet.save(r"_review\icons_v6_test.jpg", quality=92)
print(json.dumps(manifest, indent=0))
