import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from common import *

META = dict(code="dl008_teeth", title="Brush Your Teeth with Dodo and Dini | Healthy Habits for Preschoolers",
            body="Brush, brush, brush! Learn a healthy daily routine with Dodo and Dini: a pea-size dot of toothpaste, up and down, round and round, spit and smile.",
            tags=["BrushYourTeeth", "HealthyHabits", "DailyRoutine", "Preschool", "Doodligo"])

CLIPS = [
    "Morning: Dodo and Dini wake up in a cosy bedroom with sunshine through the window, stretch and wave hello to the camera.",
    "Dodo and Dini walk into a bright, clean bathroom and pick up their colourful toothbrushes.",
    "Close-up: Dodo squeezes a tiny pea-sized dot of toothpaste onto his toothbrush; Dini watches carefully.",
    "Dodo and Dini brush their teeth up and down in front of the mirror, smiling with foamy mouths.",
    "Dodo and Dini brush their teeth in little circles, round and round, giggling.",
    "Dini squeezes way too much toothpaste and makes a big foamy mess with a silly confused face; Dodo gently giggles.",
    "Dodo and Dini spit into the sink and rinse with a cup of water.",
    "Dodo and Dini smile big at the mirror showing sparkly clean teeth; a little sparkle twinkles.",
    "Dodo and Dini look at the camera and point at the viewer with encouraging, curious faces, waiting for an answer.",
    "Night: Dodo and Dini in pyjamas brush their teeth before bed, then yawn sleepily.",
    "Dodo and Dini dance happily with their toothbrushes in the bathroom.",
    "Night: Dodo and Dini tucked in bed wave goodbye to the camera with sleepy smiles.",
]

body = [
    dict(clip="c01", lines=intro("Good morning! It's time to brush our teeth!", "Brush, brush, brush! Let's go!")),
    dict(clip="c02", label="STEP 1", labelcol=BLUE, lines=[
        DO("First, we take our toothbrush.", flags=["reveal"], card=C("1", BLUE, sub="toothbrush")),
        DI("Mine is orange, just like my spikes!")]),
    dict(clip="c03", label="STEP 2", labelcol=GRN, lines=[
        DO("Next, a tiny dot of toothpaste. Just the size of a little pea!", flags=["reveal"], card=C("2", GRN, sub="tiny dot")),
        ASK("Can you show me a tiny dot with your fingers?")]),
    dict(clip="c06", lines=[
        DI("Oops! I put too much! Look at all the bubbles!"),
        DO("Silly Dini! Just a tiny dot is all we need!", flags=["chime"])]),
    dict(clip="c04", label="STEP 3", labelcol=ORG, lines=[
        DO("Now we brush up and down, up and down!", flags=["reveal"], card=C("3", ORG, sub="up & down")),
        ASK("Can you brush up and down with me?", pause=2.8),
        DI("Up and down! Up and down!")]),
    dict(clip="c05", label="STEP 4", labelcol=PUR, lines=[
        DO("Then little circles, round and round!", flags=["reveal"], card=C("4", PUR, sub="round & round")),
        DI("Round and round! It tickles!"),
        DO("Don't forget the back teeth, and your tongue too!")]),
    dict(clip="c07", label="STEP 5", labelcol=RED, lines=[
        DO("Now we spit, and rinse!", flags=["reveal"], card=C("5", RED, sub="spit & rinse")),
        DI("Spit, spit! All clean!")]),
    dict(clip="c08", lines=[
        DO("Look at our sparkly teeth! Big smile!", flags=["chime"]),
        ASK("Can you show me your big smile?", pause=2.4)]),
    dict(clip="c09", kind="game", lines=[
        DO("Let's play a tooth game! What comes next?"),
        ASK("How much toothpaste do we use?", card=C("tiny dot", GRN, q="?")), DI("A tiny dot!", flags=["chime"], card=C("tiny dot", GRN), pause=0.8),
        ASK("How do we brush?", card=C("up & down", ORG, q="?")), DI("Up and down, and round and round!", flags=["chime"], card=C("up & down", ORG), pause=0.8),
        ASK("When do we brush our teeth?", card=C("morning & night", BLUE, q="?")), DI("In the morning and at night!", flags=["chime"], card=C("morning & night", BLUE), pause=0.8)]),
    dict(clip="c10", lines=[
        DO("We brush in the morning, and again before bed.", flags=["chime"]),
        DI("Brush, brush, brush! Healthy teeth! Dino-wow!")]),
]

PLAN = standard("Brush Your Teeth!", CLIPS, body, "Share this video with a friend to help them brush too!")
