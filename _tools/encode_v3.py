import subprocess, glob
from pathlib import Path
ROOT = Path(r'E:\deepseek\PROJECT_MYSTIC_PROMO')
FF = glob.glob(r'C:\Users\lenovo\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg*\**\bin\ffmpeg.exe', recursive=True)
FF = FF[0] if FF else 'ffmpeg'
AUD = ROOT/'06_edit'/'audio'/'not_tarot_45s_mix.wav'

def enc(frames, out, size):
    cmd = [FF, '-y', '-framerate', '24', '-i', str(frames/'frame_%05d.jpg'),
           '-i', str(AUD),
           '-vf', 'scale=%s:in_range=full:out_range=tv,format=yuv420p' % size,
           '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-profile:v', 'high', '-level', '4.2',
           '-r', '24', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest',
           '-movflags', '+faststart', str(out)]
    print(' '.join(cmd))
    subprocess.run(cmd, check=True)
    print('done', out, f'{out.stat().st_size/1e6:.2f} MB')

enc(ROOT/'07_final'/'_render_v3'/'frames_16x9', ROOT/'07_final'/'master_16x9.mp4', '1920x1080')
enc(ROOT/'07_final'/'_render_v3'/'frames_9x16', ROOT/'07_final'/'social_9x16.mp4', '1080x1920')
