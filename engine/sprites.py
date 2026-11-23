"""Procedural cartoon sprites for Doodligo: Dodo, Dini, objects, garden."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random

OUT = (43, 48, 66)          # outline colour
SKIN = (246, 205, 170)
HAIR = (110, 66, 40)
HOODIE = (76, 175, 80)
HOODIE_D = (56, 142, 60)
SHORTS = (52, 120, 220)
SNEAK = (255, 140, 30)
DINO = (120, 200, 80)
DINO_D = (90, 165, 60)
BELLY = (255, 222, 90)
SPIKE = (255, 140, 40)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size):
    return ImageFont.truetype(FONT_B, size)


def _down(img, scale):
    w, h = img.size
    return img.resize((w // scale, h // scale), Image.LANCZOS)


def _eye(d, cx, cy, r, closed, look=(0, 0)):
    if closed:
        d.arc([cx - r, cy - r * 0.6, cx + r, cy + r * 0.6], 20, 160, fill=OUT, width=max(4, r // 4))
        return
    d.ellipse([cx - r, cy - r * 1.15, cx + r, cy + r * 1.15], fill="white", outline=OUT, width=5)
    pr = r * 0.6
    px, py = cx + look[0] * r * 0.3, cy + r * 0.15 + look[1] * r * 0.3
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(40, 30, 30))
    d.ellipse([px - pr * 0.25 + pr * 0.3, py - pr * 0.6, px + pr * 0.25 + pr * 0.3, py - pr * 0.1], fill="white")


def dodo(mouth=0, blink=False, arm_up=False, S=2):
    """Boy in green hoodie, blue shorts, orange sneakers. ~220x380 output."""
    W, H = 220 * S, 380 * S
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = S
    cx = W // 2
    lw = 5 * s // 2
    # legs
    for dx in (-30, 30):
        d.rounded_rectangle([cx + dx * s - 14 * s, 285 * s, cx + dx * s + 14 * s, 345 * s], 10 * s, fill=SKIN, outline=OUT, width=lw)
    # sneakers
    for dx in (-34, 34):
        d.rounded_rectangle([cx + dx * s - 30 * s, 335 * s, cx + dx * s + 30 * s, 368 * s], 16 * s, fill=SNEAK, outline=OUT, width=lw)
        d.rectangle([cx + dx * s - 28 * s, 358 * s, cx + dx * s + 28 * s, 364 * s], fill="white")
    # shorts
    d.rounded_rectangle([cx - 62 * s, 245 * s, cx + 62 * s, 300 * s], 14 * s, fill=SHORTS, outline=OUT, width=lw)
    d.line([cx, 262 * s, cx, 300 * s], fill=OUT, width=lw)
    # arms (behind body sides)
    if arm_up:
        d.rounded_rectangle([cx + 52 * s, 95 * s, cx + 84 * s, 190 * s], 16 * s, fill=HOODIE, outline=OUT, width=lw)
        d.ellipse([cx + 52 * s, 72 * s, cx + 86 * s, 106 * s], fill=SKIN, outline=OUT, width=lw)
    else:
        d.rounded_rectangle([cx + 55 * s, 150 * s, cx + 86 * s, 250 * s], 16 * s, fill=HOODIE, outline=OUT, width=lw)
        d.ellipse([cx + 54 * s, 238 * s, cx + 88 * s, 272 * s], fill=SKIN, outline=OUT, width=lw)
    d.rounded_rectangle([cx - 86 * s, 150 * s, cx - 55 * s, 250 * s], 16 * s, fill=HOODIE, outline=OUT, width=lw)
    d.ellipse([cx - 88 * s, 238 * s, cx - 54 * s, 272 * s], fill=SKIN, outline=OUT, width=lw)
    # body hoodie
    d.rounded_rectangle([cx - 66 * s, 140 * s, cx + 66 * s, 268 * s], 34 * s, fill=HOODIE, outline=OUT, width=lw)
    d.rounded_rectangle([cx - 40 * s, 210 * s, cx + 40 * s, 250 * s], 12 * s, fill=HOODIE_D, outline=OUT, width=lw // 2 + 1)
    # hood strings
    for dx in (-16, 16):
        d.line([cx + dx * s, 150 * s, cx + dx * s, 190 * s], fill="white", width=3 * s)
        d.ellipse([cx + dx * s - 4 * s, 188 * s, cx + dx * s + 4 * s, 196 * s], fill="white")
    # hood behind head
    d.ellipse([cx - 78 * s, 20 * s, cx + 78 * s, 168 * s], fill=HOODIE_D, outline=OUT, width=lw)
    # ears
    for dx in (-66, 66):
        d.ellipse([cx + dx * s - 14 * s, 82 * s, cx + dx * s + 14 * s, 114 * s], fill=SKIN, outline=OUT, width=lw)
    # head
    d.ellipse([cx - 64 * s, 28 * s, cx + 64 * s, 160 * s], fill=SKIN, outline=OUT, width=lw)
    # hair
    d.chord([cx - 64 * s, 22 * s, cx + 64 * s, 120 * s], 180, 360, fill=HAIR, outline=OUT, width=lw)
    d.polygon([(cx - 40 * s, 60 * s), (cx - 10 * s, 84 * s), (cx + 6 * s, 64 * s), (cx + 30 * s, 82 * s), (cx + 50 * s, 60 * s)], fill=HAIR)
    d.polygon([(cx - 5 * s, 24 * s), (cx + 10 * s, 6 * s), (cx + 18 * s, 28 * s)], fill=HAIR, outline=OUT)
    # eyes
    _eye(d, cx - 24 * s, 98 * s, 13 * s, blink)
    _eye(d, cx + 24 * s, 98 * s, 13 * s, blink)
    # brows
    d.arc([cx - 38 * s, 72 * s, cx - 12 * s, 86 * s], 200, 340, fill=HAIR, width=4 * s)
    d.arc([cx + 12 * s, 72 * s, cx + 38 * s, 86 * s], 200, 340, fill=HAIR, width=4 * s)
    # cheeks
    for dx in (-42, 42):
        d.ellipse([cx + dx * s - 11 * s, 118 * s, cx + dx * s + 11 * s, 130 * s], fill=(255, 160, 160))
    # mouth
    if mouth <= 0.15:
        d.arc([cx - 18 * s, 112 * s, cx + 18 * s, 138 * s], 20, 160, fill=OUT, width=4 * s)
    else:
        h = 8 + 16 * min(1, mouth)
        d.chord([cx - 18 * s, (124 - h / 2) * s, cx + 18 * s, (124 + h) * s], 0, 180, fill=(150, 40, 50), outline=OUT, width=3 * s)
        d.ellipse([cx - 9 * s, (124 + h * 0.35) * s, cx + 9 * s, (124 + h * 0.9) * s], fill=(240, 110, 120))
    return _down(im, S)


def dini(mouth=0, blink=False, S=2):
    """Small green dinosaur, yellow belly, orange back spikes. ~280x260 output."""
    W, H = 280 * S, 260 * S
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = S
    lw = 5 * s // 2
    # tail (to the left)
    d.polygon([(20 * s, 200 * s), (95 * s, 150 * s), (110 * s, 205 * s)], fill=DINO, outline=OUT, width=lw)
    # back spikes
    for (x, y) in [(70, 165), (95, 128), (125, 108), (160, 100)]:
        d.polygon([(x * s - 15 * s, y * s + 10 * s), (x * s, y * s - 20 * s), (x * s + 15 * s, y * s + 10 * s)], fill=SPIKE, outline=OUT, width=lw)
    # legs
    for x in (105, 165):
        d.rounded_rectangle([x * s - 20 * s, 195 * s, x * s + 20 * s, 245 * s], 14 * s, fill=DINO_D, outline=OUT, width=lw)
        d.ellipse([x * s - 26 * s, 230 * s, x * s + 26 * s, 254 * s], fill=DINO_D, outline=OUT, width=lw)
    # body
    d.ellipse([70 * s, 110 * s, 210 * s, 235 * s], fill=DINO, outline=OUT, width=lw)
    d.ellipse([110 * s, 140 * s, 195 * s, 228 * s], fill=BELLY, outline=OUT, width=lw // 2 + 1)
    for yy in (160, 182, 204):
        d.arc([125 * s, yy * s - 6 * s, 182 * s, yy * s + 8 * s], 20, 160, fill=(220, 180, 60), width=2 * s)
    # head spikes
    for (x, y) in [(190, 22), (215, 18)]:
        d.polygon([(x * s - 12 * s, y * s + 14 * s), (x * s, y * s - 10 * s), (x * s + 12 * s, y * s + 14 * s)], fill=SPIKE, outline=OUT, width=lw)
    # neck/head
    d.ellipse([150 * s, 28 * s, 270 * s, 140 * s], fill=DINO, outline=OUT, width=lw)
    # arms
    d.rounded_rectangle([185 * s, 150 * s, 222 * s, 168 * s], 9 * s, fill=DINO_D, outline=OUT, width=lw)
    # eyes
    _eye(d, 196 * s, 72 * s, 15 * s, blink, look=(0.5, 0))
    _eye(d, 236 * s, 72 * s, 15 * s, blink, look=(0.5, 0))
    # nostrils
    d.ellipse([252 * s, 98 * s, 258 * s, 104 * s], fill=OUT)
    # cheeks
    d.ellipse([176 * s, 98 * s, 194 * s, 108 * s], fill=(255, 170, 150))
    # mouth
    if mouth <= 0.15:
        d.arc([200 * s, 96 * s, 250 * s, 124 * s], 15, 165, fill=OUT, width=4 * s)
    else:
        h = 8 + 18 * min(1, mouth)
        d.chord([202 * s, (108 - h / 3) * s, 250 * s, (108 + h) * s], 0, 180, fill=(150, 40, 50), outline=OUT, width=3 * s)
        d.ellipse([216 * s, (108 + h * 0.4) * s, 236 * s, (108 + h * 0.9) * s], fill=(240, 110, 120))
    return _down(im, S)


def _star_pts(cx, cy, R, r, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        a = math.radians(rot + i * 180 / n)
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return pts


def obj(name, size=240, S=2):
    W = size * S
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    u = W / 100.0
    lw = int(2.2 * u)
    def E(a, b, c, e, **k): d.ellipse([a * u, b * u, c * u, e * u], **k)
    if name == "apple":
        E(14, 26, 54, 88, fill=(225, 35, 45), outline=OUT, width=lw)
        E(46, 26, 86, 88, fill=(225, 35, 45), outline=OUT, width=lw)
        E(20, 30, 80, 90, fill=(225, 35, 45))
        E(26, 38, 38, 54, fill=(255, 130, 130))
        d.line([50 * u, 30 * u, 54 * u, 10 * u], fill=(110, 70, 40), width=int(4 * u))
        d.polygon([(55 * u, 18 * u), (72 * u, 8 * u), (80 * u, 14 * u), (62 * u, 24 * u)], fill=(80, 170, 60), outline=OUT)
    elif name == "balloon":
        d.line([50 * u, 78 * u, 46 * u, 88 * u, 54 * u, 96 * u], fill=OUT, width=int(1.5 * u))
        E(22, 6, 78, 76, fill=(40, 110, 230), outline=OUT, width=lw)
        E(32, 16, 44, 34, fill=(150, 200, 255))
        d.polygon([(45 * u, 82 * u), (50 * u, 75 * u), (55 * u, 82 * u)], fill=(40, 110, 230), outline=OUT)
    elif name == "star":
        d.polygon(_star_pts(50 * u, 54 * u, 44 * u, 19 * u), fill=(255, 215, 0), outline=OUT, width=lw)
        E(38, 46, 44, 54, fill=OUT); E(56, 46, 62, 54, fill=OUT)
        d.arc([40 * u, 52 * u, 60 * u, 66 * u], 20, 160, fill=OUT, width=int(1.6 * u))
    elif name == "leaf":
        d.polygon([(50 * u, 6 * u), (78 * u, 30 * u), (82 * u, 58 * u), (60 * u, 84 * u), (50 * u, 88 * u), (40 * u, 84 * u), (18 * u, 58 * u), (22 * u, 30 * u)], fill=(60, 180, 70), outline=OUT, width=lw)
        d.line([50 * u, 14 * u, 50 * u, 98 * u], fill=(30, 110, 40), width=int(2 * u))
        for y in (32, 48, 64):
            d.line([50 * u, y * u, 68 * u, (y - 10) * u], fill=(30, 110, 40), width=int(1.4 * u))
            d.line([50 * u, y * u, 32 * u, (y - 10) * u], fill=(30, 110, 40), width=int(1.4 * u))
    elif name == "orange":
        E(14, 18, 86, 90, fill=(255, 140, 20), outline=OUT, width=lw)
        E(26, 30, 40, 46, fill=(255, 200, 120))
        rnd = random.Random(3)
        for _ in range(24):
            x, y = rnd.uniform(30, 75), rnd.uniform(35, 80)
            E(x, y, x + 1.6, y + 1.6, fill=(225, 110, 10))
        d.line([50 * u, 20 * u, 52 * u, 10 * u], fill=(110, 70, 40), width=int(3 * u))
        d.polygon([(52 * u, 14 * u), (68 * u, 6 * u), (72 * u, 12 * u), (58 * u, 18 * u)], fill=(80, 170, 60), outline=OUT)
    elif name == "flower":
        d.line([50 * u, 55 * u, 50 * u, 98 * u], fill=(60, 150, 60), width=int(4 * u))
        d.polygon([(50 * u, 80 * u), (70 * u, 68 * u), (64 * u, 84 * u)], fill=(80, 170, 60), outline=OUT)
        for k in range(6):
            a = math.radians(k * 60)
            px, py = 50 + 20 * math.cos(a), 40 + 20 * math.sin(a)
            E(px - 15, py - 15, px + 15, py + 15, fill=(150, 70, 200), outline=OUT, width=lw)
        E(38, 28, 62, 52, fill=(255, 215, 60), outline=OUT, width=lw)
    return _down(im, S)


def grey(img):
    """Greyscale (keeps alpha), lightened a touch."""
    a = img.getchannel("A") if img.mode == "RGBA" else None
    g = img.convert("L").point(lambda v: int(v * 0.75 + 50)).convert("RGB")
    if a is not None:
        g.putalpha(a)
    return g


def garden(W=1280, H=720, rainbow=True):
    """Bright garden background (RGB)."""
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([0, y, W, y], fill=(int(130 + 100 * t), int(200 + 45 * t), int(255 - 10 * t)))
    # sun
    d.ellipse([1060, 40, 1180, 160], fill=(255, 225, 80))
    for k in range(12):
        a = math.radians(k * 30)
        d.line([1120 + 72 * math.cos(a), 100 + 72 * math.sin(a), 1120 + 95 * math.cos(a), 100 + 95 * math.sin(a)], fill=(255, 210, 60), width=8)
    # rainbow
    if rainbow:
        cols = [(240, 60, 60), (255, 150, 40), (255, 220, 60), (90, 190, 80), (60, 130, 230), (150, 80, 200)]
        for i, c in enumerate(cols):
            r = 520 - i * 26
            d.arc([640 - r, 470 - r, 640 + r, 470 + r], 180, 360, fill=c, width=26)
    # clouds
    for (x, y) in [(140, 90), (520, 60), (820, 120)]:
        for dx, dy, r in [(0, 0, 38), (40, -18, 46), (85, 0, 38), (42, 12, 40)]:
            d.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill="white")
    # hills
    d.ellipse([-300, 430, 700, 900], fill=(140, 210, 100))
    d.ellipse([500, 420, 1600, 940], fill=(120, 200, 90))
    d.rectangle([0, 560, W, H], fill=(110, 190, 80))
    # trees
    for x in (90, 1190):
        d.rectangle([x - 14, 380, x + 14, 520], fill=(130, 85, 50))
        for dx, dy, r in [(0, -10, 70), (-45, 30, 55), (45, 30, 55)]:
            d.ellipse([x + dx - r, 370 + dy - r, x + dx + r, 370 + dy + r], fill=(70, 160, 70))
    # flowers in grass
    rnd = random.Random(7)
    fcols = [(240, 70, 90), (255, 200, 40), (160, 90, 220), (255, 130, 40), (90, 150, 240), (255, 110, 180)]
    for _ in range(60):
        x, y = rnd.randint(10, W - 10), rnd.randint(575, H - 10)
        c = rnd.choice(fcols)
        r = rnd.randint(6, 11)
        d.line([x, y, x, y + 14], fill=(60, 140, 50), width=3)
        for k in range(5):
            a = math.radians(k * 72)
            d.ellipse([x + r * math.cos(a) - r * 0.7, y + r * math.sin(a) - r * 0.7, x + r * math.cos(a) + r * 0.7, y + r * math.sin(a) + r * 0.7], fill=c)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 235, 120))
    return im


def butterfly(col, S=2):
    W = 60 * S
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = S
    d.ellipse([4 * s, 6 * s, 30 * s, 32 * s], fill=col, outline=OUT, width=2 * s)
    d.ellipse([30 * s, 6 * s, 56 * s, 32 * s], fill=col, outline=OUT, width=2 * s)
    d.ellipse([10 * s, 28 * s, 30 * s, 50 * s], fill=col, outline=OUT, width=2 * s)
    d.ellipse([30 * s, 28 * s, 50 * s, 50 * s], fill=col, outline=OUT, width=2 * s)
    d.rounded_rectangle([27 * s, 8 * s, 33 * s, 50 * s], 3 * s, fill=OUT)
    return _down(im, S)


def logo(size=110, stroke=8):
    letters = "DOODLIGO"
    cols = [(240, 60, 60), (255, 150, 40), (255, 205, 40), (90, 190, 80), (60, 130, 230), (150, 80, 200), (255, 110, 180), (40, 190, 200)]
    f = font(size)
    widths = [f.getbbox(ch)[2] for ch in letters]
    W = sum(widths) + 20 * len(letters) + stroke * 4
    im = Image.new("RGBA", (W, size + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = stroke * 2
    for i, ch in enumerate(letters):
        y = 10 + (8 if i % 2 else 0)
        d.text((x, y), ch, font=f, fill=cols[i], stroke_width=stroke, stroke_fill="white")
        x += widths[i] + 20
    return im
