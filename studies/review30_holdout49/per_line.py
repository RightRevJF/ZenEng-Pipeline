"""Review 30: where song 49's words' fit fell under 958. The engine's own fit (lib/luthier/word_weight.py), read line by line on the two
chosen tunes (lyric49.without_958.song.json and lyric49.song.json): the verse lines 958 named (one bar), the other verse lines, and the
rest of the song. A line's fit is a rank correlation over 8 or 9 notes, so each is rough; the means are what is read.
    python3 studies/review30_holdout49/per_line.py -> per_line.json"""
import json, os, sys, collections
import numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import word_weight as W
NAMED = json.load(open(os.path.join(ROOT, "songs/p59/lyric49.song.json")))["spec"]["verse_closer"]["lines_given_one_bar"]
out = {}
for tag, f in (("without", "songs/p59/lyric49.without_958.song.json"), ("with", "songs/p59/lyric49.song.json")):
    R = json.load(open(os.path.join(ROOT, f))); ns = R["melody"]["notes"]; G = collections.OrderedDict()
    for n in ns: G.setdefault((n["sec"], n["line"]), []).append(n)
    grp = collections.defaultdict(list)
    for (sec, ln), g in G.items():
        k = "verse lines named" if sec in NAMED and ln in NAMED[sec] else "other verse lines" if sec.startswith("Verse") else "the rest of the song"
        grp[k].append(W.fit(g))
    out[tag] = dict(whole=round(W.fit(ns), 3), parts={k: round(v, 3) for k, v in W.fit(ns, parts=True).items()},
                    mean_line_fit={k: dict(lines=len(v), mean=round(float(np.mean(v)), 3)) for k, v in grp.items()})
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "per_line.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
