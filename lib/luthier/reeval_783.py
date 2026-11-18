"""783 check: re-evaluate every clean survivor (no cause, no soft break) of a stored l11 run from its 8-field notes.
    python3 lib/luthier/reeval_783.py p67 review     (reads runl11/melody_l11_p67_mainreview.pkl)"""
import sys, pickle, copy, io, contextlib, collections, importlib
song = sys.argv[1]; tag = sys.argv[2]
sys.argv = ["x", "1", "main"]; sys.path[:0] = [f"/home/claude/{song}"]
with contextlib.redirect_stdout(io.StringIO()): P = importlib.import_module(f"melody_l11_{song}")
D = pickle.load(open(f"/home/claude/{song}/runl11/melody_l11_{song}_main{tag}.pkl", "rb"))
for _p in ("V", "C"): P.KNOBS[_p].update(D["knobs"][_p])
P.LK.update(D["line_knobs"])
def rebuild(b):
    ns = []; last = {}
    for o, d, p, s, l, st, sy, mv in b["notes"]:
        sl = last.get(l) == sy and sy is not None; last[l] = sy
        n = dict(on=o, p=p, syl=sy, slur=sl, stress=st, dur=d, sec=s, line=l)
        if mv is not None: n["moved386"] = mv
        ns.append(n)
    return dict(notes=ns, meta=b["meta"], judge=b["judge"], info=b["info"], read=b["read"], lines=b["lines"], fp=b["fp"])
clean = [b for b in D["all"] if b.get("cause") is None and not b["info"]["soft"]]
c = collections.Counter()
for b in clean: r = P.evaluate(rebuild(b))[0]; c[r[0] if r else "passes"] += 1
print(song, "clean survivors", len(clean), "| re-evaluated from the stored record:", dict(c), "| with a 386 move:", sum(1 for b in clean if any(n[7] is not None for n in b["notes"])))
