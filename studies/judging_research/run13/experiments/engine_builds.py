"""(Make the worktree first: git worktree add --detach /home/claude/mainro origin/main.) Collect survivor melodies from the committed Luthier metre engine (read-only use of a main worktree; the engine is not changed).
Usage: python3 engine_builds.py <song.json> <N> <seed> <out.json>"""
import sys, os, json, random
ROOT = os.environ.get("MAIN_WORKTREE", "/home/claude/mainro"); os.chdir(ROOT); sys.path.insert(0, os.path.join(ROOT, "lib/luthier"))
import metre_engine as M
p, N, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
d = json.load(open(p)); spec = d["spec"]
E = M.Engine(spec); rng = random.Random(seed); keep = []; dead = 0
for k in range(N):
    c, err = E.build(rng)
    if err: dead += 1; continue
    if E.gates(c): dead += 1; continue
    keep.append([[n["on"], n["p"], n.get("dur"), n["sec"], n["line"], int(bool(n.get("stress")))] for n in c["notes"]])
json.dump(dict(song=p, metre=d["metre"], bpm=d["bpm"], key=d["key"], BAR=getattr(E, "BAR", None), BEAT=getattr(E, "BEAT", None), made=N, dead=dead, builds=keep,
               pick=[[n["on"], n["p"], n.get("dur"), n["sec"], n["line"]] for n in (d["melody"]["pick"]["notes"] if isinstance(d["melody"].get("pick"), dict) and "notes" in d["melody"]["pick"] else [])]), open(out, "w"))
print(p, "survivors", len(keep), "dead", dead, "BAR", getattr(E, "BAR", None), "BEAT", getattr(E, "BEAT", None))
