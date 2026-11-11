"""Song 40 made for real: the pick from the design run, by ear (the writer's Q22 A), and the hand edits, logged; the edited melody
is evaluated again (every gate and the design gates) and written to melody_final_d.pkl.
The pick: 713d985f016b, fourth in the shortlist by the composite. Its hook climbs by step through 'used to taste like' (D4 E4 F#4 G4),
leaps a third to B4 on 'NOTH-ing', and settles on A4 for 'earth', a held bar; 'and the hands of someone gone' climbs the same way.
The three above it hover on B4-A4-B4 around 'else' (d39be09c80d5, 2ceb9fe3a0e4) or rock between two notes (03fb9d0eef6c), and
blur the peak."""
import sys, pickle, copy
sys.argv = ["x", "1", "design"]; sys.path.insert(0, "/home/claude/p40")
import melody_p40d as P
D = pickle.load(open("/home/claude/p40/melody_design.pkl", "rb"))
PICK = "713d985f016b"
c = copy.deepcopy(next(x for x in D["alive"] if x["fp"] == PICK))
B4, A4, G4, Fs4, E4, D4 = 71, 69, 67, 66, 64, 62
EDITS = [  # (lines, syllable, new pitch, why)
    ("chorus:1", 0, B4, "'HON-ey': the stressed syllable takes the B4, not 'ey'"), ("chorus:1", 1, A4, "'ey' steps down"),
    ("chorus:2", 3, D4, "'OV-en': no sixth leap onto the weak 'en'; D4, a chord tone"), ("chorus:2", 4, E4, "'en' a step up into 'no-'"),
    ("chorus:3", 4, B4, "'SOME-one': the stress takes the B4"), ("chorus:3", 5, G4, "'one' turns down, then 'gone' A4"),
    ("chorus:5", 1, B4, "'BIT-ter': the stress takes the B4"), ("chorus:5", 2, A4, "'ter' steps down"),
    ("chorus:6", 4, G4, "'hun-GRY': no drop of a fifth to C#4"), ("chorus:6", 7, G4, "'got' "), ("chorus:6", 8, A4, "'up' "),
    ("chorus:6", 9, B4, "'WHOLE' lands on B4 over G, held: 'she got up whole' is the last chorus's peak"),
    ("tag", 0, B4, "the tag: 'NOTH-ing' on B4, as in the hook"), ("tag", 1, A4, ""), ("tag", 2, Fs4, ""), ("tag", 3, E4, ""), ("tag", 4, D4, "'earth' home to D4"),
]
def targets(key):
    if key == "tag": return [("Last Chorus", 8)]
    i = int(key.split(":")[1]); out = [("Chorus 1", i), ("Chorus 2", i)]
    if i <= 6: out.append(("Last Chorus", i))
    return out
log = []
for key, syl, p, why in EDITS:
    for sec, i in targets(key):
        ns = [n for n in c["notes"] if n["line"] == f"{sec}:{i}" and n["syl"] == syl]
        assert ns, (sec, i, syl)
        n = ns[0]; log.append(dict(line=f"{sec}:{i}", syl=syl, on=n["on"], was=n["p"], now=p, why=why)); n["p"] = p
        for m in ns[1:]:                                                     # a melisma's tail follows by step
            if abs(m["p"] - p) > 2: log.append(dict(line=f"{sec}:{i}", syl=syl, on=m["on"], was=m["p"], now=p, why="melisma tail held")); m["p"] = p
cert, meas = P.evaluate(c)
fails = P.design_fails(c)
print("evaluate:", cert or "passes", "| design gates:", fails or "pass", "| soft", c["info"]["soft"], "hard", c["info"]["hard"], "| lift", c["info"]["lift"])
c["judge"] = P.judge(c["notes"]); print("judge", round(c["judge"]["combined"], 3), "composite", meas and meas["composite"])
assert cert is None and not fails
c["meas"] = meas; c["hand_edits"] = log; c["picked_from"] = dict(run="design", order=D["order_fp"], rank_in_shortlist=[x["fp"] for x in D["alive"] if x["fp"] in set(D["short"])].index(PICK) + 1)
pickle.dump(dict(pick=c, run=dict(order_fp=D["order_fp"], survivors=D["survivors"], made=D["made"], deaths=dict(D["deaths"]), rerun=D["rerun"], knobs=D["knobs"])),
            open("/home/claude/p40/melody_final_d.pkl", "wb"))
print(len(log), "notes edited")
