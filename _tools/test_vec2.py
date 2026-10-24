import re, io, base64, time
from pathlib import Path
from PIL import Image
import numpy as np
import vtracer

ROOT = Path(r'E:\deepseek\PROJECT_MYSTIC_PROMO')
MOT = ROOT/'03_assets'/'concept_v3'/'motifs2'
OUT = ROOT/'03_assets'/'concept_v3'/'vec_test'
OUT.mkdir(parents=True, exist_ok=True)

def prep(p, scale=3, ink=(20,16,15)):
    im = Image.open(p).convert('RGBA')
    a = np.array(im); alpha = a[:,:,3].astype(np.float32)/255.0
    ink_arr = np.zeros((*alpha.shape,3), np.uint8); ink_arr[:,:] = ink
    white = np.full((*alpha.shape,3), 255, np.uint8)
    comp = (ink_arr*alpha[...,None] + white*(1-alpha[...,None])).astype(np.uint8)
    im2 = Image.fromarray(comp, 'RGB')
    if scale != 1:
        im2 = im2.resize((im2.width*scale, im2.height*scale), Image.LANCZOS)
    return im2

def postprocess(svg_text, ink_hex):
    # drop near-white fills (background), recolor remaining fills to ink
    def fix(m):
        col = m.group(2).lower()
        r,g,b = int(col[1:3],16), int(col[3:5],16), int(col[5:7],16)
        return '' if (r>235 and g>235 and b>235) else f'{m.group(1)}{ink_hex}'
    s = re.sub(r'(fill=")(#[0-9a-fA-F]{6})(")', fix, svg_text)
    # remove empty paths left behind
    s = re.sub(r'<path[^>]*fill="[^"]*"[^>]*/>', lambda m: m.group(0) if 'd="' in m.group(0) else '', s)
    s = re.sub(r'\n\s*', ' ', s)
    return s

def trace(p, name, scale=2, ink=(143,44,59), **kw):
    src = prep(p, scale, ink if False else (20,16,15))
    tmp = OUT/f'_{name}_src.png'; src.save(tmp)
    raw = OUT/f'_{name}_raw.svg'
    t0=time.time()
    vtracer.convert_image_to_svg_py(str(tmp), str(raw), colormode='color', **kw)
    s = raw.read_text(encoding='utf-8')
    s = postprocess(s, '#%02X%02X%02X' % ink)
    out = OUT/f'{name}.svg'
    out.write_text(s, encoding='utf-8')
    print(f'{name}: raw {raw.stat().st_size/1024:.0f}KB -> final {out.stat().st_size/1024:.1f}KB in {time.time()-t0:.1f}s')
    return out

common = dict(hierarchical='stacked', mode='spline', color_precision=2, filter_speckle=6,
              corner_threshold=60, length_threshold=3.0, max_iterations=10, splice_threshold=45, path_precision=2)
trace(MOT/'ic_heart.png', 'heart_v', scale=3, ink=(143,44,59), **common)
trace(MOT/'eng_eye_ink.png', 'eng_eye_v', scale=2, ink=(20,16,15), **common)
trace(MOT/'eng_spider_ink.png', 'eng_spider_v', scale=2, ink=(20,16,15), **common)
trace(MOT/'ic_eye_tears.png', 'eye_tears_v', scale=3, ink=(143,44,59), **common)
print('files:', [ (p.name, round(p.stat().st_size/1024,1)) for p in sorted(OUT.glob('*_v.svg')) ])
