import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from common import *

META = dict(code="dl005_shapes", title="Shapes Adventure with Dodo and Dini | Circle, Square and Triangle for Preschoolers",
            body="Find shapes all around us with Dodo and Dini: circle, square, triangle, rectangle, star and heart! Then play a shape game.",
            tags=["Shapes", "LearnShapes", "ShapesForKids", "Preschool", "Doodligo"])

CLIPS = [
    "Dodo and Dini in a colourful toy playroom full of shape toys, waving hello to the camera.",
    "Dodo rolls a big round beach ball to Dini; a round wall clock ticks behind them.",
    "Dodo and Dini open a square gift box and peek out of a square window.",
    "Dodo and Dini share a triangle slice of pizza at a picnic, next to a triangle tent.",
    "Dodo opens a rectangle door and Dini carries a big rectangle picture book.",
    "Dodo and Dini hang shining star decorations and catch a twinkling star.",
    "Dini gives Dodo a red heart-shaped balloon; they hug happily.",
    "Dini tries to fit a square block into a round hole with a confused face; Dodo gently giggles and helps him.",
    "Dodo and Dini look at the camera and point at the viewer with encouraging, curious faces, waiting for an answer.",
    "Dodo and Dini build a little house from shape blocks: square walls and a triangle roof.",
    "Dodo and Dini dance and celebrate with colourful shape confetti.",
    "Dodo and Dini wave goodbye to the camera warmly in the playroom.",
]

SHAPES = [("circle", "c02", RED, "A ball is a circle! Round and round!"), ("square", "c03", BLUE, "A box is a square! Four sides the same!"),
          ("triangle", "c04", ORG, "Pizza is a triangle! Three sides, three corners!"), ("rectangle", "c05", GRN, "A door is a rectangle! Long and tall!"),
          ("star", "c06", YEL, "A star! It has five points! Twinkle, twinkle!"), ("heart", "c07", PINK, "A heart! I love you, Dodo!")]

body = [dict(clip="c01", lines=intro("Today we are going on a shapes adventure!", "Shapes are everywhere! Let's find them!"))]
for k, (s, clip, col, fact) in enumerate(SHAPES):
    card = C(s, col, shape=s)
    who_fact = DI if s == "heart" else DO
    lines = [DO(f"Look! What shape is this?", card=C(s, col, shape=s)),
             DO(f"It's a {s}!", flags=["reveal"], card=card), who_fact(fact, card=card)]
    if s in ("circle", "triangle", "heart"):
        lines.append(ASK(f"Can you draw a {s} in the air?", pause=2.6))
    body.append(dict(clip=clip, label=s.upper(), labelcol=col, lines=lines))
    if s == "square":
        body.append(dict(clip="c08", lines=[DI("This square block won't fit in the round hole!"), DO("Silly Dini! Squares go in the square hole!", flags=["chime"])]))
body += [
    dict(clip="c09", kind="game", lines=[
        DO("Let's play a shape game! What shape is this?"),
        ASK("What shape is this?", card=C("triangle", ORG, shape="triangle")), DI("A triangle!", flags=["chime"], card=C("triangle", ORG, shape="triangle"), pause=0.8),
        ASK("What shape is this?", card=C("circle", RED, shape="circle")), DI("A circle!", flags=["chime"], card=C("circle", RED, shape="circle"), pause=0.8),
        ASK("What shape is this?", card=C("star", YEL, shape="star")), DI("A star!", flags=["chime"], card=C("star", YEL, shape="star"), pause=0.8),
        ASK("What shape is this?", card=C("square", BLUE, shape="square")), DI("A square!", flags=["chime"], card=C("square", BLUE, shape="square"), pause=0.8)]),
    dict(clip="c10", lines=[
        DO("Look! We made a house with shapes! Square walls and a triangle roof!", flags=["chime"]),
        DI("Circle, square, triangle, rectangle, star and heart! Dino-wow!")]),
]

PLAN = standard("Shapes Adventure", CLIPS, body, "Share this video with a friend who loves shapes!")
