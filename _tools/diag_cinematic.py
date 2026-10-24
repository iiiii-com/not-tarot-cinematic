# -*- coding: utf-8 -*-
"""Diagnostics: capture specific absolute times from the HTML film, log JS errors."""
import os
import sys
from playwright.sync_api import sync_playwright

ROOT = r"E:/deepseek/PROJECT_MYSTIC_PROMO"
HTML = "file:///" + os.path.join(ROOT, "07_final", "NOT_TAROT_45s_cinematic.html").replace("\\", "/")
OUT = os.path.join(ROOT, "03_assets", "keyframes", "html_review")
CHROME = r"C:\Users\lenovo\AppData\Local\ms-playwright\chromium-1234\chrome-win64\chrome.exe"


def main():
    times = [float(x) for x in sys.argv[1:]] or [2.4, 5.0, 8.0, 12.0, 17.0, 19.5, 21.9, 33.0, 38.0, 41.0]
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        kw = dict(headless=True, args=["--force-color-profile=srgb", "--hide-scrollbars"])
        try:
            browser = p.chromium.launch(channel="msedge", **kw)
        except Exception:
            browser = p.chromium.launch(executable_path=CHROME, **kw)
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        page.on("console", lambda m: print("CONSOLE", m.type, m.text[:200]))
        page.on("pageerror", lambda e: print("PAGEERROR", str(e)[:400]))
        page.goto(HTML + "?capture=1", wait_until="load")
        page.wait_for_function("window.__rendered === true", timeout=60000)
        page.wait_for_timeout(300)
        for t in times:
            page.evaluate("t => window.__renderAt(t)", t)
            page.evaluate("() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
            path = os.path.join(OUT, "t%05.1f.jpg" % t)
            page.screenshot(path=path, type="jpeg", quality=92)
            print("shot", path)
        browser.close()


if __name__ == "__main__":
    main()
