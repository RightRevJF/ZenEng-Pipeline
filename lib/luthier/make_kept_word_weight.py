"""895 (749.70): the maker of tables/kept_word_weight.json (fixes 879-887), with paths inside the repo.
    python3 lib/luthier/make_kept_word_weight.py            # needs the kept corpus (lib/luthier/kept_corpus.py says where to fetch it)
Weights: 0 a one-syllable function word, 0.4 a weak syllable, 1 a stressed one, read from the lexicon (lib/carol/lyricsearch.py); a word the lexicon does not hold,
or whose sung syllables are not the lexicon's count, is left out. The control deals each line's weights again over its notes, 200 times, seed 1."""
import os, sys, json, random, re, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, "..", "carol")]
import word_weight as W, kept_corpus as KC, lyricsearch as LS
from scipy.stats import spearmanr
def word_info(w, cache={}):
    w = re.sub(r"[^a-z']", "", w.lower())
    if w in cache: return cache[w]
    try: sy = LS.syllables(w); out = ([(bool(st), bool(fn)) for _, _, st, fn in sy], LS.zipf(w))
    except Exception: out = None
    cache[w] = out; return out
def tiers(words):
    out = []; wid = []
    for q, (w, n) in enumerate(words):
        info = word_info(w)
        if info is None or len(info[0]) != n: out += [None] * n
        else:
            sy, z = info
            for st, fn in sy: out.append(0 if (fn and len(sy) == 1) else 2 if st else 1)
        wid += [q] * n
    return out, wid
if __name__ == "__main__":
    WPc = [0, 0, 0]; rng = random.Random(1); C = np.zeros((3, 5)); D = np.zeros((3, 3, 3)); rows = []; FV = [3, 6, 9, 12, 18, 24, 36, 48]; FIN = np.zeros((3, len(FV))); FC = lambda d: min(range(len(FV)), key=lambda j: abs(FV[j] - d)); LEN = np.zeros((3, 6)); LC = lambda g: 0 if g <= 3 else 1 if g <= 6 else 2 if g <= 9 else 3 if g <= 12 else 4 if g <= 18 else 5
    for k in KC.kept_songs():
        tr, wid = tiers(k["words"])
        if len(tr) != len(k["t"]): continue
        t, p, lines = k["t"], k["p"], k["lines"]; idx = [i for i in range(len(tr)) if tr[i] is not None]
        for i in idx:
            C[tr[i], W.place(int(t[i]))] += 1
            if i + 1 >= len(tr) or lines[i + 1] != lines[i]: FIN[tr[i], FC(int(k["dur"][i]))] += 1
            if i + 1 < len(tr) and lines[i + 1] == lines[i]: LEN[tr[i], LC(int(t[i + 1] - t[i]))] += 1
            if i and tr[i - 1] is not None and wid[i] == wid[i - 1] and (tr[i] == 2) != (tr[i - 1] == 2):          # 911 (749.89): inside a word, the stressed syllable against the one beside it (847's figure, given a maker)
                hi = (p[i] - p[i - 1]) if tr[i] == 2 else (p[i - 1] - p[i]); WPc[0 if hi > 0 else 1 if hi == 0 else 2] += 1
            if i and tr[i - 1] is not None and lines[i] == lines[i - 1] and wid[i] != wid[i - 1]: D[tr[i - 1], tr[i], int(np.sign(p[i] - p[i - 1])) + 1] += 1
        if len(idx) < 40: continue
        S = W.salience(t, k["dur"], p, lines); w = np.array([W.WEIGHT[tr[i]] for i in idx]); f = {c: W.spearman(w, S[c][idx]) for c in S}; lid = np.array([lines[i] for i in idx]); perms = []
        for _ in range(200):
            pw = w.copy()
            for l in set(lid.tolist()):
                m = np.where(lid == l)[0]; q = list(pw[m]); rng.shuffle(q); pw[m] = q
            perms.append(W.spearman(pw, S["all"][idx]))
        rows.append(dict(song=k["song"], weeks=k["weeks"], peak=k["peak"], above=bool(f["all"] > np.percentile(perms, 95)), **f))
    q = lambda c, ps=(10, 25, 50, 75, 90): [round(float(x), 3) for x in np.percentile([r[c] for r in rows], ps)]
    G = [r for r in rows if r["weeks"] == r["weeks"]]
    T = {"source": "159 kept 4/4 songs (CoCoPops Billboard), syllables the lexicon holds; weights 0 function word, 0.4 weak syllable, 1 stressed", "songs": len(rows),
         "fit_percentiles_10_25_50_75_90": q("all"), "fit_by_length": q("length"), "fit_by_place": q("place"), "fit_by_height": q("height"), "songs_above_their_shuffled_words_95th": round(float(np.mean([r["above"] for r in rows])), 3),
         "fit_vs_weeks_on_chart": [round(float(x), 3) for x in spearmanr([r["all"] for r in G], [r["weeks"] for r in G])], "fit_vs_peak": [round(float(x), 3) for x in spearmanr([r["all"] for r in G], [-r["peak"] for r in G])], "graded_songs": len(G),
         "places": ["bar start", "half bar", "another beat", "off-beat eighth", "finer"], "tiers": ["function word", "weak syllable", "stressed syllable"],
         "place_share_by_tier": [[round(float(x), 4) for x in C[k] / C[k].sum()] for k in range(3)], "place_share_all": [round(float(x), 4) for x in C.sum(0) / C.sum()],
         "step_down_level_up_from_tier_to_tier": [[[round(float(x), 4) for x in D[a, b] / D[a, b].sum()] for b in range(3)] for a in range(3)], "step_down_level_up_all": [round(float(x), 4) for x in D.sum((0, 1)) / D.sum()], "step_counts": D.sum(2).tolist(),
         "lengths": ["a sixteenth", "an eighth", "a dotted eighth", "a quarter", "to a dotted quarter", "a half or more"], "length_share_by_tier": [[round(float(x), 4) for x in LEN[k] / LEN[k].sum()] for k in range(3)], "length_share_all": [round(float(x), 4) for x in LEN.sum(0) / LEN.sum()],
         "last_note_lengths_twelfths": FV, "last_note_length_share_by_tier": [[round(float(x), 4) for x in FIN[k] / FIN[k].sum()] for k in range(3)], "last_note_counts": FIN.sum(1).tolist(),
         "within_a_word_the_stressed_syllable_higher_level_lower": [round(x / sum(WPc), 3) for x in WPc], "within_a_word_pairs": int(sum(WPc))}
    json.dump(T, open(os.path.join(KC.ROOT, "tables", "kept_word_weight.json"), "w"), indent=1); print("tables/kept_word_weight.json written:", len(rows), "songs; fit", T["fit_percentiles_10_25_50_75_90"])
