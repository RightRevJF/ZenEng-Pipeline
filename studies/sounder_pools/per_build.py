"""749.140: rhythm scaling under the kept 10th, read per build, with and without the planted peak. See PREDICTION2.md.
python3 studies/sounder_pools/per_build.py with.json without.json -> per_build.json"""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); A = json.load(open(sys.argv[1]))["749.140"]; B = json.load(open(sys.argv[2]))["749.140"]; k10 = A["kept_10th_25th_75th"][0]; rng = np.random.default_rng(140); out = dict(kept_10th=k10)
for where in ("pools", "living"):
    songs = list(A[where]); a = {s: np.array(A[where][s]) < k10 for s in songs}; b = {s: np.array(B[where][s]) < k10 for s in songs}
    sh = lambda d: float(np.mean(np.concatenate([d[s] for s in songs]))); gap = sh(b) - sh(a); big = 0
    for _ in range(10000):
        pa, pb = {}, {}
        for s in songs:
            z = rng.permutation(np.concatenate([a[s], b[s]])); pa[s] = z[:len(a[s])]; pb[s] = z[len(a[s]):]
        big += abs(sh(pb) - sh(pa)) >= abs(gap)
    out[where] = dict(builds_with_the_peak=int(sum(len(a[s]) for s in songs)), builds_without=int(sum(len(b[s]) for s in songs)), under_the_kept_10th_with=round(sh(a), 3), under_the_kept_10th_without=round(sh(b), 3), gap=round(gap, 3), shuffles_as_large=round(big / 10000, 4),
                      by_song={s: [round(float(a[s].mean()), 3), round(float(b[s].mean()), 3)] for s in songs})
out["pool_spread_over_kept_spread"] = dict(with_the_peak=A["pool_spread_over_kept_spread"], without=B["pool_spread_over_kept_spread"])
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(HERE, "per_build.json"), "w"), indent=1)
