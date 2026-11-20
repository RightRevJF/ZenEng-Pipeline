import re, importlib.util, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy.stats import rankdata, pearsonr, norm as Nm
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)|feat.*$|featuring.*$", "", str(s).lower().replace("&", "and")))
sp = importlib.util.spec_from_file_location("c", "/home/claude/arena/candidates/sound.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); fn = {c["name"]: c["fn"] for c in m.CANDIDATES}["concentrated_spectrum"]
D = pd.concat([pd.read_pickle("/home/claude/arena/sound_open.pkl"), pd.read_pickle("/home/claude/arena_locked/sound_locked.pkl")], ignore_index=True); D["cs"] = np.asarray(fn(D.copy()), float)
S = pd.read_excel("/home/claude/corpus/try2/tidytuesday/data/2021/2021-09-14/Hot 100 Audio Features.xlsx").dropna(subset=["spotify_track_popularity"]); S["t"] = S.Song.map(norm); S["a"] = S.Performer.map(norm); S = S.sort_values("spotify_track_popularity", ascending=False).drop_duplicates(["t", "a"]); D = D.merge(S[["t", "a", "spotify_genre", "instrumentalness", "speechiness"]], on=["t", "a"], how="left")
FAM = [r"rock|metal|punk|grunge", r"soul|motown|r&b|funk|disco|quiet storm", r"country|nashville", r"hip hop|rap", r"folk|singer-songwriter", r"adult standards|easy listening|lounge|vocal jazz|brill", r"dance|new wave|synth|europop"]
PROX = ["pitch_salience.mean", "onset_rate", "beats_loudness.mean", "hfc.mean", "spectral_flux.mean", "zerocrossingrate.mean"]; print("proxies present:", [p for p in PROX if p in D.columns])
def run(tg, extra_cols, sub=None):
    R = []
    for st in ("mcgill_whole_recordings", "msd_previews"):
        x = D[D.store == st].dropna(subset=["cs"] + [c for c in extra_cols if c in D.columns]).copy()
        if sub is not None: x = x[sub(x)]
        g = np.array([[float(bool(re.search(p, str(v)))) for p in FAM] for v in x.spotify_genre]); y5 = pd.get_dummies((x.year // 5).astype(int)).values[:, 1:].astype(float)
        C = np.c_[tuple([np.ones(len(x)), rankdata(x.peak), y5, g] + [rankdata(x[c]) for c in extra_cols if c in x.columns])]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; r, p = pearsonr(res(rankdata(x.cs)), res(rankdata(x[tg]))); R.append((float(r), float(p), len(x)))
    z = sum(np.sign(r) * Nm.isf(p / 2) * np.sqrt(n) for r, p, n in R) / np.sqrt(sum(n for _, _, n in R)); return round(R[0][0], 3), round(R[1][0], 3), round(sum(r * n for r, _, n in R) / sum(n for _, _, n in R), 3), float(2 * Nm.sf(abs(z)))
out = {}
for label, cols in (("peak, five-year band, genre", []), ("+ pitch salience (how pitched and voice-like)", ["pitch_salience.mean"]), ("+ onset rate, beat loudness (how percussive)", ["onset_rate", "beats_loudness.mean"]), ("+ high-frequency content, flux, zero crossings", ["hfc.mean", "spectral_flux.mean", "zerocrossingrate.mean"]), ("ALL six held (T1)", PROX), ("ALL six + Spotify instrumentalness, speechiness", PROX + ["instrumentalness", "speechiness"])):
    out[label] = run("G", cols); print(f"{label:52} whole {out[label][0]:+.3f}  previews {out[label][1]:+.3f}  pooled {out[label][2]:+.3f} (p {out[label][3]:.1g})")
print("the stand-ins themselves against the yardstick (peak, band, genre held), pooled:")
for c in PROX:
    D["_"] = D["cs"]; D["cs"] = D[c]; r = run("G", []); D["cs"] = D["_"]; print(f"   {c:26} {r[2]:+.3f} (p {r[3]:.1g})")
json.dump(out, open("t1_results.json", "w"), indent=1)
