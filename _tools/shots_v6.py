import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
HTML = ROOT / "07_final" / "NOT_TAROT_45s_v6.html"
OUT = ROOT / "03_assets" / "keyframes_v6" / "pages"; OUT.mkdir(parents=True, exist_ok=True)
TIMES = [2.0, 7.8, 13.2, 17.6, 20.2, 26.8, 30.6, 35.6, 38.6, 41.6, 44.2]
with sync_playwright() as p:
    br = p.chromium.launch(channel="msedge")
    pg = br.new_page(viewport={"width":1920,"height":1080}, device_scale_factor=1)
    errs=[]
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(HTML.as_uri()+"?capture=1", wait_until="load")
    pg.wait_for_function("window.__rendered===true", timeout=20000)
    pg.wait_for_timeout(300)
    for t in TIMES:
        pg.evaluate(f"window.__renderAt({t})"); pg.wait_for_timeout(80)
        pg.screenshot(path=str(OUT/f"p_{t:05.2f}.png"))
    br.close()
print("errs", errs[:5]); print("done")
