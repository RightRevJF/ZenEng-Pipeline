"""749.207 (a trial, studies/borrow_kept): the kept share of a part's lines that repeat the line before or the line two before.
A repeat: both lines four notes or more, read as steps of the song's scale, aligned from the first note over the shorter line; their intervals agree in four places of five (studies/line_repeats).
Beside it, as a description (list for v51, addendum 8): the share by the best of three alignments (the later line as it is, less its first note, or against the earlier line less its first note), and how many lines are so short that every interval must agree.
    python3 lib/luthier/make_kept_line_repeat.py   -> tables/kept_line_repeat.json"""
import os, sys, json, math, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, "..", "carol"), os.path.join(HERE, "..", "..", "tables", "metre_atlas")]
import numpy as np, kept_corpus as KC
MAJ = [0, 2, 4, 5, 7, 9, 11]; MIN = [0, 2, 3, 5, 7, 8, 10]
def deg(p, tonic, scale):
    d = (p - tonic) % 12; o = (p - tonic) // 12
    while d not in scale: d -= 1
    return 7 * o + scale.index(d)
def repeat(a, b):
    m = min(len(a), len(b))
    if m < 4: return None
    if sum(a[k + 1] - a[k] == b[k + 1] - b[k] for k in range(m - 1)) < math.ceil(0.8 * (m - 1)): return None
    return int(np.median([b[k] - a[k] for k in range(m)]))
def repeat3(a, b): return next((h for x, y in ((a, b), (a, b[1:]), (a[1:], b)) for h in [repeat(x, y)] if h is not None), None)
def kind(s): s = str(s).lstrip(">"); return "Chorus" if s in ("chorus", "refrain") else "Verse" if s == "verse" else "other"
if __name__ == "__main__":
    d = KC.table(); key = {str(s): (int(g.key_pc.iloc[0]), MIN if str(g["mode"].iloc[0]) == "minor" else MAJ) for s, g in d.groupby("song", sort=False)}
    BC = collections.Counter()
    N = collections.Counter(); R = collections.Counter(); R3 = collections.Counter(); short = collections.Counter(); songs = 0
    for k in KC.kept_songs():
        if k["song"] not in key: continue
        songs += 1; tonic, scale = key[k["song"]]; cur = None; lines = collections.OrderedDict()
        def flush():
            ls = list(lines.values()); kd = kind(cur)
            for i in range(1, len(ls)):
                if len(ls[i]) < 4: continue
                for part in (kd, "all"):
                    N[part] += 1; short[part] += len(ls[i]) < 6
                    for j in (i - 2, i - 1):
                        if j >= 0 and len(ls[j]) >= 4: dd = min(3, abs(len(ls[i]) - len(ls[j]))); BC[(part, dd, "n")] += 1; BC[(part, dd, "r")] += repeat(ls[j], ls[i]) is not None; BC[(part, dd, "r3")] += repeat3(ls[j], ls[i]) is not None
                    R[part] += any(repeat(ls[j], ls[i]) is not None for j in (i - 2, i - 1) if j >= 0); R3[part] += any(repeat3(ls[j], ls[i]) is not None for j in (i - 2, i - 1) if j >= 0)
        for i, (l, s) in enumerate(zip(k["lines"], k["sec"])):
            if str(s) != cur:
                if cur is not None: flush()
                cur = str(s); lines = collections.OrderedDict()
            lines.setdefault(l, []).append(deg(int(k["p"][i]), tonic, scale))
        flush()
    T = dict(note="749.207, a trial: the kept share of a part's lines (from its second, four notes or more) that repeat the line before or the line two before, within one section. 'other' is every part that is neither a verse nor a chorus; a part with no table of its own takes 'all'.",
             songs=songs, share={p: round(R[p] / N[p], 3) for p in ("Verse", "Chorus", "other", "all")}, lines={p: N[p] for p in N},
             described=dict(best_of_three_alignments={p: round(R3[p] / N[p], 3) for p in ("Verse", "Chorus", "other", "all")}, lines_of_four_or_five_notes_where_every_interval_must_agree={p: round(short[p] / N[p], 3) for p in ("Verse", "Chorus", "all")}))
    T["by_count"] = {p: [round(BC[(p, dd, "r3")] / BC[(p, dd, "n")], 3) for dd in range(4)] for p in ("Verse", "Chorus", "other", "all")}; T["by_count_strict"] = {p: [round(BC[(p, dd, "r")] / BC[(p, dd, "n")], 3) for dd in range(4)] for p in ("Verse", "Chorus", "other", "all")}; T["by_count_pairs"] = {p: [BC[(p, dd, "n")] for dd in range(4)] for p in ("Verse", "Chorus", "other", "all")}
    T["by_count_note"] = "749.209, a trial: of a part's nearby line pairs (a line and the line before or two before, both four notes or more) whose syllable counts differ by 0, 1, 2, 3 or more, the share that are repeats; by_count by the best of three alignments, by_count_strict aligned from the first note."
    json.dump(T, open(os.path.join(HERE, "..", "..", "tables", "kept_line_repeat.json"), "w"), indent=1); print(json.dumps(T, indent=1))
