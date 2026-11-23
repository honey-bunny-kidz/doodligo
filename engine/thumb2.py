"""Child-friendly YouTube thumbnail (1280x720).

python3 thumb2.py CODE CLIPFILE TIME 'TITLE' 'SUBTITLE' STICKERS
STICKERS: comma list; each item is TEXT or TEXT:#rrggbb or :#rrggbb (colour blob, no text)
"""
import sys, math, random, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import sprites as SP

W, H = 1280, 720
RAINBOW = [(255, 70, 80), (255, 150, 30), (255, 205, 0), (60, 190, 80), (40, 150, 255), (170, 90, 230), (255, 100, 180)]
NAVY = (28, 36, 80)


def hexcol(s):
    s = s.lstrip("#"); return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def frame(clip, t):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", clip, "-frames:v", "1", "/tmp/th2.png"], check=True)
    im = Image.open("/tmp/th2.png").convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.25)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Brightness(im).enhance(1.05)
    return im


def bubble_text(base, text, x, y, size, colors=None, angle=-4):
    """Chunky multicolour letters with navy outer + white inner outline and drop shadow."""
    f = SP.font(size)
    pad = 40
    tw = int(sum(f.getlength(ch) for ch in text) + len(text) * size * 0.04) + pad * 2
    layer = Image.new("RGBA", (tw, int(size * 1.5) + pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = pad
    for i, ch in enumerate(text):
        col = (colors or RAINBOW)[i % len(colors or RAINBOW)]
        yy = pad // 2 + (6 if i % 2 else 0)
        d.text((cx + 6, yy + 8), ch, font=f, fill=(0, 0, 0, 90), stroke_width=int(size * 0.16), stroke_fill=(0, 0, 0, 90))
        d.text((cx, yy), ch, font=f, fill=col, stroke_width=int(size * 0.16), stroke_fill=NAVY)
        d.text((cx, yy), ch, font=f, fill=col, stroke_width=int(size * 0.09), stroke_fill="white")
        d.text((cx, yy), ch, font=f, fill=col)
        cx += f.getlength(ch) + size * 0.04
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    base.alpha_composite(layer, (int(x), int(y)))
    return layer.size


def sticker(base, txt, col, cx, cy, r, rot):
    s = Image.new("RGBA", (r * 2 + 30, r * 2 + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    c = r + 15
    d.ellipse([c - r + 6, c - r + 10, c + r + 6, c + r + 10], fill=(0, 0, 0, 70))
    d.ellipse([c - r, c - r, c + r, c + r], fill="white")
    d.ellipse([c - r + 9, c - r + 9, c + r - 9, c + r - 9], fill=col)
    d.ellipse([c - r * 0.55, c - r * 0.75, c - r * 0.05, c - r * 0.4], fill=(255, 255, 255, 110))
    if txt:
        size = int(r * (1.15 if len(txt) == 1 else 0.85 if len(txt) == 2 else 0.6))
        f = SP.font(size)
        tw = d.textlength(txt, font=f); bb = f.getbbox(txt)
        d.text((c - tw / 2, c - (bb[1] + bb[3]) / 2), txt, font=f, fill="white", stroke_width=max(3, size // 14), stroke_fill=NAVY)
    s = s.rotate(rot, resample=Image.BICUBIC)
    base.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))


def sparkle(d, x, y, r, col=(255, 240, 120)):
    d.polygon([(x, y - r), (x + r * 0.25, y - r * 0.25), (x + r, y), (x + r * 0.25, y + r * 0.25), (x, y + r), (x - r * 0.25, y + r * 0.25), (x - r, y), (x - r * 0.25, y - r * 0.25)], fill=col)


def make(code, clip, t, title, subtitle, stickers, shift=330, out=None, zoom=1.0, cropx=0):
    src = frame(clip, t)
    sc = H / src.height * zoom
    fr = src.resize((int(src.width * sc), int(src.height * sc)), Image.LANCZOS)
    fr = fr.crop((cropx, (fr.height - H) // 2, cropx + W, (fr.height - H) // 2 + H))
    canvas = Image.new("RGBA", (W, H))
    # left panel: bright sky gradient
    sky = Image.new("RGB", (W, H))
    sd = ImageDraw.Draw(sky)
    for yy in range(H):
        k = yy / H
        sd.line([0, yy, W, yy], fill=(int(120 + 110 * k), int(205 + 35 * k), 255))
    for i, cc in enumerate(RAINBOW[:6]):
        r = 640 - i * 30
        sd.arc([-360 - r + 360, H + 120 - r, -360 + r + 360, H + 120 + r], 180, 300, fill=cc, width=30)
    for (cx, cy, s) in [(110, 600, 1.2), (330, 650, 1.0), (40, 120, 0.7)]:
        for dx, dy, rr in [(0, 0, 50), (55, -25, 62), (115, 0, 50), (58, 18, 55)]:
            sd.ellipse([cx + dx * s - rr * s, cy + dy * s - rr * s, cx + dx * s + rr * s, cy + dy * s + rr * s], fill="white")
    canvas.paste(sky, (0, 0))
    # photo shifted right with a soft left edge
    mask = Image.new("L", (W, H), 255)
    md = ImageDraw.Draw(mask)
    fade = 170
    for xx in range(fade):
        md.line([xx, 0, xx, H], fill=int(255 * (xx / fade) ** 1.3))
    canvas.paste(fr, (shift, 0), mask)
    d = ImageDraw.Draw(canvas)
    # title + subtitle ribbon
    size = 140
    while size > 60 and SP.font(size).getlength(title) + len(title) * size * 0.04 > 540:
        size -= 4
    w1, h1 = bubble_text(canvas, title, 14, 18, size)
    fsub = SP.font(40)
    tw = d.textlength(subtitle, font=fsub)
    ry = 18 + h1 - 30
    d.rounded_rectangle([40, ry, 40 + tw + 50, ry + 66], 33, fill=(255, 214, 40), outline=NAVY, width=5)
    d.text((65, ry + 9), subtitle, font=fsub, fill=NAVY)
    # stickers
    rnd = random.Random(code)
    items = [s for s in stickers.split(",") if s]
    n = len(items)
    for i, it in enumerate(items):
        txt, _, col = it.partition(":")
        col = hexcol(col) if col else RAINBOW[i % len(RAINBOW)]
        r = 58 if n <= 4 else 50
        cols = min(n, 3) if n > 4 else n
        row, k = divmod(i, cols)
        cx = 95 + k * (r * 2 + 18) + row * 40
        cy = ry + 150 + row * (r * 2 + 6)
        sticker(canvas, txt, col, cx, cy, r, rnd.uniform(-12, 12))
    # sparkles
    for (x, y, r) in [(560, 60, 22), (610, 120, 12), (40, 330, 14), (520, 330, 18), (1230, 640, 20), (1190, 590, 11), (720, 30, 14)]:
        sparkle(d, x, y, r)
    # logo badge
    lg = SP.logo(40, 6)
    d.rounded_rectangle([W - lg.width - 36, H - 80, W - 14, H - 14], 30, fill=(255, 255, 255, 230), outline=NAVY, width=4)
    canvas.alpha_composite(lg, (W - lg.width - 26, H - 78))
    # bright white rounded frame
    d.rounded_rectangle([4, 4, W - 5, H - 5], 26, outline=(255, 255, 255), width=8)
    canvas.convert("RGB").save(out or f"/home/claude/doodligo/thumbnails/{code}.jpg", quality=93)


if __name__ == "__main__":
    code, clip, t, title, subtitle, stickers = sys.argv[1:7]
    shift = int(sys.argv[7]) if len(sys.argv) > 7 else 330
    zoom = float(sys.argv[8]) if len(sys.argv) > 8 else 1.0
    cropx = int(sys.argv[9]) if len(sys.argv) > 9 else 0
    make(code, clip, float(t), title, subtitle, stickers, shift, zoom=zoom, cropx=cropx)
