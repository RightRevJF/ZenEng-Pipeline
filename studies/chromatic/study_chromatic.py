"""Does harmony that lives outside the key go with views or with covers? Hooktheory songs (clips averaged per song, weighted by
chord events; clips with a key change left out), against three outcomes, with the controls of the earlier studies:
- views: log YouTube views (10,8xx songs); controls log subscribers, age, duration, music category, clips, events; across songs
  and within artist (songs by the same artist, demeaned).
- covers (Discogs-VI): log(1+covers); controls as above plus log views and the first release year (song age).
- covers (SHS100K): log versions; controls as above plus log views and whether the artist is the first performer.
Measure sets, each tested alone over the controls and again with the earlier note measures (melody and chord surprise,
uncertainty, Cheung terms, repetition) added as controls:
  A  chrom_mm (share of chord time outside plain major/minor) and its square (a sweet spot?)
  B  the kinds: mixture, applied dominants, other chromatic (shares of chord events)
  C  lives: share of the song's sections with two or more chromatic chord events
Standardised betas, artist-clustered errors. Writes chromatic_results.json."""
import json, collections, re, datetime, sys
import numpy as np, statsmodels.api as sm
S = json.load(open("/home/claude/shape/hooktheory_surprise.json")); CH = json.load(open("/home/claude/shape/hooktheory_chromatic.json"))
Y = json.load(open("/home/claude/dl/shape/youtube/hooktheory_youtube.json")); V, C = Y["videos"], Y["channels"]
FE = ["mel_ic_mean", "mel_h_mean", "mel_cheung", "ch_ic_mean", "ch_h_mean", "ch_cheung", "mel_rep", "ch_rep"]
CF = ["chrom_mm", "chrom", "mixture", "secdom", "other_chrom", "lives", "distinct_chrom"]
by = collections.defaultdict(list)
for c in S:
    h = CH.get(c["k"])
    if h and h["nkeys"] == 1: by[c["vid"]].append(dict(c, **h))
def dur_s(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or ""); return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else np.nan
def song_rows():
    rows = []
    for vid, cs in by.items():
        v = V.get(vid)
        if not v or not v["views"]: continue
        sub = (C.get(v["channel"]) or {}).get("subscribers")
        if not sub: continue
        w = np.array([c["n_ev"] for c in cs], float); wm = np.array([float(c["n_mel"]) for c in cs])
        r = {f: float(np.average([float(c[f]) for c in cs], weights=wm)) for f in FE}
        r.update({f: float(np.average([c[f] for c in cs], weights=w)) for f in CF if f not in ("lives", "distinct_chrom")})
        r["lives"] = float(np.mean([c["lives"] for c in cs])); r["distinct_chrom"] = float(len({0}) * 0 + np.mean([c["distinct_chrom"] for c in cs]))
        pub = datetime.datetime.fromisoformat(v["published"].replace("Z", "+00:00"))
        r.update(vid=vid, artist=cs[0]["artist"], views=v["views"], subs=sub, age=(datetime.datetime(2026, 11, 15, tzinfo=datetime.timezone.utc) - pub).days,
                 dur=dur_s(v["duration"]), music=1.0 if v["category"] == "10" else 0.0, nclips=len(cs), nev=float(w.sum()), major=float(np.mean([c["major"] for c in cs])))
        rows.append(r)
    return [r for r in rows if r["age"] > 30 and np.isfinite(r["dur"]) and r["dur"] > 0]
def zc(M): M = np.asarray(M, float); s = M.std(0); s[s == 0] = 1; return (M - M.mean(0)) / s
SETS = {"A_share": ["chrom_mm", "chrom_mm^2"], "B_kinds": ["mixture", "secdom", "other_chrom"], "C_lives": ["lives"]}
def design(rows, names):
    cols = []
    for nm in names:
        if nm.endswith("^2"): x = np.array([r[nm[:-2]] for r in rows]); x = (x - x.mean()) / x.std(); cols.append(x ** 2)
        else: cols.append(np.array([r[nm] for r in rows], float))
    return zc(np.column_stack(cols))
