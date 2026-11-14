"""Fix 715's port check: luthier_judge4.pick on song 48's clean survivors gives the picks listed in luthier_v6_judge.json."""
import pickle, sys, time, json
sys.path.insert(0, "/home/claude/p58")
t0 = time.time(); import luthier_judge4 as J4; print("loaded", round(time.time() - t0, 1), "s")
def clean(path):
    D = pickle.load(open(path, "rb")); alive = {a[0] for a in D["all_alive"]}
    out = [(b["fp"], [(o, p, s) for o, d, p, s, l, st, sy in b["notes"]]) for b in D["all"] if b["fp"] in alive and not (b.get("info") or {}).get("soft")]
    return out
for lab, path, want in (("v4 main", "runl4/melody_l4_p58_main.pkl", "f867204f03ac"), ("v4 ctl", "runl4/melody_l4_p58_ctl.pkl", "5d7d02f8a36c"), ("run B", "runl3/melody_l3p2_p58_main.pkl", "d12fc936a701")):
    B = clean(path); t0 = time.time(); pk, R = J4.pick(B)
    el = sum(r["eligible for the pick"] for _, r in R)
    print(lab, "clean", len(B), "eligible", el, "pick", pk, "want", want, "OK" if pk == want else "DIFFERS", round(time.time() - t0), "s")
