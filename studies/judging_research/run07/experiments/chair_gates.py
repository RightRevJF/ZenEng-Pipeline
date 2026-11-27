"""Run 07 chair: measure-side gate inputs on the 5,901 songs: each measure on the whole song and on the first and second half of the
first file (bars and chord tokens split at the middle), plus R03-G3 p_min (run 03 obtuse_statue code, on Lakh tokens). Notes only; no
outcome is read. Usage: python3 -I chair_gates.py rows.json  (about 2 minutes), then chair_gates_report.py rows.json gates.json"""
import sys, json, math, hashlib, collections, time
sys.path.insert(0, "/home/claude/zeneng-pipeline/studies/judging_research/run07/experiments")
import numpy as np, common as C
from scipy import stats
from scipy.sparse.csgraph import connected_components
t0 = time.time()
S = C.add_shapes(C.lakh_songs())
print("songs", len(S), "artists", len({s['artist_key'] for s in S}), round(time.time()-t0), flush=True)
notes = {n["tid"]: n for n in json.load(open("/home/claude/dl/lakh/notes.json"))}
Z = np.load("/home/claude/dl/lakh/chroma.npz"); MI = json.load(open("/home/claude/dl/lpd/midi_info_v2.json"))

def resist(W):
    Qd = np.linalg.pinv(np.diag(W.sum(1)) - W); d = np.diag(Qd); return d[:, None] + d[None, :] - 2 * Qd
def pmin_of(t):
    names = sorted(set(t)); ix = {x: i for i, x in enumerate(names)}; n = len(names); M = np.zeros((n, n))
    for a, b in zip(t, t[1:]): M[ix[a], ix[b]] += 1
    if len(t) > 1 and t[-1] != t[0]: M[ix[t[-1]], ix[t[0]]] += 1
    A = ((M + M.T) > 0).astype(float); np.fill_diagonal(A, 0); links = int(np.triu(A, 1).sum())
    npc, lab = connected_components(A, directed=False)
    big = max(range(npc), key=lambda p: ((lab == p).sum(), -p)); idx = np.nonzero(lab == big)[0]
    if len(idx) < 3: return np.nan, n, links
    Ap = A[np.ix_(idx, idx)]; p = 1 - 0.5 * (Ap * resist(Ap)).sum(1); return float(p.min()), n, links

def part(X, t, seed, tm):
    d = C.song_shape(X, t, seed, tm)
    d.update(ch_rep=C.repetition(t) if len(t) >= 3 else np.nan, V=len(set(t)), ln_chg=math.log(max(len(t), 1)), ln_bars=math.log(max(len(X), 1)),
             CH=C.CH(t), A=C.A_arrow(t))
    d["pmin"], d["nd"], d["links"] = pmin_of(t) if len(set(t)) >= 3 else (np.nan, len(set(t)), 0)
    return d
rows = []
for i, s in enumerate(S):
    tid = s["tids"][0]; X = Z[tid].astype(float); t = notes[tid]["toks"]; tm = MI.get(notes[tid]["md5"], {}).get("tempo")
    sd = int(hashlib.md5(tid.encode()).hexdigest()[:8], 16); h = len(X) // 2; ht = len(t) // 2
    r = dict(artist=s["artist_key"], whole=part(X, t, sd, tm), a=part(X[:h], t[:ht], sd, tm), b=part(X[h:], t[ht:], sd, tm))
    # song-level pmin: mean over the song's files (as every measure)
    pv = [pmin_of(notes[x]["toks"]) for x in s["tids"]]
    r["pmin_song"] = float(np.nanmean([p[0] for p in pv])) if np.isfinite([p[0] for p in pv]).any() else np.nan
    r["links_song"] = float(np.mean([p[2] for p in pv]))
    rows.append(r)
    if i % 1000 == 0: print(i, round(time.time() - t0), flush=True)
json.dump(rows, open(sys.argv[1], "w"), default=float)
print("done", round(time.time() - t0))
