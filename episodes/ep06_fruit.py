import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from common import *

META = dict(code="dl006_fruit", title="Fruit Adventure with Dodo and Dini | Learn Fruit Names for Preschoolers",
            body="Explore colourful fruits with Dodo and Dini: banana, strawberry, grapes, watermelon, orange and pineapple! Then play a yummy fruit game.",
            tags=["Fruits", "LearnFruits", "FruitNames", "HealthyEating", "Preschool", "Doodligo"])

CLIPS = [
    "Dodo and Dini in a sunny fruit garden with a colourful fruit stand, waving hello to the camera.",
    "Dodo peels a long yellow banana and shares it with Dini under a banana tree.",
    "Dodo and Dini pick bright red strawberries in a strawberry patch.",
    "Dini holds up a bunch of purple grapes from a vine; Dodo smiles.",
    "Dodo and Dini share a big juicy slice of watermelon at a picnic, juice dripping, laughing.",
    "Dodo picks a round orange from an orange tree and gives it to Dini.",
    "Dini looks at a spiky pineapple with a puzzled face and touches it gently; Dodo giggles.",
    "Dodo and Dini sit on a picnic blanket with a basket full of colourful fruits, munching happily.",
    "Dodo and Dini look at the camera and point at the viewer with encouraging, curious faces, waiting for an answer.",
    "Dodo and Dini make a colourful fruit salad in a big bowl together.",
    "Dodo and Dini dance and celebrate in the fruit garden.",
    "Dodo and Dini wave goodbye to the camera warmly in the fruit garden.",
]

FRUITS = [("banana", "c02", YEL, "yellow", "Bananas are long and yellow!"), ("strawberry", "c03", RED, "red", "Strawberries are red and sweet!"),
          ("grapes", "c04", PUR, "purple", "Grapes are small, round and purple!"), ("watermelon", "c05", GRN, "green and red", "Watermelon is green outside and red inside!"),
          ("orange", "c06", ORG, "orange", "An orange is round and orange!"), ("pineapple", "c07", YEL, "yellow", "A pineapple is spiky outside, but sweet inside!")]

body = [dict(clip="c01", lines=intro("Today we are going on a fruit adventure!", "Yum! I'm so hungry! Let's go!"))]
for k, (f, clip, col, colour, fact) in enumerate(FRUITS):
    card = C(f, col, sub=colour)
    lines = [DO(f"What fruit is this?") if k % 2 == 0 else DI("Ooh, what fruit is this?"),
             (DO if k % 2 == 0 else DO)(f"It's {'a ' if f not in ('grapes',) else ''}{f}!".replace("a orange", "an orange"), flags=["reveal"], card=card),
             (DI if k % 2 == 0 else DO)(fact, card=card)]
    if f in ("banana", "grapes", "pineapple"):
        lines.append(ASK(f"Can you say {f}?", pause=2.0))
    if f == "pineapple":
        lines.insert(1, DI("Ouch! It's spiky! Is it a hedgehog?"))
    body.append(dict(clip=clip, label=f.upper(), labelcol=col, lines=lines))
body += [
    dict(clip="c09", kind="game", lines=[
        DO("Let's play a fruit game! Which fruit is it?"),
        ASK("Which fruit is long and yellow?", card=C("banana", YEL, q="?")), DI("Banana!", flags=["chime"], card=C("banana", YEL), pause=0.8),
        ASK("Which fruit is small and purple?", card=C("grapes", PUR, q="?")), DI("Grapes!", flags=["chime"], card=C("grapes", PUR), pause=0.8),
        ASK("Which fruit is red and sweet?", card=C("strawberry", RED, q="?")), DI("Strawberry!", flags=["chime"], card=C("strawberry", RED), pause=0.8)]),
    dict(clip="c10", lines=[
        DO("Let's make a yummy fruit salad!", flags=["chime"]),
        DI("Banana, strawberry, grapes, watermelon, orange and pineapple! Dino-yum!"),
        DO("Fruit helps us grow big and strong!")]),
]

PLAN = standard("Fruit Adventure", CLIPS, body, "Share this video with a friend who loves fruit!")
