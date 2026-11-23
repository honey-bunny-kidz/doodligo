"""Compose a Doodligo episode from Muse 3D clips + Muse voice MP3s.

python3 compose.py <episode_plan.py> <clips_dir> <voices_dir> <out.mp4>

The plan lists segments: each has a clip, an optional style (grey) and the
numbered voice lines spoken over it. Overlays (captions, labels, "Your turn!",
flash cards, logo, title/end cards) are drawn here.
"""
import sys, os, math, glob, subprocess, importlib.util, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.io import wavfile
import sprites as SP

W, H, FPS, SR = 1280, 720, 24, 44100
TMP = "/tmp/dlg3d"
os.makedirs(TMP, exist_ok=True)


def sh(*a):
    subprocess.run(list(a), check=True)


def load_voice(path):
    out = f"{TMP}/{os.path.basename(path)}.wav"
    if not os.path.exists(out):
        sh("ffmpeg", "-loglevel", "error", "-y", "-i", path, "-ac", "1", "-ar", str(SR), "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,highpass=f=80,treble=g=-4:f=5500,lowpass=f=9000,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120,volume=1.1", out)
    sr, a = wavfile.read(out)
    return a.astype(np.float32) / 32768.0


def env_curve(a):
    hop = SR // FPS
    e = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2) + 1e-9) for i in range(len(a) // hop + 1)])
    return e / (e.max() + 1e-9)


def note(freq, dur, vol, kind="tri"):
    t = np.arange(int(dur * SR)) / SR
    w = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * freq * t)) if kind == "tri" else np.sin(2 * np.pi * freq * t)
    return (w * np.minimum(1, t / 0.03) * np.exp(-t * 2.5) * vol).astype(np.float32)


