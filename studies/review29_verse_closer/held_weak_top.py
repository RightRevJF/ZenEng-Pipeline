"""Review 29: how long a weak syllable is held on a song's top note, kept songs (CoCoPops durations, 12 to a beat) against Luthier's records.  python3 studies/review29_verse_closer/held_weak_top.py"""
import sys, os, json, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); os.chdir(ROOT); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import kept_corpus as KC, make_kept_word_weight as MW
ks = list(KC.kept_songs()); print("kept dur sample", ks[0]["dur"][:12])
held = []; n = 0
for k in ks:
    tr, _ = MW.tiers(k["words"]); p = k["p"]
    if len(tr) != len(p): continue
    top = max(p); w = [k["dur"][i] for i in range(len(p)) if p[i] == top and tr[i] is not None and tr[i] < 2]
    held.append(max(w) if w else 0.0); n += 1
held = np.array(held, float)
print("kept songs", n, "longest weak top note in beats (12 a beat), 50/75/90/95/99th", np.percentile(held, (50, 75, 90, 95, 99)) / 12, "share >= 1 beat", round(float(np.mean(held >= 12)), 3), ">= 2 beats", round(float(np.mean(held >= 24)), 3), ">= 4 beats", round(float(np.mean(held >= 48)), 3))
for tag, path in (("55", "songs/p65/lyric55.song.json"), ("54", "songs/p64/lyric54.song.json"), ("58", "songs/p68/lyric58.song.json"), ("60", "songs/p70/lyric60.v44.song.json"), ("59", "songs/p69/lyric59.song.json")):
    R = json.load(open(path)); beat = R["bar"] / R["beats"] if isinstance(R.get("beats"), int) else R["bar"] / 4
    ns = [x for x in R["melody"]["notes"] if x.get("melisma") != "second"]; top = max(x["midi"] for x in ns)
    w = [x["dur"] / beat for x in ns if x["midi"] == top and not x["stress"]]
    print(tag, "longest weak top note, beats", max(w) if w else 0, [(x["text"], round(x["dur"]/beat, 2)) for x in ns if x["midi"] == top and not x["stress"]])
