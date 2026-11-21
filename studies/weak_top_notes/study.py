"""749.141: the share of a song's top-note occurrences on weak syllables, kept songs and Luthier's. See PREDICTION.md. python3 studies/weak_top_notes/study.py -> result.json"""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import kept_corpus as KC, make_kept_word_weight as MW
kept = []; tops = []
for k in KC.kept_songs():
    tr, _ = MW.tiers(k["words"]); p = k["p"]
    if len(tr) != len(p): continue
    at = [tr[i] for i in range(len(p)) if p[i] == max(p) and tr[i] is not None]
    if at: kept.append(float(np.mean([x < 2 for x in at]))); tops.append(len(at))
q = [round(float(x), 3) for x in np.percentile(kept, (10, 25, 50, 75, 90))]
out = dict(kept=dict(songs=len(kept), p10_25_50_75_90=q, top_note_occurrences_quartiles=[float(x) for x in np.percentile(tops, (25, 50, 75))]), songs={})
for tag, path in (("55", "songs/p65/lyric55.song.json"), ("54", "songs/p64/lyric54.song.json"), ("58", "songs/p68/lyric58.song.json"), ("60", "songs/p70/lyric60.v44.song.json"), ("59", "songs/p69/lyric59.song.json")):
    ns = [n for n in json.load(open(os.path.join(ROOT, path)))["melody"]["notes"] if n.get("melisma") != "second"]; top = max(n["midi"] for n in ns); at = [n for n in ns if n["midi"] == top]
    out["songs"][tag] = dict(top_notes=len(at), on_weak=sum(not n["stress"] for n in at), share=round(float(np.mean([not n["stress"] for n in at])), 3), over_the_kept_90th=bool(np.mean([not n["stress"] for n in at]) > q[4]), weak_words=sorted({n["text"] for n in at if not n["stress"]}))
n_over = sum(out["songs"][t]["over_the_kept_90th"] for t in ("55", "54", "58", "60")); out["over_of_four"] = n_over
out["verdict"] = "the engine's: plant on stressed syllables only, to be tried" if n_over >= 2 else "not the engine's as a body; nothing built"
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1)
