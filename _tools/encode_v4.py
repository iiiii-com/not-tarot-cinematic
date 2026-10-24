"""Encode v4 frames (DPR-2, 3840x2160 / 2160x3840) down to 1080p masters."""
import subprocess
from pathlib import Path

ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
R = ROOT / "07_final" / "_render_v4"
AUD = ROOT / "06_edit" / "audio" / "not_tarot_45s_mix.wav"
OUT = ROOT / "07_final"


def ffmpeg():
    for p in [r"E:\ffmpeg\bin\ffmpeg.exe"]:
        if Path(p).exists():
            return p
    import glob
    g = glob.glob(r"C:\Users\lenovo\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg*\**\bin\ffmpeg.exe", recursive=True)
    if g:
        return g[0]
    return "ffmpeg"


def encode(tag, w, h, out):
    frames = R / f"frames_{tag}" / "frame_%05d.jpg"
    cmd = [ffmpeg(), "-y", "-v", "warning", "-framerate", "24",
           "-i", str(frames), "-i", str(AUD),
           "-vf", f"scale={w}:{h}:flags=lanczos:in_range=full:out_range=tv,format=yuv420p",
           "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-level", "4.2",
           "-r", "24", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
           "-shortest", "-movflags", "+faststart", str(out)]
    print(">", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("done", out, f"{out.stat().st_size/1e6:.2f} MB")


if __name__ == "__main__":
    encode("16x9", 1920, 1080, OUT / "master_16x9.mp4")
    encode("9x16", 1080, 1920, OUT / "social_9x16.mp4")
