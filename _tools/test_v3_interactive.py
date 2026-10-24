from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(r'E:\deepseek\PROJECT_MYSTIC_PROMO')
html = (ROOT/'07_final'/'NOT_TAROT_45s_v3.html').as_uri()
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge', headless=True)
    pg = b.new_page(viewport={'width':1280,'height':800})
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(html); pg.wait_for_timeout(700)
    pg.mouse.click(640, 400)              # start (poster)
    pg.wait_for_timeout(1400)
    tc = pg.inner_text('#tc'); print('tc after start:', tc)
    pg.evaluate('document.querySelectorAll(".chap")[3].click()')  # jump to act 04
    pg.wait_for_timeout(300); print('tc after chapter jump:', pg.inner_text('#tc'))
    pg.evaluate('window.__renderAt(25.6)')  # first card
    pg.wait_for_timeout(200)
    pg.evaluate('document.querySelectorAll("#scenes > div")[6].querySelector("div").click()')  # flip card
    pg.wait_for_timeout(200)
    pg.evaluate('window.__renderAt(44.0); document.getElementById("draw").classList.add("show")')
    pg.wait_for_timeout(200)
    pg.evaluate('document.getElementById("dBtn").click()')
    pg.wait_for_timeout(300)
    print('draw visible:', pg.is_visible('#draw'), '| dname:', pg.inner_text('#dname'))
    pg.screenshot(path=str(ROOT/'03_assets'/'keyframes_v3'/'interactive_test.jpg'), type='jpeg', quality=85)
    print('JS errors:', errs if errs else 'none')
    b.close()

