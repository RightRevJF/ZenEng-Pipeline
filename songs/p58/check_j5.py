"""Fix 730's port check: luthier_judge5.pick on the clean survivors of the Luthier v6 runs gives the listed picks."""
import pickle, sys
sys.path.insert(0, "/home/claude/p58"); import luthier_judge5 as J5
def clean(path):
    D = pickle.load(open(path, "rb")); alive = {a[0] for a in D["all_alive"]}
    return [(b["fp"], [(o, p, s) for o, d, p, s, l, st, sy in b["notes"]]) for b in D["all"] if b["fp"] in alive and not (b.get("info") or {}).get("soft")]
for lab, path, want in (("48 main", "/home/claude/p58/runl6/melody_l6_p58_main.pkl", "3bf00742c210"), ("48 ctl", "/home/claude/p58/runl6/melody_l6_p58_ctl.pkl", "e5bb0fda1502"),
                        ("49 main", "/home/claude/p59/runl6/melody_l6_p59_main.pkl", "2a630947f684"), ("49 ctl", "/home/claude/p59/runl6/melody_l6_p59_ctl.pkl", "8a996bd122a8")):
    B = clean(path); pk, R = J5.pick(B); el = sum(r["eligible for the pick"] for _, r in R); e715 = sum(r["eligible under 715"] for _, r in R)
    ls = min(r["charge"] for _, r in R if r["eligible for the pick"]); nr = sum(1 for _, r in R if r["eligible for the pick"] and r["charge"] <= ls + 0.02)
    RD = dict(R); x = RD.get("e2b80cdc3a1c")
    print(lab, "clean", len(B), "715", e715, "730", el, "near", nr, "pick", pk, "want", want, "OK" if pk == want else "DIFFERS", "| e2b80cdc3a1c:", (x["eligible for the pick"], round(x["most-repeating window, place for its density"], 3)) if x else "")
