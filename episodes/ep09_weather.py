import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from common import *

META = dict(code="dl009_weather", title="Weather Adventure with Dodo and Dini | Sunny, Rainy, Windy and Snowy",
            body="Discover the weather with Dodo and Dini: sunny, cloudy, rainy, windy and snowy days, and a rainbow too! Then play a weather game.",
            tags=["Weather", "WeatherForKids", "Seasons", "Preschool", "Doodligo"])

CLIPS = [
    "Dodo and Dini look out of a big window at the sky in a cosy house, then wave hello to the camera.",
    "A bright sunny day: Dodo and Dini in sunhats play in a sunny garden, the sun shining warmly.",
    "Fluffy white and grey clouds drift across the sky; Dodo and Dini lie on the grass pointing at cloud shapes.",
    "A rainy day: Dodo and Dini in yellow raincoats and boots splash happily in puddles.",
    "A windy day: Dodo and Dini fly a kite while leaves swirl around them; Dodo's hair blows.",
    "A snowy day: Dodo and Dini in warm scarves build a snowman as snowflakes fall.",
    "Dini wears sunglasses and a swimsuit in the falling snow with a silly confused face, shivering; Dodo gently giggles and gives him a scarf.",
    "After the rain, a big rainbow appears over the garden; Dodo and Dini gasp and smile.",
    "Dodo and Dini look at the camera and point at the viewer with encouraging, curious faces, waiting for an answer.",
    "Dodo and Dini catch snowflakes on their tongues, laughing.",
    "Dodo and Dini dance and celebrate under the rainbow.",
    "Dodo and Dini wave goodbye to the camera warmly from the window.",
]

WX = [("sunny", "c02", YEL, "The sun is shining! It's warm and bright!", "Can you make a big sun with your arms?"),
      ("cloudy", "c03", (110, 120, 140), "Look at the fluffy clouds! That one looks like a bunny!", None),
      ("rainy", "c04", BLUE, "Pitter patter! We wear raincoats and splash in puddles!", "Can you make the rain with your fingers? Pitter patter!"),
      ("windy", "c05", GRN, "Whoosh! The wind blows the leaves and flies our kite!", "Can you blow like the wind? Whoosh!"),
      ("snowy", "c06", (90, 160, 220), "Brrr! Snowflakes are falling! Let's build a snowman!", None)]

body = [dict(clip="c01", lines=intro("Today let's learn about the weather!", "What is the weather like today? Let's look!"))]
for k, (w, clip, col, fact, ask) in enumerate(WX):
    card = C(w, col)
    lines = [DO("What's the weather like?") if k % 2 == 0 else DI("What's the weather now?"),
             DO(f"It's {w}!", flags=["reveal"], card=card), (DI if k % 2 == 0 else DO)(fact, card=card)]
    if ask:
        lines.append(ASK(ask, pause=2.6))
    body.append(dict(clip=clip, label=w.upper(), labelcol=col, lines=lines))
    if w == "snowy":
        body.append(dict(clip="c07", lines=[DI("I'm ready for the beach! Brrr, it's so cold!"), DO("Silly Dini! On a snowy day we wear a warm scarf and hat!", flags=["chime"])]))
        body.append(dict(clip="c10", lines=[DI("Snowflakes taste so cold! Yum!")]))
body += [
    dict(clip="c08", label="RAINBOW", labelcol=PUR, lines=[
        DO("Look! After the rain and sun comes a rainbow!", flags=["reveal", "chime"], card=C("rainbow", PUR)),
        DI("So many colors! Dino-wow!")]),
    dict(clip="c09", kind="game", lines=[
        DO("Let's play a weather game! What do we wear?"),
        ASK("It's rainy! What do we wear?", card=C("raincoat", BLUE, q="?")), DI("A raincoat and boots!", flags=["chime"], card=C("raincoat", BLUE), pause=0.8),
        ASK("It's sunny! What do we wear?", card=C("sun hat", YEL, q="?")), DI("A sun hat!", flags=["chime"], card=C("sun hat", YEL), pause=0.8),
        ASK("It's snowy! What do we wear?", card=C("scarf", RED, q="?")), DI("A warm scarf and hat!", flags=["chime"], card=C("scarf", RED), pause=0.8)]),
    dict(clip="c11", lines=[
        DO("Sunny, cloudy, rainy, windy and snowy!", flags=["chime"]),
        DI("I love every kind of weather!")]),
]

PLAN = standard("Weather Adventure", CLIPS, body, "Share this video with a friend and tell them today's weather!")
