"""Q2: song 55's page floor. Which parts put the 7 passed-over builds under the floor, and what the floor does with range and leaps out of the mean (floor refit on the kept tunes)."""
# Review 19 (Luthier v32). Run from the repo root with PYTHONHASHSEED=0.
import sys, os, json, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier")); sys.argv = sys.argv[:1]
import song_from_lyric as SL, metre_engine as M, page_gate as PG
T = PG.table(); P = PG.PLAIN; seen = []
orig = PG.read
def rec_read(p, d, T_=None):
    r = orig(p, d, T_); seen.append(r); return r
PG.read = rec_read
out = {}
for tag, lp in (("55", "songs/p65/lyric55.json"), ("54", "songs/p64/lyric54.json"), ("58", "songs/p68/lyric58.json")):
    del seen[:]; L = json.load(open(os.path.join(ROOT, lp)))
    res = SL.write(L, 1000, 12)
    rows = list(seen)
    z = lambda r, c: P[c] * (r[c] - T["mean"][c]) / T["sd"][c]
    kv = T["kept_values"]; nk = len(kv["range"])
    def kept_plain(drop): return [float(np.mean([P[c] * (kv[c][j] - T["mean"][c]) / T["sd"][c] for c in P if c not in drop])) for j in range(nk)] if all(c in kv for c in P) else None
    o = dict(read=len(rows))
    for drop in ((), ("range", "leaps")):
        kp = kept_plain(drop); fl = float(np.percentile(kp, 10)) if kp else None
        pl = [float(np.mean([z(r, c) for c in P if c not in drop])) for r in rows]
        o["drop " + ("+".join(drop) or "none")] = dict(floor=round(fl, 3), passed_over=int(sum(x < fl for x in pl)), first_passing_index=next((j for j, x in enumerate(pl) if x >= fl), None))
    under = [r for r in rows if r["plainness"] < T["floor"]["plainness"]]
    o["passed_over_mean_part_z"] = {c: round(float(np.mean([z(r, c) for r in under])), 2) for c in P} if under else {}
    o["all_read_mean_part_z"] = {c: round(float(np.mean([z(r, c) for r in rows])), 2) for c in P}
    out[tag] = o; print(tag, json.dumps(o), flush=True)
json.dump(out, open(os.path.join(ROOT, "studies", "review19", "floor.json"), "w"), indent=1)
