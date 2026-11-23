import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from common import *

META = dict(code="dl007_wild", title="Wild Animals Adventure with Dodo and Dini | Lion, Elephant, Giraffe and Monkey",
            body="Go on a safari with Dodo and Dini! Meet the lion, elephant, giraffe, monkey, zebra and hippo, with easy animal facts for little ones.",
            tags=["WildAnimals", "SafariAnimals", "AnimalsForKids", "Preschool", "Doodligo"])

CLIPS = [
    "Dodo and Dini in a little safari jeep on the sunny savanna, wearing explorer hats, waving hello to the camera.",
    "A friendly lion with a big fluffy mane yawns under a tree; Dodo and Dini watch from the jeep, amazed.",
    "A gentle baby elephant sprays water from its trunk; Dodo and Dini giggle as they get splashed.",
    "A tall giraffe eats leaves from a tall tree; Dodo and Dini look way up.",
    "A playful monkey swings from vine to vine in the jungle; Dini tries to copy it.",
    "A zebra with black and white stripes gallops by; Dodo and Dini wave.",
    "A big friendly hippo yawns in a river; Dini covers his mouth, surprised and laughing.",
    "Dini puts on a lion mane costume and tries to roar but makes a tiny squeak; Dodo gently giggles.",
    "Dodo and Dini look at the camera and point at the viewer with encouraging, curious faces, waiting for an answer.",
    "Sunset on the savanna: animals walk past as Dodo and Dini watch from a hill.",
    "Dodo and Dini dance and celebrate on the savanna with happy animals around.",
    "Dodo and Dini wave goodbye to the camera warmly from the safari jeep.",
]

ANIMALS = [("lion", "c02", ORG, "The lion is the king of the jungle! He says roar!"), ("elephant", "c03", BLUE, "The elephant has a long trunk and big ears!"),
           ("giraffe", "c04", YEL, "The giraffe has a very long neck! So tall!"), ("monkey", "c05", BRN, "The monkey swings in the trees! Ooh ooh, ah ah!"),
           ("zebra", "c06", (60, 60, 60), "The zebra has black and white stripes!"), ("hippo", "c07", PUR, "The hippo loves to splash in the river!")]

body = [dict(clip="c01", lines=intro("Today we are going on a safari adventure!", "Wild animals! Let's go explore!"))]
for k, (a, clip, col, fact) in enumerate(ANIMALS):
    card = C(a.upper(), col)
    lines = [DI("Look! Who is that?") if k % 2 == 0 else DO("Who is that?"),
             DO(f"It's {'an' if a[0] in 'aeiou' else 'a'} {a}!", flags=["reveal"], card=card),
             (DO if k % 2 == 0 else DI)(fact, card=card)]
    if a in ("lion", "monkey", "elephant"):
        lines.append(ASK({"lion": "Can you roar like a lion?", "monkey": "Can you jump like a monkey?", "elephant": "Can you swing your arm like a trunk?"}[a], pause=2.6))
    body.append(dict(clip=clip, label=a.upper(), labelcol=col, lines=lines))
    if a == "lion":
        body.append(dict(clip="c08", lines=[DI("I'm a lion too! Roar!"), DO("Ha ha! That's a tiny roar, Dini! But a very cute one!", flags=["chime"])]))
body += [
    dict(clip="c09", kind="game", lines=[
        DO("Let's play an animal game! Who is it?"),
        ASK("Who has a very long neck?", card=C("GIRAFFE", YEL, q="?")), DI("The giraffe!", flags=["chime"], card=C("GIRAFFE", YEL), pause=0.8),
        ASK("Who has black and white stripes?", card=C("ZEBRA", (60, 60, 60), q="?")), DI("The zebra!", flags=["chime"], card=C("ZEBRA", (60, 60, 60)), pause=0.8),
        ASK("Who has a long trunk?", card=C("ELEPHANT", BLUE, q="?")), DI("The elephant!", flags=["chime"], card=C("ELEPHANT", BLUE), pause=0.8)]),
    dict(clip="c10", lines=[
        DO("What a wonderful safari!", flags=["chime"]),
        DI("Lion, elephant, giraffe, monkey, zebra and hippo! Dino-wow!")]),
]

PLAN = standard("Wild Animals Adventure", CLIPS, body, "Share this video with a friend who loves wild animals!")
