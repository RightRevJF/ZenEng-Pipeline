"""The same reading with proposed_v47 loop_less applied (the trial, 960). 749.159 step one, a reading, no change to the engine: within-section chord repetition of the chord writer's verses, choruses and bridges
against the kept sections of the same kind and mode.
The measure is the fresh-songs ch_rep (studies/fresh_songs/measures.py): chord tokens merged when a chord repeats the one before (bar lines
ignored), sections of at least 4 merged chords, the share of chord 3-grams already heard earlier in the section. One clarification, written
before running: the writer's vocabulary folds voicing marks (5, sus, add, +) and carries no seventh marks (chord_writer.norm), so kept sections
are read in the same vocabulary (chord_writer.bars_of), and the frozen-rule reading of the same kept sections is printed beside it.
Per kind and mode, 1,000 sections drawn with Writer.section, each with a length drawn from the kept sections of that kind and mode, and a
song's own share from outside the key drawn as Writer.song draws it (823). Seed 749159.
The rule (749.159): if the writer's median sits below the kept median in both verse and bridge, there is nothing to trial; otherwise the trial goes ahead.
    python3 studies/loop_less_reading/reading.py [N] -> reading.json"""
import sys, os, json, random, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import proposed_v47 as P; P.apply(loop_less=True)
from chord_writer import Writer, sections, weight_for, KIND
from scipy.stats import mannwhitneyu
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
def repetition(s, n=3):
    seen = set(); rep = tot = 0
    for i in range(len(s) - n + 1):
        g = tuple(s[i:i + n]); tot += 1; rep += g in seen; seen.add(g)
    return rep / tot if tot else 0.0
def merged(bars):
    seq = []
    for t in bars:
        for x in t:
            if not seq or seq[-1] != x: seq.append(x)
    return seq
def ch_rep(bars):
    s = merged(bars); return repetition(s) if len(s) >= 4 else None
songs = json.load(open(os.path.join(ROOT, "studies/harmony/billboard_sections.json"))); out = {}
for mode in ("major", "minor"):
    W = Writer(mode=mode, songs=songs); S = sections(songs, mode); rng = random.Random(749159)
    for k in ("verse", "chorus", "bridge"):
        kept = [b for kk, b, _, _ in S if kk == k]
        if not kept: continue
        kr = [r for r in (ch_rep(b) for b in kept) if r is not None]
        fz = []
        for so in songs:
            if so["mode"] != mode: continue
            for sec in so["sections"]:
                if KIND.get(sec["label"]) != k: continue
                seq = []
                for b in sec["bars"]:
                    for r, sv in zip(b["rn"], b["sev"]):
                        if r is None: continue
                        t = r + ("7" if sv else "")
                        if not seq or seq[-1] != t: seq.append(t)
                if len(seq) >= 4: fz.append(repetition(seq))
        wr = []
        for i in range(N):
            n = len(rng.choice(kept)); W.chromatic = weight_for(rng.choice(W.kept_out), mode)
            try: r = ch_rep(W.section(rng, k, n))
            except RuntimeError: r = None
            if r is not None: wr.append(r)
        p = mannwhitneyu(wr, kr).pvalue if wr and kr else None
        out[f"{mode} {k}"] = dict(kept_n=len(kr), kept_median=round(st.median(kr), 4), kept_mean=round(st.mean(kr), 4), kept_frozen_rule_median=round(st.median(fz), 4) if fz else None,
                                  writer_n=len(wr), writer_median=round(st.median(wr), 4), writer_mean=round(st.mean(wr), 4),
                                  writer_share_below_kept_median=round(sum(r < st.median(kr) for r in wr) / len(wr), 3), kept_share_below_kept_median=round(sum(r < st.median(kr) for r in kr) / len(kr), 3), mannwhitney_p=p)
        print(mode, k, out[f"{mode} {k}"], flush=True)
below = {m: all(out[f"{m} {k}"]["writer_median"] < out[f"{m} {k}"]["kept_median"] for k in ("verse", "bridge") if f"{m} {k}" in out) for m in ("major", "minor")}
out["verdict"] = {m: ("nothing to trial" if v else "the trial goes ahead") for m, v in below.items()}
json.dump(out, open(os.path.join(HERE, "reading_v47.json"), "w"), indent=1); print(out["verdict"])
