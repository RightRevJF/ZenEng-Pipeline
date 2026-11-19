import sys, os, re, json, pickle, collections, hashlib, warnings, numpy as np, pandas as pd; warnings.filterwarnings("ignore")
sys.path[:0] = ["/home/claude/zeneng/corpus/v22", "/home/claude/zeneng/corpus/v25", "/home/claude/rightrevjf/zeneng-pipeline/lib/luthier"]
os.chdir("/home/claude/zeneng/corpus/v22"); import fit as F; os.chdir("/home/claude/zeneng/corpus/v26"); import shapes as S
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)|feat.*$|featuring.*$", "", str(s).lower().replace("&", "and")))
ROOT = "/tmp/claude-0/lyr/Lyrics-Conditioned-Neural-Melody-Generation/"; D = ROOT + "lmd-full_and_reddit_MIDI_dataset/"; J = json.load(open(ROOT + "lmd-full_MIDI_dataset/listSongJSON.json"))
B = pd.read_csv("/home/claude/zeneng/corpus/billboard_songs.csv"); B["t"] = B.title.map(norm); B["a"] = B.performer.map(norm); B["year"] = B["first"].str[:4].astype(int)
byT = collections.defaultdict(list)
for r in B.itertuples(): byT[r.t].append(r)
def match(name):
    d, b = os.path.split(name); b = re.sub(r"\.(mid|kar|npy)$", "", b, flags=re.I); b = re.sub(r"[ _.]+[LlKk]$|[ _]*\d+$", "", b); b = re.sub(r"[ _.]+[LlKk]$|[ _]*\d+$", "", b); full = norm(d + " " + b); cands = []
    parts = [p for p in re.split(r"\s+-\s+|_-_|-|\.", b) if p.strip()]; tries = [b] + parts + ["".join(parts[1:])] if len(parts) > 1 else [b]
    for x in tries:
        t = norm(x.replace("_", " "))
        for r in byT.get(t, []):
            if len(r.a) >= 3 and (r.a in full.replace(t, "", 1) or r.a in norm(d)): cands.append((0, r))
            elif len(byT[t]) == 1 and len(t) >= 9 and x == b: cands.append((1, r))
    return min(cands, key=lambda c: (c[0], c[1].peak)) if cands else None
def read(f):
    a = np.load(f, allow_pickle=True, encoding="latin1"); notes, syl = a[0][1], [str(s) for s in a[0][2]]
    t = []; now = 0.0
    for p, d, r in notes: now += float(r); t.append(now); now += float(d)
    p = [int(n[0]) for n in notes]; tr = [None] * len(syl); i = 0; clean = [re.sub(r"[^a-z']", "", s.lower()) for s in syl]
    while i < len(syl):
        for k in (5, 4, 3, 2, 1):
            if i + k > len(syl): continue
            info = F.word_info("".join(clean[i:i + k])) if all(clean[i:i + k]) else None
            if info is not None and len(info[0]) == k:
                for j, (st, fn) in enumerate(info[0]): tr[i + j] = 0 if (fn and k == 1) else 2 if st else 1
                i += k; break
        else: i += 1
    lines = np.cumsum([1 if (j and notes[j][2] >= 1.0) else 0 for j in range(len(notes))])
    return np.array(t), np.array(p), tr, lines
def cc1(A, Bm):
    A = A - A.mean(0); Bm = Bm - Bm.mean(0); return float(np.linalg.svd(np.linalg.qr(A)[0].T @ np.linalg.qr(Bm)[0], compute_uv=False)[0])
if __name__ == "__main__":
    used = set(pickle.load(open("/home/claude/zeneng/corpus/v25/shapes.pkl", "rb")).title); rows = {}; rng = np.random.default_rng(0); n = 0
    for f in sorted(os.listdir(D + "syllable_level_npy_39")):
        name = J.get(f[:-4], f); m = match(name)
        if not m or m[1].year > 2005 or m[1].t in used: continue
        try: t, p, tr, lines = read(D + "syllable_level_npy_39/" + f)
        except Exception as e: continue
        idx = np.array([i for i in range(len(tr)) if tr[i] is not None])
        if len(idx) < 60 or len(set(p.tolist())) < 4: continue
        key = (m[1].t, m[1].a)
        if key in rows and rows[key]["n"] >= len(idx): continue
        P = S.path(list(zip(t, p))); w = np.array([(0, .4, 1)[tr[i]] for i in idx]); Wd = np.c_[w, w == 0]; ln = lines[idx]
        try:
            obs = cc1(Wd, P[idx]); sh = []
            for _ in range(100):
                o = np.arange(len(idx))
                for l in set(ln.tolist()):
                    q = np.where(ln == l)[0]; o[q] = rng.permutation(q)
                sh.append(cc1(Wd[o], P[idx]))
            ms = S.measures([list(zip(t, p))])
        except Exception as e: continue
        rows[key] = dict(file=f, name=name, title=m[1].t, artist=m[1].a, loose=m[0], year=m[1].year, peak=m[1].peak, weeks=m[1].weeks, notes=len(p), n=len(idx), M7=(obs - np.mean(sh)) / (np.std(sh) + 1e-9), M7r=obs, M3=ms["M3"], M4=ms["M4"])
    x = pd.DataFrame(rows.values()); print("songs matched, 2005 or earlier, fresh:", len(x), "loose", int(x.loose.sum())); pickle.dump(x, open("fresh.pkl", "wb"))
