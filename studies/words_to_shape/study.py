"""Do a song's words and form predict its tune's shape? See PREDICTION.md. python3 studies/words_to_shape/study.py -> result.json"""
import sys, os, json, re, collections, numpy as np
from scipy.stats import spearmanr
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupKFold
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import kept_corpus as KC, words_to_shape as WS
KR = json.load(open(os.path.join(ROOT, "tables", "metre_atlas", "kept_readings.json")))["4-4_pop_sung"]; NM = KR["names"]; ROW = dict(zip(KR["song_names"], KR["rows"]))
MODE = {str(s): str(g["mode"].iloc[0]) for s, g in KC.table().groupby("song", sort=False)}
SHAPE = ["range", "moves by step", "moves by leap", "repeated notes", "bars on a figure already sung", "bars on a rhythm already sung", "rhythm scaling"]; CHECK = "notes a bar"
PRED = ["syllables in the song (log)", "syllables a line", "unevenness of the lines", "syllables a word", "different words over all words", "lines said again word for word", "words in a three-word run already sung", "kinds of section", "share of syllables in a chorus", "has a bridge", "minor", "year"]
X, Y, G, names = [], [], [], []
for k in KC.kept_songs():
    s = str(k["song"])
    if s not in ROW: continue
    lines = WS.kept_lines(k); sec = [str(x).lower() for x in k["sec"]]                                       # 749.128: lines read as a Luthier lyric's are (the first run split the words by the lines' notes; result_v39.json)
    X.append(WS.features(lines, len({re.sub(r"[^a-z]", "", x) for x in sec}), float(np.mean([("chorus" in x or "refrain" in x) for x in sec])), any("bridge" in x for x in sec), "min" in MODE.get(s, "").lower(), k["year"]))
    r = dict(zip(NM, ROW[s])); Y.append([r[c] for c in SHAPE + [CHECK]]); G.append(s.split("_")[0]); names.append(s)
X = np.array(X, float); Y = np.array(Y, float); G = np.array(G); n = len(X); print("songs", n, "artists", len(set(G)))
def oof(y):
    p = np.zeros(n)
    for tr, te in GroupKFold(5).split(X, y, G):
        m = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-1, 3, 13))).fit(X[tr], y[tr]); p[te] = m.predict(X[te])
    return float(spearmanr(p, y)[0])
rng = np.random.default_rng(0); out = dict(songs=n, artists=len(set(G)), predictors=PRED, readings={})
for j, c in enumerate(SHAPE + [CHECK]):
    r = oof(Y[:, j]); sh = [oof(rng.permutation(Y[:, j])) for _ in range(500)]; p95 = float(np.percentile(sh, 95)); beats = float(np.mean(np.array(sh) < r))
    one = {PRED[i]: round(float(spearmanr(X[:, i], Y[:, j])[0]), 2) for i in range(len(PRED))}; top = sorted(one.items(), key=lambda x: -abs(x[1]))[:3]
    out["readings"][c] = dict(held_out_rank_correlation=round(r, 3), shuffles_95th=round(p95, 3), beats_share_of_shuffles=round(beats, 3), predicted=bool(r >= 0.25 and beats >= 0.95), strongest_single_predictors=top)
    print(f"{c:32} held-out {r:+.3f}   shuffles' 95th {p95:.3f}   predicted: {out['readings'][c]['predicted']}   {top}", flush=True)
k_ = sum(out["readings"][c]["predicted"] for c in SHAPE)
out["verdict"] = dict(shape_readings_predicted=k_, of=len(SHAPE), finding="the words decide the shape" if k_ >= 3 else "the words decide part of it" if k_ >= 1 else "the shape is a free choice", method_check_notes_a_bar=out["readings"][CHECK]["predicted"])
print(out["verdict"]); json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1)
