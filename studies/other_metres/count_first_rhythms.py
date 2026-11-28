"""PREDICTION_count_first_rhythms.md: within a seed, the six-mark share by the first rhythms of the first verse and chorus; and what differs between two seeds' plans. python3 studies/other_metres/count_first_rhythms.py NAME=LYRIC.json,RECORD.song.json ... [diff=REC_A,REC_B] -> prints JSON. A count; no note is changed."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE]
import numpy as np, count_after_251 as CA, pool_count as PC
def one(lyr, rec, builds=400):
    L = json.load(open(lyr)); R = json.load(open(rec)); E, sp = CA.engine(L, R); phr = sum(sum(v) for v in sp["slots"].values()); six = PC.marks_for(sp.get("table"), True); rng = random.Random(L.get("seed", 1)); G = collections.defaultdict(list); n = 0; BL = E.BAR
    v1 = next(s for s in E.SUNG if E.KIND[s] == "Verse"); c1 = next((s for s in E.SUNG if E.KIND[s] == "Chorus"), None)
    for _ in range(builds):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        n += 1; f = PC.figs(E, E.as_sung(c["notes"]), phr, True); ok6 = all(PC.met(six, k, f[k]) for k in six); okr = PC.met(six, "rhythm_again", f["rhythm_again"]); row = (ok6, okr, f["rhythm_again"])
        for sec, nm in ((v1, "verse 1"), (c1, "chorus 1")):
            if sec is None: continue
            i0 = next((i for i in range(len(E.LINES[sec])) if E._made.get((sec, i)) in ("fresh", "870 wait")), None); xs = [x for x in c["notes"] if x["sec"] == sec]
            bars = collections.OrderedDict()
            for x in sorted(xs, key=lambda x: x["on"]): bars.setdefault(x["on"] // BL, []).append(x["on"] % BL)
            d = len(set(tuple(v) for v in bars.values())); G[f"{nm} ended with " + ("8 or fewer" if d <= 8 else "9 or 10" if d <= 10 else "11 or more") + " different bar rhythms"].append(row)
            if i0 is not None:
                U = E.line_start(sec, i0); lb = collections.OrderedDict()
                for x in sorted((x for x in xs if x["line"] == i0), key=lambda x: x["on"]):
                    if x["on"] >= U: lb.setdefault((x["on"] - U) // BL, []).append(x["on"] % BL)
                v = list(lb.values()); like = len(v) >= 2 and tuple(v[0]) == tuple(v[1]); G[f"{nm}: the first line drawn has two like bars" if like else f"{nm}: the first line drawn has two unlike bars"].append(row)
        G["all living builds"].append(row)
    return dict(living_builds=n, seed=sp.get("seed"), rows={k: dict(builds=len(v), meeting_all_six_in_100=round(100 * float(np.mean([x[0] for x in v])), 1), meeting_the_rhythm_line_in_100=round(100 * float(np.mean([x[1] for x in v])), 1), rhythm_again_median=round(float(np.median([x[2] for x in v])), 3)) for k, v in sorted(G.items())})
def diff(a, b):
    A = json.load(open(a)); B = json.load(open(b)); out = {}
    for k in sorted(set(A["spec"]) | set(B["spec"])):
        x, y = A["spec"].get(k), B["spec"].get(k)
        if x != y: out[k] = [json.dumps(x)[:260], json.dumps(y)[:260]]
    out["key (record)"] = [A["key"]["key"], B["key"]["key"]]; return out
if __name__ == "__main__":
    out = {}
    for a in sys.argv[1:]:
        name, p = a.split("=", 1)
        if name == "diff": out["what differs between the two plans"] = diff(*p.split(","))
        else: out[name] = one(*p.split(","))
    print(json.dumps(out, indent=1))
