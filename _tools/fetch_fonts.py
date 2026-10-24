# -*- coding: utf-8 -*-
"""Fetch OFL webfonts from Google Fonts (latin woff2) into a cache dir.

Used by build_cinematic_v4.py so the standalone HTML can embed real brand type
(Cormorant / EB Garamond / Jost / IM Fell) without a network dependency at play time.
"""
import os
import re
import urllib.request

CACHE = os.environ.get("NT_FONT_CACHE", r"E:/deepseek/review_out/fonts")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

FAMILIES = [
    # key, google css family string, weights
    ("playfair", "Playfair+Display:wght@500;600;700"),
    ("cormorant", "Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400"),
    ("ebgaramond", "EB+Garamond:ital,wght@0,400;0,500;1,400"),
    ("jost", "Jost:wght@300;400;500"),
    ("fell", "IM+Fell+English+SC"),
    ("pinyon", "Pinyon+Script"),
]


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout).read()


def latin_blocks(css):
    """Return [(style, weight, url)] for the /* latin */ blocks."""
    out = []
    for m in re.finditer(r"@font-face\s*\{(.*?)\}", css, re.S):
        body = m.group(1)
        if "U+0000-00FF" not in body:
            continue
        fam = re.search(r"font-family:\s*'([^']+)'", body)
        sty = re.search(r"font-style:\s*(\w+)", body)
        wgt = re.search(r"font-weight:\s*(\d+)", body)
        url = re.search(r"url\((https://[^)]+\.woff2)\)", body)
        if not (fam and url):
            continue
        out.append({
            "family": fam.group(1),
            "style": (sty.group(1) if sty else "normal"),
            "weight": int(wgt.group(1)) if wgt else 400,
            "url": url.group(1),
        })
    return out


def main():
    os.makedirs(CACHE, exist_ok=True)
    manifest = []
    total = 0
    for key, fam in FAMILIES:
        css_url = "https://fonts.googleapis.com/css2?family=" + fam + "&display=swap"
        css = fetch(css_url).decode("utf-8")
        for blk in latin_blocks(css):
            name = "%s_%s_%d.woff2" % (key, blk["style"], blk["weight"])
            path = os.path.join(CACHE, name)
            if not os.path.exists(path):
                data = fetch(blk["url"])
                with open(path, "wb") as f:
                    f.write(data)
            size = os.path.getsize(path)
            total += size
            manifest.append({"key": key, "family": blk["family"], "style": blk["style"],
                             "weight": blk["weight"], "file": name, "size": size})
            print("%-34s %-20s %s %4d %8.1f KB" % (name, blk["family"], blk["style"],
                                                   blk["weight"], size / 1024))
    print("total %.1f KB  (%d files) -> %s" % (total / 1024, len(manifest), CACHE))


if __name__ == "__main__":
    main()
