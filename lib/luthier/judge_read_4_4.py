"""Read the metre engine's 4/4 builds with the 4/4 judge (luthier_judge6, the 159 kept songs): fix 796's test of moving a 4/4 song onto the metre engine."""
import sys, json, random, numpy as np
sys.path[:0] = ["/home/claude/zeneng/corpus/judge2", "/home/claude/rightrevjf/zeneng-pipeline/lib/luthier"]
import luthier_judge6 as J6, metre_engine as M
rec = json.load(open(sys.argv[1])); spec = rec["spec"]; E = M.Engine(spec); rng = random.Random(spec.get("seed", 1)); builds = []
for k in range(int(sys.argv[2]) if len(sys.argv) > 2 else 300):
    c, err = E.build(rng)
    if err or E.gates(c): continue
    builds.append((k, [(n["on"], n["p"], "chorus" if "horus" in n["sec"] or n["sec"] == "Tag" else "verse") for n in c["notes"]]))
pk, R = J6.pick(builds); R = dict(R); pl = [r["place among kept songs"] for r in R.values()]; el = [r["eligible for the pick"] for r in R.values()]
fails = {}
for r in R.values():
    for t, ok in r["752: tests"].items():
        if not ok: fails[t] = fails.get(t, 0) + 1
    for t in r["ease or repeats outside the kept middle half"]: fails["730: " + str(t)] = fails.get("730: " + str(t), 0) + 1
out = dict(builds=len(builds), median_place=float(np.median(pl)), quartiles=[float(x) for x in np.percentile(pl, (25, 75))], eligible=int(sum(el)), judge_pick=pk, judge_pick_place=R[pk]["place among kept songs"] if pk is not None else None, fails=fails)
print(json.dumps(out, indent=1)); json.dump(out, open(sys.argv[1].replace(".song.json", ".judge6.json"), "w"), indent=1)
