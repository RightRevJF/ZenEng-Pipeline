"""How long a singer goes without a breath: phrases split at a silence of at least an eighth (or a beat), in beats. Kept: CoCoPops Billboard voice
(corpora/cocopops_notes.csv.gz or $LUTHIER_COCOPOPS_NOTES). Luthier: the records given. python3 studies/breath/phrases.py rec.song.json ..."""
import sys, os, json, numpy as np, pandas as pd
def phr(on, end, gap):
    out = []; s = on[0]
    for i in range(len(on) - 1):
        if on[i + 1] - end[i] >= gap: out.append(end[i] - s); s = on[i + 1]
    out.append(end[-1] - s); return out
d = pd.read_csv(os.environ.get("LUTHIER_COCOPOPS_NOTES", "corpora/cocopops_notes.csv.gz"), low_memory=False); d = d[(d.dur > 0) & (d.lead == "voice")]
for gap in (0.5, 1.0):
    P = []; L = []
    for s, g in d.groupby("song"):
        g = g.sort_values("abs_beat"); on = g.abs_beat.values; end = np.minimum(on + g.dur.values, np.r_[on[1:], 1e9])
        if len(g) < 100: continue
        p = phr(on, end, gap); P += p; L.append(max(p))
    print(f"kept, breath at a silence of {gap} beat or more: phrase beats 50/90/99th {np.percentile(P, (50, 90, 99)).round(1)}; share over 12 beats {np.mean(np.array(P) > 12):.3f}; each song's longest, median {np.median(L):.1f}")
    for f in sys.argv[1:]:
        R = json.load(open(f)); ns = sorted(R["melody"]["notes"], key=lambda n: n["on"]); on = np.array([n["on"] for n in ns]) / 12; end = on + np.array([n["dur"] for n in ns]) / 12
        p = phr(on, end, gap); print(f"   {f.split('/')[-1]}: 50/90th {np.percentile(p, (50, 90)).round(1)}; over 12 beats {np.mean(np.array(p) > 12):.3f}; longest {max(p):.1f}")
