# -*- coding: utf-8 -*-
"""Offline capture of the HTML cinematic film.

  python _tools/capture_cinematic.py review          -> 18 storyboard-time stills + contact sheet
  python _tools/capture_cinematic.py frames 16x9     -> 1080 jpg frames at 24 fps
  python _tools/capture_cinematic.py frames 9x16
"""
import os
import sys
import time
from playwright.sync_api import sync_playwright

ROOT = r"E:/deepseek/PROJECT_MYSTIC_PROMO"
HTML = "file:///" + os.path.join(ROOT, "07_final", "NOT_TAROT_45s_cinematic.html").replace("\\", "/")
OUT = os.path.join(ROOT, "07_final", "_render_dir_hq")
KF = os.path.join(ROOT, "03_assets", "keyframes")
FPS = 24
TOTAL = 1080
CHROME = r"C:\Users\lenovo\AppData\Local\ms-playwright\chromium-1234\chrome-win64\chrome.exe"
CHROME = CHROME if os.path.exists(CHROME) else None


def launch(p):
    kwargs = dict(headless=True, args=["--force-color-profile=srgb", "--hide-scrollbars",
                                       "--disable-lcd-text"])
    try:
        return p.chromium.launch(channel="msedge", **kwargs)
    except Exception:
        if CHROME:
            return p.chromium.launch(executable_path=CHROME, **kwargs)
        raise


def open_page(browser, w, h, vertical=False):
    page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
    page.goto(HTML + ("?capture=1&vertical=1" if vertical else "?capture=1"), wait_until="load")
    page.wait_for_function("window.__rendered === true", timeout=60000)
    page.wait_for_timeout(250)
    return page


def shot(page, t, path):
    page.evaluate("t => window.__renderAt(t)", t)
    page.evaluate("() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
    page.screenshot(path=path, type="jpeg", quality=94)


def review(browser):
    page = open_page(browser, 1920, 1080)
    reps = {"S01a": 0.9, "S01b": 3.6, "S02a": 5.2, "S02b": 9.4, "S03": 13.0,
            "S04a": 17.6, "S04b": 19.8, "S05a": 21.9, "S05b": 23.4, "S05c": 24.9,
            "S05d": 26.4, "S05e": 27.9, "S05f": 29.4, "S06a": 30.9, "S06b": 34.5,
            "S06c": 37.6, "S07a": 40.7, "S07b": 44.2}
    times = [(sid, t) for sid, t in reps.items()]
    outdir = os.path.join(KF, "html_review")
    os.makedirs(outdir, exist_ok=True)
    for sid, t in times:
        shot(page, t, os.path.join(outdir, sid + ".jpg"))
        print("review", sid, t)
    page.close()
    make_sheet(outdir, [s for s, _ in times])


def make_sheet(outdir, order):
    from PIL import Image, ImageDraw, ImageFont
    cols, rows = 3, 6
    tw, th, lh = 640, 360, 26
    sheet = Image.new("RGB", (cols * tw, rows * (th + lh)), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(r"C:/Windows/Fonts/arial.ttf", 18)
    for i, sid in enumerate(order):
        im = Image.open(os.path.join(outdir, sid + ".jpg")).convert("RGB").resize((tw, th), Image.LANCZOS)
        r, c = divmod(i, cols)
        x, y = c * tw, r * (th + lh)
        sheet.paste(im, (x, y))
        d.text((x + 8, y + th + 3), sid, font=font, fill=(20, 20, 20))
    p = os.path.join(outdir, "contact_sheet.jpg")
    sheet.save(p, quality=90)
    print("sheet", p)


def frames(browser, fmt):
    if fmt == "16x9":
        w, h = 1920, 1080
    else:
        w, h = 1080, 1920
    page = open_page(browser, w, h, vertical=(fmt != "16x9"))
    out = os.path.join(OUT, "frames_" + fmt)
    os.makedirs(out, exist_ok=True)
    t0 = time.time()
    for i in range(TOTAL):
        t = i / FPS
        page.evaluate("t => window.__renderAt(t)", t)
        page.evaluate("() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
        page.screenshot(path=os.path.join(out, "frame_%05d.jpg" % (i + 1)),
                        type="jpeg", quality=95)
        if (i + 1) % 120 == 0:
            el = time.time() - t0
            print(fmt, i + 1, "/", TOTAL, "%.1fs" % el, flush=True)
    page.close()
    print("done", fmt, "%.1fs" % (time.time() - t0))


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "review"
    with sync_playwright() as p:
        browser = launch(p)
        try:
            if mode == "review":
                review(browser)
            elif mode == "frames":
                frames(browser, sys.argv[2] if len(sys.argv) > 2 else "16x9")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
