"""749.177: where a kept title line's longest note falls. See PREDICTION.md, section 2. Writes title_lines.json (counts only)."""
import os, sys, re, json, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); L = os.path.normpath(os.path.join(HERE, "..", "..", "lib", "luthier")); sys.path[:0] = [L, os.path.join(L, "..", "carol")]
import kept_corpus as KC, make_kept_word_weight as MK
CATS = ["stressed", "weak, the line's last syllable", "weak, in the last word but not its last syllable", "weak, before the last word"]
norm = lambda w: re.sub(r"[^a-z]", "", w.lower()); by_line = collections.Counter(); by_song = []; songs = 0; left_out = 0
for k in KC.kept_songs():
    title = [norm(x) for x in re.findall(r"[A-Z][a-z']*|\d+", k["song"].split("_")[1])]; title = [x for x in title if x]
    tr, wid = MK.tiers(k["words"])
    if len(tr) != len(k["t"]) or not title: continue
    ws = [norm(w) for w, _ in k["words"]]; lines = collections.defaultdict(list)
    for i, l in enumerate(k["lines"]): lines[l].append(i)
    own = collections.Counter()
    for l, idx in lines.items():
        lw = []
        for i in idx:
            if not lw or lw[-1] != wid[i]: lw.append(wid[i])
        seq = [ws[q] for q in lw]
        if not any(seq[j:j + len(title)] == title for j in range(len(seq) - len(title) + 1)): continue
        if any(tr[i] is None for i in idx): left_out += 1; continue
        top = max(idx, key=lambda i: k["dur"][i]); c = 0 if tr[top] == 2 else 1 if top == idx[-1] else 2 if wid[top] == wid[idx[-1]] else 3; by_line[CATS[c]] += 1; own[c] += 1
    if own: songs += 1; n = sum(own.values()); by_song.append([own[c] / n for c in range(4)])
n = sum(by_line.values()); out = dict(kept_songs_with_a_title_line=songs, title_lines=n, lines_left_out_for_a_word_not_in_the_lexicon=left_out, by_line={c: round(by_line[c] / n, 3) for c in CATS},
    by_song_mean={c: round(st.mean(r[i] for r in by_song), 3) for i, c in enumerate(CATS)}, songs_with_any_weak_before_the_last_word=round(sum(r[3] > 0 for r in by_song) / songs, 3))
json.dump(out, open(os.path.join(HERE, "title_lines.json"), "w"), indent=1); print(json.dumps(out, indent=1))
