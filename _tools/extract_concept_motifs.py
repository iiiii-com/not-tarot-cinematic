# -*- coding: utf-8 -*-
"""Extract high-res engraving motifs from reference_06 and icon motifs, for concept v3.

Outputs RGBA pngs into 03_assets/concept_v3/motifs/ and a preview sheet.
"""
import os
import numpy as np
from PIL import Image, ImageOps, ImageFilter

ROOT = r"E:/deepseek/PROJECT_MYSTIC_PROMO"
OUT = os.path.join(ROOT, "03_assets", "concept_v3", "motifs")
os.makedirs(OUT, exist_ok=True)

REF6 = Image.open(os.path.join(ROOT, "00_reference", "reference_06_engraving_deck.jpg")).convert("RGB")
INK = (20, 16, 15)
BONE = (247, 242, 230)


def engrave(name, box, rotate=0.0, thr=46, color=INK, hi=1.0):
    """white-line engraving -> RGBA motif. alpha = line strength, color tint."""
    im = REF6.crop(box)
    if rotate:
        im = im.rotate(rotate, expand=True, resample=Image.BICUBIC)
    g = np.array(im.convert("L")).astype(np.float32)
    # engraving: white lines on black. line strength = luminance, normalize
    a = np.clip((g - thr) / max(1e-3, (255 - thr)) * 255.0, 0, 255)
    # gamma to keep thin hatching visible
    a = (a / 255.0) ** 0.85 * 255.0
    mask = Image.fromarray(a.astype(np.uint8), "L")
    bbox = mask.point(lambda v: 255 if v > 26 else 0).getbbox()
    if bbox:
        mask = mask.crop(bbox)
    rgba = Image.new("RGBA", mask.size, color + (0,))
    rgba.putalpha(mask)
    p = os.path.join(OUT, name + ".png")
    rgba.save(p)
    print("motif", name, rgba.size)
    return rgba


def clean_icon(card_path, inset=0.12, thr=128, color=INK, upscale=3):
    """icon card crop -> clean RGBA line art (alpha=darkness), 3x upscale."""
    im = Image.open(card_path).convert("RGB")
    w, h = im.size
    # inset: drop frame + label band
    im = im.crop((int(w * 0.10), int(h * 0.06), int(w * 0.90), int(h * 0.80)))
    g = np.array(im.convert("L")).astype(np.float32)
    # lines are dark on pink: alpha = darkness relative to local bg
    bg = np.percentile(g, 88)
    a = np.clip((bg - g) / max(1e-3, bg - 40) * 255.0, 0, 255)
    a = (a / 255.0) ** 0.80 * 255.0
    mask = Image.fromarray(a.astype(np.uint8), "L")
    bbox = mask.point(lambda v: 255 if v > 22 else 0).getbbox()
    if bbox:
        mask = mask.crop(bbox)
    mask = mask.resize((mask.width * upscale, mask.height * upscale), Image.LANCZOS)
    mask = mask.filter(ImageFilter.UnsharpMask(radius=1.4, percent=80, threshold=2))
    rgba = Image.new("RGBA", mask.size, color + (0,))
    rgba.putalpha(mask)
    p = os.path.join(OUT, os.path.basename(card_path).rsplit(".", 1)[0] + ".png")
    rgba.save(p)
    print("icon", os.path.basename(p), rgba.size)
    return rgba


if __name__ == "__main__":
    motifs = {}
    # engraving: eye, ouroboros, spider, moth, cloud-eye, banner
    motifs["eng_eye"] = engrave("eng_eye", (430, 260, 1180, 1080), rotate=-6.5)
    motifs["eng_ouroboros"] = engrave("eng_ouroboros", (1150, 230, 1830, 1090), rotate=-5.0)
    motifs["eng_spider"] = engrave("eng_spider", (500, 1120, 1300, 2030), rotate=-6.0)
    motifs["eng_moth"] = engrave("eng_moth", (1200, 1150, 1960, 1990), rotate=-4.0)
    motifs["eng_cloud"] = engrave("eng_cloud", (60, 120, 430, 540), rotate=0.0)
    motifs["eng_banner_eye"] = engrave("eng_banner_eye", (330, 830, 1010, 1075), rotate=-6.0)
    motifs["eng_banner_ouro"] = engrave("eng_banner_ouro", (1180, 780, 1800, 1030), rotate=-5.0)

    # icon cards: heart, skull, moon, cloud eye, hands, crown, butterfly, tiger, unicorn
    cards = ["m1_02_band_aid_whisperer", "m1b_02_waiting_for_gold", "m1b_04_retrograde_realness",
             "m1b_03_end_of_drama", "m1_06_namaste_bitches", "m1_03_ceo_babe",
             "m1_10_bruised_not_broken", "m1_08_fearless", "m1_07_get_shit_done",
             "m1b_12_dont_give_a_fuck", "m1_05_no_gps_lost_forever", "m1_12_heavenly_insights"]
    for c in cards:
        p = os.path.join(ROOT, "03_assets", "cards", c + ".png")
        if os.path.exists(p):
            clean_icon(p)

    # preview sheet
    allf = sorted([f for f in os.listdir(OUT) if f.endswith(".png")])
    cell_w, cell_h = 380, 300
    cols = 4
    rows = (len(allf) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (250, 242, 236))
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(r"C:/Windows/Fonts/arial.ttf", 15)
    for i, fn in enumerate(allf):
        im = Image.open(os.path.join(OUT, fn)).convert("RGBA")
        k = min((cell_w - 20) / im.width, (cell_h - 40) / im.height, 1.6)
        im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
        c, r = i % cols, i // cols
        x = c * cell_w + (cell_w - im.width) // 2
        y = r * cell_h + 26
        sheet.paste(im, (x, y), im)
        d.text((c * cell_w + 8, r * cell_h + 6), fn.replace(".png", ""), font=f, fill=(20, 20, 20))
    p = os.path.join(ROOT, "03_assets", "concept_v3", "motif_sheet.jpg")
    sheet.save(p, quality=90)
    print("sheet", p, sheet.size)
