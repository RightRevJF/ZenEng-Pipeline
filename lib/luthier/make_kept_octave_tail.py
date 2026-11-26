"""749.192: the maker of tables/kept_octave_tail.json. The kept interval table (tables/metre_atlas/4-4_pop_sung.json) counts every interval of an octave or more in its
+12 and -12 bins. This table says how those bins divide in the kept songs: the octave itself, and everything past it.
    python3 lib/luthier/make_kept_octave_tail.py        # needs the kept corpus (lib/luthier/kept_corpus.py)"""
import os, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kept_corpus as KC
def table(): return json.load(open(os.path.join(HERE, "..", "..", "tables", "kept_octave_tail.json")))
if __name__ == "__main__":
    C = {"up": collections.Counter(), "down": collections.Counter()}; n = 0; songs = 0
    for k in KC.kept_songs():
        songs += 1; p = k["p"]
        for a, b in zip(p, p[1:]):
            d = int(b) - int(a); n += 1
            if abs(d) >= 12: C["up" if d > 0 else "down"]["octave" if abs(d) == 12 else "past"] += 1
    out = dict(source="kept songs, 4/4 (kept_corpus.kept_songs()): every pair of consecutive sung notes, within lines and across them", kept_songs=songs, intervals=n,
               up=dict(octave=C["up"]["octave"], past=C["up"]["past"], octave_share=round(C["up"]["octave"] / max(1, sum(C["up"].values())), 3)),
               down=dict(octave=C["down"]["octave"], past=C["down"]["past"], octave_share=round(C["down"]["octave"] / max(1, sum(C["down"].values())), 3)))
    json.dump(out, open(os.path.join(HERE, "..", "..", "tables", "kept_octave_tail.json"), "w"), indent=1); print(json.dumps(out))
