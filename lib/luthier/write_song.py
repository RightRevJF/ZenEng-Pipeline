"""Luthier v13 (fix 807): chords and melody with no chord chosen by hand. Takes a melody spec (lib/luthier/metre_engine.py), throws away its chords, has the chord
writer write the form's chords in the spec's key, and runs the melody engine on them.
    python3 lib/luthier/write_song.py songs/p62/spec52.json 1000 [chord seeds, default 5]"""
import json, sys, os, copy, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chord_writer as C, metre_engine as M
def kind_of(name):
    n = name.lower()
    for k in ("pre", "verse", "chorus", "bridge", "intro", "outro"):
        if k in n: return k
    return "solo"
def with_chords(spec, seed, tonic_pc, mode="major", chromatic=1.0, require=None):
    W = C.Writer(mode, chromatic=chromatic); form = [(name, kind_of(name), len(chs)) for name, chs in spec["form"]]
    names = [re.sub(r"^Last Chorus$", "Chorus 9", n) for n, _, _ in form]                    # a last chorus returns the chorus (801)
    plan = W.song([(n2, k, b) for n2, (_, k, b) in zip(names, form)], seed=seed, require=require); s = copy.deepcopy(spec); s["chords"] = {}; s["form"] = []
    tonic = C.tonic_name(tonic_pc, mode)
    for (name, _), n2 in zip(spec["form"], names):
        bars = []
        for bar in plan[n2]:
            nm = [C.name(x, tonic) for x in bar]
            for x, y in zip(bar, nm): s["chords"][y] = sorted((t + tonic_pc) % 12 for t in C.tones(x))
            bars.append(nm[0] if len(nm) == 1 else nm)
        s["form"].append([name, bars])
    s["clash_rule"] = True
    s["line_rules"] = {k: {a: b for a, b in v.items() if a != "avoid"} for k, v in s.get("line_rules", {}).items()}     # rules written for a hand-chosen chord go with it
    c, d, r = W.charge(list(plan.values())); return s, plan, dict(charge=round(c, 3), distance=round(d, 2), readings=r, kept=W.Q)
if __name__ == "__main__":
    spec = json.load(open(sys.argv[1])); N = int(sys.argv[2]) if len(sys.argv) > 2 else 1000; K = int(sys.argv[3]) if len(sys.argv) > 3 else 5; out = []
    tonic_pc = spec.get("tonic", 2)
    for seed in range(1, K + 1):
        s, plan, cr = with_chords(spec, seed, tonic_pc); r = (M.Hymn(s) if s.get("mode") == "hymn" else M.Engine(s)).run(N, spec.get("seed", 1))
        out.append(dict(chord_seed=seed, chords={k: [" ".join(b) if not isinstance(b, str) else b for b in v] for k, v in s["form"]}, roman={k: [" ".join(b) for b in v] for k, v in plan.items()}, survivors=r["survivors"], made=N, chord_charge=cr["charge"], chord_distance=cr["distance"], chord_readings=cr["readings"], kept_chord_quartiles=cr["kept"],
                        charge=r.get("pick", {}).get("charge"), median_charge=r.get("median_charge"), pick=r.get("pick", {}).get("fp"), deaths=r["deaths"]))
        print(seed, "chords' charge", cr["charge"], "| melody: survivors", r["survivors"], "pick's charge", r.get("pick", {}).get("charge")); print("   verse:", " | ".join(out[-1]["chords"].get("Verse 1", [])), "\n   chorus:", " | ".join(out[-1]["chords"].get("Chorus 1", [])))
    ok = [o for o in out if o["survivors"]]; least = min(o["chord_charge"] for o in ok); near = [o for o in ok if o["chord_charge"] <= least + 0.05]      # 809: the least charge on the kept songs' chord readings, then nearest their medians
    best = min(near, key=lambda o: (o["chord_distance"], o["chord_seed"])); best["chosen"] = True
    print("chosen: chord draft", best["chord_seed"], "| chords' charge", best["chord_charge"], "| melody pick's charge", best["charge"])
    json.dump(out, open(sys.argv[1].replace(".json", "") + ".written_chords.json", "w"), indent=1)
