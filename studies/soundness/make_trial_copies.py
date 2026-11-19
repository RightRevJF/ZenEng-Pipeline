"""The trial copies of song_from_lyric.py behind margin_turns_of_four.json and neighbour_turns_of_four*.json (749.95, 749.97). Writes them outside the repo:
    python3 studies/soundness/make_trial_copies.py /tmp/sfl4 /tmp/sfl4b
then MARGIN_TURNS_OF_FOUR=/tmp/sfl4 python3 studies/soundness/margin.py ...   (every turn four bars)
     MARGIN_TURNS_OF_FOUR=/tmp/sfl4b TRIAL_NAME=turns_of_four_borrow_rhythm_0.2 python3 studies/soundness/neighbour.py ...   (and 818's rhythm borrow at 0.2)"""
import os, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); src = open(os.path.join(ROOT, "lib", "luthier", "song_from_lyric.py")).read()
def sub(s, a, b): assert s.count(a) == 1, a; return s.replace(a, b)
four = sub(sub(src, 'tb = rs_.choices([2, 4], [0.62, 0.38])[0]', 'tb = 4'), 'tb = 2; flags.append("916: the song runs long: its turns are two bars")', 'tb = 4')
four = sub(four, 'HERE = os.path.dirname(os.path.abspath(__file__))', f'HERE = "{os.path.join(ROOT, "lib", "luthier")}"')
for d, s in ((sys.argv[1], four), (sys.argv[2], sub(four, 'borrow=dict(rhythm=0.0, figure=0.6)', 'borrow=dict(rhythm=0.2, figure=0.6)'))):
    os.makedirs(d, exist_ok=True); open(os.path.join(d, "song_from_lyric.py"), "w").write(s); print("written", d)
