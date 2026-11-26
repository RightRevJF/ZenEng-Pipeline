"""PREDICTION_2.md: A counted apart (returns / borrowed figures), B height against the line two before.  python3 read2.py kept | builds"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from read import deg, repeat, ROOT, MAJ, MIN
def shared(wa, wb):
    m = min(len(wa), len(wb)); return m > 0 and sum(x == y and x != "" for x, y in zip(wa, wb)) >= 0.5 * m
def part(lines, words=None):
    """for each line from the third: dict(rep height or None, kind, same-height vs i-2)"""
    out = []
    for i in range(1, len(lines)):
        if len(lines[i]) < 4: continue
        r = None; kind = None
        for j in (i - 2, i - 1):
            if j < 0: continue
            h = repeat(lines[j], lines[i])
            if h is not None: r = h; kind = ("return" if words is not None and shared(words[j], words[i]) else "borrowed"); break
        d2 = float(np.median(lines[i]) - np.median(lines[i - 2])) if i >= 2 and len(lines[i - 2]) >= 4 else None
        out.append(dict(r=r, kind=kind, d2=d2))
    return out
def A(rows):
    o = {}
    for kd in ("return", "borrowed"):
        hs = [x["r"] for x in rows if x["kind"] == kd]; n = max(1, len(hs))
        o[kd] = dict(n=len(hs), same_pitch=round(sum(h == 0 for h in hs) / n, 3), higher=round(sum(h > 0 for h in hs) / n, 3), lower=round(sum(h < 0 for h in hs) / n, 3), heights={str(k): v for k, v in sorted(collections.Counter(hs).items())})
    return o
def B(by):
    def sh(rows, rep):
        v = [abs(x["d2"]) < 1 for x in rows if x["d2"] is not None and (x["r"] is not None) == rep]; return (sum(v) / len(v), len(v)) if v else (None, 0)
    allr = [x for v in by.values() for x in v]; o = {}
    for rep, nm in ((False, "other_lines"), (True, "repeats")):
        s, n = sh(allr, rep); bs = [sh(v, rep)[0] for v in by.values() if sh(v, rep)[1] >= 6]
        o[nm] = dict(n=n, at_the_same_height=None if s is None else round(s, 3), by_song_25_50_75=[round(float(x), 3) for x in np.percentile(bs, (25, 50, 75))] if len(bs) >= 5 else None)
    d = [abs(x["d2"]) for x in allr if x["d2"] is not None]; o["middle_distance_in_steps"] = round(float(np.median(d)), 2) if d else None
    return o
if sys.argv[1] == "kept":
    import kept_corpus as KC
    d = KC.table(); key = {str(s): (int(g.key_pc.iloc[0]), MIN if str(g["mode"].iloc[0]) == "minor" else MAJ) for s, g in d.groupby("song", sort=False)}; R = {"verse": collections.defaultdict(list), "chorus": collections.defaultdict(list)}
    for k in KC.kept_songs():
        if k["song"] not in key: continue
        tonic, scale = key[k["song"]]; wn = [w.lower() if j == 0 else "" for w, n in k["words"] for j in range(n)]; cur = None; lines = collections.OrderedDict(); ws = collections.OrderedDict()
        def flush():
            if cur in R and len(lines) >= 2: R[cur][k["song"]] += part(list(lines.values()), [[w for w in v if w] for v in ws.values()])
        for i, (l, s) in enumerate(zip(k["lines"], k["sec"])):
            if str(s) != cur: flush(); cur = str(s); lines = collections.OrderedDict(); ws = collections.OrderedDict()
            lines.setdefault(l, []).append(deg(int(k["p"][i]), tonic, scale)); ws.setdefault(l, []).append(wn[i])
        flush()
    out = {p: dict(A=A([x for v in by.values() for x in v]), B=B(by)) for p, by in R.items()}; json.dump(out, open(os.path.join(HERE, "kept2.json"), "w"), indent=1); print(json.dumps(out))
else:
    import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
    out = {}
    for name, stem in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59")):
        L = json.load(open(os.path.join(ROOT, stem + ".json"))); spec = json.load(open(os.path.join(ROOT, stem + ".song.json")))["spec"]; spec["borrow"] = spec["borrow"] if os.environ.get("BORROW", "1") == "1" else None; E = M.Engine(spec); scale = sorted(spec["scale"])
        E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        rng = random.Random(L.get("seed", 1)); R = {"Verse": collections.defaultdict(list), "Chorus": collections.defaultdict(list)}; nb = 0
        for _ in range(300):
            c, err = E.build(rng)
            if err or E.gates(c): continue
            nb += 1; by = collections.OrderedDict()
            for n in sorted(E.as_sung(c["notes"]), key=lambda n: n["on"]):
                if n.get("melisma") == "second": continue
                by.setdefault(n["sec"], collections.OrderedDict()).setdefault(n["line"], []).append(deg(n["p"], 0, scale))
            for sec, lines in by.items():
                kd = CP.kind(sec)
                if kd in R and len(lines) >= 2: R[kd][nb] += part(list(lines.values()))
        out[name] = {p: B(by) for p, by in R.items()}; print(name, json.dumps(out[name]["Verse"]), flush=True)
    json.dump(out, open(os.path.join(HERE, "builds2.json" if os.environ.get("BORROW", "1") == "1" else "builds2_no_borrow.json"), "w"), indent=1)
