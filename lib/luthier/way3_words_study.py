"""Way 3, the study behind lib/luthier/word_weight.py and tables/kept_word_weight.json. Needs the maintainer's kept corpus (not in the repo). Two parts: fit.py (the first measure, with word rarity) and kept_table.py (the table, weights by tier only)."""
# ---- fit.py
import sys, json, random, re, numpy as np, collections
sys.path[:0] = ["/home/claude/zeneng/corpus/nine", "/home/claude/rightrevjf/zeneng-pipeline/lib/carol", "/home/claude/rightrevjf/zeneng-pipeline/lib/luthier"]
from scipy.stats import spearmanr, rankdata
import lyricsearch as LS
def word_info(w, cache={}):
    """-> list of (stressed, function) per syllable, zipf"""
    w = re.sub(r"[^a-z']", "", w.lower())
    if w in cache: return cache[w]
    try: sy = LS.syllables(w); out = ([(bool(st), bool(fn)) for _, _, st, fn in sy], LS.zipf(w))
    except Exception: out = None
    cache[w] = out; return out
def weights(words):
    """words: list of (word text, n syllables as sung). Returns a weight per sung syllable, or None for unknown words."""
    out = []
    for w, n in words:
        info = word_info(w)
        if info is None or len(info[0]) != n: out += [None] * n; continue
        sy, z = info; rare = max(0.0, min(1.0, (5.5 - z) / 3.0))
        for st, fn in sy: out.append(0.0 if (fn and len(sy) == 1) else (1.0 if st else 0.4) + rare)
    return out
