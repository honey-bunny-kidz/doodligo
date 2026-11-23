"""Doodligo episode renderer: script JSON -> narrated, captioned MP4.

Usage: python3 render.py episodes/ep01_colors.py out.mp4
"""
import sys, os, math, json, subprocess, importlib.util, random, shutil
import numpy as np
from PIL import Image, ImageDraw
from scipy.io import wavfile
import sprites as SP

W, H, FPS, SR = 1280, 720, 24, 44100
TMP = "/tmp/dlg"
os.makedirs(TMP, exist_ok=True)

VOICES = {  # flite voice, pitch factor, tempo
    "Dodo": ("slt", 1.10, 0.92),
    "Dini": ("kal16", 1.32, 0.95),
}


def tts(speaker, text, idx):
    path = f"{TMP}/l{idx:03d}_{speaker}.wav"
    if os.path.exists(path):
        return path
    voice, pitch, tempo = VOICES[speaker]
    safe = text.replace("'", "").replace(":", " ").replace(",", " ,")
    raw = f"{TMP}/raw{idx:03d}.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"flite=text='{safe}':voice={voice}", raw], check=True)
    sr0 = int(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=sample_rate", "-of", "csv=p=0", raw]).strip())
    af = f"asetrate={int(sr0 * pitch)},aresample={SR},atempo={tempo / pitch * 1.0:.4f},atempo=1.0,highpass=f=90,lowpass=f=7000,volume=1.6"
    # keep pitch raised but bring speed back toward natural
    af = f"asetrate={int(sr0 * pitch)},aresample={SR},atempo={max(0.5, tempo / pitch):.4f},volume=1.7"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-af", af, "-ac", "1", path], check=True)
    return path


def load_wav(p):
    sr, a = wavfile.read(p)
    a = a.astype(np.float32)
    if a.ndim > 1:
        a = a.mean(1)
    a /= 32768.0
    return a


def note_tone(freq, dur, vol=0.2, kind="tri"):
    t = np.arange(int(dur * SR)) / SR
    if kind == "tri":
        w = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * freq * t))
    else:
        w = np.sin(2 * np.pi * freq * t)
    env = np.minimum(1, t / 0.02) * np.exp(-t * 3.0)
    return (w * env * vol).astype(np.float32)


def music(total):
    """Playful looping melody (C major pentatonic) + bass, gentle."""
    bpm = 104
    beat = 60 / bpm
    mel = [72, 76, 79, 76, 74, 77, 81, 77, 72, 76, 79, 84, 81, 79, 76, 74]
    bass = [48, 48, 53, 53, 55, 55, 48, 48]
    out = np.zeros(int(total * SR) + SR, np.float32)
    f = lambda m: 440 * 2 ** ((m - 69) / 12)
    t, i = 0.0, 0
    while t < total:
        s = int(t * SR)
        n = note_tone(f(mel[i % len(mel)]), beat * 0.9, 0.05)
        out[s:s + len(n)] += n[: len(out) - s]
        if i % 2 == 0:
            b = note_tone(f(bass[(i // 2) % len(bass)]), beat * 1.8, 0.06, "sine")
            out[s:s + len(b)] += b[: len(out) - s]
        t += beat
        i += 1
    return out[: int(total * SR)]


def chime(dur=0.9):
    out = np.zeros(int(dur * SR), np.float32)
    for k, m in enumerate([84, 88, 91, 96]):
        n = note_tone(440 * 2 ** ((m - 69) / 12), 0.5, 0.12, "sine")
        s = int(k * 0.08 * SR)
        out[s:s + len(n)] += n[: len(out) - s]
    return out


def env_curve(a, fps=FPS):
    hop = SR // fps
    n = len(a) // hop + 1
    e = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2) + 1e-9) for i in range(n)])
    e = e / (e.max() + 1e-9)
    return e


