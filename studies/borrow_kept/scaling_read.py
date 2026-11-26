"""PREDICTION_scaling.md.  python3 scaling_read.py kept | python3 scaling_read.py builds DIR"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "ladder")]
import numpy as np, scaling as SC
from ladder import verse_figs
from make_kept_line_repeat import deg, MAJ, MIN, kind
q = lambda v: [round(float(x), 3) for x in np.percentile(v, (25, 50, 75))]
def dist(lines):
    """middle distance of a line's middle note from the line before's, in scale steps"""
    return [abs(float(np.median(lines[i]) - np.median(lines[i - 1]))) for i in range(1, len(lines)) if len(lines[i]) >= 4 and len(lines[i - 1]) >= 4]
if sys.argv[1] == "kept":
    import kept_corpus as KC
    d = KC.table(); key = {str(s): (int(g.key_pc.iloc[0]), MIN if str(g["mode"].iloc[0]) == "minor" else MAJ) for s, g in d.groupby("song", sort=False)}; A = collections.defaultdict(list); rows = []
    for k in KC.kept_songs():
        if k["song"] not in key: continue
        tonic, scale = key[k["song"]]; a = SC.dfa(np.array(k["p"], float)); cur = None; lines = collections.OrderedDict(); raw = collections.OrderedDict(); D = []; BL = []
        def flush():
            if kind(cur) == "Verse" and len(lines) >= 2:
                D.extend(dist(list(lines.values()))); f = verse_figs(list(raw.values()))
                if f: BL.append(f["between lines"])
        for i, (l, s) in enumerate(zip(k["lines"], k["sec"])):
            if str(s) != cur:
                if cur is not None: flush()
                cur = str(s); lines = collections.OrderedDict(); raw = collections.OrderedDict()
            lines.setdefault(l, []).append(deg(int(k["p"][i]), tonic, scale)); raw.setdefault(l, []).append(int(k["p"][i]))
        flush()
        if a: A["alpha"].append(a["alpha"]); A["short"].append(a["short"]); A["long"].append(a["long"])
        if len(D) >= 6: A["distance from the line before"].append(float(np.median(D)))
        if a and BL: rows.append((float(np.median(BL)), a["alpha"]))
    from scipy.stats import spearmanr
    out = {k: q(v) for k, v in A.items()}; out["songs"] = len(A["alpha"]); out["rank correlation of between-line spread with pitch scaling, across kept songs"] = round(float(spearmanr([r[0] for r in rows], [r[1] for r in rows])[0]), 3)
    json.dump(out, open(os.path.join(HERE, "scaling_kept.json"), "w"), indent=1); print(json.dumps(out, indent=1))
else:
    import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
    from scipy.stats import spearmanr
    out = {}
    for n, p in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59")):
        L = json.load(open(os.path.join(ROOT, p + ".json"))); o = {}
        for lab, f in (("v50", os.path.join(ROOT, p + ".song.json")), ("the pair", os.path.join(sys.argv[2], f"lyric{n}.song.json"))):
            spec = json.load(open(f))["spec"]; scale = sorted(spec["scale"]); E = M.Engine(spec)
            E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
            rng = random.Random(L.get("seed", 1)); A = collections.defaultdict(list); D = []; rows = []
            for _ in range(int(os.environ.get("N", "300"))):
                c, err = E.build(rng)
                if err or E.gates(c): continue
                ns = sorted(c["notes"], key=lambda x: x["on"]); a = SC.dfa(np.array([x["p"] for x in ns], float))
                if not a: continue
                A["alpha"].append(a["alpha"]); A["short"].append(a["short"]); A["long"].append(a["long"]); by = collections.OrderedDict(); bl = []
                for x in sorted(E.as_sung(c["notes"]), key=lambda x: x["on"]):
                    if CP.kind(x["sec"]) == "Verse" and x.get("melisma") != "second": by.setdefault(x["sec"], collections.OrderedDict()).setdefault(x["line"], []).append(x["p"])
                for lines in by.values():
                    ls = list(lines.values()); D.extend(dist([[deg(q_, 0, scale) for q_ in l] for l in ls])); f_ = verse_figs(ls)
                    if f_: bl.append(f_["between lines"])
                if bl: rows.append((float(np.median(bl)), a["alpha"]))
            o[lab] = dict(builds=len(A["alpha"]), alpha=round(st.median(A["alpha"]), 3), short=round(st.median(A["short"]), 3), long=round(st.median(A["long"]), 3), distance_from_the_line_before=round(float(np.median(D)), 2), mean_distance=round(float(np.mean(D)), 2), rank_correlation_spread_with_scaling=round(float(spearmanr([r[0] for r in rows], [r[1] for r in rows])[0]), 3))
        out[n] = o; print(n, json.dumps(o), flush=True)
    json.dump(out, open(os.path.join(HERE, os.environ.get("OUT", "scaling_builds.json")), "w"), indent=1)
