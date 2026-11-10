"""calibration probe: targets drawn against what the finished builds read (224)."""
import sys, os, random, collections, numpy as np
N = int(sys.argv[1]); sys.argv = [sys.argv[0], "1", "main"]
import melody_p37 as P
P.F["f224"] = os.environ.get("CTL") != "1"
rng = random.Random(7); rows = []; outs = collections.Counter(); errs = collections.Counter()
for _ in range(N):
    c, e = P.generate(rng)
    if e: errs[e] += 1; continue
    r = P.song_read(c["notes"]); t = c["meta"]["targets"]; f = r["feats"]
    rows.append((t, f, r["distance"]))
    for k, *_ in r["outside"]: outs[k] += 1
print("built", len(rows), dict(errs))
for k in P.TARGETS:
    tv = np.array([t[k] for t, f, d in rows]); fv = np.array([f.get(k, np.nan) for t, f, d in rows]); ok = np.isfinite(fv)
    cc = np.corrcoef(tv[ok], fv[ok])[0, 1] if ok.sum() > 3 and tv[ok].std() > 0 else float("nan")
    print(f"{k:28s} target {tv.mean():.3f}  read {np.nanmean(fv):.3f} (5-95 {np.nanpercentile(fv,5):.3f}-{np.nanpercentile(fv,95):.3f})  r {cc:.2f}   chart q25-q75 {P.q(k)}")
d = [x for *_, x in rows]; print("distance", np.percentile(d, [5, 50, 95]).round(3), "too central", np.mean([x < 0.086 for x in d]).round(2))
print("outside both (share of builds):", [(k, round(v / len(rows), 2)) for k, v in outs.most_common(20)])
