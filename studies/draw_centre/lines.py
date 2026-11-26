"""The second reading (PREDICTION.md): a verse's spread between its lines and within them.  python3 lines.py kept | python3 lines.py builds"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np
def split(lines):
    lines = [l for l in lines if len(l) >= 3]
    if len(lines) < 3: return None
    allp = np.concatenate([np.array(l, float) for l in lines]); m = allp.mean(); mids = np.array([np.mean(l) for l in lines]); w = np.array([len(l) for l in lines], float)
    between = float(np.sqrt(np.sum(w * (mids - m) ** 2) / w.sum())); within = float(np.sqrt(sum(np.sum((np.array(l, float) - np.mean(l)) ** 2) for l in lines) / w.sum()))
    return dict(between=between, within=within, total=float(allp.std()), lines=len(lines), line_mid_range=float(mids.max() - mids.min()))
q = lambda rows, k: [round(float(x), 2) for x in np.percentile([r[k] for r in rows], (25, 50, 75))]
summ = lambda rows: dict(n=len(rows), between=q(rows, "between"), within=q(rows, "within"), total=q(rows, "total"), line_mid_range=q(rows, "line_mid_range"))
if sys.argv[1] == "kept":
    import kept_corpus as KC
    rows = []
    for k in KC.kept_songs():
        cur = None; sec = []; lines = collections.OrderedDict()
        def flush():
            if cur == "verse" and lines:
                r = split(list(lines.values()))
                if r: rows.append(r)
        for i, (l, s) in enumerate(zip(k["lines"], k["sec"])):
            if str(s) != cur: flush(); cur = str(s); lines = collections.OrderedDict()
            lines.setdefault(l, []).append(int(k["p"][i]))
        flush()
    out = summ(rows); json.dump(out, open(os.path.join(HERE, "lines_kept.json"), "w"), indent=1); print("kept", json.dumps(out))
else:
    import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
    out = {}
    for name, stem in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59")):
        L = json.load(open(os.path.join(ROOT, stem + ".json"))); spec = json.load(open(os.path.join(ROOT, stem + ".song.json")))["spec"]; E = M.Engine(spec)
        E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        rng = random.Random(L.get("seed", 1)); rows = []
        for _ in range(400):
            c, err = E.build(rng)
            if err or E.gates(c): continue
            by = collections.OrderedDict()
            for n in sorted(E.as_sung(c["notes"]), key=lambda n: n["on"]):
                if CP.kind(n["sec"]) == "Verse": by.setdefault(n["sec"], collections.OrderedDict()).setdefault(n["line"], []).append(n["p"])
            for sec, lines in by.items():
                r = split(list(lines.values()))
                if r: rows.append(r)
        out[name] = summ(rows); print(name, json.dumps(out[name]), flush=True)
    json.dump(out, open(os.path.join(HERE, "lines_builds.json"), "w"), indent=1)
