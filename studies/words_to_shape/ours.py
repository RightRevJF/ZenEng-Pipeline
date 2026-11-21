"""What the kept songs' own link from words to shape would ask of Luthier's four lyrics, beside what each song was told by the kept song it drew.
The model is study.py's, fitted on all 160 kept songs; year is held at the kept songs' middle year, since Luthier's songs are outside the years it was fitted on.
A look for the redesign, not a trial. python3 studies/words_to_shape/ours.py -> ours.json"""
import sys, os, json, re, collections, numpy as np, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import importlib.util; sp = importlib.util.spec_from_file_location("study", os.path.join(HERE, "study.py")); S = importlib.util.module_from_spec(sp); sys.argv = sys.argv[:1]
    src = open(os.path.join(HERE, "study.py")).read().split("def oof(y):")[0]; exec(compile(src, "study_head", "exec"), S.__dict__)
from sklearn.linear_model import RidgeCV; from sklearn.preprocessing import StandardScaler; from sklearn.pipeline import make_pipeline
X, Y, SHAPE, PRED = S.X, S.Y, S.SHAPE, S.PRED; T = ["range", "bars on a figure already sung", "bars on a rhythm already sung"]; yr = float(np.median(X[:, 11]))
M = {c: make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-1, 3, 13))).fit(X, Y[:, SHAPE.index(c)]) for c in T}; Q = {c: [round(float(x), 3) for x in np.percentile(Y[:, SHAPE.index(c)], (25, 50, 75))] for c in T}; out = dict(kept_quartiles=Q, songs={})
for tag, p in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("59", "songs/p69/lyric59")):
    R = json.load(open(os.path.join(ROOT, p + ".song.json"))); sung = R["spec"]["sung"]; lw = []; kinds = set(); cho = 0; tot = 0; br = 0.0
    for name, kind, lines in sung:
        kinds.add(kind.lower()); br = max(br, float(kind.lower() == "bridge"))
        for ln in lines:
            ws = []
            for txt, _ in ln:
                if not ws or ws[-1] != txt: ws.append(txt)                                     # a word is written once for each of its syllables
            lw.append((ws, len(ln))); tot += len(ln); cho += len(ln) * (kind.lower() == "chorus")
    w = [re.sub(r"[^a-z']", "", a.lower()) for ws, _ in lw for a in ws]; w = [a for a in w if a]; L = np.array([n for _, n in lw], float); seen = set(); rep = 0
    for ws, _ in lw:
        x = " ".join(ws)
        if x in seen: rep += 1
        seen.add(x)
    tri = [tuple(w[i:i + 3]) for i in range(len(w) - 2)]; st = set(); t3 = 0
    for x in tri:
        if x in st: t3 += 1
        st.add(x)
    x = np.array([[np.log(tot), L.mean(), L.std() / L.mean(), tot / len(w), len(set(w)) / len(w), rep / len(lw), t3 / max(len(tri), 1), len(kinds), cho / tot, br, float(R["spec"].get("mode", "major") == "minor"), yr]])
    tg = R["spec"]["target"]; out["songs"][tag] = dict(title=R["title"], drew=tg["kept_song"], words={PRED[i]: round(float(x[0, i]), 3) for i in (4, 5, 6)},
        from_its_own_words={c: round(float(M[c].predict(x)[0]), 3) for c in T}, told_by_the_song_it_drew={c: round(float(tg["readings"][c]), 3) for c in T}); print(tag, json.dumps(out["songs"][tag]))
print(Q); json.dump(out, open(os.path.join(HERE, "ours.json"), "w"), indent=1)
