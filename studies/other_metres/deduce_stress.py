"""PREDICTION_deduce.md, after the method passed: the pop 3/4 stress table deduced, position by position on the log scale.  python3 studies/other_metres/deduce_stress.py
pop 3/4 = standard 3/4 x pop 4/4 / standard 4/4: standard cells from the Wikifonia lead sheets' words, pop 4/4 from the kept Billboard songs' words. Writes trial_tables/3-4_pop_sung.stress.json, labelled deduced."""
import os, sys, json, glob, collections
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [HERE, os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "lib", "luthier")]
import numpy as np, tables_3_4 as T34, hymn_atlas as HA, kept_corpus as KC
POS = ("downbeat", "beat", "off the beat"); CLS = ("primary", "unstressed")
def lead_S(path): x = T34.one(path); return None if x is None else x["S"]
def leadsheets(M, BL, BEATS):
    T34.M = M; T34.BL = BL; T34.BEATS = BEATS
    with Pool(2) as pool: return sum((s for s in pool.map(lead_S, sorted(glob.glob("/home/claude/corpus/choco/partitions/wikifonia/raw/*.mxl")), chunksize=20) if s), collections.Counter())
def shares(S): return {c: {p: S[(c, p)] / sum(S[(c, q)] for q in POS) for p in POS} for c in CLS}, {c: sum(S[(c, q)] for q in POS) for c in CLS}
def billboard():
    S = collections.Counter()
    for k in KC.kept_songs():
        i = 0
        for w, n in k["words"]:
            st = HA.word_stresses(w, n) if w else None
            if st is not None:
                for j, s_ in enumerate(st):
                    if s_ == 2: continue
                    pos = int(k["t"][i + j]) % 48; S[("primary" if s_ == 1 else "unstressed", "downbeat" if pos == 0 else "beat" if pos % 12 == 0 else "off the beat")] += 1
            i += n
    return S
if __name__ == "__main__":
    s34, n34 = shares(leadsheets("3/4", 36, [0, 12, 24])); s44, n44 = shares(leadsheets("4/4", 48, [0, 12, 24, 36])); p44, np44 = shares(billboard()); ded = {}
    for c in CLS:
        raw = {p: s34[c][p] * p44[c][p] / s44[c][p] for p in POS}; t = sum(raw.values()); ded[c] = {p: raw[p] / t for p in POS}
    tot = n34["primary"] + n34["unstressed"]; anyp = {p: (ded["primary"][p] * n34["primary"] + ded["unstressed"][p] * n34["unstressed"]) / tot for p in POS}
    out = dict(metre="3/4", DEDUCED=True, note="DEDUCED, not counted (749.231; PREDICTION_deduce.md): pop 3/4 = standard 3/4 x pop 4/4 / standard 4/4, each share position by position, renormalised within a weight; the method passed its check on four countable figures (deduce_check.json). To be replaced when pop songs in 3/4 with words are counted. Secondary stress left out.",
               inputs=dict(standard_3_4={c: {p: round(v, 4) for p, v in s34[c].items()} for c in CLS}, standard_4_4={c: {p: round(v, 4) for p, v in s44[c].items()} for c in CLS}, pop_4_4_Billboard={c: {p: round(v, 4) for p, v in p44[c].items()} for c in CLS}, syllables=dict(standard_3_4=n34, standard_4_4=n44, pop_4_4=np44)),
               shares={c: {p: round(v, 4) for p, v in ded[c].items()} for c in CLS}, any_syllable={p: round(v, 4) for p, v in anyp.items()}, place={c: {p: round(float(np.log(ded[c][p] / anyp[p])), 4) for p in POS} for c in CLS})
    json.dump(out, open(os.path.join(HERE, "trial_tables", "3-4_pop_sung.stress.json"), "w"), indent=1); print(json.dumps({k: out[k] for k in ("inputs", "shares", "place")}, indent=0))
