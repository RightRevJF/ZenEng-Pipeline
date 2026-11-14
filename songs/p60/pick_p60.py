"""Song 50 (The Small Things): the pick of record, luthier_judge5's (730) over the clean survivors of the main run of Luthier v7, taken as drawn --
no hand edits. Evaluated again (every gate and the design gates) and written to melody_final.pkl."""
import sys, pickle, copy, io, contextlib
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p60"]
with contextlib.redirect_stdout(io.StringIO()): import melody_l7_p60 as P
D = pickle.load(open("/home/claude/p60/runl7/melody_l7_p60_main.pkl", "rb"))
FP = sys.argv[1] if len(sys.argv) > 1 and len(sys.argv[1]) == 12 else D["pick"]["fp"]
def rebuild(b):
    ns = []; last = {}
    for o, d, p, s, l, st, sy in b["notes"]:
        sl = last.get(l) == sy and sy is not None; last[l] = sy
        ns.append(dict(on=o, p=p, syl=sy, slur=sl, stress=st, dur=d, sec=s, line=l))
    return dict(notes=ns, meta=b["meta"], judge=b["judge"], info=b["info"], read=b["read"], lines=b["lines"], fp=b["fp"])
c = copy.deepcopy(D["pick"]) if FP == D["pick"]["fp"] else copy.deepcopy(rebuild(next(b for b in D["all"] if b["fp"] == FP)))
for _p in ("V", "C"): P.KNOBS[_p].update(D["knobs"][_p])
P.LK.update(D["line_knobs"])
cert, meas = P.evaluate(c)
print("evaluate:", cert or "passes", "| design:", P.design_fails(c) or "pass", "| soft", c["info"]["soft"], "| lift", c["info"]["lift"])
assert cert is None and not P.design_fails(c)
c["judge"] = P.judge(c["notes"]); c["meas"] = meas; c["hand_edits"] = []
order = [x[0] for x in D["all_alive"]]; rank = order.index(c["fp"]) + 1
c["picked_from"] = dict(run="main", order=D["order_fp"], rank_by_composite=rank, rule="730: luthier_judge5.pick over the clean survivors", judge5_pick=D["pick"]["fp"])
pickle.dump(dict(pick=c, run=dict(order_fp=D["order_fp"], survivors=D["survivors"], made=D["made"], deaths=dict(D["deaths"]), rerun=D["rerun"], knobs=D["knobs"],
                                  line_knobs=D["line_knobs"], chords2=D["chords2"], bass8=D["bass8"])), open("/home/claude/p60/melody_final.pkl", "wb"))
print(c["fp"], "rank by composite", rank, "of", len(order))