def music(total):
    """Soft music-box style loop (gentle for small kids)."""
    beat = 60 / 96
    mel = [72, 76, 79, 76, 74, 77, 81, 77, 72, 76, 79, 84, 81, 79, 76, 74]
    bass = [48, 48, 53, 53, 55, 55, 48, 48]
    f = lambda m: 440 * 2 ** ((m - 69) / 12)
    out = np.zeros(int(total * SR) + SR * 3, np.float32)
    t, i = 0.0, 0
    while t < total:
        s = int(t * SR)
        n = note(f(mel[i % 16]), beat * 1.2, 0.035, "sine") + np.pad(note(f(mel[i % 16] + 12), beat * 1.2, 0.012, "sine"), (0, 0))
        out[s:s + len(n)] += n
        if i % 2 == 0:
            b = note(f(bass[(i // 2) % 8]), beat * 2, 0.04, "sine")
            out[s:s + len(b)] += b
        t += beat; i += 1
    return out[: int(total * SR)]


def chime():
    out = np.zeros(int(0.9 * SR), np.float32)
    for k, m in enumerate([84, 88, 91, 96]):
        n = note(440 * 2 ** ((m - 69) / 12), 0.5, 0.07, "sine")
        s = int(k * 0.08 * SR); out[s:s + len(n)] += n[: len(out) - s]
    return out


# ------------------------------------------------------------------ timeline
def build(plan, voices_dir):
    files = {int(os.path.basename(p)[:2]): p for p in glob.glob(os.path.join(voices_dir, "*.mp3"))}
    t = 0.0
    segs, events = [], []
    track = []
    for sg in plan["segments"]:
        st = t
        t += sg.get("lead", 0.5)
        for ln in sg.get("lines", []):
            nums = ln["n"] if isinstance(ln["n"], list) else [ln["n"]]
            parts = [load_voice(files[n]) for n in nums]
            if len(parts) > 1:  # spoken together
                L = max(len(p) for p in parts); a = np.zeros(L, np.float32)
                for p in parts: a[:len(p)] += p * 0.75
            else:
                a = parts[0]
            d = len(a) / SR
            ev = dict(start=t, end=t + d, who=ln["who"], say=ln["say"], env=env_curve(a), flags=ln.get("flags", []), seg=len(segs), card=ln.get("card"), _pause=ln.get("pause", 0.5))
            events.append(ev); track.append((t, a))
            t += d + ln.get("pause", 0.5)
        t += sg.get("tail", 0.4)
        if "min" in sg and t - st < sg["min"]:
            t = st + sg["min"]
        segs.append(dict(sg, start=st, end=t))
    total = t
    mix = np.zeros(int(total * SR) + SR, np.float32)
    mask = np.zeros_like(mix)
    for st, a in track:
        s = int(st * SR); mix[s:s + len(a)] += a; mask[s:s + len(a)] = 1
    for ev in events:
        if "chime" in ev["flags"] or "reveal" in ev["flags"]:
            c = chime(); s = int(ev["start"] * SR); mix[s:s + len(c)] += c[: len(mix) - s]
    m = music(total + 1)[: len(mix)]; m = np.pad(m, (0, len(mix) - len(m)))
    k = int(0.3 * SR)
    sm = np.convolve(mask, np.ones(k) / k, mode="same")
    mix += m * (1 - 0.6 * sm)
    # fade music out at the very end
    fo = int(2.0 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
    mix = mix / max(1e-6, np.abs(mix).max()) * 0.92
    wavfile.write(f"{TMP}/mix.wav", SR, (mix[: int(total * SR)] * 32767).astype(np.int16))
    return segs, events, total


# ------------------------------------------------------------------ base video
def base_video(plan, segs, clips_dir, total):
    """Cut each segment from its clip (ping-pong loop if longer) -> base.mp4."""
    starts = plan["clip_start"]
    used = {}
    parts = []
    for i, sg in enumerate(segs):
        c = sg["clip"]; d = sg["end"] - sg["start"]
        src = os.path.join(clips_dir, c + ".mp4")
        loop = f"{TMP}/loop_{c}.mp4"
        if not os.path.exists(loop):
            ss = starts.get(c, 1.0)
            vf = "scale=1280:854,crop=1280:720:0:50,fps=24,setsar=1"
            fw, rv = f"{TMP}/fw_{c}.mp4", f"{TMP}/rv_{c}.mp4"
            sh("ffmpeg", "-loglevel", "error", "-y", "-ss", str(ss), "-i", src, "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", fw)
            sh("ffmpeg", "-loglevel", "error", "-y", "-i", fw, "-vf", "reverse", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", rv)
            with open(f"{TMP}/l_{c}.txt", "w") as fh:
                for _ in range(4):
                    fh.write(f"file '{fw}'\nfile '{rv}'\n")
            sh("ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/l_{c}.txt", "-c", "copy", loop)
        off = used.get(c, 0.0) if sg.get("continue", True) else 0.0
        used[c] = off + d
        out = f"{TMP}/seg{i:02d}.mp4"
        vf = ["fps=24"]
        if sg.get("style") == "grey":
            vf.append("hue=s=0.08,eq=brightness=0.02")
        if sg.get("style") == "blur":
            vf.append("gblur=sigma=14,eq=brightness=0.05")
        if sg.get("slow"):
            vf.insert(0, f"setpts={sg['slow']}*PTS")
        sh("ffmpeg", "-loglevel", "error", "-y", "-ss", f"{off:.3f}", "-i", loop, "-t", f"{d:.3f}", "-vf", ",".join(vf), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-r", "24", out)
        parts.append(out)
    # concat with short crossfades
    with open(f"{TMP}/parts.txt", "w") as fh:
        for p in parts:
            fh.write(f"file '{p}'\n")
    sh("ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/parts.txt", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-r", "24", f"{TMP}/base.mp4")
    return f"{TMP}/base.mp4"


# ------------------------------------------------------------------ overlays
def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=f) > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = test
    lines.append(cur); return lines


def compose(plan, clips_dir, voices_dir, out):
    segs, events, total = build(plan, voices_dir)
    base = base_video(plan, segs, clips_dir, total)
    nfr = int(total * FPS)
    print(f"duration {total:.1f}s frames {nfr}", flush=True)
    f_cap, f_name, f_big, f_turn, f_title = SP.font(36), SP.font(28), SP.font(78), SP.font(40), SP.font(56)
    logo_big, logo_small = SP.logo(120, 9), SP.logo(40, 5)
    cards = {n: SP.obj(n, 170) for n in plan.get("objects", [])}
    shelf = {n: SP.obj(n, 64) for n in plan.get("objects", [])}
    reveal_at = {}
    for ev in events:
        if "reveal" in ev["flags"] and ev.get("card"):
            reveal_at.setdefault(ev["card"], ev["start"])
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", f"{TMP}/mix.wav", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    fsz = W * H * 3
    last = None
    for fi in range(nfr):
        t = fi / FPS
        buf = dec.stdout.read(fsz)
        if len(buf) < fsz:
            buf = last
        last = buf
        img = Image.frombuffer("RGB", (W, H), buf).convert("RGBA")
        d = ImageDraw.Draw(img)
        sg = next((s for s in segs if s["start"] <= t < s["end"]), segs[-1])
        kind = sg.get("kind", "story")
        ev = None
        for e in events:
            if e["start"] <= t:
                ev = e
        cur = ev if ev and t < ev["end"] + 0.35 else None
        if kind in ("title", "end"):
            ov = Image.new("RGBA", (W, H), (255, 255, 255, 70)); img.alpha_composite(ov)
            lt = t - sg["start"]
            sc = 0.6 + 0.4 * ease(lt / 0.8)
            lg = logo_big.resize((int(logo_big.width * sc), int(logo_big.height * sc)), Image.LANCZOS)
            img.alpha_composite(lg, (W // 2 - lg.width // 2, 170 + int(8 * math.sin(t * 3))))
            sub = sg.get("text", "")
            tw = d.textlength(sub, font=f_title)
            d.text((W / 2 - tw / 2, 360), sub, font=f_title, fill=(60, 60, 110), stroke_width=7, stroke_fill="white")
            if kind == "end":
                tag = "PLAY • LEARN • DISCOVER"; tw = d.textlength(tag, font=f_turn)
                d.text((W / 2 - tw / 2, 450), tag, font=f_turn, fill=(240, 90, 60), stroke_width=6, stroke_fill="white")
        else:
            # corner logo
            img.alpha_composite(logo_small, (W - logo_small.width - 18, 16))
            # colour shelf (found colours)
            if plan.get("objects") and kind != "game":
                d.rounded_rectangle([18, 16, 18 + 6 * 70 + 12, 94], 22, fill=(255, 255, 255, 175))
                for k, n in enumerate(plan["objects"]):
                    if n in reveal_at and t >= reveal_at[n] + 0.6:
                        img.alpha_composite(shelf[n], (24 + k * 70, 22))
                    else:
                        d.ellipse([40 + k * 70, 37, 76 + k * 70, 73], outline=(160, 160, 160), width=4)
            # big colour word after reveal, for the rest of the segment
            lab = sg.get("label")
            card = sg.get("card")
            if lab and card in reveal_at and t >= reveal_at[card]:
                p = ease((t - reveal_at[card]) / 0.4)
                fb = SP.font(int(40 + 40 * p))
                tw = d.textlength(lab, font=fb)
                d.text((W - 60 - tw, 130), lab, font=fb, fill=tuple(sg["labelcol"]), stroke_width=8, stroke_fill="white")
                if p < 1:
                    for k in range(10):
                        a = math.radians(k * 36 + t * 220); r = 90 + 60 * p
                        x, y = W - 60 - tw / 2 + r * math.cos(a), 175 + r * 0.6 * math.sin(a)
                        d.polygon(SP._star_pts(x, y, 14, 6), fill=(255, 230, 80))
            # flash cards in the colour game
            if kind == "game" and ev and ev.get("card") and ev["seg"] == segs.index(sg):
                n = ev["card"]
                show = cards[n]
                rv = ev["start"] if "gamereveal" in ev["flags"] else 1e9
                cx, cy = W - 150, 215
                d.rounded_rectangle([cx - 112, cy - 112, cx + 112, cy + 112], 30, fill=(255, 255, 255, 235), outline=(255, 200, 60), width=8)
                img.alpha_composite(show, (cx - 85, cy - 85 + int(6 * math.sin(t * 3))))
                if t >= rv:
                    lab2 = n_label = plan["game_labels"][n]
                    tw = d.textlength(lab2[0], font=f_title)
                    d.text((cx - tw / 2 - 40, cy + 120), lab2[0], font=f_title, fill=tuple(lab2[1]), stroke_width=8, stroke_fill="white")
            # your turn bubble during the pause after a question
            if ev and t >= ev["end"] and "ask" in ev["flags"]:
                lt = t - ev["end"]
                if lt < ev.get("_pause", 2.4):
                    s = 1 + 0.06 * math.sin(lt * 8)
                    bw, bh = 330 * s, 86 * s
                    bx, by = W / 2 - bw / 2, 470
                    d.rounded_rectangle([bx, by, bx + bw, by + bh], 43, fill=(255, 245, 160), outline=(240, 150, 40), width=6)
                    tw = d.textlength("Your turn!", font=f_turn)
                    d.text((W / 2 - tw / 2, by + bh / 2 - 25), "Your turn!", font=f_turn, fill=(220, 80, 40))
                    for k in range(3):
                        on = (lt * 1.4) % 3 > k
                        d.ellipse([W / 2 - 30 + k * 24, by + bh + 12, W / 2 - 16 + k * 24, by + bh + 26], fill=(240, 150, 40) if on else (255, 255, 255))
        # captions
        if cur:
            name = cur["who"]
            ncol = {"Dodo": (46, 140, 50), "Dini": (230, 110, 20)}.get(name, (130, 60, 190))
            lines = wrap(d, cur["say"], f_cap, 980)
            bh = 26 + 46 * len(lines); y0 = H - bh - 20
            d.rounded_rectangle([110, y0, W - 110, H - 20], 26, fill=(255, 255, 255, 230), outline=ncol + (255,), width=4)
            nw = d.textlength(name, font=f_name)
            d.rounded_rectangle([132, y0 - 22, 132 + nw + 30, y0 + 16], 16, fill=ncol + (255,))
            d.text((147, y0 - 19), name, font=f_name, fill="white")
            for k, ln in enumerate(lines):
                tw = d.textlength(ln, font=f_cap)
                d.text((W / 2 - tw / 2, y0 + 16 + 46 * k), ln, font=f_cap, fill=(40, 40, 60))
        enc.stdin.write(img.convert("RGB").tobytes())
        if fi % 600 == 0:
            print("frame", fi, flush=True)
    enc.stdin.close(); enc.wait(); dec.kill()
    with open(out.replace(".mp4", ".srt"), "w") as fh:
        def ts(x):
            h, r = divmod(x, 3600); m, s = divmod(r, 60)
            return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"
        for k, e in enumerate(events, 1):
            fh.write(f"{k}\n{ts(e['start'])} --> {ts(e['end'] + 0.3)}\n{e['who']}: {e['say']}\n\n")
    return total, segs, events


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("p", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    tot, segs, evs = compose(m.PLAN, sys.argv[2], sys.argv[3], sys.argv[4])
    for s in segs:
        print(f"{s['start']:7.1f} {s.get('kind','story'):6s} {s['clip']}")
    print("total", tot)
