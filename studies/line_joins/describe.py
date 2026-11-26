"""After the result (a description, not a test): where a verse's lines start, end and peak, about the verse's own middle: the spread of the lines' first notes, last notes, highest notes and lowest notes. Kept verses and the builds. -> describe.json"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np
def read(lines):
    lines = [l for l in lines if len(l) >= 3]
    if len(lines) < 3: return None
    m = np.mean([p for l in lines for p in l]); sd = lambda v: float(np.std(v))
    return dict(first=sd([l[0] for l in lines]), last=sd([l[-1] for l in lines]), top=sd([max(l) for l in lines]), bottom=sd([min(l) for l in lines]), mid=sd([np.mean(l) for l in lines]), line_range=float(np.median([max(l) - min(l) for l in lines])), first_less_mid=float(np.mean([l[0] - np.mean(l) for l in lines])), last_less_mid=float(np.mean([l[-1] - np.mean(l) for l in lines])), notes=float(np.median([len(l) for l in lines])))
med = lambda rows: {k: round(float(np.median([r[k] for r in rows])), 2) for k in rows[0]}
out = {}
import kept_corpus as KC
rows = []
for k in KC.kept_songs():
    cur = None; lines = collections.OrderedDict()
    def flush():
        if cur == "verse" and lines:
            r = read(list(lines.values()))
            if r: rows.append(r)
    for i, (l, s) in enumerate(zip(k["lines"], k["sec"])):
        if str(s) != cur: flush(); cur = str(s); lines = collections.OrderedDict()
        lines.setdefault(l, []).append(int(k["p"][i]))
    flush()
out["kept verses"] = dict(n=len(rows), **med(rows)); print("kept", out["kept verses"], flush=True)
import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
for name, stem in (("55", "songs/p65/lyric55"), ("58", "songs/p68/lyric58"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59")):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); spec = json.load(open(os.path.join(ROOT, stem + ".song.json")))["spec"]; E = M.Engine(spec)
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
    rng = random.Random(L.get("seed", 1)); rows = []
    for _ in range(300):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        by = collections.OrderedDict()
        for n in sorted(E.as_sung(c["notes"]), key=lambda n: n["on"]):
            if CP.kind(n["sec"]) == "Verse": by.setdefault(n["sec"], collections.OrderedDict()).setdefault(n["line"], []).append(n["p"])
        for sec, lines in by.items():
            r = read(list(lines.values()))
            if r: rows.append(r)
    out[name] = dict(n=len(rows), **med(rows)); print(name, out[name], flush=True)
json.dump(out, open(os.path.join(HERE, "describe.json"), "w"), indent=1)
