"""749.94: does pitch scaling follow the chorus's lift over the verse? Per kept song: pitch scaling (as make_kept_4_4_tables reads it) and the chorus's
median sung pitch over the verse's (sections by the transcribers' labels); the same for the records given.
    python3 studies/soundness/pitch_scaling_lift.py songs/p65/lyric55.song.json songs/p64/lyric54.song.json songs/p68/lyric58.song.json"""
import os, sys, json, statistics, numpy as np
from scipy.stats import spearmanr
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import kept_corpus as KC, scaling as SC
def ps(t, p):
    keep = [i for i in range(len(t)) if (i == 0 or t[i] > t[i - 1]) and t[i] % 3 == 0]; sc = SC.series([(int(t[i]), int(p[i])) for i in keep]); a = SC.dfa(sc["pitch"]); return a["alpha"] if a else None
rows = []
for k in KC.kept_songs():
    sec = [str(s).lower() for s in k["sec"]]; v = [p for p, s in zip(k["p"], sec) if "verse" in s]; c = [p for p, s in zip(k["p"], sec) if "chorus" in s and "pre" not in s]
    a = ps(k["t"], k["p"])
    if a is not None and len(v) >= 20 and len(c) >= 20: rows.append((a, statistics.median(c) - statistics.median(v)))
out = dict(kept_songs=len(rows), spearman=[round(float(x), 3) for x in spearmanr([r[0] for r in rows], [r[1] for r in rows])], lift_quartiles=[float(x) for x in np.percentile([r[1] for r in rows], (25, 50, 75, 90))],
           pitch_scaling_by_lift={g: round(float(np.median([r[0] for r in rows if lo <= r[1] < hi])), 3) for g, lo, hi in (("under 1", -99, 1), ("1 to 4", 1, 4.5), ("5 to 7", 4.5, 7.5), ("8 or more", 7.5, 99))}, records={})
for f in sys.argv[1:]:
    R = json.load(open(f)); ns = sorted(R["melody"]["notes"], key=lambda n: n["on"]); v = [n["midi"] for n in ns if n["sec"].startswith("Verse")]; c = [n["midi"] for n in ns if "Chorus" in n["sec"]]
    out["records"][os.path.basename(f)] = dict(pitch_scaling=round(ps([n["on"] for n in ns], [n["midi"] for n in ns]), 3), lift=statistics.median(c) - statistics.median(v))
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pitch_scaling_lift.json"), "w"), indent=1)
