"""899 (749.76, 749.80): how a kept line ends.  python3 lib/luthier/make_kept_line_ends.py -> tables/kept_line_ends.json (needs the kept corpus; see kept_corpus.py)
A lyric line begins at a capital letter (not 'I') or after two beats of silence, as the transcribers set the words. For each line's last syllable: its weight
(function word, weak syllable, stressed); G, the time from its onset to the next line's first onset; D, how long it is held (its own note and any notes slurred to it).
The table gives, by weight and by G, the counts of each D: so the last note and the rest after it (G - D) are drawn together, and a line may run into the next
as kept lines do. Twelfths of a quarter note; G and D are taken to the nearest listed value."""
import os, sys, json, re, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, "..", "carol")]
import kept_corpus as KC, make_kept_word_weight as MW
GV = [12, 18, 24, 30, 36, 42, 48, 60, 72, 96, 144]; DV = [3, 6, 9, 12, 18, 24, 30, 36, 48, 60, 72, 96]; I_WORDS = {"i", "i'm", "i'll", "i've", "i'd"}
near = lambda V, x: min(range(len(V)), key=lambda j: abs(V[j] - x))
def line_ends(min_notes=150):
    """each kept song -> [(tier or None, G, D, rest)] for every line but the song's last"""
    import pandas as pd
    K = set(json.load(open(os.path.join(KC.ROOT, "tables", "kept_songs_4-4_pop.json"))))
    for s, g in KC.table().groupby("song", sort=False):
        if str(s) not in K or len(g) < min_notes: continue
        g = g.sort_values("abs_beat"); t = np.round((g.bar.values * 4.0 + g.beat.values) * 12).astype(int); du = np.round(g.dur.values * 12).astype(int); syl = [str(x) if x == x else "" for x in g.syl.values]
        S = []                                                                               # syllables: [onset, end, text, starts a line]
        for i, x in enumerate(syl):
            w = x.strip()
            if w == "_" and S: S[-1][1] = max(S[-1][1], t[i] + du[i]); continue              # a note slurred to the syllable before
            new = bool(S) and ((t[i] - S[-1][1]) >= 24 or (w[:1].isupper() and w.lower().strip(".,!?;:'\"") not in I_WORDS))
            S.append([int(t[i]), int(t[i] + du[i]), w, new or not S])
        words = []; cur = ""; n = 0
        for on, end, w, new in S:
            cont = w.endswith("-"); cur += re.sub(r"[^A-Za-z']", "", w); n += 1
            if not cont: words.append((cur, n)); cur = ""; n = 0
        if n: words.append((cur, n))
        tr, _ = MW.tiers(words); out = []
        if len(tr) != len(S): continue
        for i in range(len(S) - 1):
            if S[i + 1][3]: out.append((tr[i], S[i + 1][0] - S[i][0], S[i][1] - S[i][0], S[i + 1][0] - S[i][1]))
        yield str(s), out, S
if __name__ == "__main__":
    C = np.zeros((3, len(GV), len(DV))); Gs = []; rests = []; runon = []; per = []; EN = {True: [0, 0, 0], False: [0, 0, 0]}; SB = []
    for s, ends, S in line_ends():
        words = []; cur = ""; n_ = 0                                                          # 911 (749.89): how a line enters (771) and how often a stressed syllable is on a beat (731), given makers
        for on, end, w, new in S:
            cont = w.endswith("-"); cur += re.sub(r"[^A-Za-z']", "", w); n_ += 1
            if not cont: words.append((cur, n_)); cur = ""; n_ = 0
        if n_: words.append((cur, n_))
        tr_, _ = MW.tiers(words); sb = [0, 0]
        for i, (on, end, w, new) in enumerate(S):
            if tr_[i] is None: continue
            if new: EN[tr_[i] == 2][0 if on % 48 >= 36 else 1 if on % 48 == 0 else 2] += 1
            if tr_[i] == 2: sb[1] += 1; sb[0] += on % 12 == 0
        if sb[1] >= 40: SB.append(sb[0] / sb[1])
        for tr, G, D, r in ends:
            Gs.append(G); rests.append(r)
            if tr is not None: C[tr, near(GV, G), near(DV, min(D, G))] += 1
        if ends: runon.append(float(np.mean([r < 12 for _, _, _, r in ends]))); per.append(len(S) / (len(ends) + 1))
    T = dict(source="159 kept 4/4 songs (CoCoPops Billboard); lyric lines by the transcribers' capitals or two beats of silence", line_ends=int(len(Gs)), G_values=GV, D_values=DV, counts_by_tier_G_D=C.astype(int).tolist(),
             G_percentiles_10_25_50_75_90=[float(x) for x in np.percentile(Gs, (10, 25, 50, 75, 90))], rest_percentiles_10_25_50_75_90=[float(x) for x in np.percentile(rests, (10, 25, 50, 75, 90))],
             lines_run_on_with_under_a_beat_of_rest_share=round(float(np.mean([r < 12 for r in rests])), 3), run_on_share_by_song_quartiles=[round(float(x), 3) for x in np.percentile(runon, (25, 50, 75))], syllables_a_line_quartiles=[round(float(x), 1) for x in np.percentile(per, (25, 50, 75))],
             held_a_half_or_more_by_tier=[round(float(C[k][:, 5:].sum() / C[k].sum()), 3) for k in range(3)], an_eighth_or_less_by_tier=[round(float(C[k][:, :2].sum() / C[k].sum()), 3) for k in range(3)])
    P_ = []; L_ = []                                                                          # 906 (749.83): how long a kept singer goes without a breath, a breath read at half a beat of silence
    for k in KC.kept_songs():
        on = k["t"] / 12.0; end = np.minimum(on + k["dur"] / 12.0, np.r_[on[1:], 1e9]); ph = []; s0 = on[0]
        for i in range(len(on) - 1):
            if on[i + 1] - end[i] >= 0.5: ph.append(end[i] - s0); s0 = on[i + 1]
        ph.append(end[-1] - s0); P_ += ph; L_.append(max(ph))
    T["phrases_split_at_half_a_beat"] = dict(share_over_12_beats=round(float(np.mean(np.array(P_) > 12)), 3), beats_50_90_99=[round(float(x), 1) for x in np.percentile(P_, (50, 90, 99))], each_songs_longest_quartiles=[round(float(x), 1) for x in np.percentile(L_, (25, 50, 75))])
    T["entries_before_on_after_the_bar_line"] = dict(note="a line's first syllable: within a beat before a bar line, on it, or elsewhere", stressed=[round(x / sum(EN[True]), 3) for x in EN[True]], unstressed=[round(x / sum(EN[False]), 3) for x in EN[False]], lines=[int(sum(EN[True])), int(sum(EN[False]))])
    T["stressed_syllables_on_a_beat_by_song_5_10_25_50_75"] = [round(float(x), 3) for x in np.percentile(SB, (5, 10, 25, 50, 75))]
    json.dump(T, open(os.path.join(KC.ROOT, "tables", "kept_line_ends.json"), "w"), indent=1); print({k: v for k, v in T.items() if k != "counts_by_tier_G_D"})
