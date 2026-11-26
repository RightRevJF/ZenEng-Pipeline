"""The clean reading (PREDICTION.md, marks 1 to 3): each v50 record's fitted spec, the form off and on. OUT=x.json python3 clean.py stem ..."""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP, make_kept_line_heights as LH
out = {}
for stem in sys.argv[1:]:
    L = json.load(open(stem + ".json")); rec = json.load(open(stem + ".song.json")); o = {}
    for form in (False, True):
        spec = json.loads(json.dumps(rec["spec"])); spec["line_heights"] = form
        E = M.Engine(spec); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        rng = random.Random(L.get("seed", 1)); sh = []; bt = []; fo = []; sd = []; wi = []; lift = []
        for _ in range(1000):
            c, err = E.build(rng)
            if err or E.gates(c): continue
            s = sorted(E.as_sung(c["notes"]), key=lambda n: n["on"]); v = [n["p"] for n in s if CP.kind(n["sec"]) == "Verse"]; ch = [n["p"] for n in s if CP.kind(n["sec"]) == "Chorus"]
            sh.append(collections.Counter(v).most_common(1)[0][1] / len(v)); sd.append(float(np.std(v)))
            if ch: lift.append(float(np.median(ch) - np.median(v)))
            by = collections.OrderedDict()
            for n in s:
                if CP.kind(n["sec"]) == "Verse": by.setdefault(n["sec"], collections.OrderedDict()).setdefault(n["line"], []).append(n["p"])
            for sec, lines in by.items():
                h = LH.heights(list(lines.values()))
                if h is None: continue
                off, w = h; bt.append(LH.between(off, w)); f = LH.follows(off); ls = [l for l in lines.values() if len(l) >= 3]; wi.append(float(np.sqrt(sum(np.sum((np.array(l, float) - np.mean(l)) ** 2) for l in ls) / sum(len(l) for l in ls))))
                if f is not None: fo.append(f)
        m = lambda v: round(float(st.median(v)), 3) if v else None
        o["the form" if form else "v50"] = dict(living=len(sh), between_lines=m(bt), within_lines=m(wi), follows_the_last=m(fo), share_on_the_commonest_pitch=m(sh), verses_over_the_ceiling_in_100=round(100 * sum(x > 0.44 for x in sh) / max(1, len(sh)), 1), spread=m(sd), chorus_median_over_verse=m(lift))
    out[os.path.basename(stem)] = o; print(os.path.basename(stem), json.dumps(o), flush=True)
json.dump(out, open(os.path.join(HERE, os.environ.get("OUT", "clean.json")), "w"), indent=1)
