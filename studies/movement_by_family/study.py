"""Does movement differ by genre family in kept songs? See PREDICTION.md. python3 studies/movement_by_family/study.py -> result.json"""
import sys, os, json, numpy as np, importlib.util
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
src = open(os.path.join(ROOT, "studies", "genre", "genre_test.py")).read(); ns = {}; exec(src[src.index("SOUL = "):src.index("MAJ = {")], ns)      # the families of studies/genre, by artist
KR = json.load(open(os.path.join(ROOT, "tables", "metre_atlas", "kept_readings.json")))["4-4_pop_sung"]; NM = KR["names"]; fam = [ns["family"](s) for s in KR["song_names"]]; F = np.array(fam); rng = np.random.default_rng(0)
out = dict(songs=len(F), family_sizes={f: int((F == f).sum()) for f in sorted(set(fam))}, readings={})
for c in ("moves by step", "moves by leap", "repeated notes"):
    y = np.array([r[NM.index(c)] for r in KR["rows"]]); w = float(np.subtract(*np.percentile(y, (75, 25)))); use = [f for f in sorted(set(fam)) if (F == f).sum() >= 15]
    sp = lambda lab: (lambda m: max(m) - min(m))([float(np.median(y[lab == f])) for f in use]); true = sp(F); sh = np.array([sp(rng.permutation(F)) for _ in range(2000)]); p = float(np.mean(sh >= true))
    out["readings"][c] = dict(family_middles={f: round(float(np.median(y[F == f])), 3) for f in sorted(set(fam))}, kept_middle=round(float(np.median(y)), 3), spread=round(true, 3), a_quarter_width=round(w / 4, 3), share_of_shuffles_as_large=round(p, 3), differs=bool(p < 0.05 and true >= w / 4))
    print(c, out["readings"][c])
k = sum(v["differs"] for v in out["readings"].values()); out["verdict"] = "movement from the family" if k >= 2 else "one reading from the family" if k == 1 else "the families move alike; the kept middle stays"
print(out["family_sizes"], out["verdict"]); json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1)
