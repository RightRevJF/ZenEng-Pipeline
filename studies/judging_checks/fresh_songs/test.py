"""J6b: within-section chord repetition against covers on McGill Billboard songs not among the Hooktheory songs. See PREDICTION.md (committed before the join).
python3 studies/judging_checks/fresh_songs/test.py -> result.json, and studies/judging_data/mcgill_covers_discogs_HOLDOUT.json"""
import os, re, json, collections, numpy as np, statsmodels.api as sm
from scipy.stats import norm as N
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
norm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))
def merge(seq):
    out = []
    for x in seq:
        if not out or out[-1] != x: out.append(x)
    return out
def rep3(seq):
    seen = set(); rep = tot = 0
    for i in range(len(seq) - 2):
        g = tuple(seq[i:i + 3]); tot += 1; rep += g in seen; seen.add(g)
    return rep / tot if tot else None
B = json.load(open(os.path.join(ROOT, "studies", "harmony", "billboard_sections.json"))); songs = []
for s in B:
    seen = set(); num = den = 0.0
    for sec in s["sections"]:
        if sec["letter"] in seen: continue
        seen.add(sec["letter"]); m = merge([r + ("7" if v else "") for b in sec["bars"] for r, v in zip(b["rn"], b["sev"]) if r is not None])
        if len(m) >= 4: num += rep3(m) * len(sec["bars"]); den += len(sec["bars"])
    if den: songs.append(dict(id=s["id"], title=s["title"], artist=s["artist"], rep=num / den, peak=int(s["peak"]) if str(s.get("peak", "")).isdigit() else None))
print(len(B), "charts;", len(songs), "with the measure", flush=True)
# the join (after the measure is fixed above)
Q = json.load(open("/home/claude/shape/discogs_cliques.json")); by = collections.defaultdict(list)
for q in Q: by[q["title"]].append(q)
used = {v["clique"] for v in json.load(open("/home/claude/shape/hooktheory_covers_discogs.json")).values()}; rows = []; dropped = 0
for s in songs:
    a = norm(s["artist"]); cands = [q for q in by.get(norm(s["title"]), []) if a in q["artists"]]
    if not cands: continue
    q = max(cands, key=lambda q: q["n_artist_sets"])
    if q["id"] in used: dropped += 1; continue
    if q["first_year"]: rows.append(dict(s, covers=q["n_artist_sets"] - 1, first_year=q["first_year"], clique=q["id"]))
seen_c = set(); rows = [r for r in rows if not (r["clique"] in seen_c or seen_c.add(r["clique"]))]
def zc(v): v = np.asarray(v, float); return (v - v.mean()) / v.std()
def fit(R, extra=None):
    art = [norm(r["artist"]) for r in R]; codes = {a: i for i, a in enumerate(sorted(set(art)))}; g = np.array([codes[a] for a in art])
    X = [zc([r["rep"] for r in R]), zc([r["first_year"] for r in R])] + ([zc(extra(R))] if extra else [])
    m = sm.OLS(zc(np.log1p([r["covers"] for r in R])), sm.add_constant(np.column_stack(X))).fit(cov_type="cluster", cov_kwds={"groups": g})
    return dict(beta=float(m.params[1]), se=float(m.bse[1]), p=float(m.pvalues[1]), lo=float(m.params[1] - 1.96 * m.bse[1]), hi=float(m.params[1] + 1.96 * m.bse[1]))
t = fit(rows); power = float(N.cdf(0.05 / t["se"] - 1.96) + N.cdf(-0.05 / t["se"] - 1.96))
print(f"matched and fresh: {len(rows)} songs ({dropped} dropped as Hooktheory's groups); power to see -0.05: {power:.2f}", flush=True)
verdict = "holds on fresh songs" if (t["beta"] <= -0.05 and t["hi"] < 0) else "against" if t["beta"] > 0 else "same direction, not settled"
pk = [r for r in rows if r["peak"]]
out = dict(charts=len(B), with_the_measure=len(songs), matched_and_fresh=len(rows), dropped_as_hooktheory_groups=dropped, covers_median=float(np.median([r["covers"] for r in rows])), power_for_minus_0_05=round(power, 2),
           chord_repetition=dict(beta=round(t["beta"], 4), se=round(t["se"], 4), p=round(t["p"], 4), range_95=[round(t["lo"], 3), round(t["hi"], 3)]), verdict=verdict,
           sensitivity=dict(with_chart_peak_held=(lambda r: dict(songs=len(pk), beta=round(r["beta"], 4), p=round(r["p"], 4)))(fit(pk, lambda R: [r["peak"] for r in R])),
                            songs_with_no_cover=int(sum(r["covers"] == 0 for r in rows))))
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1)
json.dump(dict(HOLD_OUT="These cover counts are a hold-out. They were joined once, on 22 November 2026, for one test whose rule was committed first (studies/judging_checks/fresh_songs). Do not explore on them: no new measure may be tried against them until its rule is written and committed, and each such test should be counted. Otherwise they stop being fresh.",
               source="McGill Billboard charts (studies/harmony/billboard_sections.json) matched to Discogs-VI 20240701 groups (CC BY-SA 4.0) by title and artist; groups any Hooktheory song matched are left out", made_by="studies/judging_checks/fresh_songs/test.py",
               songs=[dict(mcgill_id=r["id"], title=r["title"], artist=r["artist"], discogs_group=r["clique"], covers=r["covers"], first_year=r["first_year"]) for r in rows]), open(os.path.join(ROOT, "studies", "judging_data", "mcgill_covers_discogs_HOLDOUT.json"), "w"), indent=0)
