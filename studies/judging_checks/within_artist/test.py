"""R02-1: chord repetition within a section against covers, within each artist's own songs. See PREDICTION.md (written before the outcome was joined).
Rows are built exactly as studies/covers/study_covers_discogs.py builds them. python3 studies/judging_checks/within_artist/test.py -> result.json"""
import json, collections, re, datetime, hashlib, os
import numpy as np, statsmodels.api as sm
from scipy.stats import norm as N
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open("/home/claude/shape/hooktheory_surprise.json")); RH = {r["k"]: r for r in json.load(open("/home/claude/shape/hooktheory_rhythm.json"))}
Y = json.load(open("/home/claude/dl/shape/youtube/hooktheory_youtube.json")); V, C = Y["videos"], Y["channels"]
COV = json.load(open("/home/claude/shape/hooktheory_covers_discogs.json"))
RF = ["rhy_ic_mean", "rhy_h_mean", "rhy_cheung", "sync_per_note", "rest_share", "phrase_mean", "phrase_on_downbeat", "density", "length_variety"]
FE = ["mel_ic_mean", "mel_h_mean", "mel_cheung", "ch_ic_mean", "ch_h_mean", "ch_cheung", "mel_rep", "ch_rep"] + RF
by = collections.defaultdict(list)
for c in S:
    if c["k"] in RH: by[c["vid"]].append(dict(c, **{f: RH[c["k"]][f] for f in RF}))
def dur_s(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or ""); return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else np.nan
rows = []
for vid, cv in COV.items():
    cs = by.get(vid); v = V.get(vid)
    if not cs or not v or not v["views"]: continue
    sub = (C.get(v["channel"]) or {}).get("subscribers") or 1
    w = np.array([c["n_mel"] for c in cs], float); r = {f: float(np.average([c[f] for c in cs], weights=w)) for f in FE}
    pub = datetime.datetime.fromisoformat(v["published"].replace("Z", "+00:00"))
    r.update(vid=vid, artist=cs[0]["artist"], covers=cv["covers"], first_year=cv["first_year"], clique=cv["clique"], views=v["views"], subs=sub,
             age=max(31, (datetime.datetime(2026, 11, 15, tzinfo=datetime.timezone.utc) - pub).days), dur=dur_s(v["duration"]), music=1.0 if v["category"] == "10" else 0.0, nclips=len(cs))
    rows.append(r)
rows = [r for r in rows if np.isfinite(r["dur"]) and r["dur"] > 0 and r["first_year"]]
# covers by period (R02-2's table): the other artists' versions, by the year of each one's earliest release
want = {r["clique"] for r in rows}; VER = {}
for line in open("/home/claude/shape/discogs_versions.jsonl"):
    d = json.loads(line)
    if d["id"] in want: VER[d["id"]] = d["sets"]
norm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))
for r in rows:
    a = norm(r["artist"]); oth = [y for names, y, _ in VER[r["clique"]] if a not in names]; r["others"] = len(oth)
    r["early"] = sum(1 for y in oth if y is not None and y <= r["first_year"] + 5); r["late"] = sum(1 for y in oth if y is not None and y > r["first_year"] + 10); r["undated"] = sum(1 for y in oth if y is None)
cnt = collections.Counter(r["artist"] for r in rows); sub = [r for r in rows if cnt[r["artist"]] >= 2]
def zc(M): M = np.asarray(M, float); s = np.atleast_1d(M.std(0)).copy(); s[s == 0] = 1; return (M - M.mean(0)) / (s if M.ndim > 1 else s[0])
def within(R, yname, feats, ctrl):
    """artist fixed effects by demeaning; y and every column standardised over R first, so a coefficient is in SDs of y per SD of the measure, as in the covers study"""
    art = np.array([r["artist"] for r in R]); codes = {a: i for i, a in enumerate(sorted(set(art)))}; g = np.array([codes[a] for a in art])
    y = zc(np.log1p([r[yname] for r in R])); X = zc(np.column_stack([[r[f] for r in R] for f in feats] + [ctrl(R)]))
    def dm(M):
        M = np.array(M, float).reshape(len(R), -1); out = M.copy()
        for k in range(len(codes)): out[g == k] -= M[g == k].mean(0)
        return out
    m = sm.OLS(dm(y).ravel(), dm(X)).fit(cov_type="cluster", cov_kwds={"groups": g, "df_correction": True})
    return {f: dict(beta=float(m.params[i]), se=float(m.bse[i]), p=float(m.pvalues[i])) for i, f in enumerate(feats)}, len(R), len(codes)
plain = lambda R: np.column_stack([[r["first_year"] for r in R], np.log([r["views"] for r in R])])
full = lambda R: np.column_stack([np.log([r["subs"] for r in R]), np.log([r["age"] for r in R]), np.log([r["dur"] for r in R]), [r["music"] for r in R], np.log([r["nclips"] for r in R]), [r["first_year"] for r in R], np.log([r["views"] for r in R])])
half = lambda r: int(hashlib.md5(r["artist"].encode()).hexdigest(), 16) % 2
main, n, na = within(sub, "covers", ["ch_rep"], plain); t = main["ch_rep"]; power = float(N.cdf(0.04 / t["se"] - 1.96) + N.cdf(-0.04 / t["se"] - 1.96))
print(f"rows {len(rows)}; artists with two or more songs: {na} artists, {n} songs; power to see -0.04 at .05: {power:.2f}", flush=True)
H = {h: within([r for r in sub if half(r) == h], "covers", ["ch_rep"], plain) for h in (0, 1)}
b = t["beta"]; same = (H[0][0]["ch_rep"]["beta"] < 0) == (H[1][0]["ch_rep"]["beta"] < 0) == (b < 0)
verdict = "holds" if (b <= -0.04 and t["p"] < 0.05 and same) else "belongs to performers, eras or genres" if b > -0.02 else "unsettled"
out = dict(rows=len(rows), between_artists_committed=-0.0715, songs=n, artists=na, power_for_minus_0_04=round(power, 2), within_artist=dict(beta=round(b, 4), se=round(t["se"], 4), p=round(t["p"], 4)),
           halves=[dict(songs=H[h][1], artists=H[h][2], beta=round(H[h][0]["ch_rep"]["beta"], 4), p=round(H[h][0]["ch_rep"]["p"], 4)) for h in (0, 1)], verdict=verdict)
def one(yname, ctrl=plain, feats=("ch_rep",)): r_, n_, a_ = within(sub, yname, list(feats), ctrl); return {f: dict(beta=round(v["beta"], 4), p=round(v["p"], 4)) for f, v in r_.items()}
out["deciding_nothing"] = dict(covers_within_five_years=one("early")["ch_rep"], covers_after_ten_years=one("late")["ch_rep"], all_other_artists_versions=one("others")["ch_rep"],
                               median_early_late_undated=[float(np.median([r[k] for r in sub])) for k in ("early", "late", "undated")],
                               full_controls_with_the_artist_held=one("covers", full)["ch_rep"], every_measure_one_at_a_time={f: one("covers", plain, (f,))[f] for f in FE},
                               every_measure_together_full_controls=one("covers", full, FE),
                               songs_per_artist_quartiles=[float(x) for x in np.percentile([c for c in cnt.values() if c >= 2], (25, 50, 75))],
                               artists_with_five_or_more=dict(zip(("beta", "p"), (lambda r_: (round(r_[0]["ch_rep"]["beta"], 4), round(r_[0]["ch_rep"]["p"], 4)))(within([r for r in sub if cnt[r["artist"]] >= 5], "covers", ["ch_rep"], plain)))))
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1)
