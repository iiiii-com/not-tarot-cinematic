# -*- coding: utf-8 -*-
"""Build the standalone HTML cinematic film:
   _tools/cinematic_template.html + embedded assets -> 07_final/NOT_TAROT_45s_cinematic.html
"""
import base64
import io
import json
import os
from PIL import Image

ROOT = r"E:/deepseek/PROJECT_MYSTIC_PROMO"
SPR = os.path.join(ROOT, "03_assets", "symbols", "sprites")
TEX = os.path.join(ROOT, "03_assets", "textures")
TPL = os.path.join(ROOT, "_tools", "cinematic_template.html")
OUT = os.path.join(ROOT, "07_final", "NOT_TAROT_45s_cinematic.html")

SPRITES = ["heart", "eye", "eye_tears", "butterfly", "tiger", "unicorn", "crown", "mirror",
           "compass", "hands", "wand", "skull", "moon", "cloud_eye", "scales", "question",
           "book", "key", "flower", "star", "snake", "hourglass", "arch", "candle", "scissors"]

VARIANTS = {
    "gold": (123, 85, 33),
    "bone": (247, 242, 230),
    "plum": (36, 31, 34),
}


def alpha_boost(im):
    # extracted line art is thin + low-alpha; lift it so 1px lines survive on screen
    lut = [min(255, int(255 * ((i / 255.0) ** 0.40) * 1.75)) for i in range(256)]
    im = im.copy()
    im.putalpha(im.split()[3].point(lut))
    return im


def data_uri(im, fmt="PNG", quality=92):
    buf = io.BytesIO()
    if fmt == "JPEG":
        im.convert("RGB").save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
        mime = "image/jpeg"
    else:
        im.save(buf, "PNG", optimize=True)
        mime = "image/png"
    b = base64.b64encode(buf.getvalue()).decode("ascii")
    return "data:%s;base64,%s" % (mime, b)


def tinted(im, color):
    out = Image.new("RGBA", im.size, color + (255,))
    out.putalpha(im.split()[3])
    return out


def main():
    sprites = {}
    for name in SPRITES:
        p = os.path.join(SPR, name + ".png")
        im = alpha_boost(Image.open(p).convert("RGBA"))
        sprites[name] = data_uri(im)
        for v, rgb in VARIANTS.items():
            sprites[name + "_" + v] = data_uri(tinted(im, rgb))
    papers = {}
    for key, fn in [("cream", "paper_cream.jpg"), ("env", "paper_env_black.jpg"),
                    ("rose", "paper_rose.jpg"), ("pageWhite", "paper_page_white.jpg")]:
        im = Image.open(os.path.join(TEX, fn)).convert("RGB")
        if im.width > 900:
            im = im.resize((900, 900), Image.LANCZOS)
        papers[key] = data_uri(im, "JPEG", quality=82)
    assets = {"sprites": sprites, "papers": papers}
    tpl = open(TPL, encoding="utf-8").read()
    blob = json.dumps(assets, ensure_ascii=False, separators=(",", ":"))
    html = tpl.replace("/*__ASSET_JSON__*/ {}", blob)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(html)
    print("built", OUT, "%.2f MB" % (os.path.getsize(OUT) / 1e6),
          "| sprites", len(sprites), "| papers", len(papers))


if __name__ == "__main__":
    main()
