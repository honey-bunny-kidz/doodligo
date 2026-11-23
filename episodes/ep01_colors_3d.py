"""Doodligo Ep01 (3D): Learn Colors with Dodo and Dini.
Clips c01–c12 and voice lines 01–49 were generated with Muse (muse.ai)."""

RED, BLUE, YEL, GRN, ORG, PUR = (225, 35, 45), (40, 110, 230), (235, 180, 0), (50, 160, 60), (245, 125, 10), (140, 60, 190)


def L(n, who, say, pause=0.55, flags=(), card=None):
    return dict(n=n, who=who, say=say, pause=pause, flags=list(flags), card=card)


def ASK(n, say, pause=2.4, card=None):
    return L(n, "Dodo", say, pause=pause, flags=["ask"], card=card)


PLAN = dict(
    objects=["apple", "balloon", "star", "leaf", "orange", "flower"],
    clip_start=dict(c01=1.2, c02=2.4, c03=1.2, c04=1.3, c05=1.7, c06=2.0, c07=0.8, c08=1.0, c09=1.0, c10=0.9, c11=1.1, c12=3.0),
    game_labels=dict(balloon=("BLUE", BLUE), apple=("RED", RED), leaf=("GREEN", GRN), flower=("PURPLE", PUR), star=("YELLOW", YEL), orange=("ORANGE", ORG)),
    segments=[
        dict(kind="title", clip="c08", style="blur", text="Learn Colors with Dodo and Dini", lead=0, min=4.5, continue_=False),
        dict(clip="c09", style="grey", lead=0.4, lines=[
            L(1, "Dodo", "Hi, little explorers! I'm Dodo!"),
            L(2, "Dini", "And I'm Dini! Dino-hello!")]),
        dict(clip="c01", lead=0.2, lines=[
            L(3, "Dodo", "Welcome to the rainbow garden. But oh no! Everything is grey!"),
            L(4, "Dini", "Where did all the colors go?"),
            L(5, "Dodo", "Let's find six colorful things and bring the colors back!")]),
        dict(clip="c02", label="RED", labelcol=RED, card="apple", lines=[
            L(6, "Dini", "Look! A blue apple!"),
            L(7, "Dodo", "Not quite, Dini. This apple is red!", flags=["reveal"], card="apple"),
            ASK(8, "Red! Can you say red?"),
            L(9, "Dini", "Red! Red like a yummy apple!")]),
        dict(clip="c10", lead=0.2, lines=[ASK(10, "Can you find something red near you?", pause=3.0)]),
        dict(clip="c03", label="BLUE", labelcol=BLUE, card="balloon", lines=[
            L(11, "Dodo", "What is floating up there?"),
            L(12, "Dini", "A balloon! Is it yellow?"),
            ASK(13, "No, silly! What color is the balloon?"),
            L(14, "Dodo", "It's blue! Blue like the sky!", flags=["reveal"], card="balloon"),
            L(15, "Dini", "Blue! Dino-wow!")]),
        dict(clip="c04", label="YELLOW", labelcol=YEL, card="star", lines=[
            L(16, "Dini", "Something is shining! Ooh, a green star!"),
            L(17, "Dodo", "Try again, Dini. The star is yellow!", flags=["reveal"], card="star"),
            ASK(18, "Can you say yellow?"),
            L(19, "Dini", "Yellow! Yellow like the sunshine!")]),
        dict(clip="c05", label="GREEN", labelcol=GRN, card="leaf", lines=[
            L(20, "Dodo", "Look, a little leaf!"),
            L(21, "Dini", "Is it purple?"),
            L(22, "Dodo", "No, it's green! Just like you, Dini!", flags=["reveal"], card="leaf"),
            L(23, "Dini", "Green like me! Hooray!"),
            ASK(24, "Which thing is green? The leaf!", pause=1.6)]),
        dict(clip="c11", lead=0.3, lines=[L(25, "Dini", "Mmm, a round fruit! Is it red?")]),
        dict(clip="c06", label="ORANGE", labelcol=ORG, card="orange", lead=0.2, lines=[
            L(26, "Dodo", "Close! This is an orange, and its color is orange too!", flags=["reveal"], card="orange"),
            ASK(27, "Say orange!"),
            L(28, "Dini", "Orange! Like your sneakers, Dodo!")]),
        dict(clip="c07", label="PURPLE", labelcol=PUR, card="flower", lines=[
            L(29, "Dodo", "One more color to find!"),
            L(30, "Dini", "A pretty flower! Is it blue?"),
            L(31, "Dodo", "Almost! This flower is purple!", flags=["reveal"], card="flower"),
            ASK(32, "Can you say purple?"),
            L(33, "Dini", "Purple! I love purple!")]),
        dict(clip="c08", lines=[
            L(34, "Dodo", "We found all six colors! Look at the garden!", flags=["chime"]),
            L(35, "Dini", "The rainbow is back! Hooray!")]),
        dict(kind="game", clip="c10", lines=[
            L(36, "Dodo", "Let's play a color game! I show a thing, you shout the color!"),
            *[x for obj in ["balloon", "apple", "leaf", "flower", "star", "orange"]
              for x in (L(37, "Dodo", "What color is this?", pause=2.2, flags=["ask"], card=obj),
                        L({"balloon": 38, "apple": 39, "leaf": 40, "flower": 41, "star": 42, "orange": 43}[obj], "Dini",
                          {"balloon": "Blue!", "apple": "Red!", "leaf": "Green!", "flower": "Purple!", "star": "Yellow!", "orange": "Orange!"}[obj],
                          pause=0.8, flags=["gamereveal", "chime"], card=obj))]]),
        dict(clip="c10", lines=[ASK(44, "Can you remember all six colors?", pause=3.0)]),
        dict(clip="c12", lines=[
            L(45, "Dodo", "Wow! We learned six beautiful colors today!"),
            L(46, "Dini", "Red, blue, yellow, green, orange and purple! Dino-wow!")]),
        dict(clip="c09", lines=[
            L(47, "Dodo", "Share this video with a friend who loves colors!"),
            L([48, 49], "Dodo & Dini", "See you next time, little explorers!")]),
        dict(kind="end", clip="c12", style="blur", text="See you next time!", lead=0, min=5.0),
    ],
)
