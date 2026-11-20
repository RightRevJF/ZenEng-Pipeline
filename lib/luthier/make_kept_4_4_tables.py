"""904 (749.82): the makers of the 4/4 pop kept tables in one place, with paths inside the repo, run on the kept corpus as the parser now reads it (tie starts kept).
    python3 lib/luthier/make_kept_4_4_tables.py        # needs the kept corpus (kept_corpus.py says where to fetch it)
Writes tables/metre_atlas/4-4_pop_sung.json (fix 812's table: bars, two-bar windows, moves, places, lengths, readings' quartiles; 817's pairs; 864's and 867's readings;
863's surprise quartiles) and the 4-4_pop_sung rows of tables/metre_atlas/kept_readings.json (fix 860; the 6/8 and 3/4 rows, from Essen, are left as they stand)."""
import os, sys, json, math, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [HERE, os.path.join(ROOT, "tables", "metre_atlas")]
import kept_corpus as KC, atlas_build as AB, scaling as SC
BAR, BEATS, BEAT = 48, [0, 12, 24, 36], 12
def structure(ns, barlen):
    bars = {}
    for on, d, p in ns: bars.setdefault(on // barlen, []).append((on % barlen, p))
    seen_r = set(); seen_f = set(); r = f = 0; keys = sorted(bars)
    for k in keys:
        v = bars[k]; rh = tuple(x for x, _ in v); fig = (rh, tuple(b[1] - a[1] for a, b in zip(v, v[1:])))
        r += rh in seen_r; f += fig in seen_f; seen_r.add(rh); seen_f.add(fig)
    return {"bars on a rhythm already sung": r / len(keys), "bars on a figure already sung": f / len(keys)}
if __name__ == "__main__":
    R = []; BARS = collections.Counter(); WIN = collections.defaultdict(collections.Counter); IV = collections.Counter(); POS = collections.Counter(); DUR = collections.Counter(); n = 0; IV2 = collections.defaultdict(collections.Counter); rows = []; songs = []; NAMES_ = []; LIFTS_ = []; MEL_ = []; MELS_ = {}
    for s_, g_ in KC.table().groupby("song", sort=False):                                    # 932 (749.110): each kept song's melismas, syllables in a hundred sung on more than one note ("_" continues a syllable)
        sy_ = [str(x) if x == x else "" for x in g_.sort_values("abs_beat").syl.values]; ns_ = sum(1 for x in sy_ if x.strip() != "_"); MELS_[str(s_)] = round(100.0 * sum(1 for i_, x in enumerate(sy_) if x.strip() != "_" and i_ + 1 < len(sy_) and sy_[i_ + 1].strip() == "_") / max(ns_, 1), 2)
    for k in KC.kept_songs():
        t, p, d = k["t"], k["p"], k["dur"]; keep = [i for i in range(len(t)) if t[i] % 3 == 0 and (i == 0 or t[i] > t[i - 1])]
        ns = [[int(t[i]), int(max(3, d[i])), int(p[i])] for i in keep]; n += 1; songs.append(ns)
        R.append(AB.readings(ns, BAR, BEATS, BEAT)); bars = collections.defaultdict(list)
        for on, dd, q in ns: bars[on // BAR].append(on % BAR); DUR[min(96, dd // 3 * 3)] += 1; POS[on % BAR] += 1
        for a, b in zip(ns, ns[1:]): IV[max(-12, min(12, b[2] - a[2]))] += 1
        ivs = [max(-12, min(12, y[2] - x[2])) for x, y in zip(ns, ns[1:])]
        for x, y in zip(ivs, ivs[1:]): IV2[x][y] += 1
        for b, v in bars.items():
            BARS[tuple(v)] += 1
            if b + 1 in bars: w = tuple(v) + tuple(x + BAR for x in bars[b + 1]); WIN[len(w)][w] += 1
        keep2 = [i for i in range(len(t)) if i == 0 or t[i] > t[i - 1]]; ns2 = [[int(t[i]), 6, int(p[i])] for i in keep2 if t[i] % 3 == 0]; sc = SC.series([(x[0], x[2]) for x in ns2]); a_ = SC.dfa(sc["pitch"]); b_ = SC.dfa(sc["onsets on the grid"])
        rows.append({**AB.readings(ns2, BAR, BEATS, BEAT), **structure(ns2, BAR), "pitch scaling": a_["alpha"] if a_ else 0.9, "rhythm scaling": b_["alpha"] if b_ else 0.66})
        kn_ = [("chorus" if ("chorus" in x.lower() or "refrain" in x.lower()) else "verse" if "verse" in x.lower() else None) for x in (str(z) for z in k["sec"])]; v_ = [int(q) for q, kk in zip(p, kn_) if kk == "verse"]; c_ = [int(q) for q, kk in zip(p, kn_) if kk == "chorus"]      # 925 (749.98): each kept song's own lift, beside its row
        MEL_.append(MELS_.get(str(k["song"]))); NAMES_.append(k["song"]); LIFTS_.append(float(np.median(c_) - np.median(v_)) if len(v_) > 20 and len(c_) > 20 else None)
    tot = sum(POS.values()); IVT = sum(IV.values())
    def ivp(dd, last):                                                                       # as metre_engine.Engine.ivp reads the table
        dd = max(-12, min(12, dd)); row = IV2.get(max(-12, min(12, last))) if last is not None else None
        if row and sum(row.values()) >= 50: return (row.get(dd, 0) + 12.5 * (IV.get(dd, 0) + 0.5) / IVT) / (sum(row.values()) + 12.5)
        return (IV.get(dd, 0) + 0.5) / IVT
    sur = []
    for ns in songs:
        ic = []; last = None
        for a, b in zip(ns, ns[1:]): dd = b[2] - a[2]; ic.append(-math.log2(max(1e-9, ivp(dd, last)))); last = dd
        sur.append(float(np.mean(ic)))
    T = dict(metre="4/4", kind="sung pop", bar=BAR, beats=BEATS, beat=BEAT, tunes=n, source="CoCoPops Billboard, the 159 kept songs; parsed with tie starts kept (904)", licence="derived counts; the corpus is for research use",
             readings_quartiles={k: [float(np.percentile([r[k] for r in R], q)) for q in (25, 50, 75)] for k in R[0]},
             bar_rhythms=[[list(k), c] for k, c in BARS.most_common(400)], two_bar_windows={str(k): [[list(w), c] for w, c in v.most_common(60)] for k, v in sorted(WIN.items()) if k <= 24},
             intervals={str(k): v for k, v in sorted(IV.items())}, interval_pairs={str(k): {str(j): c for j, c in sorted(v.items())} for k, v in sorted(IV2.items())}, onset_weights={str(k): round(v / tot, 4) for k, v in sorted(POS.items())}, durations={str(k): v for k, v in sorted(DUR.items())},
             surprise_quartiles=[round(float(x), 3) for x in np.percentile(sur, (25, 50, 75))],
             two_bar_windows_all={str(k): [[list(w), c] for w, c in sorted(v.items(), key=lambda x: (-x[1], x[0]))] for k, v in sorted(WIN.items()) if k <= 24},      # 912: every kept two-bar rhythm, not the sixty commonest: the commonest are the squarest
             bar_rhythms_all=[[list(k), c] for k, c in sorted(BARS.items(), key=lambda x: (-x[1], x[0]))])
    names = sorted(rows[0])
    for nm in ("bars on a rhythm already sung", "bars on a figure already sung", "pitch scaling", "rhythm scaling"): T["readings_quartiles"][nm] = [float(x) for x in np.percentile([round(float(r[nm]), 5) for r in rows], (25, 50, 75))]
    json.dump(T, open(os.path.join(ROOT, "tables", "metre_atlas", "4-4_pop_sung.json"), "w"))
    kr = os.path.join(ROOT, "tables", "metre_atlas", "kept_readings.json"); K = json.load(open(kr)); K["4-4_pop_sung"] = dict(names=names, rows=[[round(float(r[x]), 5) for x in names] for r in rows], songs=len(rows), source="the 159 kept CoCoPops Billboard songs; tie starts kept (904)", song_names=NAMES_, lifts=LIFTS_, melismas=MEL_); json.dump(K, open(kr, "w"))
    print(n, "songs;", {k: [round(x, 3) for x in v] for k, v in T["readings_quartiles"].items()}); print("surprise", T["surprise_quartiles"])
