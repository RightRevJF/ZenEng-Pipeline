"""PREDICTION_again.md: what 'sing it again' changes when 818 fires.  python3 again_read.py"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "line_repeats")]
import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
from read import deg, repeat
sys.path.insert(0, os.path.join(ROOT, "lib", "luthier")); from make_kept_line_repeat import repeat3
def steps(E, on, ps, U, sec, i):
    """the pitch loop of again(), replayed on the source's own notes: which step moves each note"""
    mu, lo, hi = E.reg(sec, i); c = collections.Counter()
    for j_, (t, p) in enumerate(zip(on, ps)):
        ch = E.chord_at(U + t); long_ = j_ == len(on) - 1 or on[j_ + 1] - t >= E.BEAT; p0 = p
        if E.S.get("clash_rule") and long_ and p % 12 not in ch and ((p + 1) % 12 in ch or (p - 1) % 12 in ch):
            p = min((p + d for d in (-1, 1, -2, 2, -3, 3, -4, 4) if (p + d) % 12 in E.SCALE and (p + d) % 12 in ch and lo <= p + d <= hi), key=lambda q_: abs(q_ - p), default=p)
        if p != p0: c["the clash rule"] += 1; continue
        if "chord_tie" not in E.S and E.on_beat(U + t) and p % 12 not in ch: p = min((p + d for d in (-1, 1, -2, 2) if (p + d) % 12 in E.SCALE and (p + d) % 12 in ch), key=lambda q_: abs(q_ - p), default=p)
        if p != p0: c["the chord on the beat"] += 1; continue
        if p > hi or p < lo: c["the register"] += 1
    return c
out = {}; TOT = {"all": collections.Counter(), "Verse": collections.Counter()}
for name, stem in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59")):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); spec = json.load(open(os.path.join(ROOT, stem + ".song.json")))["spec"]; E = M.Engine(spec); scale = sorted(spec["scale"]); R = {"all": collections.Counter(), "Verse": collections.Counter()}
    last = {}; a0, j0 = E.again, E.join
    def again(rng, src, src_st0, sy, U, sec, i, tmin, slot):
        r = a0(rng, src, src_st0, sy, U, sec, i, tmin, slot)
        if E.HOW.get((sec, i), ["fresh"])[0] == "fresh": last.clear(); last.update(src=list(src), r=r, n=len(sy), U=U, sec=sec, i=i, joined="not reached"); E._log.append(last.copy()) if r is None else None
        return r
    def join(r, lines, k, sec, i):
        r2 = j0(r, lines, k, sec, i)
        if last and r is last.get("r") and last.get("joined") == "not reached": d = dict(last); d["joined"] = r2; E._log.append(d); last["joined"] = "done"
        return r2
    E.again, E.join = again, join; rng = random.Random(L.get("seed", 1))
    for _ in range(300):
        E._log = []; c, err = E.build(rng)
        if err or E.gates(c): continue
        for d in E._log:
            for grp in ("all", CP.kind(d["sec"])):
                if grp not in R: continue
                C = R[grp]; C["818 fires"] += 1
                if d["r"] is None or d["joined"] is None or d["joined"] == "not reached": C["fails, drawn fresh"] += 1; continue      # 'not reached': the line failed its slot tests before the join
                C["kept"] += 1; src = d["src"]; res = d["joined"]; rep = repeat([deg(p, 0, scale) for _, p in src], [deg(p, 0, scale) for _, p in res]) is not None; C["kept and a repeat"] += rep; rep3 = repeat3([deg(p, 0, scale) for _, p in src], [deg(p, 0, scale) for _, p in res]) is not None; C["kept and a repeat by the best of three alignments"] += rep3; C["the count differs and a repeat by the best of three"] += rep3 and d["n"] != len(src)
                if d["n"] != len(src): cause = "A the count differs"; C["A by one"] += abs(d["n"] - len(src)) == 1; C["A by one, a repeat"] += rep and abs(d["n"] - len(src)) == 1
                elif [t for t, _ in res] != [t for t, _ in src]: cause = "B the same count, onsets re-fitted"
                elif [p for _, p in res] != [p for _, p in src]:
                    st = steps(E, [t for t, _ in src], [p for _, p in src], d["U"], d["sec"], d["i"])
                    if res[0][1] != d["r"][0][1]: st["the join"] += 1
                    cause = "C pitches changed: " + (st.most_common(1)[0][0] if st else "other")
                else: cause = "D unchanged"
                C[cause] += 1; C[cause + ", a repeat"] += rep
                if not rep: C["not a repeat: " + cause] += 1
    out[name] = {g: dict(v) for g, v in R.items()}
    for g in R: TOT[g].update(R[g])
    nr = R["all"]["kept"] - R["all"]["kept and a repeat"]; print(name, {k: v for k, v in sorted(R["all"].items()) if not k.startswith("not")}, "| of the non-repeats:", {k[14:]: round(v / max(1, nr), 2) for k, v in R["all"].items() if k.startswith("not a repeat")}, flush=True)
out["six songs"] = {g: dict(v) for g, v in TOT.items()}; json.dump(out, open(os.path.join(HERE, "again_read.json"), "w"), indent=1)
for g in TOT: nr = TOT[g]["kept"] - TOT[g]["kept and a repeat"]; print("SIX", g, dict(fires=TOT[g]["818 fires"], fails=TOT[g]["fails, drawn fresh"], kept=TOT[g]["kept"], repeats=TOT[g]["kept and a repeat"], repeats3=TOT[g]["kept and a repeat by the best of three alignments"], A=TOT[g]["A the count differs"], A_rep=TOT[g]["A the count differs, a repeat"], A_rep3=TOT[g]["the count differs and a repeat by the best of three"], A1=TOT[g]["A by one"], A1_rep=TOT[g]["A by one, a repeat"], D=TOT[g]["D unchanged"]), {k[14:]: round(v / max(1, nr), 3) for k, v in TOT[g].items() if k.startswith("not a repeat")})
