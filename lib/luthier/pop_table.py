"""Fix 812: a kept table for sung pop in 4/4 in the metre atlas's format, from the 159 kept CoCoPops Billboard songs (the 4/4 engine's own kept corpus),
so the metre engine can write a pop song in 4/4 against pop songs and not against Essen's folk tunes. Derived counts only."""
import sys, json, collections, numpy as np
sys.path.insert(0, "/home/claude/zeneng/corpus/nine"); sys.path.insert(0, "/home/claude/rightrevjf/zeneng-pipeline/tables/metre_atlas")
import common as C, atlas_build as AB
BAR, BEATS, BEAT = 48, [0, 12, 24, 36], 12
R = []; BARS = collections.Counter(); WIN = collections.defaultdict(collections.Counter); IV = collections.Counter(); POS = collections.Counter(); DUR = collections.Counter(); n = 0; IV2 = collections.defaultdict(collections.Counter)
for s, g in C.G.d.groupby("song", sort=False):
    if str(s) not in C.PT.SONGS: continue
    g = g.sort_values("abs_beat"); t = np.round((g.bar.values * 4.0 + g.beat.values) * 12).astype(int); p = g.pitch.values.astype(int); d = np.round(g.dur.values * 12).astype(int)
    if len(t) < 150: continue
    keep = [i for i in range(len(t)) if t[i] % 3 == 0 and (i == 0 or t[i] > t[i - 1])]
    ns = [[int(t[i]), int(max(3, d[i])), int(p[i])] for i in keep]; n += 1
    R.append(AB.readings(ns, BAR, BEATS, BEAT)); bars = collections.defaultdict(list)
    for on, dd, q in ns: bars[on // BAR].append(on % BAR); DUR[min(96, dd // 3 * 3)] += 1; POS[on % BAR] += 1
    for a, b in zip(ns, ns[1:]): IV[max(-12, min(12, b[2] - a[2]))] += 1
    ivs = [max(-12, min(12, y[2] - x[2])) for x, y in zip(ns, ns[1:])]
    for x, y in zip(ivs, ivs[1:]): IV2[x][y] += 1
    for b, v in bars.items():
        BARS[tuple(v)] += 1
        if b + 1 in bars: w = tuple(v) + tuple(x + BAR for x in bars[b + 1]); WIN[len(w)][w] += 1
tot = sum(POS.values())
T = dict(metre="4/4", kind="sung pop", bar=BAR, beats=BEATS, beat=BEAT, tunes=n, source="CoCoPops Billboard, the 159 kept songs", licence="derived counts; the corpus is for research use",
         readings_quartiles={k: [float(np.percentile([r[k] for r in R], q)) for q in (25, 50, 75)] for k in R[0]},
         bar_rhythms=[[list(k), c] for k, c in BARS.most_common(400)], two_bar_windows={str(k): [[list(w), c] for w, c in v.most_common(60)] for k, v in sorted(WIN.items()) if k <= 24},
         intervals={str(k): v for k, v in sorted(IV.items())}, interval_pairs={str(k): {str(j): c for j, c in sorted(v.items())} for k, v in sorted(IV2.items())}, onset_weights={str(k): round(v / tot, 4) for k, v in sorted(POS.items())}, durations={str(k): v for k, v in sorted(DUR.items())})
json.dump(T, open("/home/claude/rightrevjf/zeneng-pipeline/tables/metre_atlas/4-4_pop_sung.json", "w"))
print(n, "songs;", {k: [round(x, 3) for x in v] for k, v in T["readings_quartiles"].items()}); print({k: len(v) for k, v in T["two_bar_windows"].items()})