def build(ep):
    """Turn episode events into a timeline with audio."""
    t = 0.0
    tl = []
    voice_track = []
    idx = 0
    for sc in ep["scenes"]:
        sc_start = t
        lead = sc.get("lead", 0.6)
        t += lead
        for ln in sc["lines"]:
            spk, text = ln["who"], ln["say"]
            if spk == "Both":
                pa = load_wav(tts("Dodo", text, idx)); pb = load_wav(tts("Dini", text, idx + 500))
                n = max(len(pa), len(pb)); a = np.zeros(n, np.float32); a[:len(pa)] += pa * 0.7; a[:len(pb)] += pb * 0.7
            else:
                a = load_wav(tts(spk, text, idx))
            idx += 1
            dur = len(a) / SR
            if "item" in ln:
                sc.setdefault("_items", []).append(dict(ln["item"], start=t, reveal=1e9))
            if "gamereveal" in ln.get("flags", []):
                sc["_items"][-1]["reveal"] = t
            ev = dict(scene=sc["id"], who=spk, say=text, start=t, end=t + dur, env=env_curve(a), flags=ln.get("flags", []))
            voice_track.append((t, a))
            tl.append(ev)
            t += dur + ln.get("pause", 0.45)
        t += sc.get("tail", 0.6)
        sc["start"], sc["end"] = sc_start, t
    total = t
    mix = np.zeros(int(total * SR) + SR, np.float32)
    vocal_mask = np.zeros_like(mix)
    for st, a in voice_track:
        s = int(st * SR)
        mix[s:s + len(a)] += a
        vocal_mask[s:s + len(a)] = 1
    for ev in tl:
        if "reveal" in ev["flags"] or "chime" in ev["flags"]:
            c = chime(); s = int(ev["start"] * SR)
            mix[s:s + len(c)] += c[: len(mix) - s]
    m = music(total + 1)[: len(mix)]
    m = np.pad(m, (0, len(mix) - len(m)))
    # duck music under speech (smoothed mask)
    k = int(0.25 * SR)
    sm = np.convolve(vocal_mask, np.ones(k) / k, mode="same")
    mix += m * (1 - 0.55 * sm)
    mix = np.clip(mix / max(1.0, np.abs(mix).max() / 0.95), -1, 1)
    wavfile.write(f"{TMP}/mix.wav", SR, (mix[: int(total * SR)] * 32767).astype(np.int16))
    return tl, total


# ------------------------------------------------------------------ drawing
def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


class Painter:
    def __init__(self, ep):
        self.ep = ep
        self.bg_col = np.asarray(SP.garden(rainbow=False), np.float32)
        self.bg_rain = np.asarray(SP.garden(rainbow=True), np.float32)
        g = np.asarray(SP.grey(SP.garden(rainbow=False).convert("RGBA")).convert("RGB"), np.float32)
        self.bg_grey = g
        self.dodo = {(m, b): SP.dodo(m, b) for m in (0, 0.5, 1) for b in (False, True)}
        self.dodo_up = {m: SP.dodo(m, False, arm_up=True) for m in (0, 0.5, 1)}
        self.dini = {(m, b): SP.dini(m, b) for m in (0, 0.5, 1) for b in (False, True)}
        self.objs = {n: (SP.obj(n, 230), SP.grey(SP.obj(n, 230))) for n in ep["objects"]}
        self.small = {n: SP.obj(n, 70) for n in ep["objects"]}
        self.logo_big = SP.logo(120, 9)
        self.logo_small = SP.logo(44, 5)
        self.flies = [SP.butterfly(c) for c in [(255, 110, 180), (255, 200, 40), (90, 150, 240)]]
        self.f_cap = SP.font(34); self.f_name = SP.font(30); self.f_title = SP.font(54); self.f_turn = SP.font(40)

    def paste(self, img, sprite, x, y):
        img.alpha_composite(sprite, (int(x), int(y)))


