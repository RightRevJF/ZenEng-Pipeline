"""A small outcome check: the 20 songs Hooked on Music players recognised fastest (published in November 2014; percentiles by mid-rank, 12,000+ players;
list as reported by the Christian Science Monitor) against every other Hooktheory song. Each matched song's chorus clips are placed
as percentiles of all chorus clips on the hook features, and a sign test asks whether the fast-recognised choruses sit above or
below the median more often than chance."""
import gzip, json, re
import numpy as np
from scipy import stats
FAST = [("spice-girls", "wannabe"), ("lou-bega", "mambo-no-5"), ("survivor", "eye-of-the-tiger"), ("lady-gaga", "just-dance"), ("abba", "sos"),
        ("roy-orbison", "oh-pretty-woman"), ("michael-jackson", "beat-it"), ("whitney-houston", "i-will-always-love-you"), ("the-human-league", "dont-you-want-me"),
        ("aerosmith", "i-dont-want-to-miss-a-thing"), ("lady-gaga", "poker-face"), ("hanson", "mmmbop"), ("elvis-presley", "its-now-or-never"),
        ("bachman-turner-overdrive", "you-aint-seen-nothing-yet"), ("michael-jackson", "billie-jean"), ("culture-club", "karma-chameleon"),
        ("britney-spears", "baby-one-more-time"), ("elvis-presley", "devil-in-disguise"), ("boney-m", "rivers-of-babylon"), ("elton-john", "candle-in-the-wind")]
D = json.load(gzip.open("/home/claude/zeneng-pipeline/studies/hooks/hooks_clips.json.gz", "rt"))
def slug(s): return re.sub(r"[^a-z0-9]", "", s.lower())
songs = {}
for r in D: songs.setdefault(r["song"], []).append(r)
found = {}
for a, t in FAST:
    for s in songs:
        ar, so = s.split("/", 1)
        if slug(ar) in (slug(a), slug(a.replace("the-", ""))) and (slug(so) == slug(t) or slug(so).startswith(slug(t)) or slug(t).startswith(slug(so))):
            found[(a, t)] = s
print(len(found), "of 20 found:", sorted(found.values()))
F = ["recurrence", "convention", "ic_mean", "i_entropy", "top_cell_cover", "mean_pitch", "density", "up_rhythm"]
ch = [r for r in D if r["section"] == "chorus"]
res = dict(found=len(found), songs=sorted(found.values()), features={})
for f in F:
    allv = np.array([r[f] for r in ch if r[f] is not None], float)
    pct = []
    for s in found.values():
        v = [r[f] for r in songs[s] if r["section"] == "chorus" and r[f] is not None]
        if v: m = float(np.mean(v)); pct.append(float(((allv < m).mean() + 0.5 * (allv == m).mean()) * 100))
    above = sum(p > 50 for p in pct); n = len(pct)
    res["features"][f] = dict(n=n, median_pct=round(float(np.median(pct)), 1) if pct else None, above=above, p=stats.binomtest(above, n).pvalue if n else None)
    print("%-15s n %2d  median percentile %5.1f  above median %2d  p %.3f" % (f, n, res["features"][f]["median_pct"] or 0, above, res["features"][f]["p"] or 1))
json.dump(res, open("/home/claude/zeneng-pipeline/studies/hooks/hooks_catchiest_results.json", "w"), indent=1)
