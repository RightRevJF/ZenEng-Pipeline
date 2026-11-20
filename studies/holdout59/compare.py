"""Hold-out (song 59): where each song's record stands against single kept songs (checks outside the kept middle half and outside the 10th to 90th),
and the soundness rule on every three of songs 55, 54, 58 and 59. From the repo root: python3 studies/holdout59/compare.py"""
import sys, os, json, itertools, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "studies", "soundness"), os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
sys.argv = sys.argv[:1]
import soundness as S
K = S.kept_rows(); NAMES = [n for n, _ in S.CHECKS]; full = [r for r in K.values() if all(n in r for n in S.KEPT_NAMES)] if hasattr(S, "KEPT_NAMES") else [r for r in K.values() if all(n in r for n in NAMES if n in next(iter(K.values())))]
kn = [n for n in NAMES if all(n in r for r in full)]
Q = {n: [float(x) for x in np.percentile([r[n] for r in full], (10, 25, 50, 75, 90))] for n in kn}
def counts(r, names): return sum(S.side(Q[n], r[n], "half") != 0 for n in names if n in r), sum(S.side(Q[n], r[n], "wide") != 0 for n in names if n in r)
kc = np.array([counts(r, kn) for r in full])
recs = {t: S.record_row(json.load(open(os.path.join(ROOT, p)))) for t, p in (("55", "songs/p65/lyric55.song.json"), ("54", "songs/p64/lyric54.song.json"), ("58", "songs/p68/lyric58.song.json"), ("59", "songs/p69/lyric59.song.json"))}
out = dict(checks_read_on_kept_songs=len(kn), kept_songs=len(full), kept_outside_middle_half_10_25_50_75_90=[float(x) for x in np.percentile(kc[:, 0], (10, 25, 50, 75, 90))], kept_outside_10_90_10_25_50_75_90=[float(x) for x in np.percentile(kc[:, 1], (10, 25, 50, 75, 90))], songs={}, triples={})
for t, r in recs.items():
    h, w = counts(r, kn); out["songs"][t] = dict(outside_middle_half=h, outside_10_90=w, kept_songs_at_or_under_this_many_outside_middle_half=round(float(np.mean(kc[:, 0] <= h)), 3), which=[n for n in kn if S.side(Q[n], r[n], "half") != 0])
Qa = {n: [float(x) for x in np.percentile([r[n] for r in K.values() if n in r], (10, 25, 50, 75, 90))] for n in NAMES}
for tri in itertools.combinations(recs, 3):
    rows = [recs[t] for t in tri]; w = S.same_side(Qa, rows, NAMES, "wide"); h = S.same_side(Qa, rows, NAMES, "half")
    out["triples"]["+".join(tri)] = dict(sound=(not w and len(h) <= 2), leans_10_90=w, leans_25_75=h)
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(ROOT, "studies", "holdout59", "compare.json"), "w"), indent=1)
