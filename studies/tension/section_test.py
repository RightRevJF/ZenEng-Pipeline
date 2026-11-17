"""Tension readings by section role and at the approach to a chorus, in the 214 CoCoPops songs (all with melody), and the listeners'
arousal where rated; plus how far the listeners agree (the ceiling for any model). Values are z-scored within song."""
import json, re, numpy as np, collections
F = json.load(open("cocopops_features.json")); S = json.load(open("cocopops_bars.json"))
def role(l):
    l = (l or "").lower()
    if "pre" in l and "chorus" in l: return "pre-chorus"
    for r in ("chorus", "verse", "bridge", "intro", "outro", "solo", "interlude"):
        if r in l: return r
    return "other"
FE = ["tps_tonic", "tps_seq", "diss", "dom_bar", "tonic_bar", "pitch", "onset_rate", "nct", "rms", "arousal"]
acc = collections.defaultdict(lambda: collections.defaultdict(list)); appr = collections.defaultdict(list); first = collections.defaultdict(list)
for k, s in F.items():
    bars = s["bars"]; Z = {}
    for f in FE:
        v = np.array([b.get(f) if b.get(f) is not None else np.nan for b in bars], float)
        if np.sum(np.isfinite(v)) < 10 or np.nanstd(v) == 0: continue
        Z[f] = (v - np.nanmean(v)) / np.nanstd(v)
    R = [role(b["label"]) for b in bars]
    for i, r in enumerate(R):
        for f, z in Z.items():
            if np.isfinite(z[i]): acc[r][f].append(z[i])
    # the two bars before each chorus starts, and the chorus's first bar
    for i in range(2, len(R)):
        if R[i] == "chorus" and R[i - 1] != "chorus":
            for f, z in Z.items():
                for d, tag in ((-2, "two bars before"), (-1, "last bar before"), (0, "chorus bar 1")):
                    if np.isfinite(z[i + d]): appr[(tag, f)].append(z[i + d])
out = dict(by_role={}, approach={})
print(f"{'role':11s} " + " ".join(f"{f[:9]:>9s}" for f in FE) + "   bars")
for r in ["intro", "verse", "pre-chorus", "chorus", "bridge", "solo", "outro"]:
    row = {f: round(float(np.mean(acc[r][f])), 2) if acc[r][f] else None for f in FE}; n = len(acc[r]["pitch"]) or len(acc[r]["tps_tonic"])
    out["by_role"][r] = dict(row, n_bars=n)
    print(f"{r:11s} " + " ".join(f"{row[f]:+9.2f}" if row[f] is not None else f"{'':>9s}" for f in FE) + f"  {n}")
for tag in ("two bars before", "last bar before", "chorus bar 1"):
    row = {f: round(float(np.mean(appr[(tag, f)])), 2) if appr[(tag, f)] else None for f in FE}
    out["approach"][tag] = row; print(f"{tag:15s}", {f: row[f] for f in ("tps_tonic", "dom_bar", "tonic_bar", "pitch", "rms", "arousal")})
# the listeners' agreement: within-song split-half (raters 1+2 against 3+4), Spearman-Brown corrected
rel = []
for k, s in S.items():
    if not s["varms"]: continue
    a, b = [], []
    for bar in s["bars"]:
        rows = [x for x in bar["ar"] if len(x) == 4]
        if rows: m = np.mean(rows, 0); a.append((m[0] + m[1]) / 2); b.append((m[2] + m[3]) / 2)
    if len(a) > 20 and np.std(a) > 0 and np.std(b) > 0:
        r = np.corrcoef(a, b)[0, 1]; rel.append(2 * r / (1 + r) if r > -1 else r)
out["listener_split_half_reliability"] = dict(median=round(float(np.median(rel)), 3), q1=round(float(np.percentile(rel, 25)), 3), q3=round(float(np.percentile(rel, 75)), 3), songs=len(rel))
print("listener agreement (split-half, corrected):", out["listener_split_half_reliability"])
json.dump(out, open("section_results.json", "w"), indent=1)
