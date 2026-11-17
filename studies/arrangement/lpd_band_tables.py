"""Arrangement study, part 2c: the tables by genre from lpd_band_rows.json. Writes lpd_band_tables.json and prints the readings."""
import json, collections, statistics as st, numpy as np
R = json.load(open("lpd_band_rows.json"))
G = ["country", "soul / r&b", "gospel", "pop", "rock", "folk", "blues", "jazz", "hip hop", "electronic", "metal"]
def q(v): v = [x for x in v if x is not None]; return [round(float(x), 3) for x in np.percentile(v, [25, 50, 75])] if len(v) >= 8 else None
def pat(p): return "".join("x" if i in p else "." for i in range(16))
out = {"about": "LPD-5 cleansed with MSD artist-term genres; quartiles 25/50/75; patterns on sixteenths, x = an onset (bar starts left)", "by_genre": {}}
for g in G:
    rs = [r for r in R if r["genre"] == g]; d = [r["drums"] for r in rs if "drums" in r]; b = [r["bass"] for r in rs if "bass" in r]
    o = dict(songs=len(rs), tempo=q([r["tempo"] for r in rs]), drums_share=round(len(d) / len(rs), 3))
    if d:
        fb = np.sum([x["fills_by_bar_of_8"] for x in d], 0); cb = np.sum([x["crash_by_bar_of_8"] for x in d], 0)
        o["drums"] = dict(backbeat=q([x["backbeat"] for x in d]), hats_16ths_share=round(float(np.mean([x["hats16"] > 0.5 for x in d])), 3), hats_8ths_share=round(float(np.mean([x["hats8"] > 0.5 for x in d])), 3),
                          fill_rate=q([x["fill_rate"] for x in d]), fills_by_bar_of_8=[round(float(v / fb.sum()), 3) for v in fb], crashes_by_bar_of_8=[round(float(v / cb.sum()), 3) for v in cb] if cb.sum() else None,
                          commonest_share=q([x["commonest_share"] for x in d]),
                          kick=[[pat(k), round(c / len(d), 3)] for k, c in collections.Counter(tuple(x["kick"]) for x in d).most_common(5)],
                          snare=[[pat(k), round(c / len(d), 3)] for k, c in collections.Counter(tuple(x["snare"]) for x in d).most_common(4)])
    if b: o["bass"] = dict(per_beat=q([x["per_beat"] for x in b]), off8=q([x["off8"] for x in b]), pitch=q([x["median_pitch"] for x in b]))
    for k in ("piano", "guitar", "strings"):
        c = [r[k] for r in rs if k in r]
        if len(c) < 20: continue
        o[k] = dict(share=round(len(c) / len(rs), 3), onsets_a_bar=q([x["onsets_a_bar"] for x in c]), together=q([x["together"] for x in c]), low=q([x["low"] for x in c]), high=q([x["high"] for x in c]),
                    held=q([x["held"] for x in c]), with_bass=q([x["with_bass"] for x in c]),
                    rhythm=[[pat(t), round(n / len(c), 3)] for t, n in collections.Counter(tuple(x["commonest_rhythm"]) for x in c).most_common(5)])
    pt = np.array([r["parts_by_tenth"] for r in rs]); mx = np.array([max(1, r["parts_max"]) for r in rs])
    o["parts_by_tenth_share_of_max"] = [round(float(v), 3) for v in np.median(pt / mx[:, None], 0)]
    o["drums_enter_bar"] = q([r["drums_enter_bar"] for r in rs if r.get("drums_enter_bar") is not None])
    out["by_genre"][g] = o
# the bass by tempo (A5), all genres
bins = [(0, 85), (85, 100), (100, 115), (115, 130), (130, 999)]
out["bass_by_tempo"] = {f"{a}-{z}": dict(songs=len(v), per_beat=q([x["bass"]["per_beat"] for x in v]), off8=q([x["bass"]["off8"] for x in v]))
                        for a, z in bins for v in [[r for r in R if "bass" in r and a <= r["tempo"] < z]]}
json.dump(out, open("lpd_band_tables.json", "w"), indent=1)
for g, o in out["by_genre"].items():
    print(f"\n== {g} songs {o['songs']} tempo {o['tempo']} drums {o['drums_share']} parts/tenth {o['parts_by_tenth_share_of_max']} enter {o['drums_enter_bar']}")
    if "drums" in o: dd = o["drums"]; print("  drums backbeat", dd["backbeat"], "16ths", dd["hats_16ths_share"], "8ths", dd["hats_8ths_share"], "fill", dd["fill_rate"], "fills/bar8", dd["fills_by_bar_of_8"], "crash/bar8", dd["crashes_by_bar_of_8"], "commonest", dd["commonest_share"]); print("  kick", dd["kick"][:4]); print("  snare", dd["snare"][:3])
    if "bass" in o: print("  bass", o["bass"])
    for k in ("piano", "guitar", "strings"):
        if k in o: print(f"  {k}", {kk: vv for kk, vv in o[k].items() if kk != "rhythm"}, "\n     rhythm", o[k]["rhythm"][:4])
print("\nbass by tempo", out["bass_by_tempo"])
