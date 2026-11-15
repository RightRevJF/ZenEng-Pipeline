"""Sung to Sleep, first edition against second, both read against the 3/4 hymn tables (Open Hymnal Project, 46 hymns)."""
import json, sys
import numpy as np
sys.path.insert(0, "/home/claude/atlas")
import atlas_build as AB, harm68
HYM = json.load(open("/home/claude/atlas/tables/hymns.json"))["by_metre"]["3/4"]
Q = HYM["readings_quartiles"]
def tune_readings(path):
    t = json.load(open(path))["pick"]["tune"]; out = []
    for i, sec in enumerate(("verse", "refrain")):
        for ln in t[sec]:
            for n in ln: out.append([n["on"] + i * 16 * 36 + 12, n["dur"], n["p"]])
    return AB.readings(out, 36, [0, 12, 24], 12)
def choir(path):
    R = json.load(open(path)); V = R["voices"]; S = V["S"]; res = {}
    for v in ("A", "T", "B"):
        rs = []
        for part in ("verse", "refrain", "refrain_final"):
            lead = [dict(e, midi=e["p"], sec=e["part"]) for e in S if e["part"] == part]
            a, b = lead[0]["on"], lead[-1]["on"] + lead[-1]["dur"]
            pv = [dict(e, midi=e["p"]) for e in V[v] if a <= e["on"] < b]
            r = harm68.readings(lead, pv); r["short"] = float(np.mean([e["dur"] < 12 for e in pv])); r["n"] = len(pv); rs.append(r)
        res[v] = {k: float(np.average([r[k] for r in rs], weights=[r["n"] for r in rs])) for k in ("moves with the lead (similar)", "against it (contrary)", "holding while it moves, or the reverse (oblique)", "short")}
        res[v]["parallels"] = sum(r["parallel fifths or octaves"] for r in rs)
    return res
t1, t2 = tune_readings("melody_final_v1.json"), tune_readings("melody_final_v2.json")
c1, c2 = choir("song_record_v1.json"), choir("song_record.json")
def inside(k, v): a, m, z = Q[k]; return a <= v <= z
rows = []
for k in Q:
    rows.append(dict(reading=k, first=t1[k], second=t2[k], hymn=Q[k], first_in=inside(k, t1[k]), second_in=inside(k, t2[k])))
H = {"A": HYM["harmony"]["S1V2"], "T": HYM["harmony"]["S2V1"], "B": HYM["harmony"]["S2V2"]}
TX = {"A": HYM["texture"]["S1V2"], "T": HYM["texture"]["S2V1"], "B": HYM["texture"]["S2V2"]}
json.dump(dict(tune=rows, choir_first=c1, choir_second=c2, hymn_harmony=H, hymn_texture=TX), open("editions_compare.json", "w"))
print("tune readings inside the hymn quartiles: first", sum(r["first_in"] for r in rows), "of", len(rows), "; second", sum(r["second_in"] for r in rows))
for r in rows:
    if not (r["first_in"] and r["second_in"]): print(f"  {r['reading']}: first {r['first']:.3f} second {r['second']:.3f} hymn {[round(x, 3) for x in r['hymn']]}")
for v in "ATB":
    print(v, "first", {k[:12]: round(x, 2) for k, x in c1[v].items()}, "\n  second", {k[:12]: round(x, 2) for k, x in c2[v].items()}, "\n  hymn", {k: round(x, 2) for k, x in H[v].items() if k != 'parallels_per_100_moves'}, "short", round(TX[v]["notes_shorter_than_beat"], 3))
