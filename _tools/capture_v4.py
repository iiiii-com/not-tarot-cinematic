import sys, time, math
from pathlib import Path
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = Path(r'E:\deepseek\PROJECT_MYSTIC_PROMO')
HTML = ROOT/'07_final'/'NOT_TAROT_45s_v4.html'
URL = HTML.as_uri()
KF = ROOT/'03_assets'/'keyframes_v4'
KF.mkdir(parents=True, exist_ok=True)
TIMES = [0,2.6,8.0,14.0,17.5,22.0,24.5,26.0,27.5,29.0,30.5,32.0,33.5,36.0,40.0,42.0,43.5]
REPS = [1.4,6.4,11.0,16.2,20.4,23.4,25.7,27.1,28.6,30.0,31.5,33.0,35.0,38.4,41.2,43.1,44.5]
DPR = 2


def open_page(p, w, h, vertical=False, dpr=DPR):
    b = p.chromium.launch(channel='msedge', headless=True)
    pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=dpr)
    q = '?capture=1' + ('&vertical=1' if vertical else '')
    pg.goto(URL + q)
    pg.wait_for_function('window.__rendered === true')
    pg.wait_for_function('document.fonts.status === "loaded"')
    pg.wait_for_timeout(500)
    return b, pg


def review():
    with sync_playwright() as p:
        b, pg = open_page(p, 1920, 1080, dpr=1)
        shots = []
        for i, t in enumerate(REPS):
            pg.evaluate(f'window.__renderAt({t})')
            pg.wait_for_timeout(90)
            f = KF/f'S{i+1:02d}.jpg'
            pg.screenshot(path=str(f), clip={'x': 0, 'y': 0, 'width': 1920, 'height': 1080}, type='jpeg', quality=90)
            shots.append(f)
            print('shot', i+1, t, 'ok')
        b.close()
    cols, tw, th = 3, 640, 360
    rows = math.ceil(len(shots)/cols)
    sheet = Image.new('RGB', (cols*tw, rows*th), (23, 18, 20))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(shots):
        im = Image.open(f).convert('RGB').resize((tw, th), Image.LANCZOS)
        x, y = (i % cols)*tw, (i//cols)*th
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x+tw-1, y+th-1], outline=(120, 96, 82))
        d.text((x+10, y+8), f'{i+1:02d}  t={REPS[i]}s', fill=(247, 242, 230))
    out = KF/'review_sheet.jpg'
    sheet.save(out, quality=88)
    print('review sheet', out)


def frames(vertical=False):
    w, h = (1080, 1920) if vertical else (1920, 1080)
    dpr = DPR
    tag = '9x16' if vertical else '16x9'
    outdir = ROOT/'07_final'/'_render_v4'/f'frames_{tag}'
    outdir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b, pg = open_page(p, w, h, vertical=vertical, dpr=dpr)
        t0 = time.time()
        for i in range(1080):
            t = i/24.0
            pg.evaluate(f'window.__renderAt({t})')
            pg.screenshot(path=str(outdir/f'frame_{i+1:05d}.jpg'), type='jpeg', quality=92)
            if i % 180 == 0:
                print(tag, 'frame', i, f'{time.time()-t0:.1f}s', flush=True)
        b.close()
    print(tag, 'frames done', f'{time.time()-t0:.1f}s')


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'review'
    if mode == 'review':
        review()
    elif mode == 'frames':
        frames(vertical=False)
    elif mode == 'frames9':
        frames(vertical=True)
