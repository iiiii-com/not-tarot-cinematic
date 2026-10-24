# -*- coding: utf-8 -*-
"""Build 03_assets: card crops from the 7 references, paper textures, logo SVGs,
symbol index sheet + CSVs (symbols/borders/combos)."""
import sys, io, csv, re, math, random
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
REF = ROOT / "00_reference"
ASSETS = ROOT / "03_assets"
CARDS = ASSETS / "cards"
SYMS = ASSETS / "symbols"
TEX = ASSETS / "textures"
LOGO = ASSETS / "logo"
for p in (CARDS, SYMS, TEX, LOGO):
    p.mkdir(parents=True, exist_ok=True)

BIBLE = ROOT / "01_style_bible" / "style_bible.md"

# palette
P = {
    "cream": "#FAF2EC", "blush": "#F7C7C7", "rose": "#F6B7CC", "mauve": "#D8A5B8",
    "pale_rose": "#FCE9EF", "berry": "#8F2C3B", "crimson": "#B01F38", "gold": "#7B5521",
    "lampblack": "#14100F", "env_black": "#0B0908", "bone": "#F7F2E6",
    "lilac": "#CFC3D2", "mint": "#B7D8DC", "warm_white": "#FFF8EE",
    "page_white": "#FEFAF9", "brand_plum": "#241F22",
}


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- card crops
REF_IMGS = {
    "01": Image.open(REF / "reference_01_cards.jpg").convert("RGB"),
    "02": Image.open(REF / "reference_02_symbol_sheet.jpg").convert("RGB"),
    "03": Image.open(REF / "reference_03_icon_cards_b.jpg").convert("RGB"),
    "04": Image.open(REF / "reference_04_eyeline_colorways.jpg").convert("RGB"),
    "05": Image.open(REF / "reference_05_gold_emblem_knowing.jpg").convert("RGB"),
    "06": Image.open(REF / "reference_06_engraving_deck.jpg").convert("RGB"),
    "07": Image.open(REF / "reference_07_brand_page.jpg").convert("RGB"),
}

manifest_rows = []


def save_crop(key, box, name, mode, note):
    img = REF_IMGS[key]
    x0, y0, x1, y1 = [int(v) for v in box]
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(img.width, x1), min(img.height, y1)
    crop = img.crop((x0, y0, x1, y1))
    out = CARDS / name
    crop.save(out)
    manifest_rows.append([name, f"reference_{key}", f"{x0},{y0},{x1},{y1}",
                          f"{crop.width}x{crop.height}", mode, note])
    return crop


m1_names = [
    ("IMAGINATION GURU", "imagination_guru"), ("BAND-AID WHISPERER", "band_aid_whisperer"),
    ("CEO BABE", "ceo_babe"), ("WISH-FULFILLING WIZARD", "wish_fulfilling_wizard"),
    ("NO GPS, LOST FOREVER", "no_gps_lost_forever"), ("NAMASTE BITCHES", "namaste_bitches"),
    ("GET SHIT DONE", "get_shit_done"), ("FEARLESS", "fearless"),
    ("DRAMA QUEEN", "drama_queen"), ("BRUISED, NOT BROKEN", "bruised_not_broken"),
    ("FANTASIES DONT PAY", "fantasies_dont_pay"), ("HEAVENLY INSIGHTS", "heavenly_insights"),
]
xs = [48, 294, 540, 786]
ys = [24, 364, 704]
for i, (label, slug) in enumerate(m1_names):
    c, r = i % 4, i // 4
    save_crop("01", (xs[c] - 2, ys[r] - 2, xs[c] + 238, ys[r] + 328),
              f"m1_{i+1:02d}_{slug}.png", "M1", label)

