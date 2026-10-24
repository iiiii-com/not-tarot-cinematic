# -*- coding: utf-8 -*-
"""Verify director cut doc + CSV: shot count, columns, timing continuity, duration."""
import csv, re, sys, io

ROOT = r"E:\deepseek\PROJECT_MYSTIC_PROMO"
DOC = ROOT + r"\02_storyboard\storyboard_45s_director_cut.md"
CSV = ROOT + r"\02_storyboard\shot_list_director_cut.csv"

text = io.open(DOC, encoding="utf-8").read()
lines = text.splitlines()

# locate section 4 table
start = next(i for i, l in enumerate(lines) if l.startswith("## 4."))
end = next(i for i, l in enumerate(lines) if l.startswith("## 5."))
sec = lines[start:end]

table_rows = []
header = None
for l in sec:
    if not l.startswith("|"):
        continue
    cells = [c.strip() for c in l.strip().strip("|").split("|")]
    if set("".join(cells)) <= set("-: "):
        continue
    if header is None:
        header = cells
    else:
        table_rows.append(cells)

print("S4 header cells:", len(header))
print("S4 data rows:", len(table_rows))
bad_cols = [(i + 1, len(r)) for i, r in enumerate(table_rows) if len(r) != len(header)]
print("S4 rows with wrong col count:", bad_cols if bad_cols else "none")

# timing continuity from shot ids and time codes
def tc(s):
    m, rest = s.split(":")
    return int(m) * 60 + float(rest)

times = []
for r in table_rows:
    m = re.search(r"(\d\d:\d\d\.\d)\s*[–-]\s*(\d\d:\d\d\.\d)", r[1])
    if not m:
        print("WARN no timecode in row:", r[0])
        continue
    times.append((r[0], tc(m.group(1)), tc(m.group(2))))

prev = 0.0
gaps = []
for sid, a, b in times:
    if abs(a - prev) > 0.001:
        gaps.append((sid, prev, a))
    if b <= a:
        gaps.append((sid, "bad-dur", a, b))
    prev = b
print("shots parsed:", len(times), "| end:", prev, "| continuity gaps:", gaps if gaps else "none")

# CSV
rows = list(csv.reader(io.open(CSV, encoding="utf-8-sig")))
print("CSV header cells:", len(rows[0]), "| CSV shot rows:", len(rows) - 1)
print("CSV duration sum:", round(sum(float(r[5]) for r in rows[1:]), 3))

# leftovers
leftovers = ["NAM ASTE", "9.5s（21%）", "The Fool（第一张牌）", "M2 大牌 | 15–20% | 3s"]
for k in leftovers:
    print("leftover", repr(k), ":", text.count(k))
