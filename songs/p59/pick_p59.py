"""Song 49 (The World Is Asking): the pick of record, the engine's pick on the default path (362 with 472, under 630's threshold) of the main
run of Luthier v4, taken as drawn -- no hand edits. Evaluated again (every gate and the design gates) and written to melody_final.pkl."""
import sys, pickle, copy, io, contextlib
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p59"]
with contextlib.redirect_stdout(io.StringIO()): import melody_l4_p59 as P
D = pickle.load(open("/home/claude/p59/run/melody_l4_p59_main.pkl", "rb"))
c = copy.deepcopy(D["pick"])
for _p in ("V", "C"): P.KNOBS[_p].update(D["knobs"][_p])
P.LK.update(D["line_knobs"])
cert, meas = P.evaluate(c)
print("evaluate:", cert or "passes", "| design:", P.design_fails(c) or "pass", "| soft", c["info"]["soft"], "| lift", c["info"]["lift"])
assert cert is None and not P.design_fails(c)
c["judge"] = P.judge(c["notes"]); c["meas"] = meas; c["hand_edits"] = []
order = [x[0] for x in D["all_alive"]]; rank = order.index(c["fp"]) + 1
c["picked_from"] = dict(run="main", order=D["order_fp"], rank_by_composite=rank, rule="the default path: the engine's pick (362/472, 630)", judge_first=D["judge_first"]["fp"])
pickle.dump(dict(pick=c, run=dict(order_fp=D["order_fp"], survivors=D["survivors"], made=D["made"], deaths=dict(D["deaths"]), rerun=D["rerun"], knobs=D["knobs"],
                                  line_knobs=D["line_knobs"], chords2=D["chords2"], bass8=D["bass8"])),
            open("/home/claude/p59/melody_final.pkl", "wb"))
print(c["fp"], "rank by composite", rank, "of", len(order), "judge", round(c["judge"]["combined"], 3), "composite", meas["composite"])
N = "C C# D Eb E F F# G Ab A Bb B".split()
def nm(p): return f"{N[p % 12]}{p // 12 - 1}"
by = {}
for n in c["notes"]: by.setdefault(n["line"], []).append(n)
for s in P.SUNG:
    for i in range(len(P.LINES[s])):
        ns = sorted(by.get(f"{s}:{i}", []), key=lambda n: n["on"]); U = P.line_start(s, i)
        sy = P.LINES[s][i]
        row = []
        for n in ns:
            k = n.get("syl"); w = sy[k][0] if k is not None and k < len(sy) else "~"
            row.append(f"{w}{'*' if n.get('stress') else ''}:{nm(n['p'])}@{(n['on'] - U) / 12:.2f}/{n.get('dur', 0) / 12:.2f}")
        print(f"{s} {i} [{c['meta']['kinds'].get((s, i))}] ", "  ".join(row))
