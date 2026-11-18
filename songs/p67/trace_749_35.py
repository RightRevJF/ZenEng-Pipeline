"""749.35: re-evaluates the clean survivors of the trace run (melody_l8_p67_trace.py: song 57 on v8 storing every note field with each note) three ways: notes bare as the run stores them, with moved386 restored, and with every field restored. Usage: PYTHONHASHSEED=0 python3 melody_l8_p67_trace.py 1000 main trace2; python3 trace_749_35.py"""
import sys, pickle, copy, io, contextlib, collections
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p67"]
with contextlib.redirect_stdout(io.StringIO()): import melody_l8_p67 as P
D = pickle.load(open("/home/claude/p67/runl8/melody_l8_p67_maintrace2.pkl", "rb"))
for _p in ("V", "C"): P.KNOBS[_p].update(D["knobs"][_p])
P.LK.update(D["line_knobs"])
def rebuild(b, mode):
    ns = []; last = {}
    for o, d, p, s, l, st, sy, ex in b["notes"]:
        sl = last.get(l) == sy and sy is not None; last[l] = sy
        n = dict(on=o, p=p, syl=sy, slur=sl, stress=st, dur=d, sec=s, line=l)
        if mode == "full": n.update(ex)
        elif mode == "moved": 
            if "moved386" in ex: n["moved386"] = ex["moved386"]
        ns.append(n)
    return dict(notes=ns, meta=b["meta"], judge=b["judge"], info=b["info"], read=b["read"], lines=b["lines"], fp=b["fp"])
clean = [b for b in D["all"] if not b["info"]["soft"]]                                   # as the first reading took them: includes the builds evaluate killed
print("of which killed by evaluate in the run:", sum(1 for b in clean if b.get("cause")))
keys = collections.Counter(k for b in clean for n in b["notes"] for k in n[7]); print("extra note keys:", dict(keys))
for mode in ("bare", "moved", "full"):
    c = collections.Counter()
    for b in clean: r = P.evaluate(rebuild(b, mode))[0]; c[r[0] if r else "passes"] += 1
    print(mode, len(clean), dict(c))
