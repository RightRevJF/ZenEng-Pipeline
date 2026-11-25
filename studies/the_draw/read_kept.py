"""The two readings on the kept songs (PREDICTION.md). -> kept.json"""
import os, sys, re, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); Lb = os.path.normpath(os.path.join(HERE, "..", "..", "lib", "luthier")); sys.path[:0] = [Lb, os.path.join(Lb, "..", "carol")]
import kept_corpus as KC, make_kept_word_weight as MK
norm = lambda w: re.sub(r"[^a-z]", "", w.lower()); A = []; songs = 0; with_leap = 0; notes = 0; B = []; tl = 0; LEN = collections.defaultdict(list); ALL = collections.defaultdict(list)
for k in KC.kept_songs():
    songs += 1; p, du, t = k["p"], k["dur"], k["t"]; top = max(p); lines = collections.defaultdict(list); notes += len(p)
    for i, l in enumerate(k["lines"]): lines[l].append(i)
    tr, wid = MK.tiers(k["words"]); ok = len(tr) == len(t); had = False
    for l, idx in lines.items():
        iv = [int(p[b]) - int(p[a]) for a, b in zip(idx, idx[1:])]
        for j, d in enumerate(iv):
            if abs(d) <= 12: continue
            far = idx[j + 1] if d > 0 else idx[j]; had = True
            A.append(dict(sec=str(k["sec"][far]), where="first" if j == 0 else "last" if j == len(iv) - 1 else "between", pair=any(abs(iv[q]) > 12 and iv[q] * d < 0 for q in (j - 2, j - 1, j + 1, j + 2) if 0 <= q < len(iv)),
                          far_top=int(p[far]) == top, far_dur=int(du[far]), far_stress=(tr[far] == 2) if ok and tr[far] is not None else None))
    with_leap += had
    if not ok: continue
    title = [norm(x) for x in re.findall(r"[A-Z][a-z']*|\d+", k["song"].split("_")[1])]; title = [x for x in title if x]; ws = [norm(w) for w, _ in k["words"]]
    for l, idx in lines.items():
        if any(tr[i] is None for i in idx): continue
        for i in idx: ALL[("function word", "weak", "stressed")[tr[i]]].append(int(du[i]))
        lw = []
        for i in idx:
            if not lw or lw[-1] != wid[i]: lw.append(wid[i])
        seq = [ws[q] for q in lw]
        if not title or len(idx) < 2 or not any(seq[j:j + len(title)] == title for j in range(len(seq) - len(title) + 1)): continue
        tl += 1
        for i in idx: LEN[("function word", "weak", "stressed")[tr[i]]].append(int(du[i]))
        topn = max(idx, key=lambda i: du[i]); kk = idx.index(topn)
        if tr[topn] == 2 or wid[topn] == wid[idx[-1]]: continue
        gaps = [int(t[b]) - int(t[a]) for a, b in zip(idx, idx[1:])]; st = [int(du[i]) for i in idx if tr[i] == 2]
        B.append(dict(function_word=tr[topn] == 0, first=kk == 0, before_widest_gap=kk < len(gaps) and gaps[kk] == max(gaps), short_by=int(du[topn]) - max(st) if st else None))
n = max(1, len(A)); sh = lambda R, f: round(sum(1 for r in R if f(r)) / max(1, len(R)), 3); As = [r for r in A if r["far_stress"] is not None]
out = dict(A=dict(kept_songs=songs, songs_with_a_leap=round(with_leap / songs, 3), leaps=len(A), per_1000_notes=round(1000 * len(A) / notes, 2), far_note_is_the_songs_top=sh(A, lambda r: r["far_top"]), in_a_pair=sh(A, lambda r: r["pair"]),
                  far_note_stressed=sh(As, lambda r: r["far_stress"]), by_place=dict(collections.Counter(r["where"] for r in A)), by_part=dict(collections.Counter(r["sec"] for r in A)), far_median_length=sorted(r["far_dur"] for r in A)[len(A) // 2]),
           B=dict(title_lines=tl, cases=len(B), cases_in_100_title_lines=round(100 * len(B) / max(1, tl), 1), function_word=sh(B, lambda r: r["function_word"]), first_note_of_the_line=sh(B, lambda r: r["first"]), before_the_widest_gap=sh(B, lambda r: r["before_widest_gap"]),
                  longest_stressed_shorter_by_3=sh(B, lambda r: r["short_by"] is not None and r["short_by"] <= 3), by_6=sh(B, lambda r: r["short_by"] is not None and 3 < r["short_by"] <= 6), by_more=sh(B, lambda r: r["short_by"] is not None and r["short_by"] > 6),
                  mean_length_by_kind_title_lines={k: round(sum(v) / len(v), 1) for k, v in LEN.items()}, mean_length_by_kind_all_lines={k: round(sum(v) / len(v), 1) for k, v in ALL.items()}))
json.dump(out, open(os.path.join(HERE, "kept.json"), "w"), indent=1); print(json.dumps(out, indent=1))
