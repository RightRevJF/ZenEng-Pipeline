"""944 (Window 196): tables/kept_words_to_shape.json from the kept 4/4 songs. python3 lib/luthier/make_kept_words_to_shape.py
A ridge regression of each of three shape readings on twelve things known from the words and the form (studies/words_to_shape/study.py, where it was tested on songs held out by artist)."""
import os, sys, json, re, collections, numpy as np
from sklearn.linear_model import RidgeCV
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", ".."); sys.path.insert(0, HERE)
import kept_corpus as KC, words_to_shape as WS
KR = json.load(open(os.path.join(ROOT, "tables", "metre_atlas", "kept_readings.json")))["4-4_pop_sung"]; NM = KR["names"]; ROW = dict(zip(KR["song_names"], KR["rows"]))
MODE = {str(s): str(g["mode"].iloc[0]) for s, g in KC.table().groupby("song", sort=False)}; T3 = ["range", "bars on a figure already sung", "bars on a rhythm already sung"]; X = []; Y = []; GRP = []
for k in KC.kept_songs():
    s = str(k["song"])
    if s not in ROW: continue
    lines = WS.kept_lines(k); sec = [str(x).lower() for x in k["sec"]]                                       # 946 (749.128): the kept song's lines read as a Luthier lyric's are
    x = WS.features(lines, len({re.sub(r"[^a-z]", "", z) for z in sec}), float(np.mean([("chorus" in z or "refrain" in z) for z in sec])), any("bridge" in z for z in sec), "min" in MODE.get(s, "").lower(), k["year"])
    X.append(x); r = dict(zip(NM, ROW[s])); Y.append([r[c] for c in T3]); GRP.append(s.split('_')[0])
X = np.array(X); Y = np.array(Y); mu = X.mean(0); sd = X.std(0); Z = (X - mu) / sd; out = dict(source=f"{len(X)} kept 4/4 songs (CoCoPops Billboard); made by lib/luthier/make_kept_words_to_shape.py; tested in studies/words_to_shape",
    what="what a song's words and form say of its tune's shape: a ridge regression on twelve predictors, each standardised; a prediction is held inside the kept 10th to 90th", predictors=WS.PRED, mean=[round(float(v), 6) for v in mu], sd=[round(float(v), 6) for v in sd], year_held_at=float(np.median(X[:, 11])), readings={})
for j, c in enumerate(T3):
    m = RidgeCV(alphas=np.logspace(-1, 3, 13)).fit(Z, Y[:, j]); out["readings"][c] = dict(intercept=round(float(m.intercept_), 6), coef=[round(float(v), 6) for v in m.coef_], alpha=float(m.alpha_), kept_10th=round(float(np.percentile(Y[:, j], 10)), 4), kept_90th=round(float(np.percentile(Y[:, j], 90)), 4))
    print(c, "alpha", m.alpha_, "fit rank correlation", round(float(np.corrcoef(np.argsort(np.argsort(m.predict(Z))), np.argsort(np.argsort(Y[:, j])))[0, 1]), 3))
# 954 (749.135): how far a kept song's range stands from what its words ask, read on songs held out by artist (five folds). The engine's floor for the chosen tune's range is the asking plus the 25th of these (a negative number).
from sklearn.pipeline import make_pipeline; from sklearn.preprocessing import StandardScaler; from sklearn.model_selection import GroupKFold
_yr = Y[:, 0]; _pr = np.zeros(len(_yr))
for _tr, _te in GroupKFold(5).split(X, _yr, np.array(GRP)): _pr[_te] = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-1, 3, 13))).fit(X[_tr], _yr[_tr]).predict(X[_te])
_e = _yr - np.clip(_pr, out["readings"]["range"]["kept_10th"], out["readings"]["range"]["kept_90th"])
out["range_less_the_asking_held_out"] = dict(note="954 (749.135): a kept song's range less what its words ask, the asking made with that song's artist held out; the engine takes no chosen tune narrower than the asking plus the 25th", songs=int(len(_e)), sd=round(float(_e.std()), 2), p10_25_50_75_90=[round(float(v), 2) for v in np.percentile(_e, (10, 25, 50, 75, 90))], within_2=round(float(np.mean(np.abs(_e) <= 2)), 3))
print("range less the asking, held out:", out["range_less_the_asking_held_out"])
# 952 (749.131, 749.133): the family middles of repeated notes are made here (before, no script wrote them). Each family's middle is given with its bootstrap range and
# is pulled toward the kept middle by its size: weight n / (n + k), k = the variance of a family's median from sampling (1.57 x the variance within families) over the variance between the families' middles (less that sampling variance).
_src = open(os.path.join(ROOT, "studies", "genre", "genre_test.py")).read(); _ns = {}; exec(_src[_src.index("SOUL = "):_src.index("MAJ = {")], _ns)
_F = np.array([_ns["family"](s) for s in KR["song_names"]]); _y = np.array([r[NM.index("repeated notes")] for r in KR["rows"]]); _rng = np.random.default_rng(0); _km = float(np.median(_y)); _fs = sorted(set(_F))
_within = float(np.mean([np.var(_y[_F == f], ddof=1) for f in _fs])); _samp = float(np.mean([1.57 * _within / (_F == f).sum() for f in _fs])); _between = max(1e-9, float(np.var([np.median(_y[_F == f]) for f in _fs], ddof=1)) - _samp); _k = 1.57 * _within / _between
fam_out = dict(note="947 (749.129), 952 (749.131, 749.133): the share of repeated notes by genre family (studies/movement_by_family: of steps, leaps and repeated notes only repeated notes differ by family, at 2.2 shuffles in 100, uncorrected for the three tests; corrected the bar is 1.7). The engine takes the shrunk middle. Families as studies/genre",
               kept_middle=round(_km, 3), k=round(_k, 2), families={})
for f in _fs:
    v = _y[_F == f]; b = [float(np.median(_rng.choice(v, len(v)))) for _ in range(2000)]; w = len(v) / (len(v) + _k); m = float(np.median(v))
    fam_out["families"][f] = dict(songs=int(len(v)), middle=round(m, 3), range_90=[round(float(x), 3) for x in np.percentile(b, (5, 95))], weight=round(w, 3), shrunk=round(w * m + (1 - w) * _km, 3)); fam_out[f] = fam_out["families"][f]["shrunk"]
    print(f, fam_out["families"][f])
out["repeated_notes_by_family"] = fam_out
json.dump(out, open(os.path.join(ROOT, "tables", "kept_words_to_shape.json"), "w"), indent=1); print("songs", len(X), "| year held at", out["year_held_at"])
