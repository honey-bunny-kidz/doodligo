"""Shared helpers for Doodligo episode plans (3D Muse workflow)."""

RED, BLUE, YEL, GRN, ORG, PUR, PINK, BRN = (225, 35, 45), (40, 110, 230), (235, 180, 0), (50, 160, 60), (245, 125, 10), (140, 60, 190), (235, 80, 150), (140, 90, 50)
PALETTE = [RED, BLUE, GRN, ORG, PUR, PINK, YEL]


def L(who, say, pause=0.55, flags=(), card=None):
    return dict(who=who, say=say, pause=pause, flags=list(flags), card=card)


def DO(say, **k):
    return L("Dodo", say, **k)


def DI(say, **k):
    return L("Dini", say, **k)


def ASK(say, pause=2.4, card=None, who="Dodo"):
    return L(who, say, pause=pause, flags=["ask"], card=card)


def BOTH(say, **k):
    return L("Dodo & Dini", say, **k)


def C(text, col=BLUE, **k):
    """Flash card."""
    return dict(text=text, col=col, **k)


def intro(topic_line, dini_line):
    return [DO("Hi, little explorers! I'm Dodo!"), DI("And I'm Dini! Dino-hello!"), DO(topic_line), DI(dini_line)]


def outro(share_line):
    return [DO(share_line), BOTH("See you next time, little explorers!")]


def standard(title, clips, body, share, clip_start=None):
    """title card + body segments + goodbye + end card. clips: 12 Muse prompts.
    Conventions: c01 = wave hello, c12 = wave goodbye, c11 = celebrate dance."""
    segs = [dict(kind="title", clip="c11", style="blur", text=title, lead=0, min=4.5)]
    segs += body
    segs += [dict(clip="c12", lines=outro(share)),
             dict(kind="end", clip="c11", style="blur", text="See you next time!", lead=0, min=5.0)]
    cs = dict(c01=1.2, c02=1.4, c03=1.4, c04=1.4, c05=1.4, c06=1.4, c07=1.4, c08=1.4, c09=1.2, c10=1.2, c11=2.2, c12=1.2)
    cs.update(clip_start or {})
    return dict(clips=clips, clip_start=cs, segments=segs)


STYLE = ("3D Pixar-style, same Dodo and Dini as the references (Dodo: brown-haired boy, green hoodie, blue shorts, "
         "orange sneakers; Dini: small green baby dinosaur, yellow belly, orange back spikes), 16:9, ~10 s, no speech, gentle motion")
