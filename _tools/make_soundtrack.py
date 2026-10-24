# -*- coding: utf-8 -*-
"""Generate the 45s not-tarot soundtrack (48kHz stereo wav) with numpy only."""
import numpy as np, wave, os, math

SR = 48000
DUR = 45.0
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)

L = np.zeros(N); R = np.zeros(N)

def add(sig, at=0.0, pan=0.0):
    i0 = int(at * SR)
    n = len(sig)
    if i0 >= N: return
    n = min(n, N - i0)
    gl = math.sqrt(0.5 * (1 - pan)); gr = math.sqrt(0.5 * (1 + pan))
    L[i0:i0+n] += sig[:n] * gl
    R[i0:i0+n] += sig[:n] * gr

def env_ad(n, a=0.01, d=0.3, curve=3.0):
    e = np.ones(n)
    na = max(1, int(a * SR)); nd = max(1, int(d * SR))
    na = min(na, n); nd = min(nd, n - na)
    e[:na] = np.linspace(0, 1, na, endpoint=False) ** 0.6
    if nd > 0:
        e[na:na+nd] = np.linspace(1, 0, nd, endpoint=False) ** curve
        e[na+nd:] = 0
    return e

def noise(n):
    return rng.standard_normal(n)

def band_noise(n, lo, hi, soft=0.15):
    """cheap band-limited noise via FFT mask"""
    x = noise(n)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    m = np.zeros_like(f)
    band = (f >= lo) & (f <= hi)
    m[band] = 1.0
    # smooth edges
    k = max(1, int(len(f) * 0.01))
    m = np.convolve(m, np.ones(k) / k, mode='same')
    return np.fft.irfft(X * m, n)

# ---------- 1. heartbeat 1.6-10s, slowing ----------
beat_t = 1.6
k = 0
while beat_t < 10.2:
    # lub
    n = int(0.22 * SR)
    f0 = 56 if k % 2 == 0 else 48
    s = np.sin(2 * np.pi * f0 * np.linspace(0, 0.22, n)) * env_ad(n, 0.005, 0.20, 5)
    s += 0.35 * np.sin(2 * np.pi * (f0 * 1.5) * np.linspace(0, 0.22, n)) * env_ad(n, 0.005, 0.12, 6)
    add(s * 0.30, beat_t)
    # dub
    n2 = int(0.15 * SR)
    s2 = np.sin(2 * np.pi * (f0 + 10) * np.linspace(0, 0.15, n2)) * env_ad(n2, 0.004, 0.13, 5)
    add(s2 * 0.18, beat_t + 0.16)
    beat_t += 0.86 + 0.02 * k
    k += 1

# ---------- 2. low drone beds ----------
def drone(at, dur, f, amp=0.10, rise=1.2, fall=1.5):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.5 * tt + 0.7)
    s *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * tt)
    e = np.ones(n)
    nr = min(n, int(rise * SR)); nf = min(n - nr, int(fall * SR))
    e[:nr] = np.linspace(0, 1, nr) ** 1.5
    if nf > 0:
        e[-nf:] = np.linspace(1, 0, nf) ** 1.5
    add(s * e * amp, at, pan=0.05)

drone(6.0, 4.5, 42.0, 0.085)
drone(9.8, 6.4, 36.0, 0.105)
drone(29.8, 11.4, 32.0, 0.115)
drone(40.0, 2.2, 38.0, 0.070)

# ---------- 3. paper / whoosh at transitions ----------
TRANS = [1.4, 4.0, 6.2, 10.0, 16.0, 18.2, 21.0, 22.5, 24.0, 25.5, 27.0, 28.5, 30.0, 31.5, 36.0, 40.0, 42.0]
for i, at in enumerate(TRANS):
    n = int(0.55 * SR)
    x = band_noise(n, 1600, 9000)
    tt = np.linspace(0, 0.55, n)
    e = np.exp(-((tt - 0.18) ** 2) / (2 * 0.09 ** 2))
    add(x * e * (0.13 if i % 4 else 0.17), at - 0.10, pan=(-0.3 if i % 2 else 0.3))
    # soft ink drop / card tap
    n2 = int(0.09 * SR)
    s = np.sin(2 * np.pi * 140 * np.linspace(0, 0.09, n2)) * env_ad(n2, 0.002, 0.085, 6)
    add(s * 0.10, at + 0.03)

# ---------- 4. card flips (sharp paper tick) ----------
for at in [21.1, 22.6, 24.1, 25.6, 27.1, 28.6, 18.6]:
    n = int(0.16 * SR)
    x = band_noise(n, 2200, 11000)
    tt = np.linspace(0, 0.16, n)
    e = np.exp(-((tt - 0.03) ** 2) / (2 * 0.03 ** 2))
    add(x * e * 0.16, at, pan=0.15)

# ---------- 5. chimes at the climax ----------
def chime(at, f=1318.5, amp=0.064, dur=2.6):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * tt) + 0.45 * np.sin(2 * np.pi * f * 2.004 * tt) + 0.22 * np.sin(2 * np.pi * f * 3.01 * tt)
    e = np.exp(-tt * 1.7) * env_ad(n, 0.004, 0.05, 2)
    add(s * e * amp, at, pan=-0.08)
chime(35.9, 1318.5)
chime(42.2, 987.77, 0.058, 2.8)
chime(42.2, 1318.5, 0.040, 2.6)

# ---------- 6. final air ----------
n = int(2.4 * SR)
x = band_noise(n, 300, 4000)
e = np.linspace(0, 1, n) ** 2 * np.linspace(1, 0, n) ** 0.8
add(x * e * 0.05, 42.2)

# ---------- master ----------
mix = np.stack([L, R], axis=1)
# gentle high-pass to remove DC & rumble
def hp(x, f=28.0):
    X = np.fft.rfft(x, axis=0)
    fr = np.fft.rfftfreq(x.shape[0], 1 / SR)
    m = (fr / f) ** 2 / (1 + (fr / f) ** 2)
    return np.fft.irfft(X * m[:, None], x.shape[0], axis=0)
mix = hp(mix, 26.0)
# fade in/out
fade_in = int(0.6 * SR); fade_out = int(1.4 * SR)
mix[:fade_in] *= np.linspace(0, 1, fade_in)[:, None] ** 1.5
mix[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None] ** 1.2
peak = np.max(np.abs(mix))
mix = mix / peak * 0.92
mix = mix * 2.35
mix = np.tanh(mix / 0.78) * 0.78
rms = np.sqrt(np.mean(mix ** 2))
print('peak', round(float(np.max(np.abs(mix))), 3), 'rms dBFS', round(float(20 * np.log10(rms)), 1))

out = os.path.join(os.path.dirname(__file__), '..', '06_edit', 'audio', 'not_tarot_45s_mix.wav')
out = os.path.abspath(out)
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
print('wrote', out)
