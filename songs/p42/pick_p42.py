"""Song 42: the pick of record (255: the composite's first inside the judge's top half of the main run), inspected line by line and taken
as drawn (the default path): no hand edits. Evaluated again (every gate and the design gate) and written to melody_final.pkl."""
import sys, pickle, copy
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p42", "/home/claude/p40"]
import melody_p42 as P
D = pickle.load(open("/home/claude/p42/melody_p42_main.pkl", "rb")); Dr = pickle.load(open("/home/claude/p42/melody_p42_main_r.pkl", "rb"))
assert D["order_fp"] == Dr["order_fp"] and D["pick"]["fp"] == Dr["pick"]["fp"]
c = copy.deepcopy(D["pick"])
for _p in ("V", "C"): P.KNOBS[_p].update(D["knobs"][_p])
P.LK.update(D["line_knobs"])
cert, meas = P.evaluate(c)
print("evaluate:", cert or "passes", "| design:", P.design_fails(c) or "pass", "| soft", c["info"]["soft"], "| lift", c["info"]["lift"])
assert cert is None and not P.design_fails(c)
c["judge"] = P.judge(c["notes"]); c["meas"] = meas; c["hand_edits"] = []
rank = [x["fp"] for x in D["alive"]].index(c["fp"]) + 1
c["picked_from"] = dict(run="main", order=D["order_fp"], rank_by_composite=rank, rule="255: composite first inside the judge's top half")
pickle.dump(dict(pick=c, run=dict(order_fp=D["order_fp"], survivors=D["survivors"], made=D["made"], deaths=dict(D["deaths"]), rerun=D["rerun"], knobs=D["knobs"], line_knobs=D["line_knobs"])),
            open("/home/claude/p42/melody_final.pkl", "wb"))
print(c["fp"], "rank by composite", rank, "judge", round(c["judge"]["combined"], 3), "composite", meas["composite"])
