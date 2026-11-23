import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from common import *

META = dict(code="dl004_farm", title="Farm Animals and Their Sounds with Dodo and Dini | Preschool Learning",
            body="Visit the farm with Dodo and Dini! Meet the cow, sheep, hen, pig, horse, duck and dog, and learn every animal sound.",
            tags=["FarmAnimals", "AnimalSounds", "OldMacdonald", "Preschool", "Doodligo"])

CLIPS = [
    "Dodo and Dini at a sunny farm gate with a red barn behind, waving hello to the camera.",
    "A friendly black-and-white cow munches grass in a meadow; Dodo and Dini gently pat her.",
    "Fluffy white sheep in a green field; Dini hugs a soft lamb and Dodo laughs.",
    "A mother hen with tiny yellow chicks pecks in the farmyard; Dodo and Dini crouch to watch.",
    "A happy pink pig rolls in mud; Dini giggles and Dodo covers his eyes, laughing.",
    "A brown horse trots in a paddock; Dodo and Dini watch in wonder by the fence.",
    "A white duck swims in a farm pond with ducklings; Dodo and Dini wave at them.",
    "A playful puppy runs to Dodo and Dini wagging its tail and licks Dodo's cheek.",
    "Dini tries to make an animal sound with a funny confused face; Dodo gently giggles.",
    "In front of the barn, Dodo and Dini look at the camera and point at the viewer with encouraging, curious faces, waiting for an answer.",
    "Dodo and Dini dance in the farmyard with the animals around them, celebrating.",
    "Sunset at the farm: Dodo and Dini wave goodbye to the camera warmly.",
]

ANIMALS = [("cow", "Moo", "c02", BRN), ("sheep", "Baa", "c03", BLUE), ("hen", "Cluck cluck", "c04", ORG), ("pig", "Oink oink", "c05", PINK),
           ("horse", "Neigh", "c06", BRN), ("duck", "Quack quack", "c07", YEL), ("dog", "Woof woof", "c08", GRN)]

body = [dict(clip="c01", lines=intro("Welcome to the farm! Let's meet the animals!", "And hear what they say! Let's go!"))]
for k, (a, snd, clip, col) in enumerate(ANIMALS):
    lines = [DO(f"Who is this? It's the {a}!", flags=["reveal"], card=C(a.upper(), col, sub=snd + "!")),
             ASK(f"What does the {a} say?", pause=2.0),
             DI(f"{snd}! {snd}!", card=C(a.upper(), col, sub=snd + "!"))]
    if a == "pig":
        lines.insert(1, DI("Look, he's playing in the mud!"))
    body.append(dict(clip=clip, label=a.upper(), labelcol=col, lines=lines))
    if a == "hen":
        body.append(dict(clip="c09", lines=[DI("Does the pig say... moo?"), DO("No, silly! The cow says moo! Let's find the pig!", flags=["chime"])]))
body += [
    dict(clip="c10", kind="game", lines=[
        DO("Let's play a sound game! Who says this?"),
        ASK("Who says moo?", card=C("COW", BRN, q="?", sub="Moo!")), DI("The cow!", flags=["chime"], card=C("COW", BRN, sub="Moo!"), pause=0.8),
        ASK("Who says quack quack?", card=C("DUCK", YEL, q="?", sub="Quack!")), DI("The duck!", flags=["chime"], card=C("DUCK", YEL, sub="Quack!"), pause=0.8),
        ASK("Who says oink oink?", card=C("PIG", PINK, q="?", sub="Oink!")), DI("The pig!", flags=["chime"], card=C("PIG", PINK, sub="Oink!"), pause=0.8),
        ASK("Who says woof woof?", card=C("DOG", GRN, q="?", sub="Woof!")), DI("The dog!", flags=["chime"], card=C("DOG", GRN, sub="Woof!"), pause=0.8)]),
    dict(clip="c11", lines=[
        DO("We met so many farm animals today!", flags=["chime"]),
        DI("Cow, sheep, hen, pig, horse, duck and dog! Dino-wow!")]),
]

PLAN = standard("Farm Animals and Their Sounds", CLIPS, body, "Share this video with a friend who loves animals!")
