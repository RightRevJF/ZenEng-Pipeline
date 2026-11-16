"""749.24/749.25 trace: wrap line_rhythm, record every call's line, syllables, earliest start, latest last onset and slot end, and whether it
returned a rhythm; then build N control builds at the run's seed and calibration, and report the failing calls by line."""
import sys, io, contextlib, random, collections, pickle
N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
sys.argv = ["x", "1", "ctl"]; sys.path[:0] = ["/home/claude/p65"]
with contextlib.redirect_stdout(io.StringIO()): import melody_l7_p65 as P
LOG = []
_lr = P.line_rhythm
def wrapped(sy, rng, tmin, sec, last_max=None, *a, **kw):
    r = _lr(sy, rng, tmin, sec, last_max, *a, **kw)
    i = kw.get("i"); se = P.slot_end(sec, i) if i is not None else None; U = P.line_start(sec, i) if i is not None else None
    LOG.append(dict(sec=sec, i=i, n=len(sy), tmin=tmin, last_max=last_max, U=U, se=se, ok=r is not None, kw=tuple(sorted(k for k, v in kw.items() if v not in (None, False)))))
    return r
P.line_rhythm = wrapped
D = pickle.load(open("/home/claude/p65/runl7/melody_l7_p65_ctl.pkl", "rb"))
for _p in ("V", "C"): P.KNOBS[_p].update(D["knobs"][_p])
P.LK.update(D["line_knobs"])
rng = random.Random(P.__dict__.get("SEED", 20261113 + 455))
deaths = collections.Counter(); fails = collections.defaultdict(list); oks = collections.defaultdict(list)
with contextlib.redirect_stdout(io.StringIO()):
    for b in range(N):
        LOG.clear(); c, err = P.generate(rng)
        for r in LOG:
            (oks if r["ok"] else fails)[(r["sec"], r["i"])].append(r)
        if err: deaths[(err, str(P.WHERE))] += 1
def room(r):
    """the window the line has: from its earliest start to its latest last onset (or slot end), in eighths, relative to the slot."""
    hi = r["last_max"] if r["last_max"] is not None else r["se"]
    return ((r["tmin"] or 0) / 6, (hi - r["U"]) / 6 if (hi is not None and r["U"] is not None) else None)
print("deaths:", deaths.most_common(12))
for k in sorted(fails, key=lambda k: -len(fails[k]))[:10]:
    f = fails[k]; o = oks.get(k, [])
    import statistics as st
    print(f"{k}: {len(f)} failed calls, {len(o)} ok; syllables {f[0]['n']}; kw {collections.Counter(x['kw'] for x in f).most_common(2)}")
    print("   failed: earliest start (eighths) median", st.median([room(x)[0] for x in f]), "latest last onset (eighths into slot) median", st.median([room(x)[1] for x in f if room(x)[1] is not None] or [0]))
    if o: print("   ok:     earliest start median", st.median([room(x)[0] for x in o]), "latest last onset median", st.median([room(x)[1] for x in o if room(x)[1] is not None] or [0]))
