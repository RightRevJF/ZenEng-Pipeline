"""749.77: do kept songs give a stressed syllable a sixteenth more often in returning lines than in first ones? Stressed syllables (the lexicon's weights, as
make_kept_word_weight reads them) whose next onset in the same line comes a sixteenth or less later. First verse and first chorus against the later ones.
Reads the kept corpus at $LUTHIER_COCOPOPS_NOTES or corpora/. python3 studies/kept_checks/stressed16_returns.py"""
import sys, os, collections, numpy as np
sys.path[:0] = ["lib/luthier", "lib/carol"]
import kept_corpus as KC, make_kept_word_weight as MW
cnt = collections.Counter(); per_song = []
for k in KC.kept_songs():
    tr, wid = MW.tiers(k["words"])
    if len(tr) != len(k["t"]): continue
    t, lines, sec = k["t"], k["lines"], [str(x).lower() for x in k["sec"]]
    inst = {}; seen = collections.Counter(); cur = None
    for i in range(len(t)):
        if sec[i] != cur: cur = sec[i]; seen[cur] += 1
        inst[i] = (cur, seen[cur])
    a = collections.Counter()
    for i in range(len(t) - 1):
        if tr[i] != 2 or lines[i + 1] != lines[i]: continue
        s, n = inst[i]
        if s not in ("verse", "chorus"): continue
        grp = "first" if n == 1 else "later"; short = (t[i + 1] - t[i]) <= 3
        cnt[(grp, "n")] += 1; cnt[(grp, "short")] += short; a[(grp, "n")] += 1; a[(grp, "short")] += short
    if a[("first", "n")] >= 10 and a[("later", "n")] >= 10: per_song.append(a[("later", "short")] / a[("later", "n")] - a[("first", "short")] / a[("first", "n")])
f = cnt[("first", "short")] / cnt[("first", "n")]; l = cnt[("later", "short")] / cnt[("later", "n")]; ps = np.array(per_song)
print(f"{os.environ.get('LUTHIER_COCOPOPS_NOTES', 'corpora/cocopops_notes.csv.gz')}: stressed syllables a sixteenth long inside lines: first verse and chorus {f:.3f} ({cnt[('first','n')]}), later ones {l:.3f} ({cnt[('later','n')]}); "
      f"later minus first by song ({len(ps)} songs): median {np.median(ps):+.3f}, quartiles {np.quantile(ps, 0.25):+.3f} {np.quantile(ps, 0.75):+.3f}")
