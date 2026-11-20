"""Traces for the v35 list. (a) 749.114: which lines fail in song 59's rhythm draw. (b) 749.113: where repeated notes are made: fresh lines, returning lines, joins.
python3 studies/v35_traces/trace.py [N] -> trace.json"""
import sys, os, json, random, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", ".."); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier")); N = int(sys.argv[1]) if len(sys.argv) > 1 else 150
import metre_engine as M
REC = {"55": "songs/p65/lyric55", "54": "songs/p64/lyric54", "58": "songs/p68/lyric58", "59": "songs/p69/lyric59"}; out = {}
for tag, p in REC.items():
    R = json.load(open(os.path.join(ROOT, p + ".song.json"))); spec = R["spec"]; E = M.Engine(spec); fresh = {}; orig = E.pitches
    def rec_p(rng, ons, U, sec, i, prev, avoid=None, end_off=None, orig=orig, fresh=fresh):
        ps = orig(rng, ons, U, sec, i, prev, avoid=avoid, end_off=end_off); fresh[(sec, i)] = ps; return ps
    E.pitches = rec_p; rng = random.Random(9); fails = collections.Counter(); rows = []
    for _ in range(N):
        fresh.clear(); c, err = E.build(rng)
        if err: fails[f"{err[0]} | {err[1]} line {err[2] + 1}: {len(E.LINES[err[1]][err[2]])} syllables, slot {E.slot_len(err[1], err[2]) / E.BAR:g} bars" if len(err) > 2 else str(err[0])] += 1; continue
        if E.gates(c): continue
        by = collections.OrderedDict()
        for n in c["notes"]: by.setdefault((n["sec"], n["line"]), []).append(n["p"])
        fr = [v for k, v in by.items() if fresh.get(k) == v]; ot = [v for k, v in by.items() if fresh.get(k) != v]; ks = list(by.values())
        rep = lambda ls: [b == a for v in ls for a, b in zip(v, v[1:])]; jo = [b[0] == a[-1] for a, b in zip(ks, ks[1:])]; al = [n["p"] for n in c["notes"]]
        rows.append(dict(whole=float(np.mean([b == a for a, b in zip(al, al[1:])])), fresh_lines=float(np.mean(rep(fr))) if rep(fr) else np.nan, returning_lines=float(np.mean(rep(ot))) if rep(ot) else np.nan, joins=float(np.mean(jo)),
                         notes_in_fresh_lines=sum(map(len, fr)) / len(al), joins_share_of_moves=len(jo) / (len(al) - 1)))
    out[tag] = dict(aim_repeated_notes=spec["target"]["readings"]["repeated notes"], builds=len(rows), tries=N, rhythm_and_other_failures=dict(fails.most_common(12)), repeated_notes={k: round(float(np.nanmedian([r[k] for r in rows])), 3) for k in rows[0]} if rows else None)
    print(tag, json.dumps(out[tag]), flush=True)
json.dump(out, open(os.path.join(HERE, "trace.json"), "w"), indent=1)
