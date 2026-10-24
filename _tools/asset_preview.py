# -*- coding: utf-8 -*-
"""Asset preview sheets: sprites (berry on cream) + paper textures."""
import os

from PIL import Image, ImageDraw

ROOT = r"E:/deepseek/PROJECT_MYSTIC_PROMO"
SPR = os.path.join(ROOT, "03_assets", "symbols", "sprites")
TEX = os.path.join(ROOT, "03_assets", "textures")
OUT = r"E:/deepseek/review_out"

SPRITES = ["heart", "eye", "eye_tears", "butterfly", "tiger", "unicorn", "crown", "mirror",
           "compass", "hands", "wand", "skull", "moon", "cloud_eye", "scales", "question",
           "book", "key", "flower", "star", "snake", "hourglass", "arch", "candle", "scissors"]


def alpha_boost(im):
    lut = [min(255, int(255 * ((i / 255.0) ** 0.40) * 1.75)) for i in range(256)]
    im = im.copy()
    im.putalpha(im.split()[3].point(lut))
    return im


def tinted(im, color):
    out = Image.new("RGBA", im.size, color + (255,))
    out.putalpha(im.split()[3])
    return out


cream = Image.open(os.path.join(TEX, "paper_cream.jpg")).convert("RGB").resize((1200, 1200))
cols, cell = 5, 240
rows = (len(SPRITES) + cols - 1) // cols
sheet = cream.crop((0, 0, cols * cell, rows * cell + 26)).copy()
d = ImageDraw.Draw(sheet)
for i, name in enumerate(SPRITES):
    im = alpha_boost(Image.open(os.path.join(SPR, name + ".png")).convert("RGBA"))
    im = tinted(im, (143, 44, 59))
    w, h = im.size
    s = min((cell - 36) / w, (cell - 36) / h)
    im = im.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
    r, c = divmod(i, cols)
    x = c * cell + (cell - im.width) // 2
    y = r * cell + (cell - im.height) // 2 + 26
    sheet.paste(im, (x, y), im)
    d.text((c * cell + 8, r * cell + 6), name, fill=(60, 40, 45))

sheet.save(os.path.join(OUT, "sprite_sheet.jpg"), quality=90)
print("sprite sheet", sheet.size)

names = ["paper_cream.jpg", "paper_cream_hi.jpg", "paper_page_white.jpg", "paper_bone.jpg",
         "paper_blush.jpg", "paper_pale_rose.jpg", "paper_rose.jpg", "paper_mauve.jpg",
         "paper_env_black.jpg", "paper_env_hi.jpg"]
cw = 300
psheet = Image.new("RGB", (cols * cw, 2 * cw + 26), (30, 28, 30))
d = ImageDraw.Draw(psheet)
for i, fn in enumerate(names):
    im = Image.open(os.path.join(TEX, fn)).convert("RGB").resize((cw, cw), Image.LANCZOS)
    r, c = divmod(i, cols)
    psheet.paste(im, (c * cw, r * (cw + 26) + 26))
    d.text((c * cw + 8, r * (cw + 26) + 8), fn, fill=(235, 230, 220))
psheet.save(os.path.join(OUT, "paper_sheet.jpg"), quality=90)
print("paper sheet", psheet.size)
