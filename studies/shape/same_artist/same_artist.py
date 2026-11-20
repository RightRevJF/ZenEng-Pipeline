import sys, os, json, pickle, hashlib, warnings, numpy as np, pandas as pd; warnings.filterwarnings("ignore")
sys.path[:0] = ["/home/claude/zeneng/corpus/v26", "/home/claude/zeneng/corpus/v25"]
os.chdir("/home/claude/zeneng/corpus/v26"); import build as Bd; os.chdir("/home/claude/zeneng/corpus/v33"); S = Bd.S
from scipy.stats import rankdata, pearsonr
G = pickle.load(open("/home/claude/zeneng/corpus/v23/graded.pkl", "rb")); byid = {(s["src"], s["id"]): s for s in G}; s1, s2, s3 = pickle.load(open("/home/claude/zeneng/corpus/v31/s_sets.pkl", "rb"))
L = {}
for ln in open("/home/claude/corpus/parsed_lakh.jsonl"):
    r = json.loads(ln); L[r["id"]] = r
def traits(clips):
    t = np.concatenate([[n[0] for n in c] for c in clips]); p = np.concatenate([[n[1] for n in c] for c in clips]).astype(float); io = np.concatenate([np.diff([n[0] for n in c]) for c in clips]); io = io[io > 0]; st = np.concatenate([np.abs(np.diff([n[1] for n in c])) for c in clips])
    d = dict(pace=float(np.median(np.log2(io))), span=float(np.percentile(p, 90) - np.percentile(p, 10)), step=float(st.mean()), same=float((st == 0).mean()), leaps=float((st > 4).mean()), long=float((io >= 2).mean()), range=float(p.max() - p.min()))
    try: m = S.measures(clips); d.update({k: m[k] for k in ("M1", "M2", "M3", "M4", "M5")})
    except Exception: pass
    return d
rows = []
for r in s1.itertuples(): rows.append(dict(set=1, artist=r.artist, title=r.title, year=r.year, notes=r.notes, G=r.G, Sp=r.Sp, Sr=r.Sr, **traits([c for c in byid[(r.src, r.id)]["clips"] if len(c) >= 8])))
for r in s2.itertuples():
    t, p, tr, lines = Bd.read(Bd.D + "syllable_level_npy_39/" + r.file); rows.append(dict(set=2, artist=r.artist, title=r.title, year=r.year, notes=r.notes, G=r.G, Sp=r.Sp, Sr=r.Sr, **traits([list(zip(t, p))])))
for r in s3.itertuples():
    ns = sorted({(float(n["off"]), int(n["p"])) for s in L[r.id]["melody"]["sections"] for n in s["notes"] if "off" in n}); rows.append(dict(set=3, artist=r.artist, title=r.title, year=r.year, notes=r.notes, G=r.G, Sp=r.Sp, Sr=r.Sr, **traits([ns])))
T = pd.DataFrame(rows); T["G"] = T.groupby("set").G.transform(lambda v: rankdata(v) / len(v)); T.to_pickle("tune_table.pkl")
c = pd.concat([pd.read_pickle("/home/claude/zeneng/corpus/v32/chords.pkl").assign(set=4), pd.read_pickle("/home/claude/zeneng/corpus/v32/chords_fresh.pkl").assign(set=5)]); c["artist"] = c.id.str.split("/").str[0].str.replace("-", "", regex=False); c["G"] = c.groupby("set").G.transform(lambda v: rankdata(v) / len(v)); c.to_pickle("chord_table.pkl")
def fe(d, m):
    d = d.dropna(subset=[m, "G"]); k = d.artist.map(d.artist.value_counts()); d = d[k >= 3]
    if len(d) < 60: return None
    C = np.c_[tuple([rankdata(d.year), rankdata(d.notes)] + [(d.set == s).astype(float).values for s in sorted(d.set.unique())[1:]])]; a = pd.Categorical(d.artist).codes
    def res(v):
        v = np.asarray(v, float); X = np.c_[v, C]; X = X - pd.DataFrame(X).groupby(a).transform("mean").values; v, Cc = X[:, 0], X[:, 1:]; return v - Cc @ np.linalg.lstsq(Cc, v, rcond=None)[0]
    x, y = res(rankdata(d[m])), res(d.G.values); r = float(np.corrcoef(x, y)[0, 1]); df = len(d) - d.artist.nunique() - C.shape[1] - 1; from scipy.stats import t as tt; tv = r * np.sqrt(df / (1 - r * r)); return round(r, 3), round(float(2 * tt.sf(abs(tv), df)), 4), len(d), int(d.artist.nunique())
out = {}
for tab, ms in ((T, ["Sp", "Sr", "M1", "M2", "M3", "M4", "M5", "pace", "span", "step", "same", "leaps", "long", "range"]), (c, [f"C{i}" for i in range(1, 8)])):
    tab = tab.assign(h=[int(hashlib.md5(a.encode()).hexdigest(), 16) % 2 for a in tab.artist])
    for m in ms:
        A, B, P = fe(tab[tab.h == 0], m), fe(tab[tab.h == 1], m), fe(tab, m); ok = bool(A and B and np.sign(A[0]) == np.sign(B[0]) and A[1] < .05 and B[1] < .05 and P[1] < .0024); out[m] = dict(A=A, B=B, pooled=P, verdict="PASS" if ok else "fail"); print(f"{m:6} A {A}  B {B}  pooled {P}  {'PASS' if ok else 'fail'}", flush=True)
json.dump(out, open("same_artist_results.json", "w"), indent=1)
