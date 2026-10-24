"""Review v5 magazine HTML: load, render keyframes, report errors, make contact sheet."""
import sys, json, time
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
HTML = ROOT / "07_final" / "NOT_TAROT_45s_v6.html"
OUT = ROOT / "03_assets" / "keyframes_v6"
OUT.mkdir(parents=True, exist_ok=True)
TIMES = [1.0, 3.0, 5.6, 7.8, 11.0, 13.2, 15.4, 17.6, 20.2, 22.2, 24.6, 26.8, 28.4, 30.6, 33.2, 35.6, 38.6, 41.6, 44.2]
VERT = len(sys.argv) > 1 and sys.argv[1] == "vert"


def main():
    errs = []
    with sync_playwright() as p:
        br = p.chromium.launch(channel="msedge")
        vw, vh = (1080, 1920) if VERT else (1920, 1080)
        pg = br.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=1)
        pg.on("console", lambda m: errs.append("console:" + m.type + ":" + m.text) if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: errs.append("pageerror:" + str(e)))
        url = HTML.as_uri() + "?capture=1" + ("&vert=1" if VERT else "")
        pg.goto(url, wait_until="load")
        try:
            pg.wait_for_function("window.__rendered===true", timeout=20000)
        except Exception as e:
            errs.append("rendered timeout:" + str(e))
        pg.wait_for_timeout(400)
        files = []
        for i, t in enumerate(TIMES):
            pg.evaluate(f"window.__renderAt({t})")
            pg.wait_for_timeout(90)
            f = OUT / (("v_" if VERT else "") + f"kf_{i}_{t:05.2f}.jpg")
            pg.screenshot(path=str(f), type="jpeg", quality=88)
            files.append(f)
        br.close()
    print("errors:", errs[:10])
    # contact sheet 4x3
    ims = [Image.open(f).convert("RGB") for f in files]
    tw = 384
    th = int(tw * ims[0].height / ims[0].width)
    cols = 5
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (18, 15, 16))
    for i, im in enumerate(ims):
        im = im.resize((tw, th), Image.LANCZOS)
        sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
    out = OUT / (("review_sheet_vert.jpg" if VERT else "review_sheet.jpg"))
    sheet.save(out, quality=88)
    print("sheet", out)


if __name__ == "__main__":
    main()
