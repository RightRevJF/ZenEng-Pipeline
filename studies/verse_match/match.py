"""Do later verses match the first verse? Kept 4/4 songs against Luthier's songs and lyrics.
Kept songs: each verse (a run of notes under one verse label), syllables counted bar by bar from the verse's first bar; verse 1 against each later verse:
the share of bars with the same number of syllables, and the share of bars sung on the same rhythm (the same onsets in the bar).
Luthier's songs: the same reading on their records; and, on the lyric alone, the share of later-verse lines with verse 1's syllable count.
python3 studies/verse_match/match.py -> match.json"""
import sys, os, json, re, collections, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import kept_corpus as KC
def verses(secs, ons, isyl, bar):
    """runs of one verse label -> for each run, {bar index from its first bar: sorted onsets in the bar of notes that begin a syllable}"""
    runs = []; cur = None
    for s, t, y in zip(secs, ons, isyl):
        v = "verse" in str(s).lower()
        if v and (cur is None or cur[0] != str(s)): cur = [str(s), t // bar, collections.defaultdict(list)]; runs.append(cur)
        if not v: cur = None; continue
        if y: cur[2][t // bar - cur[1]].append(t % bar)
    return [r[2] for r in runs if sum(map(len, r[2].values())) >= 12]
def compare(vs):
    a = vs[0]; cnt = []; rhy = []; dif = []
    for b0 in vs[1:]:
        best = None
        for sh in (-1, 0, 1):                                                                # a pickup can put a verse's first note in the bar before: the later verse is tried a bar early and a bar late, and the best match kept
            b = {k + sh: v for k, v in b0.items()}; ks = range(min(min(a), min(b)), min(max(a), max(b)) + 1)
            c_ = [len(a.get(k, [])) == len(b.get(k, [])) for k in ks]
            if best is None or np.mean(c_) > np.mean(best[0]): best = (c_, [sorted(a.get(k, [])) == sorted(b.get(k, [])) for k in ks], [abs(len(a.get(k, [])) - len(b.get(k, []))) for k in ks])
        cnt += best[0]; rhy += best[1]; dif += best[2]
    return dict(bars_same_syllable_count=float(np.mean(cnt)), bars_same_rhythm=float(np.mean(rhy)), mean_difference_in_syllables_a_bar=float(np.mean(dif))) if cnt else None
K = []
for k in KC.kept_songs():
    g = KC.table(); break
T = KC.table()
for s, g in T.groupby("song", sort=False):
    g = g.sort_values("abs_beat"); ons = np.round((g.bar.values * 4.0 + g.beat.values) * 12).astype(int); syl = [str(x) if x == x else "" for x in g.syl.values]
    vs = verses(list(g.section.values), list(ons), [x.strip() != "_" for x in syl], 48)
    if len(vs) >= 2:
        r = compare(vs)
        if r: K.append(r)
cols = list(K[0]); q = {c: [round(float(x), 3) for x in np.percentile([r[c] for r in K], (10, 25, 50, 75, 90))] for c in cols}; out = dict(kept_songs_with_two_verses=len(K), kept_10_25_50_75_90=q, luthier={})
print("kept songs with two verses or more:", len(K)); [print(f"  {c:38} {q[c]}") for c in cols]
for tag, p in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("59", "songs/p69/lyric59")):
    R = json.load(open(os.path.join(ROOT, p + ".song.json"))); L = json.load(open(os.path.join(ROOT, p + ".json"))); ns = sorted(R["melody"]["notes"], key=lambda n: n["on"])
    vs = verses([n["sec"] for n in ns], [n["on"] for n in ns], [n.get("melisma") != "second" for n in ns], R["bar"]); r = compare(vs) if len(vs) >= 2 else None
    V = [x[2] for x in R["spec"]["sung"] if x[1] == "Verse"]; lyr = None
    if len(V) >= 2:
        a = V[0]; pairs = [(a[j], y) for v in V[1:] for j, y in enumerate(v) if j < len(a)]; same = [len(x) == len(y) for x, y in pairs]
        st = [[p[1] for p in x] == [p[1] for p in y] for x, y in pairs]; pos = [float(np.mean([p[1] == q_[1] for p, q_ in zip(x, y)])) for x, y in pairs if len(x) == len(y)]
        lyr = dict(later_verse_lines=len(pairs), with_verse_1s_syllable_count=round(float(np.mean(same)), 2), with_verse_1s_stresses_exactly=round(float(np.mean(st)), 2), stresses_matching_where_the_counts_match=round(float(np.mean(pos)), 2) if pos else None,
                   mean_difference_in_syllables_a_line=round(float(np.mean([abs(len(x) - len(y)) for x, y in pairs])), 2), verse_line_lengths=[[len(y) for y in v] for v in V])
    place = {c: round(float(np.mean([x[c] <= r[c] for x in K])), 2) for c in cols} if r else None
    out["luthier"][tag] = dict(title=R["title"], record={c: round(r[c], 3) for c in cols} if r else None, share_of_kept_songs_at_or_under=place, lyric=lyr); print(tag, json.dumps(out["luthier"][tag]))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "match.json"), "w"), indent=1)
