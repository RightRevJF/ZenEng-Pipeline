"""a quick reading of a v116 pickle (smoke runs): the sixteenths, the outside share, unit returns, the calibration."""
import sys, pickle, importlib, numpy as np
sys.argv_, sys.argv = sys.argv, ["x", "1", "main"]; sys.path.insert(0, "/home/claude/p47")
P = importlib.import_module(sys.argv_[1].split("_main")[0].split("_ctl")[0].replace(".pkl", ""))
sys.argv = sys.argv_
D = pickle.load(open(sys.argv[1], "rb")); Al = D["all"]; BAR = 48
def m(k): v = [b["read"][w].get(k) for b in Al for w in ("v", "c") if b["read"][w] and b["read"][w].get(k) is not None]; v = [x for x in v if np.isfinite(x)]; return round(float(np.mean(v)), 3)
n6 = r6 = p6 = 0
for b in Al:
    ons_all = [x[0] for x in b["notes"]]; secs = {}
    for o, d, p, s, l, st, sy in b["notes"]: secs.setdefault(s, []).append(o)
    for s in ("Verse 1", "Chorus 1"):
        if s not in secs: continue
        b0 = P.BAR0[s] * BAR
        ons = sorted({o for o in secs[s] if b0 <= o < b0 + 8 * BAR}); S = set(ons)
        for t in ons:
            if t % 6 == 3: n6 += 1; r6 += (t - 3) in S and (t + 3) in S; p6 += (t + 3) not in S
print("complete", len(Al), "survivors", D["survivors"], "| on16", m("on_sixteenth"), "pushed", round(p6 / max(1, n6), 3), "runs", round(r6 / max(1, n6), 3),
      "| gaps", [m(k) for k in ("gap_sixteenth", "gap_eighth", "gap_quarter", "gap_longer")], "| outside", m("outside_scale"), "| dd", m("distinct_durations"),
      "| units", [m(k) for k in ("unit2_returns", "unit3_returns", "unit4_to_unit2")])
print("knobs", {k: round(v, 3) for k, v in D["line_knobs"].items()}, "rounds", D["rerun"].get("calibration_rounds"), D["rerun"].get("stop356"))
print({k: v for k, v in D["stats"].items() if k[:3] in ("355", "356", "357", "358", "349", "351", "360", "361", "293", "348")})