m1b_names = [
    ("DREAM BIG, BURN BRIGHT", "dream_big_burn_bright"), ("WAITING FOR GOLD", "waiting_for_gold"),
    ("END OF DRAMA", "end_of_drama"), ("RETROGRADE REALNESS", "retrograde_realness"),
    ("CELEBRATION MODE", "celebration_mode"), ("TEARS ARE POWER", "tears_are_power"),
    ("MASTER OF WEALTH", "master_of_wealth"), ("NOSTALGIA OVERLOAD", "nostalgia_overload"),
    ("KARMA IS A BITCH", "karma_is_a_bitch"), ("CURIOSITY UNLEASHED", "curiosity_unleashed"),
    ("BAND-AID WHISPERER", "band_aid_whisperer_b"), ("DONT GIVE A FUCK", "dont_give_a_fuck"),
]
for i, (label, slug) in enumerate(m1b_names):
    c, r = i % 4, i // 4
    save_crop("03", (xs[c] - 1, ys[r] - 2, xs[c] + 240, ys[r] + 330),
              f"m1b_{i+1:02d}_{slug}.png", "M1", label)

# 04 colorways: berry / black / lilac variants of TEARS ARE POWER
for j, (slug, note) in enumerate([("v1_berry", "C1 default"), ("v2_black", "C2 lampblack"),
                                  ("v3_lilac", "C3 lilac+mint")]):
    x0 = 96 + j * 305
    save_crop("04", (x0, 178, x0 + 296, 592), f"m1_{slug}_tears_are_power.png",
              "M1-variant", note)

# 02 arcana: the Fool + visible majors
fool = REF_IMGS["02"].crop((631, 355, 1369, 1645))
fool.save(CARDS / "m2_the_fool.png")
manifest_rows.append(["m2_the_fool.png", "reference_02", "631,355,1369,1645",
                      f"{fool.width}x{fool.height}", "M2", "THE FOOL 0 (中心主卡)"])
majors = [(81, 66, 313, 470), (403, 66, 634, 470), (1366, 66, 1597, 470), (1687, 66, 1918, 470),
          (84, 554, 315, 958), (403, 554, 614, 958), (1687, 554, 1919, 958),
          (81, 1042, 313, 1446), (403, 1042, 634, 1446), (1684, 1530, 1915, 1934)]
for i, bb in enumerate(majors, 1):
    save_crop("02", bb, f"m2_major_{i:02d}.png", "M2", "大牌网格裁切（局部可见）")

# 05 gold KNOWING full card
know = REF_IMGS["05"].crop((6, 6, 1393, 1984))
know.save(CARDS / "m3_knowing_26.png")
manifest_rows.append(["m3_knowing_26.png", "reference_05", "6,6,1393,1984",
                      f"{know.width}x{know.height}", "M3", "KNOWING #26 金印卡"])

# 06 engraving crops (angled comps, keep rotation as-is)
for slug, bb in [("eye", (360, 200, 1080, 1080)), ("ouroboros", (1020, 170, 1730, 900)),
                 ("spider", (470, 920, 1230, 1900)), ("moth", (1420, 860, 2010, 1750))]:
    save_crop("06", bb, f"m4_engraving_{slug}_angled.png", "M4", "蚀刻牌斜置裁切（comp）")

# 07 brand botanical heart（品牌页插图，含参考排版文字——仅作参考，生产用 SVG）
save_crop("07", (366, 115, 695, 518), "brand_page_illustration_detail.png", "Brand",
          "品牌页插图参考（含原排版文字，不直接做 Logo）")
brand_heart = Image.open(CARDS / "brand_page_illustration_detail.png")

with (CARDS / "card_assets.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["file", "source_reference", "crop_box_px", "size_px", "mode", "label_or_note"])
    w.writerows(manifest_rows)
print("cards:", len(manifest_rows))

# contact sheet
thumbs = []
for row in manifest_rows:
    im = Image.open(CARDS / row[0]).convert("RGB")
    im.thumbnail((260, 360))
    thumbs.append((im, row[0]))
cols = 8
cw, ch = 280, 400
rows = math.ceil(len(thumbs) / cols)
sheet = Image.new("RGB", (cols * cw + 40, rows * ch + 40), hex2rgb(P["page_white"]))
d = ImageDraw.Draw(sheet)
try:
    ft = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 13)
