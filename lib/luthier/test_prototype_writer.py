"""Held-out test of a chord writer: train on 80% of songs, write one section for every held-out section (its kind and length), compare."""
import json, random, sys, collections, statistics as st, os, tempfile, importlib
R = "/home/claude/rightrevjf/zeneng-pipeline"; sys.path.insert(0, R)
def split(mode, seed=56):
    S = [s for s in json.load(open(f"{R}/studies/harmony/billboard_sections.json")) if s["mode"] == mode]; rng = random.Random(seed); rng.shuffle(S); k = int(0.8 * len(S)); return S[:k], S[k:]
def tv(a, b):
    ta, tb = sum(a.values()), sum(b.values()); return 0.5 * sum(abs(a[k] / ta - b[k] / tb) for k in set(a) | set(b))
def measures(C, secs, mode):
    """secs: list of (kind, change list [[rn, beats]], nbars)"""
    out = {}
    for k in sorted({x[0] for x in secs}):
        v = [x for x in secs if x[0] == k]; seqs = [tuple(c[0] for c in ch) for _, ch, nb in v]; tot = lambda ch: sum(d for _, d in ch)
        per = collections.Counter(C.period(C.to_bars(ch, nb)) for _, ch, nb in v); big = collections.Counter(p for s in seqs for p in zip(s, s[1:]))
        cells = collections.Counter(tuple(C.to_bars(ch, nb)[:2]) for _, ch, nb in v)
        out[k] = dict(n=len(v), first=collections.Counter(s[0] for s in seqs), last=collections.Counter(s[-1] for s in seqs), bigrams=big, period=per,
                      distinct=st.median(len(set(s)) for s in seqs), tonic=st.median(sum(d for x, d in ch if x in ("I", "i")) / tot(ch) for _, ch, nb in v),
                      cpb=st.median(len(ch) / nb for _, ch, nb in v), out=st.mean(sum(d for x, d in ch if x not in C.IN[mode]) / tot(ch) for _, ch, nb in v),
                      loops=sum(c for p, c in per.items() if p) / len(v), top_cell=cells.most_common(1)[0][1] / len(v), cells=len(cells) / len(v), chords=collections.Counter(x for s in seqs for x in s))
    return out
def kept_sections(C, songs):
    out = []
    for so in songs:
        for s in so["sections"]:
            k = C.KIND.get(s["label"])
            if not k or any(b.get("metre", "4/4") != "4/4" for b in s["bars"]): continue
            ch = C.changes(C.beats(s))
            if ch and len(s["bars"]) >= 2: out.append((k, ch, len(s["bars"])))
    return out
def compare(K, W):
    rows = {}
    for k in K:
        if k not in W: continue
        a, b = K[k], W[k]
        rows[k] = dict(n=a["n"], first=round(tv(a["first"], b["first"]), 2), last=round(tv(a["last"], b["last"]), 2), bigrams=round(tv(a["bigrams"], b["bigrams"]), 2), chords=round(tv(a["chords"], b["chords"]), 2),
                       distinct=(a["distinct"], b["distinct"]), tonic=(round(a["tonic"], 2), round(b["tonic"], 2)), cpb=(round(a["cpb"], 2), round(b["cpb"], 2)), out=(round(a["out"], 3), round(b["out"], 3)),
                       loops=(round(a["loops"], 2), round(b["loops"], 2)), top_cell=(round(a["top_cell"], 2), round(b["top_cell"], 2)), cells=(round(a["cells"], 2), round(b["cells"], 2)))
    return rows
if __name__ == "__main__":
    import writers.chords as C
    res = {}
    for mode in ("major", "minor"):
        tr, te = split(mode); f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); json.dump(tr, f); f.close(); C.DATA = f.name
        M = C.Model(mode); held = kept_sections(C, te); held = [h for h in held if h[0] in ("verse", "chorus", "bridge", "pre")]; rng = random.Random(1); W = []
        if len(held) > 400: held = random.Random(2).sample(held, 400)
        for k, ch, nb in held:
            c = M.section(k, nb, rng, n=int(sys.argv[1]) if len(sys.argv) > 1 else 100)
            if c: W.append((k, c[0][1], nb))
        res[mode] = compare(measures(C, held, mode), measures(C, W, mode))
        # the noise floor: kept against kept (the training songs' sections against the held-out)
        res[mode + ", kept against kept"] = compare(measures(C, held, mode), measures(C, [h for h in kept_sections(C, tr) if h[0] in ("verse", "chorus", "bridge", "pre")], mode))
        for k, r in res[mode].items(): print(mode, k, r); print("   floor", {x: res[mode + ', kept against kept'][k][x] for x in ("first", "last", "bigrams", "chords", "loops", "top_cell", "cells")})
    json.dump(res, open("/home/claude/zeneng/corpus/v12/prototype_heldout.json", "w"), indent=1)
