"""896 (749.67): how much of its source does a kept song's returning line keep?  python3 lib/luthier/make_kept_returns.py -> tables/kept_returns.json (needs the kept corpus)
Verse (and chorus) instances are runs of notes with that section label; lines are runs split at onsets a half note apart; a later instance's line is matched to the
first instance's line that starts the same number of bars in. Kept share = the longest common subsequence over the source's length, of pitches and of onsets counted
from the line's first onset, which is how lib/luthier/review9_again_check.py reads the engine's lines sung again."""
import os, sys, json, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import kept_corpus as KC
def lcs(a, b):
    L = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a)):
        for j in range(len(b)): L[i + 1][j + 1] = L[i][j] + 1 if a[i] == b[j] else max(L[i][j + 1], L[i + 1][j])
    return L[-1][-1]
if __name__ == "__main__":
    rows = []
    for k in KC.kept_songs():
        t, p, sec = k["t"], k["p"], k["sec"]
        for kind in ("verse", "chorus"):
            inst = []; cur = None
            for i in range(len(t)):
                if sec[i] == kind:
                    if cur is None or (i and sec[i - 1] != kind) or (i and t[i] - t[i - 1] >= 96 * 2): cur = []; inst.append(cur)
                    cur.append(i)
            if len(inst) < 2: continue
            def lines(ix):
                out = collections.OrderedDict(); b0 = t[ix[0]] // 48; cur = None
                for q, i in enumerate(ix):
                    if q == 0 or t[i] - t[ix[q - 1]] >= 24: cur = []; out[int(round((t[i] - b0 * 48) / 48.0))] = cur
                    cur.append(i)
                return out
            A = lines(inst[0])
            for later in inst[1:]:
                same = []; diff = []
                for q, ix in lines(later).items():
                    if q not in A or len(ix) < 3 or len(A[q]) < 3: continue
                    a, b = ix, A[q]; pa, pb = list(p[a]), list(p[b]); ra, rb = list(t[a] - t[a[0]]), list(t[b] - t[b[0]]); (same if len(pa) == len(pb) else diff).append((lcs(pa, pb) / len(pb), lcs(ra, rb) / len(rb), pa == pb and ra == rb))
                if len(same) + len(diff) >= 3: rows.append(dict(song=k["song"], kind=kind, lines=len(same) + len(diff), same_count=len(same), identical=sum(x[2] for x in same), same_pitch=float(np.mean([x[0] for x in same])) if same else None, same_rhythm=float(np.mean([x[1] for x in same])) if same else None,
                                                                 diff_pitch=float(np.mean([x[0] for x in diff])) if diff else None, diff_rhythm=float(np.mean([x[1] for x in diff])) if diff else None))
    q = lambda v: [round(float(x), 3) for x in np.percentile([y for y in v if y is not None], (25, 50, 75))]; out = {}
    for kind in ("verse", "chorus"):
        v = [r for r in rows if r["kind"] == kind]
        out[kind] = dict(returns=len(v), songs=len({r["song"] for r in v}), share_of_lines_with_the_same_count=round(sum(r["same_count"] for r in v) / sum(r["lines"] for r in v), 3), identical_among_same_count=round(sum(r["identical"] for r in v) / max(1, sum(r["same_count"] for r in v)), 3),
                         same_count_pitch_kept=q([r["same_pitch"] for r in v]), same_count_rhythm_kept=q([r["same_rhythm"] for r in v]), other_count_pitch_kept=q([r["diff_pitch"] for r in v]), other_count_rhythm_kept=q([r["diff_rhythm"] for r in v]))
    json.dump(out, open(os.path.join(KC.ROOT, "tables", "kept_returns.json"), "w"), indent=1); print(json.dumps(out["verse"]))