except Exception:
    ft = ImageFont.load_default()
for i, (im, name) in enumerate(thumbs):
    c, r = i % cols, i // cols
    x, y = 20 + c * cw, 20 + r * ch
    sheet.paste(im, (x + (260 - im.width) // 2, y))
    d.text((x + 4, y + 368), name[:34], font=ft, fill=hex2rgb(P["brand_plum"]))
sheet.save(CARDS / "cards_contact_sheet.png")
print("contact sheet ok")

# ---------------------------------------------------------------- textures
def paper_texture(base_hex, name, fibers=900, speck=0.0006, grain=2.2, size=1024, seed=7):
    rng = np.random.default_rng(seed)
    base = np.array(hex2rgb(base_hex), dtype=np.float32)
    arr = base[None, None, :] + rng.normal(0, grain, (size, size, 1))
    arr = np.clip(arr, 0, 255)
    img = Image.fromarray(arr.astype(np.uint8), "RGB")
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(fibers):
        x0, y0 = rng.uniform(0, size), rng.uniform(0, size)
        ln = rng.uniform(6, 40)
        a = rng.uniform(-0.35, 0.35) + (0 if rng.random() < 0.7 else math.pi / 2)
        x1, y1 = x0 + math.cos(a) * ln, y0 + math.sin(a) * ln
        v = rng.integers(-16, 12)
        col = tuple(int(np.clip(c + v, 0, 255)) for c in base) + (int(rng.uniform(10, 30)),)
        d.line([(x0, y0), (x1, y1)], fill=col, width=1)
    n = int(size * size * speck)
    for _ in range(n):
        x, y = rng.integers(0, size), rng.integers(0, size)
        v = int(rng.integers(-40, -8))
        col = tuple(int(np.clip(c + v, 0, 255)) for c in base)
        d.point((x, y), fill=col)
    img = img.filter(ImageFilter.GaussianBlur(0.35))
    img.save(TEX / name, quality=92)
    print("texture", name)


for hx, nm, fbr, gr in [
    (P["cream"], "paper_cream.jpg", 700, 2.0),
    (P["blush"], "paper_blush.jpg", 800, 2.2),
    (P["rose"], "paper_rose.jpg", 800, 2.2),
    (P["mauve"], "paper_mauve.jpg", 700, 2.4),
    (P["pale_rose"], "paper_pale_rose.jpg", 700, 2.0),
    (P["bone"], "paper_bone.jpg", 1200, 3.0),
    (P["env_black"], "paper_env_black.jpg", 500, 2.0),
    (P["page_white"], "paper_page_white.jpg", 600, 1.8),
]:
    paper_texture(hx, nm, fibers=fbr, grain=gr)

# ---------------------------------------------------------------- logo SVGs
logo_wordmark = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="640" height="180" viewBox="0 0 640 180" role="img" aria-label="NOT TAROT wordmark">
  <rect width="640" height="180" fill="#FEFAF9"/>
  <g fill="none" stroke="#241F22" stroke-width="1.4">
    <line x1="56" y1="42" x2="584" y2="42"/>
    <line x1="56" y1="138" x2="584" y2="138"/>
    <line x1="56" y1="42" x2="56" y2="50"/>
    <line x1="584" y1="42" x2="584" y2="50"/>
  </g>
  <text x="320" y="105" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif"
        font-size="52" letter-spacing="14" fill="#241F22">NOT TAROT</text>
  <text x="320" y="128" text-anchor="middle" font-family="Georgia, serif"
        font-size="12" letter-spacing="6" fill="#8F2C3B">AN ENTIRELY ORIGINAL DECK</text>
</svg>
"""
(LOGO / "not_tarot_wordmark.svg").write_text(logo_wordmark, encoding="utf-8")

logo_heart = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="420" height="460" viewBox="0 0 420 460" role="img" aria-label="Botanical heart">
  <rect width="420" height="460" fill="none"/>
  <g fill="none" stroke="#8F2C3B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
    <path d="M210 400 C 130 330, 70 268, 70 196 C 70 138, 112 100, 162 100 C 188 100, 204 114, 210 134
             C 216 114, 232 100, 258 100 C 308 100, 350 138, 350 196 C 350 268, 290 330, 210 400 Z"/>
    <path d="M210 134 C 206 190, 208 250, 210 330"/>
    <path d="M210 210 C 180 190, 158 160, 166 132"/>
    <path d="M210 250 C 240 232, 262 208, 250 178"/>
    <path d="M210 300 C 184 288, 168 268, 174 244"/>
    <path d="M210 340 C 236 330, 252 310, 248 290"/>
  </g>
  <g fill="#8F2C3B">
    <ellipse cx="163" cy="128" rx="12" ry="5" transform="rotate(-38 163 128)"/>
    <ellipse cx="252" cy="174" rx="12" ry="5" transform="rotate(34 252 174)"/>
    <ellipse cx="171" cy="240" rx="11" ry="4.5" transform="rotate(-30 171 240)"/>
    <ellipse cx="250" cy="286" rx="11" ry="4.5" transform="rotate(24 250 286)"/>
  </g>
  <g fill="none" stroke="#8F2C3B" stroke-width="1.6">
    <circle cx="120" cy="150" r="3"/><circle cx="300" cy="150" r="3"/>
    <circle cx="120" cy="230" r="2.4"/><circle cx="300" cy="210" r="2.4"/>
  </g>
</svg>
"""
(LOGO / "botanical_heart.svg").write_text(logo_heart, encoding="utf-8")

logo_vine = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="700" height="1000" viewBox="0 0 700 1000" role="img" aria-label="Vine border">
  <g fill="none" stroke="#8F2C3B" stroke-width="2.2" stroke-linecap="round">
    <rect x="40" y="40" width="620" height="920" rx="10"/>
    <rect x="58" y="58" width="584" height="884" rx="6" stroke-width="1"/>
    <path d="M40 120 C 20 140, 20 180, 40 200"/>
    <path d="M660 120 C 680 140, 680 180, 660 200"/>
    <path d="M40 800 C 20 820, 20 860, 40 880"/>
    <path d="M660 800 C 680 820, 680 860, 660 880"/>
  </g>
  <g fill="none" stroke="#8F2C3B" stroke-width="1.8">
    <path d="M90 90 q 30 -30 60 0 q -30 30 -60 0"/>
    <path d="M610 90 q -30 -30 -60 0 q 30 30 60 0"/>
    <path d="M90 910 q 30 30 60 0 q -30 -30 -60 0"/>
    <path d="M610 910 q -30 30 -60 0 q 30 -30 60 0"/>
    <circle cx="120" cy="84" r="3"/><circle cx="580" cy="84" r="3"/>
    <circle cx="120" cy="916" r="3"/><circle cx="580" cy="916" r="3"/>
  </g>
</svg>
"""
(LOGO / "vine_border.svg").write_text(logo_vine, encoding="utf-8")

logo_plate = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="130" viewBox="0 0 200 130" role="img" aria-label="Number plate 26">
  <g fill="none" stroke="#7B5521" stroke-width="2">
    <path d="M14 46 Q14 26 40 26 L160 26 Q186 26 186 46 L186 84 Q186 104 160 104 L40 104 Q14 104 14 84 Z"/>
    <path d="M24 46 Q24 36 40 36 L160 36 Q176 36 176 46 L176 84 Q176 94 160 94 L40 94 Q24 94 24 84 Z" stroke-width="1"/>
  </g>
  <text x="100" y="84" text-anchor="middle" font-family="Georgia, serif" font-size="46"
        letter-spacing="2" fill="#FFF8EE">26</text>
</svg>
"""
(LOGO / "number_plate_26.svg").write_text(logo_plate, encoding="utf-8")
print("logo svgs ok")

# ---------------------------------------------------------------- parse bible tables
text = BIBLE.read_text(encoding="utf-8")

s51 = text.find("### 5.1")
s52 = text.find("### 5.2")
s53 = text.find("### 5.3")
s54 = text.find("### 5.4")
assert min(s51, s52, s53, s54) > 0

symbols = []
cls = ""
for ln in text[s51:s52].splitlines():
    m = re.match(r"^####\s*([ⅠⅡⅢⅣⅤⅥⅦⅧ])\s*(.+)$", ln.strip())
    if m:
        cls = m.group(1) + " " + m.group(2).strip()
        continue
    cells = [c.strip() for c in ln.strip().strip("|").split("|")]
    if len(cells) == 7 and re.fullmatch(r"\d{2}", cells[0]):
        symbols.append(dict(no=cells[0], name=cells[1], surface=cells[2], deep=cells[3],
                            emotion=cells[4], anim=cells[5], mode=cells[6], cls=cls))
print("symbols parsed:", len(symbols))

# border glyphs
borders = []
for ln in text[s52:s53].splitlines():
    cells = [c.strip() for c in ln.strip().strip("|").split("|")]
    if len(cells) == 6 and cells[0] and cells[0] not in ("符号",) and not set(cells[0]) <= set("-"):
        borders.append(dict(glyph=cells[0], meaning=cells[1], anim=cells[2]))
        borders.append(dict(glyph=cells[3], meaning=cells[4], anim=cells[5]))
print("border glyphs:", len(borders))

combos = []
for ln in text[s53:s54].splitlines():
    cells = [c.strip() for c in ln.strip().strip("|").split("|")]
    if len(cells) == 4 and cells[0] and cells[0] != "组合" and set(cells[0]) != {"-"}:
        combos.append(cells)
print("combos:", len(combos))

# ---------------------------------------------------------------- symbol CSVs
def en_split(name):
    """Names are stored as '中文 English' or 'English 中文' — split both orders."""
    m = re.match(r"^([A-Za-z][A-Za-z0-9'’\-\+&., ]*?)\s+([\u4e00-\u9fff].*)$", name)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    idx = None
    for i, ch in enumerate(name):
        if ("a" <= ch.lower() <= "z"):
            idx = i
            break
    if idx is not None and idx > 0:
        return name[idx:].strip(), name[:idx].strip()
    return name, name


mode_prompt = {
    "M1": "pink #F7C7C7 panel, warm cream #FAF2EC card border, berry red #8F2C3B ink only, minimal, sparse",
    "M2": "pale rose #FCE9EF card, crimson #B01F38 ink, mauve #D8A5B8 stage, heart-chain border",
    "M3": "rose #F6B7CC card, muted gold #7B5521 ink, double ornate border, corner ornaments",
    "M4": "bone #F7F2E6 paper, lampblack #14100F ink, dense etching, black environment",
}

sym_rows = []
for s in symbols:
    en, cn = en_split(s["name"])
    modes = s["mode"].replace(" ", "")
    primary = modes[:2] if len(modes) >= 2 else modes
    prompt = (f"{en}, single centered object, thin line art, {mode_prompt.get(primary, mode_prompt['M1'])}, "
              f"one object only, huge negative space, no text no letters, vintage letterpress print, "
              f"19th-century etching, occult tarot card illustration")
    sym_rows.append([s["no"], en, cn, s["cls"], s["mode"], s["surface"], s["deep"],
                     s["emotion"], s["anim"], prompt])
with (SYMS / "symbol_prompts.csv").open("w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["no", "name_en", "name_cn", "class", "modes", "surface", "metaphor",
                "emotion", "animation", "prompt_base"])
    w.writerows(sym_rows)

with (SYMS / "border_glyphs.csv").open("w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["glyph", "meaning", "animation", "where"])
    for b in borders:
        w.writerow([b["glyph"], b["meaning"], b["anim"], "M3 边框/侧饰带/角花，≤3mm，线宽0.07mm"])

with (SYMS / "combos.csv").open("w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["combination", "formula", "meaning", "example_copy"])
    w.writerows(combos)
print("csv ok")

# ---------------------------------------------------------------- symbol index sheet (A3 300dpi)
W, H = 3508, 4960
sheet = Image.new("RGB", (W, H), hex2rgb(P["page_white"]))
d = ImageDraw.Draw(sheet)


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


g_b = "C:/Windows/Fonts/georgiab.ttf"
g_r = "C:/Windows/Fonts/georgia.ttf"
msyh = "C:/Windows/Fonts/msyh.ttc"
f_title = font(g_r, 96)
f_sub = font(g_r, 38)
f_no = font(g_b, 44)
f_en = font(g_r, 40)
f_cn = font(msyh, 34)
f_badge = font(msyh, 28)

MARG = 150
d.text((MARG, 130), "NOT TAROT  ·  SYMBOL INDEX", font=f_title, fill=hex2rgb(P["brand_plum"]))
d.text((MARG, 262), "68 symbols / 8 classes  |  source: 01_style_bible/style_bible.md §5.1  |  v1.1 2026-10-24",
       font=f_sub, fill=hex2rgb(P["brand_plum"]))
d.line([(MARG, 330), (W - MARG, 330)], fill=hex2rgb(P["berry"]), width=3)
d.text((MARG, 352),
       "Ⅰ eyes  ·  Ⅱ heart & body  ·  Ⅲ crown & power  ·  Ⅳ animals  ·  Ⅴ cosmos  ·  Ⅵ objects  ·  Ⅶ thresholds  ·  Ⅷ signs",
       font=font(msyh, 30), fill=hex2rgb(P["berry"]))

COLS, ROWS = 3, 23
gw = (W - 2 * MARG) // COLS
gh = (H - 470 - 120) // ROWS
mode_col = {"M1": P["berry"], "M2": P["crimson"], "M3": P["gold"], "M4": P["lampblack"]}
for i, s in enumerate(symbols):
    c, r = i % COLS, i // COLS
    x = MARG + c * gw
    y = 470 + r * gh
    d.line([(x, y), (x + gw - 34, y)], fill=(210, 200, 195), width=1)
    d.text((x + 12, y + 18), f"#{s['no']}", font=f_no, fill=hex2rgb(P["berry"]))
    en, cn = en_split(s["name"])
    d.text((x + 120, y + 14), en[:34], font=f_en, fill=hex2rgb(P["brand_plum"]))
    d.text((x + 120, y + 64), s["cls"].split(" ", 1)[0] + "  " + cn[:12], font=f_cn,
           fill=hex2rgb(P["brand_plum"]))
    mlist = re.findall(r"M[1-4]", s["mode"])
    bw, gap = 52, 8
    bx = x + gw - 36 - (len(mlist) * bw + (len(mlist) - 1) * gap)
    for j, mo in enumerate(mlist):
        d.rectangle([bx + j * (bw + gap), y + 24, bx + j * (bw + gap) + bw, y + 70],
                    outline=hex2rgb(mode_col.get(mo, P["brand_plum"])), width=2)
        d.text((bx + j * (bw + gap) + 11, y + 34), mo, font=f_badge, fill=hex2rgb(P["brand_plum"]))

d.line([(MARG, H - 110), (W - MARG, H - 110)], fill=hex2rgb(P["berry"]), width=2)
d.text((MARG, H - 88), "USE: one symbol = one metaphor.  Max 2 main symbols per card.  Never invent unregistered symbols (R34).",
       font=font(msyh, 28), fill=hex2rgb(P["brand_plum"]))
sheet.save(SYMS / "symbol_index_sheet.png")
print("symbol sheet saved")

print("\nALL DONE")
