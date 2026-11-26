"""749.216 (a trial, studies/borrow_kept): the kept moves across a join, from a line's last note to the next line's first within one section, in semitones (12 and -12 hold an octave or more), by part.
    python3 lib/luthier/make_kept_line_join.py   -> tables/kept_line_join.json"""
import os, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, "..", "carol"), os.path.join(HERE, "..", "..", "tables", "metre_atlas")]
import kept_corpus as KC
from make_kept_line_repeat import kind
if __name__ == "__main__":
    C = collections.defaultdict(collections.Counter); songs = 0
    for k in KC.kept_songs():
        songs += 1; lines = []; cur = None
        for i, (l, s) in enumerate(zip(k["lines"], k["sec"])):
            if (str(s), l) != cur: cur = (str(s), l); lines.append((str(s), []))
            lines[-1][1].append(int(k["p"][i]))
        for (s1, l1), (s2, l2) in zip(lines, lines[1:]):
            if s1 == s2:
                d = max(-12, min(12, l2[0] - l1[-1]))
                for part in (kind(s1), "all"): C[part][d] += 1
    T = dict(note="749.216, a trial: counts of the move from a line's last note to the next line's first, within one section, kept 4/4 songs; semitones, 12 and -12 an octave or more. 'other' is every part that is neither a verse nor a chorus.", songs=songs, joins={p: sum(c.values()) for p, c in C.items()}, moves={p: {str(d): c[d] for d in range(-12, 13)} for p, c in C.items()})
    json.dump(T, open(os.path.join(HERE, "..", "..", "tables", "kept_line_join.json"), "w"), indent=1); print(T["joins"], {d: T["moves"]["Verse"][str(d)] for d in (-12, -7, -5, -2, 0, 2, 5, 7, 12)})