def fit(y, ctrl, P, names, g):
    yz = (y - y.mean()) / y.std(); A0 = sm.add_constant(zc(ctrl)); A1 = sm.add_constant(np.column_stack([zc(ctrl), P]))
    m0 = sm.OLS(yz, A0).fit(); m1 = sm.OLS(yz, A1).fit(); mr = sm.OLS(yz, A1).fit(cov_type="cluster", cov_kwds={"groups": g}); k = ctrl.shape[1]
    return dict(n=len(y), delta_r2=float(m1.rsquared - m0.rsquared), f_p=float(m1.compare_f_test(m0)[1]),
                terms={nm: dict(beta=float(mr.params[1 + k + i]), p=float(mr.pvalues[1 + k + i])) for i, nm in enumerate(names)})
def demean(M, g):
    M = np.asarray(M, float).copy()
    for a in np.unique(g):
        s = g == a; M[s] = M[s] - M[s].mean(0)
    return M
def run(rows, y, base, label, within=False):
    art = np.array([r["artist"] for r in rows]); codes = {a: i for i, a in enumerate(sorted(set(art)))}; g = np.array([codes[a] for a in art])
    notes = np.column_stack([[r[f] for r in rows] for f in FE]); out = {}
    for sname, names in SETS.items():
        P = design(rows, names)
        for ctl_name, ctl in (("controls", base), ("controls+notes", np.column_stack([base, notes]))):
            yy, cc, PP, gg = y, ctl, P, g
            if within:
                cnt = collections.Counter(art); keep = np.array([cnt[a] >= 2 for a in art])
                yy, cc, PP, gg = demean(y[keep], g[keep]), demean(ctl[keep], g[keep]), demean(P[keep], g[keep]), g[keep]
            out[f"{sname}|{ctl_name}"] = fit(yy, cc, PP, names, gg)
    return out
if __name__ == "__main__":
    rows = song_rows(); res = {}
    base = lambda R: np.column_stack([np.log([r["subs"] for r in R]), np.log([r["age"] for r in R]), np.log([r["dur"] for r in R]), [r["music"] for r in R],
                                      np.log([r["nclips"] for r in R]), np.log([r["nev"] for r in R]), [r["major"] for r in R]])
    y = np.log([r["views"] for r in rows])
    res["views_across"] = run(rows, y, base(rows), "views"); res["views_within_artist"] = run(rows, y, base(rows), "views", within=True)
    for name, path, cfield in (("covers_discogs", "hooktheory_covers_discogs.json", "covers"), ("covers_shs", "hooktheory_covers.json", "versions")):
        COV = json.load(open("/home/claude/shape/" + path)); R = [r for r in rows if r["vid"] in COV]
        if name == "covers_discogs":
            R = [r for r in R if COV[r["vid"]].get("first_year")]; extra = np.array([[COV[r["vid"]]["first_year"]] for r in R], float); yc = np.log1p([COV[r["vid"]][cfield] for r in R])
        else:
            extra = np.array([[float(COV[r["vid"]]["artist_is_first"])] for r in R]); yc = np.log([COV[r["vid"]][cfield] for r in R])
        b = np.column_stack([base(R), np.log([r["views"] for r in R]), extra]); res[name] = run(R, yc, b, name)
    D = {f: dict(mean=float(np.mean([r[f] for r in rows])), median=float(np.median([r[f] for r in rows])), p75=float(np.percentile([r[f] for r in rows], 75)), p90=float(np.percentile([r[f] for r in rows], 90))) for f in CF}
    res["descr"] = dict(songs=len(rows), measures=D)
    json.dump(res, open("/home/claude/shape/chromatic_results.json", "w"), indent=1)
    print("songs", len(rows))
    for f, d in D.items(): print("  %-14s mean %.3f median %.3f p75 %.3f p90 %.3f" % (f, d["mean"], d["median"], d["p75"], d["p90"]))
    for outc in ("views_across", "views_within_artist", "covers_discogs", "covers_shs"):
        print("==", outc)
        for k, v in res[outc].items():
            print("  %-28s n %5d dR2 %.4f p %.3g | " % (k, v["n"], v["delta_r2"], v["f_p"]) + "  ".join("%s %+.3f (p %.3f)" % (t, x["beta"], x["p"]) for t, x in v["terms"].items()))