def mouth_level(ev, t):
    if ev is None or not (ev["start"] <= t < ev["end"]):
        return 0
    i = int((t - ev["start"]) * FPS)
    e = ev["env"][min(i, len(ev["env"]) - 1)]
    return 0 if e < 0.12 else (0.5 if e < 0.45 else 1)


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=f) > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = test
    lines.append(cur)
    return lines


def render(ep, out):
    tl, total = build(ep)
    P = Painter(ep)
    scenes = {s["id"]: s for s in ep["scenes"]}
    # reveal times per object (for colour progress / collection)
    reveal_t = {}
    for ev in tl:
        for f in ev["flags"]:
            if f == "reveal":
                o = scenes[ev["scene"]].get("object")
                if o and o not in reveal_t:
                    reveal_t[o] = ev["start"]
    game_reveal = {}
    for ev in tl:
        if "gamereveal" in ev["flags"]:
            game_reveal[(ev["scene"], ev.get("say"))] = ev["start"]
    nobj = len(ep["objects"])
    frames = int(total * FPS) + 1
    print(f"duration {total:.1f}s, frames {frames}", flush=True)
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", f"{TMP}/mix.wav", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    rnd = random.Random(1)
    blink_times = sorted(rnd.uniform(0, total) for _ in range(int(total / 3)))
    ev_i = 0
    for fi in range(frames):
        t = fi / FPS
        while ev_i + 1 < len(tl) and tl[ev_i + 1]["start"] <= t:
            ev_i += 1
        ev = tl[ev_i] if tl and tl[ev_i]["start"] <= t else None
        cur_ev = ev if ev and t < ev["end"] + 1.2 else None
        sc = next((s for s in ep["scenes"] if s["start"] <= t < s["end"]), ep["scenes"][-1])
        kind = sc.get("kind", "story")
        # colour progress
        found = sum(ease((t - rt) / 1.2) for rt in reveal_t.values() if t >= rt)
        prog = found / nobj
        if kind in ("title", "end", "finale", "game", "recap"):
            prog = 1.0
        base = P.bg_grey * (1 - prog) + P.bg_col * prog
        if kind in ("finale", "game", "recap", "end"):
            rp = ease((t - scenes.get("finale", sc)["start"]) / 1.5) if "finale" in scenes else 1
            base = P.bg_col * (1 - rp) + P.bg_rain * rp
        img = Image.fromarray(base.astype(np.uint8)).convert("RGBA")
        d = ImageDraw.Draw(img)

        if kind == "title" or kind == "end":
            ov = Image.new("RGBA", (W, H), (255, 255, 255, 90)); img.alpha_composite(ov)
            lt = (t - sc["start"])
            sc_l = 0.6 + 0.4 * ease(lt / 0.8)
            lg = P.logo_big.resize((int(P.logo_big.width * sc_l), int(P.logo_big.height * sc_l)), Image.LANCZOS)
            img.alpha_composite(lg, (W // 2 - lg.width // 2, 150 + int(8 * math.sin(t * 3))))
            sub = sc.get("text", "")
            tw = d.textlength(sub, font=P.f_title)
            d.text((W / 2 - tw / 2, 340), sub, font=P.f_title, fill=(60, 60, 110), stroke_width=6, stroke_fill="white")
            if kind == "end":
                tag = "PLAY • LEARN • DISCOVER"
                tw = d.textlength(tag, font=P.f_turn)
                d.text((W / 2 - tw / 2, 430), tag, font=P.f_turn, fill=(240, 90, 60), stroke_width=5, stroke_fill="white")
        # butterflies
        for k, bf in enumerate(P.flies):
            if (prog < 0.3 and kind == "story") or kind in ("title", "end"):
                continue
            x = (t * (40 + 15 * k) + 300 * k) % (W + 200) - 100
            y = 220 + 60 * k + 30 * math.sin(t * 1.7 + k)
            flap = abs(math.sin(t * 9 + k))
            b = bf.resize((bf.width, max(8, int(bf.height * (0.5 + 0.5 * flap)))))
            img.alpha_composite(b, (int(x), int(y)))

        if kind not in ("title", "end"):
            # characters
            speaking = cur_ev["who"] if cur_ev and t < cur_ev["end"] else None
            blink = any(0 <= t - bt < 0.12 for bt in blink_times)
            m_dodo = mouth_level(cur_ev, t) if speaking in ("Dodo", "Both") else 0
            m_dini = mouth_level(cur_ev, t) if speaking in ("Dini", "Both") else 0
            hop_d = abs(math.sin(t * 7)) * 8 if speaking in ("Dodo", "Both") else 0
            hop_n = abs(math.sin(t * 7.5)) * 10 if speaking in ("Dini", "Both") else 0
            celebrate = kind in ("finale", "end") or (cur_ev and "cheer" in cur_ev["flags"])
            if celebrate:
                hop_d = abs(math.sin(t * 6)) * 26; hop_n = abs(math.sin(t * 6 + 1)) * 30
            bob = math.sin(t * 2.2) * 3
            point = cur_ev and "point" in cur_ev["flags"] and speaking == "Dodo"
            spr_d = P.dodo_up[m_dodo] if (point or celebrate) else P.dodo[(m_dodo, blink)]
            P.paste(img, spr_d, 230, 600 - spr_d.height + 18 - hop_d + bob)
            spr_n = P.dini[(m_dini, blink)]
            P.paste(img, spr_n, 430, 610 - spr_n.height + 10 - hop_n - bob)
            # wrong guess marker
            if cur_ev and "wrong" in cur_ev["flags"] and t < cur_ev["end"] + 0.6:
                d.text((640, 330 - 10 * math.sin(t * 6)), "?", font=P.f_title, fill=(240, 90, 60), stroke_width=5, stroke_fill="white")
            # current object
            o = sc.get("object")
            if o and kind == "story":
                lt = t - sc["start"]
                col, gr = P.objs[o]
                appear = ease(lt / 0.7)
                rv = reveal_t.get(o, 1e9)
                cp = ease((t - rv) / 0.6)
                spr = Image.blend(gr, col, cp) if 0 < cp < 1 else (col if cp >= 1 else gr)
                if appear < 1:
                    s2 = max(1, int(spr.width * appear)); spr = spr.resize((s2, s2))
                fy = 8 * math.sin(t * 2.5)
                if o == "balloon":
                    fy = 160 * (1 - appear) + 14 * math.sin(t * 1.8)
                cx, cy = 900, 300
                if cp > 0 and cp < 1:
                    for k in range(10):
                        a = k * 36 + t * 200
                        r = 140 + 40 * cp
                        x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
                        d.polygon(SP._star_pts(x, y, 16, 7), fill=(255, 230, 80))
                img.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2 + fy)))
                if cp >= 1:
                    lab = sc.get("label", "")
                    tw = d.textlength(lab, font=P.f_title)
                    d.text((cx - tw / 2, 445), lab, font=P.f_title, fill=tuple(sc.get("labelcol", (60, 60, 60))), stroke_width=6, stroke_fill="white")
            if kind == "game":
                # find the current game item based on time
                items = sc["_items"]
                cur = None
                for it in items:
                    if it["start"] <= t:
                        cur = it
                if cur:
                    col, gr = P.objs[cur["obj"]]
                    cp = ease((t - cur["reveal"]) / 0.4) if t >= cur["reveal"] else 0
                    spr = Image.blend(gr, col, cp)
                    img.alpha_composite(spr, (900 - spr.width // 2, 300 - spr.height // 2 + int(8 * math.sin(t * 3))))
                    if cp >= 1:
                        lab = cur["label"]; tw = d.textlength(lab, font=P.f_title)
                        d.text((900 - tw / 2, 445), lab, font=P.f_title, fill=tuple(cur["col"]), stroke_width=6, stroke_fill="white")
            if kind in ("finale", "recap"):
                n = len(ep["objects"])
                for k, oname in enumerate(ep["objects"]):
                    spr = P.objs[oname][0].resize((130, 130), Image.LANCZOS)
                    ang = k / n * 2 * math.pi + t * 0.6
                    x = 930 + 210 * math.cos(ang) * 0.75; y = 290 + 130 * math.sin(ang)
                    img.alpha_composite(spr, (int(x - 65), int(y - 65)))
            # collection shelf
            if kind == "story":
                d.rounded_rectangle([20, 20, 20 + 6 * 78 + 14, 108], 22, fill=(255, 255, 255, 170))
                for k, oname in enumerate(ep["objects"]):
                    if oname in reveal_t and t >= reveal_t[oname] + 0.6:
                        img.alpha_composite(P.small[oname], (30 + k * 78, 28))
                    else:
                        d.ellipse([44 + k * 78, 42, 86 + k * 78, 84], outline=(170, 170, 170), width=4)
                lg = P.logo_small
                img.alpha_composite(lg, (W - lg.width - 20, 24))
            # your turn bubble during pauses
            if ev and t >= ev["end"] and "ask" in ev["flags"]:
                lt = t - ev["end"]
                if lt < 2.4:
                    sc_b = 1 + 0.06 * math.sin(lt * 8)
                    bw, bh = 300 * sc_b, 80 * sc_b
                    bx, by = 640 - bw / 2 + 260, 520 - bh / 2 - 380
                    d.rounded_rectangle([bx, by + 300, bx + bw, by + 300 + bh], 40, fill=(255, 245, 160), outline=(240, 150, 40), width=5)
                    tw = d.textlength("Your turn!", font=P.f_turn)
                    d.text((bx + bw / 2 - tw / 2, by + 300 + bh / 2 - 24), "Your turn!", font=P.f_turn, fill=(220, 80, 40))
        # captions (burned-in closed captions)
        if cur_ev and t < cur_ev["end"] + 0.35:
            name = cur_ev["who"] if cur_ev["who"] != "Both" else "Dodo & Dini"
            ncol = {"Dodo": (46, 140, 50), "Dini": (230, 110, 20)}.get(cur_ev["who"], (130, 60, 190))
            lines = wrap(d, cur_ev["say"], P.f_cap, 980)
            bh = 26 + 44 * len(lines)
            y0 = H - bh - 18
            d.rounded_rectangle([110, y0, W - 110, H - 18], 24, fill=(255, 255, 255, 225), outline=ncol + (255,), width=4)
            nw = d.textlength(name, font=P.f_name)
            d.rounded_rectangle([130, y0 - 22, 130 + nw + 30, y0 + 18], 16, fill=ncol + (255,))
            d.text((145, y0 - 19), name, font=P.f_name, fill="white")
            for k, ln in enumerate(lines):
                tw = d.textlength(ln, font=P.f_cap)
                d.text((W / 2 - tw / 2, y0 + 16 + 44 * k), ln, font=P.f_cap, fill=(40, 40, 60))
        ff.stdin.write(img.convert("RGB").tobytes())
        if fi % 480 == 0:
            print(f"frame {fi}/{frames}", flush=True)
    ff.stdin.close(); ff.wait()
    # write captions file too (SRT) for YouTube CC
    with open(out.replace(".mp4", ".srt"), "w") as fh:
        for k, e in enumerate(tl, 1):
            def ts(x):
                h, r = divmod(x, 3600); m, s = divmod(r, 60)
                return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"
            nm = "Dodo & Dini" if e["who"] == "Both" else e["who"]
            fh.write(f"{k}\n{ts(e['start'])} --> {ts(e['end'] + 0.3)}\n{nm}: {e['say']}\n\n")
    return total


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("ep", sys.argv[1])
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    ep = m.EPISODE
    # game items need timings: game scene lines are generated in episode file with flags
    print(render(ep, sys.argv[2]))
