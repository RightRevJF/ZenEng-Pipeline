"""Where in the song each curve peaks: harmonic tension (Lerdahl distance from the tonic, 24-second memory), melodic height, loudness and
listeners' arousal (8-second memory), on a normalised time axis, in the CoCoPops songs. Reports the median position of each smoothed
curve's highest point, and the mean curve in tenths."""
import json, numpy as np
F = json.load(open("cocopops_features.json"))
def ema(v, sec, tau):
    out = np.empty_like(v); acc = v[0]
    for i in range(len(v)):
        a = np.exp(-sec[i] / tau); acc = a * acc + (1 - a) * v[i]; out[i] = acc
    return out
peaks = {"tps_tonic": [], "pitch": [], "rms": [], "arousal": []}; curves = {f: [] for f in peaks}
for k, s in F.items():
    bars = s["bars"]
    if len(bars) < 30: continue
    sec = np.array([b["sec"] if b["sec"] and 0.5 < b["sec"] < 8 else np.nan for b in bars]); sec = np.where(np.isnan(sec), np.nanmedian(sec) if np.any(np.isfinite(sec)) else 2.0, sec)
    t = np.cumsum(sec) / sec.sum()
    for f, tau in (("tps_tonic", 24), ("pitch", 8), ("rms", 8), ("arousal", 8)):
        v = np.array([b.get(f) if b.get(f) is not None else np.nan for b in bars], float)
        if np.sum(np.isfinite(v)) < 20: continue
        if f == "pitch":
            last = np.nanmean(v)
            for i in range(len(v)):
                if np.isnan(v[i]): v[i] = last
                else: last = v[i]
        v = np.where(np.isnan(v), np.nanmean(v), v)
        sm = ema((v - v.mean()) / (v.std() or 1), sec, tau)
        lo = int(0.1 * len(sm))                       # skip the first tenth while the memory fills
        i = lo + int(np.argmax(sm[lo:])); peaks[f].append(float(t[i]))
        curves[f].append([float(np.mean(sm[(t > a) & (t <= a + 0.1)])) if np.any((t > a) & (t <= a + 0.1)) else np.nan for a in np.arange(0, 1, 0.1)])
out = {}
for f in peaks:
    c = np.nanmean(np.array(curves[f]), 0)
    out[f] = dict(songs=len(peaks[f]), median_peak=round(float(np.median(peaks[f])), 3), iqr=[round(float(np.percentile(peaks[f], 25)), 2), round(float(np.percentile(peaks[f], 75)), 2)],
                  mean_curve_tenths=[round(float(x), 2) for x in c])
    print(f, out[f])
json.dump(out, open("profile_results.json", "w"), indent=1)
