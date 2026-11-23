import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from common import *

META = dict(code="dl002_counting", title="Let's Count from 1 to 20 with Dodo and Dini | Counting for Preschoolers",
            body="Count toys, apples, balloons and ducklings with Dodo and Dini, all the way from 1 to 20! Then play a fun how-many game.",
            tags=["Counting", "Numbers1To20", "CountingForKids", "Preschool", "Doodligo"])

CLIPS = [
    "Dodo and Dini in a bright cosy playroom, facing the camera and waving hello warmly.",
    "Dodo stacks five colourful toy blocks one by one on the playroom floor while Dini watches, excited.",
    "A wooden kitchen table with a bowl of shiny red apples; Dini points at the apples one by one, Dodo smiles.",
    "In a sunny garden many colourful balloons float up into the blue sky; Dodo and Dini jump and reach for them.",
    "A line of fluffy yellow ducklings waddles past Dodo and Dini beside a little pond; Dini waddles along too.",
    "Dini counts on his tiny claws with a puzzled, silly face; Dodo gently giggles and helps him count.",
    "Dodo and Dini sit on a rug building a very tall tower of blocks; it wobbles and they laugh.",
    "Night garden: Dodo and Dini lie on soft grass looking up at twinkling stars, pointing and counting.",
    "In the playroom, Dodo and Dini look at the camera and point at the viewer with encouraging, curious faces, waiting for an answer.",
    "Butterflies flutter around flowers; Dodo and Dini gently reach out and count them.",
    "Dodo and Dini dance and celebrate happily with confetti and balloons in the playroom.",
    "Sunset garden: Dodo and Dini wave goodbye to the camera warmly.",
]

def nums(a, b):
    return ", ".join(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
                      "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"][a - 1:b])

def cap(s):
    return s[0].upper() + s[1:]

body = [
    dict(clip="c01", lines=intro("Today we are going to count from one to twenty!", "Twenty? That's so many! Let's go!")),
    dict(clip="c02", label="1 – 5", labelcol=BLUE, lines=[
        DO("Let's count the blocks!"),
        DO(cap(nums(1, 5)) + "!", flags=["reveal"], card=C("5", BLUE, dots=5)),
        DI("Five blocks! I counted with you!"),
        ASK("Can you show me five fingers?")]),
    dict(clip="c03", label="6 – 10", labelcol=RED, lines=[
        DO("Now let's count yummy apples!"),
        DO(cap(nums(6, 10)) + "!", flags=["reveal"], card=C("10", RED, dots=10)),
        DI("Ten apples! Crunch, crunch!"),
        ASK("Can you count to ten with me? One, two, three, four, five, six, seven, eight, nine, ten!", pause=1.2)]),
    dict(clip="c04", label="11 – 15", labelcol=PUR, lines=[
        DO("Look at all the balloons!"),
        DO(cap(nums(11, 15)) + "!", flags=["reveal"], card=C("15", PUR, dots=15)),
        DI("Fifteen balloons! Pop, pop, pop!"),
        DO("Oh no, Dini! Let's not pop them!")]),
    dict(clip="c05", label="16 – 20", labelcol=ORG, lines=[
        DO("Here come the little ducklings!"),
        DO(cap(nums(16, 19)) + "...", card=C("19", ORG, dots=19))]),
    dict(clip="c06", lines=[
        DI("Um, Dodo, what comes after nineteen? Is it eleventy?"),
        DO("Ha ha! After nineteen comes twenty!", flags=["reveal"], card=C("20", ORG, dots=20)),
        DI("Twenty ducklings! Quack, quack!")]),
    dict(clip="c07", lines=[
        DO("We counted all the way to twenty!", flags=["chime"]),
        DI("Hooray! Dino-wow!")]),
    dict(clip="c09", kind="game", lines=[
        DO("Let's play a counting game! How many dots do you see?"),
        ASK("How many dots?", pause=2.4, card=C("3", GRN, dots=3)), DI("Three!", flags=["chime"], card=C("3", GRN, dots=3), pause=0.8),
        ASK("How many dots?", pause=2.4, card=C("5", BLUE, dots=5)), DI("Five!", flags=["chime"], card=C("5", BLUE, dots=5), pause=0.8),
        ASK("How many dots?", pause=2.4, card=C("8", PINK, dots=8)), DI("Eight!", flags=["chime"], card=C("8", PINK, dots=8), pause=0.8),
        ASK("How many dots?", pause=2.4, card=C("10", RED, dots=10)), DI("Ten!", flags=["chime"], card=C("10", RED, dots=10), pause=0.8)]),
    dict(clip="c08", lines=[
        ASK("Now let's count to twenty together!", pause=0.6),
        DO(cap(nums(1, 10)) + "!", card=C("1 – 10", BLUE)),
        DI(cap(nums(11, 20)) + "!", card=C("11 – 20", ORG))]),
    dict(clip="c11", lines=[DO("Great counting, little explorers!"), DI("You are super counters!")]),
]

PLAN = standard("Let's Count from 1 to 20!", CLIPS, body, "Share this video with a friend who loves counting!")
