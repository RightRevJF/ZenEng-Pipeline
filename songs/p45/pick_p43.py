"""Song 43: the pick of record (Q18 A, the writer's choice under 255's open question): the judge's first build of the main run,
dc24946f27cb, taken as drawn -- no hand edits. 255's own pick (the composite's first inside the judge's top half) is recorded beside it.
Evaluated again (every gate and the design gate) and written to melody_final.pkl."""
import sys, pickle, copy
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p45", "/home/claude/p40"]
import melody_p43 as P
D = pickle.load(open("/home/claude/p45/melody_p43_main.pkl", "rb")); Dr = pickle.load(open("/home/claude/p45/melody_p43_main_r.pkl", "rb"))
assert D["order_fp"] == Dr["order_fp"] and D["judge_first"]["fp"] == Dr["judge_first"]["fp"] == "dc24946f27cb"
c = copy.deepcopy(D["judge_first"])
for _p in ("V", "C"): P.KNOBS[_p].update(D["knobs"][_p])
P.LK.update(D["line_knobs"])
cert, meas = P.evaluate(c)
print("evaluate:", cert or "passes", "| design:", P.design_fails(c) or "pass", "| soft", c["info"]["soft"], "| lift", c["info"]["lift"])
assert cert is None and not P.design_fails(c)
c["judge"] = P.judge(c["notes"]); c["meas"] = meas; c["hand_edits"] = []
order = [x[0] for x in D["all_alive"]]; rank = order.index(c["fp"]) + 1
c["picked_from"] = dict(run="main", order=D["order_fp"], rank_by_composite=rank, rule="Q18 A: the judge's first (255's open question); 255's pick 840d7b4af214 recorded",
                        rule_255_pick=D["pick"]["fp"])
pickle.dump(dict(pick=c, run=dict(order_fp=D["order_fp"], survivors=D["survivors"], made=D["made"], deaths=dict(D["deaths"]), rerun=D["rerun"], knobs=D["knobs"], line_knobs=D["line_knobs"])),
            open("/home/claude/p45/melody_final.pkl", "wb"))
print(c["fp"], "rank by composite", rank, "of", len(order), "judge", round(c["judge"]["combined"], 3), "composite", meas["composite"])
