"""PREDICTION_direction.md.  python3 direction_read.py kept | N=300 python3 direction_read.py builds DIR"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np
sg = lambda x: (x > 0) - (x < 0)
def figs(lines):
    """lines: lists of pitches. Counts over the song's lines."""
    C = collections.Counter(); trav = []; runs = []
    for l in lines:
        if len(l) < 4: continue
        iv = [b - a for a, b in zip(l, l[1:])]; mid = float(np.median(l)); trav.append(abs(l[-1] - l[0])); run = best = 0; last = 0
        for k, d in enumerate(iv):
            s = sg(d)
            if s != 0 and s == last: run += 1
            elif s != 0: run = 1
            if s != 0: last = s; best = max(best, run)
            if k + 1 < len(iv):
                nx = sg(iv[k + 1])
                if abs(d) >= 5: C["a n"] += 1; C["a turn"] += nx == -s; C["a rep"] += nx == 0
                if k >= 1 and 1 <= abs(d) <= 2 and 1 <= abs(iv[k - 1]) <= 2 and sg(iv[k - 1]) == s and not (k >= 2 and sg(iv[k - 2]) == s): C["b n"] += 1; C["b turn"] += nx == -s; C["b rep"] += nx == 0
                if k >= 2 and s != 0 and sg(iv[k - 1]) == s and sg(iv[k - 2]) == s: C["c n"] += 1; C["c turn"] += nx == -s; C["c rep"] += nx == 0
                p = l[k + 1]
                if abs(p - mid) >= 5: C["d n"] += 1; C["d toward"] += nx == -sg(p - mid)
        runs.append(best)
    if not trav: return None
    o = {"e travel": float(np.median(trav)), "e travel mean": float(np.mean(trav)), "e longest run one way": float(np.mean(runs))}
    for c, t in (("a", "turn"), ("b", "turn"), ("c", "turn"), ("d", "toward")):
        if C[c + " n"] >= 8: o[f"{c} {t}"] = C[f"{c} {t}"] / C[c + " n"]
        if t == "turn" and C[c + " n"] >= 8: o[f"{c} repeat"] = C[c + " rep"] / C[c + " n"]
    return o
q = lambda v: [round(float(x), 3) for x in np.percentile(v, (25, 50, 75))]
if __name__ != "__main__": pass
elif sys.argv[1] == "kept":
    import kept_corpus as KC
    A = collections.defaultdict(list)
    for k in KC.kept_songs():
        lines = []; cur = None
        for i, (l, s) in enumerate(zip(k["lines"], k["sec"])):
            if (str(s), l) != cur: cur = (str(s), l); lines.append([])
            lines[-1].append(int(k["p"][i]))
        f = figs(lines)
        if f:
            for x, y in f.items(): A[x].append(y)
    out = {x: q(y) for x, y in sorted(A.items())}; json.dump(out, open(os.path.join(HERE, "direction_kept.json"), "w"), indent=1); print(json.dumps(out))
else:
    import song_from_lyric as SL, metre_engine as M
    out = {}
    for n, p in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59")):
        L = json.load(open(os.path.join(ROOT, p + ".json"))); o = {}
        for lab, f in (("v50", os.path.join(ROOT, p + ".song.json")), ("the pair", os.path.join(sys.argv[2], f"lyric{n}.song.json"))):
            spec = json.load(open(f))["spec"]; E = M.Engine(spec)
            E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
            rng = random.Random(L.get("seed", 1)); A = collections.defaultdict(list)
            for _ in range(int(os.environ.get("N", "300"))):
                c, err = E.build(rng)
                if err or E.gates(c): continue
                lines = []; cur = None
                for x in sorted(E.as_sung(c["notes"]), key=lambda x: x["on"]):
                    if x.get("melisma") == "second": continue
                    if (x["sec"], x["line"]) != cur: cur = (x["sec"], x["line"]); lines.append([])
                    lines[-1].append(x["p"])
                ff = figs(lines)
                for x, y in ff.items(): A[x].append(y)
            o[lab] = dict({x: round(st.median(y), 3) for x, y in sorted(A.items())}, builds=len(A["e travel"]), register_spread=(spec.get("target") or {}).get("moves", {}).get("spread"), moves=(spec.get("target") or {}).get("moves"))
        out[n] = o; print(n, json.dumps(o), flush=True)
    json.dump(out, open(os.path.join(HERE, "direction_builds.json"), "w"), indent=1)
