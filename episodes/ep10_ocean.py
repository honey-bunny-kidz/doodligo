import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from common import *

META = dict(code="dl010_ocean", title="Underwater Adventure with Dodo and Dini | Ocean Animals for Preschoolers",
            body="Dive under the sea with Dodo and Dini! Meet the fish, turtle, dolphin, whale, octopus and crab, with easy ocean facts for little ones.",
            tags=["OceanAnimals", "SeaAnimals", "UnderTheSea", "Preschool", "Doodligo"])

CLIPS = [
    "On a sunny beach Dodo and Dini put on little diving masks, then wave hello to the camera.",
    "Underwater: colourful little fish swim around Dodo and Dini (in diving masks) among coral, bubbles rising.",
    "Underwater: a friendly sea turtle swims slowly beside Dodo and Dini; Dini rides gently on its shell.",
    "Underwater: a happy dolphin swims and spins around Dodo and Dini playfully.",
    "Underwater: a huge gentle blue whale swims by; Dodo and Dini look tiny and amazed.",
    "Underwater: a cute pink octopus waves its eight arms at Dodo and Dini; they wave back.",
    "On the sandy sea floor a little red crab walks sideways; Dini tries to walk sideways too with a silly confused face, Dodo giggles.",
    "Underwater: a bright orange starfish on a rock; Dodo gently points at its five arms.",
    "Underwater: Dodo and Dini look at the camera and point at the viewer with encouraging, curious faces, waiting for an answer.",
    "Underwater: Dodo and Dini swim through sparkling bubbles and sun rays from above.",
    "Underwater: Dodo and Dini dance and celebrate with the sea animals around them.",
    "Back on the beach at sunset, Dodo and Dini wave goodbye to the camera warmly.",
]

SEA = [("fish", "c02", ORG, "Fish swim with their fins and tails! Swish, swish!"), ("turtle", "c03", GRN, "The turtle carries his shell like a little house!"),
       ("dolphin", "c04", BLUE, "Dolphins are friendly and love to jump and play!"), ("whale", "c05", (40, 80, 170), "The whale is the biggest animal in the ocean!"),
       ("octopus", "c06", PINK, "The octopus has eight wiggly arms!"), ("crab", "c07", RED, "The crab walks sideways! Click, click!")]

body = [dict(clip="c01", lines=intro("Today we are going under the sea!", "Splash! Let's dive in and meet the ocean animals!"))]
for k, (a, clip, col, fact) in enumerate(SEA):
    card = C(a.upper(), col)
    lines = [DI("Look! Who is swimming there?") if k % 2 == 0 else DO("Who is that?"),
             DO(f"It's {'an' if a[0] in 'aeiou' else 'a'} {a}!", flags=["reveal"], card=card),
             (DO if k % 2 == 0 else DI)(fact, card=card)]
    if a in ("fish", "octopus", "crab"):
        lines.append(ASK({"fish": "Can you swim like a fish with your hands?", "octopus": "Can you wiggle your arms like an octopus?",
                          "crab": "Can you pinch like a crab? Click, click!"}[a], pause=2.6))
    if a == "crab":
        lines.insert(3, DI("I'm walking sideways too! Whoa, whoa!"))
    body.append(dict(clip=clip, label=a.upper(), labelcol=col, lines=lines))
body += [
    dict(clip="c08", label="STARFISH", labelcol=ORG, lines=[
        DO("And look, a starfish! It has five arms, like a star!", flags=["reveal", "chime"], card=C("STARFISH", ORG))]),
    dict(clip="c09", kind="game", lines=[
        DO("Let's play an ocean game! Who is it?"),
        ASK("Who has eight wiggly arms?", card=C("OCTOPUS", PINK, q="?")), DI("The octopus!", flags=["chime"], card=C("OCTOPUS", PINK), pause=0.8),
        ASK("Who carries a shell on its back?", card=C("TURTLE", GRN, q="?")), DI("The turtle!", flags=["chime"], card=C("TURTLE", GRN), pause=0.8),
        ASK("Who is the biggest animal in the ocean?", card=C("WHALE", (40, 80, 170), q="?")), DI("The whale!", flags=["chime"], card=C("WHALE", (40, 80, 170)), pause=0.8)]),
    dict(clip="c10", lines=[
        DO("What a wonderful underwater adventure!", flags=["chime"]),
        DI("Fish, turtle, dolphin, whale, octopus, crab and starfish! Dino-wow!")]),
]

PLAN = standard("Underwater Adventure", CLIPS, body, "Share this video with a friend who loves the ocean!")
