# -*- coding: utf-8 -*-
"""Encode the captured 24fps frame sequences + soundtrack into the two deliverables."""
import subprocess, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FF = r'E:\ffmpeg\bin\ffmpeg.exe'
if not os.path.exists(FF):
    # fall back to WinGet install
    import glob
    cand = glob.glob(r'C:\Users\lenovo\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg*\**\bin\ffmpeg.exe', recursive=True)
    FF = cand[0] if cand else 'ffmpeg'
print('ffmpeg:', FF)

AUD = os.path.join(ROOT, '06_edit', 'audio', 'not_tarot_45s_mix.wav')

def enc(frames_dir, out, w, h):
    cmd = [FF, '-y', '-framerate', '24', '-i', os.path.join(frames_dir, 'frame_%05d.jpg'),
           '-i', AUD,
           '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-vf', 'scale=in_range=full:out_range=tv,format=yuv420p', '-pix_fmt', 'yuv420p',
           '-profile:v', 'high', '-level', '4.2',
           '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
           '-shortest', '-movflags', '+faststart',
           '-metadata', 'title=NOT TAROT 鈥?45s brand film',
           os.path.join(ROOT, '07_final', out)]
    print(' '.join(cmd))
    subprocess.run(cmd, check=True)
    print('wrote', out)

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'both'
    if which in ('16x9', 'both'):
        enc(os.path.join(ROOT, '07_final', '_render_dir_hq', 'frames_16x9'), 'master_16x9.mp4', 1920, 1080)
    if which in ('9x16', 'both'):
        enc(os.path.join(ROOT, '07_final', '_render_dir_hq', 'frames_9x16'), 'social_9x16.mp4', 1080, 1920)

