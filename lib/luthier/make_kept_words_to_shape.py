"""944 (Window 196): tables/kept_words_to_shape.json from the kept 4/4 songs. python3 lib/luthier/make_kept_words_to_shape.py
A ridge regression of each of three shape readings on twelve things known from the words and the form (studies/words_to_shape/study.py, where it was tested on songs held out by artist)."""
import os, sys, json, re, collections, numpy as np
from sklearn.linear_model import RidgeCV
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", ".."); sys.path.insert(0, HERE)
import kept_corpus as KC, words_to_shape as WS
KR = json.load(open(os.path.join(ROOT, "tables", "metre_atlas", "kept_readings.json")))["4-4_pop_sung"]; NM = KR["names"]; ROW = dict(zip(KR["song_names"], KR["rows"]))
MODE = {str(s): str(g["mode"].iloc[0]) for s, g in KC.table().groupby("song", sort=False)}; T3 = ["range", "bars on a figure already sung", "bars on a rhythm already sung"]; X = []; Y = []
for k in KC.kept_songs():
    s = str(k["song"])
    if s not in ROW: continue
    w = [a for a, _ in k["words"]]; cnt = collections.OrderedDict()
    for ln in k["lines"]: cnt[ln] = cnt.get(ln, 0) + 1
    L = np.array(list(cnt.values()), float); cuts = np.cumsum(L) / L.sum() * len(w); lines = [(w[int(a):int(b)], n) for a, b, n in zip(np.r_[0, cuts[:-1]], cuts, L)]      # the words by line, in proportion to the lines' notes
    sec = [str(x).lower() for x in k["sec"]]; syl = sum(n for _, n in k["words"])
    x = WS.features(lines, len({re.sub(r"[^a-z]", "", z) for z in sec}), float(np.mean([("chorus" in z or "refrain" in z) for z in sec])), any("bridge" in z for z in sec), "min" in MODE.get(s, "").lower(), k["year"])
    x[0] = float(np.log(max(syl, 1))); x[3] = syl / max(len([a for a in w if re.sub(r"[^a-z']", "", a.lower())]), 1)                                    # syllables as sung, as the study counted them
    X.append(x); r = dict(zip(NM, ROW[s])); Y.append([r[c] for c in T3])
X = np.array(X); Y = np.array(Y); mu = X.mean(0); sd = X.std(0); Z = (X - mu) / sd; out = dict(source=f"{len(X)} kept 4/4 songs (CoCoPops Billboard); made by lib/luthier/make_kept_words_to_shape.py; tested in studies/words_to_shape",
    what="what a song's words and form say of its tune's shape: a ridge regression on twelve predictors, each standardised; a prediction is held inside the kept 10th to 90th", predictors=WS.PRED, mean=[round(float(v), 6) for v in mu], sd=[round(float(v), 6) for v in sd], year_held_at=float(np.median(X[:, 11])), readings={})
for j, c in enumerate(T3):
    m = RidgeCV(alphas=np.logspace(-1, 3, 13)).fit(Z, Y[:, j]); out["readings"][c] = dict(intercept=round(float(m.intercept_), 6), coef=[round(float(v), 6) for v in m.coef_], alpha=float(m.alpha_), kept_10th=round(float(np.percentile(Y[:, j], 10)), 4), kept_90th=round(float(np.percentile(Y[:, j], 90)), 4))
    print(c, "alpha", m.alpha_, "fit rank correlation", round(float(np.corrcoef(np.argsort(np.argsort(m.predict(Z))), np.argsort(np.argsort(Y[:, j])))[0, 1]), 3))
json.dump(out, open(os.path.join(ROOT, "tables", "kept_words_to_shape.json"), "w"), indent=1); print("songs", len(X), "| year held at", out["year_held_at"])
