"""The join between lines (PREDICTION.md).  python3 read.py kept | python3 read.py builds"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np
def kinds(iv): iv = np.abs(np.array(iv)); n = max(1, len(iv)); return dict(n=len(iv), repeat=round(float((iv == 0).sum() / n), 3), step=round(float(((iv >= 1) & (iv <= 2)).sum() / n), 3), skip=round(float(((iv >= 3) & (iv <= 4)).sum() / n), 3), leap=round(float((iv >= 5).sum() / n), 3), mean_size=round(float(iv.mean()), 2) if len(iv) else None)
q = lambda v: [round(float(x), 2) for x in np.percentile(v, (10, 25, 50, 75, 90))]
if sys.argv[1] == "kept":
    import kept_corpus as KC
    J = collections.defaultdict(list); W = collections.defaultdict(list); sj = []; sw = []
    for k in KC.kept_songs():
        p, L, S = k["p"], k["lines"], k["sec"]; j = []; w = []
        for i in range(1, len(p)):
            if str(S[i]) != str(S[i - 1]): continue                    # a change of part is not a join inside a part
            d = int(p[i]) - int(p[i - 1]); (j if L[i] != L[i - 1] else w).append(d); (J if L[i] != L[i - 1] else W)[str(S[i])].append(d)
        if len(j) >= 8: sj.append(float(np.mean(np.abs(j)))); sw.append(float(np.mean(np.abs(w))))
    out = dict(joins={k: kinds(v) for k, v in J.items() if k in ("verse", "chorus", "bridge", "prechorus")}, inside={k: kinds(v) for k, v in W.items() if k in ("verse", "chorus", "bridge", "prechorus")}, all_joins=kinds([d for v in J.values() for d in v]), all_inside=kinds([d for v in W.values() for d in v]),
               by_song_mean_join_size_10_25_50_75_90=q(sj), by_song_mean_inside_size_10_25_50_75_90=q(sw), songs=len(sj), joins_up_share=round(float(np.mean([d > 0 for v in J.values() for d in v if d != 0])), 3))
    json.dump(out, open(os.path.join(HERE, "kept.json"), "w"), indent=1); print(json.dumps(out, indent=1))
else:
    import song_from_lyric as SL, metre_engine as M
    out = {}
    for name, stem in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59")):
        L = json.load(open(os.path.join(ROOT, stem + ".json"))); spec = json.load(open(os.path.join(ROOT, stem + ".song.json")))["spec"]; E = M.Engine(spec)
        E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        rng = random.Random(L.get("seed", 1)); j = []; w = []; nb = 0
        for _ in range(400):
            c, err = E.build(rng)
            if err or E.gates(c): continue
            nb += 1; s = sorted(E.as_sung(c["notes"]), key=lambda n: n["on"])
            for a, b in zip(s, s[1:]):
                if a["sec"] != b["sec"]: continue
                (j if a["line"] != b["line"] else w).append(b["p"] - a["p"])
        out[name] = dict(living=nb, joins=kinds(j), inside=kinds(w)); print(name, json.dumps(out[name]), flush=True)
    json.dump(out, open(os.path.join(HERE, "builds.json"), "w"), indent=1)
