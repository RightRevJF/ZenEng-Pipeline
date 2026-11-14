"""Song 49 (The World Is Asking) under Luthier v6: the writer's choice C (14 Nov). 715's pick (625a95a05b1f) chants on one note through
two verse lines (Verse 1 window repeats 59% against the kept 75th of 36%); among 715's eligible clean survivors, only those whose every
section window stays under 713's ceiling (repick_v6.py), then 715's rule: e2b80cdc3a1c. Taken as drawn -- no hand edits. Evaluated again
(every gate and the design gates) and written to melody_final.pkl."""
import sys, pickle, copy, io, contextlib
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p59"]
with contextlib.redirect_stdout(io.StringIO()): import melody_l6_p59 as P
D = pickle.load(open("/home/claude/p59/runl6/melody_l6_p59_main.pkl", "rb"))
FP = open("/home/claude/p59/repick.txt").read().strip()
def rebuild(b):
    ns = []; last = {}
    for o, d, p, s, l, st, sy in b["notes"]:
        sl = last.get(l) == sy and sy is not None; last[l] = sy
        ns.append(dict(on=o, p=p, syl=sy, slur=sl, stress=st, dur=d, sec=s, line=l))
    return dict(notes=ns, meta=b["meta"], judge=b["judge"], info=b["info"], read=b["read"], lines=b["lines"], fp=b["fp"])
chk = rebuild(next(b for b in D["all"] if b["fp"] == D["pick"]["fp"]))           # the rebuild checked on 715's pick, kept whole in the run
assert [tuple(sorted(n.items())) for n in chk["notes"]] == [tuple(sorted({k: n[k] for k in ("on", "p", "syl", "slur", "stress", "dur", "sec", "line")}.items())) for n in D["pick"]["notes"]]
c = copy.deepcopy(rebuild(next(b for b in D["all"] if b["fp"] == FP)))
for _p in ("V", "C"): P.KNOBS[_p].update(D["knobs"][_p])
P.LK.update(D["line_knobs"])
cert, meas = P.evaluate(c)
print("evaluate:", cert or "passes", "| design:", P.design_fails(c) or "pass", "| soft", c["info"]["soft"], "| lift", c["info"]["lift"])
assert cert is None and not P.design_fails(c)
c["judge"] = P.judge(c["notes"]); c["meas"] = meas; c["hand_edits"] = []
order = [x[0] for x in D["all_alive"]]; rank = order.index(c["fp"]) + 1
c["picked_from"] = dict(run="main", order=D["order_fp"], rank_by_composite=rank, rule="715 among builds with every section window under 713's ceiling (the writer's choice C)", judge4_pick=D["j4"]["pick"])
pickle.dump(dict(pick=c, run=dict(order_fp=D["order_fp"], survivors=D["survivors"], made=D["made"], deaths=dict(D["deaths"]), rerun=D["rerun"], knobs=D["knobs"],
                                  line_knobs=D["line_knobs"], chords2=D["chords2"], bass8=D["bass8"])),
            open("/home/claude/p59/melody_final.pkl", "wb"))
print(c["fp"], "rank by composite", rank, "of", len(order), "composite", meas["composite"])
N = "C C# D Eb E F F# G Ab A Bb B".split()
def nm(p): return f"{N[p % 12]}{p // 12 - 1}"
by = {}
for n in c["notes"]: by.setdefault(n["line"], []).append(n)
for s in P.SUNG:
    for i in range(len(P.LINES[s])):
        ns = sorted(by.get(f"{s}:{i}", []), key=lambda n: n["on"]); U = P.line_start(s, i); sy = P.LINES[s][i]
        print(f"{s} {i} [{c['meta']['kinds'].get((s, i))}] ", "  ".join(f"{sy[n['syl']][0] if n.get('syl') is not None and n['syl'] < len(sy) else '~'}:{nm(n['p'])}@{(n['on'] - U) / 12:.2f}/{n.get('dur', 0) / 12:.2f}" for n in ns))
