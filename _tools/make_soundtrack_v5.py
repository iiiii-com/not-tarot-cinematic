"""Synthesize a 45s magazine-film soundtrack (48k stereo) with numpy -> wav."""
import wave
import numpy as np
from pathlib import Path

ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
OUT = ROOT / "06_edit" / "audio" / "not_tarot_45s_v5_mix.wav"
SR = 48000
DUR = 45.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
mix = np.zeros(N, dtype=np.float64)


def idx(t):
    return max(0, min(N, int(t * SR)))


def add(sig, t, gain=1.0):
    i = idx(t)
    j = min(N, i + len(sig))
    if j > i:
        mix[i:j] += sig[:j - i] * gain


def env(n, a=0.01, d=0.2, curve=6.0):
    t = np.arange(n) / SR
    e = np.ones(n)
    na = max(1, int(a * SR))
    nd = max(1, int(d * SR))
    e[:na] = np.linspace(0, 1, na)
    if na + nd < n:
        e[na + nd:] = 0.0
    seg = min(nd, n - na)
    if seg > 0:
        e[na:na + seg] = np.exp(-np.linspace(0, curve, seg))
    return e


def thump(f=54.0, dur=0.42, gain=1.0, click=0.10):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (f + 26 * np.exp(-t * 26)) * t) * env(n, 0.004, dur, 6.5)
    c = rng.normal(0, 1, n) * env(n, 0.001, 0.03, 9) * click
    return (s + c) * gain


def bell(f=880.0, dur=2.2, gain=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * f * 1.5 * t) + 0.2 * np.sin(2 * np.pi * f * 2.02 * t))
    return s * env(n, 0.002, dur, 5.2) * gain


def whoosh(dur=0.55, gain=0.5, bright=0.5):
    n = int(dur * SR)
    x = rng.normal(0, 1, n)
    # crude low-pass by smoothing
    k = max(3, int(24 * (1.0 - bright)) + 3)
    x = np.convolve(x, np.ones(k) / k, mode="same")
    e = np.sin(np.linspace(0, np.pi, n)) ** 1.6
    return x * e * gain


def rustle(dur=1.1, gain=0.35):
    n = int(dur * SR)
    x = rng.normal(0, 1, n)
    x = np.convolve(x, np.array([1, -0.96]), mode="same")  # highpass-ish
    e = np.zeros(n)
    seg = int(0.09 * SR); hann = np.hanning(seg)
    for k in range(9):
        s = int((0.05 + 0.1 * k) * SR)
        if s + seg <= n:
            e[s:s + seg] += hann * (0.5 + 0.5 * rng.random())
    e = e[:n] * env(n, 0.02, dur, 2.2)
    return x * e * gain


def drone_dur(f=55.0, dur=8.0, gain=0.10, fifth=False):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t)
    if fifth:
        s += 0.5 * np.sin(2 * np.pi * f * 1.5 * t) + 0.25 * np.sin(2 * np.pi * f * 2.0 * t)
    s += 0.12 * rng.normal(0, 1, n)
    s = np.convolve(s, np.ones(48) / 48, mode="same")
    e = np.concatenate([np.linspace(0, 1, n // 2), np.linspace(1, 0, n - n // 2)]) ** 0.8
    return s * e * gain


# bed: very low room tone across the film
room = rng.normal(0, 1, N)
room = np.convolve(room, np.ones(600) / 600, mode="same") * 0.02
mix += room

# page / scene whooshes
for t, g in [(0.35, 0.28), (4.5, 0.45), (8.98, 0.40), (14.0, 0.42), (18.5, 0.40), (23.0, 0.38),
             (29.5, 0.55), (31.5, 0.50), (37.0, 0.38), (40.5, 0.34), (43.5, 0.30)]:
    add(whoosh(0.62, g), t - 0.12)

# cover: soft paper settle
add(rustle(0.7, 0.16), 0.5)

# feature: heartbeat 9.2 - 13.6 (double thump every 0.78s)
t = 9.2
while t < 13.6:
    add(thump(52, 0.40, 0.60), t)
    add(thump(58, 0.30, 0.30), t + 0.20)
    t += 0.78

# index: ticks as icons appear
for k in range(20):
    add(bell(1450 + 30 * k, 0.10, 0.045), 14.4 + k * 0.11)

# pull quote: air swell
add(drone_dur(220.0, 4.2, 0.05, fifth=True), 18.6)

# sticker sheet: peel rustle
add(rustle(1.5, 0.30), 25.9)
add(rustle(0.8, 0.18), 26.9)

# black interlude: dip then sub drone + distant bell
mix[idx(29.2):idx(29.75)] *= np.linspace(1, 0.15, idx(29.75) - idx(29.2))
add(drone_dur(41.0, 2.2, 0.16, fifth=False), 29.55)
add(bell(220.0, 3.0, 0.28), 29.6)
mix[idx(29.75):idx(31.4)] *= np.minimum(1, np.linspace(0.5, 1.0, idx(31.4) - idx(29.75)) + 0.25)

# seal: warm drone and shimmer
add(drone_dur(55.0, 5.6, 0.10, fifth=True), 31.5)
add(drone_dur(65.4, 5.2, 0.06, fifth=True), 31.6)
add(bell(523.25, 2.6, 0.16), 32.0)
add(bell(783.99, 2.4, 0.12), 33.4)

# colophon: paper settle, soft bell
add(rustle(0.9, 0.16), 37.1)
add(bell(392.0, 2.2, 0.14), 37.6)

# back cover: reveal bell
add(bell(659.25, 2.6, 0.14), 40.8)
add(drone_dur(48.0, 3.4, 0.05), 40.9)
add(rustle(0.8, 0.12), 43.4)

# gentle master: fade in/out, soft clip, normalize
mix *= np.concatenate([np.linspace(0, 1, int(0.25 * SR)), np.ones(N - int(0.55 * SR)), np.linspace(1, 0, int(0.30 * SR))])
mix = np.tanh(mix * 1.25) * 0.92
peak = np.max(np.abs(mix))
mix = mix / peak * 0.72
# stereo: haas widening on pads only is skipped; slight decorrelation
left = mix.copy()
right = np.concatenate([np.zeros(14), mix[:-14]]) * 0.985
st = np.stack([left, right], axis=1)
pcm = (st * 32767).astype(np.int16)
with wave.open(str(OUT), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote", OUT, OUT.stat().st_size / 1e6, "MB")
