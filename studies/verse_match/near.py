"""Where does a bar's rhythm come back from? For each bar that holds sung notes: the nearest earlier bar with the same rhythm (the same onsets in the bar), by how far back it is.
Kept 4/4 songs against Luthier's records. python3 studies/verse_match/near.py -> near.json"""
import sys, os, json, collections, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import kept_corpus as KC
def read(ons, bar=48):
    by = collections.defaultdict(list)
    for t in ons: by[t // bar].append(t % bar)
    bars = sorted(by); pat = {b: tuple(sorted(by[b])) for b in bars}; last = {}; d = []
    for b in bars:
        p = pat[b]; d.append(b - last[p] if p in last else None); last[p] = b
    n = len(d); sh = lambda f: sum(1 for x in d if x is not None and f(x)) / n
    return dict(sung_again=sh(lambda x: True), from_the_bar_before=sh(lambda x: x == 1), from_two_bars_back=sh(lambda x: x == 2), from_3_or_4_bars_back=sh(lambda x: 3 <= x <= 4), from_5_to_8_bars_back=sh(lambda x: 5 <= x <= 8), from_9_to_16_bars_back=sh(lambda x: 9 <= x <= 16), from_further_back=sh(lambda x: x > 16))
K = [read([int(x) for x in np.asarray(k["t"])]) for k in KC.kept_songs()]      # kept onsets are in twelfths of a quarter: 48 to the bar, as in the records
cols = list(K[0]); q = {c: [round(float(x), 3) for x in np.percentile([r[c] for r in K], (25, 50, 75))] for c in cols}; out = dict(kept_songs=len(K), kept_quartiles=q, luthier={})
print("kept", len(K)); [print(f"  {c:26} {q[c]}") for c in cols]
for tag, p in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("59", "songs/p69/lyric59")):
    R = json.load(open(os.path.join(ROOT, p + ".song.json"))); r = read([n["on"] for n in R["melody"]["notes"]], R["bar"]); out["luthier"][tag] = {c: round(r[c], 3) for c in cols}
    print(tag, {c: (round(r[c], 3), "under 25th" if r[c] < q[c][0] else "over 75th" if r[c] > q[c][2] else "middle") for c in cols})
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "near.json"), "w"), indent=1)
