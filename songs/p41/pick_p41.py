"""Song 41: the pick of record (255: the composite's first inside the judge's top half of the main run), inspected by hand line by line
(show_pick.py) and taken as drawn: no hand edits (the default path). Evaluated again and written to melody_final.pkl."""
import sys, pickle, copy
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p41"]
import melody_p41 as P
D = pickle.load(open("/home/claude/p41/melody_p41_main.pkl", "rb"))
R = pickle.load(open("/home/claude/p41/melody_p41_main_r.pkl", "rb"))
assert D["order_fp"] == R["order_fp"] and D["pick"]["fp"] == R["pick"]["fp"]
c = copy.deepcopy(D["pick"])
for _p in ("V", "C"): P.KNOBS[_p].update(D["knobs"][_p])
cert, meas = P.evaluate(c)
print("evaluate:", cert or "passes", "| soft", c["info"]["soft"], "hard", c["info"]["hard"], "| lift", c["info"]["lift"])
assert cert is None
c["judge"] = P.judge(c["notes"]); c["meas"] = meas; c["hand_edits"] = []
rank = [x["fp"] for x in D["alive"]].index(c["fp"]) + 1
c["picked_from"] = dict(run="main", order=D["order_fp"], rank_by_composite=rank, rule="255: composite first inside the judge's top half")
pickle.dump(dict(pick=c, run=dict(order_fp=D["order_fp"], survivors=D["survivors"], made=D["made"], deaths=dict(D["deaths"]), rerun=D["rerun"], knobs=D["knobs"])),
            open("/home/claude/p41/melody_final.pkl", "wb"))
print(c["fp"], "rank by composite", rank, "judge", round(c["judge"]["combined"], 3), "composite", meas["composite"])
