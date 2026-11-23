"""DOODLIGO EPISODE 01 — Learn Colors with Dodo and Dini | A Fun Rainbow Adventure"""

RED, BLUE, YEL, GRN, ORG, PUR = (225, 35, 45), (40, 110, 230), (235, 180, 0), (50, 160, 60), (245, 125, 10), (140, 60, 190)

def ask(text, pause=2.4, who="Dodo", extra=()):
    return dict(who=who, say=text, pause=pause, flags=["ask", *extra])

EPISODE = dict(
    title="Learn Colors with Dodo and Dini | A Fun Rainbow Adventure",
    objects=["apple", "balloon", "star", "leaf", "orange", "flower"],
    scenes=[
        dict(id="title", kind="title", text="Learn Colors with Dodo and Dini", lead=4.2, lines=[], tail=0.2),
        dict(id="intro", lines=[
            dict(who="Dodo", say="Hi, little explorers! I'm Dodo!", flags=["point"]),
            dict(who="Dini", say="And I'm Dini! Dino-hello!"),
            dict(who="Dodo", say="Welcome to the rainbow garden. But oh no! Everything is grey!"),
            dict(who="Dini", say="Where did all the colors go?", flags=["wrong"]),
            dict(who="Dodo", say="Let's find six colorful things and bring the colors back!", flags=["point"]),
        ]),
        dict(id="red", object="apple", label="RED", labelcol=RED, lines=[
            dict(who="Dini", say="Look! A blue apple!", flags=["wrong"]),
            dict(who="Dodo", say="Not quite, Dini. This apple is red!", flags=["reveal", "point"]),
            ask("Red! Can you say red?"),
            dict(who="Dini", say="Red! Red like a yummy apple!"),
            ask("Can you find something red near you?", pause=2.8),
        ]),
        dict(id="blue", object="balloon", label="BLUE", labelcol=BLUE, lines=[
            dict(who="Dodo", say="What is floating up there?", flags=["point"]),
            dict(who="Dini", say="A balloon! Is it yellow?", flags=["wrong"]),
            ask("No, silly! What color is the balloon?"),
            dict(who="Dodo", say="It's blue! Blue like the sky!", flags=["reveal"]),
            dict(who="Dini", say="Blue! Dino-wow!", flags=["cheer"]),
        ]),
        dict(id="yellow", object="star", label="YELLOW", labelcol=YEL, lines=[
            dict(who="Dini", say="Something is shining! Ooh, a green star!", flags=["wrong"]),
            dict(who="Dodo", say="Try again, Dini. The star is yellow!", flags=["reveal", "point"]),
            ask("Can you say yellow?"),
            dict(who="Dini", say="Yellow! Yellow like the sunshine!"),
        ]),
        dict(id="green", object="leaf", label="GREEN", labelcol=GRN, lines=[
            dict(who="Dodo", say="Look, a little leaf!", flags=["point"]),
            dict(who="Dini", say="Is it purple?", flags=["wrong"]),
            dict(who="Dodo", say="No, it's green! Just like you, Dini!", flags=["reveal"]),
            dict(who="Dini", say="Green like me! Hooray!", flags=["cheer"]),
            ask("Which thing is green? The leaf!", pause=1.6),
        ]),
        dict(id="orange", object="orange", label="ORANGE", labelcol=ORG, lines=[
            dict(who="Dini", say="Mmm, a round fruit! Is it red?", flags=["wrong"]),
            dict(who="Dodo", say="Close! This is an orange, and its color is orange too!", flags=["reveal", "point"]),
            ask("Say orange!"),
            dict(who="Dini", say="Orange! Like your sneakers, Dodo!"),
        ]),
        dict(id="purple", object="flower", label="PURPLE", labelcol=PUR, lines=[
            dict(who="Dodo", say="One more color to find!"),
            dict(who="Dini", say="A pretty flower! Is it blue?", flags=["wrong"]),
            dict(who="Dodo", say="Almost! This flower is purple!", flags=["reveal", "point"]),
            ask("Can you say purple?"),
            dict(who="Dini", say="Purple! I love purple!", flags=["cheer"]),
        ]),
        dict(id="finale", kind="finale", lines=[
            dict(who="Dodo", say="We found all six colors! Look at the garden!", flags=["chime"]),
            dict(who="Dini", say="The rainbow is back! Hooray!", flags=["cheer"]),
        ]),
        dict(id="game", kind="game", lines=[
            dict(who="Dodo", say="Let's play a color game! I show a thing, you shout the color!", flags=["point"]),
            *[x for obj, lab, col in [("balloon", "BLUE", BLUE), ("apple", "RED", RED), ("leaf", "GREEN", GRN),
                                      ("flower", "PURPLE", PUR), ("star", "YELLOW", YEL), ("orange", "ORANGE", ORG)]
              for x in (dict(who="Dodo", say="What color is this?", pause=2.2, flags=["ask"], item=dict(obj=obj, label=lab, col=col)),
                        dict(who="Dini", say=lab.capitalize() + "!", flags=["gamereveal", "chime"], pause=0.6))],
        ]),
        dict(id="recap", kind="recap", lines=[
            ask("Can you remember all six colors?", pause=2.6),
            dict(who="Dodo", say="Wow! We learned six beautiful colors today!", flags=["cheer"]),
            dict(who="Dini", say="Red, blue, yellow, green, orange and purple! Dino-wow!", flags=["cheer"]),
            dict(who="Dodo", say="Share this video with a friend who loves colors!"),
            dict(who="Both", say="See you next time, little explorers!", flags=["cheer"]),
        ]),
        dict(id="end", kind="end", text="See you next time!", lead=5.0, lines=[], tail=0.0),
    ],
)
