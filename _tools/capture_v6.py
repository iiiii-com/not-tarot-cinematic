"""Capture v5 magazine film frames with Playwright/Edge at DPR2."""
import sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
HTML = ROOT / "07_final" / "NOT_TAROT_45s_v6.html"
FPS, DUR = 24, 45
N = FPS * DUR


def run(vert: bool):
    tag = "frames_9x16" if vert else "frames_16x9"
    out = ROOT / "07_final" / "_render_v6" / tag
    out.mkdir(parents=True, exist_ok=True)
    vw, vh = (1080, 1920) if vert else (1920, 1080)
    url = HTML.as_uri() + "?capture=1" + ("&vert=1" if vert else "")
    with sync_playwright() as p:
        br = p.chromium.launch(channel="msedge")
        pg = br.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=2)
        pg.goto(url, wait_until="load")
        pg.wait_for_function("window.__rendered===true", timeout=20000)
        pg.wait_for_timeout(300)
        t0 = time.time()
        for i in range(N):
            t = i / FPS
            pg.evaluate(f"window.__renderAt({t:.5f})")
            pg.screenshot(path=str(out / f"frame_{i+1:05d}.jpg"), type="jpeg", quality=92)
            if i % 180 == 0:
                print(tag, "frame", i, f"{time.time()-t0:.1f}s", flush=True)
        br.close()
    print(tag, "done", f"{time.time()-t0:.1f}s", flush=True)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("both", "16x9"):
        run(False)
    if which in ("both", "9x16"):
        run(True)
