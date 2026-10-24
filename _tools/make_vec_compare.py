from pathlib import Path
import base64
ROOT = Path(r'E:\deepseek\PROJECT_MYSTIC_PROMO')
V = ROOT/'03_assets'/'concept_v3'/'vec_test'
M = ROOT/'03_assets'/'concept_v3'/'motifs2'
def b64(p):
    return 'data:image/svg+xml;base64,' + base64.b64encode(p.read_bytes()).decode()
rows = [('heart_v.svg','ic_heart.png',520),('eye_tears_v.svg','ic_eye_tears.png',520),
        ('eng_eye_v.svg','eng_eye_ink.png',760),('eng_spider_v.svg','eng_spider_ink.png',640)]
cells = []
for svg, png, h in rows:
    cells.append(f'''<div style="display:inline-block;margin:10px;text-align:center;vertical-align:top">
      <div style="width:900px;background:#FAF2EC;padding:10px">
        <img src="{b64(V/svg)}" style="height:{h}px">
      </div>
      <div style="margin-top:6px;font:12px monospace;color:#8F2C3B">{svg}</div></div>''')
html = '<html><body style="background:#241F22;margin:0;padding:20px">' + ''.join(cells) + '</body></html>'
(ROOT/'_tools'/'_vec_compare.html').write_text(html, encoding='utf-8')
print('ok', len(html))
