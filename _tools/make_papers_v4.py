"""High-resolution paper textures for the v4 cinematic player.
Generates 1600x1600 print-paper tiles: mottled base, fibers, specks, faint laid lines.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
OUT = ROOT / "03_assets" / "textures"
OUT.mkdir(parents=True, exist_ok=True)
RNG = np.random.default_rng(20261024)
S = 1600


def smooth_noise(scale, seed):
    rng = np.random.default_rng(seed)
    small = rng.normal(0, 1, (max(4, S // scale), max(4, S // scale))).astype(np.float32)
    im = Image.fromarray(((small - small.min()) / (np.ptp(small) + 1e-6) * 255).astype(np.uint8))
    im = im.resize((S, S), Image.BICUBIC)
    return np.array(im, dtype=np.float32) / 255.0


def paper(base_rgb, dark_amt=1.0, seed=1, env=False):
    base = np.ones((S, S, 3), dtype=np.float32) * np.array(base_rgb, dtype=np.float32)
    mott = smooth_noise(240, seed) * 0.55 + smooth_noise(90, seed + 1) * 0.30 + smooth_noise(28, seed + 2) * 0.15
    mott = mott - mott.mean()
    base += (mott * (10 if env else 7) * dark_amt)[..., None]

    # fine grain
    grain = RNG.normal(0, 1.0, (S, S)).astype(np.float32)
    base += (grain * (2.0 if env else 2.6))[..., None]

    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im, "RGBA")

    # fibers: thin, short, mostly horizontal strands
    for _ in range(2600 if not env else 1400):
        x, y = RNG.uniform(0, S), RNG.uniform(0, S)
        ln = RNG.uniform(6, 34)
        ang = RNG.normal(0, 0.45)
        dx, dy = np.cos(ang) * ln, np.sin(ang) * ln
        v = int(RNG.integers(0, 40))
        col = (255, 250, 242, int(RNG.integers(8, 24))) if not env else (120, 110, 100, int(RNG.integers(6, 16)))
        d.line([(x, y), (x + dx, y + dy)], fill=col, width=1)
    # specks
    for _ in range(900 if not env else 500):
        x, y = RNG.uniform(0, S), RNG.uniform(0, S)
        r = RNG.uniform(0.4, 1.5)
        a = int(RNG.integers(10, 40))
        col = (90, 60, 45, a) if not env else (200, 188, 170, a)
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)

    # laid lines (very faint vertical chain lines, print paper feel)
    if not env:
        overlay = Image.new("L", (S, S), 0)
        od = ImageDraw.Draw(overlay)
        for x in range(0, S, 26):
            od.line([(x, 0), (x, S)], fill=int(RNG.integers(10, 20)), width=1)
        overlay = overlay.filter(ImageFilter.GaussianBlur(0.6))
        tint = Image.new("RGB", (S, S), (120, 96, 78))
        im = Image.composite(tint, im, overlay.point(lambda v: int(v * 0.9)))

    # soft irregular edge darkening for a plate-print feel
    if not env:
        yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
        cx, cy = S / 2, S / 2
        rr = np.sqrt(((xx - cx) / (S * 0.62)) ** 2 + ((yy - cy) / (S * 0.62)) ** 2)
        vig = np.clip((rr - 0.55) / 0.55, 0, 1) ** 1.6
        arr = np.array(im).astype(np.float32)
        arr -= vig[..., None] * 9
        im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return im


cream = paper((250, 242, 236), seed=11)
cream.save(OUT / "paper_cream_hi.jpg", quality=88, optimize=True)
envp = paper((11, 9, 8), dark_amt=1.6, seed=23, env=True)
envp.save(OUT / "paper_env_hi.jpg", quality=88, optimize=True)
print("cream", (OUT / "paper_cream_hi.jpg").stat().st_size // 1024, "KB")
print("env", (OUT / "paper_env_hi.jpg").stat().st_size // 1024, "KB")
