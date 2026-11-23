"""thumb.py CODE CLIP TIME 'LINE1' 'LINE2' [card...] -> thumbnails/CODE.jpg"""
import sys, subprocess
from PIL import Image, ImageDraw, ImageEnhance
import sprites as SP
code, clip, t, l1, l2 = sys.argv[1:6]
src = f"/home/claude/work/{code}/clips/{clip}.mp4"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", t, "-i", src, "-frames:v", "1", "-vf", "scale=1280:854,crop=1280:720:0:60", "/tmp/thb.png"], check=True)
bg = ImageEnhance.Color(Image.open("/tmp/thb.png").convert("RGB")).enhance(1.15).convert("RGBA")
d = ImageDraw.Draw(bg)
for i, (txt, c) in enumerate([(l1, (240, 60, 60)), (l2, (60, 130, 230))]):
    size = 112
    while d.textlength(txt, font=SP.font(size)) > 640 and size > 60:
        size -= 6
    d.text((30, 20 + i * (size + 6)), txt, font=SP.font(size), fill=c, stroke_width=11, stroke_fill="white")
lg = SP.logo(46, 6); bg.alpha_composite(lg, (1280 - lg.width - 20, 20))
bg.convert("RGB").save(f"/home/claude/doodligo/thumbnails/{code}.jpg", quality=92)
