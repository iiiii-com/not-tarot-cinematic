import re, time, json
from pathlib import Path
from PIL import Image
import numpy as np
import vtracer

try:
    from scipy import ndimage
    HAVE_SP = True
except Exception:
    HAVE_SP = False

ROOT = Path(r'E:\deepseek\PROJECT_MYSTIC_PROMO')
MOT = ROOT/'03_assets'/'concept_v3'/'motifs2'
OUT = ROOT/'03_assets'/'concept_v3'/'vec'
TMP = ROOT/'03_assets'/'concept_v3'/'vec'/'_tmp'
OUT.mkdir(parents=True, exist_ok=True); TMP.mkdir(parents=True, exist_ok=True)

def alpha_of(p):
    a = np.array(Image.open(p).convert('RGBA'))
    return a[:, :, 3].astype(np.float32)

def mask_from_alpha(alpha, scale, pct=0.20, min_thr=24, min_area=80):
    p99 = np.percentile(alpha[alpha > 0], 99) if (alpha > 0).any() else 255
    thr = max(min_thr, pct * p99)
    al = Image.fromarray(alpha.astype(np.uint8), 'L')
    al = al.resize((al.width * scale, al.height * scale), Image.LANCZOS)
    m = np.array(al) > thr
    if HAVE_SP:
        lab, n = ndimage.label(m)
        sizes = ndimage.sum(m, lab, range(1, n + 1))
        keep = np.zeros(n + 1, bool); keep[1:] = sizes >= min_area
        m = keep[lab]
    return m

def prep_mask_rgb(alpha, scale, pct=0.20, min_thr=24, min_area=80, ink=(20,16,15)):
    m = mask_from_alpha(alpha, scale, pct, min_thr, min_area)
    h, w = m.shape
    arr = np.full((h, w, 3), 255, np.uint8)
    arr[m] = ink
    return Image.fromarray(arr, 'RGB')

def round_svg(svg, nd=0):
    def rd(m):
        try:
            return str(int(round(float(m.group(0)))))
        except ValueError:
            return m.group(0)
    return re.sub(r'-?\d+\.\d+', rd, svg)

def postprocess(svg_text, ink_hex):
    def path_fix(m):
        tag = m.group(0)
        fm = re.search(r'fill="(#[0-9a-fA-F]{6})"', tag)
        if not fm:
            return tag
        col = fm.group(1).lower()
        r, g, b = int(col[1:3],16), int(col[3:5],16), int(col[5:7],16)
        if r > 235 and g > 235 and b > 235:
            return ''
        tm = re.sub(r'fill="#[0-9a-fA-F]{6}"', 'fill="%s"' % ink_hex, tag)
        dm = re.search(r'd="([^"]+)"', tm)
        if dm:
            d0 = dm.group(1)
            d1 = re.sub(r'\s+', ' ', round_svg(d0)).strip()
            tm = tm[:dm.start(1)] + d1 + tm[dm.end(1):]
        return tm
    svg = re.sub(r'<path\b[^>]*/>', path_fix, svg_text)
    svg = re.sub(r'<!--.*?-->', '', svg)
    svg = re.sub(r'<\?xml.*?\?>', '', svg)
    svg = re.sub(r'\n\s*', ' ', svg).strip()
    svg = re.sub(r'>\s+<', '><', svg)
    return svg

def trace_one(name, src, ink, scale, pct=0.20, min_thr=24, min_area=80):
    alpha = alpha_of(src)
    img = prep_mask_rgb(alpha, scale, pct, min_thr, min_area)
    tmp = TMP/f'_{name}.png'; img.save(tmp, optimize=True)
    raw = TMP/f'_{name}.svg'
    t0 = time.time()
    vtracer.convert_image_to_svg_py(str(tmp), str(raw))
    svg = postprocess(raw.read_text(encoding='utf-8'), '#%02X%02X%02X' % ink)
    out = OUT/f'{name}.svg'; out.write_text(svg, encoding='utf-8')
    print('%-16s %5d KB  %4.1fs  src %dx%d' % (name, out.stat().st_size/1024, time.time()-t0, img.width, img.height), flush=True)
    return out.stat().st_size

ICONS = ['ic_heart','ic_skull','ic_moon','ic_cloud_eye','ic_hands','ic_crown','ic_butterfly',
         'ic_tiger','ic_unicorn','ic_eye_tears','ic_book','ic_mirror','ic_compass','ic_wand','ic_dragon']
ENG = ['eng_eye_ink','eng_eye_wide_ink','eng_ouroboros_ink','eng_spider_ink','eng_moth_ink','eng_cloud_ink']
total = 0
for n in ICONS:
    total += trace_one(n, MOT/(n + '.png'), (143, 44, 59), 3)
for n in ENG:
    total += trace_one(n, MOT/(n + '.png'), (20, 16, 15), 1, pct=0.16, min_area=30)
print('TOTAL %.1f KB' % (total/1024))