def salience(t, dur, p, line_id, barlen=48):
    t = np.asarray(t); d = np.log(np.maximum(3, np.asarray(dur, float))); pos = t % barlen
    metr = np.where(pos == 0, 3.0, np.where(pos == barlen // 2, 2.0, np.where(pos % 12 == 0, 1.0, np.where(pos % 6 == 0, 0.3, 0.0))))
    p = np.asarray(p, float); h = np.zeros(len(p))
    for l in set(line_id):
        m = np.array(line_id) == l; h[m] = p[m] - p[m].mean()
    z = lambda v: (v - v.mean()) / (v.std() + 1e-9)
    return dict(length=z(d), place=z(metr), height=z(h), all=(z(d) + z(metr) + z(h)) / 3)
def fit(w, s):
    m = np.array([x is not None for x in w]); 
    if m.sum() < 40: return None
    return float(spearmanr(np.array([x for x in w if x is not None]), s[m]).correlation)
def song_fit(w, S, line_id, rng, nperm=200, stressed_only=False):
    """true fit and the shuffled-words control (each line's weights dealt again over its notes)"""
    w = list(w); idx = [i for i, x in enumerate(w) if x is not None and (not stressed_only or x >= 1.0)]
    if len(idx) < 40: return None
    wv = np.array([w[i] for i in idx]); lid = np.array([line_id[i] for i in idx]); out = {}
    for k, s in S.items():
        sv = s[idx]; true = float(spearmanr(wv, sv).correlation) if np.std(wv) > 0 else 0.0; perms = []
        if k == "all":
            for _ in range(nperm):
                pw = wv.copy()
                for l in set(lid):
                    m = np.where(lid == l)[0]; q = list(pw[m]); rng.shuffle(q); pw[m] = q
                perms.append(float(spearmanr(pw, sv).correlation) if np.std(pw) > 0 else 0.0)
            out[k] = dict(fit=true, control_mean=float(np.mean(perms)), control_95=float(np.percentile(perms, 95)), z=float((true - np.mean(perms)) / (np.std(perms) + 1e-9)))
        else: out[k] = dict(fit=true)
    return out
def kept_songs():
    import common as C
    for s, g in C.G.d.groupby("song", sort=False):
        if str(s) not in C.PT.SONGS: continue
        g = g.sort_values("abs_beat")
        if len(g) < 150: continue
        t = np.round((g.bar.values * 4.0 + g.beat.values) * 12).astype(int); du = np.round(g.dur.values * 12).astype(int); p = g.pitch.values.astype(int); syl = [str(x) if x == x else "" for x in g.syl.values]
        # words from syllables: a trailing hyphen joins to the next
        words = []; cur = ""; n = 0; lines = []; line = 0; wid = []
        for i, sx in enumerate(syl):
            if i and t[i] - t[i - 1] >= 24: line += 1
            lines.append(line); x = sx.strip(); cont = x.endswith("-"); x2 = re.sub(r"[^A-Za-z']", "", x); cur += x2; n += 1
            if not cont: words.append((cur, n)); cur = ""; n = 0
        if n: words.append((cur, n))
        try: weeks = float(g.weeks.iloc[0]); peak = float(g.peak.iloc[0])
        except Exception: weeks = peak = float("nan")
        yield dict(song=str(s), t=t, dur=du, p=p, words=words, lines=lines, weeks=weeks, peak=peak, year=int(g.year.iloc[0]) if str(g.year.iloc[0]).isdigit() else None)
if __name__ == "__main__":
    rng = random.Random(1); rows = []
    for k in kept_songs():
        w = weights(k["words"])
        if len(w) != len(k["t"]): continue
        S = salience(k["t"], k["dur"], k["p"], k["lines"]); a = song_fit(w, S, k["lines"], rng); b = song_fit(w, S, k["lines"], rng, nperm=100, stressed_only=True)
        if a: rows.append(dict(song=k["song"], weeks=k["weeks"], peak=k["peak"], year=k["year"], known=float(np.mean([x is not None for x in w])), a=a, b=b))
    q = lambda v: [round(float(x), 3) for x in np.percentile(v, (25, 50, 75))]; R = {"songs": len(rows), "words known, median share": round(float(np.median([r["known"] for r in rows])), 3)}
    R["fit (all salience)"] = q([r["a"]["all"]["fit"] for r in rows]); R["control mean"] = q([r["a"]["all"]["control_mean"] for r in rows]); R["z against the control"] = q([r["a"]["all"]["z"] for r in rows]); R["songs above their control's 95th"] = round(float(np.mean([r["a"]["all"]["fit"] > r["a"]["all"]["control_95"] for r in rows])), 3)
    for comp in ("length", "place", "height"): R[f"fit by {comp} alone"] = q([r["a"][comp]["fit"] for r in rows])
    rb = [r for r in rows if r["b"]]; R["stressed syllables only: fit"] = q([r["b"]["all"]["fit"] for r in rb]); R["stressed only: songs above their control's 95th"] = round(float(np.mean([r["b"]["all"]["fit"] > r["b"]["all"]["control_95"] for r in rb])), 3); R["stressed only: z"] = q([r["b"]["all"]["z"] for r in rb])
    for comp in ("length", "place", "height"): R[f"stressed only: fit by {comp} alone"] = q([r["b"][comp]["fit"] for r in rb])
    G = [r for r in rows if r["weeks"] == r["weeks"]]; f = np.array([r["a"]["all"]["fit"] for r in G]); zz = np.array([r["a"]["all"]["z"] for r in G]); w = np.array([r["weeks"] for r in G]); pk = -np.array([r["peak"] for r in G]); yr = np.array([r["year"] or 1975 for r in G], float)
    def partial(x, y, Z):
        rx, ry = rankdata(x), rankdata(y); Zr = np.column_stack([rankdata(z) for z in Z] + [np.ones(len(x))]); ex = rx - Zr @ np.linalg.lstsq(Zr, rx, rcond=None)[0]; ey = ry - Zr @ np.linalg.lstsq(Zr, ry, rcond=None)[0]; return round(float(np.corrcoef(ex, ey)[0, 1]), 3)
    R["grade"] = dict(songs=len(G), fit_vs_weeks=[round(float(v), 3) for v in spearmanr(f, w)], fit_vs_peak=[round(float(v), 3) for v in spearmanr(f, pk)], fit_vs_weeks_holding_year=partial(f, w, [yr]), fit_vs_peak_holding_year=partial(f, pk, [yr]), z_vs_peak=[round(float(v), 3) for v in spearmanr(zz, pk)], fit_vs_year=round(float(spearmanr(f, yr)[0]), 3))
    gb = [r for r in G if r["b"]]; fb = np.array([r["b"]["all"]["fit"] for r in gb]); R["grade"]["stressed_only_fit_vs_peak"] = [round(float(v), 3) for v in spearmanr(fb, [-r["peak"] for r in gb])]; R["grade"]["stressed_only_fit_vs_weeks"] = [round(float(v), 3) for v in spearmanr(fb, [r["weeks"] for r in gb])]
    json.dump(dict(summary=R, rows=[dict(song=r["song"], fit=r["a"]["all"]["fit"], z=r["a"]["all"]["z"], peak=r["peak"], weeks=r["weeks"]) for r in rows]), open("fit_kept.json", "w"), indent=1); print(json.dumps(R, indent=1))

# ---- kept_table.py (run separately)
# """builds tables/kept_word_weight.json from the kept songs (private corpus): the tier-only fit, place shares by tier, step directions between tiers across words"""
# import sys, json, random, numpy as np, collections
# R = "/home/claude/rightrevjf/zeneng-pipeline/"; sys.path[:0] = [".", R + "lib/luthier"]
# import fit as F, word_weight as W
# from scipy.stats import spearmanr
# def tiers(words):
#     out = []; wid = []
#     for q, (w, n) in enumerate(words):
#         info = F.word_info(w)
#         if info is None or len(info[0]) != n: out += [None] * n
#         else:
#             sy, z = info
#             for st, fn in sy: out.append(0 if (fn and len(sy) == 1) else 2 if st else 1)
#         wid += [q] * n
#     return out, wid
# rng = random.Random(1); C = np.zeros((3, 5)); D = np.zeros((3, 3, 3)); rows = []
# for k in F.kept_songs():
#     tr, wid = tiers(k["words"])
#     if len(tr) != len(k["t"]): continue
#     t, p, lines = k["t"], k["p"], k["lines"]; idx = [i for i in range(len(tr)) if tr[i] is not None]
#     for i in idx:
#         C[tr[i], W.place(int(t[i]))] += 1
#         if i and tr[i - 1] is not None and lines[i] == lines[i - 1] and wid[i] != wid[i - 1]: D[tr[i - 1], tr[i], int(np.sign(p[i] - p[i - 1])) + 1] += 1     # down, level, up
#     if len(idx) < 40: continue
#     S = W.salience(t, k["dur"], p, lines); w = np.array([W.WEIGHT[tr[i]] for i in idx]); f = {c: W.spearman(w, S[c][idx]) for c in S}; lid = np.array([lines[i] for i in idx]); perms = []
#     for _ in range(200):
#         pw = w.copy()
#         for l in set(lid.tolist()):
#             m = np.where(lid == l)[0]; q = list(pw[m]); rng.shuffle(q); pw[m] = q
#         perms.append(W.spearman(pw, S["all"][idx]))
#     rows.append(dict(song=k["song"], weeks=k["weeks"], peak=k["peak"], above=bool(f["all"] > np.percentile(perms, 95)), **f))
# q = lambda c, ps=(10, 25, 50, 75, 90): [round(float(x), 3) for x in np.percentile([r[c] for r in rows], ps)]
# G = [r for r in rows if r["weeks"] == r["weeks"]]
# T = {"source": "159 kept 4/4 songs (CoCoPops Billboard), syllables the lexicon holds; weights 0 function word, 0.4 weak syllable, 1 stressed", "songs": len(rows),
#      "fit_percentiles_10_25_50_75_90": q("all"), "fit_by_length": q("length"), "fit_by_place": q("place"), "fit_by_height": q("height"), "songs_above_their_shuffled_words_95th": round(float(np.mean([r["above"] for r in rows])), 3),
#      "fit_vs_weeks_on_chart": [round(float(x), 3) for x in spearmanr([r["all"] for r in G], [r["weeks"] for r in G])], "fit_vs_peak": [round(float(x), 3) for x in spearmanr([r["all"] for r in G], [-r["peak"] for r in G])], "graded_songs": len(G),
#      "places": ["bar start", "half bar", "another beat", "off-beat eighth", "finer"], "tiers": ["function word", "weak syllable", "stressed syllable"],
#      "place_share_by_tier": [[round(float(x), 4) for x in C[k] / C[k].sum()] for k in range(3)], "place_share_all": [round(float(x), 4) for x in C.sum(0) / C.sum()],
#      "step_down_level_up_from_tier_to_tier": [[[round(float(x), 4) for x in D[a, b] / D[a, b].sum()] for b in range(3)] for a in range(3)], "step_down_level_up_all": [round(float(x), 4) for x in D.sum((0, 1)) / D.sum()], "step_counts": D.sum(2).tolist()}
# json.dump(T, open(R + "tables/kept_word_weight.json", "w"), indent=1); json.dump(rows, open("fit_kept_tiers.json", "w"))
# for k, v in T.items(): print(k, v)
