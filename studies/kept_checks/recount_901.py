"""901 recount: kept line ends on a word's weak syllable; does the weak syllable outlast the stressed one? Uses make_kept_line_ends.line_ends."""
import sys, os, re, numpy as np
sys.path[:0] = ["lib/luthier", "lib/carol"]
import make_kept_line_ends as LE, make_kept_word_weight as MW
n = weak_longer = stressed_short = 0; lines = 0; ends_tier = [0, 0, 0, 0]; half = [[0, 0] for _ in range(3)]
for s, ends, S in LE.line_ends():
    words = []; cur = ""; k = 0
    for on, end, w, new in S:
        cont = w.endswith("-"); cur += re.sub(r"[^A-Za-z']", "", w); k += 1
        if not cont: words.append((cur, k)); cur = ""; k = 0
    if k: words.append((cur, k))
    tr, wid = MW.tiers(words)
    if len(tr) != len(S): continue
    for i in range(len(S) - 1):
        if not S[i + 1][3]: continue
        lines += 1; ends_tier[tr[i] if tr[i] is not None else 3] += 1
        if tr[i] is not None: half[tr[i]][0] += (S[i][1] - S[i][0]) >= 24; half[tr[i]][1] += 1
        if tr[i] != 1: continue
        j = i
        while j > 0 and wid[j - 1] == wid[i] and tr[j] != 2: j -= 1
        if tr[j] != 2 or wid[j] != wid[i]: continue
        n += 1; dw = S[i][1] - S[i][0]; ds = S[j][1] - S[j][0]
        weak_longer += dw > ds; stressed_short += ds < 12
print(f"{os.environ.get('LUTHIER_COCOPOPS_NOTES', 'corpora/cocopops_notes.csv.gz')}: line ends {lines}; last syllable tier counts (function, weak, stressed, unread) {ends_tier}")
print(f"  ends on a weak syllable after its stressed one: {n}; weak outlasts stressed {weak_longer / n:.2f}; stressed under a quarter {stressed_short / n:.2f}")
print("  held a half or more, by tier:", [round(a / b, 3) for a, b in half])
