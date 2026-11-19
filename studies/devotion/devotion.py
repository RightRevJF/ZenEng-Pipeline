import sys, re, json, hashlib, numpy as np, pandas as pd, pyarrow.parquet as pq, warnings; warnings.filterwarnings("ignore")
from scipy.stats import rankdata, pearsonr
from sklearn.linear_model import RidgeCV; from sklearn.preprocessing import StandardScaler
which = sys.argv[1]; P = "/tmp/claude-0/hspd/"; f = pq.ParquetFile(P + ("hsp-s_essentia.parquet" if which == "S" else "hsp-l_acousticbrainz.parquet")); n = f.schema.names
means = [c for c in n if re.match(r"(lowlevel|rhythm|tonal)\.", c) and (c.endswith(".mean") or c.count(".") == 1) and "histogram" not in c.split(".")[1] or c in ("rhythm.bpm_histogram_first_peak_weight.mean",)]
means = [c for c in dict.fromkeys(means) if str(f.schema_arrow.field(c).type) in ("double", "float", "int64", "int32")]
hl = [c for c in n if re.match(r"highlevel\.(mood_\w+|danceability|voice_instrumental|gender|timbre|tonal_atonal)\.all\.", c)]
d = f.read(columns=means + hl + ["uuid", "lastfm_listener_count", "lastfm_playcount"] + [c for c in n if c in ("highlevel.genre_dortmund.value", "highlevel.genre_rosamerica.value")] + (["peakPos"] if "peakPos" in n else [])).to_pandas(); d.columns = [re.sub(r"^(lowlevel|rhythm|tonal)\.", "", c) for c in d.columns]
y = pd.read_csv(P + f"hsp-{which.lower()}_uuid_year.csv")[["uuid", "year"]]; d = d.merge(y, on="uuid").drop_duplicates("uuid"); d = d[(d.lastfm_listener_count >= 50) & (d.lastfm_playcount > 0) & (d.year > 1900)].reset_index(drop=True)
d["breadth"] = np.log(d.lastfm_listener_count); d["ppl"] = np.log(d.lastfm_playcount) - d.breadth; d["half"] = [int(hashlib.md5(u.encode()).hexdigest(), 16) % 2 for u in d.uuid]
F = [c for c in d.columns if c.endswith(".mean") or c in ("average_loudness", "dynamic_complexity", "bpm", "danceability", "onset_rate", "chords_changes_rate", "chords_number_rate", "key_strength", "tuning_diatonic_strength", "tuning_equal_tempered_deviation", "tuning_nontempered_energy_ratio")]; F = [c for c in F if d[c].notna().mean() > .95 and d[c].std() > 0 and not c.startswith("highlevel")]
GEN = None
def part(mask, v, tg, hold):
    x = d[mask]; C = np.c_[tuple([np.ones(len(x))] + [rankdata(x[h]) for h in hold] + ([GEN[mask]] if GEN is not None else []))]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; r, p = pearsonr(res(rankdata(v)), res(rankdata(x[tg]))); return round(float(r), 3), float(p)
GEN = np.c_[pd.get_dummies(d["highlevel.genre_dortmund.value"]).values[:, 1:].astype(float), pd.get_dummies(d["highlevel.genre_rosamerica.value"]).values[:, 1:].astype(float)] if len(sys.argv) > 2 else None
A = np.ones(len(d), bool); HD = ["year", "breadth"]; HB = ["year"]; rk = lambda c: rankdata(d[c]) / len(d)
d["cs"] = (rk("melbands_flatness_db.mean") + rk("barkbands_kurtosis.mean") + rk("barkbands_skewness.mean") + rk("melbands_crest.mean") - rk("melbands_spread.mean") - rk("spectral_centroid.mean")) / 6
print(f"HSP-{which}: tracks {len(d)}, sound means {len(F)}; plays per listener median {np.exp(d.ppl.median()):.2f}; devotion vs breadth (year held) {part(A, d.ppl.values, 'breadth', HB)[0]:+.3f}"); out = {}
out["D1 concentrated_spectrum"] = dict(devotion=part(A, d.cs.values, "ppl", HD), breadth=part(A, d.cs.values, "breadth", HB), half0=part((d.half == 0).values, d.cs.values[(d.half == 0).values], "ppl", HD), half1=part((d.half == 1).values, d.cs.values[(d.half == 1).values], "ppl", HD)); print("D1", out["D1 concentrated_spectrum"])
for c in hl:
    nm = c.replace("highlevel.", "").replace(".all.", ":"); out[nm] = dict(devotion=part(A, d[c].fillna(d[c].median()).values, "ppl", HD), breadth=part(A, d[c].fillna(d[c].median()).values, "breadth", HB))
keep = [k for k in out if ":" in k and not k.split(":")[1].startswith("not_")]; print("D2 and the other classifiers (devotion | breadth):"); [print(f"   {k:34} {out[k]['devotion'][0]:+.3f} (p {out[k]['devotion'][1]:.1g}) | {out[k]['breadth'][0]:+.3f}") for k in sorted(keep, key=lambda k: -abs(out[k]['devotion'][0]))[:16]]
X = d[F].fillna(d[F].median()).values
for tg, hold in (("ppl", HD), ("breadth", HB)):
    pr = np.zeros(len(d))
    for h in (0, 1):
        a, b = (d.half != h).values, (d.half == h).values; sc = StandardScaler().fit(X[a]); C = np.c_[np.ones(a.sum())] ; pr[b] = RidgeCV(alphas=np.logspace(0, 5, 16)).fit(sc.transform(X[a]), d[tg].values[a]).predict(sc.transform(X[b]))
    out["D3 reader for " + tg] = dict(all=part(A, pr, tg, hold), half0=part((d.half == 0).values, pr[(d.half == 0).values], tg, hold), half1=part((d.half == 1).values, pr[(d.half == 1).values], tg, hold)); print("D3 reader for", "devotion" if tg == "ppl" else "breadth", out["D3 reader for " + tg])
L = []
for c in F:
    a, b = part((d.half == 0).values, d[c].fillna(d[c].median()).values[(d.half == 0).values], "ppl", HD), part((d.half == 1).values, d[c].fillna(d[c].median()).values[(d.half == 1).values], "ppl", HD)
    if np.sign(a[0]) == np.sign(b[0]): L.append((c, part(A, d[c].fillna(d[c].median()).values, "ppl", HD)[0], part(A, d[c].fillna(d[c].median()).values, "breadth", HB)[0]))
L.sort(key=lambda x: -abs(x[1])); print("single readings, devotion | breadth (same sign in both halves for devotion):"); [print(f"   {c:36} {a:+.3f} | {b:+.3f}") for c, a, b in L[:14]]; out["leads"] = L[:20]
if "peakPos" in d: 
    for nm, mk in (("hits", d.peakPos.notna().values), ("never charted", d.peakPos.isna().values)): print(f"   D1 among {nm} ({int(mk.sum())}): devotion {part(mk, d.cs.values[mk], 'ppl', HD)[0]:+.3f}  breadth {part(mk, d.cs.values[mk], 'breadth', HB)[0]:+.3f}")
json.dump(out, open(f"devotion_{which}{'_genre' if GEN is not None else ''}.json", "w"), indent=1, default=float)
