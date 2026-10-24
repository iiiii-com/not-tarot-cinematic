"""Encode v5 magazine film frames -> 16:9 and 9:16 MP4 with soundtrack."""
import shutil
from pathlib import Path

ROOT = Path(r"E:\deepseek\PROJECT_MYSTIC_PROMO")
FF = Path(r"C:\Users\lenovo\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe")
AUDIO = ROOT / "06_edit" / "audio" / "not_tarot_45s_v6_mix.wav"


def encode(frames: str, out: str, w: int, h: int):
    src = ROOT / "07_final" / "_render_v6" / frames
    dst = ROOT / "07_final" / out
    cmd = [str(FF), "-y", "-v", "warning", "-framerate", "24", "-i", str(src / "frame_%05d.jpg")]
    if AUDIO.exists():
        cmd += ["-i", str(AUDIO)]
    cmd += ["-vf", f"scale={w}:{h}:flags=lanczos:in_range=full:out_range=tv,format=yuv420p",
            "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-level", "4.2", "-r", "24"]
    if AUDIO.exists():
        cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest"]
    cmd += ["-movflags", "+faststart", str(dst)]
    print(">", " ".join(cmd))
    import subprocess
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:])
        raise SystemExit(1)
    print("done", dst, f"{dst.stat().st_size/1e6:.2f} MB")


if __name__ == "__main__":
    encode("frames_16x9", "master_16x9.mp4", 1920, 1080)
    encode("frames_9x16", "social_9x16.mp4", 1080, 1920)
