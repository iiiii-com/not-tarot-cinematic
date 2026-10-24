# -*- coding: utf-8 -*-
"""Detect individual card bounding boxes in the 7 reference images using scipy labeling."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

REF = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO\00_reference")


def load(name):
    return Image.open(REF / name).convert("RGB")


def components(mask, min_area=15000, min_w=80, min_h=120, name=""):
    lab, n = ndi.label(mask, structure=np.ones((3, 3), dtype=int))
    sl = ndi.find_objects(lab)
    cards = []
    for i, s in enumerate(sl, 1):
        if s is None:
            continue
        y0, y1, x0, x1 = s[0].start, s[0].stop, s[1].start, s[1].stop
        area = (lab[s] == i).sum()
        w, h = x1 - x0, y1 - y0
        if area >= min_area and w >= min_w and h >= min_h:
            cards.append((x0, y0, x1, y1, int(area)))
    cards.sort(key=lambda b: (round(b[1] / 60), b[0]))
    print(f"\n{name}: {len(cards)} components")
    for b in cards:
        print("   ", b[:4], "size", b[2] - b[0], "x", b[3] - b[1], "area", b[4])
    return cards


# 01
img = load("reference_01_cards.jpg")
a = np.asarray(img).astype(np.int16)
mask = (a.min(axis=2) < 246) & (a.max(axis=2) > 240)
# fill small holes so card interior is solid
mask = ndi.binary_closing(mask, structure=np.ones((9, 9)))
components(mask, name="01")

# 03
img = load("reference_03_icon_cards_b.jpg")
a = np.asarray(img).astype(np.int16)
mask = (a.min(axis=2) < 246) & (a.max(axis=2) > 240)
mask = ndi.binary_closing(mask, structure=np.ones((9, 9)))
components(mask, name="03")

# 04 colorways
img = load("reference_04_eyeline_colorways.jpg")
a = np.asarray(img).astype(np.int16)
mask = (a.min(axis=2) < 246) & (a.max(axis=2) > 238)
mask = ndi.binary_closing(mask, structure=np.ones((9, 9)))
components(mask, name="04", min_area=20000)

# 02 arcana grid
img = load("reference_02_symbol_sheet.jpg")
a = np.asarray(img).astype(np.int16)
mask = (a.min(axis=2) > 150) & (a.max(axis=2) > 240)
mask = ndi.binary_closing(mask, structure=np.ones((5, 5)))
components(mask, name="02", min_area=30000)

# 06 engraving: light cards on dark bg
img = load("reference_06_engraving_deck.jpg")
a = np.asarray(img).astype(np.int16)
mask = a.mean(axis=2) > 150
mask = ndi.binary_closing(mask, structure=np.ones((7, 7)))
components(mask, name="06", min_area=60000)

# 05 gold: card on pink; use gold-ish line detect? just report whole
img = load("reference_05_gold_emblem_knowing.jpg")
print("\n05 size", img.size)
# 07 brand berry bbox already known
print("done")
