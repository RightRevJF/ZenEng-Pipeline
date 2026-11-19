"""Trace 882 on the pick of a song: every 'again' call (712 lines and 818 borrows) of the picked build, with what changed against its source."""
import sys, os, json, runpy
sys.path.insert(0, "/home/claude/zeneng-pipeline/lib/luthier"); os.chdir("/home/claude/zeneng-pipeline")
import metre_engine as M
E = M.Engine; orig_again, orig_build, orig_run = E.again, E.build, E.run; ST = dict(k=-1, log={}, runs=[])
def again(self, rng, src, src_st0, sy, U, sec, i, tmin, slot):
    out = orig_again(self, rng, src, src_st0, sy, U, sec, i, tmin, slot)
    ST["log"].setdefault(ST["k"], []).append(dict(sec=sec, i=i, src=[list(x) for x in src], words=[w for w, _ in sy], stress=[s for _, s in sy], out=[list(x) for x in out] if out else None, tmin=tmin, slot=slot))
    return out
def build(self, rng):
    ST["k"] += 1; return orig_build(self, rng)
def run(self, N, seed):
    ST["k"] = -1; ST["log"] = {}; res = orig_run(self, N, seed)
    pick = res.get("pick"); ST["runs"].append(dict(pick=pick, res_keys=list(res.keys()), logs=ST["log"]))
    return res
E.again, E.build, E.run = again, build, run
song = sys.argv[1]; sys.argv = ["song_from_lyric.py"] + sys.argv[1:]
try: runpy.run_path("lib/luthier/song_from_lyric.py", run_name="__main__")
finally:
    json.dump([dict(pick=r["pick"], logs=r["logs"]) for r in ST["runs"]], open("/tmp/rev/trace882_" + os.path.basename(song).split(".")[0] + ".json", "w"))
