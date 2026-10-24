# -*- coding: utf-8 -*-
"""Build a labelled contact sheet of the 18 director-cut keyframes."""
import os
from PIL import Image, ImageDraw, ImageFont

KF = r"E:/deepseek/PROJECT_MYSTIC_PROMO/03_assets/keyframes"
OUT = os.path.join(KF, "keyframes_contact_sheet.png")
order = ["S01a", "S01b", "S02a", "S02b", "S03", "S04a", "S04b",
         "S05a", "S05b", "S05c", "S05d", "S05e", "S05f",
         "S06a", "S06b", "S06c", "S07a", "S07b"]
cols, rows = 3, 6
tw, th = 640, 360
label_h = 26
sheet = Image.new("RGB", (cols * tw, rows * (th + label_h)), (255, 255, 255))
d = ImageDraw.Draw(sheet)
font = ImageFont.truetype(r"C:/Windows/Fonts/arial.ttf", 18)
for i, sid in enumerate(order):
    im = Image.open(os.path.join(KF, sid + "_keyframe.png")).convert("RGB").resize((tw, th), Image.LANCZOS)
    r, c = divmod(i, cols)
    x, y = c * tw, r * (th + label_h)
    sheet.paste(im, (x, y))
    d.text((x + 8, y + th + 3), sid, font=font, fill=(20, 20, 20))
sheet.save(OUT)
print("saved", OUT, sheet.size)
