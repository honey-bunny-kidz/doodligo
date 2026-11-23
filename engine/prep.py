"""Print Muse prompts for an episode: python3 prep.py ../episodes/epXX.py [clips1|clips2|voices]"""
import sys, importlib.util, json
import compose
spec = importlib.util.spec_from_file_location("p", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
P, M = m.PLAN, m.META
from common import STYLE
which = sys.argv[2]
if which == "count":
    ll = compose.number_lines(P); print(M["code"], len(ll), "lines")
elif which in ("clips1", "clips2"):
    rng = range(0, 6) if which == "clips1" else range(6, 12)
    hdr = (f"New episode: \"{M['title'].split(' | ')[0]}\". Please make 6 clips ({STYLE}). Use the same Dodo and Dini references as before. "
           f"Name the files with the clip number and episode code {M['code']} (e.g. {M['code']}-clip{rng[0]+1:02d}).\n")
    print(hdr + "\n".join(f"{i+1}. {P['clips'][i]}" for i in rng))
elif which == "voices":
    print(f"Now the voices for {M['code']}: MP3, one file per numbered line, named NN-dodo.mp3 / NN-dini.mp3, in one zip named {M['code']}-voices. "
          "Use exactly the same v2 voices as Episode 01 (soft, child-like Dodo; tiny, soft, cute Dini), slow and clear.\n\n" + compose.line_list(P))
