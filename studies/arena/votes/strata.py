import re, importlib.util, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy.stats import rankdata, pearsonr, norm as Nm
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)|feat.*$|featuring.*$", "", str(s).lower().replace("&", "and")))
sp = importlib.util.spec_from_file_location("c", "/home/claude/arena/candidates/sound.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); fn = {c["name"]: c["fn"] for c in m.CANDIDATES}["concentrated_spectrum"]
D = pd.concat([pd.read_pickle("/home/claude/arena/sound_open.pkl"), pd.read_pickle("/home/claude/arena_locked/sound_locked.pkl")], ignore_index=True); D["cs"] = np.asarray(fn(D.copy()), float)
S = pd.read_excel("/home/claude/corpus/try2/tidytuesday/data/2021/2021-09-14/Hot 100 Audio Features.xlsx").dropna(subset=["spotify_track_popularity"]); S["t"] = S.Song.map(norm); S["a"] = S.Performer.map(norm); S = S.sort_values("spotify_track_popularity", ascending=False).drop_duplicates(["t", "a"]); D = D.merge(S[["t", "a", "spotify_genre", "acousticness", "energy", "tempo", "valence"]].rename(columns={"tempo": "sp_tempo", "energy": "sp_energy", "valence": "sp_valence"}), on=["t", "a"], how="left")
FAM = dict(rock=r"rock|metal|punk|grunge", soul=r"soul|motown|r&b|funk|disco|quiet storm", country=r"country|nashville", hiphop=r"hip hop|rap", folk=r"folk|singer-songwriter", standards=r"adult standards|easy listening|lounge|vocal jazz|brill", dance=r"dance|new wave|synth|europop")
def dummies(x): 
    g = np.array([[float(bool(re.search(p, str(v)))) for p in FAM.values()] for v in x.spotify_genre]); y5 = pd.get_dummies((x.year // 5).astype(int)).values[:, 1:].astype(float); tb = pd.get_dummies(pd.qcut(x.bpm, 5, labels=False, duplicates="drop")).values[:, 1:].astype(float); return g, y5, tb
def part(x, v, tg, extra):
    C = np.c_[tuple([np.ones(len(x)), rankdata(x.peak)] + list(extra))]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; r, p = pearsonr(res(rankdata(v)), res(rankdata(x[tg]))); return float(r), float(p), len(x)
def pool(R): z = sum(np.sign(r) * Nm.isf(p / 2) * np.sqrt(n) for r, p, n in R) / np.sqrt(sum(n for _, _, n in R)); return float(sum(r * n for r, _, n in R) / sum(n for _, _, n in R)), float(2 * Nm.sf(abs(z)))
out = {}; stores = ("mcgill_whole_recordings", "msd_previews")
for label, what in (("year (rank) and peak only", "base"), ("+ five-year bands", "y5"), ("+ tempo bands", "y5t"), ("+ genre families (ALL held: Q3)", "all"), ("ALL + Spotify acousticness, energy, valence", "allsp")):
    for tg in ("G", "love", "cover_rank"):
        R = []
        for st in stores:
            x = D[D.store == st].dropna(subset=["cs", "bpm"]).copy()
            if what == "allsp": x = x.dropna(subset=["acousticness", "sp_energy", "sp_valence"])
            g, y5, tb = dummies(x); ex = dict(base=[rankdata(x.year)], y5=[y5], y5t=[y5, tb], all=[y5, tb, g], allsp=[y5, tb, g, rankdata(x.acousticness), rankdata(x.sp_energy), rankdata(x.sp_valence)])[what]; R.append(part(x, x.cs.values, tg, ex))
        out[f"{label}|{tg}"] = dict(mcgill=round(R[0][0], 3), previews=round(R[1][0], 3), pooled=round(pool(R)[0], 3), p=pool(R)[1])
    print(f"{label:46} G: McGill {out[label+'|G']['mcgill']:+.3f} previews {out[label+'|G']['previews']:+.3f} pooled {out[label+'|G']['pooled']:+.3f} (p {out[label+'|G']['p']:.1g})   love {out[label+'|love']['pooled']:+.3f}   covers {out[label+'|cover_rank']['pooled']:+.3f}")
print("\nQ4 inside tempo thirds (five-year bands, genre, peak held), pooled over stores")
for k, nm in enumerate(("slow", "middle", "fast")):
    R = []
    for st in stores:
        x = D[D.store == st].dropna(subset=["cs", "bpm"]).copy(); x = x[pd.qcut(x.bpm, 3, labels=False) == k]; g, y5, tb = dummies(x); R.append(part(x, x.cs.values, "G", [y5, g]))
    print(f"   {nm:7} McGill {R[0][0]:+.3f} (n {R[0][2]})  previews {R[1][0]:+.3f} (n {R[1][2]})  pooled {pool(R)[0]:+.3f} p {pool(R)[1]:.2g}")
print("by era (tempo bands, genre, peak held), pooled")
for lo, hi in ((1958, 1969), (1970, 1979), (1980, 1989), (1990, 2005)):
    R = []
    for st in stores:
        x = D[(D.store == st) & (D.year >= lo) & (D.year <= hi)].dropna(subset=["cs", "bpm"]).copy()
        if len(x) < 60: continue
        g, y5, tb = dummies(x); R.append(part(x, x.cs.values, "G", [rankdata(x.year), tb, g]))
    print(f"   {lo}-{hi}  " + "  ".join(f"{r:+.3f} (n {n})" for r, _, n in R) + f"  pooled {pool(R)[0]:+.3f} p {pool(R)[1]:.2g}")
json.dump(out, open("strata_results.json", "w"), indent=1)
