import base64, io, json, re
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(r'E:\deepseek\PROJECT_MYSTIC_PROMO')
TPL = ROOT/'_tools'/'cinematic_v3_template.html'
OUT = ROOT/'07_final'/'NOT_TAROT_45s_v3.html'
MOT = ROOT/'03_assets'/'concept_v3'/'motifs2'

def data_uri(img, fmt='PNG', maxpx=900, q=90):
    im = img.copy()
    if max(im.size) > maxpx:
        r = maxpx/max(im.size)
        im = im.resize((max(1,int(im.width*r)), max(1,int(im.height*r))), Image.LANCZOS)
    buf = io.BytesIO()
    if fmt == 'PNG':
        im.save(buf, 'PNG', optimize=True)
        return 'data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
    im.convert('RGB').save(buf, 'JPEG', quality=q, optimize=True)
    return 'data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()

def clean_icon(im):
    a = np.array(im.convert('RGBA'))
    alpha = np.clip((a[:, :, 3].astype(np.float32) - 42) * 2.35, 0, 255)
    h, w = alpha.shape
    for y in range(h):
        m = alpha[y] > 30
        best = run = 0
        for v in m:
            run = run + 1 if v else 0
            best = max(best, run)
        if best > 0.72 * w:
            alpha[y, :] = 0
    for x in range(w):
        m = alpha[:, x] > 30
        best = run = 0
        for v in m:
            run = run + 1 if v else 0
            best = max(best, run)
        if best > 0.72 * h:
            alpha[:, x] = 0
    a[:, :, 3] = alpha.astype(np.uint8)
    out = Image.fromarray(a, 'RGBA')
    bw, bh = out.size
    out = out.crop((int(bw*0.035), int(bh*0.035), int(bw*0.965), int(bh*0.965)))
    return out

def tint_icon(im, rgb=(143, 44, 59)):
    a = np.array(im)
    a[:, :, 0] = rgb[0]; a[:, :, 1] = rgb[1]; a[:, :, 2] = rgb[2]
    return Image.fromarray(a, 'RGBA')

def load_png(p):
    return Image.open(p).convert('RGBA')

assets = {}
# icons + engraving motifs
for p in sorted(MOT.glob('ic_*.png')):
    assets[p.stem] = data_uri(tint_icon(clean_icon(load_png(p))))
for p in sorted(MOT.glob('eng_*_ink.png')):
    assets[p.stem] = data_uri(load_png(p), maxpx=1200)
# aliases used by the film
if 'ic_heart' in assets: assets['icon_heart'] = assets['ic_heart']
if 'eng_eye_ink' in assets: assets['eng_eye'] = assets['eng_eye_ink']
if 'eng_cloud_ink' in assets: assets['eng_cloud'] = assets['eng_cloud_ink']

SVG = {
 'scissors_sym': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><g fill="none" stroke="#8F2C3B" stroke-width="5" stroke-linecap="round"><circle cx="52" cy="150" r="20"/><circle cx="148" cy="150" r="20"/><path d="M66 60 L134 138 M134 60 L66 138 M100 100 L100 60 M88 52 L100 40 L112 52"/></g></svg>''',
 'flower_sym': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><g fill="none" stroke="#8F2C3B" stroke-width="5" stroke-linecap="round"><path d="M100 132 C100 168 92 186 78 196"/><circle cx="100" cy="72" r="26"/><circle cx="138" cy="98" r="26"/><circle cx="128" cy="140" r="26"/><circle cx="72" cy="140" r="26"/><circle cx="62" cy="98" r="26"/><circle cx="100" cy="100" r="10"/></g></svg>''',
}
for k, svg in SVG.items():
    assets[k] = 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()

tex = {}
paper = ROOT/'03_assets'/'textures'/'paper_cream.jpg'
im = Image.open(paper)
im.thumbnail((1100, 1100), Image.LANCZOS)
buf = io.BytesIO(); im.convert('RGB').save(buf, 'JPEG', quality=82, optimize=True)
tex['paper'] = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

tpl = TPL.read_text(encoding='utf-8')
html = tpl.replace('/*__ASSETS__*/{}', json.dumps(assets, ensure_ascii=False))
html = html.replace('/*__TEXTURES__*/{}', json.dumps(tex, ensure_ascii=False))
OUT.write_text(html, encoding='utf-8')

# extract inline JS for syntax check
js = re.search(r'<script>(.*)</script>', html, re.S).group(1)
(ROOT/'_tools'/'_tmp_v3_check.js').write_text(js, encoding='utf-8')
print('built', OUT, f'{OUT.stat().st_size/1e6:.2f} MB', 'assets', len(assets))
