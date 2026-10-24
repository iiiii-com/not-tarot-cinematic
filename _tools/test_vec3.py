import re, time
from pathlib import Path
from PIL import Image
import numpy as np
import vtracer

ROOT = Path(r'E:\deepseek\PROJECT_MYSTIC_PROMO')
MOT = ROOT/'03_assets'/'concept_v3'/'motifs2'
OUT = ROOT/'03_assets'/'concept_v3'/'vec_test'
OUT.mkdir(parents=True, exist_ok=True)

def prep_mask(p, scale=2, dark=(20,16,15), thr=110):
    im = Image.open(p).convert('RGBA')
    a = np.array(im)
    alpha = a[:,:,3].astype(np.float32)
    al = Image.fromarray(alpha.astype(np.uint8), 'L')
    al = al.resize((al.width*scale, al.height*scale), Image.LANCZOS)
    m = (np.array(al) > thr)
    h, w = m.shape
    arr = np.full((h, w, 3), 255, np.uint8)
    arr[m] = dark
    return Image.fromarray(arr, 'RGB')

def postprocess(svg_text, ink_hex):
    def path_fix(m):
        tag = m.group(0)
        fm = re.search(r'fill="(#[0-9a-fA-F]{6})"', tag)
        if not fm:
            return tag
        col = fm.group(1).lower()
        r, g, b = int(col[1:3],16), int(col[3:5],16), int(col[5:7],16)
        if r > 235 and g > 235 and b > 235:
            return ''  # drop near-white background path
        return re.sub(r'fill="#[0-9a-fA-F]{6}"', 'fill="%s"' % ink_hex, tag)
    svg = re.sub(r'<path\b[^>]*/>', path_fix, svg_text)
    svg = re.sub(r'\n\s*', ' ', svg)
    return svg

def trace(p, name, scale=2, ink=(143,44,59), thr=110):
    src = prep_mask(p, scale, (20,16,15), thr)
    tmp = OUT / ('_' + name + '_src.png'); src.save(tmp, optimize=True)
    raw = OUT / ('_' + name + '_raw.svg')
    t0 = time.time()
    vtracer.convert_image_to_svg_py(str(tmp), str(raw))
    svg = postprocess(raw.read_text(encoding='utf-8'), '#%02X%02X%02X' % ink)
    out = OUT / (name + '.svg'); out.write_text(svg, encoding='utf-8')
    print(name, src.size, 'raw %.0fKB -> %.1fKB %.1fs' % (raw.stat().st_size/1024, out.stat().st_size/1024, time.time()-t0), flush=True)
    return out

trace(MOT/'ic_heart.png', 'heart_v', scale=2, ink=(143,44,59), thr=120)
trace(MOT/'ic_eye_tears.png', 'eye_tears_v', scale=2, ink=(143,44,59), thr=120)
trace(MOT/'eng_eye_ink.png', 'eng_eye_v', scale=1, ink=(20,16,15), thr=60)
trace(MOT/'eng_spider_ink.png', 'eng_spider_v', scale=1, ink=(20,16,15), thr=60)
print('first80:', (OUT/'heart_v.svg').read_text(encoding='utf-8')[:160])
print('done')
