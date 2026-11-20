import sys, json, pickle, re, collections, hashlib, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
src = open("/home/claude/zeneng/corpus/v43/transfer.py").read(); exec(src[:src.index("# hits")])
sys.path.insert(0, "/home/claude/zeneng/corpus/v45"); import shape as SH
Hh = pd.concat([pd.read_pickle("/home/claude/arena/hot100_open.pkl"), pd.read_pickle("/home/claude/arena_locked/hot100_locked.pkl")], ignore_index=True); Hh["store"] = "hot100"; FH = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "spotify_track_duration_ms"]
Zs = np.nan_to_num(SH.era_coords(np.nan_to_num(Hh[FH].fillna(Hh[FH].median()).values.astype(float)), Hh.year.values.astype(int), Hh.store.values)); Hh["far_sp"] = np.sqrt((Zs ** 2).sum(1)); byT = collections.defaultdict(list)
for r in Hh.itertuples(): byT[r.t].append((r.a, r.far_sp, r.peak))
D = pd.concat([pd.read_pickle("/home/claude/arena/sound_open.pkl"), pd.read_pickle("/home/claude/arena_locked/sound_locked.pkl")], ignore_index=True); FE = [c for c in D.columns if c.endswith(".mean") and D[c].notna().mean() > .98 and D[c].std() > 0] + [c for c in ("average_loudness", "dynamic_complexity", "bpm", "danceability", "onset_rate", "chords_changes_rate", "key_strength") if c in D.columns]
Ze = np.nan_to_num(SH.era_coords(np.nan_to_num(D[FE].replace([np.inf, -np.inf], np.nan).fillna(D[FE].median()).values.astype(float)), D.year.values.astype(int), D.store.values)); D["far_es"] = np.sqrt((Ze ** 2).sum(1)); D["far_es"] = D.groupby("store").far_es.transform(lambda v: (v - v.mean()) / v.std()); byE = collections.defaultdict(list)
for r in D.itertuples(): byE[r.t].append((r.a, r.far_es))
H = pickle.load(open("/home/claude/arena/tunes_open.pkl", "rb")) + pickle.load(open("/home/claude/arena_locked/tunes_locked.pkl", "rb")); rows = []
for st in (1, 2, 3):
    X = [s for s in H if s["set"] == st]; fr = []; seqs = []; meta = []
    for s in X:
        c = max(s["clips"], key=len); p = [n[1] for n in c]; t = [n[0] for n in c]; d = list(np.diff(t)) + [1.0]
        if len(p) < 40 or len(set(p)) < 4: continue
        a = s["artist"]; sp = [x for x in byT.get(s["title"], []) if a and (a in x[0] or x[0] in a)]; es = [x for x in byE.get(s["title"], []) if a and (a in x[0] or x[0] in a)]
        fr.append(feats(p, d)); seqs.append(toks(p, d)); meta.append(dict(set=st, title=s["title"], year=s["year"], notes=len(p), G=s["G"], love=s["love"], cover_rank=s["cover_rank"], peak=sp[0][2] if sp else (s["peak"] if s["peak"] is not None else np.nan), far_sp=sp[0][1] if sp else np.nan, far_es=es[0][1] if es else np.nan, h=int(hashlib.sha1(a.encode()).hexdigest(), 16) % 2))
    f = pd.DataFrame(fr); m = pd.DataFrame(meta); f["ic"] = crossfit_ic(seqs, m.h.values); z = StandardScaler().fit_transform(f[F].fillna(f[F].median()).values); m["plain"] = R.predict(np.c_[z, z ** 2]); rows.append(m)
M = pd.concat(rows, ignore_index=True); M["peak"] = M.peak.fillna(M.peak.median()); M.to_pickle("combo.pkl"); print("songs with a tune:", len(M), "| with Spotify shell:", int(M.far_sp.notna().sum()), "| with Essentia shell:", int(M.far_es.notna().sum()))
def test(far):
    out = collections.defaultdict(list)
    for st in (1, 2, 3):
        x = M[(M.set == st) & M[far].notna()].copy()
        if len(x) < 60: continue
        zp = (x.plain - x.plain.mean()) / x.plain.std(); zf = (x[far] - x[far].mean()) / x[far].std(); x["prod"] = zp * zf; x["zp"] = zp; x["zf"] = zf; base = [np.ones(len(x)), rankdata(x.year), rankdata(x.notes), rankdata(x.peak)]
        def part(col, extra=()):
            C = np.c_[tuple(base + [x[e].values for e in extra])]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; r, p = pearsonr(res(x[col].values if col == "prod" else rankdata(x[col])), res(rankdata(x.G))); return float(r), float(p), len(x)
        out["C1 far alone"].append(part("zf")); out["C2 plain alone"].append(part("zp")); out["C3 plain x far (both held)"].append(part("prod", ("zp", "zf")))
    for k, Rs in out.items():
        z = sum(np.sign(r) * Nm.isf(p / 2) * np.sqrt(n) for r, p, n in Rs) / np.sqrt(sum(n for _, _, n in Rs)); print(f"   {k:28} sets " + " ".join(f"{r:+.3f} (n {n})" for r, _, n in Rs) + f"   pooled {sum(r * n for r, _, n in Rs) / sum(n for _, _, n in Rs):+.3f}, p {2 * Nm.sf(abs(z)):.3g}")
    x = M[M[far].notna()].copy(); x["Gr"] = x.groupby("set").G.transform(lambda v: rankdata(v) / len(v)); x["P"] = x.groupby("set").plain.transform(lambda v: v > v.median()); x["Fa"] = x.groupby("set")[far].transform(lambda v: v > v.median())
    t = x.groupby(["P", "Fa"]).Gr.agg(n="size", great=lambda v: round(float((v >= .8).mean()), 3)); print("   share of great songs (top fifth) by corner:"); [print(f"      {'plain tune' if p else 'less plain':10} / {'far from its era' if f else 'near its era':16}: {r.great:.1%}  (n {int(r.n)})") for (p, f), r in t.iterrows()]
print("WITH SPOTIFY'S SHELL"); test("far_sp"); print("WITH ESSENTIA'S SHELL (fewer songs)"); test("far_es")
