"""PREDICTION_bands.md.  python3 bands_read.py kept | N=300 python3 bands_read.py builds DIR"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np
BANDS = ["4 to 8", "8 to 16", "16 to 32", "over 32"]
def F(x, s):
    x = np.asarray(x, float); n = len(x); y = np.cumsum(x - x.mean()); m = n // s; segs = np.concatenate([y[:m * s].reshape(m, s), y[n - m * s:].reshape(m, s)]); t = np.arange(s)
    return float(np.sqrt(np.mean([np.mean((seg - np.polyval(np.polyfit(t, seg, 1), t)) ** 2) for seg in segs])))
def bands(p):
    n = len(p)
    if n < 160 or np.std(p) == 0: return None
    S = [4, 8, 16, 32, n // 4]; f = [F(p, s) for s in S]
    if min(f) <= 0: return None
    return {b: float(np.log(f[i + 1] / f[i]) / np.log(S[i + 1] / S[i])) for i, b in enumerate(BANDS)}
def joins(lines):
    """lines: [(section, [pitches])] in order -> moves inside a line, moves across a join within a section"""
    ins = [abs(b - a) for _, l in lines for a, b in zip(l, l[1:])]; acr = [abs(l2[0] - l1[-1]) for (s1, l1), (s2, l2) in zip(lines, lines[1:]) if s1 == s2 and l1 and l2]
    return ins, acr
q = lambda v: [round(float(x), 3) for x in np.percentile(v, (25, 50, 75))]
def figs(ins, acr): return {"move inside a line, mean semitones": float(np.mean(ins)), "move across a join, mean semitones": float(np.mean(acr)), "no move inside a line, share": float(np.mean([x == 0 for x in ins])), "no move across a join, share": float(np.mean([x == 0 for x in acr])), "across a join, a fourth or more, share": float(np.mean([x >= 5 for x in acr]))}
if __name__ != "__main__": pass
elif sys.argv[1] == "kept":
    import kept_corpus as KC
    A = collections.defaultdict(list)
    for k in KC.kept_songs():
        b = bands(np.array(k["p"], float)); lines = []; cur = None
        for i, (l, s) in enumerate(zip(k["lines"], k["sec"])):
            if (str(s), l) != cur: cur = (str(s), l); lines.append((str(s), []))
            lines[-1][1].append(int(k["p"][i]))
        ins, acr = joins(lines)
        if b:
            for x, y in b.items(): A[x].append(y)
        if len(acr) >= 10:
            for x, y in figs(ins, acr).items(): A[x].append(y)
    out = {x: q(y) for x, y in A.items()}; out["songs with bands"] = len(A["4 to 8"]); json.dump(out, open(os.path.join(HERE, "bands_kept.json"), "w"), indent=1); print(json.dumps(out, indent=1))
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
                ns = sorted(E.as_sung(c["notes"]), key=lambda x: x["on"]); b = bands(np.array([x["p"] for x in ns], float)); lines = []; cur = None
                for x in ns:
                    if (x["sec"], x["line"]) != cur: cur = (x["sec"], x["line"]); lines.append((x["sec"], []))
                    lines[-1][1].append(x["p"])
                ins, acr = joins(lines)
                if b:
                    for x, y in b.items(): A[x].append(y)
                for x, y in figs(ins, acr).items(): A[x].append(y)
            o[lab] = dict({x: round(st.median(y), 3) for x, y in A.items()}, builds=len(A["move inside a line, mean semitones"]))
        out[n] = o; print(n, json.dumps(o), flush=True)
    json.dump(out, open(os.path.join(HERE, "bands_builds.json"), "w"), indent=1)
