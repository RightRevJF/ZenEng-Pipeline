"""Song 49 under v6, the writer's choice C (14 Nov): among the clean survivors 715 finds eligible, only builds whose every section window
(each sung section's first eight bars) repeats notes under the kept windows' 75th percentile for its density (713's ceiling, applied to
the pick); then 715's rule: the least charge, and within 0.02 of it the least distance from the kept medians."""
import pickle, sys, io, contextlib, numpy as np
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p59"]
with contextlib.redirect_stdout(io.StringIO()): import melody_l6_p59 as P
D = pickle.load(open("/home/claude/p59/runl6/melody_l6_p59_main.pkl", "rb")); J = D["j4"]["per_build"]
byfp = {b["fp"]: b for b in D["all"]}
def wins(b):
    ns = [dict(on=o, dur=d, p=p, sec=s) for o, d, p, s, l, st, sy in b["notes"]]; out = {}
    for s in P.SUNG:
        f = P.win_feats(ns, P.BAR0[s])
        if f and np.isfinite(f.get("repeat", np.nan)): out[s] = (round(f["repeat"], 3), P.KREP683[P.kband(f["notes_per_bar"])]["75th"])
    return out
ok = []
for fp, r in J.items():
    if not r["eligible"]: continue
    w = wins(byfp[fp])
    if all(a < t for a, t in w.values()): ok.append((fp, r, w))
print("eligible", sum(r["eligible"] for r in J.values()), "| every window under its ceiling", len(ok))
lst = min(r["charge"] for _, r, _ in ok); near = [x for x in ok if x[1]["charge"] <= lst + 0.02]
fp, r, w = min(near, key=lambda x: x[1]["distance"])
print("pick", fp, "charge", r["charge"], "place", r["place"], "distance", r["distance"], "near", len(near)); print(w)
print("715's pick", D["j4"]["pick"], wins(byfp[D["j4"]["pick"]]))
open("/home/claude/p59/repick.txt", "w").write(fp)
