"""Song 53 (Sung to Sleep, 3/4, Common Meter with a refrain) as a hymn-mode spec for lib/luthier/metre_engine.py (Luthier v12, fix 791).
    python3 songs/p63/mkspec53.py   ->  songs/p63/spec53.json"""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
IAMB8, IAMB6 = [0, 1] * 4, [0, 1] * 3; HUSH8, HUSH6 = [1, 0, 0, 1, 0, 1, 0, 1], [1, 0, 0, 1, 0, 1]
verse = dict(name="verse", start=66, chords=["D", "G", "D", "A", "Bm", "G", "Em", "A", "D", "Bm", "G", "Em", "G", "A", "D", "D"],
             lines=[dict(stress=IAMB8, rule=dict(lo=61, hi=71)), dict(stress=IAMB6, rule=dict(lo=61, hi=71, end=[9, 1, 4])), dict(stress=IAMB8, rule=dict(lo=61, hi=71)), dict(stress=IAMB6, rule=dict(lo=61, hi=71, end=[2]))])
refrain = dict(name="refrain", start=62, chords=["D", "D", "G", "D", "Bm", "G", "A", "A", "G", "D", "Bm", "Em7", "G", "A7", "D", "D"],
               lines=[dict(stress=HUSH8, rule=dict(lo=62, hi=66)), dict(stress=HUSH6, rule=dict(lo=62, hi=69, end=[9, 1, 4])),
                      dict(stress=IAMB8, plain=[5], rule=dict(lo=64, hi=74, rise=True, pin={"5": 74}, count={"74": 1})),                    # climbs to D5 on 'world', the tune's only D5, held
                      dict(stress=IAMB6, rule=dict(lo=62, hi=71, end=[2], pairs=[dict(a=1, b=3, min=1, max=2)], end_leap_max=5))])              # the second 'sleeping' a step above the first; 'here' home
spec = dict(title="Sung to Sleep (song 53)", mode="hymn", metre="3/4", seed=20261115 + 4532, scale=[2, 4, 6, 7, 9, 11, 1], compass=[61, 73], leap_max=7, slur_share=0.4,
            chords={"D": [2, 6, 9], "G": [7, 11, 2], "A": [9, 1, 4], "A7": [9, 1, 4, 7], "Bm": [11, 2, 6], "Em": [4, 7, 11], "Em7": [4, 7, 11, 2], "F#m": [6, 9, 1]},
            only_over={"1": ["A", "A7"]}, tune=[verse, refrain])
json.dump(spec, open(f"{H}/spec53.json", "w"), indent=1); print("wrote spec53.json")
