"""Stressed syllables a sixteenth long (onset to the next onset 3 twelfths or less), in lines sung again and in the other lines, at two commits.
python3 lib/luthier/review9_stressed16.py 1ffe2e6,59e473c songs/p64/lyric54.song.json ..."""
import json, subprocess, collections, sys
for path in sys.argv[2:]:
    for rev in sys.argv[1].split(","):
        R = json.loads(subprocess.check_output(["git", "show", f"{rev}:{path}"])); how = R["spec"]["how"]; L = collections.defaultdict(list)
        for n in sorted(R["melody"]["notes"], key=lambda n: n["on"]): L[(n["sec"], n["line"])].append(n)
        out = {}
        for grp in ("again", "other"):
            st = short = 0
            for (s, i), ns in L.items():
                h = how.get(f"{s}:{i}"); g = "again" if isinstance(h, list) and h[0] == "again" else "other"
                if g != grp: continue
                for a, b in zip(ns, ns[1:]):
                    if a["stress"] and a["text"]: st += 1; short += (b["on"] - a["on"]) <= 3
            out[grp] = f"{short}/{st}"
        print(path.split("/")[-1], rev, out)
