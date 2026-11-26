"""The draw sits on its centre (PREDICTION.md).  python3 read.py kept | OUT=x.json python3 read.py builds stem ..."""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np
def spread(ps):
    c = collections.Counter(ps).most_common(); n = len(ps); lo, hi = min(ps), max(ps); p0 = c[0][0]
    return dict(top1=c[0][1] / n, top2=sum(x[1] for x in c[:2]) / n, top3=sum(x[1] for x in c[:3]) / n, different=len(c), sd=float(np.std(ps)), span=hi - lo, where=0 if p0 - lo <= (hi - lo) / 3 else 2 if hi - p0 <= (hi - lo) / 3 else 1)
def summary(rows):
    q = lambda k: [round(float(x), 3) for x in np.percentile([r[k] for r in rows], (25, 50, 75))]; n = len(rows)
    return dict(n=n, top1=q("top1"), top2=q("top2"), top3=q("top3"), different=q("different"), sd=q("sd"), span=q("span"), commonest_in_bottom_middle_top=[round(sum(r["where"] == w for r in rows) / n, 3) for w in (0, 1, 2)], over_0_44=round(sum(r["top1"] > 0.44 for r in rows) / n, 3))
if sys.argv[1] == "kept":
    import kept_corpus as KC
    d = KC.table(); K = set(json.load(open(os.path.join(ROOT, "tables", "kept_songs_4-4_pop.json")))); d = d[d.song.astype(str).isin(K)]; out = {}
    for kind in ("verse", "chorus"):
        rows = [spread(list(g.pitch.astype(int))) for s, g in d[d.section.astype(str) == kind].groupby("song") if len(g) >= 40]; out[kind] = summary(rows)
    json.dump(out, open(os.path.join(HERE, "kept.json"), "w"), indent=1); print(json.dumps(out, indent=1))
else:
    import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
    TIE = json.load(open(os.path.join(ROOT, "tables", "kept_chord_tie.json")))["weights"]; out = {}
    for stem in sys.argv[2:]:
        L = json.load(open(os.path.join(ROOT, stem + ".json"))); rec = json.load(open(os.path.join(ROOT, stem + ".song.json"))); o = {}
        for label, sw in (("v50", ()), ("the tie at kept odds", ("tie",)), ("1. the register's pull halved", ("tie", "reg")), ("2. the degrees levelled", ("tie", "deg")), ("3. the figure memory off", ("tie", "mem")), ("4. the pull halved and the degrees levelled", ("tie", "reg", "deg"))):
            spec = json.loads(json.dumps(rec["spec"]))
            if "tie" in sw: spec["chord_tie"] = TIE
            if "reg" in sw: spec["target"]["moves"]["spread"] = 2 * spec["target"]["moves"]["spread"]
            if "deg" in sw:
                for k, w in spec["degrees"]["weights"].items():
                    for dg in w: w[dg] = 1.0 if w[dg] > 0 else 0.0
            if "mem" in sw: spec["page_gate"]["memory"] = 1.0
            E = M.Engine(spec); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
            rng = random.Random(L.get("seed", 1)); V = []; Cc = []
            for _ in range(1000):
                c, err = E.build(rng)
                if err or E.gates(c): continue
                s = E.as_sung(c["notes"]); V.append(spread([n["p"] for n in s if CP.kind(n["sec"]) == "Verse"])); ch = [n["p"] for n in s if CP.kind(n["sec"]) == "Chorus"]
                if ch: Cc.append(spread(ch))
            o[label] = dict(living=len(V), verse=summary(V) if V else None, chorus=summary(Cc) if Cc else None); print(os.path.basename(stem), label, "living", len(V), "verse top1", o[label]["verse"]["top1"] if V else None, "sd", o[label]["verse"]["sd"] if V else None, "over", o[label]["verse"]["over_0_44"] if V else None, flush=True)
        out[os.path.basename(stem)] = o
    json.dump(out, open(os.path.join(HERE, os.environ.get("OUT", "builds.json")), "w"), indent=1)
