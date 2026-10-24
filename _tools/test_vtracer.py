import io, base64, time
from pathlib import Path
from PIL import Image
import numpy as np
import vtracer

ROOT = Path(r'E:\deepseek\PROJECT_MYSTIC_PROMO')
MOT = ROOT/'03_assets'/'concept_v3'/'motifs2'
OUT = ROOT/'03_assets'/'concept_v3'/'vec_test'
OUT.mkdir(parents=True, exist_ok=True)

def prep(p, scale=3, ink=(143,44,59)):
    im = Image.open(p).convert('RGBA')
    a = np.array(im)
    alpha = a[:,:,3].astype(np.float32)/255.0
    ink_arr = np.zeros((*alpha.shape,3), np.uint8); ink_arr[:,:] = ink
    white = np.full((*alpha.shape,3), 255, np.uint8)
    comp = (ink_arr*alpha[...,None] + white*(1-alpha[...,None])).astype(np.uint8)
    im2 = Image.fromarray(comp, 'RGB')
    im2 = im2.resize((im2.width*scale, im2.height*scale), Image.LANCZOS)
    return im2

def trace(src, name, **kw):
    t0=time.time()
    out = OUT/f'{name}.svg'
    vtracer.convert_image_to_svg_py(str(src), str(out), colormode='binary', **kw)
    sz = out.stat().st_size/1024
    print(f'{name}: {sz:.1f} KB in {time.time()-t0:.2f}s', kw)
    return out

# icon heart
p = MOT/'ic_heart.png'
im = prep(p, 3)
im.save(OUT/'ic_heart_white3x.png')
trace(OUT/'ic_heart_white3x.png', 'ic_heart_spline', mode='spline', filter_speckle=6, corner_threshold=60, length_threshold=3.0, path_precision=2)
trace(OUT/'ic_heart_white3x.png', 'ic_heart_poly', mode='polygon', filter_speckle=4, path_precision=1)

# engraving eye
p = MOT/'eng_eye_ink.png'
im = prep(p, 2, ink=(20,16,15))
im.save(OUT/'eng_eye_white2x.png')
trace(OUT/'eng_eye_white2x.png', 'eng_eye_fine', mode='spline', filter_speckle=3, corner_threshold=60, length_threshold=3.0, path_precision=2)
trace(OUT/'eng_eye_white2x.png', 'eng_eye_coarse', mode='spline', filter_speckle=8, corner_threshold=70, length_threshold=6.0, path_precision=1)
print('done')
