"""Song 44: the pick of record under 362: the judge's first among the main run's survivors with no soft break, e8dc84c25324, taken as drawn --
no hand edits. The judge's own first (with a soft break) and 255's pick are recorded beside it. Evaluated again (every gate and the design gate)
and written to melody_final.pkl."""
import sys, pickle, copy
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p48", "/home/claude/p40"]
import melody_p44 as P
D = pickle.load(open("/home/claude/p48/melody_p44_main.pkl", "rb")); Dr = pickle.load(open("/home/claude/p48/melody_p44_main_r.pkl", "rb"))
assert D["order_fp"] == Dr["order_fp"] and D["pick"]["fp"] == Dr["pick"]["fp"] == "e8dc84c25324"
c = copy.deepcopy(D["pick"])
for _p in ("V", "C"): P.KNOBS[_p].update(D["knobs"][_p])
P.LK.update(D["line_knobs"])
cert, meas = P.evaluate(c)
print("evaluate:", cert or "passes", "| design:", P.design_fails(c) or "pass", "| soft", c["info"]["soft"], "| lift", c["info"]["lift"])
assert cert is None and not P.design_fails(c) and not c["info"]["soft"]
c["judge"] = P.judge(c["notes"]); c["meas"] = meas; c["hand_edits"] = []
order = [x[0] for x in D["all_alive"]]; rank = order.index(c["fp"]) + 1
ojudge = [x[0] for x in sorted(D["all_alive"], key=lambda x: (-x[1], x[0]))]
c["picked_from"] = dict(run="main", order=D["order_fp"], rank_by_composite=rank, rank_by_judge=ojudge.index(c["fp"]) + 1, qualified=D["clean"],
                        rule="362: the judge's first among survivors with no soft break", judges_first=D["pick_352"]["fp"], rule_255_pick=D["pick_255"]["fp"])
pickle.dump(dict(pick=c, run=dict(order_fp=D["order_fp"], survivors=D["survivors"], made=D["made"], deaths=dict(D["deaths"]), rerun=D["rerun"], knobs=D["knobs"], line_knobs=D["line_knobs"])),
            open("/home/claude/p48/melody_final.pkl", "wb"))
print(c["fp"], "rank by composite", rank, "of", len(order), "by judge", c["picked_from"]["rank_by_judge"], "judge", round(c["judge"]["combined"], 3), "composite", meas["composite"])
