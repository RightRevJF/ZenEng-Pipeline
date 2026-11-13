"""Song 48 (The Ratios Hold): the pick of record, the engine's pick on the default path (362, with 472: the refit judge's first among the
survivors with no soft break) of the main run, taken as drawn -- no hand edits. Both makings must agree (the same order, the same pick).
Evaluated again (every gate and the design gate) and written to melody_final.pkl."""
import sys, pickle, copy
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p58"]
import melody_v134_p58 as P
D = pickle.load(open("/home/claude/p58/run/melody_v134_p58_main.pkl", "rb")); Dr = pickle.load(open("/home/claude/p58/run/melody_v134_p58_main_r.pkl", "rb"))
assert D["order_fp"] == Dr["order_fp"] and D["pick"]["fp"] == Dr["pick"]["fp"], "the two makings differ"
c = copy.deepcopy(D["pick"])
for _p in ("V", "C"): P.KNOBS[_p].update(D["knobs"][_p])
P.LK.update(D["line_knobs"])
cert, meas = P.evaluate(c)
print("evaluate:", cert or "passes", "| design:", P.design_fails(c) or "pass", "| soft", c["info"]["soft"], "| lift", c["info"]["lift"])
assert cert is None and not P.design_fails(c)
c["judge"] = P.judge(c["notes"]); c["meas"] = meas; c["hand_edits"] = []
order = [x[0] for x in D["all_alive"]]; rank = order.index(c["fp"]) + 1
c["picked_from"] = dict(run="main", order=D["order_fp"], rank_by_composite=rank, rule="the default path: the engine's pick (362/472)", judge_first=D["judge_first"]["fp"])
pickle.dump(dict(pick=c, run=dict(order_fp=D["order_fp"], survivors=D["survivors"], made=D["made"], deaths=dict(D["deaths"]), rerun=D["rerun"], knobs=D["knobs"],
                                  line_knobs=D["line_knobs"], chords2=D["chords2"], bass8=D["bass8"])),
            open("/home/claude/p58/melody_final.pkl", "wb"))
print(c["fp"], "rank by composite", rank, "of", len(order), "judge", round(c["judge"]["combined"], 3), "composite", meas["composite"])
