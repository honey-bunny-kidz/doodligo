import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from common import *

META = dict(code="dl003_abc", title="ABC Alphabet Adventure with Dodo and Dini | Learn A to Z for Preschoolers",
            body="Discover every letter from A to Z with Dodo and Dini: apple, ball, cat and lots more! Then play a letter guessing game.",
            tags=["ABC", "Alphabet", "LearnABC", "Phonics", "Preschool", "Doodligo"])

CLIPS = [
    "Dodo and Dini in a bright storybook classroom with colourful alphabet posters, waving hello to the camera.",
    "Giant colourful alphabet blocks gently tumble and stack around Dodo and Dini; they look amazed.",
    "Under an apple tree Dodo picks a shiny red apple; Dini bounces a big red ball beside him.",
    "A friendly cat and a happy puppy play with Dodo and Dini on the grass; a duck waddles by.",
    "In a park, Dodo and Dini watch a baby elephant spray water and colourful fish jump in a pond.",
    "Dodo and Dini fly a colourful kite on a green hill on a sunny windy day.",
    "Dini holds a big letter block upside down and scratches his head, confused; Dodo gently laughs and turns it the right way.",
    "Dodo and Dini sit together reading a giant ABC picture book, pointing at pictures.",
    "Dodo and Dini look at the camera and point at the viewer with encouraging, curious faces, waiting for an answer.",
    "At night Dodo and Dini look at the moon and stars from a cosy window, smiling.",
    "Dodo and Dini dance and celebrate with letter-shaped balloons and confetti in the classroom.",
    "Dodo and Dini wave goodbye to the camera warmly in the storybook classroom.",
]

ABC = [("A", "apple"), ("B", "ball"), ("C", "cat"), ("D", "dog"), ("E", "elephant"), ("F", "fish"), ("G", "grapes"), ("H", "hat"),
       ("I", "ice cream"), ("J", "jelly"), ("K", "kite"), ("L", "lion"), ("M", "moon"), ("N", "nest"), ("O", "orange"), ("P", "pig"),
       ("Q", "queen"), ("R", "rainbow"), ("S", "sun"), ("T", "tree"), ("U", "umbrella"), ("V", "van"), ("W", "whale"), ("X", "xylophone"),
       ("Y", "yo-yo"), ("Z", "zebra")]
CLIP_FOR = {"A": "c03", "B": "c03", "C": "c04", "D": "c04", "E": "c05", "F": "c05", "G": "c08", "H": "c08", "I": "c02", "J": "c02",
            "K": "c06", "L": "c06", "M": "c10", "N": "c10", "O": "c08", "P": "c08", "Q": "c02", "R": "c06", "S": "c06", "T": "c03",
            "U": "c08", "V": "c02", "W": "c05", "X": "c11", "Y": "c11", "Z": "c05"}


def letter_line(i, L_, w):
    who = DO if i % 2 == 0 else DI
    return who(f"{L_} is for {w}!", card=C(L_, PALETTE[i % len(PALETTE)], sub=w))


body = [dict(clip="c01", lines=intro("Today we are going on an A B C adventure!", "Letters! I love letters! Let's go!"))]
# group consecutive letters that share a clip
i = 0
while i < 26:
    c = CLIP_FOR[ABC[i][0]]
    lines = []
    while i < 26 and CLIP_FOR[ABC[i][0]] == c:
        lines.append(letter_line(i, *ABC[i]))
        if ABC[i][0] in ("A", "M"):
            lines.append(ASK(f"Can you say {ABC[i][0]}?", pause=2.0))
        i += 1
    body.append(dict(clip=c, lines=lines))
    if ABC[i - 1][0] == "F":
        body.append(dict(clip="c07", lines=[DI("G is for... giraffe? No, wait!"), DO("Silly Dini! G is for grapes, and giraffe too!", flags=["chime"])]))
body += [
    dict(clip="c09", kind="game", lines=[
        DO("Let's play a letter game! What letter is this?"),
        ASK("What letter is this?", card=C("B", BLUE, q="?", sub="ball")), DI("B! B is for ball!", flags=["chime"], card=C("B", BLUE, sub="ball"), pause=0.8),
        ASK("What letter is this?", card=C("S", ORG, q="?", sub="sun")), DI("S! S is for sun!", flags=["chime"], card=C("S", ORG, sub="sun"), pause=0.8),
        ASK("What letter is this?", card=C("Z", PUR, q="?", sub="zebra")), DI("Z! Z is for zebra!", flags=["chime"], card=C("Z", PUR, sub="zebra"), pause=0.8)]),
    dict(clip="c11", lines=[
        DO("Let's say the whole alphabet together!"),
        DO("A, B, C, D, E, F, G", card=C("A–G", RED)), DI("H, I, J, K, L, M, N, O, P", card=C("H–P", BLUE)),
        DO("Q, R, S, T, U, V", card=C("Q–V", GRN)), DI("W, X, Y and Z!", card=C("W–Z", ORG)),
        DO("Wow! We learned all the letters from A to Z!", flags=["chime"])]),
]

PLAN = standard("ABC Alphabet Adventure", CLIPS, body, "Share this video with a friend who loves the A B C!")
