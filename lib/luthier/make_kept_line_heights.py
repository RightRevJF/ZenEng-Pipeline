"""749.201: the maker of tables/kept_line_heights.json. For each part of the kept songs (verse, chorus, bridge, pre-chorus), the heights of its lines: each line's middle pitch
less the part's own (weighted by notes), in semitones to the half, in the order sung. A line is three notes or more; a part, three such lines or more (lines as the kept corpus cuts them).
The engine draws a part's line centres as one of these kept contours (studies/line_heights). Also the figures a check reads: the spread between lines, and how one line's height follows the last.
    python3 lib/luthier/make_kept_line_heights.py        # needs the kept corpus (lib/luthier/kept_corpus.py)"""
import os, sys, json, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
KIND = {"verse": "Verse", "chorus": "Chorus", "bridge": "Bridge", "prechorus": "Pre-chorus"}
def table(): return json.load(open(os.path.join(HERE, "..", "..", "tables", "kept_line_heights.json")))
def heights(lines):
    """the offsets of a part's lines (lists of pitches) from the part's own middle; None if too few"""
    lines = [l for l in lines if len(l) >= 3]
    if len(lines) < 3: return None
    w = np.array([len(l) for l in lines], float); mids = np.array([np.mean(l) for l in lines]); return mids - float(np.sum(w * mids) / w.sum()), w
def between(off, w): return float(np.sqrt(np.sum(w * off ** 2) / w.sum()))
def follows(off):
    """how one line's height follows the last: the correlation of each line's offset with the one before (None under four lines or where the heights do not vary)"""
    if len(off) < 4 or np.std(off[:-1]) == 0 or np.std(off[1:]) == 0: return None
    return float(np.corrcoef(off[:-1], off[1:])[0, 1])
if __name__ == "__main__":
    import kept_corpus as KC
    C = collections.defaultdict(list); B = collections.defaultdict(list); F = collections.defaultdict(list); songs = 0
    for k in KC.kept_songs():
        songs += 1; cur = None; lines = collections.OrderedDict()
        def flush():
            if cur in KIND and lines:
                h = heights(list(lines.values()))
                if h is not None:
                    off, w = h; C[KIND[cur]].append([round(float(x) * 2) / 2 for x in off]); B[KIND[cur]].append(between(off, w)); f = follows(off)
                    if f is not None: F[KIND[cur]].append(f)
        for i, (l, s) in enumerate(zip(k["lines"], k["sec"])):
            if str(s) != cur: flush(); cur = str(s); lines = collections.OrderedDict()
            lines.setdefault(l, []).append(int(k["p"][i]))
        flush()
    q = lambda v: [round(float(x), 3) for x in np.percentile(v, (10, 25, 50, 75, 90))]
    out = dict(source="kept songs, 4/4 (kept_corpus.kept_songs())", kept_songs=songs, contours=dict(C), between_lines_10_25_50_75_90={k: q(v) for k, v in B.items()}, follows_the_last_10_25_50_75_90={k: q(v) for k, v in F.items()}, parts={k: len(v) for k, v in C.items()})
    json.dump(out, open(os.path.join(HERE, "..", "..", "tables", "kept_line_heights.json"), "w")); print(json.dumps({k: v for k, v in out.items() if k != "contours"}, indent=1))
