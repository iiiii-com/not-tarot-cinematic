import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(r'E:\deepseek\PROJECT_MYSTIC_PROMO')
html = (ROOT/'07_final'/'NOT_TAROT_45s_v3.html').as_uri()
out = ROOT/'03_assets'/'keyframes_v3'/'diag'
out.mkdir(parents=True, exist_ok=True)
TIMES = [1.2, 6.4, 12.0, 16.0, 25.7, 38.4]
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge', headless=True)
    for w,h,tag in [(1366,768,'1366x768'),(2560,1440,'2560x1440')]:
        pg = b.new_page(viewport={'width':w,'height':h}, device_scale_factor=1)
        pg.goto(html); pg.wait_for_function('window.__rendered===true'); pg.wait_for_timeout(300)
        pg.mouse.click(w//2, h//2); pg.wait_for_timeout(200)
        for t in TIMES:
            pg.evaluate(f'window.__renderAt({t})'); pg.wait_for_timeout(150)
            pg.screenshot(path=str(out/f'{tag}_t{t}.jpg'), type='jpeg', quality=88)
        print(tag, 'done')
        pg.close()
    b.close()
