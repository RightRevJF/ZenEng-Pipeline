"""749.93: what rhythm scaling follows in the kept songs. Per kept song: rhythm scaling (DFA of onsets on the grid, as make_kept_4_4_tables reads it)
against how much the density of sung onsets changes over the song: the spread (sd / mean) of onsets per 4-bar block, the share of 4-bar blocks with no
sung onset (the voice out), and the spread of onsets per bar. The same for the records given.
    python3 studies/soundness/rhythm_scaling_why.py songs/p65/lyric55.song.json songs/p64/lyric54.song.json songs/p68/lyric58.song.json"""
import os, sys, json, numpy as np
from scipy.stats import spearmanr
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import kept_corpus as KC, scaling as SC
def feats(t):
    t = np.asarray(sorted(set(int(x) for x in t if x % 3 == 0))); b4 = (t - t[0]) // 192; c4 = np.bincount(b4); b1 = (t - t[0]) // 48; c1 = np.bincount(b1)
    sc = SC.series([(int(x), 60) for x in t]); r = SC.dfa(sc["onsets on the grid"])
    return dict(rhythm_scaling=r["alpha"] if r else None, block_spread=float(np.std(c4) / np.mean(c4)), empty_blocks=float(np.mean(c4 == 0)), bar_spread=float(np.std(c1) / np.mean(c1)), empty_bars=float(np.mean(c1 == 0)))
K = [feats(k["t"]) for k in KC.kept_songs()]; K = [k for k in K if k["rhythm_scaling"] is not None]
out = dict(kept_songs=len(K), spearman_with_rhythm_scaling={f: [round(float(x), 3) for x in spearmanr([k["rhythm_scaling"] for k in K], [k[f] for k in K])] for f in ("block_spread", "empty_blocks", "bar_spread", "empty_bars")},
           kept_quartiles={f: [round(float(x), 3) for x in np.percentile([k[f] for k in K], (25, 50, 75))] for f in K[0]}, records={})
for f in sys.argv[1:]:
    R = json.load(open(f)); out["records"][os.path.basename(f)] = {k: round(v, 3) for k, v in feats([n["on"] for n in R["melody"]["notes"]]).items()}
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rhythm_scaling_why.json"), "w"), indent=1)
